#!/usr/bin/env python3
"""
Script para adicionar os perfis de reforço E e F no banco de dados
"""

import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def adicionar_perfis_reforco():
    produtos_para_criar = [
        {
            'descricao': 'PERFIL F 4"',
            'custo_centavos': 1970,  # R$ 19,70
            'tipo': 'F',
            'uso': 'I38'
        },
        {
            'descricao': 'E - 4\'x1.3/16\' #3/16\'',
            'custo_centavos': 1473,  # R$ 14,73
            'tipo': 'E',
            'uso': 'I25'
        }
    ]
    
    produtos_criados = []
    
    for produto_info in produtos_para_criar:
        # Verificar se já existe
        produto_existente = MP_Produtos.objects.filter(descricao__icontains=produto_info['descricao'])
        
        if produto_existente.exists():
            print(f"❌ Produto '{produto_info['descricao']}' já existe!")
            produto = produto_existente.first()
            print(f"   ID: {produto.id} | {produto.descricao} | R$ {produto.custo_centavos/100:.2f}")
            produtos_criados.append(produto)
            continue
        
        # Criar o produto
        novo_produto = MP_Produtos.objects.create(
            descricao=produto_info['descricao'],
            custo_centavos=produto_info['custo_centavos'],
            peso_und=0.3,  # Peso estimado em kg/m
            unidade='m',
            categoria='PERFIS',
            subcategoria='REFORCO',
            tipo_produto='MATERIAL'
        )
        
        print(f"✅ Produto '{produto_info['descricao']}' criado com sucesso!")
        print(f"   ID: {novo_produto.id} | {novo_produto.descricao} | R$ {novo_produto.custo_centavos/100:.2f}")
        print(f"   Uso: {produto_info['uso']} | Tipo: {produto_info['tipo']}")
        produtos_criados.append(novo_produto)
    
    print("\n=== RESUMO DOS PERFIS DE REFORÇO ===")
    for produto in produtos_criados:
        print(f"ID: {produto.id} | {produto.descricao} | R$ {produto.custo_centavos/100:.2f}")
    
    return produtos_criados

if __name__ == "__main__":
    adicionar_perfis_reforco()
