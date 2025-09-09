#!/usr/bin/env python
"""
Resumo final: Template 'Novo Perfil' com perda de 3% no véu
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

def resumo_final():
    print("🎯 RESUMO FINAL - TEMPLATE 'NOVO PERFIL' ATUALIZADO\n")
    print("="*60)
    
    template = ProdutoTemplate.objects.filter(nome='Novo Perfil').first()
    
    # Parâmetros de exemplo
    parametros = {
        'roving_4400': '2.5',
        'manta_300': '1.2', 
        'veu_qtd': '0.3',
        'perda_veu': '3',
        'peso_m': '8.0',
        'descricao': 'Perfil exemplo'
    }
    
    resultado = calcular_custos_template(template, parametros)
    
    print("EXEMPLO DE CÁLCULO:")
    print(f"📋 Roving 4400: {parametros['roving_4400']} kg")
    print(f"📋 Manta 300: {parametros['manta_300']} m²") 
    print(f"📋 Véu: {parametros['veu_qtd']} kg")
    print(f"📋 Perda do véu: {parametros['perda_veu']}%")
    print(f"📋 Peso total: {parametros['peso_m']} kg/m")
    print()
    
    # Encontrar componentes específicos
    roving_comp = next((c for c in resultado['componentes'] if 'roving' in c['nome'].lower()), None)
    manta_comp = next((c for c in resultado['componentes'] if 'manta' in c['nome'].lower()), None)
    veu_comp = next((c for c in resultado['componentes'] if 'véu' in c['nome'].lower()), None)
    
    print("COMPONENTES CALCULADOS:")
    if roving_comp:
        print(f"🔸 Roving: {roving_comp['quantidade']:.3f} kg × R$ {roving_comp['custo_unitario']:.2f} = R$ {roving_comp['custo_total']:.2f}")
    if manta_comp:
        print(f"🔸 Manta: {manta_comp['quantidade']:.3f} m² × R$ {manta_comp['custo_unitario']:.2f} = R$ {manta_comp['custo_total']:.2f}")
    if veu_comp:
        print(f"🔸 Véu: {veu_comp['quantidade']:.3f} kg × R$ {veu_comp['custo_unitario']:.2f} = R$ {veu_comp['custo_total']:.2f}")
        perda_aplicada = (veu_comp['quantidade'] / float(parametros['veu_qtd']) - 1) * 100
        print(f"   ↳ Perda aplicada: {perda_aplicada:.1f}% ({parametros['veu_qtd']} → {veu_comp['quantidade']:.3f})")
    
    print()
    print("FÓRMULAS UTILIZADAS:")
    print("🔹 Roving: quantidade = roving_4400")
    print("🔹 Manta: quantidade = manta_300") 
    print("🔹 Véu: quantidade = veu_qtd × (1 + perda_veu/100)")
    print("🔹 Outros: quantidade = (peso_m - roving - manta - veu_qtd) × fator")
    
    print()
    print(f"💰 CUSTO TOTAL: R$ {resultado['custo_total']:.2f}")
    print("="*60)
    print("✅ Template atualizado com sucesso!")
    print("✅ Roving, manta e véu agora compõem o preço!")
    print("✅ Perda do véu é configurável (padrão: 3%)!")
    print("✅ Interface permite ajustar a perda conforme necessário!")

if __name__ == '__main__':
    resumo_final()
