# 🚀 DEPLOY PARA PRODUÇÃO - PostgreSQL Neon

## 📋 Passo a Passo

### 1. Conectar no VPS

Execute o arquivo: `conectar-vps.bat`

Ou manualmente:
```bash
ssh root@69.62.89.102
```
Senha: `j89hahPXbz,uVndACJM+`

### 2. Baixar e Executar Script de Deploy

No VPS, execute:

```bash
# Baixar script de deploy
curl -o deploy-neon.sh https://raw.githubusercontent.com/Fernando-Godinho/FIBERMEYER/main/deploy-neon.sh

# Tornar executável
chmod +x deploy-neon.sh

# Executar deploy
./deploy-neon.sh
```

### 3. Aguardar Deploy

O script irá:
1. ✅ Parar containers antigos
2. ✅ Baixar código atualizado do GitHub
3. ✅ Instalar dependências (incluindo psycopg2-binary)
4. ✅ Executar migrações no PostgreSQL Neon
5. ✅ Criar superusuário admin
6. ✅ Iniciar servidor na porta 8000

### 4. Verificar se Funcionou

Após ~30 segundos, acesse:
- **Aplicação:** http://69.62.89.102:8000
- **Admin:** http://69.62.89.102:8000/admin/
- **Login:** admin / admin123

### 5. Ver Logs (se necessário)

```bash
docker-compose -f docker-compose-neon.yml logs -f
```

Pressione `Ctrl+C` para sair dos logs.

---

## 🎯 O que mudou?

### ANTES:
- ❌ Banco SQLite local no VPS
- ❌ Dados perdidos ao reiniciar container
- ❌ Um banco para desenvolvimento, outro para produção

### AGORA:
- ✅ Banco PostgreSQL online (Neon)
- ✅ Mesmo banco para desenvolvimento e produção
- ✅ Dados sincronizados automaticamente
- ✅ Acesso de qualquer lugar

---

## 📊 Verificar Dados

Os dados que você vê em produção são os MESMOS do seu desenvolvimento local:
- 215 Produtos (incluindo o "TESTE SINCRONIZAÇÃO DB ONLINE")
- 4 Orçamentos
- 118 Impostos
- 4 Mão de Obra
- 422 Componentes

Se você criar um produto no local (http://localhost:8000), **ele aparecerá na produção (http://69.62.89.102:8000)** instantaneamente! 🚀

---

## 🔧 Troubleshooting

### Aplicação não inicia?
```bash
# Ver logs
docker-compose -f docker-compose-neon.yml logs

# Reiniciar
docker-compose -f docker-compose-neon.yml restart

# Rebuild completo
docker-compose -f docker-compose-neon.yml down
./deploy-neon.sh
```

### Erro de conexão com banco?
- Verifique se a URL do Neon está correta no script
- Confirme que o banco Neon está ativo no painel

### Porta 8000 não acessível?
```bash
# Verificar firewall
ufw status

# Liberar porta
ufw allow 8000/tcp
```

---

## 🎉 Pronto!

Depois do deploy, você terá:
- ✅ Sistema rodando em produção
- ✅ Usando PostgreSQL online
- ✅ Dados sincronizados com desenvolvimento
- ✅ Acesso remoto ao mesmo banco
