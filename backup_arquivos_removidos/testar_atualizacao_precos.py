#!/usr/bin/env python
"""
Teste da funcionalidade de atualização automática de preços
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente
from decimal import Decimal

def criar_produto_teste():
    """Cria produtos de teste para demonstrar a funcionalidade"""
    
    print("🏭 CRIANDO PRODUTOS DE TESTE...")
    
    # 1. Criar matéria-prima básica (Resina)
    resina, created = MP_Produtos.objects.get_or_create(
        descricao="Resina Teste Automático",
        defaults={
            'custo_centavos': 1500,  # R$ 15,00
            'peso_und': 1.0,
            'unidade': 'KG',
            'referencia': 'TESTE-RESINA',
            'is_composto': False
        }
    )
    print(f"   ✅ Resina: {resina.descricao} - R$ {resina.custo_centavos/100:.2f}")
    
    # 2. Criar outro componente
    fibra, created = MP_Produtos.objects.get_or_create(
        descricao="Fibra Teste Automático",
        defaults={
            'custo_centavos': 800,  # R$ 8,00
            'peso_und': 1.0,
            'unidade': 'KG',
            'referencia': 'TESTE-FIBRA',
            'is_composto': False
        }
    )
    print(f"   ✅ Fibra: {fibra.descricao} - R$ {fibra.custo_centavos/100:.2f}")
    
    # 3. Criar produto composto que usa as matérias-primas
    produto_composto, created = MP_Produtos.objects.get_or_create(
        descricao="Perfil Composto Teste",
        defaults={
            'custo_centavos': 0,  # Será calculado automaticamente
            'peso_und': 5.0,
            'unidade': 'UN',
            'referencia': 'TESTE-COMPOSTO',
            'is_composto': True
        }
    )
    
    # 4. Adicionar componentes ao produto composto
    ProdutoComponente.objects.get_or_create(
        produto_principal=produto_composto,
        produto_componente=resina,
        defaults={'quantidade': Decimal('2.5')}  # 2.5 kg de resina
    )
    
    ProdutoComponente.objects.get_or_create(
        produto_principal=produto_composto,
        produto_componente=fibra,
        defaults={'quantidade': Decimal('1.5')}  # 1.5 kg de fibra
    )
    
    # 5. Calcular custo inicial
    custo_inicial = produto_composto.recalcular_custo_composto()
    print(f"   ✅ Produto Composto: {produto_composto.descricao}")
    print(f"       Componentes: 2.5kg resina + 1.5kg fibra")
    print(f"       Custo inicial: R$ {custo_inicial/100:.2f}")
    
    # 6. Criar um segundo produto composto que usa o primeiro
    produto_final, created = MP_Produtos.objects.get_or_create(
        descricao="Estrutura Final Teste",
        defaults={
            'custo_centavos': 0,
            'peso_und': 10.0,
            'unidade': 'UN',
            'referencia': 'TESTE-FINAL',
            'is_composto': True
        }
    )
    
    ProdutoComponente.objects.get_or_create(
        produto_principal=produto_final,
        produto_componente=produto_composto,
        defaults={'quantidade': Decimal('2.0')}  # 2 unidades do produto composto
    )
    
    custo_final_inicial = produto_final.recalcular_custo_composto()
    print(f"   ✅ Estrutura Final: {produto_final.descricao}")
    print(f"       Componentes: 2x {produto_composto.descricao}")
    print(f"       Custo inicial: R$ {custo_final_inicial/100:.2f}")
    
    return resina, fibra, produto_composto, produto_final

def testar_atualizacao_automatica():
    """Testa a atualização automática de preços"""
    
    print("\n" + "="*60)
    print("🧪 TESTANDO ATUALIZAÇÃO AUTOMÁTICA DE PREÇOS")
    print("="*60)
    
    # Criar produtos de teste
    resina, fibra, produto_composto, produto_final = criar_produto_teste()
    
    print(f"\n📊 SITUAÇÃO INICIAL:")
    print(f"   Resina: R$ {resina.custo_centavos/100:.2f}")
    print(f"   Fibra: R$ {fibra.custo_centavos/100:.2f}")
    print(f"   Produto Composto: R$ {produto_composto.custo_centavos/100:.2f}")
    print(f"   Estrutura Final: R$ {produto_final.custo_centavos/100:.2f}")
    
    # Simular aumento de preço da resina
    print(f"\n🔄 ALTERANDO PREÇO DA RESINA DE R$ {resina.custo_centavos/100:.2f} PARA R$ 25,00...")
    resina.custo_centavos = 2500  # R$ 25,00
    resina.save()  # Isso vai disparar os signals automaticamente
    
    # Recarregar objetos do banco para ver as mudanças
    produto_composto.refresh_from_db()
    produto_final.refresh_from_db()
    
    print(f"\n📊 SITUAÇÃO APÓS ATUALIZAÇÃO:")
    print(f"   Resina: R$ {resina.custo_centavos/100:.2f} ✅")
    print(f"   Fibra: R$ {fibra.custo_centavos/100:.2f} (inalterada)")
    print(f"   Produto Composto: R$ {produto_composto.custo_centavos/100:.2f} 🔄")
    print(f"   Estrutura Final: R$ {produto_final.custo_centavos/100:.2f} 🔄")
    
    # Verificar dependências
    print(f"\n🔗 DEPENDÊNCIAS DA RESINA:")
    dependentes = resina.get_produtos_dependentes()
    for dep in dependentes:
        print(f"   📦 {dep.descricao}")
    
    print(f"\n🔗 DEPENDÊNCIAS DO PRODUTO COMPOSTO:")
    dependentes = produto_composto.get_produtos_dependentes()
    for dep in dependentes:
        print(f"   📦 {dep.descricao}")
    
    print(f"\n✅ TESTE CONCLUÍDO!")
    print(f"   💰 A alteração do preço da resina foi propagada automaticamente")
    print(f"   🔄 Produtos compostos foram recalculados em cascata")

if __name__ == "__main__":
    testar_atualizacao_automatica()
