from pyspark.sql import SparkSession
from extract import extract_data
from transform import transform_data

spark = SparkSession.builder.appName("Load_data")\
        .master("spark://spark-master:7077")\
        .config("spark.sql.warehouse.dir", "/tmp/spark-artifacts") \
        .config("spark.sql.artifacts.dir", "/tmp/spark-artifacts") \
        .config("spark.local.dir", "/tmp/spark-artifacts") \
        .config("spark.jars","/opt/spark/jars/postgresql-42.7.1.jar")\
        .getOrCreate()

def load_data(restaurant_data, categories_data, item_data, customize_item_data, customize_option_data,data_fact):

    jdbc_url = "jdbc:postgresql://postgres:5432/befood_db"
    properties = {
        "user":"befood",
        "password":"befood123",
        "driver": "org.postgresql.Driver"
    }
    
    restaurant_data.write.jdbc(url = jdbc_url, table = "dim_restaurants", mode = "append", properties = properties)
    categories_data.write.jdbc(url = jdbc_url, table = "dim_categories", mode = "append", properties = properties)
    item_data.write.jdbc(url = jdbc_url, table = "dim_items", mode = "append", properties = properties)
    customize_item_data.write.jdbc(url = jdbc_url, table = "dim_customize_groups", mode = "append", properties = properties)
    customize_option_data.write.jdbc(url = jdbc_url, table = "dim_customize_options", mode = "append", properties = properties)
    data_fact.write.jdbc(url = jdbc_url, table = "fact_menu_snapshot", mode = "append", properties = properties)

df = extract_data()

restaurant_data, categories_data, item_data, customize_item_data, customize_option_data,data_fact = transform_data(df)
load_data(restaurant_data, categories_data, item_data, customize_item_data, customize_option_data,data_fact)