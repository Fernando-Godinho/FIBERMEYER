#!/usr/bin/env python
"""
Script para adicionar produtos de exemplo para testar a funcionalidade de duplicação
"""
import os
import sys
import django
from datetime import datetime

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def add_sample_products():
    """Adiciona produtos de exemplo se não existirem"""
    
    sample_products = [
        {
            'descricao': 'Barra de Aço CA-50 12mm',
            'custo_centavos': 2500,  # R$ 25,00
            'peso_und': 0.888,
            'unidade': 'M',
            'referencia': 'Gerdau'
        },
        {
            'descricao': 'Chapa de Aço 3mm x 1200mm x 2400mm',
            'custo_centavos': 45000,  # R$ 450,00
            'peso_und': 67.680,
            'unidade': 'UN',
            'referencia': 'Usiminas'
        },
        {
            'descricao': 'Tubo Quadrado 50x50x2mm',
            'custo_centavos': 3200,  # R$ 32,00
            'peso_und': 3.760,
            'unidade': 'M',
            'referencia': 'ArcelorMittal'
        },
        {
            'descricao': 'Parafuso Sextavado M12x50',
            'custo_centavos': 450,  # R$ 4,50
            'peso_und': 0.025,
            'unidade': 'UN',
            'referencia': 'Votorantim'
        },
        {
            'descricao': 'Solda MIG ER70S-6 1.2mm',
            'custo_centavos': 1800,  # R$ 18,00
            'peso_und': 1.000,
            'unidade': 'KG',
            'referencia': 'Belgo'
        }
    ]
    
    # Verificar se já existem produtos
    if MP_Produtos.objects.count() > 0:
        print(f"Já existem {MP_Produtos.objects.count()} produtos no banco.")
        response = input("Deseja adicionar os produtos de exemplo mesmo assim? (s/n): ")
        if response.lower() != 's':
            print("Operação cancelada.")
            return
    
    # Adicionar produtos
    created_count = 0
    for product_data in sample_products:
        # Verificar se já existe produto com a mesma descrição
        if not MP_Produtos.objects.filter(descricao=product_data['descricao']).exists():
            product_data['data_revisao'] = datetime.now()
            MP_Produtos.objects.create(**product_data)
            created_count += 1
            print(f"✓ Produto criado: {product_data['descricao']}")
        else:
            print(f"⚠ Produto já existe: {product_data['descricao']}")
    
    print(f"\n{created_count} produto(s) adicionado(s) com sucesso!")
    print(f"Total de produtos no banco: {MP_Produtos.objects.count()}")

if __name__ == '__main__':
    add_sample_products()
