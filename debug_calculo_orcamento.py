#!/usr/bin/env python3
"""
DEBUG - Função de cálculo do Guarda Corpo no Orçamento
"""

import webbrowser
import time

def debug_calculo_orcamento():
    """Debug da função de cálculo do orçamento"""
    
    print("🔧 DEBUG: FUNÇÃO DE CÁLCULO GUARDA CORPO ORÇAMENTO")
    print("=" * 70)
    
    print("\n❌ ERRO IDENTIFICADO:")
    print("   Error: Tubo quadrado Tubo Quadrado 50 #6mm não encontrado no banco")
    
    print("\n🔍 PROBLEMA:")
    print("   ✅ Template atualizado com opções corretas")
    print("   ❌ Função de cálculo ainda usando lógica antiga")
    print("   ❌ Busca por produtos usando fetch('/api/produtos/')")
    print("   ❌ Filtros find() não funcionando corretamente")
    
    print("\n💡 SOLUÇÃO:")
    print("   ✅ Substituir por Promise.all + buscarProdutoPorDescricao")
    print("   ✅ Mesma lógica que funciona no MP")
    print("   ✅ Incluir todos os componentes (corrimão, rodapé, etc.)")
    
    print("\n🛠️  ALTERAÇÕES NECESSÁRIAS:")
    print("   1. Substituir fetch('/api/produtos/') por Promise.all([")
    print("      buscarProdutoPorDescricao(dados.tipo_tubo_quad),")
    print("      buscarProdutoPorDescricao(dados.tipo_omega),")
    print("      buscarProdutoPorDescricao(dados.tipo_sapata),")
    print("      buscarProdutoPorDescricao('Perfil Corrimão...'),")
    print("      buscarProdutoPorDescricao('Perfil Rodapé...'),")
    print("      buscarProdutoPorDescricao('PARAF-SXT-M6X70-AI304'),")
    print("      buscarProdutoPorDescricao('POR-SXT-M6-AI304'),")
    print("      buscarProdutoPorDescricao('PARAF-AA-PN-PH-4,8X19-AI304')")
    print("   ])")
    print("   ")
    print("   2. Usar mesma lógica de cálculo do MP:")
    print("      - quantidadeTuboQuadrado = (n_colunas/larg_modulo) * larg_modulo * altura")
    print("      - metrosOmega = n_br_intermediaria * larg_modulo")
    print("      - metrosCorrimao = larg_modulo")
    print("      - metrosRodape = larg_modulo")
    print("      - quantidadeParaf70 = (n_colunas/larg_modulo) * larg_modulo * 2")
    print("      - quantidadePorcas = mesma lógica do paraf70")
    print("      - quantidadeParafAA = (n_colunas/larg_modulo) * larg_modulo * (n_barras * 2 + 6)")
    print("   ")
    print("   3. Incluir todos os componentes na lista")
    print("   4. Valor fixo da porca: 41 centavos")
    
    print("\n🎯 ABRINDO ORÇAMENTO PARA TESTE...")
    webbrowser.open("http://127.0.0.1:8000/orcamento/1/")
    
    print("\n📝 TESTE APÓS CORREÇÃO:")
    print("   - Clique em 'Adicionar Produto'")
    print("   - Selecione 'Guarda Corpo Horizontal'")
    print("   - Nome: debug_correcao")
    print("   - Largura: 1")
    print("   - Altura: 1.1")
    print("   - Colunas: 1")
    print("   - Barras Intermed.: 1")
    print("   - Tubo Quadrado: Tubo Quadrado 50 #6mm")
    print("   - Tipo Ômega: PERFIL OMEGA 45X20MM")
    print("   - Sapata: SAPATA INOX 150#3MM")
    print("   - Clique em 'Calcular'")
    
    print("\n✅ RESULTADO ESPERADO:")
    print("   - Cálculo deve funcionar sem erros")
    print("   - Todos os componentes devem aparecer na tabela")
    print("   - Porca com valor de R$ 0,41")
    print("   - Lógica idêntica ao MP")
    
    print("\n" + "=" * 70)
    print("🔧 FUNÇÃO SERÁ CORRIGIDA PARA USAR MESMA LÓGICA DO MP!")

if __name__ == "__main__":
    debug_calculo_orcamento()