#!/usr/bin/env python
"""
Corrigir DEFINITIVAMENTE o item COLA ESTRUTURAL
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import OrcamentoItem

def corrigir_definitivo():
    """Corrige definitivamente o valor total"""
    print("=== CORREÇÃO DEFINITIVA ===")
    
    item = OrcamentoItem.objects.filter(descricao__icontains='COLA ESTRUTURAL').first()
    
    if item:
        print(f"ANTES:")
        print(f"Valor Total: R$ {item.valor_total}")
        
        # Cálculo correto
        custo_unitario = Decimal('86.85')
        quantidade = Decimal('10')
        lucro_percentual = Decimal('22.5')
        
        custo_total = custo_unitario * quantidade  # 868.50
        lucro_unitario = custo_unitario * (lucro_percentual / 100)  # 19.54
        valor_venda_unitario = custo_unitario + lucro_unitario  # 106.39
        valor_total_correto = valor_venda_unitario * quantidade  # 1063.91
        lucro_total = lucro_unitario * quantidade  # 195.41
        
        print(f"\nCÁLCULO CORRETO:")
        print(f"Custo Total: R$ {custo_total}")
        print(f"Lucro Total: R$ {lucro_total}")
        print(f"Valor Total: R$ {valor_total_correto}")
        
        # Atualizar
        item.valor_total = valor_total_correto
        item.desconto_item = lucro_total
        item.save()
        
        print(f"\nDEPOIS:")
        print(f"Valor Total: R$ {item.valor_total}")
        
        # Atualizar orçamento
        orcamento = item.orcamento
        itens = list(orcamento.itens.all())
        orcamento.total_liquido = sum([i.valor_total for i in itens])
        orcamento.desconto_total = sum([i.desconto_item for i in itens])
        orcamento.save()
        
        print(f"\nORÇAMENTO ATUALIZADO:")
        print(f"Total Líquido: R$ {orcamento.total_liquido}")
        print(f"Total Lucro: R$ {orcamento.desconto_total}")

if __name__ == "__main__":
    corrigir_definitivo()