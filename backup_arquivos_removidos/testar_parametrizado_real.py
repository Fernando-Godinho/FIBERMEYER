import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoTemplate, ParametroTemplate, ProdutoComponente

print("🧪 TESTE CORRETO DE PRODUTOS PARAMETRIZADOS")
print("=" * 60)

# 1. Encontrar produtos reais para usar como componentes
resinas = list(MP_Produtos.objects.filter(categoria='Resinas', tipo_produto='simples')[:3])
fibras = list(MP_Produtos.objects.filter(categoria='Fibras', tipo_produto='simples')[:3])

print(f"🧪 Resinas disponíveis: {len(resinas)}")
for resina in resinas:
    print(f"   • {resina.descricao}: R$ {resina.custo_centavos/100:.2f}")

print(f"\n🧶 Fibras disponíveis: {len(fibras)}")
for fibra in fibras:
    print(f"   • {fibra.descricao}: R$ {fibra.custo_centavos/100:.2f}")

if not resinas or not fibras:
    print("❌ Produtos necessários não encontrados")
    exit()

# 2. Criar produto parametrizado com componentes reais
print(f"\n🔨 Criando produto parametrizado com componentes reais...")

resina_principal = resinas[0]
fibra_principal = fibras[0]

# Dados do produto
produto_data = {
    'descricao': 'Grade Personalizada 2x2m',
    'custo_centavos': 0,  # Será calculado
    'peso_und': 5.0,
    'unidade': 'M²', 
    'referencia': 'GRADE-PARAM-001',
    'tipo_produto': 'parametrizado',
    'categoria': 'Produtos Customizados'
}

# Componentes com produtos reais
componentes_calculados = [
    {
        'nome': 'Resina Principal',
        'produto': resina_principal.descricao,
        'formula': 'area * 0.5',
        'quantidade': 2.0,  # 2m² * 0.5 = 1.0 kg
        'custo_unitario': resina_principal.custo_centavos / 100,
        'custo_total': (resina_principal.custo_centavos / 100) * 2.0
    },
    {
        'nome': 'Fibra de Reforço',
        'produto': fibra_principal.descricao,
        'formula': 'area * 0.3', 
        'quantidade': 1.2,  # 4m² * 0.3 = 1.2 kg
        'custo_unitario': fibra_principal.custo_centavos / 100,
        'custo_total': (fibra_principal.custo_centavos / 100) * 1.2
    }
]

# Calcular custo total
custo_total = sum(comp['custo_total'] for comp in componentes_calculados)
produto_data['custo_centavos'] = int(custo_total * 100)

print(f"   💰 Custo calculado: R$ {custo_total:.2f}")

# 3. Criar produto usando o serializer
from main.serializers import MP_ProdutosSerializer

produto_data['componentes_calculados'] = componentes_calculados
produto_data['parametros_utilizados'] = {'area': 4.0, 'largura': 2000, 'altura': 2000}

serializer = MP_ProdutosSerializer(data=produto_data)

if serializer.is_valid():
    produto_criado = serializer.save()
    print(f"✅ Produto criado: {produto_criado.descricao}")
    print(f"   💰 Custo: R$ {produto_criado.custo_centavos/100:.2f}")
    print(f"   🏷️ Tipo: {produto_criado.tipo_produto}")
    print(f"   📂 Categoria: {produto_criado.categoria}")
    
    # 4. Verificar componentes criados
    componentes = produto_criado.componentes.all()
    print(f"\n🔗 Componentes criados: {componentes.count()}")
    for comp in componentes:
        print(f"   • {comp.produto_componente.descricao}")
        print(f"     └─ Quantidade: {comp.quantidade}")
        print(f"     └─ Custo unitário: R$ {comp.produto_componente.custo_centavos/100:.2f}")
        print(f"     └─ Custo total: R$ {(comp.produto_componente.custo_centavos/100) * float(comp.quantidade):.2f}")
        print(f"     └─ Observação: {comp.observacao}")
    
    # 5. Testar propagação de preços
    print(f"\n💥 TESTANDO PROPAGAÇÃO DE PREÇOS:")
    
    if componentes.exists():
        componente_teste = componentes.first().produto_componente
        preco_original = componente_teste.custo_centavos / 100
        custo_produto_original = produto_criado.custo_centavos / 100
        
        print(f"   🎯 Testando com: {componente_teste.descricao}")
        print(f"   💰 Preço original do componente: R$ {preco_original:.2f}")
        print(f"   💰 Custo original do produto: R$ {custo_produto_original:.2f}")
        
        # Alterar preço do componente
        novo_preco = preco_original + 5.00
        print(f"\n   🔄 Alterando preço do componente para: R$ {novo_preco:.2f}")
        
        componente_teste.custo_centavos = int(novo_preco * 100)
        componente_teste.save()
        
        # Verificar se produto parametrizado foi atualizado
        produto_criado.refresh_from_db()
        custo_produto_novo = produto_criado.custo_centavos / 100
        
        print(f"   📦 Custo do produto após alteração: R$ {custo_produto_novo:.2f}")
        
        if custo_produto_novo != custo_produto_original:
            print(f"   ✅ SUCESSO! Propagação funcionou!")
            diferenca = custo_produto_novo - custo_produto_original
            print(f"   📈 Diferença: R$ {diferenca:.2f}")
        else:
            print(f"   ⚠️ Produto não foi atualizado automaticamente")
        
        # Reverter
        componente_teste.custo_centavos = int(preco_original * 100)
        componente_teste.save()
        print(f"   🔄 Preço revertido")
    
    # 6. Mostrar hierarquia
    print(f"\n🌳 HIERARQUIA DE DEPENDÊNCIAS:")
    print(f"   📐 {produto_criado.descricao} (Parametrizado)")
    for comp in componentes:
        tipo_icon = "🧪" if comp.produto_componente.is_materia_prima_basica() else "🏗️"
        print(f"      └─ {tipo_icon} {comp.produto_componente.descricao}")
    
else:
    print(f"❌ Erro na validação: {serializer.errors}")

print(f"\n🎉 Teste concluído!")
print("=" * 60)
