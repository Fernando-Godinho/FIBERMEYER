#!/usr/bin/env python
"""
Exemplo da nova lógica: aplicar impostos e lucro no valor unitário
"""

def exemplo_nova_logica():
    """Demonstrar a nova lógica de cálculo"""
    
    print("=== NOVA LÓGICA DE CÁLCULO IMPLEMENTADA ===\n")
    
    print("🔄 MUDANÇA NA ABORDAGEM:")
    print("   ❌ ANTES: Qt × Custo Unit × Impostos × Lucro")
    print("   ✅ AGORA: Qt × (Custo Unit × Impostos × Lucro)")
    print("            (Aplicar impostos e lucro no valor unitário)")
    print()
    
    print("📋 NOVA FÓRMULA:")
    print("   1. Valor Unitário Final = Custo Unit × (1 + Impostos/100) × (1 + Lucro/100)")
    print("   2. Valor Total = Quantidade × Valor Unitário Final")
    print()
    
    # Exemplo prático
    print("📊 EXEMPLO PRÁTICO:")
    quantidade = 45
    custo_unitario = 125.86
    lucro_percent = 22.5
    
    # Impostos (exemplo)
    icms = 18.59
    comissao = 5.0
    pis_cofins = 3.65
    ir_csocial = 2.28
    embalagem = 1.0
    frete = 0.0
    desp_financ = 1.5
    desp_adm = 18.0
    
    total_impostos = icms + comissao + pis_cofins + ir_csocial + embalagem + frete + desp_financ + desp_adm
    
    print(f"   - Quantidade: {quantidade} unidades")
    print(f"   - Custo Unitário: R$ {custo_unitario:.2f}")
    print(f"   - Impostos Totais: {total_impostos:.2f}%")
    print(f"   - Lucro: {lucro_percent}%")
    print()
    
    # Cálculo passo a passo
    print("🧮 CÁLCULO PASSO A PASSO:")
    
    # Passo 1: Aplicar impostos no custo unitário
    multiplicador_impostos = 1 + (total_impostos / 100)
    custo_com_impostos = custo_unitario * multiplicador_impostos
    
    print(f"   1. Custo com impostos:")
    print(f"      R$ {custo_unitario:.2f} × (1 + {total_impostos:.2f}/100)")
    print(f"      R$ {custo_unitario:.2f} × {multiplicador_impostos:.4f}")
    print(f"      = R$ {custo_com_impostos:.2f}")
    print()
    
    # Passo 2: Aplicar lucro
    multiplicador_lucro = 1 + (lucro_percent / 100)
    valor_unitario_final = custo_com_impostos * multiplicador_lucro
    
    print(f"   2. Valor unitário final (com lucro):")
    print(f"      R$ {custo_com_impostos:.2f} × (1 + {lucro_percent}/100)")
    print(f"      R$ {custo_com_impostos:.2f} × {multiplicador_lucro:.4f}")
    print(f"      = R$ {valor_unitario_final:.2f}")
    print()
    
    # Passo 3: Calcular total
    valor_total = quantidade * valor_unitario_final
    
    print(f"   3. Valor total:")
    print(f"      {quantidade} × R$ {valor_unitario_final:.2f}")
    print(f"      = R$ {valor_total:.2f}")
    print()
    
    # Breakdown detalhado
    print("📈 BREAKDOWN DETALHADO:")
    custo_base_total = quantidade * custo_unitario
    impostos_total = quantidade * (custo_com_impostos - custo_unitario)
    lucro_total = quantidade * (valor_unitario_final - custo_com_impostos)
    
    print(f"   Custo Base ({quantidade} × R${custo_unitario:.2f}): R$ {custo_base_total:.2f}")
    print(f"   + Impostos ({total_impostos:.2f}%): R$ {impostos_total:.2f}")
    print(f"   + Lucro ({lucro_percent}%): R$ {lucro_total:.2f}")
    print(f"   = TOTAL: R$ {valor_total:.2f}")
    print()
    
    # Comparação com método anterior
    print("🔄 COMPARAÇÃO COM MÉTODO ANTERIOR:")
    valor_total_anterior = quantidade * custo_unitario * multiplicador_impostos * multiplicador_lucro
    diferenca = valor_total - valor_total_anterior
    
    print(f"   Método ANTERIOR: {quantidade} × {custo_unitario:.2f} × {multiplicador_impostos:.4f} × {multiplicador_lucro:.4f} = R$ {valor_total_anterior:.2f}")
    print(f"   Método NOVO: {quantidade} × ({custo_unitario:.2f} × {multiplicador_impostos:.4f} × {multiplicador_lucro:.4f}) = R$ {valor_total:.2f}")
    print(f"   Diferença: R$ {diferenca:.2f}")
    print()
    
    print("✅ VANTAGENS DA NOVA ABORDAGEM:")
    print("   🔹 Lógica mais clara: trabalha com valor unitário")
    print("   🔹 Fórmula simples: Qtd × Valor Unit Final")
    print("   🔹 Melhor compreensão do preço unitário")
    print("   🔹 Facilita análise de margem por unidade")
    print("   🔹 Mesmo resultado matemático")
    print()
    
    print("🔍 COMO VERIFICAR:")
    print("   1. Abra qualquer orçamento no navegador")
    print("   2. Pressione F12 para ver o Console")
    print("   3. Procure por '=== CÁLCULO VALORES UNITÁRIOS E TOTAIS ==='")
    print("   4. Veja o breakdown detalhado de cada item")

if __name__ == "__main__":
    exemplo_nova_logica()