#!/bin/bash
# Deploy super simples - FIBERMEYER na porta 8000

echo "🚀 Deploy simples FIBERMEYER na porta 8000..."

# Parar containers existentes
docker-compose down 2>/dev/null || true

# Criar docker-compose simples
cat > docker-compose-simple.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fibermeyer
      POSTGRES_USER: fibermeyer
      POSTGRES_PASSWORD: fibermeyer123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  app:
    image: python:3.11-slim
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://fibermeyer:fibermeyer123@db:5432/fibermeyer
      DJANGO_DEBUG: "False"
      DJANGO_ALLOWED_HOSTS: "*"
      DJANGO_SETTINGS_MODULE: "fibermeyer_project.settings"
      PYTHONUNBUFFERED: "1"
    working_dir: /app
    ports:
      - "8000:8000"
    volumes:
      - app_media:/app/media
      - app_static:/app/staticfiles
    command: bash -c "apt-get update -qq && apt-get install -y -qq git netcat-traditional build-essential pkg-config default-libmysqlclient-dev && git clone https://github.com/Fernando-Godinho/FIBERMEYER.git /app && cd /app && pip install -q Django==5.2.4 djangorestframework reportlab psycopg2-binary requests pillow python-decouple asgiref sqlparse tzdata && while ! nc -z db 5432; do sleep 2; done && python manage.py migrate --noinput && mkdir -p /app/staticfiles && python manage.py collectstatic --noinput --clear && python -c 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=\"admin\").exists() or User.objects.create_superuser(\"admin\", \"admin@fibermeyer.com\", \"admin123\")' && python manage.py runserver 0.0.0.0:8000"
    restart: unless-stopped

volumes:
  postgres_data:
  app_media:
  app_static:
EOF

# Liberar porta 8000 no firewall
ufw allow 8000/tcp 2>/dev/null || true

# Iniciar aplicação
docker-compose -f docker-compose-simple.yml up -d

echo "✅ Deploy simples concluído!"
echo "🌐 Acesse: http://69.62.89.102:8000"
echo "👨‍💼 Admin: http://69.62.89.102:8000/admin/"
echo "🔑 Login: admin / admin123"