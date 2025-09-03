
# Projeto Data Lake Moderno: Bronze → Silver → Gold

> Estrutura inicial do projeto para ingestão, processamento e disponibilização de dados em ambiente Kubernetes, com Spark, MinIO, Airflow e GitOps.

## 📁 Estrutura Organizada

```
mudar-depois/
├── src/                          # Código fonte
│   ├── core/                     # Scripts principais
│   │   └── bronze_ingestion.py   # Pipeline Bronze
│   ├── pipelines/                # Scripts de processamento
│   │   ├── test_bronze_ingestion.sh
│   │   ├── test_local_ingestion.py
│   │   └── test_silver_transformation.sh
│   └── dags/                     # DAGs do Airflow
│       ├── bronze_ingestion_dag.py
│       └── catfacts_silver_transformation_dag.py
├── config/                       # Configurações
│   ├── .env.example              # Exemplo de variáveis
│   ├── requirements.txt          # Dependências Python
│   └── infra/                    # Configurações K8s
│       ├── namespace.yaml
│       ├── minio-deployment.yaml
│       ├── airflow-deployment.yaml
│       ├── secrets.yaml
│       └── deploy.sh
├── data/                         # Dados (Bronze/Silver/Gold)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── scripts/                      # Scripts utilitários
│   └── check_dependencies.sh
├── docs/                         # Documentação
│   └── INSTALL.md
├── tests/                        # Testes
├── .gitignore
├── README.md
└── .venv/                        # Ambiente virtual (opcional)
```

## Descrição das pastas
- **infra/**: Arquivos de configuração e manifestos para infraestrutura (Kubernetes, MinIO, Airflow, etc).
- **pipelines/**: Scripts e notebooks de processamento de dados (ETL/ELT com Spark).
- **dags/**: DAGs do Airflow para orquestração dos pipelines.
- **data/**: Dados organizados nas camadas Bronze (ingestão), Silver (limpeza/transformação) e Gold (dados prontos para consumo).
- **tests/**: Testes unitários e de integração para garantir qualidade dos pipelines e infraestrutura.
- **docs/**: Documentação técnica, diagramas e exemplos de uso.
- **.gitignore**: Evita versionar dados sensíveis, arquivos temporários e ambientes locais.

## Como validar a estrutura
1. Verifique se todos os diretórios foram criados:
	```bash
	tree -L 2
	```
2. Confira se o `.gitignore` está presente e correto.
3. Leia este README para entender o propósito de cada pasta.

## Etapa 2: Ambiente Kubernetes + MinIO + Airflow

### O que foi implementado
- **Namespace**: `data-lake` para isolamento.
- **MinIO**: Object storage para camadas Bronze/Silver/Gold.
- **Airflow**: Orquestração de pipelines com Postgres como DB.
- **Secrets e ConfigMaps**: Para credenciais e configurações.
- **Resources**: Limits e requests para evitar conflitos de recursos.
- **Script de deploy**: Automatiza a aplicação no cluster.

### Boas práticas aplicadas
- Segurança: Credenciais em Secrets (base64 encoded).
- Escalabilidade: Replicas configuráveis, volumes persistentes simulados.
- Observabilidade: Logs via kubectl, health checks implícitos.
- GitOps-ready: Manifestos versionados para integração com ArgoCD/Flux.

### Como executar
1. Certifique-se de ter um cluster Kubernetes (minikube, kind ou cloud).
2. Execute o script de deploy:
   ```bash
   cd infra
   ./deploy.sh
   ```

### Como validar
1. Verifique os pods:
   ```bash
   kubectl get pods -n data-lake
   ```
   Deve mostrar: minio, postgres, airflow-webserver, airflow-scheduler (todos Running).

2. Verifique os serviços:
   ```bash
   kubectl get services -n data-lake
   ```
   MinIO: ClusterIP na porta 9000, Airflow: LoadBalancer na porta 8080.

3. Acesse Airflow (porta-forward se necessário):
   ```bash
   kubectl port-forward svc/airflow-webserver-service 8080:8080 -n data-lake
   ```
   Abra http://localhost:8080 (user: admin, pass: admin).

4. Teste MinIO (porta-forward):
   ```bash
   kubectl port-forward svc/minio-service 9000:9000 -n data-lake
   ```
   Abra http://localhost:9000 (use credenciais do ConfigMap).

## Etapa 3: Pipeline de Ingestão (Camada Bronze)

### O que foi implementado
- **Script PySpark**: `pipelines/bronze_ingestion.py` - Extrai dados de API (ex: JSONPlaceholder) e salva no MinIO.
- **DAG Airflow**: `dags/bronze_ingestion_dag.py` - Orquestra a execução diária.
- **Script de teste**: `pipelines/test_bronze_ingestion.sh` - Para testar localmente.

### Boas práticas aplicadas (Airflow 2.x)
- **TaskFlow API**: Uso de `@task` decorators para código mais limpo e legível
- **Dag Decorator**: DAG definida como função decorada com `@dag`
- **Tipagem e validação**: Validação de dados entre tarefas
- **XCom automático**: Passagem de dados entre tarefas via return
- **Tags**: Organização com tags ['bronze', 'ingestion', 'catfacts', 'api']
- **Execution timeout**: Timeout de 1 hora para evitar execuções infinitas
- **Retries aumentado**: 3 tentativas com delay de 5 minutos
- **Schedule moderno**: Uso de '@daily' ao invés de timedelta
- **Docstrings**: Documentação completa das funções e DAG

### Como executar
1. **Via Airflow (produção)**:
   - Copie o DAG para o pod do Airflow:
     ```bash
     kubectl cp dags/catfacts_bronze_ingestion_dag.py data-lake/airflow-webserver-xxx:/opt/airflow/dags/
     ```
   - Acesse Airflow UI e ative o DAG `catfacts_bronze_ingestion_dag`.

2. **Teste local (desenvolvimento)**:
   - Configure MinIO local (porta-forward):
     ```bash
     kubectl port-forward svc/minio-service 9000:9000 -n data-lake
     ```
   - Execute: `./pipelines/test_bronze_ingestion.sh`

### Como validar
1. Verifique logs no Airflow ou console.
2. Acesse MinIO UI (porta 9000) e confira o bucket `bronze-landing` com arquivo `catfacts_batch_YYYY-MM-DD.json`.
3. Conteúdo do arquivo deve ter dados JSON com campos como `fact`, `length`, etc., mais `ingestion_timestamp`.

### Observabilidade implementada
- **Logs por hora**: Cada tarefa imprime timestamp e status com emojis
- **Métricas**: Contagem de registros processados
- **Validação**: Verificação de campos obrigatórios
- **Estatísticas**: Distribuição por categoria na Silver

### Exemplo de output esperado
```
[2025-09-02 14:30:15] 🚀 Iniciando extração de dados da API CatFacts...
[2025-09-02 14:30:16] ✅ Extraídos 10 fatos sobre gatos da API
[2025-09-02 14:30:17] 🔍 Iniciando validação dos dados...
[2025-09-02 14:30:17] ✅ Dados validados: 10 registros com campos obrigatórios
[2025-09-02 14:30:18] 💾 Iniciando salvamento na camada Bronze...
[2025-09-02 14:30:20] ✅ Dados salvos em: s3a://bronze-landing/catfacts_batch_2025-09-02.json
[2025-09-02 14:30:20] 📊 Total processado: 10 fatos sobre gatos
```

### Próximos passos
- Executar DAGs no Airflow
- Criar pipeline de transformação Silver (já implementado em `dags/catfacts_silver_transformation_dag.py`)
- Adicionar testes automatizados
- Implementar observabilidade (logs, métricas, alertas)

---
> DAGs seguem as melhores práticas do Airflow 2.x: TaskFlow API, validação de dados, tipagem e documentação completa.

## 📋 Dependências Verificadas ✅

### Sistema
- ✅ **Python 3.12.3** - Linguagem principal
- ✅ **OpenJDK 11** - Necessário para PySpark
- ✅ **pip 24.0** - Gerenciador de pacotes
- ✅ **Docker** - Para serviços locais (MinIO, etc.)
- ✅ **kubectl** - Para Kubernetes (opcional)

### Python Packages
- ✅ **requests** - Para chamadas de API
- ✅ **boto3** - Para integração com MinIO/S3
- ✅ **pyspark** - Para processamento distribuído

### Arquivos de Configuração
- 📄 `config/requirements.txt` - Lista completa de dependências
- 📄 `docs/INSTALL.md` - Guia detalhado de instalação
- 📄 `config/.env.example` - Exemplo de variáveis de ambiente
- 🛠️ `scripts/check_dependencies.sh` - Script de verificação automática

### Como Usar
1. **Copie o arquivo de configuração:**
   ```bash
   cp config/.env.example .env
   ```

2. **Configure as variáveis no `.env`** conforme seu ambiente

3. **Execute a verificação:**
   ```bash
   ./scripts/check_dependencies.sh
   ```

### Próximos Passos
- Configurar MinIO local ou cluster Kubernetes
- Executar pipelines de teste
- Desenvolver camadas Silver e Gold
