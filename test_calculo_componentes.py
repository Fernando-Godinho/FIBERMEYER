#!/usr/bin/env python3

"""
Teste do cálculo de componentes para verificar se a lógica está correta
"""

# Dados de exemplo
dados = {
    'peso_metro_kg': 2.5,
    'roving_4400_kg': 1.2,
    'manta_300_kg': 0.8, 
    'veu_kg': 0.2
}

# Peso da resina base = peso do metro - (roving + manta + véu)
peso_resina_base = dados['peso_metro_kg'] - (dados['roving_4400_kg'] + dados['manta_300_kg'] + dados['veu_kg'])

print(f"Peso do metro: {dados['peso_metro_kg']} kg")
print(f"Peso fibras (roving + manta + véu): {dados['roving_4400_kg'] + dados['manta_300_kg'] + dados['veu_kg']} kg")
print(f"Peso resina base: {peso_resina_base} kg")
print()

# Fatores de multiplicação conforme especificado
fatores = {
    'resina': 0.6897,           # 68.97%
    'monomero': 0.0213,         # 2.13%
    'antiUV': 0.0028,           # 0.28%
    'antiOX': 0.0011,           # 0.11%
    'bpo': 0.0071,              # 0.71%
    'tbpb': 0.0043,             # 0.43%
    'desmoldante': 0.0071,      # 0.71%
    'antichama': 0.1777,        # 17.77%
    'cargaMineral': 0.0711,     # 7.11%
    'pigmento': 0.0178          # 1.78%
}

print("COMPONENTES CALCULADOS:")
print("-" * 80)
print(f"{'Componente':<25} {'Quantidade':<12} {'Custo Unit':<12} {'Custo Total':<12}")
print("-" * 80)

componentes = [
    ('Roving 4400 KG', dados['roving_4400_kg'], 8.50),
    ('Manta 300 KG', dados['manta_300_kg'], 12.00),
    ('Véu KG', dados['veu_kg'], 25.00),
    ('Resina PET', peso_resina_base * fatores['resina'], 12.96),
    ('Monômero de estireno', peso_resina_base * fatores['monomero'], 8.00),
    ('Anti UV', peso_resina_base * fatores['antiUV'], 45.00),
    ('Anti OX', peso_resina_base * fatores['antiOX'], 35.00),
    ('BPO', peso_resina_base * fatores['bpo'], 28.00),
    ('TBPB', peso_resina_base * fatores['tbpb'], 42.00),
    ('Desmoldante', peso_resina_base * fatores['desmoldante'], 22.00),
    ('Antichama', peso_resina_base * fatores['antichama'], 18.50),
    ('Carga mineral', peso_resina_base * fatores['cargaMineral'], 3.20),
    ('Pigmento', peso_resina_base * fatores['pigmento'], 15.80)
]

custo_total = 0
for nome, quantidade, custo_unit in componentes:
    custo_comp = quantidade * custo_unit
    custo_total += custo_comp
    print(f"{nome:<25} {quantidade:<12.4f} R$ {custo_unit:<9.2f} R$ {custo_comp:<9.2f}")

print("-" * 80)
print(f"{'CUSTO TOTAL':<25} {'':<12} {'':<12} R$ {custo_total:<9.2f}")
print("-" * 80)

# Verificar se os percentuais somam 100%
soma_fatores = sum(fatores.values())
print(f"\nSoma dos fatores: {soma_fatores:.4f} ({soma_fatores*100:.2f}%)")

if abs(soma_fatores - 1.0) > 0.001:
    print("⚠️  ATENÇÃO: Os fatores não somam 100%!")
else:
    print("✅ Fatores corretos - somam 100%")
