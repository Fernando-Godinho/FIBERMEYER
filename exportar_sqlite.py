import os
import sys
import django
from io import StringIO

# Forçar SQLite temporariamente
os.environ['DATABASE_URL'] = ''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.core.management import call_command

print("📤 Exportando dados do SQLite...")

try:
    # Exportar para arquivo com encoding UTF-8
    with open('backup_dados_completo.json', 'w', encoding='utf-8') as f:
        call_command(
            'dumpdata',
            'main',
            indent=2,
            natural_foreign=True,
            natural_primary=True,
            stdout=f
        )
    
    print("✓ Dados exportados com sucesso para backup_dados_completo.json")
    
    # Verificar tamanho do arquivo
    import os
    size = os.path.getsize('backup_dados_completo.json')
    print(f"✓ Tamanho do arquivo: {size:,} bytes")
    
except Exception as e:
    print(f"✗ Erro ao exportar: {e}")
    sys.exit(1)
