#!/usr/bin/env python3
"""
Script para testar se o setup do Docker está funcionando corretamente
"""

import os
import time
import subprocess
import requests
from urllib.parse import urljoin

def run_command(command, description):
    """Executa um comando e retorna o resultado"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True, result.stdout
        else:
            print(f"❌ {description} - ERRO")
            print(f"Erro: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ {description} - EXCEÇÃO: {e}")
        return False, str(e)

def test_url(url, description, timeout=10):
    """Testa se uma URL está respondendo"""
    print(f"🌐 Testando {description}: {url}")
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {description} - OK (Status: {response.status_code})")
            return True
        else:
            print(f"⚠️ {description} - Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectHTrottleror:
        print(f"❌ {description} - Erro de conexão")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Erro: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DO SETUP DOCKER - FIBERMEYER")
    print("=" * 50)
    
    # Teste 1: Docker está instalado?
    print("\n1️⃣ VERIFICANDO DOCKER")
    print("-" * 30)
    docker_ok, _ = run_command("docker --version", "Verificando Docker")
    
    if not docker_ok:
        print("❌ Docker não encontrado! Instale o Docker Desktop.")
        return
    
    # Teste 2: Docker Compose está disponível?
    compose_ok, _ = run_command("docker-compose --version", "Verificando Docker Compose")
    
    if not compose_ok:
        print("❌ Docker Compose não encontrado!")
        return
    
    # Teste 3: Containers estão rodando?
    print("\n2️⃣ VERIFICANDO CONTAINERS")
    print("-" * 30)
    containers_ok, containers_output = run_command("docker-compose ps", "Listando containers")
    
    if containers_ok:
        print("📋 Status dos containers:")
        print(containers_output)
    
    # Teste 4: Logs do container principal
    print("\n3️⃣ VERIFICANDO LOGS DA APLICAÇÃO")
    print("-" * 30)
    logs_ok, logs_output = run_command("docker-compose logs --tail=10 app", "Últimos logs da aplicação")
    
    if logs_ok and logs_output:
        print("📄 Últimos logs:")
        print(logs_output[-500:])  # Últimos 500 caracteres
    
    # Teste 5: Aguardar um pouco para o servidor subir
    print("\n4️⃣ AGUARDANDO SERVIDOR INICIALIZAR")
    print("-" * 30)
    print("⏳ Aguardando 10 segundos...")
    time.sleep(10)
    
    # Teste 6: Testar URLs
    print("\n5️⃣ TESTANDO CONECTIVIDADE")
    print("-" * 30)
    
    urls_to_test = [
        ("http://localhost:8000", "Página principal FIBERMEYER"),
        ("http://localhost:8000/admin/", "Django Admin"),
        ("http://localhost:8000/orcamento/", "Sistema de orçamentos"),
    ]
    
    all_urls_ok = True
    for url, description in urls_to_test:
        if not test_url(url, description):
            all_urls_ok = False
    
    # Teste 7: Se tem PostgreSQL, testar adminer
    if os.path.exists("docker-compose.yml") and "adminer" in open("docker-compose.yml").read():
        test_url("http://localhost:8080", "Adminer (gerenciador de banco)")
    
    # Resultado final
    print("\n📊 RESULTADO FINAL")
    print("=" * 30)
    
    if docker_ok and compose_ok and all_urls_ok:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n📱 Acessos disponíveis:")
        print("   🌐 FIBERMEYER: http://localhost:8000")
        print("   👨‍💼 Admin: http://localhost:8000/admin/")
        print("   🔑 Login: admin / Senha: admin123")
        
        if os.path.exists("docker-compose.yml") and "adminer" in open("docker-compose.yml").read():
            print("   🗄️ Banco: http://localhost:8080")
        
        print("\n✅ Setup funcionando perfeitamente!")
        
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("\n🔧 Possíveis soluções:")
        print("1. Execute: docker-compose down && docker-compose up -d")
        print("2. Verifique os logs: docker-compose logs -f app")
        print("3. Confirme que as portas 8000, 5432, 8080 estão livres")
        
    print("\n📋 Comandos úteis:")
    print("   docker-compose logs -f app    # Ver logs em tempo real")
    print("   docker-compose restart app    # Reiniciar aplicação")
    print("   docker-compose down           # Parar tudo")

if __name__ == "__main__":
    main()