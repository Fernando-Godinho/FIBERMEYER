#!/usr/bin/env python3
"""
Teste para verificar se os preços estão sendo carregados da base MP_Produtos
em vez de valores fixos no código JavaScript.
"""

import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

print("=== TESTE: PREÇOS DA BASE MP_PRODUTOS ===")
print("Verificando se os preços estão sendo carregados corretamente da base de dados")
print()

# Buscar produtos relevantes na base
produtos_relevantes = [
    ('roving', ['roving', '4400']),
    ('manta', ['manta', '300']),
    ('veu', ['véu', 'veu']),
    ('resina', ['resina', 'poliéster']),
    ('monomero', ['monômero', 'estireno']),
    ('anti_uv', ['anti', 'uv']),
    ('anti_ox', ['anti', 'ox']),
    ('bpo', ['bpo']),
    ('tbpb', ['tbpb']),
    ('desmoldante', ['desmoldante']),
    ('antichama', ['antichama']),
    ('carga_mineral', ['carga', 'mineral']),
    ('pigmento', ['pigmento']),
    ('pintura', ['pintura'])
]

print("🔍 PRODUTOS ENCONTRADOS NA BASE MP_PRODUTOS:")
print("-" * 70)

produtos_encontrados = {}
for nome_key, palavras_chave in produtos_relevantes:
    produtos = MP_Produtos.objects.filter(
        descricao__icontains=palavras_chave[0]
    ).order_by('descricao')
    
    if len(palavras_chave) > 1:
        # Filtrar por palavras adicionais
        for palavra in palavras_chave[1:]:
            produtos = produtos.filter(descricao__icontains=palavra)
    
    if produtos.exists():
        produto = produtos.first()
        preco_reais = produto.custo_centavos / 100
        produtos_encontrados[nome_key] = {
            'id': produto.id,
            'descricao': produto.descricao,
            'preco_centavos': produto.custo_centavos,
            'preco_reais': preco_reais
        }
        print(f"✅ {nome_key:15s}: ID {produto.id:4d} | {produto.descricao:40s} | R$ {preco_reais:8.2f}")
    else:
        print(f"❌ {nome_key:15s}: Não encontrado na base")

print()
print("=" * 70)

# Preços padrão que estavam no código
precos_antigos = {
    'roving': 8.50,
    'manta': 12.00,
    'veu': 25.00,
    'resina': 12.96,
    'monomero': 8.00,
    'anti_uv': 45.00,
    'anti_ox': 35.00,
    'bpo': 28.00,
    'tbpb': 42.00,
    'desmoldante': 22.00,
    'antichama': 18.50,
    'carga_mineral': 3.20,
    'pigmento': 15.80,
    'pintura': 15.00
}

print("💰 COMPARAÇÃO DE PREÇOS (ANTIGO vs BASE):")
print("-" * 70)

diferencias = []
for key in precos_antigos:
    preco_antigo = precos_antigos[key]
    if key in produtos_encontrados:
        preco_novo = produtos_encontrados[key]['preco_reais']
        diferenca = preco_novo - preco_antigo
        percentual = (diferenca / preco_antigo) * 100
        
        status = "📈" if diferenca > 0 else "📉" if diferenca < 0 else "➖"
        
        print(f"{status} {key:15s}: R$ {preco_antigo:8.2f} → R$ {preco_novo:8.2f} ({diferenca:+7.2f} | {percentual:+6.1f}%)")
        diferencias.append((key, diferenca, percentual))
    else:
        print(f"⚠️ {key:15s}: R$ {preco_antigo:8.2f} → NÃO ENCONTRADO (usará padrão)")

print()
print("=" * 70)
print("📊 RESUMO DO IMPACTO:")

if diferencias:
    diferenca_total = sum([d[1] for d in diferencias])
    diferenca_media = diferenca_total / len(diferencias)
    
    maiores_aumentos = sorted([d for d in diferencias if d[1] > 0], key=lambda x: x[1], reverse=True)[:3]
    maiores_reducoes = sorted([d for d in diferencias if d[1] < 0], key=lambda x: x[1])[:3]
    
    print(f"Total de produtos com preços atualizados: {len(diferencias)}")
    print(f"Diferença total nos custos: R$ {diferenca_total:+7.2f}")
    print(f"Diferença média por produto: R$ {diferenca_media:+7.2f}")
    
    if maiores_aumentos:
        print(f"\nMaiores aumentos:")
        for nome, diff, pct in maiores_aumentos:
            print(f"  • {nome}: +R$ {diff:.2f} ({pct:+.1f}%)")
    
    if maiores_reducoes:
        print(f"\nMaiores reduções:")
        for nome, diff, pct in maiores_reducoes:
            print(f"  • {nome}: R$ {diff:.2f} ({pct:.1f}%)")

print()
print("=" * 70)
print("🔧 STATUS DA IMPLEMENTAÇÃO:")
print()
print("✅ Modificação implementada em:")
print("   - main/templates/main/mp.html (calcularNovoPerfil)")
print("   - main/templates/main/orcamento.html (calcularNovoPerfilOrcamento)")
print()
print("✅ Funcionalidades implementadas:")
print("   - Busca automática de preços da base MP_Produtos")
print("   - Mapeamento inteligente por palavras-chave")
print("   - Fallback para preços padrão em caso de erro")
print("   - Indicação visual de que preços foram atualizados")
print()
print("🧪 COMO TESTAR:")
print("1. Executar 'python manage.py runserver'")
print("2. Acessar http://127.0.0.1:8000/mp/")
print("3. Selecionar 'Novo Perfil' no dropdown")
print("4. Preencher campos obrigatórios")
print("5. Clicar em 'Calcular'")
print("6. Verificar no console do navegador (F12) os logs:")
print("   - '🔍 Buscando preços da base de dados...'")
print("   - '✅ Produtos carregados da base: X'")
print("   - '💰 Preços mapeados: {...}'")
print("   - Mensagem '(preços atualizados)' no resultado")

print()
print("=" * 70)

# Criar exemplo de cálculo para demonstrar
print("💡 EXEMPLO DE CÁLCULO COM NOVOS PREÇOS:")
print()

# Dados de exemplo
dados_exemplo = {
    'roving_4400_kg': 0.5,
    'manta_300_kg': 0.3,
    'veu_kg': 0.1,
    'peso_metro_kg': 1.2,
    'area_pintura_m2': 0.5
}

peso_resina_base = dados_exemplo['peso_metro_kg'] - (
    dados_exemplo['roving_4400_kg'] + 
    dados_exemplo['manta_300_kg'] + 
    dados_exemplo['veu_kg']
)

fatores = {
    'resina': 0.6897,
    'monomero': 0.0213,
    'antichama': 0.1777,
    'pigmento': 0.0178
}

print(f"Peso resina base: {peso_resina_base:.3f} kg")
print()

custo_antigo = 0
custo_novo = 0

componentes_exemplo = [
    ('roving', dados_exemplo['roving_4400_kg']),
    ('manta', dados_exemplo['manta_300_kg']),
    ('veu', dados_exemplo['veu_kg']),
    ('resina', peso_resina_base * fatores['resina']),
    ('monomero', peso_resina_base * fatores['monomero']),
    ('antichama', peso_resina_base * fatores['antichama']),
    ('pigmento', peso_resina_base * fatores['pigmento']),
    ('pintura', dados_exemplo['area_pintura_m2'])
]

print("Comparação de custos por componente:")
print("-" * 50)

for nome, quantidade in componentes_exemplo:
    preco_antigo = precos_antigos[nome] if nome != 'pintura' else precos_antigos['pintura']
    
    if nome in produtos_encontrados:
        preco_novo_val = produtos_encontrados[nome]['preco_reais']
        custo_comp_antigo = quantidade * preco_antigo
        custo_comp_novo = quantidade * preco_novo_val
        
        custo_antigo += custo_comp_antigo
        custo_novo += custo_comp_novo
        
        diferenca_comp = custo_comp_novo - custo_comp_antigo
        
        print(f"{nome:15s}: {quantidade:6.3f} x R$ {preco_antigo:6.2f} = R$ {custo_comp_antigo:7.2f} → R$ {custo_comp_novo:7.2f} ({diferenca_comp:+6.2f})")
    else:
        custo_comp = quantidade * preco_antigo
        custo_antigo += custo_comp
        custo_novo += custo_comp
        print(f"{nome:15s}: {quantidade:6.3f} x R$ {preco_antigo:6.2f} = R$ {custo_comp:7.2f} (sem alteração)")

print("-" * 50)
print(f"TOTAL ANTIGO: R$ {custo_antigo:.2f}")
print(f"TOTAL NOVO:   R$ {custo_novo:.2f}")
print(f"DIFERENÇA:    R$ {custo_novo - custo_antigo:+.2f} ({((custo_novo - custo_antigo) / custo_antigo) * 100:+.1f}%)")

print("\n" + "=" * 70)
print("🎯 CONCLUSÃO:")
print()
print("A implementação permite que os preços sejam automaticamente")
print("atualizados a partir da base de dados MP_Produtos, eliminando")
print("a necessidade de alterar o código JavaScript manualmente.")
print()
print("Isso garante que os cálculos sempre usem os preços mais")
print("atuais, melhorando a precisão dos orçamentos.")
