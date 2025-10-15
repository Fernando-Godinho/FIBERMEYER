#!/usr/bin/env python
"""
Testar nova fórmula de cálculo: Qt × Custo Unit × Impostos × Lucro
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento, OrcamentoItem

def testar_nova_formula():
    """Testar a nova fórmula de cálculo"""
    try:
        # Pegar um orçamento com itens
        orcamento = Orcamento.objects.filter(itens__isnull=False).first()
        
        if not orcamento:
            print("❌ Nenhum orçamento com itens encontrado")
            return
        
        print("=== TESTE DA NOVA FÓRMULA DE CÁLCULO ===\n")
        print(f"📋 Orçamento: {orcamento.numero_orcamento}")
        print(f"💰 ICMS: {orcamento.icms}%")
        print(f"💼 Comissão: {orcamento.comissao}%")
        
        # Calcular percentual total de impostos
        icms = float(orcamento.icms)
        comissao = float(orcamento.comissao)
        
        simples_iss = icms
        pis_cofins = 3.65
        ir_csocial = 2.28
        embalagem = 1.0
        frete = 0.0
        desp_financ = 1.5
        desp_adm = 18.0
        
        outros_impostos = simples_iss + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
        total_impostos_percent = comissao + outros_impostos
        
        print(f"📊 Total de Impostos: {total_impostos_percent:.2f}%")
        
        # Testar com itens do orçamento
        itens = orcamento.itens.all()[:3]  # Pegar até 3 itens
        
        print(f"\n🧮 EXEMPLOS DE CÁLCULO:")
        print(f"Fórmula: Qt × Custo Unit × (1 + Impostos/100) × (1 + Lucro/100)")
        print(f"Impostos totais: {total_impostos_percent:.2f}%")
        print()
        
        for item in itens:
            quantidade = float(item.quantidade)
            custo_unit = float(item.custo_unitario)
            lucro_percent = float(item.lucro)
            
            # Aplicar nova fórmula
            multiplicador_impostos = 1 + (total_impostos_percent / 100)
            multiplicador_lucro = 1 + (lucro_percent / 100)
            valor_total_novo = quantidade * custo_unit * multiplicador_impostos * multiplicador_lucro
            
            # Valor atual no banco
            valor_total_atual = float(item.valor_total)
            
            diferenca = valor_total_novo - valor_total_atual
            percentual_diferenca = (diferenca / valor_total_atual * 100) if valor_total_atual > 0 else 0
            
            print(f"📦 {item.descricao[:50]}...")
            print(f"   Qt: {quantidade} × R${custo_unit:.2f} × {multiplicador_impostos:.4f} × {multiplicador_lucro:.4f}")
            print(f"   = R${valor_total_novo:.2f}")
            print(f"   🔄 Valor atual: R${valor_total_atual:.2f}")
            print(f"   📈 Diferença: R${diferenca:+.2f} ({percentual_diferenca:+.1f}%)")
            print()
        
        # Criar exemplos teóricos
        print(f"📋 EXEMPLOS TEÓRICOS:")
        exemplos = [
            {"qt": 1, "custo": 100.0, "lucro": 22.5, "desc": "Item básico"},
            {"qt": 2, "custo": 250.0, "lucro": 30.0, "desc": "Item premium"},
            {"qt": 10, "custo": 50.0, "lucro": 15.0, "desc": "Item volume"}
        ]
        
        for ex in exemplos:
            multiplicador_impostos = 1 + (total_impostos_percent / 100)
            multiplicador_lucro = 1 + (ex["lucro"] / 100)
            valor_total = ex["qt"] * ex["custo"] * multiplicador_impostos * multiplicador_lucro
            
            print(f"   {ex['desc']}: {ex['qt']} × R${ex['custo']:.2f} × {multiplicador_impostos:.4f} × {multiplicador_lucro:.4f} = R${valor_total:.2f}")
        
        print(f"\n🔗 Teste no navegador: http://127.0.0.1:8000/orcamento/{orcamento.id}/")
        print(f"🔍 Abra o Console (F12) para ver os cálculos detalhados")
        
        return orcamento.id
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    testar_nova_formula()