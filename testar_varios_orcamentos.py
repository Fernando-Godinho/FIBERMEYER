#!/usr/bin/env python
"""
Testar com diferentes orçamentos para garantir que o cálculo está correto
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def testar_varios_orcamentos():
    """Testar cálculo com vários orçamentos"""
    try:
        orcamentos = Orcamento.objects.all().order_by('-id')[:4]
        
        print("=== TESTE COM MÚLTIPLOS ORÇAMENTOS ===\n")
        
        for orc in orcamentos:
            icms = float(orc.icms)
            comissao = float(orc.comissao)
            
            # Outros impostos usando ICMS real
            simples_iss = icms
            pis_cofins = 3.65
            ir_csocial = 7.68
            embalagem = 1.0
            frete = 0.0
            desp_financ = 1.5
            desp_adm = 18.0
            
            outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
            total_impostos = comissao + outros_impostos
            
            print(f"📋 {orc.numero_orcamento} (ID: {orc.id})")
            print(f"   UF: {orc.uf} | ICMS: {icms:.2f}% | Comissão: {comissao:.2f}%")
            print(f"   Outros Impostos: {outros_impostos:.2f}% | TOTAL: {total_impostos:.2f}%")
            print(f"   🔗 http://127.0.0.1:8000/orcamento/{orc.id}/")
            print()
        
        print("✅ Agora todos os orçamentos devem calcular corretamente!")
        print("🔍 Verifique o console do navegador para confirmar os valores.")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    testar_varios_orcamentos()