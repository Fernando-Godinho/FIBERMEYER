@echo off
echo ==========================================
echo 🚀 EXECUTANDO DEPLOY FIBERMEYER NO VPS
echo ==========================================
echo.

echo 📡 Conectando no VPS 69.62.89.102...
echo 👤 Usuario: root
echo.

echo 🔄 Executando comandos de deploy...
echo.

REM Conectar via SSH e executar comandos
plink -ssh root@69.62.89.102 -pw "j89hahPXbz,uVndACJM+" -batch "curl -s https://raw.githubusercontent.com/Fernando-Godinho/FIBERMEYER/main/deploy-hostinger.sh -o deploy.sh && chmod +x deploy.sh && ./deploy.sh"

echo.
echo ✅ Deploy concluído!
echo.
echo 🌐 Acesse: http://69.62.89.102
echo 👨‍💼 Admin: http://69.62.89.102/admin/
echo 🔑 Login: admin / admin123
echo.

pause