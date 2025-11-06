# 🗄️ Guia de Migração para PostgreSQL Online

Este guia explica como migrar seu banco de dados SQLite para PostgreSQL online.

## 📋 Pré-requisitos

- Python 3.x instalado
- Dependências instaladas (`pip install -r requirements.txt`)

## 🚀 Opções de Banco de Dados Gratuito

### 1. Supabase (Recomendado) ⭐
**Gratuito até 500MB**

1. Acesse: https://supabase.com
2. Crie uma conta e um novo projeto
3. Defina uma senha forte
4. Aguarde ~2 minutos para o banco ser criado
5. Vá em **Settings** → **Database**
6. Copie a **Connection String** (modo "Session")
7. A URL será algo como:
   ```
   postgresql://postgres.xxxxx:[SUA-SENHA]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

### 2. Neon
**Gratuito com 0.5GB**

1. Acesse: https://neon.tech
2. Crie uma conta
3. Crie um novo projeto
4. Copie a Connection String
5. A URL será algo como:
   ```
   postgresql://usuario:senha@ep-xxxxx.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

### 3. Railway
**Gratuito com limitações**

1. Acesse: https://railway.app
2. Crie uma conta
3. Crie um novo projeto PostgreSQL
4. Copie a DATABASE_URL
5. A URL será algo como:
   ```
   postgresql://postgres:senha@containers-us-west-xxx.railway.app:6543/railway
   ```

## ⚙️ Configuração

### Passo 1: Instalar Dependências

```powershell
pip install -r requirements.txt
```

### Passo 2: Configurar Variáveis de Ambiente

1. Copie o arquivo `.env.example` para `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edite o arquivo `.env` e adicione sua DATABASE_URL:
   ```
   SECRET_KEY=sua-chave-secreta
   DEBUG=True
   DATABASE_URL=postgresql://usuario:senha@host:5432/banco
   ```

   **Exemplo com Supabase:**
   ```
   DATABASE_URL=postgresql://postgres.xxxxx:MinhaSenh@123@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

### Passo 3: Testar Conexão

Teste se consegue conectar ao PostgreSQL:

```powershell
python -c "from django.db import connection; connection.ensure_connection(); print('Conectado com sucesso!')"
```

Se aparecer "Conectado com sucesso!", está tudo certo! ✅

## 📦 Migração de Dados

### Opção A: Migração Automática (Recomendado)

Execute o script de migração:

```powershell
python migrar_para_postgresql.py
```

O script irá:
1. ✅ Verificar conexão com PostgreSQL
2. 📤 Exportar dados do SQLite
3. 🔄 Executar migrações no PostgreSQL
4. 📥 Importar dados para PostgreSQL
5. ✔️ Verificar se tudo foi importado

### Opção B: Migração Manual

1. **Executar migrações:**
   ```powershell
   python manage.py migrate
   ```

2. **Exportar dados do SQLite:**
   ```powershell
   python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --indent=2 > backup_sqlite.json
   ```

3. **Importar dados para PostgreSQL:**
   ```powershell
   python manage.py loaddata backup_sqlite.json
   ```

## ✅ Verificação

1. **Listar dados:**
   ```powershell
   python manage.py shell
   ```
   
   No shell Python:
   ```python
   from main.models import *
   print(f"Produtos: {Produto.objects.count()}")
   print(f"Orçamentos: {Orcamento.objects.count()}")
   ```

2. **Iniciar servidor:**
   ```powershell
   python manage.py runserver
   ```

3. Acesse: http://localhost:8000

## 🔄 Voltar para SQLite (Se necessário)

Se quiser voltar para SQLite temporariamente:

1. Edite o arquivo `.env`
2. Comente a linha DATABASE_URL:
   ```
   # DATABASE_URL=postgresql://...
   ```

3. Reinicie o servidor

O sistema voltará a usar `db.sqlite3` automaticamente.

## 🛡️ Backup

**Importante:** Sempre faça backup antes de qualquer migração!

```powershell
# Backup do SQLite
Copy-Item db.sqlite3 db.sqlite3.backup

# Backup do PostgreSQL (após migração)
python manage.py dumpdata > backup_postgresql.json
```

## 🔒 Segurança

### Para Produção:

1. **Nunca** commite o arquivo `.env` no Git
2. Adicione `.env` ao `.gitignore`
3. Use uma `SECRET_KEY` forte e única
4. Configure `DEBUG=False` em produção
5. Configure `ALLOWED_HOSTS` corretamente

Exemplo `.gitignore`:
```
.env
*.sqlite3
*.pyc
__pycache__/
backup_*.json
```

## 📊 Vantagens do PostgreSQL

✅ Mais robusto e confiável  
✅ Melhor performance com muitos dados  
✅ Suporte a recursos avançados  
✅ Acesso remoto (trabalhe de qualquer lugar)  
✅ Backups automáticos (dependendo do serviço)  
✅ Escalável para produção  

## 🆘 Problemas Comuns

### Erro de conexão
- Verifique se a DATABASE_URL está correta
- Confirme se o banco está ativo no painel do serviço
- Teste a conexão com: `python manage.py dbshell`

### Erro de SSL
Adicione `?sslmode=require` no final da URL:
```
DATABASE_URL=postgresql://...?sslmode=require
```

### Erro de permissões
Verifique se o usuário do banco tem permissões corretas

### Timeout
Alguns serviços gratuitos podem ter tempo de inatividade. Aguarde alguns segundos e tente novamente.

## 📞 Suporte

Se tiver problemas:
1. Verifique os logs de erro
2. Teste a conexão passo a passo
3. Consulte a documentação do seu provedor de banco
4. Mantenha o backup do SQLite até ter certeza que tudo funciona

---

**Dica:** Comece testando com o Supabase. É o mais fácil de configurar e muito confiável! 🚀
