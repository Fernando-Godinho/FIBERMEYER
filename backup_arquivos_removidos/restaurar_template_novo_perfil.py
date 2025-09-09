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
    print("=== RECUPERANDO COMPONENTES DO TEMPLATE 'NOVO PERFIL' ===")
    
    # Buscar o produto e template do Novo Perfil
    novo_perfil = MP_Produtos.objects.filter(descricao="Novo Perfil").first()
    
    if not novo_perfil:
        print("❌ Produto 'Novo Perfil' não encontrado!")
        return
    
    print(f"✅ Produto 'Novo Perfil' encontrado (ID: {novo_perfil.id})")
    
    # Lista dos produtos que devem fazer parte do template baseado na análise anterior
    produtos_template = [
        # Estruturas
        {"nome": "ROVING 4400", "quantidade": 0.1},
        {"nome": "MANTA 300", "quantidade": 0.05}, 
        {"nome": "VÉU", "quantidade": 0.02},
        
        # Resinas  
        {"nome": "POLIÉSTER", "quantidade": 0.15},
        {"nome": "ISOFTÁLICA", "quantidade": 0.1},
        {"nome": "ÉSTER VINÍLICA", "quantidade": 0.08},
        
        # Aditivos químicos
        {"nome": "ANTI UV", "quantidade": 0.001},
        {"nome": "BPO", "quantidade": 0.002},
        {"nome": "COBALTO", "quantidade": 0.001},
        {"nome": "DMA", "quantidade": 0.001},
        {"nome": "ESTEARATO DE ZINCO", "quantidade": 0.001},
        {"nome": "INIBIDOR", "quantidade": 0.001},
        {"nome": "PERÓXIDO", "quantidade": 0.002},
        {"nome": "PROMOTOR", "quantidade": 0.001},
        {"nome": "SÍLICA", "quantidade": 0.05},
        
        # Mão de obra
        {"nome": "Mão de Obra - Pultrusão", "quantidade": 0.1}
    ]
    
    print(f"📋 Tentando adicionar {len(produtos_template)} componentes...")
    print()
    
    componentes_adicionados = 0
    componentes_faltando = []
    
    for item in produtos_template:
        # Buscar produto por nome (case insensitive e partial match)
        produto = MP_Produtos.objects.filter(descricao__icontains=item["nome"]).first()
        
        if produto:
            # Verificar se componente já existe
            componente_existente = ProdutoComponente.objects.filter(
                produto_principal=novo_perfil,
                produto_componente=produto
            ).first()
            
            if not componente_existente:
                # Criar componente
                ProdutoComponente.objects.create(
                    produto_principal=novo_perfil,
                    produto_componente=produto,
                    quantidade=item["quantidade"],
                    observacao=f"Componente do template {novo_perfil.descricao}"
                )
                print(f"✅ Adicionado: {produto.descricao} (Qtd: {item['quantidade']})")
                componentes_adicionados += 1
            else:
                print(f"⚠️  Já existe: {produto.descricao}")
        else:
            print(f"❌ Produto não encontrado: {item['nome']}")
            componentes_faltando.append(item["nome"])
    
    print()
    print("📊 RESUMO:")
    print(f"✅ Componentes adicionados: {componentes_adicionados}")
    print(f"❌ Produtos não encontrados: {len(componentes_faltando)}")
    
    if componentes_faltando:
        print("\n🔍 PRODUTOS NÃO ENCONTRADOS:")
        for nome in componentes_faltando:
            print(f"  - {nome}")
            
            # Tentar busca mais ampla
            produtos_similares = MP_Produtos.objects.filter(descricao__icontains=nome.split()[0])[:3]
            if produtos_similares:
                print(f"    💡 Produtos similares encontrados:")
                for p in produtos_similares:
                    print(f"       - {p.descricao} (ID: {p.id})")
    
    # Verificar componentes finais
    componentes_finais = ProdutoComponente.objects.filter(produto_principal=novo_perfil)
    print(f"\n📋 COMPONENTES FINAIS DO TEMPLATE ({componentes_finais.count()}):")
    
    total_custo = 0
    for comp in componentes_finais:
        custo_unit = comp.produto_componente.custo_centavos / 100
        custo_total = custo_unit * float(comp.quantidade)
        total_custo += custo_total
        
        print(f"  - {comp.produto_componente.descricao}")
        print(f"    Qtd: {comp.quantidade}, Custo unit: R$ {custo_unit:.2f}, Total: R$ {custo_total:.2f}")
    
    print(f"\n💰 CUSTO TOTAL ESTIMADO: R$ {total_custo:.2f}")
    
    # Atualizar custo do produto principal se necessário
    if novo_perfil.custo_centavos != int(total_custo * 100):
        print(f"\n🔄 Atualizando custo do produto de R$ {novo_perfil.custo_centavos/100:.2f} para R$ {total_custo:.2f}")
        novo_perfil.custo_centavos = int(total_custo * 100)
        novo_perfil.save()
        print("✅ Custo atualizado!")
    
    print(f"\n🎯 TEMPLATE 'NOVO PERFIL' RESTAURADO!")
    print(f"   📦 Produto: {novo_perfil.descricao} (ID: {novo_perfil.id})")
    print(f"   📋 Template: ID {novo_perfil.template.id}")
    print(f"   🧩 Componentes: {componentes_finais.count()}")
    print(f"   💰 Custo: R$ {novo_perfil.custo_centavos/100:.2f}")

if __name__ == "__main__":
    main()
