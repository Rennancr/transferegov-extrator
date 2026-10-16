"""Gera .claude/skills/transferegov-extrator/references/<modulo>.md a partir do OpenAPI.

Uso (ferramenta de desenvolvimento, não vai no pacote da skill):
    python tools/gerar_references.py                 # usa os snapshots de tests/fixtures/
    python tools/gerar_references.py --online        # baixa o OpenAPI atual
    python tools/gerar_references.py --contagens     # inclui nº de linhas atual de cada tabela (1 chamada/tabela)

A interpretação do schema (colunas, tipos, filtros, PK) é a mesma do script da skill: importa tg_extract.
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
import time
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / ".claude" / "skills" / "transferegov-extrator"
FIXTURES = RAIZ / "tests" / "fixtures"
sys.path.insert(0, str(SKILL / "scripts"))
sys.dont_write_bytecode = True  # sem __pycache__ dentro da skill

import tg_extract as tg  # noqa: E402

MODULOS = ["especiais", "fundoafundo", "ted", "parcerias"]
LIMITE_INDICE = 300
MAX_ENUM_LISTADO = 10


def _celula(txt) -> str:
    return str(txt or "").replace("|", "\\|").replace("\n", " ").strip()


def _comparacao(f: tg.Filtro) -> str:
    if f.enum:
        vals = list(map(str, f.enum))
        if len(vals) <= MAX_ENUM_LISTADO:
            return "lista: " + ", ".join(vals)
        return f"lista ({len(vals)} valores; veja `colunas`)"
    if f.formato == "date" or (f.pattern and "\\d{4}" in f.pattern):
        return "igual (AAAA-MM-DD)"
    if f.tipo == "string":
        return "contém"
    return "igual"


def _dono_da_chave(chave: str, candidatas: list[str]) -> str | None:
    """Tabela 'dona' de uma chave id_*: entre as que a têm como 1ª coluna, a de nome mais parecido."""
    if not candidatas:
        return None
    raiz = chave.removeprefix("id_")
    return max(candidatas, key=lambda t: difflib.SequenceMatcher(None, raiz, t).ratio())


def _mapa_chaves(eps: list[tg.Endpoint]) -> dict[str, dict]:
    """chave id_* → {dono, tabelas}; só chaves presentes em 2+ tabelas."""
    tabelas_por_chave: dict[str, list[str]] = {}
    primeira: dict[str, list[str]] = {}
    for ep in eps:
        for i, c in enumerate(ep.colunas):
            if c.nome.startswith("id_") and not c.origem:
                tabelas_por_chave.setdefault(c.nome, []).append(ep.tabela)
                if i == 0 or c.pk:
                    primeira.setdefault(c.nome, []).append(ep.tabela)
    return {k: {"dono": _dono_da_chave(k, primeira.get(k, [])), "tabelas": ts}
            for k, ts in tabelas_por_chave.items() if len(ts) > 1}


def _info_op(s: dict, tabela: str) -> tuple[str, str, str]:
    op = s["paths"][f"/{tabela}"]["get"]
    return op.get("summary", ""), op.get("description", ""), ", ".join(op.get("tags", []))


def gerar(modulo: str, contagens: dict[str, int] | None, data_contagem: str | None) -> str:
    s = tg.spec(modulo)
    eps = [tg.endpoint(modulo, t) for t in tg.tabelas(modulo)]
    chaves = _mapa_chaves(eps)
    info = s.get("info", {})
    L: list[str] = []
    a = L.append

    a(f"# Módulo `{modulo}` — {info.get('title', '')}")
    a("")
    a(f"> Gerado por `tools/gerar_references.py` a partir do OpenAPI (versão {info.get('version', '?')}). "
      "Não edite à mão; regenere quando o schema mudar.")
    a("")
    a(f"- Endpoint base: `{tg.BASE}/{modulo}/<tabela>` · documentação: `{tg.BASE}/{modulo}/docs`")
    a(f"- Linhas por página (máximo): {eps[0].max_pagina if eps else '?'}")
    if contagens:
        a(f"- Volumes de **{data_contagem}**: mudam a cada carga diária. Use só para ter a ordem de grandeza e confirme com `contar`.")
    a("")

    a("## Índice")
    a("")
    cab = "| Tabela | Conteúdo | Colunas |" + (" Linhas (aprox.) |" if contagens else "")
    a(cab)
    a("|" + "---|" * (cab.count("|") - 1))
    for ep in eps:
        resumo, desc, _ = _info_op(s, ep.tabela)
        linha = f"| [`{ep.tabela}`](#{ep.tabela}) | {_celula(desc or resumo)} | {len(ep.colunas)} |"
        if contagens:
            n = contagens.get(ep.tabela)
            linha += f" {n:,} |".replace(",", ".") if isinstance(n, int) else " ? |"
        a(linha)
    a("")

    if chaves:
        a("## Chaves de junção prováveis")
        a("")
        a("Uma coluna `id_*` presente em várias tabelas costuma ser a chave da junção. A \"dona\" é a tabela em que "
          "a chave é a 1ª coluna (ou a PK); nas outras, ela funciona como referência. É uma heurística: confira os "
          "valores antes de confiar na junção.")
        a("")
        a("| Chave | Tabela dona (provável) | Também aparece em |")
        a("|---|---|---|")
        for k, v in sorted(chaves.items()):
            outras = [t for t in v["tabelas"] if t != v["dono"]]
            a(f"| `{k}` | {('`' + v['dono'] + '`') if v['dono'] else '—'} | {', '.join(f'`{t}`' for t in outras)} |")
        a("")

    a("## Tabelas")
    for ep in eps:
        resumo, desc, tag = _info_op(s, ep.tabela)
        a("")
        a(f"### {ep.tabela}")
        a("")
        a(f"{_celula(desc or resumo)}" + (f" Grupo: {tag}." if tag else ""))
        a("")
        meta = [f"PK: {', '.join(f'`{p}`' for p in ep.pk) if ep.pk else 'não declarada'}"]
        if contagens and isinstance(contagens.get(ep.tabela), int):
            meta.append(f"linhas em {data_contagem}: {contagens[ep.tabela]:,}".replace(",", "."))
        a("- " + " · ".join(meta))
        juncoes = []
        for c in ep.colunas:
            if c.nome in chaves:
                dono = chaves[c.nome]["dono"]
                if dono and dono != ep.tabela:
                    juncoes.append(f"`{c.nome}` → `{dono}`")
                elif dono == ep.tabela:
                    outras = [t for t in chaves[c.nome]["tabelas"] if t != ep.tabela]
                    juncoes.append(f"`{c.nome}` ← {', '.join(f'`{t}`' for t in outras)}")
        if juncoes:
            a("- Junções: " + "; ".join(juncoes))
        a("")
        a("| Coluna | Tipo | Filtro na API | Descrição |")
        a("|---|---|---|---|")
        for c in ep.colunas:
            f = ep.filtros.get(c.nome)
            tipo = (c.formato or c.tipo) + (" · PK" if c.pk else "")
            a(f"| `{c.nome}` | {tipo} | {_comparacao(f) if f else '—'} | {_celula(c.descricao)} |")
        extras = [f for n, f in ep.filtros.items() if n not in {c.nome for c in ep.colunas}]
        if extras:
            a("")
            a("Filtros aceitos pela API que não vêm como coluna na resposta: "
              + "; ".join(f"`{f.nome}` ({_comparacao(f)})" for f in extras) + ".")
    a("")
    return "\n".join(L)


def _comparacao_csv(nome: str, nomes: set[str]) -> tuple[str, str]:
    """(tipo, comparação) pela mesma convenção do script."""
    tipo, fmt = tg._tipo_csv(nome)
    if nome.upper().startswith("DIA_") and f"MES_{nome[4:]}".upper() in nomes:
        tipo, fmt = "integer", None
    if fmt == "date":
        return "date (dd/mm/aaaa no CSV)", "igual (AAAA-MM-DD) · faixa"
    if tipo in ("integer", "number"):
        return tipo, "igual · faixa"
    if tg._eh_codigo(nome):
        return "texto (código)", "igual"
    return "texto", "contém (ignora acento)"


def gerar_discricionarias(modelo: Path, listagem: Path) -> str:
    """Reference do módulo de CSVs a partir do modelo oficial (SchemaSpy) e da listagem do /downloads."""
    import xml.etree.ElementTree as ET
    raiz = ET.parse(modelo).getroot()
    arquivos = {}
    for b in ET.parse(listagem).getroot().iter("Blob"):
        n = b.findtext("Name") or ""
        if n.endswith(".zip") and not n.startswith("data_carga"):
            p = b.find("Properties")
            arquivos[n[:-4].removeprefix("siconv_")] = (n, int(p.findtext("Content-Length") or 0),
                                                         p.findtext("Last-Modified"))
    tabelas = {t.get("name").removeprefix("siconv_"): t for t in raiz.iter("table")}
    data_lista = next(iter(arquivos.values()))[2] if arquivos else "?"

    L: list[str] = []
    a = L.append
    a(f"# Módulo `{tg.MODULO_CSV}` — Transferências Discricionárias e Legais (convênios, contratos de repasse)")
    a("")
    a("> Gerado por `tools/gerar_references.py` a partir do modelo de dados oficial (SchemaSpy) e da listagem "
      "de `/downloads`. Não edite à mão.")
    a("")
    a("- **Não há API.** Os dados saem em CSVs (zip) em "
      f"`{tg.DOWNLOADS}`, atualizados diariamente. O script baixa o zip **inteiro** para um cache local "
      "e aplica os filtros localmente; o tempo depende do tamanho do arquivo.")
    a("- Apelidos aceitos em `--modulo`: `discricionarias`, `convenios`, `siconv`, `downloads`. `--tabela` é o "
      "nome do arquivo sem `siconv_` e sem `.zip` (ex.: `convenio`, `proposta`, `emenda`).")
    a("- **Texto** compara por *contém*, ignorando acento e maiúsculas; **códigos** (`ID_`, `COD_`, `NR_`, `CNPJ`, "
      "`UF_`...) comparam por igualdade exata; **datas e valores** aceitam faixa.")
    a(f"- Tamanhos da listagem de {data_lista}; confira o atual com `tabelas --modulo {tg.MODULO_CSV}`. "
      "Acima de ~200 MB, avise o usuário antes: o download e a leitura levam minutos.")
    a("")
    a("## Por onde começar")
    a("")
    a("| Pedido | Arquivos | Junção |")
    a("|---|---|---|")
    a("| Convênios/contratos de repasse (situação, vigência, valores) | `convenio` | — |")
    a("| ...de um órgão (ministério), UF ou município | `convenio` + `proposta` | `ID_PROPOSTA` (órgão: "
      "`COD_ORGAO_SUP`/`DESC_ORGAO_SUP`; local: `UF_PROPONENTE`, `COD_MUNIC_IBGE`) |")
    a("| Emendas parlamentares em convênios | `emenda` + `convenio`/`proposta` | `ID_PROPOSTA` |")
    a("| Empenhos, desembolsos, pagamentos | `empenho`, `desembolso`, `pagamento` | `NR_CONVENIO` |")
    a("| Programas | `programa` + `programa_proposta` | `ID_PROGRAMA`, `ID_PROPOSTA` |")
    a("")

    a("## Índice")
    a("")
    a("| Arquivo (`--tabela`) | Tamanho do zip | Colunas | PK |")
    a("|---|---|---|---|")
    for t in sorted(arquivos):
        blob, tam, _ = arquivos[t]
        tb = tabelas.get(t)
        cols = len(tb.findall("column")) if tb is not None else "—"
        pk = ", ".join(f"`{p.get('column')}`" for p in tb.findall("primaryKey")) if tb is not None else ""
        alvo = f"[`{t}`](#{t})" if tb is not None else f"`{t}` (sem modelo; use `colunas`)"
        a(f"| {alvo} | {tam / 1e6:,.1f} MB | {cols} | {pk or '—'} |".replace(",", "X").replace(".", ",").replace("X", "."))
    a("")

    a("## Chaves de junção (chaves estrangeiras do modelo oficial)")
    a("")
    a("| Chave | Tabela dona | Referenciada por |")
    a("|---|---|---|")
    for t, tb in sorted(tabelas.items()):
        for c in tb.findall("column"):
            filhos = sorted({ch.get("table").removeprefix("siconv_") for ch in c.findall("child")})
            if filhos:
                a(f"| `{c.get('name')}` | `{t}` | {', '.join(f'`{f}`' for f in filhos)} |")
    a("")

    a("## Arquivos")
    for t in sorted(arquivos):
        tb = tabelas.get(t)
        if tb is None:
            continue
        nomes = {c.get("name").upper() for c in tb.findall("column")}
        a("")
        a(f"### {t}")
        a("")
        if tb.get("remarks"):
            a(_celula(tb.get("remarks")))
            a("")
        a(f"- Arquivo: `{arquivos[t][0]}`")
        a("")
        a("| Coluna | Tipo | Filtro | Descrição |")
        a("|---|---|---|---|")
        for c in tb.findall("column"):
            tipo, comp = _comparacao_csv(c.get("name"), nomes)
            a(f"| `{c.get('name')}` | {tipo} | {comp} | {_celula(c.get('remarks'))} |")
    a("")
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modulos", nargs="*", default=MODULOS)
    ap.add_argument("--online", action="store_true", help="baixa o OpenAPI atual em vez dos snapshots")
    ap.add_argument("--contagens", action="store_true", help="inclui o nº de linhas atual de cada tabela")
    a = ap.parse_args()

    destino = SKILL / "references"
    destino.mkdir(parents=True, exist_ok=True)
    for m in a.modulos:
        if not a.online:
            tg._cache_spec[m] = json.loads((FIXTURES / f"openapi_{m}.json").read_text(encoding="utf-8"))
        contagens = None
        if a.contagens:
            contagens = {}
            for t in tg.tabelas(m):
                ep = tg.endpoint(m, t)
                contagens[t] = tg._pagina(ep, {}, 1, 1)["total_items"]
                time.sleep(tg.PAUSA_ENTRE_PAGINAS)
        md = gerar(m, contagens, date.today().strftime("%d/%m/%Y") if contagens else None)
        arq = destino / f"{m}.md"
        arq.write_text(md, encoding="utf-8")
        print(f"{arq} ({md.count(chr(10)) + 1} linhas)", file=sys.stderr)

    # Discricionárias: modelo oficial + listagem (snapshots em tests/fixtures; --online atualiza a listagem)
    listagem = FIXTURES / "downloads_listagem.xml"
    if a.online:
        r = tg._get(tg.DOWNLOADS, params={"restype": "container", "comp": "list"})
        listagem.write_bytes(r.content)
    md = gerar_discricionarias(FIXTURES / "modelo_discricionarias.xml", listagem)
    arq = destino / f"{tg.MODULO_CSV}.md"
    arq.write_text(md, encoding="utf-8")
    print(f"{arq} ({md.count(chr(10)) + 1} linhas)", file=sys.stderr)


if __name__ == "__main__":
    main()
