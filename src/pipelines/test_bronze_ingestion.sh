#!/bin/bash
# Script para testar o pipeline de ingestão localmente (fora do Airflow)

# Configurar variáveis de ambiente
export API_URL="https://jsonplaceholder.typicode.com/users"
export MINIO_ENDPOINT="http://localhost:9000"  # Ajustar para seu setup local
export MINIO_ACCESS_KEY="datalakeuser"
export MINIO_SECRET_KEY="datalakepassword"
export MINIO_BUCKET="bronze-landing"

# Executar script
python3 pipelines/bronze_ingestion.py
