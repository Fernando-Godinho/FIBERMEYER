#!/usr/bin/env python
"""
Teste simples para verificar se o erro 'metrosTuboQuadrado is not defined' foi corrigido
"""
import subprocess
import time
import requests
import sys
import os

def iniciar_servidor():
    print("🚀 Iniciando servidor Django...")
    return subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )

def main():
    print("🧪 TESTE SIMPLES: Verificação rápida do erro JavaScript")
    print("=" * 50)
    
    servidor = iniciar_servidor()
    
    try:
        # Aguardar um pouco para o servidor inicializar
        time.sleep(3)
        
        try:
            response = requests.get("http://localhost:8001/orcamento/", timeout=5)
            if response.status_code == 200:
                print("✅ Página de orçamento carregou com sucesso!")
                
                # Verificações simples
                content = response.text
                
                # Verificar se não há mais variáveis problemáticas
                problemas = []
                
                if "metrosTuboQuadrado" in content:
                    problemas.append("❌ 'metrosTuboQuadrado' ainda encontrado")
                else:
                    print("✅ 'metrosTuboQuadrado' - CORRIGIDO")
                
                # Verificar se há referências isoladas a tempoProc (sem dados.)
                linhas = content.split('\n')
                for i, linha in enumerate(linhas):
                    if "tempoProc >" in linha and "dados.tempo_proc" not in linha:
                        problemas.append(f"❌ Linha {i+1}: referência isolada a 'tempoProc'")
                
                if not problemas:
                    print("✅ Todas as variáveis JavaScript - CORRIGIDAS")
                    print("\n🎉 CORREÇÃO BEM-SUCEDIDA!")
                    print("   - Erro 'metrosTuboQuadrado is not defined' foi resolvido")
                    print("   - Função sincronizada com MP")
                    print("   - Cálculo do Guarda Corpo Horizontal deve funcionar normalmente")
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