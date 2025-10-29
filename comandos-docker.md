# Comandos úteis para gerenciar o FIBERMEYER

## 🚀 PUBLICAR O SISTEMA
docker-compose up --build -d

## 📊 VER LOGS EM TEMPO REAL
docker-compose logs -f

## 🛑 PARAR O SISTEMA
docker-compose down

## 🔄 REINICIAR O SISTEMA
docker-compose restart

## 🗑️ LIMPAR TUDO (CUIDADO: Remove dados!)
docker-compose down -v
docker system prune -af

## 📋 VER STATUS DOS CONTAINERS
docker-compose ps

## 🔧 ENTRAR NO CONTAINER DA APLICAÇÃO
docker-compose exec app bash

## 🗄️ ENTRAR NO BANCO DE DADOS
docker-compose exec db psql -U fibermeyer -d fibermeyer

## 🌐 ACESSOS
# Sistema: http://localhost:8000
# Admin: http://localhost:8000/admin/ (admin/admin123)

## 📁 BACKUP DO BANCO
docker-compose exec db pg_dump -U fibermeyer fibermeyer > backup_$(date +%Y%m%d_%H%M%S).sql