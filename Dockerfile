# Dockerfile para FastAPI Health Analysis Server
FROM python:3.10-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements da raiz e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da API
COPY api-server/main.py .

# Definir variáveis de ambiente
ENV ADK_API_URL=${ADK_API_URL}
ENV PYTHONPATH=/app

# Expor a porta da FastAPI
EXPOSE 8002

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]