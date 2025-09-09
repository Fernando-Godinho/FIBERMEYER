#!/usr/bin/env python3
"""
Script para verificar o estado atual do banco de dados
Mostra todos os produtos e templates existentes
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos

def main():
    print("=== VERIFICAÇÃO DO BANCO DE DADOS ===")
    
    # Verificar templates
    print("\n📋 TEMPLATES:")
    templates = ProdutoTemplate.objects.all()
    print(f"Total: {templates.count()}")
    
    if templates.exists():
        for template in templates:
            produto_desc = template.produto_base.descricao if template.produto_base else "Sem produto base"
            print(f"  - Template ID: {template.id} | Produto: {produto_desc}")
    else:
        print("  ✅ Nenhum template encontrado (perfeito!)")
    
    # Verificar produtos com "Novo Perfil" no nome
    print("\n🔍 PRODUTOS COM 'NOVO PERFIL':")
    produtos_novo_perfil = MP_Produtos.objects.filter(descricao__icontains="novo perfil")
    print(f"Total: {produtos_novo_perfil.count()}")
    
    if produtos_novo_perfil.exists():
        print("🗑️  Produtos encontrados (podem causar conflito):")
        for produto in produtos_novo_perfil:
            print(f"  - Produto ID: {produto.id} | {produto.descricao} | Categoria: {produto.categoria}")
        
        # Opção para remover
        resposta = input("\n❓ Deseja remover estes produtos? (s/N): ").lower()
        if resposta == 's':
            print("🗑️  Removendo produtos...")
            count = produtos_novo_perfil.count()
            produtos_novo_perfil.delete()
            print(f"✅ {count} produto(s) removido(s)!")
        else:
            print("ℹ️  Produtos mantidos")
    else:
        print("  ✅ Nenhum produto 'Novo Perfil' encontrado (perfeito!)")
    
    # Verificar total de produtos
    print(f"\n📊 RESUMO:")
    total_produtos = MP_Produtos.objects.count()
    total_templates = ProdutoTemplate.objects.count()
    print(f"  - Total de produtos: {total_produtos}")
    print(f"  - Total de templates: {total_templates}")
    
    print("\n✅ Verificação concluída!")

if __name__ == '__main__':
    main()
