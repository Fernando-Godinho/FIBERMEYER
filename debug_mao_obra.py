#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def verificar_mao_obra_em_produto():
    """Verifica se a mão de obra foi salva como componente"""
    try:
        produto = MP_Produtos.objects.get(id=1392)
        print(f"=== VERIFICAÇÃO DE MÃO DE OBRA - PRODUTO {produto.id} ===")
        print(f"Produto: {produto.descricao}")
        print(f"Custo total: R$ {produto.custo_centavos/100:.2f}")
        
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        print(f"\n=== COMPONENTES ({componentes.count()}) ===")
        
        mao_obra_encontrada = False
        custo_total_componentes = 0
        
        for comp in componentes:
            print(f"• {comp.produto_componente.descricao}")
            print(f"  ID: {comp.produto_componente.id} | Qtd: {comp.quantidade} | Custo: R$ {comp.produto_componente.custo_centavos/100:.2f}")
            
            custo_total_componentes += comp.produto_componente.custo_centavos * float(comp.quantidade)
            
            # Verificar se é mão de obra
            if 'processamento' in comp.produto_componente.descricao.lower() or 'montagem' in comp.produto_componente.descricao.lower():
                mao_obra_encontrada = True
                print(f"  ✅ MÃODE OBRA ENCONTRADA!")
        
        print(f"\n=== RESUMO ===")
        print(f"Mão de obra salva: {'✅ SIM' if mao_obra_encontrada else '❌ NÃO'}")
        print(f"Custo total produto: R$ {produto.custo_centavos/100:.2f}")
        print(f"Soma componentes: R$ {custo_total_componentes/100:.2f}")
        print(f"Diferença: R$ {(produto.custo_centavos - custo_total_componentes)/100:.2f}")
        
        if not mao_obra_encontrada:
            print(f"\n🔍 DIAGNÓSTICO:")
            print(f"A diferença de R$ {(produto.custo_centavos - custo_total_componentes)/100:.2f} pode ser a mão de obra não salva.")
            print(f"Se o valor deveria ser R$ 500,10, a mão de obra seria: R$ {(50010 - custo_total_componentes)/100:.2f}")
            
            # Verificar produto de mão de obra disponível
            mo_produto = MP_Produtos.objects.filter(descricao__icontains='processamento').first()
            if mo_produto:
                print(f"Produto de mão de obra disponível: ID {mo_produto.id} - {mo_produto.descricao} - R$ {mo_produto.custo_centavos/100:.2f}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    verificar_mao_obra_em_produto()
