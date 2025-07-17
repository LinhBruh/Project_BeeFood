from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    "owner" : "airflow",
    "start_date": datetime(2025,7,16),
    "retries" : 2
}

with DAG(
    dag_id='befood_crawl_to_postgres',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Crawl -> Mongo -> Spark -> Postgres',
) as dag:
    crawl_task = BashOperator(
        task_id = "crawl_task",
        bash_command = "cd /opt/airflow && python -m crawl_data.crawl"
    )

    etl_task = SparkSubmitOperator(
        task_id = "etl_task",
        application = "/opt/airflow/spark_jobs/load.py",
        conn_id = "spark_default",
        verbose = False,
        conf = {
            "spark.master": "spark://spark-master:7077",
        }
    )


    crawl_task >> etl_task