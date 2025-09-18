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

def analisar_componentes_detalhado():
    """Análise detalhada dos componentes para identificar o problema do recálculo"""
    try:
        produto = MP_Produtos.objects.get(id=1392)
        print(f"=== ANÁLISE DETALHADA DOS COMPONENTES ===")
        print(f"Produto: {produto.descricao}")
        print(f"Custo atual: R$ {produto.custo_centavos/100:.2f}")
        
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        print(f"\n=== COMPONENTES ({componentes.count()}) ===")
        
        custo_total_calculado = 0
        custo_total_observacao = 0
        
        for i, comp in enumerate(componentes, 1):
            print(f"\n{i}. ID {comp.id}: {comp.produto_componente.descricao}")
            print(f"   Quantidade: {comp.quantidade}")
            print(f"   Custo base unitário: R$ {comp.produto_componente.custo_centavos/100:.2f}")
            
            # Cálculo padrão (quantidade × custo base)
            custo_padrao_total = comp.produto_componente.custo_centavos * float(comp.quantidade)
            custo_total_calculado += custo_padrao_total
            print(f"   Custo padrão total: R$ {custo_padrao_total/100:.2f}")
            
            # Analisar observação
            if comp.observacao:
                print(f"   Observação completa: {comp.observacao}")
                try:
                    obs_data = json.loads(comp.observacao)
                    print(f"   Dados da observação:")
                    for key, value in obs_data.items():
                        if key == 'custo_total':
                            print(f"     • {key}: R$ {value/100:.2f}")
                            custo_total_observacao += value
                        elif key == 'custo_unitario':
                            print(f"     • {key}: R$ {value/100:.2f}")
                        else:
                            print(f"     • {key}: {value}")
                except json.JSONDecodeError as e:
                    print(f"   ❌ Erro ao decodificar JSON: {e}")
                    custo_total_observacao += custo_padrao_total
            else:
                print(f"   Sem observação")
                custo_total_observacao += custo_padrao_total
        
        print(f"\n=== RESUMO DE CUSTOS ===")
        print(f"Custo atual no produto: R$ {produto.custo_centavos/100:.2f}")
        print(f"Soma custos padrão: R$ {custo_total_calculado/100:.2f}")
        print(f"Soma custos observação: R$ {custo_total_observacao/100:.2f}")
        
        # Se há diferença significativa
        if abs(50010 - custo_total_observacao) < abs(50010 - custo_total_calculado):
            print(f"\n✅ O valor correto (R$ 500,10) está mais próximo dos custos nas observações")
            print(f"💡 O problema pode estar na lógica do recálculo que não está usando as observações corretamente")
        else:
            print(f"\n⚠️ Nenhum dos cálculos chega próximo ao valor correto de R$ 500,10")
            print(f"🔍 Pode haver um problema na forma como os custos foram salvos")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    analisar_componentes_detalhado()
