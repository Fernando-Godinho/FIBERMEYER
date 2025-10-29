# FIBERMEYER - Deploy Local com Docker
# =====================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FIBERMEYER - Deploy Local com Docker" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Docker está instalado
try {
    docker --version | Out-Null
    Write-Host "✅ Docker encontrado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não encontrado! Instale o Docker Desktop primeiro." -ForegroundColor Red
    Write-Host "Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# Parar containers existentes se houver
Write-Host "🛑 Parando containers existentes..." -ForegroundColor Yellow
docker-compose down 2>$null

Write-Host ""
Write-Host "🚀 Iniciando FIBERMEYER..." -ForegroundColor Blue
Write-Host ""

# Executar docker-compose
$result = docker-compose up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ FIBERMEYER publicado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Acesse o sistema em:" -ForegroundColor Cyan
    Write-Host "   http://localhost:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "👨‍💼 Admin Django:" -ForegroundColor Cyan
    Write-Host "   URL: http://localhost:8000/admin/" -ForegroundColor White
    Write-Host "   Usuario: admin" -ForegroundColor White
    Write-Host "   Senha: admin123" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Ver logs em tempo real:" -ForegroundColor Cyan
    Write-Host "   docker-compose logs -f" -ForegroundColor White
    Write-Host ""
    Write-Host "🛑 Para parar o sistema:" -ForegroundColor Cyan
    Write-Host "   docker-compose down" -ForegroundColor White
    Write-Host ""
    
    # Abrir automaticamente no navegador
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:8000"
} else {
    Write-Host ""
    Write-Host "❌ Erro ao iniciar o sistema!" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 Ver logs de erro:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs" -ForegroundColor White
    Write-Host ""
}

Read-Host "Pressione Enter para continuar"