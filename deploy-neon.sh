#!/bin/bash
# Deploy FIBERMEYER com PostgreSQL Online (Neon)
# Execute este script no VPS

echo "🚀 DEPLOY FIBERMEYER - PostgreSQL Online (Neon)"
echo "================================================"

# Parar containers antigos
echo "🛑 Parando containers antigos..."
docker-compose down 2>/dev/null || true
docker rm -f $(docker ps -aq) 2>/dev/null || true

# Criar docker-compose com PostgreSQL do Neon
echo "📝 Criando configuração..."
cat > docker-compose-neon.yml << 'EOF'
version: '3.8'

services:
  app:
    image: python:3.11-slim
    environment:
      # PostgreSQL Online - Neon
      DATABASE_URL: postgresql://neondb_owner:npg_WHw0KL1qUsmN@ep-falling-unit-acyw2gc7-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require
      SECRET_KEY: django-insecure-production-change-me-12345
      DEBUG: "False"
      ALLOWED_HOSTS: "*"
      DJANGO_SETTINGS_MODULE: "fibermeyer_project.settings"
      PYTHONUNBUFFERED: "1"
    working_dir: /app
    ports:
      - "8000:8000"
    volumes:
      - app_media:/app/media
      - app_static:/app/staticfiles
    command: bash -c "
      apt-get update -qq && 
      apt-get install -y -qq git netcat-traditional build-essential pkg-config && 
      echo '📦 Clonando repositório...' &&
      rm -rf /app/* &&
      git clone https://github.com/Fernando-Godinho/FIBERMEYER.git /tmp/repo && 
      cp -r /tmp/repo/* /app/ && 
      cd /app && 
      echo '📚 Instalando dependências...' &&
      pip install -q -r requirements.txt && 
      echo '🔄 Executando migrações...' &&
      python manage.py migrate --noinput && 
      echo '📁 Coletando arquivos estáticos...' &&
      mkdir -p /app/staticfiles && 
      python manage.py collectstatic --noinput --clear && 
      echo '👨‍💼 Criando superusuário...' &&
      python -c 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=\"admin\").exists() or User.objects.create_superuser(\"admin\", \"admin@fibermeyer.com\", \"admin123\")' && 
      echo '✅ Deploy concluído! Iniciando servidor...' &&
      python manage.py runserver 0.0.0.0:8000
    "
    restart: unless-stopped

volumes:
  app_media:
  app_static:
EOF

echo "🔥 Liberando porta 8000 no firewall..."
ufw allow 8000/tcp 2>/dev/null || true

echo "🚀 Iniciando aplicação..."
docker-compose -f docker-compose-neon.yml up -d

echo ""
echo "⏳ Aguardando 30 segundos para aplicação inicializar..."
sleep 30

echo ""
echo "🔍 Verificando se a aplicação está rodando..."
if curl -f http://localhost:8000/ >/dev/null 2>&1; then
    echo "✅ DEPLOY REALIZADO COM SUCESSO!"
    echo ""
    echo "================================================"
    echo "🌐 Aplicação: http://69.62.89.102:8000"
    echo "👨‍💼 Admin: http://69.62.89.102:8000/admin/"
    echo "🔑 Login: admin / admin123"
    echo "💾 Banco: PostgreSQL (Neon - Online)"
    echo "================================================"
    echo ""
    echo "📊 Ver logs:"
    echo "   docker-compose -f docker-compose-neon.yml logs -f"
else
    echo "❌ ERRO: Aplicação não está respondendo!"
    echo "📋 Ver logs de erro:"
    echo "   docker-compose -f docker-compose-neon.yml logs"
fi
