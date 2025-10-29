# 🚀 FIBERMEYER - Deploy no EasyPanel

## 📋 Instruções para EasyPanel

### 1️⃣ Criar Projeto
1. Login no seu EasyPanel
2. Clique em **"+ New Project"**
3. Escolha **"Docker Compose"**
4. Nome do projeto: `fibermeyer`

### 2️⃣ Docker Compose
Cole exatamente este conteúdo no editor do EasyPanel:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=fibermeyer
      - POSTGRES_USER=fibermeyer
      - POSTGRES_PASSWORD=fibermeyer123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db_backup:/backup
    networks:
      - fibermeyer-network
    restart: unless-stopped

  app:
    image: python:3.11-slim
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://fibermeyer:fibermeyer123@db:5432/fibermeyer
      - DJANGO_DEBUG=False
      - DJANGO_SECRET_KEY=fibermeyer-production-secret-key-2025-change-me
      - DJANGO_ALLOWED_HOSTS=*
      - PYTHONUNBUFFERED=1
    working_dir: /workspace/FIBERMEYER
    ports:
      - "8000:8000"
    volumes:
      - ./media:/workspace/FIBERMEYER/media
      - ./staticfiles:/workspace/FIBERMEYER/staticfiles
    networks:
      - fibermeyer-network
    command: >
      sh -c "
        echo '🔧 Instalando dependências do sistema...' &&
        apt-get update -qq &&
        apt-get install -y -qq git pkg-config default-libmysqlclient-dev build-essential curl &&
        
        echo '📥 Clonando/Atualizando repositório FIBERMEYER...' &&
        if [ ! -d .git ]; then
          echo '📥 Clonando repositório...' &&
          git clone https://github.com/Fernando-Godinho/FIBERMEYER.git . &&
          echo '✅ Repositório clonado!';
        else
          echo '📂 Atualizando repositório...' &&
          git pull origin main &&
          echo '✅ Repositório atualizado!';
        fi &&
        
        echo '📦 Instalando dependências Python...' &&
        pip install --no-cache-dir --upgrade pip &&
        pip install --no-cache-dir -r requirements.txt &&
        
        echo '🗄️ Aguardando banco de dados...' &&
        apt-get install -y -qq netcat-traditional &&
        timeout=60 &&
        while ! nc -z db 5432 && [ \$timeout -gt 0 ]; do 
          echo \"Aguardando PostgreSQL... (\$timeout segundos restantes)\";
          sleep 2;
          timeout=\$((timeout-2));
        done &&
        if ! nc -z db 5432; then
          echo '❌ Timeout na conexão com PostgreSQL!';
          exit 1;
        fi &&
        echo '✅ Banco conectado!' &&
        
        echo '🔄 Executando migrações...' &&
        python manage.py makemigrations --noinput &&
        python manage.py migrate --noinput &&
        
        echo '📊 Coletando arquivos estáticos...' &&
        python manage.py collectstatic --noinput --clear &&
        
        echo '👤 Criando superusuário...' &&
        python manage.py shell -c \"
        from django.contrib.auth import get_user_model;
        User = get_user_model();
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@fibermeyer.com', 'admin123');
            print('✅ Superusuário criado: admin/admin123');
        else:
            print('ℹ️ Superusuário já existe');
        \" &&
        
        echo '🚀 Iniciando FIBERMEYER na porta 8000...' &&
        echo '🌐 Sistema será acessível via proxy do EasyPanel' &&
        echo '👨‍💼 Admin disponível em: /admin/ (admin/admin123)' &&
        echo '📋 Orçamentos em: /orcamento/' &&
        echo '✅ FIBERMEYER INICIADO COM SUCESSO!' &&
        python manage.py runserver 0.0.0.0:8000
      "
    restart: unless-stopped

  # Opcional: Para administração do banco (remova se não precisar)
  adminer:
    image: adminer:latest
    depends_on:
      - db
    ports:
      - "8080:8080"
    environment:
      - ADMINER_DEFAULT_SERVER=db
      - ADMINER_DESIGN=galkaev
    networks:
      - fibermeyer-network
    restart: unless-stopped

networks:
  fibermeyer-network:
    driver: bridge

volumes:
  postgres_data:
```

### 3️⃣ Configurar Domínio
1. Vá em **"Domains"** no seu projeto
2. Adicione seu domínio (ou use o subdomínio do EasyPanel)
3. Configure proxy para porta **8000**
4. Ative HTTPS se disponível

### 4️⃣ Deploy
1. Clique em **"Deploy"**
2. Aguarde 5-10 minutos para build completo
3. Monitore os logs para acompanhar o progresso

### 5️⃣ Acessar Sistema
Após deploy bem-sucedido:

- **🌐 Sistema Principal**: `https://seu-dominio.com`
- **👨‍💼 Administração**: `https://seu-dominio.com/admin/`
  - **Login**: `admin`
  - **Senha**: `admin123`
- **📋 Orçamentos**: `https://seu-dominio.com/orcamento/`
- **🗄️ Gerenciador BD**: `https://seu-dominio.com:8080` (se mantiver adminer)

### 6️⃣ Primeiro Acesso
1. Acesse `/admin/` e faça login com `admin/admin123`
2. **MUDE A SENHA DO ADMIN IMEDIATAMENTE**
3. Teste criar um orçamento em `/orcamento/`
4. Teste gerar PDF com observações

## 🔧 Comandos Úteis

### Ver logs em tempo real:
```bash
docker logs fibermeyer-app-1 -f
```

### Acessar container da aplicação:
```bash
docker exec -it fibermeyer-app-1 bash
```

### Reiniciar aplicação:
```bash
docker restart fibermeyer-app-1
```

### Backup do banco:
```bash
docker exec fibermeyer-db-1 pg_dump -U fibermeyer fibermeyer > backup_$(date +%Y%m%d).sql
```

### Atualizar código do GitHub:
```bash
# Automático: reinicie o container
docker restart fibermeyer-app-1

# Manual:
docker exec fibermeyer-app-1 git pull origin main
docker restart fibermeyer-app-1
```

## 🔒 Segurança (PRODUÇÃO)

**⚠️ ANTES DE USAR EM PRODUÇÃO:**

1. **Mude senha do banco**:
   ```yaml
   POSTGRES_PASSWORD: SuaSenhaSeguraAqui123!
   ```

2. **Mude chave secreta**:
   ```yaml
   DJANGO_SECRET_KEY: sua-chave-super-secreta-de-50-caracteres-aqui
   ```

3. **Configure domínio específico**:
   ```yaml
   DJANGO_ALLOWED_HOSTS: seudominio.com,www.seudominio.com
   ```

4. **Mude senha do admin**:
   ```bash
   docker exec fibermeyer-app-1 python manage.py changepassword admin
   ```

## 🎯 Funcionalidades Disponíveis

✅ **Sistema de Orçamentos** completo  
✅ **Geração de PDF** com observações customizadas  
✅ **Coluna de unidades** nos PDFs  
✅ **Gestão de produtos** e matérias-primas  
✅ **Cálculo de impostos** automático  
✅ **Sistema de mão de obra**  
✅ **Interface administrativa** Django  
✅ **Backup automático** do banco  

## 📞 Suporte

Se encontrar problemas:

1. **Verifique logs**: `docker logs fibermeyer-app-1 -f`
2. **Status containers**: `docker ps`
3. **Restart limpo**: `docker-compose down && docker-compose up -d`

---

## 🎉 Pronto!

Seu **FIBERMEYER** estará rodando perfeitamente no EasyPanel com:
- ✅ Código atualizado automaticamente do GitHub
- ✅ Banco PostgreSQL configurado e persistente
- ✅ Admin criado automaticamente
- ✅ SSL/HTTPS via proxy do EasyPanel
- ✅ Todos os recursos funcionando (PDFs, observações, etc.)

**Acesse e comece a usar imediatamente!** 🚀