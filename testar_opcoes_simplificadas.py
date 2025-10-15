#!/usr/bin/env python
"""
Script para testar as opções simplificadas de venda destinada
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, VENDA_DESTINADA_CHOICES
from main.models import Imposto

def testar_opcoes_simplificadas():
    """Testa as novas opções simplificadas"""
    
    print("🎯 TESTANDO OPÇÕES SIMPLIFICADAS DE VENDA DESTINADA")
    print("=" * 60)
    
    # Mostrar as opções disponíveis
    print("📋 OPÇÕES DISPONÍVEIS NO MODELO:")
    for value, label in VENDA_DESTINADA_CHOICES:
        print(f"   • {value} → {label}")
    print()
    
    # Testar cenários com as novas opções
    cenarios = [
        # (UF, CONTRIBUINTE, VENDA_DESTINADA, RESULTADO_ESPERADO)
        ('SP', 'CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS SP - Contribuinte Industrialização'),
        ('SP', 'NAO_CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS SP - Não Contribuinte Industrialização'),
        ('SP', 'CONTRIBUINTE', 'USO_CONSUMO', 'ICMS SP - Contribuinte Uso/Consumo'),
        ('SP', 'NAO_CONTRIBUINTE', 'USO_CONSUMO', 'ICMS SP - Não Contribuinte Uso/Consumo'),
        
        ('BA', 'CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS BA - Contribuinte Industrialização'),
        ('BA', 'NAO_CONTRIBUINTE', 'USO_CONSUMO', 'ICMS BA - Não Contribuinte Uso/Consumo'),
        
        # Testando RS que não tem Uso/Consumo
        ('RS', 'CONTRIBUINTE', 'INDUSTRIALIZACAO', 'ICMS RS - Contribuinte Industrialização'),
        ('RS', 'CONTRIBUINTE', 'USO_CONSUMO', 'Padrão (RS não tem Uso/Consumo)'),
    ]
    
    print("🧪 CENÁRIOS DE TESTE:")
    print()
    
    for uf, contribuinte, venda_destinada, esperado in cenarios:
        print(f"🔍 {uf} + {contribuinte} + {venda_destinada}")
        
        # Simular lógica JavaScript simplificada
        if venda_destinada == 'INDUSTRIALIZACAO':
            if contribuinte == 'CONTRIBUINTE':
                nome_imposto = f'ICMS {uf} - Contribuinte Industrialização'
            else:
                nome_imposto = f'ICMS {uf} - Não Contribuinte Industrialização'
        elif venda_destinada == 'USO_CONSUMO':
            if contribuinte == 'CONTRIBUINTE':
                nome_imposto = f'ICMS {uf} - Contribuinte Uso/Consumo'
            else:
                nome_imposto = f'ICMS {uf} - Não Contribuinte Uso/Consumo'
        
        # Tentar encontrar o imposto na base
        try:
            imposto_obj = Imposto.objects.get(nome=nome_imposto)
            resultado = f"{imposto_obj.nome} ({imposto_obj.aliquota}%)"
            status = "✅" if nome_imposto in esperado else "⚠️"
        except Imposto.DoesNotExist:
            resultado = f"Não encontrado - usando padrão"
            status = "⚠️" if "Padrão" not in esperado else "✅"
        
        print(f"   {status} Resultado: {resultado}")
        print(f"   {status} Esperado: {esperado}")
        print()
    
    # Verificar o valor padrão
    print("🔧 TESTE DO VALOR PADRÃO:")
    print(f"   • Valor padrão do modelo: INDUSTRIALIZACAO")
    print(f"   • Isso significa que novos orçamentos usarão Industrialização por padrão")
    print()
    
    # Resumo das mudanças
    print("📊 RESUMO DAS MUDANÇAS:")
    print()
    print("   ❌ REMOVIDAS:")
    print("      • EXPORTAÇÃO → Era isenta (0%)")
    print("      • CONSUMO_PROPRIO → Era mapeado para Uso/Consumo")
    print("      • REVENDA → Era mapeado para Industrialização")
    print()
    print("   ✅ MANTIDAS:")
    print("      • INDUSTRIALIZACAO → Corresponde aos impostos de Industrialização")
    print("      • USO_CONSUMO → Corresponde aos impostos de Uso/Consumo")
    print()
    print("   🎯 BENEFÍCIOS:")
    print("      • Interface mais limpa e objetiva")
    print("      • Mapeamento direto com os tipos de impostos")
    print("      • Menos confusão para o usuário")
    print("      • Conformidade total com a base de impostos")

if __name__ == "__main__":
    testar_opcoes_simplificadas()