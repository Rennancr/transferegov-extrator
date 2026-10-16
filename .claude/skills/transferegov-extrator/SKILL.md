---
name: transferegov-extrator
description: Extrai dados abertos do TransfereGov (api-publica.transferegov.gestao.gov.br) e entrega planilha Excel ou CSV. Cobre Transferências Especiais (emendas parlamentares individuais, "emendas Pix"), Fundo a Fundo, TED (Termos de Execução Descentralizada), Gestão de Parcerias e convênios/contratos de repasse (Transferências Discricionárias e Legais, antigo Siconv). Use sempre que o usuário mencionar TransfereGov ou Transferegov.br, emendas parlamentares, emendas Pix, transferência especial, fundo a fundo, TED, convênios, contratos de repasse, Siconv, Plataforma +Brasil, repasses ou transferências federais a estados e municípios, parcerias com OSCs, planos de ação, municípios ou entes beneficiados, ou pedir para baixar, consultar, cruzar, planilhar ou atualizar todo dia esses dados, mesmo que não cite a API.
---

# TransfereGov → planilha

Toda a lógica (descoberta pelo OpenAPI, validação de filtros, paginação, retry, tipagem, junção e exportação)
fica em `scripts/tg_extract.py`. **Não escreva chamadas HTTP próprias: use o script.** Ele conhece as
armadilhas da API, e um código feito na hora não conhece.

```
python scripts/tg_extract.py <tabelas|colunas|contar|extrair> --modulo M --tabela T [-f filtro ...]
```

Os caminhos são relativos à pasta desta skill. No Windows, o comando pode ser `py` em vez de `python`.
Dependências: `pip install requests pandas openpyxl` (em sandbox Linux gerenciado, acrescente `--break-system-packages`).

## Módulos

| Módulo | O que é | Reference |
|---|---|---|
| `especiais` | Transferências Especiais: emendas parlamentares individuais, as "emendas Pix", repassadas direto ao ente sem convênio | `references/especiais.md` |
| `fundoafundo` | Repasses da União para fundos estaduais e municipais (saúde, assistência etc.) | `references/fundoafundo.md` |
| `ted` | Termos de Execução Descentralizada: crédito entre órgãos federais | `references/ted.md` |
| `parcerias` | Gestão de Parcerias: propostas e parcerias com organizações da sociedade civil, emendas destinadas a elas | `references/parcerias.md` |
| `discricionarias` (ou `convenios`) | Convênios e contratos de repasse (Transferências Discricionárias e Legais, antigo Siconv): proposta, convênio, emendas, empenhos, pagamentos | `references/discricionarias.md` |

O módulo `discricionarias` **não é API**: são CSVs (zip) do `/downloads`, atualizados todo dia. O script baixa
o arquivo **inteiro** para um cache local e filtra localmente. Por isso, confira o tamanho com
`tabelas --modulo discricionarias` antes de usar um arquivo grande. Os mesmos comandos (`colunas`, `contar`,
`extrair`, `--juntar`) funcionam nele.

## Fluxo

1. **Identifique o módulo e a tabela.** Leia **só** a reference do módulo envolvido. O índice no topo descreve
   cada tabela e o volume aproximado; a seção "Chaves de junção prováveis" mostra como as tabelas se ligam.
   Nunca adivinhe nomes de tabela, coluna ou filtro: tudo vem do OpenAPI, e o script rejeita nome errado
   listando os válidos. Em caso de dúvida: `python scripts/tg_extract.py colunas --modulo M --tabela T`.
2. **Traduza o pedido em filtros** (sintaxe completa em `references/filtros.md`):
   - `-f coluna=valor`; para vários valores, repita o filtro (`-f uf_beneficiario=SP -f uf_beneficiario=RJ`);
   - faixas: `-f "ano_plano_acao>=2023" -f "ano_plano_acao<=2025"`;
   - texto compara por *contém*, sem diferenciar maiúsculas: `nome=SANTOS` também traz "SANTOS DUMONT".
     **Nas APIs, o acento conta**: `UBERLANDIA` não acha "UBERLÂNDIA". Por isso, para município, ente ou órgão,
     prefira o **código** quando a tabela tiver um (IBGE, CNPJ, `id_*`, UF). Ele é exato e independe da grafia
     que o usuário digitou. Se precisar filtrar por nome, use a grafia oficial, com acento. Se o resultado vier
     vazio, o script avisa. (Nos CSVs de `discricionarias`, o texto ignora acento e códigos comparam exato.)
   - Se a informação pedida (ex.: UF) não está na tabela principal, use junção (passo 4).
3. **Conte antes de extrair:** `contar` com os mesmos filtros.
   - Com junção, conte cada tabela com os filtros dela.
   - Se passar de **500 mil linhas**, ou se a soma das tabelas passar disso, **pare e pergunte**. Informe o
     volume, o tempo estimado (cerca de 0,5 s por página; páginas de 200 linhas em especiais e parcerias,
     de 1000 em fundoafundo e ted) e sugira filtros (ano, UF, situação) ou `--formato csv`.
   - Se o `contar` avisar sobre faixa local, o número é o que será **baixado**; o resultado final sai menor.
   - Em `discricionarias`, o custo é o tamanho do arquivo, não o número de linhas. Acima de ~200 MB de zip,
     informe o tamanho e confirme antes, porque o download e a leitura levam minutos.
4. **Extraia:**
   ```
   python scripts/tg_extract.py extrair --modulo M --tabela T [-f ...] [--formato xlsx|csv] [--saida PASTA] [--arquivo NOME]
   ```
   - Saída padrão: `./saida/`. No claude.ai, use `--saida /mnt/user-data/outputs` para o usuário receber o arquivo.
   - **Duas tabelas ou mais:** repita `--tabela`. O filtro sem prefixo precisa existir em todas; para
     restringir a uma só, use `-f tabela:coluna=valor`.
   - **Cruzar tabelas:** acrescente `--juntar CHAVE`, usando a chave da seção "Chaves de junção" da reference.
     O resultado tem a aba `juntado` (junção interna) e uma aba por tabela.
     - Sem filtro, cada aba vem **completa**: é o que o usuário espera de "uma aba por tabela".
     - Com filtro numa tabela (ex.: UF em beneficiários), as **outras** abas ficam restritas ao que casa com
       ela, porque a junção funciona como filtro: "planos de SP".
     - O script baixa primeiro a tabela menor e, quando compensa, consulta as outras pelas chaves encontradas.
   - O stdout traz só o(s) caminho(s) do arquivo; progresso e avisos vão para o stderr.
5. **Resuma em poucas linhas:** arquivo, linhas por aba, filtros usados, data da base (`data_atualizacao_base`
   nos metadados) e **todas** as linhas `ATENÇÃO:` do stderr, explicadas em linguagem simples. Não esconda avisos.
   Fale da planilha entregue e de como abri-la. Não suponha ferramentas do usuário (BI, banco de dados,
   linguagens) nem sugira uma que ele não citou: quem pede uma planilha pode não usar nenhuma delas.

Se o usuário quiser receber os dados **todo dia, automaticamente**, leia `references/agendamento.md`.

## Mapa rápido dos pedidos comuns (módulo `especiais`)

| Pedido | Tabela(s) | Como |
|---|---|---|
| Emendas Pix / transferências especiais (valores, parlamentar, objeto) | `planos-acao-especiais` | ano: `ano_plano_acao`; parlamentar: `nome_parlamentar_emenda_plano_acao`; valores: `valor_custeio_plano_acao` + `valor_investimento_plano_acao` |
| Emendas Pix **de uma UF ou município** | `planos-acao-especiais` + `beneficiarios-especiais` | `-f beneficiarios-especiais:uf_beneficiario=SP --juntar id_beneficiario` (a UF só existe em beneficiários) |
| Municípios ou entes beneficiados | `beneficiarios-especiais` | `uf_beneficiario`, `nome_beneficiario`, `cnpj_beneficiario` |
| Empenhos, pagamentos, ordens bancárias | `empenhos-especiais`, `documentos-habeis-especiais`, `ordens-pagamentos-ordens-bancarias-especiais` | ligam-se aos planos por `id_plano_acao` e entre si por `id_empenho` e `id_dh` |
| Execução (executor, metas, finalidade) | `executores-especiais`, `meta-especiais`, `finalidade-especiais` | `id_plano_acao`, `id_executor` |

Nos outros módulos, o padrão se repete: `programas` → `planos-acao` (ou `proposta`/`parceria`) → tabelas
financeiras, ligados por `id_programa` e `id_plano_acao` (ou `id_proposta`/`id_parceria`). A UF e o município
do beneficiário costumam estar em `programas-beneficiarios` (fundoafundo) ou em `proposta` (parcerias); confira
na reference.

**Convênios** (`discricionarias`): `convenio` traz situação, vigência e valores, e `proposta` traz órgão
concedente, proponente, UF e município. Os dois se ligam por `ID_PROPOSTA`. Exemplo: convênios do Ministério da
Saúde assinados em 2025:
`--tabela convenio --tabela proposta -f proposta:COD_ORGAO_SUP=36000 -f "convenio:DIA_ASSIN_CONV>=2025-01-01"
-f "convenio:DIA_ASSIN_CONV<=2025-12-31" --juntar ID_PROPOSTA`. O código do órgão superior é mais seguro que o
nome; se não souber o código, filtre por `DESC_ORGAO_SUP` com parte do nome. Pagamentos, empenhos e desembolsos
ligam-se ao convênio por `NR_CONVENIO`.

## Pedido vago

Resolva sozinho até a tabela certa usando o mapa acima e a reference. Pergunte só o que mudaria o resultado e
não dá para inferir: período, quando o volume sem ele for grande, ou qual de duas tabelas igualmente plausíveis.
Antes de extrair, diga em uma linha qual tabela e quais filtros vai usar.

## Erros e limites

- **Tabela, coluna ou filtro inexistente:** o script lista os válidos e sugere o nome parecido. Use a sugestão
  ou explique ao usuário; nunca chute outro nome.
- **Filtro que a API não suporta** ("diferente de", OU entre colunas diferentes, faixa em texto): explique e
  ofereça a alternativa (vários valores, faixa numérica ou de data, filtrar depois na planilha).
- **Rede:** se a conexão com `api-publica.transferegov.gestao.gov.br` falhar (proxy, firewall, sandbox sem
  internet), avise que o domínio precisa estar liberado. Nunca desative a verificação SSL.
- **Avisos de integridade** (total divergente, duplicatas, base atualizada durante a extração): a API não tem
  ordenação, então a extração confere o próprio resultado. Diante de um desses avisos, sugira rodar de novo.
- **Excel:** acima de 1.048.575 linhas, a tabela é dividida em abas `<tabela>_1`, `<tabela>_2`... Para volumes
  grandes, CSV (`;`, vírgula decimal, UTF-8 com BOM) é bem mais rápido e abre direto no Excel em português.
- A aba `metadados` (ou o arquivo `<nome>_metadados.csv`) registra fonte, filtros, linhas, data da base e
  avisos de cada tabela. Mencione-a no resumo.
