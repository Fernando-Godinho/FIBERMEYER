#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos, ProdutoComponente

def main():
    print("=== RESTAURANDO TEMPLATE COMPLETO 'NOVO PERFIL' ===")
    
    # Buscar o produto Novo Perfil
    novo_perfil = MP_Produtos.objects.filter(descricao="Novo Perfil").first()
    
    if not novo_perfil:
        print("❌ Produto 'Novo Perfil' não encontrado!")
        return
    
    print(f"✅ Produto 'Novo Perfil' encontrado (ID: {novo_perfil.id})")
    
    # Lista completa baseada na saída do script anterior
    produtos_template = [
        # ESTRUTURA
        {"id": 1237, "nome": "Roving 4400", "quantidade": 0.1},
        {"id": 1238, "nome": "Manta 300", "quantidade": 0.05},
        {"id": 1239, "nome": "Véu", "quantidade": 0.02},
        
        # RESINAS
        {"id": 1269, "nome": "Resina Poliéster", "quantidade": 0.15},
        {"id": 1268, "nome": "Resina Isoftálica", "quantidade": 0.1},
        {"id": 1270, "nome": "Resina Éster Vinílica", "quantidade": 0.08},
        
        # QUÍMICOS
        {"id": 1266, "nome": "Monômero de estireno", "quantidade": 0.01},
        {"id": 1243, "nome": "Anti UV", "quantidade": 0.001},
        {"id": 1244, "nome": "Anti OX", "quantidade": 0.001},
        {"id": 1245, "nome": "BPO", "quantidade": 0.002},
        {"id": 1246, "nome": "TBPB", "quantidade": 0.002},
        {"id": 1247, "nome": "Desmoldante", "quantidade": 0.005},
        {"id": 1248, "nome": "Antichama", "quantidade": 0.01},
        {"id": 1249, "nome": "Carga mineral", "quantidade": 0.05},
        {"id": 1250, "nome": "Pigmento", "quantidade": 0.003}
    ]
    
    print(f"📋 Adicionando {len(produtos_template)} componentes materiais...")
    print()
    
    # Limpar componentes existentes primeiro (exceto mão de obra)
    componentes_existentes = ProdutoComponente.objects.filter(produto_principal=novo_perfil)
    if componentes_existentes.exists():
        print(f"🧹 Removendo {componentes_existentes.count()} componentes existentes...")
        componentes_existentes.delete()
    
    componentes_adicionados = 0
    componentes_erro = []
    
    for item in produtos_template:
        try:
            # Buscar produto por ID
            produto = MP_Produtos.objects.get(id=item["id"])
            
            # Criar componente
            ProdutoComponente.objects.create(
                produto_principal=novo_perfil,
                produto_componente=produto,
                quantidade=item["quantidade"],
                observacao=f"Template {novo_perfil.descricao}"
            )
            
            custo = produto.custo_centavos / 100
            custo_total = custo * item["quantidade"]
            print(f"✅ {produto.descricao} (Qtd: {item['quantidade']}, Custo: R$ {custo_total:.2f})")
            componentes_adicionados += 1
            
        except MP_Produtos.DoesNotExist:
            print(f"❌ Produto ID {item['id']} não encontrado: {item['nome']}")
            componentes_erro.append(item)
        except Exception as e:
            print(f"❌ Erro ao adicionar {item['nome']}: {str(e)}")
            componentes_erro.append(item)
    
    # Adicionar mão de obra se não existir
    print()
    print("🔧 Verificando mão de obra...")
    
    # Buscar produto de mão de obra existente ou criar
    mao_obra_produto = MP_Produtos.objects.filter(descricao__icontains="Mão de Obra").filter(descricao__icontains="Pultrusão").first()
    
    if not mao_obra_produto:
        print("📦 Criando produto 'Mão de Obra - Pultrusão'...")
        mao_obra_produto = MP_Produtos.objects.create(
            descricao="Mão de Obra - Pultrusão",
            tipo_produto="simples",
            custo_centavos=100,  # R$ 1.00 base
            categoria="MÃO_DE_OBRA",
            unidade="H"
        )
        print(f"✅ Produto mão de obra criado (ID: {mao_obra_produto.id})")
    
    # Adicionar componente mão de obra
    ProdutoComponente.objects.create(
        produto_principal=novo_perfil,
        produto_componente=mao_obra_produto,
        quantidade=0.1,  # 0.1 hora
        observacao=f"Mão de obra para {novo_perfil.descricao}"
    )
    print(f"✅ Mão de obra adicionada: {mao_obra_produto.descricao} (0.1H)")
    
    print()
    print("📊 RESUMO FINAL:")
    print(f"✅ Componentes materiais adicionados: {componentes_adicionados}")
    print(f"✅ Mão de obra adicionada: 1")
    print(f"❌ Componentes com erro: {len(componentes_erro)}")
    
    if componentes_erro:
        print("\n❌ COMPONENTES COM ERRO:")
        for item in componentes_erro:
            print(f"  - {item['nome']} (ID: {item['id']})")
    
    # Calcular custo total final
    componentes_finais = ProdutoComponente.objects.filter(produto_principal=novo_perfil)
    print(f"\n📋 COMPONENTES FINAIS DO TEMPLATE ({componentes_finais.count()}):")
    
    total_custo = 0
    for comp in componentes_finais:
        custo_unit = comp.produto_componente.custo_centavos / 100
        custo_total = custo_unit * float(comp.quantidade)
        total_custo += custo_total
        
        categoria = comp.produto_componente.categoria or "SEM CATEGORIA"
        print(f"  [{categoria:12}] {comp.produto_componente.descricao[:40]:40} | Qtd: {comp.quantidade:6} | R$ {custo_total:7.2f}")
    
    print(f"\n💰 CUSTO TOTAL FINAL: R$ {total_custo:.2f}")
    
    # Atualizar custo do produto
    novo_perfil.custo_centavos = int(total_custo * 100)
    novo_perfil.save()
    
    print(f"\n🎉 TEMPLATE 'NOVO PERFIL' COMPLETAMENTE RESTAURADO!")
    print(f"   📦 Produto: {novo_perfil.descricao} (ID: {novo_perfil.id})")
    print(f"   📋 Template: ID {novo_perfil.template.id}")
    print(f"   🧩 Componentes: {componentes_finais.count()}")
    print(f"   💰 Custo total: R$ {total_custo:.2f}")
    print(f"   ✅ Sistema pronto para parametrização!")

if __name__ == "__main__":
    main()
