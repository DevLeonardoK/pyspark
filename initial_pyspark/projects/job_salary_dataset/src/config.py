#Pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

#Pydantic
from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import SecretStr, Field

#Spark create
spark = SparkSession.builder.master("local[*]").appName("spark_project_job_salary").getOrCreate()

#Environments
class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    database_url : SecretStr = Field(..., alias="DATABASE_ADDRESS")
    database_username : SecretStr = Field(..., alias="DATABASE_USER")
    database_password : SecretStr = Field(..., alias="DATABASE_PASSWORD")
    database_name : SecretStr = Field(..., alias="DATABASE_NAME")
    

env_vars = Environment()
