"""Salva o OpenAPI de cada módulo do TransfereGov em tests/fixtures/openapi_<modulo>.json.

Uso (ferramenta de desenvolvimento, não vai no pacote da skill):
    python tools/snapshot_schemas.py            # todos os módulos
    python tools/snapshot_schemas.py ted        # só um

Os módulos expõem OpenAPI 3.1 em /<modulo>/openapi.json (FastAPI), não PostgREST.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

BASE = "https://api-publica.transferegov.gestao.gov.br"
MODULOS = ["especiais", "fundoafundo", "ted", "parcerias"]
USER_AGENT = "transferegov-extrator/0.1 (dev; snapshot_schemas)"
DESTINO = Path(__file__).resolve().parent.parent / "tests" / "fixtures"


def baixar(modulo: str) -> Path:
    r = requests.get(f"{BASE}/{modulo}/openapi.json", headers={"User-Agent": USER_AGENT}, timeout=60)
    r.raise_for_status()
    spec = r.json()
    DESTINO.mkdir(parents=True, exist_ok=True)
    arq = DESTINO / f"openapi_{modulo}.json"
    # ensure_ascii=False + indent: diff legível quando o schema mudar
    arq.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    n = sum(1 for p in spec.get("paths", {}) if p != "/data-atualizacao")
    print(f"{modulo}: {n} endpoints de dados, versão {spec.get('info', {}).get('version')}", file=sys.stderr)
    return arq


def main(argv: list[str]) -> None:
    for m in argv or MODULOS:
        if m not in MODULOS:
            raise SystemExit(f"Módulo '{m}' desconhecido. Válidos: {', '.join(MODULOS)}")
        print(baixar(m))


if __name__ == "__main__":
    main(sys.argv[1:])
