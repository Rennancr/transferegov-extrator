# Módulo `especiais` — API de dados abertos do módulo de Transferências Especiais do Transferegov

> Gerado por `tools/gerar_references.py` a partir do OpenAPI (versão 1.0). Não edite à mão; regenere quando o schema mudar.

- Endpoint base: `https://api-publica.transferegov.gestao.gov.br/especiais/<tabela>` · documentação: `https://api-publica.transferegov.gestao.gov.br/especiais/docs`
- Linhas por página (máximo): 200
- Volumes de **15/10/2026**: mudam a cada carga diária. Use só para ter a ordem de grandeza e confirme com `contar`.

## Índice

| Tabela | Conteúdo | Colunas | Linhas (aprox.) |
|---|---|---|---|
| [`plano-trabalho-analise-historico-especiais`](#plano-trabalho-analise-historico-especiais) | Retorna uma Lista Paginada dos dados do Histórico de Análises. | 7 | 62.388 |
| [`programas-especiais`](#programas-especiais) | Retorna uma Lista Paginada dos dados de Programas Especiais. | 24 | 15 |
| [`planos-acao-especiais`](#planos-acao-especiais) | Retorna uma Lista Paginada dos dados dos Planos de Ação Especiais. | 33 | 57.827 |
| [`planos-acao-historico-especiais`](#planos-acao-historico-especiais) | Retorna uma Lista Paginada dos dados do Histórico dos Planos de Ação Especiais. | 6 | 142.497 |
| [`beneficiarios-especiais`](#beneficiarios-especiais) | Retorna uma Lista Paginada dos dados dos Beneficiários Especiais. | 5 | 5.539 |
| [`planos-trabalho-especiais`](#planos-trabalho-especiais) | Retorna uma Lista Paginada dos dados dos Planos de Trabalho Especiais. | 14 | 56.416 |
| [`planos-trabalho-analises-especiais`](#planos-trabalho-analises-especiais) | Retorna uma Lista Paginada dos dados das Análises dos Planos de Trabalho Especiais. | 10 | 106.755 |
| [`relatorios-gestao-novos-especiais`](#relatorios-gestao-novos-especiais) | Retorna uma Lista Paginada dos dados dos Relatórios de Gestão Novos Especiais. | 9 | 27.384 |
| [`relatorios-gestao-analise-especiais`](#relatorios-gestao-analise-especiais) | Retorna uma Lista Paginada dos dados das Análises dos Relatórios de Gestão Especiais. | 10 | 15 |
| [`relatorios-gestao-documento-liquidacao-especiais`](#relatorios-gestao-documento-liquidacao-especiais) | Retorna uma Lista Paginada dos dados dos Documentos de Liquidação dos Relatórios de Gestão Especiais. | 9 | 103.809 |
| [`relatorios-gestao-especiais`](#relatorios-gestao-especiais) | Retorna uma Lista Paginada de dados de Relatórios de Gestão Especial. | 9 | 5.362 |
| [`empenhos-especiais`](#empenhos-especiais) | Retorna uma Lista Paginada dos dados dos Empenhos Especiais. | 24 | 60.322 |
| [`documentos-habeis-especiais`](#documentos-habeis-especiais) | Retorna uma Lista Paginada dos dados dos Documentos hábeis Especiais. | 25 | 57.986 |
| [`ordens-pagamentos-ordens-bancarias-especiais`](#ordens-pagamentos-ordens-bancarias-especiais) | Retorna uma Lista Paginada dos dados de Ordens de Pagamento e Ordens Bancárias Especiais. | 13 | 55.148 |
| [`executores-especiais`](#executores-especiais) | Retorna uma Lista Paginada dos dados dos Executores Especiais. | 17 | 57.372 |
| [`meta-especiais`](#meta-especiais) | Retorna uma Lista Paginada dos dados das Metas Especiais. | 16 | 156.193 |
| [`finalidade-especiais`](#finalidade-especiais) | Retorna uma Lista Paginada dos dados das Finalidades Especiais. | 5 | 94.358 |
| [`gestao-financeira-lancamentos-especiais`](#gestao-financeira-lancamentos-especiais) | Retorna uma Lista Paginada dos dados dos Lançamentos da Gestão Financeira Especiais. | 34 | 739.458 |
| [`gestao-financeira-subtransacoes-especiais`](#gestao-financeira-subtransacoes-especiais) | Retorna uma Lista Paginada dos dados das Subtransações da Gestão Financeira Especiais. | 14 | 14.123 |
| [`orgaos-analises-pendentes-especiais`](#orgaos-analises-pendentes-especiais) | Retorna uma Lista Paginada dos dados dos Órgãos de Análises Pendentes Especiais. | 4 | 0 |
| [`planos-trabalho-historico`](#planos-trabalho-historico) | Retorna uma Lista Paginada dos dados de Planos de Trabalho Histórico. | 5 | 461.138 |
| [`saldo-conta-gestao-financeira-especiais`](#saldo-conta-gestao-financeira-especiais) | Retorna uma Lista Paginada dos dados dos Saldos de Conta da Gestão Financeira Especiais. | 5 | 31.124 |
| [`devolucao-especiais`](#devolucao-especiais) | Retorna uma Lista Paginada dos dados das Devoluções de recursos dos Planos de Ação Especiais. | 22 | 438 |

## Chaves de junção prováveis

Uma coluna `id_*` presente em várias tabelas costuma ser a chave da junção. A "dona" é a tabela em que a chave é a 1ª coluna (ou a PK); nas outras, ela funciona como referência. É uma heurística: confira os valores antes de confiar na junção.

| Chave | Tabela dona (provável) | Também aparece em |
|---|---|---|
| `id_agencia_conta` | `saldo-conta-gestao-financeira-especiais` | `planos-acao-especiais`, `gestao-financeira-lancamentos-especiais` |
| `id_beneficiario` | `beneficiarios-especiais` | `planos-acao-especiais` |
| `id_dh` | `documentos-habeis-especiais` | `ordens-pagamentos-ordens-bancarias-especiais` |
| `id_empenho` | `empenhos-especiais` | `documentos-habeis-especiais` |
| `id_executor` | `executores-especiais` | `relatorios-gestao-novos-especiais`, `meta-especiais`, `finalidade-especiais` |
| `id_lancamento_gestao_financeira` | `gestao-financeira-lancamentos-especiais` | `gestao-financeira-subtransacoes-especiais` |
| `id_plano_acao` | `planos-acao-especiais` | `planos-acao-historico-especiais`, `planos-trabalho-especiais`, `relatorios-gestao-novos-especiais`, `relatorios-gestao-especiais`, `empenhos-especiais`, `executores-especiais`, `devolucao-especiais` |
| `id_plano_trabalho` | `planos-trabalho-especiais` | `planos-trabalho-analises-especiais`, `orgaos-analises-pendentes-especiais`, `planos-trabalho-historico` |
| `id_plano_trabalho_analise_pt` | `planos-trabalho-analises-especiais` | `plano-trabalho-analise-historico-especiais` |
| `id_programa` | `programas-especiais` | `planos-acao-especiais` |
| `id_relatorio_gestao_novo` | `relatorios-gestao-novos-especiais` | `relatorios-gestao-analise-especiais`, `relatorios-gestao-documento-liquidacao-especiais` |

## Tabelas

### plano-trabalho-analise-historico-especiais

Retorna uma Lista Paginada dos dados do Histórico de Análises. Grupo: Análises.

- PK: não declarada · linhas em 15/10/2026: 62.388
- Junções: `id_plano_trabalho_analise_pt` → `planos-trabalho-analises-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `codigo_siorg_orgao_analise_pt_hist` | integer | igual | Código SIORG do órgão responsável pela análise registrada no histórico. |
| `nome_orgao_analise_pt_hist` | string | contém | Nome do órgão responsável pela análise registrada no histórico. |
| `situacao_parecer_analise_pt_hist` | string | lista: Aprovar Plano de Trabalho, Não se aplica, Reprovar Plano de Trabalho, Solicitar Complementação | Situação do parecer da análise no histórico. |
| `data_analise_pt_hist` | date-time | igual (AAAA-MM-DD) | Data e hora em que a análise foi registrada no histórico (AAAA-MM-DD). |
| `situacao_analise_pt_hist` | string | lista: Em elaboração, Concluída, Não se aplica | Situação da análise no momento do registro histórico. |
| `responsaveis_analise_pt_hist` | string | contém | Responsáveis pela análise registrada no histórico. |
| `id_plano_trabalho_analise_pt` | integer | igual | Identificador único da análise do plano de trabalho ao qual este registro de histórico se refere. |

### programas-especiais

Retorna uma Lista Paginada dos dados de Programas Especiais. Grupo: Programa.

- PK: não declarada · linhas em 15/10/2026: 15
- Junções: `id_programa` ← `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_programa` | integer | igual | Identificador único do programa. |
| `ano_programa` | integer | igual | Ano de vigência ou cadastro do programa. |
| `modalidade_programa` | string | contém | Modalidade do programa. |
| `codigo_programa` | string | contém | Código alfanumérico único do programa. |
| `id_orgao_superior_programa` | integer | igual | ID do órgão superior (hierárquico) do programa. |
| `sigla_orgao_superior_programa` | string | contém | Sigla do órgão superior. |
| `cnpj_orgao_superior_programa` | string | contém | CNPJ do órgão superior. |
| `nome_orgao_superior_programa` | string | contém | Nome do órgão superior. |
| `id_orgao_programa` | integer | igual | ID do órgão executor do programa. |
| `sigla_orgao_programa` | string | contém | Sigla do órgão executor. |
| `cnpj_orgao_programa` | string | contém | CNPJ do órgão executor. |
| `nome_orgao_programa` | string | contém | Nome do órgão executor. |
| `id_unidade_gestora_programa` | integer | igual | ID da unidade gestora responsável. |
| `documentos_origem_programa` | string | contém | Documentos ou base legal que originaram o programa. |
| `id_unidade_orcamentaria_responsavel_programa` | integer | igual | ID da unidade orçamentária responsável. |
| `data_inicio_ciencia_programa` | date | igual (AAAA-MM-DD) | Data de início da ciência do programa (AAAA-MM-DD). |
| `data_fim_ciencia_programa` | date | igual (AAAA-MM-DD) | Data de término da ciência do programa (AAAA-MM-DD). |
| `valor_necessidade_financeira_programa` | number | igual | Valor total da necessidade financeira estimada para o programa. |
| `valor_total_disponibilizado_programa` | number | igual | Valor total já disponibilizado para o programa. |
| `valor_impedido_programa` | number | igual | Valor que está impedido de ser usado. |
| `valor_a_disponibilizar_programa` | number | igual | Valor restante a ser disponibilizado. |
| `valor_documentos_habeis_gerados_programa` | number | igual | Valor total dos documentos hábeis gerados. |
| `valor_obs_geradas_programa` | number | igual | Valor total de Ordens Bancárias (OBs) geradas. |
| `valor_disponibilidade_atual_programa` | number | igual | Valor da disponibilidade financeira atual do programa. |

### planos-acao-especiais

Retorna uma Lista Paginada dos dados dos Planos de Ação Especiais. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 57.827
- Junções: `id_plano_acao` ← `planos-acao-historico-especiais`, `planos-trabalho-especiais`, `relatorios-gestao-novos-especiais`, `relatorios-gestao-especiais`, `empenhos-especiais`, `executores-especiais`, `devolucao-especiais`; `id_agencia_conta` → `saldo-conta-gestao-financeira-especiais`; `id_beneficiario` → `beneficiarios-especiais`; `id_programa` → `programas-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_acao` | integer | igual | Identificador único do plano de ação (chave primária). |
| `codigo_plano_acao` | string | contém | Código identificador do plano de ação. |
| `ano_plano_acao` | integer | igual | Ano do plano de ação (AAAA). |
| `modalidade_plano_acao` | string | contém | Modalidade do plano de ação. |
| `situacao_plano_acao` | string | lista: CIENTE, IMPEDIDO | Situação atual do plano de ação. |
| `email_camara` | string | contém | E-mail de contato da câmara. |
| `data_aceite_plano_acao` | date | igual (AAAA-MM-DD) | Data de aceite do plano de ação (AAAA-MM-DD). |
| `codigo_banco_plano_acao` | string | contém | Código do banco associado ao plano. |
| `codigo_situacao_dado_bancario_plano_acao` | integer | igual | Código da situação dos dados bancários. |
| `descricao_situacao_dado_bancario_plano_acao` | string | contém | Descrição da situação dos dados bancários. |
| `nome_banco_plano_acao` | string | contém | Nome do banco associado ao plano. |
| `numero_agencia_plano_acao` | string | contém | Número da agência bancária. |
| `dv_agencia_plano_acao` | string | contém | Dígito verificador da agência. |
| `numero_conta_plano_acao` | string | contém | Número da conta bancária. |
| `dv_conta_plano_acao` | string | contém | Dígito verificador da conta bancária. |
| `nome_parlamentar_emenda_plano_acao` | string | contém | Nome do parlamentar associado à emenda. |
| `ano_emenda_parlamentar_plano_acao` | integer | igual | Ano da emenda parlamentar. |
| `codigo_parlamentar_emenda_plano_acao` | integer | igual | Código do parlamentar da emenda. |
| `sequencial_emenda_parlamentar_plano_acao` | integer | igual | Sequencial da emenda parlamentar. |
| `numero_emenda_parlamentar_plano_acao` | integer | igual | Número da emenda parlamentar. |
| `codigo_emenda_parlamentar_formatado_plano_acao` | string | contém | Código formatado da emenda parlamentar. |
| `categoria_despesa_plano_acao` | string | lista: CUSTEIO, CUSTEIO E INVESTIMENTO, INVESTIMENTO | Categoria de despesa do plano de ação. |
| `codigo_descricao_areas_politicas_publicas_plano_acao` | string | contém | Códigos e descrições de áreas de políticas públicas relacionadas. |
| `descricao_programacao_orcamentaria_plano_acao` | string | contém | Descrição da programação orçamentária vinculada ao plano de ação. |
| `motivo_impedimento_plano_acao` | string | contém | Motivo de impedimento do plano de ação. |
| `valor_custeio_plano_acao` | number | igual | Valor de custeio do plano de ação. |
| `valor_investimento_plano_acao` | number | igual | Valor de investimento do plano de ação. |
| `id_agencia_conta` | string | contém | Identificador da agência/conta. |
| `id_beneficiario` | integer | igual | Identificador do beneficiário. |
| `id_objeto` | integer | igual | Identificador do objeto. |
| `nome_objeto` | string | contém | Nome do objeto. |
| `detalhamento_objeto` | string | contém | Detalhamento do objeto. |
| `id_programa` | integer | igual | Identificador do programa. |

### planos-acao-historico-especiais

Retorna uma Lista Paginada dos dados do Histórico dos Planos de Ação Especiais. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 142.497
- Junções: `id_plano_acao` → `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_historico_plano_acao` | integer | igual | Identificador Único do Histórico do Plano de Ação |
| `situacao_historico_plano_acao` | string | lista: AGUARDANDO_CIENCIA, AGUARDANDO_CONCLUSAO_PLANO_TRABALHO, CIENTE, IMPEDIDO, IMPEDIDO_REJEICAO_PLANO_TRABALHO | Situação do Histórico do Plano de Ação |
| `operacao_historico_plano_acao` | string | lista: ATUALIZACAO, INSERCAO | Operação do Histórico do Plano de Ação |
| `descricao_historico_plano_acao` | string | contém | Descrição do Histórico do Plano de Ação |
| `data_hora_historico_plano_acao` | date-time | igual (AAAA-MM-DD) | Data e Hora do Histórico do Plano de Ação (AAAA-MM-DD) |
| `id_plano_acao` | integer | igual | Identificador do Plano de Ação |

### beneficiarios-especiais

Retorna uma Lista Paginada dos dados dos Beneficiários Especiais. Grupo: Planos de Ação.

- PK: não declarada · linhas em 15/10/2026: 5.539
- Junções: `id_beneficiario` ← `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_beneficiario` | integer | igual | Identificador Único do Beneficiário |
| `uf_beneficiario` | string | lista (27 valores; veja `colunas`) | UF do Beneficiário |
| `nome_beneficiario` | string | contém | Nome do Beneficiário |
| `cnpj_beneficiario` | string | contém | CNPJ do Beneficiário |
| `id_ente` | integer | igual | Identificador do Ente |

### planos-trabalho-especiais

Retorna uma Lista Paginada dos dados dos Planos de Trabalho Especiais. Grupo: Planos de Trabalho.

- PK: não declarada · linhas em 15/10/2026: 56.416
- Junções: `id_plano_trabalho` ← `planos-trabalho-analises-especiais`, `orgaos-analises-pendentes-especiais`, `planos-trabalho-historico`; `id_plano_acao` → `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_trabalho` | integer | igual | Identificador único do plano de trabalho. |
| `dt_hora_situacao_plano_trabalho` | date-time | igual (AAAA-MM-DD) | Data e hora da situação atual do plano de trabalho (AAAA-MM-DD). |
| `situacao_plano_trabalho` | string | contém | Descrição textual da situação do plano. |
| `ind_orcamento_proprio_plano_trabalho` | string | lista: Sim, Não | Indicador se o plano possui orçamento próprio. |
| `data_inicio_execucao_plano_trabalho` | date | igual (AAAA-MM-DD) | Data de início da execução do plano (AAAA-MM-DD). |
| `data_fim_execucao_plano_trabalho` | date | igual (AAAA-MM-DD) | Data de término da execução do plano (AAAA-MM-DD). |
| `prazo_execucao_meses_plano_trabalho` | integer | igual | Prazo de execução em meses. |
| `id_plano_acao` | integer | igual | Identificador do plano de ação a qual o plano de trabalho está vinculado. |
| `classificacao_orcamentaria_pt` | string | contém | Classificação orçamentária detalhada do plano de trabalho. |
| `ind_justificativa_prorrogacao_atraso_pt` | string | lista: SIM, NÃO | Indicador de justificativa para prorrogação por atraso. |
| `ind_justificativa_prorrogacao_paralizacao_pt` | string | lista: SIM, NÃO | Indicador de justificativa para prorrogação por paralisação. |
| `justificativa_prorrogacao_paralizacao_pt` | string | contém | Texto da justificativa para prorrogação por paralisação. |
| `dt_hora_pt_aprovado` | date-time | contém | Data e hora em que o plano de trabalho foi aprovado. |
| `ind_orgao_analises_pendentes` | string | lista: Não, Sim | Indicador de pendências de análise por parte do órgão. |

### planos-trabalho-analises-especiais

Retorna uma Lista Paginada dos dados das Análises dos Planos de Trabalho Especiais. Grupo: Análises.

- PK: não declarada · linhas em 15/10/2026: 106.755
- Junções: `id_plano_trabalho_analise_pt` ← `plano-trabalho-analise-historico-especiais`; `id_plano_trabalho` → `planos-trabalho-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_trabalho_analise_pt` | integer | igual | Identificador Único da Análise do Plano de Trabalho |
| `codigo_siorg_orgao_analise_pt` | integer | igual | Código SIORG do Órgão de Análise do Plano de Trabalho |
| `nome_orgao_analise_pt` | string | contém | Nome do Órgão de Análise do Plano de Trabalho |
| `situacao_planejamento_pt` | string | lista: APROVADO, CONCLUIDO, CONCLUIDO_NT_TCU, EM_ADITIVACAO, EM_COMPLEMENTACAO, ENVIADO_PARA_ANALISE, REPROVADO | Situação do Planejamento do Plano de Trabalho |
| `situacao_parecer_analise_pt` | string | lista: Aprovar Plano de Trabalho, Não se aplica, Reprovar Plano de Trabalho, Solicitar Complementação | Situação do Parecer de Análise do Plano de Trabalho |
| `texto_parecer_analise_pt` | string | contém | Texto do Parecer de Análise do Plano de Trabalho |
| `situacao_analise_pt` | string | lista: Concluída, Em elaboração | Situação da Análise do Plano de Trabalho |
| `data_analise_pt` | date-time | igual (AAAA-MM-DD) | Data da Análise do Plano de Trabalho (AAAA-MM-DD) |
| `valor_reprovado_pt` | number | igual | Valor Reprovado do Plano de Trabalho |
| `id_plano_trabalho` | integer | igual | Identificador do Plano de Trabalho |

### relatorios-gestao-novos-especiais

Retorna uma Lista Paginada dos dados dos Relatórios de Gestão Novos Especiais. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 27.384
- Junções: `id_relatorio_gestao_novo` ← `relatorios-gestao-analise-especiais`, `relatorios-gestao-documento-liquidacao-especiais`; `id_plano_acao` → `planos-acao-especiais`; `id_executor` → `executores-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao_novo` | integer | igual | Identificador Único do Relatório de Gestão Novo |
| `data_relatorio_gestao_novo` | date | igual (AAAA-MM-DD) | Data do Relatório de Gestão Novo (AAAA-MM-DD) |
| `data_e_hora_relatorio_gestao_novo` | date-time | igual (AAAA-MM-DD) | Data e Hora do Relatório de Gestão Novo (AAAA-MM-DD) |
| `tipo_relatorio_gestao_novo` | string | lista: Final, Parcial | Tipo do Relatório de Gestão Novo |
| `valor_executado_relatorio_gestao_novo` | number | igual | Valor Executado do Relatório de Gestão Novo |
| `valor_pendente_relatorio_gestao_novo` | number | igual | Valor Pendente do Relatório de Gestão Novo |
| `situacao_relatorio_gestao_novo` | string | lista: DISPONIBILIZADO, EM_ELABORACAO | Situação do Relatório de Gestão Novo |
| `id_plano_acao` | integer | igual | Identificador do Plano de Ação |
| `id_executor` | integer | igual | Identificador do Executor |

### relatorios-gestao-analise-especiais

Retorna uma Lista Paginada dos dados das Análises dos Relatórios de Gestão Especiais. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 15
- Junções: `id_relatorio_gestao_novo` → `relatorios-gestao-novos-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao_analise` | integer | contém | Identificador único da análise do relatório de gestão (lista separada por vírgula). |
| `id_relatorio_gestao_novo` | integer | contém | Identificador do relatório de gestão novo associado à análise (lista separada por vírgula). |
| `tx_parecer_relatorio_gestao_analise` | string | contém | Texto do parecer emitido na análise do relatório de gestão. |
| `st_parecer_relatorio_gestao_analise` | string | contém | Situação do parecer emitido na análise. Domínio: Aprovar Plano de Trabalho, Não se aplica, Reprovar Plano de Trabalho, Solicitar Complementação |
| `st_analise_relatorio_gestao_analise` | string | contém | Situação geral da análise do relatório de gestão. Domínio: Concluída, Em elaboração |
| `cd_orgao_siorg_relatorio_gestao_analise` | integer | igual | Código SIORG do órgão responsável pela análise. |
| `tx_orgao_nome_relatorio_gestao_analise` | string | contém | Nome do órgão que realizou a análise. |
| `dt_analise_relatorio_gestao_analise` | date-time | igual (AAAA-MM-DD) | Data e hora da análise do relatório de gestão (AAAA-MM-DD). |
| `tx_cpf_mascarado_relatorio_gestao_analise` | string | contém | CPF do responsável pela análise, mascarado. |
| `tx_nome_mascarado_relatorio_gestao_analise` | string | contém | Nome do responsável pela análise, mascarado. |

Filtros aceitos pela API que não vêm como coluna na resposta: `tx_cpf_relatorio_gestao_analise` (contém); `tx_nome_relatorio_gestao_analise` (contém).

### relatorios-gestao-documento-liquidacao-especiais

Retorna uma Lista Paginada dos dados dos Documentos de Liquidação dos Relatórios de Gestão Especiais. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 103.809
- Junções: `id_relatorio_gestao_novo` → `relatorios-gestao-novos-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao_dl` | integer | contém | Identificador único do documento de liquidação do relatório de gestão (lista separada por vírgula). |
| `id_relatorio_gestao_novo` | integer | contém | Identificador do relatório de gestão novo associado ao documento de liquidação (lista separada por vírgula). |
| `tx_descricao_relatorio_gestao_dl` | string | contém | Descrição do documento de liquidação do relatório de gestão. |
| `tp_doc_recebedor_relatorio_gestao_dl` | string | lista: CNPJ, CPF | Tipo de documento do recebedor do pagamento. Domínio: CNPJ, CPF |
| `tx_identificacao_recebedor_mascarado_relatorio_gestao_dl` | string | — | Tx Identificacao Recebedor Mascarado Relatorio Gestao Dl |
| `tx_nome_recebedor_relatorio_gestao_dl` | string | contém | Nome do recebedor do pagamento. |
| `vl_pagamento_relatorio_gestao_dl` | number | igual | Valor monetário do pagamento realizado no documento de liquidação. |
| `dt_pagamento_relatorio_gestao_dl` | date | igual (AAAA-MM-DD) | Data em que o pagamento foi realizado (AAAA-MM-DD). |
| `tx_natureza_relatorio_gestao_dl` | string | lista: INVESTIMENTO, CUSTEIO | Natureza da despesa do pagamento. Domínio: INVESTIMENTO, CUSTEIO |

Filtros aceitos pela API que não vêm como coluna na resposta: `tx_identificacao_recebedor_relatorio_gestao_dl` (contém).

### relatorios-gestao-especiais

Retorna uma Lista Paginada de dados de Relatórios de Gestão Especial. Grupo: Relatórios de Gestão.

- PK: não declarada · linhas em 15/10/2026: 5.362
- Junções: `id_plano_acao` → `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_relatorio_gestao` | integer | igual | Identificador Único do Relatório de Gestão |
| `data_relatorio_gestao` | date | igual (AAAA-MM-DD) | Data de referência do relatório de gestão (AAAA-MM-DD) |
| `data_e_hora_relatorio_gestao` | date-time | — | Data E Hora Relatorio Gestao |
| `tipo_relatorio_gestao` | string | contém | Tipo do relatório. Domínio: Final, Parcial |
| `situacao_relatorio_gestao` | string | lista: DISPONIBILIZADO, EM_ELABORACAO | Situação atual do relatório. |
| `valor_executado_relatorio_gestao` | number | igual | Valor financeiro executado reportado neste relatório |
| `valor_pendente_relatorio_gestao` | number | igual | Valor financeiro pendente de execução reportado neste relatório |
| `descritivo_relatorio_gestao` | string | contém | Texto descritivo, justificativas ou observações detalhadas do relatório |
| `id_plano_acao` | integer | igual | Identificador Único do Plano de Ação Especial associado ao relatório |

### empenhos-especiais

Retorna uma Lista Paginada dos dados dos Empenhos Especiais. Grupo: Execução Financeira.

- PK: não declarada · linhas em 15/10/2026: 60.322
- Junções: `id_empenho` ← `documentos-habeis-especiais`; `id_plano_acao` → `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_empenho` | integer | igual | Identificador único do empenho especial. |
| `id_minuta_empenho` | string | contém | Identificador da minuta de empenho associada. |
| `numero_empenho` | string | contém | Número do empenho. |
| `situacao_empenho` | integer | igual | Código da situação atual do empenho. |
| `descricao_situacao_empenho` | string | lista: Minuta de Empenho, Enviado | Descrição da situação atual do empenho. |
| `tipo_documento_empenho` | integer | igual | Código do tipo de documento do empenho. |
| `descricao_tipo_documento_empenho` | string | contém | Descrição do tipo de documento do empenho. |
| `status_processamento_empenho` | string | lista: AGUARDANDO_GERACAO_EMPENHO, ENVIADA | Status de processamento do empenho. |
| `ug_responsavel_empenho` | integer | igual | Unidade Gestora responsável pelo empenho. |
| `ug_emitente_empenho` | integer | igual | Unidade Gestora que emitiu o empenho. |
| `descricao_ug_emitente_empenho` | string | contém | Descrição da Unidade Gestora emitente. |
| `fonte_recurso_empenho` | string | contém | Código da fonte de recurso utilizada no empenho. |
| `plano_interno_empenho` | string | lista: 13326EMTESP, T.ESPECIAIS | Plano Interno do empenho. |
| `ptres_empenho` | integer | igual | Programa de Trabalho Resumido do empenho. |
| `grupo_natureza_despesa_empenho` | integer | igual | Grupo de Natureza da Despesa do empenho. |
| `natureza_despesa_empenho` | integer | igual | Natureza da Despesa do empenho. |
| `subitem_empenho` | integer | igual | Código do subitem de despesa do empenho. |
| `categoria_despesa_empenho` | string | lista: INVESTIMENTO, CUSTEIO | Categoria de Despesa do empenho. |
| `modalidade_despesa_empenho` | integer | igual | Modalidade de Despesa do empenho. |
| `numero_ro_empenho` | string | contém | Número do Registro de Ordem associado ao empenho. |
| `data_emissao_empenho` | date | igual (AAAA-MM-DD) | Data de emissão do empenho (AAAA-MM-DD). |
| `prioridade_desbloqueio_empenho` | integer | igual | Prioridade para desbloqueio do empenho. |
| `valor_empenho` | number | igual | Valor monetário total do empenho. |
| `id_plano_acao` | integer | igual | Identificador do plano de ação associado. |

### documentos-habeis-especiais

Retorna uma Lista Paginada dos dados dos Documentos hábeis Especiais. Grupo: Execução Financeira.

- PK: não declarada · linhas em 15/10/2026: 57.986
- Junções: `id_dh` ← `ordens-pagamentos-ordens-bancarias-especiais`; `id_empenho` → `empenhos-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_dh` | integer | igual | Identificador único do Documento Hábil. |
| `id_minuta_documento_habil` | string | contém | Identificador da minuta do documento hábil. |
| `numero_documento_habil` | string | contém | Número do documento hábil. |
| `situacao_dh` | integer | igual | Código da situação do Documento Hábil. |
| `descricao_situacao_dh` | string | contém | Descrição da situação do Documento Hábil. |
| `tipo_documento_dh` | string | contém | Tipo do Documento Hábil. |
| `ug_emitente_dh` | integer | igual | Código da Unidade Gestora emitente do Documento Hábil. |
| `descricao_ug_emitente_dh` | string | contém | Descrição da UG emitente. |
| `data_vencimento_dh` | date | igual (AAAA-MM-DD) | Data de vencimento do Documento Hábil (AAAA-MM-DD). |
| `data_emissao_dh` | date | igual (AAAA-MM-DD) | Data de emissão do Documento Hábil (AAAA-MM-DD). |
| `ug_pagadora_dh` | integer | igual | Código da Unidade Gestora pagadora do Documento Hábil. |
| `descricao_ug_pagadora_dh` | string | contém | Descrição da UG pagadora. |
| `variacao_patrimonial_diminuta_dh` | integer | contém | Indicador de Variação Patrimonial Diminuta. |
| `passivo_transferencia_constitucional_legal_dh` | integer | contém | Indicador de Passivo de Transferência Constitucional/Legal. |
| `descricao_centro_custo_dh` | string | contém | Descrição do centro de custo do Documento Hábil. |
| `codigo_siorg_centro_custo_dh` | integer | igual | Código SIORG do centro de custo. |
| `mes_referencia_centro_custo_dh` | integer | contém | Mês de referência do centro de custo. |
| `ano_referencia_centro_custo_dh` | integer | igual | Ano de referência do centro de custo (AAAA). |
| `mes_ano_referencia_centro_custo_dh` | string | contém | Mês/Ano de referência do centro de custo (M/AAAA). |
| `ug_beneficiada_centro_custo_dh` | integer | igual | Código da Unidade Gestora beneficiada pelo centro de custo. |
| `descricao_ug_beneficiada_centro_custo_dh` | string | contém | Descrição da UG beneficiada pelo centro de custo. |
| `valor_dh` | number | igual | Valor total do Documento Hábil. |
| `valor_rateio_dh` | number | igual | Valor de rateio do Documento Hábil. |
| `valor_custo_centro_custo_dh` | number | igual | Valor de custo do centro de custo do Documento Hábil. |
| `id_empenho` | integer | igual | Identificador do Empenho associado. |

### ordens-pagamentos-ordens-bancarias-especiais

Retorna uma Lista Paginada dos dados de Ordens de Pagamento e Ordens Bancárias Especiais. Grupo: Execução Financeira.

- PK: não declarada · linhas em 15/10/2026: 55.148
- Junções: `id_dh` → `documentos-habeis-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_op_ob` | integer | igual | Identificador único da Ordem de Pagamento/Ordem Bancária. |
| `data_emissao_op` | date | igual (AAAA-MM-DD) | Data de emissão da Ordem de Pagamento (AAAA-MM-DD). |
| `numero_ordem_pagamento` | string | contém | Número da Ordem de Pagamento (AAAAOPNNNNNN)<br/>Ex.: “2020OP146800” |
| `vinculacao_op` | integer | igual | Código de vinculação da Ordem de Pagamento. |
| `situacao_op` | integer | igual | Código da situação da Ordem de Pagamento. |
| `descricao_situacao_op` | string | lista: OB Enviada à instituição bancária para pagamento, OP Pendente (Retorno com erro no envio ao SIAFI) | Descrição da situação da Ordem de Pagamento. |
| `data_situacao_op` | date | igual (AAAA-MM-DD) | Data em que a OP atingiu a situação atual (AAAA-MM-DD). |
| `data_emissao_ob` | date | igual (AAAA-MM-DD) | Data de emissão da Ordem Bancária (AAAA-MM-DD). |
| `numero_ordem_bancaria` | string | contém | Número da Ordem Bancária (AAAAOBNNNNNN) |
| `numero_ordem_lancamento` | string | contém | Número da Nota de Lançamento no sistema (AAAANSNNNNNN) |
| `data_assinatura_ordenador_despesa_ob` | date | igual (AAAA-MM-DD) | Data da assinatura do ordenador de despesa na Ordem Bancária (AAAA-MM-DD). |
| `data_assinatura_gestor_financeiro_ob` | date | igual (AAAA-MM-DD) | Data da assinatura do gestor financeiro na Ordem Bancária (AAAA-MM-DD). |
| `id_dh` | integer | igual | Identificador do Documento Hábil associado. |

### executores-especiais

Retorna uma Lista Paginada dos dados dos Executores Especiais. Grupo: Planos de Trabalho.

- PK: não declarada · linhas em 15/10/2026: 57.372
- Junções: `id_executor` ← `relatorios-gestao-novos-especiais`, `meta-especiais`, `finalidade-especiais`; `id_plano_acao` → `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_executor` | integer | igual | Identificador do executor. |
| `cnpj_executor` | string | contém | Número do Cadastro Nacional da Pessoa Jurídica (CNPJ) do executor. |
| `nome_executor` | string | contém | Nome ou Razão Social do executor. |
| `objeto_executor` | string | contém | Descrição detalhada do objeto da execução ou parceria. |
| `vl_custeio_executor` | number | igual | Valor destinado ao custeio da execução. |
| `vl_investimento_executor` | number | igual | Valor destinado a investimento na execução. |
| `ind_recursos_gerenciados_conta_especifica_executor` | string | lista: Sim, Não | Indicador de recursos gerenciados em conta específica. |
| `codigo_banco_executor` | string | contém | Código do banco onde a conta do executor está cadastrada. |
| `nome_banco_executor` | string | contém | Nome do banco. |
| `numero_agencia_executor` | string | contém | Número da agência bancária do executor. |
| `numero_dv_agencia_executor` | string | contém | Dígito verificador da agência bancária. |
| `nome_agencia_executor` | string | contém | Nome da agência bancária. |
| `numero_conta_executor` | string | contém | Número da conta bancária do executor. |
| `numero_dv_conta_executor` | string | contém | Dígito verificador da conta bancária. |
| `codigo_situacao_dado_bancario_executor` | integer | contém | Código da situação atual do dado bancário. |
| `descricao_situacao_dado_bancario_executor` | string | lista: , Aguardando Solicitação de Abertura de Conta, Conta Ativa | Descrição da situação do dado bancário. |
| `id_plano_acao` | integer | igual | Identificador do plano de ação associado. |

### meta-especiais

Retorna uma Lista Paginada dos dados das Metas Especiais. Grupo: Planos de Trabalho.

- PK: não declarada · linhas em 15/10/2026: 156.193
- Junções: `id_executor` → `executores-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_executor` | integer | igual | Identificador do Executor associado à Meta. |
| `id_meta` | integer | igual | Identificador ÚnicoIdentificador único da Meta. |
| `sequencial_meta` | integer | igual | Número sequencial da Meta. |
| `nome_meta` | string | contém | Nome da Meta. |
| `desc_meta` | string | contém | Descrição detalhada da Meta. |
| `un_medida_meta` | string | contém | Unidade de medida da Meta. |
| `qt_unidade_meta` | integer | igual | Quantidade de unidades previstas na Meta. |
| `vl_custeio_emenda_especial_meta` | number | igual | Valor de custeio previsto com Emenda Especial. |
| `vl_investimento_emenda_especial_meta` | number | igual | Valor de investimento previsto com Emenda Especial. |
| `vl_custeio_recursos_proprios_meta` | number | igual | Valor de custeio previsto com Recursos Próprios. |
| `vl_investimento_recursos_proprios_meta` | number | igual | Valor de investimento previsto com Recursos Próprios. |
| `vl_custeio_rendimento_meta` | number | igual | Valor de custeio previsto com Rendimento. |
| `vl_investimento_rendimento_meta` | number | igual | Valor de investimento previsto com Rendimento. |
| `vl_custeio_doacao_meta` | number | igual | Valor de custeio previsto com Doação. |
| `vl_investimento_doacao_meta` | number | igual | Valor de investimento previsto com Doação. |
| `qt_meses_meta` | integer | igual | Quantidade de meses previstos para a execução da Meta. |

### finalidade-especiais

Retorna uma Lista Paginada dos dados das Finalidades Especiais. Grupo: Planos de Trabalho.

- PK: não declarada · linhas em 15/10/2026: 94.358
- Junções: `id_executor` → `executores-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_executor` | integer | igual | Identificador Único do Executor Especial |
| `cd_area_politica_publica_tipo_pt` | integer | igual | Código do tipo de política pública da Finalidade Plano de Trabalho Especial |
| `area_politica_publica_tipo_pt` | string | contém | Descrição do tipo de política pública da Finalidade do Plano de Trabalho Especial |
| `cd_area_politica_publica_pt` | integer | igual | Código da área da política pública da Finalidade do Plano de Trabalho Especial |
| `area_politica_publica_pt` | string | contém | Descrição da área da política pública da Finalidade do Plano de Trabalho Especial |

### gestao-financeira-lancamentos-especiais

Retorna uma Lista Paginada dos dados dos Lançamentos da Gestão Financeira Especiais. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 739.458
- Junções: `id_lancamento_gestao_financeira` ← `gestao-financeira-subtransacoes-especiais`; `id_agencia_conta` → `saldo-conta-gestao-financeira-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_lancamento_gestao_financeira` | string | contém | Identificador Único do Lançamento da Gestão Financeira |
| `origem_solicitacao_gestao_financeira` | string | contém | Origem da Solicitação da Gestão Financeira |
| `cnpj_ente_solicitante_gestao_financeira` | string | contém | CNPJ do Ente Solicitante da Gestão Financeira |
| `nome_ente_solicitante_gestao_financeira` | string | contém | Nome do Ente Solicitante da Gestão Financeira |
| `codigo_banco_gestao_financeira` | integer | igual | Código do Banco da Gestão Financeira |
| `codigo_agencia_gestao_financeira` | integer | igual | Código da Agência da Gestão Financeira |
| `dv_agencia_gestao_financeira` | string | contém | DV da Agência da Gestão Financeira |
| `codigo_conta_gestao_financeira` | integer | igual | Código da Conta da Gestão Financeira |
| `dv_conta_gestao_financeira` | string | contém | DV da Conta da Gestão Financeira |
| `descricao_gestao_financeira` | string | contém | Descrição da Gestão Financeira |
| `data_lancamento_gestao_financeira` | date | igual (AAAA-MM-DD) | Data do Lançamento da Gestão Financeira (AAAA-MM-DD) |
| `numero_ordem_gestao_financeira` | integer | igual | Número da Ordem da Gestão Financeira |
| `numero_referencia_unica_gestao_financeira` | string | contém | Número de Referência Única da Gestão Financeira |
| `tipo_operacao_gestao_financeira` | string | contém | Tipo de Operação da Gestão Financeira |
| `valor_gestao_financeira` | number | igual | Valor da Gestão Financeira |
| `doc_depositante_gestao_financeira` | string | contém | Documento do Depositante da Gestão Financeira |
| `nome_depositante_gestao_financeira` | string | contém | Nome do Depositante da Gestão Financeira |
| `tipo_depositante_gestao_financeira` | integer | igual | Tipo do Depositante da Gestão Financeira |
| `codigo_banco_depositante_gestao_financeira` | string | contém | Código do Banco do Depositante da Gestão Financeira |
| `codigo_agencia_depositante_gestao_financeira` | string | contém | Código da Agência do Depositante da Gestão Financeira |
| `dv_agencia_depositante_gestao_financeira` | string | contém | DV da Agência do Depositante da Gestão Financeira |
| `codigo_conta_depositante_gestao_financeira` | string | igual | Código da Conta do depositante da Gestão Financeira |
| `dv_conta_depositante_gestao_financeira` | string | contém | Dígito verificador da conta do depositante. |
| `doc_favorecido_gestao_financeira` | string | contém | Documento do Favorecido da Gestão Financeira |
| `nome_favorecido_gestao_financeira` | string | contém | Nome do Favorecido da Gestão Financeira |
| `tipo_favorecido_gestao_financeira` | integer | igual | Tipo do Favorecido da Gestão Financeira |
| `codigo_banco_favorecido_gestao_financeira` | integer | igual | Código do Banco Favorecido da Gestão Financeira |
| `codigo_agencia_favorecido_gestao_financeira` | integer | — | Codigo Agencia Favorecido Gestao Financeira |
| `dv_agencia_favorecido_gestao_financeira` | string | — | Dv Agencia Favorecido Gestao Financeira |
| `codigo_conta_favorecido_gestao_financeira` | integer | — | Codigo Conta Favorecido Gestao Financeira |
| `dv_conta_favorecido_gestao_financeira` | string | — | Dv Conta Favorecido Gestao Financeira |
| `codigo_categoria_despesa_lancamento_gestao_financeira` | integer | igual | Código da Categoria de Despesa do Lançamento da Gestão Financeira |
| `id_agencia_conta` | string | contém | Identificador da Agência e Conta |
| `quantidade_subtransacoes_lancamento_gestao_financeira` | integer | igual | Quantidade de Subtransações do Lançamento da Gestão Financeira |

### gestao-financeira-subtransacoes-especiais

Retorna uma Lista Paginada dos dados das Subtransações da Gestão Financeira Especiais. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 14.123
- Junções: `id_lancamento_gestao_financeira` → `gestao-financeira-lancamentos-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_subtransacao_gestao_financeira` | string | contém | Identificador da Subtransação da Gestão Financeira |
| `estado_subtransacao_gestao_financeira` | integer | igual | Estado da Subtransação da Gestão Financeira |
| `situacao_pagamento_subtransacao_gestao_financeira` | integer | igual | Situação de Pagamento da Subtransação da Gestão Financeira |
| `data_pagamento_subtransacao_gestao_financeira` | date | igual (AAAA-MM-DD) | Data de Pagamento da Subtransação da Gestão Financeira (AAAA-MM-DD) |
| `valor_subtransacao_gestao_financeira` | number | igual | Valor da Subtransação da Gestão Financeira |
| `codigo_banco_beneficiario_subtransacao_gestao_financeira` | integer | igual | Código do Banco Beneficiário da Subtransação da Gestão Financeira |
| `codigo_agencia_beneficiario_subtransacao_gestao_financeira` | integer | — | Codigo Agencia Beneficiario Subtransacao Gestao Financeira |
| `codigo_conta_beneficiario_subtransacao_gestao_financeira` | integer | — | Codigo Conta Beneficiario Subtransacao Gestao Financeira |
| `tipo_pessoa_beneficiario_subtransacao_gestao_financeira` | integer | igual | Tipo de Pessoa Beneficiária da Subtransação da Gestão Financeira |
| `numero_documento_beneficiario_subtransacao_gestao_financeira` | string | contém | Número do Documento Beneficiário da Subtransação da Gestão Financeira |
| `nome_beneficiario_subtransacao_gestao_financeira` | string | contém | Nome do Beneficiário da Subtransação da Gestão Financeira |
| `codigo_categoria_despesa_subtransacao_gestao_financeira` | integer | igual | Código da Categoria de Despesa da Subtransação da Gestão Financeira |
| `descricao_subtransacao_gestao_financeira` | string | contém | Descrição da Subtransação da Gestão Financeira |
| `id_lancamento_gestao_financeira` | string | contém | Identificador do Lançamento da Gestão Financeira |

### orgaos-analises-pendentes-especiais

Retorna uma Lista Paginada dos dados dos Órgãos de Análises Pendentes Especiais. Grupo: Análises.

- PK: não declarada · linhas em 15/10/2026: 0
- Junções: `id_plano_trabalho` → `planos-trabalho-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_trabalho` | integer | igual | Identificador do Plano de Trabalho |
| `id_orgao_analise_pendente_pt` | integer | igual | Identificador do Órgão de Análise Pendente do Plano de Trabalho |
| `nome_orgao_analise_pendente_pt` | string | contém | Nome do Órgão de Análise Pendente do Plano de Trabalho |
| `ind_orgao_analises_pendentes` | string | contém | Indicador de Órgão de Análises Pendentes |

### planos-trabalho-historico

Retorna uma Lista Paginada dos dados de Planos de Trabalho Histórico. Grupo: Planos de Trabalho.

- PK: não declarada · linhas em 15/10/2026: 461.138
- Junções: `id_plano_trabalho` → `planos-trabalho-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_plano_trabalho_hist` | integer | igual | Identificador único do registro de histórico do plano de trabalho. |
| `data_plano_trabalho_hist` | date-time | igual (AAAA-MM-DD) | Data e hora em que a situação foi registrada no histórico. (AAAA-MM-DD) |
| `cpf_responsavel_plano_trabalho_hist` | string | contém | CPF do responsável pela alteração registrada no histórico. |
| `situacao_plano_trabalho_hist` | string | lista: Aguardando envio para Análise, Aprovado, Em Ajuste do Plano de Trabalho, Em Complementação, Em Elaboração, Enviado para Análise, Legado ADPF 854 STF / NT - TCU, Reprovado | Situação do plano de trabalho no momento do registro histórico. |
| `id_plano_trabalho` | integer | igual | Identificador do Plano de Trabalho ao qual este registro de histórico se refere. |

### saldo-conta-gestao-financeira-especiais

Retorna uma Lista Paginada dos dados dos Saldos de Conta da Gestão Financeira Especiais. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 31.124
- Junções: `id_agencia_conta` ← `planos-acao-especiais`, `gestao-financeira-lancamentos-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_agencia_conta` | string | contém | Identificador da Agência e Conta |
| `agencia_batch` | integer | igual | Número da agência |
| `conta_batch` | integer | igual | Número da conta |
| `data_saldo_conta` | date | igual (AAAA-MM-DD) | Data do saldo da conta (formato: YYYY-MM-DD) |
| `saldo_final_gestao_financeira` | number | igual | Valor do saldo final calculado para a gestão financeira |

### devolucao-especiais

Retorna uma Lista Paginada dos dados das Devoluções de recursos dos Planos de Ação Especiais. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 438
- Junções: `id_plano_acao` → `planos-acao-especiais`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_devolucao` | integer | contém | Identificador único da devolução. |
| `id_plano_acao` | integer | contém | Identificador do plano de ação associado à devolução. |
| `dt_solicitacao_devolucao` | date-time | igual (AAAA-MM-DD) | Data e hora da solicitação da devolução (AAAA-MM-DD). |
| `dt_pagamento_devolucao` | date-time | igual (AAAA-MM-DD) | Data e hora do pagamento da devolução (AAAA-MM-DD). |
| `mes_ano_competencia_devolucao` | string | contém | Mês e ano de competência da devolução (MM/AAAA). |
| `dt_vencimento_devolucao` | date-time | igual (AAAA-MM-DD) | Data e hora de vencimento da devolução (AAAA-MM-DD). |
| `situacao_devolucao` | string | contém | Situação atual da devolução. |
| `tx_metodo_devolucao` | string | contém | Método utilizado para a devolução (ex.: PIX). |
| `tx_cnpj_devolucao` | string | contém | CNPJ do ente devolvedor dos recursos (14 dígitos). |
| `tx_nome_devolucao` | string | contém | Nome do ente devolvedor dos recursos. |
| `tx_cpf_responsavel_mascarado_devolucao` | string | — | Tx Cpf Responsavel Mascarado Devolucao |
| `tx_nome_responsavel_mascarado_devolucao` | string | — | Tx Nome Responsavel Mascarado Devolucao |
| `tipo_devolucao` | string | lista: RENDIMENTOS, RESTITUICAO | Tipo da devolução. |
| `tx_justificativa_devolucao` | string | contém | Justificativa informada para a devolução. |
| `ds_motivo_devolucao` | string | contém | Descrição do motivo da devolução. |
| `vl_devolucao` | number | igual | Valor monetário devolvido. |
| `vl_multa_devolucao` | number | igual | Valor da multa incidida sobre a devolução. |
| `vl_juros_devolucao` | number | igual | Valor dos juros incididos sobre a devolução. |
| `vl_acrescimos_devolucao` | number | igual | Valor dos acréscimos sobre a devolução. |
| `vl_desconto_devolucao` | number | igual | Valor do desconto aplicado à devolução. |
| `vl_deducoes_devolucao` | number | igual | Valor das deduções aplicadas à devolução. |
| `vl_total_devolucao` | number | igual | Valor monetário total da devolução. |

Filtros aceitos pela API que não vêm como coluna na resposta: `tx_cpf_responsavel_devolucao` (contém); `tx_nome_responsavel_devolucao` (contém).
