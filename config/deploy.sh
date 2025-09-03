#!/bin/bash
# Script para deploy da infraestrutura no Kubernetes

set -e  # Para no primeiro erro

echo "Aplicando namespace..."
kubectl apply -f infra/namespace.yaml

echo "Aplicando ConfigMaps..."
kubectl apply -f infra/minio-configmap.yaml
kubectl apply -f infra/airflow-configmap.yaml

echo "Aplicando Secrets..."
kubectl apply -f infra/secrets.yaml

echo "Aplicando Postgres..."
kubectl apply -f infra/postgres-deployment.yaml

echo "Aplicando MinIO..."
kubectl apply -f infra/minio-deployment.yaml

echo "Aplicando Airflow..."
kubectl apply -f infra/airflow-deployment.yaml

echo "Aguardando pods ficarem prontos..."
kubectl wait --for=condition=ready pod -l app=minio -n data-lake --timeout=300s
kubectl wait --for=condition=ready pod -l app=postgres -n data-lake --timeout=300s
kubectl wait --for=condition=ready pod -l app=airflow-webserver -n data-lake --timeout=300s
kubectl wait --for=condition=ready pod -l app=airflow-scheduler -n data-lake --timeout=300s

echo "Deploy concluído! Verifique os serviços:"
kubectl get pods -n data-lake
kubectl get services -n data-lake
