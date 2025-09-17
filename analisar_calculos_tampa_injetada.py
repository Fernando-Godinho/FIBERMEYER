#!/usr/bin/env python
"""
Análise dos cálculos da Tampa Injetada baseado no screenshot
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def analisar_calculos_tampa_injetada():
    print("=== ANÁLISE DOS CÁLCULOS TAMPA INJETADA ===\n")
    
    print("📊 DADOS DO SCREENSHOT:")
    print("   • Grade: GRADE INJETADA GI25X38X38MM (com 5% perda)")
    print("   • Quantidade: 1.000 (parece estar em m²)")
    print("   • Custo Unitário: R$ 187,00")
    print("   • Custo Total: R$ 196,35")
    print("   • Mão de Obra: R$ 65,79")
    
    # Buscar a grade no banco para verificar
    try:
        grade = MP_Produtos.objects.get(id=1385)  # GI25X38X38MM
        print(f"\n🔍 DADOS DA GRADE NO BANCO:")
        print(f"   • ID: {grade.id}")
        print(f"   • Descrição: {grade.descricao}")
        print(f"   • Custo: R$ {grade.custo_centavos/100:.2f}/m²")
        
        print(f"\n🧮 VERIFICAÇÃO DOS CÁLCULOS:")
        
        # Analisando o custo da grade
        custo_unitario_mostrado = 187.00
        custo_total_mostrado = 196.35
        quantidade_mostrada = 1.000
        
        print(f"   GRADE:")
        print(f"   • Custo unitário no banco: R$ {grade.custo_centavos/100:.2f}")
        print(f"   • Custo unitário mostrado: R$ {custo_unitario_mostrado:.2f}")
        print(f"   • Quantidade: {quantidade_mostrada} m²")
        
        # Calcular esperado com 5% perda
        custo_sem_perda = quantidade_mostrada * (grade.custo_centavos/100)
        custo_com_perda = custo_sem_perda * 1.05
        
        print(f"   • Cálculo esperado SEM perda: {quantidade_mostrada} × R$ {grade.custo_centavos/100:.2f} = R$ {custo_sem_perda:.2f}")
        print(f"   • Cálculo esperado COM perda: R$ {custo_sem_perda:.2f} × 1.05 = R$ {custo_com_perda:.2f}")
        print(f"   • Custo total mostrado: R$ {custo_total_mostrado:.2f}")
        
        diferenca = abs(custo_com_perda - custo_total_mostrado)
        if diferenca < 0.01:
            print(f"   ✅ Cálculo da grade está CORRETO")
        else:
            print(f"   ❌ Diferença de R$ {diferenca:.2f}")
            
        # Analisando mão de obra
        print(f"\n   MÃO DE OBRA:")
        mo_mostrada = 65.79
        valor_hora = 65.79
        
        # Se for 1 hora total (0.5 + 0.5 ou outro)
        horas_calculadas = mo_mostrada / valor_hora
        print(f"   • Valor mostrado: R$ {mo_mostrada:.2f}")
        print(f"   • Valor/hora padrão: R$ {valor_hora:.2f}")
        print(f"   • Horas calculadas: {horas_calculadas:.1f}h")
        print(f"   • Padrão Tampa Injetada: 0.3 + 0.3 = 0.6h")
        print(f"   • Esperado: 0.6h × R$ {valor_hora:.2f} = R$ {0.6 * valor_hora:.2f}")
        
        if abs(mo_mostrada - (0.6 * valor_hora)) < 0.01:
            print(f"   ✅ Mão de obra está CORRETA (0.6h)")
        elif abs(mo_mostrada - (1.0 * valor_hora)) < 0.01:
            print(f"   ⚠️ Mão de obra calculada para 1.0h (pode estar usando valores padrão diferentes)")
        else:
            print(f"   ❌ Mão de obra com valor inesperado")
            
        # Total geral
        total_esperado = custo_com_perda + mo_mostrada
        print(f"\n💰 TOTAL GERAL:")
        print(f"   • Grade com perda: R$ {custo_com_perda:.2f}")
        print(f"   • Mão de obra: R$ {mo_mostrada:.2f}")
        print(f"   • Total esperado: R$ {total_esperado:.2f}")
        print(f"   • (Verificar se o total mostrado na interface confere)")
        
        print(f"\n🔍 PONTOS A VERIFICAR:")
        print(f"   1. A quantidade 1.000 representa realmente a área em m²?")
        print(f"   2. A perda de 5% está sendo aplicada corretamente?")
        print(f"   3. Os tempos de processamento estão configurados corretamente?")
        print(f"   4. O custo unitário mostrado deveria ser o valor COM perda ou SEM perda?")
        
    except Exception as e:
        print(f"❌ Erro ao buscar grade: {e}")

if __name__ == '__main__':
    analisar_calculos_tampa_injetada()
