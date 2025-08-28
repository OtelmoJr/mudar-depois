
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

## Próximos passos
- Configurar o ambiente Kubernetes e deploy de MinIO/Airflow.
- Versionar tudo no Git desde o início.

---
> Siga as boas práticas: modularização, testes, logging, segurança, versionamento e documentação incremental.
