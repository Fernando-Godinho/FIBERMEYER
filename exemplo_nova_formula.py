#!/usr/bin/env python
"""
Exemplo prático da nova fórmula de cálculo
"""

def calcular_exemplo_pratico():
    """Mostrar exemplo prático da nova fórmula"""
    
    print("=== NOVA FÓRMULA DE CÁLCULO IMPLEMENTADA ===\n")
    
    print("📋 FÓRMULA: Qt × Custo Unit × (1 + Impostos/100) × (1 + Lucro/100)")
    print()
    
    # Exemplo com dados reais
    print("📊 EXEMPLO PRÁTICO:")
    print("   - Quantidade: 45 unidades")
    print("   - Custo Unitário: R$ 125,86")
    print("   - Lucro: 22,5%")
    print("   - ICMS do orçamento: 18,59%")
    print("   - Comissão: 5,00%")
    print()
    
    # Dados do exemplo
    quantidade = 45
    custo_unit = 125.86
    lucro_percent = 22.5
    
    # Impostos (exemplo com ICMS 18.59% + comissão 5%)
    icms = 18.59
    comissao = 5.0
    pis_cofins = 3.65
    ir_csocial = 2.28
    embalagem = 1.0
    frete = 0.0
    desp_financ = 1.5
    desp_adm = 18.0
    
    total_impostos = icms + comissao + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
    
    print("🧮 CÁLCULO DETALHADO:")
    print(f"   Impostos totais = {icms}% + {comissao}% + {pis_cofins}% + {ir_csocial}% + {embalagem}% + {frete}% + {desp_financ}% + {desp_adm}%")
    print(f"   Impostos totais = {total_impostos:.2f}%")
    print()
    
    # Multiplicadores
    mult_impostos = 1 + (total_impostos / 100)
    mult_lucro = 1 + (lucro_percent / 100)
    
    print(f"   Multiplicador Impostos = 1 + ({total_impostos:.2f}/100) = {mult_impostos:.4f}")
    print(f"   Multiplicador Lucro = 1 + ({lucro_percent}/100) = {mult_lucro:.4f}")
    print()
    
    # Cálculo final
    valor_total = quantidade * custo_unit * mult_impostos * mult_lucro
    
    print(f"   Valor Total = {quantidade} × R${custo_unit:.2f} × {mult_impostos:.4f} × {mult_lucro:.4f}")
    print(f"   Valor Total = R${valor_total:.2f}")
    print()
    
    # Breakdown do valor
    valor_base = quantidade * custo_unit
    valor_com_impostos = valor_base * mult_impostos
    valor_com_lucro = valor_com_impostos * mult_lucro
    
    valor_impostos = valor_com_impostos - valor_base
    valor_lucro = valor_com_lucro - valor_com_impostos
    
    print("📈 BREAKDOWN DO VALOR:")
    print(f"   Valor Base (Qt × Custo): R${valor_base:.2f}")
    print(f"   + Impostos ({total_impostos:.2f}%): R${valor_impostos:.2f}")
    print(f"   + Lucro ({lucro_percent}%): R${valor_lucro:.2f}")
    print(f"   = TOTAL: R${valor_total:.2f}")
    print()
    
    print("✅ VANTAGENS DA NOVA FÓRMULA:")
    print("   🔹 Usa ICMS real de cada orçamento")
    print("   🔹 Aplica impostos sobre o custo base")
    print("   🔹 Aplica lucro sobre valor já com impostos")
    print("   🔹 Cálculo automático em tempo real")
    print("   🔹 Precisão matemática")
    print()
    
    print("🔍 COMO TESTAR:")
    print("   1. Abra qualquer orçamento no navegador")
    print("   2. Pressione F12 para ver o Console")
    print("   3. Procure por '=== CÁLCULO VALORES TOTAIS ==='")
    print("   4. Veja os cálculos detalhados de cada item")
    print("   5. Os valores na tabela são atualizados automaticamente")

if __name__ == "__main__":
    calcular_exemplo_pratico()