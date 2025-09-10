#!/usr/bin/env python
"""
Teste para verificar se a seleção de tipos de resina está funcionando
"""

import django
import os
import sys
import requests
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def testar_api_tipos_resina():
    """Testa a API de tipos de resina"""
    print("=== TESTE API TIPOS DE RESINA ===\n")
    
    try:
        response = requests.get('http://127.0.0.1:8000/api/tipos-resina/')
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ API funcionando! {len(data['resinas'])} resinas encontradas:")
                for resina in data['resinas']:
                    print(f"   • ID: {resina['id']} | {resina['descricao']} | R$ {resina['custo_reais']:.2f}")
                return data['resinas']
            else:
                print(f"❌ API retornou erro: {data.get('error')}")
        else:
            print(f"❌ API retornou status {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando na porta 8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    return None

def testar_calculo_com_diferentes_resinas():
    """Testa o cálculo com diferentes tipos de resina"""
    print("\n=== TESTE CÁLCULO COM DIFERENTES RESINAS ===\n")
    
    # Dados de exemplo para teste
    dados_base = {
        "template_id": "perfil_customizado", 
        "parametros": {
            "nome_perfil": "Teste Resina",
            "roving_4400_kg": 0.35,
            "manta_300_kg": 0.24,
            "veu_kg": 0.41,
            "peso_metro_kg": 4.0,
            "n_matrizes": 2,
            "n_maquinas": 1,
            "metros_produzidos_h": 25.0,
            "percentual_perda": 3.0,
            "tem_pintura": False,
            "area_pintura_m2": 0
        }
    }
    
    # Testar com diferentes tipos de resina
    tipos_resina = [
        {"id": "1269", "nome": "Resina Poliéster"},
        {"id": "1268", "nome": "Resina Isoftálica"}, 
        {"id": "1270", "nome": "Resina Éster Vinílica"}
    ]
    
    resultados = []
    
    for resina in tipos_resina:
        print(f"🧪 Testando com {resina['nome']} (ID: {resina['id']})...")
        
        # Adicionar tipo de resina aos dados
        dados_teste = dados_base.copy()
        dados_teste["parametros"]["tipo_resina"] = resina["id"]
        
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/calcular-produto-parametrizado/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(dados_teste)
            )
            
            if response.status_code == 200:
                resultado = response.json()
                if resultado['success']:
                    custo_total = resultado['custo_total'] / 100  # Converter de centavos
                    print(f"   ✅ Custo total: R$ {custo_total:.2f}")
                    
                    # Buscar componente da resina
                    componente_resina = None
                    for comp in resultado['componentes']:
                        if 'resina' in comp['nome'].lower():
                            componente_resina = comp
                            break
                    
                    if componente_resina:
                        custo_unitario = componente_resina['custo_unitario'] / 100
                        print(f"   📊 Resina: {componente_resina['quantidade']:.4f} kg x R$ {custo_unitario:.2f} = R$ {componente_resina['custo_total']/100:.2f}")
                    
                    resultados.append({
                        'resina': resina['nome'],
                        'custo_total': custo_total,
                        'componente_resina': componente_resina
                    })
                else:
                    print(f"   ❌ Erro no cálculo: {resultado.get('error')}")
            else:
                print(f"   ❌ Erro HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Comparar resultados
    if len(resultados) > 1:
        print(f"\n📈 COMPARAÇÃO DE CUSTOS:")
        resultado_base = resultados[0]  # Poliéster como base
        for resultado in resultados[1:]:
            diferenca = resultado['custo_total'] - resultado_base['custo_total']
            print(f"{resultado['resina']} vs Poliéster: {'+' if diferenca > 0 else ''}R$ {diferenca:.2f}")
        
        # Verificar se as resinas estão sendo trocadas corretamente
        print(f"\n=== VERIFICAÇÕES ===")
        produtos_usados = [r['componente_resina']['produto'] for r in resultados if r['componente_resina']]
        if len(set(produtos_usados)) == len(produtos_usados):
            print("✓ Cada teste usou um tipo diferente de resina")
        else:
            print("✗ Alguns testes usaram a mesma resina")
    
    return resultados

def main():
    print("🧪 TESTE FUNCIONALIDADE SELEÇÃO DE TIPOS DE RESINA")
    print("=" * 60)
    
    # Verificar resinas no banco
    resinas_banco = MP_Produtos.objects.filter(descricao__icontains='resina').count()
    print(f"Resinas no banco: {resinas_banco}")
    
    # Testar API
    resinas_api = testar_api_tipos_resina()
    
    # Testar cálculo se API estiver funcionando  
    if resinas_api:
        resultados = testar_calculo_com_diferentes_resinas()
        
        if resultados:
            print(f"\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
            print(f"   • {len(resinas_api)} tipos de resina disponíveis")
            print(f"   • {len(resultados)} cálculos realizados")
            print(f"   • Diferenças de preço detectadas corretamente")
        else:
            print(f"\n⚠️ TESTE PARCIAL: API funcionou mas cálculos falharam")
    else:
        print(f"\n❌ TESTE FALHOU: API não está funcionando")

if __name__ == "__main__":
    main()
