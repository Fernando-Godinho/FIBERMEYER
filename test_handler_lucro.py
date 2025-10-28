#!/usr/bin/env python3
"""
Teste do handler AJAX de atualização de lucro
"""

import os
import django
import requests
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem

def testar_handler_lucro():
    """Testa o endpoint de atualização de lucro"""
    print("=== TESTE DO HANDLER AJAX DE LUCRO ===")
    print(f"Timestamp: {datetime.now()}\n")
    
    # Buscar um orçamento e item
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado")
        return
    
    item = orcamento.itens.first()
    if not item:
        print("❌ Nenhum item encontrado")
        return
    
    print(f"🧪 Testando com:")
    print(f"   Orçamento ID: {orcamento.id}")
    print(f"   Item ID: {item.id}")
    print(f"   Lucro atual: {item.desconto_item}%")
    print(f"   Valor atual: R$ {item.valor_total}")
    print()
    
    # Obter session e CSRF token
    session = requests.Session()
    url = f"http://localhost:8000/orcamento/{orcamento.id}/"
    
    try:
        # Primeiro, obter a página para pegar o CSRF token
        response = session.get(url)
        if response.status_code != 200:
            print(f"❌ Erro ao obter página: {response.status_code}")
            return
            
        print("✅ Página obtida com sucesso")
        
        # Testar diferentes valores de lucro
        valores_teste = [10, 25, 45, 30]
        
        for novo_lucro in valores_teste:
            print(f"\n🔧 Testando lucro: {novo_lucro}%")
            
            # Dados para enviar
            data = {
                'edit_item_id': item.id,
                'lucro': novo_lucro,
                'ajax_update_lucro': 'true'
            }
            
            # Fazer requisição AJAX
            ajax_response = session.post(url, data=data, headers={
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            print(f"   Status: {ajax_response.status_code}")
            
            if ajax_response.status_code == 200:
                try:
                    json_data = ajax_response.json()
                    if json_data.get('success'):
                        print(f"   ✅ Sucesso: {json_data.get('message')}")
                        print(f"   📊 Novo total: R$ {json_data.get('novo_total')}")
                        print(f"   📈 Total orçamento: R$ {json_data.get('total_orcamento')}")
                    else:
                        print(f"   ❌ Erro: {json_data.get('error')}")
                except Exception as e:
                    print(f"   ❌ Erro ao parsear JSON: {e}")
                    print(f"   📄 Resposta: {ajax_response.text[:200]}...")
            else:
                print(f"   ❌ Erro HTTP: {ajax_response.status_code}")
                print(f"   📄 Resposta: {ajax_response.text[:200]}...")
        
        # Verificar se o valor foi atualizado no banco
        print(f"\n🔍 Verificação final:")
        item.refresh_from_db()
        print(f"   Lucro final: {item.desconto_item}%")
        print(f"   Valor final: R$ {item.valor_total}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor não está rodando?")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def testar_calculo_manual():
    """Testa o cálculo manual da nova fórmula"""
    print("\n" + "=" * 50)
    print("🧮 TESTE DE CÁLCULO MANUAL")
    print("=" * 50)
    
    # Dados do exemplo do usuário
    custo = 4.15
    quantidade = 250
    impostos = 33.93  # %
    lucro = 45        # %
    ipi = 0           # %
    
    print(f"📋 Dados de entrada:")
    print(f"   Custo unitário: R$ {custo}")
    print(f"   Quantidade: {quantidade}")
    print(f"   Impostos: {impostos}%")
    print(f"   Lucro: {lucro}%")
    print(f"   IPI: {ipi}%")
    print()
    
    # Cálculo sequencial
    print("🔢 Cálculo sequencial:")
    
    # 1. Valor Base
    valor_base = custo * quantidade
    print(f"   1. Valor Base: R$ {custo} × {quantidade} = R$ {valor_base:.2f}")
    
    # 2. + Impostos
    valor_com_impostos = valor_base * (1 + impostos / 100)
    print(f"   2. + Impostos ({impostos}%): R$ {valor_com_impostos:.2f}")
    
    # 3. + Lucro
    valor_com_lucro = valor_com_impostos * (1 + lucro / 100)
    print(f"   3. + Lucro ({lucro}%): R$ {valor_com_lucro:.2f}")
    
    # 4. + IPI
    valor_final = valor_com_lucro * (1 + ipi / 100)
    print(f"   4. + IPI ({ipi}%): R$ {valor_final:.2f}")
    
    # Valor unitário final
    valor_unitario_final = valor_final / quantidade
    print(f"   📊 Valor Unitário Final: R$ {valor_unitario_final:.2f}")
    
    print()
    print("✅ Este é o resultado esperado conforme a nova fórmula!")

if __name__ == "__main__":
    testar_handler_lucro()
    testar_calculo_manual()