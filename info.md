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
