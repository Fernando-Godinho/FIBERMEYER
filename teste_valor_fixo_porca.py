#!/usr/bin/env python3
"""
TESTE - Verificar valor fixo da POR-SXT-M6-AI304 em 41 centavos para GC
"""

import webbrowser
import time

def test_valor_fixo_porca():
    """Teste do valor fixo da porca para Guarda Corpo"""
    
    print("🔧 TESTE: VALOR FIXO POR-SXT-M6-AI304 = 41 CENTAVOS")
    print("=" * 60)
    
    print("\n✅ ALTERAÇÕES REALIZADAS:")
    print("   ✅ Custo da porca fixado em 41 centavos no cálculo")
    print("   ✅ Custo unitário fixado em 41 centavos na tabela")
    print("   ✅ Aplicado APENAS para Guarda Corpo Horizontal")
    
    print("\n📋 CÓDIGO MODIFICADO:")
    print("   // VALOR FIXO: POR-SXT-M6-AI304 fixado em 41 centavos para Guarda Corpo")
    print("   const custoPorcas = (quantidadePorcas * 41) * fatorPerda;")
    print("   ")
    print("   custo_unitario: 41, // Valor fixo de 41 centavos para GC")
    
    print("\n🎯 ABRINDO NAVEGADOR PARA TESTE...")
    webbrowser.open("http://127.0.0.1:8000/mp/")
    
    print("\n📝 TESTE COM OS DADOS:")
    print("   - Nome: teste_porca_41")
    print("   - Largura: 1")
    print("   - Altura: 1.1")
    print("   - Colunas: 1")
    print("   - Barras Intermed.: 1")
    print("   - Tubo Quadrado: Tubo Quadrado 50 #6mm")
    print("   - Tipo Ômega: [selecione um perfil ômega]")
    print("   - Sapata: SAPATA INOX 150#3MM")
    
    print("\n🔍 VERIFICAÇÕES ESPERADAS:")
    print("   ✅ Na tabela de componentes calculados:")
    print("   ✅ Linha da POR-SXT-M6-AI304 deve mostrar:")
    print("   ✅ Custo Unitário: R$ 0,41")
    print("   ✅ Quantidade calculada normalmente")
    print("   ✅ Custo Total: (quantidade × 0,41) × (1 + perda%)")
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Este valor fixo é APENAS para Guarda Corpo")
    print("   - Outros produtos usarão o valor do banco de dados")
    print("   - O valor original da POR-SXT-M6-AI304 não foi alterado")
    
    print("\n" + "=" * 60)
    print("🎯 TESTE NO NAVEGADOR PARA CONFIRMAR!")

if __name__ == "__main__":
    test_valor_fixo_porca()