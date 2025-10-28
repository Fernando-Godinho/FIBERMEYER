#!/usr/bin/env python3
"""
Script para testar os cálculos de IPI no sistema de orçamentos
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

def test_calculo_ipi():
    """Testa se o cálculo de IPI está funcionando corretamente"""
    
    print("=== TESTE DE CÁLCULO DE IPI ===\n")
    
    # Cenário de teste
    custo_unitario = Decimal('100.00')
    quantidade = Decimal('2.00')
    lucro_percentual = Decimal('25.00')  # 25%
    imposto_percentual = Decimal('10.00')  # 10% 
    ipi_percentual = Decimal('5.00')  # 5%
    
    print(f"Cenário de teste:")
    print(f"- Custo unitário: R$ {custo_unitario}")
    print(f"- Quantidade: {quantidade}")
    print(f"- Lucro: {lucro_percentual}%")
    print(f"- Imposto: {imposto_percentual}%")
    print(f"- IPI: {ipi_percentual}%")
    print()
    
    # Cálculos esperados
    valor_lucro_unitario = custo_unitario * (lucro_percentual / 100)
    valor_venda_unitario = custo_unitario + valor_lucro_unitario
    valor_bruto = valor_venda_unitario * quantidade
    valor_imposto = valor_bruto * (imposto_percentual / 100)
    valor_sem_ipi = valor_bruto + valor_imposto
    valor_ipi = valor_sem_ipi * (ipi_percentual / 100)
    valor_total_esperado = valor_sem_ipi + valor_ipi
    
    print(f"Cálculos manuais:")
    print(f"- Valor lucro unitário: R$ {valor_lucro_unitario}")
    print(f"- Valor venda unitário: R$ {valor_venda_unitario}")
    print(f"- Valor bruto (venda x qtd): R$ {valor_bruto}")
    print(f"- Valor imposto: R$ {valor_imposto}")
    print(f"- Valor sem IPI: R$ {valor_sem_ipi}")
    print(f"- Valor IPI: R$ {valor_ipi}")
    print(f"- Valor total esperado: R$ {valor_total_esperado}")
    print()
    
    # Buscar um orçamento existente para teste
    try:
        orcamento = Orcamento.objects.first()
        if not orcamento:
            print("❌ Nenhum orçamento encontrado para teste")
            return
            
        # Criar item de teste
        item = OrcamentoItem.objects.create(
            orcamento=orcamento,
            tipo_item='produto',
            descricao='Teste IPI',
            quantidade=quantidade,
            valor_unitario=custo_unitario,
            desconto_item=valor_lucro_unitario * quantidade,
            imposto_item=valor_imposto,
            ipi_item=ipi_percentual,
            unidade='UN'
        )
        
        print(f"Item criado no banco:")
        print(f"- ID: {item.id}")
        print(f"- Valor total calculado: R$ {item.valor_total}")
        print(f"- IPI item: {item.ipi_item}%")
        print()
        
        # Verificar se o cálculo está correto
        diferenca = abs(item.valor_total - valor_total_esperado)
        tolerance = Decimal('0.01')
        
        if diferenca <= tolerance:
            print("✅ CÁLCULO CORRETO! O valor total está sendo calculado corretamente com IPI.")
        else:
            print(f"❌ ERRO NO CÁLCULO!")
            print(f"   Esperado: R$ {valor_total_esperado}")
            print(f"   Calculado: R$ {item.valor_total}")
            print(f"   Diferença: R$ {diferenca}")
        
        # Limpar item de teste
        item.delete()
        print("\n✅ Item de teste removido")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

if __name__ == '__main__':
    test_calculo_ipi()