# Imersão Alura Dados no Databricks

Este repositório reúne os artefatos do projeto de Engenharia de Dados construído no Databricks durante a imersão, com foco na organização das camadas Bronze, Silver e Gold a partir da base de voos da ANAC. O objetivo é estruturar a ingestão dos dados brutos, aplicar governança e padronização na Silver e deixar o terreno preparado para análises e agregações na Gold.

## Objetivo do projeto

* ingerir arquivos brutos de voos e tabelas de referência;
* organizar os dados em uma arquitetura por camadas;
* transformar a Silver em um espelho governado da Bronze, sem perder grão nem linhas;
* documentar regras de tipagem, padronização e colunas derivadas;
* preparar a base para análises posteriores sobre atrasos, aeroportos e companhias.

## Estrutura atual

* `notebooks/`
  * notebooks do projeto com ingestão, consultas exploratórias, referências e regras de governança
* `dados/vra/`
  * cópia dos arquivos CSV de VRA trazidos de `/Volumes/voebem/bronze/arquivos/vra`
* `dados/referencias/`
  * cópia dos arquivos CSV de referência trazidos de `/Volumes/voebem/bronze/arquivos/referencias`

As cópias em `dados/` foram feitas sem alterar os diretórios originais na Volume, para evitar qualquer impacto no projeto principal.

## O que foi trabalhado até agora

### 1. Organização do repositório

* os notebooks do projeto foram agrupados na pasta `notebooks/`;
* a pasta `dados/` foi criada para armazenar cópias locais dos arquivos usados no projeto;
* foi adicionada a separação entre `dados/vra/` e `dados/referencias/`.

### 2. Camada Bronze

* ingestão e exploração inicial dos arquivos VRA;
* análise dos dados brutos antes de qualquer transformação;
* uso de arquivos auxiliares de referência para enriquecer o entendimento dos dados.

### 3. Camada Silver

* definição da regra central de que a Silver deve espelhar a Bronze com governança aplicada;
* manutenção do mesmo grão e da mesma contagem de linhas da tabela original;
* transformação de colunas de horário de `STRING` para `TIMESTAMP`;
* conversão de valores sentinela como `'null'` para `NULL` real;
* padronização de `codigo_justificativa`, convertendo `N/A` para `NULL`;
* criação de colunas derivadas como datas, horas, `atraso_partida_min`, `atraso_chegada_min` e `minutos_recuperados`.

### 4. Comparação Bronze vs Silver

Foi adicionada uma análise comparativa no notebook da Silver para validar as mudanças aplicadas entre `voebem.bronze.vra` e `voebem.silver.vra`, cobrindo:

* estrutura das tabelas;
* tipos das colunas;
* amostra de registros antes e depois;
* identificação objetiva de campos tratados e padronizados.

Entre os principais resultados observados:

* Bronze e Silver mantêm 1.014.705 linhas;
* quatro colunas mudaram de `STRING` para `TIMESTAMP`;
* novas colunas analíticas e de rastreabilidade foram adicionadas na Silver;
* os tratamentos aplicados foram mensurados diretamente sobre os dados.

## Próximos passos sugeridos

* evoluir a camada Gold com métricas analíticas por companhia, rota e aeroporto;
* documentar regras de negócio que devem ficar fora da Silver e entrar apenas na Gold;
* adicionar validações automatizadas de qualidade entre as camadas;
* complementar este repositório com instruções de execução e dependências, se necessário.
