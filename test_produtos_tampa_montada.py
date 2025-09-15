#!/usr/bin/env python
"""
Teste para verificar se todos os produtos necessários para Tampa Montada existem
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def test_produtos_tampa_montada():
    print("=== VERIFICANDO PRODUTOS PARA TAMPA MONTADA ===\n")
    
    produtos_necessarios = [
        {
            'nome': 'Perfis I25',
            'busca': 'i25',
            'obrigatorio': True
        },
        {
            'nome': 'Perfis I32', 
            'busca': 'i32',
            'obrigatorio': True
        },
        {
            'nome': 'Perfis I38',
            'busca': 'i38', 
            'obrigatorio': True
        },
        {
            'nome': 'Perfil TRAV',
            'busca': 'trav',
            'obrigatorio': True
        },
        {
            'nome': 'Chaveta',
            'busca': 'chaveta',
            'obrigatorio': True
        },
        {
            'nome': 'Cola Estrutural',
            'busca': 'cola estrutural',
            'obrigatorio': True
        },
        {
            'nome': 'Chapa 2,5mm',
            'busca': 'chapa lisa',
            'obrigatorio': True
        },
        {
            'nome': 'Perfil U4"',
            'busca': 'u4',
            'obrigatorio': False
        },
        {
            'nome': 'Alça',
            'busca': 'alça',
            'obrigatorio': False
        },
        {
            'nome': 'Chapa EV',
            'busca': 'chapa ev',
            'obrigatorio': False
        },
        {
            'nome': 'Mão de Obra Processamento',
            'busca': 'processamento/montagem',
            'obrigatorio': True
        }
    ]
    
    todos_ok = True
    
    for item in produtos_necessarios:
        print(f"🔍 Procurando: {item['nome']} (termo: '{item['busca']}')")
        
        produtos = MP_Produtos.objects.filter(
            descricao__icontains=item['busca']
        )
        
        if produtos.exists():
            print(f"   ✅ Encontrado(s) {produtos.count()} produto(s):")
            for p in produtos[:3]:  # Mostrar apenas os primeiros 3
                print(f"      • ID {p.id}: {p.descricao} - R$ {p.custo_centavos/100:.2f}")
            if produtos.count() > 3:
                print(f"      ... e mais {produtos.count() - 3} produto(s)")
        else:
            status = "❌ NÃO ENCONTRADO" if item['obrigatorio'] else "⚠️  OPCIONAL - Não encontrado"
            print(f"   {status}")
            if item['obrigatorio']:
                todos_ok = False
        
        print()
    
    print("=" * 60)
    if todos_ok:
        print("✅ TODOS OS PRODUTOS OBRIGATÓRIOS ESTÃO DISPONÍVEIS!")
        print("   A implementação de Tampa Montada pode funcionar.")
    else:
        print("❌ ALGUNS PRODUTOS OBRIGATÓRIOS ESTÃO FALTANDO!")
        print("   Será necessário criar ou ajustar os produtos no banco.")
    
    print(f"\nTotal de produtos no banco: {MP_Produtos.objects.count()}")

if __name__ == '__main__':
    test_produtos_tampa_montada()
