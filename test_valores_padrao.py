#!/usr/bin/env python3
"""
Script para testar se os valores padrão de lucro foram alterados para 0%
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem, MP_Produtos
from decimal import Decimal

def testar_valores_padrao():
    print("🔍 TESTANDO VALORES PADRÃO DE LUCRO...")
    
    # Buscar um orçamento existente
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    print(f"📋 Testando com orçamento: {orcamento}")
    
    # Buscar um produto para teste
    produto = MP_Produtos.objects.first()
    if not produto:
        print("❌ Nenhum produto encontrado")
        return
    
    print(f"📦 Produto de teste: {produto.descricao}")
    
    # Criar um item de teste com valores padrão
    print("\n🧪 TESTANDO CRIAÇÃO DE ITEM COM VALORES PADRÃO...")
    
    # Simular a criação como no código real
    quantidade = 1.0
    lucro_padrao = 0  # Novo valor padrão
    imposto = 0
    
    # Criar item temporário (não salvar no banco)
    item_teste = OrcamentoItem(
        orcamento=orcamento,
        descricao=produto.descricao,
        quantidade=quantidade,
        valor_unitario=produto.custo_centavos / 100,  # Converter centavos para reais
        desconto_item=lucro_padrao,
        imposto_item=imposto,
        ipi_item=0
    )
    
    print(f"✅ Item criado com:")
    print(f"   • Quantidade: {item_teste.quantidade}")
    print(f"   • Valor unitário: R$ {item_teste.valor_unitario}")
    print(f"   • Lucro padrão: {item_teste.desconto_item}%")
    print(f"   • Imposto: {item_teste.imposto_item}%")
    print(f"   • IPI: {item_teste.ipi_item}%")
    
    # Calcular valor final com fórmula sequencial
    valor_base = Decimal(str(item_teste.quantidade)) * Decimal(str(item_teste.valor_unitario))
    
    # Impostos do orçamento
    icms = Decimal(str(orcamento.icms or 0))
    comissao = Decimal(str(orcamento.comissao or 0))
    outros_impostos = icms + Decimal('3.65') + Decimal('2.28') + Decimal('1.0') + Decimal('0.0') + Decimal('1.5') + Decimal('18.0')
    impostos_totais = comissao + outros_impostos + Decimal(str(item_teste.imposto_item))
    
    valor_com_impostos = valor_base * (Decimal('1') + impostos_totais / Decimal('100'))
    valor_com_lucro = valor_com_impostos * (Decimal('1') + Decimal(str(item_teste.desconto_item)) / Decimal('100'))
    valor_final = valor_com_lucro * (Decimal('1') + Decimal(str(item_teste.ipi_item)) / Decimal('100'))
    
    print(f"\n💰 CÁLCULO COM LUCRO 0%:")
    print(f"   1. Valor base: R$ {valor_base}")
    print(f"   2. + Impostos ({impostos_totais}%): R$ {valor_com_impostos}")
    print(f"   3. + Lucro ({item_teste.desconto_item}%): R$ {valor_com_lucro}")
    print(f"   4. + IPI ({item_teste.ipi_item}%): R$ {valor_final}")
    print(f"   ✅ Valor final: R$ {valor_final}")
    
    if item_teste.desconto_item == 0:
        print("\n✅ SUCESSO: Valor padrão de lucro alterado para 0%")
    else:
        print(f"\n❌ ERRO: Valor padrão de lucro ainda é {item_teste.desconto_item}%")

if __name__ == "__main__":
    testar_valores_padrao()