"""
Script para resetar sequências do PostgreSQL após migração do SQLite
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.db import connection

def resetar_sequencias():
    """Reseta as sequências de auto-incremento do PostgreSQL"""
    
    tabelas_com_sequencia = [
        ('main_mp_produtos', 'id'),
        ('main_produtocomponente', 'id'),
        ('main_orcamento', 'id'),
        ('main_itemorcamento', 'id'),
        ('main_maoobra', 'id'),
        ('main_produtotemplate', 'id'),
        ('main_componentetemplate', 'id'),
        ('main_tiporesina', 'id'),
    ]
    
    with connection.cursor() as cursor:
        print("=== RESETANDO SEQUÊNCIAS DO POSTGRESQL ===\n")
        
        for tabela, coluna in tabelas_com_sequencia:
            try:
                # Obter o valor máximo atual da tabela
                cursor.execute(f"SELECT MAX({coluna}) FROM {tabela}")
                max_id = cursor.fetchone()[0]
                
                if max_id is None:
                    max_id = 0
                
                # Nome da sequência no PostgreSQL
                sequencia = f"{tabela}_{coluna}_seq"
                
                # Resetar a sequência para max_id + 1
                novo_valor = max_id + 1
                cursor.execute(f"SELECT setval('{sequencia}', {novo_valor}, false)")
                
                print(f"✅ {tabela}")
                print(f"   Máximo ID atual: {max_id}")
                print(f"   Próximo ID será: {novo_valor}\n")
                
            except Exception as e:
                print(f"⚠️  Erro ao resetar {tabela}: {e}\n")
        
        print("=== SEQUÊNCIAS RESETADAS COM SUCESSO ===")

if __name__ == '__main__':
    resetar_sequencias()
