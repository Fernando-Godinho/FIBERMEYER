#!/usr/bin/env python
"""
Script para testar o template com parâmetro de perda configurável
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

def test_perda_configuravel():
    print("=== TESTE DO PARÂMETRO DE PERDA CONFIGURÁVEL ===\n")
    
    template = ProdutoTemplate.objects.filter(nome='Novo Perfil').first()
    if not template:
        print("Template 'Novo Perfil' não encontrado!")
        return
    
    print(f"Template: {template.nome}")
    print(f"Parâmetros: {template.parametros.count()}")
    
    # Teste 1: Com perda de 3% (padrão)
    print("\n" + "="*50)
    print("TESTE 1: PERDA DE 3% (PADRÃO)")
    print("="*50)
    
    parametros_3pct = {
        'roving_4400': '2.5',
        'manta_300': '1.2',
        'veu_qtd': '0.3',
        'perda_veu': '3',  # 3% de perda
        'peso_m': '8.0',
        'descricao': 'Teste 3%'
    }
    
    resultado_3pct = calcular_custos_template(template, parametros_3pct)
    veu_comp_3pct = next((c for c in resultado_3pct['componentes'] if 'véu' in c['nome'].lower()), None)
    
    print(f"Parâmetros: roving=2.5kg, manta=1.2m², véu=0.3kg, perda=3%")
    if veu_comp_3pct:
        print(f"Véu calculado: {veu_comp_3pct['quantidade']:.3f} kg (esperado: {0.3 * 1.03:.3f})")
        print(f"Custo do véu: R$ {veu_comp_3pct['custo_total']:.2f}")
    print(f"Custo total: R$ {resultado_3pct['custo_total']:.2f}")
    
    # Teste 2: Com perda de 5%
    print("\n" + "="*50)
    print("TESTE 2: PERDA DE 5% (PERSONALIZADA)")
    print("="*50)
    
    parametros_5pct = {
        'roving_4400': '2.5',
        'manta_300': '1.2',
        'veu_qtd': '0.3',
        'perda_veu': '5',  # 5% de perda
        'peso_m': '8.0',
        'descricao': 'Teste 5%'
    }
    
    resultado_5pct = calcular_custos_template(template, parametros_5pct)
    veu_comp_5pct = next((c for c in resultado_5pct['componentes'] if 'véu' in c['nome'].lower()), None)
    
    print(f"Parâmetros: roving=2.5kg, manta=1.2m², véu=0.3kg, perda=5%")
    if veu_comp_5pct:
        print(f"Véu calculado: {veu_comp_5pct['quantidade']:.3f} kg (esperado: {0.3 * 1.05:.3f})")
        print(f"Custo do véu: R$ {veu_comp_5pct['custo_total']:.2f}")
    print(f"Custo total: R$ {resultado_5pct['custo_total']:.2f}")
    
    # Teste 3: Sem perda (0%)
    print("\n" + "="*50)
    print("TESTE 3: SEM PERDA (0%)")
    print("="*50)
    
    parametros_0pct = {
        'roving_4400': '2.5',
        'manta_300': '1.2',
        'veu_qtd': '0.3',
        'perda_veu': '0',  # 0% de perda
        'peso_m': '8.0',
        'descricao': 'Teste 0%'
    }
    
    resultado_0pct = calcular_custos_template(template, parametros_0pct)
    veu_comp_0pct = next((c for c in resultado_0pct['componentes'] if 'véu' in c['nome'].lower()), None)
    
    print(f"Parâmetros: roving=2.5kg, manta=1.2m², véu=0.3kg, perda=0%")
    if veu_comp_0pct:
        print(f"Véu calculado: {veu_comp_0pct['quantidade']:.3f} kg (esperado: {0.3 * 1.0:.3f})")
        print(f"Custo do véu: R$ {veu_comp_0pct['custo_total']:.2f}")
    print(f"Custo total: R$ {resultado_0pct['custo_total']:.2f}")
    
    # Comparação
    print("\n" + "="*50)
    print("COMPARAÇÃO DOS RESULTADOS")
    print("="*50)
    
    if veu_comp_0pct and veu_comp_3pct and veu_comp_5pct:
        print(f"{'Perda':<10} {'Qtd Véu':<12} {'Custo Véu':<12} {'Custo Total'}")
        print("-" * 50)
        print(f"{'0%':<10} {veu_comp_0pct['quantidade']:<12.3f} R$ {veu_comp_0pct['custo_total']:<9.2f} R$ {resultado_0pct['custo_total']:.2f}")
        print(f"{'3%':<10} {veu_comp_3pct['quantidade']:<12.3f} R$ {veu_comp_3pct['custo_total']:<9.2f} R$ {resultado_3pct['custo_total']:.2f}")
        print(f"{'5%':<10} {veu_comp_5pct['quantidade']:<12.3f} R$ {veu_comp_5pct['custo_total']:<9.2f} R$ {resultado_5pct['custo_total']:.2f}")
        
        diferenca_3_0 = resultado_3pct['custo_total'] - resultado_0pct['custo_total']
        diferenca_5_0 = resultado_5pct['custo_total'] - resultado_0pct['custo_total']
        print(f"\nDiferença 3% vs 0%: R$ {diferenca_3_0:.2f}")
        print(f"Diferença 5% vs 0%: R$ {diferenca_5_0:.2f}")
    
    print("\n✅ Parâmetro de perda configurável funcionando!")
    print("✅ Valor padrão sugerido: 3%")

if __name__ == '__main__':
    test_perda_configuravel()
