# coding=utf-8
from etl_src.workers.Extract import ExtratJob
from etl_src.workers.Transfom import TransformJob
from etl_src.workers.Load import LoadJob
from importlib.resources import path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os


default_args = {
    "owner": "testde",
    "start_date": days_ago(1)
}

# Extract job 
def extract()-> None:
    ExtratJob().run_worker()

# Transform job
def transform() -> None:
    TransformJob().run_worker()

# Load job 
def load() -> None:
    LoadJob().run_worker()


# Defining the DAG using Context Manager
with DAG(
    dag_id="ETL pipeline",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    #schedule=None
) as dag:

    Extract = PythonOperator(
        task_id="Extract",
        python_callable=extract
    )

    Transform = PythonOperator(
        task_id="Transform",
        python_callable=transform
    )
    
    Load= PythonOperator(
        task_id="Load",
        python_callable=load
    )
    
    Extract >> Transform >> Load
