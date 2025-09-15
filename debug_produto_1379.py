#!/usr/bin/env python
"""
Debug específico do produto ID 1379 com problema
"""
import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def debug_produto_1379():
    print("=== DEBUG PRODUTO ID 1379 ===\n")
    
    try:
        produto = MP_Produtos.objects.get(id=1379)
        print(f"📊 PRODUTO: {produto.descricao}")
        print(f"   Custo salvo: {produto.custo_centavos} centavos = R$ {produto.custo_centavos/100:.2f}")
        print(f"   Tipo: {produto.tipo_produto}")
        print()
        
        print("🔍 ANÁLISE DOS COMPONENTES:")
        componentes = produto.componentes.all()
        soma_real = 0
        soma_observacao = 0
        
        for i, comp in enumerate(componentes, 1):
            custo_real = comp.produto_componente.custo_centavos * comp.quantidade
            soma_real += custo_real
            
            print(f"\n{i}. {comp.produto_componente.descricao}")
            print(f"   Quantidade: {comp.quantidade}")
            print(f"   Custo unitário real: {comp.produto_componente.custo_centavos} centavos")
            print(f"   Custo total real: {custo_real:.2f} centavos")
            
            if comp.observacao:
                try:
                    obs = json.loads(comp.observacao)
                    custo_obs_total = obs.get('custo_total', 0)
                    custo_obs_unit = obs.get('custo_unitario', 0)
                    soma_observacao += custo_obs_total
                    
                    print(f"   Custo na observação:")
                    print(f"     - Unitário: {custo_obs_unit} centavos")
                    print(f"     - Total: {custo_obs_total} centavos")
                    
                    # Verificar diferenças
                    diff_unit = abs(custo_obs_unit - comp.produto_componente.custo_centavos)
                    diff_total = abs(custo_obs_total - custo_real)
                    
                    if diff_unit > 1:
                        print(f"     ❌ DIFERENÇA UNITÁRIO: {diff_unit} centavos")
                    if diff_total > 1:
                        print(f"     ❌ DIFERENÇA TOTAL: {diff_total:.2f} centavos")
                        
                except Exception as e:
                    print(f"   ❌ Erro ao ler observação: {e}")
                    print(f"   Raw observação: {comp.observacao}")
            else:
                print(f"   ⚠️ Sem observação salva")
        
        print(f"\n📊 RESUMO FINAL:")
        print(f"   Soma custos reais: {soma_real:.2f} centavos = R$ {soma_real/100:.2f}")
        print(f"   Soma observações: {soma_observacao} centavos = R$ {soma_observacao/100:.2f}")
        print(f"   Custo produto salvo: {produto.custo_centavos} centavos = R$ {produto.custo_centavos/100:.2f}")
        
        # Verificar qual está sendo usado
        custo_metodo_get = produto.get_custo_total()
        print(f"   Método get_custo_total(): {custo_metodo_get} centavos = R$ {custo_metodo_get/100:.2f}")
        
        print(f"\n🔎 DIAGNÓSTICO:")
        if abs(produto.custo_centavos - soma_observacao) < 10:
            print("   ✅ O sistema está usando os valores da observação")
        elif abs(produto.custo_centavos - soma_real) < 10:
            print("   ✅ O sistema está usando os valores reais dos produtos")
        elif abs(produto.custo_centavos - custo_metodo_get) < 10:
            print("   ✅ O sistema está usando o método get_custo_total()")
        else:
            print("   ❌ Não consegui identificar qual lógica está sendo usada")
        
        # Testar recálculo
        print(f"\n🔄 TESTANDO RECÁLCULO:")
        custo_recalculado = produto.recalcular_custo_composto()
        print(f"   Custo recalculado: {custo_recalculado} centavos = R$ {custo_recalculado/100:.2f}")
        
        # Recarregar produto do banco
        produto.refresh_from_db()
        print(f"   Custo após reload: {produto.custo_centavos} centavos = R$ {produto.custo_centavos/100:.2f}")
        
    except MP_Produtos.DoesNotExist:
        print("❌ Produto ID 1379 não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    debug_produto_1379()
