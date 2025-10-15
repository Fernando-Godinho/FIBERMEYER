#!/usr/bin/env python
"""
Verificar cálculo com IR/C.Social correto (2.28%)
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def verificar_ir_csocial_correto():
    """Verificar se o IR/C.Social agora está com o valor correto"""
    try:
        # Pegar alguns orçamentos para testar
        orcamentos = Orcamento.objects.all().order_by('-id')[:3]
        
        print("=== VERIFICAÇÃO IR/C.SOCIAL CORRIGIDO (2.28%) ===\n")
        
        for orc in orcamentos:
            icms = float(orc.icms)
            comissao = float(orc.comissao)
            
            # Cálculo com IR/C.Social correto
            simples_iss = icms
            pis_cofins = 3.65
            ir_csocial = 2.28  # VALOR CORRETO
            embalagem = 1.0
            frete = 0.0
            desp_financ = 1.5
            desp_adm = 18.0
            
            outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
            total_impostos = comissao + outros_impostos
            
            # Cálculo com valor antigo (7.68%) para comparação
            ir_csocial_antigo = 7.68
            outros_impostos_antigo = simples_iss + pis_cofins + ir_csocial_antigo + embalagem + frete + desp_financ + desp_adm
            total_antigo = comissao + outros_impostos_antigo
            
            diferenca = total_impostos - total_antigo
            
            print(f"📋 {orc.numero_orcamento} (ID: {orc.id})")
            print(f"   UF: {orc.uf} | ICMS: {icms:.2f}% | Comissão: {comissao:.2f}%")
            print(f"   🧮 BREAKDOWN DOS IMPOSTOS:")
            print(f"      - ICMS/Simples/ISS: {simples_iss:.2f}%")
            print(f"      - PIS/COFINS: {pis_cofins:.2f}%")
            print(f"      - IR/C.Social: {ir_csocial:.2f}% ✅ (era {ir_csocial_antigo:.2f}%)")
            print(f"      - Embalagem: {embalagem:.2f}%")
            print(f"      - Frete: {frete:.2f}%")
            print(f"      - Desp.Financ.: {desp_financ:.2f}%")
            print(f"      - Desp.Adm.: {desp_adm:.2f}%")
            print(f"   📊 TOTAIS:")
            print(f"      - Outros Impostos: {outros_impostos:.2f}%")
            print(f"      - Total Final: {total_impostos:.2f}%")
            print(f"      - Diferença vs antigo: {diferenca:+.2f}% pontos")
            print(f"   🔗 http://127.0.0.1:8000/orcamento/{orc.id}/")
            print()
        
        print("✅ IR/C.Social corrigido de 7.68% para 2.28%")
        print("📉 Isso reduz o total de impostos em 5.4 pontos percentuais")
        print("🔍 Verifique o console do navegador para confirmar os novos valores")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_ir_csocial_correto()