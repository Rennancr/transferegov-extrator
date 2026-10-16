# Filtros: sintaxe e semântica

A API do TransfereGov aceita **um parâmetro por coluna** e só compara por igualdade (ou por *contém*, em
texto). O script completa o que falta, como vários valores e faixas, e valida tudo **antes** de chamar a API.
A validação prévia é necessária porque a API **ignora em silêncio** um filtro de nome desconhecido e devolve
a tabela inteira.

## Sintaxe (`-f`, repetível)

| Forma | Exemplo | Efeito |
|---|---|---|
| `coluna=valor` | `-f ano_plano_acao=2025` | igualdade (ou *contém*, em texto) |
| mesmo filtro repetido | `-f uf_beneficiario=SP -f uf_beneficiario=RJ` | OU: uma consulta por valor, resultados somados |
| filtros diferentes | `-f ano_plano_acao=2025 -f situacao_plano_acao=CIENTE` | E |
| faixa | `-f "ano_plano_acao>=2023" -f "ano_plano_acao<=2025"` | também `>` e `<`; use aspas no shell |
| escopo (várias tabelas) | `-f beneficiarios-especiais:uf_beneficiario=SP` | aplica só àquela tabela |

## Como cada tipo compara

| Tipo (coluna "Filtro na API" da reference) | Comparação | Observações |
|---|---|---|
| `contém` (texto) | contém, sem diferenciar maiúsculas | `nome_beneficiario=AGUDO` traz "AGUDO", "AGUDOS" e "MORRO AGUDO". Não existe igualdade exata para texto |
| `lista: ...` | igualdade com um dos valores | minúsculas são aceitas (`sp` → `SP`); valor fora da lista dá erro com a lista |
| `igual` (inteiro/número) | igualdade | `valor=1000` só casa com 1000.0 exato; para valores, use faixa |
| `igual (AAAA-MM-DD)` | data exata | um período se escreve como faixa: `-f "data_x>=2025-01-01" -f "data_x<=2025-03-31"` |
| `—` (sem filtro na API) | não filtrável no servidor | faixa ainda funciona se a coluna é numérica ou de data (é aplicada localmente) |

## Faixas: onde são aplicadas

- **Inteiro com início e fim** (até 50 valores), em coluna que é filtro da API, como `ano>=2023` e `ano<=2025`:
  vira uma consulta por valor, **exata e no servidor**. Não há download a mais.
- **Demais faixas** (datas, valores monetários, faixa aberta como `ano>=2023`, inteiros largos): o script baixa
  o que os **outros filtros** permitem e aplica a faixa localmente.
  - `contar` mostra o volume que será baixado e avisa que o resultado final sai menor.
  - Os metadados marcam a faixa como `(local)` e trazem `linhas_baixadas`.
  - Uma faixa local **sem** outro filtro baixa a tabela inteira. Confira o volume antes.
- Nulos ficam fora de qualquer faixa, como no SQL.
- Em coluna data-hora, um limite só com a data vale para o dia inteiro: `<=2024-12-31` inclui 31/12 às 23:59.

## No módulo `discricionarias` (CSVs)

Todos os filtros são aplicados localmente, depois do download do arquivo. A sintaxe é a mesma, com estas
diferenças:

- **Texto:** *contém*, ignorando acento e maiúsculas (`SAUDE` acha "SAÚDE").
- **Códigos** (colunas `ID_`, `COD_`, `NR_`, `CNPJ`, `CPF`, `UF_`, `UG_`...): igualdade exata. `ID_PROPOSTA=10`
  não traz 100.
- **Datas** (`DIA_`, `DATA_`, `DT_`, que no arquivo vêm em `dd/mm/aaaa`): escreva em `AAAA-MM-DD`. Aceitam faixa.
- **Valores** (`VL_`, `VALOR_`): número com ponto ou vírgula. Aceitam faixa.
- Sem limite de "50 valores" nem de consultas: a leitura é uma só por arquivo.

## O que não existe

- "diferente de" (`!=`), OU entre colunas diferentes e faixa em texto. Ofereça alternativas: listar os valores
  desejados, filtrar depois na planilha ou fazer duas extrações.
- Sintaxe PostgREST (`eq.`, `gte.`, `in.(...)`) é rejeitada com a forma correta.

## Junção (`--juntar CHAVE`)

- Use a chave da seção "Chaves de junção prováveis" da reference do módulo, por exemplo `id_beneficiario`,
  `id_plano_acao`, `id_programa` ou `id_proposta`.
- A aba `juntado` é uma junção **interna**: só ficam as linhas com par em todas as tabelas. As colunas
  repetidas (fora a chave) ganham o sufixo `__<tabela>`.
- Abas de cada tabela:
  - sem filtro nas outras tabelas, a aba vem **completa**;
  - se outra tabela tem filtro do usuário, a aba é restrita às chaves que casam, porque a junção funciona
    como filtro.

  Os metadados registram `linhas_fora_do_filtro_da_juncao`.
- O script conta cada tabela, baixa primeiro a de menor volume e, quando há poucas chaves, consulta as
  outras por chave no servidor, sem baixá-las inteiras.

Exemplo: emendas Pix de 2025 para municípios do Acre.

```
python scripts/tg_extract.py extrair --modulo especiais \
  --tabela planos-acao-especiais --tabela beneficiarios-especiais \
  -f beneficiarios-especiais:uf_beneficiario=AC -f planos-acao-especiais:ano_plano_acao=2025 \
  --juntar id_beneficiario
```
