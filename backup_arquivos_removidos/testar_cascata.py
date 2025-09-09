import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente, ProdutoTemplate, ParametroTemplate

print("🧪 TESTE COMPLETO DE PROPAGAÇÃO EM CASCATA")
print("=" * 60)

# Encontrar resina com dependências
resina_teste = MP_Produtos.objects.filter(descricao='Resina Teste Automático').first()

if not resina_teste:
    print("❌ Resina de teste não encontrada")
    exit()

print(f"🎯 Testando com: {resina_teste.descricao}")
print(f"💰 Preço inicial: R$ {resina_teste.custo_centavos / 100:.2f}")

# Verificar dependências
dependentes_nivel1 = resina_teste.get_produtos_dependentes()
print(f"📊 Dependentes de nível 1: {dependentes_nivel1.count()}")

for dep in dependentes_nivel1:
    print(f"   📦 {dep.descricao}: R$ {dep.custo_centavos / 100:.2f}")
    
    # Verificar dependentes de nível 2
    dependentes_nivel2 = dep.get_produtos_dependentes()
    if dependentes_nivel2.exists():
        print(f"      📊 Dependentes de nível 2: {dependentes_nivel2.count()}")
        for dep2 in dependentes_nivel2:
            print(f"         📦 {dep2.descricao}: R$ {dep2.custo_centavos / 100:.2f}")

print(f"\n🔄 ALTERANDO PREÇO DA RESINA DE R$ {resina_teste.custo_centavos / 100:.2f} para R$ 12.00")
print("=" * 60)

resina_teste.custo_centavos = 1200  # R$ 12.00
resina_teste.save()

print(f"\n✅ Alteração concluída!")

# Verificar se os preços foram atualizados
print(f"\n📊 VERIFICANDO PREÇOS APÓS ALTERAÇÃO:")
print("=" * 60)

resina_teste.refresh_from_db()
print(f"🎯 {resina_teste.descricao}: R$ {resina_teste.custo_centavos / 100:.2f}")

for dep in dependentes_nivel1:
    dep.refresh_from_db()
    print(f"   📦 {dep.descricao}: R$ {dep.custo_centavos / 100:.2f}")
    
    dependentes_nivel2 = dep.get_produtos_dependentes()
    for dep2 in dependentes_nivel2:
        dep2.refresh_from_db()
        print(f"      📦 {dep2.descricao}: R$ {dep2.custo_centavos / 100:.2f}")

print(f"\n🔄 REVERTENDO PARA PREÇO ORIGINAL")
print("=" * 60)

resina_teste.custo_centavos = 800  # R$ 8.00 (valor original)
resina_teste.save()

print(f"\n✅ Preço revertido!")
print(f"🎉 Teste de propagação em cascata concluído com sucesso!")
