from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BeFood ETL").getOrCreate()

df = spark.read.csv("/opt/airflow/tmp/mongo_data.csv", header=True, inferSchema=True)
df.printSchema()
df.show(5)
df.groupBy("category").count().show()

spark.stop()
