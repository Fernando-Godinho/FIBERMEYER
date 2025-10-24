#!/usr/bin/env python
"""
Demonstração prática da nova lógica do arco
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def demonstrar_nova_logica():
    print("🔄 NOVA LÓGICA DO ARCO - DEMONSTRAÇÃO PRÁTICA")
    print("=" * 60)
    
    # Buscar produtos
    escada = MP_Produtos.objects.get(id=1465)  # ESCADA DE MARINHEIRO
    arco = MP_Produtos.objects.filter(descricao__icontains='arco').first()  # Primeiro arco encontrado
    
    print(f"\n📋 PRODUTOS UTILIZADOS:")
    print(f"   🏗️ Escada: {escada.descricao} - R$ {escada.custo_centavos/100:.2f}/m")
    print(f"   🏛️ Arco: {arco.descricao} - R$ {arco.custo_centavos/100:.2f}/m")
    
    print(f"\n📐 REGRA: Quantidade de arco = Comprimento da escada - 2 metros")
    print(f"📝 FÓRMULA: arco_metros = max(0, escada_metros - 2)")
    
    # Exemplos práticos
    exemplos = [
        {"escada": 10, "descricao": "Exemplo do usuário"},
        {"escada": 5, "descricao": "Escada média"},
        {"escada": 3, "descricao": "Escada pequena"},
        {"escada": 2, "descricao": "Escada mínima (sem arco)"},
        {"escada": 1, "descricao": "Escada muito pequena (sem arco)"},
    ]
    
    print(f"\n🧮 EXEMPLOS DE CÁLCULO:")
    print(f"{'Escada':<8} {'Arco':<8} {'Custo Escada':<15} {'Custo Arco':<15} {'Total':<15} {'Descrição'}")
    print("-" * 80)
    
    for exemplo in exemplos:
        comprimento_escada = exemplo["escada"]
        comprimento_arco = max(0, comprimento_escada - 2)
        
        custo_escada = (escada.custo_centavos / 100) * comprimento_escada
        custo_arco = (arco.custo_centavos / 100) * comprimento_arco if comprimento_arco > 0 else 0
        custo_total = custo_escada + custo_arco
        
        arco_texto = f"{comprimento_arco}m" if comprimento_arco > 0 else "0m"
        
        print(f"{comprimento_escada}m      {arco_texto:<8} R$ {custo_escada:<12.2f} R$ {custo_arco:<12.2f} R$ {custo_total:<12.2f} {exemplo['descricao']}")
    
    # Destacar o exemplo específico do usuário
    print(f"\n🎯 EXEMPLO ESPECÍFICO (10m de escada):")
    print(f"   📏 Escada: 10 metros × R$ {escada.custo_centavos/100:.2f} = R$ {(escada.custo_centavos/100) * 10:.2f}")
    print(f"   🏛️ Arco: (10 - 2) = 8 metros × R$ {arco.custo_centavos/100:.2f} = R$ {(arco.custo_centavos/100) * 8:.2f}")
    print(f"   💰 Subtotal: R$ {((escada.custo_centavos/100) * 10) + ((arco.custo_centavos/100) * 8):.2f}")
    print(f"   👷 + Mão de obra: R$ 240,00 (estimativa)")
    print(f"   🏆 TOTAL: R$ {((escada.custo_centavos/100) * 10) + ((arco.custo_centavos/100) * 8) + 240:.2f}")
    
    print(f"\n✅ IMPLEMENTAÇÃO CONCLUÍDA!")
    print(f"   - Quantidade do arco agora segue a regra: escada - 2m")
    print(f"   - Custo é calculado automaticamente baseado na quantidade correta")
    print(f"   - Para escadas ≤ 2m, quantidade de arco = 0 (sem custo)")

if __name__ == '__main__':
    demonstrar_nova_logica()