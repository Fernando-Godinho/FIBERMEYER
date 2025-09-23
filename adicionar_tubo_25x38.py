#!/usr/bin/env python3
"""
Script para adicionar o Tubo Quadrado 25x38#3mm no banco de dados
"""

import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def adicionar_tubo_quadrado():
    # Verificar se já existe
    produto_existente = MP_Produtos.objects.filter(descricao__icontains='Tubo Quadrado 25x38#3mm')
    
    if produto_existente.exists():
        print("❌ Produto já existe!")
        produto = produto_existente.first()
        print(f"ID: {produto.id} | {produto.descricao} | R$ {produto.custo_centavos/100:.2f}")
        return produto
    
    # Criar o produto
    novo_produto = MP_Produtos.objects.create(
        descricao='Tubo Quadrado 25x38#3mm',
        custo_centavos=1198,  # R$ 11,98
        peso_und=0.8,  # Peso estimado em kg/m
        unidade='m',
        categoria='TUBOS',
        subcategoria='ESTRUTURAL',
        tipo_produto='MATERIAL'
    )
    
    print("✅ Produto criado com sucesso!")
    print(f"ID: {novo_produto.id} | {novo_produto.descricao} | R$ {novo_produto.custo_centavos/100:.2f}")
    return novo_produto

if __name__ == "__main__":
    adicionar_tubo_quadrado()
