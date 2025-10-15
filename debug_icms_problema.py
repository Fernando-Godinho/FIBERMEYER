#!/usr/bin/env python
"""
Investigar problema do ICMS não batendo nos cálculos
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def investigar_icms():
    """Investigar por que o ICMS não está batendo"""
    try:
        # Pegar os últimos orçamentos
        orcamentos = Orcamento.objects.all().order_by('-id')[:5]
        
        print("=== INVESTIGAÇÃO ICMS ===\n")
        
        for orc in orcamentos:
            print(f"📋 Orçamento ID: {orc.id} - {orc.numero_orcamento}")
            print(f"   🏢 Cliente: {orc.cliente}")
            print(f"   📍 UF: {orc.uf}")
            print(f"   💰 ICMS no BD: {orc.icms}%")
            print(f"   🏭 Venda: {orc.venda_destinada}")
            print(f"   👤 Contribuinte: {orc.cliente_contrib_icms}")
            print(f"   💼 Comissão: {orc.comissao}%")
            print(f"   📊 Status: {orc.status}")
            print(f"   ⏰ Atualizado: {orc.atualizado_em}")
            print()
        
        # Verificar se há algum orçamento com ICMS 18.59%
        orc_problema = None
        for orc in orcamentos:
            if float(orc.icms) == 18.59:
                orc_problema = orc
                break
        
        if orc_problema:
            print(f"🎯 ORÇAMENTO COM PROBLEMA IDENTIFICADO:")
            print(f"   ID: {orc_problema.id}")
            print(f"   ICMS: {orc_problema.icms}%")
            print(f"   Este ICMS deveria ser usado nos cálculos!")
            print(f"   URL: http://127.0.0.1:8000/orcamento/{orc_problema.id}/")
        
        # Buscar orçamentos com ICMS próximo de 12%
        print(f"\n🔍 ORÇAMENTOS COM ICMS PRÓXIMO DE 12%:")
        for orc in orcamentos:
            if 11.0 <= float(orc.icms) <= 13.0:
                print(f"   ID {orc.id}: ICMS {orc.icms}% - {orc.numero_orcamento}")
        
        print(f"\n⚠️  PROBLEMA IDENTIFICADO:")
        print(f"   - O ICMS exibido na tela: 18.59%")
        print(f"   - O ICMS usado no cálculo: 12.0% (ICMS/Simples/ISS)")
        print(f"   - Há dessincronia entre o valor do orçamento e o cálculo JavaScript")
        
        return orc_problema
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    investigar_icms()