#!/usr/bin/env python
"""
Ajuste fino para encontrar parâmetros exatos
"""

import requests

def ajuste_fino():
    print("=== AJUSTE FINO DOS PARÂMETROS ===")
    
    # Da imagem sabemos que:
    # Perfil: 17.5000 m com 5% perda = R$ 113.40
    # Chaveta: 14.0000 m com 5% perda = R$ 29.68
    
    # Se perfil com perda dá 17.5, então sem perda = 17.5 / 1.05 = 16.6667
    # Se chaveta com perda dá 14.0, então sem perda = 14.0 / 1.05 = 13.3333
    
    metros_lineares_sem_perda = 17.5 / 1.05  # 16.6667
    chaveta_sem_perda = 14.0 / 1.05  # 13.3333
    
    print(f"Metros lineares sem perda: {metros_lineares_sem_perda:.4f}")
    print(f"Chaveta sem perda: {chaveta_sem_perda:.4f}")
    
    # Para chaveta: (vao / 150) * 2 = 13.3333
    # vao = 13.3333 * 150 / 2 = 1000
    vao = chaveta_sem_perda * 150 / 2
    print(f"Vão calculado: {vao:.1f} mm")
    
    # Para perfil: (comprimento / eixo_i) * (vao / 1000) = 16.6667
    # (comprimento / eixo_i) * (1000 / 1000) = 16.6667
    # comprimento / eixo_i = 16.6667
    
    # Testando diferentes combinações:
    combinacoes = [
        (25, 16.6667 * 25),      # eixo_i=25, comprimento=416.67
        (32, 16.6667 * 32),      # eixo_i=32, comprimento=533.33
        (38, 16.6667 * 38),      # eixo_i=38, comprimento=633.33
        (40, 16.6667 * 40),      # eixo_i=40, comprimento=666.67
    ]
    
    print(f"\nCombinações possíveis (vão={vao:.1f}):")
    for eixo_i, comprimento in combinacoes:
        metros_calc = (comprimento / eixo_i) * (vao / 1000)
        print(f"  eixo_i={eixo_i:2d}, comprimento={comprimento:6.1f} -> metros={metros_calc:.4f}")
    
    # Testando a combinação mais provável
    dados_teste = {
        'vao': 1000.0,
        'comprimento': 416.67,
        'eixo_i': 25.0,
        'perda': 5.0,
        'tempo_total': 0.4
    }
    
    print(f"\n=== TESTE COM PARÂMETROS AJUSTADOS ===")
    print(f"Dados: {dados_teste}")
    
    # Calcular
    metros_lineares = (dados_teste['comprimento'] / dados_teste['eixo_i']) * (dados_teste['vao'] / 1000)
    quantidade_chaveta = (dados_teste['vao'] / 150) * 2
    
    print(f"Metros lineares calculados: {metros_lineares:.4f}")
    print(f"Quantidade chaveta calculada: {quantidade_chaveta:.4f}")
    print(f"Com 5% perda:")
    print(f"  Perfil: {metros_lineares * 1.05:.4f} m")
    print(f"  Chaveta: {quantidade_chaveta * 1.05:.4f} m")

if __name__ == "__main__":
    ajuste_fino()