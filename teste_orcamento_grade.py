#!/usr/bin/env python
"""
Teste para verificar se a grade no orçamento está funcionando
"""

import requests
import time

def testar_orcamento_grade():
    print("=== TESTE DO ORÇAMENTO COM GRADE ===")
    
    # Verificar se o orçamento está acessível
    url_orcamento = "http://127.0.0.1:8000/orcamento/14/"
    
    try:
        response = requests.get(url_orcamento)
        if response.status_code == 200:
            print("✅ Orçamento acessível")
            
            # Verificar se o modal de grade está presente
            if 'addGradeModal' in response.text:
                print("✅ Modal de grade encontrado")
            else:
                print("❌ Modal de grade não encontrado")
                
            # Verificar se a função calcularGradeOrcamento está presente
            if 'calcularGradeOrcamento' in response.text:
                print("✅ Função calcularGradeOrcamento encontrada")
            else:
                print("❌ Função calcularGradeOrcamento não encontrada")
                
            # Verificar se os campos estão presentes
            campos_esperados = [
                'grade_nome_orc', 'grade_vao_orc', 'grade_comprimento_orc', 
                'grade_eixo_i_orc', 'grade_perfil_orc'
            ]
            
            for campo in campos_esperados:
                if campo in response.text:
                    print(f"✅ Campo {campo} encontrado")
                else:
                    print(f"❌ Campo {campo} não encontrado")
                    
            print("\n📝 Para testar manualmente:")
            print("1. Abra http://127.0.0.1:8000/orcamento/14/")
            print("2. Clique no botão 'Adicionar Grade'")
            print("3. Preencha os campos:")
            print("   - Nome: GRADE TESTE 40x40")
            print("   - Vão: 1000")
            print("   - Comprimento: 416.67")
            print("   - Eixo I: 25")
            print("   - Perfil: Selecione um I25mm")
            print("   - Perda: 5")
            print("4. Clique em 'Calcular Grade'")
            print("5. Verifique se o resultado é ~R$ 174.87")
            
        else:
            print(f"❌ Erro ao acessar orçamento: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == "__main__":
    testar_orcamento_grade()