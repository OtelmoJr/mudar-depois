from datetime import datetime, timedelta
from airflow.decorators import dag, task
import sys
import os

# Adicionar caminho para pipelines
sys.path.append('/opt/airflow/dags/pipelines')

@dag(
    dag_id='catfacts_bronze_ingestion_dag',
    description='DAG para ingestão de fatos sobre gatos na camada Bronze usando TaskFlow API',
    schedule_interval='@daily',  # Cron expression mais legível
    start_date=datetime(2025, 9, 1),
    catchup=False,
    tags=['bronze', 'ingestion', 'catfacts', 'api'],
    default_args={
        'owner': 'data-lake',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 3,  # Aumentado para melhor resiliência
        'retry_delay': timedelta(minutes=5),
        'execution_timeout': timedelta(hours=1),  # Timeout para evitar execuções infinitas
    }
)
def catfacts_bronze_ingestion_dag():
    """
    DAG para ingestão de fatos sobre gatos na camada Bronze.

    Este DAG executa diariamente a extração de fatos da API CatFacts
    e salva na camada Bronze do data lake.

    Fluxo:
    1. Extrair dados da API
    2. Validar dados
    3. Salvar no MinIO
    """

    @task
    def extract_catfacts():
        """Extrai fatos sobre gatos da API."""
        from datetime import datetime
        print(f"[{datetime.now()}] 🚀 Iniciando extração de dados da API CatFacts...")
        
        from bronze_ingestion import extract_from_api, API_URL
        try:
            data = extract_from_api(API_URL)
            print(f"[{datetime.now()}] ✅ Extraídos {len(data)} fatos sobre gatos da API")
            return data
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Erro na extração: {e}")
            raise

    @task
    def validate_data(data):
        """Valida os dados extraídos."""
        from datetime import datetime
        print(f"[{datetime.now()}] 🔍 Iniciando validação dos dados...")
        
        if not data:
            raise ValueError("Nenhum dado foi extraído")
        
        # Validações básicas
        required_fields = ['fact', 'length']
        for item in data:
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Campo obrigatório '{field}' ausente")
        
        print(f"[{datetime.now()}] ✅ Dados validados: {len(data)} registros com campos obrigatórios")
        return data

    @task
    def save_to_bronze(validated_data):
        """Salva dados validados na camada Bronze."""
        from datetime import datetime
        print(f"[{datetime.now()}] 💾 Iniciando salvamento na camada Bronze...")
        
        from bronze_ingestion import save_to_minio
        import pyspark
        from pyspark.sql import SparkSession
        
        # Criar SparkSession temporária
        spark = SparkSession.builder \
            .appName("BronzeIngestion") \
            .getOrCreate()
        
        try:
            # Gerar caminho com data
            from datetime import datetime
            date_str = datetime.now().strftime('%Y-%m-%d')
            output_path = f"s3a://bronze-landing/catfacts_batch_{date_str}.json"
            
            save_to_minio(spark, validated_data, output_path)
            print(f"[{datetime.now()}] ✅ Dados salvos em: {output_path}")
            print(f"[{datetime.now()}] 📊 Total processado: {len(validated_data)} fatos sobre gatos")
        finally:
            spark.stop()
            print(f"[{datetime.now()}] 🔄 Spark session finalizada")

    # Definir fluxo de tarefas
    raw_data = extract_catfacts()
    validated_data = validate_data(raw_data)
    save_to_bronze(validated_data)

# Instanciar DAG
dag = catfacts_bronze_ingestion_dag()
