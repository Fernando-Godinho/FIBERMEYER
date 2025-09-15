#!/usr/bin/env python
"""
Corrigir automaticamente produtos com valores incorretos
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

def corrigir_automaticamente():
    print("=== CORREÇÃO AUTOMÁTICA DE VALORES INCORRETOS ===\n")
    
    # Buscar produtos compostos recentes que podem ter problema
    produtos_problematicos = []
    
    produtos_compostos = MP_Produtos.objects.filter(
        tipo_produto='composto'
    ).order_by('-id')[:10]  # Últimos 10 produtos compostos
    
    for produto in produtos_compostos:
        custo_real = produto.get_custo_total()
        custo_salvo = produto.custo_centavos
        diferenca = abs(custo_real - custo_salvo)
        
        # Se a diferença for muito grande (> 10%), é problemático
        if diferenca > (custo_real * 0.1) or diferenca > 1000:  # Ou mais de R$ 10,00
            produtos_problematicos.append({
                'produto': produto,
                'custo_real': custo_real,
                'custo_salvo': custo_salvo,
                'diferenca': diferenca
            })
    
    if not produtos_problematicos:
        print("✅ Nenhum produto problemático encontrado")
        return
    
    print(f"🔍 Encontrados {len(produtos_problematicos)} produtos com problemas:")
    
    corrigidos = 0
    erros = 0
    
    for item in produtos_problematicos:
        produto = item['produto']
        print(f"\n📊 {produto.descricao} (ID: {produto.id})")
        print(f"   Custo salvo: {item['custo_salvo']}¢ = R$ {item['custo_salvo']/100:.2f}")
        print(f"   Custo real: {item['custo_real']}¢ = R$ {item['custo_real']/100:.2f}")
        print(f"   Diferença: {item['diferenca']}¢ = R$ {item['diferenca']/100:.2f}")
        
        try:
            # Recalcular e salvar o custo correto
            custo_correto = produto.recalcular_custo_composto()
            print(f"   🔧 Produto corrigido: {custo_correto}¢ = R$ {custo_correto/100:.2f}")
            
            # Também corrigir os valores nas observações dos componentes
            componentes = produto.componentes.all()
            componentes_corrigidos = 0
            
            for comp in componentes:
                if comp.observacao:
                    try:
                        obs = json.loads(comp.observacao)
                        
                        # Recalcular valores corretos
                        custo_unit_correto = comp.produto_componente.custo_centavos
                        custo_total_correto = int(custo_unit_correto * comp.quantidade)
                        
                        # Verificar se precisa correção
                        custo_unit_obs = obs.get('custo_unitario', 0)
                        custo_total_obs = obs.get('custo_total', 0)
                        
                        if (abs(custo_unit_obs - custo_unit_correto) > 1 or 
                            abs(custo_total_obs - custo_total_correto) > 1):
                            
                            # Atualizar observação
                            obs['custo_unitario'] = custo_unit_correto
                            obs['custo_total'] = custo_total_correto
                            obs['corrected_at'] = "2024-12-19 - Corrigir valores incorretos"
                            
                            comp.observacao = json.dumps(obs)
                            comp.save()
                            
                            componentes_corrigidos += 1
                            print(f"     ✅ Componente corrigido: {comp.produto_componente.descricao}")
                    except Exception as e:
                        print(f"     ❌ Erro ao corrigir componente {comp.produto_componente.descricao}: {e}")
            
            print(f"   📊 {componentes_corrigidos} componentes corrigidos")
            corrigidos += 1
                
        except Exception as e:
            print(f"   ❌ Erro ao corrigir produto: {e}")
            erros += 1
    
    print(f"\n🎯 RESUMO DA CORREÇÃO:")
    print(f"   ✅ Produtos corrigidos: {corrigidos}")
    print(f"   ❌ Produtos com erro: {erros}")
    print(f"   📋 Total processados: {len(produtos_problematicos)}")

if __name__ == '__main__':
    corrigir_automaticamente()
