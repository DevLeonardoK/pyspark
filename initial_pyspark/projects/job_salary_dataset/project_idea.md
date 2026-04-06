# 🔧 Projeto ETL Simples - Análise de Salários

Pipeline ETL básico para treinar PySpark, Pydantic e SQLAlchemy

---

## 📁 ESTRUTURA DO PROJETO

```
etl_salary/
├── data/
│   ├── raw/                    # CSV original aqui
│   └── processed/              # Dados processados salvos aqui
│
├── src/
│   ├── extract.py              # Ler dados do CSV
│   ├── transform.py            # Limpar e transformar dados
│   ├── load.py                 # Salvar no banco de dados
│   ├── models.py               # Modelos Pydantic (validação)
│   ├── database.py             # Configuração do banco SQLAlchemy
│   └── config.py               # Configurações do projeto
│
├── main.py                     # Executa o pipeline completo
├── requirements.txt            # Dependências
└── .env                        # Variáveis de ambiente
```

---

## ⚙️ SETUP INICIAL

### 1. Criar ambiente e instalar dependências

**requirements.txt:**
```
pyspark==3.5.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
pandas==2.1.4
python-dotenv==1.0.0
```

**Comandos:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Criar arquivo .env

```
DB_PATH=salary_data.db
MIN_SALARY=10000
MAX_SALARY=500000
```

---

## 📝 IMPLEMENTAÇÃO

### **ARQUIVO 1: src/config.py**

**O que fazer:**
- Criar classe de configuração usando Pydantic
- Ler variáveis do .env
- Definir paths do projeto

**Campos necessários:**
- DB_PATH: caminho do banco SQLite
- MIN_SALARY, MAX_SALARY: limites de validação
- Paths para data/raw e data/processed

---

### **ARQUIVO 2: src/models.py**

**O que fazer:**
- Criar modelo Pydantic para validar cada linha do CSV

**Modelo JobData deve ter:**
- job_title: string
- experience_years: int (entre 0 e 50)
- education_level: string (High School, Diploma, Bachelor, Master, PhD)
- skills_count: int (>= 0)
- industry: string
- company_size: string (Startup, Small, Medium, Large, Enterprise)
- location: string
- remote_work: string (Yes, No, Hybrid)
- certifications: int (>= 0)
- salary: float (entre MIN_SALARY e MAX_SALARY)

**Use Field() com validações:**
- `Field(..., ge=0, le=50)` para experience_years
- `Field(..., gt=0)` para salary
- `@field_validator` para validar listas de valores aceitos

---

### **ARQUIVO 3: src/database.py**

**O que fazer:**
- Criar modelo SQLAlchemy para a tabela do banco
- Criar função para inicializar o banco

**Tabela jobs deve ter:**
- Todos os campos do CSV
- Campos extras:
  - id (primary key, autoincrement)
  - salary_category (Low, Medium, High, Very High)
  - experience_level (Junior, Mid, Senior, Expert)
  - created_at (timestamp)

**Funções necessárias:**
- `create_engine()`: criar conexão com SQLite
- `create_tables()`: criar tabelas
- `get_session()`: retornar sessão para inserir dados

---

### **ARQUIVO 4: src/extract.py**

**O que fazer:**
- Ler o CSV usando PySpark
- Retornar DataFrame

**Função extract_data(file_path):**
1. Criar SparkSession
2. Definir schema explícito (StructType com todos os campos)
3. Ler CSV com o schema
4. Retornar DataFrame

**Dica:** Use `spark.read.option("header", "true").schema(schema).csv(path)`

---

### **ARQUIVO 5: src/transform.py**

**O que fazer:**
- Limpar e transformar os dados
- Criar novas colunas

**Função transform_data(df):**

1. **Limpeza:**
   - Remover duplicatas
   - Filtrar salários fora do range válido

2. **Criar novas colunas:**
   
   **salary_category:**
   - < 100k = "Low"
   - 100-150k = "Medium"  
   - 150-200k = "High"
   - > 200k = "Very High"
   
   **experience_level:**
   - 0-2 anos = "Junior"
   - 3-6 anos = "Mid"
   - 7-14 anos = "Senior"
   - 15+ anos = "Expert"

3. Retornar DataFrame transformado

**Dica:** Use `F.when().otherwise()` para criar as categorias

---

### **ARQUIVO 6: src/load.py**

**O que fazer:**
- Validar dados com Pydantic
- Salvar no banco SQLite

**Função load_data(df, session):**

1. **Validação:**
   - Converter Spark DataFrame para pandas: `df.toPandas()`
   - Para cada linha, validar com modelo Pydantic
   - Separar registros válidos e inválidos

2. **Inserção no banco:**
   - Converter registros válidos para dicts
   - Usar `session.bulk_insert_mappings(Model, dicts)`
   - Fazer commit

3. Retornar contadores: total, válidos, inválidos

---

### **ARQUIVO 7: main.py**

**O que fazer:**
- Executar o pipeline completo

**Função main():**
```python
1. Inicializar banco (criar tabelas se não existirem)
2. EXTRACT: ler CSV
3. TRANSFORM: limpar e transformar
4. LOAD: validar e salvar no banco
5. Imprimir estatísticas:
   - Total de registros processados
   - Registros inseridos
   - Registros inválidos
   - Tempo de execução
```

---

## 🎯 FUNCIONALIDADES EXTRAS (OPCIONAL)

### 1. Agregações

Criar arquivo `src/analytics.py` com função que calcula:
- Salário médio por indústria
- Salário médio por nível de educação
- Salário médio por cargo
- Quantidade de jobs por localização

**Use PySpark:**
```python
df.groupBy("industry").agg(
    F.count("*").alias("total_jobs"),
    F.avg("salary").alias("avg_salary"),
    F.min("salary").alias("min_salary"),
    F.max("salary").alias("max_salary")
)
```

### 2. Salvar dados processados

Salvar DataFrame transformado em:
- Parquet: `df.write.parquet("data/processed/jobs.parquet")`
- CSV: `df.coalesce(1).write.csv("data/processed/jobs.csv", header=True)`

---

## 🚀 COMO EXECUTAR

```bash
# 1. Copiar CSV para data/raw/
cp job_salary_dataset.csv data/raw/

# 2. Executar pipeline
python main.py

# 3. Verificar banco de dados
sqlite3 salary_data.db "SELECT COUNT(*) FROM jobs;"
sqlite3 salary_data.db "SELECT industry, AVG(salary) FROM jobs GROUP BY industry;"
```

---

## 📊 VALIDAÇÕES QUE VOCÊ DEVE IMPLEMENTAR

### No Pydantic (models.py):

1. **experience_years:** entre 0 e 50
2. **salary:** entre MIN_SALARY e MAX_SALARY (do .env)
3. **education_level:** apenas valores válidos
4. **remote_work:** apenas Yes, No, Hybrid
5. **company_size:** apenas tamanhos válidos
6. **skills_count e certifications:** >= 0

### No PySpark (transform.py):

1. Remover duplicatas
2. Filtrar salários negativos ou muito altos
3. Remover registros com campos obrigatórios vazios

---

## 🧪 TESTANDO

### Teste 1: Validação Pydantic
```python
# Criar teste rápido no models.py
if __name__ == "__main__":
    # Teste com dados válidos
    valid_data = {
        "job_title": "Data Engineer",
        "experience_years": 5,
        "education_level": "Bachelor",
        "skills_count": 10,
        "industry": "Technology",
        "company_size": "Medium",
        "location": "USA",
        "remote_work": "Yes",
        "certifications": 2,
        "salary": 120000
    }
    job = JobData(**valid_data)
    print("✓ Dados válidos OK")
    
    # Teste com dados inválidos
    try:
        invalid_data = valid_data.copy()
        invalid_data["salary"] = -1000  # Inválido
        job = JobData(**invalid_data)
    except ValidationError as e:
        print("✓ Validação de salary inválido OK")
```

### Teste 2: Pipeline Completo
```bash
python main.py

# Deve ver output como:
# ========================================
# Pipeline ETL Iniciado
# ========================================
# [EXTRACT] Lendo dados...
# [EXTRACT] 50000 registros extraídos
# [TRANSFORM] Aplicando transformações...
# [TRANSFORM] 49500 registros após limpeza
# [LOAD] Validando dados...
# [LOAD] 49200 registros válidos
# [LOAD] 300 registros inválidos
# [LOAD] Inserindo no banco...
# [LOAD] 49200 registros inseridos
# ========================================
# Pipeline concluído em 45.2 segundos
# ========================================
```

---

## 💡 DICAS DE IMPLEMENTAÇÃO

### PySpark:
- Sempre defina schema explícito (mais rápido)
- Use `.cache()` se for reusar o DataFrame
- Minimize uso de `.collect()` (traz tudo pra memória)

### Pydantic:
- Use `Field()` para validações simples
- Use `@field_validator` para validações complexas
- Sempre trate `ValidationError` ao validar dados externos

### SQLAlchemy:
- Use `bulk_insert_mappings()` para inserir muitos registros
- Sempre faça `commit()` após inserções
- Use `session.rollback()` em caso de erro

### Performance:
- Valide em batches (ex: 1000 registros por vez)
- Use pandas como ponte entre Spark e SQLAlchemy
- Configure Spark com memória adequada: `.config("spark.driver.memory", "2g")`

---

## 📋 CHECKLIST

- [ ] Ambiente virtual criado e dependências instaladas
- [ ] Estrutura de pastas criada
- [ ] Arquivo .env configurado
- [ ] config.py implementado
- [ ] models.py com validações Pydantic
- [ ] database.py com modelo SQLAlchemy
- [ ] extract.py lendo CSV com PySpark
- [ ] transform.py com limpeza e feature engineering
- [ ] load.py validando e salvando no banco
- [ ] main.py executando pipeline completo
- [ ] Pipeline executa sem erros
- [ ] Dados aparecem no banco SQLite
- [ ] Agregações básicas funcionando (opcional)

---

## 🎓 O QUE VOCÊ VAI APRENDER

**PySpark:**
- Criar SparkSession
- Definir schemas
- Ler CSV
- Transformações: select, filter, withColumn
- Funções: when, col, current_timestamp
- GroupBy e agregações

**Pydantic:**
- BaseModel e BaseSettings
- Field com validações (ge, le, gt)
- Validators customizados
- ValidationError handling
- Conversão de tipos automática

**SQLAlchemy:**
- Declarative Base
- Column types (Integer, String, Float, DateTime)
- Primary keys e autoincrement
- create_engine e create_all
- Session e commits
- bulk_insert_mappings

**Integração:**
- Spark → Pandas → Pydantic → SQLAlchemy
- Pipeline ETL end-to-end
- Tratamento de erros
- Validação de dados em múltiplas camadas

---

Simples e direto! É assim que um Data Engineer faz ETL no dia a dia. 🚀
