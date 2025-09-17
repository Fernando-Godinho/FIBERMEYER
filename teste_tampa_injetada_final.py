#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import django
import requests
import json

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def test_tampa_injetada_api():
    """Testa a API da Tampa Injetada via requisição HTTP"""
    
    print("=== TESTE API TAMPA INJETADA ===")
    
    # Dados de teste
    dados_teste = {
        "tipo_calculo": "tampa_injetada",
        "nome_tampa": "Tampa Injetada Teste 50x40cm",
        "largura": 500,  # 50cm
        "comprimento": 400,  # 40cm
        "perda": 5,
        "grade_tipo": "GI25X38X38MM",
        "chapa_ev": True,  # Com chapa EV especial
        "quadro_u4": True,  # Com quadro U4
        "alca": False,  # Sem alça
        "tempo_proc": 1.5,
        "tempo_mtg": 1.0
    }
    
    try:
        # Fazer requisição para a API
        url = "http://localhost:8000/api/calcular_grade/"
        response = requests.post(url, json=dados_teste, timeout=10)
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ API respondeu com sucesso!")
            print(f"📦 Produto: {resultado['nome_produto']}")
            print(f"💰 Custo Total: R$ {resultado['custo_total']/100:.2f}")
            print(f"⚖️ Peso Total: {resultado['peso_total']:.2f} kg")
            print(f"📐 Área Tampa: {resultado['area_tampa']:.2f} m²")
            
            print("\n🧩 COMPONENTES DETALHADOS:")
            print("-" * 80)
            for i, comp in enumerate(resultado['componentes'], 1):
                print(f"{i}. {comp['nome']}")
                print(f"   📋 Descrição: {comp.get('descricao_produto', 'N/A')}")
                print(f"   📊 Quantidade: {comp['quantidade']:.3f} {comp['unidade']}")
                print(f"   💵 Unitário: R$ {comp['custo_unitario']/100:.2f}")
                print(f"   💰 Total: R$ {comp['custo_total']/100:.2f}")
                print()
                
            # Verificar componentes esperados
            componentes_nomes = [comp['nome'] for comp in resultado['componentes']]
            
            print("🔍 VERIFICAÇÕES:")
            print(f"✅ Grade Injetada: {'Sim' if any('GRADE INJETADA' in nome for nome in componentes_nomes) else '❌ Não'}")
            print(f"✅ Cola Estrutural: {'Sim' if any('COLA ESTRUTURAL' in nome for nome in componentes_nomes) else '❌ Não'}")
            print(f"✅ Chapa EV: {'Sim' if any('EV' in nome or 'Chapa' in nome for nome in componentes_nomes) else '❌ Não'}")
            print(f"✅ Quadro U4: {'Sim' if any('U4' in nome for nome in componentes_nomes) else '❌ Não'}")
            print(f"❌ Alça: {'Sim' if any('ALCA' in nome for nome in componentes_nomes) else 'Não (esperado)'}")
            print(f"✅ Mão de Obra: {'Sim' if any('MÃO DE OBRA' in nome for nome in componentes_nomes) else '❌ Não'}")
            
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def verificar_produtos_necessarios():
    """Verifica se todos os produtos necessários existem no banco"""
    
    print("\n=== VERIFICAÇÃO PRODUTOS NECESSÁRIOS ===")
    
    # Verificar grade injetada
    grades = MP_Produtos.objects.filter(descricao__icontains='GRADE INJETADA')
    print(f"📦 Grades Injetadas encontradas: {grades.count()}")
    for grade in grades:
        print(f"   • ID {grade.id}: {grade.descricao} - R$ {grade.custo_centavos/100:.2f}")
    
    # Verificar cola
    cola = MP_Produtos.objects.filter(id=1183).first()
    if cola:
        print(f"🧴 Cola ID 1183: {cola.descricao} - R$ {cola.custo_centavos/100:.2f}")
    else:
        print("❌ Cola ID 1183 não encontrada!")
    
    # Verificar chapa 2.5mm
    chapa = MP_Produtos.objects.filter(descricao__icontains='Chapa Lisa 2,5mm').first()
    if chapa:
        print(f"📋 Chapa 2.5mm: {chapa.descricao} - R$ {chapa.custo_centavos/100:.2f}")
    else:
        print("❌ Chapa 2.5mm não encontrada!")

if __name__ == "__main__":
    verificar_produtos_necessarios()
    test_tampa_injetada_api()
