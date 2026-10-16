"""Filtros de faixa (>=, <=, >, <): a API não suporta.

Inteiro com início e fim, quando a coluna é filtro da API, vira uma consulta por valor (exato, no servidor).
O resto é aplicado no pandas depois de baixar, e os metadados registram isso.
"""
from __future__ import annotations

import pytest

from conftest import tg


def planos(n_por_ano: int = 2, anos=range(2020, 2027)) -> list[dict]:
    ls, i = [], 1
    for ano in anos:
        for k in range(n_por_ano):
            ls.append({"id_plano_acao": i, "ano_plano_acao": ano, "valor_custeio_plano_acao": 1000.0 * k,
                       "data_aceite_plano_acao": f"{ano}-0{k + 1}-15"})
            i += 1
    return ls


def por_igualdade(q, linhas):
    """Simula o servidor: aplica os filtros de igualdade recebidos."""
    out = linhas
    for k, v in q.items():
        if k in ("pagina", "tamanho_da_pagina"):
            continue
        out = [l for l in out if str(l.get(k)) == v]
    return out


TAB = ("especiais", "planos-acao-especiais")


def test_faixa_inteira_fechada_vira_uma_consulta_por_valor(servir_tabela):
    ch = servir_tabela(*TAB, planos(), filtro=por_igualdade)
    r = tg.extrair(*TAB, ["ano_plano_acao>=2023", "ano_plano_acao<=2025"])
    assert sorted({c["ano_plano_acao"] for c in ch}) == ["2023", "2024", "2025"]
    assert len(r.df) == 6
    assert r.meta["linhas_baixadas"] == 6
    assert "local" not in r.meta["filtros"]


def test_faixa_com_limites_estritos(servir_tabela):
    ch = servir_tabela(*TAB, planos(), filtro=por_igualdade)
    tg.extrair(*TAB, ["ano_plano_acao>2022", "ano_plano_acao<2025"])
    assert sorted({c["ano_plano_acao"] for c in ch}) == ["2023", "2024"]


def test_contar_faixa_expandida_e_exato(servir_tabela):
    servir_tabela(*TAB, planos(), filtro=por_igualdade)
    assert tg.contar(*TAB, ["ano_plano_acao>=2023", "ano_plano_acao<=2025"]) == 6


def test_faixa_aberta_e_aplicada_localmente(servir_tabela):
    ch = servir_tabela(*TAB, planos(), filtro=por_igualdade)
    r = tg.extrair(*TAB, ["ano_plano_acao>=2025"])
    assert all("ano_plano_acao" not in c for c in ch)       # servidor recebeu sem o filtro
    assert sorted(r.df["ano_plano_acao"].unique()) == [2025, 2026]
    assert r.meta["linhas_baixadas"] == 14 and r.meta["linhas"] == 4
    assert "ano_plano_acao>=2025 (local)" in r.meta["filtros"]


def test_faixa_inteira_muito_larga_vai_para_local(servir_tabela, monkeypatch):
    monkeypatch.setattr(tg, "MAX_EXPANSAO_FAIXA", 3)
    ch = servir_tabela(*TAB, planos(), filtro=por_igualdade)
    r = tg.extrair(*TAB, ["ano_plano_acao>=2021", "ano_plano_acao<=2025"])
    assert len(ch) == 1 and len(r.df) == 10


def test_faixa_de_valor_e_data_combinada_com_igualdade_no_servidor(servir_tabela):
    ch = servir_tabela(*TAB, planos(), filtro=por_igualdade)
    r = tg.extrair(*TAB, ["ano_plano_acao=2024", "valor_custeio_plano_acao>=500",
                          "data_aceite_plano_acao<=2024-12-31"])
    assert {c.get("ano_plano_acao") for c in ch} == {"2024"}  # igualdade continua no servidor
    assert len(r.df) == 1 and r.df["valor_custeio_plano_acao"].iloc[0] == 1000.0


def test_faixa_combinada_com_igualdade_na_mesma_coluna(servir_tabela):
    ch = servir_tabela(*TAB, planos(), filtro=por_igualdade)
    r = tg.extrair(*TAB, ["ano_plano_acao=2020", "ano_plano_acao=2024", "ano_plano_acao>=2023",
                          "ano_plano_acao<=2025"])
    assert {c["ano_plano_acao"] for c in ch} == {"2024"}
    assert len(r.df) == 2


def test_faixa_vazia_ou_sem_intersecao_e_erro(api):
    with pytest.raises(tg.ErroTG, match="(?i)vazia"):
        tg.contar(*TAB, ["ano_plano_acao>=2025", "ano_plano_acao<=2023"])
    with pytest.raises(tg.ErroTG, match="(?i)vazia"):
        tg.contar(*TAB, ["ano_plano_acao=2020", "ano_plano_acao>=2023", "ano_plano_acao<=2025"])


def test_nulos_ficam_fora_da_faixa(servir_tabela):
    ls = planos(1, [2024]) + [{"id_plano_acao": 99, "ano_plano_acao": 2024, "valor_custeio_plano_acao": None}]
    servir_tabela(*TAB, ls, filtro=por_igualdade)
    r = tg.extrair(*TAB, ["valor_custeio_plano_acao>=0"])
    assert list(r.df["id_plano_acao"]) == [1]


def test_datetime_com_limite_so_de_data_inclui_o_dia_inteiro(servir_tabela):
    col = "dh_recebimento_programacao"
    ls = [{"id_programacao": 1, col: "2024-12-31T23:59:00"},
          {"id_programacao": 2, col: "2025-01-01T00:00:00"},
          {"id_programacao": 3, col: "2024-06-01T10:00:00"}]
    servir_tabela("ted", "programacoes-financeiras", ls)
    r = tg.extrair("ted", "programacoes-financeiras", [f"{col}<=2024-12-31"])
    assert sorted(r.df["id_programacao"]) == [1, 3]
    r = tg.extrair("ted", "programacoes-financeiras", [f"{col}>2024-12-31"])
    assert list(r.df["id_programacao"]) == [2]


@pytest.mark.parametrize("f,msg", [
    ("nome_beneficiario>=A", "numéric"),            # texto não tem faixa
    ("coluna_x>=1", "não existe"),
    ("id_ente>=abc", "inteiro"),
    ("id_ente!=3", "diferente"),
])
def test_faixas_invalidas(api, f, msg):
    with pytest.raises(tg.ErroTG, match=msg):
        tg.contar("especiais", "beneficiarios-especiais", [f])


def test_data_invalida_em_faixa(api):
    with pytest.raises(tg.ErroTG, match="AAAA-MM-DD"):
        tg.contar(*TAB, ["data_aceite_plano_acao>=01/01/2024"])


def test_cli_contar_avisa_que_faixa_local_reduz_depois(servir_tabela, capsys):
    servir_tabela(*TAB, planos(), filtro=por_igualdade)
    assert tg.main(["contar", "--modulo", "especiais", "--tabela", TAB[1], "-f", "valor_custeio_plano_acao>=500"]) == 0
    out, err = capsys.readouterr()
    assert out.strip() == "14" and "local" in err
