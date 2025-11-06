import os
import django
import json
from decouple import config

# Configurar para usar PostgreSQL
os.environ['DATABASE_URL'] = config('DATABASE_URL')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import *
from django.db import transaction

print("📥 Importando dados para PostgreSQL...")
print("=" * 60)

# Carregar dados do JSON
with open('backup_dados_completo.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Agrupar por modelo
dados_por_modelo = {}
for item in dados:
    modelo = item['model']
    if modelo not in dados_por_modelo:
        dados_por_modelo[modelo] = []
    dados_por_modelo[modelo].append(item)

print(f"\n📊 Encontrados {len(dados)} registros em {len(dados_por_modelo)} modelos")

# Ordem de importação (respeitando dependências)
ordem_importacao = [
    'main.imposto',
    'main.maoobra',
    'main.mp_produtos',
    'main.produtocomponente',
    'main.produtotemplate',
    'main.parametroformula',
    'main.produtoparametrizado',
    'main.orcamento',
    'main.orcamentoitem',
    'main.orcamentoparametro',
    'main.orcamentohistorico',
]

from django.core import serializers

total_importados = 0

for modelo_nome in ordem_importacao:
    if modelo_nome not in dados_por_modelo:
        continue
    
    registros = dados_por_modelo[modelo_nome]
    print(f"\n🔄 Importando {modelo_nome}: {len(registros)} registros...")
    
    try:
        # Importar em lotes de 50
        tamanho_lote = 50
        for i in range(0, len(registros), tamanho_lote):
            lote = registros[i:i+tamanho_lote]
            
            with transaction.atomic():
                for obj_data in serializers.deserialize('json', json.dumps(lote)):
                    obj_data.save()
            
            importados = min(i + tamanho_lote, len(registros))
            print(f"   ✓ {importados}/{len(registros)} registros", end='\r')
        
        print(f"   ✓ {len(registros)}/{len(registros)} registros importados!")
        total_importados += len(registros)
        
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        # Continuar com próximo modelo

print("\n" + "=" * 60)
print(f"✅ Importação concluída! Total: {total_importados} registros")
print("=" * 60)

# Verificar dados
print("\n📊 Verificando dados importados:")
print(f"   - Produtos: {MP_Produtos.objects.count()}")
print(f"   - Orçamentos: {Orcamento.objects.count()}")
print(f"   - Impostos: {Imposto.objects.count()}")
print(f"   - Mão de Obra: {MaoObra.objects.count()}")
print(f"   - Componentes: {ProdutoComponente.objects.count()}")
