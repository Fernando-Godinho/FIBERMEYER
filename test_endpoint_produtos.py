#!/usr/bin/env python3
"""
Teste do endpoint /api/produtos/ para salvamento de perfis parametrizados.
"""

import requests
import json
from datetime import datetime

def testar_endpoint_produtos():
    print("=== TESTE DO ENDPOINT /api/produtos/ ===")
    print()
    
    # URL do endpoint
    url = "http://127.0.0.1:8000/api/produtos/"
    
    # Primeiro, vamos obter o CSRF token através de uma requisição GET
    session = requests.Session()
    
    try:
        # Obter página principal para pegar o CSRF token
        response_csrf = session.get("http://127.0.0.1:8000/mp/")
        csrf_token = None
        
        # Extrair CSRF token dos cookies
        if 'csrftoken' in session.cookies:
            csrf_token = session.cookies['csrftoken']
            print(f"✅ CSRF Token obtido: {csrf_token[:10]}...")
        else:
            print("❌ Não foi possível obter CSRF token")
            return False
        
        # Dados de teste para um perfil
        dados_perfil = {
            "nome_perfil": "Perfil Teste API 50x25mm",
            "roving_4400_kg": 0.4,
            "manta_300_kg": 0.2,
            "veu_kg": 0.1,
            "peso_metro_kg": 1.0,
            "tem_pintura": True,
            "area_pintura_m2": 0.6,
            "metros_produzidos_h": 15,
            "n_matrizes": 2,
            "n_maquinas": 1
        }
        
        # Simular os dados que seriam enviados pelo frontend
        produto_data = {
            "descricao": dados_perfil["nome_perfil"],
            "custo_centavos": 2850,  # R$ 28,50 simulado
            "peso_und": str(dados_perfil["peso_metro_kg"]),
            "unidade": "M",  # Metro linear
            "referencia": f"PER-5025-{datetime.now().strftime('%H%M')}",
            "tipo": "Perfil",
            "categoria": "Perfis",
            "subcategoria": "Pultrusão",
            "data_revisao": datetime.now().isoformat(),
            "dados_perfil": json.dumps(dados_perfil)
        }
        
        print("📦 DADOS DO PRODUTO A SEREM ENVIADOS:")
        for chave, valor in produto_data.items():
            if chave == "dados_perfil":
                print(f"  {chave}: {valor[:50]}... (JSON truncado)")
            else:
                print(f"  {chave}: {valor}")
        
        print("\n🚀 ENVIANDO REQUISIÇÃO POST...")
        
        # Headers da requisição
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Referer': 'http://127.0.0.1:8000/mp/'
        }
        
        # Enviar requisição POST
        response = session.post(url, 
                              headers=headers,
                              data=json.dumps(produto_data))
        
        print(f"📡 Status da resposta: {response.status_code}")
        print(f"📡 Headers de resposta: {dict(response.headers)}")
        
        if response.status_code == 200 or response.status_code == 201:
            try:
                resultado = response.json()
                print("✅ PRODUTO CRIADO COM SUCESSO!")
                print("📋 Dados retornados:")
                for chave, valor in resultado.items():
                    if chave == "dados_perfil":
                        print(f"  {chave}: {str(valor)[:50]}... (JSON truncado)")
                    else:
                        print(f"  {chave}: {valor}")
                return True
                
            except json.JSONDecodeError:
                print(f"✅ Produto criado (status {response.status_code})")
                print(f"📝 Resposta em texto: {response.text[:200]}...")
                return True
                
        else:
            print(f"❌ ERRO NA REQUISIÇÃO!")
            print(f"📝 Resposta: {response.text}")
            
            # Tentar parsear JSON de erro
            try:
                erro = response.json()
                print("📋 Detalhes do erro:")
                for chave, valor in erro.items():
                    print(f"  {chave}: {valor}")
            except:
                pass
                
            return False
            
    except requests.ConnectionError:
        print("❌ ERRO DE CONEXÃO!")
        print("🔧 Verifique se o servidor Django está rodando em http://127.0.0.1:8000/")
        return False
        
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        return False

def verificar_servidor():
    print("🔍 VERIFICANDO SE SERVIDOR ESTÁ ATIVO...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Django está rodando")
            return True
        else:
            print(f"⚠️ Servidor responde mas com status {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ Servidor Django não está acessível")
        print("💡 Execute: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar servidor: {e}")
        return False

def main():
    print("🧪 TESTE DE INTEGRAÇÃO - SALVAMENTO DE PERFIS")
    print("=" * 60)
    
    # Verificar se servidor está rodando
    if not verificar_servidor():
        return
    
    print()
    
    # Testar endpoint
    sucesso = testar_endpoint_produtos()
    
    print()
    print("=" * 60)
    
    if sucesso:
        print("🎉 TESTE PASSOU! Endpoint funcionando corretamente")
        print("💡 Agora você pode testar no frontend em:")
        print("   http://127.0.0.1:8000/mp/")
        print("   1. Selecione 'Novo Perfil'")
        print("   2. Preencha os campos")
        print("   3. Clique em 'Calcular'")
        print("   4. Clique em 'Salvar Produto'")
        print("   ✅ A função gerarReferenciaPerfil() agora está disponível")
    else:
        print("❌ TESTE FALHOU! Verifique:")
        print("   1. Se o servidor Django está rodando")
        print("   2. Se o endpoint /api/produtos/ existe")
        print("   3. Se não há erros de CSRF")
        print("   4. Se o modelo Produto existe na base")

if __name__ == "__main__":
    main()
