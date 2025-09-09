#!/usr/bin/env python
"""
Script para adicionar dados iniciais de Mão de Obra
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MaoObra

def add_mao_obra_inicial():
    """Adiciona os dados iniciais de mão de obra"""
    
    mao_obra_dados = [
        {
            'nome': 'MÃO DE OBRA PULTRUSÃO',
            'descricao': 'Mão de obra especializada para processos de pultrusão',
            'valor_centavos': 9976258,  # R$ 99.762,58
            'unidade': 'HORA',
            'categoria': 'Pultrusão',
            'ativo': True
        },
        {
            'nome': 'MÃO DE OBRA Processamento/Montagem',
            'descricao': 'Mão de obra para processamento e montagem de produtos',
            'valor_centavos': 6579,  # R$ 65,79
            'unidade': 'HORA',
            'categoria': 'Processamento/Montagem',
            'ativo': True
        },
        {
            'nome': 'MÃO DE OBRA Operações',
            'descricao': 'Mão de obra para operações gerais',
            'valor_centavos': 8382,  # R$ 83,82
            'unidade': 'HORA',
            'categoria': 'Operações',
            'ativo': True
        }
    ]
    
    print("🔧 Adicionando dados iniciais de Mão de Obra...")
    
    for dados in mao_obra_dados:
        mao_obra, criado = MaoObra.objects.get_or_create(
            nome=dados['nome'],
            defaults=dados
        )
        
        if criado:
            print(f"✅ Criado: {mao_obra.nome} - R$ {mao_obra.valor_real:.2f}/{mao_obra.unidade}")
        else:
            print(f"⚠️  Já existe: {mao_obra.nome}")
    
    print(f"\n📊 Total de registros de Mão de Obra: {MaoObra.objects.count()}")
    print("✅ Processo concluído!")

if __name__ == '__main__':
    add_mao_obra_inicial()
