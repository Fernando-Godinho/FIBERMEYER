#!/usr/bin/env python
"""
Script para criar templates de exemplo para produtos parametrizáveis
"""
import os
import sys
import django
import json

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoTemplate, ParametroTemplate, ComponenteTemplate

def criar_template_grade():
    """Cria um template de exemplo para grades"""
    
    # Verificar se já existe
    if ProdutoTemplate.objects.filter(nome="Grade Standard").exists():
        print("Template 'Grade Standard' já existe.")
        return
    
    # Produtos base necessários para grades
    produtos_base = [
        {
            'descricao': 'Perfil I 100x50x6mm',
            'unidade': 'M',
            'custo_centavos': 4500,  # R$ 45,00 por metro
            'peso_und': 15.000,
            'referencia': 'PI-100x50x6'
        },
        {
            'descricao': 'Chaveta 6mm',
            'unidade': 'UN',
            'custo_centavos': 250,  # R$ 2,50 por unidade
            'peso_und': 0.010,
            'referencia': 'CH-6MM'
        }
    ]
    
    produtos_criados = {}
    for produto_data in produtos_base:
        produto, created = MP_Produtos.objects.get_or_create(
            descricao=produto_data['descricao'],
            defaults=produto_data
        )
        produtos_criados[produto_data['descricao']] = produto
        if created:
            print(f"✓ Produto criado: {produto_data['descricao']}")
        else:
            print(f"⚠ Produto já existe: {produto_data['descricao']}")
    
    # Usar produto de cola existente da base de dados
    try:
        cola_existente = MP_Produtos.objects.get(descricao='COLA ESTRUTURAL 4500 A/B -')
        produtos_criados['Cola Estrutural'] = cola_existente
        print(f"✓ Usando cola existente: {cola_existente.descricao} - R$ {cola_existente.custo_centavos/100:.2f}")
    except MP_Produtos.DoesNotExist:
        print("⚠ Cola estrutural não encontrada na base de dados")
    
    # Criar template
    template = ProdutoTemplate.objects.create(
        nome="Grade Standard",
        descricao="Template para criação de grades com perfis quadrados",
        categoria="Grade",
        unidade_final="M²"
    )
    print(f"✓ Template criado: {template.nome}")
    
    # Criar parâmetros
    parametros = [
        {
            'nome': 'largura',
            'label': 'Largura (mm)',
            'tipo': 'inteiro',
            'obrigatorio': True,
            'valor_padrao': '3000',
            'ajuda': 'Largura total da grade em milímetros',
            'ordem': 1
        },
        {
            'nome': 'vao',
            'label': 'Vão (mm)',
            'tipo': 'inteiro',
            'obrigatorio': True,
            'valor_padrao': '1500',
            'ajuda': 'Distância do vão para cálculo das travas em milímetros',
            'ordem': 2
        },
        {
            'nome': 'perfil_id',
            'label': 'Tipo de Perfil Principal',
            'tipo': 'produto',
            'obrigatorio': True,
            'ajuda': 'Selecione o perfil que será utilizado na estrutura principal',
            'ordem': 3
        },
        {
            'nome': 'perfil_trava_id',
            'label': 'Perfil de Trava',
            'tipo': 'produto',
            'obrigatorio': True,
            'ajuda': 'Selecione o perfil que será utilizado como trava',
            'ordem': 4
        },
        {
            'nome': 'espacamento',
            'label': 'Espaçamento entre barras (mm)',
            'tipo': 'inteiro',
            'obrigatorio': True,
            'valor_padrao': '150',
            'ajuda': 'Espaçamento entre barras verticais em milímetros',
            'ordem': 5
        }
    ]
    
    for param_data in parametros:
        param = ParametroTemplate.objects.create(
            template=template,
            **param_data
        )
        print(f"✓ Parâmetro criado: {param.label}")
    
    # Criar componentes simplificados: apenas Perfil I, Chaveta e Cola
    componentes = [
        {
            'nome_componente': 'Perfil I',
            'produto': produtos_criados['Perfil I 100x50x6mm'],
            'formula_quantidade': '(largura / espacamento) * vao / 1000',  # Sem arredondamento - valor preciso
            'ordem': 1
        },
        {
            'nome_componente': 'Chaveta',
            'produto': produtos_criados['Chaveta 6mm'],
            'formula_quantidade': '(vao / 150) * 2',  # Sem arredondamento - valor preciso
            'ordem': 2
        },
        {
            'nome_componente': 'Cola Estrutural',
            'produto': produtos_criados['Cola Estrutural'],
            'formula_quantidade': '0.06',  # Quantidade fixa: 0.06 * valor da cola
            'ordem': 3
        }
    ]
    
    for comp_data in componentes:
        # Para este exemplo simples, usar sempre o perfil 20x20
        # Em uma implementação mais avançada, você poderia ter lógica condicional
        componente = ComponenteTemplate.objects.create(
            template=template,
            **comp_data
        )
        print(f"✓ Componente criado: {componente.nome_componente}")
    
    print(f"\n🎉 Template '{template.nome}' criado com sucesso!")
    print("Agora você pode usar este template para criar grades personalizadas.")

def criar_template_estrutura():
    """Cria um template para estruturas simples"""
    
    if ProdutoTemplate.objects.filter(nome="Estrutura Simples").exists():
        print("Template 'Estrutura Simples' já existe.")
        return
        
    # Criar template para estrutura
    template = ProdutoTemplate.objects.create(
        nome="Estrutura Simples",
        descricao="Template para estruturas metálicas simples com vigas e pilares",
        categoria="Estrutura",
        unidade_final="M²"
    )
    
    # Parâmetros para estrutura
    parametros = [
        {
            'nome': 'comprimento',
            'label': 'Comprimento (m)',
            'tipo': 'decimal',
            'obrigatorio': True,
            'valor_padrao': '6.0',
            'ordem': 1
        },
        {
            'nome': 'largura',
            'label': 'Largura (m)', 
            'tipo': 'decimal',
            'obrigatorio': True,
            'valor_padrao': '4.0',
            'ordem': 2
        },
        {
            'nome': 'altura',
            'label': 'Altura dos Pilares (m)',
            'tipo': 'decimal',
            'obrigatorio': True,
            'valor_padrao': '3.0',
            'ordem': 3
        }
    ]
    
    for param_data in parametros:
        ParametroTemplate.objects.create(template=template, **param_data)
    
    print(f"✓ Template criado: {template.nome}")

if __name__ == '__main__':
    print("Criando templates de exemplo...")
    criar_template_grade()
    criar_template_estrutura()
    print("\n✅ Templates criados com sucesso!")
