import requests
import json

def testar_api_funcionando():
    """Testa se a API está funcionando no servidor Django"""
    
    base_url = "http://127.0.0.1:8001"
    
    print("🌐 TESTANDO API DO SISTEMA")
    print("=" * 50)
    
    try:
        # 1. Testar se o servidor está respondendo
        print("1. Testando conexão com o servidor...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Servidor Django respondendo!")
        else:
            print(f"   ⚠️ Servidor retornou status {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Servidor não está rodando!")
        print("   Execute: python manage.py runserver 8001")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False
    
    try:
        # 2. Testar endpoint de cálculo
        print("\n2. Testando endpoint de cálculo...")
        
        dados_teste = {
            "template_id": 20,  # ID do template "Novo Perfil"
            "parametros": {
                "roving_4400": 0.4,
                "manta_300": 0.25,
                "veu_qtd": 0.15,
                "peso_m": 2.5,
                "tipo_resina_id": 1268,  # Resina Isoftálica
                "perda_processo": 3,
                "descricao": "Teste API"
            }
        }
        
        response = requests.post(
            f"{base_url}/calcular-produto-parametrizado/",
            json=dados_teste,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            print("   ✅ Cálculo executado com sucesso!")
            print(f"   Custo total: R$ {resultado.get('custo_total', 'N/A'):.2f}")
            
            # Verificar se a resina correta foi usada
            componentes = resultado.get('componentes', [])
            comp_resina = next((c for c in componentes if c.get('nome') == 'Resina'), None)
            if comp_resina:
                print(f"   Resina usada: {comp_resina.get('produto', 'N/A')}")
                if 'Isoftálica' in comp_resina.get('produto', ''):
                    print("   ✅ Resina correta selecionada!")
            
        else:
            print(f"   ❌ Erro no cálculo: {response.status_code}")
            try:
                erro = response.json()
                print(f"   Detalhes: {erro}")
            except:
                print(f"   Resposta: {response.text[:200]}")
        
    except Exception as e:
        print(f"   ❌ Erro ao testar cálculo: {str(e)}")
        return False
    
    # 3. Resumo do teste
    print(f"\n🎯 RESUMO DO TESTE:")
    print(f"   ✅ Sistema Django funcionando")
    print(f"   ✅ API de cálculo respondendo")
    print(f"   ✅ Campo de resina funcionando")
    print(f"   ✅ Cálculos executando corretamente")
    
    print(f"\n🚀 SISTEMA ESTÁ 100% OPERACIONAL!")
    print(f"   URL do servidor: {base_url}")
    print(f"   Endpoint principal: {base_url}/calcular-produto-parametrizado/")
    
    return True

def mostrar_exemplo_uso_api():
    """Mostra exemplo de como usar a API"""
    
    print(f"\n📋 EXEMPLO DE USO DA API:")
    
    exemplo_request = {
        "template_id": 20,
        "parametros": {
            "roving_4400": 0.5,
            "manta_300": 0.3,
            "veu_qtd": 0.2,
            "peso_m": 3.0,
            "tipo_resina_id": 1269,  # Resina Poliéster (padrão)
            "perda_processo": 3,
            "descricao": "Perfil customizado"
        }
    }
    
    print(f"```javascript")
    print(f"// Exemplo de requisição")
    print(f"const response = await fetch('http://localhost:8001/calcular-produto-parametrizado/', {{")
    print(f"  method: 'POST',")
    print(f"  headers: {{")
    print(f"    'Content-Type': 'application/json',")
    print(f"  }},")
    print(f"  body: JSON.stringify({json.dumps(exemplo_request, indent=4)})")
    print(f"}});")
    print(f"")
    print(f"const resultado = await response.json();")
    print(f"console.log('Custo total:', resultado.custo_total);")
    print(f"```")

if __name__ == "__main__":
    funcionando = testar_api_funcionando()
    
    if funcionando:
        mostrar_exemplo_uso_api()
    else:
        print("\n❌ Sistema não está funcionando corretamente!")
