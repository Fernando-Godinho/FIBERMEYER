#!/usr/bin/env python
"""
Teste de simulação do cálculo da Tampa Injetada
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def simular_calculo_tampa_injetada():
    print("=== SIMULAÇÃO CÁLCULO TAMPA INJETADA ===\n")
    
    # Dados do teste (baseado no screenshot)
    dados = {
        'nome_tampa': 'Teste Tampa Injetada',
        'vao': 1000,  # mm
        'comprimento': 1000,  # mm  
        'grade_id': 1385,  # GI25X38X38MM
        'perda': 5,  # %
        'tempo_proc': 0.3,  # h - PADRÃO
        'tempo_mtg': 0.3   # h - PADRÃO
    }
    
    print("📊 DADOS DO TESTE:")
    for key, value in dados.items():
        print(f"   • {key}: {value}")
    
    # Simulação do cálculo
    print(f"\n🧮 SIMULAÇÃO DO CÁLCULO:")
    
    # 1. Área da tampa
    area_tampa = (dados['vao'] / 1000) * (dados['comprimento'] / 1000)
    print(f"   Área: ({dados['vao']}/1000) × ({dados['comprimento']}/1000) = {area_tampa} m²")
    
    # 2. Fator de perda
    fator_perda = 1 + (dados['perda'] / 100)
    print(f"   Fator perda: 1 + ({dados['perda']}/100) = {fator_perda}")
    
    # 3. Custo da grade
    custo_grade_unitario = 18700  # R$ 187,00 em centavos
    custo_grade_sem_perda = area_tampa * custo_grade_unitario
    custo_grade_com_perda = custo_grade_sem_perda * fator_perda
    
    print(f"   Custo grade SEM perda: {area_tampa} × {custo_grade_unitario} = {custo_grade_sem_perda} centavos")
    print(f"   Custo grade COM perda: {custo_grade_sem_perda} × {fator_perda} = {custo_grade_com_perda} centavos")
    print(f"   = R$ {custo_grade_com_perda/100:.2f}")
    
    # 4. Mão de obra
    valor_hora_mo = 65.79
    tempo_total = dados['tempo_proc'] + dados['tempo_mtg'] 
    custo_mo = tempo_total * valor_hora_mo * 100  # em centavos
    
    print(f"   Tempo total MO: {dados['tempo_proc']} + {dados['tempo_mtg']} = {tempo_total}h")
    print(f"   Custo MO: {tempo_total}h × R$ {valor_hora_mo} = R$ {custo_mo/100:.2f}")
    
    # 5. Total
    custo_total = custo_grade_com_perda + custo_mo
    print(f"   TOTAL: R$ {custo_grade_com_perda/100:.2f} + R$ {custo_mo/100:.2f} = R$ {custo_total/100:.2f}")
    
    print(f"\n📋 RESULTADO ESPERADO NA TABELA:")
    print(f"   Grade:")
    print(f"   ├─ Quantidade: {area_tampa} m²")
    print(f"   ├─ Custo Unitário: R$ {(custo_grade_unitario * fator_perda)/100:.2f} (com perda)")
    print(f"   └─ Custo Total: R$ {custo_grade_com_perda/100:.2f}")
    print(f"   ")
    print(f"   Mão de Obra:")
    print(f"   ├─ Quantidade: {tempo_total} h")
    print(f"   ├─ Custo Unitário: R$ {valor_hora_mo:.2f}/h")
    print(f"   └─ Custo Total: R$ {custo_mo/100:.2f}")
    
    # Comparar com screenshot
    print(f"\n🔍 COMPARAÇÃO COM SCREENSHOT:")
    screenshot_grade_total = 196.35
    screenshot_mo_total = 65.79
    
    if abs(custo_grade_com_perda/100 - screenshot_grade_total) < 0.01:
        print(f"   ✅ Grade: Calculado R$ {custo_grade_com_perda/100:.2f} = Screenshot R$ {screenshot_grade_total:.2f}")
    else:
        print(f"   ❌ Grade: Calculado R$ {custo_grade_com_perda/100:.2f} ≠ Screenshot R$ {screenshot_grade_total:.2f}")
        
    if abs(custo_mo/100 - screenshot_mo_total) < 0.01:
        print(f"   ✅ MO: Calculado R$ {custo_mo/100:.2f} = Screenshot R$ {screenshot_mo_total:.2f}")
    else:
        print(f"   ❌ MO: Calculado R$ {custo_mo/100:.2f} ≠ Screenshot R$ {screenshot_mo_total:.2f}")
        tempo_screenshot = screenshot_mo_total / valor_hora_mo
        print(f"       (Screenshot indica {tempo_screenshot:.1f}h em vez de {tempo_total:.1f}h)")

if __name__ == '__main__':
    simular_calculo_tampa_injetada()
