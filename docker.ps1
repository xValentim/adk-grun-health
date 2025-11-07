# Script helper para gerenciar os containers Docker no Windows
param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$Service
)

function Show-Help {
    Write-Host "🐳 Docker Helper - ADK + MCP Servers" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\docker.ps1 [comando] [serviço]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Comandos disponíveis:" -ForegroundColor Green
    Write-Host "  setup     - Setup completo (build + start) - USE NA PRIMEIRA VEZ"
    Write-Host "  build     - Faz build das imagens Docker"
    Write-Host "  start     - Inicia os containers"
    Write-Host "  stop      - Para os containers"
    Write-Host "  restart   - Reinicia os containers"
    Write-Host "  logs      - Mostra logs (use 'logs adk-api' ou 'logs mcp-server')"
    Write-Host "  rebuild   - Para, reconstrói e inicia"
    Write-Host "  status    - Mostra status e uso de recursos"
    Write-Host "  test      - Testa se os serviços estão respondendo"
    Write-Host "  clean     - Remove containers, volumes e limpa sistema"
    Write-Host ""
    Write-Host "Exemplos:" -ForegroundColor Yellow
    Write-Host "  .\docker.ps1 setup          # Primeira vez"
    Write-Host "  .\docker.ps1 build          # Build das imagens"
    Write-Host "  .\docker.ps1 start          # Iniciar containers"
    Write-Host "  .\docker.ps1 logs adk-api   # Ver logs do ADK"
    Write-Host "  .\docker.ps1 test           # Testar serviços"
}

switch ($Command) {
    "setup" {
        Write-Host "🏗️  Setup completo - Build + Start" -ForegroundColor Cyan
        Write-Host ""
        
        # Verificar se .env existe
        if (-not (Test-Path ".env")) {
            Write-Host "⚠️  Arquivo .env não encontrado!" -ForegroundColor Yellow
            Write-Host ""
            if (Test-Path ".env.example") {
                Write-Host "Copiando .env.example para .env..." -ForegroundColor Yellow
                Copy-Item ".env.example" ".env"
                Write-Host "✅ Arquivo .env criado!" -ForegroundColor Green
                Write-Host ""
                Write-Host "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua GOOGLE_API_KEY!" -ForegroundColor Red
                Write-Host ""
                $response = Read-Host "Pressione ENTER depois de configurar o .env..."
            } else {
                Write-Host "❌ Arquivo .env.example não encontrado!" -ForegroundColor Red
                return
            }
        }
        
        Write-Host "1/2 - Fazendo build das imagens..." -ForegroundColor Cyan
        docker-compose build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Build completo!" -ForegroundColor Green
            Write-Host ""
            Write-Host "2/2 - Iniciando containers..." -ForegroundColor Cyan
            docker-compose up -d
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Containers iniciados!" -ForegroundColor Green
                Write-Host ""
                Write-Host "📊 Status:" -ForegroundColor Yellow
                docker-compose ps
                Write-Host ""
                Write-Host "🌐 Serviços disponíveis:" -ForegroundColor Cyan
                Write-Host "  - ADK API: http://localhost:8000"
                Write-Host "  - ADK Docs: http://localhost:8000/docs"
                Write-Host "  - MCP Server: http://localhost:8001/mcp"
                Write-Host ""
                Write-Host "💡 Use '.\docker.ps1 test' para testar os serviços" -ForegroundColor Yellow
            }
        } else {
            Write-Host "❌ Erro no build!" -ForegroundColor Red
        }
    }
    
    "build" {
        Write-Host "🏗️  Fazendo build das imagens..." -ForegroundColor Cyan
        docker-compose build
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Build completo!" -ForegroundColor Green
        } else {
            Write-Host "❌ Erro no build!" -ForegroundColor Red
        }
    }
    
    "start" {
        Write-Host "🚀 Iniciando containers..." -ForegroundColor Cyan
        docker-compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Containers iniciados!" -ForegroundColor Green
            Write-Host ""
            Write-Host "📊 Status:" -ForegroundColor Yellow
            docker-compose ps
            Write-Host ""
            Write-Host "🌐 Serviços disponíveis:" -ForegroundColor Cyan
            Write-Host "  - ADK API: http://localhost:8000"
            Write-Host "  - ADK Docs: http://localhost:8000/docs"
            Write-Host "  - MCP Server: http://localhost:8001/mcp"
        } else {
            Write-Host "❌ Erro ao iniciar! Você fez o build primeiro? Use '.\docker.ps1 build'" -ForegroundColor Red
        }
    }    "stop" {
        Write-Host "⏹️  Parando containers..." -ForegroundColor Cyan
        docker-compose down
        Write-Host "✅ Containers parados!" -ForegroundColor Green
    }
    
    "restart" {
        Write-Host "🔄 Reiniciando containers..." -ForegroundColor Cyan
        docker-compose restart
        Write-Host "✅ Containers reiniciados!" -ForegroundColor Green
    }
    
    "logs" {
        if ($Service) {
            docker-compose logs -f --tail=100 $Service
        } else {
            docker-compose logs -f --tail=100
        }
    }
    
    "build" {
        Write-Host "🏗️  Reconstruindo containers..." -ForegroundColor Cyan
        docker-compose build --no-cache
        Write-Host "✅ Build completo!" -ForegroundColor Green
    }
    
    "rebuild" {
        Write-Host "🏗️  Reconstruindo e iniciando..." -ForegroundColor Cyan
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        Write-Host "✅ Containers reconstruídos e iniciados!" -ForegroundColor Green
    }
    
    "status" {
        Write-Host "📊 Status dos containers:" -ForegroundColor Cyan
        docker-compose ps
        Write-Host ""
        Write-Host "💾 Uso de recursos:" -ForegroundColor Cyan
        docker stats --no-stream
    }
    
    "test" {
        Write-Host "🧪 Testando serviços..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Testing ADK API..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/list-apps" -UseBasicParsing
            $response.Content | ConvertFrom-Json | ConvertTo-Json
            Write-Host "✅ ADK API funcionando!" -ForegroundColor Green
        } catch {
            Write-Host "❌ ADK API não disponível" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "Testing MCP Server..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8001/mcp" -UseBasicParsing
            Write-Host "✅ MCP Server funcionando!" -ForegroundColor Green
        } catch {
            Write-Host "❌ MCP Server não disponível" -ForegroundColor Red
        }
    }
    
    "clean" {
        Write-Host "🧹 Limpando containers, volumes e imagens..." -ForegroundColor Cyan
        docker-compose down -v
        docker system prune -f
        Write-Host "✅ Limpeza completa!" -ForegroundColor Green
    }
    
    default {
        Show-Help
    }
}
