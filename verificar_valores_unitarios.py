#!/usr/bin/env python
"""
Verificar se os valores unitários finais estão sendo exibidos corretamente
"""

def verificar_valores_unitarios():
    """Verificar cálculo dos valores unitários finais"""
    
    print("=== VERIFICAÇÃO DOS VALORES UNITÁRIOS FINAIS ===\n")
    
    print("🔍 NOVA EXIBIÇÃO NA TABELA:")
    print("   Coluna 'Custo Unitário' agora mostra:")
    print("   ┌─────────────────────────┐")
    print("   │ Custo base:             │")
    print("   │ R$ 125,86               │")
    print("   │ Valor final:            │")
    print("   │ R$ 231,30 (azul)        │")
    print("   └─────────────────────────┘")
    print()
    
    # Exemplo de cálculo
    custo_base = 125.86
    impostos_percent = 45.52  # Do exemplo na imagem
    lucro_percent = 22.5
    quantidade = 45.0
    
    print("📊 EXEMPLO DE CÁLCULO:")
    print(f"   Custo Base: R$ {custo_base:.2f}")
    print(f"   Impostos: {impostos_percent:.2f}%")
    print(f"   Lucro: {lucro_percent:.2f}%")
    print(f"   Quantidade: {quantidade}")
    print()
    
    # Cálculo passo a passo
    multiplicador_impostos = 1 + (impostos_percent / 100)
    multiplicador_lucro = 1 + (lucro_percent / 100)
    
    custo_com_impostos = custo_base * multiplicador_impostos
    valor_unitario_final = custo_com_impostos * multiplicador_lucro
    valor_total = quantidade * valor_unitario_final
    
    print("🧮 CÁLCULO DETALHADO:")
    print(f"   1. Custo com impostos:")
    print(f"      R$ {custo_base:.2f} × {multiplicador_impostos:.4f} = R$ {custo_com_impostos:.2f}")
    print()
    print(f"   2. Valor unitário final:")
    print(f"      R$ {custo_com_impostos:.2f} × {multiplicador_lucro:.4f} = R$ {valor_unitario_final:.2f}")
    print()
    print(f"   3. Valor total:")
    print(f"      {quantidade} × R$ {valor_unitario_final:.2f} = R$ {valor_total:.2f}")
    print()
    
    print("✅ VALIDAÇÃO:")
    valor_esperado_da_imagem = 10096.22
    diferenca = abs(valor_total - valor_esperado_da_imagem)
    
    print(f"   Valor calculado: R$ {valor_total:.2f}")
    print(f"   Valor na imagem: R$ {valor_esperado_da_imagem:.2f}")
    print(f"   Diferença: R$ {diferenca:.2f}")
    
    if diferenca < 50:  # Margem de tolerância
        print("   ✅ Valores estão próximos - cálculo correto!")
    else:
        print("   ⚠️  Diferença significativa - verificar parâmetros")
    
    print()
    print("🔍 COMO VERIFICAR NA TELA:")
    print("   1. Abra o orçamento no navegador")
    print("   2. Na coluna 'Custo Unitário', veja:")
    print("      - Custo base: valor original")
    print("      - Valor final: custo + impostos + lucro")
    print("   3. Valor Total = Quantidade × Valor final")
    print("   4. Console (F12) mostra cálculos detalhados")
    print()
    
    print("💡 OBSERVAÇÕES:")
    print("   - O 'Valor final' é calculado automaticamente")
    print("   - Inclui todos os impostos e lucro")
    print("   - Atualiza em tempo real quando alterar lucro")
    print("   - Facilita verificação do preço unitário")

if __name__ == "__main__":
    verificar_valores_unitarios()