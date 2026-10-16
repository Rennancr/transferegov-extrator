# Módulo `fundoafundo` — API de dados abertos do módulo de Transferências Fundo a Fundo do Transferegov

> Gerado por `tools/gerar_references.py` a partir do OpenAPI (versão 1.1). Não edite à mão; regenere quando o schema mudar.

- Endpoint base: `https://api-publica.transferegov.gestao.gov.br/fundoafundo/<tabela>` · documentação: `https://api-publica.transferegov.gestao.gov.br/fundoafundo/docs`
- Linhas por página (máximo): 1000
- Volumes de **15/10/2026**: mudam a cada carga diária. Use só para ter a ordem de grandeza e confirme com `contar`.

## Índice

| Tabela | Conteúdo | Colunas | Linhas (aprox.) |
|---|---|---|---|
| [`programas`](#programas) | Retorna uma Lista Paginada dos dados dos Programas - FaF. | 31 | 125 |
| [`programas-beneficiarios`](#programas-beneficiarios) | Retorna uma Lista Paginada dos dados dos Beneficiários dos Programas - FaF. | 13 | 31.026 |
| [`programas-gestao-agil`](#programas-gestao-agil) | Retorna uma Lista Paginada dos dados dos Programas cadastrados no Sistema Gestão Ágil BB - FaF. | 10 | 185 |
| [`planos-acao`](#planos-acao) | Retorna uma Lista Paginada dos dados dos Plano de Ação - FaF. | 51 | 25.971 |
| [`planos-acao-dados-bancarios`](#planos-acao-dados-bancarios) | Retorna uma Lista Paginada dos Dados Bancários dos Planos de Ação - FaF. | 13 | 31.252 |
| [`planos-acao-metas`](#planos-acao-metas) | Retorna uma Lista Paginada dos dados das Metas dos Planos de Ação - FaF. | 8 | 56.499 |
| [`planos-acao-metas-acoes`](#planos-acao-metas-acoes) | Retorna uma Lista Paginada dos dados das Ações das Metas dos Planos de Ação - FaF. | 8 | 79.581 |
| [`planos-acao-destinacao-recursos`](#planos-acao-destinacao-recursos) | Retorna uma Lista Paginada dos dados dos Itens de Despesa cadastrados nos Planos de Ação - FaF. | 6 | 33.769 |
| [`planos-acao-analises`](#planos-acao-analises) | Retorna uma Lista Paginada dos dados das Análises dos Planos de Ação - FaF. | 8 | 40.399 |
| [`planos-acao-analises-responsaveis`](#planos-acao-analises-responsaveis) | Retorna uma Lista Paginada dos dados dos Responsáveis pela Análise dos Planos de Ação - FaF. | 4 | 47.650 |
| [`planos-acao-historico`](#planos-acao-historico) | Retorna uma Lista Paginada dos dados do Histórico dos Planos de Ação - FaF. | 5 | 184.200 |
| [`termos-adesao`](#termos-adesao) | Retorna uma Lista Paginada dos dados dos Termos de Adesão - FaF. | 10 | 23.967 |
| [`termos-adesao-historico`](#termos-adesao-historico) | Retorna uma Lista Paginada dos dados do Histórico dos Termos de Adesão - FaF. | 4 | 71.313 |
| [`empenhos`](#empenhos) | Retorna uma Lista Paginada dos dados dos Empenhos - FaF. | 30 | 4.248 |
| [`gestao-financeira-lancamentos`](#gestao-financeira-lancamentos) | Retorna uma Lista Paginada dos dados de Lançamentos - FaF. | 28 | 1.170.500 |
| [`gestao-financeira-subtransacoes`](#gestao-financeira-subtransacoes) | Retorna uma Lista Paginada dos dados das Subtransações - FaF. | 14 | 396.172 |
| [`relatorios-gestao`](#relatorios-gestao) | Retorna uma Lista Paginada dos dados dos Relatórios de Gestão - FaF. | 13 | 19.673 |
| [`relatorios-gestao-acoes`](#relatorios-gestao-acoes) | Retorna uma Lista Paginada dos dados das Ações associadas ao Relatório de Gestão - FaF. | 5 | 56.462 |
| [`relatorios-gestao-analises`](#relatorios-gestao-analises) | Retorna uma Lista Paginada dos dados das Análises associadas ao Relatório de Gestão - FaF. | 8 | 18.146 |
| [`relatorios-gestao-analises-responsaveis`](#relatorios-gestao-analises-responsaveis) | Retorna uma Lista Paginada dos dados dos Responsáveis pela Análise do Relatório de Gestão - FaF. | 4 | 22.776 |

## Chaves de junção prováveis

Uma coluna `id_*` presente em várias tabelas costuma ser a chave da junção. A "dona" é a tabela em que a chave é a 1ª coluna (ou a PK); nas outras, ela funciona como referência. É uma heurística: confira os valores antes de confiar na junção.

| Chave | Tabela dona (provável) | Também aparece em |
|---|---|---|
| `id_acao_meta_plano_acao` | `planos-acao-metas-acoes` | `relatorios-gestao-acoes` |
| `id_agencia_conta` | — | `planos-acao-dados-bancarios`, `gestao-financeira-lancamentos` |
| `id_analise_plano_acao` | `planos-acao-analises` | `planos-acao-analises-responsaveis` |
| `id_historico_plano_acao` | `planos-acao-historico` | `planos-acao-analises` |
| `id_lancamento_gestao_financeira` | `gestao-financeira-lancamentos` | `gestao-financeira-subtransacoes` |
| `id_meta_plano_acao` | `planos-acao-metas` | `planos-acao-metas-acoes` |
| `id_plano_acao` | `planos-acao` | `planos-acao-dados-bancarios`, `planos-acao-metas`, `planos-acao-destinacao-recursos`, `planos-acao-analises`, `planos-acao-historico`, `termos-adesao`, `empenhos`, `relatorios-gestao` |
| `id_programa` | `programas` | `programas-beneficiarios`, `programas-gestao-agil`, `planos-acao` |
| `id_relatorio_gestao` | `relatorios-gestao` | `relatorios-gestao-acoes`, `relatorios-gestao-analises` |
| `id_relatorio_gestao_analise` | `relatorios-gestao-analises` | `relatorios-gestao-analises-responsaveis` |
| `id_termo_adesao` | `termos-adesao` | `termos-adesao-historico` |

## Tabelas

### programas

Retorna uma Lista Paginada dos dados dos Programas - FaF. Grupo: Programas.

- PK: não declarada · linhas em 15/10/2026: 125
- Junções: `id_programa` ← `programas-beneficiarios`, `programas-gestao-agil`, `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_programa` | integer | contém | Identificador Único do Programa |
| `ano_programa` | integer | igual | Ano do Programa |
| `modalidade_programa` | string | contém | Modalidade do Programa |
| `codigo_programa` | integer | contém | Código do Prefixo do Programa concatenado com o Ano do Programa seguido do Código do Sufixo do Programa |
| `nome_programa` | string | contém | Nome do Programa |
| `id_unidade_gestora_programa` | integer | igual | Identificador Único do Código UG - Unidade Gestora do Orgão do Programa |
| `nome_institucional_programa` | string | contém | Nome Institucional do Programa |
| `permite_transferencia_sem_fundo_programa` | boolean | igual | Indicador de Permissão de Transferência sem Fundo Constituído |
| `objetivo_programa` | string | contém | Objetivo do Programa |
| `descricao_programa` | string | contém | Descrição do Programa |
| `situacao_programa` | string | contém | Situação do Programa |
| `valor_global_programa` | number | igual | Valor Global do Programa |
| `quantidade_parcelas_programa` | integer | igual | Quantidade de Parcelas do Programa |
| `id_orgao_superior_programa` | integer | igual | Identificador Único do Orgão Superior do Programa |
| `sigla_orgao_superior_programa` | string | contém | Sigla do Orgão Superior do Programa |
| `cnpj_orgao_superior_programa` | string | contém | CNPJ do Orgão Superior do Programa |
| `nome_orgao_superior_programa` | string | contém | Nome do Orgão Superior do Programa |
| `id_fundo_programa` | integer | igual | Identificador Único do Fundo do Programa |
| `cnpj_fundo_programa` | string | contém | CNPJ do Fundo do Programa |
| `nome_fundo_programa` | string | contém | Nome do Fundo do Programa |
| `uf_fundo_programa` | string | lista (27 valores; veja `colunas`) | Sigla da Unidade da Federação do Fundo do Programa |
| `municipio_fundo_programa` | string | contém | Nome do Município do Fundo do Programa |
| `codigo_ibge_fundo_programa` | integer | igual | Código IBGE do Município do Fundo do Programa |
| `programa_natureza_despesa` | json | — | Programa Natureza Despesa |
| `programa_acao_orcamentaria` | json | — | Programa Acao Orcamentaria |
| `data_inicio_recebimento_planos_acao_beneficiarios_especificos` | date | igual (AAAA-MM-DD) | Data de Início do Recebimento dos Planos de Ação para Beneficiários Específicos (YYYY-MM-DD) |
| `data_fim_recebimento_planos_acao_beneficiarios_especificos` | date | igual (AAAA-MM-DD) | Data Final do Recebimento dos Planos de Ação para Beneficiários Específicos (YYYY-MM-DD) |
| `data_inicio_recebimento_planos_acao_beneficiarios_emendas` | date | igual (AAAA-MM-DD) | Data de Início do Recebimento dos Planos de Ação para Beneficiários de Emenda Parlamentar (YYYY-MM-DD) |
| `data_fim_recebimento_planos_acao_beneficiarios_emendas` | date | igual (AAAA-MM-DD) | Data Final do Recebimento dos Planos de Ação para Beneficiários de Emenda Parlamentar (YYYY-MM-DD) |
| `data_inicio_recebimento_planos_acao_beneficiarios_voluntarios` | date | igual (AAAA-MM-DD) | Data de Início do Recebimento dos Planos de Ação para Beneficiários Voluntários (YYYY-MM-DD) |
| `data_fim_recebimento_planos_acao_beneficiarios_voluntarios` | date | igual (AAAA-MM-DD) | Data Final do Recebimento dos Planos de Ação para Beneficiários Voluntários (YYYY-MM-DD) |

Filtros aceitos pela API que não vêm como coluna na resposta: `grupo_natureza_despesa_programa` (lista: CUSTEIO, INVESTIMENTO); `codigo_acao_orcamentaria_programa` (contém); `descricao_acao_orcamentaria_programa` (contém).

### programas-beneficiarios

Retorna uma Lista Paginada dos dados dos Beneficiários dos Programas - FaF. Grupo: Programas.

- PK: não declarada · linhas em 15/10/2026: 31.026
- Junções: `id_programa` → `programas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_beneficiario_programa` | integer | contém | Identificador Único do Beneficiário do Programa |
| `cnpj_beneficiario_programa` | string | contém | CNPJ do Beneficiário do Programa |
| `nome_beneficiario_programa` | string | contém | Nome do Beneficiário do Programa |
| `valor_beneficiario_programa` | number | igual | Valor Destinado ao Beneficiário do Programa |
| `numero_emenda_beneficiario_programa` | string | contém | Número da Emenda do Beneficiário do Programa |
| `nome_parlamentar_beneficiario_programa` | string | contém | Nome do Parlamentar Autor da Emenda do Beneficiário do Programa |
| `tipo_beneficiario_programa` | string | contém | Tipo do Beneficiário do Programa |
| `nome_ente_beneficiario_programa` | string | contém | Nome do Ente do Beneficiário do Programa |
| `uf_ente_beneficiario_programa` | string | lista (27 valores; veja `colunas`) | Sigla da Unidade da Federação do Beneficiário do Programa |
| `nome_municipio_ente_beneficiario_programa` | string | contém | Nome do Município do Ente Beneficiário do Programa |
| `codigo_ibge_municipio_ente_beneficiario_programa` | integer | igual | Código IBGE do Município do Ente Beneficiário do Programa |
| `id_ente_beneficiario_programa` | integer | igual | Identificador Único do Ente Beneficiário do Programa |
| `id_programa` | integer | contém | Identificador Único do Programa |

### programas-gestao-agil

Retorna uma Lista Paginada dos dados dos Programas cadastrados no Sistema Gestão Ágil BB - FaF. Grupo: Programas.

- PK: não declarada · linhas em 15/10/2026: 185
- Junções: `id_programa` → `programas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_programa_agil` | integer | contém | Identificador Único do Programa Ágil |
| `id_programa_agil_bb` | integer | igual | Identificador Único do Programa Ágil no BB |
| `nome_programa_agil` | string | contém | Nome do Programa Ágil no Sistema de Gestão Ágil BB |
| `codigo_programa_agil` | string | contém | Código do Programa no Sistema de Gestão Ágil BB |
| `id_orgao_programa_agil` | integer | — | Id Orgao Programa Agil |
| `codigo_siorg_orgao_programa_agil` | integer | igual | Código SIORG do Órgão do Programa |
| `sigla_orgao_programa_agil` | string | contém | Sigla do Órgão do Programa |
| `cnpj_orgao_programa_agil` | string | contém | CNPJ do Órgão do Programa |
| `nome_orgao_programa_agil` | string | contém | Nome do Órgão do Programa |
| `id_programa` | integer | contém | Identificador Único do Programa |

### planos-acao

Retorna uma Lista Paginada dos dados dos Plano de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 25.971
- Junções: `id_plano_acao` ← `planos-acao-dados-bancarios`, `planos-acao-metas`, `planos-acao-destinacao-recursos`, `planos-acao-analises`, `planos-acao-historico`, `termos-adesao`, `empenhos`, `relatorios-gestao`; `id_programa` → `programas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `codigo_plano_acao` | string | contém | Código do Programa concatenado com o Identificador Único do Plano de Ação |
| `data_inicio_vigencia_plano_acao` | date | igual (AAAA-MM-DD) | Data do Ínicio da Vigência do Plano de Ação (YYYY-MM-DD) |
| `data_fim_vigencia_plano_acao` | date | igual (AAAA-MM-DD) | Data do Fim da Vigência do Plano de Ação (YYYY-MM-DD) |
| `diagnostico_plano_acao` | string | contém | Diagnóstico do Plano de Ação |
| `objetivos_plano_acao` | string | contém | Objetivos do Plano de Ação |
| `situacao_plano_acao` | string | contém | Situação do Plano de Ação |
| `valor_repasse_emenda_plano_acao` | number | igual | Valor de Repasse da Emenda Parlamentar do Plano de Ação |
| `valor_repasse_especifico_plano_acao` | number | igual | Valor do Repasse Específico do Plano de Ação |
| `valor_repasse_voluntario_plano_acao` | number | igual | Valor do Repasse Voluntário do Plano de Ação |
| `valor_total_repasse_plano_acao` | number | igual | Valor Total do Repasse do Plano de Ação |
| `valor_recursos_proprios_plano_acao` | number | igual | Valor dos Recursos Próprios do Plano de Ação |
| `valor_outros_plano_acao` | number | igual | Valor Outros do Plano de Ação |
| `valor_rendimentos_aplicacao_plano_acao` | number | igual | Valor dos Rendimentos da Aplicação do Plano de Ação |
| `valor_total_plano_acao` | number | igual | Valor Total do Plano de Ação |
| `valor_total_investimento_plano_acao` | number | igual | Valor Total de Investimento do Plano de Ação |
| `valor_total_custeio_plano_acao` | number | igual | Valor Total de Custeio do Plano de Ação |
| `valor_saldo_disponivel_plano_acao` | number | igual | Valor do Saldo Disponível do Plano de Ação |
| `id_orgao_repassador_plano_acao` | integer | igual | Identificador Único do Órgão Repassador no cadastro do Plano de Ação |
| `sigla_orgao_repassador_plano_acao` | string | contém | Sigla do Órgão Repassador do Plano de Ação |
| `cnpj_orgao_repassador_plano_acao` | string | contém | CNPJ do Órgão Repassador do Plano de Ação |
| `nome_orgao_repassador_plano_acao` | string | contém | Nome do Órgão Repassador do Plano de Ação |
| `id_ente_repassador_plano_acao` | integer | igual | Identificador Único do Ente Repassador no cadastro do Plano de Ação |
| `cnpj_ente_repassador_plano_acao` | string | contém | CNPJ do Ente Repassador do Plano de Ação |
| `nome_ente_repassador_plano_acao` | string | contém | Nome do Ente Repassador do Plano de Ação |
| `uf_ente_repassador_plano_acao` | string | lista (27 valores; veja `colunas`) | Sigla da Unidade da Federação do Ente Repassador do Plano de Ação |
| `nome_municipio_ente_repassador_plano_acao` | string | contém | Nome do Município do Ente Repassador do Plano de Ação |
| `codigo_ibge_municipio_ente_repassador_plano_acao` | integer | igual | Código IBGE do Município do Ente Repassador do Plano de Ação |
| `id_ente_recebedor_plano_acao` | integer | igual | Identificador Único do Ente Recebedor no cadastro do Plano de Ação |
| `cnpj_ente_recebedor_plano_acao` | string | contém | CNPJ do Ente Recebedor do Plano de Ação |
| `nome_ente_recebedor_plano_acao` | string | contém | Nome do Ente Recebedor do Plano de Ação |
| `uf_ente_recebedor_plano_acao` | string | lista (27 valores; veja `colunas`) | Sigla da Unidade da Federação do Ente Recebedor do Plano de Ação |
| `nome_municipio_ente_recebedor_plano_acao` | string | contém | Nome do Município do Ente Recebedor do Plano de Ação |
| `codigo_ibge_municipio_ente_recebedor_plano_acao` | integer | igual | Código IBGE do Município do Ente Recebedor do Plano de Ação |
| `tipo_unidade_recebedora_plano_acao` | string | contém | Tipo da Unidade Recebedora do Plano de Ação |
| `descricao_tipo_unidade_ente_plano_acao` | string | contém | Descrição do Tipo da Unidade do Ente do Plano de Ação |
| `id_fundo_repassador_plano_acao` | integer | igual | Identificador Único do Fundo Repassador no cadastro do Plano de Ação |
| `cnpj_fundo_repassador_plano_acao` | string | contém | CNPJ do Fundo Repassador do Plano de Ação |
| `nome_fundo_repassador_plano_acao` | string | contém | Nome do Fundo Repassador do Plano de Ação |
| `uf_fundo_repassador_plano_acao` | string | lista (27 valores; veja `colunas`) | Sigla da Unidade da Federação do Fundo Repassador do Plano de Ação |
| `municipio_fundo_repassador_plano_acao` | string | — | Municipio Fundo Repassador Plano Acao |
| `codigo_ibge_fundo_repassador_plano_acao` | integer | igual | Código IBGE do Município do Fundo Repassador do Plano de Ação |
| `id_fundo_vinculado_plano_acao` | integer | igual | Identificador Único do Fundo Vinculado no cadastro do Plano de Ação |
| `cnpj_fundo_vinculado_plano_acao` | string | contém | CNPJ do Fundo Vinculado ao Plano de Ação |
| `nome_fundo_vinculado_plano_acao` | string | contém | Nome do Fundo Vinculado ao Plano de Ação |
| `uf_fundo_vinculado_plano_acao` | string | lista (27 valores; veja `colunas`) | Sigla da Unidade da Federação do Fundo Vinculado ao Plano de Ação |
| `municipio_fundo_vinculado_plano_acao` | string | — | Municipio Fundo Vinculado Plano Acao |
| `codigo_ibge_fundo_vinculado_plano_acao` | integer | igual | Código IBGE do Município do Fundo Vinculado ao Plano de Ação |
| `tipo_unidade_recebedora_vinculada_plano_acao` | string | contém | Tipo da Unidade Recebedora Vinculada ao Plano de Ação |
| `descricao_tipo_unidade_recebedora_vinculada_plano_acao` | string | contém | Descrição do Tipo da Unidade Recebedora Vinculada ao Plano de Ação |
| `id_programa` | integer | contém | Identificador Único do Programa |

Filtros aceitos pela API que não vêm como coluna na resposta: `nome_municipio_fundo_repassador_plano_acao` (contém); `nome_municipio_fundo_vinculado_plano_acao` (contém).

### planos-acao-dados-bancarios

Retorna uma Lista Paginada dos Dados Bancários dos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 31.252
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_acao_dado_bancario` | integer | contém | Identificador Único do Dado Bancário do Plano de Ação |
| `id_agencia_conta` | string | contém | Identificador Único da Conta Bancária (Número da Agência Bancária seguida do Número da Conta Bancária) do Plano de Ação |
| `codigo_banco_plano_acao_dado_bancario` | string | contém | Código do Banco do Plano de Ação |
| `nome_banco_plano_acao_dado_bancario` | string | contém | Nome do Banco do Plano de Ação |
| `numero_agencia_plano_acao_dado_bancario` | string | contém | Número da Agência Bancária do Plano de Ação |
| `dv_agencia_plano_acao_dado_bancario` | string | contém | Dígito Verificador (DV) da Agência Bancária do Plano de Ação |
| `numero_conta_plano_acao_dado_bancario` | string | contém | Número da Conta Bancária do Plano de Ação |
| `dv_conta_plano_acao_dado_bancario` | string | contém | Dígito Verificador (DV) da Conta Bancária do Plano de Ação |
| `situacao_conta_plano_acao_dado_bancario` | string | contém | Situação da Conta Bancária do Plano de Ação |
| `data_abertura_conta_plano_acao_dado_bancario` | date | igual (AAAA-MM-DD) | Data de Abertura da Conta Bancária do Plano de Ação (YYYY-MM-DD) |
| `nome_programa_agil_conta_plano_acao_dado_bancario` | string | contém | Nome do Programa Gestão Ágil da Conta Bancária do Plano de Ação |
| `saldo_final_dado_bancario__saldo_final_gestao_financeira` | number | — | Saldo Final Gestao Financeira |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |

Filtros aceitos pela API que não vêm como coluna na resposta: `saldo_final_conta_plano_acao_dado_bancario` (igual).

### planos-acao-metas

Retorna uma Lista Paginada dos dados das Metas dos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 56.499
- Junções: `id_meta_plano_acao` ← `planos-acao-metas-acoes`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_meta_plano_acao` | integer | contém | Identificador Único da Meta do Plano de Ação |
| `numero_meta_plano_acao` | string | contém | Número da Meta do Plano de Ação (Letra 'M' seguida do Sequencial da Meta do Plano de Ação) |
| `nome_meta_plano_acao` | string | contém | Nome da Meta do Plano de Ação |
| `descricao_meta_plano_acao` | string | contém | Descrição da Meta do Plano de Ação |
| `valor_meta_plano_acao` | number | igual | Somatório dos Valores das Ações da Meta do Plano de Ação |
| `versao_meta_plano_acao` | integer | igual | Versão da Meta do Plano de Ação |
| `sequencial_meta_plano_acao` | integer | igual | Número Sequencial da Meta do Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |

### planos-acao-metas-acoes

Retorna uma Lista Paginada dos dados das Ações das Metas dos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 79.581
- Junções: `id_acao_meta_plano_acao` ← `relatorios-gestao-acoes`; `id_meta_plano_acao` → `planos-acao-metas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_acao_meta_plano_acao` | integer | contém | Identificador Único da Ação da Meta do Plano de Ação |
| `numero_acao_meta_plano_acao` | string | contém | Número da Ação da Meta do Plano de Ação (Letra 'A' seguida do sequencial da Meta do Plano de Ação, seguido de '.', seguida do Sequencial da Ação da Meta do Plano de Ação ) |
| `nome_acao_meta_plano_acao` | string | contém | Nome da Ação da Meta do Plano de Ação |
| `descricao_acao_meta_plano_acao` | string | contém | Descrição da Ação da Meta do Plano de Ação |
| `valor_acao_meta_plano_acao` | number | igual | Valor da Ação da Meta do Plano de Ação |
| `versao_acao_meta_plano_acao` | integer | igual | Versão da Ação da Meta do Plano de Ação |
| `sequencial_acao_meta_plano_acao` | integer | igual | Número Sequencial da Ação da Meta do Plano de Ação |
| `id_meta_plano_acao` | integer | contém | Identificador Único da Meta do Plano de Ação |

### planos-acao-destinacao-recursos

Retorna uma Lista Paginada dos dados dos Itens de Despesa cadastrados nos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 33.769
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_destinacao_recursos_plano_acao` | integer | contém | Identificador Único do Item de Despesa Cadastrado no Plano de Ação |
| `codigo_natureza_despesa_destinacao_recursos_plano_acao` | integer | igual | Código da Natureza de Despesa no SIAFI do Item de Despesa Cadastrado no Plano de Ação |
| `descricao_natureza_despesa_destinacao_recursos_plano_acao` | string | contém | Descrição da Natureza de Despesa no SIAFI do Item de Despesa Cadastrado no Plano de Ação |
| `tipo_despesa_destinacao_recursos_plano_acao` | string | lista: CUSTEIO, INVESTIMENTO | Tipo da Natureza de Despesa do Item de Despesa Cadastrado no Plano de Ação |
| `valor_destinacao_recursos_plano_acao` | number | igual | Valor do Recurso destinado ao Item de Despesa Cadastrado no Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |

### planos-acao-analises

Retorna uma Lista Paginada dos dados das Análises dos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 40.399
- Junções: `id_analise_plano_acao` ← `planos-acao-analises-responsaveis`; `id_plano_acao` → `planos-acao`; `id_historico_plano_acao` → `planos-acao-historico`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_analise_plano_acao` | integer | contém | Identificador Único da Análise do Plano de Ação |
| `tipo_analise_plano_acao` | string | lista: MERITO, TECNICA, FINANCEIRA, TECNICA_FINANCEIRA | Tipo de Análise do Plano de Ação ('MERITO', 'TECNICA', 'FINANCEIRA' ou 'TECNICA_FINANCEIRA') |
| `tipo_resultado_analise_plano_acao` | string | lista: COMPLEMENTACAO, APROVADO, COM_RESSALVA, REJEITADO | Tipo de Resultado da Análise do Plano de Ação ('COMPLEMENTACAO', 'APROVADO', 'COM_RESSALVA' ou 'REJEITADO') |
| `data_analise_plano_acao` | date | igual (AAAA-MM-DD) | Data da Análise do Plano de Ação (YYYY-MM-DD) |
| `parecer_analise_plano_acao` | string | contém | Parecer da Análise do Plano de Ação |
| `tipo_origem_analise_plano_acao` | string | contém | Tipo de Origem da Análise realizada no Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `id_historico_plano_acao` | integer | contém | Identificador Único do Histórico do Plano de Ação |

### planos-acao-analises-responsaveis

Retorna uma Lista Paginada dos dados dos Responsáveis pela Análise dos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 47.650
- Junções: `id_analise_plano_acao` → `planos-acao-analises`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_analise_responsavel_plano_acao` | integer | contém | Identificador Único do Responsável pela Análise do Plano de Ação |
| `nome_responsavel_analise_plano_acao` | string | contém | Nome do Responsável pela Análise do Plano de Ação |
| `cargo_responsavel_analise_plano_acao` | string | contém | Nome do Responsável pela Análise do Plano de Ação |
| `id_analise_plano_acao` | integer | contém | Identificador Único da Análise do Plano de Ação |

### planos-acao-historico

Retorna uma Lista Paginada dos dados do Histórico dos Planos de Ação - FaF. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 184.200
- Junções: `id_historico_plano_acao` ← `planos-acao-analises`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_historico_plano_acao` | integer | contém | Identificador Único do Histórico do Plano de Ação |
| `situacao_historico_plano_acao` | string | contém | Situação do Histórico do Plano de Ação |
| `data_historico_plano_acao` | date | igual (AAAA-MM-DD) | Data do Registro no Histórico do Plano de Ação (YYYY-MM-DD) |
| `versao_historico_plano_acao` | integer | igual | Versão do Histórico do Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |

### termos-adesao

Retorna uma Lista Paginada dos dados dos Termos de Adesão - FaF. Grupo: Termos de Adesão.

- PK: não declarada · linhas em 15/10/2026: 23.967
- Junções: `id_termo_adesao` ← `termos-adesao-historico`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_termo_adesao` | integer | contém | Identificador Único do Termo de Adesão |
| `numero_processo_termo_adesao` | string | contém | Número do Processo do Termo de Adesão |
| `situacao_termo_adesao` | string | lista: EM_ELABORACAO, ENVIADO, ASSINADO | Situação do Termo de Adesão (Podendo ser: 'EM_ELABORACAO', 'ENVIADO' ou 'ASSINADO') |
| `objeto_termo_adesao` | string | contém | Objeto do Termo de Adesão |
| `data_assinatura_termo_adesao` | date | igual (AAAA-MM-DD) | Data de Assinatura do Termo de Adesão (YYYY-MM-DD) |
| `ano_termo_adesao` | integer | igual | Ano do Termo de Adesão |
| `secao_publicacao_dou_termo_adesao` | integer | igual | Seção no DOU (Diário Oficial da União) do Termo de Adesão |
| `pagina_publicacao_dou_termo_adesao` | integer | igual | Página no DOU (Diário Oficial da União) do Termo de Adesão |
| `data_publicacao_dou_termo_adesao` | date | igual (AAAA-MM-DD) | Data da Publicação no DOU (Diário Oficial da União) do Termo de Adesão (YYYY-MM-DD) |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |

### termos-adesao-historico

Retorna uma Lista Paginada dos dados do Histórico dos Termos de Adesão - FaF. Grupo: Termos de Adesão.

- PK: não declarada · linhas em 15/10/2026: 71.313
- Junções: `id_termo_adesao` → `termos-adesao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_historico_termo_adesao` | integer | contém | Identificador Único do Histórico do Termo de Adesão |
| `situacao_historico_termo_adesao` | string | contém | Situação do Histórico do Termo de Adesão |
| `data_historico_termo_adesao` | date | igual (AAAA-MM-DD) | Data do Registro no Histórico do Termo de Adesão |
| `id_termo_adesao` | integer | contém | Identificador Único do Termo de Adesão |

### empenhos

Retorna uma Lista Paginada dos dados dos Empenhos - FaF. Grupo: Empenhos.

- PK: não declarada · linhas em 15/10/2026: 4.248
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_empenho` | integer | contém | Identificador(es) Único(s) da Nota de Empenho |
| `numero_empenho` | string | contém | Número da Nota de Empenho gerada e enviada pelo SIAFI (Sistema Integrado de Administração Financeira) |
| `ano_empenho` | integer | igual | Ano do Empenho |
| `gestao_emitente_empenho` | string | contém | Gestão Emitente no SIAFI |
| `ug_emitente_empenho` | integer | igual | Unidade Gestora Emitente no SIAFI |
| `data_emissao_empenho` | date | igual (AAAA-MM-DD) | Data da Emissão da Nota de Empenho (YYYY-MM-DD) |
| `fonte_recurso_empenho` | string | contém | Fonte de Recurso da Nota de Empenho no SIAFI |
| `esfera_orcamentaria_empenho` | integer | lista: 0, 1, 2, 3, 4, 5 | Indicador da Esfera Orçamentária podendo assumir os seguintes valores: (0, 1, 2, 3, 4, 5) |
| `descricao_esfera_orcamentaria_empenho` | string | lista: Federal, Estadual, Municipal, Estatal, Privada, Organismos Internacionais | Descrição do Indicador da Esfera Orçamentária podendo assumir os seguintes valores: (0 - 'Federal', 1 - 'Estadual'; 2 - 'Municipal'; 3 - 'Estatal'; 4 - 'Privada'; 5 - 'Organismos Internacionais') |
| `plano_interno_empenho` | string | contém | Instrumento de planejamento e de acompanhamento da ação planejada, usado como forma de detalhamento desta, de uso exclusivo de cada Ministério/órgão, com as seguintes características: - Há um atributo na tabela de órgão para indicar se o órgão utiliza ou não o Plano Interno (PI). Este atributo é mantido pela STN decorrente da solicitação do órgão. - A unidade setorial de orçamento do órgão é responsável por registrar na tabela os códigos de PI. - O SIAFI (Sistema Integrado de Administração Financeira), de acordo com o cadastramento previsto acima, só aceitará a emissão de nota de empenho com o código de PI existente. - Os códigos de PI poderão ter até 11 (onze) posições alfa-numéricas |
| `unidade_gestora_responsavel_empenho` | integer | igual | Unidade Gestora do Favorecido |
| `observacao_empenho` | string | contém | Observação referente a Nota de Empenho informada pelo usuário |
| `cnpj_favorecido_empenho` | string | contém | CNPJ do Favorecido |
| `numero_lista_empenho` | string | contém | Número da Lista gerado e enviado pelo SIAFI |
| `unidade_gestora_referencia_empenho` | integer | igual | Unidade Gestora de referência no SIAFI |
| `gestao_referencia_empenho` | string | contém | Gestão de referência no SIAFI |
| `numero_interno_empenho` | integer | igual | Número Interno Sequencial |
| `objeto_empenho` | string | contém | Objeto da Nota de Empenho informado pelo usuário |
| `numero_sistema_empenho` | string | contém | Campo preenchido com Nota de Sistema “NS” ou Nota de Lançamento “NL”, pelo usuário, sobre Nota de Empenho registrada diretamente no SIAFI (Sistema Integrado de Administração Financeira) |
| `natureza_despesa_empenho` | integer | igual | Identificador da tabela de Natureza Despesa, recuperado do SICONV |
| `natureza_despesa_sub_item_empenho` | integer | igual | Identificador da tabela de Natureza Despesa Subitem, recuperado do SICONV |
| `tipo_empenho` | integer | lista: 1, 3, 5 | Tipo de Empenho podendo assumir os valores: (1, 3, 5) |
| `descricao_tipo_empenho` | string | lista: Empenho Ordinário, Estimado, Global | Descrição do Tipo de Empenho podendo assumir os valores: (1 - 'Empenho Ordinário'; 3 - 'Estimado'; 5 - 'Global') |
| `codigo_tipo_nota_empenho` | string | contém | Código do Tipo da Nota de Empenho |
| `descricao_tipo_nota_empenho` | string | contém | Descrição do Tipo da Nota de Empenho |
| `situacao_empenho` | integer | lista: 1, 4, 5, 6 | Situação da Nota de Empenho, podendo assumir os valores: (1, 4, 5, 6) |
| `descricao_situacao_empenho` | string | lista: Minuta de Empenho, Enviado, Pendente, Registrado no SIAFI | Descrição da Situação da Nota de Empenho, podendo assumir os valores: (1 - 'Minuta de Empenho'; 4 - 'Enviado'; 5 - 'Pendente'; 6 - 'Registrado no SIAFI') |
| `valor_empenho` | number | igual | Valor Total da Nota de Empenho |
| `versao_empenho` | integer | igual | Versão da Nota de Empenho |
| `id_plano_acao` | integer | contém | Identificador(es) Único(s) do Plano de Ação |

### gestao-financeira-lancamentos

Retorna uma Lista Paginada dos dados de Lançamentos - FaF. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 1.170.500
- Junções: `id_lancamento_gestao_financeira` ← `gestao-financeira-subtransacoes`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_lancamento_gestao_financeira` | integer | contém | Identificador Único do Lançamento |
| `origem_solicitacao_gestao_financeira` | string | lista: TFF, TE | Origem da solicitação de abertura de contas: ('TFF' ou 'TE') |
| `descricao_origem_solicitacao_gestao_financeira` | string | contém | Descrição da Origem da solicitação de abertura de contas: ('Transferências Fundo a Fundo' ou 'Transferências Especiais') |
| `cnpj_ente_solicitante_gestao_financeira` | string | contém | CNPJ do Ente Solicitante da Conta Bancária |
| `nome_ente_solicitante_gestao_financeira` | string | contém | Nome do Ente Solicitante da Conta Bancária |
| `nome_personalizado_ente_solicitante_gestao_financeira` | string | contém | Nome Personalizado do Ente Solicitante da Conta Bancária |
| `codigo_programa_agil_ente_solicitante_gestao_financeira` | string | contém | Código do GestaoFinanceiraLancamentos Ágil cadastrado no BB |
| `codigo_banco_gestao_financeira` | string | contém | Código do Banco do Lançamento |
| `codigo_agencia_gestao_financeira` | string | contém | Número da Agência Bancária do Lançamento |
| `dv_agencia_gestao_financeira` | string | contém | Dígito Verificador (DV) da Agência Bancária do Lançamento |
| `codigo_conta_gestao_financeira` | string | contém | Número da Conta Corrente do Lançamento |
| `dv_conta_gestao_financeira` | string | contém | Dígito Verificador (DV) da Conta Corrente do Lançamento |
| `tipo_operacao_gestao_financeira` | string | lista: D, C | Tipo da Operação ('D' ou 'C') |
| `descricao_tipo_operacao_gestao_financeira` | string | lista: Débito, Crédito | Descrição do Tipo da Operação ('Débito' ou 'Crédito') |
| `descricao_gestao_financeira` | string | contém | Descrição do Lançamento |
| `data_lancamento_gestao_financeira` | date | igual (AAAA-MM-DD) | Data do Lançamento (YYYY-MM-DD) |
| `data_evento_lancamento_gestao_financeira` | date | igual (AAAA-MM-DD) | Data do Evento do Lançamento (YYYY-MM-DD) |
| `numero_ordem_gestao_financeira` | integer | igual | Número de Ordem do Lançamento |
| `numero_referencia_unica_gestao_financeira` | string | contém | Número de Referência do Lançamento |
| `tipo_favorecido_gestao_financeira` | integer | lista: 1, 2, 0 | Tipo do Favorecido (1, 2 ou 0) |
| `descricao_tipo_favorecido_gestao_financeira` | string | lista: CPF, CNPJ, Não Identificado | Descrição do Tipo do Favorecido (1 - 'CPF', 2 - 'CNPJ' ou 0 - 'Não Identificado') |
| `doc_favorecido_gestao_financeira_mask` | string | contém | Identificação Anonimizada do Favorecido do Lançamento |
| `nome_favorecido_gestao_financeira` | string | contém | Nome do Favorecido do Lançamento |
| `valor_lancamento_gestao_financeira` | number | igual | Valor do Lançamento |
| `codigo_categoria_despesa_lancamento_gestao_financeira` | integer | igual | Código da Categoria de Despesa do Lançamento |
| `categorias_despesa_lancamento__caminho_categoria_lancamento` | string | — | Caminho Categoria Lancamento |
| `quantidade_subtransacoes_lancamento_gestao_financeira` | integer | igual | Quantidade de Subtransações do Lançamento |
| `id_agencia_conta` | string | contém | Identificador Único da Conta Bancária (Número da Agência Bancária seguida do Número da Conta Bancária) do Plano de Ação |

Filtros aceitos pela API que não vêm como coluna na resposta: `caminho_categoria_despesa_lancamento_gestao_financeira` (contém).

### gestao-financeira-subtransacoes

Retorna uma Lista Paginada dos dados das Subtransações - FaF. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 396.172
- Junções: `id_lancamento_gestao_financeira` → `gestao-financeira-lancamentos`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_subtransacao_gestao_financeira` | string | contém | Identificador Único da Subtransação (ID do Lançamento seguido do ID da Subtransação) |
| `estado_subtransacao_gestao_financeira` | integer | igual | Estado da Subtransação |
| `situacao_pagamento_subtransacao_gestao_financeira` | integer | lista: 3, 6 | Situação do Pagamento (3 ou 6) da Subtransação |
| `descricao_situacao_pagamento_subtransacao_gestao_financeira` | string | lista: Pago, Cancelado | Descrição da Situação do Pagamento (3 - 'Pago' ou 6 - 'Cancelado') da Subtransação |
| `data_pagamento_subtransacao_gestao_financeira` | date | igual (AAAA-MM-DD) | Data do Pagamento da Subtransação (YYYY-MM-DD) |
| `tipo_pessoa_beneficiario_subtransacao_gestao_financeira` | integer | lista: 1, 2, 0 | Tipo do Favorecido (1, 2 ou 0) da Subtransação |
| `descricao_tp_pessoa_beneficiario_subtransacao_gestao_financeira` | string | lista: CPF, CNPJ, Não Identificado | Descrição do Tipo do Favorecido (1 - 'CPF', 2 - 'CNPJ' ou 0 - 'Não Identificado') da Subtransação |
| `doc_beneficiario_subtransacao_gestao_financeira_mask` | string | contém | Identificação Anonimizada do Favorecido da Subtransação |
| `nome_beneficiario_subtransacao_gestao_financeira` | string | contém | Nome do Favorecido da Subtransação |
| `descricao_subtransacao_gestao_financeira` | string | contém | Descrição da Subtransação |
| `valor_subtransacao_gestao_financeira` | number | igual | Valor da Subtransação |
| `codigo_categoria_despesa_subtransacao_gestao_financeira` | integer | igual | Código da Categoria de Despesa da Subtransação |
| `categorias_despesa_subtransacao__caminho_categoria_subtransacao` | string | — | Caminho Categoria Subtransacao |
| `id_lancamento_gestao_financeira` | integer | contém | Identificador Único do Lançamento |

Filtros aceitos pela API que não vêm como coluna na resposta: `caminho_categoria_despesa_subtransacao_gestao_financeira` (contém).

### relatorios-gestao

Retorna uma Lista Paginada dos dados dos Relatórios de Gestão - FaF. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 19.673
- Junções: `id_relatorio_gestao` ← `relatorios-gestao-acoes`, `relatorios-gestao-analises`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao` | integer | contém | Identificador(es) Único(s) do Relatório de Gestão |
| `data_relatorio_gestao` | date | igual (AAAA-MM-DD) | Data do Envio do Relatório de Gestão (YYYY-MM-DD) |
| `data_e_hora_relatorio_gestao` | date-time | igual (AAAA-MM-DD) | Data e Hora do Envio do Relatório de Gestão (YYYY-MM-DD HH:MM:SS) |
| `tipo_relatorio_gestao` | string | lista: PARCIAL, FINAL | Tipo do Relatório de Gestão: ('PARCIAL' ou 'FINAL') |
| `situacao_relatorio_gestao` | string | lista: EM_ELABORACAO, ENVIADO_ANALISE_CONSELHO, ENVIADO_ANALISE, EM_COMPLEMENTACAO, ANALISE_CONCLUIDA_CONSELHO, ANALISE_CONCLUIDA, REJEITADO | Situação do Relatório de Gestão: ('EM_ELABORACAO', 'ENVIADO_ANALISE_CONSELHO', 'ENVIADO_ANALISE', 'EM_COMPLEMENTACAO', 'ANALISE_CONCLUIDA_CONSELHO', 'ANALISE_CONCLUIDA', 'REJEITADO') |
| `valor_executado_relatorio_gestao` | number | igual | Valor Repassado do Relatório de Gestão |
| `valor_pendente_relatorio_gestao` | number | igual | Valor Pendente do Relatório de Gestão |
| `resultados_alcancados_metas_relatorio_gestao` | string | contém | Resultados Alcançados do Relatório de Gestão |
| `descritivo_relatorio_gestao` | string | contém | Descritivo do Parecer do Relatório de Gestão |
| `contrapartida_relatorio_gestao` | string | contém | Contrapartida do Relatório de Gestão |
| `endereco_eletronico_publicidade_acoes_relatorio_gestao` | string | contém | URL de Publicidade das Ações Pactuadas no Relatório de Gestão |
| `declaracao_conformidade_relatorio_gestao` | boolean | igual | Indicador da Declaração de Conformidade do Relatório de Gestão |
| `id_plano_acao` | integer | contém | Identificador(es) Único(s) do Plano de Ação) |

### relatorios-gestao-acoes

Retorna uma Lista Paginada dos dados das Ações associadas ao Relatório de Gestão - FaF. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 56.462
- Junções: `id_relatorio_gestao` → `relatorios-gestao`; `id_acao_meta_plano_acao` → `planos-acao-metas-acoes`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_acao_relatorio_gestao` | integer | contém | Identificador Único da Ação associada ao Relatório de Gestão |
| `percentual_execucao_fisica_acao_relatorio_gestao_acao` | number | igual | Percentual de Conclusão da Ação do Relatório de Gestão |
| `observacoes_justificativas_relatorio_gestao_acao` | string | contém | Justificativa referente ao Percentual de Conclusão da Ação do Relatório de Gestão |
| `id_relatorio_gestao` | integer | contém | Identificador Único do Relatório de Gestão |
| `id_acao_meta_plano_acao` | integer | contém | Identificador Único da Ação da Meta do Plano de Ação |

### relatorios-gestao-analises

Retorna uma Lista Paginada dos dados das Análises associadas ao Relatório de Gestão - FaF. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 18.146
- Junções: `id_relatorio_gestao_analise` ← `relatorios-gestao-analises-responsaveis`; `id_relatorio_gestao` → `relatorios-gestao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao_analise` | integer | contém | Identificador Único da Análise do Relatório de Gestão |
| `tipo_analise_relatorio_gestao_analise` | string | contém | Tipo de Análise realizada no Relatório de Gestão |
| `resultado_analise_relatorio_gestao_analise` | string | contém | Tipo do Resultado da Análise do Relatório de Gestão |
| `parecer_analise_relatorio_gestao_analise` | string | contém | Parecer da Análise do Relatório de Gestão |
| `origem_analise_relatorio_gestao_analise` | string | contém | Tipo de Origem da Análise realizada no Relatório de Gestão |
| `data_analise_relatorio_gestao_analise` | date | igual (AAAA-MM-DD) | Data de Realização da Análise no Relatório de Gestão (YYYY-MM-DD) |
| `versao_analise_relatorio_gestao_analise` | integer | igual | Versão da Análise do Relatório de Gestão |
| `id_relatorio_gestao` | integer | contém | Identificador Único do Relatório de Gestão |

### relatorios-gestao-analises-responsaveis

Retorna uma Lista Paginada dos dados dos Responsáveis pela Análise do Relatório de Gestão - FaF. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 22.776
- Junções: `id_relatorio_gestao_analise` → `relatorios-gestao-analises`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao_analise_responsavel` | integer | contém | Identificador Único do Responsável pela Análise do Relatório de Gestão |
| `nome_responsavel_analise_relatorio_gestao_analise` | string | contém | Nome do Responsável pela Análise do Relatório de Gestão |
| `cargo_responsavel_analise_relatorio_gestao_analise` | string | contém | Cargo do Responsável pela Análise do Relatório de Gestão |
| `id_relatorio_gestao_analise` | integer | contém | Identificador Único da Análise do Relatório de Gestão |
