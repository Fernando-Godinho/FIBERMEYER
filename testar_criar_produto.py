import os
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos
from django.db import connection
from datetime import datetime

# Verificar conexão
db_settings = connection.settings_dict
print(f"🔗 Conectado ao: {db_settings['HOST']}")
print("\n" + "=" * 60)

# Criar produto de teste
print("➕ Criando produto de teste...\n")

try:
    produto = MP_Produtos.objects.create(
        descricao='TESTE SINCRONIZAÇÃO DB ONLINE',
        referencia='TEST-SYNC-001',
        unidade='UN',
        custo_centavos=9999,  # R$ 99,99 em centavos
        tipo_produto='simples',
        categoria='TESTE'
    )
    
    print(f"✅ Produto criado com sucesso!")
    print(f"   ID: {produto.id}")
    print(f"   Descrição: {produto.descricao}")
    print(f"   Referência: {produto.referencia}")
    print(f"   Custo: R$ {produto.custo_centavos / 100:.2f}")
    print()
    
    # Verificar se foi salvo
    print("🔍 Verificando se foi salvo no banco...")
    verificacao = MP_Produtos.objects.filter(id=produto.id).first()
    
    if verificacao:
        print(f"✅ CONFIRMADO! Produto ID {produto.id} está no banco online!")
    else:
        print(f"❌ ERRO! Produto não encontrado após salvar!")
    
except Exception as e:
    print(f"❌ Erro ao criar produto: {e}")

print("\n" + "=" * 60)
print(f"📊 Total de produtos agora: {MP_Produtos.objects.count()}")
