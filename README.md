
# Projeto Data Lake Moderno: Bronze → Silver → Gold

> Estrutura inicial do projeto para ingestão, processamento e disponibilização de dados em ambiente Kubernetes, com Spark, MinIO, Airflow e GitOps.

## Estrutura de diretórios
```
.
├── README.md
├── infra/           # Infraestrutura (K8s, MinIO, Airflow, configs)
├── pipelines/       # Pipelines ETL/ELT (Spark, scripts)
├── dags/            # DAGs do Airflow
├── data/            # Dados brutos e processados (Bronze/Silver/Gold)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── tests/           # Testes automatizados
├── docs/            # Documentação adicional
└── .gitignore
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

### Próximos passos
- Criar pipeline de ingestão (camada Bronze).
- Adicionar volumes persistentes reais (PVCs) para produção.

---
> Revisar e aprovar antes de prosseguir para Etapa 3.
