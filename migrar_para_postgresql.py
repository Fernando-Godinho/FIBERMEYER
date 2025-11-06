"""
Script para migrar dados do SQLite para PostgreSQL

Este script exporta os dados do db.sqlite3 e os importa no PostgreSQL online.

Uso:
1. Configure a variável DATABASE_URL no arquivo .env
2. Execute: python migrar_para_postgresql.py
"""

import os
import sys
import django
from decouple import config

# Carregar variáveis de ambiente
os.environ['DATABASE_URL'] = config('DATABASE_URL', default='')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from django.apps import apps


def verificar_conexao_postgresql():
    """Verifica se consegue conectar ao PostgreSQL"""
    try:
        connection = connections['default']
        connection.ensure_connection()
        db_name = connection.settings_dict['NAME']
        print(f"✓ Conectado ao PostgreSQL: {db_name}")
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar ao PostgreSQL: {e}")
        return False


def exportar_dados_sqlite():
    """Exporta dados do SQLite em formato JSON"""
    print("\n1. Exportando dados do SQLite...")
    
    try:
        # Exportar todos os dados
        with open('backup_sqlite.json', 'w', encoding='utf-8') as f:
            call_command('dumpdata', 
                        '--natural-foreign', 
                        '--natural-primary',
                        '--exclude=contenttypes',
                        '--exclude=auth.permission',
                        '--indent=2',
                        stdout=f)
        
        print("✓ Dados exportados para backup_sqlite.json")
        return True
    except Exception as e:
        print(f"✗ Erro ao exportar dados: {e}")
        return False


def importar_dados_postgresql():
    """Importa dados para o PostgreSQL"""
    print("\n2. Importando dados para PostgreSQL...")
    
    try:
        # Limpar banco PostgreSQL (cuidado!)
        print("   - Limpando banco de dados...")
        call_command('flush', '--no-input')
        
        # Importar dados
        print("   - Importando dados...")
        call_command('loaddata', 'backup_sqlite.json')
        
        print("✓ Dados importados com sucesso!")
        return True
    except Exception as e:
        print(f"✗ Erro ao importar dados: {e}")
        return False


def executar_migracoes():
    """Executa as migrações no PostgreSQL"""
    print("\n3. Executando migrações no PostgreSQL...")
    
    try:
        call_command('migrate', '--no-input')
        print("✓ Migrações executadas com sucesso!")
        return True
    except Exception as e:
        print(f"✗ Erro ao executar migrações: {e}")
        return False


def verificar_dados():
    """Verifica se os dados foram importados corretamente"""
    print("\n4. Verificando dados importados...")
    
    try:
        # Listar todos os modelos e contar registros
        for model in apps.get_models():
            if not model._meta.app_label.startswith('django.contrib'):
                count = model.objects.count()
                print(f"   - {model._meta.label}: {count} registros")
        
        print("✓ Verificação concluída!")
        return True
    except Exception as e:
        print(f"✗ Erro ao verificar dados: {e}")
        return False


def main():
    print("=" * 60)
    print("MIGRAÇÃO DE DADOS: SQLite → PostgreSQL")
    print("=" * 60)
    
    # Verificar se DATABASE_URL está configurado
    database_url = config('DATABASE_URL', default='')
    if not database_url:
        print("\n⚠ ERRO: DATABASE_URL não está configurado!")
        print("\nPor favor:")
        print("1. Crie um arquivo .env na raiz do projeto")
        print("2. Adicione: DATABASE_URL=postgresql://usuario:senha@host:5432/banco")
        print("\nExemplo Supabase:")
        print("DATABASE_URL=postgresql://postgres.xxxxx:[SENHA]@aws-0-us-east-1.pooler.supabase.com:6543/postgres")
        sys.exit(1)
    
    print(f"\n📊 Banco de dados atual: {connections['default'].settings_dict['ENGINE']}")
    
    # Verificar se está usando PostgreSQL
    if 'postgresql' not in connections['default'].settings_dict['ENGINE']:
        print("\n⚠ ERRO: Não está configurado para usar PostgreSQL!")
        print("\nConfigure DATABASE_URL no arquivo .env e tente novamente.")
        sys.exit(1)
    
    # Verificar conexão
    if not verificar_conexao_postgresql():
        sys.exit(1)
    
    # Confirmar migração
    print("\n⚠ ATENÇÃO: Este processo irá:")
    print("1. Exportar todos os dados do SQLite")
    print("2. APAGAR todos os dados do PostgreSQL")
    print("3. Importar os dados do SQLite para o PostgreSQL")
    
    resposta = input("\nDeseja continuar? (sim/não): ").strip().lower()
    if resposta not in ['sim', 's', 'yes', 'y']:
        print("\n❌ Migração cancelada.")
        sys.exit(0)
    
    # Executar migração
    sucesso = True
    
    # Passo 1: Executar migrações primeiro
    if sucesso:
        sucesso = executar_migracoes()
    
    # Passo 2: Exportar dados
    if sucesso:
        sucesso = exportar_dados_sqlite()
    
    # Passo 3: Importar dados
    if sucesso:
        sucesso = importar_dados_postgresql()
    
    # Passo 4: Verificar dados
    if sucesso:
        sucesso = verificar_dados()
    
    # Resultado final
    print("\n" + "=" * 60)
    if sucesso:
        print("✓ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\nPróximos passos:")
        print("1. Teste seu aplicativo com o PostgreSQL")
        print("2. Verifique se todos os dados estão corretos")
        print("3. Faça backup do arquivo backup_sqlite.json")
        print("4. Quando confirmar que está tudo OK, pode excluir db.sqlite3")
    else:
        print("✗ MIGRAÇÃO FALHOU!")
        print("\nSeus dados do SQLite estão seguros em db.sqlite3")
        print("Revise os erros acima e tente novamente.")
    print("=" * 60)


if __name__ == '__main__':
    main()
