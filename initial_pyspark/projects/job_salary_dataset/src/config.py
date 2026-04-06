#Pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


#Spark create
spark = SparkSession.builder.master("local[*]").appName("spark_project_job_salary").getOrCreate()
