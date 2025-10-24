#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def criar_produto_teste_perda():
    print("=== TESTE DIRETO: CRIAR PRODUTO COM PERDA ===")
    print()
    
    # Buscar alguns produtos simples para usar como componentes
    produtos_simples = MP_Produtos.objects.filter(tipo_produto='simples')[:2]
    
    if produtos_simples.count() < 2:
        print("❌ Erro: Não há produtos simples suficientes para o teste")
        return
    
    # Cálculo manual do custo com perda
    componente1 = produtos_simples[0]
    componente2 = produtos_simples[1]
    
    quantidade1 = 2
    quantidade2 = 1.5
    
    custo1_total = (componente1.custo_centavos / 100) * quantidade1
    custo2_total = (componente2.custo_centavos / 100) * quantidade2
    custo_base = custo1_total + custo2_total
    
    percentual_perda = 10.0  # 10%
    valor_perda = custo_base * (percentual_perda / 100)
    custo_total_final = custo_base + valor_perda
    custo_centavos = round(custo_total_final * 100)
    
    print("📊 CÁLCULO MANUAL:")
    print(f"├─ Componente 1: {componente1.descricao[:40]}...")
    print(f"│  └─ R$ {(componente1.custo_centavos/100):.2f} × {quantidade1} = R$ {custo1_total:.2f}")
    print(f"├─ Componente 2: {componente2.descricao[:40]}...")
    print(f"│  └─ R$ {(componente2.custo_centavos/100):.2f} × {quantidade2} = R$ {custo2_total:.2f}")
    print(f"├─ Custo Base: R$ {custo_base:.2f}")
    print(f"├─ Percentual Perda: {percentual_perda}%")
    print(f"├─ Valor Perda: R$ {valor_perda:.2f}")
    print(f"├─ Custo Total Final: R$ {custo_total_final:.2f}")
    print(f"└─ Custo em Centavos: {custo_centavos}")
    print()
    
    # Criar produto composto diretamente
    produto_composto = MP_Produtos.objects.create(
        descricao="TESTE PRODUTO COM PERDA 10%",
        custo_centavos=custo_centavos,
        tipo_produto='composto',
        unidade='UN',
        referencia='TESTE-PERDA-10'
    )
    
    print(f"✅ PRODUTO CRIADO: ID {produto_composto.id}")
    print(f"├─ Descrição: {produto_composto.descricao}")
    print(f"├─ Custo Salvo: R$ {(produto_composto.custo_centavos/100):.2f}")
    print(f"└─ Tipo: {produto_composto.tipo_produto}")
    print()
    
    # Criar componentes
    comp1 = ProdutoComponente.objects.create(
        produto_principal=produto_composto,
        produto_componente=componente1,
        quantidade=quantidade1
    )
    
    comp2 = ProdutoComponente.objects.create(
        produto_principal=produto_composto,
        produto_componente=componente2,
        quantidade=quantidade2
    )
    
    print("🔗 COMPONENTES CRIADOS:")
    print(f"├─ {comp1.produto_componente.descricao} × {comp1.quantidade}")
    print(f"└─ {comp2.produto_componente.descricao} × {comp2.quantidade}")
    print()
    
    # Verificar se o custo foi salvo corretamente
    produto_verificacao = MP_Produtos.objects.get(id=produto_composto.id)
    custo_salvo = produto_verificacao.custo_centavos / 100
    
    print("🔍 VERIFICAÇÃO:")
    print(f"├─ Custo Calculado: R$ {custo_total_final:.2f}")
    print(f"├─ Custo Salvo: R$ {custo_salvo:.2f}")
    diferenca = abs(custo_total_final - custo_salvo)
    print(f"├─ Diferença: R$ {diferenca:.4f}")
    
    if diferenca < 0.01:
        print("└─ ✅ SALVAMENTO CORRETO!")
    else:
        print("└─ ❌ SALVAMENTO INCORRETO!")
    
    print()
    print("🎯 CONCLUSÃO:")
    print("Se o teste mostra 'SALVAMENTO CORRETO', então o problema")
    print("está no JavaScript que não está calculando ou enviando")
    print("o valor correto para a API.")
    
    return produto_composto.id

if __name__ == '__main__':
    produto_id = criar_produto_teste_perda()
    print(f"\n🔗 Produto criado com ID: {produto_id}")
    print("Agora teste criar um produto pela interface e compare os custos!")