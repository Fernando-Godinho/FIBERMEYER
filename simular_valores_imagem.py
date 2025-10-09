#!/usr/bin/env python
"""
Teste para simular exatamente os valores da imagem
"""

import requests

def simular_valores_imagem():
    print("=== SIMULANDO VALORES DA IMAGEM ===")
    
    # Parâmetros descobertos da imagem:
    # - Vão: 1050mm
    # - Perda: 5%
    # - Mão de obra: 0.4h
    # - Metros lineares calculados: ~17.5
    
    # Se metros lineares = 17.5 e vão = 1050
    # Fórmula: (comprimento / eixo_i) * (vao / 1000) = 17.5
    # (comprimento / eixo_i) * (1050 / 1000) = 17.5
    # (comprimento / eixo_i) * 1.05 = 17.5
    # (comprimento / eixo_i) = 16.667
    
    # Vamos testar com eixo_i = 25 e comprimento = 416.67
    # Ou eixo_i = 38 e comprimento = 633.33
    
    dados = {
        'vao': 1050.0,
        'comprimento': 633.33,  # Para dar metros lineares ~17.5
        'eixo_i': 38.0,
        'perda': 5.0,
        'tempo_proc': 0.3,  # Total 0.4h
        'tempo_mtg': 0.1,   # Total 0.4h
    }
    
    print(f"Dados de teste: {dados}")
    
    # Buscar produtos
    response = requests.get('http://127.0.0.1:8000/api/produtos/')
    produtos = response.json()
    
    perfil = next((p for p in produtos if p['id'] == 1328), None)
    chaveta = next((p for p in produtos if p['id'] == 1332), None)
    cola = next((p for p in produtos if p['id'] == 1183), None)
    
    # Aplicar fórmulas
    metros_lineares_por_m2 = (dados['comprimento'] / dados['eixo_i']) * (dados['vao'] / 1000)
    quantidade_chaveta = (dados['vao'] / 150) * 2
    quantidade_cola = 0.06
    fator_perda = 1 + (dados['perda'] / 100)
    
    print(f"\n=== CÁLCULOS ===")
    print(f"Metros lineares: ({dados['comprimento']}/{dados['eixo_i']}) * ({dados['vao']}/1000) = {metros_lineares_por_m2:.4f}")
    print(f"Quantidade chaveta: ({dados['vao']}/150) * 2 = {quantidade_chaveta:.4f}")
    print(f"Quantidade cola: {quantidade_cola:.4f}")
    print(f"Fator perda: {fator_perda:.2f}")
    
    # Calcular custos
    custo_perfil = metros_lineares_por_m2 * float(perfil['custo_centavos']) * fator_perda
    custo_chaveta = quantidade_chaveta * float(chaveta['custo_centavos']) * fator_perda
    custo_cola = quantidade_cola * float(cola['custo_centavos']) * fator_perda
    
    tempo_total = dados['tempo_proc'] + dados['tempo_mtg']
    custo_mao_obra = tempo_total * 65.79 * 100  # em centavos
    
    print(f"\n=== CUSTOS ===")
    print(f"Perfil: {metros_lineares_por_m2 * fator_perda:.4f} m - R$ {custo_perfil/100:.2f}")
    print(f"Chaveta: {quantidade_chaveta * fator_perda:.4f} m - R$ {custo_chaveta/100:.2f}")
    print(f"Cola: {quantidade_cola * fator_perda:.4f} unid - R$ {custo_cola/100:.2f}")
    print(f"Mão de obra: {tempo_total:.4f} h - R$ {custo_mao_obra/100:.2f}")
    
    total = (custo_perfil + custo_chaveta + custo_cola + custo_mao_obra) / 100
    print(f"\nTOTAL: R$ {total:.2f}")
    
    print(f"\n=== COMPARAÇÃO COM IMAGEM ===")
    print(f"Esperado - Perfil: 17.5000 m - R$ 113.40")
    print(f"Calculado - Perfil: {metros_lineares_por_m2 * fator_perda:.4f} m - R$ {custo_perfil/100:.2f}")
    print(f"")
    print(f"Esperado - Chaveta: 14.0000 m - R$ 29.68")
    print(f"Calculado - Chaveta: {quantidade_chaveta * fator_perda:.4f} m - R$ {custo_chaveta/100:.2f}")
    print(f"")
    print(f"Esperado - Cola: 0.0630 unid - R$ 5.47")
    print(f"Calculado - Cola: {quantidade_cola * fator_perda:.4f} unid - R$ {custo_cola/100:.2f}")
    print(f"")
    print(f"Esperado - M.O.: 0.4000 h - R$ 26.32")
    print(f"Calculado - M.O.: {tempo_total:.4f} h - R$ {custo_mao_obra/100:.2f}")
    print(f"")
    print(f"Esperado - TOTAL: R$ 174.87")
    print(f"Calculado - TOTAL: R$ {total:.2f}")

if __name__ == "__main__":
    simular_valores_imagem()