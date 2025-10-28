#!/usr/bin/env python3
"""
Script para testar atualizações de lucro e IPI via AJAX
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

def criar_item_teste():
    """Cria um item de teste para verificar atualizações"""
    
    print("=== CRIANDO ITEM DE TESTE ===\n")
    
    # Buscar um orçamento existente
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return None
    
    # Criar item de teste
    item = OrcamentoItem.objects.create(
        orcamento=orcamento,
        tipo_item='produto',
        descricao='Teste Atualização AJAX',
        quantidade=Decimal('1.00'),
        valor_unitario=Decimal('100.00'),  # Custo
        desconto_item=Decimal('0.00'),     # Lucro será calculado
        imposto_item=Decimal('0.00'),      # Imposto será calculado  
        ipi_item=Decimal('5.00'),          # 5% de IPI
        unidade='UN',
        valor_total=Decimal('0.00')        # Será calculado no save()
    )
    
    print(f"Item criado:")
    print(f"- ID: {item.id}")
    print(f"- Custo unitário: R$ {item.valor_unitario}")
    print(f"- IPI: {item.ipi_item}%")
    print(f"- Valor total inicial: R$ {item.valor_total}")
    print()
    
    return item

def testar_atualizacao_lucro(item):
    """Testa atualização de lucro"""
    print("=== TESTE ATUALIZAÇÃO LUCRO ===\n")
    
    lucro_percentual = Decimal('20.00')  # 20%
    
    # Simular cálculo manual
    custo_unitario = item.valor_unitario
    quantidade = item.quantidade
    ipi_percentual = item.ipi_item
    
    valor_lucro_unitario = custo_unitario * (lucro_percentual / 100)
    valor_venda_unitario = custo_unitario + valor_lucro_unitario
    valor_bruto = valor_venda_unitario * quantidade
    valor_imposto = valor_bruto * (Decimal('10.00') / 100)  # Supondo 10% de imposto
    valor_sem_ipi = valor_bruto + valor_imposto
    valor_ipi = valor_sem_ipi * (ipi_percentual / 100)
    valor_total_esperado = valor_sem_ipi + valor_ipi
    
    print(f"Cálculo manual com lucro {lucro_percentual}%:")
    print(f"- Valor lucro unitário: R$ {valor_lucro_unitario}")
    print(f"- Valor bruto: R$ {valor_bruto}")
    print(f"- Valor imposto: R$ {valor_imposto}")
    print(f"- Valor sem IPI: R$ {valor_sem_ipi}")
    print(f"- Valor IPI: R$ {valor_ipi}")
    print(f"- Valor total esperado: R$ {valor_total_esperado}")
    print()
    
    # Atualizar item como a view faria
    item.desconto_item = valor_lucro_unitario * quantidade
    item.imposto_item = valor_imposto
    item.valor_total = valor_total_esperado
    item.save()
    
    # Recarregar do banco
    item.refresh_from_db()
    
    print(f"Após save():")
    print(f"- Desconto item (lucro): R$ {item.desconto_item}")
    print(f"- Imposto item: R$ {item.imposto_item}")
    print(f"- Valor total: R$ {item.valor_total}")
    
    # Verificar se o save() manteve o valor correto
    diferenca = abs(item.valor_total - valor_total_esperado)
    if diferenca <= Decimal('0.01'):
        print("✅ Atualização de lucro funcionando!")
    else:
        print(f"❌ Erro na atualização de lucro! Diferença: R$ {diferenca}")
    
    print()

def testar_atualizacao_ipi(item):
    """Testa atualização de IPI"""
    print("=== TESTE ATUALIZAÇÃO IPI ===\n")
    
    novo_ipi = Decimal('10.00')  # Mudar para 10%
    valor_antes = item.valor_total
    
    print(f"Valor antes da mudança de IPI: R$ {valor_antes}")
    print(f"IPI antes: {item.ipi_item}%")
    print(f"Novo IPI: {novo_ipi}%")
    
    # Atualizar IPI
    item.ipi_item = novo_ipi
    item.save()  # Isso deve recalcular o valor_total automaticamente
    
    # Recarregar do banco
    item.refresh_from_db()
    
    print(f"Valor depois da mudança de IPI: R$ {item.valor_total}")
    print(f"IPI depois: {item.ipi_item}%")
    
    if item.valor_total != valor_antes:
        print("✅ Atualização de IPI funcionando!")
    else:
        print("❌ Erro: Valor total não mudou com a alteração do IPI!")
    
    print()

def limpar_item_teste(item):
    """Remove o item de teste"""
    item.delete()
    print("✅ Item de teste removido")

if __name__ == '__main__':
    item = criar_item_teste()
    if item:
        testar_atualizacao_lucro(item)
        testar_atualizacao_ipi(item)
        limpar_item_teste(item)