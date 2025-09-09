#!/usr/bin/env python3
"""
Teste da nova fórmula de mão de obra
Fórmula: ((mo_pultrusao / 3) * n° de máquinas) / (VELOCIDADE M/H * N° MATRIZES * 24 * 21 * 0,5)
"""

import os
import django
import json

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MaoObra, ProdutoTemplate

def testar_nova_formula():
    print("="*70)
    print("🧪 TESTE DA NOVA FÓRMULA DE MÃO DE OBRA")
    print("="*70)
    
    # 1. Verificar valor base na tabela
    try:
        mao_obra_base = MaoObra.objects.get(id=1)
        mo_pultrusao = mao_obra_base.valor_centavos
        print(f"✅ Valor base (ID=1): {mo_pultrusao} centavos = R$ {mo_pultrusao/100:,.2f}")
        print(f"   Nome: {mao_obra_base.nome}")
    except MaoObra.DoesNotExist:
        print("❌ Erro: Não foi encontrado registro com ID=1 na tabela main_maoobra")
        return
    
    print(f"\n📋 NOVA FÓRMULA:")
    print(f"   ((mo_pultrusao / 3) * n° de máquinas) / (VELOCIDADE M/H * N° MATRIZES * 24 * 21 * 0,5)")
    
    # 2. Testar com dados de exemplo
    print(f"\n🧮 EXEMPLOS DE CÁLCULO:")
    
    exemplos = [
        {
            'nome': 'Perfil Padrão',
            'velocidade_m_h': 12.0,
            'num_matrizes': 2.0,
            'num_maquinas_utilizadas': 1.0
        },
        {
            'nome': 'Perfil Complexo',
            'velocidade_m_h': 8.0,
            'num_matrizes': 4.0,
            'num_maquinas_utilizadas': 2.0
        },
        {
            'nome': 'Perfil Simples',
            'velocidade_m_h': 20.0,
            'num_matrizes': 1.0,
            'num_maquinas_utilizadas': 1.0
        }
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n--- Exemplo {i}: {exemplo['nome']} ---")
        
        velocidade = exemplo['velocidade_m_h']
        matrizes = exemplo['num_matrizes']
        maquinas = exemplo['num_maquinas_utilizadas']
        
        # Aplicar a fórmula
        numerador = (mo_pultrusao / 3) * maquinas
        denominador = velocidade * matrizes * 24 * 21 * 0.5
        custo_raw = numerador / denominador
        custo_final = max(1, int(custo_raw)) if custo_raw > 0 else 0
        
        print(f"   Parâmetros:")
        print(f"     Velocidade: {velocidade} m/h")
        print(f"     N° Matrizes: {matrizes}")
        print(f"     N° Máquinas: {maquinas}")
        
        print(f"   Cálculo:")
        print(f"     Numerador = ({mo_pultrusao:,} / 3) * {maquinas} = {numerador:,.2f}")
        print(f"     Denominador = {velocidade} * {matrizes} * 24 * 21 * 0.5 = {denominador:,.0f}")
        print(f"     Resultado = {numerador:,.2f} / {denominador:,.0f} = {custo_raw:.8f}")
        print(f"     Custo final = {custo_final} centavos = R$ {custo_final/100:.2f}")
    
    print(f"\n🔄 TESTANDO VIA API:")
    
    # 3. Testar via API (simulação)
    from django.test import Client
    from django.urls import reverse
    import json
    
    # Buscar template "Novo Perfil" 
    try:
        template = ProdutoTemplate.objects.filter(nome__icontains='novo perfil').first()
        if not template:
            print("❌ Template 'Novo Perfil' não encontrado")
            return
            
        print(f"✅ Template encontrado: {template.nome} (ID: {template.id})")
        
        # Dados de teste
        dados_teste = {
            'template_id': template.id,
            'parametros': {
                'nome_perfil': 'Teste Nova Fórmula',
                'roving_4400': '0.5',
                'manta_300': '0.3',
                'veu': '0.1',
                'peso_metro_kg': '1.2',
                'velocidade_m_h': '10',
                'num_matrizes': '2',
                'num_maquinas_utilizadas': '1',
                'percentual_perda': '5',
                'tem_pintura': False
            }
        }
        
        # Simular chamada da API
        client = Client()
        response = client.post(
            '/api/calcular-produto-parametrizado/',
            data=json.dumps(dados_teste),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ API funcionando!")
            print(f"   Custo total: R$ {resultado.get('custo_total', 0)/100:.2f}")
            
            # Procurar componente de mão de obra
            for comp in resultado.get('componentes', []):
                if 'mão de obra' in comp['nome'].lower():
                    print(f"   Mão de obra: R$ {comp['custo_total']/100:.2f}")
        else:
            print(f"❌ Erro na API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste da API: {e}")
    
    print(f"\n✅ TESTE CONCLUÍDO!")
    print("="*70)

if __name__ == "__main__":
    testar_nova_formula()
