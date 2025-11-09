# Health Analysis FastAPI Server

Uma API FastAPI para análise de prescrições médicas usando os agentes ADK.

## Funcionalidades

- **Análise Simples**: Avaliação de segurança geral de prescrições
- **Análise Paralela**: Avaliação especializada de medicamento, dose e rota
- **Análise Sequencial**: Análise abrangente de saúde com avaliação de impacto
- **Análise Completa**: Executa todas as análises em uma única requisição

## Endpoints Principais

### Health Check
- `GET /` - Status básico da API
- `GET /health` - Verificação detalhada de saúde
- `GET /agents` - Lista agentes disponíveis

### Análises
- `POST /analyze/simple` - Análise de segurança simples
- `POST /analyze/parallel` - Análise paralela especializada  
- `POST /analyze/sequential` - Análise sequencial abrangente
- `POST /analyze/all` - Todas as análises em uma requisição

## Formato de Requisição

```json
{
  "health_data": "dados do paciente e prescrição em formato texto"
}
```

## Formato de Resposta

```json
{
  "status": "success|error",
  "data": {
    "results_criticality": {
      "level": "low|medium|high",
      "description": "descrição da análise"
    }
  },
  "message": "mensagem de status"
}
```

## Instalação e Execução

1. Instalar dependências:
```bash
cd api-server
pip install -r requirements.txt
```

2. Configurar variável de ambiente (opcional):
```bash
export ADK_API_URL=http://localhost:8000
```

3. Executar o servidor:
```bash
python main.py
```

O servidor estará disponível em `http://localhost:8002`

## Documentação Interativa

Acesse `http://localhost:8002/docs` para documentação Swagger automática.

## Configuração

- **ADK_API_URL**: URL do servidor ADK (padrão: http://localhost:8000)
- **Porta**: 8002 (configurável no main.py)
- **CORS**: Configurado para aceitar todas as origens (ajustar para produção)

## Estrutura

- `main.py` - Aplicação FastAPI principal
- `requirements.txt` - Dependências Python
- `README.md` - Esta documentação
- `../Dockerfile.api` - Dockerfile na raiz do projeto

## Deploy com Docker

Para fazer build e executar com Docker (a partir da raiz do projeto):

```bash
# Build da imagem
docker build -f Dockerfile.api -t health-fastapi-server .

# Executar container
docker run -p 8002:8002 -e ADK_API_URL=http://localhost:8000 health-fastapi-server
```