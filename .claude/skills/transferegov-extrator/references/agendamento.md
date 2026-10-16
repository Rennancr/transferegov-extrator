# Receber os dados todo dia, automaticamente

A base do TransfereGov é recarregada **uma vez por dia**: `GET /<modulo>/data-atualizacao` informa a data da
última carga. Como a API não oferece extração incremental ("só o que mudou"), uma rotina diária baixa tudo de
novo. O script economiza esse trabalho quando a base não mudou.

## O comando da rotina

Monte e teste primeiro o comando manual com o usuário: tabela, filtros e formato. Depois acrescente:

- `--arquivo NOME`: nome **fixo**, sem data. Cada execução substitui o arquivo da anterior.
- `--so-se-atualizou`: se a base e os parâmetros são os mesmos da execução anterior (lidos dos metadados
  do arquivo existente), não baixa nada e mantém o arquivo.
- `--saida PASTA`: caminho **absoluto**, porque o agendador não roda na pasta do usuário.
- `--estrito` (opcional): termina com código 3 quando houver avisos de integridade, para o agendador
  registrar que algo merece atenção.

A gravação é atômica: quem abrir o arquivo durante uma execução vê a versão anterior completa, nunca um
arquivo pela metade. Se o arquivo estiver aberto no Excel no momento da troca, a execução falha com uma
mensagem pedindo para fechá-lo, e a próxima execução tenta de novo.

Códigos de saída: `0` ok (ou mantido sem mudança) · `1` erro · `2` uso incorreto · `3` ok com avisos (`--estrito`).

## Agendar

Use caminhos absolutos para o Python, o script e a pasta de saída. Horário sugerido: começo da manhã, depois
da carga diária. Rode o comando uma vez à mão antes de agendar.

**Windows (Agendador de Tarefas), em um prompt do usuário:**

```
schtasks /Create /TN "TransfereGov - <nome>" /SC DAILY /ST 07:00 /TR "\"C:\caminho\python.exe\" \"C:\caminho\skill\scripts\tg_extract.py\" extrair --modulo especiais --tabela planos-acao-especiais -f ano_plano_acao=2025 --saida \"C:\caminho\saida\" --arquivo emendas_2025 --so-se-atualizou"
```

Para guardar o log, crie um `.cmd` com o comando e ` >> "C:\caminho\saida\log.txt" 2>&1` no fim, e agende o
`.cmd`.

**Linux/macOS (cron), via `crontab -e`:**

```
0 7 * * * /caminho/python /caminho/skill/scripts/tg_extract.py extrair --modulo especiais --tabela planos-acao-especiais -f ano_plano_acao=2025 --saida /caminho/saida --arquivo emendas_2025 --so-se-atualizou >> /caminho/saida/log.txt 2>&1
```

## O que dizer ao usuário

- O agendamento roda **na máquina dele**, que precisa estar ligada e com internet no horário.
- Tabelas muito grandes (centenas de milhares de linhas ou mais) levam de minutos a cerca de uma hora a cada
  carga nova. Se possível, use filtros que reduzam o volume, e prefira CSV para esse porte.
- Para conferir uma execução: a aba `metadados` traz `extraido_em` e `data_atualizacao_base`.
- Para parar: Windows, `schtasks /Delete /TN "TransfereGov - <nome>"`; cron, remover a linha.

Não crie o agendamento sem o usuário confirmar o comando, o horário e a pasta: é uma ação que fica rodando
na máquina dele.
