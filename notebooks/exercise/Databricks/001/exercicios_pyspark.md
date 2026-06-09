# 🐍 Exercícios PySpark — Treino das Aulas 04, 05 e 06

> Temas abordados: `col`, `lit`, `when`, `groupBy`, `agg`, `dropna`, `fillna`, `isnull`, `trim`, `regexp_replace`

---

## Exercício 1 — Criando um DataFrame e adicionando coluna literal

Crie um DataFrame com as colunas `id`, `produto` e `preco` com os dados abaixo.  
Em seguida, adicione uma coluna chamada `"desconto"` com o valor literal `None` usando `lit()`.

```
Dados:
(1, "Notebook", 3500),
(2, "Mouse", 150),
(3, "Teclado", 250)
```

**O que praticar:** `spark.createDataFrame`, `withColumn`, `lit`

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import col, lit

data = [(1, "Notebook", 3500), (2, "Mouse", 150), (3, "Teclado", 250)]
schema = ["id", "produto", "preco"]

df = spark.createDataFrame(data, schema)
df = df.withColumn("desconto", lit(None))
display(df)
```
</details>

---

## Exercício 2 — Removendo linhas com valores nulos

Com o DataFrame abaixo, remova todas as linhas que possuem **qualquer** valor nulo.

```
Dados:
(1, "Ana", 25),
(2, None, 30),
(3, "Carlos", None),
(4, "João", 40)
```

**O que praticar:** `dropna()`

<details>
<summary>💡 Ver solução</summary>

```python
data = [(1, "Ana", 25), (2, None, 30), (3, "Carlos", None), (4, "João", 40)]
schema = ["id", "nome", "idade"]

df = spark.createDataFrame(data, schema)
df = df.dropna()
display(df)
```
</details>

---

## Exercício 3 — Preenchendo valores nulos com fillna

Use o DataFrame abaixo e preencha os valores `None` da coluna `"departamento"` com o texto `"Não informado"`.

```
Dados:
(1, "Ana", "TI"),
(2, "Bruno", None),
(3, "Carlos", None),
(4, "Diana", "RH")
```

**O que praticar:** `fillna(value, subset)`

<details>
<summary>💡 Ver solução</summary>

```python
data = [(1, "Ana", "TI"), (2, "Bruno", None), (3, "Carlos", None), (4, "Diana", "RH")]
schema = ["id", "nome", "departamento"]

df = spark.createDataFrame(data, schema)
df = df.fillna("Não informado", subset=["departamento"])
display(df)
```
</details>

---

## Exercício 4 — Criando categoria de salário com when

Crie um DataFrame com `nome`, `departamento` e `salario`.  
Adicione uma coluna `"faixa_salarial"` com as regras:
- Salário acima de 4000 → `"Alta"`
- Salário entre 2500 e 4000 → `"Média"`
- Abaixo de 2500 → `"Baixa"`

```
Dados:
("Ana", "TI", 5000),
("Bruno", "RH", 3000),
("Carlos", "Financeiro", 2000),
("Diana", "TI", 4500)
```

**O que praticar:** `when(...).when(...).otherwise(...)`

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import col, when

data = [("Ana", "TI", 5000), ("Bruno", "RH", 3000), ("Carlos", "Financeiro", 2000), ("Diana", "TI", 4500)]
schema = ["nome", "departamento", "salario"]

df = spark.createDataFrame(data, schema)
df = df.withColumn("faixa_salarial",
    when(col("salario") > 4000, "Alta")
    .when((col("salario") >= 2500) & (col("salario") <= 4000), "Média")
    .otherwise("Baixa")
)
display(df)
```
</details>

---

## Exercício 5 — Agrupando e calculando média por departamento

Usando o DataFrame do Exercício 4, calcule a **média salarial** por departamento e ordene do maior para o menor.

**O que praticar:** `groupBy`, `agg`, `avg`, `orderBy`

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import avg

resultado = df.groupBy(col("departamento")).agg(avg(col("salario")).alias("media_salario")).orderBy(col("media_salario"), ascending=False)
display(resultado)
```
</details>

---

## Exercício 6 — Preenchendo nulos com a média calculada

Crie o DataFrame abaixo e preencha os valores nulos da coluna `"salario"` com a **média dos salários existentes**.

```
Dados:
(1, "Ana", "TI", 3000),
(2, "Bruno", "RH", None),
(3, "Carlos", "Financeiro", 5000),
(4, "Diana", "TI", None),
(5, "Eduardo", "RH", 4000)
```

**O que praticar:** `agg`, `avg`, `collect()[0][0]`, `fillna`

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import col, avg

data = [(1, "Ana", "TI", 3000), (2, "Bruno", "RH", None), (3, "Carlos", "Financeiro", 5000), (4, "Diana", "TI", None), (5, "Eduardo", "RH", 4000)]
schema = ["id", "nome", "departamento", "salario"]

df = spark.createDataFrame(data, schema)

media = df.agg(avg(col("salario"))).collect()[0][0]

df = df.fillna(media, subset=["salario"])
display(df)
```
</details>

---

## Exercício 7 — Identificando nulos com isnull

Crie o DataFrame abaixo e adicione uma coluna booleana chamada `"cidade_nula"` que indica se a coluna `"cidade"` é nula.  
Em seguida, **filtre** apenas as linhas onde a cidade é nula.

```
Dados:
("Ricardo", 45, "Salvador"),
("Fernanda", 30, None),
("Gabriel", None, None),
("Leandro", 32, "Recife")
```

**O que praticar:** `isnull`, `withColumn`, `filter`

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import col, isnull

data = [("Ricardo", 45, "Salvador"), ("Fernanda", 30, None), ("Gabriel", None, None), ("Leandro", 32, "Recife")]
schema = ["nome", "idade", "cidade"]

df = spark.createDataFrame(data, schema)
df = df.withColumn("cidade_nula", isnull(col("cidade")))

df_filtrado = df.filter(col("cidade_nula") == True)
display(df_filtrado)
```
</details>

---

## Exercício 8 — Limpando espaços em branco com trim

Crie o DataFrame abaixo e use `trim()` para remover os espaços da coluna `"cidade"`.  
Depois, converta os valores que ficarem como string vazia `""` para `None`.

```
Dados:
("Ana", "       São Paulo      "),
("Bruno", "   Curitiba"),
("Carlos", ""),
("Diana", "    ")
```

**O que praticar:** `trim`, `when`, `lit(None)`

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import col, trim, when, lit

data = [("Ana", "       São Paulo      "), ("Bruno", "   Curitiba"), ("Carlos", ""), ("Diana", "    ")]
schema = ["nome", "cidade"]

df = spark.createDataFrame(data, schema)
df = df.withColumn("cidade", trim(col("cidade")))
df = df.withColumn("cidade", when(col("cidade") == "", lit(None)).otherwise(col("cidade")))
display(df)
```
</details>

---

## Exercício 9 — Limpando tabs com regexp_replace

Crie o DataFrame abaixo onde a coluna `"idade"` contém caracteres de tabulação (`\t`).  
Remova os tabs, converta strings vazias para `None`, faça o cast para `double` e preencha os nulos com a média arredondada.

```
Dados:
("João", "\t", "Salvador"),
("Pedro", "35\t", "Curitiba"),
("Lucas", "\t28", "Porto Alegre"),
("Julia", "40", "Florianópolis")
```

**O que praticar:** `regexp_replace`, `when`, `lit`, `cast`, `fillna`, `round`

<details>
<summary>💡 Ver solução</summary>

```python
import builtins
from pyspark.sql.functions import col, regexp_replace, when, lit, avg

data = [("João", "\t", "Salvador"), ("Pedro", "35\t", "Curitiba"), ("Lucas", "\t28", "Porto Alegre"), ("Julia", "40", "Florianópolis")]
schema = ["nome", "idade", "cidade"]

df = spark.createDataFrame(data, schema)

df = df.withColumn("idade", regexp_replace(col("idade"), r'\s+', ''))
df = df.withColumn("idade", when(col("idade") == "", lit(None)).otherwise(col("idade")))
df = df.withColumn("idade", col("idade").cast("double"))

media = df.agg(avg(col("idade"))).collect()[0][0]
df = df.fillna(builtins.round(media), subset=["idade"])
display(df)
```
</details>

---

## Exercício 10 — Desafio completo

Crie o DataFrame abaixo com problemas misturados: nulos, strings vazias e espaços.  
Aplique **todo o pipeline de limpeza**:

1. Converter strings vazias em `None` (colunas `"nome"` e `"salario"`)
2. Fazer `trim` na coluna `"nome"`
3. Fazer cast de `"salario"` para `double`
4. Preencher nulos de `"salario"` com a média
5. Preencher nulos de `"nome"` com `"Desconhecido"`
6. Remover linhas que ainda tiverem nulos

```
Dados:
(1, "  Ana  ", "TI", "3000"),
(2, "", "RH", "2500"),
(3, "Carlos", None, None),
(4, None, "Financeiro", "5000"),
(5, "João", "TI", "")
```

**O que praticar:** tudo que foi visto nas 3 aulas!

<details>
<summary>💡 Ver solução</summary>

```python
from pyspark.sql.functions import col, trim, when, lit, avg

data = [(1, "  Ana  ", "TI", "3000"), (2, "", "RH", "2500"), (3, "Carlos", None, None), (4, None, "Financeiro", "5000"), (5, "João", "TI", "")]
schema = ["id", "nome", "departamento", "salario"]

df = spark.createDataFrame(data, schema)

# 1. Strings vazias → None
df = df.withColumn("nome", when(col("nome") == "", lit(None)).otherwise(col("nome")))
df = df.withColumn("salario", when(col("salario") == "", lit(None)).otherwise(col("salario")))

# 2. Trim no nome
df = df.withColumn("nome", trim(col("nome")))

# 3. Cast salário para double
df = df.withColumn("salario", col("salario").cast("double"))

# 4. Preencher salário com a média
media = df.agg(avg(col("salario"))).collect()[0][0]
df = df.fillna(media, subset=["salario"])

# 5. Preencher nome com "Desconhecido"
df = df.fillna("Desconhecido", subset=["nome"])

# 6. Remover linhas com nulos restantes
df = df.dropna()

display(df)
```
</details>

---

## 📋 Resumo das funções praticadas

| Função | O que faz |
|---|---|
| `lit(valor)` | Cria uma coluna com valor constante/literal |
| `col("coluna")` | Referencia uma coluna do DataFrame |
| `when(cond, val).otherwise(val)` | Lógica condicional (if/else) |
| `groupBy().agg()` | Agrupa e agrega dados |
| `avg()` / `sum()` | Média / Soma em agregações |
| `dropna()` | Remove linhas com valores nulos |
| `fillna(valor, subset)` | Preenche nulos com valor definido |
| `isnull(col)` | Retorna True se o valor for nulo |
| `trim(col)` | Remove espaços no início e fim |
| `regexp_replace(col, padrão, novo)` | Substitui padrão regex por novo valor |
| `cast("tipo")` | Converte tipo da coluna |
| `collect()[0][0]` | Traz valor escalar para memória local |
