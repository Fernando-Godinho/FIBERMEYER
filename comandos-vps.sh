#!/bin/bash
# COMANDOS PARA EXECUTAR NO VPS - DEPLOY FIBERMEYER

echo "=========================================="
echo "🚀 FIBERMEYER - Deploy VPS Hostinger"
echo "=========================================="

# Baixar script de deploy
curl -s https://raw.githubusercontent.com/Fernando-Godinho/FIBERMEYER/main/deploy-hostinger.sh -o deploy.sh

# Dar permissão e executar
chmod +x deploy.sh
./deploy.sh