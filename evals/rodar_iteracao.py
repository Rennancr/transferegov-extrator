"""Roda uma iteração de evals com `claude -p` FORA do projeto (baseline limpo, sem CLAUDE.md nem memória).

Uso (desenvolvimento):
    python evals/rodar_iteracao.py 2 [--paralelo 4] [--so eval-3 ...]

Para cada eval e configuração (with_skill / without_skill):
- cria uma pasta temporária vazia fora do repositório e roda `claude -p` com ela como diretório de trabalho;
- with_skill recebe uma CÓPIA da skill dentro dessa pasta; without_skill não recebe nada;
- a ferramenta Skill fica bloqueada nas duas, para nenhuma skill instalada no usuário interferir;
- ao final copia outputs/ e o JSON da CLI para transferegov-extrator-workspace/iteration-N/.../run-1/.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / ".claude" / "skills" / "transferegov-extrator"
PYTHON = RAIZ / ".venv" / "Scripts" / "python.exe"
WORKSPACE = RAIZ / "transferegov-extrator-workspace"
MODELO = "claude-opus-5-5"
FERRAMENTAS = "Bash PowerShell Read Write Edit Glob Grep WebFetch WebSearch"  # no Windows o shell é PowerShell

REGRAS = """
- Python com requests, pandas e openpyxl instalados: {python} (use-o no lugar de `python`).
- Grave os arquivos para o usuário na pasta ./outputs (crie se não existir).
- O usuário NÃO pode responder durante a tarefa. Se você precisar perguntar algo antes de prosseguir, não
  prossiga: encerre e deixe a pergunta na resposta final.
- No fim, grave sua resposta final ao usuário (o texto exato que você mostraria a ele) em ./outputs/resposta.md.
- Não crie tarefas agendadas nem altere configurações do sistema.
"""

COM_SKILL = """Execute a tarefa do usuário abaixo como um assistente faria para um usuário real.
- Você tem uma skill para isso: leia e siga ./skill/SKILL.md (os caminhos `scripts/...` e `references/...`
  citados nela são relativos a ./skill).
{regras}
Tarefa do usuário: "{prompt}"
"""

SEM_SKILL = """Execute a tarefa do usuário abaixo como um assistente faria para um usuário real, usando seu
conhecimento e as ferramentas disponíveis (pode acessar a internet e escrever código; scripts temporários em
./trabalho).
{regras}
Tarefa do usuário: "{prompt}"
"""


def rodar(evento: dict, config: str, iteracao: Path, base_tmp: Path) -> str:
    nome = f"eval-{evento['id']}-{evento['name']}"
    destino = iteracao / nome / config / "run-1"
    trabalho = base_tmp / f"{nome}-{config}"
    shutil.rmtree(trabalho, ignore_errors=True)
    (trabalho / "outputs").mkdir(parents=True)
    regras = REGRAS.format(python=PYTHON.as_posix())
    if config == "with_skill":
        shutil.copytree(SKILL, trabalho / "skill", ignore=shutil.ignore_patterns("__pycache__"))
        prompt = COM_SKILL.format(regras=regras, prompt=evento["prompt"])
    else:
        prompt = SEM_SKILL.format(regras=regras, prompt=evento["prompt"])
    claude = shutil.which("claude") or "claude"   # caminho completo: sem shell, o prompt vai intacto
    cmd = [claude, "-p", prompt, "--output-format", "json", "--model", MODELO,
           "--allowedTools", *FERRAMENTAS.split(), "--disallowedTools", "Skill"]
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=trabalho, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=3600)
    dur = time.time() - t0
    destino.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(destino / "outputs", ignore_errors=True)
    shutil.copytree(trabalho / "outputs", destino / "outputs")
    (destino / "claude_stdout.json").write_text(proc.stdout, encoding="utf-8")
    if proc.stderr:
        (destino / "claude_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    try:
        saida = json.loads(proc.stdout)
        uso = saida.get("usage", {})
        tokens = sum(uso.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens",
                                             "cache_read_input_tokens"))
        dur_ms = saida.get("duration_ms", int(dur * 1000))
    except json.JSONDecodeError:
        tokens, dur_ms = 0, int(dur * 1000)
    (destino / "timing.json").write_text(json.dumps({"total_tokens": tokens, "duration_ms": dur_ms,
                                                     "total_duration_seconds": round(dur_ms / 1000, 1)}),
                                         encoding="utf-8")
    return f"{nome:45} {config:14} rc={proc.returncode} {dur:6.0f}s tokens={tokens}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("iteracao", type=int)
    ap.add_argument("--paralelo", type=int, default=4, help="execuções simultâneas (respeite a API pública)")
    ap.add_argument("--so", nargs="*", help="prefixos de eval a rodar, ex.: eval-3")
    a = ap.parse_args()

    evals = json.loads((RAIZ / "evals" / "evals.json").read_text(encoding="utf-8"))["evals"]
    iteracao = WORKSPACE / f"iteration-{a.iteracao}"
    # Caminho longo: o tempdir do Windows vem em 8.3 (ex.: USUARI~1) e aí o Claude Code não reconhece a pasta de
    # trabalho como "dentro do projeto" e nega as gravações.
    base_tmp = Path.home() / "AppData" / "Local" / "Temp" / "tg-evals" / f"iteration-{a.iteracao}" \
        if sys.platform == "win32" else Path(tempfile.gettempdir()) / "tg-evals" / f"iteration-{a.iteracao}"
    assert RAIZ not in base_tmp.parents, "a pasta de trabalho precisa ficar FORA do projeto"
    tarefas = []
    for e in evals:
        nome = f"eval-{e['id']}-{e['name']}"
        if a.so and not any(nome.startswith(p) for p in a.so):
            continue
        (iteracao / nome).mkdir(parents=True, exist_ok=True)
        (iteracao / nome / "eval_metadata.json").write_text(json.dumps(
            {"eval_id": e["id"], "eval_name": e["name"], "prompt": e["prompt"], "assertions": []},
            ensure_ascii=False, indent=2), encoding="utf-8")
        tarefas += [(e, "with_skill"), (e, "without_skill")]
    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        for linha in ex.map(lambda t: rodar(t[0], t[1], iteracao, base_tmp), tarefas):
            print(linha, flush=True)


if __name__ == "__main__":
    main()
