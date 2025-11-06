import os
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos
from django.db import connection

# Verificar qual banco está sendo usado
db_settings = connection.settings_dict
print(f"🔗 Banco em uso: {db_settings['ENGINE']}")
print(f"🌐 Host: {db_settings['HOST']}")
print("\n" + "=" * 60)

# Buscar o produto
print("🔍 Buscando produto 'sincronização db'...\n")

produtos = MP_Produtos.objects.filter(descricao__icontains='sincronização')

if produtos.exists():
    print(f"✅ ENCONTRADO {produtos.count()} produto(s):\n")
    for p in produtos:
        print(f"   ID: {p.id}")
        print(f"   Descrição: {p.descricao}")
        print(f"   Código: {p.codigo}")
        print(f"   Preço: R$ {p.preco}")
        print(f"   Unidade: {p.unidade}")
        print(f"   Data criação: {p.data_cadastro}")
        print()
else:
    print("❌ Produto NÃO encontrado no banco!")
    print("\n🔍 Mostrando últimos 5 produtos cadastrados:")
    ultimos = MP_Produtos.objects.all().order_by('-id')[:5]
    for p in ultimos:
        print(f"   - {p.id}: {p.descricao}")

print("=" * 60)
print(f"📊 Total de produtos no banco: {MP_Produtos.objects.count()}")
