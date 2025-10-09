#!/usr/bin/env python3
"""
Teste para verificar se a tabela de componentes está exibindo corretamente
"""

import requests
import json

def test_tabela_componentes():
    """Testa a exibição da tabela de componentes após cálculo"""
    
    print("🧪 TESTANDO TABELA DE COMPONENTES")
    print("=" * 50)
    
    # URL base
    base_url = "http://127.0.0.1:8000"
    
    try:
        # 1. Testar acesso à página MP
        print("\n1. Testando acesso à página MP...")
        response = requests.get(f"{base_url}/mp/")
        
        if response.status_code == 200:
            print("✅ Página MP acessível")
            
            # Verificar se contém os elementos da tabela
            content = response.text
            
            # Verificar cabeçalhos da tabela
            headers_esperados = [
                "Material/Serviço",
                "Descrição do Produto", 
                "Fator %",
                "Quantidade",
                "Custo Unitário",
                "Custo Total",
                "Ação"
            ]
            
            print("\n2. Verificando cabeçalhos da tabela...")
            for header in headers_esperados:
                if header in content:
                    print(f"✅ Cabeçalho '{header}' encontrado")
                else:
                    print(f"❌ Cabeçalho '{header}' NÃO encontrado")
            
            # Verificar se contém a tabela de componentes
            if "componentesCalculadosTable" in content:
                print("✅ Tabela de componentes encontrada")
            else:
                print("❌ Tabela de componentes NÃO encontrada")
                
            # Verificar se contém a função de mostrar componentes
            if "mostrarComponentesCalculados" in content:
                print("✅ Função mostrarComponentesCalculados encontrada")
            else:
                print("❌ Função mostrarComponentesCalculados NÃO encontrada")
                
        else:
            print(f"❌ Erro ao acessar página MP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando em localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TESTE CONCLUÍDO")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Acesse http://127.0.0.1:8000/mp/")
    print("2. Faça um cálculo de Guarda Corpo")
    print("3. Verifique se a tabela mostra:")
    print("   - Nome do material na coluna 1")
    print("   - Descrição na coluna 2") 
    print("   - Fator 1.00 na coluna 3")
    print("   - Quantidade + unidade na coluna 4")
    print("   - Custo unitário na coluna 5")
    print("   - Custo total na coluna 6")
    print("   - Botão remover na coluna 7")

if __name__ == "__main__":
    test_tabela_componentes()