#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

print("=== PRODUTOS NECESSÁRIOS PARA NOVO PERFIL ===")
print()

# Lista dos IDs dos componentes conforme mapeamento no código
componentes_ids = {
    1237: 'Roving 4400',
    1238: 'Manta 300', 
    1239: 'Véu',
    1266: 'Monômero de estireno',
    1243: 'Anti UV',
    1244: 'Anti OX',
    1245: 'BPO',
    1246: 'TBPB',
    1247: 'Desmoldante',
    1248: 'Antichama',
    1249: 'Carga mineral',
    1250: 'Pigmento',
    1269: 'Resina Poliéster (padrão)',
    1268: 'Resina Isoftálica (opcional)',
    1270: 'Resina Éster Vinílica (opcional)'
}

print("📋 MATERIAIS BÁSICOS:")
print("=" * 70)

# Buscar cada produto na base
for mp_id, nome_esperado in componentes_ids.items():
    try:
        produto = MP_Produtos.objects.get(id=mp_id)
        categoria = "ESTRUTURA" if mp_id in [1237, 1238, 1239] else \
                   "RESINA" if "resina" in nome_esperado.lower() else \
                   "QUÍMICO"
        
        print(f"✅ {categoria:10} | ID: {mp_id:4} | {produto.descricao:35} | R$ {produto.custo_centavos/100:8.2f}")
        
    except MP_Produtos.DoesNotExist:
        print(f"❌ FALTANDO  | ID: {mp_id:4} | {nome_esperado:35} | PRODUTO NÃO ENCONTRADO")

print("\n🔧 MÃO DE OBRA:")
print("=" * 70)

try:
    from main.models import MaoObra
    mao_obra = MaoObra.objects.filter(nome__icontains='pultrusão').first()
    if mao_obra:
        print(f"✅ TRABALHO   | ID: {mao_obra.id:4} | {mao_obra.nome:35} | R$ {mao_obra.valor_centavos/100:8.2f}/mês")
    else:
        print("❌ MÃO DE OBRA PULTRUSÃO NÃO ENCONTRADA")
except:
    print("❌ ERRO AO BUSCAR MÃO DE OBRA")

print("\n" + "=" * 70)
print("📊 RESUMO POR CATEGORIA:")
print("=" * 70)

# Agrupar por categoria
categorias = {
    'ESTRUTURA': [1237, 1238, 1239],
    'RESINAS': [1269, 1268, 1270],
    'QUÍMICOS': [1266, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250]
}

for categoria, ids in categorias.items():
    print(f"\n🏷️  {categoria}:")
    custo_categoria = 0
    itens_encontrados = 0
    
    for mp_id in ids:
        try:
            produto = MP_Produtos.objects.get(id=mp_id)
            custo_categoria += produto.custo_centavos / 100
            itens_encontrados += 1
            print(f"   • {produto.descricao} (R$ {produto.custo_centavos/100:.2f})")
        except MP_Produtos.DoesNotExist:
            print(f"   ❌ ID {mp_id} - {componentes_ids.get(mp_id, 'Desconhecido')} (NÃO ENCONTRADO)")
    
    print(f"   📈 Custo médio categoria: R$ {custo_categoria/len(ids) if ids else 0:.2f}")
    print(f"   📊 Produtos encontrados: {itens_encontrados}/{len(ids)}")

print(f"\n" + "=" * 70)
print("🎯 CONCLUSÃO:")
print("   • Total de produtos necessários: 15 materiais + 1 mão de obra")
print("   • Estrutura: Roving, Manta, Véu (reforços)")
print("   • Resinas: 3 opções (Poliéster, Isoftálica, Éster Vinílica)")
print("   • Químicos: 9 aditivos (catalisadores, desmoldante, etc.)")
print("   • Mão de obra: Pultrusão (processo de fabricação)")
print("=" * 70)
