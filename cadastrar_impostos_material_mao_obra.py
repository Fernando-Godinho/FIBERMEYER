#!/usr/bin/env python
"""
Script para cadastrar impostos específicos para Material e Mão de Obra
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def cadastrar_impostos_material_mao_obra():
    """Cadastra impostos específicos para Material e Mão de Obra"""
    
    print("💼 CADASTRANDO IMPOSTOS PARA MATERIAL E MÃO DE OBRA")
    print("=" * 60)
    
    # Dados fornecidos pelo usuário
    impostos_data = [
        # Impostos para MÃO DE OBRA
        {
            'nome': 'PIS/COFINS - Mão de Obra',
            'descricao': 'PIS e COFINS aplicados sobre mão de obra',
            'aliquota': Decimal('3.65'),
            'categoria': 'MAO_OBRA'
        },
        {
            'nome': 'IR/Contribuição Social - Mão de Obra', 
            'descricao': 'Imposto de Renda e Contribuição Social sobre mão de obra',
            'aliquota': Decimal('7.68'),
            'categoria': 'MAO_OBRA'
        },
        {
            'nome': 'Embalagem - Mão de Obra',
            'descricao': 'Custo de embalagem para mão de obra (não aplicável)',
            'aliquota': Decimal('0.00'),
            'categoria': 'MAO_OBRA'
        },
        {
            'nome': 'Frete s/ Venda - Mão de Obra',
            'descricao': 'Frete sobre venda para mão de obra',
            'aliquota': Decimal('0.00'),
            'categoria': 'MAO_OBRA'
        },
        {
            'nome': 'Despesas Financeiras - Mão de Obra',
            'descricao': 'Despesas financeiras aplicadas sobre mão de obra',
            'aliquota': Decimal('1.50'),
            'categoria': 'MAO_OBRA'
        },
        {
            'nome': 'Despesas Administrativas - Mão de Obra',
            'descricao': 'Despesas administrativas aplicadas sobre mão de obra',
            'aliquota': Decimal('18.00'),
            'categoria': 'MAO_OBRA'
        },
        
        # Impostos para MATERIAL
        {
            'nome': 'PIS/COFINS - Material',
            'descricao': 'PIS e COFINS aplicados sobre material',
            'aliquota': Decimal('3.65'),
            'categoria': 'MATERIAL'
        },
        {
            'nome': 'IR/Contribuição Social - Material',
            'descricao': 'Imposto de Renda e Contribuição Social sobre material',
            'aliquota': Decimal('2.28'),
            'categoria': 'MATERIAL'
        },
        {
            'nome': 'Embalagem - Material',
            'descricao': 'Custo de embalagem aplicado sobre material',
            'aliquota': Decimal('1.00'),
            'categoria': 'MATERIAL'
        },
        {
            'nome': 'Frete s/ Venda - Material',
            'descricao': 'Frete sobre venda para material',
            'aliquota': Decimal('0.00'),
            'categoria': 'MATERIAL'
        },
        {
            'nome': 'Despesas Financeiras - Material',
            'descricao': 'Despesas financeiras aplicadas sobre material',
            'aliquota': Decimal('1.50'),
            'categoria': 'MATERIAL'
        },
        {
            'nome': 'Despesas Administrativas - Material',
            'descricao': 'Despesas administrativas aplicadas sobre material',
            'aliquota': Decimal('18.00'),
            'categoria': 'MATERIAL'
        },
    ]
    
    impostos_criados = 0
    impostos_atualizados = 0
    
    print("📋 PROCESSANDO IMPOSTOS:")
    print()
    
    for imposto_info in impostos_data:
        nome = imposto_info['nome']
        
        # Verificar se já existe
        imposto, criado = Imposto.objects.get_or_create(
            nome=nome,
            defaults={
                'descricao': imposto_info['descricao'],
                'aliquota': imposto_info['aliquota'],
                'ativo': True
            }
        )
        
        if criado:
            impostos_criados += 1
            categoria = imposto_info['categoria']
            aliquota = imposto_info['aliquota']
            print(f"   ✅ {categoria}: {nome} - {aliquota}%")
        else:
            # Se já existe, verificar se precisa atualizar
            if imposto.aliquota != imposto_info['aliquota']:
                old_aliquota = imposto.aliquota
                imposto.aliquota = imposto_info['aliquota']
                imposto.descricao = imposto_info['descricao']
                imposto.save()
                impostos_atualizados += 1
                print(f"   📝 {nome}: {old_aliquota}% → {imposto_info['aliquota']}%")
            else:
                print(f"   ⚪ {nome}: já existe ({imposto.aliquota}%)")
    
    print()
    print("=" * 60)
    print("📊 RESUMO:")
    print(f"   ✅ Impostos criados: {impostos_criados}")
    print(f"   📝 Impostos atualizados: {impostos_atualizados}")
    
    # Calcular totais
    print()
    print("🧮 CÁLCULO DOS TOTAIS:")
    
    # Total Mão de Obra
    total_mao_obra = Decimal('0.00')
    impostos_mao_obra = Imposto.objects.filter(nome__icontains="Mão de Obra")
    
    print("   🔧 MÃO DE OBRA:")
    for imposto in impostos_mao_obra.order_by('nome'):
        tipo = imposto.nome.split(' - ')[0]
        print(f"      • {tipo}: {imposto.aliquota}%")
        total_mao_obra += imposto.aliquota
    
    print(f"      📊 TOTAL MÃO DE OBRA: {total_mao_obra}%")
    
    # Total Material  
    total_material = Decimal('0.00')
    impostos_material = Imposto.objects.filter(nome__icontains="Material")
    
    print()
    print("   📦 MATERIAL:")
    for imposto in impostos_material.order_by('nome'):
        tipo = imposto.nome.split(' - ')[0]
        print(f"      • {tipo}: {imposto.aliquota}%")
        total_material += imposto.aliquota
        
    print(f"      📊 TOTAL MATERIAL: {total_material}%")
    
    print()
    print("✅ Cadastro concluído com sucesso!")
    
    # Verificar se os totais conferem
    print()
    print("🔍 VERIFICAÇÃO DOS TOTAIS:")
    if total_mao_obra == Decimal('30.83'):  # 3.65 + 7.68 + 0 + 0 + 1.50 + 18 = 30.83
        print("   ✅ Total Mão de Obra: CORRETO (30.83%)")
    else:
        print(f"   ⚠️ Total Mão de Obra: {total_mao_obra}% (esperado: 30.83%)")
        
    if total_material == Decimal('26.43'):  # 3.65 + 2.28 + 1 + 0 + 1.50 + 18 = 26.43  
        print("   ✅ Total Material: CORRETO (26.43%)")
    else:
        print(f"   ⚠️ Total Material: {total_material}% (esperado: 26.43%)")

if __name__ == "__main__":
    try:
        cadastrar_impostos_material_mao_obra()
    except Exception as e:
        print(f"❌ Erro durante o cadastro: {e}")
        raise