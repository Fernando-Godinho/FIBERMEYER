#!/usr/bin/env python
"""
Teste para verificar se a correção do mao_obra_produto_id está funcionando
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos, ProdutoComponente, MaoObra
import requests
import json

def test_grade_creation():
    print("=== TESTE DE CRIAÇÃO DE GRADE COM MÃO DE OBRA ===")
    
    # Verificar produtos necessários
    print("\n1. Verificando produtos necessários...")
    
    # Perfis
    perfis = MP_Produtos.objects.filter(
        descricao__icontains='I25'
    ).union(
        MP_Produtos.objects.filter(descricao__icontains='I32')
    ).union(
        MP_Produtos.objects.filter(descricao__icontains='I38')
    )
    print(f"   • Perfis encontrados: {perfis.count()}")
    
    # Chaveta
    chaveta = MP_Produtos.objects.filter(id=1332).first()
    print(f"   • Chaveta (ID 1332): {'✅ OK' if chaveta else '❌ NÃO ENCONTRADA'}")
    
    # Cola
    cola = MP_Produtos.objects.filter(id=1183).first()
    print(f"   • Cola (ID 1183): {'✅ OK' if cola else '❌ NÃO ENCONTRADA'}")
    
    # Mão de obra
    mo_produto = MP_Produtos.objects.filter(
        descricao__icontains='mão de obra'
    ).filter(
        descricao__icontains='processamento'
    ).first()
    
    if mo_produto:
        print(f"   • Produto Mão de Obra: ✅ ID {mo_produto.id} - {mo_produto.descricao}")
    else:
        print("   • Produto Mão de Obra: ❌ NÃO ENCONTRADO")
        
        # Criar produto de mão de obra se não existir
        print("   • Criando produto de mão de obra...")
        mo_record = MaoObra.objects.first()
        if mo_record:
            mo_produto, created = MP_Produtos.objects.get_or_create(
                descricao=f'MÃO DE OBRA {mo_record.nome}',
                defaults={
                    'custo_centavos': mo_record.valor_centavos,
                    'peso_und': 0,
                    'unidade': mo_record.unidade,
                    'referencia': f'MO-{mo_record.id}',
                    'tipo_produto': 'simples',
                    'categoria': 'Mão de Obra'
                }
            )
            print(f"     ✅ Criado: ID {mo_produto.id} - {mo_produto.descricao}")
    
    print("\n2. Produtos existentes antes do teste:")
    produtos_antes = MP_Produtos.objects.count()
    componentes_antes = ProdutoComponente.objects.count()
    print(f"   • MP_Produtos: {produtos_antes}")
    print(f"   • ProdutoComponente: {componentes_antes}")
    
    # Dados de teste para grade
    dados_grade = {
        "nome_grade": "GRADE TESTE MO",
        "perfil": "I25",
        "tipo_perfil": "normal",
        "comprimento": 6000,
        "vao": 1200,
        "eixo_i": 150,
        "perda": 3,
        "tempo_proc": 1.5,
        "tempo_mtg": 0.5,
        "tipo_calculo": "grade"
    }
    
    print(f"\n3. Dados da grade teste:")
    for key, value in dados_grade.items():
        print(f"   • {key}: {value}")
    
    print(f"\n✅ Teste preparado. Execute manualmente na interface para testar:")
    print(f"   • Acesse: http://localhost:8000/mp")
    print(f"   • Clique em 'Novo Perfil'")
    print(f"   • Selecione 'Grade'")
    print(f"   • Preencha os dados acima")
    print(f"   • Calcule e salve")
    print(f"   • Verifique se salvou com mão de obra incluída")

if __name__ == '__main__':
    test_grade_creation()
