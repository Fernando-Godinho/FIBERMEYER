#!/usr/bin/env python
"""
Teste para verificar se o erro 'atualizarTabelaComponentesOrcamento is not defined' foi corrigido
"""
import subprocess
import time
import requests
import sys
import os

def iniciar_servidor():
    print("🚀 Iniciando servidor Django...")
    return subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "8002"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )

def main():
    print("🧪 TESTE: Verificação da função atualizarTabelaComponentesOrcamento")
    print("=" * 60)
    
    servidor = iniciar_servidor()
    
    try:
        # Aguardar servidor inicializar
        time.sleep(3)
        
        try:
            response = requests.get("http://localhost:8002/orcamento/", timeout=5)
            if response.status_code == 200:
                print("✅ Página de orçamento carregou com sucesso!")
                
                content = response.text
                
                # Verificar as correções
                problemas = []
                
                if "atualizarTabelaComponentesOrcamento" in content:
                    problemas.append("❌ Ainda há chamadas para 'atualizarTabelaComponentesOrcamento'")
                else:
                    print("✅ 'atualizarTabelaComponentesOrcamento' - REMOVIDO")
                
                if "mostrarComponentesCalculados" in content:
                    print("✅ 'mostrarComponentesCalculados' - PRESENTE")
                else:
                    problemas.append("❌ 'mostrarComponentesCalculados' não encontrada")
                
                # Contar ocorrências da função correta
                count_mostrar = content.count("mostrarComponentesCalculados(")
                if count_mostrar >= 2:
                    print(f"✅ {count_mostrar} chamadas para 'mostrarComponentesCalculados' encontradas")
                else:
                    problemas.append(f"❌ Apenas {count_mostrar} chamadas para 'mostrarComponentesCalculados'")
                
                if not problemas:
                    print("\n🎉 CORREÇÃO BEM-SUCEDIDA!")
                    print("   - Erro 'atualizarTabelaComponentesOrcamento is not defined' foi resolvido")
                    print("   - Função substituída por 'mostrarComponentesCalculados' existente")
                    print("   - Cálculo do Guarda Corpo deve funcionar sem erros de JavaScript")
                else:
                    print(f"\n⚠️  Ainda há {len(problemas)} problemas:")
                    for problema in problemas:
                        print(f"   {problema}")
                
            else:
                print(f"❌ Erro ao acessar página: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            
    finally:
        print("\n🛑 Parando servidor...")
        servidor.terminate()
        servidor.wait()

if __name__ == "__main__":
    main()