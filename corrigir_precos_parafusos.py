#!/usr/bin/env python3
"""
Script para corrigir os preços dos parafusos e porcas para degraus
"""

import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def corrigir_precos_parafusos_porcas():
    # Correções de preços conforme especificação
    correcoes = [
        {
            'descricao': 'PARAF-SXT-M6X40-AI304',
            'custo_novo': 400,  # R$ 4,00
            'custo_esperado': 45  # R$ 0,45 atual
        },
        {
            'descricao': 'PARAF-SXT-M6X60-AI304', 
            'custo_novo': 200,  # R$ 2,00
            'custo_esperado': 6149  # R$ 61,49 atual
        },
        {
            'descricao': 'POR-SXT-M6-AI304',
            'custo_novo': 600,  # R$ 6,00
            'custo_esperado': 138  # R$ 1,38 atual
        }
    ]
    
    produtos_corrigidos = []
    
    for correcao in correcoes:
        # Buscar o produto
        produtos = MP_Produtos.objects.filter(descricao__icontains=correcao['descricao'])
        
        if not produtos.exists():
            print(f"❌ Produto '{correcao['descricao']}' não encontrado!")
            continue
            
        # Usar o primeiro produto encontrado (sem travante para porca)
        if 'POR-SXT-M6-AI304' in correcao['descricao']:
            produto = produtos.filter(descricao__exact='POR-SXT-M6-AI304 - ').first()
        else:
            produto = produtos.first()
            
        if not produto:
            print(f"❌ Produto específico '{correcao['descricao']}' não encontrado!")
            continue
        
        print(f"📝 Corrigindo {produto.descricao}:")
        print(f"   Preço atual: R$ {produto.custo_centavos/100:.2f}")
        print(f"   Preço novo: R$ {correcao['custo_novo']/100:.2f}")
        
        # Atualizar o preço
        produto.custo_centavos = correcao['custo_novo']
        produto.save()
        
        print(f"   ✅ Atualizado com sucesso!")
        produtos_corrigidos.append(produto)
    
    print("\n=== RESUMO DAS CORREÇÕES ===")
    for produto in produtos_corrigidos:
        print(f"ID: {produto.id} | {produto.descricao} | R$ {produto.custo_centavos/100:.2f}")
    
    return produtos_corrigidos

if __name__ == "__main__":
    corrigir_precos_parafusos_porcas()
