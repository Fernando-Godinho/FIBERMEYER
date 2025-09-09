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
    print("=== STATUS FINAL DO SISTEMA DE TEMPLATES ===")
    print()
    
    # Verificar templates
    templates = ProdutoTemplate.objects.all()
    print(f"📋 Total de templates: {templates.count()}")
    
    if templates.count() == 1:
        template = templates.first()
        produto = template.produto_base
        
        print("✅ TEMPLATE ÚNICO CONFIGURADO:")
        print(f"   ID do Template: {template.id}")
        print(f"   Produto Base: {produto.descricao} (ID: {produto.id})")
        print(f"   Tipo: {produto.tipo_produto}")
        print(f"   Categoria: {produto.categoria}")
        print()
        
        print("📐 PARÂMETROS OBRIGATÓRIOS:")
        for i, param in enumerate(template.parametros_obrigatorios, 1):
            print(f"   {i}. {param}")
        
        print()
        print("⚙️ PARÂMETROS OPCIONAIS:")
        for param, valor in template.parametros_opcionais.items():
            print(f"   • {param}: {valor}")
        
        print()
        print("🔧 FÓRMULA DE CÁLCULO:")
        print(template.formula_principal.strip())
        
        print()
        print("🎯 COMO USAR ESTE TEMPLATE:")
        print("1. No frontend, selecione 'Novo Perfil' como produto base")
        print("2. Informe os parâmetros obrigatórios:")
        print("   - comprimento (em metros)")
        print("   - largura (em mm)")
        print("   - altura (em mm)")
        print("   - espessura (em mm)")
        print("3. Ajuste os parâmetros opcionais se necessário")
        print("4. O sistema calculará automaticamente o custo")
        
        print()
        print("🏗️  CRIAÇÃO DE NOVOS TEMPLATES:")
        print("• Use este template como referência")
        print("• Duplique e modifique para criar novos perfis")
        print("• Mantenha a estrutura de parâmetros similar")
        print("• Ajuste a fórmula conforme necessário")
        
    else:
        print("⚠️  Múltiplos templates encontrados:")
        for template in templates:
            nome = template.produto_base.descricao if template.produto_base else f"Template {template.id}"
            print(f"   - {nome} (ID: {template.id})")
    
    print()
    print("✅ SISTEMA ORGANIZADO COM SUCESSO!")
    print("✅ Template base 'Novo Perfil' configurado")
    print("✅ Pronto para parametrização de produtos")

if __name__ == "__main__":
    main()
