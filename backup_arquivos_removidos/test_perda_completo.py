import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate
from main.views import calcular_custos_template

def test_perda_processo():
    """Testa se a perda de processo está sendo aplicada corretamente"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    
    # Teste 1: Sem perda (0%)
    parametros_sem_perda = {
        'roving_4400': 0.35,
        'manta_300': 0.24,
        'veu_qtd': 0.41,
        'peso_m': 4.0,
        'perda_processo': 0,
        'descricao': 'Teste sem perda'
    }
    
    resultado_sem_perda = calcular_custos_template(template, parametros_sem_perda)
    
    # Teste 2: Com 3% de perda
    parametros_com_perda = {
        'roving_4400': 0.35,
        'manta_300': 0.24,
        'veu_qtd': 0.41,
        'peso_m': 4.0,
        'perda_processo': 3,
        'descricao': 'Teste com 3% perda'
    }
    
    resultado_com_perda = calcular_custos_template(template, parametros_com_perda)
    
    # Teste 3: Com 5% de perda
    parametros_com_perda_5 = {
        'roving_4400': 0.35,
        'manta_300': 0.24,
        'veu_qtd': 0.41,
        'peso_m': 4.0,
        'perda_processo': 5,
        'descricao': 'Teste com 5% perda'
    }
    
    resultado_com_perda_5 = calcular_custos_template(template, parametros_com_perda_5)
    
    print("=== TESTE DE PERDA DE PROCESSO ===\n")
    
    print(f"1. SEM PERDA (0%):")
    print(f"   Custo dos materiais: R$ {resultado_sem_perda['custo_total_sem_perda']:.2f}")
    print(f"   Perda aplicada: R$ {resultado_sem_perda['perda_processo']:.2f}")
    print(f"   Custo total: R$ {resultado_sem_perda['custo_total']:.2f}")
    
    print(f"\n2. COM 3% DE PERDA:")
    print(f"   Custo dos materiais: R$ {resultado_com_perda['custo_total_sem_perda']:.2f}")
    print(f"   Perda aplicada: R$ {resultado_com_perda['perda_processo']:.2f}")
    print(f"   Custo total: R$ {resultado_com_perda['custo_total']:.2f}")
    
    print(f"\n3. COM 5% DE PERDA:")
    print(f"   Custo dos materiais: R$ {resultado_com_perda_5['custo_total_sem_perda']:.2f}")
    print(f"   Perda aplicada: R$ {resultado_com_perda_5['perda_processo']:.2f}")
    print(f"   Custo total: R$ {resultado_com_perda_5['custo_total']:.2f}")
    
    # Verificações
    print(f"\n=== VERIFICAÇÕES ===")
    
    # Verificar se custo dos materiais é igual em todos os casos
    custo_base = resultado_sem_perda['custo_total_sem_perda']
    assert abs(resultado_com_perda['custo_total_sem_perda'] - custo_base) < 0.01, "Custo base deve ser igual"
    assert abs(resultado_com_perda_5['custo_total_sem_perda'] - custo_base) < 0.01, "Custo base deve ser igual"
    print("✓ Custo dos materiais é consistente em todos os testes")
    
    # Verificar cálculo da perda de 3%
    perda_esperada_3 = custo_base * 0.03
    perda_calculada_3 = resultado_com_perda['perda_processo']
    assert abs(perda_esperada_3 - perda_calculada_3) < 0.01, f"Perda 3% incorreta: esperado {perda_esperada_3:.2f}, calculado {perda_calculada_3:.2f}"
    print(f"✓ Perda de 3% calculada corretamente: R$ {perda_calculada_3:.2f}")
    
    # Verificar cálculo da perda de 5%
    perda_esperada_5 = custo_base * 0.05
    perda_calculada_5 = resultado_com_perda_5['perda_processo']
    assert abs(perda_esperada_5 - perda_calculada_5) < 0.01, f"Perda 5% incorreta: esperado {perda_esperada_5:.2f}, calculado {perda_calculada_5:.2f}"
    print(f"✓ Perda de 5% calculada corretamente: R$ {perda_calculada_5:.2f}")
    
    # Verificar custo total
    total_esperado_3 = custo_base + perda_esperada_3
    total_calculado_3 = resultado_com_perda['custo_total']
    assert abs(total_esperado_3 - total_calculado_3) < 0.01, f"Total 3% incorreto: esperado {total_esperado_3:.2f}, calculado {total_calculado_3:.2f}"
    print(f"✓ Custo total com 3% de perda correto: R$ {total_calculado_3:.2f}")
    
    print(f"\n🎉 TODOS OS TESTES PASSARAM!")
    print(f"A perda de processo está sendo aplicada corretamente sobre o custo total dos materiais.")

if __name__ == "__main__":
    test_perda_processo()
