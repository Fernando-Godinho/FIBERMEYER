# 🚀 FIBERMEYER - Setup com Docker

Este é um guia para executar o projeto FIBERMEYER usando Docker Compose.

## 📋 Pré-requisitos

- Docker instalado
- Docker Compose instalado
- Git (opcional, o container faz o clone automaticamente)

## 🏃‍♂️ Como executar

### 1. Clone este repositório (ou baixe apenas o docker-compose.yml)

```bash
git clone https://github.com/Fernando-Godinho/FIBERMEYER.git
cd FIBERMEYER
```

### 2. Configure as variáveis de ambiente (opcional)

```bash
cp .env.example .env
# Edite o arquivo .env se necessário
```

### 3. Execute o projeto

```bash
docker-compose up -d
```

### 4. Acompanhe os logs (opcional)

```bash
docker-compose logs -f app
```

## 📱 Acessos

Após a inicialização completa:

- **🌐 Aplicação FIBERMEYER**: http://localhost:8000
- **👨‍💼 Django Admin**: http://localhost:8000/admin/
  - Usuário: `admin`
  - Senha: `admin123`
- **🗄️ Adminer (Banco de dados)**: http://localhost:8080
  - Sistema: PostgreSQL
  - Servidor: db
  - Usuário: fibermeyer
  - Senha: fibermeyer123
  - Base: fibermeyer

## 🔧 Comandos úteis

### Parar os containers
```bash
docker-compose down
```

### Reiniciar apenas a aplicação
```bash
docker-compose restart app
```

### Ver logs em tempo real
```bash
docker-compose logs -f app
```

### Executar comandos Django no container
```bash
docker-compose exec app python manage.py shell
docker-compose exec app python manage.py createsuperuser
docker-compose exec app python manage.py migrate
```

### Backup do banco de dados
```bash
docker-compose exec db pg_dump -U fibermeyer fibermeyer > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar backup
```bash
docker-compose exec -T db psql -U fibermeyer fibermeyer < backup.sql
```

## 🗂️ Estrutura do projeto

```
FIBERMEYER/
├── docker-compose.yml          # Configuração dos containers
├── .env.example               # Exemplo de variáveis de ambiente
├── .env                       # Suas variáveis de ambiente (criar)
├── media/                     # Arquivos de mídia (uploads)
├── staticfiles/              # Arquivos estáticos coletados
└── db_backup/                # Pasta para backups do banco
```

## 🔄 Atualizações

Para atualizar o código do repositório:

```bash
docker-compose exec app git pull
docker-compose restart app
```

Ou simplesmente:

```bash
docker-compose down
docker-compose up -d
```

O container irá verificar automaticamente por atualizações no repositório.

## ⚠️ Notas importantes

1. **Primeira execução**: Pode demorar alguns minutos para baixar as imagens e instalar dependências
2. **Dados persistentes**: O banco de dados é persistente entre reinicializações
3. **Desenvolvimento**: Este setup é adequado para desenvolvimento. Para produção, ajuste as configurações de segurança
4. **Logs**: Use `docker-compose logs app` para ver logs detalhados em caso de problemas

## 🛠️ Solução de problemas

### Container não inicia
```bash
docker-compose logs app
```

### Erro de banco de dados
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recria tudo
```

### Limpar tudo e recomeçar
```bash
docker-compose down -v --remove-orphans
docker system prune -f
docker-compose up -d
```

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs -f`
2. Confirme que as portas 8000, 5432 e 8080 estão livres
3. Certifique-se que o Docker está executando corretamente

---

**🎉 Pronto! Seu FIBERMEYER está rodando em containers Docker!**