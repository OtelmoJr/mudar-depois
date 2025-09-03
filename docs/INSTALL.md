# Data Lake Moderno - Guia de Instalação

## 📋 Pré-requisitos do Sistema

### Sistema Operacional
- Linux (recomendado): Ubuntu 20.04+ ou CentOS 7+
- macOS: 12.0+
- Windows: 10+ com WSL2

### Python
- Python 3.9+ (recomendado: 3.11)
- pip 21.0+

### Java (para PySpark)
- OpenJDK 11 ou 17

### Docker (opcional, para desenvolvimento local)
- Docker 20.10+
- Docker Compose 2.0+

## 🛠️ Instalação das Dependências

### 1. Python e pip
```bash
# Verificar versão
python3 --version
pip3 --version

# Atualizar pip
pip3 install --upgrade pip
```

### 2. Java (necessário para PySpark)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk

# CentOS/RHEL
sudo yum install java-11-openjdk

# macOS
brew install openjdk@11

# Verificar
java -version
```

### 3. Instalar dependências Python
```bash
# No diretório do projeto
cd /path/to/mudar-depois

# Instalar todas as dependências
pip3 install -r requirements.txt

# Ou instalar apenas essenciais para desenvolvimento
pip3 install requests boto3 pyspark
```

## 🏗️ Serviços Externos Necessários

### Para Desenvolvimento Local
```bash
# Instalar MinIO local
docker run -p 9000:9000 -p 9090:9090 \
  -e "MINIO_ACCESS_KEY=datalakeuser" \
  -e "MINIO_SECRET_KEY=datalakepassword" \
  minio/minio server /data

# Instalar Airflow local (simplificado)
pip3 install apache-airflow
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

### Para Produção (Kubernetes)
- Cluster Kubernetes (minikube, kind, ou cloud)
- Helm 3.0+
- kubectl configurado

## 🔧 Configuração do Ambiente

### 1. Variáveis de Ambiente
```bash
# Arquivo .env (criar na raiz do projeto)
API_URL=https://catfact.ninja/facts?limit=10
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=datalakeuser
MINIO_SECRET_KEY=datalakepassword
MINIO_BUCKET=bronze-landing
```

### 2. Configurar PySpark
```bash
# Variáveis de ambiente para PySpark
export SPARK_HOME=/path/to/spark
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=python3
```

### 3. Configurar Airflow (se usar localmente)
```bash
# Inicializar banco de dados
airflow db init

# Criar usuário admin
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Configurar dags_folder
export AIRFLOW__CORE__DAGS_FOLDER=/path/to/mudar-depois/dags
```

## 🚀 Como Executar

### Teste Local (sem cluster)
```bash
# 1. Iniciar MinIO
docker run -d -p 9000:9000 minio/minio server /data

# 2. Executar pipeline Bronze
cd pipelines
python3 bronze_ingestion.py

# 3. Executar transformação Silver
python3 -c "from dags.catfacts_silver_transformation_dag import *"
```

### Com Airflow Local
```bash
# Iniciar scheduler
airflow scheduler &

# Iniciar webserver
airflow webserver --port 8080

# Acessar http://localhost:8080
# Usuário: admin / Senha: admin
```

### Produção (Kubernetes)
```bash
# 1. Aplicar infraestrutura
cd infra
./deploy.sh

# 2. Copiar DAGs para Airflow
kubectl cp dags/ data-lake/airflow-webserver-xxx:/opt/airflow/dags/

# 3. Acessar Airflow UI
kubectl port-forward svc/airflow-webserver-service 8080:8080 -n data-lake
```

## 🔍 Verificação da Instalação

### Teste Básico
```bash
# Verificar Python
python3 -c "import requests, boto3, pyspark; print('✅ Dependências OK')"

# Testar API
python3 -c "import requests; print(requests.get('https://catfact.ninja/facts?limit=1').json())"
```

### Teste Completo
```bash
# Executar testes
pytest tests/

# Executar pipeline de exemplo
./pipelines/test_bronze_ingestion.sh
```

## 🐛 Troubleshooting

### Problema: "ModuleNotFoundError"
```bash
# Reinstalar dependências
pip3 uninstall -r requirements.txt
pip3 install -r requirements.txt
```

### Problema: PySpark não encontra Java
```bash
# Configurar JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### Problema: Airflow não inicia
```bash
# Limpar banco e reinicializar
rm airflow.db
airflow db init
```

## 📚 Recursos Adicionais

- [Documentação PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Documentação Airflow](https://airflow.apache.org/docs/)
- [Documentação MinIO](https://docs.min.io/)
- [Guia Kubernetes](https://kubernetes.io/docs/)

---

> Este guia cobre tanto desenvolvimento local quanto produção em Kubernetes.
