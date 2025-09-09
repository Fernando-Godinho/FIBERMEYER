#!/usr/bin/env python
"""
Script para verificar erro no cálculo
"""
import os
import sys
import django

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate
from main.views import calcular_custos_template

def debug_calculo():
    print("=== DEBUG DO CÁLCULO ===\n")
    
    template = ProdutoTemplate.objects.filter(nome='Novo Perfil').first()
    
    parametros = {
        'roving_4400': '2.5',
        'manta_300': '1.2',
        'veu_qtd': '0.3',
        'perda_veu': '3',
        'peso_m': '8.0',
        'descricao': 'Debug'
    }
    
    print("Parâmetros:", parametros)
    
    resultado = calcular_custos_template(template, parametros)
    print("\nResultado:", resultado)
    
    if 'erro' in resultado:
        print(f"ERRO: {resultado['erro']}")

if __name__ == '__main__':
    debug_calculo()
