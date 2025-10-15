#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar a nova fórmula de cálculo do custo unitário
Nova fórmula: Custo Unit / (1 - (impostos + lucro))
"""

def testar_nova_formula():
    print("=== TESTE DA NOVA FÓRMULA DE CUSTO UNITÁRIO ===")
    print("Fórmula: Custo Unit / (1 - (impostos + lucro))")
    print()
    
    # Dados de exemplo
    custo_original = 100.0
    impostos_percent = 45.52  # Exemplo dos cálculos anteriores
    lucro_percent = 22.5
    
    # Converter para decimais
    impostos_decimal = impostos_percent / 100  # 0.4552
    lucro_decimal = lucro_percent / 100        # 0.225
    
    # Calcular denominador
    denominador = 1 - (impostos_decimal + lucro_decimal)
    
    # Calcular valor unitário final
    valor_unitario_final = custo_original / denominador
    
    print(f"Custo Original: R$ {custo_original:.2f}")
    print(f"Impostos: {impostos_percent:.2f}% ({impostos_decimal:.4f})")
    print(f"Lucro: {lucro_percent:.2f}% ({lucro_decimal:.4f})")
    print(f"Soma impostos + lucro: {impostos_decimal + lucro_decimal:.4f}")
    print(f"Denominador: 1 - {impostos_decimal + lucro_decimal:.4f} = {denominador:.4f}")
    print(f"Valor Unitário Final: R$ {custo_original:.2f} / {denominador:.4f} = R$ {valor_unitario_final:.2f}")
    print()
    
    # Verificação: Quanto % o valor final representa em relação ao custo original
    percentual_aumento = ((valor_unitario_final - custo_original) / custo_original) * 100
    print(f"Aumento: {percentual_aumento:.2f}%")
    print(f"Multiplicador efetivo: {valor_unitario_final / custo_original:.4f}x")
    print()
    
    # Teste com diferentes cenários
    print("=== TESTE COM DIFERENTES CENÁRIOS ===")
    cenarios = [
        {"custo": 50.0, "impostos": 30.0, "lucro": 15.0},
        {"custo": 200.0, "impostos": 40.0, "lucro": 25.0},
        {"custo": 75.0, "impostos": 45.52, "lucro": 22.5},
        {"custo": 150.0, "impostos": 35.0, "lucro": 20.0},
    ]
    
    for i, cenario in enumerate(cenarios, 1):
        custo = cenario["custo"]
        imp_pct = cenario["impostos"]
        lucro_pct = cenario["lucro"]
        
        imp_dec = imp_pct / 100
        lucro_dec = lucro_pct / 100
        denom = 1 - (imp_dec + lucro_dec)
        
        if denom <= 0:
            print(f"Cenário {i}: ERRO - Denominador inválido ({denom:.4f})")
            continue
            
        valor_final = custo / denom
        aumento = ((valor_final - custo) / custo) * 100
        
        print(f"Cenário {i}: R$ {custo:.2f} → R$ {valor_final:.2f} (+{aumento:.1f}%)")
    
    print()
    print("=== COMPARAÇÃO COM FÓRMULA ANTERIOR ===")
    
    # Fórmula anterior: Custo × (1 + impostos) × (1 + lucro)
    mult_imp = 1 + (impostos_percent / 100)
    mult_lucro = 1 + (lucro_percent / 100)
    valor_anterior = custo_original * mult_imp * mult_lucro
    
    print(f"Fórmula anterior: R$ {custo_original:.2f} × {mult_imp:.4f} × {mult_lucro:.4f} = R$ {valor_anterior:.2f}")
    print(f"Fórmula nova: R$ {custo_original:.2f} / {denominador:.4f} = R$ {valor_unitario_final:.2f}")
    print(f"Diferença: R$ {valor_unitario_final - valor_anterior:.2f}")

if __name__ == "__main__":
    testar_nova_formula()