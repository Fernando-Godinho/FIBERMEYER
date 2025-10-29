#!/bin/bash
# Deploy automático FIBERMEYER no VPS Hostinger

echo "=========================================="
echo "🚀 EXECUTANDO DEPLOY AUTOMÁTICO"
echo "=========================================="
echo ""

# Informações do VPS
VPS_IP="69.62.89.102"
VPS_USER="root"
VPS_PASS="j89hahPXbz,uVndACJM+"

echo "📡 Conectando no VPS: $VPS_IP"
echo "👤 Usuario: $VPS_USER"
echo ""

# Script para executar no VPS
cat > deploy_remote.sh << 'REMOTE_SCRIPT'
#!/bin/bash
set -e

echo "🔄 Iniciando deploy do FIBERMEYER..."

# Baixar script de deploy
echo "📥 Baixando script de deploy..."
curl -s https://raw.githubusercontent.com/Fernando-Godinho/FIBERMEYER/main/deploy-hostinger.sh -o deploy.sh

# Dar permissão
chmod +x deploy.sh

# Executar deploy
echo "🚀 Executando deploy..."
./deploy.sh

echo "✅ Deploy concluído!"
REMOTE_SCRIPT

# Executar no VPS via SSH
echo "🔐 Executando deploy no VPS..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_IP" 'bash -s' < deploy_remote.sh

echo ""
echo "🎉 Deploy executado com sucesso!"
echo ""
echo "🌐 Acesse: http://69.62.89.102"
echo "👨‍💼 Admin: http://69.62.89.102/admin/"
echo "🔑 Login: admin / admin123"