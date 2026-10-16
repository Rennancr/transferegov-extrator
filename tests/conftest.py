"""Infra de teste: importa o script da skill e simula a API com `responses`.

O OpenAPI vem dos snapshots reais em tests/fixtures/. As páginas de dados podem vir das fixtures gravadas
ou ser geradas por `servir_tabela`, que fatia uma lista de linhas como o servidor faria
(`pagina` + `tamanho_da_pagina` → envelope com total_items/total_pages).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
import responses

RAIZ = Path(__file__).resolve().parent.parent
FIXTURES = RAIZ / "tests" / "fixtures"
sys.path.insert(0, str(RAIZ / ".claude" / "skills" / "transferegov-extrator" / "scripts"))
sys.dont_write_bytecode = True  # sem __pycache__ dentro da skill: o .pyc embute caminhos desta máquina

import tg_extract as tg  # noqa: E402

MODULOS = ["especiais", "fundoafundo", "ted", "parcerias"]
DATA_BASE = "2026-10-15T00:00:00"


def ler_fixture(nome: str):
    return json.loads((FIXTURES / nome).read_text(encoding="utf-8"))


def envelope(linhas: list[dict], pagina: int, tamanho: int, total: int | None = None) -> dict:
    total = len(linhas) if total is None else total
    fatia = linhas[(pagina - 1) * tamanho: pagina * tamanho]
    return {"data": fatia, "total_pages": math.ceil(total / tamanho) if tamanho else 0,
            "total_items": total, "page_number": pagina, "page_size": len(fatia)}


def qs(req) -> dict[str, str]:
    return {k: v[0] for k, v in parse_qs(urlparse(req.url).query).items()}


@pytest.fixture(autouse=True)
def sem_espera(monkeypatch):
    """Zera sleeps (backoff e pausa entre páginas) e registra as esperas pedidas."""
    esperas: list[float] = []
    monkeypatch.setattr(tg.time, "sleep", lambda s: esperas.append(s))
    tg._cache_spec.clear()
    return esperas


@pytest.fixture
def api():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        for m in MODULOS:
            rsps.get(f"{tg.BASE}/{m}/openapi.json", json=ler_fixture(f"openapi_{m}.json"))
            rsps.get(f"{tg.BASE}/{m}/data-atualizacao", json={"data_ultima_atualizacao": DATA_BASE})
        yield rsps


@pytest.fixture
def servir_tabela(api):
    """Registra um endpoint que pagina `linhas` de verdade.

    `filtro` (opcional) recebe o dict da query e devolve as linhas que o servidor retornaria;
    `total` força um total_items diferente do real (simula base mudando).
    Devolve a lista de chamadas para inspeção.
    """
    def _registrar(modulo: str, tabela: str, linhas: list[dict], filtro=None, total=None):
        chamadas: list[dict] = []

        def cb(req):
            q = qs(req)
            chamadas.append(q)
            base = filtro(q, linhas) if filtro else linhas
            corpo = envelope(base, int(q.get("pagina", 1)), int(q.get("tamanho_da_pagina", 50)), total)
            return 200, {}, json.dumps(corpo)

        api.add_callback(responses.GET, f"{tg.BASE}/{modulo}/{tabela}", callback=cb)
        return chamadas
    return _registrar
