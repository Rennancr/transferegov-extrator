# TransfereGov → planilha (skill do Claude)

![testes](https://img.shields.io/badge/testes-91%20passando-brightgreen)
![cobertura](https://img.shields.io/badge/cobertura-89%25-brightgreen)
![python](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue)
![licença](https://img.shields.io/badge/licen%C3%A7a-MIT-lightgrey)

Skill do [Claude](https://claude.ai) que busca **dados abertos do TransfereGov** e entrega **planilha Excel ou
CSV**, a partir de um pedido em linguagem natural:

> "quero as emendas Pix de 2025 do meu município, Caruaru-PE, numa planilha"
>
> "convênios do Ministério da Saúde assinados em 2025, em Excel"
>
> "planos de ação de TED com os dados do programa, uma aba para cada tabela"

Você não precisa conhecer a API, os nomes das tabelas nem os filtros. A skill descobre tudo, confere o volume
antes de baixar e devolve a planilha com uma aba de **metadados**: fonte, filtros usados, número de linhas e
data da base.

## O que ela cobre

| Módulo | O que é |
|---|---|
| **Transferências Especiais** | Emendas parlamentares individuais, as "emendas Pix": planos de ação, beneficiários, empenhos, pagamentos |
| **Fundo a Fundo** | Repasses da União para fundos estaduais e municipais |
| **TED** | Termos de Execução Descentralizada entre órgãos federais |
| **Gestão de Parcerias** | Propostas e parcerias com organizações da sociedade civil |
| **Discricionárias e Legais** | Convênios e contratos de repasse (antigo Siconv / Plataforma +Brasil) |

Fonte: [api-publica.transferegov.gestao.gov.br](https://api-publica.transferegov.gestao.gov.br), a API
pública oficial, sem login nem token. Convênios saem dos arquivos de `/downloads`, atualizados diariamente.

## Como instalar

### Instalação rápida (Claude Code e outros agentes) · recomendada
Com o [Node.js](https://nodejs.org) instalado, rode no terminal:

```bash
npx skills add Rennancr/transferegov-extrator -a claude-code -g
```

- Com `-g`, a skill vale em **todas as pastas**. Sem `-g`, só no projeto em que o comando foi rodado.
- **Atualizar** para a versão mais recente: `npx skills update transferegov-extrator -g`
- **Remover:** `npx skills remove transferegov-extrator`
- **Outros agentes:** troque `-a claude-code` pelo agente desejado, ou use `-a '*'` para todos os suportados.

A instalação usa a CLI aberta [skills](https://github.com/vercel-labs/skills), que lista a skill no
[skills.sh](https://www.skills.sh). A CLI envia uma contagem anônima de instalações; para desativar, defina a
variável `DISABLE_TELEMETRY=1` antes do comando.

### Pelo arquivo `.skill` (claude.ai, ou sem Node.js)
Baixe o arquivo **[`dist/transferegov-extrator.skill`](dist/transferegov-extrator.skill)**: abra o link e
clique em *Download raw file*.

#### No claude.ai
1. Abra **Configurações → Skills** (o nome do menu pode variar conforme o plano).
2. Envie o arquivo `transferegov-extrator.skill`.
3. Numa conversa, peça os dados normalmente. A skill é acionada sozinha.

É preciso ter **execução de código** habilitada. Se a sua organização restringe a rede, o domínio
`api-publica.transferegov.gestao.gov.br` precisa estar liberado.

#### No Claude Code, sem a CLI
O `.skill` é um arquivo zip. Extraia o conteúdo em `~/.claude/skills/` (no Windows,
`C:\Users\<seu usuário>\.claude\skills\`), de modo que fique assim:

```
~/.claude/skills/transferegov-extrator/SKILL.md
```

A partir daí, a skill vale em qualquer pasta. Outra opção é clonar este repositório e abrir o Claude Code
dentro dele: a skill já está em `.claude/skills/` e é carregada automaticamente.

### Requisitos
- Python com as 3 bibliotecas da seção [Dependências](#dependências). No claude.ai, o ambiente já costuma
  ter. No Claude Code: `pip install -r requirements.txt`.
- Acesso à internet para `api-publica.transferegov.gestao.gov.br`.

## Dependências

A skill usa **só três bibliotecas**, de propósito: cada dependência a mais é um risco de algo ficar
obsoleto ou mudar de comportamento numa atualização. Todo o resto é biblioteca padrão do Python.

| Biblioteca | Para quê | Faixa aceita | Versões testadas |
|---|---|---|---|
| [requests](https://pypi.org/project/requests/) | chamadas HTTP à API e download dos arquivos | `>=2.31,<3` | 2.31.0 · 2.34.2 |
| [pandas](https://pypi.org/project/pandas/) | tipagem, filtros locais, junções e exportação | `>=2.2,<4` | 2.2.3 · 2.3.3 · 3.0.6 |
| [openpyxl](https://pypi.org/project/openpyxl/) | escrita do `.xlsx` (usada pelo pandas) | `>=3.1,<4` | 3.1.0 · 3.1.5 |

- **Python testado:** 3.13 e 3.14.
- Os 91 testes passam tanto com o **conjunto mínimo** (Python 3.13, requests 2.31.0, pandas 2.2.3,
  openpyxl 3.1.0) quanto com o **conjunto atual** (Python 3.14, requests 2.34.2, pandas 3.0.6,
  openpyxl 3.1.5).
- O openpyxl 3.1.0 funciona, mas emite um aviso interno de descontinuação; a versão recomendada é a **3.1.5**.
- O teto de cada faixa (`<próxima versão major`) evita que uma versão futura com mudanças incompatíveis
  quebre a skill sem aviso.

Só para desenvolvimento: `pytest`, `responses` (simula a API nos testes) e `pytest-cov` (cobertura). Veja
`requirements-dev.txt`.

## O que esperar

- **Pedidos vagos funcionam.** "Emendas Pix de SP" vira o cruzamento dos planos de ação com os
  beneficiários de SP, porque a UF só existe nessa segunda tabela.
- **Volume grande é confirmado antes.** Acima de 500 mil linhas, ou de arquivos grandes, a skill informa o
  tamanho e o tempo estimado, e pergunta como seguir.
- **Filtros:** ano, UF, município, faixas de valor e data, vários valores ao mesmo tempo. Para municípios,
  ela prefere o código IBGE, porque a busca por nome na API diferencia acentos.
- **Conferência automática:** a API não tem ordenação, então a skill confere o total baixado, a
  ausência de duplicatas e se a base mudou durante a extração, e avisa quando algo não bate.
- **Formatos:** `.xlsx`, com uma aba por tabela e outra cruzada quando pedido, ou `.csv` no padrão
  brasileiro (`;`, vírgula decimal, UTF-8), que abre direto no Excel.
- **Todo dia, automaticamente:** a skill monta o comando para agendar no Windows (Agendador de Tarefas)
  ou no Linux/macOS (cron). Se a base não mudou desde a última execução, ela não baixa nada de novo.

## Estrutura do repositório

```
.claude/skills/transferegov-extrator/   ← a skill (o que vai no .skill)
├── SKILL.md                            fluxo e regras que o Claude segue
├── scripts/tg_extract.py               CLI que faz o trabalho (descoberta, filtros, paginação, exportação)
└── references/                         documentação por módulo (gerada) + filtros e agendamento
dist/transferegov-extrator.skill        pacote pronto para instalar
tests/                                  testes automatizados (pytest, sem rede)
tools/                                  geração das references e snapshots dos schemas
evals/                                  casos de teste da skill e scripts de avaliação
docs/                                   achados sobre a API real
```

## Desenvolvimento

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1  ·  Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt

pytest -m "not online" -q            # testes offline (rápidos, sem rede)
pytest -m "not online" -q --cov=tg_extract   # testes + cobertura do script da skill
pytest -m online -q                  # testes contra a API real
python tools/snapshot_schemas.py     # atualiza os schemas gravados em tests/fixtures/
python tools/gerar_references.py --contagens   # regenera as references (com volumes atuais)
```

### Cobertura de testes
**89%** do script da skill (`tg_extract.py`), medindo linhas e ramificações: 914 linhas e 392 ramificações.
Os testes offline simulam a API a partir de respostas reais gravadas em `tests/fixtures/`. As partes que
dependem da rede real (falhas de conexão, download de arquivos grandes) são exercitadas pelos testes `online`,
que não entram nessa conta. Cobertura mede o que foi executado, não a qualidade dos testes; os casos
obrigatórios estão descritos nos próprios arquivos de teste.

Uma API descontinuada usada pelo script da skill **falha os testes** (configurado em `pytest.ini`). É o aviso
antecipado de que uma versão futura de alguma biblioteca vai quebrar a skill.

A CLI pode ser usada sem o Claude:

```bash
python .claude/skills/transferegov-extrator/scripts/tg_extract.py tabelas --modulo especiais
python .claude/skills/transferegov-extrator/scripts/tg_extract.py contar  --modulo especiais --tabela planos-acao-especiais -f ano_plano_acao=2025
python .claude/skills/transferegov-extrator/scripts/tg_extract.py extrair --modulo especiais --tabela planos-acao-especiais -f ano_plano_acao=2025
```

Para gerar um novo `.skill` depois de mudanças, use o `package_skill` da skill
[skill-creator](https://github.com/anthropics/skills) e grave o resultado em `dist/`.

### Avaliação
`evals/evals.json` traz 8 pedidos realistas com asserções verificáveis. Os scripts em `evals/` rodam cada
pedido com e sem a skill, via `claude -p` numa pasta temporária fora do projeto, e corrigem o resultado
contra contagens feitas na hora. Na última rodada, a skill acertou 100% das asserções; sem ela, o Claude
acertou 75%.

Rodar os evals consome a cota da sua conta e abre várias sessões do Claude. Use poucas em paralelo
(`--paralelo 2`).

### Verificação periódica (uma vez por mês ou antes de redistribuir o `.skill`)
O maior risco da skill não está no código: está na **API do governo mudar sem aviso**, como já aconteceu
quando um path e o formato da API foram trocados. Os testes offline usam respostas gravadas e não percebem esse
tipo de mudança. Por isso, de tempos em tempos:

1. **A API mudou?**
   ```bash
   python tools/snapshot_schemas.py      # baixa os schemas atuais para tests/fixtures/
   git diff --stat tests/fixtures/       # algum openapi_*.json mudou?
   ```
   Se mudou: rode `python tools/gerar_references.py --online --contagens` e `pytest -m "not online"`, corrija
   o que quebrar e gere o `.skill` de novo.
2. **A skill ainda funciona de verdade?** `pytest -m online -q` consulta a API real, com poucas requisições.
3. **As bibliotecas novas quebram algo?** Num ambiente separado, instale as versões mais recentes dentro das
   faixas (`pip install -U -r requirements-dev.txt`) e rode `pytest -m "not online"`. Um aviso de API
   descontinuada já faz os testes falharem (veja `pytest.ini`).
4. Se algo mudou: gere o `.skill`, faça o commit e envie para o GitHub.

Quando a skill ganhar mais usuários ou virar rotina diária de alguém, vale automatizar esses passos com uma
verificação agendada no GitHub Actions.

## Limitações conhecidas

- **Filtros de texto na API** comparam por "contém" e diferenciam acentos (`UBERLANDIA` ≠ `UBERLÂNDIA`).
  A skill orienta a usar códigos.
- **Sem extração incremental:** a API não oferece "só o que mudou". Rotinas diárias baixam de novo quando
  há carga nova.
- **Arquivos de convênios** são baixados inteiros (de 1 MB a 750 MB por arquivo) e ficam num cache local.
- **Dados de origem:** alguns campos chegam da própria fonte sem acentos ou com grafias diferentes.

## Licença

[MIT](LICENSE). Use, modifique e redistribua livremente, mantendo o aviso de autoria.

Os dados são públicos e pertencem ao Governo Federal (TransfereGov / Ministério da Gestão e da Inovação em
Serviços Públicos). Este projeto não tem vínculo oficial com o governo.
