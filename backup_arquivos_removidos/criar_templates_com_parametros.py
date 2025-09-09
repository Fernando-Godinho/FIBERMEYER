#!/usr/bin/env python
"""
Script para criar templates de exemplo com parâmetros para testar o sistema.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoTemplate

def criar_templates_exemplo():
    print("=== CRIANDO TEMPLATES DE EXEMPLO ===\n")
    
    # 1. Template para Grade Personalizada
    try:
        # Buscar ou criar produto base
        produto_grade, created = MP_Produtos.objects.get_or_create(
            descricao="Grade Personalizada",
            defaults={
                'tipo_produto': 'parametrizado',
                'custo_centavos': 50000,  # R$ 500,00
                'unidade': 'UN',
                'referencia': 'GRADE-PARAM',
                'categoria': 'Estruturas',
                'subcategoria': 'Grades'
            }
        )
        
        # Criar template para grade
        template_grade, created = ProdutoTemplate.objects.get_or_create(
            produto_base=produto_grade,
            defaults={
                'parametros_obrigatorios': ['largura', 'comprimento', 'altura'],
                'parametros_opcionais': {
                    'cor': 'branco',
                    'acabamento': 'liso',
                    'espessura': '25mm'
                },
                'formula_principal': '(largura * comprimento * altura) * preco_base + (cor == "especial" ? 100 : 0)'
            }
        )
        
        if created:
            print(f"✅ Template 'Grade Personalizada' criado com sucesso!")
        else:
            print(f"ℹ️  Template 'Grade Personalizada' já existe")
        
        print(f"   - Parâmetros obrigatórios: {template_grade.parametros_obrigatorios}")
        print(f"   - Parâmetros opcionais: {template_grade.parametros_opcionais}")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao criar template Grade: {e}")
    
    # 2. Template para Perfil Pultrudado
    try:
        produto_perfil, created = MP_Produtos.objects.get_or_create(
            descricao="Perfil Pultrudado Personalizado",
            defaults={
                'tipo_produto': 'parametrizado',
                'custo_centavos': 15000,  # R$ 150,00 por metro
                'unidade': 'M',
                'referencia': 'PERFIL-PARAM',
                'categoria': 'Perfis',
                'subcategoria': 'Pultrudados'
            }
        )
        
        template_perfil, created = ProdutoTemplate.objects.get_or_create(
            produto_base=produto_perfil,
            defaults={
                'parametros_obrigatorios': ['comprimento', 'largura', 'tipo_fibra'],
                'parametros_opcionais': {
                    'tipo_resina': 'poliester',
                    'cor': 'natural',
                    'quantidade_barras': '1',
                    'tolerancia': '±2mm'
                },
                'formula_principal': 'comprimento * largura * preco_metro + (tipo_fibra == "carbono" ? comprimento * 50 : 0)'
            }
        )
        
        if created:
            print(f"✅ Template 'Perfil Pultrudado' criado com sucesso!")
        else:
            print(f"ℹ️  Template 'Perfil Pultrudado' já existe")
            
        print(f"   - Parâmetros obrigatórios: {template_perfil.parametros_obrigatorios}")
        print(f"   - Parâmetros opcionais: {template_perfil.parametros_opcionais}")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao criar template Perfil: {e}")
    
    # 3. Template para Tanque Personalizado
    try:
        produto_tanque, created = MP_Produtos.objects.get_or_create(
            descricao="Tanque de Fibra Personalizado",
            defaults={
                'tipo_produto': 'parametrizado',
                'custo_centavos': 200000,  # R$ 2.000,00
                'unidade': 'UN',
                'referencia': 'TANQUE-PARAM',
                'categoria': 'Tanques',
                'subcategoria': 'Fibra de Vidro'
            }
        )
        
        template_tanque, created = ProdutoTemplate.objects.get_or_create(
            produto_base=produto_tanque,
            defaults={
                'parametros_obrigatorios': ['capacidade_litros', 'diametro', 'altura_total'],
                'parametros_opcionais': {
                    'tipo_resina': 'isoftalica',
                    'reforco_estrutural': 'sim',
                    'tampa': 'incluida',
                    'conexoes': 'padrão',
                    'cor': 'azul'
                },
                'formula_principal': '(capacidade_litros * 2.5) + (diametro * altura_total * 0.8) + (reforco_estrutural == "sim" ? 500 : 0)'
            }
        )
        
        if created:
            print(f"✅ Template 'Tanque Personalizado' criado com sucesso!")
        else:
            print(f"ℹ️  Template 'Tanque Personalizado' já existe")
            
        print(f"   - Parâmetros obrigatórios: {template_tanque.parametros_obrigatorios}")
        print(f"   - Parâmetros opcionais: {template_tanque.parametros_opcionais}")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao criar template Tanque: {e}")
    
    # Mostrar estatísticas finais
    print("=== ESTATÍSTICAS ===")
    templates_total = ProdutoTemplate.objects.count()
    templates_com_parametros = ProdutoTemplate.objects.exclude(
        parametros_obrigatorios=[], parametros_opcionais={}
    ).count()
    
    print(f"Total de templates: {templates_total}")
    print(f"Templates com parâmetros: {templates_com_parametros}")
    print(f"Templates sem parâmetros: {templates_total - templates_com_parametros}")
    
    print("\n🎉 Templates de exemplo criados com sucesso!")
    print("Agora você pode testar o formulário de produtos parametrizados!")

if __name__ == "__main__":
    criar_templates_exemplo()
