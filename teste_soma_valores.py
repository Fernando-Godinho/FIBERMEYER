#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar a soma dos valores na tabela
"""

def simular_calculo_total():
    print("=== SIMULAÇÃO DO CÁLCULO DE TOTAL DO ORÇAMENTO ===")
    print()
    
    # Simular dados de exemplo como se fossem da tabela
    itens = [
        {"custo": 100.0, "quantidade": 2, "lucro": 22.5},
        {"custo": 75.0, "quantidade": 1, "lucro": 22.5},
        {"custo": 50.0, "quantidade": 3, "lucro": 22.5},
    ]
    
    # Impostos fixos (como no sistema)
    impostos_percent = 45.52  # Exemplo dos cálculos anteriores
    
    total_orcamento = 0
    
    print("Calculando cada item:")
    print("-" * 60)
    
    for i, item in enumerate(itens, 1):
        custo = item["custo"]
        quantidade = item["quantidade"]
        lucro_percent = item["lucro"]
        
        # Aplicar nova fórmula: Custo Unit / (1 - (impostos + lucro))
        impostos_decimal = impostos_percent / 100
        lucro_decimal = lucro_percent / 100
        denominador = 1 - (impostos_decimal + lucro_decimal)
        
        if denominador <= 0:
            print(f"Item {i}: ERRO - Denominador inválido!")
            continue
            
        valor_unitario_final = custo / denominador
        valor_total_item = quantidade * valor_unitario_final
        
        print(f"Item {i}:")
        print(f"  Custo: R$ {custo:.2f}")
        print(f"  Quantidade: {quantidade}")
        print(f"  Impostos: {impostos_percent:.2f}%")
        print(f"  Lucro: {lucro_percent:.2f}%")
        print(f"  Denominador: {denominador:.4f}")
        print(f"  Valor unitário final: R$ {valor_unitario_final:.2f}")
        print(f"  Valor total: R$ {valor_total_item:.2f}")
        print()
        
        total_orcamento += valor_total_item
    
    print("-" * 60)
    print(f"TOTAL DO ORÇAMENTO: R$ {total_orcamento:.2f}")
    print()
    
    # Comparar com a fórmula antiga
    print("=== COMPARAÇÃO COM FÓRMULA ANTERIOR ===")
    total_antigo = 0
    
    for i, item in enumerate(itens, 1):
        custo = item["custo"]
        quantidade = item["quantidade"]
        lucro_percent = item["lucro"]
        
        # Fórmula anterior: Custo × (1 + impostos) × (1 + lucro)
        mult_impostos = 1 + (impostos_percent / 100)
        mult_lucro = 1 + (lucro_percent / 100)
        valor_unitario_antigo = custo * mult_impostos * mult_lucro
        valor_total_antigo = quantidade * valor_unitario_antigo
        
        total_antigo += valor_total_antigo
        print(f"Item {i} (fórmula antiga): R$ {valor_total_antigo:.2f}")
    
    print(f"Total anterior: R$ {total_antigo:.2f}")
    print(f"Total novo: R$ {total_orcamento:.2f}")
    print(f"Diferença: R$ {total_orcamento - total_antigo:.2f}")

if __name__ == "__main__":
    simular_calculo_total()