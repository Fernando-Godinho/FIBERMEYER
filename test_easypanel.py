#!/usr/bin/env python3
"""
Script para testar se o FIBERMEYER está funcionando corretamente no EasyPanel
"""

import requests
import time
import sys
from urllib.parse import urljoin

def test_fibermeyer(base_url):
    """Testa se o FIBERMEYER está funcionando"""
    
    print("🧪 TESTANDO FIBERMEYER NO EASYPANEL")
    print("=" * 50)
    print(f"🌐 URL Base: {base_url}")
    print()
    
    tests = [
        {
            'name': 'Página Principal',
            'url': '',
            'expected_status': 200,
            'expected_content': ['FIBERMEYER', 'Django']
        },
        {
            'name': 'Admin Login',
            'url': '/admin/',
            'expected_status': 200,
            'expected_content': ['Django', 'administration', 'login']
        },
        {
            'name': 'Sistema de Orçamentos',
            'url': '/orcamento/',
            'expected_status': 200,
            'expected_content': ['orçamento', 'FIBERMEYER']
        },
        {
            'name': 'API de Impostos',
            'url': '/api/impostos/',
            'expected_status': 200,
            'expected_content': []
        }
    ]
    
    success_count = 0
    total_tests = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"{i}️⃣ Testando {test['name']}...")
        
        try:
            url = urljoin(base_url, test['url'])
            print(f"   📡 GET {url}")
            
            response = requests.get(url, timeout=10)
            
            # Verificar status code
            if response.status_code == test['expected_status']:
                print(f"   ✅ Status: {response.status_code} (OK)")
                status_ok = True
            else:
                print(f"   ❌ Status: {response.status_code} (Esperado: {test['expected_status']})")
                status_ok = False
            
            # Verificar conteúdo
            content_ok = True
            if test['expected_content']:
                for expected in test['expected_content']:
                    if expected.lower() in response.text.lower():
                        print(f"   ✅ Conteúdo contém: '{expected}'")
                    else:
                        print(f"   ❌ Conteúdo NÃO contém: '{expected}'")
                        content_ok = False
            else:
                print("   ✅ Sem verificação de conteúdo")
            
            if status_ok and content_ok:
                print(f"   🎉 {test['name']} - PASSOU!")
                success_count += 1
            else:
                print(f"   💥 {test['name']} - FALHOU!")
            
        except requests.exceptions.ConnectHttpError:
            print(f"   ❌ Erro de conexão - Verifique se o serviço está rodando")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout - Serviço pode estar lento")
        except Exception as e:
            print(f"   💥 Erro inesperado: {e}")
        
        print()
    
    # Resultado final
    print("📊 RESULTADO FINAL")
    print("=" * 30)
    print(f"✅ Testes que passaram: {success_count}/{total_tests}")
    print(f"❌ Testes que falharam: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ FIBERMEYER está funcionando perfeitamente!")
        print("\n📱 Próximos passos:")
        print(f"1. Acesse: {base_url}/admin/")
        print("2. Login: admin / admin123")
        print("3. MUDE A SENHA DO ADMIN!")
        print(f"4. Teste o sistema: {base_url}/orcamento/")
        print("5. Crie um orçamento e gere PDF")
        
    elif success_count > 0:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        print("O sistema pode estar iniciando ainda...")
        print("💡 Aguarde mais alguns minutos e teste novamente")
        
    else:
        print("\n❌ TODOS OS TESTES FALHARAM")
        print("🔧 Verifique:")
        print("1. O deploy terminou?")
        print("2. Os containers estão rodando?")
        print("3. O domínio está configurado corretamente?")
        print("4. As portas estão liberadas?")
    
    return success_count == total_tests

def main():
    """Função principal"""
    if len(sys.argv) != 2:
        print("📖 USO:")
        print("python test_easypanel.py https://seu-dominio.com")
        print("python test_easypanel.py https://fibermeyer.seu-easypanel.com")
        print("\nExemplos:")
        print("python test_easypanel.py https://fibermeyer.example.com")
        print("python test_easypanel.py http://localhost:8000")
        return
    
    base_url = sys.argv[1].rstrip('/')
    
    print("⏳ Aguardando 10 segundos para o serviço estar pronto...")
    time.sleep(10)
    
    success = test_fibermeyer(base_url)
    
    if success:
        print("\n🎊 PARABÉNS! Seu FIBERMEYER está funcionando no EasyPanel!")
        sys.exit(0)
    else:
        print("\n🔧 Alguns testes falharam. Verifique os logs e tente novamente.")
        sys.exit(1)

if __name__ == "__main__":
    main()