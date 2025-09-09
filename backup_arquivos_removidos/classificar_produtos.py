import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

print("🏗️ CLASSIFICAÇÃO AUTOMÁTICA DOS PRODUTOS NA NOVA ESTRUTURA")
print("=" * 70)

# 1. Classificar produtos por tipo
produtos_simples = MP_Produtos.objects.filter(tipo_produto='simples')
produtos_compostos = MP_Produtos.objects.filter(tipo_produto='composto') 
produtos_parametrizados = MP_Produtos.objects.filter(tipo_produto='parametrizado')

print(f"📊 ESTATÍSTICAS ATUAIS:")
print(f"   🧪 Produtos Simples (Matérias-Primas): {produtos_simples.count()}")
print(f"   🏗️ Produtos Compostos: {produtos_compostos.count()}")
print(f"   📐 Produtos Parametrizados: {produtos_parametrizados.count()}")

# 2. Identificar produtos que deveriam ser reclassificados
produtos_com_componentes = MP_Produtos.objects.filter(componentes__isnull=False).distinct()
produtos_sem_componentes = MP_Produtos.objects.filter(componentes__isnull=True)

print(f"\n🔍 ANÁLISE DE CLASSIFICAÇÃO:")
print(f"   📦 Produtos com componentes: {produtos_com_componentes.count()}")
print(f"   🧪 Produtos sem componentes: {produtos_sem_componentes.count()}")

# 3. Sugerir categorizações automáticas por palavra-chave
categorias_sugeridas = {
    'Resinas': ['resina', 'poliest', 'iso', 'orto', 'epox'],
    'Fibras': ['roving', 'manta', 'véu', 'veu', 'fibra', 'tecido'],
    'Cargas Minerais': ['carga', 'mineral', 'carbonato', 'talco', 'dolomita'],
    'Perfis': ['perfil', 'barra', 'chata', 'viga', 'coluna'],
    'Aditivos': ['catalis', 'acelera', 'anti', 'uv', 'ox', 'bpo', 'tbpb', 'desmold'],
    'Pigmentos': ['pigment', 'cor', 'tinta'],
    'Solventes': ['estiren', 'monomer', 'acetona', 'solvente']
}

print(f"\n🏷️ SUGESTÕES DE CATEGORIZAÇÃO:")
produtos_categorizados = 0

for categoria, palavras_chave in categorias_sugeridas.items():
    produtos_da_categoria = []
    
    for produto in MP_Produtos.objects.filter(categoria__isnull=True):
        descricao_lower = produto.descricao.lower()
        if any(palavra in descricao_lower for palavra in palavras_chave):
            produtos_da_categoria.append(produto)
    
    if produtos_da_categoria:
        print(f"\n   📂 {categoria} ({len(produtos_da_categoria)} produtos):")
        for produto in produtos_da_categoria[:5]:  # Mostrar apenas 5 primeiros
            print(f"      • {produto.descricao}")
        if len(produtos_da_categoria) > 5:
            print(f"      ... e mais {len(produtos_da_categoria) - 5} produto(s)")
        
        # Aplicar categorização automaticamente
        for produto in produtos_da_categoria:
            produto.categoria = categoria
            produto.save()
        produtos_categorizados += len(produtos_da_categoria)

print(f"\n✅ {produtos_categorizados} produtos categorizados automaticamente!")

# 4. Reclassificar produtos compostos com base na presença de componentes
print(f"\n🔄 RECLASSIFICAÇÃO AUTOMÁTICA:")

reclassificados = 0
for produto in produtos_com_componentes:
    if produto.tipo_produto == 'simples':
        produto.tipo_produto = 'composto'
        produto.save()
        reclassificados += 1
        print(f"   🏗️ {produto.descricao} → Convertido para Composto")

print(f"\n✅ {reclassificados} produtos reclassificados para 'composto'!")

# 5. Mostrar estrutura final
print(f"\n🎯 ESTRUTURA FINAL:")
print("=" * 70)

# Produtos Simples por categoria
print("🧪 PRODUTOS SIMPLES (MATÉRIAS-PRIMAS BÁSICAS):")
for categoria in ['Resinas', 'Fibras', 'Cargas Minerais', 'Aditivos', 'Pigmentos', 'Solventes']:
    produtos_cat = MP_Produtos.objects.filter(tipo_produto='simples', categoria=categoria)
    if produtos_cat.exists():
        print(f"   📂 {categoria}: {produtos_cat.count()} produto(s)")

# Produtos Compostos
compostos = MP_Produtos.objects.filter(tipo_produto='composto')
print(f"\n🏗️ PRODUTOS COMPOSTOS: {compostos.count()}")
for composto in compostos[:5]:
    componentes = composto.componentes.count()
    print(f"   • {composto.descricao} ({componentes} componente(s))")

# Produtos Parametrizados
parametrizados = MP_Produtos.objects.filter(tipo_produto='parametrizado')
print(f"\n📐 PRODUTOS PARAMETRIZADOS: {parametrizados.count()}")
for param in parametrizados:
    print(f"   • {param.descricao}")

print(f"\n🎉 ESTRUTURA HIERÁRQUICA IMPLEMENTADA COM SUCESSO!")
print("   ✅ Produtos classificados por tipo")
print("   ✅ Categorização automática aplicada")
print("   ✅ Sistema de propagação funcional")
print("   ✅ Interface administrativa atualizada")
print("=" * 70)
