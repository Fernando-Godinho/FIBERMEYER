#!/usr/bin/env python
"""
Corrigir produtos com valores incorretos na observação
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

def corrigir_produtos_com_valores_incorretos():
    print("=== CORRIGINDO PRODUTOS COM VALORES INCORRETOS ===\n")
    
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
        if diferenca > (custo_real * 0.1):
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
    
    for item in produtos_problematicos:
        produto = item['produto']
        print(f"\n📊 {produto.descricao} (ID: {produto.id})")
        print(f"   Custo salvo: {item['custo_salvo']}¢ = R$ {item['custo_salvo']/100:.2f}")
        print(f"   Custo real: {item['custo_real']}¢ = R$ {item['custo_real']/100:.2f}")
        print(f"   Diferença: {item['diferenca']}¢ = R$ {item['diferenca']/100:.2f}")
        
        # Opção de corrigir
        resposta = input(f"   🔧 Corrigir este produto? (s/N): ").lower().strip()
        
        if resposta == 's' or resposta == 'sim':
            try:
                # Recalcular e salvar o custo correto
                custo_correto = produto.recalcular_custo_composto()
                print(f"   ✅ Produto corrigido: {custo_correto}¢ = R$ {custo_correto/100:.2f}")
                
                # Também corrigir os valores nas observações dos componentes
                componentes = produto.componentes.all()
                for comp in componentes:
                    if comp.observacao:
                        try:
                            obs = json.loads(comp.observacao)
                            
                            # Recalcular valores corretos
                            custo_unit_correto = comp.produto_componente.custo_centavos
                            custo_total_correto = int(custo_unit_correto * comp.quantidade)
                            
                            # Atualizar observação
                            obs['custo_unitario'] = custo_unit_correto
                            obs['custo_total'] = custo_total_correto
                            obs['corrected_at'] = json.dumps({
                                "timestamp": "2024-12-19",
                                "reason": "Corrigir valores incorretos"
                            })
                            
                            comp.observacao = json.dumps(obs)
                            comp.save()
                            
                            print(f"     ✅ Componente corrigido: {comp.produto_componente.descricao}")
                        except Exception as e:
                            print(f"     ❌ Erro ao corrigir componente {comp.produto_componente.descricao}: {e}")
                
            except Exception as e:
                print(f"   ❌ Erro ao corrigir produto: {e}")
        else:
            print(f"   ⏭️ Produto ignorado")
    
    print(f"\n🎯 Correção concluída!")

if __name__ == '__main__':
    corrigir_produtos_com_valores_incorretos()
