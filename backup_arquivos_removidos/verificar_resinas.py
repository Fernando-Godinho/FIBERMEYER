import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

# Verificar tipos de resina existentes
print("=== VERIFICANDO TIPOS DE RESINA ===\n")

# Buscar produtos que podem ser resinas
resinas = MP_Produtos.objects.filter(descricao__icontains='resina').values('id', 'descricao', 'custo_centavos')
print("PRODUTOS COM 'RESINA' NO NOME:")
for p in resinas:
    print(f"ID: {p['id']}, Desc: {p['descricao']}, Custo: R$ {p['custo_centavos']/100:.2f}")

print("\n" + "="*50)

# Buscar especificamente os tipos mencionados
tipos_buscar = ['isoftálica', 'poliéster', 'éster vinílica', 'vinilester']

for tipo in tipos_buscar:
    produtos = MP_Produtos.objects.filter(descricao__icontains=tipo).values('id', 'descricao', 'custo_centavos')
    print(f"\n{tipo.upper()}:")
    if produtos:
        for p in produtos:
            print(f"  ID: {p['id']}, Desc: {p['descricao']}, Custo: R$ {p['custo_centavos']/100:.2f}")
    else:
        print(f"  Nenhum produto encontrado com '{tipo}'")

print("\n" + "="*50)
print("TODOS OS PRODUTOS (primeiros 20):")
todos = MP_Produtos.objects.all().values('id', 'descricao', 'custo_centavos')[:20]
for p in todos:
    print(f"ID: {p['id']}, Desc: {p['descricao']}, Custo: R$ {p['custo_centavos']/100:.2f}")
