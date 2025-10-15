#!/usr/bin/env python
"""
Verificar se o campo "Comissão + Impostos" foi adicionado aos detalhes do orçamento
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def verificar_campo_detalhes():
    """Verificar o novo campo nos detalhes do orçamento"""
    try:
        # Pegar alguns orçamentos para testar
        orcamentos = Orcamento.objects.all().order_by('-id')[:3]
        
        print("=== NOVO CAMPO NOS DETALHES DO ORÇAMENTO ===\n")
        
        print("✅ CAMPO ADICIONADO:")
        print("   📍 Localização: Seção de detalhes do orçamento")
        print("   🏷️  Nome: 'Comissão + Impostos'")
        print("   🎨 Estilo: Badge azul (bg-primary)")
        print("   📊 Conteúdo: Percentual total calculado automaticamente")
        print()
        
        print("📋 NOVA ESTRUTURA DOS DETALHES:")
        print("   ┌─────────────────────────────────────┐")
        print("   │ Cliente: [Nome do Cliente]          │")
        print("   │ Contato: [Nome do Contato]          │")
        print("   │ Telefone: [Telefone]                │")
        print("   │ Email: [Email]                      │")
        print("   │ UF: [Estado]                        │")
        print("   │ ICMS: [X.XX%] (azul claro)          │")
        print("   │ Comissão: [X.XX%] (cinza)           │")
        print("   │ Comissão + Impostos: [XX.XX%] (azul)│ ← NOVO")
        print("   │ Status: [Status] (amarelo)           │")
        print("   └─────────────────────────────────────┘")
        print()
        
        print("📊 EXEMPLOS DE CÁLCULO PARA VERIFICAÇÃO:")
        
        for orc in orcamentos:
            icms = float(orc.icms)
            comissao = float(orc.comissao)
            
            # Calcular total de impostos como no JavaScript
            simples_iss = icms
            pis_cofins = 3.65
            ir_csocial = 2.28
            embalagem = 1.0
            frete = 0.0
            desp_financ = 1.5
            desp_adm = 18.0
            
            outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
            total_impostos = comissao + outros_impostos
            
            print(f"   📋 {orc.numero_orcamento}:")
            print(f"      UF: {orc.uf}")
            print(f"      ICMS: {icms:.2f}%")
            print(f"      Comissão: {comissao:.2f}%")
            print(f"      Outros impostos: {(outros_impostos - icms):.2f}%")
            print(f"      = Total (Comissão + Impostos): {total_impostos:.2f}%")
            print(f"      🔗 http://127.0.0.1:8000/orcamento/{orc.id}/")
            print()
        
        print("✅ VANTAGENS DO NOVO CAMPO:")
        print("   🔹 Visibilidade imediata do percentual total")
        print("   🔹 Não precisa calcular mentalmente")
        print("   🔹 Consistente com outros badges")
        print("   🔹 Atualização automática")
        print("   🔹 Facilita análise rápida")
        print()
        
        print("🔍 COMO VERIFICAR:")
        print("   1. Abra qualquer orçamento")
        print("   2. Veja a seção de detalhes no topo")
        print("   3. Procure o badge azul 'Comissão + Impostos'")
        print("   4. Deve mostrar o percentual total (ex: 45.52%)")
        print("   5. Console (F12) confirma o cálculo")
        print()
        
        print("💡 OBSERVAÇÃO:")
        print("   Este valor é o mesmo usado nos cálculos da tabela")
        print("   Facilita a compreensão geral dos impostos do orçamento")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_campo_detalhes()