#!/usr/bin/env python
"""
Script para verificar os impostos ICMS cadastrados na base
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def verificar_impostos():
    """Verifica e exibe os impostos ICMS cadastrados"""
    
    print("📊 VERIFICAÇÃO DOS IMPOSTOS ICMS CADASTRADOS")
    print("=" * 70)
    
    # Estatísticas gerais
    total_impostos = Imposto.objects.count()
    impostos_icms = Imposto.objects.filter(nome__icontains="ICMS").count()
    impostos_ativos = Imposto.objects.filter(ativo=True).count()
    
    print(f"\n📈 ESTATÍSTICAS GERAIS:")
    print(f"   📋 Total de impostos: {total_impostos}")
    print(f"   🏛️  Impostos ICMS: {impostos_icms}")
    print(f"   ✅ Impostos ativos: {impostos_ativos}")
    
    # Organizar por categorias
    contribuinte_indust = Imposto.objects.filter(nome__icontains="Contribuinte Industrialização").count()
    contribuinte_uso = Imposto.objects.filter(nome__icontains="Contribuinte Uso/Consumo").count()
    nao_contribuinte_indust = Imposto.objects.filter(nome__icontains="Não Contribuinte Industrialização").count()
    nao_contribuinte_uso = Imposto.objects.filter(nome__icontains="Não Contribuinte Uso/Consumo").count()
    
    print(f"\n📊 POR CATEGORIA:")
    print(f"   🏭 Contribuinte Industrialização: {contribuinte_indust}")
    print(f"   🔧 Contribuinte Uso/Consumo: {contribuinte_uso}")
    print(f"   🏭 Não Contribuinte Industrialização: {nao_contribuinte_indust}")
    print(f"   🔧 Não Contribuinte Uso/Consumo: {nao_contribuinte_uso}")
    
    # Estados com maiores e menores alíquotas
    print(f"\n🏆 RANKING DE ALÍQUOTAS - NÃO CONTRIBUINTE INDUSTRIALIZAÇÃO:")
    maiores = Imposto.objects.filter(
        nome__icontains="Não Contribuinte Industrialização"
    ).order_by('-aliquota')[:5]
    
    for i, imposto in enumerate(maiores, 1):
        estado = imposto.nome.split()[1]
        print(f"   {i}. {estado}: {imposto.aliquota}%")
    
    print(f"\n💰 ESTADOS COM ALÍQUOTAS DE 12% PARA CONTRIBUINTE:")
    estados_12pct = Imposto.objects.filter(
        nome__icontains="Contribuinte Industrialização",
        aliquota=12.0
    ).order_by('nome')
    
    for imposto in estados_12pct:
        estado = imposto.nome.split()[1]
        print(f"   🎯 {estado}: {imposto.aliquota}%")
    
    # Verificar completude - todos os estados têm todas as modalidades?
    estados_completos = []
    estados_incompletos = []
    
    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
               'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RN', 'RS', 
               'RJ', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    
    for estado in estados:
        impostos_estado = Imposto.objects.filter(nome__icontains=f"ICMS {estado}").count()
        # RS tem apenas 2 modalidades, os outros têm 4
        modalidades_esperadas = 2 if estado == 'RS' else 4
        
        if impostos_estado == modalidades_esperadas:
            estados_completos.append(estado)
        else:
            estados_incompletos.append((estado, impostos_estado, modalidades_esperadas))
    
    print(f"\n✅ VERIFICAÇÃO DE COMPLETUDE:")
    print(f"   🎯 Estados completos: {len(estados_completos)}/27")
    if estados_incompletos:
        print(f"   ⚠️  Estados incompletos:")
        for estado, atual, esperado in estados_incompletos:
            print(f"      - {estado}: {atual}/{esperado} modalidades")
    else:
        print(f"   🎉 Todos os estados estão completos!")
    
    # Alguns exemplos específicos
    print(f"\n📋 EXEMPLOS POR ESTADO:")
    exemplos = ['SP', 'RJ', 'BA', 'MG', 'RS']
    for estado in exemplos:
        print(f"\n   🏛️  {estado}:")
        impostos_estado = Imposto.objects.filter(nome__icontains=f"ICMS {estado}").order_by('nome')
        for imposto in impostos_estado:
            tipo = imposto.nome.split('-')[-1].strip()
            status = "🟢" if imposto.ativo else "🔴"
            print(f"      {status} {tipo}: {imposto.aliquota}%")

if __name__ == "__main__":
    verificar_impostos()