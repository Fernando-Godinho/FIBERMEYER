#!/usr/bin/env python
"""
Script para testar se a API de impostos está retornando os dados corretos
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def testar_api_impostos():
    """Simula o que a API retorna para o JavaScript"""
    
    print("🔍 TESTANDO API DE IMPOSTOS")
    print("=" * 60)
    
    # Simular o que a API /api/impostos/ retorna
    impostos = Imposto.objects.all().order_by('nome')
    
    print(f"📊 Total de impostos na API: {impostos.count()}")
    
    # Mostrar alguns exemplos do que será processado pelo JavaScript
    print(f"\n📋 EXEMPLOS DE DADOS DA API:")
    
    for estado in ['SP', 'RJ', 'BA', 'MG', 'RS']:
        print(f"\n🏛️  {estado}:")
        impostos_estado = impostos.filter(nome__icontains=f"ICMS {estado}")
        
        for imposto in impostos_estado:
            print(f"   📋 {imposto.nome} → {imposto.aliquota}%")
    
    # Testar o padrão regex que será usado no JavaScript
    print(f"\n🧪 TESTANDO PADRÃO REGEX:")
    
    exemplos_nomes = [
        "ICMS SP - Contribuinte Industrialização",
        "ICMS RJ - Contribuinte Uso/Consumo", 
        "ICMS BA - Não Contribuinte Industrialização",
        "ICMS MG - Não Contribuinte Uso/Consumo"
    ]
    
    import re
    pattern = r'^ICMS\s+(\w{2})\s+-\s+(.*)'
    
    for nome in exemplos_nomes:
        match = re.match(pattern, nome, re.IGNORECASE)
        if match:
            estado = match.group(1).upper()
            tipo_completo = match.group(2).lower()
            
            # Mapear tipos
            tipo_simples = ''
            if 'contribuinte industrialização' in tipo_completo:
                tipo_simples = 'contrib_industrializacao'
            elif 'contribuinte uso' in tipo_completo:
                tipo_simples = 'contrib_uso_consumo'
            elif 'não contribuinte industrialização' in tipo_completo:
                tipo_simples = 'nao_contrib_industrializacao'
            elif 'não contribuinte uso' in tipo_completo:
                tipo_simples = 'nao_contrib_uso_consumo'
            
            print(f"   ✅ {nome}")
            print(f"      Estado: {estado}")
            print(f"      Tipo: {tipo_simples}")
        else:
            print(f"   ❌ {nome} (não bateu com regex)")
    
    # Mostrar como ficará o cache JavaScript
    print(f"\n💾 SIMULAÇÃO DO CACHE JAVASCRIPT:")
    cache_simulado = {}
    
    for imposto in impostos:
        match = re.match(pattern, imposto.nome, re.IGNORECASE)
        if match:
            estado = match.group(1).upper()
            tipo_completo = match.group(2).lower()
            
            if estado not in cache_simulado:
                cache_simulado[estado] = {}
            
            # Mapear tipos corretamente
            if tipo_completo.startswith('contribuinte industrialização'):
                cache_simulado[estado]['contrib_industrializacao'] = float(imposto.aliquota)
            elif tipo_completo.startswith('contribuinte uso'):
                cache_simulado[estado]['contrib_uso_consumo'] = float(imposto.aliquota)
            elif tipo_completo.startswith('não contribuinte industrialização'):
                cache_simulado[estado]['nao_contrib_industrializacao'] = float(imposto.aliquota)
            elif tipo_completo.startswith('não contribuinte uso'):
                cache_simulado[estado]['nao_contrib_uso_consumo'] = float(imposto.aliquota)
    
    # Mostrar alguns estados do cache
    for estado in ['SP', 'BA', 'MG', 'RS']:
        if estado in cache_simulado:
            print(f"\n   🏛️  {estado}: {cache_simulado[estado]}")
    
    # Testar cenários de cálculo
    print(f"\n🧮 SIMULAÇÃO DE CÁLCULOS:")
    
    cenarios = [
        ('SP', 'CONTRIBUINTE', 'REVENDA'),
        ('SP', 'NAO_CONTRIBUINTE', 'REVENDA'),
        ('SP', 'CONTRIBUINTE', 'CONSUMO_PROPRIO'),
        ('SP', 'NAO_CONTRIBUINTE', 'CONSUMO_PROPRIO'),
        ('BA', 'CONTRIBUINTE', 'REVENDA'),
        ('RS', 'CONTRIBUINTE', 'CONSUMO_PROPRIO'),  # Teste RS que não tem uso/consumo
    ]
    
    for uf, contribuinte, venda_destinada in cenarios:
        print(f"\n   📋 {uf} - {contribuinte} - {venda_destinada}:")
        
        if uf in cache_simulado:
            impostos_estado = cache_simulado[uf]
            
            if venda_destinada == 'REVENDA':
                if contribuinte == 'CONTRIBUINTE':
                    aliquota = impostos_estado.get('contrib_industrializacao', 7.00)
                    tipo = 'Contribuinte Industrialização'
                else:
                    aliquota = impostos_estado.get('nao_contrib_industrializacao', 18.00)
                    tipo = 'Não Contribuinte Industrialização'
            elif venda_destinada == 'CONSUMO_PROPRIO':
                if contribuinte == 'CONTRIBUINTE':
                    aliquota = impostos_estado.get('contrib_uso_consumo', 7.20)
                    tipo = 'Contribuinte Uso/Consumo'
                else:
                    aliquota = impostos_estado.get('nao_contrib_uso_consumo', 18.00)
                    tipo = 'Não Contribuinte Uso/Consumo'
            
            print(f"      ✅ {tipo}: {aliquota}%")
        else:
            print(f"      ❌ Estado não encontrado no cache")

if __name__ == "__main__":
    testar_api_impostos()