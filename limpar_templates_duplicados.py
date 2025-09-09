#!/usr/bin/env python3
"""
Script para limpar templates duplicados do banco de dados
Mantém apenas os templates corretos e remove duplicações
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
    print("=== LIMPEZA DE TEMPLATES DUPLICADOS ===")
    
    # Listar todos os templates atuais
    templates = ProdutoTemplate.objects.all()
    print(f"\n📋 Templates encontrados: {templates.count()}")
    
    for template in templates:
        produto_base_desc = template.produto_base.descricao if template.produto_base else "Sem produto base"
        print(f"  - ID: {template.id} | Produto: {produto_base_desc}")
    
    # Identificar templates com nome "Novo Perfil" ou similares
    templates_novo_perfil = ProdutoTemplate.objects.filter(
        produto_base__descricao__icontains="novo perfil"
    )
    
    print(f"\n🔍 Templates 'Novo Perfil' encontrados: {templates_novo_perfil.count()}")
    
    if templates_novo_perfil.exists():
        print("\n🗑️  REMOVENDO templates 'Novo Perfil' duplicados...")
        for template in templates_novo_perfil:
            print(f"  - Removendo Template ID: {template.id} - {template.produto_base.descricao}")
            # Remover também o produto base associado se existir
            if template.produto_base:
                produto_base = template.produto_base
                print(f"    - Removendo Produto Base ID: {produto_base.id} - {produto_base.descricao}")
                produto_base.delete()
            template.delete()
        
        print("✅ Templates 'Novo Perfil' removidos com sucesso!")
    else:
        print("ℹ️  Nenhum template 'Novo Perfil' encontrado no banco")
    
    # Listar templates restantes
    templates_restantes = ProdutoTemplate.objects.all()
    print(f"\n📊 Templates restantes: {templates_restantes.count()}")
    
    if templates_restantes.exists():
        print("📋 Lista final de templates:")
        for template in templates_restantes:
            produto_base_desc = template.produto_base.descricao if template.produto_base else "Sem produto base"
            categoria = template.produto_base.categoria if template.produto_base else "Sem categoria"
            print(f"  - ID: {template.id} | {produto_base_desc} | Categoria: {categoria}")
    else:
        print("ℹ️  Nenhum template restante")
    
    print("\n✅ Limpeza concluída!")
    print("🔄 Recarregue a página do sistema para ver as mudanças")

if __name__ == '__main__':
    main()
