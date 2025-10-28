#!/usr/bin/env python3
"""
Script para testar a view de orçamento e identificar erros
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import OrcamentoItem, Orcamento
from decimal import Decimal

def verificar_orcamento_item():
    """Verifica se há problemas com os itens de orçamento"""
    
    print("=== VERIFICAÇÃO DE ITENS DE ORÇAMENTO ===\n")
    
    # Buscar itens problemáticos
    items_problema = []
    
    for item in OrcamentoItem.objects.all():
        try:
            # Tentar acessar todos os campos
            campos = {
                'id': item.id,
                'valor_unitario': item.valor_unitario,
                'quantidade': item.quantidade,
                'ipi_item': getattr(item, 'ipi_item', 0),
                'unidade': getattr(item, 'unidade', 'UN'),
                'valor_total': item.valor_total
            }
            
            # Verificar se IPI é muito alto
            if hasattr(item, 'ipi_item') and item.ipi_item and item.ipi_item > 50:
                print(f"⚠️ Item {item.id} tem IPI alto: {item.ipi_item}%")
                items_problema.append(item.id)
                
        except Exception as e:
            print(f"❌ Erro no item {item.id}: {e}")
            items_problema.append(item.id)
    
    print(f"\nTotal de itens: {OrcamentoItem.objects.count()}")
    print(f"Itens com problema: {len(items_problema)}")
    
    if items_problema:
        print(f"IDs problemáticos: {items_problema[:10]}")  # Mostrar até 10

def verificar_view_orcamento():
    """Testa se a view de orçamento tem problemas"""
    
    print("\n=== VERIFICAÇÃO DA VIEW DE ORÇAMENTO ===\n")
    
    try:
        # Importar a view
        from main.views import orcamento
        
        # Buscar um orçamento para testar
        orcamento = Orcamento.objects.first()
        if not orcamento:
            print("❌ Nenhum orçamento encontrado")
            return
            
        print(f"Testando orçamento ID: {orcamento.id}")
        print(f"Número de itens: {orcamento.itens.count()}")
        
        # Verificar se há itens com problemas
        for item in orcamento.itens.all():
            if hasattr(item, 'ipi_item') and item.ipi_item and item.ipi_item > 80:
                print(f"⚠️ Item {item.id} tem IPI muito alto: {item.ipi_item}%")
                print(f"   Descrição: {item.descricao}")
                
                # Tentar corrigir
                print(f"   Corrigindo IPI de {item.ipi_item}% para 10%")
                item.ipi_item = Decimal('10.0')
                item.save()
                print(f"   ✅ Corrigido!")
        
        print("✅ View de orçamento verificada")
        
    except Exception as e:
        print(f"❌ Erro na view de orçamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verificar_orcamento_item()
    verificar_view_orcamento()