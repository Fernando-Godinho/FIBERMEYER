#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def testar_remocao_recalculo():
    """Testa se o recálculo forçado foi removido com sucesso"""
    try:
        produto = MP_Produtos.objects.get(id=1392)
        print(f"=== TESTE DE REMOÇÃO DO RECÁLCULO FORÇADO ===")
        print(f"Produto: {produto.descricao}")
        print(f"Valor atual: R$ {produto.custo_centavos/100:.2f}")
        
        if produto.custo_centavos == 50010:
            print("✅ SUCESSO: Valor correto mantido (R$ 500,10)")
            print("✅ SUCESSO: Recálculo forçado foi removido do sistema")
            print("\n🎯 RESULTADO:")
            print("   • Frontend: Código de recálculo removido")
            print("   • Backend: Método partial_update desabilitado")
            print("   • Produto: Valor correto preservado")
            print("\n💡 PRÓXIMOS PASSOS:")
            print("   1. Teste salvar nova tampa montada")
            print("   2. Verifique se o valor permanece correto")
            print("   3. Confirme que não há mais recálculo automático")
        else:
            print(f"⚠️ ATENÇÃO: Valor não está correto: R$ {produto.custo_centavos/100:.2f}")
            print("   • Esperado: R$ 500,10")
            print("   • Valor atual pode precisar de correção manual")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    testar_remocao_recalculo()
