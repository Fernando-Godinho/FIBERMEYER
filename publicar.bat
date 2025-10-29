@echo off
echo ========================================
echo FIBERMEYER - Deploy Local com Docker
echo ========================================
echo.

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado! Instale o Docker Desktop primeiro.
    echo Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker encontrado!
echo.

REM Parar containers existentes se houver
echo 🛑 Parando containers existentes...
docker-compose down 2>nul

echo.
echo 🚀 Iniciando FIBERMEYER...
echo.

REM Executar docker-compose
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ FIBERMEYER publicado com sucesso!
    echo.
    echo 🌐 Acesse o sistema em:
    echo    http://localhost:8000
    echo.
    echo 👨‍💼 Admin Django:
    echo    URL: http://localhost:8000/admin/
    echo    Usuario: admin
    echo    Senha: admin123
    echo.
    echo 📊 Ver logs em tempo real:
    echo    docker-compose logs -f
    echo.
    echo 🛑 Para parar o sistema:
    echo    docker-compose down
    echo.
    
    REM Abrir automaticamente no navegador
    timeout /t 3 >nul
    start http://localhost:8000
) else (
    echo.
    echo ❌ Erro ao iniciar o sistema!
    echo.
    echo 🔍 Ver logs de erro:
    echo    docker-compose logs
    echo.
)

pause