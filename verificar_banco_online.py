#!/usr/bin/env python3
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, Orcamento, Imposto

print("🔍 Verificando dados no banco online...")

try:
    # Contar produtos
    produtos_count = MP_Produtos.objects.count()
    print(f"📦 Produtos: {produtos_count}")
    
    # Contar orçamentos
    orcamentos_count = Orcamento.objects.count()
    print(f"💰 Orçamentos: {orcamentos_count}")
    
    # Contar impostos
    impostos_count = Imposto.objects.count()
    print(f"📊 Impostos: {impostos_count}")
    
    if produtos_count > 0 or orcamentos_count > 0:
        print("✅ Dados encontrados! Migração bem-sucedida!")
        
        # Mostrar alguns produtos de exemplo
        if produtos_count > 0:
            print("\n📦 Produtos de exemplo:")
            for produto in MP_Produtos.objects.all()[:5]:
                print(f"   - {produto.descricao}")
        
        # Mostrar alguns orçamentos de exemplo
        if orcamentos_count > 0:
            print("\n💰 Orçamentos de exemplo:")
            for orcamento in Orcamento.objects.all()[:3]:
                print(f"   - Orçamento #{orcamento.id}")
                
    else:
        print("⚠️ Nenhum dado encontrado. Pode ser que:")
        print("   1. O banco ainda esteja vazio")
        print("   2. A migração não funcionou")
        print("   3. O container ainda esteja inicializando")
        
except Exception as e:
    print(f"❌ Erro ao verificar dados: {e}")
    sys.exit(1)
