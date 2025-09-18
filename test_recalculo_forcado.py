#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente
from django.test import Client

def test_recalculo_forcado():
    """Testa o recálculo forçado via API"""
    try:
        # Verificar produto antes do recálculo
        produto = MP_Produtos.objects.get(id=1392)
        custo_antes = produto.custo_centavos
        print(f"=== TESTE DE RECÁLCULO FORÇADO ===")
        print(f"Produto: {produto.descricao}")
        print(f"Custo antes: R$ {custo_antes/100:.2f}")
        
        # Simular recálculo forçado
        client = Client()
        
        # Preparar dados da requisição
        data = {
            'force_recalculate': True
        }
        
        # Fazer requisição PATCH para forçar recálculo
        response = client.patch(
            f'/api/produtos/{produto.id}/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        print(f"Status da requisição: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar produto após recálculo
            produto.refresh_from_db()
            custo_depois = produto.custo_centavos
            
            print(f"Custo depois: R$ {custo_depois/100:.2f}")
            diferenca = custo_depois - custo_antes
            print(f"Diferença: R$ {diferenca/100:.2f}")
            
            if abs(diferenca) < 1:  # Menos de 1 centavo
                print("✅ Recálculo manteve o valor correto")
            else:
                print(f"⚠️ Recálculo alterou o valor em R$ {diferenca/100:.2f}")
                
            # Mostrar dados da resposta
            response_data = response.json()
            print(f"Custo na resposta: R$ {response_data['custo_centavos']/100:.2f}")
        else:
            print(f"❌ Erro na requisição: {response.content}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    test_recalculo_forcado()
