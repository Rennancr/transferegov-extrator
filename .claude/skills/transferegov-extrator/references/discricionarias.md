# Módulo `discricionarias` — Transferências Discricionárias e Legais (convênios, contratos de repasse)

> Gerado por `tools/gerar_references.py` a partir do modelo de dados oficial (SchemaSpy) e da listagem de `/downloads`. Não edite à mão.

- **Não há API.** Os dados saem em CSVs (zip) em `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/`, atualizados diariamente. O script baixa o zip **inteiro** para um cache local e aplica os filtros localmente; o tempo depende do tamanho do arquivo.
- Apelidos aceitos em `--modulo`: `discricionarias`, `convenios`, `siconv`, `downloads`. `--tabela` é o nome do arquivo sem `siconv_` e sem `.zip` (ex.: `convenio`, `proposta`, `emenda`).
- **Texto** compara por *contém*, ignorando acento e maiúsculas; **códigos** (`ID_`, `COD_`, `NR_`, `CNPJ`, `UF_`...) comparam por igualdade exata; **datas e valores** aceitam faixa.
- Tamanhos da listagem de Thu, 15 Oct 2026 11:09:53 GMT; confira o atual com `tabelas --modulo discricionarias`. Acima de ~200 MB, avise o usuário antes: o download e a leitura levam minutos.

## Por onde começar

| Pedido | Arquivos | Junção |
|---|---|---|
| Convênios/contratos de repasse (situação, vigência, valores) | `convenio` | — |
| ...de um órgão (ministério), UF ou município | `convenio` + `proposta` | `ID_PROPOSTA` (órgão: `COD_ORGAO_SUP`/`DESC_ORGAO_SUP`; local: `UF_PROPONENTE`, `COD_MUNIC_IBGE`) |
| Emendas parlamentares em convênios | `emenda` + `convenio`/`proposta` | `ID_PROPOSTA` |
| Empenhos, desembolsos, pagamentos | `empenho`, `desembolso`, `pagamento` | `NR_CONVENIO` |
| Programas | `programa` + `programa_proposta` | `ID_PROGRAMA`, `ID_PROPOSTA` |

## Índice

| Arquivo (`--tabela`) | Tamanho do zip | Colunas | PK |
|---|---|---|---|
| [`acomp_obras_contratos_medicoes_modulo_empresas`](#acomp_obras_contratos_medicoes_modulo_empresas) | 0,8 MB | 10 | `ID_MEDICAO_ACOMPANHAMENTO_OBRA` |
| [`acomp_obras_valores_itens_medicao_modulo_empresas`](#acomp_obras_valores_itens_medicao_modulo_empresas) | 0,4 MB | 6 | `ID_SUBMETA_VRPL` |
| [`apoiadores_emendas_programas`](#apoiadores_emendas_programas) | 6,8 MB | 13 | `ID_CNPJ_PROGRAMA_EMENDA_APOIADORES_EMENDAS` |
| `app_parceriasgov_necessidades` (sem modelo; use `colunas`) | 0,3 MB | — | — |
| `app_parceriasgov_necessidades_aprovadas` (sem modelo; use `colunas`) | 0,1 MB | — | — |
| [`consorcios`](#consorcios) | 1,3 MB | 9 | — |
| [`contrato`](#contrato) | 74,7 MB | 12 | `ID_CONTRATO` |
| `contrato_cipi` (sem modelo; use `colunas`) | 4,2 MB | — | — |
| [`convenio`](#convenio) | 18,4 MB | 40 | `NR_CONVENIO` |
| [`coordenadas_obra`](#coordenadas_obra) | 3,0 MB | 4 | — |
| [`cronograma_desembolso`](#cronograma_desembolso) | 19,6 MB | 7 | — |
| `dados_obrasgov_geral` (sem modelo; use `colunas`) | 0,8 MB | — | — |
| [`desbloqueio_cr`](#desbloqueio_cr) | 12,6 MB | 8 | — |
| `desbloqueio_recurso_cr` (sem modelo; use `colunas`) | 0,9 MB | — | — |
| [`desembolso`](#desembolso) | 16,8 MB | 11 | `ID_DESEMBOLSO` |
| `dl` (sem modelo; use `colunas`) | 214,7 MB | — | — |
| [`emenda`](#emenda) | 8,3 MB | 10 | — |
| [`empenho`](#empenho) | 23,5 MB | 18 | `ID_EMPENHO` |
| `empenho_cipi` (sem modelo; use `colunas`) | 1,6 MB | — | — |
| [`empenho_desembolso`](#empenho_desembolso) | 2,8 MB | 3 | — |
| [`etapa_crono_fisico`](#etapa_crono_fisico) | 198,8 MB | 13 | — |
| `execucao_fisica_cipi` (sem modelo; use `colunas`) | 0,4 MB | — | — |
| [`historico_projeto_basico`](#historico_projeto_basico) | 4,9 MB | 5 | — |
| [`historico_situacao`](#historico_situacao) | 103,9 MB | 6 | — |
| [`ingresso_contrapartida`](#ingresso_contrapartida) | 3,6 MB | 3 | — |
| [`inst_cont_contratos_lotes_empresas_modulo_empresas`](#inst_cont_contratos_lotes_empresas_modulo_empresas) | 1,3 MB | 12 | `ID_CONTRATO_INSTRUMENTO_CONTRATUAL` |
| [`inst_cont_metas_submetas_po_modulo_empresas`](#inst_cont_metas_submetas_po_modulo_empresas) | 2,2 MB | 15 | `ID_SUBMETA_INSTRUMENTO_CONTRATUAL` |
| [`inst_cont_proposta_aio_modulo_empresas`](#inst_cont_proposta_aio_modulo_empresas) | 0,3 MB | 5 | `ID_PROPOSTA_INSTRUMENTO_CONTRATUAL` |
| [`itens_dl`](#itens_dl) | 542,1 MB | 6 | `ID_ITEM_DL` |
| [`itens_licitacao`](#itens_licitacao) | 233,9 MB | 10 | `ID_ITEM_LICITACAO` |
| [`justificativas_proposta`](#justificativas_proposta) | 751,0 MB | 8 | — |
| [`licitacao`](#licitacao) | 27,0 MB | 18 | `ID_LICITACAO` |
| [`meta_crono_fisico`](#meta_crono_fisico) | 112,0 MB | 17 | `ID_META` |
| [`obtv_convenente`](#obtv_convenente) | 58,4 MB | 5 | — |
| [`pagamento`](#pagamento) | 372,3 MB | 11 | `NR_MOV_FIN` |
| [`pagamento_tributo`](#pagamento_tributo) | 4,8 MB | 3 | — |
| [`pergunta_selecao_pac`](#pergunta_selecao_pac) | 0,1 MB | 3 | `ID_PERGUNTA_SELECAO_PAC` |
| [`plano_aplicacao_detalhado`](#plano_aplicacao_detalhado) | 292,2 MB | 15 | — |
| [`programa`](#programa) | 11,1 MB | 20 | `ID_PROGRAMA` |
| [`programa_proponentes`](#programa_proponentes) | 2,5 MB | 2 | — |
| [`programa_proposta`](#programa_proposta) | 6,5 MB | 2 | — |
| [`projeto_basico_acffo_modulo_empresas`](#projeto_basico_acffo_modulo_empresas) | 2,1 MB | 7 | `ID_ACFFO` |
| [`projeto_basico_lae_modulo_empresas`](#projeto_basico_lae_modulo_empresas) | 3,3 MB | 6 | `ID_QCI_ACFFO` |
| [`projeto_basico_metas_modulo_empresas`](#projeto_basico_metas_modulo_empresas) | 7,3 MB | 8 | `ID_META_PROJETO_BASICO` |
| [`projeto_basico_proposta_modulo_empresas`](#projeto_basico_proposta_modulo_empresas) | 1,1 MB | 3 | `ID_PROPOSTA_ACFFO` |
| [`projeto_basico_submetas_modulo_empresas`](#projeto_basico_submetas_modulo_empresas) | 16,4 MB | 15 | `ID_SUBMETA_PROJETO_BASICO` |
| `prop_inst_indicadores_estados` (sem modelo; use `colunas`) | 1,0 MB | — | — |
| `prop_inst_indicadores_municipios` (sem modelo; use `colunas`) | 10,6 MB | — | — |
| [`proponentes`](#proponentes) | 6,4 MB | 11 | `ID_PROPONENTE` |
| [`proposta`](#proposta) | 205,9 MB | 36 | `ID_PROPOSTA` |
| [`proposta_cancelada`](#proposta_cancelada) | 10,6 MB | 34 | — |
| [`proposta_formalizacao_pac`](#proposta_formalizacao_pac) | 0,1 MB | 3 | — |
| [`proposta_selecao_pac`](#proposta_selecao_pac) | 39,9 MB | 11 | `ID_PROPOSTA_SELECAO_PAC` |
| [`prorroga_oficio`](#prorroga_oficio) | 2,0 MB | 7 | — |
| [`resposta_selecao_pac`](#resposta_selecao_pac) | 18,8 MB | 3 | — |
| [`resumo_fisico_financeiro`](#resumo_fisico_financeiro) | 0,4 MB | 4 | — |
| `solicitacao_ajuste_pt` (sem modelo; use `colunas`) | 1,9 MB | — | — |
| [`solicitacao_alteracao`](#solicitacao_alteracao) | 13,9 MB | 6 | `ID_SOLICITACAO` |
| [`solicitacao_rendimento_aplicacao`](#solicitacao_rendimento_aplicacao) | 0,3 MB | 7 | `ID_SOLICITACAO_REND_APLICACAO` |
| [`termo_aditivo`](#termo_aditivo) | 61,0 MB | 11 | — |
| [`vrpl_lotes_fornecedores_licitacao_modulo_empresas`](#vrpl_lotes_fornecedores_licitacao_modulo_empresas) | 2,1 MB | 6 | `ID_LICITACAO_VRPL` |
| [`vrpl_metas_submetas_modulo_empresas`](#vrpl_metas_submetas_modulo_empresas) | 8,4 MB | 18 | `ID_SUBMETA_VRPL` |
| [`vrpl_proposta_licitacao_modulo_empresas`](#vrpl_proposta_licitacao_modulo_empresas) | 1,2 MB | 9 | `ID_PROPOSTA_VRPL` |

## Chaves de junção (chaves estrangeiras do modelo oficial)

| Chave | Tabela dona | Referenciada por |
|---|---|---|
| `NR_CONVENIO` | `convenio` | `cronograma_desembolso`, `desbloqueio_cr`, `desembolso`, `empenho`, `historico_situacao`, `ingresso_contrapartida`, `licitacao`, `meta_crono_fisico`, `pagamento`, `pagamento_tributo`, `prorroga_oficio`, `solicitacao_alteracao`, `solicitacao_rendimento_aplicacao`, `termo_aditivo` |
| `ID_DESEMBOLSO` | `desembolso` | `empenho_desembolso` |
| `ID_EMPENHO` | `empenho` | `empenho_desembolso` |
| `ID_PROPOSTA_INSTRUMENTO_CONTRATUAL` | `inst_cont_proposta_aio_modulo_empresas` | `inst_cont_contratos_lotes_empresas_modulo_empresas`, `inst_cont_metas_submetas_po_modulo_empresas` |
| `ID_LICITACAO` | `licitacao` | `contrato`, `itens_licitacao` |
| `ID_META` | `meta_crono_fisico` | `etapa_crono_fisico` |
| `NR_MOV_FIN` | `pagamento` | `obtv_convenente` |
| `ID_PERGUNTA_SELECAO_PAC` | `pergunta_selecao_pac` | `resposta_selecao_pac` |
| `ID_PROGRAMA` | `programa` | `apoiadores_emendas_programas`, `pergunta_selecao_pac`, `programa_proponentes`, `programa_proposta`, `proposta_selecao_pac` |
| `ID_ACFFO` | `projeto_basico_acffo_modulo_empresas` | `projeto_basico_lae_modulo_empresas` |
| `ID_QCI_ACFFO` | `projeto_basico_lae_modulo_empresas` | `projeto_basico_metas_modulo_empresas` |
| `ID_META_PROJETO_BASICO` | `projeto_basico_metas_modulo_empresas` | `projeto_basico_submetas_modulo_empresas` |
| `ID_PROPONENTE` | `proponentes` | `programa_proponentes`, `proposta_selecao_pac` |
| `IDENTIF_PROPONENTE` | `proponentes` | `proposta` |
| `ID_PROPOSTA` | `proposta` | `acomp_obras_contratos_medicoes_modulo_empresas`, `ajuste_plano_trabalho`, `consorcios`, `convenio`, `coordenadas_obra`, `cronograma_desembolso`, `emenda`, `historico_projeto_basico`, `historico_situacao`, `inst_cont_proposta_aio_modulo_empresas`, `justificativas_proposta`, `meta_crono_fisico`, `plano_aplicacao_detalhado`, `programa_proposta`, `projeto_basico_acffo_modulo_empresas`, `projeto_basico_lae_modulo_empresas`, `projeto_basico_proposta_modulo_empresas`, `proposta_formalizacao_pac`, `resumo_fisico_financeiro`, `vrpl_proposta_licitacao_modulo_empresas` |
| `ID_PROPOSTA_SELECAO_PAC` | `proposta_selecao_pac` | `proposta_formalizacao_pac`, `resposta_selecao_pac` |
| `ID_SOLICITACAO` | `solicitacao_alteracao` | `termo_aditivo` |
| `ID_LICITACAO_VRPL` | `vrpl_lotes_fornecedores_licitacao_modulo_empresas` | `vrpl_proposta_licitacao_modulo_empresas` |
| `ID_PROPOSTA_VRPL` | `vrpl_proposta_licitacao_modulo_empresas` | `vrpl_metas_submetas_modulo_empresas` |

## Arquivos

### acomp_obras_contratos_medicoes_modulo_empresas

- Arquivo: `siconv_acomp_obras_contratos_medicoes_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Identificador único da tabela proposta |
| `ID_CONTRATO_MEDICAO_ACOMPANHAMENTO_OBRA` | texto (código) | igual | Identificador único da tabela med_contrato |
| `ID_MEDICAO_ACOMPANHAMENTO_OBRA` | texto (código) | igual | Identificador único da tabela med_medicao |
| `DATA_INICIO_OBRA_CONTRATO_ACOMPANHAMENTO_OBRA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Início da Obra do Contrato |
| `CNPJ_FORNECEDOR_CONTRATO_ACOMPANHAMENTO_OBRA` | texto (código) | igual | CNJP do Fornecedor |
| `NUMERO_MEDICAO_ACOMPANHAMENTO_OBRA` | texto (código) | igual | Número Sequencial da Medição |
| `SITUACAO_MEDICAO_ACOMPANHAMENTO_OBRA` | texto | contém (ignora acento) | Indicador da Situação da Medição |
| `DATA_INICIO_MEDICAO_OBJETO_ACOMPANHAMENTO_OBRA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Inicial da Medição |
| `DATA_FIM_MEDICAO_OBJETO_ACOMPANHAMENTO_OBRA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Final da Medição |
| `QTD_DIAS_SEM_MEDICAO_ACOMPANHAMENTO_OBRA` | integer | igual · faixa | Quantidade de Dias sem Medição no Acompanhamento da Obra |

### acomp_obras_valores_itens_medicao_modulo_empresas

- Arquivo: `siconv_acomp_obras_valores_itens_medicao_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_SUBMETA_VRPL` | texto (código) | igual | Identificador único da tabela med_submeta_medicao |
| `ID_CONTRATO_MEDICAO_ACOMPANHAMENTO_OBRA` | texto (código) | igual | Identificador único da tabela med_contrato |
| `VALOR_EXECUCAO_FISICA_ACUMULADA_TOTAL_ACOMPANHAMENTO_OBRA` | number | igual · faixa | Somatório do Valor Total Acumulado da Execução Física da Obra |
| `VALOR_EXECUCAO_FISICA_ACUMULADA_CONCEDENTE_ACOMPANHAMENTO_OBRA` | number | igual · faixa | Somatório do Valor Acumulado da Execução Física por parte do Concedente da Obra |
| `VALOR_EXECUCAO_FISICA_ACUMULADA_CONVENENTE_ACOMPANHAMENTO_OBRA` | number | igual · faixa | Somatório do Valor Acumulado da Execução Física por parte do Convenente da Obra |
| `VALOR_EXECUCAO_FISICA_ACUMULADA_EMPRESA_ACOMPANHAMENTO_OBRA` | number | igual · faixa | Somatório do Valor Acumulado da Execução Física por parte da Empresa da Obra |

### apoiadores_emendas_programas

- Arquivo: `apoiadores_emendas_programas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_CNPJ_PROGRAMA_EMENDA_APOIADORES_EMENDAS` | texto (código) | igual |  |
| `NUMERO_EMENDA_APOIADORES_EMENDAS` | texto (código) | igual |  |
| `NOME_PARLAMENTAR_APOIADORES_EMENDAS` | texto | contém (ignora acento) |  |
| `INDICACAO_APOIADORES_EMENDAS` | texto | contém (ignora acento) |  |
| `PARLAMENTAR_SOLICITANTE_APOIADORES_EMENDAS` | texto | contém (ignora acento) |  |
| `CPF_PF_SOLICITANTE_APOIADORES_EMENDAS` | texto (código) | igual |  |
| `NOME_PF_SOLICITANTE_APOIADORES_EMENDAS` | texto | contém (ignora acento) |  |
| `CNPJ_PJ_SOLICITANTE_APOIADORES_EMENDAS` | texto (código) | igual |  |
| `NOME_PJ_SOLICITANTE_APOIADORES_EMENDAS` | texto | contém (ignora acento) |  |
| `CNPJ_PROPONENTE_APOIADORES_EMENDAS` | texto (código) | igual |  |
| `NOME_PROPONENTE_APOIADORES_EMENDAS` | texto | contém (ignora acento) |  |
| `VALOR_REPASSE_PROPOSTA_APOIADORES_EMENDAS` | number | igual · faixa |  |
| `ID_PROGRAMA` | texto (código) | igual |  |

### consorcios

- Arquivo: `siconv_consorcios.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `CNPJ_CONSORCIO` | texto (código) | igual | CNPJ do Consórcio |
| `NOME_CONSORCIO` | texto | contém (ignora acento) | Razão Social do Consórcio |
| `CODIGO_CNAE_PRIMARIO` | texto | contém (ignora acento) | Código do CNAE Primário na Receita Federal |
| `DESC_CNAE_PRIMARIO` | texto | contém (ignora acento) | Descrição do CNAE Primário na Receita Federal |
| `CODIGO_CNAE_SECUNDARIO` | texto | contém (ignora acento) | Código do CNAE Secundário na Receita Federal |
| `DESC_CNAE_SECUNDARIO` | texto | contém (ignora acento) | Descrição do CNAE Secundário na Receita Federal |
| `CNPJ_PARTICIPANTE` | texto (código) | igual | CNPJ dos Participantes do Consórcio |
| `NOME_PARTICIPANTE` | texto | contém (ignora acento) | Descrição do nome dos participantes do Consórcio |

### contrato

- Arquivo: `siconv_contrato.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONTRATO` | texto (código) | igual | Número do contrato, gerado sequencialmente pelo Sistema |
| `DATA_PUBLICACAO_CONTRATO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da publicação do contrato |
| `DATA_ASSINATURA_CONTRATO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da assinatura do contrato |
| `DATA_INICIO_VIGENCIA_CONTRATO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de início de vigência do contrato |
| `DATA_FIM_VIGENCIA_CONTRATO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data fim de vigência do contrato |
| `OBJETO_CONTRATO` | texto | contém (ignora acento) | Objeto do contrato |
| `TIPO_AQUISICAO_CONTRATO` | texto | contém (ignora acento) | Tipo da aquisição envolvida no contrato:“SERVICO_DE_ENGENHARIA”,“SERVICO”,“MATERIAL_SERVICO”,“OBRAS”,“MATERIAL” |
| `VALOR_GLOBAL_CONTRATO` | number | igual · faixa | Valor global do contrato |
| `ID_FORNECEDOR_CONTRATO` | texto (código) | igual | Identificação do fornecedor, podendo ser o número do CNPJ, número do CPF ou número da Inscrição Genérica |
| `NOME_FORNECEDOR_CONTRATO` | texto | contém (ignora acento) | Razão Social do fornecedor |
| `ID_LICITACAO` | texto (código) | igual | Identificador único da tabela licitação |
| `ID_CONTRATO` | texto (código) | igual | Identificador único da tabela contrato |

### convenio

- Arquivo: `siconv_convenio.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `DIA` | integer | igual · faixa | Dia em que o Convênio foi assinado |
| `MES` | integer | igual · faixa | Mês em que o Convênio foi assinado |
| `ANO` | integer | igual · faixa | Ano Assinatura do Convênio |
| `DIA_ASSIN_CONV` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Assinatura do Convênio |
| `SIT_CONVENIO` | texto | contém (ignora acento) | Situação atual do Convênio. Domínio: Em execução, Convênio Anulado, Prestação de Contas enviada para Análise, Prestação de Contas Aprovada, Prestação de Contas em Análise, Prestação de Contas em Complementação, Inadimplente, etc |
| `SUBSITUACAO_CONV` | texto | contém (ignora acento) | Sub-Situação atual do Convênio. Domínio: Convênio, Convênio Cancelado, Convênio Encerrado, Proposta, Em aditivação |
| `SITUACAO_PUBLICACAO` | texto | contém (ignora acento) | Situação atual da Publicação do instrumento. Domínio: Publicado e Transferido para IN |
| `INSTRUMENTO_ATIVO` | texto | contém (ignora acento) | Convênios que ainda não foram finalizados. Domínio: SIM, NÃO |
| `IND_OPERA_OBTV` | texto | contém (ignora acento) | Indicativo de que o Convênio opera com OBTV. Domínio: SIM, NÃO |
| `NR_PROCESSO` | texto (código) | igual | Número interno do processo físico do instrumento |
| `UG_EMITENTE` | texto (código) | igual | Número da Unidade Gestora |
| `DIA_PUBL_CONV` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da Publicação do Convênio |
| `DIA_INIC_VIGENC_CONV` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Início de Vigência do Convênio |
| `DIA_FIM_VIGENC_CONV` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Fim de Vigência do Convênio |
| `DIA_FIM_VIGENC_ORIGINAL_CONV` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Fim de Vigência Original do Convênio sem os TAs e Prorrogas |
| `DIAS_PREST_CONTAS` | integer | igual · faixa | Pazo para a Prestação de Contas do Convênio |
| `DIA_LIMITE_PREST_CONTAS` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data limite para Prestação de Contas do Convênio |
| `DATA_SUSPENSIVA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data prevista para resolução da Cláusula Suspensiva |
| `DATA_RETIRADA_SUSPENSIVA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de retirada do instrumento da situação de Cláusula Suspensiva |
| `DIAS_CLAUSULA_SUSPENSIVA` | integer | igual · faixa | Quantidade de dias calculado a partir da diferença entre as datas de previsão para resolução da Cláusula Suspensiva e da data de assinatura do instrumento |
| `SITUACAO_CONTRATACAO` | texto | contém (ignora acento) | Situação atual da Contratação. Domínio: Cláusula Suspensiva, Liminar Judicial, Normal e Sob Liminar Judicial e Cláusula Suspensiva |
| `IND_ASSINADO` | texto | contém (ignora acento) | Indicativo se o Convênio está assinado ou não. Domínio: SIM, NÃO |
| `MOTIVO_SUSPENSAO` | texto | contém (ignora acento) | Descrição do motivo de suspensão referente a cláusula suspensiva |
| `IND_FOTO` | texto | contém (ignora acento) | Indicativo se o Convênio possui foto ou não. Domínio: SIM, NÃO |
| `QTDE_CONVENIOS` | integer | igual · faixa | Quantidade de Instrumentos Assinados |
| `QTD_TA` | integer | igual · faixa | Quantidade de Termos Aditivos |
| `QTD_PRORROGA` | integer | igual · faixa | Quantidade de Prorrogas de Ofício |
| `VL_GLOBAL_CONV` | number | igual · faixa | Valor global dos Instrumentos assinados (Valor de Repasse + Valor Contrapartida) |
| `VL_REPASSE_CONV` | number | igual · faixa | Valor total do aporte do Governo Federal referente a celebração do Instrumento |
| `VL_CONTRAPARTIDA_CONV` | number | igual · faixa | Valor total da Contrapartida que será disponibilizada pelo convenente |
| `VL_EMPENHADO_CONV` | number | igual · faixa | Valor total empenhado do Governo Federal para os Instrumentos |
| `VL_DESEMBOLSADO_CONV` | number | igual · faixa | Valor total desembolsado do Governo Federal para a conta do Instrumento |
| `VL_SALDO_REMAN_TESOURO` | number | igual · faixa | Valores devolvidos ao Tesouro ao término do instrumento |
| `VL_SALDO_REMAN_CONVENENTE` | number | igual · faixa | Valores devolvidos ao Convenente ao término do instrumento |
| `VL_RENDIMENTO_APLICACAO` | number | igual · faixa | Valores referentes aos redimentos de aplicação financeira |
| `VL_INGRESSO_CONTRAPARTIDA` | number | igual · faixa | Total de valores referente a ingresso de contrapartida dos Instrumentos |
| `VL_SALDO_CONTA` | number | igual · faixa | O Saldo em Conta deve ser entendido como um valor estimado, podendo sofrer variação até o próximo dia útil, principalmente, pelo fato dos rendimentos de aplicação previstos fazerem parte do referido valor. |
| `VALOR_GLOBAL_ORIGINAL_CONV` | number | igual · faixa | Valor Global Original do Instrumento |

### coordenadas_obra

- Arquivo: `siconv_coordenadas_obra.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual |  |
| `NOME_PROJETO_CADASTRO_OBRA` | texto | contém (ignora acento) |  |
| `LATITUDE_CADASTRO_OBRA	` | texto | contém (ignora acento) |  |
| `LONGITUDE_CADASTRO_OBRA` | texto | contém (ignora acento) |  |

### cronograma_desembolso

- Arquivo: `siconv_cronograma_desembolso.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `NR_PARCELA_CRONO_DESEMBOLSO` | texto (código) | igual | Número da Parcela do Desembolso |
| `MES_CRONO_DESEMBOLSO` | integer | igual · faixa | Mês do Desembolso |
| `ANO_CRONO_DESEMBOLSO` | integer | igual · faixa | Ano do Desembolso |
| `TIPO_RESP_CRONO_DESEMBOLSO` | texto | contém (ignora acento) | Tipo do Responsável definido no Cronograma de Desembolsos. Domínio: Concedente, Convenente e Rendimento de Aplicação |
| `VALOR_PARCELA_CRONO_DESEMBOLSO` | number | igual · faixa | Valor da Parcela do Desembolso |

### desbloqueio_cr

- Arquivo: `siconv_desbloqueio_cr.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `NR_OB` | texto (código) | igual | Número da OB |
| `DATA_CADASTRO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Cadastro |
| `DATA_ENVIO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de envio da solicitação de desbloqueio do recurso |
| `TIPO_RECURSO_DESBLOQUEIO` | texto | contém (ignora acento) | Tipo do Recurso. Domínio: OB, INGRESSO CONTRAPARTIDA e RENDIMENTO APLICAÇÃO |
| `VL_TOTAL_DESBLOQUEIO` | number | igual · faixa | Valor total de desbloqueio para o Contrato de Repasse |
| `VL_DESBLOQUEADO` | number | igual · faixa | Valor desbloqueado para o Contrato de Repasse |
| `VL_BLOQUEADO` | number | igual · faixa | Valor bloqueado para o Contrato de Repasse |

### desembolso

- Arquivo: `siconv_desembolso.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_DESEMBOLSO` | texto (código) | igual | Identificador único gerado pelo Sistema para o Desembolso |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `DT_ULT_DESEMBOLSO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da última Ordem Bancária gerada |
| `QTD_DIAS_SEM_DESEMBOLSO` | integer | igual · faixa | Indicador de dias sem desembolso. Domínio: 90,180 e 365 dias |
| `DATA_DESEMBOLSO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da Ordem Bancária |
| `ANO_DESEMBOLSO` | integer | igual · faixa | Ano da Ordem Bancária |
| `MES_DESEMBOLSO` | integer | igual · faixa | Mês da Ordem Bancária |
| `NR_SIAFI` | texto (código) | igual | Número do Documento no SIAFI |
| `UG_EMITENTE_DH` | texto (código) | igual | Código da Unidade Gestora responsável pela emissão do documento. |
| `OBSERVACAO_DH` | texto | contém (ignora acento) | Observação a respeito do documento hábil. |
| `VL_DESEMBOLSADO` | number | igual · faixa | Valor disponibilizado pelo Governo Federal para a conta do instrumento |

### emenda

- Arquivo: `siconv_emenda.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `QUALIF_PROPONENTE` | texto | contém (ignora acento) | Qualificação do proponente |
| `COD_PROGRAMA_EMENDA` | texto (código) | igual | Chave que identifica o programa composta por: (Cód.Órgão+Ano+Cód.Sequencial do Sistema) |
| `NR_EMENDA` | texto (código) | igual | Número da Emenda Parlamentar |
| `NOME_PARLAMENTAR` | texto | contém (ignora acento) | Nome do Parlamentar |
| `BENEFICIARIO_EMENDA` | texto | contém (ignora acento) | CNPJ do Proponente |
| `IND_IMPOSITIVO` | texto | contém (ignora acento) | Indicativo de Orçamento Impositivo (Tipo Parlamentar igual a INDIVIDUAL + Ano de Cadastro da Proposta >= 2014). Domínio: SIM, NÃO |
| `TIPO_PARLAMENTAR` | texto | contém (ignora acento) | Tipo do Parlamentar. Domínio pode ser: INDIVIDUAL, COMISSAO, BANCADA |
| `VALOR_REPASSE_PROPOSTA_EMENDA` | number | igual · faixa | Valor da Emenda cadastrada na proposta |
| `VALOR_REPASSE_EMENDA` | number | igual · faixa | Valor da Emenda assinada |

### empenho

- Arquivo: `siconv_empenho.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_EMPENHO` | texto (código) | igual | Identificador único gerado pelo Sistema para o Empenho |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `NR_EMPENHO` | texto (código) | igual | Número da Nota de Empenho |
| `TIPO_NOTA` | texto | contém (ignora acento) | Código do Tipo de Empenho |
| `DESC_TIPO_NOTA` | texto | contém (ignora acento) | Descrição do Tipo de Empenho. Domínio: Empenho Original, Empenho de Despesa Pré-Empenhada, Anulação de Empenho, Reforço de Empenho, Estorno de Anulação de Empenho, etc |
| `DATA_EMISSAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de emissão do Empenho |
| `COD_SITUACAO_EMPENHO` | texto (código) | igual | Código da Situação atual do empenho |
| `DESC_SITUACAO_EMPENHO` | texto | contém (ignora acento) | Descrição da Situação atual do empenho. Domínio: Registrado no SIAFI e Enviado |
| `UG_EMITENTE` | texto (código) | igual | Unidade Gestora Emitente |
| `UG_RESPONSAVEL` | texto (código) | igual | Unidade Gestora Responsável |
| `FONTE_RECURSO` | texto | contém (ignora acento) | Fonte de Recurso da Nota de Empenho |
| `NATUREZA_DESPESA` | texto | contém (ignora acento) | Código da natureza de despesa |
| `PLANO_INTERNO` | texto | contém (ignora acento) | Descreve o Plano Interno que é composto por até 11 (onze) dígitos alfa-numéricos. |
| `PTRES` | texto | contém (ignora acento) | Programa de Trabalho Resumido corresponde à codificação resumida do Programa de Trabalho (PT) |
| `VALOR_EMPENHO` | number | igual · faixa | Valor empenhado |
| `RESULTADO_PRIMARIO` | texto | contém (ignora acento) | Resultado primário do empenho |
| `OBSERVACAO_EMPENHO` | texto | contém (ignora acento) | Observação do empenho |
| `DESCRICAO_EMENDA_SIAFI` | texto | contém (ignora acento) | Descrição da emenda SIAFI |

### empenho_desembolso

- Arquivo: `siconv_empenho_desembolso.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_DESEMBOLSO` | texto (código) | igual | Identificador único gerado pelo Sistema para o Desembolso |
| `ID_EMPENHO` | texto (código) | igual | Identificador único gerado pelo Sistema para o Empenho |
| `VALOR_GRUPO` | number | igual · faixa | Valor presente nos dados orçamentários da OB |

### etapa_crono_fisico

- Arquivo: `siconv_etapa_crono_fisico.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_META` | texto (código) | igual | Código Sequencial do Sistema para uma Meta |
| `ID_ETAPA` | texto (código) | igual | Código Sequencial do Sistema para uma Etapa |
| `NR_ETAPA` | texto (código) | igual | Número da Etapa gerada pelo Sistema |
| `DESC_ETAPA` | texto | contém (ignora acento) | Especificação da etapa vinculada a meta do cronograma físico |
| `DATA_INICIO_ETAPA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de início prevista para execução da etapa |
| `DATA_FIM_ETAPA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data fim prevista para execução da etapa |
| `UF_ETAPA` | texto (código) | igual | UF cadastrada para a Etapa |
| `MUNICIPIO_ETAPA` | texto | contém (ignora acento) | Município cadastrado para a Etapa |
| `ENDERECO_ETAPA` | texto | contém (ignora acento) | Endereço cadastrado para a Etapa |
| `CEP_ETAPA` | texto (código) | igual | CEP cadastrado para a Etapa |
| `QTD_ETAPA` | integer | igual · faixa | Quantidade da etapa vinculada a meta do cronograma físico. |
| `UND_FORNECIMENTO_ETAPA` | texto | contém (ignora acento) | Unidade de fornecimento vinculada a etapa |
| `VL_ETAPA` | number | igual · faixa | Valor total da etapa vinculada a meta do cronograma físico |

### historico_projeto_basico

- Arquivo: `siconv_historico_projeto_basico.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `DATA_HIST_PB_TR` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de registro |
| `SITUACAO_HIST_PB_TR` | texto | contém (ignora acento) | Situação do acompanhamento, valores possiveis ELA(Em Elaboracao), ANL (Em Análise), SCP (Complementação Solicitada), COM (Em complementacao), ACT (Aceita) |
| `EVENTO_HIST_PB_TR` | texto | contém (ignora acento) | Indicador do Evento |
| `VERSAO_DOC_PB_TR` | texto | contém (ignora acento) | Número da Versão usada no sistema de versionamento |

### historico_situacao

- Arquivo: `siconv_historico_situacao.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `DIA_HISTORICO_SIT` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de entrada da situação no sistema |
| `HISTORICO_SIT` | texto | contém (ignora acento) | Situação histórica da Proposta/Convênio |
| `DIAS_HISTORICO_SIT` | integer | igual · faixa | Dias em que a Proposta/Convênio permaneceu na situação |
| `COD_HISTORICO_SIT` | texto (código) | igual | Código da situação histórica da Proposta/Convênio, contendo a ordem cronológica do ciclo de vida de um convênio |

### ingresso_contrapartida

- Arquivo: `siconv_ingresso_contrapartida.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `DT_INGRESSO_CONTRAPARTIDA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da disponibilização do recurso por parte do Convenente |
| `VL_INGRESSO_CONTRAPARTIDA` | number | igual · faixa | Valor disponibilizado pelo Convenente para a conta do instrumento |

### inst_cont_contratos_lotes_empresas_modulo_empresas

- Arquivo: `siconv_inst_cont_contratos_lotes_empresas_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_CONTRATO_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.contrato |
| `ID_PROPOSTA_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.proposta |
| `ID_LOTE_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.lote |
| `NUMERO_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Número do Instrumento Contratual |
| `SITUACAO_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Situação do Instrumento Contratual |
| `DATA_ASSINATURA_INSTRUMENTO_CONTRATUAL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Assinatura do Instrumento Contratual |
| `DATA_INICIO_VIGENCIA_INSTRUMENTO_CONTRATUAL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data do Início da Vigência do Instrumento Contratual |
| `DATA_FIM_VIGENCIA_INSTRUMENTO_CONTRATUAL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data do Fim da Vigência do Instrumento Contratual |
| `NUMERO_LOTE_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Número do Lote do Instrumento Contratual |
| `RAZAO_SOCIAL_EMPRESA_EXECUTORA_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Razão Social do Executor do Instrumento Contratual |
| `TIPO_IDENTIFICACAO_EMPRESA_EXECUTORA_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Tipo de Identificação (CPF ou CNPJ) do Executor do Instrumento Contratual |
| `IDENTIFICACAO_EMPRESA_EXECUTORA_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | CPF ou CNPJ do Executor do Instrumento Contratual |

### inst_cont_metas_submetas_po_modulo_empresas

- Arquivo: `siconv_inst_cont_metas_submetas_po_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_META_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.meta |
| `ID_SUBMETA_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.submeta |
| `ID_PO_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.po |
| `ID_PROPOSTA_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.proposta |
| `ID_LOTE_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.lote |
| `NUMERO_META_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Número da Meta do Instrumento Contratual |
| `DESCRICAO_META_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Descrição da Meta do Instrumento Contratual |
| `NUMERO_SUBMETA_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Número da Submeta do Instrumento Contratual |
| `DESCRICAO_SUBMETA_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Descrição da Submeta do Instrumento Contratual |
| `SITUACAO_SUBMETA_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Situação da Submeta do Instrumento Contratual |
| `VALOR_TOTAL_LICITADO_INSTRUMENTO_CONTRATUAL` | number | igual · faixa | Valor Total Licitado do Instrumento Contratual |
| `DATA_PREVISAO_INICIO_OBRA_INSTRUMENTO_CONTRATUAL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Previsão do Início da Obra do Instrumento Contratual |
| `DATABASE_PO_VRPL_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Data-base do Instrumento Contratual |
| `SIGLA_LOCALIDADE_PO_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Sigla da Localidade do Instrumento Contratual |
| `ACOMPANHADO_POR_EVENTO_PO_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Indicador se o PO é acompanhado por eventos no Instrumento Contratual |

### inst_cont_proposta_aio_modulo_empresas

- Arquivo: `siconv_inst_cont_proposta_aio_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.proposta |
| `ID_PROPOSTA` | texto (código) | igual | Identificador único da tabela proposta |
| `ID_AIO_INSTRUMENTO_CONTRATUAL` | texto (código) | igual | Identificador único da tabela instrumentos_contratuais_VBL.aio |
| `SITUACAO_AIO_INSTRUMENTO_CONTRATUAL` | texto | contém (ignora acento) | Situação da Emissão do AIO |
| `DATA_EMISSAO_AIO_INSTRUMENTO_CONTRATUAL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Emissão do AIO |

### itens_dl

- Arquivo: `siconv_itens_dl.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NOME_ITEM_DL` | texto | contém (ignora acento) | Nome Do Item Do Documento De Liquidação |
| `QTD_ITEM_DL` | integer | igual · faixa | Quantidade Do Item Do Documento De Liquidação |
| `UNIDADE_ITEM_DL` | texto | contém (ignora acento) | Unidade Do Item Do Documento De Liquidação |
| `VALOR_TOTAL_ITEM_DL` | number | igual · faixa | Valor Total Do Item Do Documento De Liquidação |
| `DESCRICAO_ITEM_DL` | texto | contém (ignora acento) | Descrição Do Item Do Documento De Liquidação |
| `ID_ITEM_DL` | texto (código) | igual | Identificador Do Item Do Documento De Liquidação |

### itens_licitacao

- Arquivo: `siconv_itens_licitacao.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_LICITACAO` | texto (código) | igual | Identificador único da tabela licitação |
| `ID_ITEM_LICITACAO` | texto (código) | igual | Identificador do item da licitação |
| `SEQUENCIAL_ITEM_LICITACAO` | texto | contém (ignora acento) |  |
| `DESCRICAO_ITEM_LICITACAO` | texto | contém (ignora acento) |  |
| `TIPO_UNIDADE_ITEM_LICITACAO` | texto | contém (ignora acento) |  |
| `QUANTIDADE_ITEM_LICITACAO` | integer | igual · faixa |  |
| `PRECO_UNITARIO_ITEM_LICITACAO` | texto | contém (ignora acento) |  |
| `NOME_FORNECEDOR_ITEM_LICITACAO` | texto | contém (ignora acento) |  |
| `IDENTIFICACAO_FORNECEDOR_ITEM_LICITACAO` | texto | contém (ignora acento) |  |
| `VALOR_TOTAL_ITEM_LICITACAO` | number | igual · faixa |  |

### justificativas_proposta

- Arquivo: `siconv_justificativas_proposta.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `CARACTERIZACAO_INTERESSES_RECI` | texto | contém (ignora acento) | Caracterização dos interesses recíprocos da proposta |
| `PUBLICO_ALVO` | texto | contém (ignora acento) | Público alvo da proposta |
| `PROBLEMA_A_SER_RESOLVIDO` | texto | contém (ignora acento) | Problema a ser resolvido pela proposta |
| `RESULTADOS_ESPERADOS` | texto | contém (ignora acento) | Resultados esperados da proposta |
| `RELACAO_PROPOSTA_OBJETIVOS_PRO` | texto | contém (ignora acento) | Relação entre a proposta e os objetivos e diretrizes do programa |
| `CAPACIDADE_TECNICA` | texto | contém (ignora acento) | Capacidade Técnica e Gerencial da proposta |
| `JUSTIFICATIVA` | texto | contém (ignora acento) | Justificativa da solicitação da proposta |

### licitacao

- Arquivo: `siconv_licitacao.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_LICITACAO` | texto (código) | igual | Identificador único da tabela licitação |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `NR_LICITACAO` | texto (código) | igual | Número do Processo de Execução |
| `MODALIDADE_LICITACAO` | texto | contém (ignora acento) | Modalidade, depende do Recurso Nacional ou Internacional:Recurso - Lei 8.666/1993:  Convite, Tomada de Preços, Concorrência e Concurso. Recurso - Lei 10.520/2002 - Pregão: Pregão |
| `TP_PROCESSO_COMPRA` | texto | contém (ignora acento) | Processo de Compras: Dispensa de Licitação, Inexigibilidade, Licitação, Cotação Prévia, Pesquisa de Mercado |
| `TIPO_LICITACAO` | texto | contém (ignora acento) | Tipo da Licitação: depende da modalidade.Modalidade Convite: Menor Valor.Modalidade Tomada de Preço: Menor Preço, Melhor Técnica, Técnica e Preço.Modalidade Concorrência:  Internacional, Menor Preço, Melhor Técnica e Técnica e Preço.Modalidade Pregão:  Eletrônico, Eletrônico para Registro de Preço, Eletrônico por Maior Desconto, Eletrônico por Lote (grupo de itens), Presencial, Presencial para Registro de Preço, Presencial por Maior Desconto |
| `NR_PROCESSO_LICITACAO` | texto (código) | igual | Número do Processo informado pelo usuário |
| `DATA_PUBLICACAO_LICITACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de publicação do Processo de Execução |
| `DATA_ABERTURA_LICITACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de abertura do Processo de Execução |
| `DATA_ENCERRAMENTO_LICITACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de encerramento do Processo de Execução |
| `DATA_HOMOLOGACAO_LICITACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de homologação do Processo de Execução |
| `STATUS_LICITACAO` | texto | contém (ignora acento) | Status: "Concluído", "Em Elaboração" |
| `SITUACAO_ACEITE_PROCESSO_EXECU` | texto | contém (ignora acento) | Situação do aceite do processo de execução |
| `SISTEMA_ORIGEM` | texto | contém (ignora acento) | Nome do Sistema de Origem da Licitação |
| `SITUACAO_SISTEMA` | texto | contém (ignora acento) | Descrição da Situação da Licitação no Sistema de Compras Externo |
| `VALOR_LICITACAO` | number | igual · faixa | Valor da Licitação |
| `DATA_ANALISE_ACEITE` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de aceite da análise |
| `DATA_ENVIO_ANALISE` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de envio da análise |

### meta_crono_fisico

- Arquivo: `siconv_meta_crono_fisico.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_META` | texto (código) | igual | Código Sequencial do Sistema para uma Meta |
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `COD_PROGRAMA` | texto (código) | igual | Chave que identifica o programa composta por: (Cód.Órgão+Ano+Cód.Sequencial do Sistema) |
| `NOME_PROGRAMA` | texto | contém (ignora acento) | Descrição do Programa de Governo |
| `NR_META` | texto (código) | igual | Número da Meta gerada pelo Sistema |
| `TIPO_META` | texto | contém (ignora acento) | Tipo da Meta: NORMAL/APLICAÇÃO |
| `DESC_META` | texto | contém (ignora acento) | Especificação da Meta do Cronograma Físico |
| `DATA_INICIO_META` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de início da Meta |
| `DATA_FIM_META` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de término da Meta |
| `UF_META` | texto (código) | igual | UF cadastrada para a Meta |
| `MUNICIPIO_META` | texto | contém (ignora acento) | Município cadastrado para a Meta |
| `ENDERECO_META` | texto | contém (ignora acento) | Endereço cadastrado para a Meta |
| `CEP_META` | texto (código) | igual | CEP cadastrado para a Meta |
| `QTD_META` | integer | igual · faixa | Quantidade da Meta |
| `UND_FORNECIMENTO_META` | texto | contém (ignora acento) | Unidade de Fornecimento da Meta |
| `VL_META` | number | igual · faixa | Valor da Meta |

### obtv_convenente

- Arquivo: `siconv_obtv_convenente.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_MOV_FIN` | texto (código) | igual | Número identificador da movimentação financeira |
| `IDENTIF_FAVORECIDO_OBTV_CONV` | texto | contém (ignora acento) | CNPJ/CPF do Favorecido recebedor do pagamento |
| `NM_FAVORECIDO_OBTV_CONV` | texto | contém (ignora acento) | Nome do Favorecido recebedor do pagamento |
| `TP_AQUISICAO` | texto | contém (ignora acento) | Tipo de Aquisição |
| `VL_PAGO_OBTV_CONV` | number | igual · faixa | Valor pago ao favorecido |

### pagamento

- Arquivo: `siconv_pagamento.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_MOV_FIN` | texto (código) | igual | Número identificador da movimentação financeira |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `IDENTIF_FORNECEDOR` | texto | contém (ignora acento) | CNPJ/CPF do Fornecedor |
| `NOME_FORNECEDOR` | texto | contém (ignora acento) | Nome do Fornecedor |
| `TP_MOV_FINANCEIRA` | texto | contém (ignora acento) | Tipo da movimentação financeira realizada. Domínio: Pagamento a favorecido, Pagamento a favorecido com OBTV |
| `DATA_PAG` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da realização do pagamento |
| `NR_DL` | texto (código) | igual | Número identificador do Documento de Liquidação |
| `DESC_DL` | texto | contém (ignora acento) | Descrição do Documento de Liquidação. Domínio: DIÁRIAS, DUPLICATA, FATURA, FOLHA DE PAGAMENTO, NOTA FISCAL, NOTA FISCAL / FATURA, OBTV PARA EXECUTOR, OBTV PARA O CONVENENTE, etc |
| `VL_PAGO` | number | igual · faixa | Valor do pagamento |
| `ID_DL` | texto (código) | igual | Identificador Do Documento De Liquidação |
| `DATA_EMISSAO_DL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data De Emissão Do Documento De Liquidação |

### pagamento_tributo

- Arquivo: `siconv_pagamento_tributo.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `DATA_TRIBUTO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da realização do pagamento do tributo |
| `VL_PAG_TRIBUTOS` | number | igual · faixa | Valor do tributo |

### pergunta_selecao_pac

- Arquivo: `siconv_pergunta_selecao_pac.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PERGUNTA_SELECAO_PAC` | texto (código) | igual | Identificador único da pergunta do programa Novo PAC |
| `ID_PROGRAMA` | texto (código) | igual | Código Sequencial do Sistema para um Programa |
| `PERGUNTA_SELECAO_PAC` | texto | contém (ignora acento) | Campo para definição da pergunta do programa Novo PAC. |

### plano_aplicacao_detalhado

- Arquivo: `siconv_plano_aplicacao_detalhado.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `SIGLA` | texto (código) | igual | UF cadastrada referente a localidade do item. Domínio: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO |
| `MUNICIPIO` | texto | contém (ignora acento) | Município cadastrado referente a localidade do item |
| `NATUREZA_AQUISICAO` | texto | contém (ignora acento) | Código de natureza de aquisição |
| `DESCRICAO_ITEM` | texto | contém (ignora acento) | Descrição do Item |
| `CEP_ITEM` | texto (código) | igual | CEP cadastrado referente a localidade do item |
| `ENDERECO_ITEM` | texto | contém (ignora acento) | Endereço cadastrado referente a localidade do item |
| `TIPO_DESPESA_ITEM` | texto | contém (ignora acento) | Tipo da Despesa. Domínio: SERVICO, BEM, OUTROS, TRIBUTO, OBRA e DESPESA_ADMINISTRATIVA |
| `NATUREZA_DESPESA` | texto | contém (ignora acento) | Natureza da Despesa referente ao item |
| `SIT_ITEM` | texto | contém (ignora acento) | Situação atual do Item. Domínio: APROVADO |
| `COD_NATUREZA_DESPESA` | texto (código) | igual | O campo que se refere à natureza da despesa contém um código composto por oito algarismos, sendo que o 1º dígito representa a categoria econômica, o 2º o grupo de natureza da despesa, o 3º e o 4º dígitos representam a modalidade de aplicação, o 5º e o 6º o elemento de despesa e o 7º e o 8º dígitos representam o desdobramento facultativo do elemento de despesa (subelemento). |
| `QTD_ITEM` | integer | igual · faixa | Quantidade de Itens |
| `VALOR_UNITARIO_ITEM` | number | igual · faixa | Valor unitário do item |
| `VALOR_TOTAL_ITEM` | number | igual · faixa | Valor total do item |
| `ID_ITEM_PAD` | texto (código) | igual | Identificador único do item do plano de aplicação |

### programa

- Arquivo: `siconv_programa.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROGRAMA` | texto (código) | igual | Código Sequencial do Sistema para um Programa |
| `COD_ORGAO_SUP_PROGRAMA` | texto (código) | igual | Código do Órgão executor do Programa |
| `DESC_ORGAO_SUP_PROGRAMA` | texto | contém (ignora acento) | Nome do Órgão executor do Programa |
| `COD_PROGRAMA` | texto (código) | igual | Chave que identifica o programa composta por: (Cód.Órgão+Ano+Cód.Sequencial do Sistema) |
| `NOME_PROGRAMA` | texto | contém (ignora acento) | Descrição do Programa de Governo |
| `SIT_PROGRAMA` | texto | contém (ignora acento) | Situação atual do Programa. Domínio: Cadastrado; Disponibilizado; Inativo |
| `DATA_DISPONIBILIZACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de disponibilização do Programa |
| `ANO_DISPONIBILIZACAO` | integer | igual · faixa | Ano de disponibilização do Programa |
| `DT_PROG_INI_RECEB_PROP` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início para o recebimento das propostas voluntárias para o Programa |
| `DT_PROG_FIM_RECEB_PROP` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim para o recebimento das propostas voluntárias para o Programa |
| `DT_PROG_INI_EMENDA_PAR` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início para o recebimento das propostas de Emenda Parlamentar para o Programa |
| `DT_PROG_FIM_EMENDA_PAR` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim para o recebimento das propostas de Emenda Parlamentar para o Programa |
| `DT_PROG_INI_BENEF_ESP` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início para o recebimento das propostas de beneficiário específico para o Programa |
| `DT_PROG_FIM_BENEF_ESP` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim para o recebimento das propostas de beneficiário específico para o Programa |
| `MODALIDADE_PROGRAMA` | texto | contém (ignora acento) | Modalidade do Programa. Domínio pode ser: CONTRATO DE REPASSE, CONVENIO, TERMO DE COLABORACAO, TERMO DE FOMENTO e TERMO DE PARCERIA |
| `NATUREZA_JURIDICA_PROGRAMA` | texto | contém (ignora acento) | Natureza Jurídica Atendida pelo Programa. Domínio: Administração Pública Estadual ou do Distrito Federal, Administração Pública Municipal, Consórcio Público, Empresa pública/Sociedade de economia mista e Organização da Sociedade Civil |
| `UF_PROGRAMA` | texto (código) | igual | Ufs Habilitadas para o Programa. Domínio: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO, <null>. Quando o valor é nulo, o programa atende a todo o Brasil |
| `ACAO_ORCAMENTARIA` | texto | contém (ignora acento) | Número da Ação Orçamentária |
| `NOME_SUBTIPO_PROGRAMA` | texto | contém (ignora acento) | Nome do subtipo de instrumento |
| `DESCRICAO_SUBTIPO_PROGRAMA` | texto | contém (ignora acento) | Descrição do subtipo do instrumento |

### programa_proponentes

- Arquivo: `siconv_programa_proponentes.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROGRAMA` | texto (código) | igual | Código Sequencial do Sistema para um Programa |
| `ID_PROPONENTE` | texto (código) | igual | Identificador único do proponente |

### programa_proposta

- Arquivo: `siconv_programa_proposta.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROGRAMA` | texto (código) | igual | Código Sequencial do Sistema para um Programa |
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |

### projeto_basico_acffo_modulo_empresas

- Arquivo: `siconv_projeto_basico_acffo_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_ACFFO` | texto (código) | igual | Identificador único da tabela acffo |
| `ID_PROPOSTA` | texto (código) | igual | Identificador único da tabela proposta |
| `ULTIMA_VERSAO_PROJETO_BASICO` | texto | contém (ignora acento) | Número da versão atual do Projeto Básico |
| `APELIDO_EMPREENDIMENTO_PROJETO_BASICO` | texto | contém (ignora acento) | Apelido do empreendimento |
| `SITUACAO_PROJETO_BASICO` | texto | contém (ignora acento) | Situacao do Projeto Básico |
| `SITUACAO_SPA` | texto | contém (ignora acento) | Situação do SPA |
| `DATA_ACEITE_PROJETO_BASICO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data do aceite do Projeto Básico |

### projeto_basico_lae_modulo_empresas

- Arquivo: `siconv_projeto_basico_lae_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_QCI_ACFFO` | texto (código) | igual | Identificador único da tabela acffo_qci |
| `ID_ACFFO` | texto (código) | igual | Identificador único da tabela acffo |
| `ID_PROPOSTA` | texto (código) | igual | Identificador único da tabela proposta |
| `SITUACAO_LAE_PROJETO_BASICO` | texto | contém (ignora acento) | Situação da LAE do Projeto Básico |
| `EMISSAO_LAE_PROJETO_BASICO` | texto | contém (ignora acento) | Emissão da LAE do Projeto Básico |
| `DATA_EMISSAO_LAE_PROJETO_BASICO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Emissão da LAE do Projeto Básico |

### projeto_basico_metas_modulo_empresas

- Arquivo: `siconv_projeto_basico_metas_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_META_PROJETO_BASICO` | texto (código) | igual | Identificador único da tabela acffo_meta |
| `ID_QCI_ACFFO` | texto (código) | igual | Identificador único da tabela acffo_qci |
| `NUMERO_META_PROJETO_BASICO` | texto (código) | igual | Número da Meta |
| `DESCRICAO_META_PROJETO_BASICO` | texto | contém (ignora acento) | Descrição da Meta |
| `NOME_ITEM_INVESTIMENTO_META` | texto | contém (ignora acento) | Nome do Item de Investimento |
| `DESCRICAO_SUBITEM_INVESTIMENTO_META` | texto | contém (ignora acento) | Descrição do Subitem de Investimento |
| `QUANTIDADE_ITENS_META_PROJETO_BASICO` | integer | igual · faixa | Quantidade de itens da Meta |
| `UNIDADE_ITEM_INVESTIMENTO_META` | texto | contém (ignora acento) | Código da unidade de fornecimento |

### projeto_basico_proposta_modulo_empresas

- Arquivo: `siconv_projeto_basico_proposta_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA_ACFFO` | texto (código) | igual | Identificador único da tabela acffo_proposta |
| `ID_PROPOSTA` | texto (código) | igual | Identificador único da tabela proposta |
| `VALOR_GLOBAL_PROPOSTA_PROJETO_BASICO` | number | igual · faixa | Valor Global da Proposta do Projeto Básico |

### projeto_basico_submetas_modulo_empresas

- Arquivo: `siconv_projeto_basico_submetas_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_SUBMETA_PROJETO_BASICO` | texto (código) | igual | Identificador único da tabela acffo_submeta |
| `ID_META_PROJETO_BASICO` | texto (código) | igual | Identificador único da tabela acffo_meta |
| `LOTE_SUBMETA_PROJETO_BASICO` | texto | contém (ignora acento) | Número do Lote |
| `NUMERO_SUBMETA_PROJETO_BASICO` | texto (código) | igual | Número da Submeta |
| `DESCRICAO_SUBMETA_PROJETO_BASICO` | texto | contém (ignora acento) | Descrição da Submeta |
| `SITUACAO_SUBMETA_PROJETO_BASICO` | texto | contém (ignora acento) | Indicador da Situação |
| `VALOR_REPASSE_SUBMETA_PROJETO_BASICO` | number | igual · faixa | Valor do Repasse |
| `VALOR_CONTRAPARTIDA_SUBMETA_PROJETO_BASICO` | number | igual · faixa | Valor da Contrapartida |
| `VALOR_OUTROS_SUBMETA_PROJETO_BASICO` | number | igual · faixa | Valor Outros |
| `VALOR_TOTAL_SUBMETA_PROJETO_BASICO` | number | igual · faixa | Valor Total |
| `DATA_PREVISAO_INICIO_OBRA_PROJETO_BASICO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de previsão do início da obra |
| `QUANTIDADE_MESES_DURACAO_OBRA_PROJETO_BASICO` | integer | igual · faixa | Quantidade de meses de duração da obra |
| `DATABASE_OBRA_PROJETO_BASICO` | texto | contém (ignora acento) | Data-base da PO |
| `SIGLA_LOCALIDADE_OBRA_PROJETO_BASICO` | texto (código) | igual | Sigla da localidade |
| `OBRA_ACOMPANHADA_POR_EVENTO_PROJETO_BASICO` | texto | contém (ignora acento) | Indicador de acompanhamento de eventos |

### proponentes

- Arquivo: `siconv_proponentes.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPONENTE` | texto (código) | igual | Identificador único do proponente |
| `IDENTIF_PROPONENTE` | texto | contém (ignora acento) | CNPJ do Proponente |
| `NM_PROPONENTE` | texto | contém (ignora acento) | Nome da Entidade Proponente |
| `MUNICIPIO_PROPONENTE` | texto | contém (ignora acento) | Município do Proponente |
| `UF_PROPONENTE` | texto (código) | igual | UF do Proponente. Domínio: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO |
| `ENDERECO_PROPONENTE` | texto | contém (ignora acento) | Endereço do Proponente |
| `BAIRRO_PROPONENTE` | texto | contém (ignora acento) | Bairro do Proponente |
| `CEP_PROPONENTE` | texto (código) | igual | CEP do Proponente |
| `EMAIL_PROPONENTE` | texto | contém (ignora acento) | E-mail do Proponente |
| `TELEFONE_PROPONENTE` | texto | contém (ignora acento) | Telefone do Proponente |
| `FAX_PROPONENTE` | texto | contém (ignora acento) | Fax do Proponente |

### proposta

- Arquivo: `siconv_proposta.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `UF_PROPONENTE` | texto (código) | igual | UF do Proponente. Domínio: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO |
| `MUNIC_PROPONENTE` | texto | contém (ignora acento) | Município do Proponente |
| `COD_MUNIC_IBGE` | texto (código) | igual | Código IBGE do Município |
| `COD_ORGAO_SUP` | texto (código) | igual | Código do Órgão Superior do Concedente |
| `DESC_ORGAO_SUP` | texto | contém (ignora acento) | Nome do Órgão Superior do Concedente |
| `NATUREZA_JURIDICA` | texto | contém (ignora acento) | Natureza Jurídica do Proponente. Domínio: Administração Pública Estadual ou do Distrito Federal, Administração Pública Municipal, Consórcio Público, Empresa pública/Sociedade de economia mista e Organização da Sociedade Civil |
| `NR_PROPOSTA` | texto (código) | igual | Número da Proposta gerado pelo Siconv |
| `DIA_PROP` | integer | igual · faixa | Dia do cadastro da Proposta |
| `MES_PROP` | integer | igual · faixa | Mês do cadastro da Proposta |
| `ANO_PROP` | integer | igual · faixa | Ano do cadastro da Proposta |
| `DIA_PROPOSTA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data do cadastro da Proposta |
| `COD_ORGAO` | texto (código) | igual | Código do Órgão ou Entidade Concedente |
| `DESC_ORGAO` | texto | contém (ignora acento) | Nome do Órgão ou Entidade Concedente |
| `MODALIDADE` | texto | contém (ignora acento) | Modalidade da Proposta. Domínio pode ser: CONTRATO DE REPASSE, CONVENIO, TERMO DE COLABORACAO, TERMO DE FOMENTO e TERMO DE PARCERIA |
| `IDENTIF_PROPONENTE` | texto | contém (ignora acento) | CNPJ do Proponente |
| `NM_PROPONENTE` | texto | contém (ignora acento) | Nome da Entidade Proponente |
| `CEP_PROPONENTE` | texto (código) | igual | CEP do Proponente |
| `ENDERECO_PROPONENTE` | texto | contém (ignora acento) | Endereço do Proponente |
| `BAIRRO_PROPONENTE` | texto | contém (ignora acento) | Bairro do Proponente |
| `NM_BANCO` | texto | contém (ignora acento) | Nome do Banco para depósito do recurso da Transferência Voluntária |
| `SITUACAO_CONTA` | texto | contém (ignora acento) | Situação atual da conta bancária do instrumento. Domínio: Aguardando Retorno do Banco, Enviada, Cadastrada, Registrada, Erro na Abertura de Conta, Regularizada, A Verificar, Aguardando Envio e Pendente de Regularização |
| `SITUACAO_PROJETO_BASICO` | texto | contém (ignora acento) | Situação atual do Projeto Básico/Termo de Referência. Domínio: Aguardando Projeto Básico, Não Cadastrado, Projeto Básico Aprovado, Projeto Básico em Análise, Projeto Básico em Complementação, Projeto Básico Rejeitado |
| `SIT_PROPOSTA` | texto | contém (ignora acento) | Situação atual da Proposta. Domínio pode ser: Proposta/Plano de Trabalho Cadastrados, Proposta/Plano de Trabalho em Análise, Proposta/Plano de Trabalho Rejeitados, Proposta/Plano de Trabalho Aprovados, etc |
| `DIA_INIC_VIGENCIA_PROPOSTA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início da Vigência da Proposta |
| `DIA_FIM_VIGENCIA_PROPOSTA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim da Vigência da Proposta |
| `OBJETO_PROPOSTA` | texto | contém (ignora acento) | Descrição do Objeto da Proposta |
| `ITEM_INVESTIMENTO` | texto | contém (ignora acento) | Itens de Investimento da proposta |
| `ENVIADA_MANDATARIA` | texto | contém (ignora acento) | Campo que indica se o Contrato de Repasse foi enviado para Instituição Mandatária. Domínio: SIM, NÃO e NÃO APLICÁVEL |
| `VL_GLOBAL_PROP` | number | igual · faixa | Valor Global da proposta cadastrada (Valor de Repasse Proposta + Valor Contrapartida Proposta) |
| `VL_REPASSE_PROP` | number | igual · faixa | Valor de Repasse do Governo Federal referente a proposta cadastrada |
| `VL_CONTRAPARTIDA_PROP` | number | igual · faixa | Valor da Contrapartida apresentada na proposta pelo convenente |
| `NOME_SUBTIPO_PROPOSTA` | texto | contém (ignora acento) | Nome do subtipo de instrumento |
| `DESCRICAO_SUBTIPO_PROPOSTA` | texto | contém (ignora acento) | Descrição do subtipo do instrumento |
| `CD_AGENCIA` | texto (código) | igual | Código da Agência |
| `CD_CONTA` | texto (código) | igual | Código da Conta |

### proposta_cancelada

- Arquivo: `siconv_proposta_cancelada.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA ` | texto (código) | igual | Código Sequencial do Sistema para uma Proposta |
| `UF_PROPONENTE` | texto (código) | igual | UF do Proponente. Domínio: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO |
| `MUNIC_PROPONENTE` | texto | contém (ignora acento) | Município do Proponente |
| `COD_MUNIC_IBGE` | texto (código) | igual | Código IBGE do Município |
| `COD_ORGAO_SUP` | texto (código) | igual | Código do Órgão Superior do Concedente |
| `DESC_ORGAO_SUP` | texto | contém (ignora acento) | Nome do Órgão Superior do Concedente |
| `NATUREZA_JURIDICA` | texto | contém (ignora acento) | Natureza Jurídica do Proponente. Domínio: Administração Pública Estadual ou do Distrito Federal, Administração Pública Municipal, Consórcio Público, Empresa pública/Sociedade de economia mista e Organização da Sociedade Civil |
| `NR_PROPOSTA` | texto (código) | igual | Número da Proposta gerado pelo Siconv |
| `DIA_PROP` | integer | igual · faixa | Dia do cadastro da Proposta |
| `MES_PROP` | integer | igual · faixa | Mês do cadastro da Proposta |
| `ANO_PROP` | integer | igual · faixa | Ano do cadastro da Proposta |
| `DIA_PROPOSTA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data do cadastro da Proposta |
| `COD_ORGAO` | texto (código) | igual | Código do Órgão ou Entidade Concedente |
| `DESC_ORGAO` | texto | contém (ignora acento) | Nome do Órgão ou Entidade Concedente |
| `MODALIDADE` | texto | contém (ignora acento) | Modalidade da Proposta. Domínio pode ser: CONTRATO DE REPASSE, CONVENIO, TERMO DE COLABORACAO, TERMO DE FOMENTO e TERMO DE PARCERIA |
| `IDENTIF_PROPONENTE ` | texto | contém (ignora acento) | CNPJ do Proponente |
| `NM_PROPONENTE` | texto | contém (ignora acento) | Nome da Entidade Proponente |
| `CEP_PROPONENTE` | texto (código) | igual | CEP do Proponente |
| `ENDERECO_PROPONENTE` | texto | contém (ignora acento) | Endereço do Proponente |
| `BAIRRO_PROPONENTE` | texto | contém (ignora acento) | Bairro do Proponente |
| `NM_BANCO` | texto | contém (ignora acento) | Nome do Banco para depósito do recurso da Transferência Voluntária |
| `SITUACAO_CONTA` | texto | contém (ignora acento) | Situação atual da conta bancária do instrumento. Domínio: Aguardando Retorno do Banco, Enviada, Cadastrada, Registrada, Erro na Abertura de Conta, Regularizada, A Verificar, Aguardando Envio e Pendente de Regularização |
| `SITUACAO_PROJETO_BASICO` | texto | contém (ignora acento) | Situação atual do Projeto Básico/Termo de Referência. Domínio: Aguardando Projeto Básico, Não Cadastrado, Projeto Básico Aprovado, Projeto Básico em Análise, Projeto Básico em Complementação, Projeto Básico Rejeitado |
| `SIT_PROPOSTA` | texto | contém (ignora acento) | Situação atual da Proposta. Domínio pode ser: Proposta/Plano de Trabalho Cancelados |
| `DIA_INIC_VIGENCIA_PROPOSTA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início da Vigência da Proposta |
| `DIA_FIM_VIGENCIA_PROPOSTA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim da Vigência da Proposta |
| `OBJETO_PROPOSTA` | texto | contém (ignora acento) | Descrição do Objeto da Proposta |
| `ITEM_INVESTIMENTO` | texto | contém (ignora acento) | Itens de Investimento da proposta |
| `ENVIADA_MANDATARIA` | texto | contém (ignora acento) | Campo que indica se o Contrato de Repasse foi enviado para Instituição Mandatária. Domínio: SIM, NÃO e NÃO APLICÁVEL |
| `VL_GLOBAL_PROP` | number | igual · faixa | Valor Global da proposta cadastrada (Valor de Repasse Proposta + Valor Contrapartida Proposta) |
| `VL_REPASSE_PROP` | number | igual · faixa | Valor de Repasse do Governo Federal referente a proposta cadastrada |
| `VL_CONTRAPARTIDA_PROP` | number | igual · faixa | Valor da Contrapartida apresentada na proposta pelo convenente |
| `NOME_SUBTIPO_PROPOSTA` | texto | contém (ignora acento) | Nome do subtipo de instrumento |
| `DESCRICAO_SUBTIPO_PROPOSTA` | texto | contém (ignora acento) | Descrição do subtipo do instrumento |

### proposta_formalizacao_pac

- Arquivo: `siconv_proposta_formalizacao_pac.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA_SELECAO_PAC` | texto (código) | igual |  |
| `ID_PROPOSTA` | texto (código) | igual |  |
| `NR_RESERVADO_PAC` | texto (código) | igual |  |

### proposta_selecao_pac

- Arquivo: `siconv_proposta_selecao_pac.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA_SELECAO_PAC` | texto (código) | igual | Identificador único da Proposta do Novo PAC |
| `ID_PROGRAMA` | texto (código) | igual | Código Sequencial do Sistema para um Programa |
| `ID_PROPONENTE` | texto (código) | igual | Identificador único do proponente |
| `NR_PROPOSTA_SELECAO_PAC` | texto (código) | igual | Número da Proposta do Novo PAC |
| `DATA_CADASTRO_PROPOSTA_SELECAO_PAC` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Cadastro da Proposta do Novo PAC |
| `DATA_ENVIO_PROPOSTA_SELECAO_PAC` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de Envio da Proposta do Novo PAC |
| `OBJETO_PROPOSTA_SELECAO_PAC` | texto | contém (ignora acento) | Objeto da Proposta do Novo PAC |
| `SITUACAO_PROPOSTA_SELECAO_PAC` | texto | contém (ignora acento) | Situação da Proposta do Novo PAC. |
| `VALOR_TOTAL_PROPOSTA_SELECAO_PAC` | number | igual · faixa | Valor Total da Proposta do Novo PAC |
| `JUSTIFICATIVA_PROPOSTA_SELECAO_PAC` | texto | contém (ignora acento) | Justificativa da Proposta do Novo PAC |
| `TEM_ANEXO_PROPOSTA_SELECAO_PAC` | texto | contém (ignora acento) | Indica se a Proposta do Novo PAC tem anexos. Domínio: SIM, NÃO |

### prorroga_oficio

- Arquivo: `siconv_prorroga_oficio.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `NR_PRORROGA` | texto (código) | igual | Número do Prorroga de Ofício |
| `DT_INICIO_PRORROGA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início de Vigência do Prorroga de Ofício |
| `DT_FIM_PRORROGA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim de Vigência do Prorroga de Ofício |
| `DIAS_PRORROGA` | integer | igual · faixa | Dias de prorrogação |
| `DT_ASSINATURA_PRORROGA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de assinatura do Prorroga de Ofício |
| `SIT_PRORROGA` | texto | contém (ignora acento) | Situação atual do Prorroga de Ofício. Domínio: DISPONIBILIZADA, PUBLICADA |

### resposta_selecao_pac

- Arquivo: `siconv_resposta_selecao_pac.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PERGUNTA_SELECAO_PAC` | texto (código) | igual | Identificador único da pergunta do programa Novo PAC |
| `ID_PROPOSTA_SELECAO_PAC` | texto (código) | igual | Identificador único da Proposta do Novo PAC |
| `RESPOSTA_SELECAO_PAC` | texto | contém (ignora acento) | Resposta da pergunta da Proposta do Novo PAC |

### resumo_fisico_financeiro

- Arquivo: `siconv_resumo_fisico_financeiro.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual |  |
| `VALOR_TOTAL_RESUMO_FISICO_FINANCEIRO` | number | igual · faixa |  |
| `PERCENTUAL_EXECUCAO_RESUMO_FISICO_FINANCEIRO` | number | igual · faixa |  |
| `VALOR_REALIZADO_RESUMO_FISICO_FINANCEIRO` | number | igual · faixa |  |

### solicitacao_alteracao

- Arquivo: `siconv_solicitacao_alteracao.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_SOLICITACAO` | texto (código) | igual | Identificador único da tabela solicitacao_alteracao |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `NR_SOLICITACAO` | texto (código) | igual | Número sequencial juntamente com o ano da solicitação de alteração do Convenente para o Concedente, via termo aditivo. |
| `SITUACAO_SOLICITACAO` | texto | contém (ignora acento) | Situação da solicitação de alteração do Convenente para o Concedente, via termo aditivo: “ACEITA”, “RECUSADA”, “EM_ANALISE”, “CADASTRADA” |
| `OBJETO_SOLICITACAO` | texto | contém (ignora acento) | Objeto de alteração da solicitação de alteração do Convenente para o Concedente, via termo aditivo. |
| `DATA_SOLICITACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da solicitação de alteração do convenente para o concedente, via termo aditivo. |

### solicitacao_rendimento_aplicacao

- Arquivo: `siconv_solicitacao_rendimento_aplicacao.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_SOLICITACAO_REND_APLICACAO` | texto (código) | igual | Identificador único do registro de solicitação de uso de rendimento de aplicação. |
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999. |
| `NR_SOLICITACAO_REND_APLICACAO` | texto (código) | igual | Número único da solicitação por instrumento. |
| `STATUS_SOLICITACAO_REND_APLICACAO` | texto | contém (ignora acento) | Situação da solicitação de uso do rendimento de aplicação. Domínio: PT Ajustado e Aprovado (Aguardando atualização Agendador), Aguardando Análise do Concedente, Cadastrado, Cancelado pelo Convenente, Em Análise pelo Concedente, Autorizada (Aguardando ajuste PT), Recusada pelo Concedente, Em Complementação pelo Convenente, PT Ajustado (aguardando aprovação do Concedente), PT Ajustado e Aprovado, PT Reprovado e Cancelado,   Pendente de Envio ao SIAFI,   Enviado para o SIAFI, PT Ajustado e Pendente de Envio ao SIAFI |
| `DATA_SOLICITACAO_REND_APLICACAO` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da solicitação de uso de rendimento de aplicação. |
| `VALOR_SOLICITACAO_REND_APLICACAO` | number | igual · faixa | Valor da solicitação de uso de rendimento de aplicação. |
| `VALOR_APROVADO_SOLICITACAO_REND_APLICACAO` | number | igual · faixa | Valor aprovado pelo Concedente para uso do rendimento de aplicação. |

### termo_aditivo

- Arquivo: `siconv_termo_aditivo.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `NR_CONVENIO` | texto (código) | igual | Número gerado pelo Siconv. Possui faixa de numeração reservada que vai de 700000 a 999999 |
| `ID_SOLICITACAO` | texto (código) | igual | Identificador único da tabela solicitacao_alteracao |
| `NUMERO_TA` | texto (código) | igual | Número do Termo Aditivo |
| `TIPO_TA` | texto | contém (ignora acento) | Tipo do Termo Aditivo |
| `VL_GLOBAL_TA` | number | igual · faixa | Valor Global referente ao TA |
| `VL_REPASSE_TA` | number | igual · faixa | Valor de Repasse referente ao TA |
| `VL_CONTRAPARTIDA_TA` | number | igual · faixa | Valor de Contrapartida referente ao TA |
| `DT_ASSINATURA_TA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da assinatura do Termo Aditivo |
| `DT_INICIO_TA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Início de Vigência do Termo Aditivo |
| `DT_FIM_TA` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data Fim de Vigência do Termo Aditivo |
| `JUSTIFICATIVA_TA` | texto | contém (ignora acento) | Justificativa para a realização do Termo Aditivo |

### vrpl_lotes_fornecedores_licitacao_modulo_empresas

- Arquivo: `siconv_vrpl_lotes_fornecedores_licitacao_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_LICITACAO_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_licitacao |
| `ID_LOTE_LICITACAO_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_lote_licitacao |
| `NUMERO_LOTE_LICITACAO_VRPL` | texto (código) | igual | Número do Lote Associado |
| `RAZAO_SOCIAL_FORNECEDOR_LICITACAO_VRPL` | texto | contém (ignora acento) | Razão Social do Fornecedor |
| `TIPO_IDENTIFICACAO_FORNECEDOR_LICITACAO_VRPL` | texto | contém (ignora acento) | Informa se a identificação é CPF ou CNPJ |
| `IDENTIFICACAO_FORNECEDOR_LICITACAO_VRPL` | texto | contém (ignora acento) | CPF ou CNPJ do Fornecedor |

### vrpl_metas_submetas_modulo_empresas

- Arquivo: `siconv_vrpl_metas_submetas_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_META_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_meta |
| `ID_SUBMETA_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_submeta |
| `ID_PO_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_po |
| `ID_PROPOSTA_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_proposta |
| `NUMERO_META_VRPL` | texto (código) | igual | Número da Meta da Análise |
| `DESCRICAO_META_VRPL` | texto | contém (ignora acento) | Descrição da Meta da Análise |
| `NUMERO_LOTE_LICITACAO_VRPL` | texto (código) | igual | Número do Lote Associado |
| `NUMERO_SUBMETA_VRPL` | texto (código) | igual | Número da Submeta da fase de Análise |
| `DESCRICAO_SUBMETA_VRPL` | texto | contém (ignora acento) | Descrição da fase de Análise |
| `SITUACAO_SUBMETA_VRPL` | texto | contém (ignora acento) | Indicador da Situação da Submeta |
| `VALOR_TOTAL_LICITADO_VRPL` | number | igual · faixa | Valor total licitado |
| `DATA_PREVISAO_INICIO_OBRA_PO_VRPL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data de previsão do início da obra do VRPL |
| `DATABASE_PO_VRPL` | texto | contém (ignora acento) | Data-base preenchida no VRPL |
| `SIGLA_LOCALIDADE_PO_VRPL` | texto (código) | igual | Sigla da Localidade |
| `ACOMPANHADO_POR_EVENTO_PO_VRPL` | texto | contém (ignora acento) | Indica se PO é acompanhada por eventos |
| `QUANTIDADE_ITENS_META_VRPL` | integer | igual · faixa | Quantidade de itens da Meta da Análise |
| `DESCRICAO_SUBITEM_INVESTIMENTO_META_VRPL` | texto | contém (ignora acento) | Descrição do Subitem de Investimento |
| `UNIDADE_ITEM_INVESTIMENTO_META_VRPL` | texto | contém (ignora acento) | Código da unidade do item |

### vrpl_proposta_licitacao_modulo_empresas

- Arquivo: `siconv_vrpl_proposta_licitacao_modulo_empresas.zip`

| Coluna | Tipo | Filtro | Descrição |
|---|---|---|---|
| `ID_PROPOSTA` | texto (código) | igual | Identificador único da tabela proposta |
| `ID_PROPOSTA_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_proposta |
| `ID_LICITACAO_VRPL` | texto (código) | igual | Identificador único da tabela vrpl_licitacao |
| `ULTIMA_VERSAO_PROPOSTA_VRPL` | texto | contém (ignora acento) | Versão atual da Proposta do VRPL |
| `SITUACAO_VRPL` | texto | contém (ignora acento) | Sigla da Situação da Documentação |
| `SITUACAO_PARECER_VRPL` | texto | contém (ignora acento) | Situação do Parecer do VRPL |
| `EMISSAO_PARECER_VRPL` | texto | contém (ignora acento) | Indicador da Emissão do Parecer do VRPL |
| `DATA_EMISSAO_PARECER_VRPL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data da Emissão do Parecer do VRPL |
| `DATA_ACEITE_LICITACAO_VRPL` | date (dd/mm/aaaa no CSV) | igual (AAAA-MM-DD) · faixa | Data do Aceite da Licitação |
