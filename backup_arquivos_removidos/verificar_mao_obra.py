#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MaoObra

print("=== VERIFICANDO REGISTROS DE MÃO DE OBRA ===")

registros = MaoObra.objects.all()
print(f"Total de registros: {registros.count()}")

for m in registros:
    print(f"  ID: {m.id}")
    print(f"  Nome: {m.nome}")
    print(f"  Valor (centavos): {m.valor_centavos}")
    print(f"  Valor (R$): {m.valor_centavos / 100:.2f}")
    print("  ---")

# Testar busca específica por Pultrusão
print("\n=== TESTANDO BUSCA POR PULTRUSÃO ===")
pultrusao1 = MaoObra.objects.filter(nome='Pultrusão').first()
print(f"Busca exata 'Pultrusão': {pultrusao1}")

pultrusao2 = MaoObra.objects.filter(nome__icontains='pultrusao').first()
print(f"Busca icontains 'pultrusao': {pultrusao2}")

if pultrusao1:
    print(f"  Valor encontrado: {pultrusao1.valor_centavos} centavos")
elif pultrusao2:
    print(f"  Valor encontrado: {pultrusao2.valor_centavos} centavos")
else:
    print("  Nenhum registro encontrado!")
