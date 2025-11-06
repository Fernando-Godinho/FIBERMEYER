import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')

# Temporariamente forçar SQLite
os.environ['DATABASE_URL'] = ''

django.setup()

from main.models import MP_Produtos, Orcamento, Imposto, MaoObra

print("📊 Contando registros no SQLite:")
print(f"   - Produtos: {MP_Produtos.objects.using('default').count()}")
print(f"   - Orçamentos: {Orcamento.objects.using('default').count()}")
print(f"   - Impostos: {Imposto.objects.using('default').count()}")
print(f"   - Mão de Obra: {MaoObra.objects.using('default').count()}")
