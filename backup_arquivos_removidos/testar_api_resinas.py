#!/usr/bin/env python
import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

# Testar se o servidor está rodando
try:
    response = requests.get('http://localhost:8000/api/produtos/')
    print(f'Status da API: {response.status_code}')
    
    if response.status_code == 200:
        produtos_api = response.json()
        print(f'Produtos retornados pela API: {len(produtos_api)}')
        
        # Verificar alguns produtos de resina
        resinas_api = [p for p in produtos_api if 'resina' in p['descricao'].lower()]
        print(f'Produtos de resina na API: {len(resinas_api)}')
        
        for resina in resinas_api[:5]:  # Primeiros 5
            print(f'  ID: {resina["id"]} - {resina["descricao"]} - R$ {resina["custo_centavos"]/100:.2f}')
    else:
        print(f'Erro na API: {response.text}')
        
except requests.exceptions.ConnectionError:
    print('Erro: Servidor não está rodando na porta 8000')
except Exception as e:
    print(f'Erro inesperado: {e}')

# Comparar com banco direto
print('\n=== COMPARAÇÃO COM BANCO DIRETO ===')
resinas_banco = MP_Produtos.objects.filter(descricao__icontains='resina')
print(f'Produtos de resina no banco: {resinas_banco.count()}')
