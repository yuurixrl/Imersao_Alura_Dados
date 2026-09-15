# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Introdução
# MAGIC %md
# MAGIC # Bronze Consultas
# MAGIC
# MAGIC Este notebook reúne consultas de validação para as tabelas criadas anteriormente pelos ativos `03_bronze_vra` e `04_bronze_referencias`.
# MAGIC
# MAGIC Objetivo:
# MAGIC * inspecionar a ingestão sem alterar os dados no catálogo;
# MAGIC * validar volume carregado, estrutura das tabelas e amostras de registros;
# MAGIC * manter as explicações em Markdown e as consultas em células SQL separadas.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Quantidade de registros - explicação
# MAGIC %md
# MAGIC ## 1. Quantidade de registros por tabela
# MAGIC
# MAGIC Esta consulta retorna a quantidade de linhas presentes em cada tabela Bronze criada anteriormente.
# MAGIC Ela é útil para validar se a carga foi materializada e para comparar rapidamente o volume entre os objetos publicados no catálogo.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Quantidade de registros
# MAGIC %sql
# MAGIC SELECT 'voebem.bronze.vra' AS tabela, COUNT(*) AS quantidade_registros
# MAGIC FROM voebem.bronze.vra
# MAGIC UNION ALL
# MAGIC SELECT 'voebem.bronze.aerodromos' AS tabela, COUNT(*) AS quantidade_registros
# MAGIC FROM voebem.bronze.aerodromos
# MAGIC UNION ALL
# MAGIC SELECT 'voebem.bronze.empresas_nacionais' AS tabela, COUNT(*) AS quantidade_registros
# MAGIC FROM voebem.bronze.empresas_nacionais
# MAGIC UNION ALL
# MAGIC SELECT 'voebem.bronze.empresas_estrangeiras' AS tabela, COUNT(*) AS quantidade_registros
# MAGIC FROM voebem.bronze.empresas_estrangeiras
# MAGIC UNION ALL
# MAGIC SELECT 'voebem.bronze.codigos_operacao' AS tabela, COUNT(*) AS quantidade_registros
# MAGIC FROM voebem.bronze.codigos_operacao
# MAGIC ORDER BY tabela;
# MAGIC

# COMMAND ----------

# DBTITLE 1,Colunas disponíveis - explicação
# MAGIC %md
# MAGIC ## 2. Colunas disponíveis nas tabelas Bronze
# MAGIC
# MAGIC Esta consulta lê o catálogo de metadados em `information_schema.columns` para listar as colunas disponíveis, sua posição, tipo e nulabilidade.
# MAGIC Ela permite validar a estrutura publicada sem consultar ou modificar diretamente o conteúdo das tabelas.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Colunas disponíveis
# MAGIC %sql
# MAGIC SELECT
# MAGIC   table_name,
# MAGIC   ordinal_position,
# MAGIC   column_name,
# MAGIC   data_type,
# MAGIC   is_nullable
# MAGIC FROM voebem.information_schema.columns
# MAGIC WHERE table_schema = 'bronze'
# MAGIC   AND table_name IN (
# MAGIC     'vra',
# MAGIC     'aerodromos',
# MAGIC     'empresas_nacionais',
# MAGIC     'empresas_estrangeiras',
# MAGIC     'codigos_operacao'
# MAGIC   )
# MAGIC ORDER BY table_name, ordinal_position;
# MAGIC

# COMMAND ----------

# DBTITLE 1,Primeiros registros - explicação
# MAGIC %md
# MAGIC ## 3. Primeiros registros armazenados
# MAGIC
# MAGIC As consultas abaixo retornam amostras simples das tabelas Bronze para inspeção visual inicial.
# MAGIC Como a intenção é validação rápida, cada consulta aplica apenas `LIMIT 10`, sem transformar ou alterar os dados.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Primeiros registros - vra
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM voebem.bronze.vra
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,Primeiros registros - aerodromos
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM voebem.bronze.aerodromos
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,Primeiros registros - empresas_nacionais
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM voebem.bronze.empresas_nacionais
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,Primeiros registros - empresas_estrangeiras
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM voebem.bronze.empresas_estrangeiras
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# DBTITLE 1,Primeiros registros - codigos_operacao
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM voebem.bronze.codigos_operacao
# MAGIC LIMIT 10;
# MAGIC