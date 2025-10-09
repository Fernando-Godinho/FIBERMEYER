#!/usr/bin/env python
"""
Verificar valores do item COLA ESTRUTURAL
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import OrcamentoItem

def verificar_cola_estrutural():
    """Verifica detalhes do item COLA ESTRUTURAL"""
    print("=== VERIFICANDO ITEM COLA ESTRUTURAL ===")
    
    item = OrcamentoItem.objects.filter(descricao__icontains='COLA ESTRUTURAL').first()
    
    if item:
        print(f"Item: {item.descricao}")
        print(f"ID: {item.id}")
        print(f"Custo Unitário (valor_unitario): {item.valor_unitario}")
        print(f"Quantidade: {item.quantidade}")
        print(f"Lucro Total (desconto_item): {item.desconto_item}")
        print(f"Imposto: {item.imposto_item}")
        print(f"Valor Total: {item.valor_total}")
        
        # Calcular o que deveria ser
        custo_total = item.valor_unitario * item.quantidade
        lucro_unitario = item.desconto_item / item.quantidade
        percentual_lucro = (lucro_unitario / item.valor_unitario) * 100
        valor_venda_unitario = item.valor_unitario + lucro_unitario
        valor_venda_total = valor_venda_unitario * item.quantidade
        
        print(f"\n=== ANÁLISE ===")
        print(f"Custo Total: {custo_total}")
        print(f"Lucro Unitário: {lucro_unitario}")
        print(f"Percentual de Lucro: {percentual_lucro:.1f}%")
        print(f"Valor Venda Unitário: {valor_venda_unitario}")
        print(f"Valor Venda Total: {valor_venda_total}")
        print(f"Esperado com 22.5%: {custo_total * 1.225}")

if __name__ == "__main__":
    verificar_cola_estrutural()