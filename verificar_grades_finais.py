#!/usr/bin/env python
"""
Verificação final: Listar todas as grades e seus componentes
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

def verificar_grades_finais():
    print("=== VERIFICAÇÃO FINAL: TODAS AS GRADES ===\n")
    
    # Buscar todas as grades
    grades = MP_Produtos.objects.filter(
        models.Q(descricao__icontains='grade') | 
        models.Q(categoria__icontains='grade')
    ).order_by('-id')
    
    if not grades.exists():
        print("❌ Nenhuma grade encontrada no banco")
        return
    
    print(f"📊 Total de grades encontradas: {grades.count()}\n")
    
    for grade in grades:
        print(f"🏗️ GRADE {grade.id}: {grade.descricao}")
        print(f"   Tipo: {grade.tipo_produto}")
        print(f"   Custo: R$ {grade.custo_centavos/100:.2f}")
        print(f"   Peso: {grade.peso_und} kg")
        print(f"   Unidade: {grade.unidade}")
        print(f"   Categoria: {grade.categoria or 'N/A'}")
        
        # Verificar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=grade)
        print(f"   Componentes: {componentes.count()}")
        
        if componentes.exists():
            total_calculado = 0
            tem_mao_obra = False
            
            for comp in componentes:
                produto_comp = comp.produto_componente
                custo_padrao = produto_comp.custo_centavos * float(comp.quantidade)
                custo_final = custo_padrao
                
                # Verificar se tem custo na observação
                if comp.observacao:
                    try:
                        custos_obs = json.loads(comp.observacao)
                        if 'custo_total' in custos_obs:
                            custo_final = custos_obs['custo_total']
                    except:
                        pass
                
                total_calculado += custo_final
                
                # Verificar se é mão de obra
                if ('mão de obra' in produto_comp.descricao.lower() or 
                    'processamento' in produto_comp.descricao.lower() or
                    'montagem' in produto_comp.descricao.lower()):
                    tem_mao_obra = True
                
                print(f"     • {produto_comp.descricao}")
                print(f"       Qtd: {comp.quantidade}")
                print(f"       Custo: R$ {custo_final/100:.2f}")
            
            print(f"   💰 Soma componentes: R$ {total_calculado/100:.2f}")
            diferenca = abs(grade.custo_centavos - total_calculado)
            
            if diferenca < 10:  # tolerância 10 centavos
                print(f"   ✅ Custo confere (dif: R$ {diferenca/100:.2f})")
            else:
                print(f"   ❌ Custo não confere (dif: R$ {diferenca/100:.2f})")
            
            if tem_mao_obra:
                print(f"   ✅ Inclui mão de obra")
            else:
                print(f"   ⚠️ Não inclui mão de obra")
                
        else:
            print(f"   ⚠️ Sem componentes (produto simples?)")
        
        print() # linha em branco
    
    # Resumo final
    grades_compostas = grades.filter(tipo_produto='composto').count()
    grades_com_componentes = sum(1 for g in grades if ProdutoComponente.objects.filter(produto_principal=g).exists())
    
    print(f"📋 RESUMO:")
    print(f"   Total de grades: {grades.count()}")
    print(f"   Grades compostas: {grades_compostas}")
    print(f"   Grades com componentes: {grades_com_componentes}")
    
    if grades_compostas > 0 and grades_com_componentes > 0:
        print(f"   ✅ Sistema funcionando corretamente!")
    else:
        print(f"   ⚠️ Algumas grades podem não ter componentes")

if __name__ == '__main__':
    from django.db import models
    verificar_grades_finais()
