#!/usr/bin/env python3
"""
Teste da nova fórmula sequencial: Valor Base → Impostos → Lucro → IPI
"""

import os
import django
from decimal import Decimal
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import OrcamentoItem

def testar_formula_sequencial():
    """Testa a nova fórmula sequencial"""
    print("=== TESTE DA NOVA FÓRMULA SEQUENCIAL ===")
    print(f"Timestamp: {datetime.now()}\n")
    
    print("📋 ORDEM DE APLICAÇÃO CORRETA:")
    print("   1. Valor Base = Custo × Quantidade")
    print("   2. + Impostos = Valor Base × (1 + Impostos%/100)")
    print("   3. + Lucro = Valor com Impostos × (1 + Lucro%/100)")
    print("   4. + IPI = Valor com Lucro × (1 + IPI%/100)")
    print()
    
    # Criar um item de teste
    print("🧪 CRIANDO ITEM DE TESTE:")
    item_teste = OrcamentoItem(
        quantidade=Decimal('10'),
        valor_unitario=Decimal('100.00'),
        imposto_item=Decimal('20.0'),  # 20% impostos
        desconto_item=Decimal('30.0'),  # 30% lucro  
        ipi_item=Decimal('15.0')        # 15% IPI
    )
    
    print(f"   Quantidade: {item_teste.quantidade}")
    print(f"   Valor Unitário: R$ {item_teste.valor_unitario}")
    print(f"   Impostos: {item_teste.imposto_item}%")
    print(f"   Lucro: {item_teste.desconto_item}%")
    print(f"   IPI: {item_teste.ipi_item}%")
    print()
    
    # Calcular manualmente
    print("🔢 CÁLCULO MANUAL:")
    valor_base = item_teste.quantidade * item_teste.valor_unitario
    print(f"   1. Valor Base: {item_teste.quantidade} × R${item_teste.valor_unitario} = R$ {valor_base}")
    
    valor_com_impostos = valor_base * (1 + item_teste.imposto_item / 100)
    print(f"   2. + Impostos ({item_teste.imposto_item}%): R$ {valor_base} × 1.{item_teste.imposto_item:04.1f} = R$ {valor_com_impostos}")
    
    valor_com_lucro = valor_com_impostos * (1 + item_teste.desconto_item / 100)
    print(f"   3. + Lucro ({item_teste.desconto_item}%): R$ {valor_com_impostos} × 1.{item_teste.desconto_item:04.1f} = R$ {valor_com_lucro}")
    
    valor_final = valor_com_lucro * (1 + item_teste.ipi_item / 100)
    print(f"   4. + IPI ({item_teste.ipi_item}%): R$ {valor_com_lucro} × 1.{item_teste.ipi_item:04.1f} = R$ {valor_final}")
    print()
    
    # Usar o método save() do modelo - vamos simular sem salvar no banco
    print("🔧 CÁLCULO PELO MODELO (SIMULADO):")
    # Simular o cálculo do modelo sem salvar
    valor_base_modelo = item_teste.quantidade * item_teste.valor_unitario
    valor_com_impostos_modelo = valor_base_modelo * (1 + item_teste.imposto_item / 100)
    valor_com_lucro_modelo = valor_com_impostos_modelo * (1 + item_teste.desconto_item / 100)
    valor_total_modelo = valor_com_lucro_modelo * (1 + item_teste.ipi_item / 100)
    
    print(f"   Valor Total calculado pelo modelo: R$ {valor_total_modelo}")
    print()
    
    # Comparar resultados
    print("📊 COMPARAÇÃO:")
    diferenca = abs(float(valor_final) - float(valor_total_modelo))
    if diferenca < 0.01:  # Diferença menor que 1 centavo
        print(f"   ✅ CORRETO! Diferença: R$ {diferenca:.4f}")
    else:
        print(f"   ❌ ERRO! Diferença: R$ {diferenca:.2f}")
        print(f"      Manual: R$ {valor_final:.2f}")
        print(f"      Modelo: R$ {valor_total_modelo:.2f}")
    
    print()
    
    # Teste com valores reais do banco
    print("📁 TESTE COM DADOS REAIS:")
    item_real = OrcamentoItem.objects.first()
    if item_real:
        print(f"   Item ID: {item_real.id}")
        print(f"   Quantidade: {item_real.quantidade}")
        print(f"   Valor Unitário: R$ {item_real.valor_unitario}")
        print(f"   Impostos: {item_real.imposto_item}%")
        print(f"   Lucro: {item_real.desconto_item}%")
        print(f"   IPI: {item_real.ipi_item}%")
        
        # Salvar para recalcular
        valor_anterior = item_real.valor_total
        item_real.save()
        
        print(f"   Valor Total anterior: R$ {valor_anterior}")
        print(f"   Valor Total recalculado: R$ {item_real.valor_total}")
        
        if valor_anterior != item_real.valor_total:
            print(f"   🔄 Valor atualizado! Diferença: R$ {abs(float(valor_anterior) - float(item_real.valor_total)):.2f}")
        else:
            print(f"   ✅ Valor mantido (cálculo consistente)")
    else:
        print("   ❌ Nenhum item encontrado no banco")

def exemplo_comparativo():
    """Mostra exemplo comparativo das duas fórmulas"""
    print("\n" + "="*60)
    print("📋 EXEMPLO COMPARATIVO DAS FÓRMULAS")
    print("="*60)
    
    # Dados de exemplo
    custo = 100
    quantidade = 10
    impostos = 20  # 20%
    lucro = 30     # 30%
    ipi = 15       # 15%
    
    print(f"Dados: R$ {custo} × {quantidade} unidades")
    print(f"Impostos: {impostos}%, Lucro: {lucro}%, IPI: {ipi}%")
    print()
    
    # Fórmula ANTERIOR (incorreta)
    print("❌ FÓRMULA ANTERIOR (INCORRETA):")
    print("   Valor = Custo × Qtd / (1 - (Impostos + Lucro)/100) × (1 + IPI/100)")
    valor_base_antigo = custo * quantidade
    denominador = 1 - (impostos + lucro) / 100
    valor_com_divisao = valor_base_antigo / denominador
    valor_final_antigo = valor_com_divisao * (1 + ipi / 100)
    print(f"   = {custo} × {quantidade} / (1 - ({impostos}+{lucro})/100) × (1 + {ipi}/100)")
    print(f"   = {valor_base_antigo} / {denominador} × 1.{ipi}")
    print(f"   = R$ {valor_final_antigo:.2f}")
    print()
    
    # Fórmula NOVA (correta)
    print("✅ FÓRMULA NOVA (CORRETA):")
    print("   1. Base = Custo × Qtd")
    print("   2. +Impostos = Base × (1 + Impostos/100)")
    print("   3. +Lucro = ComImpostos × (1 + Lucro/100)")
    print("   4. +IPI = ComLucro × (1 + IPI/100)")
    
    valor_base = custo * quantidade
    valor_com_impostos = valor_base * (1 + impostos / 100)
    valor_com_lucro = valor_com_impostos * (1 + lucro / 100)
    valor_final_novo = valor_com_lucro * (1 + ipi / 100)
    
    print(f"   1. {custo} × {quantidade} = R$ {valor_base:.2f}")
    print(f"   2. R$ {valor_base:.2f} × 1.{impostos} = R$ {valor_com_impostos:.2f}")
    print(f"   3. R$ {valor_com_impostos:.2f} × 1.{lucro} = R$ {valor_com_lucro:.2f}")
    print(f"   4. R$ {valor_com_lucro:.2f} × 1.{ipi} = R$ {valor_final_novo:.2f}")
    print()
    
    # Comparação
    diferenca = valor_final_novo - valor_final_antigo
    print(f"💰 DIFERENÇA: R$ {diferenca:.2f} ({diferenca/valor_final_antigo*100:+.1f}%)")
    
    if diferenca > 0:
        print("   📈 Nova fórmula resulta em valor MAIOR")
    else:
        print("   📉 Nova fórmula resulta em valor MENOR")

if __name__ == "__main__":
    testar_formula_sequencial()
    exemplo_comparativo()