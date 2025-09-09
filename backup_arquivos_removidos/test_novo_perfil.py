#!/usr/bin/env python
"""
Script para testar o cálculo do template 'Novo Perfil' com roving, manta e véu incluídos
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

def test_novo_perfil_calculation():
    print("=== TESTE DE CÁLCULO DO TEMPLATE 'NOVO PERFIL' ===\n")
    
    # Buscar o template
    template = ProdutoTemplate.objects.filter(nome='Novo Perfil').first()
    if not template:
        print("Template 'Novo Perfil' não encontrado!")
        return
    
    print(f"Template encontrado: {template.nome}")
    print(f"Componentes cadastrados: {template.componentes.count()}")
    
    # Parâmetros de teste
    parametros_teste = {
        'roving_4400': '2.5',    # 2.5 kg de roving
        'manta_300': '1.2',      # 1.2 kg de manta  
        'veu': '0.3',            # 0.3 kg de véu
        'peso_m': '8.0',         # 8.0 kg/m peso total
        'descricao': 'Perfil de teste'
    }
    
    print(f"\nParâmetros de teste:")
    for param, valor in parametros_teste.items():
        print(f"  {param}: {valor}")
    
    # Realizar cálculo
    resultado = calcular_custos_template(template, parametros_teste)
    
    if 'erro' in resultado:
        print(f"\nERRO: {resultado['erro']}")
        return
    
    print(f"\n=== RESULTADO DO CÁLCULO ===")
    print(f"Custo total: R$ {resultado['custo_total']:.2f}")
    print(f"Número de componentes: {len(resultado['componentes'])}")
    
    print(f"\n=== DETALHES DOS COMPONENTES ===")
    custo_roving_manta_veu = 0
    custo_outros = 0
    
    for comp in resultado['componentes']:
        custo = comp['custo_total']
        print(f"{comp['nome']:20} | Qtd: {comp['quantidade']:8.3f} {comp['unidade']} | Custo Unit: R$ {comp['custo_unitario']:6.2f} | Total: R$ {custo:8.2f}")
        
        # Separar custos de roving/manta/véu dos outros
        if comp['nome'] in ['Roving 4400', 'Manta 300', 'Véu']:
            custo_roving_manta_veu += custo
        else:
            custo_outros += custo
    
    print(f"\n=== RESUMO DE CUSTOS ===")
    print(f"Roving + Manta + Véu: R$ {custo_roving_manta_veu:.2f}")
    print(f"Outros componentes:   R$ {custo_outros:.2f}")
    print(f"TOTAL:                R$ {resultado['custo_total']:.2f}")
    
    # Verificar se as quantidades estão corretas
    print(f"\n=== VERIFICAÇÃO DAS QUANTIDADES ===")
    peso_reforcos = float(parametros_teste['roving_4400']) + float(parametros_teste['manta_300']) + float(parametros_teste['veu'])
    peso_matriz = float(parametros_teste['peso_m']) - peso_reforcos
    print(f"Peso dos reforços (roving+manta+véu): {peso_reforcos:.1f} kg")
    print(f"Peso da matriz e aditivos: {peso_matriz:.1f} kg")
    print(f"Peso total: {parametros_teste['peso_m']} kg")

if __name__ == '__main__':
    test_novo_perfil_calculation()
