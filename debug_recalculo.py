#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente
import json

def debug_recalculo():
    """Debug do problema de recálculo do produto"""
    try:
        produto = MP_Produtos.objects.get(id=1392)
        print(f"=== PRODUTO: {produto.descricao} ===")
        print(f"Custo atual: R$ {produto.custo_centavos/100:.2f}")
        
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        print(f"\n=== COMPONENTES ({componentes.count()}) ===")
        
        custo_recalculado = 0
        custo_com_observacao = 0
        
        for i, comp in enumerate(componentes, 1):
            print(f"\n{i}. {comp.produto_componente.descricao}")
            print(f"   ID Componente: {comp.id}")
            print(f"   Quantidade: {comp.quantidade}")
            print(f"   Custo base produto: R$ {comp.produto_componente.custo_centavos/100:.2f}")
            
            # Cálculo padrão (quantidade × custo base)
            custo_padrao = comp.produto_componente.custo_centavos * float(comp.quantidade)
            custo_recalculado += custo_padrao
            print(f"   Custo padrão (qtd × base): R$ {custo_padrao/100:.2f}")
            
            # Verificar observação
            if comp.observacao:
                print(f"   Observação: {comp.observacao[:100]}...")
                try:
                    obs_data = json.loads(comp.observacao)
                    if 'custo_total' in obs_data:
                        custo_customizado = obs_data['custo_total']
                        custo_com_observacao += custo_customizado
                        print(f"   Custo customizado (observação): R$ {custo_customizado/100:.2f}")
                    else:
                        custo_com_observacao += custo_padrao
                        print(f"   Sem custo_total na observação, usando padrão")
                except json.JSONDecodeError:
                    custo_com_observacao += custo_padrao
                    print(f"   Erro ao ler observação, usando padrão")
            else:
                custo_com_observacao += custo_padrao
                print(f"   Sem observação, usando padrão")
        
        print(f"\n=== RESUMO DOS CÁLCULOS ===")
        print(f"Custo atual do produto: R$ {produto.custo_centavos/100:.2f}")
        print(f"Custo recalculado (padrão): R$ {custo_recalculado/100:.2f}")
        print(f"Custo com observações: R$ {custo_com_observacao/100:.2f}")
        
        diferenca = produto.custo_centavos - custo_com_observacao
        print(f"Diferença: R$ {diferenca/100:.2f}")
        
        if abs(diferenca) > 1:  # Mais de 1 centavo de diferença
            print(f"⚠️ PROBLEMA: O recálculo está usando custos padrão em vez dos customizados!")
        else:
            print(f"✅ Custos estão corretos")
            
    except MP_Produtos.DoesNotExist:
        print("❌ Produto ID 1392 não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    debug_recalculo()
