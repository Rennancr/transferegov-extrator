"""Testes contra a API real. Rode só quando pedido: pytest -m online"""
from __future__ import annotations

import openpyxl
import pytest

from conftest import tg

pytestmark = pytest.mark.online


@pytest.fixture(autouse=True)
def sem_espera():  # sobrepõe o fixture do conftest: aqui as pausas são reais
    tg._cache_spec.clear()


def test_quatro_modulos_respondem():
    for m in ("especiais", "fundoafundo", "ted", "parcerias"):
        assert len(tg.tabelas(m)) > 5


def test_contar_e_extrair_batem(tmp_path):
    filtros = ["uf_beneficiario=AC"]
    n = tg.contar("especiais", "beneficiarios-especiais", filtros)
    r = tg.extrair("especiais", "beneficiarios-especiais", filtros, tamanho_pagina=20)
    assert len(r.df) == n > 0 and r.avisos == []
    [p] = tg.exportar([r], "xlsx", tmp_path, "ac")
    assert openpyxl.load_workbook(p)["beneficiarios-especiais"].max_row == n + 1
