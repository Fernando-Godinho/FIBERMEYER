#!/usr/bin/env python3
"""
Teste específico para RS - Industrialização - Contribuinte
"""

import requests

def testar_rs_especifico():
    print("=== TESTE: RS - INDUSTRIALIZAÇÃO - CONTRIBUINTE ===\n")
    
    # Consultar base
    response = requests.get('http://127.0.0.1:8000/api/impostos/')
    impostos = response.json()
    
    # Encontrar RS - ICMS Interno
    rs_interno = next((i for i in impostos if i['nome'] == 'RS - ICMS Interno'), None)
    
    if rs_interno:
        percentual = float(rs_interno['aliquota'])
        print(f"🎯 RESPOSTA: {percentual}%")
        print(f"📋 Imposto usado: {rs_interno['nome']}")
        print(f"💡 Lógica: RS + INDUSTRIALIZAÇÃO + CONTRIBUINTE = ICMS Interno")
        
        # Verificar se está correto conforme tabela
        if abs(percentual - 12.0) < 0.01:  # Considerar pequenas diferenças de float
            print("✅ CORRETO conforme tabela de referência!")
        else:
            print(f"❌ INCORRETO - deveria ser 12.0%")
    else:
        print("❌ Imposto não encontrado!")
    
    print(f"\n📊 Mapeamento usado:")
    print(f"   Estado: RS")
    print(f"   Tipo de Venda: REVENDA (= Industrialização)")
    print(f"   Cliente: CONTRIBUINTE")
    print(f"   Resultado: ICMS Interno = {float(rs_interno['aliquota']) if rs_interno else 'N/A'}%")

if __name__ == "__main__":
    testar_rs_especifico()