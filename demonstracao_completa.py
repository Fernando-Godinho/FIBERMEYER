#!/usr/bin/env python
"""
Demonstração completa: Escada com todos os opcionais usando produtos reais
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def demonstracao_completa():
    print("🎯 DEMONSTRAÇÃO COMPLETA - ESCADA COM TODOS OS OPCIONAIS")
    print("=" * 65)
    
    # Buscar todos os produtos
    try:
        escada = MP_Produtos.objects.get(id=1465)
        saida_piscina = MP_Produtos.objects.get(id=1472)
        portinhola = MP_Produtos.objects.filter(descricao__icontains='PORTINHOLA').first()
        tunel = MP_Produtos.objects.filter(descricao__icontains='TUNEL').first()
        arco = MP_Produtos.objects.filter(descricao__icontains='arco').first()
    except Exception as e:
        print(f"❌ Erro ao buscar produtos: {e}")
        return
    
    print(f"\n📋 PRODUTOS UTILIZADOS:")
    print(f"   🏗️ {escada.descricao} - R$ {escada.custo_centavos/100:.2f}/m")
    print(f"   🏊 {saida_piscina.descricao} - R$ {saida_piscina.custo_centavos/100:.2f}/un")
    print(f"   🚪 {portinhola.descricao} - R$ {portinhola.custo_centavos/100:.2f}/un")
    print(f"   🚇 {tunel.descricao} - R$ {tunel.custo_centavos/100:.2f}/un")
    print(f"   🏛️ {arco.descricao} - R$ {arco.custo_centavos/100:.2f}/m")
    
    # Exemplo: Escada de 10m com todos os opcionais
    comprimento_escada = 10
    quantidade_arco = max(0, comprimento_escada - 2)  # 8m de arco
    
    print(f"\n🧮 CÁLCULO COMPLETO (Escada {comprimento_escada}m + todos opcionais):")
    print(f"{'Item':<25} {'Qtd':<8} {'Unit.':<12} {'Total':<12}")
    print("-" * 60)
    
    # Cálculos
    custo_escada = (escada.custo_centavos / 100) * comprimento_escada
    custo_saida = saida_piscina.custo_centavos / 100
    custo_portinhola = portinhola.custo_centavos / 100
    custo_tunel = tunel.custo_centavos / 100
    custo_arco = (arco.custo_centavos / 100) * quantidade_arco
    custo_mao_obra = (50.00 * 3.0) + (45.00 * 2.0)
    
    print(f"{'Escada base':<25} {comprimento_escada}m      R$ {escada.custo_centavos/100:<9.2f} R$ {custo_escada:<9.2f}")
    print(f"{'Saída piscina':<25} {'1 un':<8} R$ {saida_piscina.custo_centavos/100:<9.2f} R$ {custo_saida:<9.2f}")
    print(f"{'Portinhola':<25} {'1 un':<8} R$ {portinhola.custo_centavos/100:<9.2f} R$ {custo_portinhola:<9.2f}")
    print(f"{'Túnel 2000mm':<25} {'1 un':<8} R$ {tunel.custo_centavos/100:<9.2f} R$ {custo_tunel:<9.2f}")
    print(f"{'Arco guarda corpo':<25} {quantidade_arco}m      R$ {arco.custo_centavos/100:<9.2f} R$ {custo_arco:<9.2f}")
    print(f"{'Mão de obra':<25} {'3+2h':<8} R$ {'80.00':<9} R$ {custo_mao_obra:<9.2f}")
    
    custo_total = custo_escada + custo_saida + custo_portinhola + custo_tunel + custo_arco + custo_mao_obra
    
    print("-" * 60)
    print(f"{'TOTAL':<25} {'':<8} {'':<12} R$ {custo_total:<9.2f}")
    
    # Comparação com valores antigos (estimados)
    print(f"\n📊 COMPARAÇÃO COM VALORES ANTERIORES (ESTIMADOS):")
    
    # Valores antigos estimados
    saida_antigo = 50.00
    arco_antigo = arco.custo_centavos / 100  # Antes era quantidade fixa = 1
    
    custo_total_antigo = custo_escada + saida_antigo + custo_portinhola + custo_tunel + arco_antigo + custo_mao_obra
    
    print(f"   🔴 Saída piscina (estimado): R$ {saida_antigo:.2f}")
    print(f"   🟢 Saída piscina (real): R$ {custo_saida:.2f}")
    print(f"   📊 Diferença saída: R$ {custo_saida - saida_antigo:+.2f}")
    print()
    print(f"   🔴 Arco (1 unidade): R$ {arco_antigo:.2f}")
    print(f"   🟢 Arco ({quantidade_arco}m): R$ {custo_arco:.2f}")
    print(f"   📊 Diferença arco: R$ {custo_arco - arco_antigo:+.2f}")
    print()
    print(f"   🔴 TOTAL ANTIGO: R$ {custo_total_antigo:.2f}")
    print(f"   🟢 TOTAL NOVO: R$ {custo_total:.2f}")
    print(f"   📊 DIFERENÇA TOTAL: R$ {custo_total - custo_total_antigo:+.2f}")
    
    # Resumo das melhorias
    print(f"\n✅ MELHORIAS IMPLEMENTADAS:")
    print(f"   1. ✅ Saída piscina: Produto real (ID 1472) em vez de estimativa")
    print(f"   2. ✅ Arco: Quantidade correta (escada - 2m) em vez de 1 unidade")
    print(f"   3. ✅ Escada: Produto base simplificado (ID 1465)")
    print(f"   4. ✅ Custos: Sempre atualizados da base de dados")
    print(f"   5. ✅ Rastreabilidade: Todos os componentes identificados")
    
    print(f"\n🎯 SISTEMA OTIMIZADO E PRECISO! 🚀")

if __name__ == '__main__':
    demonstracao_completa()