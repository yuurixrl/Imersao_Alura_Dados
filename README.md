# VoeBem Analytics no Databricks

Este repositório reúne os artefatos do projeto de engenharia de dados construído com dados públicos da ANAC durante a Imersão Alura. O fluxo cobre ingestão, modelagem em camadas, qualidade, governança e consumo analítico no Databricks.

O projeto usa a arquitetura Bronze, Silver e Gold para transformar arquivos CSV de voos regulares ativos e tabelas de referência em tabelas prontas para análise. A base principal do trabalho é a tabela `voebem.gold.obt_voos`, preparada para responder perguntas de negócio sobre atrasos, pontualidade, rotas, aeroportos e companhias aéreas.

## O que o projeto entrega

* ingestão dos arquivos VRA da ANAC para a camada Bronze;
* carga das tabelas de referência de aeródromos, empresas e códigos operacionais;
* transformação da Bronze em uma Silver governada, tipada e documentada, sem perder grão nem linhas;
* pipeline de qualidade para auditoria e quarentena na camada Silver;
* modelagem Gold com dimensão, fato e OBT para análise;
* materiais auxiliares para documentação, perguntas de negócio e uso com Genie.

## Arquitetura de dados

### Bronze

Camada de aterrissagem dos dados brutos, com mínima intervenção.

Tabelas principais:

* `voebem.bronze.vra`
* `voebem.bronze.aerodromos`
* `voebem.bronze.empresas_nacionais`
* `voebem.bronze.empresas_estrangeiras`
* `voebem.bronze.codigos_operacao`

### Silver

Camada governada que preserva a granularidade da Bronze, aplica tipagem, padronização e colunas derivadas, mas evita regras de negócio que filtrem ou agreguem a base.

Tabelas principais:

* `voebem.silver.vra`
* `voebem.silver.aerodromos`
* `voebem.silver.empresas`
* `voebem.silver.codigos_operacao`

### Gold

Camada de consumo analítico.

Tabelas principais:

* `voebem.gold.dim_aeroporto`
* `voebem.gold.fato_voos`
* `voebem.gold.obt_voos`

## Estrutura do repositório

* `dados/`
  * arquivos CSV usados no projeto, separados em `vra/` e `referencias/`
* `docs/`
  * documentação de apoio, guia inicial, fontes, perguntas de negócio e testes de aceitação
* `genie/`
  * instruções e configuração do espaço Genie
* `notebooks/`
  * notebooks Databricks de ingestão, validação, governança e resultados
* `pipelines/qualidade/`
  * arquivos SQL usados no pipeline de qualidade
* `scripts/`
  * utilitários para download de dados, montagem do Genie e execução via CLI
* `sql/`
  * preparação do ambiente, consultas de qualidade, modelagem Gold e gabaritos das perguntas

## Como rodar o projeto no Databricks

### 1. Pré-requisitos

Você precisa de um workspace Databricks com:

* permissão para criar catálogo, schemas, volume e tabelas;
* compute serverless ou outro compute compatível com SQL e Python;
* acesso para importar notebooks e, se quiser usar os scripts, Databricks CLI configurada.

O projeto assume o catálogo `voebem` e o volume `/Volumes/voebem/bronze/arquivos`.

### 2. Preparar o ambiente

Execute o arquivo `sql/00_preparar_ambiente.sql` em um notebook SQL ou editor SQL no Databricks. Ele cria:

* catálogo `voebem`
* schemas `bronze`, `silver` e `gold`
* volume `voebem.bronze.arquivos`

### 3. Disponibilizar os arquivos CSV

Há dois caminhos possíveis:

* usar os arquivos já versionados em `dados/vra` e `dados/referencias`;
* baixar novamente os arquivos da ANAC com `scripts/baixar_anac.py`.

Depois, envie os CSVs para o volume do Databricks nestes caminhos:

* `/Volumes/voebem/bronze/arquivos/vra/`
* `/Volumes/voebem/bronze/arquivos/referencias/`

O notebook `03_bronze_vra` espera os CSVs mensais em `/Volumes/voebem/bronze/arquivos/vra/*.csv`.

### 4. Executar os notebooks da camada Bronze e Silver

Importe os notebooks da pasta `notebooks/` para o workspace e execute nesta ordem:

1. `03_bronze_vra`
2. `04_bronze_referencias`
3. `bronze_consultas`
4. `05_silver_espelho`

O que cada etapa faz:

* `03_bronze_vra`: lê os 12 CSVs mensais do VRA e cria `voebem.bronze.vra`;
* `04_bronze_referencias`: carrega aeródromos, empresas e códigos de apoio;
* `bronze_consultas`: valida contagens, colunas e amostras da Bronze;
* `05_silver_espelho`: aplica tipagem, padronização e colunas derivadas na Silver.

### 5. Executar o pipeline de qualidade

Os arquivos em `pipelines/qualidade/` devem ser usados em um pipeline SQL no Databricks. Adicione ao mesmo pipeline:

* `01_vra_marcado.sql`
* `02_vra_auditado.sql`
* `03_vra_quarentena.sql`

Esse pipeline mede regras de qualidade, publica auditoria e isola registros problemáticos para investigação sem alterar a proposta central da Silver.

### 6. Construir a camada Gold

Execute os arquivos SQL abaixo nesta ordem:

1. `sql/gold/01_dim_aeroporto.sql`
2. `sql/gold/02_fato_voos.sql`
3. `sql/gold/03_obt_voos.sql`

Em seguida, execute os notebooks:

1. `09_governanca_gold`
2. `10_resultados_gold`

Essas etapas criam e documentam as tabelas analíticas finais e registram metadados úteis para consumo humano e por IA.

### 7. Validar o resultado

Ao final da execução, valide pelo menos:

* existência das tabelas Bronze, Silver e Gold;
* contagem equivalente entre `voebem.bronze.vra` e `voebem.silver.vra`;
* existência da OBT `voebem.gold.obt_voos` com dados consultáveis;
* documentação e governança aplicadas às tabelas Gold.

Nos resultados já observados no projeto:

* `voebem.bronze.vra` foi carregada com 1.014.705 linhas;
* a Silver preservou a mesma contagem;
* a Gold foi organizada em dimensão, fato e OBT para perguntas de negócio.

## Como rodar os scripts auxiliares

Os scripts da pasta `scripts/` são opcionais, mas ajudam na operação do projeto.

* `baixar_anac.py`
  * baixa os arquivos mais recentes da ANAC para `dados/` e atualiza `docs/fontes.md`
* `montar_genie_space.py`
  * gera `genie/genie_space.json` a partir das perguntas e gabaritos SQL
* `perguntar_genie.py`
  * envia perguntas para um espaço Genie já configurado
* `rodar_notebook.sh`
  * dispara a execução de um notebook do workspace como execução one-time
* `rodar_pipeline.sh`
  * inicia uma atualização de pipeline e acompanha o status

Para usar os scripts que dependem da CLI, configure antes:

* `DATABRICKS_CONFIG_PROFILE`
* `DATABRICKS_WORKSPACE_PATH` quando aplicável
* `GENIE_SPACE_ID` no caso do script do Genie

## Perguntas de negócio cobertas

A pasta `sql/gabarito/` traz consultas para responder perguntas como:

* quais aeroportos concentram os maiores atrasos de partida;
* como o atraso evolui ao longo do dia;
* qual companhia apresenta melhor pontualidade e menor taxa de cancelamento;
* se voos internacionais atrasam mais do que domésticos;
* quanto atraso é recuperado em voo.

## Documentação complementar

Consulte também:

* `docs/comece-aqui.md` para um passo a passo detalhado;
* `docs/fontes.md` para a origem dos arquivos e armadilhas das fontes da ANAC;
* `docs/perguntas-de-negocio.md` para o contexto analítico;
* `docs/teste-aceitacao.md` para validar a entrega.

## Resumo do fluxo

1. preparar catálogo, schemas e volume;
2. enviar ou baixar os CSVs da ANAC;
3. executar notebooks Bronze e Silver;
4. rodar o pipeline de qualidade;
5. construir a Gold;
6. validar as tabelas finais e explorar as consultas de negócio.

Com isso, o repositório fica pronto para estudo, demonstração e evolução do projeto dentro do Databricks.
