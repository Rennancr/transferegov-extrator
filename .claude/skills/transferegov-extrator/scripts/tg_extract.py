#!/usr/bin/env python3
"""
Extrator das APIs de Dados Abertos do TransfereGov para Excel/CSV.

As APIs são FastAPI (OpenAPI 3.1 em /<modulo>/openapi.json). Tabelas, colunas, tipos, filtros e
tamanho máximo de página são lidos do OpenAPI em tempo de execução; nada é fixo no código.

Subcomandos:
  tabelas  --modulo M                            lista as tabelas (endpoints) do módulo
  colunas  --modulo M --tabela T                 colunas (tipo, PK) e filtros aceitos
  contar   --modulo M --tabela T [-f ...]        conta linhas sem baixar
  extrair  --modulo M --tabela T [--tabela T2 ...] [-f ...] [--formato xlsx|csv]
           [--saida PASTA] [--arquivo NOME] [--juntar CHAVE] [--so-se-atualizou] [--estrito]

Junção: --juntar id_beneficiario com 2+ tabelas → aba 'juntado' (só linhas com par em todas) + uma aba por
tabela, restrita às chaves que casaram.
Rotina agendada: --arquivo fixo + --so-se-atualizou → não baixa nada se a base (data-atualizacao) e os
parâmetros não mudaram desde a execução anterior; o arquivo existente é mantido.

Módulos: especiais (emendas Pix), fundoafundo, ted, parcerias.

Filtros: -f coluna=valor (repetível)
  - texto: a API busca "contém", sem diferenciar maiúsculas;
  - inteiro, número, data (AAAA-MM-DD) e listas fechadas (ex.: UF): igualdade;
  - mesmo filtro repetido = OU (-f uf_beneficiario=SP -f uf_beneficiario=RJ → uma consulta por valor);
  - filtros diferentes = E;
  - com várias tabelas, prefixe para restringir: -f beneficiarios-especiais:uf_beneficiario=SP
  - faixas: -f "ano_plano_acao>=2023" -f "ano_plano_acao<=2025" (também > e <), em colunas numéricas ou de data.
    A API não tem faixa. Inteiro com início e fim (até 50 valores), em coluna que é filtro da API, vira uma
    consulta por valor (exato). As demais faixas são aplicadas localmente depois do download; `contar`
    informa o volume que será baixado. Nulos ficam fora da faixa. Em coluna data-hora, um limite só com
    a data vale para o dia inteiro.
  Não há OU entre colunas diferentes nem "diferente de".

Saída: caminho do(s) arquivo(s) no stdout; progresso e avisos no stderr.
Códigos de saída: 0 ok | 1 erro | 2 uso incorreto | 3 ok com avisos (só com --estrito).
"""
from __future__ import annotations

import argparse
import csv
import difflib
import io
import itertools
import json
import math
import os
import re
import sys
import tempfile
import time
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

import pandas as pd
import requests

VERSAO = "1.1.0"
BASE = "https://api-publica.transferegov.gestao.gov.br"
MODULO_CSV = "discricionarias"      # convênios/contratos de repasse: CSVs em /downloads, sem API
MODULOS = {
    "especiais": "especiais",
    "transferenciasespeciais": "especiais",
    "fundoafundo": "fundoafundo",
    "faf": "fundoafundo",
    "ted": "ted",
    "parcerias": "parcerias",
    MODULO_CSV: MODULO_CSV,
    "convenios": MODULO_CSV,
    "siconv": MODULO_CSV,
    "downloads": MODULO_CSV,
}
DOWNLOADS = f"{BASE}/downloads/dadosgov/"
CACHE_DIR = Path(os.environ.get("TG_CACHE") or Path(tempfile.gettempdir()) / "transferegov-extrator")
CSV_BLOCO = 200_000                 # linhas por bloco ao ler CSV grande (memória controlada)
EXCEL_MAX_ROWS = 1_048_575          # 1.048.576 menos o cabeçalho
EXCEL_MAX_CELULA = 32_767           # limite de caracteres por célula no Excel
TIMEOUT = 120
TENTATIVAS = 5
PAUSA_ENTRE_PAGINAS = 0.2           # segundos; sequencial e educado com a API pública
PAGINA_PADRAO = 50                  # só se o endpoint não declarar `maximum`
MAX_COMBINACOES = 200               # teto de consultas geradas por filtros repetidos
USER_AGENT = f"transferegov-extrator/{VERSAO} (skill Claude; extracao de dados abertos)"
PARAMS_PAGINACAO = ("pagina", "tamanho_da_pagina")

session = requests.Session()
session.headers.update({"Accept": "application/json", "User-Agent": USER_AGENT})


class ErroTG(Exception):
    """Erro com mensagem pronta para o usuário (pt-BR)."""


def _log(msg: str = "", fim: str = "\n") -> None:
    print(msg, file=sys.stderr, end=fim, flush=True)


# ---------- HTTP ----------

def _detalhe(r: requests.Response) -> str:
    """Resume o corpo de erro do FastAPI ({"detail": str | [{loc, msg}]})."""
    try:
        d = r.json().get("detail")
    except (ValueError, AttributeError):
        return r.text[:300]
    if isinstance(d, list):
        return "; ".join(f"{'.'.join(str(x) for x in e.get('loc', [])[1:])}: {e.get('msg')}" for e in d)
    return str(d)


def _get(url: str, params: dict | None = None) -> requests.Response:
    """GET com backoff exponencial em 429/5xx/rede; erro imediato nos demais 4xx."""
    for i in range(TENTATIVAS):
        try:
            r = session.get(url, params=params, timeout=TIMEOUT)
        except (requests.ConnectionError, requests.Timeout) as e:
            motivo, espera = type(e).__name__, 2 ** i
        else:
            if r.status_code < 400:
                return r
            if r.status_code != 429 and r.status_code < 500:
                raise ErroTG(f"HTTP {r.status_code} em {r.url}: {_detalhe(r)}")
            motivo = f"HTTP {r.status_code}"
            ra = r.headers.get("Retry-After", "")
            espera = int(ra) if ra.isdigit() else 2 ** i
        if i == TENTATIVAS - 1:
            raise ErroTG(f"{motivo} em {url} após {TENTATIVAS} tentativas. A API pode estar instável; tente mais tarde.")
        espera = min(espera, 60)
        _log(f"  ! {motivo}; nova tentativa em {espera}s")
        time.sleep(espera)
    raise AssertionError("inalcançável")


# ---------- descoberta (OpenAPI) ----------

_cache_spec: dict[str, dict] = {}


def _modulo(modulo: str) -> str:
    m = MODULOS.get(modulo.lower().strip())
    if not m:
        raise ErroTG(f"Módulo '{modulo}' não existe. Válidos: especiais, fundoafundo, ted, parcerias, "
                     f"{MODULO_CSV} (convênios e contratos de repasse).")
    return m


def spec(modulo: str) -> dict:
    m = _modulo(modulo)
    if m not in _cache_spec:
        _cache_spec[m] = _get(f"{BASE}/{m}/openapi.json").json()
    return _cache_spec[m]


@dataclass
class Coluna:
    nome: str
    tipo: str                       # integer | number | boolean | string | json | misto
    formato: str | None = None      # date | date-time | None
    pk: bool = False
    descricao: str = ""
    origem: tuple[str, str] | None = None   # (coluna_pai, subcampo) quando veio de objeto aninhado


@dataclass
class Filtro:
    nome: str
    tipo: str
    formato: str | None = None
    enum: list | None = None
    pattern: str | None = None
    descricao: str = ""


@dataclass
class Endpoint:
    modulo: str
    tabela: str
    url: str
    colunas: list[Coluna]
    filtros: dict[str, Filtro]
    max_pagina: int

    @property
    def pk(self) -> list[str]:
        return [c.nome for c in self.colunas if c.pk]


def _ref(s: dict, ref: str) -> dict:
    return s["components"]["schemas"][ref.rsplit("/", 1)[-1]]


def _alternativas(p: dict) -> list[dict]:
    """Remove o ramo `null` do anyOf: `anyOf: [{type: integer}, {type: null}]` → [{type: integer}]."""
    return [a for a in p.get("anyOf", [p]) if a.get("type") != "null"]


def _schema_item(s: dict, op: dict | None) -> dict | None:
    """Schema de uma linha de um endpoint paginado; None se o endpoint não devolve {data: [...]}."""
    try:
        env = op["responses"]["200"]["content"]["application/json"]["schema"]
    except (KeyError, TypeError):
        return None
    if "$ref" in env:
        env = _ref(s, env["$ref"])
    data = env.get("properties", {}).get("data")
    if not data or data.get("type") != "array":
        return None
    it = data.get("items", {})
    return _ref(s, it["$ref"]) if "$ref" in it else it


def _tipo(p: dict) -> tuple[str, str | None]:
    alts = _alternativas(p)
    if len(alts) != 1:
        return "misto", None
    a = alts[0]
    if "$ref" in a or a.get("type") in ("array", "object"):
        return "json", None
    if a.get("type") in ("integer", "number", "boolean", "string"):
        return a["type"], a.get("format")
    return "misto", None


def _colunas(s: dict, item: dict) -> list[Coluna]:
    cols: list[Coluna] = []
    for nome, p in item.get("properties", {}).items():
        alts = _alternativas(p)
        pk = bool(p.get("primary_key")) or any(a.get("primary_key") for a in alts)
        # Objeto aninhado ($ref para schema com properties): achata em coluna__subcampo, tipado pelo sub-schema.
        if len(alts) == 1 and "$ref" in alts[0]:
            sub = _ref(s, alts[0]["$ref"])
            if sub.get("properties"):
                for sn, sp in sub["properties"].items():
                    t, f = _tipo(sp)
                    cols.append(Coluna(f"{nome}__{sn}", t, f, descricao=sp.get("title", ""), origem=(nome, sn)))
                continue
        t, f = _tipo(p)
        cols.append(Coluna(nome, t, f, pk, p.get("title", "")))
    return cols


def tabelas(modulo: str) -> list[str]:
    if _modulo(modulo) == MODULO_CSV:
        return sorted(_listagem())
    s = spec(modulo)
    return [p.strip("/") for p, ops in s.get("paths", {}).items() if _schema_item(s, ops.get("get"))]


def endpoint(modulo: str, tabela: str) -> Endpoint:
    if _modulo(modulo) == MODULO_CSV:
        return _endpoint_csv(tabela)
    s, m = spec(modulo), _modulo(modulo)
    t = tabela.strip().strip("/")
    op = s.get("paths", {}).get(f"/{t}", {}).get("get")
    item = _schema_item(s, op)
    if item is None:
        validas = tabelas(modulo)
        parecidas = difflib.get_close_matches(t, validas, n=3, cutoff=0.5)
        dica = f" Você quis dizer: {', '.join(parecidas)}?" if parecidas else ""
        raise ErroTG(f"Tabela '{t}' não existe no módulo '{m}'.{dica}\nTabelas disponíveis: {', '.join(validas)}")

    filtros: dict[str, Filtro] = {}
    max_pagina = PAGINA_PADRAO
    for prm in op.get("parameters", []):
        if prm.get("in") != "query":
            continue
        sch = prm.get("schema", {})
        alts = _alternativas(sch) or [{}]
        a = alts[0]
        if prm["name"] == "tamanho_da_pagina":
            max_pagina = int(a.get("maximum", sch.get("maximum", PAGINA_PADRAO)))
            continue
        if prm["name"] in PARAMS_PAGINACAO:
            continue
        filtros[prm["name"]] = Filtro(prm["name"], a.get("type", "string"), a.get("format"),
                                      a.get("enum") or sch.get("enum"), a.get("pattern"),
                                      prm.get("description") or sch.get("description", ""))
    cols = _colunas(s, item)
    for c in cols:  # descrição útil mora no parâmetro de mesmo nome; o schema de resposta só tem `title`
        if c.nome in filtros and filtros[c.nome].descricao:
            c.descricao = filtros[c.nome].descricao
    return Endpoint(m, t, f"{BASE}/{m}/{t}", cols, filtros, max_pagina)


# ---------- discricionárias: CSVs do /downloads (convênios, contratos de repasse) ----------
#
# Não há OpenAPI. A lista de arquivos vem da listagem pública do container; as colunas, do cabeçalho de cada
# CSV. O modelo oficial (SchemaSpy) declara tudo como varchar, então os tipos seguem a convenção de nomes
# desse modelo, validada nos valores: o que não casa com o tipo vira nulo e gera aviso, como na API.

_cache_listagem: dict[str, dict] = {}
_cache_csv: dict[tuple, pd.DataFrame] = {}
_RE_INTEIRO = re.compile(r"^(QTD|QTDE|QUANTIDADE|DIAS)_|^(ANO|MES|DIA)$|^(ANO|MES)_")
_RE_DATA = re.compile(r"^(DIA|DATA|DT)_")
_RE_NUMERO = re.compile(r"^(VL|VALOR|PERCENTUAL)_")
# Códigos e chaves: igualdade exata (ID_PROPOSTA=10 não pode casar com 100); o resto do texto é "contém"
_RE_CODIGO = re.compile(r"^(ID|COD|CD|NR|NUMERO|CNPJ|CPF|CEP|UF|SG|SIGLA|UG)(_|$)|_(ID|COD|CNPJ|CPF|UF|IBGE)$")


def _eh_codigo(nome: str) -> bool:
    return bool(_RE_CODIGO.search(nome.upper()))


def _listagem() -> dict[str, dict]:
    """tabela → {blob, url, tamanho, modificado, etag}. tabela = nome do zip sem 'siconv_' nem '.zip'."""
    if not _cache_listagem:
        marcador = ""
        while True:
            params = {"restype": "container", "comp": "list", **({"marker": marcador} if marcador else {})}
            raiz = ET.fromstring(_get(DOWNLOADS, params=params).content)
            for b in raiz.iter("Blob"):
                nome = b.findtext("Name") or ""
                if not nome.endswith(".zip") or nome.startswith("data_carga"):  # data_carga_*: só a data da carga
                    continue
                p = b.find("Properties")
                _cache_listagem[re.sub(r"^siconv_", "", nome[:-4])] = {
                    "blob": nome, "url": DOWNLOADS + nome,
                    "tamanho": int(p.findtext("Content-Length") or 0) if p is not None else 0,
                    "modificado": p.findtext("Last-Modified") if p is not None else None,
                    "etag": (p.findtext("Etag") or "").strip('"') if p is not None else "",
                }
            marcador = (raiz.findtext("NextMarker") or "").strip()
            if not marcador:
                break
    return _cache_listagem


def _baixar(info: dict) -> Path:
    """Baixa o zip para o cache local (reaproveitado enquanto o etag não muda) e devolve o caminho."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    base = info["blob"][:-4]
    destino = CACHE_DIR / f"{base}.{re.sub(r'[^0-9A-Za-z]', '', info['etag']) or 'sem-etag'}.zip"
    if destino.exists():
        return destino
    for antigo in CACHE_DIR.glob(f"{base}.*.zip"):  # versão anterior do mesmo arquivo
        antigo.unlink(missing_ok=True)
    _log(f"Baixando {info['blob']} ({info['tamanho'] / 1e6:,.1f} MB)...")
    tmp = destino.with_suffix(".parcial")
    for i in range(TENTATIVAS):
        try:
            with session.get(info["url"], stream=True, timeout=TIMEOUT) as r:
                if 400 <= r.status_code < 500 and r.status_code != 429:
                    raise ErroTG(f"HTTP {r.status_code} ao baixar {info['url']}.")
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    for bloco in r.iter_content(1 << 20):
                        f.write(bloco)
            os.replace(tmp, destino)
            return destino
        except requests.RequestException as e:
            tmp.unlink(missing_ok=True)
            if i == TENTATIVAS - 1:
                raise ErroTG(f"Falha ao baixar {info['url']} após {TENTATIVAS} tentativas: {e}") from None
            _log(f"  ! {type(e).__name__}; nova tentativa em {2 ** i}s")
            time.sleep(2 ** i)
    raise AssertionError("inalcançável")


def _membro_csv(z: zipfile.ZipFile) -> zipfile.ZipInfo:
    membros = [i for i in z.infolist() if i.filename.lower().endswith(".csv")]
    if not membros:
        raise ErroTG(f"O arquivo {z.filename} não contém CSV.")
    return membros[0]


def _tipo_csv(nome: str) -> tuple[str, str | None]:
    n = nome.upper()
    if _RE_INTEIRO.search(n):
        return "integer", None
    if _RE_DATA.search(n):
        return "string", "date"
    if _RE_NUMERO.search(n):
        return "number", None
    return "string", None


def _endpoint_csv(tabela: str) -> Endpoint:
    lst = _listagem()
    t = tabela.strip().lower().removeprefix("siconv_").removesuffix(".zip")
    if t not in lst:
        raise ErroTG(f"Arquivo '{t}' não existe em {MODULO_CSV}.{_sugestoes(t, list(lst))}\n"
                     f"Arquivos disponíveis: {', '.join(sorted(lst))}")
    info = lst[t]
    with zipfile.ZipFile(_baixar(info)) as z, z.open(_membro_csv(z)) as f:
        cabecalho = next(csv.reader(io.TextIOWrapper(f, encoding="utf-8-sig"), delimiter=";"))
    cols, filtros = [], {}
    nomes = [c.strip() for c in cabecalho]
    for nome in nomes:
        tipo, formato = _tipo_csv(nome)
        # DIA_X junto de MES_X (e ANO_X) é o trio dia/mês/ano em números, não uma data (ex.: DIA_PROP, MES_PROP)
        if nome.upper().startswith("DIA_") and f"MES_{nome[4:]}".upper() in {n.upper() for n in nomes}:
            tipo, formato = "integer", None
        cols.append(Coluna(nome, tipo, formato))
        filtros[nome] = Filtro(nome, tipo, formato)
    # max_pagina "infinito": a leitura é local, não existe paginação; isso também desliga a consulta por chave
    return Endpoint(MODULO_CSV, t, info["url"], cols, filtros, 10 ** 9)


def _sem_acento(txt: str) -> str:
    return unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii").upper()


def _normalizar_csv(df: pd.DataFrame, ep: Endpoint) -> pd.DataFrame:
    """Datas dd/mm/aaaa → ISO; números com vírgula decimal → ponto. O resto fica como o CSV publica."""
    for c in ep.colunas:
        if c.nome not in df:
            continue
        s = df[c.nome]
        if c.formato == "date":
            df[c.nome] = s.str.replace(r"^\s*(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", regex=True)
        elif c.tipo in ("number", "integer"):
            com_virgula = s.str.contains(",", regex=False, na=False)
            df[c.nome] = s.where(~com_virgula,
                                 s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return df


def _mascara_csv(df: pd.DataFrame, ep: Endpoint, combos: list[dict[str, str]]) -> pd.Series:
    """Igualdade local. Texto = contém, sem diferenciar acento nem maiúsculas (mais tolerante que a API)."""
    m = pd.Series(True, index=df.index)
    valores: dict[str, list[str]] = {}
    for c in combos:
        for k, v in c.items():
            valores.setdefault(k, [])
            if v not in valores[k]:
                valores[k].append(v)
    cols = {c.nome: c for c in ep.colunas}
    for nome, vs in valores.items():
        c, s = cols[nome], df[nome]
        if c.formato == "date":
            mm = s.str[:10].isin(vs)
        elif c.tipo in ("number", "integer"):
            mm = pd.to_numeric(s, errors="coerce").isin([float(v) for v in vs])
        elif _eh_codigo(nome):
            mm = s.fillna("").str.strip().str.upper().isin([v.strip().upper() for v in vs])
        else:
            alvo = s.fillna("").map(_sem_acento)
            mm = pd.Series(False, index=df.index)
            for v in vs:
                mm |= alvo.str.contains(_sem_acento(v), regex=False)
        m &= mm.fillna(False).astype(bool)
    return m


def _ler_csv(ep: Endpoint, combos: list[dict[str, str]]) -> pd.DataFrame:
    """Lê o CSV em blocos, normaliza e aplica os filtros de igualdade; o resultado fica em cache na execução."""
    info = _listagem()[ep.tabela]
    chave = (info["blob"], info["etag"], json.dumps(combos, sort_keys=True))
    if chave in _cache_csv:
        return _cache_csv[chave].copy()
    partes, lidas = [], 0
    with zipfile.ZipFile(_baixar(info)) as z, z.open(_membro_csv(z)) as f:
        leitor = pd.read_csv(f, sep=";", dtype=str, encoding="utf-8-sig", chunksize=CSV_BLOCO,
                             keep_default_na=False, na_values=[""])
        for bloco in leitor:
            bloco.columns = [str(c).strip() for c in bloco.columns]
            lidas += len(bloco)
            bloco = _normalizar_csv(bloco, ep)
            if combos != [{}]:
                bloco = bloco[_mascara_csv(bloco, ep, combos)]
            partes.append(bloco)
            if lidas >= CSV_BLOCO:
                _log(f"  {ep.tabela}: {lidas:,} linhas lidas")
    df = pd.concat(partes, ignore_index=True) if partes else pd.DataFrame(columns=[c.nome for c in ep.colunas])
    _cache_csv[chave] = df
    return df.copy()


# ---------- filtros ----------

_NAO_SUPORTA = ("a API do TransfereGov não suporta operadores PostgREST (gte., in., ...). Use coluna=valor; "
                "para vários valores, repita o filtro (-f col=A -f col=B); para faixas, use coluna>=valor, "
                "coluna<=valor, > ou <.")
_OP_POSTGREST = re.compile(r"^(eq|neq|gt|gte|lt|lte|in|like|ilike|is|not)\.", re.I)
_FILTRO_RE = re.compile(r"^\s*(?:(?P<escopo>[\w-]+):)?(?P<nome>\w+)\s*(?P<op>>=|<=|>|<|=)(?P<valor>.*)$", re.S)
_BOOL = {"true": "true", "false": "false", "1": "true", "0": "false", "sim": "true", "nao": "false",
         "não": "false"}
MAX_EXPANSAO_FAIXA = 50   # faixa inteira fechada até esse tamanho vira uma consulta por valor na API


def _parse_filtro(txt: str) -> tuple[str | None, str, str, str]:
    """'[tabela:]coluna<op>valor' → (escopo, coluna, op, valor), com op em = >= <= > <."""
    if "!=" in txt.split("=", 1)[0] + "=":
        raise ErroTG(f"Filtro '{txt}': 'diferente de' (!=) não é suportado. Filtre pelos valores desejados.")
    m = _FILTRO_RE.match(txt)
    if not m:
        raise ErroTG(f"Filtro inválido '{txt}'. Use coluna=valor (ex.: ano_plano_acao=2025) "
                     "ou faixa (ex.: ano_plano_acao>=2023).")
    valor = m["valor"].strip()
    if m["op"] == "=" and _OP_POSTGREST.match(valor):
        raise ErroTG(f"Filtro '{txt}': {_NAO_SUPORTA}")
    return m["escopo"], m["nome"], m["op"], valor


def _validar_valor(ep: Endpoint, f: Filtro, valor: str) -> str:
    """Valida e normaliza no cliente: um 422 da API custa uma ida e volta e explica menos."""
    onde = f"Filtro {f.nome}={valor!r} ({ep.modulo}/{ep.tabela})"
    if valor == "":
        raise ErroTG(f"{onde}: valor vazio.")
    if f.enum:
        for e in f.enum:
            if str(e).upper() == valor.upper():
                return str(e)
        raise ErroTG(f"{onde}: valor fora da lista aceita: {', '.join(map(str, f.enum))}.")
    if f.tipo == "integer":
        if not re.fullmatch(r"-?\d+", valor):
            raise ErroTG(f"{onde}: deve ser um número inteiro.")
    elif f.tipo == "number":
        try:
            valor = str(float(valor.replace(",", ".")))
        except ValueError:
            raise ErroTG(f"{onde}: deve ser numérico.") from None
    elif f.tipo == "boolean":
        if valor.lower() not in _BOOL:
            raise ErroTG(f"{onde}: use true ou false.")
        valor = _BOOL[valor.lower()]
    if f.formato == "date" or (f.pattern and "\\d{4}" in f.pattern):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", valor):
            raise ErroTG(f"{onde}: data deve estar em AAAA-MM-DD (a API compara a data exata; não há faixa).")
    elif f.pattern:
        try:
            if not re.search(f.pattern, valor):
                raise ErroTG(f"{onde}: não atende ao padrão {f.pattern}.")
        except re.error:
            pass
    return valor


def _sugestoes(nome: str, opcoes: list[str]) -> str:
    parecidos = list(dict.fromkeys([o for o in opcoes if nome.lower() in o][:3]
                                   + difflib.get_close_matches(nome, opcoes, n=3, cutoff=0.5)))
    return f" Você quis dizer: {', '.join(parecidos)}?" if parecidos else ""


@dataclass
class FiltroLocal:
    """Faixa aplicada no pandas depois do download (a API não tem >=, <)."""
    coluna: str
    op: str
    valor: object       # int | float | pd.Timestamp, já no tipo da coluna
    texto: str          # como o usuário escreveu, para os metadados


@dataclass
class Plano:
    combos: list[dict[str, str]]          # uma consulta à API por item
    locais: list[FiltroLocal]
    descricao: str


def _valor_faixa(ep: Endpoint, nome: str, tipo: str, formato: str | None, op: str, valor: str):
    """Converte o limite da faixa para o tipo da coluna. Devolve (op, valor), podendo ajustar o op."""
    onde = f"Faixa {nome}{op}{valor} ({ep.modulo}/{ep.tabela})"
    if formato in ("date", "date-time"):
        m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})([T ][\d:.]+)?", valor)
        ts = pd.to_datetime(valor, errors="coerce", format="ISO8601") if m else pd.NaT
        if pd.isna(ts):
            raise ErroTG(f"{onde}: data deve estar em AAAA-MM-DD.")
        if formato == "date-time" and not m.group(2):
            # Limite só com a data vale para o dia inteiro: <=31/12 inclui 31/12 23:59; >31/12 começa em 01/01.
            # timedelta da biblioteca padrão: pd.Timedelta aqui gera DeprecationWarning do numpy no pandas 2.x.
            dia_seguinte = pd.Timestamp(ts.to_pydatetime() + timedelta(days=1))
            if op == "<=":
                return "<", dia_seguinte
            if op == ">":
                return ">=", dia_seguinte
        return op, ts
    if tipo == "integer":
        if not re.fullmatch(r"-?\d+", valor):
            raise ErroTG(f"{onde}: deve ser um número inteiro.")
        return op, int(valor)
    if tipo == "number":
        try:
            return op, float(valor.replace(",", "."))
        except ValueError:
            raise ErroTG(f"{onde}: deve ser numérico.") from None
    raise ErroTG(f"{onde}: faixa só vale para colunas numéricas ou de data; '{nome}' é {formato or tipo}.")


def _planejar(ep: Endpoint, filtros: list[str], multi: bool = False) -> Plano:
    """Filtros do usuário → consultas à API + faixas locais.

    - igualdade: mesmo nome repetido = OU (uma consulta por valor); nomes diferentes = E;
    - faixa inteira fechada (até MAX_EXPANSAO_FAIXA valores) numa coluna que é filtro da API: vira igualdade
      por valor — exato e sem baixar a mais;
    - demais faixas: aplicadas no pandas; o download é limitado só pelos filtros de igualdade.
    Filtros com escopo de outra tabela são ignorados aqui. Nome desconhecido é erro: a API o ignoraria em
    silêncio e devolveria a tabela inteira.
    """
    iguais: dict[str, list[str]] = {}
    faixas: dict[str, list[tuple[str, str, str]]] = {}
    for txt in filtros or []:
        escopo, nome, op, valor = _parse_filtro(txt)
        if escopo and escopo != ep.tabela:
            continue
        if op != "=":
            faixas.setdefault(nome, []).append((op, valor, f"{nome}{op}{valor}"))
            continue
        if nome not in ep.filtros:
            escopo_dica = ("\nCom várias tabelas, um filtro sem prefixo precisa existir em todas; "
                           "para restringir use tabela:coluna=valor.") if multi and not escopo else ""
            raise ErroTG(f"Filtro '{nome}' não existe em {ep.modulo}/{ep.tabela}.{_sugestoes(nome, list(ep.filtros))}\n"
                         f"Filtros aceitos: {', '.join(ep.filtros)}{escopo_dica}")
        v = _validar_valor(ep, ep.filtros[nome], valor)
        if v not in iguais.setdefault(nome, []):
            iguais[nome].append(v)

    colunas = {c.nome: c for c in ep.colunas}
    locais: list[FiltroLocal] = []
    expandidas: list[str] = []
    for nome, conds in faixas.items():
        col, filtro = colunas.get(nome), ep.filtros.get(nome)
        if col is None and filtro is None:
            nomes = list(dict.fromkeys([*colunas, *ep.filtros]))
            raise ErroTG(f"Coluna '{nome}' não existe em {ep.modulo}/{ep.tabela}.{_sugestoes(nome, nomes)}\n"
                         f"Colunas: {', '.join(colunas)}")
        tipo, formato = (col.tipo, col.formato) if col else (filtro.tipo, filtro.formato)
        limites = [_valor_faixa(ep, nome, tipo, formato, op, valor) for op, valor, _ in conds]
        textos = [t for _, _, t in conds]

        if tipo == "integer" and not formato:
            lo = max([v + (op == ">") for op, v in limites if op in (">", ">=")], default=None)
            hi = min([v - (op == "<") for op, v in limites if op in ("<", "<=")], default=None)
            if lo is not None and hi is not None and lo > hi:
                raise ErroTG(f"Faixa vazia em {nome}: {' E '.join(textos)}.")
            if nome in iguais:  # igualdade + faixa na mesma coluna: interseção no cliente, sem ir à API
                manter = [x for x in iguais[nome] if (lo is None or int(x) >= lo) and (hi is None or int(x) <= hi)]
                if not manter:
                    raise ErroTG(f"Faixa vazia em {nome}: nenhum dos valores {', '.join(iguais[nome])} "
                                 f"atende a {' E '.join(textos)}.")
                iguais[nome] = manter
                continue
            if filtro and lo is not None and hi is not None and hi - lo + 1 <= MAX_EXPANSAO_FAIXA:
                iguais[nome] = [str(x) for x in range(lo, hi + 1)]
                expandidas.append(nome)
                continue
        if col is None:
            raise ErroTG(f"'{nome}' é filtro da API mas não vem nas colunas da resposta, então a faixa não pode ser "
                         f"aplicada localmente. Use valores exatos ou uma faixa inteira com início e fim "
                         f"(até {MAX_EXPANSAO_FAIXA} valores).")
        locais += [FiltroLocal(nome, op, v, t) for (op, v), t in zip(limites, textos)]

    combos = [dict(zip(iguais, vs)) for vs in itertools.product(*iguais.values())]
    if len(combos) > MAX_COMBINACOES:
        raise ErroTG(f"Os filtros geram {len(combos)} consultas (máximo {MAX_COMBINACOES}). "
                     "Reduza os valores repetidos ou o tamanho das faixas.")
    partes = [f"{k}={' OU '.join(vs)}" for k, vs in iguais.items()]
    partes += [f"{f.texto} (local)" for f in locais]
    return Plano(combos, locais, " E ".join(partes) or "(nenhum)")


def _aplicar_locais(df: pd.DataFrame, locais: list[FiltroLocal]) -> pd.DataFrame:
    """Nulo fica fora da faixa (como no SQL: NULL >= x não é verdadeiro)."""
    if not locais or df.empty:
        return df
    mascara = pd.Series(True, index=df.index)
    for f in locais:
        s = df[f.coluna]
        cmp = {">=": s.ge, "<=": s.le, ">": s.gt, "<": s.lt}[f.op](f.valor)
        mascara &= cmp.fillna(False).astype(bool)
    return df[mascara].reset_index(drop=True)


# ---------- contagem e extração ----------

def _pagina(ep: Endpoint, combo: dict, pagina: int, tamanho: int) -> dict:
    j = _get(ep.url, params={**combo, "pagina": pagina, "tamanho_da_pagina": tamanho}).json()
    if not isinstance(j, dict) or not {"data", "total_items", "total_pages"} <= j.keys():
        raise ErroTG(f"Resposta inesperada de {ep.url} (sem data/total_items). O formato da API pode ter mudado.")
    return j


def contar(modulo: str, tabela: str, filtros: list[str]) -> int:
    """Linhas que serão BAIXADAS: soma do total_items de cada consulta.

    É um teto do resultado final quando há faixa local (aplicada depois) ou valores de texto sobrepostos.
    """
    ep = endpoint(modulo, tabela)
    combos = _planejar(ep, filtros).combos
    if ep.modulo == MODULO_CSV:
        return len(_ler_csv(ep, combos))
    return sum(_pagina(ep, c, 1, 1)["total_items"] for c in combos)


def _dica_acento(ep: Endpoint, combos: list[dict[str, str]]) -> str | None:
    """Zero linhas com filtro de texto na API costuma ser acento: ela compara 'UBERLANDIA' ≠ 'UBERLÂNDIA'."""
    if ep.modulo == MODULO_CSV:  # nos CSVs a comparação já ignora acento
        return None
    textos = sorted({f"{k}={v}" for c in combos for k, v in c.items()
                     if ep.filtros[k].tipo == "string" and not ep.filtros[k].enum and not ep.filtros[k].formato})
    if not textos:
        return None
    return (f"Nenhuma linha com {', '.join(textos)}. A API diferencia acentos no texto (UBERLANDIA ≠ UBERLÂNDIA): "
            "tente a grafia oficial com acento ou, melhor, filtre por código (IBGE, CNPJ, id).")


def _data_atualizacao(ep: Endpoint) -> str | None:
    if ep.modulo == MODULO_CSV:
        return _listagem()[ep.tabela]["modificado"]
    if "/data-atualizacao" not in spec(ep.modulo).get("paths", {}):
        return None
    try:
        j = _get(f"{BASE}/{ep.modulo}/data-atualizacao").json()
    except (ErroTG, ValueError):
        return None
    return str(next(iter(j.values()))) if isinstance(j, dict) and j else None


def _paginar(ep: Endpoint, combo: dict, tam: int, rotulo: str, avisos: list[str]) -> tuple[list[dict], int]:
    """Percorre pagina=1..N. Para no lote vazio ou menor que `tam`; trava de segurança após total_pages."""
    linhas: list[dict] = []
    pagina, total, total_pages = 1, 0, 0
    tty = sys.stderr.isatty()
    while True:
        j = _pagina(ep, combo, pagina, tam)
        if pagina == 1:
            total, total_pages = j["total_items"], j["total_pages"]
            _log(f"{ep.modulo}/{ep.tabela} [{rotulo}]: {total:,} linhas em {total_pages:,} página(s) de {tam}")
        lote = j["data"]
        if not lote:
            break
        linhas.extend(lote)
        if tty:
            _log(f"\r  {len(linhas):,}/{total:,}", fim="")
        elif pagina % 50 == 0:
            _log(f"  {len(linhas):,}/{total:,}")
        if len(lote) < tam:
            break
        pagina += 1
        if pagina > total_pages + 1:
            avisos.append(f"{ep.tabela} [{rotulo}]: parada de segurança — a API continuou devolvendo páginas "
                          f"cheias além de total_pages={total_pages}.")
            break
        time.sleep(PAUSA_ENTRE_PAGINAS)
    if tty:
        _log()
    return linhas, total


@dataclass
class Resultado:
    endpoint: Endpoint
    df: pd.DataFrame
    meta: dict
    avisos: list[str] = field(default_factory=list)


def extrair(modulo: str, tabela: str, filtros: list[str], tamanho_pagina: int | None = None) -> Resultado:
    ep = endpoint(modulo, tabela)
    plano = _planejar(ep, filtros)
    combos = plano.combos
    tam = tamanho_pagina or ep.max_pagina
    if not 1 <= tam <= ep.max_pagina:
        raise ErroTG(f"Tamanho de página {tam} fora do permitido para {ep.modulo}/{ep.tabela} (1 a {ep.max_pagina}).")

    avisos: list[str] = []
    antes = _data_atualizacao(ep)
    linhas: list[dict] | pd.DataFrame = []
    total_api = 0
    if ep.modulo == MODULO_CSV:
        linhas = _ler_csv(ep, combos)
        total_api = len(linhas)
        _log(f"{ep.modulo}/{ep.tabela}: {total_api:,} linhas após os filtros de igualdade")
    else:
        for combo in combos:
            rotulo = ", ".join(f"{k}={v}" for k, v in combo.items()) or "sem filtro"
            parte, total = _paginar(ep, combo, tam, rotulo, avisos)
            if len(parte) != total:
                avisos.append(f"{ep.tabela} [{rotulo}]: coletadas {len(parte):,} linhas, mas a API informou "
                              f"total_items={total:,}. A base pode ter mudado durante a extração; rode de novo.")
            linhas.extend(parte)
            total_api += total
    if total_api == 0 and (dica := _dica_acento(ep, combos)):
        avisos.append(dica)
    depois = _data_atualizacao(ep)
    if antes and depois and antes != depois:
        avisos.append(f"A base de {ep.modulo} foi atualizada durante a extração ({antes} → {depois}). "
                      "Linhas podem ter duplicado ou sumido; rode de novo.")

    df = tipar(linhas, ep, avisos)
    # Só na API (várias consultas); no CSV a leitura é uma só e não há sobreposição.
    texto_multi = [k for k in (combos[0] if combos and ep.modulo != MODULO_CSV else {})
                   if len({c[k] for c in combos}) > 1 and ep.filtros[k].tipo == "string" and not ep.filtros[k].enum]
    if texto_multi:
        # Texto é "contém": nome=AGUDO e nome=MORRO podem trazer a mesma linha nas duas consultas.
        n0 = len(df)
        df = df.drop_duplicates(ignore_index=True)
        if n0 > len(df):
            _log(f"  {n0 - len(df):,} linha(s) repetida(s) entre as consultas por {', '.join(texto_multi)} foram removidas.")
    chave = ep.pk or None
    n_dup = int(df.duplicated(subset=chave).sum()) if len(df) else 0
    if n_dup:
        criterio = f"pela PK ({', '.join(ep.pk)})" if ep.pk else "(linha inteira igual)"
        avisos.append(f"{ep.tabela}: {n_dup:,} linha(s) duplicada(s) {criterio}. Sem ordenação na API, isso "
                      "indica base mudando durante a extração ou duplicata na origem.")
    baixadas = len(df)
    df = _aplicar_locais(df, plano.locais)
    if plano.locais:
        _log(f"  Faixa local ({', '.join(f.texto for f in plano.locais)}): {baixadas:,} → {len(df):,} linhas.")

    meta = {
        "modulo": ep.modulo,
        "endpoint": ep.url,
        "filtros": plano.descricao,
        "linhas": len(df),
        "linhas_baixadas": baixadas,
        "total_api": total_api,
        "data_atualizacao_base": antes or "(indisponível)",
        "extraido_em": datetime.now().isoformat(timespec="seconds"),
        "versao_script": VERSAO,
        "avisos": " | ".join(avisos) or "(nenhum)",
    }
    return Resultado(ep, df, meta, avisos)


# ---------- junção ----------

def _usuario_filtra(ep: Endpoint, filtros: list[str], coluna: str) -> bool:
    return any(n == coluna and e in (None, ep.tabela) for e, n, _, _ in map(_parse_filtro, filtros))


def extrair_juntando(modulo: str, nomes: list[str], filtros: list[str], chave: str,
                     tamanho_pagina: int | None = None) -> list[Resultado]:
    """Junção interna de 2+ tabelas por `chave`. Devolve [juntado, tabela1, tabela2, ...] na ordem pedida.

    Regra das abas: uma tabela só é restringida às chaves da junção quando OUTRA tabela tem filtro do usuário
    (aí a junção funciona como filtro: "planos de SP" = planos cujo beneficiário é de SP). Sem filtro nas outras,
    a aba vem completa, como o usuário pediu ("uma aba por tabela"); a interseção fica só na aba 'juntado'.

    A tabela de menor volume é baixada primeiro. As chaves das tabelas filtradas restringem as seguintes e, se
    forem poucas (menos consultas do que páginas para baixar a tabela inteira), a tabela seguinte é consultada
    por chave no servidor.
    """
    eps = [endpoint(modulo, t) for t in nomes]
    if len(eps) < 2:
        raise ErroTG("--juntar precisa de pelo menos duas tabelas (--tabela A --tabela B).")
    sem = [ep.tabela for ep in eps if chave not in {c.nome for c in ep.colunas}]
    if sem:
        raise ErroTG(f"A chave '{chave}' não existe em: {', '.join(sem)}. Veja 'Chaves de junção prováveis' na "
                     "reference do módulo ou use o subcomando colunas.")

    volumes = {ep.tabela: contar(modulo, ep.tabela, filtros) for ep in eps}
    filtrada = {ep.tabela: _planejar(ep, filtros).combos != [{}] or bool(_planejar(ep, filtros).locais) for ep in eps}

    def restringir(t: str) -> bool:
        return any(v for o, v in filtrada.items() if o != t)

    chaves: set | None = None   # interseção das chaves das tabelas FILTRADAS já baixadas
    por_tabela: dict[str, Resultado] = {}
    for ep in sorted(eps, key=lambda e: volumes[e.tabela]):
        if restringir(ep.tabela) and chaves is not None and not chaves:
            _log(f"{ep.modulo}/{ep.tabela}: nenhuma chave {chave} em comum até aqui; tabela não baixada.")
            por_tabela[ep.tabela] = Resultado(ep, tipar([], ep), {
                "modulo": ep.modulo, "endpoint": ep.url, "filtros": "(não baixada: junção sem chaves em comum)",
                "linhas": 0, "linhas_baixadas": 0, "total_api": 0, "data_atualizacao_base": "(não consultada)",
                "extraido_em": datetime.now().isoformat(timespec="seconds"), "versao_script": VERSAO,
                "avisos": "(nenhum)"})
            continue
        fs, nota = list(filtros), None
        if restringir(ep.tabela) and chaves and chave in ep.filtros and not _usuario_filtra(ep, filtros, chave):
            n_comb = len(_planejar(ep, filtros).combos)
            if len(chaves) * n_comb <= MAX_COMBINACOES:
                paginas = math.ceil(volumes[ep.tabela] / (tamanho_pagina or ep.max_pagina))
                if len(chaves) < paginas:
                    fs += [f"{ep.tabela}:{chave}={k}" for k in sorted(chaves, key=str)]
                    nota = f"{chave} em {len(chaves)} valores da junção"
                    _log(f"{ep.tabela}: consultando por {len(chaves)} valor(es) de {chave} em vez de baixar "
                         f"{paginas:,} página(s).")
        r = extrair(modulo, ep.tabela, fs, tamanho_pagina)
        if nota:
            base = _planejar(ep, filtros).descricao
            r.meta["filtros"] = nota if base == "(nenhum)" else f"{base} E {nota}"
        if filtrada[ep.tabela]:
            ks = set(r.df[chave].dropna().tolist())
            chaves = ks if chaves is None else chaves & ks
        por_tabela[ep.tabela] = r
    primeira = next(iter(por_tabela.values()))

    resultados = [por_tabela[ep.tabela] for ep in eps]
    df = resultados[0].df
    cols = list(resultados[0].endpoint.colunas)
    for r in resultados[1:]:
        # Coluna repetida (fora a chave) ganha sufixo com o nome da tabela: nada é sobrescrito em silêncio.
        ren = {c: f"{c}__{r.endpoint.tabela}" for c in r.df.columns if c != chave and c in df.columns}
        df = df.merge(r.df.rename(columns=ren), on=chave, how="inner")
        cols += [replace(c, nome=ren.get(c.nome, c.nome)) for c in r.endpoint.colunas if c.nome != chave]
    comuns = list(set(df[chave].dropna().tolist()))
    for r in resultados:
        if not restringir(r.endpoint.tabela):
            continue
        antes = len(r.df)
        r.df = r.df[r.df[chave].isin(comuns)].reset_index(drop=True)
        r.meta["linhas"] = len(r.df)
        if antes > len(r.df):
            r.meta["linhas_fora_do_filtro_da_juncao"] = antes - len(r.df)

    _log(f"Junção por {chave}: {len(df):,} linha(s).")
    meta = {
        "modulo": eps[0].modulo,
        "juncao": f"{' + '.join(ep.tabela for ep in eps)} por {chave} (interna: só linhas com par em todas)",
        "filtros": " | ".join(f"{r.endpoint.tabela}: {r.meta['filtros']}" for r in resultados),
        "linhas": len(df),
        "data_atualizacao_base": primeira.meta["data_atualizacao_base"],
        "extraido_em": datetime.now().isoformat(timespec="seconds"),
        "versao_script": VERSAO,
        "avisos": " | ".join(a for r in resultados for a in r.avisos) or "(nenhum)",
    }
    juntado = Endpoint(eps[0].modulo, "juntado", " + ".join(ep.url for ep in eps), cols, {}, 0)
    return [Resultado(juntado, df.reset_index(drop=True), meta)] + resultados


# ---------- execução agendada ----------

def _pular_se_atual(ep: Endpoint, pasta: Path, arquivo: str, formato: str, assinatura: str) -> list[Path] | None:
    """Arquivos da execução anterior se a base não mudou e os parâmetros são os mesmos; senão None.

    A API não tem extração incremental: sem isso, uma rotina diária baixaria tudo de novo mesmo sem carga nova.
    """
    try:
        if formato == "xlsx":
            p = pasta / f"{arquivo}.xlsx"
            if not p.exists():
                return None
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            linhas = list(wb["metadados"].iter_rows(min_row=2, values_only=True))
            wb.close()
            caminhos = [p]
        else:
            pm = pasta / f"{arquivo}_metadados.csv"
            if not pm.exists():
                return None
            linhas = list(pd.read_csv(pm, sep=";", encoding="utf-8-sig", dtype=str).itertuples(index=False, name=None))
            tabelas_ant = list(dict.fromkeys(t for t, _, _ in linhas))
            caminhos = ([pasta / f"{arquivo}.csv"] if len(tabelas_ant) == 1 else
                        [pasta / f"{arquivo}_{t}.csv" for t in tabelas_ant]) + [pm]
    except Exception:  # arquivo corrompido ou de outra versão: extrai de novo
        return None
    meta: dict[str, dict[str, str]] = {}
    for t, k, v in linhas:
        meta.setdefault(str(t), {})[str(k)] = str(v)
    if not meta or not all(p.exists() for p in caminhos):
        return None
    if any(m.get("parametros") != assinatura for m in meta.values()):
        return None
    atual = _data_atualizacao(ep)
    if not atual or any(m.get("data_atualizacao_base") not in (atual, "(não consultada)") for m in meta.values()):
        return None
    _log(f"Base de {ep.modulo} sem atualização desde {atual} e parâmetros iguais: arquivo mantido, nada baixado.")
    return caminhos


# ---------- tipagem ----------

def _nulo(v) -> bool:
    return v is None or v is pd.NA or (isinstance(v, float) and math.isnan(v))


def _texto(v):
    if _nulo(v):
        return None
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _converter(s: pd.Series, c: Coluna, avisos: list[str]) -> pd.Series:
    nao_nulos = int(s.map(lambda v: not _nulo(v)).sum())
    if c.tipo == "integer":
        try:  # via int() direto: to_numeric passaria por float e perderia precisão acima de 2**53
            out = pd.Series(pd.array([None if _nulo(v) else int(v) for v in s], dtype="Int64"))
        except (TypeError, ValueError, OverflowError):
            out = pd.to_numeric(s, errors="coerce").astype("Float64")
    elif c.tipo == "number":
        out = pd.to_numeric(s, errors="coerce").astype("Float64")
    elif c.tipo == "boolean":
        out = pd.Series(pd.array([None if _nulo(v) else (v if isinstance(v, bool) else
                                  _BOOL.get(str(v).lower()) == "true") for v in s], dtype="boolean"))
    elif c.tipo == "string" and c.formato in ("date", "date-time"):
        out = (pd.to_datetime(s, errors="coerce", format="ISO8601", utc=True)
               .dt.tz_localize(None).astype("datetime64[us]"))  # resolução fixa, independe dos dados
    elif c.tipo in ("string", "json"):
        out = s.map(_texto).astype("string")
    else:
        out = s.map(lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
    perdidos = nao_nulos - int(out.notna().sum())
    if perdidos > 0:
        avisos.append(f"Coluna {c.nome}: {perdidos:,} valor(es) não convertido(s) para {c.formato or c.tipo} "
                      "ficaram vazios.")
    return out.reset_index(drop=True)


def tipar(dados: list[dict] | pd.DataFrame, ep: Endpoint, avisos: list[str] | None = None) -> pd.DataFrame:
    """Aplica os tipos do schema. Colunas na ordem do schema; ausentes viram nulas com o tipo certo.

    Uma coluna toda nula numa página (ou em todas) mantém o tipo, porque ele vem do schema, não dos dados.
    """
    avisos = [] if avisos is None else avisos
    df = dados if isinstance(dados, pd.DataFrame) else pd.DataFrame(dados, dtype=object)
    n = len(df)
    df = df.reset_index(drop=True)
    vazia = pd.Series([None] * n, dtype=object)
    out: dict[str, pd.Series] = {}
    pais = set()
    for c in ep.colunas:
        if c.origem:
            pai, sub = c.origem
            pais.add(pai)
            s = df[pai].map(lambda d, k=sub: d.get(k) if isinstance(d, dict) else None) if pai in df else vazia
        else:
            s = df[c.nome] if c.nome in df else vazia
        out[c.nome] = _converter(s, c, avisos)
    extras = [x for x in df.columns if x not in out and x not in pais]
    if extras:
        avisos.append(f"Colunas fora do schema mantidas como texto: {', '.join(map(str, extras))}.")
        for x in extras:
            out[str(x)] = df[x].map(_texto).astype("string").reset_index(drop=True)
    return pd.DataFrame(out, index=pd.RangeIndex(n))


# ---------- exportação ----------

def _gravar_atomico(destino: Path, escrever: Callable[[Path], None]) -> None:
    """Escreve em .tmp e troca no fim: quem abre o arquivo durante uma execução nunca vê meio arquivo."""
    tmp = destino.with_name(f"{destino.stem}.tmp{destino.suffix}")
    try:
        escrever(tmp)
        os.replace(tmp, destino)
    except PermissionError:
        tmp.unlink(missing_ok=True)
        raise ErroTG(f"Sem permissão para gravar {destino}. O arquivo está aberto no Excel? Feche e rode de novo.") from None
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def _cols_data(r: Resultado, formato: str) -> list[str]:
    return [c.nome for c in r.endpoint.colunas if c.formato == formato and c.nome in r.df]


def _linhas_meta(resultados: list[Resultado]) -> pd.DataFrame:
    return pd.DataFrame([(r.endpoint.tabela, k, v) for r in resultados for k, v in r.meta.items()],
                        columns=["tabela", "chave", "valor"])


def _para_csv(r: Resultado) -> pd.DataFrame:
    df = r.df.copy()
    for c in _cols_data(r, "date"):
        df[c] = df[c].dt.strftime("%d/%m/%Y")
    for c in _cols_data(r, "date-time"):
        df[c] = df[c].dt.strftime("%d/%m/%Y %H:%M:%S")
    for c in df.columns:  # `decimal=","` só se aplica a float nativo
        if str(df[c].dtype) == "Float64":
            df[c] = df[c].astype("float64")
    return df


def _para_excel(r: Resultado) -> pd.DataFrame:
    from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
    df = r.df.copy()
    for c in df.columns:
        if str(df[c].dtype) == "string":
            s = df[c].str.replace(ILLEGAL_CHARACTERS_RE, "", regex=True)
            longos = int((s.str.len() > EXCEL_MAX_CELULA).sum())
            if longos:
                r.avisos.append(f"Coluna {c}: {longos:,} texto(s) truncado(s) em {EXCEL_MAX_CELULA:,} caracteres (limite do Excel).")
                s = s.str.slice(0, EXCEL_MAX_CELULA)
            df[c] = s
    return df


def _nome_aba(tabela: str, parte: int | None, usados: set[str]) -> str:
    sufixo = f"_{parte}" if parte else ""
    nome = tabela[:31 - len(sufixo)] + sufixo
    i = 2
    while nome.lower() in usados:
        extra = f"~{i}{sufixo}"
        nome, i = tabela[:31 - len(extra)] + extra, i + 1
    usados.add(nome.lower())
    return nome


_FORMATO_EXCEL = {"date": "DD/MM/YYYY", "date-time": "DD/MM/YYYY HH:MM:SS"}


def _formatar_aba(ws, df: pd.DataFrame, r: Resultado | None = None) -> None:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    amostra = df.head(200)
    for i, c in enumerate(df.columns, start=1):
        largura = max([len(str(c))] + [len(str(v)) for v in amostra[c] if not _nulo(v)])
        ws.column_dimensions[ws.cell(1, i).column_letter].width = min(largura + 2, 60)
    if r is None:
        return
    # O pandas 3 ignora date_format/datetime_format do ExcelWriter: formata pelas colunas que o schema diz ser data.
    posicao = {c: i for i, c in enumerate(df.columns, start=1)}
    for fmt_schema, fmt_excel in _FORMATO_EXCEL.items():
        for c in _cols_data(r, fmt_schema):
            for (cel,) in ws.iter_rows(min_row=2, max_row=len(df) + 1, min_col=posicao[c], max_col=posicao[c]):
                cel.number_format = fmt_excel


def exportar(resultados: list[Resultado], formato: str, pasta: Path | str, arquivo: str) -> list[Path]:
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    meta = _linhas_meta(resultados)
    csv_kw = dict(index=False, sep=";", decimal=",", encoding="utf-8-sig")

    if formato == "csv":
        caminhos = []
        for r in resultados:
            p = pasta / (f"{arquivo}.csv" if len(resultados) == 1 else f"{arquivo}_{r.endpoint.tabela}.csv")
            df = _para_csv(r)
            _gravar_atomico(p, lambda tmp, d=df: d.to_csv(tmp, **csv_kw))
            caminhos.append(p)
        pm = pasta / f"{arquivo}_metadados.csv"
        _gravar_atomico(pm, lambda tmp: meta.to_csv(tmp, **csv_kw))
        return caminhos + [pm]

    p = pasta / f"{arquivo}.xlsx"
    total = sum(len(r.df) for r in resultados)
    if total > 300_000:
        _log(f"Gravando {total:,} linhas em Excel; pode levar alguns minutos (CSV é bem mais rápido).")

    def escrever(tmp: Path) -> None:
        usados: set[str] = set()
        with pd.ExcelWriter(tmp, engine="openpyxl") as xw:
            for r in resultados:
                df = _para_excel(r)
                partes = max(1, math.ceil(len(df) / EXCEL_MAX_ROWS))
                for i in range(partes):
                    nome = _nome_aba(r.endpoint.tabela, i + 1 if partes > 1 else None, usados)
                    parte = df.iloc[i * EXCEL_MAX_ROWS:(i + 1) * EXCEL_MAX_ROWS]
                    parte.to_excel(xw, sheet_name=nome, index=False)
                    _formatar_aba(xw.sheets[nome], parte, r)
            _linhas_meta(resultados).to_excel(xw, sheet_name="metadados", index=False)
            _formatar_aba(xw.sheets["metadados"], meta)

    _gravar_atomico(p, escrever)
    return [p]


# ---------- CLI ----------

def _cmd_colunas(ep: Endpoint) -> None:
    cols = pd.DataFrame([{"coluna": c.nome, "tipo": c.formato or c.tipo, "PK": "sim" if c.pk else "",
                          "descricao": c.descricao} for c in ep.colunas])
    if ep.modulo == MODULO_CSV:
        info = _listagem()[ep.tabela]
        print(f"{ep.modulo}/{ep.tabela} — {len(ep.colunas)} colunas · arquivo {info['blob']} "
              f"({info['tamanho'] / 1e6:.1f} MB, atualizado em {info['modificado']}); filtros aplicados localmente")
    else:
        print(f"{ep.modulo}/{ep.tabela} — {len(ep.colunas)} colunas, até {ep.max_pagina} linhas por página")
    print(cols.to_string(index=False))
    fs = pd.DataFrame([{"filtro": f.nome, "tipo": f.formato or f.tipo,
                        "como_compara": ("lista: " + ",".join(map(str, f.enum))) if f.enum else
                        ("igual (código)" if ep.modulo == MODULO_CSV and f.tipo == "string" and _eh_codigo(f.nome)
                         else "contém (ignora acento e maiúsc.)" if ep.modulo == MODULO_CSV and f.tipo == "string"
                         and not f.formato else
                         "contém (sem maiúsc./minúsc.; acento conta)" if f.tipo == "string" and not f.pattern
                         and not f.formato else "igual; aceita faixa" if f.tipo in ("integer", "number")
                         or f.formato else "igual"),
                        } for f in ep.filtros.values()])
    print("\nFiltros aceitos:")
    print(fs.to_string(index=False) if len(fs) else "(nenhum)")


def _cmd_extrair(a) -> int:
    nomes = list(dict.fromkeys(t.strip().strip("/") for t in a.tabela))
    eps = [endpoint(a.modulo, t) for t in nomes]
    multi = len(eps) > 1
    # Valida tudo antes de baixar qualquer coisa: erro na 2ª tabela não pode desperdiçar a 1ª.
    for txt in a.filtro:
        escopo = _parse_filtro(txt)[0]
        if escopo and escopo not in nomes:
            raise ErroTG(f"Filtro '{txt}' tem prefixo '{escopo}', que não está entre as tabelas pedidas: {', '.join(nomes)}.")
    for ep in eps:
        _planejar(ep, a.filtro, multi)
    if a.juntar and not multi:
        raise ErroTG("--juntar precisa de pelo menos duas tabelas (--tabela A --tabela B).")

    assinatura = json.dumps({"modulo": eps[0].modulo, "tabelas": nomes, "filtros": sorted(a.filtro),
                             "juntar": a.juntar, "formato": a.formato}, ensure_ascii=False, sort_keys=True)
    if a.so_se_atualizou:
        if not a.arquivo:
            raise ErroTG("--so-se-atualizou exige --arquivo com nome fixo, para comparar com a execução anterior.")
        mantidos = _pular_se_atual(eps[0], Path(a.saida), a.arquivo, a.formato, assinatura)
        if mantidos:
            for p in mantidos:
                print(p)
            return 0

    if a.juntar:
        resultados = extrair_juntando(a.modulo, nomes, a.filtro, a.juntar, a.tamanho_pagina)
    else:
        resultados = [extrair(a.modulo, ep.tabela, a.filtro, a.tamanho_pagina) for ep in eps]
    for r in resultados:
        r.meta["parametros"] = assinatura
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    sufixo = "juntado" if a.juntar else ("multi" if multi else nomes[0])
    arquivo = a.arquivo or f"transferegov_{eps[0].modulo}_{sufixo}_{stamp}"
    caminhos = exportar(resultados, a.formato, Path(a.saida), arquivo)
    avisos = [x for r in resultados for x in r.avisos]
    for x in avisos:
        _log(f"ATENÇÃO: {x}")
    for r in resultados:
        _log(f"{r.endpoint.tabela}: {len(r.df):,} linhas")
    for p in caminhos:
        print(p)
    return 3 if (a.estrito and avisos) else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("tabelas", help="lista as tabelas do módulo")
    s.add_argument("--modulo", required=True)
    s = sub.add_parser("colunas", help="colunas, tipos, PK e filtros de uma tabela")
    s.add_argument("--modulo", required=True)
    s.add_argument("--tabela", required=True)
    s = sub.add_parser("contar", help="conta linhas sem baixar")
    s.add_argument("--modulo", required=True)
    s.add_argument("--tabela", required=True)
    s.add_argument("-f", "--filtro", action="append", default=[])
    s = sub.add_parser("extrair", help="baixa e grava xlsx/csv")
    s.add_argument("--modulo", required=True)
    s.add_argument("--tabela", required=True, action="append", help="repetível: uma aba por tabela")
    s.add_argument("-f", "--filtro", action="append", default=[])
    s.add_argument("--formato", choices=["xlsx", "csv"], default="xlsx")
    s.add_argument("--saida", default="saida", help="pasta de saída (padrão: ./saida)")
    s.add_argument("--arquivo", help="nome do arquivo sem extensão; fixo = sobrescreve (útil em agendamento)")
    s.add_argument("--tamanho-pagina", type=int, dest="tamanho_pagina", help="padrão: máximo do endpoint")
    s.add_argument("--estrito", action="store_true", help="código de saída 3 se houver avisos")
    s.add_argument("--juntar", metavar="CHAVE", help="junção interna das tabelas pela coluna CHAVE (aba 'juntado')")
    s.add_argument("--so-se-atualizou", action="store_true", dest="so_se_atualizou",
                   help="com --arquivo fixo: não baixa se a base e os parâmetros não mudaram desde a última execução")

    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return int(e.code or 0)
    try:
        if a.cmd == "tabelas":
            if _modulo(a.modulo) == MODULO_CSV:  # arquivos: tamanho do zip importa (é baixado inteiro)
                for t, i in sorted(_listagem().items()):
                    print(f"{t}\t{i['tamanho'] / 1e6:.1f} MB\t{i['modificado']}")
            else:
                print("\n".join(tabelas(a.modulo)))
        elif a.cmd == "colunas":
            _cmd_colunas(endpoint(a.modulo, a.tabela))
        elif a.cmd == "contar":
            n = contar(a.modulo, a.tabela, a.filtro)
            ep = endpoint(a.modulo, a.tabela)
            plano = _planejar(ep, a.filtro)
            locais = plano.locais
            if n == 0 and (dica := _dica_acento(ep, plano.combos)):
                _log(dica)
            if locais:
                _log(f"Faixa(s) aplicada(s) localmente após o download ({', '.join(f.texto for f in locais)}): "
                     f"serão baixadas {n:,} linhas; o resultado final será menor ou igual.")
            print(n)
        elif a.cmd == "extrair":
            return _cmd_extrair(a)
        return 0
    except ErroTG as e:
        _log(f"ERRO: {e}")
        return 1
    except KeyboardInterrupt:
        _log("Interrompido.")
        return 130


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr):  # UTF-8 também quando redirecionado para arquivo/agendador
        if hasattr(_s, "reconfigure"):
            _s.reconfigure(encoding="utf-8")
    sys.exit(main())
