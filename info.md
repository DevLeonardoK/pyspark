# Spark
Motor de processamento de dados em grande volume. Utiliza processamento em memória, por isso sua velocidade. Organiza clusters (conjunto de máquinas) para processar em paralelo.

# Modos de execução
- **local** — roda na própria máquina, sequencial (1 thread)
- **local[N]** — roda na própria máquina, paralelo (N threads)
- **local[*]** — roda na própria máquina, paralelo (todos os cores)
- **Standalone** — cluster gerenciado pelo próprio Spark (sem Hadoop)
- **YARN** — cluster gerenciado pelo Hadoop
- **Kubernetes** — cluster gerenciado por containers

# YARN
Gerenciador de recursos do Hadoop. Controla alocação de CPU e memória entre os nós do cluster e gerencia a execução dos jobs. Composto por:
- **Resource Manager** — cérebro central, decide quem usa o quê
- **Node Manager** — roda em cada nó, reporta recursos disponíveis

# HDFS
Sistema de arquivos distribuído do Hadoop. Armazena arquivos fragmentados entre os nós do cluster. O Spark pode usar HDFS, S3, GCS ou disco local.

# Processos x Threads

**Analogia:** Processo = prédio | Thread = andares do prédio

- **Thread**: sub-tarefa dentro de um processo. Compartilha memória com as outras threads. Se uma travar, pode afetar todo o processo.
- **Processo**: isolado, tem memória própria. Comunicação com outros processos via rede. Se um morrer, não afeta os outros.

## No Spark
- **local[*]** → 1 processo com várias threads (compartilham memória)
- **Standalone/Cluster** → processos isolados comunicando via rede
  - Processo Master → Processo Worker → Processo Executor

# Cluster
Conjunto de máquinas trabalhando juntas. Cada máquina pode ser servidor físico, VM em nuvem ou container. O ganho real é somar recursos (RAM + cores) de vários nós.

| Cloud | Serviço gerenciado |
|-------|--------------------|
| GCP   | Dataproc           |
| AWS   | EMR                |
| Azure | HDInsight / Synapse |

# PySpark
API do Spark para Python.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("meu-estudo") \
    .getOrCreate()
```



# RDD
Resilient Distributed Dataset — estrutura de dados mais antiga do Spark, com menos otimizações que o DataFrame. Pouco usado atualmente.

- **`.display()`** — disponível somente no Databricks

# DataFrames
Estrutura principal do PySpark. São imutáveis — cada transformação gera um novo DataFrame.

- **`withColumn(nome, valor)`** — adiciona ou substitui uma coluna

```python
df = df.withColumn("Idade - Mais 5 anos", col("Idade") + 5)
```

# Transformações x Ações
Duas categorias de operações no PySpark:

- **Transformações** — criam um novo DataFrame a partir de outro (`filter`, `select`, `withColumn`). Não executam imediatamente (lazy evaluation).
- **Ações** — disparam a execução de todas as transformações acumuladas e retornam um resultado (`show`, `count`, `collect`).

> O Spark não é otimizado para CSV — leitura lenta e cara em nuvem.

# Leitura de arquivos

## CSV

```python
df = spark.read.csv(path, header=True, inferSchema=True)
```

- **`header=True`** — detecta o cabeçalho automaticamente
- **`inferSchema=True`** — detecta os tipos de dados automaticamente
- É possível definir um schema manualmente via `StructType` para maior controle e performance

## Parquet

Formato colunar otimizado para nuvem — leitura rápida, compressão eficiente e amplamente suportado.

```python
df = spark.read.parquet(path)
df.write.parquet(path)
```

# Modos de escrita

| Modo | Comportamento |
|------|---------------|
| `append` | Adiciona os dados ao arquivo/diretório existente |
| `overwrite` | Reescreve tudo, substituindo os dados anteriores |

```python
df.write.mode("append").parquet(path)
df.write.mode("overwrite").parquet(path)
```


agg()

Utilizado para chamar uma ou mais funções de agregação após um groupBy().

df.groupBy("Departamento").agg(
    F.sum("Salário"),
    F.avg("Salário"),
    F.max("Salário")
)

Principais funções de agregação:

F.sum() → Soma
F.avg() → Média
F.count() → Contagem
F.max() → Maior valor
F.min() → Menor valor
alias()

Utilizado para renomear uma coluna resultante.

⚠️ Deve ser aplicado na coluna e não no DataFrame.

Correto:

df.groupBy("Departamento").agg(
    F.sum("Salário").alias("salario_total")
)

Incorreto:

df.groupBy("Departamento").agg(
    F.sum("Salário")
).alias("salario_total")
asc() e desc()

Utilizados para definir a ordenação da coluna.

Recomendado aplicar diretamente na coluna:

df.orderBy(F.col("Salário").asc())
df.orderBy(F.col("Salário").desc())

Também funciona:

df.orderBy(F.col("Salário"), ascending=False)

Mas para manter consistência e clareza, prefira:

F.col("Salário").asc()
F.col("Salário").desc()
