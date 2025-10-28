#!/usr/bin/env python3
"""
Script para testar as funcionalidades JavaScript que estavam com erro
"""

import os
import django
import requests
import json
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem

def testar_endpoint_atualizar_ipi():
    """Testa o endpoint de atualização de IPI"""
    print("=== TESTE DO ENDPOINT DE ATUALIZAÇÃO DE IPI ===\n")
    
    # Buscar um orçamento e seus itens
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    item = orcamento.itens.first()
    if not item:
        print("❌ Nenhum item de orçamento encontrado")
        return
    
    print(f"Testando orçamento ID: {orcamento.id}")
    print(f"Testando item ID: {item.id}")
    print(f"IPI atual: {item.ipi_item}%")
    
    # Obter CSRF token
    session = requests.Session()
    csrf_response = session.get(f"http://localhost:8000/orcamento/{orcamento.id}/")
    if csrf_response.status_code != 200:
        print(f"❌ Erro ao obter CSRF token: {csrf_response.status_code}")
        return
    
    # Testar valores válidos
    valores_teste = [0, 5, 10, 15, 100]
    
    for valor in valores_teste:
        try:
            url = f"http://localhost:8000/orcamento/{orcamento.id}/"
            data = {
                'edit_item_id': item.id,
                'ipi': valor,
                'ajax_update_ipi': 'true'
            }
            
            response = session.post(url, data=data, headers={
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('success'):
                        print(f"✅ IPI {valor}%: {result.get('message', 'OK')}")
                    else:
                        print(f"❌ IPI {valor}%: {result.get('error', 'Erro desconhecido')}")
                except json.JSONDecodeError:
                    print(f"❌ IPI {valor}%: Resposta não é JSON válido")
            else:
                print(f"❌ IPI {valor}%: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ IPI {valor}%: Erro na requisição - {e}")
    
    # Testar valores inválidos
    print("\n--- Testando valores inválidos ---")
    valores_invalidos = [-5, 150, 999]
    
    for valor in valores_invalidos:
        try:
            url = f"http://localhost:8000/orcamento/{orcamento.id}/"
            data = {
                'edit_item_id': item.id,
                'ipi': valor,
                'ajax_update_ipi': 'true'
            }
            
            response = session.post(url, data=data, headers={
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            if response.status_code == 400 or (response.status_code == 200 and not response.json().get('success')):
                print(f"✅ IPI {valor}%: Rejeitado corretamente")
            else:
                print(f"❌ IPI {valor}%: Deveria ter sido rejeitado (Status: {response.status_code})")
                
        except Exception as e:
            print(f"❌ IPI {valor}%: Erro na requisição - {e}")

def testar_endpoint_atualizar_lucro():
    """Testa o endpoint de atualização de lucro"""
    print("\n=== TESTE DO ENDPOINT DE ATUALIZAÇÃO DE LUCRO ===\n")
    
    # Buscar um orçamento e seus itens
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    item = orcamento.itens.first()
    if not item:
        print("❌ Nenhum item de orçamento encontrado")
        return
    
    print(f"Testando orçamento ID: {orcamento.id}")
    print(f"Testando item ID: {item.id}")
    print(f"Lucro atual: {item.desconto_item}%")  # desconto_item é o campo de lucro
    
    # Obter CSRF token
    session = requests.Session()
    csrf_response = session.get(f"http://localhost:8000/orcamento/{orcamento.id}/")
    if csrf_response.status_code != 200:
        print(f"❌ Erro ao obter CSRF token: {csrf_response.status_code}")
        return
    
    # Testar valores que quando somados com impostos não passem de 100%
    valores_teste = [10, 20, 30]
    
    for valor in valores_teste:
        try:
            url = f"http://localhost:8000/orcamento/{orcamento.id}/"
            data = {
                'edit_item_id': item.id,
                'lucro': valor,
                'ajax_update_lucro': 'true'  # Assumindo que existe este parâmetro
            }
            
            response = session.post(url, data=data, headers={
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('success'):
                        print(f"✅ Lucro {valor}%: {result.get('message', 'OK')}")
                    else:
                        print(f"❌ Lucro {valor}%: {result.get('error', 'Erro desconhecido')}")
                except json.JSONDecodeError:
                    print(f"❌ Lucro {valor}%: Resposta não é JSON válido")
            else:
                print(f"❌ Lucro {valor}%: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Lucro {valor}%: Erro na requisição - {e}")

def testar_calculo_total():
    """Testa se o cálculo do total está funcionando"""
    print("\n=== TESTE DE CÁLCULO DE TOTAL ===\n")
    
    # Buscar um orçamento
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    print(f"Testando orçamento ID: {orcamento.id}")
    
    total_calculado = 0
    for item in orcamento.itens.all():
        # Usar os nomes corretos dos campos
        preco_base = float(item.valor_unitario or 0)  # valor_unitario em vez de preco_item
        quantidade = float(item.quantidade or 1)
        lucro = float(item.desconto_item or 0)  # desconto_item é o campo de lucro
        impostos = float(item.imposto_item or 0)  # imposto_item
        ipi = float(item.ipi_item or 0)
        
        # Calcular como no JavaScript
        subtotal = preco_base * quantidade
        
        # Aplicar lucro e impostos (conforme a nova fórmula)
        # Valor Unitário Final = Custo Unit / (1 - (impostos + lucro)/100)
        impostos_lucro_percent = (impostos + lucro) / 100
        if impostos_lucro_percent < 1:  # Validação que adicionamos (< 100%)
            denominador = 1 - impostos_lucro_percent
            valor_com_lucro_impostos = subtotal / denominador
        else:
            valor_com_lucro_impostos = subtotal  # Se inválido, usar apenas subtotal
        
        # Aplicar IPI sobre o valor final
        valor_final = valor_com_lucro_impostos * (1 + ipi / 100)
        
        total_calculado += valor_final
        
        print(f"Item {item.id}: R$ {preco_base} x {quantidade} = R$ {subtotal:.2f}")
        print(f"  + {lucro}% lucro + {impostos}% impostos + {ipi}% IPI = R$ {valor_final:.2f}")
    
    print(f"\nTotal calculado: R$ {total_calculado:.2f}")
    print(f"Total no orçamento: R$ {orcamento.valor_total or 0:.2f}")

def main():
    print("=== TESTE DAS FUNCIONALIDADES JAVASCRIPT ===")
    print(f"Timestamp: {datetime.now()}\n")
    
    try:
        testar_endpoint_atualizar_ipi()
        testar_endpoint_atualizar_lucro()
        testar_calculo_total()
        
        print("\n=== TESTE CONCLUÍDO ===")
        print("✅ Se todos os testes passaram, as funcionalidades JavaScript devem estar funcionando")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()