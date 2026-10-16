"""Corrige uma iteração de evals: escreve grading.json em cada run-*/ (campos text/passed/evidence).

Uso (desenvolvimento):
    python evals/corrigir.py transferegov-extrator-workspace/iteration-1

As verdades de referência (contagens) são calculadas na hora, com o próprio tg_extract, para que a
comparação use a base do mesmo dia da execução.
"""
from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / ".claude" / "skills" / "transferegov-extrator" / "scripts"))
sys.dont_write_bytecode = True
import tg_extract as tg  # noqa: E402

NORDESTE = {"MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"}
IBGE_UBERLANDIA = 3170206


@lru_cache(maxsize=None)
def contar(modulo: str, tabela: str, *filtros: str) -> int:
    return tg.contar(modulo, tabela, list(filtros))


@lru_cache(maxsize=None)
def ids_benef_sp() -> frozenset:
    r = tg.extrair("especiais", "beneficiarios-especiais", ["uf_beneficiario=SP"])
    return frozenset(r.df["id_beneficiario"].dropna().astype(int))


@lru_cache(maxsize=None)
def planos_sp_total() -> int:
    """Nº de planos de ação cujo beneficiário é de SP (verdade do eval 3; baixa a tabela inteira uma vez)."""
    r = tg.extrair("especiais", "planos-acao-especiais", [])
    return int(r.df["id_beneficiario"].isin(ids_benef_sp()).sum())


# ---------- leitura das saídas ----------

class Saida:
    def __init__(self, pasta: Path):
        self.pasta = pasta
        self.arquivos = sorted(p for p in pasta.rglob("*") if p.is_file())
        self.dados = [p for p in self.arquivos if p.suffix.lower() in (".xlsx", ".csv")
                      and not p.stem.endswith("_metadados")]
        self.metas_csv = [p for p in self.arquivos if p.stem.endswith("_metadados") and p.suffix == ".csv"]
        rp = pasta / "resposta.md"
        self.resposta = rp.read_text(encoding="utf-8", errors="replace") if rp.exists() else ""
        self.abas: dict[str, pd.DataFrame] = {}
        for p in self.dados:
            try:
                if p.suffix.lower() == ".xlsx":
                    for nome, df in pd.read_excel(p, sheet_name=None).items():
                        self.abas[f"{p.name}:{nome}"] = df
                else:
                    self.abas[p.name] = _ler_csv(p)
            except Exception as e:  # noqa: BLE001
                self.abas[f"{p.name}:ERRO"] = pd.DataFrame({"erro": [str(e)]})

    def xlsx(self):
        return [p for p in self.dados if p.suffix.lower() == ".xlsx"]

    def csvs(self):
        return [p for p in self.dados if p.suffix.lower() == ".csv"]

    def aba_com(self, *colunas: str) -> tuple[str, pd.DataFrame] | tuple[None, None]:
        """Maior aba que contém todas as colunas (fora metadados)."""
        cands = [(n, df) for n, df in self.abas.items()
                 if not n.lower().endswith("metadados") and all(c in df.columns for c in colunas)]
        return max(cands, key=lambda x: len(x[1])) if cands else (None, None)

    def dados_abas(self) -> list[tuple[str, pd.DataFrame]]:
        return [(n, df) for n, df in self.abas.items() if not n.lower().endswith("metadados")]

    def aba_com_linhas(self, *ns: int) -> tuple[str, pd.DataFrame] | tuple[None, None]:
        """Primeira aba de dados com exatamente um dos números de linhas (tolerante a nomes de coluna)."""
        for n, df in self.dados_abas():
            if len(df) in ns:
                return n, df
        return None, None

    def metadados_texto(self) -> str:
        partes = [df.to_string() for n, df in self.abas.items() if n.lower().endswith("metadados")]
        partes += [_ler_csv(p).to_string() for p in self.metas_csv]
        return "\n".join(partes)


def _ler_csv(p: Path) -> pd.DataFrame:
    bruto = p.read_bytes()[:4096].decode("utf-8-sig", errors="replace")
    sep = ";" if bruto.count(";") > bruto.count(",") else ","
    return pd.read_csv(p, sep=sep, encoding="utf-8-sig", dtype=str)


def _norm(txt) -> str:
    import unicodedata
    return unicodedata.normalize("NFKD", str(txt)).encode("ascii", "ignore").decode().lower()


def coluna_como(df: pd.DataFrame | None, *trechos: str) -> str | None:
    """Coluna cujo nome (sem acento, minúsculo) contém algum dos trechos — aceita nomes amigáveis."""
    if df is None:
        return None
    for c in df.columns:
        if any(t in _norm(c) for t in trechos):
            return c
    return None


def nomes_da_api(s: "Saida", *colunas: str) -> dict:
    nome, df = s.aba_com(*colunas)
    return A("Colunas com os nomes publicados pela fonte (rastreáveis até a API/arquivo)", df is not None,
             f"aba com {colunas}: {nome}")


def A(text: str, passed: bool, evidence: str) -> dict:
    return {"text": text, "passed": bool(passed), "evidence": evidence}


def tem_metadados_com(s: Saida, *trechos: str) -> tuple[bool, str]:
    t = s.metadados_texto()
    if not t:
        return False, "nenhuma aba/arquivo de metadados"
    faltam = [x for x in trechos if x.lower() not in t.lower()]
    return not faltam, ("metadados contém " + ", ".join(trechos)) if not faltam else f"faltam nos metadados: {faltam}"


def pergunta(s: Saida) -> bool:
    r = s.resposta.lower()
    return "?" in r or any(x in r for x in ("me diga", "me avise", "escolha", "confirme", "qual delas", "qual prefere"))


# ---------- asserções por eval ----------

def e1(s: Saida):
    n_ref = contar("especiais", "planos-acao-especiais", "ano_plano_acao=2024")
    nome, df = s.aba_com("id_plano_acao", "ano_plano_acao")
    anos = set(pd.to_numeric(df["ano_plano_acao"], errors="coerce").dropna().astype(int)) if df is not None else set()
    ok_meta, ev_meta = tem_metadados_com(s, "ano_plano_acao", "2024")  # aceita =2024, =eq.2024 etc.
    return [
        A("Entregou um arquivo .xlsx", bool(s.xlsx()), f"xlsx: {[p.name for p in s.xlsx()]}"),
        A("Dados vêm de planos-acao-especiais (colunas id_plano_acao e ano_plano_acao)", df is not None, f"aba: {nome}"),
        A("Todas as linhas têm ano_plano_acao = 2024", anos == {2024}, f"anos encontrados: {sorted(anos)[:10]}"),
        A(f"Nº de linhas igual ao contar com ano_plano_acao=2024 ({n_ref})", df is not None and len(df) == n_ref,
          f"linhas: {None if df is None else len(df)} · contar: {n_ref}"),
        A("Aba metadados registra o filtro usado", ok_meta, ev_meta),
    ]


def e2(s: Saida):
    n_ref = contar("fundoafundo", "programas-beneficiarios",
                   f"codigo_ibge_municipio_ente_beneficiario_programa={IBGE_UBERLANDIA}")
    nome, df = s.aba_com_linhas(n_ref)
    ok_mun, ev = False, f"nenhuma aba com {n_ref} linhas; abas: {[(n, len(d)) for n, d in s.dados_abas()]}"
    if df is not None:
        # alguma coluna (município, beneficiário, IBGE) identifica Uberlândia em TODAS as linhas
        for c in df.columns:
            v = df[c].astype(str).map(_norm)
            if v.str.contains("uberlandia").all() or v.str.contains(str(IBGE_UBERLANDIA)).all():
                ok_mun, ev = True, f"aba {nome}: coluna '{c}' identifica Uberlândia em todas as {len(df)} linhas"
                break
        else:
            ev = f"aba {nome}: nenhuma coluna identifica Uberlândia em todas as linhas"
    nao_vazia = any(len(d) > 0 for _, d in s.dados_abas())
    return [
        A("Entregou um arquivo .xlsx", bool(s.xlsx()), f"xlsx: {[p.name for p in s.xlsx()]}"),
        A("Planilha não está vazia (o usuário digitou 'Uberlandia' sem acento)", nao_vazia,
          f"abas: {[(n, len(d)) for n, d in s.dados_abas()]}"),
        A(f"Tem aba com os {n_ref} registros de Uberlândia (= contar por código IBGE {IBGE_UBERLANDIA})",
          df is not None, f"aba: {nome}"),
        A("Todas as linhas dessa aba são de Uberlândia", ok_mun, ev),
        nomes_da_api(s, "nome_municipio_ente_beneficiario_programa"),
        A("Há aba metadados", bool(s.metadados_texto()), "metadados presentes" if s.metadados_texto() else "ausentes"),
    ]


def e3(s: Saida):
    n_ref = planos_sp_total()
    nome, df = s.aba_com_linhas(n_ref)
    col_uf = coluna_como(df, "uf")
    ufs = set(df[col_uf].dropna().astype(str)) if col_uf else set()
    tem_benef = coluna_como(df, "benefici") is not None
    return [
        A("Entregou um arquivo .xlsx", bool(s.xlsx()), f"xlsx: {[p.name for p in s.xlsx()]}"),
        A(f"Tem aba com os {n_ref} planos de SP (verdade calculada)", df is not None,
          f"aba: {nome} · abas: {[(n, len(d)) for n, d in s.dados_abas()]}"),
        A("Cada plano traz o beneficiário (cruzou planos com beneficiários)", tem_benef,
          f"coluna de beneficiário: {coluna_como(df, 'benefici')}"),
        A("Coluna de UF presente e só com SP (o usuário consegue conferir o recorte)", ufs == {"SP"},
          f"coluna: {col_uf} · UFs: {sorted(ufs)[:5]}"),
        nomes_da_api(s, "id_plano_acao", "uf_beneficiario"),
        A("Há aba metadados", bool(s.metadados_texto()), "metadados presentes" if s.metadados_texto() else "ausentes"),
    ]


def e4(s: Saida):
    r = s.resposta.lower()
    volume = bool(re.search(r"1[.,]4\d{0,2}\s*(mi|milh)|1\.43\d\.\d{3}|1\.433|1,4 milh", r))
    sugere = any(x in r for x in ("filtr", "csv", "ano", "período", "periodo"))
    return [
        A("Não baixou a tabela inteira sem perguntar (nenhum xlsx/csv gerado)", not s.dados,
          f"arquivos de dados: {[p.name for p in s.dados]}"),
        A("Informou o volume (~1,4 milhão de linhas)", volume, s.resposta[:300]),
        A("Pergunta ao usuário antes de prosseguir", pergunta(s), "contém '?'" if pergunta(s) else "sem pergunta"),
        A("Sugere reduzir o volume (filtro) ou formato CSV", sugere, "menciona filtro/CSV/ano" if sugere else "não sugere"),
    ]


def e5(s: Saida):
    n_planos = contar("ted", "planos-acao")
    n_prog = contar("ted", "programas")
    nome_p, df_p = s.aba_com("id_plano_acao", "vl_total_plano_acao")
    # aba só de programas: tem colunas do programa e NÃO tem id_plano_acao (senão é a cruzada)
    progs = [(n, df) for n, df in s.abas.items() if not n.lower().endswith("metadados")
             and "tx_nome_programa" in df.columns and "id_plano_acao" not in df.columns]
    nome_g, df_g = max(progs, key=lambda x: len(x[1])) if progs else (None, None)
    # aba cruzada: tem colunas das duas tabelas (aceita prefixo/sufixo no nome da coluna do programa)
    cruz = [(n, df) for n, df in s.abas.items() if "id_plano_acao" in df.columns
            and any("tx_nome_programa" in str(c) for c in df.columns)]
    abas_dados = [n for n in s.abas if not n.lower().endswith("metadados")]
    return [
        A("Entregou um arquivo .xlsx", bool(s.xlsx()), f"xlsx: {[p.name for p in s.xlsx()]}"),
        A("Tem aba com os planos de ação de TED", df_p is not None, f"aba: {nome_p}"),
        A("Tem aba com os programas de TED", df_g is not None, f"aba: {nome_g}"),
        A("Tem aba cruzada (planos + dados do programa)", bool(cruz), f"abas: {abas_dados}"),
        A(f"Planos de ação completos (≥ 95% do contar = {n_planos})",
          df_p is not None and len(df_p) >= 0.95 * n_planos, f"linhas: {None if df_p is None else len(df_p)}"),
        A(f"Aba de programas completa (= contar {n_prog}; o usuário pediu uma aba por tabela, sem filtro)",
          df_g is not None and len(df_g) == n_prog, f"linhas: {None if df_g is None else len(df_g)}"),
        A("Há aba metadados", bool(s.metadados_texto()), "metadados presentes" if s.metadados_texto() else "ausentes"),
    ]


def e6(s: Saida):
    n_ref = sum(contar("especiais", "beneficiarios-especiais", f"uf_beneficiario={uf}") for uf in sorted(NORDESTE))
    csvs = s.csvs()
    p = csvs[0] if csvs else None
    bruto = p.read_bytes()[:4096] if p else b""
    df = s.abas.get(p.name) if p else None
    col_uf = coluna_como(df, "uf")
    ufs = set(df[col_uf].dropna()) if col_uf else set()
    return [
        A("Entregou CSV", bool(csvs), f"csv: {[x.name for x in csvs]}"),
        A("CSV em padrão pt-BR: separador ';' e UTF-8 com BOM", bruto.startswith(b"\xef\xbb\xbf") and b";" in bruto,
          f"BOM: {bruto.startswith(bytes.fromhex('efbbbf'))} · ';' no cabeçalho: {b';' in bruto.split(b'\n')[0] if bruto else False}"),
        A("Contém exatamente as 9 UFs do Nordeste", ufs == NORDESTE, f"UFs: {sorted(ufs)}"),
        A(f"Nº de linhas igual à soma do contar das 9 UFs ({n_ref})", df is not None and len(df) == n_ref,
          f"linhas: {None if df is None else len(df)} · contar: {n_ref}"),
        A("Metadados com os filtros acompanham a entrega", bool(s.metadados_texto()),
          "metadados presentes" if s.metadados_texto() else "ausentes"),
    ]


def e7(s: Saida):
    r = s.resposta.lower()
    # aceita nomes da api-publica e da API PostgREST antiga (ex.: ordem_pagamento_ordem_bancaria_especial)
    reais = [t for t in tg.tabelas("especiais") if t in r] + re.findall(r"\b[a-z_]+_especial\b", r)
    return [
        A("Não gerou planilha de uma tabela chutada", not s.dados, f"arquivos de dados: {[p.name for p in s.dados]}"),
        A("Explica que a tabela pedida não existe", any(x in r for x in ("não existe", "nao existe", "inexistente",
                                                                          "não há", "não encontr")), s.resposta[:300]),
        A("Cita tabelas reais do módulo especiais como alternativa", bool(reais), f"tabelas citadas: {reais[:5]}"),
        A("Pergunta qual tabela o usuário quer", pergunta(s), "contém '?'" if pergunta(s) else "sem pergunta"),
    ]


@lru_cache(maxsize=None)
def convenios_saude_2025() -> tuple[int, int]:
    """(todos os instrumentos, só modalidade CONVÊNIO) do MS assinados em 2025 — verdade do eval 8."""
    rs = tg.extrair_juntando("discricionarias", ["convenio", "proposta"],
                             ["proposta:COD_ORGAO_SUP=36000", "convenio:DIA_ASSIN_CONV>=2025-01-01",
                              "convenio:DIA_ASSIN_CONV<=2025-12-31"], "ID_PROPOSTA")
    df = rs[0].df
    col_mod = next((c for c in df.columns if c.upper().startswith("MODALIDADE")), None)
    so_conv = int(df[col_mod].astype(str).str.upper().str.contains("CONV").sum()) if col_mod else -1
    return len(df), so_conv


def e8(s: Saida):
    total, so_conv = convenios_saude_2025()
    nome, df = s.aba_com_linhas(total, so_conv)
    anos, orgao_ok = set(), False
    col_data = coluna_como(df, "assin")
    if col_data:
        anos = set(pd.to_datetime(df[col_data], errors="coerce", dayfirst=True).dt.year.dropna().astype(int))
    cols_org = [c for c in (df.columns if df is not None else []) if "orgao" in _norm(c)]
    if cols_org:
        org = df[cols_org].astype(str).agg(" ".join, axis=1).map(_norm)
        orgao_ok = bool(len(df)) and bool((org.str.contains("36000") | org.str.contains("saude")).all())
    return [
        A(f"Entregou aba com os convênios ({total} instrumentos ou {so_conv} só convênios = verdade calculada)",
          df is not None, f"aba: {nome} · abas: {[(n, len(d)) for n, d in s.dados_abas()]}"),
        A("Todos assinados em 2025", anos == {2025}, f"coluna: {col_data} · anos: {sorted(anos)}"),
        A("Todos do Ministério da Saúde (órgão superior 36000 / SAÚDE)", orgao_ok,
          f"colunas de órgão: {cols_org[:3]}" if orgao_ok else "faltam colunas de órgão ou há outro órgão"),
        nomes_da_api(s, "NR_CONVENIO", "DIA_ASSIN_CONV"),
        A("Há metadados", bool(s.metadados_texto()), "metadados presentes" if s.metadados_texto() else "ausentes"),
    ]


FERRAMENTAS_NAO_PEDIDAS = ("power bi", "power query", "sql server", "carregando no sql", "no sql")


def neutra(s: Saida) -> dict:
    r = s.resposta.lower()
    achou = [x for x in FERRAMENTAS_NAO_PEDIDAS if x in r]
    return A("Linguagem neutra: não sugere ferramentas que o usuário não citou (Power BI, SQL...)", not achou,
             f"citou: {achou}" if achou else "nenhuma ferramenta não pedida")


CORRETORES = {1: e1, 2: e2, 3: e3, 4: e4, 5: e5, 6: e6, 7: e7, 8: e8}


def main(iteracao: Path) -> None:
    for d in sorted(iteracao.glob("eval-*")):
        meta = json.loads((d / "eval_metadata.json").read_text(encoding="utf-8"))
        f = CORRETORES[meta["eval_id"]]
        textos = None
        for run in sorted(d.glob("*/run-*")):
            s = Saida(run / "outputs")
            try:
                exp = f(s) + [neutra(s)]
            except Exception as e:  # noqa: BLE001
                exp = [A("Correção executou sem erro", False, repr(e))]
            textos = textos or [x["text"] for x in exp]
            ok = sum(x["passed"] for x in exp)
            grading = {"expectations": exp,
                       "summary": {"passed": ok, "failed": len(exp) - ok, "total": len(exp),
                                   "pass_rate": round(ok / len(exp), 3) if exp else 0}}
            (run / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{d.name:45} {run.parent.name:14} {ok}/{len(exp)}", file=sys.stderr)
        if textos:
            meta["assertions"] = textos
            (d / "eval_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
