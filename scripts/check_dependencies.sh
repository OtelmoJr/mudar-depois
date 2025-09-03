#!/bin/bash
# Script de verificação das dependências

echo "🔍 Verificando dependências do projeto Data Lake Moderno..."
echo ""

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
else
    echo "❌ Python3 não encontrado. Instale Python 3.9+"
    exit 1
fi

# Verificar pip
echo ""
echo "📦 Verificando pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✅ $PIP_VERSION encontrado"
else
    echo "❌ pip3 não encontrado"
    exit 1
fi

# Verificar Java
echo ""
echo "☕ Verificando Java..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1)
    echo "✅ $JAVA_VERSION encontrado"
else
    echo "❌ Java não encontrado. Instale OpenJDK 11+"
    exit 1
fi

# Verificar dependências Python críticas
echo ""
echo "🔧 Verificando dependências Python..."

PYTHON_PACKAGES=("requests" "boto3" "pyspark")
for package in "${PYTHON_PACKAGES[@]}"; do
    if python3 -c "import $package" &> /dev/null; then
        echo "✅ $package instalado"
    else
        echo "❌ $package não encontrado"
        MISSING_PACKAGES="$MISSING_PACKAGES $package"
    fi
done

# Verificar Docker (opcional)
echo ""
echo "🐳 Verificando Docker (opcional)..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "✅ $DOCKER_VERSION encontrado"
else
    echo "⚠️  Docker não encontrado (opcional para desenvolvimento local)"
fi

# Verificar kubectl (opcional)
echo ""
echo "☸️  Verificando kubectl (opcional)..."
if command -v kubectl &> /dev/null; then
    KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null)
    echo "✅ kubectl encontrado"
else
    echo "⚠️  kubectl não encontrado (necessário para Kubernetes)"
fi

# Resumo
echo ""
echo "📊 RESUMO DA VERIFICAÇÃO"
echo "========================"

if [ -z "$MISSING_PACKAGES" ]; then
    echo "✅ Todas as dependências essenciais estão instaladas!"
    echo ""
    echo "🚀 Próximos passos:"
    echo "1. Configure as variáveis de ambiente (.env)"
    echo "2. Inicie MinIO: docker run -p 9000:9000 minio/minio server /data"
    echo "3. Teste o pipeline: ./pipelines/test_bronze_ingestion.sh"
else
    echo "❌ Pacotes Python faltando:$MISSING_PACKAGES"
    echo ""
    echo "🔧 Para instalar:"
    echo "pip3 install -r requirements.txt"
fi

echo ""
echo "📖 Para instruções completas, consulte INSTALL.md"
