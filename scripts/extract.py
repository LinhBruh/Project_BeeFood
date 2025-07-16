from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Extract_Data")\
        .master("spark://spark-master:7077")\
        .config("spark.mongodb.read.connection.uri","mongodb://mongo:27017/data_raw_befood")\
        .config("spark.jars", ",".join([
        "/opt/spark/jars/mongo-spark-connector_2.12-10.4.1.jar",
        "/opt/spark/jars/mongodb-driver-sync-4.11.1.jar",
        "/opt/spark/jars/mongodb-driver-core-4.11.1.jar",
        "/opt/spark/jars/bson-4.11.1.jar",
        "/opt/spark/jars/postgresql-42.7.1.jar"]))\
        .config("spark.sql.warehouse.dir", "/tmp/spark-artifacts") \
        .config("spark.sql.artifacts.dir", "/tmp/spark-artifacts") \
        .config("spark.local.dir", "/tmp/spark-artifacts") \
        .getOrCreate()

def extract_data():
    df = spark.read.format("mongodb") \
        .option("collection","restaurants")\
        .load()
    
    return df





