#!/usr/bin/env python
"""
Script para deletar e recriar o template 'Novo Perfil' com perda de 3% no véu
"""
import os
import sys
import django

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ComponenteTemplate

def delete_and_recreate_template():
    print("=== DELETANDO TEMPLATE EXISTENTE ===")
    
    # Deletar template existente
    template_existente = ProdutoTemplate.objects.filter(nome='Novo Perfil').first()
    if template_existente:
        print(f"Deletando template: {template_existente.nome}")
        template_existente.delete()
        print("Template deletado!")
    else:
        print("Nenhum template 'Novo Perfil' encontrado para deletar")
    
    print("\n=== RECRIANDO TEMPLATE ===")
    print("Execute novamente: python add_novo_perfil_template.py")

if __name__ == '__main__':
    delete_and_recreate_template()
