#!/usr/bin/env python3
"""
🔄 SCRIPT DE REINICIALIZAÇÃO SIMPLES DO PROJETO FIBERMEYER
"""

import os
import sys
import shutil

def parar_servidor():
    """Para o servidor Django usando comando do sistema"""
    print("🛑 PARANDO SERVIDOR DJANGO...")
    
    try:
        # No Windows, parar processos Python
        os.system('taskkill /F /IM python.exe 2>nul')
        print("✅ Processos Python finalizados")
    except:
        print("ℹ️  Comando executado (pode não ter processos ativos)")

def limpar_cache():
    """Remove arquivos de cache Python"""
    print("\n🧹 LIMPANDO CACHE...")
    
    cache_removido = 0
    
    # Buscar e remover __pycache__
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"  🗑️  Removido: {cache_dir}")
                cache_removido += 1
            except Exception as e:
                print(f"  ❌ Erro: {e}")
        
        # Remover arquivos .pyc
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    cache_removido += 1
                except:
                    pass
    
    print(f"✅ {cache_removido} arquivo(s) de cache removidos")

def verificar_projeto():
    """Verifica componentes do projeto"""
    print("\n🔍 VERIFICANDO PROJETO...")
    
    arquivos = {
        'manage.py': 'Script principal Django',
        'db.sqlite3': 'Banco de dados',
        'requirements.txt': 'Dependências',
        'fibermeyer_project/settings.py': 'Configurações',
        'main/models.py': 'Modelos de dados',
        '.venv/Scripts/activate.bat': 'Ambiente virtual'
    }
    
    for arquivo, descricao in arquivos.items():
        status = "✅" if os.path.exists(arquivo) else "❌"
        print(f"  {status} {descricao}: {arquivo}")

def main():
    print("🔄 REINICIALIZAÇÃO RÁPIDA - FIBERMEYER")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('manage.py'):
        print("❌ Arquivo manage.py não encontrado!")
        print("📁 Navegue para o diretório correto:")
        print("   cd \"c:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER\"")
        return
    
    # Executar limpeza
    parar_servidor()
    limpar_cache()
    verificar_projeto()
    
    print("\n🚀 COMANDOS PARA REINICIAR:")
    print("=" * 50)
    print("1️⃣  Ativar ambiente virtual:")
    print('    .venv\\Scripts\\activate')
    print()
    print("2️⃣  Iniciar servidor:")
    print('    python manage.py runserver')
    print()
    print("3️⃣  Acessar aplicação:")
    print('    http://127.0.0.1:8000/')
    
    print("\n✅ PROJETO LIMPO E PRONTO!")
    print("💡 Execute os comandos acima para reiniciar")

if __name__ == "__main__":
    main()
