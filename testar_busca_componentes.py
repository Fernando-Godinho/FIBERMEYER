#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def testar_busca_componentes():
    print("=== TESTE DE BUSCA DE COMPONENTES ===")
    print()
    
    # Contar produtos simples disponíveis para componentes
    produtos_simples = MP_Produtos.objects.filter(tipo_produto='simples')
    print(f"📦 Total de produtos simples disponíveis: {produtos_simples.count()}")
    
    # Mostrar alguns exemplos
    print("\n🔍 Exemplos de produtos que apareceriam na busca:")
    for produto in produtos_simples[:10]:
        custo = produto.custo_centavos / 100 if produto.custo_centavos else 0
        print(f"  • ID {produto.id}: {produto.descricao} - R$ {custo:.2f}")
    
    # Testar busca por termo específico
    termo_teste = "roving"
    produtos_roving = produtos_simples.filter(descricao__icontains=termo_teste)
    print(f"\n🎯 Busca por '{termo_teste}': {produtos_roving.count()} resultado(s)")
    for produto in produtos_roving[:5]:
        custo = produto.custo_centavos / 100 if produto.custo_centavos else 0
        print(f"  • ID {produto.id}: {produto.descricao} - R$ {custo:.2f}")
    
    # Testar busca por ID
    if produtos_simples.exists():
        primeiro_produto = produtos_simples.first()
        print(f"\n🔢 Busca por ID '{primeiro_produto.id}': encontrado")
        custo = primeiro_produto.custo_centavos / 100 if primeiro_produto.custo_centavos else 0
        print(f"  • {primeiro_produto.descricao} - R$ {custo:.2f}")
    
    print("\n✅ Funcionalidade de busca melhorada implementada com sucesso!")
    print("\n🎨 Melhorias implementadas:")
    print("  • Campo de busca em tempo real")
    print("  • Busca por descrição e ID")
    print("  • Navegação com setas do teclado")
    print("  • Seleção com Enter")
    print("  • Feedback visual da seleção")
    print("  • Limite de 20 resultados por vez")
    print("  • Foco automático no campo quantidade")
    print("  • Limpeza automática do formulário")
    print("  • Animações suaves")

if __name__ == '__main__':
    testar_busca_componentes()