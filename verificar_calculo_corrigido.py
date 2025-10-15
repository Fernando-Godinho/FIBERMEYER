#!/usr/bin/env python
"""
Verificar se o cálculo do ICMS está correto após a correção
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def verificar_calculo_correto():
    """Verificar se o cálculo está usando o ICMS correto"""
    try:
        # Pegar o orçamento ID 20 que estava com problema
        orc = Orcamento.objects.get(id=20)
        
        print("=== VERIFICAÇÃO CÁLCULO ICMS CORRIGIDO ===\n")
        print(f"📋 Orçamento: {orc.numero_orcamento}")
        print(f"🏢 Cliente: {orc.cliente}")
        print(f"📍 UF: {orc.uf}")
        print(f"💰 ICMS no BD: {orc.icms}%")
        print(f"💼 Comissão: {orc.comissao}%")
        
        # Calcular manualmente como deveria ser
        icms = float(orc.icms)
        comissao = float(orc.comissao)
        
        # Outros impostos usando ICMS real
        simples_iss = icms  # Agora usa o ICMS real
        pis_cofins = 3.65
        ir_csocial = 7.68
        embalagem = 1.0
        frete = 0.0
        desp_financ = 1.5
        desp_adm = 18.0
        
        outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
        total_impostos = comissao + outros_impostos
        
        print(f"\n🧮 CÁLCULO MANUAL:")
        print(f"   ICMS/Simples/ISS: {simples_iss:.2f}%")
        print(f"   PIS/COFINS: {pis_cofins:.2f}%")
        print(f"   IR/C.Social: {ir_csocial:.2f}%")
        print(f"   Embalagem: {embalagem:.2f}%")
        print(f"   Frete: {frete:.2f}%")
        print(f"   Desp.Financ.: {desp_financ:.2f}%")
        print(f"   Desp.Adm.: {desp_adm:.2f}%")
        print(f"   ─────────────────────")
        print(f"   Total Outros Impostos: {outros_impostos:.2f}%")
        print(f"   Comissão: {comissao:.2f}%")
        print(f"   ═════════════════════")
        print(f"   TOTAL FINAL: {total_impostos:.2f}%")
        
        print(f"\n✅ AGORA O CÁLCULO DEVE USAR:")
        print(f"   - ICMS real do orçamento: {icms:.2f}%")
        print(f"   - Total correto: {total_impostos:.2f}%")
        print(f"   - URL para testar: http://127.0.0.1:8000/orcamento/{orc.id}/")
        
        # Comparar com o cálculo antigo (fixo em 12%)
        outros_impostos_antigo = 12.0 + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
        total_antigo = comissao + outros_impostos_antigo
        
        print(f"\n📊 COMPARAÇÃO:")
        print(f"   🔴 Cálculo ANTIGO (ICMS fixo 12%): {total_antigo:.2f}%")
        print(f"   🟢 Cálculo NOVO (ICMS real {icms:.2f}%): {total_impostos:.2f}%")
        print(f"   📈 Diferença: {(total_impostos - total_antigo):.2f}% pontos percentuais")
        
        return orc
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    verificar_calculo_correto()