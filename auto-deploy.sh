#!/bin/bash

# Script de auto-deploy para FIBERMEYER
# Este script deve ser executado no VPS a cada 2 minutos via cron

VPS_DIR="/root/FIBERMEYER"
LOG_FILE="/var/log/fibermeyer-autodeploy.log"
LAST_COMMIT_FILE="/tmp/fibermeyer-last-commit"

# Função de log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Ir para diretório do projeto
cd "$VPS_DIR" || {
    log "❌ ERRO: Diretório $VPS_DIR não encontrado"
    exit 1
}

# Verificar último commit local
CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "")

# Verificar último commit remoto
git fetch origin main >/dev/null 2>&1
REMOTE_COMMIT=$(git rev-parse origin/main 2>/dev/null || echo "")

# Verificar se houve mudanças
if [ -f "$LAST_COMMIT_FILE" ]; then
    LAST_KNOWN_COMMIT=$(cat "$LAST_COMMIT_FILE")
else
    LAST_KNOWN_COMMIT=""
fi

# Se há commits novos, fazer deploy
if [ "$REMOTE_COMMIT" != "$LAST_KNOWN_COMMIT" ] && [ -n "$REMOTE_COMMIT" ]; then
    log "🔄 NOVO COMMIT DETECTADO! Iniciando auto-deploy..."
    log "📍 Commit anterior: $LAST_KNOWN_COMMIT"
    log "📍 Novo commit: $REMOTE_COMMIT"
    
    # Fazer backup do banco atual
    log "💾 Fazendo backup do banco..."
    cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
    
    # Atualizar código
    log "📥 Atualizando código..."
    git reset --hard origin/main
    git pull origin main
    
    # Parar containers
    log "🛑 Parando containers..."
    docker compose -f docker-compose-sqlite.yml down >/dev/null 2>&1
    
    # Iniciar containers
    log "🚀 Iniciando containers..."
    docker compose -f docker-compose-sqlite.yml up -d --build >/dev/null 2>&1
    
    # Aguardar inicialização
    log "⏳ Aguardando aplicação inicializar..."
    sleep 30
    
    # Verificar se está funcionando
    if curl -f http://localhost:8000/ >/dev/null 2>&1; then
        log "✅ DEPLOY REALIZADO COM SUCESSO!"
        log "🌐 Aplicação disponível em: http://69.62.89.102:8000"
        echo "$REMOTE_COMMIT" > "$LAST_COMMIT_FILE"
    else
        log "❌ ERRO: Aplicação não está respondendo após deploy"
        log "🔄 Tentando rollback..."
        
        # Restaurar backup do banco
        if [ -f "db.sqlite3.backup.$(date +%Y%m%d)_"* ]; then
            cp db.sqlite3.backup.$(date +%Y%m%d)_* db.sqlite3 2>/dev/null
        fi
        
        # Reiniciar containers
        docker compose -f docker-compose-sqlite.yml down >/dev/null 2>&1
        docker compose -f docker-compose-sqlite.yml up -d >/dev/null 2>&1
        
        log "⚠️ Rollback tentado. Verifique manualmente."
        exit 1
    fi
else
    # Nenhuma mudança detectada - log silencioso apenas se houver problemas
    if ! curl -f http://localhost:8000/ >/dev/null 2>&1; then
        log "⚠️ ATENÇÃO: Aplicação não está respondendo!"
        log "🔄 Tentando reiniciar containers..."
        docker compose -f docker-compose-sqlite.yml restart >/dev/null 2>&1
    fi
fi