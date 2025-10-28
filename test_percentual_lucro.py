#!/usr/bin/env python3
"""
Teste para verificar o problema de multiplicação do percentual de lucro
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem, MP_Produtos

def testar_problema_percentual():
    print("🔍 TESTANDO PROBLEMA DE MULTIPLICAÇÃO DO PERCENTUAL...")
    
    # Buscar um orçamento e item existente
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    # Buscar um item existente ou criar um temporário
    item = orcamento.itens.first()
    if not item:
        produto = MP_Produtos.objects.first()
        if not produto:
            print("❌ Nenhum produto encontrado")
            return
        
        # Criar item temporário
        item = OrcamentoItem.objects.create(
            orcamento=orcamento,
            tipo_item='produto',
            descricao=f"TESTE - {produto.descricao}",
            quantidade=1,
            valor_unitario=produto.custo_centavos / 100,
            desconto_item=100,  # 100% de lucro
            imposto_item=0,
            ipi_item=0
        )
        print(f"✅ Item de teste criado: {item.descricao}")
    
    print(f"\n📋 Item testado: {item.descricao}")
    print(f"🎯 Percentual de lucro atual no banco: {item.desconto_item}%")
    
    # Simular o salvamento de um novo percentual
    print(f"\n🧪 TESTE 1: Salvando percentual 50%...")
    item.desconto_item = 50
    item.save()
    item.refresh_from_db()
    print(f"✅ Percentual após salvar: {item.desconto_item}%")
    
    print(f"\n🧪 TESTE 2: Salvando percentual 100%...")
    item.desconto_item = 100
    item.save()
    item.refresh_from_db()
    print(f"✅ Percentual após salvar: {item.desconto_item}%")
    
    print(f"\n🧪 TESTE 3: Salvando percentual 25.5%...")
    item.desconto_item = 25.5
    item.save()
    item.refresh_from_db()
    print(f"✅ Percentual após salvar: {item.desconto_item}%")
    
    # Verificar se está multiplicando por 10
    if item.desconto_item == 255.0:
        print(f"\n❌ PROBLEMA CONFIRMADO: 25.5% virou {item.desconto_item}%")
    elif item.desconto_item == 25.5:
        print(f"\n✅ CORREÇÃO FUNCIONANDO: Valor permaneceu {item.desconto_item}%")
    
    # Cleanup - remover item de teste se criamos um
    if item.descricao.startswith("TESTE -"):
        item.delete()
        print(f"\n🗑️ Item de teste removido")

if __name__ == "__main__":
    testar_problema_percentual()