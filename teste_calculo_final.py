#!/usr/bin/env python3
"""
Teste simples para validar a funcionalidade atual
"""

import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem
from decimal import Decimal

def simular_calculo_item():
    """Simula o cálculo que deve acontecer quando o lucro é alterado"""
    print("=" * 60)
    print("🧮 SIMULAÇÃO DO CÁLCULO DE ITEM")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}\n")
    
    # Buscar item do orçamento 27
    orcamento = Orcamento.objects.filter(id=27).first()
    if not orcamento:
        print("❌ Orçamento 27 não encontrado")
        return
    
    item = orcamento.itens.filter(id=49).first()  # CHUMBADOR
    if not item:
        print("❌ Item 49 não encontrado")
        return
    
    print(f"📋 DADOS DO ITEM:")
    print(f"   ID: {item.id}")
    print(f"   Descrição: {item.descricao}")
    print(f"   Valor Unitário: R$ {item.valor_unitario}")
    print(f"   Quantidade: {item.quantidade}")
    print(f"   Lucro atual: {item.desconto_item}%")
    print(f"   Impostos: {item.imposto_item}%")
    print(f"   IPI: {item.ipi_item}%")
    print(f"   Valor Total atual: R$ {item.valor_total}")
    print()
    
    # Simular mudança para 45% de lucro
    novo_lucro = Decimal('45.0')
    print(f"🔧 SIMULANDO MUDANÇA PARA {novo_lucro}% DE LUCRO:")
    
    # Dados para cálculo
    custo = float(item.valor_unitario)
    quantidade = float(item.quantidade)
    impostos = float(item.imposto_item)
    lucro = float(novo_lucro)
    ipi = float(item.ipi_item)
    
    # Cálculo dos impostos do orçamento
    impostos_orcamento = 33.93  # Valor do exemplo do usuário
    
    print(f"   📊 Dados para cálculo:")
    print(f"      Custo unitário: R$ {custo}")
    print(f"      Quantidade: {quantidade}")
    print(f"      Impostos totais: {impostos_orcamento}%")
    print(f"      Lucro: {lucro}%")
    print(f"      IPI: {ipi}%")
    print()
    
    # Aplicar nova fórmula sequencial
    print(f"   🔢 Aplicando nova fórmula sequencial:")
    
    # 1. Valor Base
    valor_base = custo * quantidade
    print(f"   1. Valor Base: R$ {custo} × {quantidade} = R$ {valor_base:.2f}")
    
    # 2. + Impostos
    valor_com_impostos = valor_base * (1 + impostos_orcamento / 100)
    print(f"   2. + Impostos ({impostos_orcamento}%): R$ {valor_com_impostos:.2f}")
    
    # 3. + Lucro
    valor_com_lucro = valor_com_impostos * (1 + lucro / 100)
    print(f"   3. + Lucro ({lucro}%): R$ {valor_com_lucro:.2f}")
    
    # 4. + IPI
    valor_final = valor_com_lucro * (1 + ipi / 100)
    print(f"   4. + IPI ({ipi}%): R$ {valor_final:.2f}")
    
    # Valor unitário final
    valor_unitario_final = valor_final / quantidade
    print(f"   📈 Valor Unitário Final: R$ {valor_unitario_final:.2f}")
    print()
    
    # Agora testar salvando o item com novo lucro
    print(f"💾 TESTANDO SAVE DO MODELO:")
    item_teste = OrcamentoItem.objects.get(id=item.id)
    valor_anterior = item_teste.valor_total
    lucro_anterior = item_teste.desconto_item
    
    # Alterar lucro e salvar
    item_teste.desconto_item = novo_lucro
    item_teste.save()
    
    print(f"   Lucro: {lucro_anterior}% → {item_teste.desconto_item}%")
    print(f"   Valor: R$ {valor_anterior} → R$ {item_teste.valor_total}")
    print(f"   Diferença: R$ {float(item_teste.valor_total) - float(valor_anterior):.2f}")
    
    # Verificar se o valor calculado manualmente confere
    diferenca = abs(float(item_teste.valor_total) - valor_final)
    if diferenca < 0.01:
        print(f"   ✅ CORRETO! Modelo calcula igual ao manual (diferença: R$ {diferenca:.4f})")
    else:
        print(f"   ❌ DIVERGÊNCIA! Diferença: R$ {diferenca:.2f}")
        print(f"      Manual: R$ {valor_final:.2f}")
        print(f"      Modelo: R$ {item_teste.valor_total}")
    
    # Restaurar valor original
    item_teste.desconto_item = lucro_anterior
    item_teste.save()
    print(f"   🔄 Valor restaurado para: R$ {item_teste.valor_total}")

def verificar_logs_servidor():
    """Mostra instruções para verificar logs do servidor"""
    print("\n" + "=" * 60)
    print("📊 PRÓXIMOS PASSOS PARA DEBUG")
    print("=" * 60)
    
    print("1. ✅ Nova fórmula implementada no modelo Python")
    print("2. ✅ Nova fórmula implementada no JavaScript")
    print("3. ✅ Handler AJAX para lucro adicionado")
    print("4. ✅ Tratamento de erros JSON melhorado")
    print()
    
    print("🔍 Para testar na interface web:")
    print("   1. Abra: http://localhost:8000/orcamento/27/")
    print("   2. Altere o lucro do item CHUMBADOR para 45%")
    print("   3. Verifique no console do navegador se há erros")
    print("   4. O valor deve ir de R$ 4.15 → R$ 8.06 unitário")
    print()
    
    print("📋 Cálculo esperado para CHUMBADOR:")
    print("   Custo: R$ 4.15 × 250 = R$ 1.037,50")
    print("   + Impostos (33.93%): R$ 1.389,52")
    print("   + Lucro (45%): R$ 2.014,81")
    print("   + IPI (0%): R$ 2.014,81")
    print("   = Unitário final: R$ 8.06")
    print()
    
    print("🐛 Se ainda houver erro 500:")
    print("   - Verifique logs do terminal do servidor")
    print("   - Confirme que ajax_update_lucro está sendo enviado")
    print("   - Verifique se CSRF token está correto")

if __name__ == "__main__":
    simular_calculo_item()
    verificar_logs_servidor()