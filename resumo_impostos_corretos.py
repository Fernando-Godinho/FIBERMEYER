#!/usr/bin/env python
"""
Resumo das alíquotas de impostos corretas implementadas
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def mostrar_resumo_impostos():
    """Mostrar resumo das alíquotas corretas"""
    
    print("=== RESUMO DAS ALÍQUOTAS DE IMPOSTOS CORRETAS ===\n")
    
    print("💰 ESTRUTURA DE IMPOSTOS IMPLEMENTADA:")
    print("   1. ICMS/Simples/ISS: VARIÁVEL (conforme orçamento)")
    print("   2. PIS/COFINS: 3.65%")
    print("   3. IR/C.Social: 2.28% ✅ CORRIGIDO")
    print("   4. Embalagem: 1.00%")
    print("   5. Frete: 0.00%")
    print("   6. Desp.Financ.: 1.50%")
    print("   7. Desp.Adm.: 18.00%")
    print("   8. Comissão: VARIÁVEL (conforme orçamento)")
    
    print(f"\n📊 EXEMPLOS DE CÁLCULO:")
    
    # Exemplos com diferentes ICMS
    exemplos = [
        {"icms": 7.20, "comissao": 0.0, "descricao": "ICMS baixo, sem comissão"},
        {"icms": 12.0, "comissao": 5.0, "descricao": "ICMS médio, comissão 5%"},
        {"icms": 18.59, "comissao": 5.0, "descricao": "ICMS alto MG, comissão 5%"},
        {"icms": 21.17, "comissao": 8.5, "descricao": "ICMS RJ não contrib., comissão 8.5%"}
    ]
    
    for exemplo in exemplos:
        icms = exemplo["icms"]
        comissao = exemplo["comissao"]
        
        # Cálculo
        simples_iss = icms
        pis_cofins = 3.65
        ir_csocial = 2.28
        embalagem = 1.0
        frete = 0.0
        desp_financ = 1.5
        desp_adm = 18.0
        
        outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
        total = comissao + outros_impostos
        
        print(f"\n   📋 {exemplo['descricao']}:")
        print(f"      ICMS: {icms}% + Outros: {(outros_impostos - icms):.2f}% + Comissão: {comissao}%")
        print(f"      = TOTAL: {total:.2f}%")
    
    print(f"\n🔍 ONDE VERIFICAR:")
    print(f"   1. Abra qualquer orçamento no navegador")
    print(f"   2. Pressione F12 para abrir o Console")
    print(f"   3. Procure por '=== DEBUG IMPOSTOS DETALHADOS ==='")
    print(f"   4. Confirme que IR/C.Social mostra 2.28%")
    
    print(f"\n✅ CORREÇÕES IMPLEMENTADAS:")
    print(f"   ✅ ICMS agora usa o valor real de cada orçamento")
    print(f"   ✅ IR/C.Social corrigido de 7.68% para 2.28%")
    print(f"   ✅ Cálculos precisos e consistentes")
    print(f"   ✅ Debug detalhado no console do navegador")

if __name__ == "__main__":
    mostrar_resumo_impostos()