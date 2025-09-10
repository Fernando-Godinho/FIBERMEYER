#!/usr/bin/env python3
"""
🔄 SCRIPT DE REINICIALIZAÇÃO DO PROJETO FIBERMEYER
Este script para todos os processos e limpa o ambiente para um novo start
"""

import os
import sys
import subprocess
import psutil
import signal

def parar_processos_python():
    """Para todos os processos Python relacionados ao projeto"""
    print("🛑 PARANDO PROCESSOS PYTHON...")
    
    processos_parados = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # Verificar se é processo relacionado ao Django ou ao projeto
                if any(palavra in cmdline.lower() for palavra in ['runserver', 'manage.py', 'django', 'fibermeyer']):
                    print(f"  🔴 Parando processo: PID {proc.info['pid']} - {cmdline[:60]}...")
                    proc.terminate()
                    processos_parados += 1
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if processos_parados > 0:
        print(f"✅ {processos_parados} processo(s) parado(s)")
    else:
        print("ℹ️  Nenhum processo Python do projeto encontrado")
    
    return processos_parados

def limpar_cache():
    """Remove arquivos de cache Python"""
    print("\n🧹 LIMPANDO CACHE...")
    
    cache_dirs = []
    cache_files = []
    
    # Buscar diretórios __pycache__
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            cache_dirs.append(cache_dir)
        
        # Buscar arquivos .pyc
        for file in files:
            if file.endswith('.pyc'):
                cache_files.append(os.path.join(root, file))
    
    # Remover diretórios de cache
    import shutil
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"  🗑️  Removido: {cache_dir}")
        except Exception as e:
            print(f"  ❌ Erro ao remover {cache_dir}: {e}")
    
    # Remover arquivos .pyc
    for cache_file in cache_files:
        try:
            os.remove(cache_file)
            print(f"  🗑️  Removido: {cache_file}")
        except Exception as e:
            print(f"  ❌ Erro ao remover {cache_file}: {e}")
    
    total_removidos = len(cache_dirs) + len(cache_files)
    if total_removidos > 0:
        print(f"✅ {total_removidos} arquivo(s) de cache removido(s)")
    else:
        print("ℹ️  Nenhum arquivo de cache encontrado")

def verificar_ambiente():
    """Verifica se o ambiente virtual está ativo"""
    print("\n🔍 VERIFICANDO AMBIENTE...")
    
    # Verificar se está em ambiente virtual
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Ambiente virtual ativo")
        print(f"  📁 Localização: {sys.prefix}")
    else:
        print("⚠️  Ambiente virtual não detectado")
        print("💡 Execute: .venv\\Scripts\\activate")
    
    # Verificar Django
    try:
        import django
        print(f"✅ Django instalado: versão {django.get_version()}")
    except ImportError:
        print("❌ Django não encontrado")
        print("💡 Execute: pip install django")
    
    # Verificar arquivos principais
    arquivos_principais = [
        'manage.py',
        'db.sqlite3',
        'requirements.txt',
        'fibermeyer_project/settings.py',
        'main/models.py'
    ]
    
    print("📋 Arquivos principais:")
    for arquivo in arquivos_principais:
        if os.path.exists(arquivo):
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo} (não encontrado)")

def mostrar_status():
    """Mostra status atual do projeto"""
    print("\n📊 STATUS DO PROJETO:")
    print("=" * 50)
    
    # Verificar se há processos rodando
    processos_ativos = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(palavra in cmdline.lower() for palavra in ['runserver', 'django', 'fibermeyer']):
                    processos_ativos.append(f"PID {proc.info['pid']}: {cmdline[:60]}...")
        except:
            pass
    
    if processos_ativos:
        print("🔴 PROCESSOS AINDA ATIVOS:")
        for proc in processos_ativos:
            print(f"  - {proc}")
    else:
        print("✅ NENHUM PROCESSO DO PROJETO ATIVO")
    
    # Verificar portas
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        
        if result == 0:
            print("🔴 PORTA 8000 AINDA OCUPADA")
        else:
            print("✅ PORTA 8000 LIVRE")
    except:
        print("⚠️  Não foi possível verificar porta 8000")

def mostrar_proximos_passos():
    """Mostra os próximos passos para reiniciar"""
    print("\n🚀 PRÓXIMOS PASSOS PARA REINICIAR:")
    print("=" * 50)
    print("1. Ativar ambiente virtual:")
    print("   .venv\\Scripts\\activate")
    print()
    print("2. Verificar instalações:")
    print("   pip list")
    print()
    print("3. Verificar banco de dados:")
    print("   python manage.py check")
    print()
    print("4. Executar migrações (se necessário):")
    print("   python manage.py migrate")
    print()
    print("5. Iniciar servidor:")
    print("   python manage.py runserver")
    print()
    print("6. Acessar aplicação:")
    print("   http://127.0.0.1:8000/")
    print()
    print("💡 DICAS:")
    print("- Use Ctrl+C para parar o servidor")
    print("- Use Ctrl+Break no Windows")
    print("- Verifique se a porta 8000 está livre")

def main():
    print("🔄 REINICIALIZAÇÃO DO PROJETO FIBERMEYER")
    print("=" * 60)
    
    # Mudar para diretório do projeto
    if not os.path.exists('manage.py'):
        print("❌ Arquivo manage.py não encontrado!")
        print("💡 Execute este script no diretório raiz do projeto")
        return
    
    print("✅ Diretório do projeto detectado")
    
    # Parar processos
    parar_processos_python()
    
    # Limpar cache
    limpar_cache()
    
    # Verificar ambiente
    verificar_ambiente()
    
    # Mostrar status
    mostrar_status()
    
    # Mostrar próximos passos
    mostrar_proximos_passos()
    
    print("\n" + "=" * 60)
    print("✅ REINICIALIZAÇÃO PREPARADA!")
    print("🎯 Projeto pronto para um novo start limpo!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Reinicialização interrompida pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro durante reinicialização: {e}")
    
    input("\n⏸️  Pressione Enter para fechar...")
