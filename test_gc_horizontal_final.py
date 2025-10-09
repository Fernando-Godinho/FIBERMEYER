#!/usr/bin/env python3
"""
Script para testar o Guarda Corpo Horizontal após as correções
"""

import webbrowser
import time

def test_guarda_corpo_horizontal():
    """Testa o template de Guarda Corpo Horizontal"""
    
    print("🧪 TESTANDO GUARDA CORPO HORIZONTAL CORRIGIDO")
    print("=" * 50)
    
    print("\n📋 INSTRUÇÕES DE TESTE:")
    print("1. Abrindo página MP no navegador...")
    
    # Abrir página no navegador
    webbrowser.open("http://127.0.0.1:8000/mp/")
    
    print("2. Execute os seguintes passos:")
    print("   ✅ Selecione 'Guarda Corpo - Horizontal' no dropdown")
    print("   ✅ Preencha os campos:")
    print("      - Nome: Guarda Corpo Teste")
    print("      - Largura: 2.0")
    print("      - Altura: 1.1") 
    print("      - Nº Colunas: 1")
    print("      - Nº Brr. Intermed.: 1")
    print("      - Tipo Tubo Quadrado: Tubo Quadrado 50 #6mm")
    print("      - Tipo Sapata: SAPATA INOX 150#3MM")
    print("   ✅ Clique em 'Calcular Guarda Corpo'")
    
    print("\n🔍 VERIFICAÇÕES NA TABELA:")
    print("   ✅ Material/Serviço: nomes dos produtos")
    print("   ✅ Descrição: descrições dos produtos")
    print("   ✅ Fator %: deve mostrar 1.00")
    print("   ✅ Quantidade: valores + unidades (m, unid, h)")
    print("   ✅ Custo Unitário: valores em R$")
    print("   ✅ Custo Total: valores em R$")
    print("   ✅ Ação: botão de remover")
    print("   ✅ Total Geral: na última linha")
    
    print("\n📊 COMPONENTES ESPERADOS:")
    print("   - Tubo Quadrado 50 #6mm (s/ pintura)")
    print("   - Tubo Quadrado 50 #3mm (s/ pintura)")  
    print("   - Perfil Corrimão (s/ pintura)")
    print("   - Perfil Rodapé 200mm (s/ pintura)")
    print("   - SAPATA INOX 150#3MM")
    print("   - PARAF-SXT-M6X70-AI304")
    print("   - POR-SXT-M6-AI304")
    print("   - PARAF-AA-PN-PH-4,8X19-AI304")
    print("   - Mão de Obra - Processamento")
    print("   - Mão de Obra - Montagem")
    
    print("\n" + "=" * 50)
    print("🏁 TESTE PRONTO PARA EXECUÇÃO")
    print("Acesse o navegador e siga as instruções acima!")

if __name__ == "__main__":
    test_guarda_corpo_horizontal()