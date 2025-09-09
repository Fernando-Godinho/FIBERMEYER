import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoTemplate, ParametroTemplate, ProdutoComponente

print("🧪 TESTE DE CRIAÇÃO DE PRODUTOS PARAMETRIZADOS")
print("=" * 60)

# 1. Verificar templates disponíveis
templates = ProdutoTemplate.objects.all()
print(f"📋 Templates disponíveis: {templates.count()}")
for template in templates:
    print(f"   • {template.nome}")

# 2. Pegar template para teste
template_teste = templates.first()
if not template_teste:
    print("❌ Nenhum template encontrado")
    exit()

print(f"\n🎯 Testando com template: {template_teste.nome}")

# 3. Simular criação de produto parametrizado via interface
print(f"\n🔨 Criando produto parametrizado...")

# Dados simulados (como viria do frontend)
produto_data = {
    'descricao': 'Teste Produto Parametrizado',
    'custo_centavos': 15000,  # R$ 150.00
    'peso_und': 2.5,
    'unidade': 'M²',
    'referencia': f'Template: {template_teste.nome}',
    'tipo_produto': 'parametrizado',
    'categoria': 'Produtos Customizados'
}

# Componentes simulados (como viria do cálculo)
componentes_calculados = [
    {
        'nome': 'Resina Principal',
        'produto': 'Resina Teste Automático',
        'formula': 'area * 0.5',
        'quantidade': 2.5,
        'custo_unitario': 25.00,
        'custo_total': 62.50
    },
    {
        'nome': 'Fibra',
        'produto': 'Fibra Teste Automático', 
        'formula': 'area * 0.3',
        'quantidade': 1.5,
        'custo_unitario': 15.00,
        'custo_total': 22.50
    }
]

# 4. Criar produto usando o serializer (simulando chamada da API)
from main.serializers import MP_ProdutosSerializer

# Adicionar dados específicos de parametrizado
produto_data['componentes_calculados'] = componentes_calculados
produto_data['template_id'] = template_teste.id
produto_data['parametros_utilizados'] = {'area': 5.0, 'largura': 2000, 'altura': 2500}

serializer = MP_ProdutosSerializer(data=produto_data)

if serializer.is_valid():
    produto_criado = serializer.save()
    print(f"✅ Produto criado: {produto_criado.descricao}")
    print(f"   💰 Custo: R$ {produto_criado.custo_centavos/100:.2f}")
    print(f"   🏷️ Tipo: {produto_criado.tipo_produto}")
    print(f"   📂 Categoria: {produto_criado.categoria}")
    
    # 5. Verificar componentes criados
    componentes = produto_criado.componentes.all()
    print(f"\n🔗 Componentes criados: {componentes.count()}")
    for comp in componentes:
        print(f"   • {comp.produto_componente.descricao} (Qtd: {comp.quantidade})")
        print(f"     └─ {comp.observacao}")
    
    # 6. Testar propagação de preços
    print(f"\n💥 TESTANDO PROPAGAÇÃO DE PREÇOS:")
    
    # Encontrar um componente para alterar
    if componentes.exists():
        componente_teste = componentes.first().produto_componente
        preco_original = componente_teste.custo_centavos / 100
        print(f"   🎯 Alterando preço de: {componente_teste.descricao}")
        print(f"   💰 Preço atual: R$ {preco_original:.2f}")
        
        # Alterar preço
        novo_preco = preco_original + 10.00
        print(f"   🔄 Novo preço: R$ {novo_preco:.2f}")
        
        componente_teste.custo_centavos = int(novo_preco * 100)
        componente_teste.save()
        
        # Verificar se produto parametrizado foi atualizado
        produto_criado.refresh_from_db()
        print(f"   📦 Produto atualizado: R$ {produto_criado.custo_centavos/100:.2f}")
        
        # Reverter
        componente_teste.custo_centavos = int(preco_original * 100)
        componente_teste.save()
        print(f"   ✅ Preço revertido")
    
    print(f"\n🎉 Teste concluído com sucesso!")
    
    # 7. Mostrar diferença entre tipos
    print(f"\n📊 COMPARAÇÃO DE TIPOS DE PRODUTO:")
    
    simples = MP_Produtos.objects.filter(tipo_produto='simples').count()
    compostos = MP_Produtos.objects.filter(tipo_produto='composto').count()
    parametrizados = MP_Produtos.objects.filter(tipo_produto='parametrizado').count()
    
    print(f"   🧪 Produtos Simples: {simples}")
    print(f"   🏗️ Produtos Compostos: {compostos}")
    print(f"   📐 Produtos Parametrizados: {parametrizados}")
    
else:
    print(f"❌ Erro na validação: {serializer.errors}")

print("=" * 60)
