#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos

def main():
    print("=== VERIFICANDO PRODUTOS E TEMPLATES ===")
    
    # Verifica produtos com "Novo Perfil" ou "perfil"
    produtos_perfil = MP_Produtos.objects.filter(descricao__icontains="perfil")
    print(f"📦 Produtos com 'perfil' no nome: {produtos_perfil.count()}")
    
    for produto in produtos_perfil:
        print(f"- ID {produto.id}: {produto.descricao}")
    
    print()
    
    # Verifica todos os templates
    templates = ProdutoTemplate.objects.all()
    print(f"📋 Templates existentes: {templates.count()}")
    
    for template in templates:
        print(f"- Template ID {template.id}: {template.produto_base.descricao if template.produto_base else 'Sem produto base'}")
    
    print()
    
    # Vamos criar um produto "Novo Perfil" e associar a um template
    print("🛠️  CONFIGURAÇÃO DO TEMPLATE 'NOVO PERFIL'")
    
    # Verifica se já existe produto "Novo Perfil"
    novo_perfil_produto = MP_Produtos.objects.filter(descricao="Novo Perfil").first()
    
    if not novo_perfil_produto:
        print("📦 Criando produto 'Novo Perfil'...")
        novo_perfil_produto = MP_Produtos.objects.create(
            descricao="Novo Perfil",
            tipo_produto="parametrizado",
            custo_centavos=0,
            categoria="PRODUTO_FINAL",
            unidade="UN"
        )
        print(f"✅ Produto 'Novo Perfil' criado (ID: {novo_perfil_produto.id})")
    else:
        print(f"✅ Produto 'Novo Perfil' já existe (ID: {novo_perfil_produto.id})")
    
    # Verifica se já tem template associado
    if hasattr(novo_perfil_produto, 'template'):
        print(f"✅ Produto já tem template associado (ID: {novo_perfil_produto.template.id})")
        template_principal = novo_perfil_produto.template
    else:
        # Pega um template sem produto base ou cria um novo
        template_disponivel = ProdutoTemplate.objects.filter(produto_base__isnull=True).first()
        
        if template_disponivel:
            print(f"📋 Associando template existente (ID: {template_disponivel.id}) ao produto 'Novo Perfil'")
            template_disponivel.produto_base = novo_perfil_produto
            template_disponivel.save()
            template_principal = template_disponivel
        else:
            print("📋 Criando novo template para 'Novo Perfil'...")
            template_principal = ProdutoTemplate.objects.create(
                produto_base=novo_perfil_produto,
                parametros_obrigatorios=["comprimento", "largura", "espessura"],
                parametros_opcionais={"tolerancia": 0.1, "acabamento": "padrao"},
                formula_principal="comprimento * largura * espessura * densidade_material"
            )
        
        print(f"✅ Template configurado (ID: {template_principal.id})")
    
    print()
    print("🗑️  REMOVENDO TEMPLATES DESNECESSÁRIOS")
    
    # Remove outros templates
    templates_para_remover = ProdutoTemplate.objects.exclude(id=template_principal.id)
    
    if templates_para_remover.exists():
        print(f"📋 Templates que serão removidos: {templates_para_remover.count()}")
        for template in templates_para_remover:
            nome = template.produto_base.descricao if template.produto_base else f"Template ID {template.id}"
            print(f"- {nome}")
        
        confirmacao = input("⚠️  Deseja remover os templates desnecessários? (s/N): ").lower()
        
        if confirmacao == 's':
            count = templates_para_remover.count()
            templates_para_remover.delete()
            print(f"✅ {count} templates removidos")
        else:
            print("❌ Operação cancelada")
    else:
        print("✅ Nenhum template desnecessário encontrado")
    
    print()
    print("📋 CONFIGURAÇÃO FINAL:")
    print(f"✅ Produto: {novo_perfil_produto.descricao} (ID: {novo_perfil_produto.id})")
    print(f"✅ Template: ID {template_principal.id}")
    print(f"✅ Parâmetros obrigatórios: {template_principal.parametros_obrigatorios}")
    print(f"✅ Parâmetros opcionais: {template_principal.parametros_opcionais}")

if __name__ == "__main__":
    main()
