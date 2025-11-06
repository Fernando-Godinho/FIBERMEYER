import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.db import connection

try:
    connection.ensure_connection()
    print('✓ Conectado com sucesso ao PostgreSQL!')
    print(f'✓ Banco: {connection.settings_dict["NAME"]}')
    print(f'✓ Host: {connection.settings_dict["HOST"]}')
except Exception as e:
    print(f'✗ Erro ao conectar: {e}')
