#!/usr/bin/env python3
import requests

# Verificar impostos disponíveis
response = requests.get('http://127.0.0.1:8000/api/impostos/')
impostos = response.json()

print(f"Total de impostos: {len(impostos)}")
print("\nPrimeiros 20 impostos:")
for i in impostos[:20]:
    print(f"ID: {i['id']}, Nome: \"{i['nome']}\", Alíquota: {i['aliquota']}%")

print("\nAnálise de padrões de nomenclatura:")
estados_encontrados = set()
tipos_encontrados = set()

for imposto in impostos:
    nome = imposto['nome']
    
    # Verificar padrões conhecidos
    if 'ICMS' in nome.upper():
        # Extrair estado
        import re
        match = re.search(r'\b([A-Z]{2})\b', nome)
        if match:
            estados_encontrados.add(match.group(1))
        
        # Extrair tipo
        if 'Interno' in nome:
            tipos_encontrados.add('Interno')
        elif 'Interestadual' in nome:
            tipos_encontrados.add('Interestadual')
        elif 'DIFAL' in nome:
            tipos_encontrados.add('DIFAL')

print(f"\nEstados encontrados: {sorted(estados_encontrados)}")
print(f"Tipos encontrados: {sorted(tipos_encontrados)}")

# Buscar especificamente impostos para BA
impostos_ba = [i for i in impostos if 'BA' in i['nome']]
print(f"\nImpostos para BA ({len(impostos_ba)}):")
for imposto in impostos_ba:
    print(f"  {imposto['nome']} - {imposto['aliquota']}%")