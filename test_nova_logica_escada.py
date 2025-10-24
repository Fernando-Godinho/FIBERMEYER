#!/usr/bin/env python
"""
Teste da nova lógica simplificada da escada usando produto ID 1465
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def testar_nova_logica_escada():
    print("=== TESTE NOVA LÓGICA ESCADA SIMPLIFICADA ===\n")
    
    # 1. Verificar produto base ESCADA DE MARINHEIRO
    print("1️⃣ PRODUTO BASE:")
    try:
        escada_base = MP_Produtos.objects.get(id=1465)
        print(f"   ✅ {escada_base.descricao}")
        print(f"   💰 Custo unitário: R$ {escada_base.custo_centavos/100:.2f}")
        print(f"   📏 Unidade: {escada_base.unidade}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    # 2. Simular cálculo para diferentes comprimentos
    print(f"\n2️⃣ SIMULAÇÃO DE CUSTOS:")
    comprimentos = [2, 3, 5, 10]
    custo_unitario = escada_base.custo_centavos / 100
    
    for comprimento in comprimentos:
        custo_total = custo_unitario * comprimento
        print(f"   📐 {comprimento}m de escada: {comprimento} x R$ {custo_unitario:.2f} = R$ {custo_total:.2f}")
    
    # 3. Verificar produtos opcionais
    print(f"\n3️⃣ PRODUTOS OPCIONAIS:")
    produtos_opcionais = [
        ("PORTINHOLA", "PORTINHOLA"),
        ("TÚNEL", "TUNEL"),
        ("ARCO", "ARCO")
    ]
    
    for nome, busca in produtos_opcionais:
        produtos = MP_Produtos.objects.filter(descricao__icontains=busca)
        if produtos.exists():
            produto = produtos.first()
            print(f"   ✅ {nome}: {produto.descricao} - R$ {produto.custo_centavos/100:.2f}")
        else:
            print(f"   ❌ {nome}: Não encontrado")
    
    # 4. Exemplo completo
    print(f"\n4️⃣ EXEMPLO COMPLETO (5m de escada + opcionais):")
    comprimento_exemplo = 5
    custo_escada = custo_unitario * comprimento_exemplo
    custo_portinhola = 0
    custo_arco = 0
    custo_mao_obra = (50.00 * 3.0) + (45.00 * 2.0)  # 3h proc + 2h montagem
    
    # Buscar custos opcionais reais
    try:
        portinhola = MP_Produtos.objects.filter(descricao__icontains="PORTINHOLA").first()
        if portinhola:
            custo_portinhola = portinhola.custo_centavos / 100
    except:
        pass
        
    try:
        arco = MP_Produtos.objects.filter(descricao__icontains="ARCO").first()
        if arco:
            custo_arco = arco.custo_centavos / 100
    except:
        pass
    
    custo_total = custo_escada + custo_portinhola + custo_arco + custo_mao_obra
    
    print(f"   🏗️ Escada base: R$ {custo_escada:.2f}")
    print(f"   🚪 Portinhola: R$ {custo_portinhola:.2f}")
    print(f"   🏛️ Arco: R$ {custo_arco:.2f}")
    print(f"   👷 Mão de obra: R$ {custo_mao_obra:.2f}")
    print(f"   💰 TOTAL: R$ {custo_total:.2f}")
    
    print(f"\n✅ Nova lógica simplificada pronta para uso!")

if __name__ == '__main__':
    testar_nova_logica_escada()