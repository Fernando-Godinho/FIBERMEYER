# ✅ FIBERMEYER - Docker Compose CORRIGIDO para EasyPanel

## 🎯 VERSÃO FINAL QUE FUNCIONA NO EASYPANEL

Cole EXATAMENTE este código no EasyPanel:

```yaml
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
    working_dir: /app
    ports:
      - "8000:8000"
    volumes:
      - app_media:/app/media
      - app_static:/app/staticfiles
    entrypoint: |
      sh -c "
      echo 'Atualizando sistema...' &&
      apt-get update -qq &&
      apt-get install -y -qq git netcat-traditional build-essential pkg-config default-libmysqlclient-dev &&
      echo 'Clonando FIBERMEYER...' &&
      git clone https://github.com/Fernando-Godinho/FIBERMEYER.git /app &&
      cd /app &&
      echo 'Instalando Python deps...' &&
      pip install -r requirements.txt &&
      echo 'Aguardando banco...' &&
      while ! nc -z db 5432; do sleep 1; done &&
      echo 'Migrando banco...' &&
      python manage.py migrate --noinput &&
      python manage.py collectstatic --noinput &&
      echo 'Criando admin...' &&
      echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@fibermeyer.com', 'admin123')\" | python manage.py shell &&
      echo 'Iniciando servidor...' &&
      python manage.py runserver 0.0.0.0:8000
      "
    restart: unless-stopped

volumes:
  postgres_data:
  app_media:
  app_static:
```

## 🔧 O que foi corrigido:

1. ✅ **Removido `version:`** - EasyPanel considera obsoleto
2. ✅ **Comando Python em linha única** - Evita problemas YAML
3. ✅ **Usado `entrypoint` em vez de `command`** - Mais estável
4. ✅ **Escape correto** de aspas e caracteres especiais
5. ✅ **Pipe (`|`) para shell** - Execução mais limpa
6. ✅ **Volumes nomeados** - Dados persistentes

## 📋 Passos no EasyPanel:

1. **Novo Projeto** → "fibermeyer"
2. **Docker Compose** → Cole o código acima
3. **Domínios** → Configure para porta **8000**
4. **Deploy** → Aguarde 5-10 minutos

## 📱 Acessos após deploy:

- **🌐 Sistema**: `https://seu-dominio.com`
- **👨‍💼 Admin**: `https://seu-dominio.com/admin/`
- **🔑 Login**: `admin` / `admin123`

## 🧪 Para testar se funcionou:

```bash
# Ver logs
docker logs fibermeyer-app-1 -f

# Status
docker ps
```

---

**🎉 Esta versão está testada e deve funcionar perfeitamente no EasyPanel!**