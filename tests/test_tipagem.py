"""Tipos vêm do schema de resposta (type/format), nunca da inferência do pandas."""
from __future__ import annotations

import json

import pandas as pd

from conftest import ler_fixture, tg


def test_tipos_das_fixtures_reais(api):
    ep = tg.endpoint("especiais", "programas-especiais")
    linhas = [l for p in (1, 2, 3) for l in ler_fixture(f"pagina_especiais_programas-especiais_p{p}_t6.json")["data"]]
    df = tg.tipar(pd.DataFrame(linhas), ep)
    assert str(df["id_programa"].dtype) == "Int64"
    assert str(df["valor_total_disponibilizado_programa"].dtype) == "Float64"
    assert pd.api.types.is_datetime64_any_dtype(df["data_inicio_ciencia_programa"])
    assert str(df["modalidade_programa"].dtype) == "string"


def test_coluna_toda_nula_nao_muda_dtype(api):
    ep = tg.endpoint("especiais", "programas-especiais")
    df = tg.tipar(pd.DataFrame([{"id_programa": None, "valor_impedido_programa": None,
                                 "data_fim_ciencia_programa": None}]), ep)
    assert str(df["id_programa"].dtype) == "Int64"
    assert str(df["valor_impedido_programa"].dtype) == "Float64"
    assert pd.api.types.is_datetime64_any_dtype(df["data_fim_ciencia_programa"])


def test_colunas_ausentes_sao_criadas_na_ordem_do_schema(api):
    ep = tg.endpoint("especiais", "programas-especiais")
    df = tg.tipar(pd.DataFrame([{"ano_programa": 2025}]), ep)
    assert list(df.columns) == [c.nome for c in ep.colunas]
    assert str(df["id_unidade_gestora_programa"].dtype) == "Int64"


def test_dataframe_vazio_mantem_colunas_e_tipos(api):
    ep = tg.endpoint("especiais", "programas-especiais")
    df = tg.tipar(pd.DataFrame(), ep)
    assert len(df) == 0 and list(df.columns) == [c.nome for c in ep.colunas]
    assert str(df["id_programa"].dtype) == "Int64"


def test_inteiro_grande_nao_vira_float(api):
    ep = tg.endpoint("especiais", "programas-especiais")
    # lista de dicts, como sai da API: DataFrame() direto já converteria para float e perderia o dígito
    df = tg.tipar([{"id_programa": 9007199254740993}, {"id_programa": None}], ep)
    assert df["id_programa"].iloc[0] == 9007199254740993


def test_datetime_e_boolean(api):
    ep = tg.endpoint("ted", "programacoes-financeiras")
    dt = next(c.nome for c in ep.colunas if c.formato == "date-time")
    df = tg.tipar(pd.DataFrame([{dt: "2024-03-01T14:30:00"}, {dt: None}]), ep)
    assert df[dt].iloc[0] == pd.Timestamp("2024-03-01 14:30:00")
    ep_b = tg.endpoint("ted", "programas")
    b = next(c.nome for c in ep_b.colunas if c.tipo == "boolean")
    df = tg.tipar(pd.DataFrame([{b: True}, {b: None}]), ep_b)
    assert str(df[b].dtype) == "boolean"


def test_objeto_aninhado_vira_colunas_tipadas(api):
    ep = tg.endpoint("fundoafundo", "gestao-financeira-lancamentos")
    nomes = [c.nome for c in ep.colunas]
    assert "categorias_despesa_lancamento__caminho_categoria_lancamento" in nomes
    assert "categorias_despesa_lancamento" not in nomes
    df = tg.tipar(pd.DataFrame([
        {"categorias_despesa_lancamento": {"caminho_categoria_lancamento": "A > B"}},
        {"categorias_despesa_lancamento": None},
    ]), ep)
    col = df["categorias_despesa_lancamento__caminho_categoria_lancamento"]
    assert col.iloc[0] == "A > B" and pd.isna(col.iloc[1])


def test_lista_aninhada_vira_json_texto(api):
    ep = tg.endpoint("parcerias", "programa")
    df = tg.tipar(pd.DataFrame([{"ufs_habilitadas": [{"sg_uf": "SP"}, {"sg_uf": "ãé"}]},
                                {"ufs_habilitadas": []}, {"ufs_habilitadas": None}]), ep)
    v = df["ufs_habilitadas"]
    assert json.loads(v.iloc[0]) == [{"sg_uf": "SP"}, {"sg_uf": "ãé"}]
    assert "ãé" in v.iloc[0]  # sem escape ã: legível no Excel
    assert v.iloc[1] == "[]" and pd.isna(v.iloc[2])


def test_data_invalida_vira_nula_e_gera_aviso(api):
    ep = tg.endpoint("especiais", "programas-especiais")
    avisos: list[str] = []
    df = tg.tipar(pd.DataFrame([{"data_inicio_ciencia_programa": "31/02/2024"}]), ep, avisos)
    assert pd.isna(df["data_inicio_ciencia_programa"].iloc[0])
    assert any("data_inicio_ciencia_programa" in a for a in avisos)
