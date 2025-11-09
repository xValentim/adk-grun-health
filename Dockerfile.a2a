FROM python:3.10-slim

# System deps mínimos
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas os reqs do serviço A2A
COPY requirements_a2a.txt .

RUN pip install --no-cache-dir -r requirements_a2a.txt

# Copia os agents
COPY compliance_agents ./compliance_agents

EXPOSE 8003

# Sobe o api_server do ADK apontando pros agents
CMD ["adk", "api_server", "--a2a", "--host", "0.0.0.0", "--port", "8003", "compliance_agents"]
