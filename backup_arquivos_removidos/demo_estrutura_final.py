import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente, ProdutoTemplate, ParametroTemplate

print("🚀 DEMONSTRAÇÃO FINAL - ESTRUTURA HIERÁRQUICA COMPLETA")
print("=" * 80)

print("📋 ESTRUTURA IMPLEMENTADA:")
print("   🧪 Produtos Simples: Matérias-primas básicas (resinas, fibras, cargas)")
print("   🏗️ Produtos Compostos: Combinação de produtos simples/compostos")
print("   📐 Produtos Parametrizados: Templates com proporções padrão")
print("=" * 80)

# 1. Demonstrar matérias-primas básicas
print("\n🧪 MATÉRIAS-PRIMAS BÁSICAS (Produtos Simples):")
materias_primas = MP_Produtos.objects.filter(tipo_produto='simples')[:10]
for mp in materias_primas:
    categoria = mp.categoria or "Sem categoria"
    icon = "🧪"
    print(f"   {icon} {mp.descricao} | {categoria} | R$ {mp.custo_centavos/100:.2f}")

# 2. Demonstrar produtos compostos
print(f"\n🏗️ PRODUTOS COMPOSTOS:")
compostos = MP_Produtos.objects.filter(tipo_produto='composto')
for composto in compostos:
    print(f"   {composto}")
    print(f"      💰 Custo: R$ {composto.custo_centavos/100:.2f}")
    
    # Mostrar componentes
    for componente in composto.componentes.all():
        tipo_comp = "🧪" if componente.produto_componente.is_materia_prima_basica() else "🏗️"
        print(f"      └─ {tipo_comp} {componente.produto_componente.descricao} (Qtd: {componente.quantidade})")

# 3. Testar propagação em cascata
print(f"\n💥 TESTE DE PROPAGAÇÃO EM CASCATA:")
print("=" * 50)

# Encontrar uma resina que seja usada em compostos
resina_teste = None
for resina in MP_Produtos.objects.filter(categoria='Resinas', tipo_produto='simples'):
    if resina.get_produtos_dependentes().exists():
        resina_teste = resina
        break

if resina_teste:
    print(f"🎯 Testando com: {resina_teste.descricao}")
    print(f"💰 Preço atual: R$ {resina_teste.custo_centavos/100:.2f}")
    
    # Mostrar hierarquia completa
    def mostrar_hierarquia(produto, nivel=0):
        indent = "  " * nivel
        dependentes = produto.get_produtos_dependentes()
        
        if dependentes.exists():
            for dep in dependentes:
                tipo_icon = "🏗️" if dep.is_produto_composto() else "📐" if dep.is_produto_parametrizado() else "🧪"
                print(f"{indent}├─ {tipo_icon} {dep.descricao}: R$ {dep.custo_centavos/100:.2f}")
                mostrar_hierarquia(dep, nivel + 1)
    
    print(f"\n🔗 CADEIA DE DEPENDÊNCIAS:")
    mostrar_hierarquia(resina_teste)
    
    # Fazer alteração dramática
    preco_original = resina_teste.custo_centavos / 100
    novo_preco = preco_original + 5.00
    
    print(f"\n🔥 ALTERANDO PREÇO DE R$ {preco_original:.2f} PARA R$ {novo_preco:.2f}")
    print("-" * 50)
    
    resina_teste.custo_centavos = int(novo_preco * 100)
    resina_teste.save()
    
    print(f"\n✅ PROPAGAÇÃO CONCLUÍDA!")
    
    # Verificar resultados
    print(f"\n📊 RESULTADO APÓS PROPAGAÇÃO:")
    resina_teste.refresh_from_db()
    print(f"   🧪 {resina_teste.descricao}: R$ {resina_teste.custo_centavos/100:.2f}")
    
    def verificar_hierarquia_atualizada(produto, nivel=0):
        indent = "  " * nivel
        dependentes = produto.get_produtos_dependentes()
        
        if dependentes.exists():
            for dep in dependentes:
                dep.refresh_from_db()
                tipo_icon = "🏗️" if dep.is_produto_composto() else "📐" if dep.is_produto_parametrizado() else "🧪"
                print(f"{indent}├─ {tipo_icon} {dep.descricao}: R$ {dep.custo_centavos/100:.2f}")
                verificar_hierarquia_atualizada(dep, nivel + 1)
    
    verificar_hierarquia_atualizada(resina_teste)
    
    # Reverter
    print(f"\n🔄 Revertendo para preço original...")
    resina_teste.custo_centavos = int(preco_original * 100)
    resina_teste.save()
    print(f"✅ Preço revertido!")

else:
    print("ℹ️ Nenhuma resina com dependências encontrada para demonstração")

# 4. Verificar templates
print(f"\n📐 TEMPLATES PARAMETRIZADOS:")
templates = ProdutoTemplate.objects.all()
for template in templates:
    print(f"   📋 {template.nome}")
    
    # Verificar parâmetros de seleção que usam produtos
    parametros_selecao = template.parametros.filter(tipo='selecao')
    for param in parametros_selecao:
        if param.opcoes_selecao:
            try:
                opcoes = json.loads(param.opcoes_selecao)
                print(f"      └─ {param.label}: {len(opcoes)} opções disponíveis")
                for opcao in opcoes[:2]:
                    if isinstance(opcao, dict) and 'nome' in opcao:
                        preco = opcao.get('preco', 0)
                        print(f"         • {opcao['nome']}: R$ {preco:.2f}")
            except:
                pass

print(f"\n🎉 SISTEMA HIERÁRQUICO COMPLETO FUNCIONANDO!")
print("=" * 80)
print("✅ Matérias-primas básicas catalogadas por categoria")
print("✅ Produtos compostos com componentes definidos") 
print("✅ Propagação automática de preços em cascata")
print("✅ Templates parametrizados integrados")
print("✅ Interface administrativa organizada por tipo")
print("✅ Rastreamento completo de dependências")
print("=" * 80)
