"""Paginação, filtros, verificações de integridade e política de retry."""
from __future__ import annotations

import json

import pytest
import responses

from conftest import ler_fixture, qs, tg

URL_PROG = f"{tg.BASE}/especiais/programas-especiais"


def linhas_benef(n: int, inicio: int = 1) -> list[dict]:
    ufs = ["SP", "RJ", "MG"]
    return [{"id_beneficiario": i, "uf_beneficiario": ufs[i % 3], "nome_beneficiario": f"MUNICIPIO {i}",
             "cnpj_beneficiario": f"{i:014d}", "id_ente": i * 10} for i in range(inicio, inicio + n)]


# ---------- paginação ----------

def test_para_quando_lote_menor_que_page_size_com_fixtures_reais(api):
    """15 linhas reais em páginas de 6: 6 + 6 + 3. Não deve pedir a página 4."""
    for p in (1, 2, 3):
        api.get(URL_PROG, json=ler_fixture(f"pagina_especiais_programas-especiais_p{p}_t6.json"),
                match=[responses.matchers.query_param_matcher({"pagina": str(p), "tamanho_da_pagina": "6"})])
    r = tg.extrair("especiais", "programas-especiais", [], tamanho_pagina=6)
    assert len(r.df) == 15
    paginas = [qs(c.request).get("pagina") for c in api.calls if c.request.url.startswith(URL_PROG)]
    assert paginas == ["1", "2", "3"]
    assert r.avisos == []


def test_para_quando_lote_vem_vazio(servir_tabela):
    """12 linhas em páginas de 6: a página 3 vem vazia e encerra."""
    chamadas = servir_tabela("especiais", "beneficiarios-especiais", linhas_benef(12))
    r = tg.extrair("especiais", "beneficiarios-especiais", [], tamanho_pagina=6)
    assert len(r.df) == 12
    assert [c["pagina"] for c in chamadas] == ["1", "2", "3"]


def test_page_size_padrao_vem_do_maximum_do_openapi(servir_tabela):
    ch_esp = servir_tabela("especiais", "beneficiarios-especiais", linhas_benef(5))
    ch_ted = servir_tabela("ted", "planos-acao-pareceres", [{"id_parecer": 1}])
    tg.extrair("especiais", "beneficiarios-especiais", [])
    tg.extrair("ted", "planos-acao-pareceres", [])
    assert ch_esp[0]["tamanho_da_pagina"] == "200"
    assert ch_ted[0]["tamanho_da_pagina"] == "1000"


def test_tamanho_pagina_acima_do_maximo_e_rejeitado_antes_da_api(api):
    with pytest.raises(tg.ErroTG, match="200"):
        tg.extrair("especiais", "beneficiarios-especiais", [], tamanho_pagina=500)


def test_trava_contra_paginacao_infinita(api, servir_tabela):
    """Servidor defeituoso que sempre devolve página cheia: para após total_pages e avisa."""
    def sempre_cheia(req):
        q = qs(req)
        corpo = {"data": linhas_benef(5, int(q["pagina"]) * 100), "total_pages": 2,
                 "total_items": 10, "page_number": int(q["pagina"]), "page_size": 5}
        return 200, {}, json.dumps(corpo)
    api.add_callback(responses.GET, f"{tg.BASE}/especiais/beneficiarios-especiais", callback=sempre_cheia)
    r = tg.extrair("especiais", "beneficiarios-especiais", [], tamanho_pagina=5)
    assert len(r.df) <= 15
    assert any("total_pages" in a or "parada" in a.lower() for a in r.avisos)


# ---------- filtros ----------

def test_filtro_desconhecido_lista_filtros_validos_e_nao_chama_api(api):
    with pytest.raises(tg.ErroTG) as e:
        tg.extrair("especiais", "beneficiarios-especiais", ["uf=SP"])
    msg = str(e.value)
    assert "uf_beneficiario" in msg and "nome_beneficiario" in msg
    assert not any("beneficiarios-especiais?" in c.request.url for c in api.calls)


def test_filtro_valida_enum_e_inteiro(api):
    with pytest.raises(tg.ErroTG, match="SP"):
        tg.contar("especiais", "beneficiarios-especiais", ["uf_beneficiario=XX"])
    with pytest.raises(tg.ErroTG, match="inteiro"):
        tg.contar("especiais", "beneficiarios-especiais", ["id_ente=abc"])


def test_filtro_enum_aceita_minusculas(servir_tabela):
    ch = servir_tabela("especiais", "beneficiarios-especiais", linhas_benef(3))
    tg.contar("especiais", "beneficiarios-especiais", ["uf_beneficiario=sp"])
    assert ch[0]["uf_beneficiario"] == "SP"


@pytest.mark.parametrize("f", ["id_ente=gte.10", "uf_beneficiario=in.(SP,RJ)"])
def test_sintaxe_postgrest_gera_erro_explicativo(api, f):
    with pytest.raises(tg.ErroTG, match="(?i)não suporta.*>="):
        tg.contar("especiais", "beneficiarios-especiais", [f])


def test_mesmo_filtro_repetido_vira_uma_chamada_por_valor(servir_tabela):
    """uf=SP + uf=RJ → 2 consultas (a API não aceita lista); resultado concatenado."""
    def por_uf(q, linhas):
        return [l for l in linhas if "uf_beneficiario" not in q or l["uf_beneficiario"] == q["uf_beneficiario"]]
    ch = servir_tabela("especiais", "beneficiarios-especiais", linhas_benef(9), filtro=por_uf)
    filtros = ["uf_beneficiario=SP", "uf_beneficiario=RJ"]
    assert tg.contar("especiais", "beneficiarios-especiais", filtros) == 6
    r = tg.extrair("especiais", "beneficiarios-especiais", filtros)
    assert sorted(r.df["uf_beneficiario"].unique()) == ["RJ", "SP"]
    assert len(r.df) == 6
    assert {c["uf_beneficiario"] for c in ch} == {"SP", "RJ"}


def test_valores_que_se_sobrepoem_nao_duplicam_linhas(servir_tabela):
    """Texto é 'contém': nome=AGUDO e nome=MORRO podem trazer a mesma linha."""
    linhas = [{"id_beneficiario": 1, "uf_beneficiario": "RS", "nome_beneficiario": "AGUDO",
               "cnpj_beneficiario": "1", "id_ente": 1},
              {"id_beneficiario": 2, "uf_beneficiario": "SP", "nome_beneficiario": "MORRO AGUDO",
               "cnpj_beneficiario": "2", "id_ente": 2}]

    def contem(q, ls):
        termo = q.get("nome_beneficiario", "").upper()
        return [l for l in ls if termo in l["nome_beneficiario"]]
    servir_tabela("especiais", "beneficiarios-especiais", linhas, filtro=contem)
    r = tg.extrair("especiais", "beneficiarios-especiais", ["nome_beneficiario=AGUDO", "nome_beneficiario=MORRO"])
    assert len(r.df) == 2


def test_zero_linhas_com_filtro_de_texto_avisa_sobre_acento(servir_tabela):
    """A API compara texto com acento: 'UBERLANDIA' não acha 'UBERLÂNDIA'."""
    def contem(q, ls):
        return [l for l in ls if q.get("nome_beneficiario", "") in l["nome_beneficiario"]]
    servir_tabela("especiais", "beneficiarios-especiais",
                  [{"id_beneficiario": 1, "uf_beneficiario": "MG", "nome_beneficiario": "UBERLÂNDIA",
                    "cnpj_beneficiario": "1", "id_ente": 1}], filtro=contem)
    r = tg.extrair("especiais", "beneficiarios-especiais", ["nome_beneficiario=UBERLANDIA"])
    assert len(r.df) == 0
    assert any("acento" in a for a in r.avisos)


# ---------- verificações de integridade ----------

def test_divergencia_entre_coletado_e_total_items_gera_aviso(servir_tabela):
    servir_tabela("especiais", "beneficiarios-especiais", linhas_benef(4), total=5)
    r = tg.extrair("especiais", "beneficiarios-especiais", [])
    assert len(r.df) == 4
    assert any("total_items" in a for a in r.avisos)


def test_duplicata_de_linha_inteira_gera_aviso_quando_nao_ha_pk(servir_tabela):
    ls = linhas_benef(3)
    servir_tabela("especiais", "beneficiarios-especiais", ls + [ls[0]])
    r = tg.extrair("especiais", "beneficiarios-especiais", [])
    assert any("duplicad" in a for a in r.avisos)


def test_duplicata_pela_pk_declarada(servir_tabela):
    """ted/planos-acao-pareceres declara primary_key em id_parecer."""
    assert tg.endpoint("ted", "planos-acao-pareceres").pk == ["id_parecer"]
    ls = [{"id_parecer": 1, "tx_parecer": "a"}, {"id_parecer": 1, "tx_parecer": "b"}]
    servir_tabela("ted", "planos-acao-pareceres", ls)
    r = tg.extrair("ted", "planos-acao-pareceres", [])
    assert any("id_parecer" in a for a in r.avisos)


def test_mudanca_de_data_atualizacao_durante_extracao_gera_aviso(api, servir_tabela):
    url = f"{tg.BASE}/especiais/data-atualizacao"
    api.remove(responses.GET, url)
    api.get(url, json={"data_ultima_atualizacao": "2026-10-15T00:00:00"})
    api.get(url, json={"data_ultima_atualizacao": "2026-10-16T00:00:00"})
    servir_tabela("especiais", "beneficiarios-especiais", linhas_benef(3))
    r = tg.extrair("especiais", "beneficiarios-especiais", [])
    assert any("atualizada durante" in a for a in r.avisos)
    assert r.meta["data_atualizacao_base"] == "2026-10-15T00:00:00"


# ---------- HTTP: retry e erros ----------

@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_retry_com_backoff_em_429_e_5xx(api, sem_espera, status):
    url = f"{tg.BASE}/especiais/beneficiarios-especiais"
    api.get(url, status=status)
    api.get(url, status=status)
    api.get(url, json={"data": [], "total_pages": 0, "total_items": 0, "page_number": 1, "page_size": 0})
    assert tg.contar("especiais", "beneficiarios-especiais", []) == 0
    backoffs = [s for s in sem_espera if s >= 1]
    assert backoffs[:2] == [1, 2]


def test_retry_respeita_retry_after(api, sem_espera):
    url = f"{tg.BASE}/especiais/beneficiarios-especiais"
    api.get(url, status=429, headers={"Retry-After": "7"})
    api.get(url, json={"data": [], "total_pages": 0, "total_items": 0, "page_number": 1, "page_size": 0})
    tg.contar("especiais", "beneficiarios-especiais", [])
    assert 7 in sem_espera


def test_desiste_apos_esgotar_tentativas(api):
    api.get(f"{tg.BASE}/especiais/beneficiarios-especiais", status=503)
    with pytest.raises(tg.ErroTG, match="503"):
        tg.contar("especiais", "beneficiarios-especiais", [])
    assert sum("beneficiarios" in c.request.url for c in api.calls) == tg.TENTATIVAS


@pytest.mark.parametrize("status", [400, 404, 422])
def test_erro_imediato_em_4xx(api, status):
    corpo = ler_fixture("erro_422_enum.json") if status == 422 else {"detail": "Not Found"}
    api.get(f"{tg.BASE}/especiais/beneficiarios-especiais", status=status, json=corpo)
    with pytest.raises(tg.ErroTG, match=str(status)):
        tg.contar("especiais", "beneficiarios-especiais", [])
    assert sum("beneficiarios" in c.request.url for c in api.calls) == 1


def test_user_agent_identificavel(servir_tabela, api):
    servir_tabela("especiais", "beneficiarios-especiais", [])
    tg.contar("especiais", "beneficiarios-especiais", [])
    assert all(c.request.headers["User-Agent"].startswith("transferegov-extrator/") for c in api.calls)


# ---------- descoberta ----------

def test_tabela_inexistente_lista_tabelas_validas(api):
    with pytest.raises(tg.ErroTG) as e:
        tg.endpoint("especiais", "beneficiarios")
    msg = str(e.value)
    assert "beneficiarios-especiais" in msg and "programas-especiais" in msg


def test_modulo_inexistente_lista_modulos(api):
    with pytest.raises(tg.ErroTG, match="especiais.*fundoafundo.*ted.*parcerias"):
        tg.tabelas("siafi")


def test_tabelas_vem_do_openapi_sem_data_atualizacao(api):
    ts = tg.tabelas("ted")
    assert len(ts) == 14 and "data-atualizacao" not in ts and "planos-acao-pareceres" in ts
    assert len(tg.tabelas("transferenciasespeciais")) == 23  # apelido antigo continua valendo
