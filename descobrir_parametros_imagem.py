#!/usr/bin/env python
"""
Teste para descobrir os parâmetros que geram os valores da imagem
"""

import requests

def testar_parametros_imagem():
    print("=== DESCOBRINDO PARÂMETROS DA IMAGEM ===")
    
    # Valores da imagem:
    # Perfil: Fator 17.5000 - R$ 113.40
    # Chaveta: Fator 14.0000 - R$ 29.68  
    # Cola: Fator 0.0630 - R$ 5.47
    # Mão de obra: 0.4000h - R$ 26.32
    
    # Buscar dados dos produtos
    response = requests.get('http://127.0.0.1:8000/api/produtos/')
    produtos = response.json()
    
    perfil = next((p for p in produtos if p['id'] == 1328), None)
    chaveta = next((p for p in produtos if p['id'] == 1332), None)
    cola = next((p for p in produtos if p['id'] == 1183), None)
    
    print("Produtos encontrados:")
    print(f"  Perfil: {perfil['descricao']} - R$ {perfil['custo_centavos']/100:.2f}")
    print(f"  Chaveta: {chaveta['descricao']} - R$ {chaveta['custo_centavos']/100:.2f}")
    print(f"  Cola: {cola['descricao']} - R$ {cola['custo_centavos']/100:.2f}")
    
    print("\n=== CALCULANDO PARA DESCOBRIR OS PARÂMETROS ===")
    
    # Se o perfil tem fator 17.5000 e custo R$ 113.40
    # E o perfil custa R$ 6.48/m
    # Então: quantidade = 113.40 / 6.48 = 17.5
    
    # Testando com fator perda 5% = 1.05
    fator_perda = 1.05
    
    print(f"1. PERFIL:")
    print(f"   Custo total: R$ 113.40")
    print(f"   Custo unitário: R$ {perfil['custo_centavos']/100:.2f}")
    print(f"   Se fator = 17.5000, então custo sem perda = 113.40 / 1.05 = {113.40 / 1.05:.2f}")
    print(f"   Metros lineares = {113.40 / 1.05 / (perfil['custo_centavos']/100):.4f}")
    
    print(f"\n2. CHAVETA:")
    print(f"   Custo total: R$ 29.68")
    print(f"   Custo unitário: R$ {chaveta['custo_centavos']/100:.2f}")
    print(f"   Se fator = 14.0000, então custo sem perda = 29.68 / 1.05 = {29.68 / 1.05:.2f}")
    print(f"   Quantidade chaveta = {29.68 / 1.05 / (chaveta['custo_centavos']/100):.4f}")
    
    print(f"\n3. COLA:")
    print(f"   Custo total: R$ 5.47")
    print(f"   Custo unitário: R$ {cola['custo_centavos']/100:.2f}")
    print(f"   Se fator = 0.0630, então custo sem perda = 5.47 / 1.05 = {5.47 / 1.05:.2f}")
    print(f"   Quantidade cola = {5.47 / 1.05 / (cola['custo_centavos']/100):.6f}")
    
    print(f"\n4. MÃO DE OBRA:")
    print(f"   Custo total: R$ 26.32")
    print(f"   Tempo: 0.4000h")
    print(f"   Valor hora = 26.32 / 0.4 = R$ {26.32 / 0.4:.2f}/h")
    
    print("\n=== DESCOBRINDO FÓRMULAS ===")
    
    # Se metros lineares = 17.5, vamos descobrir vão, comprimento e eixo_i
    # Fórmula: (comprimento / eixo_i) * (vao / 1000) = 17.5
    
    print("Perfil: metros lineares = 17.5")
    print("Fórmula: (comprimento / eixo_i) * (vao / 1000) = 17.5")
    print("Possibilidades:")
    print("  - Se vao=400, eixo_i=40: comprimento = 17.5 * 1000 * 40 / 400 = 1750")
    print("  - Se vao=350, eixo_i=25: comprimento = 17.5 * 1000 * 25 / 350 = 1250")
    print("  - Se vao=700, eixo_i=25: comprimento = 17.5 * 1000 * 25 / 700 = 625")
    
    # Para chaveta: quantidade = (vao / 150) * 2 = 14.0
    # vao = 14.0 * 150 / 2 = 1050
    print(f"\nChaveta: quantidade = (vao / 150) * 2 = 14.0")
    print(f"  vao = 14.0 * 150 / 2 = {14.0 * 150 / 2}")
    
    print(f"\nCola: quantidade = 0.063 (parece ser 0.06 + perda)")
    print(f"  0.06 * 1.05 = {0.06 * 1.05:.3f}")

if __name__ == "__main__":
    testar_parametros_imagem()