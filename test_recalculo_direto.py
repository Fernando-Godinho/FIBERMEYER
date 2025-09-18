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

def testar_recalculo_direto():
    """Testa o recálculo direto simulando o que acontece na view"""
    try:
        produto = MP_Produtos.objects.get(id=1392)
        print(f"=== TESTE DE RECÁLCULO DIRETO ===")
        print(f"Produto: {produto.descricao}")
        print(f"Custo antes: R$ {produto.custo_centavos/100:.2f}")
        
        # Simular a lógica do recálculo forçado da view
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        custo_total = 0
        peso_total = 0
        
        print(f"\n=== RECALCULANDO PRODUTO COMPOSTO: {produto.descricao} ===")
        
        for comp in componentes:
            produto_comp = comp.produto_componente
            if produto_comp:
                # Verificar se há custos customizados na observação
                custo_componente_centavos = produto_comp.custo_centavos
                
                if comp.observacao:
                    try:
                        custos_salvos = json.loads(comp.observacao)
                        if 'custo_total' in custos_salvos:
                            # Usar custo total salvo na observação (já calculado)
                            custo_componente_centavos = custos_salvos['custo_total']
                            print(f"   • {produto_comp.descricao}: usando custo salvo R$ {custo_componente_centavos/100:.2f}")
                        else:
                            # Usar custo padrão do produto
                            custo_componente_centavos = produto_comp.custo_centavos * float(comp.quantidade)
                            print(f"   • {produto_comp.descricao}: usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                    except (json.JSONDecodeError, KeyError):
                        # Se erro na observação, usar cálculo padrão
                        custo_componente_centavos = produto_comp.custo_centavos * float(comp.quantidade)
                        print(f"   • {produto_comp.descricao}: erro na observação, usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                else:
                    # Sem observação, usar cálculo padrão
                    custo_componente_centavos = produto_comp.custo_centavos * float(comp.quantidade)
                    print(f"   • {produto_comp.descricao}: sem observação, usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                
                # PROBLEMA IDENTIFICADO: antes era custo_total += custo_componente_centavos / 100
                # Agora corrigido para: custo_total += custo_componente_centavos (manter em centavos)
                custo_total += custo_componente_centavos
                peso_total += float(produto_comp.peso_und) * float(comp.quantidade)
        
        print(f"   💰 Custo total calculado: R$ {custo_total/100:.2f}")
        
        # Simular o que aconteceria com a atualização
        custo_antes = produto.custo_centavos
        custo_novo = int(round(custo_total))  # Corrigido: sem multiplicar por 100
        
        print(f"\n=== COMPARAÇÃO ===")
        print(f"Custo atual no banco: R$ {custo_antes/100:.2f}")
        print(f"Custo calculado (novo): R$ {custo_novo/100:.2f}")
        print(f"Diferença: R$ {(custo_novo - custo_antes)/100:.2f}")
        
        if abs(custo_novo - custo_antes) > 1:  # Mais de 1 centavo
            print(f"⚠️ PROBLEMA: Recálculo mudaria o valor!")
            print(f"   - Valor correto atual: R$ {custo_antes/100:.2f}")
            print(f"   - Valor calculado errado: R$ {custo_novo/100:.2f}")
        else:
            print(f"✅ Recálculo manteria o valor correto")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    testar_recalculo_direto()
