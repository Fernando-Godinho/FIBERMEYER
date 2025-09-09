#!/usr/bin/env python3
"""
Teste direto da API com a nova fórmula de mão de obra
"""

import os
import django
import json
import requests
from decimal import Decimal

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

def testar_api_direta():
    print("="*70)
    print("🔗 TESTE DIRETO DA API - NOVA FÓRMULA MÃO DE OBRA")
    print("="*70)
    
    # Dados de teste
    dados_teste = {
        'template_id': 1,  # Usando ID fixo do template "Novo Perfil"
        'parametros': {
            'nome_perfil': 'Teste API Nova Fórmula',
            'roving_4400': '0.5',
            'manta_300': '0.3',
            'veu': '0.1',
            'peso_metro_kg': '1.2',
            'velocidade_m_h': '12',      # 12 m/h
            'num_matrizes': '2',         # 2 matrizes  
            'num_maquinas_utilizadas': '1',  # 1 máquina
            'percentual_perda': '5',
            'tem_pintura': False
        }
    }
    
    print("📋 DADOS DE TESTE:")
    print(f"   Velocidade: {dados_teste['parametros']['velocidade_m_h']} m/h")
    print(f"   N° Matrizes: {dados_teste['parametros']['num_matrizes']}")
    print(f"   N° Máquinas: {dados_teste['parametros']['num_maquinas_utilizadas']}")
    
    # Calcular resultado esperado
    mo_pultrusao = 9976258  # Valor da tabela ID=1
    velocidade = float(dados_teste['parametros']['velocidade_m_h'])
    matrizes = float(dados_teste['parametros']['num_matrizes'])
    maquinas = float(dados_teste['parametros']['num_maquinas_utilizadas'])
    
    numerador = (mo_pultrusao / 3) * maquinas
    denominador = velocidade * matrizes * 24 * 21 * 0.5
    custo_esperado = max(1, int(numerador / denominador))
    
    print(f"\n🧮 CÁLCULO ESPERADO:")
    print(f"   Numerador = ({mo_pultrusao:,} / 3) * {maquinas} = {numerador:,.2f}")
    print(f"   Denominador = {velocidade} * {matrizes} * 24 * 21 * 0.5 = {denominador:,.0f}")
    print(f"   Resultado = {numerador:,.2f} / {denominador:,.0f} = {numerador/denominador:.6f}")
    print(f"   Custo esperado = {custo_esperado} centavos = R$ {custo_esperado/100:.2f}")
    
    # Fazer chamada direta usando a função da view
    from main.views import calcular_produto_parametrizado
    from django.http import HttpRequest
    from django.test import RequestFactory
    
    try:
        # Criar request simulado
        factory = RequestFactory()
        request = factory.post('/api/calcular-produto-parametrizado/', 
                              data=json.dumps(dados_teste),
                              content_type='application/json')
        
        # Chamar a função
        response = calcular_produto_parametrizado(request)
        
        if response.status_code == 200:
            resultado = json.loads(response.content)
            print(f"\n✅ API FUNCIONANDO!")
            print(f"   Status: {response.status_code}")
            print(f"   Custo total: R$ {resultado.get('custo_total', 0)/100:.2f}")
            
            # Procurar componente de mão de obra
            mao_obra_encontrada = False
            for comp in resultado.get('componentes', []):
                if 'mão de obra' in comp['nome'].lower():
                    custo_real = comp['custo_total']
                    print(f"   Mão de obra encontrada: {comp['nome']}")
                    print(f"   Custo calculado: {custo_real} centavos = R$ {custo_real/100:.2f}")
                    
                    # Verificar se está próximo do esperado
                    diferenca = abs(custo_real - custo_esperado)
                    if diferenca <= 1:  # Tolerância de 1 centavo
                        print(f"   ✅ RESULTADO CORRETO! (diferença: {diferenca} centavos)")
                    else:
                        print(f"   ⚠️  Diferença: {diferenca} centavos")
                    
                    mao_obra_encontrada = True
                    break
            
            if not mao_obra_encontrada:
                print("   ❌ Componente de mão de obra não encontrado!")
                print("   Componentes disponíveis:")
                for comp in resultado.get('componentes', []):
                    print(f"     - {comp['nome']}: R$ {comp['custo_total']/100:.2f}")
            
            # Mostrar todos os componentes para debug
            print(f"\n📋 TODOS OS COMPONENTES:")
            total_verificacao = 0
            for comp in resultado.get('componentes', []):
                custo = comp['custo_total']
                total_verificacao += custo
                print(f"   {comp['nome']:<25} R$ {custo/100:>8.2f}")
            print(f"   {'TOTAL':<25} R$ {total_verificacao/100:>8.2f}")
            
        else:
            print(f"❌ ERRO NA API!")
            print(f"   Status: {response.status_code}")
            print(f"   Conteúdo: {response.content.decode()}")
            
    except Exception as e:
        print(f"❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ TESTE CONCLUÍDO!")
    print("="*70)

if __name__ == "__main__":
    testar_api_direta()
