#!/bin/bash
# Script helper para gerenciar os containers Docker

case "$1" in
  setup)
    echo "🏗️  Setup completo - Build + Start"
    echo ""
    
    # Verificar se .env existe
    if [ ! -f .env ]; then
      echo "⚠️  Arquivo .env não encontrado!"
      if [ -f .env.example ]; then
        echo "Copiando .env.example para .env..."
        cp .env.example .env
        echo "✅ Arquivo .env criado!"
        echo ""
        echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua GOOGLE_API_KEY!"
        echo ""
        read -p "Pressione ENTER depois de configurar o .env..."
      else
        echo "❌ Arquivo .env.example não encontrado!"
        exit 1
      fi
    fi
    
    echo "1/2 - Fazendo build das imagens..."
    docker-compose build
    
    if [ $? -eq 0 ]; then
      echo "✅ Build completo!"
      echo ""
      echo "2/2 - Iniciando containers..."
      docker-compose up -d
      
      if [ $? -eq 0 ]; then
        echo "✅ Containers iniciados!"
        echo ""
        echo "📊 Status:"
        docker-compose ps
        echo ""
        echo "🌐 Serviços disponíveis:"
        echo "  - ADK API: http://localhost:8000"
        echo "  - ADK Docs: http://localhost:8000/docs"
        echo "  - MCP Server: http://localhost:8001/mcp"
        echo ""
        echo "💡 Use './docker.sh test' para testar os serviços"
      fi
    else
      echo "❌ Erro no build!"
    fi
    ;;
    
  build)
    echo "🏗️  Fazendo build das imagens..."
    docker-compose build
    if [ $? -eq 0 ]; then
      echo "✅ Build completo!"
    else
      echo "❌ Erro no build!"
    fi
    ;;
  
  start)
    echo "🚀 Iniciando containers..."
    docker-compose up -d
    if [ $? -eq 0 ]; then
      echo "✅ Containers iniciados!"
      echo ""
      echo "📊 Status:"
      docker-compose ps
      echo ""
      echo "🌐 Serviços disponíveis:"
      echo "  - ADK API: http://localhost:8000"
      echo "  - ADK Docs: http://localhost:8000/docs"
      echo "  - MCP Server: http://localhost:8001/mcp"
    else
      echo "❌ Erro ao iniciar! Você fez o build primeiro? Use './docker.sh build'"
    fi
    ;;
    
  stop)
    echo "⏹️  Parando containers..."
    docker-compose down
    echo "✅ Containers parados!"
    ;;
    
  restart)
    echo "🔄 Reiniciando containers..."
    docker-compose restart
    echo "✅ Containers reiniciados!"
    ;;
    
  logs)
    if [ -z "$2" ]; then
      docker-compose logs -f --tail=100
    else
      docker-compose logs -f --tail=100 "$2"
    fi
    ;;
    
  build)
    echo "🏗️  Fazendo build das imagens..."
    docker-compose build
    if [ $? -eq 0 ]; then
      echo "✅ Build completo!"
    else
      echo "❌ Erro no build!"
    fi
    ;;
    
  rebuild)
    echo "🏗️  Reconstruindo e iniciando..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    echo "✅ Containers reconstruídos e iniciados!"
    ;;
    
  status)
    echo "📊 Status dos containers:"
    docker-compose ps
    echo ""
    echo "💾 Uso de recursos:"
    docker stats --no-stream
    ;;
    
  test)
    echo "🧪 Testando serviços..."
    echo ""
    echo "Testing ADK API..."
    curl -s http://localhost:8000/list-apps | jq . || echo "❌ ADK API não disponível"
    echo ""
    echo "Testing MCP Server..."
    curl -s http://localhost:8001/mcp | head -n 5 || echo "❌ MCP Server não disponível"
    ;;
    
  clean)
    echo "🧹 Limpando containers, volumes e imagens..."
    docker-compose down -v
    docker system prune -f
    echo "✅ Limpeza completa!"
    ;;
    
  *)
    echo "🐳 Docker Helper - ADK + MCP Servers"
    echo ""
    echo "Uso: ./docker.sh [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  setup     - Setup completo (build + start) - USE NA PRIMEIRA VEZ"
    echo "  build     - Faz build das imagens Docker"
    echo "  start     - Inicia os containers"
    echo "  stop      - Para os containers"
    echo "  restart   - Reinicia os containers"
    echo "  logs      - Mostra logs (use 'logs adk-api' ou 'logs mcp-server')"
    echo "  rebuild   - Para, reconstrói e inicia"
    echo "  status    - Mostra status e uso de recursos"
    echo "  test      - Testa se os serviços estão respondendo"
    echo "  clean     - Remove containers, volumes e limpa sistema"
    echo ""
    echo "Exemplos:"
    echo "  ./docker.sh setup           # Primeira vez"
    echo "  ./docker.sh build           # Build das imagens"
    echo "  ./docker.sh start           # Iniciar containers"
    echo "  ./docker.sh logs adk-api    # Ver logs do ADK"
    echo "  ./docker.sh test            # Testar serviços"
    ;;
esac
