@echo off
echo ===========================================
echo    REINICIAR PROJETO FIBERMEYER
echo ===========================================
echo.
echo 1. Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo 2. Verificando projeto...
python manage.py check

echo.
echo 3. Iniciando servidor Django...
echo Acesse: http://127.0.0.1:8000/
echo Pressione Ctrl+C para parar o servidor
echo.
python manage.py runserver

pause
