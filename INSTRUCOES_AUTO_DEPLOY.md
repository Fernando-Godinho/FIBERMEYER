# 🚀 INSTRUÇÕES AUTO-DEPLOY FIBERMEYER

## 📋 **COMO USAR O SISTEMA DE DEPLOY AUTOMÁTICO**

### ⚡ **RESUMO RÁPIDO:**
1. Faça suas mudanças no código
2. Execute: `git add . && git commit -m "sua mensagem" && git push`
3. Aguarde **até 2 minutos**
4. ✅ **Mudanças automaticamente em produção!**

---

## 🔧 **COMO FUNCIONA:**

### 🤖 **Sistema Automático:**
- **Verificação:** A cada 2 minutos o VPS verifica novos commits
- **Detecção:** Compara último commit local vs remoto
- **Ação:** Se houver diferença, executa deploy automático
- **Backup:** Sempre faz backup do banco antes do deploy
- **Rollback:** Em caso de erro, tenta reverter automaticamente

### 📊 **Monitoramento:**
```bash
# Ver logs em tempo real
ssh root@69.62.89.102 "tail -f /var/log/fibermeyer-autodeploy.log"

# Status dos containers
ssh root@69.62.89.102 "docker ps"

# Executar deploy manual
ssh root@69.62.89.102 "/usr/local/bin/fibermeyer-autodeploy"
```

---

## 📝 **BOAS PRÁTICAS PARA COMMITS:**

### ✅ **Mensagens Recomendadas:**

#### 🎨 **Design/Interface:**
```bash
git commit -m "🎨 Design: Nova paleta de cores no PDF"
git commit -m "🖼️ Interface: Melhorias no layout do cabeçalho"
git commit -m "🌈 Estilo: Gradientes e sombras modernas"
```

#### ✨ **Novas Funcionalidades:**
```bash
git commit -m "✨ Feature: Sistema de observações personalizadas"
git commit -m "🔧 Função: Cálculo automático de impostos"
git commit -m "📊 Relatório: Exportação de dados em Excel"
```

#### 🐛 **Correções:**
```bash
git commit -m "🐛 Fix: Correção no cálculo de totais"
git commit -m "⚡ Hotfix: Problema na geração de PDF"
git commit -m "🔧 Bugfix: Erro na validação de campos"
```

#### 📈 **Melhorias:**
```bash
git commit -m "📈 Performance: Otimização de consultas"
git commit -m "🚀 Upgrade: Atualização Django 5.2.4"
git commit -m "🔒 Security: Melhoria na validação de dados"
```

#### 📚 **Documentação:**
```bash
git commit -m "📚 Docs: Instruções de auto-deploy"
git commit -m "📋 README: Guia de instalação atualizado"
```

---

## 🎯 **FLUXO COMPLETO DE DESENVOLVIMENTO:**

### 1️⃣ **Desenvolvimento Local:**
```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Fazer mudanças no código
# Testar localmente
python manage.py runserver

# Verificar se está funcionando
# http://localhost:8000
```

### 2️⃣ **Commit e Deploy:**
```bash
# Adicionar arquivos
git add .

# Commit com mensagem descritiva
git commit -m "🎨 Sua mensagem aqui"

# Push para GitHub (ativa auto-deploy)
git push
```

### 3️⃣ **Aguardar Deploy:**
- ⏰ **Máximo 2 minutos** para detecção
- ⚡ **30-60 segundos** para execução
- 🌐 **Verificar:** http://69.62.89.102:8000

---

## 📊 **LOGS DO SISTEMA:**

### 📋 **Exemplo de Log Sucesso:**
```
[2025-10-30 17:44:02] 🔄 NOVO COMMIT DETECTADO! Iniciando auto-deploy...
[2025-10-30 17:44:02] 📍 Commit anterior: 6199afb...
[2025-10-30 17:44:02] 📍 Novo commit: 2aa11a6...
[2025-10-30 17:44:02] 💾 Fazendo backup do banco...
[2025-10-30 17:44:02] 📥 Atualizando código...
[2025-10-30 17:44:02] 🛑 Parando containers...
[2025-10-30 17:44:04] 🚀 Iniciando containers...
[2025-10-30 17:44:04] ⏳ Aguardando aplicação inicializar...
[2025-10-30 17:44:34] ✅ DEPLOY REALIZADO COM SUCESSO!
[2025-10-30 17:44:34] 🌐 Aplicação disponível em: http://69.62.89.102:8000
```

### ⚠️ **Em Caso de Erro:**
```
[2025-10-30 17:45:00] ❌ ERRO: Aplicação não está respondendo após deploy
[2025-10-30 17:45:00] 🔄 Tentando rollback...
[2025-10-30 17:45:05] ⚠️ Rollback tentado. Verifique manualmente.
```

---

## 🆘 **TROUBLESHOOTING:**

### 🔍 **Deploy Não Funcionou:**
```bash
# 1. Verificar se commit foi detectado
ssh root@69.62.89.102 "tail -20 /var/log/fibermeyer-autodeploy.log"

# 2. Executar deploy manual
ssh root@69.62.89.102 "/usr/local/bin/fibermeyer-autodeploy"

# 3. Verificar containers
ssh root@69.62.89.102 "docker ps"

# 4. Reiniciar containers se necessário
ssh root@69.62.89.102 "cd FIBERMEYER && docker compose -f docker-compose-sqlite.yml restart"
```

### 🔧 **Aplicação Não Responde:**
```bash
# 1. Verificar logs do container
ssh root@69.62.89.102 "cd FIBERMEYER && docker compose -f docker-compose-sqlite.yml logs --tail=50"

# 2. Restart completo
ssh root@69.62.89.102 "cd FIBERMEYER && docker compose -f docker-compose-sqlite.yml down && docker compose -f docker-compose-sqlite.yml up -d"
```

---

## 📈 **INFORMAÇÕES DO SISTEMA:**

### 🌐 **URLs Importantes:**
- **Produção:** http://69.62.89.102:8000
- **Admin:** http://69.62.89.102:8000/admin/
- **Login:** admin / admin123

### 📁 **Arquivos do Sistema:**
- **Auto-deploy:** `/usr/local/bin/fibermeyer-autodeploy`
- **Logs:** `/var/log/fibermeyer-autodeploy.log`
- **Código:** `/root/FIBERMEYER/`
- **Banco:** `/root/FIBERMEYER/db.sqlite3`

### ⏰ **Configuração Cron:**
```bash
# Ver cron jobs
crontab -l

# Resultado esperado:
*/2 * * * * /usr/local/bin/fibermeyer-autodeploy >/dev/null 2>&1
```

---

## 🎯 **EXEMPLO PRÁTICO:**

### 📝 **Cenário: Alterar cor do botão**

```bash
# 1. Editar arquivo CSS localmente
# main/static/main/css/style.css

# 2. Testar localmente
python manage.py runserver

# 3. Commit e deploy
git add .
git commit -m "🎨 Style: Cor do botão alterada para azul FIBERMEYER"
git push

# 4. Aguardar 2 minutos
# 5. Verificar: http://69.62.89.102:8000
```

---

## ✅ **CHECKLIST PRÉ-COMMIT:**

- [ ] ✅ Código testado localmente
- [ ] ✅ Sem erros no console
- [ ] ✅ Funcionalidade funcionando
- [ ] ✅ Mensagem de commit descritiva
- [ ] ✅ Arquivos necessários adicionados (`git add .`)

---

**🚀 SISTEMA 100% AUTOMATIZADO E FUNCIONAL!**

*Última atualização: 30/10/2025*