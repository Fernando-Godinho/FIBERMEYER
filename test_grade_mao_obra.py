#!/usr/bin/env python
"""
Teste para verificar se o problema da mão de obra foi corrigido
"""

import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente, MaoObra
import json

def criar_grade_teste():
    print("=== TESTE: CRIANDO GRADE COM MÃO DE OBRA ===\n")
    
    # 1. Criar produto principal (grade)
    grade = MP_Produtos.objects.create(
        descricao="Grade Teste com Mão de Obra",
        custo_centavos=0,  # Será calculado automaticamente
        peso_und=0.5,
        unidade="m²",
        referencia="GRADE-TESTE-001",
        tipo_produto="composto",
        categoria="Grade"
    )
    print(f"✅ Grade criada: ID {grade.id} - {grade.descricao}")
    
    # 2. Buscar produtos necessários
    try:
        perfil = MP_Produtos.objects.get(id=1328)  # I25mm
        print(f"✅ Perfil encontrado: {perfil.descricao} - R$ {perfil.custo_centavos/100:.2f}")
    except MP_Produtos.DoesNotExist:
        print("❌ Perfil I25mm (ID 1328) não encontrado")
        return
    
    try:
        chaveta = MP_Produtos.objects.get(id=1332)  # Chaveta
        print(f"✅ Chaveta encontrada: {chaveta.descricao} - R$ {chaveta.custo_centavos/100:.2f}")
    except MP_Produtos.DoesNotExist:
        print("❌ Chaveta (ID 1332) não encontrada")
        return
    
    try:
        mao_obra = MaoObra.objects.get(id=2)  # Processamento/Montagem
        print(f"✅ Mão de obra encontrada: {mao_obra.nome} - R$ {mao_obra.valor_real:.2f}/{mao_obra.unidade}")
        
        # Criar produto MP para a mão de obra se não existir
        produto_mo, created = MP_Produtos.objects.get_or_create(
            descricao=f"MÃO DE OBRA {mao_obra.nome}",
            defaults={
                'custo_centavos': mao_obra.valor_centavos,
                'peso_und': 0,
                'unidade': mao_obra.unidade,
                'referencia': f'MO-{mao_obra.id}',
                'tipo_produto': 'simples',
                'categoria': 'Mão de Obra'
            }
        )
        if created:
            print(f"✅ Produto de mão de obra criado: ID {produto_mo.id}")
        else:
            print(f"✅ Produto de mão de obra existente: ID {produto_mo.id}")
    except MaoObra.DoesNotExist:
        print("❌ Mão de obra Processamento/Montagem (ID 2) não encontrada")
        return
    
    # 3. Criar componentes
    componentes_dados = [
        {
            'produto': perfil,
            'quantidade': 2.5,
            'custo_calculado': 250.0,  # R$ 2.50 calculado dinamicamente
            'nome_componente': 'Perfil I25mm (calculado)'
        },
        {
            'produto': chaveta,
            'quantidade': 1.2,
            'custo_calculado': 180.0,  # R$ 1.80 calculado dinamicamente
            'nome_componente': 'Chaveta (calculado)'
        },
        {
            'produto': produto_mo,
            'quantidade': 0.4,  # 0.4 horas
            'custo_calculado': 2632.0,  # R$ 26.32 (0.4h * R$ 65.79/h)
            'nome_componente': 'Mão de Obra Processamento/Montagem'
        }
    ]
    
    for dados in componentes_dados:
        # Salvar custos calculados na observação
        custos_observacao = {
            'custo_unitario': int(dados['custo_calculado'] / dados['quantidade']),
            'custo_total': int(dados['custo_calculado']),
            'nome_componente': dados['nome_componente'],
            'calculated_at': '2024-01-01T12:00:00'
        }
        
        componente = ProdutoComponente.objects.create(
            produto_principal=grade,
            produto_componente=dados['produto'],
            quantidade=dados['quantidade'],
            observacao=json.dumps(custos_observacao)
        )
        
        print(f"✅ Componente criado: {dados['produto'].descricao}")
        print(f"   Quantidade: {dados['quantidade']}")
        print(f"   Custo calculado: R$ {dados['custo_calculado']/100:.2f}")
        print(f"   Observação salva com custos customizados")
    
    # 4. Verificar recálculo automático
    grade.refresh_from_db()
    print(f"\n📊 RESULTADO APÓS RECÁLCULO AUTOMÁTICO:")
    print(f"   Custo da grade: R$ {grade.custo_centavos/100:.2f}")
    print(f"   Peso da grade: {grade.peso_und} kg")
    
    # Soma manual esperada
    custo_esperado = 250.0 + 180.0 + 2632.0  # 3062 centavos = R$ 30.62
    print(f"   Custo esperado: R$ {custo_esperado/100:.2f}")
    
    if abs(grade.custo_centavos - custo_esperado) < 10:  # Tolerância de 10 centavos
        print(f"✅ SUCESSO: Custo calculado corretamente!")
    else:
        print(f"❌ ERRO: Custo incorreto. Esperado R$ {custo_esperado/100:.2f}, obtido R$ {grade.custo_centavos/100:.2f}")
    
    # 5. Verificar componentes salvos
    componentes = ProdutoComponente.objects.filter(produto_principal=grade)
    print(f"\n🔍 COMPONENTES SALVOS:")
    for comp in componentes:
        print(f"   • {comp.produto_componente.descricao}")
        print(f"     Quantidade: {comp.quantidade}")
        print(f"     Custo padrão: R$ {comp.produto_componente.custo_centavos/100:.2f}")
        
        if comp.observacao:
            try:
                custos_obs = json.loads(comp.observacao)
                custo_obs = custos_obs.get('custo_total', 0) / 100
                print(f"     Custo na observação: R$ {custo_obs:.2f}")
            except json.JSONDecodeError:
                print(f"     Observação (texto): {comp.observacao}")
        else:
            print(f"     Sem observação")
    
    return grade.id

if __name__ == '__main__':
    grade_id = criar_grade_teste()
    print(f"\n🎯 Grade criada com ID: {grade_id}")
    print("Agora teste criar uma nova grade no sistema para verificar se o problema foi resolvido!")
