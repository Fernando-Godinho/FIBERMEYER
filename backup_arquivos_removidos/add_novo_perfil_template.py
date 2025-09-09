#!/usr/bin/env python
"""
Script para adicionar o template parametrizado 'N        # Fórmula: quantidade = valor do parâmetro (sem perda individual)
        formula = nome_parametroerfil' com parâmetros e componentes no banco
"""
import os
import sys
import django
from datetime import datetime

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate, ComponenteTemplate, MP_Produtos

def add_novo_perfil_template():
    # Cria o template principal
    template, created = ProdutoTemplate.objects.get_or_create(
        nome='Novo Perfil',
        defaults={
            'categoria': 'Perfil',
            'unidade_final': 'm',
            'ativo': True,
            'descricao': 'Template para perfis parametrizados',
            'criado_em': datetime.now()
        }
    )
    print(f"Template {'criado' if created else 'já existe'}: {template.nome}")

    # Parâmetros
    parametros = [
        {'nome': 'roving_4400', 'label': 'Roving 4400 (kg)', 'tipo': 'decimal', 'obrigatorio': True, 'ordem': 1},
        {'nome': 'manta_300', 'label': 'Manta 300 (m²)', 'tipo': 'decimal', 'obrigatorio': True, 'ordem': 2},
        {'nome': 'veu_qtd', 'label': 'Véu (kg)', 'tipo': 'decimal', 'obrigatorio': True, 'ordem': 3},
        {'nome': 'peso_m', 'label': 'Peso/m (kg)', 'tipo': 'decimal', 'obrigatorio': True, 'ordem': 4},
        {'nome': 'tipo_resina_id', 'label': 'Tipo de Resina', 'tipo': 'produto', 'obrigatorio': True, 'ordem': 5, 'valor_padrao': '1269'},  # ID da Resina Poliéster como padrão
        {'nome': 'perda_processo', 'label': 'Perda de Processo (%)', 'tipo': 'decimal', 'obrigatorio': True, 'ordem': 6, 'valor_padrao': '3'},
        {'nome': 'descricao', 'label': 'Descrição', 'tipo': 'texto', 'obrigatorio': False, 'ordem': 7},
    ]
    for param in parametros:
        obj, _ = ParametroTemplate.objects.get_or_create(
            template=template,
            nome=param['nome'],
            defaults={
                'label': param['label'],
                'tipo': param['tipo'],
                'obrigatorio': param['obrigatorio'],
                'ordem': param['ordem'],
                'valor_padrao': param.get('valor_padrao', '')
            }
        )
        print(f"Parametro: {obj.nome}")

    # Componentes diretos (roving, manta, véu) - quantidade = valor inputado
    componentes_diretos = [
        ('Roving 4400', 'roving_4400'),
        ('Manta 300', 'manta_300'), 
        ('Véu', 'veu_qtd'),  # Véu sem perda individual
    ]
    ordem = 1
    produtos_nao_encontrados = []
    
    # Adicionar componentes diretos primeiro
    for nome_componente, nome_parametro in componentes_diretos:
        # Buscar produto pelo nome
        produto = None
        if 'roving' in nome_componente.lower():
            produto = MP_Produtos.objects.filter(descricao='Roving 4400').first()
        elif 'manta' in nome_componente.lower():
            produto = MP_Produtos.objects.filter(descricao='Manta 300').first()
        elif 'véu' in nome_componente.lower():
            produto = MP_Produtos.objects.filter(descricao='Véu').first()
        
        if not produto:
            print(f"Produto '{nome_componente}' não encontrado, crie manualmente depois!")
            produtos_nao_encontrados.append(nome_componente)
        
        # Fórmula: quantidade = valor do parâmetro (sem perda individual)
        formula = nome_parametro
        obj, _ = ComponenteTemplate.objects.get_or_create(
            template=template,
            nome_componente=nome_componente,
            defaults={
                'produto': produto,
                'formula_quantidade': formula,
                'ativo': True,
                'ordem': ordem
            }
        )
        print(f"Componente: {obj.nome_componente} | Fórmula: {formula}")
        ordem += 1

    # Componentes calculados (resina selecionada e aditivos) - baseados no peso residual
    componentes_calculados = [
        ('Resina', 0.6897, 'tipo_resina'),  # Usar resina selecionada pelo usuário
        ('Monômero de estireno', 0.0213, None),
        ('Anti UV', 0.0028, None),
        ('Anti OX', 0.0011, None),
        ('BPO', 0.0071, None),
        ('TBPB', 0.0043, None),
        ('Desmoldante', 0.0071, None),
        ('Antichama', 0.1777, None),
        ('Carga mineral', 0.0711, None),
        ('Pigmento', 0.0178, None),
    ]
    
    for item in componentes_calculados:
        if len(item) == 3:
            nome, fator, param_produto = item
        else:
            nome, fator = item
            param_produto = None
        
        # Para resina, usar a resina poliéster como padrão (será substituída dinamicamente)
        if param_produto == 'tipo_resina':
            produto = MP_Produtos.objects.filter(descricao='Resina Poliéster').first()
            if not produto:
                print(f"Resina Poliéster não encontrada, usando primeira resina disponível")
                produto = MP_Produtos.objects.filter(descricao__icontains='resina').first()
        else:
            # Tenta encontrar o produto pelo nome
            produto = MP_Produtos.objects.filter(descricao__icontains=nome).first()
            if not produto:
                print(f"Produto '{nome}' não encontrado, crie manualmente depois!")
                produtos_nao_encontrados.append(nome)
        
        formula = f'(peso_m - (roving_4400 + manta_300 + veu_qtd)) * {fator}'
        obj, _ = ComponenteTemplate.objects.get_or_create(
            template=template,
            nome_componente=nome,
            defaults={
                'produto': produto,
                'formula_quantidade': formula,
                'ativo': True,
                'ordem': ordem
            }
        )
        print(f"Componente: {obj.nome_componente} | Fórmula: {formula}")
        ordem += 1

    if produtos_nao_encontrados:
        print("\nResumo dos produtos não encontrados:")
        for nome in produtos_nao_encontrados:
            print(f"- {nome}")

if __name__ == '__main__':
    add_novo_perfil_template()
    print('Template parametrizado "Novo Perfil" criado!')
