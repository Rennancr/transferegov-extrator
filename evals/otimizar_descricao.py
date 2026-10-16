"""Roda o run_eval / run_loop da skill-creator no Windows (ferramenta de desenvolvimento).

O run_eval original tem dois problemas aqui, e os dois fazem cada consulta virar "não acionou" em silêncio:
1. lê o stream do `claude -p` com select.select(), que no Windows só aceita sockets;
2. encerra no primeiro `message_stop`, mas com extended thinking o raciocínio fecha uma mensagem antes da
   chamada da ferramenta.
Aqui, só neste processo:
- run_single_query lê o stdout numa thread e decide na 1ª ferramenta chamada (ou no fim);
- ProcessPoolExecutor vira ThreadPoolExecutor (processos filhos no Windows reimportariam o módulo sem o ajuste).
Nada é alterado nos arquivos da skill-creator.

Uso, a partir de uma pasta temporária limpa que tenha um .claude/ vazio (sem CLAUDE.md nem skills do projeto):
    PYTHONUTF8=1 python <repo>/evals/otimizar_descricao.py <caminho-skill-creator> eval  --eval-set ... (args do run_eval)
    PYTHONUTF8=1 python <repo>/evals/otimizar_descricao.py <caminho-skill-creator> loop  --eval-set ... (args do run_loop)
"""
from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


# Ferramentas de "preparação" que não indicam decisão: com muitas ferramentas adiadas, o modelo pode carregar
# esquemas (ToolSearch) ou planejar (TodoWrite) antes de escolher entre a skill e agir por conta própria.
NEUTRAS = {"ToolSearch", "TodoWrite"}
TIMEOUT_MELHORIA = 900   # o original usa 300 s; com o SKILL.md inteiro no prompt, o Opus passa disso no Windows


def run_single_query(query: str, skill_name: str, skill_description: str, timeout: int, project_root: str,
                     model: str | None = None) -> bool:
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    # Pasta de projeto PRÓPRIA por consulta: na pasta compartilhada do original, cada sessão enxerga os comandos
    # das outras (e sobras de execuções interrompidas), aciona a "cópia" errada e conta como não acionou.
    # Irmã (não filha) da raiz: o Claude Code também lê .claude/ de pastas-pai, e o da raiz vazaria para cá.
    project_root = str(Path(project_root).parent / f"{Path(project_root).name}-consultas" / unique_id)
    comandos = Path(project_root) / ".claude" / "commands"
    arquivo = comandos / f"{clean_name}.md"
    try:
        comandos.mkdir(parents=True, exist_ok=True)
        desc = "\n  ".join(skill_description.split("\n"))
        arquivo.write_text(f"---\ndescription: |\n  {desc}\n---\n\n# {skill_name}\n\n"
                           f"This skill handles: {skill_description}\n", encoding="utf-8")
        # --strict-mcp-config sem servidores: cada sessão não sobe os servidores MCP configurados (bancos, navegador...).
        # Fica leve (10 sessões com MCP travaram a máquina) e mais próxima de um usuário genérico.
        cmd = [shutil.which("claude") or "claude", "-p", query, "--output-format", "stream-json", "--verbose",
               "--include-partial-messages", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
        if model:
            cmd += ["--model", model]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=project_root, env=env)
        linhas: queue.Queue = queue.Queue()

        def ler():
            for linha in iter(proc.stdout.readline, b""):
                linhas.put(linha)
            linhas.put(None)

        threading.Thread(target=ler, daemon=True).start()
        inicio, pendente, acumulado = time.time(), None, ""
        try:
            while time.time() - inicio < timeout:
                try:
                    bruto = linhas.get(timeout=1.0)
                except queue.Empty:
                    continue
                if bruto is None:
                    return False
                try:
                    ev = json.loads(bruto.decode("utf-8", errors="replace"))
                except json.JSONDecodeError:
                    continue
                if ev.get("type") == "stream_event":
                    se = ev.get("event", {})
                    tipo = se.get("type", "")
                    if tipo == "content_block_start":
                        cb = se.get("content_block", {})
                        if cb.get("type") == "tool_use":
                            if cb.get("name", "") in ("Skill", "Read"):
                                pendente, acumulado = cb.get("name"), ""
                            elif cb.get("name", "") in NEUTRAS:
                                continue
                            else:
                                return False
                    elif tipo == "content_block_delta" and pendente:
                        d = se.get("delta", {})
                        if d.get("type") == "input_json_delta":
                            acumulado += d.get("partial_json", "")
                            if clean_name in acumulado:
                                return True
                    elif tipo in ("content_block_stop", "message_stop"):
                        # Com extended thinking, o bloco de raciocínio fecha uma mensagem ANTES da chamada da
                        # ferramenta; o original devolvia False aqui. Decide-se na 1ª ferramenta ou no 'result'.
                        if pendente:
                            return clean_name in acumulado
                elif ev.get("type") == "assistant":
                    for item in ev.get("message", {}).get("content", []):
                        if item.get("type") != "tool_use" or item.get("name") in NEUTRAS:
                            continue
                        nome, entrada = item.get("name", ""), item.get("input", {})
                        return (nome == "Skill" and clean_name in entrada.get("skill", "")) or \
                               (nome == "Read" and clean_name in entrada.get("file_path", ""))
                elif ev.get("type") == "result":
                    return False
            return False
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
    finally:
        arquivo.unlink(missing_ok=True)
        shutil.rmtree(Path(project_root), ignore_errors=True)  # só a pasta desta consulta


def main() -> None:
    skill_creator, modo, *resto = sys.argv[1:]
    sys.path.insert(0, skill_creator)
    import scripts.run_eval as run_eval_mod
    run_eval_mod.run_single_query = run_single_query
    run_eval_mod.ProcessPoolExecutor = ThreadPoolExecutor
    sys.argv = [f"scripts.run_{modo}", *resto]
    if modo == "eval":
        run_eval_mod.main()
    else:
        import scripts.improve_description as imp
        original = imp._call_claude
        imp._call_claude = lambda prompt, model, timeout=300: original(prompt, model, timeout=TIMEOUT_MELHORIA)
        import scripts.run_loop as run_loop_mod
        run_loop_mod.main()


if __name__ == "__main__":
    main()
