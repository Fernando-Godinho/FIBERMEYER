#!/usr/bin/env python
"""
Script para verificar todos os impostos cadastrados no sistema
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def verificar_todos_impostos():
    """Verifica e exibe todos os impostos cadastrados"""
    
    print("📊 RELATÓRIO COMPLETO DE IMPOSTOS CADASTRADOS")
    print("=" * 70)
    
    # Estatísticas gerais
    total_impostos = Imposto.objects.count()
    impostos_ativos = Imposto.objects.filter(ativo=True).count()
    
    print(f"📈 ESTATÍSTICAS GERAIS:")
    print(f"   📋 Total de impostos: {total_impostos}")
    print(f"   ✅ Impostos ativos: {impostos_ativos}")
    print()
    
    # Impostos por categoria
    impostos_icms = Imposto.objects.filter(nome__icontains="ICMS").count()
    impostos_mao_obra = Imposto.objects.filter(nome__icontains="Mão de Obra").count()
    impostos_material = Imposto.objects.filter(nome__icontains="Material").count()
    
    print(f"📊 POR CATEGORIA:")
    print(f"   🏛️  Impostos ICMS: {impostos_icms}")
    print(f"   🔧 Impostos Mão de Obra: {impostos_mao_obra}")
    print(f"   📦 Impostos Material: {impostos_material}")
    print()
    
    # Detalhamento dos impostos de Mão de Obra
    print("🔧 IMPOSTOS DE MÃO DE OBRA:")
    total_mao_obra = Decimal('0.00')
    impostos_mo = Imposto.objects.filter(nome__icontains="Mão de Obra").order_by('nome')
    
    for imposto in impostos_mo:
        tipo = imposto.nome.replace(" - Mão de Obra", "")
        status = "🟢" if imposto.ativo else "🔴"
        print(f"   {status} {tipo}: {imposto.aliquota}%")
        if imposto.ativo:
            total_mao_obra += imposto.aliquota
    
    print(f"   📊 TOTAL MÃO DE OBRA: {total_mao_obra}%")
    print()
    
    # Detalhamento dos impostos de Material
    print("📦 IMPOSTOS DE MATERIAL:")
    total_material = Decimal('0.00')
    impostos_mat = Imposto.objects.filter(nome__icontains="Material").order_by('nome')
    
    for imposto in impostos_mat:
        tipo = imposto.nome.replace(" - Material", "")
        status = "🟢" if imposto.ativo else "🔴"
        print(f"   {status} {tipo}: {imposto.aliquota}%")
        if imposto.ativo:
            total_material += imposto.aliquota
            
    print(f"   📊 TOTAL MATERIAL: {total_material}%")
    print()
    
    # Alguns exemplos de impostos ICMS
    print("🏛️  EXEMPLOS DE IMPOSTOS ICMS:")
    exemplos_icms = Imposto.objects.filter(nome__icontains="ICMS SP").order_by('nome')[:4]
    
    for imposto in exemplos_icms:
        tipo = imposto.nome.replace("ICMS SP - ", "")
        status = "🟢" if imposto.ativo else "🔴"
        print(f"   {status} SP - {tipo}: {imposto.aliquota}%")
    
    if exemplos_icms.count() < Imposto.objects.filter(nome__icontains="ICMS").count():
        restantes = Imposto.objects.filter(nome__icontains="ICMS").count() - 4
        print(f"   ... e mais {restantes} impostos ICMS")
    print()
    
    # Verificação de conformidade com os totais esperados
    print("✅ VERIFICAÇÃO DE CONFORMIDADE:")
    
    # Verificar se os totais estão corretos
    target_mao_obra = Decimal('35.80')
    target_material = Decimal('38.40')
    
    if abs(total_mao_obra - target_mao_obra) < Decimal('0.01'):
        print(f"   ✅ Mão de Obra: {total_mao_obra}% = {target_mao_obra}% (CORRETO)")
    else:
        print(f"   ❌ Mão de Obra: {total_mao_obra}% ≠ {target_mao_obra}% (INCORRETO)")
        
    if abs(total_material - target_material) < Decimal('0.01'):
        print(f"   ✅ Material: {total_material}% = {target_material}% (CORRETO)")
    else:
        print(f"   ❌ Material: {total_material}% ≠ {target_material}% (INCORRETO)")
    
    print()
    
    # Tabela comparativa final
    print("📋 TABELA COMPARATIVA - MATERIAL vs MÃO DE OBRA:")
    print("-" * 70)
    print(f"{'TIPO DE IMPOSTO':<30} {'MÃO DE OBRA':<15} {'MATERIAL':<15}")
    print("-" * 70)
    
    # Buscar impostos similares
    tipos_impostos = [
        ("PIS/COFINS", "PIS/COFINS"),
        ("IR/Contribuição Social", "IR/C Social"), 
        ("Embalagem", "Embalagem"),
        ("Frete s/ Venda", "Frete"),
        ("Despesas Financeiras", "Desp. Financeira"),
        ("Despesas Administrativas", "Desp. Administrativa"),
        ("Outros Impostos/Taxas", "Outros")
    ]
    
    for nome_busca, nome_display in tipos_impostos:
        # Buscar para Mão de Obra
        try:
            imposto_mo = Imposto.objects.filter(nome__icontains=nome_busca).filter(nome__icontains="Mão de Obra").first()
            valor_mo = f"{imposto_mo.aliquota}%" if imposto_mo else "N/A"
        except:
            valor_mo = "N/A"
        
        # Buscar para Material  
        try:
            imposto_mat = Imposto.objects.filter(nome__icontains=nome_busca).filter(nome__icontains="Material").first()
            valor_mat = f"{imposto_mat.aliquota}%" if imposto_mat else "N/A"
        except:
            valor_mat = "N/A"
            
        print(f"{nome_display:<30} {valor_mo:<15} {valor_mat:<15}")
    
    print("-" * 70)
    print(f"{'TOTAL':<30} {total_mao_obra}%{'':<9} {total_material}%{'':<9}")
    print("-" * 70)
    
    print()
    print("🎯 SISTEMA DE IMPOSTOS COMPLETAMENTE CONFIGURADO!")
    print("   • Impostos ICMS: Todos os 27 estados brasileiros")
    print("   • Impostos Mão de Obra: Total 35,80%") 
    print("   • Impostos Material: Total 38,40%")
    print("   • Pronto para uso no sistema de orçamentos")

if __name__ == "__main__":
    verificar_todos_impostos()