#!/usr/bin/env python3
"""
Pipeline de Ingestão Bronze: Extração de dados de API e salvamento no MinIO.

Este script usa PySpark para extrair dados de uma API em batch e salvar na camada Bronze do MinIO.
Exemplo: API de usuários do JSONPlaceholder (dados simulados de clientes).

Boas práticas:
- Tratamento de erros e logging.
- Parametrização via variáveis de ambiente.
- Estrutura modular para reutilização.
"""

import os
import logging
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
import boto3
from botocore.exceptions import NoCredentialsError

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurações via variáveis de ambiente (para produção, use Secrets)
API_URL = os.getenv('API_URL', 'https://catfact.ninja/facts?limit=10')
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://minio-service.data-lake.svc.cluster.local:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'datalakeuser')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'datalakepassword')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'bronze-landing')
OUTPUT_PATH = f's3a://{MINIO_BUCKET}/users_batch_{{date}}.json'

def extract_from_api(url: str) -> list:
    """Extrai dados da API e retorna lista de dicionários."""
    try:
        logger.info(f"Extraindo dados da API: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # Normalizar dados da API
        if isinstance(data, dict) and 'data' in data:
            data = data['data']  # Para APIs como catfacts
    except requests.RequestException as e:
        logger.error(f"Erro ao extrair da API: {e}")
        raise

def save_to_minio(spark: SparkSession, data: list, output_path: str):
    """Salva dados no MinIO usando PySpark."""
    try:
        # Criar DataFrame do Spark
        df = spark.createDataFrame(data)
        df = df.withColumn('ingestion_timestamp', current_timestamp())

        # Configurar acesso ao MinIO
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", MINIO_ACCESS_KEY)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", MINIO_SECRET_KEY)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", MINIO_ENDPOINT)
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
        spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")

        # Salvar como JSON no MinIO
        df.write.mode('overwrite').json(output_path)
        logger.info(f"Dados salvos em: {output_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar no MinIO: {e}")
        raise

def create_minio_bucket_if_not_exists():
    """Cria bucket no MinIO se não existir."""
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY
        )
        if not s3.bucket_exists(MINIO_BUCKET):
            s3.create_bucket(Bucket=MINIO_BUCKET)
            logger.info(f"Bucket criado: {MINIO_BUCKET}")
    except NoCredentialsError:
        logger.error("Credenciais do MinIO inválidas")
        raise

def main():
    """Função principal do pipeline."""
    logger.info("Iniciando pipeline de ingestão Bronze")

    # Criar bucket se necessário
    create_minio_bucket_if_not_exists()

    # Inicializar Spark
    spark = SparkSession.builder \
        .appName("BronzeIngestion") \
        .getOrCreate()

    try:
        # Extrair dados
        data = extract_from_api(API_URL)

        # Gerar caminho com data (ex: users_batch_2025-09-02.json)
        from datetime import datetime
        date_str = datetime.now().strftime('%Y-%m-%d')
        output_path = OUTPUT_PATH.format(date=date_str)

        # Salvar no MinIO
        save_to_minio(spark, data, output_path)

        logger.info("Pipeline concluído com sucesso")
    except Exception as e:
        logger.error(f"Pipeline falhou: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
