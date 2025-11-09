# Dockerfile for MCP Server
FROM python:3.10-slim

# Instalar dependências do sistema se necessário
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server code
COPY mcp-server/ .

# Definir variáveis de ambiente
ENV ADK_API_URL=${ADK_API_URL}
ENV PYTHONPATH=/app

# Expor a porta do MCP
EXPOSE 8001

# Comando para iniciar o MCP Server
CMD ["python", "server.py"]
