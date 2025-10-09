#!/usr/bin/env python
"""
Script para corrigir item com cálculo incorreto
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import OrcamentoItem, Orcamento

def corrigir_item_cola_estrutural():
    """Corrige o item COLA ESTRUTURAL com valores incorretos"""
    print("=== CORRIGINDO ITEM COLA ESTRUTURAL ===")
    
    # Buscar item COLA ESTRUTURAL
    itens = OrcamentoItem.objects.filter(descricao__icontains='COLA ESTRUTURAL')
    
    for item in itens:
        print(f"\n📋 Item encontrado: {item.descricao} (ID: {item.id})")
        print(f"   Valores atuais:")
        print(f"   - Custo Unitário: R$ {item.valor_unitario}")
        print(f"   - Quantidade: {item.quantidade}")
        print(f"   - Lucro Total Atual: R$ {item.desconto_item}")
        print(f"   - Valor Total Atual: R$ {item.valor_total}")
        
        # Dados corretos
        custo_unitario = item.valor_unitario  # R$ 86,85
        quantidade = item.quantidade  # 10
        lucro_percentual = Decimal('22.5')  # 22,5%
        
        # Calcular valores corretos
        valor_lucro_unitario = custo_unitario * (lucro_percentual / 100)
        valor_venda_unitario = custo_unitario + valor_lucro_unitario
        valor_lucro_total = valor_lucro_unitario * quantidade
        valor_bruto = valor_venda_unitario * quantidade
        valor_total = valor_bruto + item.imposto_item  # manter imposto existente
        
        print(f"\n   Cálculo correto:")
        print(f"   - Custo Unitário: R$ {custo_unitario}")
        print(f"   - Lucro Percentual: {lucro_percentual}%")
        print(f"   - Lucro Unitário: R$ {valor_lucro_unitario}")
        print(f"   - Valor Venda Unitário: R$ {valor_venda_unitario}")
        print(f"   - Quantidade: {quantidade}")
        print(f"   - Valor Bruto: R$ {valor_bruto}")
        print(f"   - Valor Total Correto: R$ {valor_total}")
        
        # Atualizar item
        item.desconto_item = valor_lucro_total
        item.valor_total = valor_total
        item.save()
        
        print(f"   ✅ Item corrigido!")
        
        # Atualizar totais do orçamento
        orcamento = item.orcamento
        itens_orcamento = list(orcamento.itens.all())
        orcamento.total_liquido = sum([i.valor_total for i in itens_orcamento])
        orcamento.desconto_total = sum([i.desconto_item for i in itens_orcamento])
        orcamento.save()
        
        print(f"   ✅ Orçamento {orcamento.numero_orcamento} atualizado")
        print(f"   - Total Líquido: R$ {orcamento.total_liquido}")
        print(f"   - Total Lucro: R$ {orcamento.desconto_total}")

if __name__ == "__main__":
    try:
        corrigir_item_cola_estrutural()
        print("\n✅ Correção concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante a correção: {str(e)}")
        import traceback
        traceback.print_exc()