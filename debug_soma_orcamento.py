#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para depurar a soma dos valores do orçamento
"""

def debug_soma_orcamento():
    print("=== DEBUG DA SOMA DO ORÇAMENTO ===")
    print()
    
    # Dados do orçamento mostrado na imagem
    print("Dados da imagem:")
    print("- Total Orçamento: R$ 17755.65")
    print("- Valor Total do item 'gc': R$ 17710.13")
    print("- Diferença: R$ 45.52")
    print()
    
    # Vamos calcular baseado no que vemos
    custo_unitario = 393.56  # Valor azul na tabela
    quantidade = 45.0
    lucro_percent = 22.5
    
    # Impostos conforme mostrado na interface
    icms = 18.59
    comissao = 0.50
    comissao_impostos = 45.52  # Total mostrado no badge
    
    print("=== ANÁLISE DOS VALORES ===")
    print(f"Custo Unitário (azul): R$ {custo_unitario:.2f}")
    print(f"Quantidade: {quantidade}")
    print(f"Lucro: {lucro_percent}%")
    print(f"ICMS: {icms}%")
    print(f"Comissão: {comissao}%")
    print(f"Comissão + Impostos: {comissao_impostos}%")
    print()
    
    # Calcular valor total esperado usando nossa nova fórmula
    print("=== CÁLCULO COM NOVA FÓRMULA ===")
    
    # Se o custo unitário mostrado (R$ 393.56) já é o valor final calculado
    if True:  # Assumindo que o valor azul já está calculado
        valor_total_calculado = quantidade * custo_unitario
        print(f"Valor Total = {quantidade} × R$ {custo_unitario:.2f} = R$ {valor_total_calculado:.2f}")
        print(f"Valor mostrado na tabela: R$ 17710.13")
        print(f"Diferença: R$ {abs(valor_total_calculado - 17710.13):.2f}")
    
    print()
    
    # Verificar se há algum custo oculto ou base diferente
    print("=== ANÁLISE REVERSA ===")
    valor_tabela = 17710.13
    custo_original_calc = valor_tabela / quantidade
    print(f"Custo implícito na tabela: R$ {valor_tabela:.2f} / {quantidade} = R$ {custo_original_calc:.2f}")
    
    diferenca_custos = custo_unitario - custo_original_calc
    print(f"Diferença entre custos: R$ {diferenca_custos:.2f}")
    
    # Se há uma diferença, pode ser arredondamento ou outro fator
    print()
    print("=== POSSÍVEIS CAUSAS DA DISCREPÂNCIA ===")
    print("1. Arredondamento em diferentes etapas do cálculo")
    print("2. O valor 'Custo Unitário' pode não ser o valor base original")
    print("3. Pode haver outros fatores não visíveis aplicados")
    
    # Testar diferentes cenários
    print()
    print("=== TESTE DE CENÁRIOS ===")
    
    # Cenário 1: Usar o valor da tabela como correto
    total_correto = 17710.13
    diferenca_total = 17755.65 - total_correto
    print(f"Se R$ {total_correto:.2f} está correto:")
    print(f"  Sobra inexplicada: R$ {diferenca_total:.2f}")
    print(f"  Percentual: {(diferenca_total/total_correto)*100:.2f}%")

if __name__ == "__main__":
    debug_soma_orcamento()