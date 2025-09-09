#!/usr/bin/env python
"""
Script para verificar produtos de roving, manta e véu
"""
import os
import sys
import django

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def check_products():
    print("=== VERIFICANDO PRODUTOS ROVING, MANTA E VÉU ===\n")
    
    # Buscar produtos roving
    produtos_roving = MP_Produtos.objects.filter(descricao__icontains='roving')
    print("PRODUTOS ROVING:")
    if produtos_roving.exists():
        for p in produtos_roving:
            print(f"  ID: {p.id}, Desc: {p.descricao}, Custo: R$ {p.custo_centavos/100:.2f}")
    else:
        print("  Nenhum produto encontrado")
    
    # Buscar produtos manta  
    produtos_manta = MP_Produtos.objects.filter(descricao__icontains='manta')
    print("\nPRODUTOS MANTA:")
    if produtos_manta.exists():
        for p in produtos_manta:
            print(f"  ID: {p.id}, Desc: {p.descricao}, Custo: R$ {p.custo_centavos/100:.2f}")
    else:
        print("  Nenhum produto encontrado")
    
    # Buscar produtos véu
    produtos_veu = MP_Produtos.objects.filter(descricao__icontains='véu')
    print("\nPRODUTOS VÉU:")
    if produtos_veu.exists():
        for p in produtos_veu:
            print(f"  ID: {p.id}, Desc: {p.descricao}, Custo: R$ {p.custo_centavos/100:.2f}")
    else:
        print("  Nenhum produto encontrado")
    
    # Buscar produtos veu (sem acento)
    produtos_veu2 = MP_Produtos.objects.filter(descricao__icontains='veu')
    print("\nPRODUTOS VEU (sem acento):")
    if produtos_veu2.exists():
        for p in produtos_veu2:
            print(f"  ID: {p.id}, Desc: {p.descricao}, Custo: R$ {p.custo_centavos/100:.2f}")
    else:
        print("  Nenhum produto encontrado")

if __name__ == '__main__':
    check_products()
