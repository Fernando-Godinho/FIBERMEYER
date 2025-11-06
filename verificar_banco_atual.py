import os
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.db import connection

print("🔍 Verificando configuração do banco de dados:")
print("=" * 60)

db_settings = connection.settings_dict
print(f"Engine: {db_settings['ENGINE']}")
print(f"Nome: {db_settings['NAME']}")
print(f"Host: {db_settings['HOST']}")
print(f"Porta: {db_settings['PORT']}")
print(f"Usuário: {db_settings['USER']}")

print("\n" + "=" * 60)

if 'postgresql' in db_settings['ENGINE']:
    print("✅ USANDO POSTGRESQL (Neon)")
    print(f"✅ Servidor: {db_settings['HOST']}")
else:
    print("❌ USANDO SQLITE LOCAL")

print("=" * 60)

# Testar dados
from main.models import MP_Produtos

print(f"\n📊 Total de produtos no banco: {MP_Produtos.objects.count()}")
print(f"🔗 Conexão ativa: {db_settings['HOST']}")
