#!/usr/bin/env python
"""
Script para atualizar itens de orçamento sem lucro para o padrão de 22,5%
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

def atualizar_lucro_padrao():
    """Atualiza itens sem lucro para o padrão de 22,5%"""
    print("=== ATUALIZANDO ITENS PARA LUCRO PADRÃO 22,5% ===")
    
    # Buscar itens com desconto_item zero ou muito baixo
    itens_sem_lucro = OrcamentoItem.objects.filter(desconto_item__lte=Decimal('0.01'))
    
    print(f"📊 Encontrados {itens_sem_lucro.count()} itens com lucro zero ou muito baixo")
    
    contador_atualizados = 0
    
    for item in itens_sem_lucro:
        if item.valor_unitario > 0:
            # Calcular 22,5% de lucro sobre o custo
            custo_unitario = item.valor_unitario
            lucro_percentual = Decimal('22.5')
            
            # Calcular novo lucro
            valor_lucro_unitario = custo_unitario * (lucro_percentual / 100)
            valor_venda_unitario = custo_unitario + valor_lucro_unitario
            
            # Recalcular valores
            valor_bruto = valor_venda_unitario * item.quantidade
            valor_imposto = valor_bruto * (item.imposto_item / valor_bruto) if valor_bruto > 0 else Decimal('0')
            valor_total = valor_bruto + item.imposto_item  # manter imposto existente
            
            # Atualizar item
            item.desconto_item = valor_lucro_unitario * item.quantidade  # lucro total
            item.valor_total = valor_total
            item.save()
            
            print(f"✅ Item '{item.descricao}' (ID: {item.id})")
            print(f"   Custo: R$ {custo_unitario:.2f} → Lucro: {lucro_percentual}% (R$ {valor_lucro_unitario:.2f})")
            print(f"   Total: R$ {valor_total:.2f}")
            
            contador_atualizados += 1
    
    print(f"\n🎉 {contador_atualizados} itens foram atualizados com lucro de 22,5%")
    
    # Atualizar totais dos orçamentos afetados
    orcamentos_afetados = set()
    for item in itens_sem_lucro:
        orcamentos_afetados.add(item.orcamento.id)
    
    print(f"📋 Atualizando totais de {len(orcamentos_afetados)} orçamentos...")
    
    for orcamento_id in orcamentos_afetados:
        orcamento = Orcamento.objects.get(id=orcamento_id)
        itens = list(orcamento.itens.all())
        
        orcamento.total_liquido = sum([item.valor_total for item in itens])
        orcamento.desconto_total = sum([item.desconto_item for item in itens])  # agora é lucro
        orcamento.save()
        
        print(f"✅ Orçamento {orcamento.numero_orcamento} atualizado")
        print(f"   Total Líquido: R$ {orcamento.total_liquido:.2f}")
        print(f"   Total Lucro: R$ {orcamento.desconto_total:.2f}")

if __name__ == "__main__":
    try:
        atualizar_lucro_padrao()
        print("\n✅ Atualização concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante a atualização: {str(e)}")
        import traceback
        traceback.print_exc()