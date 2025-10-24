#!/usr/bin/env python
"""
Teste completo do sistema - Produto 1469 e estrutura de componentes
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def testar_sistema_completo():
    print("=== TESTE COMPLETO DO SISTEMA ===\n")
    
    # 1. Verificar produto 1469
    print("1️⃣ TESTE PRODUTO 1469:")
    try:
        produto = MP_Produtos.objects.get(id=1469)
        print(f"   ✅ Produto encontrado: {produto.descricao}")
        print(f"   💰 Custo: R$ {produto.custo_centavos/100:.2f}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 2. Verificar outros arcos para contexto
    print(f"\n2️⃣ OUTROS ARCOS DISPONÍVEIS:")
    arcos = MP_Produtos.objects.filter(descricao__icontains='arco')
    for arco in arcos:
        print(f"   ID {arco.id}: {arco.descricao} - R$ {arco.custo_centavos/100:.2f}")
    
    # 3. Verificar produtos para escada 
    print(f"\n3️⃣ PRODUTOS PARA ESCADA:")
    produtos_escada = [
        "Tubo Quadrado 50 #4mm",
        "Tubo Redondo 32 #3mm", 
        "PARAF-AA-PN-PH-4,8X19-AI304",
        "CANTONEIRA DE FIXACAO LATERAL", 
        "SAPATA BI-PARTIDA",
        "PARAF-SXT-M6X60-AI304",
        "POR-SXT-M6-AI304",
        "PORTINHOLA",
        "TUNEL"
    ]
    
    for descricao_busca in produtos_escada:
        produtos = MP_Produtos.objects.filter(descricao__icontains=descricao_busca)
        if produtos.exists():
            produto = produtos.first()
            print(f"   ✅ {descricao_busca}: ID {produto.id} - {produto.descricao}")
        else:
            print(f"   ❌ {descricao_busca}: Não encontrado")
    
    print(f"\n4️⃣ RESUMO:")
    total_produtos = MP_Produtos.objects.count()
    print(f"   📊 Total de produtos no sistema: {total_produtos}")
    print(f"   🏗️ Sistema pronto para testes!")

if __name__ == '__main__':
    testar_sistema_completo()