#!/usr/bin/env python3
"""
Debug específico para verificar por que mão de obra não está sendo salva
como componente na tampa montada
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente, MaoObra

def debug_mao_obra_components():
    print("🔍 DEBUG: Mão de obra em produtos compostos")
    print("=" * 60)
    
    # 1. Verificar produtos de mão de obra disponíveis
    print("\n1. PRODUTOS DE MÃO DE OBRA DISPONÍVEIS:")
    mao_obra_produtos = MP_Produtos.objects.filter(descricao__icontains='MÃO DE OBRA')
    for produto in mao_obra_produtos:
        print(f"   ID: {produto.id} | {produto.descricao} | R$ {produto.custo_centavos/100:.2f}")
    
    # 2. Verificar registros MaoObra
    print("\n2. REGISTROS MAOBRA:")
    mao_obra_registros = MaoObra.objects.all()
    for mo in mao_obra_registros:
        print(f"   ID: {mo.id} | {mo.nome} | {mo.descricao} | R$ {mo.valor_real:.2f}/{mo.unidade}")
    
    # 3. Verificar produtos compostos recentes (tampa montada)
    print("\n3. PRODUTOS COMPOSTOS RECENTES (TAMPA MONTADA):")
    produtos_compostos = MP_Produtos.objects.filter(
        descricao__icontains='TAMPA MONTADA'
    ).order_by('-id')[:5]
    
    for produto in produtos_compostos:
        print(f"\n   PRODUTO: ID {produto.id} | {produto.descricao}")
        print(f"   Custo Total: R$ {produto.custo_centavos/100:.2f}")
        
        # Verificar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        print(f"   Componentes ({componentes.count()}):")
        
        has_mao_obra = False
        total_componentes = 0
        
        for comp in componentes:
            custo_comp = comp.quantidade * comp.produto_componente.custo_centavos / 100
            total_componentes += custo_comp
            
            is_mao_obra = 'MÃO DE OBRA' in comp.produto_componente.descricao.upper()
            if is_mao_obra:
                has_mao_obra = True
                print(f"     ✅ {comp.produto_componente.descricao} | Qtd: {comp.quantidade} | R$ {custo_comp:.2f}")
            else:
                print(f"     📦 {comp.produto_componente.descricao} | Qtd: {comp.quantidade} | R$ {custo_comp:.2f}")
        
        print(f"   Total Componentes: R$ {float(total_componentes):.2f}")
        print(f"   Diferença: R$ {(produto.custo_centavos/100) - float(total_componentes):.2f}")
        
        if has_mao_obra:
            print("   ✅ TEM MÃO DE OBRA")
        else:
            print("   ❌ SEM MÃO DE OBRA")
    
    # 4. Verificar último produto criado especificamente
    print("\n4. ANÁLISE DO ÚLTIMO PRODUTO CRIADO:")
    ultimo_produto = MP_Produtos.objects.filter(
        descricao__icontains='TAMPA MONTADA'
    ).order_by('-id').first()
    
    if ultimo_produto:
        print(f"   Produto: {ultimo_produto.descricao}")
        print(f"   ID: {ultimo_produto.id}")
        print(f"   Criado: {ultimo_produto.data_criacao if hasattr(ultimo_produto, 'data_criacao') else 'N/A'}")
        
        componentes = ProdutoComponente.objects.filter(produto_principal=ultimo_produto)
        print(f"   Componentes salvos: {componentes.count()}")
        
        for comp in componentes:
            tipo = "MÃO DE OBRA" if 'MÃO DE OBRA' in comp.produto_componente.descricao.upper() else "MATERIAL"
            print(f"     [{tipo}] {comp.produto_componente.descricao} | Qtd: {comp.quantidade}")

if __name__ == "__main__":
    debug_mao_obra_components()
