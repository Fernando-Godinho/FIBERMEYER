#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos, ProdutoComponente

def main():
    print("=== INVESTIGANDO TEMPLATE ORIGINAL 'NOVO PERFIL' ===")
    
    # Buscar produtos com "Novo Perfil" no nome
    produtos_perfil = MP_Produtos.objects.filter(descricao__icontains="novo perfil")
    print(f"📦 Produtos com 'Novo Perfil': {produtos_perfil.count()}")
    
    for produto in produtos_perfil:
        print(f"- ID {produto.id}: {produto.descricao}")
        print(f"  Tipo: {produto.tipo_produto}")
        print(f"  Custo: R$ {produto.custo_centavos/100:.2f}")
        print(f"  Categoria: {produto.categoria}")
        
        # Verificar se tem componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        if componentes.exists():
            print(f"  📋 Componentes ({componentes.count()}):")
            for comp in componentes:
                custo = comp.produto_componente.custo_centavos / 100
                print(f"    - {comp.produto_componente.descricao}: {comp.quantidade} x R$ {custo:.2f}")
        
        # Verificar se tem template
        if hasattr(produto, 'template'):
            template = produto.template
            print(f"  ✅ Tem template (ID: {template.id})")
            print(f"     Parâmetros obrigatórios: {template.parametros_obrigatorios}")
            print(f"     Parâmetros opcionais: {template.parametros_opcionais}")
        else:
            print(f"  ❌ Não tem template")
        
        print("-" * 60)
    
    # Verificar templates existentes
    print()
    print("=== TEMPLATES ATUAIS ===")
    templates = ProdutoTemplate.objects.all()
    
    for template in templates:
        produto_nome = template.produto_base.descricao if template.produto_base else "Sem produto"
        print(f"Template ID {template.id}: {produto_nome}")
        print(f"  Parâmetros obrigatórios: {template.parametros_obrigatorios}")
        print(f"  Parâmetros opcionais: {template.parametros_opcionais}")
        
        if template.produto_base:
            # Verificar componentes do produto base
            componentes = ProdutoComponente.objects.filter(produto_principal=template.produto_base)
            if componentes.exists():
                print(f"  📋 Componentes do produto base ({componentes.count()}):")
                for comp in componentes:
                    custo = comp.produto_componente.custo_centavos / 100
                    print(f"    - {comp.produto_componente.descricao}: {comp.quantidade} x R$ {custo:.2f}")
        
        print("-" * 60)
    
    print()
    print("🔍 BUSCAR DADOS PARA RECRIAÇÃO:")
    print("1. Verificando se existem componentes órfãos...")
    
    # Verificar se há componentes que podem ter sido do template original
    componentes_todos = ProdutoComponente.objects.all().select_related('produto_principal', 'produto_componente')
    
    print(f"📊 Total de componentes no sistema: {componentes_todos.count()}")
    
    # Agrupar por produto pai para ver padrões
    produtos_com_componentes = {}
    for comp in componentes_todos:
        pai_id = comp.produto_principal.id
        if pai_id not in produtos_com_componentes:
            produtos_com_componentes[pai_id] = {
                'produto': comp.produto_principal,
                'componentes': []
            }
        produtos_com_componentes[pai_id]['componentes'].append(comp)
    
    print()
    print("📋 PRODUTOS COM COMPONENTES (possíveis templates):")
    for pai_id, dados in produtos_com_componentes.items():
        produto = dados['produto']
        componentes = dados['componentes']
        
        # Focar em produtos que podem ser templates
        if produto.tipo_produto in ['parametrizado', 'composto'] or len(componentes) > 1:
            print(f"🔍 {produto.descricao} (ID: {produto.id}) - {produto.tipo_produto}")
            print(f"   📋 {len(componentes)} componentes:")
            total_custo = 0
            for comp in componentes:
                custo = comp.produto_componente.custo_centavos / 100
                custo_total = custo * comp.quantidade
                total_custo += custo_total
                print(f"     - {comp.produto_componente.descricao}")
                print(f"       Qtd: {comp.quantidade}, Custo unit: R$ {custo:.2f}, Total: R$ {custo_total:.2f}")
            
            print(f"   💰 Custo total estimado: R$ {total_custo:.2f}")
            print(f"   💰 Custo do produto: R$ {produto.custo_centavos/100:.2f}")
            print()

if __name__ == "__main__":
    main()
