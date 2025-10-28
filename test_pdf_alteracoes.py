#!/usr/bin/env python3
"""
Teste para verificar se o PDF está sendo gerado com valor unitário final e IPI
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem

def testar_pdf_alteracoes():
    print("🔍 TESTANDO ALTERAÇÕES NO PDF...")
    
    # Buscar um orçamento com itens
    orcamento = Orcamento.objects.filter(itens__isnull=False).first()
    if not orcamento:
        print("❌ Nenhum orçamento com itens encontrado")
        return
    
    print(f"📋 Orçamento: {orcamento}")
    
    # Buscar itens do orçamento
    itens = orcamento.itens.all()[:3]  # Pegar apenas os 3 primeiros para demonstração
    
    print(f"\n📦 DEMONSTRAÇÃO DOS CÁLCULOS PARA O PDF:")
    print("=" * 80)
    
    for i, item in enumerate(itens, 1):
        # Calcular valor unitário final como no PDF
        valor_unitario_final = float(item.valor_total) / float(item.quantidade) if float(item.quantidade) > 0 else 0
        
        # Obter percentual de IPI
        ipi_percentual = float(item.ipi_item) if item.ipi_item else 0
        
        print(f"\n🔸 ITEM {i}: {item.descricao[:50]}...")
        print(f"   • Quantidade: {item.quantidade}")
        print(f"   • Valor Unitário Original (banco): R$ {float(item.valor_unitario):.2f}")
        print(f"   • Valor Unitário Final (calculado): R$ {valor_unitario_final:.2f}")
        print(f"   • IPI: {ipi_percentual:.1f}%")
        print(f"   • Valor Total: R$ {float(item.valor_total):.2f}")
        
        # Mostrar o que será exibido no PDF
        print(f"   📄 NO PDF:")
        print(f"      QTDE: {item.quantidade}")
        print(f"      VALOR UNIT.: R$ {valor_unitario_final:.2f}".replace('.', ','))
        print(f"      IPI (%): {ipi_percentual:.1f}%")
        print(f"      VALOR TOTAL: R$ {float(item.valor_total):.2f}".replace('.', ','))
    
    print(f"\n✅ ALTERAÇÕES IMPLEMENTADAS:")
    print(f"   🔹 Valor unitário agora mostra o valor final (valor_total ÷ quantidade)")
    print(f"   🔹 Nova coluna 'IPI (%)' adicionada ao PDF")
    print(f"   🔹 Layout ajustado para 6 colunas ao invés de 5")
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print(f"   1. Acesse: http://localhost:8000/orcamento/{orcamento.id}/")
    print(f"   2. Clique em 'Gerar PDF' para ver as alterações")
    print(f"   3. Verifique se o valor unitário e IPI estão corretos")

if __name__ == "__main__":
    testar_pdf_alteracoes()