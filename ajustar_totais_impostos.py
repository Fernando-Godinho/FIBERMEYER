#!/usr/bin/env python
"""
Script para ajustar impostos para atingir os totais corretos: 35,8% Mão de Obra e 38,4% Material
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def ajustar_totais_impostos():
    """Ajusta os totais para 35,8% Mão de Obra e 38,4% Material"""
    
    print("🔧 AJUSTANDO TOTAIS DE IMPOSTOS")
    print("=" * 60)
    
    # Valores originais fornecidos
    valores_originais = {
        'mao_obra': {
            'PIS/COFINS': Decimal('3.65'),
            'IR/C Social': Decimal('7.68'), 
            'Embalagem': Decimal('0.00'),
            'Frete s/ Venda': Decimal('0.00'),
            'Desp Financeira': Decimal('1.50'),
            'Desp Adm': Decimal('18.00'),
            'TOTAL_INFORMADO': Decimal('35.80')  # Total informado pelo usuário
        },
        'material': {
            'PIS/COFINS': Decimal('3.65'),
            'IR/C Social': Decimal('2.28'),
            'Embalagem': Decimal('1.00'), 
            'Frete s/ Venda': Decimal('0.00'),
            'Desp Financeira': Decimal('1.50'),
            'Desp Adm': Decimal('18.00'),
            'TOTAL_INFORMADO': Decimal('38.40')  # Total informado pelo usuário
        }
    }
    
    # Calcular totais dos valores informados
    total_calculado_mao_obra = sum([v for k, v in valores_originais['mao_obra'].items() if k != 'TOTAL_INFORMADO'])
    total_calculado_material = sum([v for k, v in valores_originais['material'].items() if k != 'TOTAL_INFORMADO'])
    
    print("📊 ANÁLISE DOS TOTAIS:")
    print()
    print(f"   MÃO DE OBRA:")
    print(f"      • Soma individual: {total_calculado_mao_obra}%")
    print(f"      • Total informado: {valores_originais['mao_obra']['TOTAL_INFORMADO']}%")
    print(f"      • Diferença: {valores_originais['mao_obra']['TOTAL_INFORMADO'] - total_calculado_mao_obra}%")
    
    print(f"   MATERIAL:")
    print(f"      • Soma individual: {total_calculado_material}%")
    print(f"      • Total informado: {valores_originais['material']['TOTAL_INFORMADO']}%")
    print(f"      • Diferença: {valores_originais['material']['TOTAL_INFORMADO'] - total_calculado_material}%")
    
    # Verificar se há impostos adicionais não listados
    diferenca_mao_obra = valores_originais['mao_obra']['TOTAL_INFORMADO'] - total_calculado_mao_obra
    diferenca_material = valores_originais['material']['TOTAL_INFORMADO'] - total_calculado_material
    
    impostos_adicionais = []
    
    if diferenca_mao_obra > 0:
        impostos_adicionais.append({
            'nome': 'Outros Impostos/Taxas - Mão de Obra',
            'descricao': 'Impostos e taxas adicionais para completar o total de 35,8%',
            'aliquota': diferenca_mao_obra,
            'categoria': 'MAO_OBRA'
        })
        
    if diferenca_material > 0:
        impostos_adicionais.append({
            'nome': 'Outros Impostos/Taxas - Material', 
            'descricao': 'Impostos e taxas adicionais para completar o total de 38,4%',
            'aliquota': diferenca_material,
            'categoria': 'MATERIAL'
        })
    
    print()
    print("💡 SOLUÇÃO PROPOSTA:")
    
    if impostos_adicionais:
        print("   Criar impostos adicionais para completar os totais:")
        print()
        
        for imposto_info in impostos_adicionais:
            nome = imposto_info['nome']
            
            # Criar ou atualizar o imposto adicional
            imposto, criado = Imposto.objects.get_or_create(
                nome=nome,
                defaults={
                    'descricao': imposto_info['descricao'],
                    'aliquota': imposto_info['aliquota'],
                    'ativo': True
                }
            )
            
            if criado:
                categoria = imposto_info['categoria']
                aliquota = imposto_info['aliquota']
                print(f"   ✅ {categoria}: {nome} - {aliquota}%")
            else:
                print(f"   ⚪ {nome}: já existe ({imposto.aliquota}%)")
    
    # Recalcular totais finais
    print()
    print("🧮 TOTAIS FINAIS APÓS AJUSTE:")
    
    # Total Mão de Obra
    total_final_mao_obra = Decimal('0.00')
    impostos_mao_obra = Imposto.objects.filter(nome__icontains="Mão de Obra")
    
    print("   🔧 MÃO DE OBRA:")
    for imposto in impostos_mao_obra.order_by('nome'):
        tipo = imposto.nome.split(' - ')[0]
        print(f"      • {tipo}: {imposto.aliquota}%")
        total_final_mao_obra += imposto.aliquota
    
    print(f"      📊 TOTAL MÃO DE OBRA: {total_final_mao_obra}%")
    
    # Total Material
    total_final_material = Decimal('0.00')
    impostos_material = Imposto.objects.filter(nome__icontains="Material")
    
    print()
    print("   📦 MATERIAL:")
    for imposto in impostos_material.order_by('nome'):
        tipo = imposto.nome.split(' - ')[0]
        print(f"      • {tipo}: {imposto.aliquota}%")
        total_final_material += imposto.aliquota
        
    print(f"      📊 TOTAL MATERIAL: {total_final_material}%")
    
    # Verificação final
    print()
    print("✅ VERIFICAÇÃO FINAL:")
    
    if abs(total_final_mao_obra - Decimal('35.80')) < Decimal('0.01'):
        print(f"   ✅ Mão de Obra: {total_final_mao_obra}% = 35,80% ✓")
    else:
        print(f"   ❌ Mão de Obra: {total_final_mao_obra}% ≠ 35,80%")
        
    if abs(total_final_material - Decimal('38.40')) < Decimal('0.01'):
        print(f"   ✅ Material: {total_final_material}% = 38,40% ✓")
    else:
        print(f"   ❌ Material: {total_final_material}% ≠ 38,40%")
    
    print()
    print("📋 RESUMO PARA CONFERÊNCIA:")
    print("   Valores que devem somar 35,8% (Mão de Obra):")
    print("   • PIS/COFINS: 3,65% + IR/C Social: 7,68% + Embalagem: 0,00% + Frete: 0,00% + Desp.Fin: 1,50% + Desp.Adm: 18,00% = 30,83%")
    print("   • Diferença para 35,8%: 4,97% (pode ser outros impostos não listados)")
    print()
    print("   Valores que devem somar 38,4% (Material):")  
    print("   • PIS/COFINS: 3,65% + IR/C Social: 2,28% + Embalagem: 1,00% + Frete: 0,00% + Desp.Fin: 1,50% + Desp.Adm: 18,00% = 26,43%")
    print("   • Diferença para 38,4%: 11,97% (pode ser outros impostos não listados)")

if __name__ == "__main__":
    try:
        ajustar_totais_impostos()
    except Exception as e:
        print(f"❌ Erro durante o ajuste: {e}")
        raise