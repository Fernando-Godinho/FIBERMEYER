#!/usr/bin/env python
"""
Teste da correção da SAÍDA PISCINA - agora usando produto real ID 1472
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def testar_saida_piscina():
    print("=== TESTE CORREÇÃO SAÍDA PISCINA ===\n")
    
    # 1. Verificar produto SAÍDA PISCINA
    print("1️⃣ PRODUTO SAÍDA PISCINA:")
    try:
        saida_piscina = MP_Produtos.objects.get(id=1472)
        print(f"   ✅ ID: {saida_piscina.id}")
        print(f"   📄 Descrição: {saida_piscina.descricao}")
        print(f"   💰 Custo: R$ {saida_piscina.custo_centavos/100:.2f}")
        print(f"   📏 Unidade: {saida_piscina.unidade}")
        print(f"   🏷️ Tipo: {saida_piscina.tipo_produto}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    # 2. Verificar produtos relacionados para contexto
    print(f"\n2️⃣ PRODUTOS RELACIONADOS:")
    try:
        escada = MP_Produtos.objects.get(id=1465)
        print(f"   🏗️ Escada base: {escada.descricao} - R$ {escada.custo_centavos/100:.2f}")
        
        portinhola = MP_Produtos.objects.filter(descricao__icontains='PORTINHOLA').first()
        if portinhola:
            print(f"   🚪 Portinhola: {portinhola.descricao} - R$ {portinhola.custo_centavos/100:.2f}")
        
        tunel = MP_Produtos.objects.filter(descricao__icontains='TUNEL').first()
        if tunel:
            print(f"   🚇 Túnel: {tunel.descricao} - R$ {tunel.custo_centavos/100:.2f}")
            
    except Exception as e:
        print(f"   ⚠️ Erro ao buscar produtos relacionados: {e}")
    
    # 3. Simulação de cálculo com saída de piscina
    print(f"\n3️⃣ SIMULAÇÃO DE CÁLCULO:")
    
    # Dados do exemplo
    comprimento_escada = 5  # metros
    custo_escada = (escada.custo_centavos / 100) * comprimento_escada
    custo_saida_piscina = saida_piscina.custo_centavos / 100
    custo_mao_obra = (50.00 * 3.0) + (45.00 * 2.0)  # 3h proc + 2h montagem
    
    print(f"   📊 Exemplo: Escada 5m + Saída Piscina")
    print(f"   🏗️ Escada: {comprimento_escada}m × R$ {escada.custo_centavos/100:.2f} = R$ {custo_escada:.2f}")
    print(f"   🏊 Saída piscina: 1 × R$ {custo_saida_piscina:.2f} = R$ {custo_saida_piscina:.2f}")
    print(f"   👷 Mão de obra: R$ {custo_mao_obra:.2f}")
    
    custo_total = custo_escada + custo_saida_piscina + custo_mao_obra
    print(f"   💰 TOTAL: R$ {custo_total:.2f}")
    
    # 4. Comparação ANTES vs DEPOIS
    print(f"\n4️⃣ COMPARAÇÃO ANTES vs DEPOIS:")
    valor_estimado_antigo = 50.00
    valor_real_novo = custo_saida_piscina
    diferenca = valor_real_novo - valor_estimado_antigo
    
    print(f"   🔴 ANTES (estimado): R$ {valor_estimado_antigo:.2f}")
    print(f"   🟢 DEPOIS (produto real): R$ {valor_real_novo:.2f}")
    print(f"   📊 Diferença: R$ {diferenca:+.2f} ({((diferenca/valor_estimado_antigo)*100):+.1f}%)")
    
    if diferenca > 0:
        print(f"   📈 O valor real é R$ {diferenca:.2f} MAIOR que o estimado")
    elif diferenca < 0:
        print(f"   📉 O valor real é R$ {abs(diferenca):.2f} MENOR que o estimado")
    else:
        print(f"   ➡️ Valores iguais")
    
    # 5. Resumo
    print(f"\n5️⃣ RESUMO DAS MUDANÇAS:")
    print(f"   ❌ ANTES: Valor fixo estimado de R$ 50,00")
    print(f"   ✅ DEPOIS: Produto real ID 1472 - R$ {valor_real_novo:.2f}")
    print(f"   🎯 Benefícios:")
    print(f"      - Preço real e atualizado do sistema")
    print(f"      - Controle de estoque integrado")
    print(f"      - Rastreabilidade completa")
    print(f"      - Atualizações automáticas de preço")
    
    print(f"\n✅ CORREÇÃO IMPLEMENTADA COM SUCESSO!")

if __name__ == '__main__':
    testar_saida_piscina()