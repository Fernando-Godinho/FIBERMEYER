import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoTemplate, ParametroTemplate

print("🧪 Testando atualização de templates após correção...")
print("=" * 60)

# 1. Encontrar produto de resina
resinas = MP_Produtos.objects.filter(descricao__icontains='poliéster').exclude(is_composto=True)
if not resinas.exists():
    print("❌ Nenhuma resina encontrada")
    exit()

resina = resinas.first()
print(f"📦 Resina selecionada: {resina.descricao}")
print(f"💰 Preço atual: R$ {resina.custo_centavos / 100:.2f}")

# 2. Encontrar template com parâmetro que usa esta resina
template_encontrado = None
parametro_encontrado = None

for template in ProdutoTemplate.objects.all():
    for parametro in template.parametros.filter(tipo='selecao'):
        if parametro.opcoes_selecao:
            try:
                opcoes = json.loads(parametro.opcoes_selecao)
                for opcao in opcoes:
                    if isinstance(opcao, dict) and opcao.get('id') == resina.id:
                        template_encontrado = template
                        parametro_encontrado = parametro
                        break
                if template_encontrado:
                    break
            except:
                continue
    if template_encontrado:
        break

if not template_encontrado:
    print("❌ Nenhum template encontrado usando esta resina")
    exit()

print(f"📋 Template encontrado: {template_encontrado.nome}")
print(f"🔧 Parâmetro: {parametro_encontrado.label}")

# 3. Verificar preço atual no template
opcoes = json.loads(parametro_encontrado.opcoes_selecao)
preco_template_antes = None
for opcao in opcoes:
    if isinstance(opcao, dict) and opcao.get('id') == resina.id:
        preco_template_antes = opcao.get('preco')
        break

print(f"💱 Preço no template ANTES: R$ {preco_template_antes:.2f}")

# 4. Alterar preço da resina
novo_preco = 15.50
print(f"\n🔄 Alterando preço para R$ {novo_preco:.2f}...")

resina.custo_centavos = int(novo_preco * 100)
resina.save()

print(f"✅ Produto salvo com novo preço: R$ {resina.custo_centavos / 100:.2f}")

# 5. Verificar se o template foi atualizado
parametro_encontrado.refresh_from_db()
opcoes_atualizadas = json.loads(parametro_encontrado.opcoes_selecao)
preco_template_depois = None
for opcao in opcoes_atualizadas:
    if isinstance(opcao, dict) and opcao.get('id') == resina.id:
        preco_template_depois = opcao.get('preco')
        break

print(f"💱 Preço no template DEPOIS: R$ {preco_template_depois:.2f}")

# 6. Verificar se funcionou
if preco_template_depois == novo_preco:
    print("\n🎉 SUCESSO! Template foi atualizado automaticamente!")
else:
    print(f"\n❌ FALHA! Template não foi atualizado. Esperado: R$ {novo_preco:.2f}, Encontrado: R$ {preco_template_depois:.2f}")

# 7. Reverter para preço original
print(f"\n🔄 Revertendo para preço original...")
resina.custo_centavos = int(12.96 * 100)
resina.save()
print(f"✅ Preço revertido para: R$ {resina.custo_centavos / 100:.2f}")
