#!/usr/bin/env python
"""
Debug dos tipos de dados da API
"""

import requests

def debug_tipos_api():
    print("=== DEBUG TIPOS DE DADOS DA API ===")
    
    response = requests.get('http://127.0.0.1:8000/api/produtos/')
    produtos = response.json()
    
    # Pegar o perfil 1328
    perfil = next((p for p in produtos if p['id'] == 1328), None)
    
    if perfil:
        print("Perfil 1328:")
        for key, value in perfil.items():
            print(f"  {key}: {value} (tipo: {type(value)})")
    
    print("\n" + "="*50)
    
    # Pegar chaveta 1332
    chaveta = next((p for p in produtos if p['id'] == 1332), None)
    
    if chaveta:
        print("Chaveta 1332:")
        for key, value in chaveta.items():
            print(f"  {key}: {value} (tipo: {type(value)})")

if __name__ == "__main__":
    debug_tipos_api()