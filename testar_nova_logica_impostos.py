#!/usr/bin/env python
"""
Script para testar a nova lógica de impostos com Industrialização e Uso/Consumo
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def testar_nova_logica():
    """Testa a nova lógica de mapeamento de impostos"""
    
    print("🎯 TESTANDO NOVA LÓGICA DE IMPOSTOS")
    print("=" * 60)
    
    # Cenários de teste baseados nas novas opções
    cenarios = [
        # (UF, CONTRIBUINTE, VENDA_DESTINADA, IMPOSTO_ESPERADO)
        ('SP', 'CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS SP - Contribuinte Industrialização'),
        ('SP', 'NAO_CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS SP - Não Contribuinte Industrialização'),
        ('SP', 'CONTRIBUINTE', 'USO_CONSUMO', 'ICMS SP - Contribuinte Uso/Consumo'),
        ('SP', 'NAO_CONTRIBUINTE', 'USO_CONSUMO', 'ICMS SP - Não Contribuinte Uso/Consumo'),
        
        # Testando compatibilidade com opções antigas
        ('BA', 'CONTRIBUINTE', 'REVENDA', 'ICMS BA - Contribuinte Industrialização'),
        ('BA', 'NAO_CONTRIBUINTE', 'CONSUMO_PROPRIO', 'ICMS BA - Não Contribuinte Uso/Consumo'),
        
        # Testando RS que não tem Uso/Consumo
        ('RS', 'CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS RS - Contribuinte Industrialização'),
        ('RS', 'CONTRIBUINTE', 'USO_CONSUMO', 'ICMS RS - Contribuinte Uso/Consumo'),
        
        # Exportação
        ('MG', 'CONTRIBUINTE', 'EXPORTACAO', 'Isento'),
        ('MG', 'NAO_CONTRIBUINTE', 'EXPORTACAO', 'Isento'),
    ]
    
    print("📋 CENÁRIOS DE TESTE:")
    print()
    
    for uf, contribuinte, venda_destinada, imposto_esperado in cenarios:
        print(f"🔍 {uf} + {contribuinte} + {venda_destinada}")
        
        # Simular lógica JavaScript
        if venda_destinada == 'EXPORTACAO':
            aliquota = 0
            tipo_usado = 'Isento'
            imposto_real = 'Isento'
        elif venda_destinada in ['INDUSTRIALIZACAO', 'REVENDA']:
            if contribuinte == 'CONTRIBUINTE':
                try:
                    imposto_obj = Imposto.objects.get(nome=f'ICMS {uf} - Contribuinte Industrialização')
                    aliquota = float(imposto_obj.aliquota)
                    tipo_usado = 'Contribuinte Industrialização'
                    imposto_real = imposto_obj.nome
                except Imposto.DoesNotExist:
                    aliquota = 7.00
                    tipo_usado = 'Contribuinte Industrialização (Padrão)'
                    imposto_real = 'Não encontrado'
            else:
                try:
                    imposto_obj = Imposto.objects.get(nome=f'ICMS {uf} - Não Contribuinte Industrialização')
                    aliquota = float(imposto_obj.aliquota)
                    tipo_usado = 'Não Contribuinte Industrialização'
                    imposto_real = imposto_obj.nome
                except Imposto.DoesNotExist:
                    aliquota = 18.00
                    tipo_usado = 'Não Contribuinte Industrialização (Padrão)'
                    imposto_real = 'Não encontrado'
        elif venda_destinada in ['USO_CONSUMO', 'CONSUMO_PROPRIO']:
            if contribuinte == 'CONTRIBUINTE':
                try:
                    imposto_obj = Imposto.objects.get(nome=f'ICMS {uf} - Contribuinte Uso/Consumo')
                    aliquota = float(imposto_obj.aliquota)
                    tipo_usado = 'Contribuinte Uso/Consumo'
                    imposto_real = imposto_obj.nome
                except Imposto.DoesNotExist:
                    aliquota = 7.20
                    tipo_usado = 'Contribuinte Uso/Consumo (Padrão)'
                    imposto_real = 'Não encontrado'
            else:
                try:
                    imposto_obj = Imposto.objects.get(nome=f'ICMS {uf} - Não Contribuinte Uso/Consumo')
                    aliquota = float(imposto_obj.aliquota)
                    tipo_usado = 'Não Contribuinte Uso/Consumo'
                    imposto_real = imposto_obj.nome
                except Imposto.DoesNotExist:
                    aliquota = 18.00
                    tipo_usado = 'Não Contribuinte Uso/Consumo (Padrão)'
                    imposto_real = 'Não encontrado'
        
        # Verificar se está correto
        if imposto_real == imposto_esperado or (imposto_esperado == 'Isento' and aliquota == 0):
            status = "✅"
        else:
            status = "❌"
        
        print(f"   {status} Alíquota: {aliquota}%")
        print(f"   {status} Tipo: {tipo_usado}")
        print(f"   {status} Esperado: {imposto_esperado}")
        print(f"   {status} Encontrado: {imposto_real}")
        print()
    
    # Resumo das novas opções disponíveis
    print("📊 RESUMO DAS OPÇÕES DISPONÍVEIS:")
    print()
    print("   🏭 INDUSTRIALIZAÇÃO:")
    print("      • Contribuinte → Alíquota reduzida (7% ou 12%)")
    print("      • Não Contribuinte → Alíquota cheia (17% a 22%)")
    print()
    print("   🔧 USO/CONSUMO:")
    print("      • Contribuinte → Alíquota de uso (7.2% ou 12.4%)")
    print("      • Não Contribuinte → Alíquota de uso (7.2% ou 12.4%)")
    print()
    print("   📦 EXPORTAÇÃO:")
    print("      • Sempre isento (0%)")
    print()
    print("   🔄 COMPATIBILIDADE:")
    print("      • REVENDA → mapeado para INDUSTRIALIZAÇÃO")
    print("      • CONSUMO_PROPRIO → mapeado para USO_CONSUMO")

if __name__ == "__main__":
    testar_nova_logica()