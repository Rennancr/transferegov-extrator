# Fase 0 — Reconhecimento da API (15/10/2026)

Base: `https://api-publica.transferegov.gestao.gov.br`. A conectividade funciona direto, sem proxy e sem
ajuste de SSL.

## Conclusão principal: a API não é PostgREST

Os quatro módulos são **FastAPI** com OpenAPI 3.1 em `/<modulo>/openapi.json`. O header
`Accept: application/openapi+json` não tem efeito: `GET /<modulo>/` redireciona (307) para o Swagger em `/docs`.
Por isso não existem `order`, `limit`/`offset`, `Prefer: count=exact`, `Content-Range` nem operadores `op.valor`.

| Premissa do CLAUDE.md | Realidade |
|---|---|
| `/transferenciasespeciais/` | **`/especiais`**. O path antigo devolve 404 |
| Parcerias: path a confirmar | **`/parcerias`** |
| Tabelas em `definitions` | Endpoints em `paths` (um GET por "tabela"); colunas em `components.schemas.<X>Response` |
| PK marcada com `<pk/>` | Nenhum schema usa `<pk/>`. Só `ted/planos-acao-pareceres.id_parecer` traz `"primary_key": true` (extensão própria) |
| `limit` + `offset` + `order` | `pagina` (começa em 1) + `tamanho_da_pagina`. **Não existe ordenação** |
| Contagem por `Content-Range` | O envelope JSON traz `total_items` e `total_pages` |
| `max-rows` no servidor | Validação explícita: acima do máximo, o servidor devolve **422**, sem truncar em silêncio |
| Filtros `eq/gte/in/like/or` | Um query param por coluna, com a semântica descrita abaixo |

## Envelope de resposta

```json
{"data": [...], "total_pages": 28, "total_items": 5539, "page_number": 1, "page_size": 200}
```

Se a página pedida passa do fim, a resposta é 200 com `data: []` e `page_size: 0`. A contagem custa uma
chamada com `tamanho_da_pagina=1`.

## Page size efetivo

| Módulo | Máx. `tamanho_da_pagina` | Testado |
|---|---|---|
| especiais | 200 | 500 → 422 `less_than_equal` |
| parcerias | 200 | (schema) |
| fundoafundo | 1000 | 1000 linhas voltaram |
| ted | 1000 | 1000 linhas voltaram |

O máximo vem do `maximum` do parâmetro no OpenAPI. O script deve ler esse valor por endpoint e não fixá-lo no código.

## Semântica dos filtros (testada em `especiais/beneficiarios-especiais`)

- **String livre:** *contém*, sem diferenciar maiúsculas (equivale a `ILIKE '%v%'`). `nome=AGUDO` traz também
  "MORRO AGUDO". Não existe filtro de igualdade exata para texto.
- **Inteiro, número, enum (UF etc.) e data:** igualdade exata. Datas aceitam `AAAA-MM-DD` (pattern). Um mês
  parcial (`2023-05`) devolve 422.
- **Multivalor** (`SP,RJ`), **faixas** (`gte.100`) e **OR**: não suportados (422).
- **Parâmetro desconhecido é ignorado em silêncio** e devolve a tabela inteira (5539 em vez de filtrar). ⚠️
  O script precisa validar os nomes de filtro contra o OpenAPI antes de chamar.
- Endpoint inexistente → 404 `{"detail":"Not Found"}`.
- Em vários endpoints, há filtros que não são colunas da resposta (por exemplo, `parcerias/parceria` tem 8 filtros
  "extras"). As colunas vêm do schema da resposta e os filtros vêm dos `parameters`, então os dois são tratados à parte.

## Estabilidade da paginação sem `order`

`beneficiarios-especiais` (5.539 linhas, 28 páginas de 200) foi baixada inteira duas vezes. Nas duas rodadas
voltou a **mesma sequência**, com 5.539 IDs distintos e nenhuma duplicata. A ordem **não** é por ID: é a ordem
física do servidor. Uma página profunda (700 × 200 em uma tabela de 142 mil linhas) respondeu em 0,5 s.

Risco que continua: se a base for atualizada durante uma extração longa, linhas podem duplicar ou sumir
(`data-atualizacao` indica carga diária). Mitigações propostas para a Fase 1:
1. Ler `/data-atualizacao` antes e depois da extração e avisar se a data mudar.
2. Comparar as linhas coletadas com o `total_items` e avisar quando divergirem.
3. Detectar duplicatas pela coluna `id_*` (a 1ª coluna do schema, ou a que tiver `primary_key`) e avisar.

## Tipos

Os schemas de **resposta** declaram `integer`, `number`, `string`, `boolean`, `string` + `format: date` e
`string` + `format: date-time`. Todas as colunas `data_`/`dt_`/`dh_` têm `format`, então não é preciso inferir
pelo nome. Nos **parâmetros**, as datas aparecem como `string` com `pattern`.

Há também colunas aninhadas, em fundoafundo, ted e parcerias:
- objeto (`$ref` → `*Embedded`), que vira colunas `coluna__subcampo` tipadas pelo sub-schema;
- lista de objetos (`array`), que vira texto JSON na célula.

## Qualidade do dado na origem

`fundoafundo/gestao-financeira-lancamentos.categorias_despesa_lancamento.caminho_categoria_lancamento`
já chega da API sem os caracteres acentuados ("Transferncias Voluntrias | Chamada pblica"), conforme os bytes
crus via curl. O problema é da origem e não do script; não há o que corrigir aqui. Outros campos vêm em UTF-8
correto ("Ministério da Gestão...").

## Volume por módulo

| Módulo | Endpoints de dados | Sem PK declarada | Page size | Maior tabela |
|---|---|---|---|---|
| especiais | 23 | 23 | 200 | gestao-financeira-lancamentos-especiais: 739.458 |
| fundoafundo | 20 | 20 | 1000 | gestao-financeira-lancamentos: 1.170.500 |
| ted | 14 | 13 | 1000 | planos-acao-metas-etapas: 57.919 |
| parcerias | 17 | 17 | 200 | extrato-bancario: 1.433.757 |

Tabelas acima de 500 mil: especiais/gestao-financeira-lancamentos-especiais (739 mil), fundoafundo/gestao-financeira-lancamentos
(1,17 mi) e parcerias/extrato-bancario (1,43 mi). Logo abaixo do limiar ficam especiais/planos-trabalho-historico (461 mil)
e parcerias/item-proposta (429 mil). Com páginas de 200, a última exige cerca de 7.200 requisições sequenciais.

## Fixtures gravadas (`tests/fixtures/`)

- `openapi_{especiais,fundoafundo,ted,parcerias}.json`: snapshot via `tools/snapshot_schemas.py`
- `pagina_especiais_programas-especiais_p{1..4}_t6.json`: 15 linhas em páginas de 6, ou seja 6 + 6 + 3, e a página 4 vazia
- `erro_422_enum.json`: resposta de validação do FastAPI
- `data_atualizacao_especiais.json`
