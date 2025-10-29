@echo off
echo 🚀 FIBERMEYER - Setup com Docker
echo ================================

echo.
echo 📋 Verificando se Docker está instalado...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado! Instale o Docker Desktop primeiro.
    echo 💡 Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker encontrado!

echo.
echo 📋 Verificando se Docker Compose está disponível...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose não encontrado!
    pause
    exit /b 1
)

echo ✅ Docker Compose encontrado!

echo.
echo 📂 Criando pastas necessárias...
if not exist "media" mkdir media
if not exist "staticfiles" mkdir staticfiles
if not exist "db_backup" mkdir db_backup

echo.
echo 🔧 Configurando ambiente...
if not exist ".env" (
    echo 📄 Criando arquivo .env...
    copy ".env.example" ".env" >nul 2>&1
)

echo.
echo 🚀 Iniciando containers Docker...
echo ⏳ Isso pode demorar alguns minutos na primeira execução...
docker-compose up -d

echo.
echo 📊 Verificando status dos containers...
docker-compose ps

echo.
echo 🎉 Setup concluído!
echo.
echo 📱 Acessos disponíveis:
echo    🌐 FIBERMEYER: http://localhost:8000
echo    👨‍💼 Admin: http://localhost:8000/admin (admin/admin123)
echo    🗄️ Banco: http://localhost:8080 (fibermeyer/fibermeyer123)
echo.
echo 📋 Comandos úteis:
echo    docker-compose logs -f app    (ver logs)
echo    docker-compose down           (parar)
echo    docker-compose restart app    (reiniciar)
echo.

pause