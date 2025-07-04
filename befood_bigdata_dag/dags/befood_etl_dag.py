from airflow import DAG
from airflow.operators.python import PythonOperator  # ✅ Sửa dòng này
from datetime import datetime, timedelta
import logging
import pandas as pd
from pymongo import MongoClient
import psycopg2
import subprocess
import os

default_args = {
    'owner': 'befood',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def extract_mongo():
    logging.info("🟡 Connecting to MongoDB...")
    client = MongoClient('mongo', 27017)
    db = client['befood_db']
    collection = db['dishes']
    data = list(collection.find())
    if not data:
        logging.warning("⚠️ No data found in MongoDB!")
        return
    df = pd.DataFrame(data)
    df.drop(columns=['_id'], inplace=True, errors='ignore')
    os.makedirs('/opt/airflow/tmp', exist_ok=True)
    df.to_csv('/opt/airflow/tmp/mongo_data.csv', index=False)
    logging.info("✅ Data exported to CSV!")

def load_to_postgres():
    logging.info("🟡 Loading CSV into PostgreSQL...")
    csv_path = '/opt/airflow/tmp/mongo_data.csv'
    if not os.path.exists(csv_path):
        logging.error(f"❌ CSV file not found: {csv_path}")
        return
    conn = psycopg2.connect(
        host='postgres',
        dbname='befood_db',
        user='befood',
        password='befood123'
    )
    cursor = conn.cursor()
    df = pd.read_csv(csv_path)
    cursor.execute("DROP TABLE IF EXISTS dishes;")
    cursor.execute("""
        CREATE TABLE dishes (
            name TEXT,
            category TEXT,
            price FLOAT
        );
    """)
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO dishes (name, category, price) VALUES (%s, %s, %s);",
                       (row['name'], row['category'], row['price']))
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("✅ Data loaded into PostgreSQL!")

def run_spark_job():
    logging.info("🟡 Running Spark job...")
    cmd = [
        '/opt/bitnami/spark/bin/spark-submit',
        '--master', 'spark://spark-master:7077',
        '/opt/airflow/scripts/spark_job.py'
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    logging.info("Spark STDOUT:\n" + result.stdout)
    if result.stderr:
        logging.error("Spark STDERR:\n" + result.stderr)

with DAG(
    dag_id='befood_etl_spark_dag',
    default_args=default_args,
    description='MongoDB → Postgres → Spark DAG for BeFood',
    schedule_interval='@daily',
    start_date=datetime(2025, 7, 4),
    catchup=False,
) as dag:
    extract_task = PythonOperator(
        task_id='extract_from_mongo',
        python_callable=extract_mongo
    )

    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    spark_task = PythonOperator(
        task_id='run_spark_job',
        python_callable=run_spark_job
    )

    extract_task >> load_task >> spark_task
