# Módulo `parcerias` — API de dados abertos do módulo de Gestão de Parcerias do Transferegov

> Gerado por `tools/gerar_references.py` a partir do OpenAPI (versão 1.0). Não edite à mão; regenere quando o schema mudar.

- Endpoint base: `https://api-publica.transferegov.gestao.gov.br/parcerias/<tabela>` · documentação: `https://api-publica.transferegov.gestao.gov.br/parcerias/docs`
- Linhas por página (máximo): 200
- Volumes de **15/10/2026**: mudam a cada carga diária. Use só para ter a ordem de grandeza e confirme com `contar`.

## Índice

| Tabela | Conteúdo | Colunas | Linhas (aprox.) |
|---|---|---|---|
| [`programa`](#programa) | Retorna uma Lista Paginada de Programas. | 51 | 182 |
| [`proposta`](#proposta) | Retorna uma Lista Paginada de Propostas. | 43 | 89.575 |
| [`meta-proposta`](#meta-proposta) | Retorna uma Lista Paginada das Metas vinculadas às Propostas. | 6 | 104.131 |
| [`item-proposta`](#item-proposta) | Retorna uma Lista Paginada dos Itens das Propostas. | 19 | 429.147 |
| [`cronograma-desembolso`](#cronograma-desembolso) | Retorna uma Lista Paginada do Cronograma de Desembolso das Propostas. | 7 | 111.197 |
| [`parceria`](#parceria) | Retorna uma Lista Paginada das Parcerias celebradas a partir de propostas. | 18 | 89.575 |
| [`parceria-conta`](#parceria-conta) | Retorna uma Lista Paginada das informações bancárias/contábeis das parcerias. | 23 | 92.185 |
| [`analise-proposta`](#analise-proposta) | Retorna uma Lista Paginada de Análises de Propostas. | 7 | 86.810 |
| [`proposta-resultado-indicador`](#proposta-resultado-indicador) | Retorna uma Lista Paginada de Resultados e Indicadores de Propostas. | 6 | 16.195 |
| [`distribuicao-recurso-proposta`](#distribuicao-recurso-proposta) | Retorna uma Lista Paginada de Distribuições de Recursos de Propostas. | 9 | 84.396 |
| [`empenho-parceria`](#empenho-parceria) | Retorna uma Lista Paginada de Empenhos de Parcerias. | 24 | 69.345 |
| [`documento-habil`](#documento-habil) | Retorna uma Lista Paginada de Documentos Hábeis. | 15 | 50.575 |
| [`ordem-pagamento`](#ordem-pagamento) | Retorna uma Lista Paginada de Ordens de Pagamento. | 11 | 50.430 |
| [`extrato-bancario`](#extrato-bancario) | Retorna uma Lista Paginada de Extratos Bancários. | 13 | 1.433.757 |
| [`beneficiario_emenda_parlamentar`](#beneficiario_emenda_parlamentar) | Retorna uma Lista Paginada de Beneficiários de Emenda Parlamentar associados aos programas. | 16 | 78.109 |
| [`opp`](#opp) | Retorna uma Lista Paginada de dados de OPP (Ordens de Pagamento e Pagamentos). | 12 | 156 |
| [`indicacao-beneficiario-emenda-parlamentar`](#indicacao-beneficiario-emenda-parlamentar) | Retorna uma Lista Paginada de indicações de beneficiários de emendas parlamentares associadas às propostas. | 5 | 19.597 |

## Chaves de junção prováveis

Uma coluna `id_*` presente em várias tabelas costuma ser a chave da junção. A "dona" é a tabela em que a chave é a 1ª coluna (ou a PK); nas outras, ela funciona como referência. É uma heurística: confira os valores antes de confiar na junção.

| Chave | Tabela dona (provável) | Também aparece em |
|---|---|---|
| `id_beneficiario_emenda_parlamentar` | — | `distribuicao-recurso-proposta`, `indicacao-beneficiario-emenda-parlamentar` |
| `id_conta_gf` | — | `parceria-conta`, `opp` |
| `id_documento_habil` | `documento-habil` | `ordem-pagamento` |
| `id_parceria` | `parceria` | `parceria-conta`, `empenho-parceria`, `documento-habil` |
| `id_parceria_conta` | `parceria-conta` | `extrato-bancario` |
| `id_programa` | `programa` | `proposta`, `beneficiario_emenda_parlamentar` |
| `id_proposta` | `proposta` | `meta-proposta`, `cronograma-desembolso`, `parceria`, `analise-proposta`, `proposta-resultado-indicador`, `distribuicao-recurso-proposta` |

## Tabelas

### programa

Retorna uma Lista Paginada de Programas. Grupo: Programa.

- PK: não declarada · linhas em 15/10/2026: 182
- Junções: `id_programa` ← `proposta`, `beneficiario_emenda_parlamentar`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_programa` | integer | contém | Identificador do programa. |
| `ano_programa` | integer | igual | Ano de referência do programa (1900–2100). |
| `cd_programa` | string | contém | Código identificador do programa. |
| `tp_instrumento` | string | contém | Tipo de instrumento do programa. |
| `cd_tipo_instrumento` | string | lista: MMA MULTA, FAF, FAF SAUDE, RENUNCIA MMA, RENUNCIA SAUDE, FUNDO ESPECIFICO | Código do tipo de instrumento. |
| `sg_ente_superior` | string | contém | Sigla do ente superior. |
| `nm_ente_superior` | string | contém | Nome do ente superior. |
| `sg_nome_ente_superior` | string | contém | Sigla/Nome estendido do ente superior. |
| `sg_ente_repassador` | string | contém | Sigla do ente repassador. |
| `nm_ente_repassador` | string | contém | Nome do ente repassador. |
| `sg_nome_ente_repassador` | string | contém | Sigla/Nome do ente repassador. |
| `nm_programa` | string | contém | Nome do programa. |
| `qualificacao_beneficiario` | string | lista: Beneficiário de Emenda Parlamentar, Beneficiário Espontâneo | Qualificação do beneficiário. |
| `ds_objetivo` | string | contém | Descrição do objetivo do programa. |
| `ds_problema` | string | contém | Descrição do problema/endereço pelo programa. |
| `ds_publico_alvo` | string | contém | Descrição do público-alvo. |
| `ds_resultado_esperado` | string | contém | Descrição dos resultados esperados. |
| `dt_inicio_beneficiario_espontaneo` | date | contém | Data de início para beneficiário espontâneo (YYYY-MM-DD). |
| `dt_fim_beneficiario_espontaneo` | date | contém | Data de fim para beneficiário espontâneo (YYYY-MM-DD). |
| `expiracao_prog_beneficiario_espotaneo` | string | lista: , expiracao_prog_distante, prog_expirado | Regra/expiração para beneficiário espontâneo. |
| `pc_meia_entrada` | string | contém | Percentual de meia-entrada. |
| `situacao_programa` | string | lista: Em Elaboração, Inativo, Disponibilizado | Situação do programa. |
| `sn_tem_meta_padrao` | integer | igual | Indica se o programa possui meta padrão. |
| `sn_permite_meta_proponente` | integer | igual | Indica se o proponente pode definir metas. |
| `sn_tem_visao_produto` | integer | igual | Indica se há visão por produto. |
| `sn_exige_plano_distribuicao` | integer | igual | Indica se exige plano de distribuição. |
| `sn_dispensa_plano_trabalho` | integer | igual | Indica se dispensa plano de trabalho. |
| `dt_inicio_beneficiario_especifico` | date | contém | Data de início para beneficiário específico (YYYY-MM-DD). |
| `dt_fim_beneficiario_especifico` | date | contém | Data de fim para beneficiário específico (YYYY-MM-DD). |
| `expiracao_prog_beneficiario_especifico` | string | contém | Regra/expiração para beneficiário específico. |
| `sn_vinc_indicadores_resultados_esperados` | integer | igual | Indica se há vínculo com indicadores de resultados esperados. |
| `sn_sazonalidade_plano_trabalho` | integer | igual | Indica se há sazonalidade no plano de trabalho. |
| `sn_existe_publico_alvo_padrao` | integer | igual | Indica se existe público-alvo padrão. |
| `sn_utiliza_cauc_na_habilitacao` | integer | igual | Indica se utiliza CAUC na habilitação. |
| `nr_vlr_global` | number | igual | Valor global do programa (não negativo). |
| `sn_permite_anexo_tipo_outros` | integer | igual | Indica se permite anexos do tipo 'outros'. |
| `dt_inicio_beneficiario_emenda` | date | contém | Data de início para beneficiário por emenda (YYYY-MM-DD). |
| `dt_fim_beneficiario_emenda` | date | contém | Data de fim para beneficiário por emenda (YYYY-MM-DD). |
| `expiracao_prog_beneficiario_emenda` | string | contém | Regra/expiração para beneficiário por emenda. |
| `nr_prazo_captacao` | integer | igual | Prazo de captação. |
| `sn_todos_cnaes` | integer | igual | Indica se abrange todos os CNAEs. |
| `in_finalidade` | string | contém | Indicador de finalidade. |
| `vincula_resultados_esperados_indicadores_progama` | string | — | Vincula Resultados Esperados Indicadores Progama |
| `sn_projeto_estruturante_calamidade` | string | — | Sn Projeto Estruturante Calamidade |
| `modalidade_projeto` | string | — | Modalidade Projeto |
| `ds_justificativa_tipo_projeto` | string | — | Ds Justificativa Tipo Projeto |
| `ufs_habilitadas` | json | — | Ufs Habilitadas |
| `programa_atende_a` | json | — | Programa Atende A |
| `categorias_despesa` | json | — | Categorias Despesa |
| `resultados_esperados` | json | — | Resultados Esperados |
| `indicadores_programa` | json | — | Indicadores Programa |

Filtros aceitos pela API que não vêm como coluna na resposta: `uf_habilitada_nm_uf` (contém); `uf_habilitada_sg_uf` (lista (27 valores; veja `colunas`)); `uf_habilitada_cd_ibge` (igual); `atende_a_tp_atende_a` (contém); `categoria_despesa_programa_categoria` (contém); `categoria_despesa_programa_subcategoria` (contém); `resultado_esperado_programa_descricao` (contém); `indicador_programa_nome` (contém); `indicador_programa_unidade_medida` (contém); `indicador_programa_valor` (igual).

### proposta

Retorna uma Lista Paginada de Propostas. Grupo: Proposta.

- PK: não declarada · linhas em 15/10/2026: 89.575
- Junções: `id_proposta` ← `meta-proposta`, `cronograma-desembolso`, `parceria`, `analise-proposta`, `proposta-resultado-indicador`, `distribuicao-recurso-proposta`; `id_programa` → `programa`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_proposta` | integer | contém | Identificador único da proposta. |
| `id_programa` | integer | contém | Identificador do programa ao qual a proposta está vinculada. |
| `cnpj_ente_recebedor` | string | contém | CNPJ do ente federativo ou entidade que receberá os recursos. |
| `nm_ente_recebedor` | string | contém | Nome completo do ente ou entidade recebedora. |
| `ed_cep` | string | contém | CEP do endereço do ente/entidade recebedora. |
| `ed_logradouro` | string | contém | Logradouro do endereço do ente/entidade recebedora. |
| `ed_numero` | string | contém | Número do endereço do ente/entidade recebedora. |
| `ed_complemento` | string | contém | Complemento do endereço do ente/entidade recebedora. |
| `ed_bairro` | string | contém | Bairro do endereço do ente/entidade recebedora. |
| `cd_ibge_recebedor` | integer | igual | Código IBGE do município do ente/entidade recebedora. |
| `nm_municipio_recebedor` | string | contém | Nome do município do ente/entidade recebedora. |
| `nm_uf_recebedor` | string | contém | Nome da unidade federativa do ente/entidade recebedora. |
| `sg_uf_recebedor` | string | lista (27 valores; veja `colunas`) | Sigla da unidade federativa do ente/entidade recebedora. |
| `nm_pais` | string | contém | Nome do país do ente/entidade recebedora. |
| `nm_natureza_juridica` | string | contém | Descrição da natureza jurídica do ente/entidade recebedora. |
| `cnpj_executor` | string | contém | CNPJ da entidade executora (quando houver). |
| `nm_executor` | string | contém | Nome da entidade executora. |
| `cnpj_terceiro_signatario` | string | contém | CNPJ de terceiro signatário (quando houver). |
| `nm_terceiro_signatario` | string | contém | Nome do terceiro signatário. |
| `id_programa_unidade_gestora` | integer | contém | Identificador da unidade gestora do programa. |
| `nm_unidade_gestora` | string | contém | Nome da unidade gestora do programa. |
| `ds_objeto` | string | contém | Descrição do objeto/escopo da proposta. |
| `ds_problema_proposta` | string | contém | Descrição do problema que a proposta busca resolver. |
| `ds_relacao_proposta_objetivo_diretrizes` | string | contém | Descrição da relação da proposta com os objetivos e diretrizes do programa. |
| `ds_caracterizacao_interesses_reciprocos` | string | contém | Descrição da caracterização dos interesses recíprocos para a execução da proposta. |
| `situacao_proposta` | string | lista: Em Análise, Rejeitada, Aprovada, Em Elaboração, Inativada | Situação atual da proposta (ex: Em análise, Aprovada, Rejeitada). |
| `in_situacao_analise` | string | lista: Proposta e Plano de Trabalho Em Complementação, Proposta e Plano de Trabalho em Análise, Proposta e Plano de Trabalho Enviados para Análise, Proposta e Plano de Trabalho Enviado para Complementação | Indicador da situação em análise da proposta. |
| `ds_resultado_esperado_proposta` | string | contém | Descrição do resultado esperado com a execução da proposta. |
| `in_formato_etapas` | string | lista: datas específicas, meses, dias | Indicador se a proposta está no formato de etapas. |
| `nr_vlr_total` | string | igual | Valor total da proposta. |
| `dt_envio_analise` | date-time | contém | Data de envio da proposta para análise (YYYY-MM-DD). |
| `in_situacao_antes_inativar` | integer | igual | Situação da proposta antes de ser inativada. |
| `in_situacao_analise_antes_inativar` | integer | contém | Situação de análise antes de inativar a proposta. |
| `in_tipo_prazo_captacao` | string | lista: Data Fixa, Prazo Máximo Previsto | Indicador do tipo de prazo para captação de recursos. |
| `dt_limite_captacao` | date | contém | Data limite para captação de recursos (YYYY-MM-DD). |
| `in_formato_etapas_antes_recalculo` | integer | contém | Formato de etapas antes do recálculo. |
| `vl_total_planejamento_gastos` | number | igual | Valor total do planejamento de gastos. |
| `ds_publico_alvo_proposta` | string | contém | Descrição do público-alvo da proposta. |
| `mes_proposta` | integer | igual | Mês de cadastro da proposta. |
| `ano_proposta` | integer | igual | Ano de cadastro da proposta. |
| `dt_proposta` | date | contém | Data de cadastro da proposta (YYYY-MM-DD). |
| `intervenientes_proposta` | json | — | Intervenientes Proposta |
| `categorias_despesa_proposta` | json | — | Categorias Despesa Proposta |

Filtros aceitos pela API que não vêm como coluna na resposta: `interveniente_cnpj_interveniente` (contém); `interveniente_nm_interveniente` (contém); `categoria_despesa_proposta_categoria_despesa` (contém); `categoria_despesa_proposta_subcategoria_despesa` (contém).

### meta-proposta

Retorna uma Lista Paginada das Metas vinculadas às Propostas. Grupo: Proposta.

- PK: não declarada · linhas em 15/10/2026: 104.131
- Junções: `id_proposta` → `proposta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_meta_proposta` | integer | contém | Identificador único da meta da proposta. |
| `id_proposta` | integer | contém | Identificador da proposta a qual esta meta pertence |
| `cd_meta` | integer | igual | Código da meta dentro do programa. |
| `nm_meta` | string | contém | Nome/título da meta. |
| `ds_meta` | string | contém | Descrição detalhada da meta. |
| `etapas_proposta` | json | — | Etapas Proposta |

Filtros aceitos pela API que não vêm como coluna na resposta: `etapa_id_etapa_proposta` (contém); `etapa_cd_etapa` (contém); `etapa_nm_etapa` (contém); `etapa_ds_etapa` (contém); `etapa_dt_inicio` (contém); `etapa_dt_fim` (contém); `etapa_nr_inicio` (igual); `etapa_nr_fim` (igual).

### item-proposta

Retorna uma Lista Paginada dos Itens das Propostas. Grupo: Proposta.

- PK: não declarada · linhas em 15/10/2026: 429.147

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_item_proposta` | integer | contém | Identificador único do item da proposta. |
| `id_classificacao_despesa` | integer | contém | Identificador da classificação da despesa. |
| `id_etapa_proposta` | integer | contém | Identificador da etapa da proposta à qual o item pertence. |
| `nm_item` | string | contém | Nome/título do item de despesa. |
| `ds_item` | string | contém | Descrição detalhada do item. |
| `nm_unidade_medida` | string | contém | Nome da unidade de medida do item. |
| `vl_unitario_item` | number | igual | Valor unitário do item. |
| `qt_quantidade` | integer | igual | Quantidade do item. |
| `nr_ocorrencia` | integer | igual | Número de ocorrências do item. |
| `vl_total_item` | number | igual | Valor total do item. |
| `cd_classificacao_despesa` | integer | igual | Código da classificação da despesa. |
| `in_categoria_despesa` | string | lista: Custeio, Investimento | Indicador da categoria da despesa. |
| `nm_classificacao_despesa` | string | contém | Nome da classificação da despesa. |
| `classificacao_despesa__id_classificacao_despesa_pai` | integer | — | Id Classificacao Despesa Pai |
| `classificacao_despesa__nm_classificacao_despesa_1` | string | — | Nm Classificacao Despesa 1 |
| `classificacao_despesa__nm_classificacao_despesa_2` | string | — | Nm Classificacao Despesa 2 |
| `classificacao_despesa__nm_classificacao_despesa_path` | string | — | Nm Classificacao Despesa Path |
| `classificacao_despesa__nm_classificacao_despesa` | string | — | Nm Classificacao Despesa |
| `classificacao_despesa__nm_classificacao_despesa_profundidade` | integer | — | Nm Classificacao Despesa Profundidade |

### cronograma-desembolso

Retorna uma Lista Paginada do Cronograma de Desembolso das Propostas. Grupo: Proposta.

- PK: não declarada · linhas em 15/10/2026: 111.197
- Junções: `id_proposta` → `proposta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_proposta_cronograma_item` | integer | contém | Identificador único do item de cronograma de desembolso. |
| `id_proposta` | integer | contém | Identificador da proposta ao qual o cronograma pertence. |
| `nr_ref_mes_data_especif` | integer | igual | Mês de referência para o desembolso (1–12). |
| `nr_ref_ano_data_especif` | integer | igual | Ano de referência para o desembolso. |
| `nr_ref_mes_sazonalidade` | integer | igual | Mês de referência para fins de sazonalidade. |
| `vl_cronograma_desembolso` | number | igual | Valor previsto para o desembolso na data/mês indicado. |
| `origem_recurso` | string | lista: Repasse, Terceiros - Nacional | Origem dos recursos. |

### parceria

Retorna uma Lista Paginada das Parcerias celebradas a partir de propostas. Grupo: Parceria.

- PK: não declarada · linhas em 15/10/2026: 89.575
- Junções: `id_parceria` ← `parceria-conta`, `empenho-parceria`, `documento-habil`; `id_proposta` → `proposta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_parceria` | integer | contém | Identificador único da parceria. |
| `cd_parceria` | integer | igual | Código sequencial da parceria. |
| `nu_externo` | string | — | Nu Externo |
| `id_proposta` | integer | contém | Identificador da proposta a qual a parceria pertence. |
| `in_situacao_parceria` | string | lista: Aprovada, Em Análise, Em Captação, Em Elaboração, Inativa, Rejeitada | Situação atual da parceria. |
| `tp_origem` | string | lista: Atos Preparatórios, Sistema Externo | Tipo de origem da parceria. |
| `cd_processo_sei` | string | contém | Número do processo no SEI. |
| `sn_assinatura_manual` | string | contém | Indicador se a assinatura foi manual. |
| `dh_assinatura` | date-time | contém | Data/hora da assinatura da parceria (YYYY-MM-DD). |
| `tx_justificativa` | string | contém | Texto de justificativa associada. |
| `in_situacao_autorizacao_execucao` | string | contém | Situação da autorização de execução. |
| `dh_solicitacao_execucao` | date-time | contém | Data/hora da solicitação de execução (YYYY-MM-DD). |
| `ds_justificativa_solicitacao` | string | contém | Descrição da justificativa da solicitação. |
| `dh_autorizacao_execucao` | date-time | contém | Data/hora da autorização de execução (YYYY-MM-DD). |
| `ds_justificativa_autorizacao` | string | contém | Descrição da justificativa da autorização. |
| `prazo_limite_captacao_recursos` | string | contém | Prazo limite para captação de recursos (intervalo no formato DD/MM/AAAA à DD/MM/AAAA). |
| `prazo_captacao_em_dias` | integer | igual | Prazo para captação de recursos, em dias. |
| `publicacoes_parceria` | json | — | Publicacoes Parceria |

Filtros aceitos pela API que não vêm como coluna na resposta: `publicacao_dt_publicacao` (contém); `publicacao_ds_numero_dou` (contém); `publicacao_nr_pagina_dou` (igual); `publicacao_ds_documento_publicado` (contém); `publicacao_ds_url_documento_publicado` (contém); `publicacao_dt_inicio_captacao` (contém); `publicacao_dt_fim_captacao` (contém); `publicacao_tp_prazo_captacao` (igual).

### parceria-conta

Retorna uma Lista Paginada das informações bancárias/contábeis das parcerias. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 92.185
- Junções: `id_parceria_conta` ← `extrato-bancario`; `id_parceria` → `parceria`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_parceria_conta` | integer | contém | Identificador único da conta da parceria. |
| `id_parceria` | integer | contém | Identificador da parceria à qual a conta está vinculada. |
| `id_conta_gf` | integer | — | Id Conta Gf |
| `tx_conta` | string | contém | Número ou código da conta. |
| `tp_conta` | string | lista: , Conta Captação, Conta Movimentação | Tipo da conta. |
| `nm_conta` | string | contém | Nome ou título da conta. |
| `dt_abertura` | date | contém | Data de abertura da conta (YYYY-MM-DD). |
| `tx_descricao` | string | contém | Breve descrição da conta. |
| `tx_detalhamento` | string | contém | Detalhamento adicional sobre a conta. |
| `nm_banco` | string | contém | Nome do banco ou instituição financeira. |
| `tx_numero` | string | contém | Número da conta. |
| `nm_agencia` | string | contém | Nome da agência bancária. |
| `nm_municipio_agencia` | string | contém | Município onde está localizada a agência. |
| `sg_uf_agencia` | string | lista (27 valores; veja `colunas`) | Sigla da UF da agência. |
| `ds_justificativa` | string | contém | Justificativa para o uso desta conta. |
| `id_historico_gf` | integer | contém | Identificador de histórico no sistema GF. |
| `cd_programa_bb_agil` | integer | igual | Código do programa BB Ágil. |
| `nm_personalizado_conta_bb_agil` | string | contém | Nome personalizado da conta no BB Ágil. |
| `vl_saldo_conta_corrente` | number | — | Vl Saldo Conta Corrente |
| `dt_referencia_saldo_conta_corrente` | date | — | Dt Referencia Saldo Conta Corrente |
| `vl_saldo_conta_investimento` | number | — | Vl Saldo Conta Investimento |
| `dt_referencia_saldo_conta_investimento` | date | — | Dt Referencia Saldo Conta Investimento |
| `classificacoes_ingresso` | json | — | Classificacoes Ingresso |

Filtros aceitos pela API que não vêm como coluna na resposta: `vl_saldo` (igual); `dt_referencia_saldo` (contém); `classificacao_identificacao_depositante` (contém); `classificacao_nome_depositante` (contém); `classificacao_nu_identificacao_depositante` (contém); `classificacao_tx_nome_depositante` (contém); `classificacao_dt_movimento_lancamento` (contém); `classificacao_tx_descricao_classificacao_ingresso` (contém); `classificacao_id_classificacao_ingresso_tipo` (igual); `classificacao_tx_descricao_classificao_ingresso_tipo` (contém); `classificacao_tx_desc_classificacao_analise_situacao` (contém).

### analise-proposta

Retorna uma Lista Paginada de Análises de Propostas. Grupo: Proposta.

- PK: não declarada · linhas em 15/10/2026: 86.810
- Junções: `id_proposta` → `proposta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_analise_proposta` | integer | contém | Identificador único da análise. |
| `id_proposta` | integer | contém | Identificador da proposta analisada. |
| `in_fase_analise` | string | contém | Fase da análise. |
| `in_resultado_analise` | string | contém | Resultado da análise. |
| `ds_parecer` | string | — | Ds Parecer |
| `dh_analise_proposta` | date-time | — | Dh Analise Proposta |
| `tipos_analise` | json | — | Tipos Analise |

Filtros aceitos pela API que não vêm como coluna na resposta: `tipo_analise_tp_analise` (contém).

### proposta-resultado-indicador

Retorna uma Lista Paginada de Resultados e Indicadores de Propostas. Grupo: Proposta.

- PK: não declarada · linhas em 15/10/2026: 16.195
- Junções: `id_proposta` → `proposta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_proposta_resultado_indicador` | integer | contém | Identificador único do resultado/indicador. |
| `id_proposta` | integer | contém | Identificador da proposta. |
| `ds_resultado_esperado_proposta_resultado_indicador` | string | contém | Descrição do resultado esperado. |
| `nm_indicador_proposta` | string | contém | Nome do indicador da proposta. |
| `vl_indicador_proposta` | number | igual | Valor do indicador da proposta. |
| `nm_unidade_medida_indicador_proposta` | string | contém | Nome da unidade de medida do indicador. |

### distribuicao-recurso-proposta

Retorna uma Lista Paginada de Distribuições de Recursos de Propostas. Grupo: Parceria.

- PK: não declarada · linhas em 15/10/2026: 84.396
- Junções: `id_proposta` → `proposta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_distribuicao_recurso_proposta` | integer | contém | Identificador único da distribuição. |
| `id_proposta` | integer | contém | Identificador da proposta. |
| `id_beneficiario_emenda_parlamentar` | integer | contém | Identificador do beneficiário da emenda parlamentar. |
| `in_tipo_distribuicao` | string | contém | Tipo de distribuição. |
| `in_tipo_gnd` | string | contém | Tipo de GND. |
| `nr_emenda_proposta` | string | contém | Número da emenda da proposta. |
| `nm_parlamentar_proposta` | string | contém | Nome do parlamentar. |
| `in_tipo_emenda_parlamentar_proposta` | string | contém | Tipo de emenda parlamentar. |
| `valor_emenda` | number | igual | Valor da emenda (não negativo). |

### empenho-parceria

Retorna uma Lista Paginada de Empenhos de Parcerias. Grupo: Dados Orçamentários.

- PK: não declarada · linhas em 15/10/2026: 69.345
- Junções: `id_parceria` → `parceria`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_empenho_parceria` | integer | contém | Identificador único do empenho. |
| `id_parceria` | integer | contém | Identificador da parceria. |
| `nr_empenho` | integer | igual | Número do empenho. |
| `cd_ug_emitente` | integer | igual | Código da unidade gestora emitente. |
| `aa_empenho` | integer | igual | Ano de referência do empenho. |
| `in_situacao_siafi` | string | contém | Situação do empenho no SIAFI. |
| `id_minuta` | string | contém | Identificador da minuta. |
| `data_emissao` | date-time | contém | Data de emissão do empenho (YYYY-MM-DD). |
| `id_tipo_empenho` | integer | igual | Identificador do tipo de empenho. |
| `nome_tipo_empenho` | string | contém | Nome do tipo de empenho. |
| `ug_emitente` | string | contém | Unidade gestora emitente. |
| `nome_favorecido` | string | contém | Nome do favorecido. |
| `identificacao_favorecido` | string | contém | CNPJ/CPF do favorecido. |
| `ug_responsavel` | string | contém | UG responsável. |
| `autor_emenda` | string | contém | Autor da emenda. |
| `descricao_empenho` | string | contém | Descrição do empenho. |
| `numero_empenho` | integer | igual | Número do empenho. |
| `numero_nota_empenho_gerada` | string | contém | Número da nota de empenho gerada. |
| `numro` | string | contém | Número do documento. |
| `nome_situacao_minuta` | string | contém | Nome da situação da minuta. |
| `id_pre_empenho` | string | contém | Identificador do pré-empenho. |
| `valor_empenho` | number | igual | Valor do empenho (não negativo). |
| `nr_pre_empenho` | string | contém | Número do pré-empenho. |
| `valor_operacao_empenho` | number | igual | Valor da operação do empenho (não negativo). |

### documento-habil

Retorna uma Lista Paginada de Documentos Hábeis. Grupo: Dados Orçamentários.

- PK: não declarada · linhas em 15/10/2026: 50.575
- Junções: `id_documento_habil` ← `ordem-pagamento`; `id_parceria` → `parceria`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_documento_habil` | integer | contém | Identificador único do documento hábil. |
| `id_parceria` | integer | contém | Identificador da parceria. |
| `nr_minuta_dh` | string | contém | Número da minuta do documento hábil. |
| `nr_documento_habil` | string | contém | Número do documento hábil. |
| `cd_ug_emitente_dh` | integer | igual | Código da unidade gestora emitente. |
| `tp_documento_habil` | string | contém | Tipo do documento hábil. |
| `vl_documento_habil` | number | igual | Valor do documento hábil (não negativo). |
| `dt_emissao` | date-time | contém | Data de emissão (YYYY-MM-DD). |
| `ano_emissao` | integer | igual | Ano de emissão. |
| `mes_emissao` | integer | igual | Mês de emissão. |
| `in_situacao_dh` | string | contém | Situação do documento hábil. |
| `cd_credor_devedor` | string | contém | CNPJ/CPF do credor/devedor. |
| `nm_credor_devedor` | string | contém | Nome do credor/devedor. |
| `tx_observacao` | string | contém | Observação. |
| `nr_empenho_dh` | string | contém | Número do empenho associado. |

### ordem-pagamento

Retorna uma Lista Paginada de Ordens de Pagamento. Grupo: Dados Orçamentários.

- PK: não declarada · linhas em 15/10/2026: 50.430
- Junções: `id_documento_habil` → `documento-habil`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_op` | integer | contém | Identificador único da ordem de pagamento. |
| `id_documento_habil` | integer | contém | Identificador do documento hábil. |
| `cd_ug_emitente_op` | integer | igual | Código da unidade gestora emitente. |
| `nr_minuta_op` | string | contém | Número da minuta da ordem de pagamento. |
| `nr_ordem_pagamento` | string | contém | Número da ordem de pagamento. |
| `in_situacao_op` | string | contém | Situação da ordem de pagamento. |
| `dt_emissao_op` | date-time | contém | Data de emissão da OP (YYYY-MM-DD). |
| `vl_ordem_pagamento` | number | igual | Valor da ordem de pagamento (não negativo). |
| `nr_ordem_bancaria` | string | contém | Número da ordem bancária. |
| `dt_emissao_ordem_bancaria` | date-time | contém | Data de emissão da ordem bancária (YYYY-MM-DD). |
| `tx_observacao_op` | string | contém | Observação da ordem de pagamento. |

### extrato-bancario

Retorna uma Lista Paginada de Extratos Bancários. Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 1.433.757
- Junções: `id_parceria_conta` → `parceria-conta`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_extrato_bancario` | integer | contém | Identificador único do extrato bancário. |
| `id_parceria_conta` | integer | contém | Identificador da conta da parceria. |
| `nu_identificador_lancamento_extrato_bancario` | integer | igual | Número identificador do lançamento. |
| `nr_interno_referencia` | integer | igual | Número interno de referência. |
| `in_transacao` | string | contém | Tipo de transação (ex: Crédito, Débito). |
| `cd_tipo_operacao` | integer | igual | Código do tipo de operação. |
| `nm_tipo_operacao` | string | contém | Nome do tipo de operação. |
| `nu_identificacao_depositante_extrato_bancario` | string | contém | CNPJ/CPF do depositante. |
| `tx_nome_depositante_extrato_bancario` | string | contém | Nome do depositante. |
| `nu_identificacao_beneficiario` | string | contém | CNPJ/CPF do beneficiário. |
| `tx_nome_beneficiario` | string | contém | Nome do beneficiário. |
| `dt_movimento_lancamento_extrato_bancario` | date-time | contém | Data do movimento do lançamento (YYYY-MM-DD). |
| `vl_lancamento_extrato_bancario` | number | igual | Valor do lançamento (não negativo). |

### beneficiario_emenda_parlamentar

Retorna uma Lista Paginada de Beneficiários de Emenda Parlamentar associados aos programas. Grupo: Programa.

- PK: não declarada · linhas em 15/10/2026: 78.109
- Junções: `id_programa` → `programa`

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_beneficiario_emenda_parlamentar_programa` | integer | contém | Identificador do beneficiário de emenda parlamentar. |
| `id_programa` | integer | contém | Identificador do programa. |
| `nr_cnpj_beneficiario_emenda` | string | contém | CNPJ do beneficiário da emenda. |
| `nm_beneficiario_emenda` | string | contém | Nome do beneficiário da emenda. |
| `nm_municipio_beneficiario_emenda` | string | contém | Município do beneficiário. |
| `sg_uf_beneficiario_emenda` | string | lista (27 valores; veja `colunas`) | UF do beneficiário. |
| `nm_natureza_juridica_beneficiario_emenda` | string | — | Nm Natureza Juridica Beneficiario Emenda |
| `aa_emenda` | integer | igual | Ano da emenda. |
| `cd_parlamentar` | integer | igual | Código do parlamentar. |
| `nr_emenda` | string | contém | Número da emenda. |
| `nm_parlamentar` | string | contém | Nome do parlamentar. |
| `in_tipo_emenda_parlamentar` | string | contém | Tipo de emenda parlamentar. |
| `vl_gnd3` | number | — | Vl Gnd3 |
| `vl_gnd4` | number | — | Vl Gnd4 |
| `vl_total_emenda` | number | — | Vl Total Emenda |
| `indicacoes_beneficiario` | json | — | Indicacoes Beneficiario |

Filtros aceitos pela API que não vêm como coluna na resposta: `indicacao_id_solicitante` (igual); `indicacao_nm_solicitante` (contém); `indicacao_tp_solicitante` (contém).

### opp

Retorna uma Lista Paginada de dados de OPP (Ordens de Pagamento e Pagamentos). Grupo: Gestão Financeira.

- PK: não declarada · linhas em 15/10/2026: 156

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_opp` | integer | contém | Identificador único da OPP. |
| `id_conta_gf` | integer | contém | Identificador da conta GF. |
| `cd_opp` | integer | igual | Código da OPP. |
| `dh_inclusao_opp` | date-time | contém | Data e hora de inclusão da OPP (YYYY-MM-DD). |
| `nr_cpf_cnpj_beneficiario_mascarado` | string | — | Nr Cpf Cnpj Beneficiario Mascarado |
| `nm_beneficiario` | string | contém | Nome do beneficiário. |
| `vl_opp` | number | igual | Valor da OPP. |
| `vl_efetivado` | number | igual | Valor efetivado da OPP. |
| `tx_descricao_operacao` | string | contém | Descrição da operação. |
| `nm_tipo_opp` | string | contém | Tipo da OPP. |
| `nm_situacao` | string | lista: Cancelada, Efetivada, Excluída, Rejeitada OD, Rejeitada OD Banco | Situação da OPP. |
| `dh_efetivacao` | date-time | contém | Data e hora de efetivação da OPP (YYYY-MM-DD). |

Filtros aceitos pela API que não vêm como coluna na resposta: `nr_cpf_cnpj_beneficiario` (contém).

### indicacao-beneficiario-emenda-parlamentar

Retorna uma Lista Paginada de indicações de beneficiários de emendas parlamentares associadas às propostas. Grupo: Parceria.

- PK: não declarada · linhas em 15/10/2026: 19.597

| Coluna | Tipo | Filtro na API | Descrição |
|---|---|---|---|
| `id_indicacao_beneficiario_emenda_parlamentar` | integer | contém | Identificador único da indicação do beneficiário da emenda parlamentar. |
| `id_beneficiario_emenda_parlamentar` | integer | contém | Identificador do beneficiário da emenda parlamentar. |
| `id_apoiador_mascarado` | integer | — | Id Apoiador Mascarado |
| `nm_apoiador` | string | contém | Nome do apoiador. |
| `tp_apoiador` | string | lista: Comissão, Parlamentar | Tipo do apoiador. |

Filtros aceitos pela API que não vêm como coluna na resposta: `id_apoiador` (contém).
