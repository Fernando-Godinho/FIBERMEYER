import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

# Criar os tipos de resina especificados
resinas_data = [
    {'descricao': 'Resina Isoftálica', 'custo': 18.34},
    {'descricao': 'Resina Poliéster', 'custo': 12.96},
    {'descricao': 'Resina Éster Vinílica', 'custo': 35.98}
]

print("=== CRIANDO TIPOS DE RESINA ===\n")

for resina_info in resinas_data:
    # Verificar se já existe
    exists = MP_Produtos.objects.filter(descricao=resina_info['descricao']).first()
    
    if exists:
        print(f"Atualizando: {resina_info['descricao']}")
        exists.custo_centavos = int(resina_info['custo'] * 100)
        exists.save()
        print(f"  Custo atualizado para R$ {resina_info['custo']:.2f}")
    else:
        print(f"Criando: {resina_info['descricao']}")
        produto = MP_Produtos.objects.create(
            descricao=resina_info['descricao'],
            custo_centavos=int(resina_info['custo'] * 100),
            peso_und=1.000,  # 1 kg por unidade
            unidade='KG',
            data_revisao='2025-08-31'
        )
        print(f"  ID: {produto.id}, Custo: R$ {resina_info['custo']:.2f}")

print("\n=== VERIFICAÇÃO FINAL ===")
for resina_info in resinas_data:
    produto = MP_Produtos.objects.filter(descricao=resina_info['descricao']).first()
    if produto:
        print(f"✓ {produto.descricao}: ID {produto.id}, R$ {produto.custo_centavos/100:.2f}")
    else:
        print(f"✗ {resina_info['descricao']}: Não encontrado!")

print("\nProdutos de resina criados com sucesso!")
