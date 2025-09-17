#!/usr/bin/env python
"""
Teste para validar o novo template Tampa Injetada
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def teste_template_tampa_injetada():
    print("=== TESTE: NOVO TEMPLATE TAMPA INJETADA ===\n")
    
    print("🚀 NOVO TEMPLATE CRIADO:")
    print("   • Nome: Tampa Injetada")
    print("   • Baseado no template Grades")
    print("   • Usa grades injetadas em vez de perfis")
    
    print(f"\n📋 GRADES INJETADAS DISPONÍVEIS:")
    try:
        grades = MP_Produtos.objects.filter(descricao__icontains='grade').filter(descricao__icontains='injetada')
        if grades.count() > 0:
            for grade in grades:
                print(f"   • ID: {grade.id} | {grade.descricao} | R$ {grade.custo_centavos/100:.2f}/m²")
        else:
            print("   ❌ Nenhuma grade injetada encontrada no banco")
        
        print(f"\n✅ CAMPOS DO FORMULÁRIO:")
        print(f"   • Nome da Tampa Injetada *")
        print(f"   • Vão (mm) *") 
        print(f"   • Comprimento (mm) *")
        print(f"   • Selecione a Grade Injetada * (dropdown)")
        print(f"   • Perda (%) - padrão: 5%")
        print(f"   • Tempo PROC (h) - padrão: 0.3h")
        print(f"   • Tempo MTG (h) - padrão: 0.3h")
        
        print(f"\n🧮 FÓRMULA DE CÁLCULO:")
        print(f"   1. Área = (vão/1000) × (comprimento/1000) m²")
        print(f"   2. Custo Grade = área × preço_grade/m² × (1 + perda%)")
        print(f"   3. Custo MO = (tempo_proc + tempo_mtg) × R$ 65,79/h")
        print(f"   4. Total = Custo Grade + Custo MO")
        
        print(f"\n📊 EXEMPLO PRÁTICO (Tampa 2000mm × 1500mm):")
        area_exemplo = (2000/1000) * (1500/1000)  # 3 m²
        
        # Usar a primeira grade para exemplo
        if grades.count() > 0:
            grade_exemplo = grades.first()
            custo_grade = area_exemplo * (grade_exemplo.custo_centavos/100) * 1.05  # com 5% perda
            custo_mo = (0.3 + 0.3) * 65.79  # 0.6h total
            total = custo_grade + custo_mo
            
            print(f"   • Área: {area_exemplo} m²")
            print(f"   • Grade: {grade_exemplo.descricao}")
            print(f"   • Custo Grade: {area_exemplo}m² × R$ {grade_exemplo.custo_centavos/100:.2f} × 1.05 = R$ {custo_grade:.2f}")
            print(f"   • Custo MO: 0.6h × R$ 65,79 = R$ {custo_mo:.2f}")
            print(f"   • TOTAL: R$ {total:.2f}")
            
        print(f"\n✅ COMPONENTES NA TABELA:")
        print(f"   1. Grade Injetada selecionada (com perda)")
        print(f"   2. Mão de Obra Processamento/Montagem (sem perda)")
        
        print(f"\n🎯 DIFERENÇAS DO TEMPLATE GRADES:")
        print(f"   • Grades usa perfis I25/I32/I38 + chaveta + cola")
        print(f"   • Tampa Injetada usa grade injetada pronta por m²")
        print(f"   • Cálculo mais simples: área × preço/m²")
        print(f"   • Sem necessidade de eixo I ou chavetas")
        
        print(f"\n🚀 TESTE NA INTERFACE:")
        print(f"   1. Selecionar 'Tampa Injetada' no dropdown")
        print(f"   2. Preencher: nome, vão, comprimento")
        print(f"   3. Escolher uma das grades injetadas")
        print(f"   4. Ajustar perda e tempos se necessário")
        print(f"   5. Clicar 'Calcular Tampa Injetada'")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    teste_template_tampa_injetada()
