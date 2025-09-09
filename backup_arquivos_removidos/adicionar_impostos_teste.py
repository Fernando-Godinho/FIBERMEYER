#!/usr/bin/env python
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar as settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def adicionar_impostos_teste():
    """Adiciona impostos de teste com nomenclatura específica para testar a lógica"""
    
    # Limpar impostos existentes para teste
    print("🧹 Limpando impostos existentes...")
    Imposto.objects.all().delete()
    
    # Lista de impostos com nomenclatura padrão para teste
    impostos_teste = [
        # Bahia
        {'nome': 'BA - ICMS Interno', 'aliquota': 7.2, 'descricao': 'ICMS interno para revenda Bahia'},
        {'nome': 'BA - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Bahia'},
        {'nome': 'BA - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Bahia'},
        
        # São Paulo
        {'nome': 'SP - ICMS Interno', 'aliquota': 12.0, 'descricao': 'ICMS interno para revenda São Paulo'},
        {'nome': 'SP - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual São Paulo'},
        {'nome': 'SP - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio São Paulo'},
        
        # Rio de Janeiro
        {'nome': 'RJ - ICMS Interno', 'aliquota': 12.0, 'descricao': 'ICMS interno para revenda Rio de Janeiro'},
        {'nome': 'RJ - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Rio de Janeiro'},
        {'nome': 'RJ - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Rio de Janeiro'},
        
        # Minas Gerais
        {'nome': 'MG - ICMS Interno', 'aliquota': 12.0, 'descricao': 'ICMS interno para revenda Minas Gerais'},
        {'nome': 'MG - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Minas Gerais'},
        {'nome': 'MG - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Minas Gerais'},
        
        # Paraná
        {'nome': 'PR - ICMS Interno', 'aliquota': 12.0, 'descricao': 'ICMS interno para revenda Paraná'},
        {'nome': 'PR - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Paraná'},
        {'nome': 'PR - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Paraná'},
        
        # Santa Catarina
        {'nome': 'SC - ICMS Interno', 'aliquota': 12.0, 'descricao': 'ICMS interno para revenda Santa Catarina'},
        {'nome': 'SC - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Santa Catarina'},
        {'nome': 'SC - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Santa Catarina'},
        
        # Rio Grande do Sul
        {'nome': 'RS - ICMS Interno', 'aliquota': 12.0, 'descricao': 'ICMS interno para revenda Rio Grande do Sul'},
        {'nome': 'RS - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Rio Grande do Sul'},
        {'nome': 'RS - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Rio Grande do Sul'},
        
        # Ceará
        {'nome': 'CE - ICMS Interno', 'aliquota': 7.0, 'descricao': 'ICMS interno para revenda Ceará'},
        {'nome': 'CE - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Ceará'},
        {'nome': 'CE - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Ceará'},
        
        # Pernambuco
        {'nome': 'PE - ICMS Interno', 'aliquota': 7.0, 'descricao': 'ICMS interno para revenda Pernambuco'},
        {'nome': 'PE - ICMS Interestadual', 'aliquota': 12.0, 'descricao': 'ICMS interestadual Pernambuco'},
        {'nome': 'PE - ICMS Consumo', 'aliquota': 18.0, 'descricao': 'ICMS consumo próprio Pernambuco'},
    ]
    
    print("📊 Adicionando impostos de teste...")
    
    for imposto_data in impostos_teste:
        imposto = Imposto.objects.create(
            nome=imposto_data['nome'],
            aliquota=imposto_data['aliquota'],
            descricao=imposto_data['descricao'],
            ativo=True
        )
        print(f"✅ {imposto.nome} - {imposto.aliquota}%")
    
    print(f"\n🎉 Total de {len(impostos_teste)} impostos adicionados com sucesso!")
    print("\n📋 Estrutura de nomenclatura:")
    print("- Formato: 'UF - ICMS Tipo'")
    print("- Tipos: Interno (revenda), Interestadual, Consumo (consumo próprio)")
    print("- Exemplo: 'BA - ICMS Interno' = 7.2%")
    
    return len(impostos_teste)

if __name__ == '__main__':
    try:
        count = adicionar_impostos_teste()
        print(f"\n✅ Script executado com sucesso! {count} impostos adicionados.")
    except Exception as e:
        print(f"❌ Erro ao executar script: {e}")
        sys.exit(1)
