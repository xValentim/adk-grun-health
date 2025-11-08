# Dockerfile para ADK API Server
FROM python:3.10-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do agente
COPY team/ ./agent/

# Definir variáveis de ambiente
ENV PYTHONPATH=/app/agent
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

# Expor a porta do ADK
EXPOSE 8000

# Comando para iniciar o ADK API Server
WORKDIR /app/agent
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8000"]
