#!/bin/bash

echo "🚀 Migrando dados locais para VPS..."

# Parar containers
echo "⏹️ Parando containers..."
docker compose -f docker-compose-sqlite.yml down 2>/dev/null || true

# Baixar código atualizado
echo "📦 Atualizando código..."
git pull

# Subir container com SQLite
echo "🐳 Iniciando container com SQLite..."
docker compose -f docker-compose-sqlite.yml up -d

# Aguardar container ficar pronto
echo "⏳ Aguardando container..."
sleep 15

# Verificar se está funcionando
echo "✅ Verificando aplicação..."
if curl -f -s http://localhost:8000 > /dev/null; then
    echo "✅ Aplicação rodando com sucesso!"
    echo "🌐 Acesse: http://69.62.89.102:8000"
else
    echo "❌ Erro ao verificar aplicação"
    docker compose -f docker-compose-sqlite.yml logs --tail=20
fi