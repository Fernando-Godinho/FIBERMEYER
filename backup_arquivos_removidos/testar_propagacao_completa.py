import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente, ProdutoTemplate, ParametroTemplate

print("🧪 Testando Sistema Completo de Propagação de Preços")
print("=" * 60)

# 1. Verificar produtos básicos (matérias-primas)
print("📦 MATÉRIAS-PRIMAS BÁSICAS:")
resinas = MP_Produtos.objects.filter(descricao__icontains='resina').exclude(is_composto=True)
if resinas.exists():
    for resina in resinas[:3]:
        print(f"   🧪 {resina.descricao}: R$ {resina.custo_centavos / 100:.2f}")

rovings = MP_Produtos.objects.filter(descricao__icontains='roving').exclude(is_composto=True)
if rovings.exists():
    for roving in rovings[:3]:
        print(f"   🧶 {roving.descricao}: R$ {roving.custo_centavos / 100:.2f}")

# 2. Verificar produtos compostos
print("\n📦 PRODUTOS COMPOSTOS:")
compostos = MP_Produtos.objects.filter(is_composto=True)
if compostos.exists():
    for composto in compostos[:3]:
        print(f"   🏗️  {composto.descricao}: R$ {composto.custo_centavos / 100:.2f}")
        
        # Mostrar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=composto)
        for comp in componentes:
            print(f"      └─ {comp.produto_componente.descricao} (Qtd: {comp.quantidade})")

# 3. Verificar templates
print("\n📋 TEMPLATES COM SELEÇÕES:")
templates = ProdutoTemplate.objects.all()
for template in templates:
    parametros_selecao = template.parametros.filter(tipo='selecao')
    if parametros_selecao.exists():
        print(f"   📋 {template.nome}:")
        for param in parametros_selecao:
            if param.opcoes_selecao:
                try:
                    opcoes = json.loads(param.opcoes_selecao)
                    print(f"      └─ {param.label}: {len(opcoes)} opções")
                    for opcao in opcoes[:2]:  # Mostrar apenas 2 primeiras
                        if isinstance(opcao, dict) and 'nome' in opcao:
                            preco = opcao.get('preco', 0)
                            print(f"         • {opcao['nome']}: R$ {preco:.2f}")
                except:
                    pass

print("\n" + "=" * 60)
print("🔥 TESTE DE PROPAGAÇÃO EM CASCATA")
print("=" * 60)

# 4. Teste: Alterar preço de matéria-prima básica
if resinas.exists():
    resina_teste = resinas.first()
    preco_original = resina_teste.custo_centavos / 100
    
    print(f"\n🎯 Testando com: {resina_teste.descricao}")
    print(f"💰 Preço atual: R$ {preco_original:.2f}")
    
    # Verificar dependências diretas
    dependentes = resina_teste.get_produtos_dependentes()
    print(f"📊 Produtos que dependem diretamente: {dependentes.count()}")
    
    if dependentes.exists():
        print("🔗 DEPENDÊNCIAS DIRETAS:")
        for dep in dependentes:
            print(f"   📦 {dep.descricao}: R$ {dep.custo_centavos / 100:.2f}")
            
            # Verificar dependências de segundo nível
            dep_nivel2 = dep.get_produtos_dependentes()
            if dep_nivel2.exists():
                print(f"      └─ Depende de {dep_nivel2.count()} produto(s) adicional(is)")
    
    # Alterar preço
    novo_preco = preco_original + 2.00
    print(f"\n🔄 Alterando preço para R$ {novo_preco:.2f}...")
    
    resina_teste.custo_centavos = int(novo_preco * 100)
    resina_teste.save()
    
    print(f"✅ Alteração concluída!")
    
    print(f"\n🔄 Revertendo para preço original...")
    resina_teste.custo_centavos = int(preco_original * 100)
    resina_teste.save()
    
    print(f"✅ Preço revertido para R$ {resina_teste.custo_centavos / 100:.2f}")
    
else:
    print("❌ Nenhuma resina encontrada para teste")

print("\n🎉 Teste de propagação concluído!")
