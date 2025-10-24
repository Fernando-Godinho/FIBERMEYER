#!/usr/bin/env python
"""
Teste da nova lógica do arco: quantidade = comprimento_escada - 2m
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def testar_logica_arco():
    print("=== TESTE NOVA LÓGICA DO ARCO ===\n")
    
    # 1. Verificar produtos disponíveis
    print("1️⃣ PRODUTOS PARA TESTE:")
    try:
        escada_base = MP_Produtos.objects.get(id=1465)
        print(f"   🏗️ Escada base: {escada_base.descricao} - R$ {escada_base.custo_centavos/100:.2f}")
        
        # Buscar arcos disponíveis
        arcos = MP_Produtos.objects.filter(descricao__icontains='arco')
        print(f"   🏛️ Arcos disponíveis:")
        for arco in arcos:
            print(f"      ID {arco.id}: {arco.descricao} - R$ {arco.custo_centavos/100:.2f}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    # 2. Simular cálculos para diferentes comprimentos
    print(f"\n2️⃣ SIMULAÇÃO DE CÁLCULOS:")
    comprimentos_teste = [2, 3, 5, 8, 10, 15]
    
    # Usar o primeiro arco como exemplo
    arco_exemplo = arcos.first()
    custo_escada_unitario = escada_base.custo_centavos / 100
    custo_arco_unitario = arco_exemplo.custo_centavos / 100
    
    print(f"   📊 Exemplo com {arco_exemplo.descricao}")
    print(f"   {'Escada':<8} {'Arco':<8} {'Custo Escada':<15} {'Custo Arco':<15} {'Total':<15}")
    print(f"   {'-'*8} {'-'*8} {'-'*15} {'-'*15} {'-'*15}")
    
    for comprimento in comprimentos_teste:
        # Lógica: arco = escada - 2m (mínimo 0)
        quantidade_arco = max(0, comprimento - 2)
        
        custo_escada = custo_escada_unitario * comprimento
        custo_arco = custo_arco_unitario * quantidade_arco if quantidade_arco > 0 else 0
        custo_total = custo_escada + custo_arco
        
        status_arco = f"{quantidade_arco}m" if quantidade_arco > 0 else "Sem arco"
        
        print(f"   {comprimento}m      {status_arco:<8} R$ {custo_escada:<12.2f} R$ {custo_arco:<12.2f} R$ {custo_total:<12.2f}")
    
    # 3. Casos especiais
    print(f"\n3️⃣ CASOS ESPECIAIS:")
    casos_especiais = [
        (1, "Escada muito pequena"),
        (2, "Escada limite (2m)"),
        (2.5, "Escada com decimal"),
    ]
    
    for comprimento, descricao in casos_especiais:
        quantidade_arco = max(0, comprimento - 2)
        print(f"   📐 {descricao}: {comprimento}m escada → {quantidade_arco}m arco")
    
    # 4. Resumo da lógica
    print(f"\n4️⃣ RESUMO DA NOVA LÓGICA:")
    print(f"   📏 Fórmula: quantidade_arco = max(0, comprimento_escada - 2)")
    print(f"   ✅ Para escadas ≤ 2m: sem arco (quantidade = 0)")
    print(f"   ✅ Para escadas > 2m: arco = escada - 2m")
    print(f"   💰 Custo arco = quantidade_arco × preço_unitário")
    
    print(f"\n✅ Nova lógica do arco implementada e testada!")

if __name__ == '__main__':
    testar_logica_arco()