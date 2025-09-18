#!/usr/bin/env python3
"""
Teste para verificar se o salvamento da tampa montada está funcionando corretamente
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def teste_tampa_montada_salvamento():
    print("=== TESTE DE SALVAMENTO DA TAMPA MONTADA ===")
    
    # 1. Verificar se os produtos necessários existem
    print("\n1. Verificando produtos necessários...")
    
    # Perfis I25, I32, I38
    perfis = MP_Produtos.objects.filter(
        descricao__icontains='I25'
    ).union(
        MP_Produtos.objects.filter(descricao__icontains='I32')
    ).union(
        MP_Produtos.objects.filter(descricao__icontains='I38')
    )
    
    print(f"   Perfis I25/I32/I38 encontrados: {perfis.count()}")
    
    # Chaveta
    chaveta = MP_Produtos.objects.filter(id=1332).first()
    print(f"   Chaveta (ID 1332): {'✅ Encontrada' if chaveta else '❌ Não encontrada'}")
    
    # Cola estrutural
    cola = MP_Produtos.objects.filter(id=1183).first()
    print(f"   Cola estrutural (ID 1183): {'✅ Encontrada' if cola else '❌ Não encontrada'}")
    
    # Chapa 2,5mm
    chapa_25 = MP_Produtos.objects.filter(
        descricao__icontains='chapa'
    ).filter(
        descricao__icontains='2,5'
    ).first()
    print(f"   Chapa 2,5mm: {'✅ Encontrada' if chapa_25 else '❌ Não encontrada'}")
    
    # Mão de obra
    mao_obra = MP_Produtos.objects.filter(
        descricao__icontains='mão de obra'
    ).filter(
        descricao__icontains='processamento'
    ).first()
    print(f"   Mão de obra processamento: {'✅ Encontrada' if mao_obra else '❌ Não encontrada'}")
    
    # 2. Verificar produtos compostos existentes (tampas montadas)
    print("\n2. Verificando produtos compostos existentes...")
    
    tampas_montadas = MP_Produtos.objects.filter(
        is_composto=True,
        descricao__icontains='tampa'
    )
    
    print(f"   Tampas montadas existentes: {tampas_montadas.count()}")
    
    if tampas_montadas.exists():
        print("   Últimas tampas montadas:")
        for tampa in tampas_montadas.order_by('-id')[:3]:
            componentes_count = ProdutoComponente.objects.filter(produto_principal=tampa).count()
            print(f"     • ID {tampa.id}: {tampa.descricao}")
            print(f"       Custo: R$ {tampa.custo_centavos/100:.2f} | Componentes: {componentes_count}")
    
    # 3. Verificar se há componentes duplicados em algum produto
    print("\n3. Verificando componentes duplicados...")
    
    from django.db.models import Count
    
    duplicados = ProdutoComponente.objects.values(
        'produto_principal', 'produto_componente'
    ).annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    if duplicados.exists():
        print(f"   ❌ Encontrados {duplicados.count()} conjuntos de componentes duplicados:")
        for dup in duplicados[:5]:
            produto_principal = MP_Produtos.objects.get(id=dup['produto_principal'])
            produto_componente = MP_Produtos.objects.get(id=dup['produto_componente'])
            print(f"     • Produto: {produto_principal.descricao}")
            print(f"       Componente duplicado: {produto_componente.descricao} ({dup['count']}x)")
    else:
        print("   ✅ Nenhum componente duplicado encontrado")
    
    # 4. Testar criação de uma tampa montada simples
    print("\n4. Testando criação de tampa montada de teste...")
    
    try:
        # Criar produto principal
        tampa_teste = MP_Produtos.objects.create(
            descricao="Tampa Montada TESTE - 1000x500mm",
            custo_centavos=50000,  # R$ 500,00
            peso_und=15.500,
            unidade='m²',
            referencia='TAMPA-TESTE-001',
            is_composto=True
        )
        
        print(f"   ✅ Tampa teste criada: ID {tampa_teste.id}")
        
        # Adicionar componentes de teste
        componentes_teste = []
        
        if perfis.exists():
            perfil = perfis.first()
            componente1 = ProdutoComponente.objects.create(
                produto_principal=tampa_teste,
                produto_componente=perfil,
                quantidade=5.250
            )
            componentes_teste.append(componente1)
            print(f"     • Componente 1: {perfil.descricao}")
        
        if chaveta:
            componente2 = ProdutoComponente.objects.create(
                produto_principal=tampa_teste,
                produto_componente=chaveta,
                quantidade=2.000
            )
            componentes_teste.append(componente2)
            print(f"     • Componente 2: {chaveta.descricao}")
        
        if cola:
            componente3 = ProdutoComponente.objects.create(
                produto_principal=tampa_teste,
                produto_componente=cola,
                quantidade=0.100
            )
            componentes_teste.append(componente3)
            print(f"     • Componente 3: {cola.descricao}")
        
        print(f"   ✅ {len(componentes_teste)} componentes adicionados")
        
        # Verificar se foi salvo corretamente
        componentes_salvos = ProdutoComponente.objects.filter(produto_principal=tampa_teste)
        print(f"   ✅ Componentes verificados no banco: {componentes_salvos.count()}")
        
        # Limpar teste
        print("   🧹 Removendo dados de teste...")
        componentes_salvos.delete()
        tampa_teste.delete()
        print("   ✅ Limpeza concluída")
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    teste_tampa_montada_salvamento()
