#!/usr/bin/env python
"""
Debug para investigar multiplicação dupla de valores
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos, ProdutoComponente, MaoObra

def debug_duplicacao_valores():
    print("=== DEBUG MULTIPLICAÇÃO DUPLA ===\n")
    
    # 1. Verificar produto de mão de obra
    print("1. VERIFICANDO PRODUTO MÃO DE OBRA:")
    mo_produtos = MP_Produtos.objects.filter(
        descricao__icontains='mão de obra'
    ).filter(
        descricao__icontains='processamento'
    )
    
    for mo in mo_produtos:
        print(f"   ID: {mo.id} | {mo.descricao}")
        print(f"   Custo: {mo.custo_centavos} centavos = R$ {mo.custo_centavos/100:.2f}")
        print(f"   Tipo: {mo.tipo_produto}")
        print()
    
    # 2. Verificar valor da mão de obra na tabela MaoObra
    print("2. VERIFICANDO TABELA MAOOBRA:")
    mo_registros = MaoObra.objects.all()
    for mo in mo_registros:
        print(f"   ID: {mo.id} | {mo.nome}")
        print(f"   Valor: {mo.valor_centavos} centavos = R$ {mo.valor_real:.2f}")
        print(f"   Unidade: {mo.unidade}")
        print()
    
    # 3. Buscar produtos Grade recentes
    print("3. VERIFICANDO PRODUTOS GRADE RECENTES:")
    grades = MP_Produtos.objects.filter(
        descricao__icontains='grade'
    ).order_by('-id')[:5]
    
    for grade in grades:
        print(f"\n📊 GRADE: ID {grade.id} - {grade.descricao}")
        print(f"   Custo total: {grade.custo_centavos} centavos = R$ {grade.custo_centavos/100:.2f}")
        print(f"   Tipo: {grade.tipo_produto}")
        
        # Verificar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=grade)
        print(f"   Componentes ({componentes.count()}):")
        
        soma_componentes = 0
        for comp in componentes:
            custo_componente = comp.produto_componente.custo_centavos * comp.quantidade
            soma_componentes += custo_componente
            
            print(f"     • {comp.produto_componente.descricao}")
            print(f"       Qtd: {comp.quantidade} | Unit: {comp.produto_componente.custo_centavos}¢ | Total: {custo_componente}¢")
            
            # Verificar observação se existe
            if comp.observacao:
                try:
                    import json
                    obs = json.loads(comp.observacao)
                    print(f"       OBS: Unit: {obs.get('custo_unitario')}¢ | Total: {obs.get('custo_total')}¢")
                except:
                    print(f"       OBS: {comp.observacao[:100]}...")
        
        print(f"   ✅ Soma componentes: {soma_componentes}¢ = R$ {soma_componentes/100:.2f}")
        print(f"   📋 Custo produto: {grade.custo_centavos}¢ = R$ {grade.custo_centavos/100:.2f}")
        
        diferenca = abs(grade.custo_centavos - soma_componentes)
        if diferenca > 1:  # Tolerância de 1 centavo
            print(f"   ❌ DIFERENÇA: {diferenca}¢ = R$ {diferenca/100:.2f}")
            if grade.custo_centavos > soma_componentes:
                fator = grade.custo_centavos / soma_componentes if soma_componentes > 0 else 0
                print(f"   📈 Produto custa {fator:.2f}x mais que a soma dos componentes")
        else:
            print(f"   ✅ Valores batem (diferença: {diferenca}¢)")
    
    # 4. Testar cálculo manual de uma grade simples
    print("\n4. TESTE MANUAL DE CÁLCULO:")
    print("   Simulando Grade I25 - 6m x 1,2m vão:")
    
    # Buscar produtos necessários
    perfil_i25 = MP_Produtos.objects.filter(descricao__icontains='I25').first()
    chaveta = MP_Produtos.objects.filter(id=1332).first()
    cola = MP_Produtos.objects.filter(id=1183).first()
    
    if perfil_i25 and chaveta and cola:
        # Cálculos
        metros_lineares = (6000/150) * (1200/1000)  # 48 m/m²
        fator_perda = 1.03  # 3% perda
        
        # Custos materiais
        custo_perfil = perfil_i25.custo_centavos * metros_lineares * fator_perda
        custo_chaveta = chaveta.custo_centavos * (1200/150) * 2 * fator_perda  # 16 m/m²
        custo_cola = cola.custo_centavos * 0.06 * fator_perda  # 0,06 unid/m²
        
        # Custo mão de obra
        valor_hora_mo = 6579  # R$ 65,79 em centavos
        tempo_total = 1.5 + 0.5  # 2 horas
        custo_mo = valor_hora_mo * tempo_total  # 13158 centavos
        
        custo_total_manual = custo_perfil + custo_chaveta + custo_cola + custo_mo
        
        print(f"   Perfil I25: {custo_perfil:.0f}¢ ({metros_lineares:.2f}m x {perfil_i25.custo_centavos}¢)")
        print(f"   Chaveta: {custo_chaveta:.0f}¢ ({(1200/150)*2:.2f}m x {chaveta.custo_centavos}¢)")
        print(f"   Cola: {custo_cola:.0f}¢ (0.06 unid x {cola.custo_centavos}¢)")
        print(f"   Mão de obra: {custo_mo:.0f}¢ ({tempo_total}h x {valor_hora_mo}¢)")
        print(f"   TOTAL MANUAL: {custo_total_manual:.0f}¢ = R$ {custo_total_manual/100:.2f}")
    else:
        print("   ❌ Produtos não encontrados para teste manual")

if __name__ == '__main__':
    debug_duplicacao_valores()
