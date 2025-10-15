#!/usr/bin/env python3
import requests

# Buscar perfis I25 disponíveis
response = requests.get('http://127.0.0.1:8000/api/produtos/')
produtos = response.json()

perfis_i25 = [p for p in produtos if 'i25' in p['descricao'].lower()]
print("Perfis I25 encontrados:")
for p in perfis_i25[:10]:
    print(f"ID {p['id']}: {p['descricao']} - R$ {p['custo_centavos']/100:.2f}")