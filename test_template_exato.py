#!/usr/bin/env python3
"""
Script para testar o template EXATO da versão do commit
"""

import webbrowser
import time

def test_template_exato():
    """Testa se o template está igual à versão do commit"""
    
    print("🧪 TESTANDO TEMPLATE EXATO DA VERSÃO DO COMMIT")
    print("=" * 60)
    
    print("\n📋 VERIFICAÇÕES OBRIGATÓRIAS:")
    print("✅ Campo 'Tipo de Ômega' deve estar presente")
    print("✅ Tabela deve ter EXATAMENTE estas colunas:")
    print("   1. Material/Serviço")
    print("   2. Descrição do Produto") 
    print("   3. Fator %")
    print("   4. Quantidade")
    print("   5. Custo Unitário")
    print("   6. Custo Total")
    print("   7. Ação")
    
    print("\n🔧 ESTRUTURA ESPERADA DA TABELA:")
    print("   Material/Serviço | Descrição | Fator % | Qtd + Unid | Custo Unit | Custo Total | Ação")
    print("   Tubo Quadrado   | Tubo Quad | 1.00    | 1.10 m     | R$ 25.64  | R$ 28.20   | 🗑️")
    print("   ...             | ...       | 1.00    | ...        | ...       | ...        | 🗑️")
    print("   TOTAL GERAL     |           |         |            |           | R$ 185.52  |")
    
    print("\n📝 DADOS DE TESTE:")
    print("   - Nome: Guarda Corpo Teste")
    print("   - Largura: 2.0") 
    print("   - Altura: 1.1")
    print("   - Nº Colunas: 1")
    print("   - Nº Brr. Intermed.: 1")
    print("   - Tipo Tubo Quadrado: Tubo Quadrado 50 #6mm")
    print("   - Tipo Ômega: PERFIL OMEGA 45X20MM")
    print("   - Tipo Sapata: SAPATA INOX 150#3MM")
    
    print("\n🎯 ABRINDO NAVEGADOR...")
    webbrowser.open("http://127.0.0.1:8000/mp/")
    
    print("\n" + "=" * 60)
    print("🏁 EXECUTE O TESTE NO NAVEGADOR!")
    print("Verifique se TUDO está igual à versão do commit")

if __name__ == "__main__":
    test_template_exato()