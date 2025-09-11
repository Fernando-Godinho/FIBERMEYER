#!/usr/bin/env python
"""
Script para verificar componentes das grades salvos no banco
"""

import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente
import json

def debug_grade_components():
    print("=== VERIFICAÇÃO DE COMPONENTES DAS GRADES ===\n")
    
    # Buscar grades no banco
    grades = MP_Produtos.objects.filter(descricao__icontains='grade')
    
    print(f"📊 Grades encontradas: {grades.count()}")
    
    for grade in grades:
        print(f"\n🏗️ GRADE: ID {grade.id} - {grade.descricao}")
        print(f"   Custo: R$ {grade.custo_centavos/100:.2f} ({grade.custo_centavos} centavos)")
        print(f"   Peso: {grade.peso_und} kg")
        print(f"   Tipo: {grade.tipo_produto}")
        
        # Buscar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=grade)
        print(f"   Componentes: {componentes.count()}")
        
        total_custo_componentes = 0
        
        for comp in componentes:
            produto = comp.produto_componente
            custo_unitario = produto.custo_centavos / 100
            custo_total = custo_unitario * float(comp.quantidade)
            total_custo_componentes += custo_total
            
            print(f"     • {produto.descricao}")
            print(f"       Quantidade: {comp.quantidade}")
            print(f"       Custo unitário: R$ {custo_unitario:.2f}")
            print(f"       Custo total: R$ {custo_total:.2f}")
            
            # Verificar se tem custos calculados na observação
            if comp.observacao:
                try:
                    custos_obs = json.loads(comp.observacao)
                    if 'custo_total' in custos_obs:
                        custo_obs = custos_obs['custo_total'] / 100
                        print(f"       Custo na observação: R$ {custo_obs:.2f}")
                        if abs(custo_obs - custo_total) > 0.01:
                            print(f"       ⚠️ DIFERENÇA: Obs R$ {custo_obs:.2f} vs Calc R$ {custo_total:.2f}")
                except (json.JSONDecodeError, KeyError):
                    print(f"       Observação (texto): {comp.observacao[:100]}")
        
        print(f"\n   💰 RESUMO:")
        print(f"     Custo do produto: R$ {grade.custo_centavos/100:.2f}")
        print(f"     Soma componentes: R$ {total_custo_componentes:.2f}")
        diferenca = (grade.custo_centavos/100) - total_custo_componentes
        print(f"     Diferença: R$ {diferenca:.2f}")
        
        if abs(diferenca) > 0.01:
            print(f"     ❌ PROBLEMA: Valor do produto não bate com soma dos componentes!")
        else:
            print(f"     ✅ OK: Valores conferem")
            
    # Verificar se temos mão de obra de processamento/montagem
    print(f"\n🔧 VERIFICAÇÃO MÃO DE OBRA:")
    try:
        from main.models import MaoObra
        mo_processamento = MaoObra.objects.filter(nome__icontains='processamento').first()
        if mo_processamento:
            print(f"   Processamento/Montagem encontrada: ID {mo_processamento.id}")
            print(f"   Valor: R$ {mo_processamento.valor_real:.2f}/{mo_processamento.unidade}")
        else:
            print(f"   ❌ Mão de obra de processamento/montagem não encontrada")
            
        # Listar todas as MO disponíveis
        todas_mo = MaoObra.objects.all()
        print(f"\n   Todas as mãos de obra no banco:")
        for mo in todas_mo:
            print(f"     ID {mo.id}: {mo.nome} - R$ {mo.valor_real:.2f}/{mo.unidade}")
    except Exception as e:
        print(f"   Erro ao verificar mão de obra: {e}")

if __name__ == '__main__':
    debug_grade_components()
