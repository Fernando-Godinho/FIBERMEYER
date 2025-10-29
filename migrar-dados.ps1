# Script para migrar dados locais para VPS
Write-Host "🚀 Migrando banco SQLite local para VPS..." -ForegroundColor Green

# Verificar se o arquivo db.sqlite3 existe
if (Test-Path "db.sqlite3") {
    Write-Host "✅ Banco local encontrado: db.sqlite3" -ForegroundColor Green
    
    # Copiar banco para VPS
    Write-Host "📤 Copiando banco para VPS..." -ForegroundColor Yellow
    scp -o StrictHostKeyChecking=no db.sqlite3 root@69.62.89.102:/tmp/db.sqlite3
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Banco copiado com sucesso!" -ForegroundColor Green
        
        # Executar deploy com banco
        Write-Host "🚀 Executando deploy com dados..." -ForegroundColor Yellow
        ssh -o StrictHostKeyChecking=no root@69.62.89.102 @"
cd FIBERMEYER
# Parar containers atuais
docker compose -f docker-compose-direto.yml down 2>/dev/null || true

# Atualizar código
git pull

# Criar diretório para dados
mkdir -p /root/fibermeyer_data

# Copiar banco
cp /tmp/db.sqlite3 /root/fibermeyer_data/db.sqlite3

# Iniciar com SQLite persistente
docker compose -f docker-compose-sqlite.yml up -d

echo "✅ Deploy concluído!"
echo "🌐 Acesse: http://69.62.89.102:8000"
"@
    } else {
        Write-Host "❌ Erro ao copiar banco!" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Arquivo db.sqlite3 não encontrado!" -ForegroundColor Red
    Write-Host "Execute 'python manage.py migrate' primeiro" -ForegroundColor Yellow
}