# Módulo `ted` — API de dados abertos do Módulo Termo de Execução Descentralizada - TED do Transferegov

> Gerado por `tools/gerar_references.py` a partir do OpenAPI (versão 1.0). Não edite à mão; regenere quando o schema mudar.

- Endpoint base: `https://api-publica.transferegov.gestao.gov.br/ted/<tabela>` · documentação: `https://api-publica.transferegov.gestao.gov.br/ted/docs`
- Linhas por página (máximo): 1000
- Volumes de **15/10/2026**: mudam a cada carga diária. Use só para ter a ordem de grandeza e confirme com `contar`.

## Índice

| Tabela | Conteúdo | Colunas | Linhas (aprox.) |
|---|---|---|---|
| [`programas`](#programas) | Retorna uma Lista Paginada dos dados dos Programas - TED. | 35 | 5.700 |
| [`programas-beneficiarios`](#programas-beneficiarios) | Retorna uma Lista Paginada dos dados dos Beneficiários dos Programas - TED. | 5 | 6.324 |
| [`programas-acoes-orcamentarias`](#programas-acoes-orcamentarias) | Retorna uma Lista Paginada dos dados das Ações Orçamentárias dos Programas - TED. | 4 | 6.438 |
| [`planos-acao`](#planos-acao) | Retorna uma Lista Paginada dos dados dos Planos de Ação - TED. | 31 | 6.477 |
| [`planos-acao-metas`](#planos-acao-metas) | Retorna uma Lista Paginada dos dados das Metas dos Planos de Ação - TED. | 10 | 23.414 |
| [`planos-acao-metas-etapas`](#planos-acao-metas-etapas) | Retorna uma Lista Paginada dos dados das Etapas das Metas dos Planos de Ação - TED. | 10 | 57.919 |
| [`planos-acao-analises`](#planos-acao-analises) | Retorna uma Lista Paginada dos dados das Análises dos Planos de Ação - TED. | 5 | 5.943 |
| [`planos-acao-pareceres`](#planos-acao-pareceres) | Retorna uma Lista Paginada dos dados dos Pareceres dos Planos de Ação - TED. | 7 | 8.755 |
| [`planos-trabalho-cronogramas`](#planos-trabalho-cronogramas) | Retorna uma Lista Paginada dos dados dos Cronogramas dos Planos de Trabalho - TED. | 6 | 14.320 |
| [`termos-execucao`](#termos-execucao) | Retorna uma Lista Paginada dos dados dos Termos de Execução - TED. | 11 | 5.177 |
| [`notas-credito`](#notas-credito) | Retorna uma Lista Paginada dos dados das Notas de Crédito - TED. | 11 | 12.113 |
| [`eventos`](#eventos) | Retorna uma Lista Paginada dos dados dos Eventos - TED. | 23 | 19.667 |
| [`programacoes-financeiras`](#programacoes-financeiras) | Retorna uma Lista Paginada dos dados das Programações Financeiras - TED. | 10 | 18.269 |
| [`programacoes-financeiras-trf`](#programacoes-financeiras-trf) | Retorna uma Lista Paginada dos dados dos Itens TRF das Programações Financeiras - TED. | 7 | 20.410 |

## Chaves de junção prováveis

Uma coluna `id_*` presente em várias tabelas costuma ser a chave da junção. A "dona" é a tabela em que a chave é a 1ª coluna (ou a PK); nas outras, ela funciona como referência. É uma heurística: confira os valores antes de confiar na junção.

| Chave | Tabela dona (provável) | Também aparece em |
|---|---|---|
| `id_meta` | `planos-acao-metas` | `planos-acao-metas-etapas` |
| `id_nota` | `notas-credito` | `eventos` |
| `id_plano_acao` | `planos-acao` | `planos-acao-metas`, `planos-acao-analises`, `planos-acao-pareceres`, `planos-trabalho-cronogramas`, `termos-execucao`, `notas-credito`, `programacoes-financeiras` |
| `id_programa` | `programas` | `programas-beneficiarios`, `programas-acoes-orcamentarias`, `planos-acao` |
| `id_programacao` | `programacoes-financeiras` | `programacoes-financeiras-trf` |

## Tabelas

### programas

Retorna uma Lista Paginada dos dados dos Programas - TED. Grupo: Programas.

- PK: não declarada · linhas em 15/10/2026: 5.700
- Junções: `id_programa` ← `programas-beneficiarios`, `programas-acoes-orcamentarias`, `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_programa` | integer | contém | Identificador Único do Programa |
| `responsavel_acompanhamento_sup` | string | contém | Nome da Unidade Superior Responsável pelo Acompanhamento |
| `unidade_responsavel_acompanhamento_fk` | integer | igual | Identificador Único da Unidade Responsável pelo Acompanhamento |
| `descentralizadora_sup` | string | contém | Nome da Unidade Superior Descentralizadora (Repassador) |
| `unidade_descentralizadora_fk` | integer | igual | Identificador Único da Unidade Descentralizadora (Repassador) |
| `tx_codigo_programa` | string | contém | Código do Programa |
| `aa_ano_programa` | integer | igual | Ano do Programa |
| `tx_situacao_programa` | string | contém | Situação do Programa |
| `tx_nome_programa` | string | contém | Nome do Programa |
| `unidade_gestora_descentralizadora` | integer | igual | Código da Unidade Gestora Descentralizadora (Repassador) |
| `unidade_gestora_acompanhamento` | integer | igual | Código da Unidade Gestora Acompanhamento |
| `tx_nome_institucional_programa` | string | contém | Nome Institucional do Programa |
| `tx_objetivo_programa` | string | contém | Objetivo do Programa |
| `tx_descricao_programa` | string | contém | Descrição do Programa |
| `in_grupo_investimento_obra` | boolean | igual | Indicador do Grupo de Investimento da Obra |
| `in_grupo_investimento_servico` | boolean | igual | Indicador do Grupo de Investimento de Serviço |
| `in_grupo_investimento_equipamento` | boolean | igual | Indicador do Grupo de Investimento de Equipamento |
| `in_autoriza_subdescentralizacao_outro` | string | contém | Indicador Autoriza Subdescentralização de Outro |
| `in_autoriza_realizacao_despesas` | string | contém | Indicador Autoriza Relização de Despesas |
| `in_autoriza_execucao_creditos_descentralizada` | string | contém | Indicador Autoriza Execução de Créditos Descentralizada |
| `in_beneficiario_especifico` | boolean | igual | Indicador de Beneficiário Específico |
| `dt_recebimento_plano_beneficiario_inicio` | date | igual (AAAA-MM-DD) | Data de Início do Recebimento do Plano de Beneficiário (YYYY-MM-DD) |
| `dt_recebimento_plano_beneficiario_fim` | date | igual (AAAA-MM-DD) | Data Final do Recebimento do Plano de Beneficiário (YYYY-MM-DD) |
| `in_chamamento_publico` | boolean | igual | Indicador de Chamamento Público |
| `dt_recebimento_plano_chamamento_inicio` | date | igual (AAAA-MM-DD) | Data de Início do Recebimento do Plano de Chamamento (YYYY-MM-DD) |
| `dt_recebimento_plano_chamamento_fim` | date | igual (AAAA-MM-DD) | Data Final do Recebimento do Plano de Chamamento (YYYY-MM-DD) |
| `tx_modalidade_transferencia` | string | contém | Modalidade de Transferência |
| `unidade_descentralizadora` | string | contém | Nome da Unidade Descentralizadora (Repassador) |
| `sigla_unidade_descentralizadora` | string | contém | Sigla da Unidade Descentralizadora (Repassador) |
| `sigla_descentralizadora_sup` | string | contém | Sigla da Unidade Superior Descentralizadora (Repassador) |
| `cd_descentralizadora_sup` | integer | igual | Código da Unidade Superior Descentralizadora (Repassador) |
| `unidade_responsavel_acompanhamento` | string | contém | Nome da Unidade Responsável pelo Acompanhamento |
| `sigla_unidade_responsavel_acompanhamento` | string | contém | Sigla da Unidade Responsável pelo Acompanhamento |
| `sigla_responsavel_acompanhamento_sup` | string | contém | Sigla da Unidade Superior Responsável pelo Acompanhamento |
| `cd_responsavel_acompanhamento_sup` | integer | igual | Código da Unidade Superior Responsável pelo Acompanhamento |

### programas-beneficiarios

Retorna uma Lista Paginada dos dados dos Beneficiários dos Programas - TED. Grupo: Programas.

- PK: não declarada · linhas em 15/10/2026: 6.324
- Junções: `id_programa` → `programas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_beneficiario_programa` | integer | contém | Identificador Único do Beneficiário do Programa |
| `tx_codigo_siorg` | string | contém | Código SIORG |
| `tx_nome_beneficiario` | string | contém | Nome do Beneficiário |
| `vl_valor_beneficiario` | number | igual | Valor do Beneficiário |
| `id_programa` | integer | contém | Identificador Único do Programa |

### programas-acoes-orcamentarias

Retorna uma Lista Paginada dos dados das Ações Orçamentárias dos Programas - TED. Grupo: Programas.

- PK: não declarada · linhas em 15/10/2026: 6.438
- Junções: `id_programa` → `programas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_acao_orcamentaria_programa` | integer | contém | Identificador Único da Ação Orçamentária |
| `tx_codigo_acao_orcamentaria` | string | contém | Código da Ação Orçamentária |
| `tx_descricao_acao_orcamentaria` | string | contém | Descrição da Ação Orçamentária |
| `id_programa` | integer | contém | Identificador Único do Programa |

### planos-acao

Retorna uma Lista Paginada dos dados dos Planos de Ação - TED. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 6.477
- Junções: `id_plano_acao` ← `planos-acao-metas`, `planos-acao-analises`, `planos-acao-pareceres`, `planos-trabalho-cronogramas`, `termos-execucao`, `notas-credito`, `programacoes-financeiras`; `id_programa` → `programas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `responsavel_execucao_sup` | string | contém | Nome da Unidade Superior Responsável pela Execução |
| `unidade_responsavel_execucao_orgao_fk` | integer | igual | Identificador Único da Unidade Responsável pela Execução |
| `descentralizada_sup` | string | contém | Nome da Unidade Superior Descentralizada (Recebedor) |
| `unidade_descentralizada_orgao_fk` | integer | igual | Identificador Único da Unidade Descentralizada (Recebedor) |
| `codigo_plano_acao` | string | contém | Código do Plano de Ação |
| `id_programa` | integer | contém | Identificador Único do Programa |
| `unidade_descentralizada_gestora` | integer | igual | Código da Unidade Gestora Descentralizada (Recebedor) |
| `unidade_responsavel_execucao_gestora` | integer | igual | Código da Unidade Gestora Responsável pela Execução |
| `vl_total_plano_acao` | number | igual | Valor Total do Plano de Ação |
| `dt_inicio_vigencia` | date | igual (AAAA-MM-DD) | Data do Início da Vigência do Plano de Ação (YYYY-MM-DD) |
| `dt_fim_vigencia` | date | igual (AAAA-MM-DD) | Data Final da Vigência do Plano de Ação (YYYY-MM-DD) |
| `tx_objeto_plano_acao` | string | contém | Objeto do Plano de Ação |
| `tx_justificativa_plano_acao` | string | contém | Justificativa do Plano de Ação |
| `in_forma_execucao_direta` | boolean | igual | Indicador da Forma de Execução Direta |
| `in_forma_execucao_particulares` | boolean | igual | Indicador da Forma de Execução Particulares |
| `in_forma_execucao_descentralizada` | boolean | igual | Indicador da Forma de Execução Descentralizada |
| `tx_situacao_plano_acao` | string | contém | Situação do Plano de Ação |
| `aa_ano_plano_acao` | integer | igual | Ano do Plano de Ação |
| `vl_beneficiario_especifico` | number | igual | Valor do Beneficiário Específico |
| `vl_chamamento_publico` | number | igual | Valor do Chamamento Público |
| `sq_instrumento` | string | contém | Sequencial do Instrumento |
| `aa_instrumento` | integer | igual | Ano do Instrumento |
| `unidade_descentralizada` | string | contém | Nome da Unidade Descentralizada (Recebedor) |
| `sigla_unidade_descentralizada` | string | contém | Sigla da Unidade Descentralizada (Recebedor) |
| `sigla_descentralizada_sup` | string | contém | Sigla da Unidade Superior Descentralizada (Recebedor) |
| `cd_descentralizada_sup` | integer | igual | Código da Unidade Superior Descentralizada (Recebedor) |
| `unidade_responsavel_execucao` | string | contém | Nome da Unidade Responsável pela Execução |
| `sigla_unidade_responsavel_execucao` | string | contém | Sigla da Unidade Responsável pela Execução |
| `sigla_responsavel_execucao_sup` | string | contém | Sigla da Unidade Superior Responsável pela Execução |
| `cd_responsavel_execucao_sup` | integer | igual | Código da Unidade Superior Responsável pela Execução |

### planos-acao-metas

Retorna uma Lista Paginada dos dados das Metas dos Planos de Ação - TED. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 23.414
- Junções: `id_meta` ← `planos-acao-metas-etapas`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_meta` | integer | contém | Identificador Único da Meta do Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `nr_numero_meta` | integer | igual | Número da Meta do Plano de Ação |
| `tx_nome_meta` | string | contém | Nome da Meta do Plano de Ação |
| `tx_descricao_meta` | string | contém | Descrição da Meta do Plano de Ação |
| `tp_unidade_meta` | string | contém | Tipo de Unidade da Meta do Plano de Ação |
| `nr_quantidade_meta` | integer | igual | Número de Quantidade da Meta do Plano de Ação |
| `vl_valor_unitario_meta` | number | igual | Valor Unitário da Meta do Plano de Ação |
| `dt_inicio_vigencia_meta` | date | igual (AAAA-MM-DD) | Data de Início da Vigência de Meta do Plano de Ação (YYYY-MM-DD) |
| `dt_fim_vigencia_meta` | date | igual (AAAA-MM-DD) | Data Final da Vigência de Meta do Plano de Ação (YYYY-MM-DD) |

### planos-acao-metas-etapas

Retorna uma Lista Paginada dos dados das Etapas das Metas dos Planos de Ação - TED. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 57.919
- Junções: `id_meta` → `planos-acao-metas`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_etapa` | integer | contém | Identificador Único da Etapa do Plano de Ação |
| `id_meta` | integer | contém | Identificador Único da Meta do Plano de Ação |
| `nr_numero_etapa` | integer | igual | Número da Etapa do Plano de Ação |
| `tx_nome_etapa` | string | contém | Nome da Etapa do Plano de Ação |
| `tx_descricao_etapa` | string | contém | Descrição da Etapa do Plano de Ação |
| `nr_quantidade_etapa` | integer | igual | Número de Quantidade da Etapa do Plano de Ação |
| `vl_valor_unitario_etapa` | number | igual | Valor Unitário da Etapa do Plano de Ação |
| `dt_inicio_vigencia_etapa` | date | igual (AAAA-MM-DD) | Data de Início da Vigência da Etapa do Plano de Ação (YYYY-MM-DD) |
| `dt_fim_vigencia_etapa` | date | igual (AAAA-MM-DD) | Data Final da Vigência da Etapa do Plano de Ação (YYYY-MM-DD) |
| `unidade_medida_etapa` | string | contém | Unidade de Medida da Etapa do Plano de Ação |

### planos-acao-analises

Retorna uma Lista Paginada dos dados das Análises dos Planos de Ação - TED. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 5.943
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_analise` | integer | contém | Identificador Único da Análise do Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `tx_justificativa_analise` | string | contém | Justificativa da Análise do Plano de Ação |
| `resultado_analise` | string | contém | Resultado da Análise do Plano de Ação |
| `tx_situacao_analise` | string | contém | Situação da Análise do Plano de Ação |

### planos-acao-pareceres

Retorna uma Lista Paginada dos dados dos Pareceres dos Planos de Ação - TED. Grupo: Planos de Ação.

- PK: `id_parecer` · linhas em 15/10/2026: 8.755
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_parecer` | integer · PK | contém | Identificador Único do Parecer do Plano de Ação |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `tp_analise_parecer` | string | contém | Tipo da Análise do Parecer do Plano de Ação |
| `resultado_parecer` | string | contém | Resultado do Parecer do Plano de Ação |
| `tx_parecer` | string | contém | Parecer do Plano de Ação |
| `plano_acao_hist_fk` | integer | contém | Identificador Único do Histórico do Plano de Ação |
| `dt_data_parecer` | date | contém | Data do Parecer do Plano de Ação |

### planos-trabalho-cronogramas

Retorna uma Lista Paginada dos dados dos Cronogramas dos Planos de Trabalho - TED. Grupo: Planos de Trabalho.

- PK: não declarada · linhas em 15/10/2026: 14.320
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_cronograma_plano_trabalho` | integer | contém | Identificador Único do Cronograma do Plano de Trabalho |
| `id_plano_trabalho` | integer | contém | Identificador Único do Plano de Trabalho |
| `mes_cronograma_plano_trabalho` | string | contém | Mês do Cronograma do Plano de Trabalho |
| `ano_cronograma_plano_trabalho` | integer | igual | Ano do Cronograma do Plano de Trabalho |
| `valor_cronograma_plano_trabalho` | number | igual | Valor do Cronograma do Plano de Trabalho |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |

### termos-execucao

Retorna uma Lista Paginada dos dados dos Termos de Execução - TED. Grupo: Termos de Execução.

- PK: não declarada · linhas em 15/10/2026: 5.177
- Junções: `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_termo` | integer | contém | Identificador Único do Termo de Execução |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `tx_situacao_termo` | string | contém | Situação do Termo de Execução |
| `tx_num_processo_sei` | string | contém | Número do Processo SEI do Termo de Execução |
| `dt_assinatura_termo` | date | igual (AAAA-MM-DD) | Data de Assinatura do Termo de Execução (YYYY-MM-DD) |
| `dt_divulgacao_termo` | date | igual (AAAA-MM-DD) | Data de Divulgação do Termo de Execução (YYYY-MM-DD) |
| `in_minuta_padrao` | boolean | igual | Indicador Minuta Padrão do Termo de Execução |
| `formalizacao_termo_execucao__tx_numero_ns_termo` | string | — | Tx Numero Ns Termo |
| `formalizacao_termo_execucao__dt_recebimento_termo` | date-time | — | Dt Recebimento Termo |
| `formalizacao_termo_execucao__dt_efetivacao_termo` | date-time | — | Dt Efetivacao Termo |
| `link_termo_execucao__tx_link` | string | — | Tx Link |

Filtros aceitos pela API que não vêm como coluna na resposta: `tx_numero_ns_termo` (contém); `dt_recebimento_termo` (igual (AAAA-MM-DD)); `dt_efetivacao_termo` (igual (AAAA-MM-DD)); `tx_link` (contém).

### notas-credito

Retorna uma Lista Paginada dos dados das Notas de Crédito - TED. Grupo: Notas de Crédito.

- PK: não declarada · linhas em 15/10/2026: 12.113
- Junções: `id_nota` ← `eventos`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_nota` | integer | contém | Identificador Único da Nota de Crédito |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `tx_minuta_nota` | string | contém | Minuta da Nota de Crédito |
| `tx_numero_nota` | string | contém | Número da Nota de Crédito |
| `dt_emissao_nota` | date-time | igual (AAAA-MM-DD) | Data e Hora de Emissão da Nota de Crédito (YYYY-MM-DDTHH:mm:ss.SSSSSS) |
| `cd_gestao_emitente_nota` | string | contém | Código da Gestão Emitente da Nota de Crédito |
| `cd_gestao_favorecida_nota` | string | contém | Código da Gestão Favorecida da Nota de Crédito |
| `tx_situacao_nota` | string | contém | Situação da Nota de Crédito |
| `cd_ug_emitente_nota` | string | contém | Código da Unidade Gestora Emitente da Nota de Crédito |
| `cd_ug_favorecida_nota` | string | contém | Código da Unidade Gestora Favorecida da Nota de Crédito |
| `tx_observacao_nota` | string | contém | Observação da Nota de Crédito |

### eventos

Retorna uma Lista Paginada dos dados dos Eventos - TED. Grupo: Notas de Crédito.

- PK: não declarada · linhas em 15/10/2026: 19.667
- Junções: `id_nota` → `notas-credito`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_evento_nota` | integer | contém | Identificador Único do Evento da Nota de Crédito |
| `id_nota` | integer | contém | Identificador Único da Nota de Crédito |
| `cd_evento` | string | contém | Código do Evento |
| `id_esfera_orcamentaria` | integer | igual | Identificador Único da Esfera Orçamentária do Evento |
| `cd_ptres_evento` | string | contém | Código PTRES do Evento |
| `cd_fonte_recurso_evento` | string | contém | Código da Fonte de Recurso do Evento |
| `cd_plano_interno_evento` | string | contém | Código do Plano Interno do Evento |
| `vl_evento` | number | igual | Valor do Evento |
| `cd_ug_responsavel_evento` | string | contém | Código da Unidade Gestora Responsável do Evento |
| `esfera_orcamentaria_evento__nome_esfera_orcamentaria` | string | — | Nome Esfera Orcamentaria |
| `natureza_despesa_evento__codigo_natureza` | string | — | Codigo Natureza |
| `natureza_despesa_evento__descricao_natureza` | string | — | Descricao Natureza |
| `id_natureza` | integer | igual | Identificador Único da Natureza de Despesa do Evento |
| `id_natureza_sub_it` | string | contém | Identificador Único do Subitem da Natureza de Despesa do Evento |
| `ptres_programa_trabalho_resumido` | string | contém | Número Plain do Programa de Trabalho Resumido - PTRES |
| `ptres_unidade_orcamentaria` | string | contém | Código da Unidade Orçamentária do SIAFI (Sistema Integrado de Administração Financeira), vinculada ao PTRES |
| `ptres_programa_trabalho` | string | contém | Código do Programa de Trabalho do SIAFI (Sistema Integrado de Administração Financeira), vinculado ao PTRES |
| `ptres_tipo_credito` | string | contém | Indicador de Tipo de Crédito. Alguns valores: A - Inicial (LOA), C - Especial, G - Extraordinário |
| `ptres_plano_orcamentario` | string | contém | Código do Plano Orçamentário do SIAFI (Sistema Integrado de Administração Financeira), vinculado ao PTRES |
| `ptres_codigo_autor_emenda` | string | contém | Código do autor da emenda parlamentar |
| `ptres_resultado_primario_original` | string | contém | Código do Indicador de Resultado Primário do Empenho |
| `ptres_resultado_primario` | string | contém | Resultado Primário do Empenho |
| `ptres_tipo_emenda` | string | contém | Tipo da Emenda |

Filtros aceitos pela API que não vêm como coluna na resposta: `codigo_natureza` (contém); `descricao_natureza` (contém); `nome_esfera_orcamentaria` (contém).

### programacoes-financeiras

Retorna uma Lista Paginada dos dados das Programações Financeiras - TED. Grupo: Programações Financeiras.

- PK: não declarada · linhas em 15/10/2026: 18.269
- Junções: `id_programacao` ← `programacoes-financeiras-trf`; `id_plano_acao` → `planos-acao`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_programacao` | integer | contém | Identificador Único da Programação Financeira |
| `id_plano_acao` | integer | contém | Identificador Único do Plano de Ação |
| `tp_pf_tipo_programacao` | string | contém | Tipo de Programação Financeira |
| `tx_minuta_programacao` | string | contém | Minuta da Programação Financeira |
| `tx_numero_programacao` | string | contém | Número da Programação Financeira |
| `tx_situacao_programacao` | string | contém | Situação da Programação Financeira |
| `tx_observacao_programacao` | string | contém | Observação da Programação Financeira |
| `ug_emitente_programacao` | string | contém | Situação da Programação Financeira |
| `ug_favorecida_programacao` | string | contém | Unidade Gestora Favorecida da Programação Financeira |
| `dh_recebimento_programacao` | date-time | igual (AAAA-MM-DD) | Data/Hora do Recebimento da Programação Financeira (YYYY-MM-DDTHH:mm:ss.SSSSSS) |

### programacoes-financeiras-trf

Retorna uma Lista Paginada dos dados dos Itens TRF das Programações Financeiras - TED. Grupo: Programações Financeiras.

- PK: não declarada · linhas em 15/10/2026: 20.410
- Junções: `id_programacao` → `programacoes-financeiras`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_item_trf` | integer | contém | Identificador Único do Item da Programação Financeira |
| `id_programacao` | integer | contém | Identificador Único da Programação Financeira |
| `cd_vinculacao_trf` | integer | igual | Código da Vinculação da Programação Financeira |
| `cd_fonte_recurso_trf` | string | contém | Código da Fonte de Recursos da Programação Financeira |
| `cd_categoria_gasto_trf` | string | contém | Código da Categoria de Gastos da Programação Financeira |
| `vl_valor_trf` | number | igual | Valor do Item da Programação Financeira |
| `cd_situacao_contabil_trf` | string | contém | Código da Situação Contábil da Programação Financeira |
