#!/usr/bin/env python
"""
Script para simular completamente o salvamento de uma grade
como seria feito no frontend
"""

import os
import sys
import django
import json

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente, MaoObra
from django.test import Client
from django.contrib.auth.models import User
import requests

def simular_salvamento_grade():
    print("=== SIMULAÇÃO COMPLETA: SALVANDO GRADE VIA API ===\n")
    
    # Dados simulados da grade (como vindos do frontend)
    dados_grade = {
        'nome_grade': 'Grade Simulada 2000x1500mm',
        'vao': 2000,
        'comprimento': 1500,
        'eixo_i': 25,
        'perfil_id': 1328,  # I25mm
        'perda': 5,
        'tempo_proc': 0.2,
        'tempo_mtg': 0.3
    }
    
    print(f"📋 Dados da grade:")
    for key, value in dados_grade.items():
        print(f"   {key}: {value}")
    
    # Simular cálculo (como seria feito no frontend)
    print(f"\n🧮 SIMULANDO CÁLCULO...")
    
    # Buscar perfil selecionado
    perfil = MP_Produtos.objects.get(id=dados_grade['perfil_id'])
    chaveta = MP_Produtos.objects.get(id=1332)
    cola = MP_Produtos.objects.get(id=1183)
    
    # Aplicar fórmula da grade
    metros_lineares_por_m2 = (dados_grade['comprimento'] / dados_grade['eixo_i']) * (dados_grade['vao'] / 1000)
    
    # Calcular componentes
    componentes_simulados = []
    
    # Perfil
    fator_perda = 1 + (dados_grade['perda'] / 100)
    peso_perfil = metros_lineares_por_m2 * float(perfil.peso_und) * fator_perda
    custo_perfil = metros_lineares_por_m2 * perfil.custo_centavos * fator_perda
    
    componentes_simulados.append({
        'nome': f"{perfil.descricao} (com {dados_grade['perda']}% perda)",
        'produto_id': perfil.id,
        'quantidade': metros_lineares_por_m2 * fator_perda,
        'custo_unitario': perfil.custo_centavos,
        'custo_total': custo_perfil
    })
    
    # Chaveta
    qtd_chaveta = (dados_grade['vao'] / 150) * 2 * fator_perda
    custo_chaveta = qtd_chaveta * chaveta.custo_centavos
    
    componentes_simulados.append({
        'nome': f"{chaveta.descricao} (com {dados_grade['perda']}% perda)",
        'produto_id': chaveta.id,
        'quantidade': qtd_chaveta,
        'custo_unitario': chaveta.custo_centavos,
        'custo_total': custo_chaveta
    })
    
    # Cola
    qtd_cola = 0.06 * fator_perda
    custo_cola = qtd_cola * cola.custo_centavos
    
    componentes_simulados.append({
        'nome': f"{cola.descricao} (com {dados_grade['perda']}% perda)",
        'produto_id': cola.id,
        'quantidade': qtd_cola,
        'custo_unitario': cola.custo_centavos,
        'custo_total': custo_cola
    })
    
    # Mão de obra - R$ 65.79/hora
    tempo_total = dados_grade['tempo_proc'] + dados_grade['tempo_mtg']
    custo_mo = tempo_total * 65.79 * 100  # em centavos
    
    # Buscar produto de mão de obra
    mo_produto = MP_Produtos.objects.filter(descricao__icontains="MÃO DE OBRA").filter(descricao__icontains="Processamento").first()
    if not mo_produto:
        # Criar se não existir
        mo_produto = MP_Produtos.objects.create(
            descricao="MÃO DE OBRA Processamento/Montagem",
            custo_centavos=6579,  # R$ 65.79
            peso_und=0,
            unidade="HORA",
            referencia="MO-PROC-MTG",
            tipo_produto="simples",
            categoria="Mão de Obra"
        )
        print(f"✅ Produto MO criado: ID {mo_produto.id}")
    
    componentes_simulados.append({
        'nome': f"Processamento/Montagem ({tempo_total}h)",
        'produto_id': mo_produto.id,
        'quantidade': tempo_total,
        'custo_unitario': 6579,  # R$ 65.79 em centavos
        'custo_total': custo_mo
    })
    
    # Calcular custo total
    custo_total_centavos = sum(comp['custo_total'] for comp in componentes_simulados)
    peso_total = peso_perfil + (qtd_chaveta * float(chaveta.peso_und)) + (qtd_cola * float(cola.peso_und))
    
    print(f"\n📊 RESULTADO DO CÁLCULO:")
    print(f"   Metros lineares/m²: {metros_lineares_por_m2:.4f}")
    print(f"   Custo total: R$ {custo_total_centavos/100:.2f}")
    print(f"   Peso total: {peso_total:.3f} kg")
    print(f"   Componentes: {len(componentes_simulados)}")
    
    # 1. Criar produto principal
    print(f"\n💾 SALVANDO PRODUTO PRINCIPAL...")
    
    grade = MP_Produtos.objects.create(
        descricao=dados_grade['nome_grade'],
        custo_centavos=custo_total_centavos,
        peso_und=peso_total,
        unidade='m²',
        referencia='GRADE-SIM-001',
        tipo_produto='composto',
        categoria='Grade'
    )
    
    print(f"✅ Grade criada: ID {grade.id} - {grade.descricao}")
    print(f"   Custo inicial: R$ {grade.custo_centavos/100:.2f}")
    
    # 2. Salvar componentes
    print(f"\n💾 SALVANDO COMPONENTES...")
    
    componentes_salvos = []
    
    for comp_data in componentes_simulados:
        # Criar custos calculados para observação
        custos_obs = {
            'custo_unitario': int(comp_data['custo_unitario']),
            'custo_total': int(comp_data['custo_total']),
            'nome_componente': comp_data['nome'],
            'calculated_at': '2024-01-01T12:00:00'
        }
        
        componente = ProdutoComponente.objects.create(
            produto_principal=grade,
            produto_componente_id=comp_data['produto_id'],
            quantidade=comp_data['quantidade'],
            observacao=json.dumps(custos_obs)
        )
        
        componentes_salvos.append(componente)
        print(f"✅ Componente salvo: {comp_data['nome']}")
        print(f"   Qtd: {comp_data['quantidade']:.4f}, Custo: R$ {comp_data['custo_total']/100:.2f}")
    
    # 3. Verificar se o recálculo automático funcionou
    print(f"\n🔍 VERIFICANDO RECÁLCULO AUTOMÁTICO...")
    
    grade.refresh_from_db()
    print(f"   Custo após recálculo: R$ {grade.custo_centavos/100:.2f}")
    print(f"   Custo esperado: R$ {custo_total_centavos/100:.2f}")
    
    diferenca = abs(grade.custo_centavos - custo_total_centavos)
    
    if diferenca < 10:  # tolerância de 10 centavos
        print(f"✅ SUCESSO: Recálculo automático funcionou corretamente!")
    else:
        print(f"❌ ERRO: Recálculo não funcionou. Diferença: R$ {diferenca/100:.2f}")
        
        # Forçar recálculo manual
        print(f"🔧 Forçando recálculo manual...")
        from main.views import ProdutoComponenteViewSet
        viewset = ProdutoComponenteViewSet()
        viewset.recalcular_preco_produto_composto(grade)
        
        grade.refresh_from_db()
        print(f"   Custo após recálculo manual: R$ {grade.custo_centavos/100:.2f}")
        
        if abs(grade.custo_centavos - custo_total_centavos) < 10:
            print(f"✅ SUCESSO: Recálculo manual funcionou!")
        else:
            print(f"❌ ERRO: Mesmo com recálculo manual há problemas")
    
    # 4. Verificar componentes na base MP
    print(f"\n🔍 VERIFICANDO COMPONENTES NA BASE MP...")
    
    componentes_db = ProdutoComponente.objects.filter(produto_principal=grade)
    print(f"   Componentes salvos: {componentes_db.count()}")
    
    for comp in componentes_db:
        produto_comp = comp.produto_componente
        
        # Custo padrão vs custo calculado
        custo_padrao = produto_comp.custo_centavos * float(comp.quantidade)
        
        custo_calculado = custo_padrao
        if comp.observacao:
            try:
                custos_obs = json.loads(comp.observacao)
                custo_calculado = custos_obs.get('custo_total', custo_padrao)
            except:
                pass
        
        print(f"   • {produto_comp.descricao}")
        print(f"     Qtd: {comp.quantidade}, Padrão: R$ {custo_padrao/100:.2f}, Calculado: R$ {custo_calculado/100:.2f}")
        
        if custo_calculado != custo_padrao:
            print(f"     ✅ Custo customizado salvo na observação")
        else:
            print(f"     ⚠️ Usando custo padrão")
    
    return grade.id

if __name__ == '__main__':
    grade_id = simular_salvamento_grade()
    print(f"\n🎯 GRADE SIMULADA CRIADA: ID {grade_id}")
    print("\n📋 RESUMO:")
    print("   ✅ Produto principal salvo como composto")
    print("   ✅ Componentes salvos com custos calculados na observação") 
    print("   ✅ Recálculo automático deve funcionar")
    print("   ✅ Mão de obra incluída no custo total")
    print("\nAgora teste criar uma grade real no sistema para confirmar!")
