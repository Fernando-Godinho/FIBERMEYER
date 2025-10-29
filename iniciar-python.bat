@echo off
echo ========================================
echo FIBERMEYER - Deploy Local (Python)
echo ========================================
echo.

echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo 📦 Instalando dependências...
pip install -r requirements.txt

echo 🗄️ Configurando banco de dados...
python manage.py makemigrations
python manage.py migrate

echo 📁 Coletando arquivos estáticos...
python manage.py collectstatic --noinput

echo 👤 Criando superuser admin...
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fibermeyer.com', 'admin123');
    print('Superuser admin criado!')
else:
    print('Superuser admin já existe')
"

echo.
echo ✅ Sistema configurado!
echo.
echo 🚀 Iniciando servidor Django...
echo.
echo 🌐 Acesse: http://localhost:8000
echo 👨‍💼 Admin: http://localhost:8000/admin/ (admin/admin123)
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python manage.py runserver