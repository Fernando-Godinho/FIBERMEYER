#!/usr/bin/env python3
"""
Script para simular uma requisição AJAX de atualização de lucro
"""
import os
import sys
import django
import requests

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from main.models import OrcamentoItem, Orcamento
from decimal import Decimal

def testar_requisicao_ajax():
    """Testa uma requisição AJAX de atualização de lucro"""
    
    print("=== TESTE REQUISIÇÃO AJAX ===\n")
    
    # Buscar um orçamento e item existente
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    item = orcamento.itens.first()
    if not item:
        print("❌ Nenhum item encontrado no orçamento")
        return
    
    print(f"Testando orçamento ID: {orcamento.id}")
    print(f"Item ID: {item.id}")
    print(f"Valor atual: R$ {item.valor_total}")
    print(f"IPI atual: {item.ipi_item}%")
    print()
    
    # Criar cliente Django para simular requisição
    client = Client()
    
    # Dados para atualização de lucro
    post_data = {
        'edit_item_id': item.id,
        'lucro': '30.0',  # 30% de lucro
        'ajax_update': 'true'
    }
    
    # Fazer requisição POST
    response = client.post(f'/orcamento/{orcamento.id}/', post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status da resposta: {response.status_code}")
    
    if response.status_code == 200:
        try:
            import json
            data = json.loads(response.content)
            print(f"Resposta JSON: {data}")
            
            # Recarregar item do banco
            item.refresh_from_db()
            print(f"Novo valor total: R$ {item.valor_total}")
            
            if data.get('success'):
                print("✅ Requisição AJAX de lucro funcionando!")
            else:
                print(f"❌ Erro na requisição: {data.get('error', 'Erro desconhecido')}")
                
        except json.JSONDecodeError:
            print(f"❌ Resposta não é JSON válido: {response.content}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")
        print(f"Conteúdo: {response.content}")

def testar_requisicao_ipi():
    """Testa uma requisição AJAX de atualização de IPI"""
    
    print("\n=== TESTE REQUISIÇÃO AJAX IPI ===\n")
    
    # Buscar um orçamento e item existente
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    item = orcamento.itens.first()
    if not item:
        print("❌ Nenhum item encontrado no orçamento")
        return
    
    print(f"Testando orçamento ID: {orcamento.id}")
    print(f"Item ID: {item.id}")
    print(f"Valor atual: R$ {item.valor_total}")
    print(f"IPI atual: {item.ipi_item}%")
    print()
    
    # Criar cliente Django para simular requisição
    client = Client()
    
    # Dados para atualização de IPI
    post_data = {
        'edit_item_id': item.id,
        'ipi': '15.0',  # 15% de IPI
        'ajax_update_ipi': 'true'
    }
    
    # Fazer requisição POST
    response = client.post(f'/orcamento/{orcamento.id}/', post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"Status da resposta: {response.status_code}")
    
    if response.status_code == 200:
        try:
            import json
            data = json.loads(response.content)
            print(f"Resposta JSON: {data}")
            
            # Recarregar item do banco
            item.refresh_from_db()
            print(f"Novo valor total: R$ {item.valor_total}")
            print(f"Novo IPI: {item.ipi_item}%")
            
            if data.get('success'):
                print("✅ Requisição AJAX de IPI funcionando!")
            else:
                print(f"❌ Erro na requisição: {data.get('error', 'Erro desconhecido')}")
                
        except json.JSONDecodeError:
            print(f"❌ Resposta não é JSON válido: {response.content}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")
        print(f"Conteúdo: {response.content}")

if __name__ == '__main__':
    testar_requisicao_ajax()
    testar_requisicao_ipi()