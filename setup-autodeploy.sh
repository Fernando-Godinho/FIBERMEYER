#!/bin/bash

# Script para configurar auto-deploy no VPS FIBERMEYER

echo "🔧 Configurando auto-deploy no VPS..."

# Copiar script de auto-deploy
echo "📋 Copiando script de auto-deploy..."
chmod +x /root/FIBERMEYER/auto-deploy.sh
cp /root/FIBERMEYER/auto-deploy.sh /usr/local/bin/fibermeyer-autodeploy

# Criar arquivo de log
echo "📝 Configurando logs..."
touch /var/log/fibermeyer-autodeploy.log
chmod 644 /var/log/fibermeyer-autodeploy.log

# Configurar logrotate para o auto-deploy
cat > /etc/logrotate.d/fibermeyer-autodeploy << 'EOF'
/var/log/fibermeyer-autodeploy.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF

# Adicionar cron job para executar a cada 2 minutos
echo "⏰ Configurando execução automática (cron)..."
(crontab -l 2>/dev/null | grep -v fibermeyer-autodeploy; echo "*/2 * * * * /usr/local/bin/fibermeyer-autodeploy >/dev/null 2>&1") | crontab -

# Testar execução manual
echo "🧪 Testando execução do auto-deploy..."
/usr/local/bin/fibermeyer-autodeploy

echo ""
echo "✅ AUTO-DEPLOY CONFIGURADO COM SUCESSO!"
echo ""
echo "📋 RESUMO DA CONFIGURAÇÃO:"
echo "   • Script: /usr/local/bin/fibermeyer-autodeploy"
echo "   • Log: /var/log/fibermeyer-autodeploy.log"
echo "   • Execução: A cada 2 minutos via cron"
echo "   • Backup automático: db.sqlite3.backup.*"
echo ""
echo "🔍 COMANDOS ÚTEIS:"
echo "   • Ver logs: tail -f /var/log/fibermeyer-autodeploy.log"
echo "   • Executar manualmente: /usr/local/bin/fibermeyer-autodeploy"
echo "   • Ver cron jobs: crontab -l"
echo "   • Status containers: docker compose -f /root/FIBERMEYER/docker-compose-sqlite.yml ps"
echo ""
echo "🚀 Agora, toda vez que você fizer um commit no GitHub,"
echo "   as mudanças serão automaticamente aplicadas na produção!"