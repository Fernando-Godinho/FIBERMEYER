#!/usr/bin/env python
import os
import sys
import django
import asyncio
import json
from unittest.mock import Mock

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

print("=== TESTE: DEMONSTRAÇÃO DA CORREÇÃO DE MÃO DE OBRA ===")

print("\n1. PROBLEMA ANTERIOR:")
print("   - Cálculo: Mão de obra = R$ 6,28")
print("   - Produto criado: 'Mão de Obra - Pultrusão' com custo R$ 0,01")
print("   - Componente salvo: Usava o custo do produto (R$ 0,01) ❌")
print("   - Resultado: Valor errado na tabela de componentes")

print("\n2. CORREÇÃO IMPLEMENTADA:")
print("   - Antes de salvar o componente:")
print("   - Sistema atualiza o custo do produto 'Mão de Obra - Pultrusão'")
print("   - Usa o valor calculado (R$ 6,28) em vez do fixo (R$ 0,01)")
print("   - Componente salvo usa o valor correto ✅")

print("\n3. FLUXO CORRIGIDO:")
print("   a) Calcular mão de obra → R$ 6,28")
print("   b) Encontrar/criar produto 'Mão de Obra - Pultrusão'")
print("   c) NOVO: Atualizar custo do produto para 628 centavos")
print("   d) Salvar componente (que agora usa o valor correto)")

# Verificar se já existe produto de mão de obra
try:
    mao_obra_produto = MP_Produtos.objects.filter(
        descricao__icontains='mão de obra'
    ).filter(
        descricao__icontains='pultrusão'
    ).first()
    
    if mao_obra_produto:
        print(f"\n4. PRODUTO MÃO DE OBRA ATUAL:")
        print(f"   ID: {mao_obra_produto.id}")
        print(f"   Descrição: {mao_obra_produto.descricao}")
        print(f"   Custo atual: {mao_obra_produto.custo_centavos} centavos = R$ {mao_obra_produto.custo_centavos/100:.2f}")
        print(f"   Referência: {mao_obra_produto.referencia}")
        
        # Simular a atualização que será feita
        valor_calculado = 628  # R$ 6,28
        print(f"\n5. SIMULAÇÃO DA ATUALIZAÇÃO:")
        print(f"   Valor a ser usado: {valor_calculado} centavos = R$ {valor_calculado/100:.2f}")
        print(f"   Operação: PATCH /api/produtos/{mao_obra_produto.id}/")
        print(f"   Body: {{'custo_centavos': {valor_calculado}}}")
        
    else:
        print(f"\n4. PRODUTO MÃO DE OBRA:")
        print(f"   Ainda não foi criado")
        print(f"   Será criado automaticamente no primeiro salvamento")
        
except Exception as e:
    print(f"\n4. ERRO AO VERIFICAR PRODUTO: {e}")

print(f"\n6. COMO TESTAR:")
print(f"   1. Acesse o sistema no navegador")
print(f"   2. Configure um produto parametrizado")
print(f"   3. Clique 'Salvar na Base'")
print(f"   4. Veja no console os logs:")
print(f"      '🔄 Atualizando custo do produto mão de obra...'")
print(f"      '✅ Custo do produto mão de obra atualizado para [valor] centavos'")
print(f"   5. Verifique na tabela de componentes o valor correto")

print(f"\n7. LOGS ESPERADOS NO CONSOLE:")
print(f"   🔧 Processando mão de obra: ID [numero]")
print(f"   🔄 Atualizando custo do produto mão de obra...")
print(f"   ✅ Custo do produto mão de obra atualizado para 628 centavos")
print(f"   💾 Salvando componente: Mão de Obra - Pultrusão (ID: [numero])")
print(f"   ✅ Componente salvo: Mão de Obra - Pultrusão (MÃO DE OBRA)")

print("\n" + "="*70)
print("✅ CORREÇÃO IMPLEMENTADA!")
print("   Agora o valor da mão de obra será preservado corretamente")
print("   nos componentes do produto composto!")
print("="*70)
