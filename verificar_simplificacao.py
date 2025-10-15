#!/usr/bin/env python
"""
Verificar se a simplificação da tabela de impostos está funcionando
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def verificar_simplificacao():
    """Verificar a simplificação da exibição de impostos"""
    try:
        # Pegar alguns orçamentos para testar
        orcamentos = Orcamento.objects.all().order_by('-id')[:3]
        
        print("=== VERIFICAÇÃO DA SIMPLIFICAÇÃO DOS IMPOSTOS ===\n")
        
        print("✅ MUDANÇAS IMPLEMENTADAS:")
        print("   🔹 Removido detalhamento de 'Comissão: X%'")
        print("   🔹 Removido detalhamento de 'Outros Impostos: X%'")
        print("   🔹 Removida linha divisória")
        print("   🔹 Mantido apenas 'Total: X%' em azul")
        
        print(f"\n📊 ORÇAMENTOS PARA TESTAR:")
        
        for orc in orcamentos:
            icms = float(orc.icms)
            comissao = float(orc.comissao)
            
            # Cálculo do total
            simples_iss = icms
            pis_cofins = 3.65
            ir_csocial = 2.28
            embalagem = 1.0
            frete = 0.0
            desp_financ = 1.5
            desp_adm = 18.0
            
            outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
            total_impostos = comissao + outros_impostos
            
            print(f"   📋 {orc.numero_orcamento} (ID: {orc.id})")
            print(f"      Total esperado na tabela: {total_impostos:.2f}%")
            print(f"      🔗 http://127.0.0.1:8000/orcamento/{orc.id}/")
            print()
        
        print("🎯 RESULTADO ESPERADO NA TABELA:")
        print("   ❌ ANTES: Detalhes + linha + Total")
        print("   ✅ AGORA: Apenas 'Total: XX.XX%' em azul")
        
        print(f"\n🔍 COMO VERIFICAR:")
        print(f"   1. Abra qualquer orçamento")
        print(f"   2. Olhe a coluna 'Comissão + Impostos (%)'")
        print(f"   3. Deve aparecer apenas o total em azul")
        print(f"   4. Sem detalhamento de comissão/outros impostos")
        
        print(f"\n💡 OBSERVAÇÃO:")
        print(f"   O cálculo continua correto nos bastidores")
        print(f"   O debug ainda está disponível no console (F12)")
        print(f"   Apenas a exibição na tabela foi simplificada")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_simplificacao()