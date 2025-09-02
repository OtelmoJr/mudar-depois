from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Adicionar caminho para pipelines
sys.path.append('/opt/airflow/dags/pipelines')

default_args = {
    'owner': 'data-lake',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'bronze_ingestion_dag',
    default_args=default_args,
    description='DAG para ingestão de dados na camada Bronze',
    schedule_interval=timedelta(days=1),  # Executa diariamente
    catchup=False,
)

def run_bronze_ingestion():
    """Executa o script de ingestão."""
    from bronze_ingestion import main
    main()

ingestion_task = PythonOperator(
    task_id='extract_and_save_bronze',
    python_callable=run_bronze_ingestion,
    dag=dag,
)

# Para futuras expansões: adicionar tarefas de validação, limpeza, etc.
