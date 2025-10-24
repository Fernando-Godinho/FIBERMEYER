#!/usr/bin/env python
"""
Teste específico do produto ID 1469 - Verificar se existe e pode ser encontrado
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def testar_produto_1469():
    print("=== TESTE PRODUTO ID 1469 ===\n")
    
    try:
        # Testar se o produto existe
        produto = MP_Produtos.objects.get(id=1469)
        print(f"✅ PRODUTO ENCONTRADO NO BANCO:")
        print(f"   ID: {produto.id}")
        print(f"   Descrição: {produto.descricao}")
        print(f"   Custo: R$ {produto.custo_centavos/100:.2f}")
        print(f"   Tipo: {produto.tipo_produto}")
        print()
        
        # Testar se está sendo retornado pela queryset padrão da API
        todos_produtos = MP_Produtos.objects.all()
        produto_na_lista = todos_produtos.filter(id=1469).first()
        
        if produto_na_lista:
            print("✅ PRODUTO ENCONTRADO NA QUERYSET DA API")
        else:
            print("❌ PRODUTO NÃO ENCONTRADO NA QUERYSET DA API")
            
        # Contar total de produtos
        total_produtos = todos_produtos.count()
        print(f"📊 Total de produtos na base: {total_produtos}")
        
        # Buscar outros arcos para comparação
        print("\n🔍 OUTROS ARCOS NA BASE:")
        arcos = MP_Produtos.objects.filter(descricao__icontains='arco')
        for arco in arcos:
            print(f"   ID {arco.id}: {arco.descricao} - R$ {arco.custo_centavos/100:.2f}")
            
    except MP_Produtos.DoesNotExist:
        print("❌ Produto ID 1469 não encontrado no banco de dados")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    testar_produto_1469()