#!/bin/bash
# =========================================================
# FIBERMEYER - Deploy Automático VPS Hostinger Ubuntu 24.04
# =========================================================

set -e  # Para na primeira falha

echo "=========================================="
echo "🚀 FIBERMEYER - Deploy VPS Hostinger"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    print_error "Execute como root: sudo $0"
    exit 1
fi

print_status "Iniciando deploy do FIBERMEYER..."

# 1. ATUALIZAR SISTEMA
print_status "Atualizando sistema Ubuntu..."
apt update -qq
apt upgrade -y -qq

# 2. INSTALAR DEPENDÊNCIAS
print_status "Instalando dependências necessárias..."
apt install -y -qq \
    nginx \
    ufw \
    htop \
    curl \
    wget \
    unzip \
    certbot \
    python3-certbot-nginx

# 3. VERIFICAR DOCKER COMPOSE
print_status "Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_warning "Instalando Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 4. CONFIGURAR FIREWALL
print_status "Configurando firewall UFW..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw --force enable

# 5. CRIAR DIRETÓRIO DO PROJETO
print_status "Criando estrutura de diretórios..."
mkdir -p /opt/fibermeyer
cd /opt/fibermeyer

# 6. BAIXAR PROJETO DO GITHUB
print_status "Baixando projeto do GitHub..."
if [ -d ".git" ]; then
    print_warning "Atualizando projeto existente..."
    git fetch origin
    git reset --hard origin/main
else
    print_status "Clonando projeto..."
    git clone https://github.com/Fernando-Godinho/FIBERMEYER.git .
fi

# 7. CRIAR ARQUIVO .ENV PARA PRODUÇÃO
print_status "Configurando variáveis de ambiente..."
cat > .env << EOF
# FIBERMEYER - Produção VPS Hostinger
DEBUG=False
SECRET_KEY=fibermeyer-production-$(openssl rand -hex 32)
ALLOWED_HOSTS=69.62.89.102,localhost,127.0.0.1

# Banco PostgreSQL
DB_NAME=fibermeyer
DB_USER=fibermeyer
DB_PASSWORD=fibermeyer123_prod_$(openssl rand -hex 8)
DB_HOST=db
DB_PORT=5432

# URLs
SITE_URL=http://69.62.89.102
ADMIN_URL=/admin/
EOF

# 8. CRIAR DOCKER COMPOSE PARA PRODUÇÃO
print_status "Criando docker-compose para produção..."
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fibermeyer
      POSTGRES_USER: fibermeyer
      POSTGRES_PASSWORD: fibermeyer123_prod
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    networks:
      - fibermeyer-net

  app:
    image: python:3.11-slim
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://fibermeyer:fibermeyer123_prod@db:5432/fibermeyer
      DJANGO_DEBUG: "False"
      DJANGO_ALLOWED_HOSTS: "69.62.89.102,localhost,127.0.0.1"
      DJANGO_SETTINGS_MODULE: "fibermeyer_project.settings"
      PYTHONUNBUFFERED: "1"
    working_dir: /app
    ports:
      - "127.0.0.1:8000:8000"
    volumes:
      - app_media:/app/media
      - app_static:/app/staticfiles
      - ./logs:/app/logs
    networks:
      - fibermeyer-net
    command: |
      bash -c "
      echo 'Instalando dependencias do sistema...' &&
      apt-get update -qq &&
      apt-get install -y -qq git netcat-traditional build-essential pkg-config default-libmysqlclient-dev &&
      echo 'Configurando aplicacao...' &&
      rm -rf /app/* &&
      git clone https://github.com/Fernando-Godinho/FIBERMEYER.git /app &&
      cd /app &&
      echo 'Instalando dependencias Python...' &&
      pip install -q Django==5.2.4 djangorestframework reportlab psycopg2-binary requests pillow python-decouple asgiref sqlparse tzdata gunicorn &&
      echo 'Aguardando PostgreSQL...' &&
      while ! nc -z db 5432; do echo 'Aguardando banco...'; sleep 3; done &&
      echo 'Executando migracoes...' &&
      python manage.py migrate --noinput &&
      echo 'Coletando arquivos estaticos...' &&
      mkdir -p /app/staticfiles /app/logs &&
      python manage.py collectstatic --noinput --clear &&
      echo 'Criando superuser admin...' &&
      python manage.py shell << 'SCRIPT'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fibermeyer.com', 'admin123')
    print('Superuser admin criado!')
else:
    print('Superuser admin ja existe')
SCRIPT
      echo 'Iniciando servidor Gunicorn...' &&
      gunicorn fibermeyer_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120 --access-logfile /app/logs/access.log --error-logfile /app/logs/error.log
      "
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  app_media:
    driver: local
  app_static:
    driver: local

networks:
  fibermeyer-net:
    driver: bridge
EOF

# 9. CONFIGURAR NGINX
print_status "Configurando Nginx..."
cat > /etc/nginx/sites-available/fibermeyer << 'EOF'
server {
    listen 80;
    server_name 69.62.89.102;
    client_max_body_size 100M;

    # Logs
    access_log /var/log/nginx/fibermeyer-access.log;
    error_log /var/log/nginx/fibermeyer-error.log;

    # Servir arquivos estáticos
    location /static/ {
        alias /opt/fibermeyer/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /opt/fibermeyer/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Proxy para Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Ativar site
ln -sf /etc/nginx/sites-available/fibermeyer /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Testar configuração do Nginx
nginx -t

# 10. CRIAR SCRIPTS DE GERENCIAMENTO
print_status "Criando scripts de gerenciamento..."

cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando FIBERMEYER..."
docker-compose -f docker-compose.prod.yml up -d
systemctl restart nginx
echo "✅ FIBERMEYER iniciado!"
echo "🌐 Acesso: http://69.62.89.102"
echo "👨‍💼 Admin: http://69.62.89.102/admin/ (admin/admin123)"
EOF

cat > stop.sh << 'EOF'
#!/bin/bash
echo "🛑 Parando FIBERMEYER..."
docker-compose -f docker-compose.prod.yml down
echo "✅ FIBERMEYER parado!"
EOF

cat > restart.sh << 'EOF'
#!/bash
echo "🔄 Reiniciando FIBERMEYER..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
systemctl restart nginx
echo "✅ FIBERMEYER reiniciado!"
EOF

cat > logs.sh << 'EOF'
#!/bin/bash
echo "📊 Logs do FIBERMEYER:"
docker-compose -f docker-compose.prod.yml logs -f
EOF

cat > backup.sh << 'EOF'
#!/bin/bash
echo "💾 Backup do banco de dados..."
mkdir -p backups
docker-compose -f docker-compose.prod.yml exec db pg_dump -U fibermeyer fibermeyer > backups/backup_$(date +%Y%m%d_%H%M%S).sql
echo "✅ Backup criado em backups/"
EOF

chmod +x *.sh

# 11. INICIAR SERVIÇOS
print_status "Iniciando serviços..."
systemctl enable nginx
systemctl start nginx

# Parar containers existentes se houver
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Iniciar aplicação
docker-compose -f docker-compose.prod.yml up -d

# Aguardar containers subirem
print_status "Aguardando containers iniciarem..."
sleep 30

# 12. VERIFICAR STATUS
print_status "Verificando status dos serviços..."
systemctl status nginx --no-pager
docker-compose -f docker-compose.prod.yml ps

print_success "=========================================="
print_success "🎉 FIBERMEYER DEPLOY CONCLUÍDO!"
print_success "=========================================="
echo ""
print_success "🌐 Sistema: http://69.62.89.102"
print_success "👨‍💼 Admin: http://69.62.89.102/admin/"
print_success "🔑 Login: admin / admin123"
echo ""
print_status "📋 Comandos úteis:"
print_status "   ./start.sh    - Iniciar sistema"
print_status "   ./stop.sh     - Parar sistema"
print_status "   ./restart.sh  - Reiniciar sistema"
print_status "   ./logs.sh     - Ver logs em tempo real"
print_status "   ./backup.sh   - Backup do banco"
echo ""
print_status "📁 Localização: /opt/fibermeyer"
print_status "📊 Logs Nginx: /var/log/nginx/"
print_status "📊 Logs App: /opt/fibermeyer/logs/"
echo ""
print_warning "⚠️  Após o deploy, configure:"
print_warning "   1. Domínio personalizado (se houver)"
print_warning "   2. SSL/HTTPS com certbot"
print_warning "   3. Backup automático"
echo ""
print_success "Deploy finalizado com sucesso! 🚀"