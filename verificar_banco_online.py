#!/usr/bin/env python
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, Imposto, MaoObra, Orcamento

def verificar_dados():
    print("=== VERIFICAÇÃO DO BANCO DE DADOS ===")
    print(f"Produtos (MP_Produtos): {MP_Produtos.objects.count()}")
    print(f"Impostos: {Imposto.objects.count()}")
    print(f"Mão de Obra: {MaoObra.objects.count()}")
    print(f"Orçamentos: {Orcamento.objects.count()}")
    
    if MP_Produtos.objects.count() > 0:
        print("\nPrimeiros 5 produtos:")
        for produto in MP_Produtos.objects.all()[:5]:
            print(f"- {produto.id}: {produto.descricao}")
    else:
        print("\n❌ BANCO VAZIO - Nenhum produto encontrado!")

if __name__ == "__main__":
    verificar_dados()