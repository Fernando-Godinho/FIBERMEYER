#!/usr/bin/env python
"""
Script para testar especificamente a perda de 3% no véu
"""
import os
import sys
import django

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos
from main.views import calcular_custos_template

def test_veu_loss():
    print("=== TESTE DA PERDA DE 3% NO VÉU ===\n")
    
    # Buscar o template
    template = ProdutoTemplate.objects.filter(nome='Novo Perfil').first()
    if not template:
        print("Template 'Novo Perfil' não encontrado!")
        return
    
    # Buscar o preço do véu
    produto_veu = MP_Produtos.objects.filter(descricao='Véu').first()
    if not produto_veu:
        print("Produto 'Véu' não encontrado!")
        return
    
    preco_veu = produto_veu.custo_centavos / 100
    print(f"Preço do Véu: R$ {preco_veu:.2f} por kg")
    
    # Parâmetros de teste
    parametros_teste = {
        'roving_4400': '0',      # Sem roving para simplificar
        'manta_300': '0',        # Sem manta para simplificar  
        'veu': '1.0',            # 1.0 kg de véu
        'peso_m': '5.0',         # 5.0 kg/m peso total
        'descricao': 'Teste perda véu'
    }
    
    print(f"\nParâmetros de teste:")
    print(f"  Véu solicitado: {parametros_teste['veu']} kg")
    print(f"  Quantidade com perda de 3%: {float(parametros_teste['veu']) * 1.03:.3f} kg")
    
    # Realizar cálculo
    resultado = calcular_custos_template(template, parametros_teste)
    
    if 'erro' in resultado:
        print(f"\nERRO: {resultado['erro']}")
        return
    
    # Encontrar o componente véu no resultado
    componente_veu = None
    for comp in resultado['componentes']:
        if 'véu' in comp['nome'].lower():
            componente_veu = comp
            break
    
    if componente_veu:
        print(f"\n=== RESULTADO DO CÁLCULO DO VÉU ===")
        print(f"Quantidade calculada: {componente_veu['quantidade']:.3f} kg")
        print(f"Preço unitário: R$ {componente_veu['custo_unitario']:.2f}")
        print(f"Custo total do véu: R$ {componente_veu['custo_total']:.2f}")
        
        # Verificar os cálculos
        quantidade_esperada = float(parametros_teste['veu']) * 1.03
        custo_esperado = quantidade_esperada * preco_veu
        
        print(f"\n=== VERIFICAÇÃO ===")
        print(f"Quantidade esperada (1.0 × 1.03): {quantidade_esperada:.3f} kg")
        print(f"Custo esperado ({quantidade_esperada:.3f} × {preco_veu:.2f}): R$ {custo_esperado:.2f}")
        
        # Verificar se os valores batem
        if abs(componente_veu['quantidade'] - quantidade_esperada) < 0.001:
            print("✅ Quantidade calculada corretamente!")
        else:
            print("❌ Erro na quantidade calculada!")
            
        if abs(componente_veu['custo_total'] - custo_esperado) < 0.01:
            print("✅ Custo calculado corretamente!")
        else:
            print("❌ Erro no custo calculado!")
            
        print(f"\n🎯 PERDA DE 3% APLICADA: {((componente_veu['quantidade'] / float(parametros_teste['veu'])) - 1) * 100:.1f}%")
    else:
        print("\n❌ Componente véu não encontrado no resultado!")

if __name__ == '__main__':
    test_veu_loss()
