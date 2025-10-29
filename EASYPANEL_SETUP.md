# 🚀 FIBERMEYER no EasyPanel - Guia Completo

## 📋 Pré-requisitos
- VPS com EasyPanel instalado
- Acesso ao painel do EasyPanel
- Repositório: https://github.com/Fernando-Godinho/FIBERMEYER.git

## 🎯 Setup no EasyPanel

### 1️⃣ **Criar Nova Aplicação**
1. Acesse seu EasyPanel
2. Clique em **"+ New Project"**
3. Escolha **"Docker Compose"**
4. Nome do projeto: `fibermeyer`

### 2️⃣ **Configurar Docker Compose**
Cole este conteúdo no editor do EasyPanel:

```yaml
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
    networks:
      - fibermeyer-network
    restart: unless-stopped

  app:
    image: python:3.11-slim
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://fibermeyer:fibermeyer123@db:5432/fibermeyer
      DJANGO_DEBUG: "False"
      DJANGO_SECRET_KEY: fibermeyer-production-2025-change-me
      DJANGO_ALLOWED_HOSTS: "*"
      PYTHONUNBUFFERED: "1"
    working_dir: /app
    ports:
      - "8000:8000"
    volumes:
      - app_media:/app/media
      - app_static:/app/staticfiles
    networks:
      - fibermeyer-network
    command: >
      sh -c "
        apt-get update -qq &&
        apt-get install -y -qq git netcat-traditional pkg-config default-libmysqlclient-dev build-essential &&
        
        if [ ! -d .git ]; then
          git clone https://github.com/Fernando-Godinho/FIBERMEYER.git . &&
          echo 'Repositório clonado!';
        else
          git pull origin main &&
          echo 'Repositório atualizado!';
        fi &&
        
        pip install --no-cache-dir --upgrade pip &&
        pip install --no-cache-dir -r requirements.txt &&
        
        while ! nc -z db 5432; do sleep 1; done &&
        
        python manage.py makemigrations --noinput &&
        python manage.py migrate --noinput &&
        python manage.py collectstatic --noinput --clear &&
        
        python manage.py shell -c \"
        from django.contrib.auth import get_user_model;
        User = get_user_model();
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@fibermeyer.com', 'admin123');
        \" &&
        
        python manage.py runserver 0.0.0.0:8000
      "
    restart: unless-stopped

networks:
  fibermeyer-network:

volumes:
  postgres_data:
  app_media:
  app_static:
```

### 3️⃣ **Configurar Proxy/Domínio**
1. Vá em **"Domains"** no seu projeto
2. Adicione seu domínio ou use o subdomínio do EasyPanel
3. Configure para apontar para a porta **8000**
4. Ative HTTPS se disponível

### 4️⃣ **Deploy da Aplicação**
1. Clique em **"Deploy"**
2. Aguarde o build e início dos containers
3. Monitore os logs para verificar se tudo está funcionando

## 📱 Acessos

Após o deploy:
- **🌐 Sistema FIBERMEYER**: `https://seu-dominio.com`
- **👨‍💼 Django Admin**: `https://seu-dominio.com/admin/`
  - Login: `admin`
  - Senha: `admin123`

## 🔧 Comandos Úteis no EasyPanel

### Ver logs da aplicação:
```bash
docker logs fibermeyer-app-1 -f
```

### Acessar container da aplicação:
```bash
docker exec -it fibermeyer-app-1 bash
```

### Backup do banco:
```bash
docker exec fibermeyer-db-1 pg_dump -U fibermeyer fibermeyer > backup.sql
```

### Executar comandos Django:
```bash
docker exec fibermeyer-app-1 python manage.py shell
docker exec fibermeyer-app-1 python manage.py createsuperuser
```

## 📊 Monitoramento

### Verificar status dos containers:
```bash
docker ps
```

### Ver uso de recursos:
```bash
docker stats
```

### Logs específicos:
```bash
docker logs fibermeyer-app-1 --tail 100
docker logs fibermeyer-db-1 --tail 50
```

## 🔄 Atualizações

Para atualizar o código do GitHub:

1. **Automático**: Reinicie o container - ele puxará as atualizações
2. **Manual**: 
   ```bash
   docker exec fibermeyer-app-1 git pull origin main
   docker restart fibermeyer-app-1
   ```

## ⚠️ Troubleshooting

### ❌ Container não inicia:
1. Verifique os logs: `docker logs fibermeyer-app-1`
2. Confirme se as portas estão livres
3. Verifique se o PostgreSQL iniciou corretamente

### ❌ Erro de banco:
```bash
# Resetar banco (CUIDADO: apaga dados!)
docker-compose down -v
docker-compose up -d
```

### ❌ Erro de dependências Python:
1. Verifique se o requirements.txt está correto
2. Teste localmente primeiro
3. Verifique logs de instalação do pip

### ❌ Erro de permissões:
```bash
# Ajustar permissões dos volumes
docker exec -it fibermeyer-app-1 chown -R www-data:www-data /app/media
docker exec -it fibermeyer-app-1 chown -R www-data:www-data /app/staticfiles
```

## 🔒 Segurança para Produção

**⚠️ IMPORTANTE**: Antes de colocar em produção:

1. **Mude a SECRET_KEY**:
   ```yaml
   DJANGO_SECRET_KEY: "sua-chave-super-secreta-aqui"
   ```

2. **Mude senha do banco**:
   ```yaml
   POSTGRES_PASSWORD: sua-senha-forte-aqui
   ```

3. **Configure domínio específico**:
   ```yaml
   DJANGO_ALLOWED_HOSTS: "seu-dominio.com,www.seu-dominio.com"
   ```

4. **Mude senha do admin**:
   ```bash
   docker exec fibermeyer-app-1 python manage.py changepassword admin
   ```

## 📈 Performance

Para melhor performance em produção:

1. **Use um servidor web real** (Nginx + Gunicorn)
2. **Configure cache** (Redis)
3. **Otimize queries** do banco
4. **Configure CDN** para arquivos estáticos

## 🎉 Pronto!

Seu FIBERMEYER está rodando no EasyPanel! 

- ✅ Código atualizado automaticamente do GitHub
- ✅ Banco PostgreSQL configurado
- ✅ Admin criado automaticamente
- ✅ Pronto para uso em produção