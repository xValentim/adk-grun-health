# Docker - ADK + MCP Servers

Este projeto contém dois serviços containerizados:
1. **ADK API Server** - Servidor FastAPI do Lead Qualification Agent
2. **MCP Server** - Servidor Model Context Protocol

## 🚀 Início Rápido

### 1. Configurar variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env e adicione sua GOOGLE_API_KEY
```

### 2. Build das imagens (primeira vez)

```bash
# Construir as imagens Docker
docker-compose build

# Ou usar o script helper:
# Windows PowerShell:
.\docker.ps1 build

# Linux/Mac:
./docker.sh build
```

### 3. Subir os containers

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ou usar o script helper:
# Windows PowerShell:
.\docker.ps1 start

# Linux/Mac:
./docker.sh start
```

### 4. Ver logs e testar

```bash
# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f adk-api
docker-compose logs -f mcp-server

# Testar se está funcionando
.\docker.ps1 test
```

### 3. Testar os serviços

**ADK API Server:**
```bash
# Listar agentes disponíveis
curl http://localhost:8000/list-apps

# Documentação da API
# Abra no navegador: http://localhost:8000/docs
```

**MCP Server:**
```bash
# Testar endpoint
curl http://localhost:8001/mcp
```

## 📦 Serviços

### ADK API Server
- **Porta:** 8000
- **Endpoint:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Agente:** lead_qualification_agent

### MCP Server
- **Porta:** 8001
- **Endpoint:** http://localhost:8001/mcp
- **Tools disponíveis:**
  - `add(a, b)` - Soma dois números
  - `pizza_salami_price()` - Retorna preço da pizza
  - `current_year()` - Retorna ano atual
  - `greet(name)` - Saúda uma pessoa

## 🛠️ Comandos Úteis

```bash
# Parar os containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuild dos containers
docker-compose up -d --build

# Ver status dos containers
docker-compose ps

# Entrar no container ADK
docker-compose exec adk-api bash

# Entrar no container MCP
docker-compose exec mcp-server bash

# Reiniciar um serviço específico
docker-compose restart adk-api
docker-compose restart mcp-server
```

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yml          # Orquestração dos containers
├── Dockerfile.adk              # Dockerfile do ADK API Server
├── Dockerfile.mcp              # Dockerfile do MCP Server
├── requirements.txt            # Dependências Python compartilhadas
├── .env                        # Variáveis de ambiente (não commitar!)
├── .env.example                # Exemplo de variáveis de ambiente
├── 10-sequential-agent/        # Código do agente ADK
│   └── lead_qualification_agent/
└── mcp-server/                 # Código do MCP Server
    └── server.py
```

## 🔧 Desenvolvimento

### Atualizar código

Os volumes estão mapeados, então mudanças no código local são refletidas nos containers:
- `./10-sequential-agent` → `/app/agent` (ADK)
- `./mcp-server` → `/app` (MCP)

Após mudanças, reinicie o serviço:
```bash
docker-compose restart adk-api
# ou
docker-compose restart mcp-server
```

### Adicionar dependências

1. Adicione a dependência em `requirements.txt`
2. Rebuild o container:
```bash
docker-compose up -d --build
```

## 🌐 Rede

Os containers estão na mesma rede (`app-network`), permitindo comunicação entre eles:
- ADK pode acessar MCP via: `http://mcp-server:8001`
- MCP pode acessar ADK via: `http://adk-api:8000`

## 📊 Monitoramento

```bash
# Ver uso de recursos
docker stats

# Ver logs em tempo real
docker-compose logs -f --tail=100

# Ver apenas erros
docker-compose logs | grep -i error
```

## ❓ Troubleshooting

### Porta já em uso
```bash
# Encontrar processo usando a porta
# Windows PowerShell:
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Container não inicia
```bash
# Ver logs detalhados
docker-compose logs adk-api
docker-compose logs mcp-server

# Reconstruir do zero
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Variável de ambiente não funciona
- Verifique se o arquivo `.env` existe
- Verifique se `GOOGLE_API_KEY` está definida
- Reinicie os containers após editar `.env`

---

**🎯 Pronto!** Seus serviços ADK e MCP estão rodando em containers Docker.
