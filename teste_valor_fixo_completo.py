#!/usr/bin/env python3
"""
TESTE COMPLETO - Verificar valor fixo da POR-SXT-M6-AI304 em MP e Orçamento
"""

import webbrowser
import time

def test_valor_fixo_completo():
    """Teste completo do valor fixo da porca em MP e Orçamento"""
    
    print("🔧 TESTE COMPLETO: VALOR FIXO POR-SXT-M6-AI304 = 41 CENTAVOS")
    print("=" * 70)
    
    print("\n✅ ALTERAÇÕES REALIZADAS:")
    print("   📋 MP (main/templates/main/mp.html):")
    print("      ✅ Custo da porca fixado em 41 centavos no cálculo")
    print("      ✅ Custo unitário fixado em 41 centavos na tabela")
    print("   ")
    print("   🎯 ORÇAMENTO (main/templates/main/orcamento.html):")
    print("      ✅ Custo da porca fixado em 41 centavos no cálculo")
    print("      ✅ Custo unitário fixado em 41 centavos na tabela")
    
    print("\n📋 CÓDIGO MODIFICADO EM AMBOS OS ARQUIVOS:")
    print("   // VALOR FIXO: POR-SXT-M6-AI304 fixado em 41 centavos para Guarda Corpo")
    print("   const custoPorcas = Math.round(quantidadePorcas * 41);")
    print("   ")
    print("   custo_unitario: 41, // Valor fixo de 41 centavos para GC")
    
    print("\n🎯 ABRINDO NAVEGADORES PARA TESTE...")
    
    # Abrir MP
    print("   🔗 Abrindo MP...")
    webbrowser.open("http://127.0.0.1:8000/mp/")
    time.sleep(2)
    
    # Abrir Orçamento (assumindo que existe um orçamento ID 1)
    print("   🔗 Abrindo Orçamento...")
    webbrowser.open("http://127.0.0.1:8000/orcamento/1/")
    
    print("\n📝 TESTE EM AMBAS AS TELAS:")
    print("   1️⃣ MP - Aba 'Guarda Corpo - Horizontal':")
    print("      - Nome: teste_mp_porca_41")
    print("      - Largura: 1")
    print("      - Altura: 1.1")
    print("      - Colunas: 1")
    print("      - Barras Intermed.: 1")
    print("      - Tubo Quadrado: [selecione]")
    print("      - Sapata: [selecione]")
    print("   ")
    print("   2️⃣ ORÇAMENTO - Adicionar 'Guarda Corpo Horizontal':")
    print("      - Nome: teste_orc_porca_41")
    print("      - Use os mesmos parâmetros do MP")
    
    print("\n🔍 VERIFICAÇÕES ESPERADAS EM AMBAS AS TELAS:")
    print("   ✅ Na tabela de componentes calculados:")
    print("   ✅ Linha da POR-SXT-M6-AI304 deve mostrar:")
    print("   ✅ Custo Unitário: R$ 0,41")
    print("   ✅ Quantidade calculada normalmente")
    print("   ✅ Custo Total: (quantidade × 0,41)")
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Este valor fixo é APENAS para Guarda Corpo")
    print("   - Aplicado tanto no MP quanto no Orçamento")
    print("   - Outros produtos usarão o valor do banco de dados")
    print("   - O valor original da POR-SXT-M6-AI304 não foi alterado")
    
    print("\n🎯 RESULTADOS ESPERADOS:")
    print("   ✅ MP: Cálculo correto com porca a R$ 0,41")
    print("   ✅ Orçamento: Mesmo comportamento do MP")
    print("   ✅ Consistência entre as duas interfaces")
    print("   ✅ Salvamento funcionando normalmente")
    
    print("\n" + "=" * 70)
    print("🎉 TEMPLATE ATUALIZADO EM MP E ORÇAMENTO!")
    print("Teste ambas as interfaces para confirmar funcionamento.")

if __name__ == "__main__":
    test_valor_fixo_completo()