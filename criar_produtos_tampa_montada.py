#!/usr/bin/env python
"""
Script para criar produtos necessários para Tampa Montada
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def criar_produtos_tampa_montada():
    print("=== CRIANDO PRODUTOS NECESSÁRIOS PARA TAMPA MONTADA ===\n")
    
    produtos_para_criar = [
        {
            'descricao': 'Chapa Lisa 2,5mm - Res. Poliéster',
            'custo_centavos': 2500,  # R$ 25,00/m²
            'peso_und': 6.25,  # kg/m² (densidade típica chapa 2,5mm)
            'unidade': 'm²',
            'referencia': 'CHAPA-2.5',
            'tipo_produto': 'simples',
            'categoria': 'Chapas'
        },
        {
            'descricao': 'Perfil U4" - Res. Poliéster',
            'custo_centavos': 850,  # R$ 8,50/m
            'peso_und': 0.85,  # kg/m
            'unidade': 'm',
            'referencia': 'PERFIL-U4',
            'tipo_produto': 'simples',
            'categoria': 'Perfis'
        },
        {
            'descricao': 'Alça Metálica - Aço Inox',
            'custo_centavos': 1200,  # R$ 12,00/unid
            'peso_und': 0.15,  # kg/unid
            'unidade': 'unid',
            'referencia': 'ALCA-INOX',
            'tipo_produto': 'simples',
            'categoria': 'Acessórios'
        },
        {
            'descricao': 'Chapa EV - Res. Poliéster',
            'custo_centavos': 3200,  # R$ 32,00/m²
            'peso_und': 4.8,  # kg/m²
            'unidade': 'm²',
            'referencia': 'CHAPA-EV',
            'tipo_produto': 'simples',
            'categoria': 'Chapas'
        }
    ]
    
    produtos_criados = 0
    
    for dados in produtos_para_criar:
        # Verificar se já existe
        existente = MP_Produtos.objects.filter(descricao=dados['descricao']).first()
        
        if existente:
            print(f"⚠️  Produto já existe: {dados['descricao']} (ID: {existente.id})")
        else:
            # Criar produto
            produto = MP_Produtos.objects.create(**dados)
            print(f"✅ Produto criado: ID {produto.id} - {produto.descricao} - R$ {produto.custo_centavos/100:.2f}")
            produtos_criados += 1
    
    print(f"\n📊 RESUMO:")
    print(f"   • Produtos criados: {produtos_criados}")
    print(f"   • Total de produtos no banco: {MP_Produtos.objects.count()}")
    
    # Verificar se agora temos todos os produtos
    print(f"\n🔍 VERIFICAÇÃO FINAL:")
    
    verificacoes = [
        ('Chapa 2,5mm', 'chapa 2,5'),
        ('Perfil U4"', 'u4'),
        ('Alça', 'alça'),
        ('Chapa EV', 'chapa ev'),
        ('Mão de Obra', 'processamento')
    ]
    
    for nome, termo in verificacoes:
        if 'processamento' in termo:
            produtos = MP_Produtos.objects.filter(descricao__icontains='mão de obra').filter(descricao__icontains='processamento')
        else:
            produtos = MP_Produtos.objects.filter(descricao__icontains=termo)
        
        status = "✅" if produtos.exists() else "❌"
        print(f"   {status} {nome}: {produtos.count()} produto(s) encontrado(s)")

if __name__ == '__main__':
    criar_produtos_tampa_montada()
