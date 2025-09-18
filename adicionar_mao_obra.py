#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def adicionar_mao_obra_manualmente():
    """Adiciona mão de obra manualmente ao produto para testar"""
    try:
        produto = MP_Produtos.objects.get(id=1392)
        mao_obra_produto = MP_Produtos.objects.get(id=1374)
        
        print(f"=== ADICIONANDO MÃO DE OBRA MANUALMENTE ===")
        print(f"Produto principal: {produto.descricao}")
        print(f"Produto mão de obra: {mao_obra_produto.descricao}")
        
        # Verificar se já existe
        componente_existente = ProdutoComponente.objects.filter(
            produto_principal=produto,
            produto_componente=mao_obra_produto
        ).first()
        
        if componente_existente:
            print(f"✅ Mão de obra já existe como componente: Qtd {componente_existente.quantidade}")
        else:
            # Calcular quantidade de mão de obra baseada na diferença de custos
            custo_atual = produto.custo_centavos
            componentes_atuais = ProdutoComponente.objects.filter(produto_principal=produto)
            custo_componentes = sum(
                comp.produto_componente.custo_centavos * float(comp.quantidade) 
                for comp in componentes_atuais
            )
            
            diferenca = custo_atual - custo_componentes
            quantidade_mao_obra = diferenca / mao_obra_produto.custo_centavos
            
            print(f"Custo total do produto: R$ {custo_atual/100:.2f}")
            print(f"Custo dos componentes atuais: R$ {custo_componentes/100:.2f}")
            print(f"Diferença (mão de obra): R$ {diferenca/100:.2f}")
            print(f"Quantidade calculada: {quantidade_mao_obra:.3f} horas")
            
            # Criar componente de mão de obra
            componente_mo = ProdutoComponente.objects.create(
                produto_principal=produto,
                produto_componente=mao_obra_produto,
                quantidade=round(quantidade_mao_obra, 3),
                observacao='{"tipo": "mao_obra", "descricao": "Adicionado manualmente para correção"}'
            )
            
            print(f"✅ Mão de obra adicionada: ID {componente_mo.id}")
            
            # Verificar novo total
            novo_custo_componentes = sum(
                comp.produto_componente.custo_centavos * float(comp.quantidade) 
                for comp in ProdutoComponente.objects.filter(produto_principal=produto)
            )
            
            print(f"Novo custo total dos componentes: R$ {novo_custo_componentes/100:.2f}")
            print(f"Diferença final: R$ {(custo_atual - novo_custo_componentes)/100:.2f}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    adicionar_mao_obra_manualmente()
