#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate

def main():
    print("=== VERIFICANDO TEMPLATES EXISTENTES ===")
    templates = ProdutoTemplate.objects.all()
    
    if not templates:
        print("❌ Nenhum template encontrado no banco de dados")
        return
    
    print(f"📋 Total de templates: {templates.count()}")
    print()
    
    for template in templates:
        print(f"ID: {template.id}")
        print(f"Nome: {template.produto_base.descricao if template.produto_base else 'Sem produto base'}")
        print(f"Parâmetros obrigatórios: {template.parametros_obrigatorios}")
        print(f"Parâmetros opcionais: {template.parametros_opcionais}")
        print("-" * 50)
    
    # Identifica o template "Novo Perfil"
    novo_perfil_template = None
    for template in templates:
        if template.produto_base and "Novo Perfil" in template.produto_base.descricao:
            novo_perfil_template = template
            break
    
    if novo_perfil_template:
        print(f"✅ Template 'Novo Perfil' encontrado (ID: {novo_perfil_template.id})")
        print(f"   Produto base: {novo_perfil_template.produto_base.descricao}")
        print()
        
        # Lista templates que serão removidos
        templates_para_remover = ProdutoTemplate.objects.exclude(id=novo_perfil_template.id)
        
        if templates_para_remover.exists():
            print("🗑️  TEMPLATES QUE SERÃO REMOVIDOS:")
            for template in templates_para_remover:
                print(f"- {template.nome} (ID: {template.id})")
            
            print()
            confirmacao = input("⚠️  Deseja realmente remover estes templates? (s/N): ").lower()
            
            if confirmacao == 's':
                count_removidos = templates_para_remover.count()
                templates_para_remover.delete()
                print(f"✅ {count_removidos} templates removidos com sucesso!")
                print()
                print("📋 TEMPLATE RESTANTE:")
                print(f"- {novo_perfil_template.nome} (ID: {novo_perfil_template.id})")
            else:
                print("❌ Operação cancelada")
        else:
            print("✅ Apenas o template 'Novo Perfil' existe. Nada para remover.")
    else:
        print("❌ Template 'Novo Perfil' não encontrado!")
        print("📝 Templates disponíveis:")
        for template in templates:
            nome = template.produto_base.descricao if template.produto_base else f"Template ID {template.id} (sem produto base)"
            print(f"- {nome}")
            
        # Vamos verificar se existe algum produto com "Novo Perfil" no nome
        from main.models import MP_Produtos
        produtos_perfil = MP_Produtos.objects.filter(descricao__icontains="Novo Perfil")
        if produtos_perfil.exists():
            print()
            print("🔍 Produtos com 'Novo Perfil' no nome:")
            for produto in produtos_perfil:
                print(f"- {produto.descricao} (ID: {produto.id})")
                # Verifica se tem template associado
                if hasattr(produto, 'template'):
                    print(f"  ✅ Tem template (ID: {produto.template.id})")
                else:
                    print(f"  ❌ Não tem template associado")

if __name__ == "__main__":
    main()
