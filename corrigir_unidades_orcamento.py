#!/usr/bin/env python3
"""
Script para corrigir as unidades dos itens de orçamento
baseado na unidade do produto relacionado na base MP
"""

import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import OrcamentoItem

def corrigir_unidades_orcamento():
    """Corrige as unidades dos itens de orçamento baseado no produto relacionado"""
    
    print("🔧 CORREÇÃO DE UNIDADES DOS ITENS DE ORÇAMENTO")
    print("=" * 60)
    
    # Buscar todos os itens de orçamento que têm produto relacionado
    itens_com_produto = OrcamentoItem.objects.filter(produto__isnull=False).select_related('produto')
    
    print(f"📊 Encontrados {itens_com_produto.count()} itens com produto relacionado")
    
    contador_atualizados = 0
    contador_erros = 0
    
    for item in itens_com_produto:
        try:
            unidade_atual = item.unidade
            unidade_produto = item.produto.unidade
            
            if unidade_atual != unidade_produto:
                print(f"🔄 Item {item.id}: '{item.descricao[:50]}...'")
                print(f"   Unidade atual: {unidade_atual} → Nova unidade: {unidade_produto}")
                
                # Atualizar a unidade
                item.unidade = unidade_produto
                item.save()
                
                contador_atualizados += 1
            else:
                print(f"✅ Item {item.id}: Unidade já correta ({unidade_atual})")
                
        except Exception as e:
            print(f"❌ Erro ao processar item {item.id}: {e}")
            contador_erros += 1
    
    print("\n" + "=" * 60)
    print("📈 RESUMO DA CORREÇÃO:")
    print(f"✅ Itens atualizados: {contador_atualizados}")
    print(f"✅ Itens já corretos: {itens_com_produto.count() - contador_atualizados - contador_erros}")
    print(f"❌ Erros encontrados: {contador_erros}")
    
    # Verificar itens sem produto relacionado
    itens_sem_produto = OrcamentoItem.objects.filter(produto__isnull=True)
    if itens_sem_produto.exists():
        print(f"\n⚠️  ATENÇÃO: {itens_sem_produto.count()} itens sem produto relacionado")
        print("   Estes itens manterão a unidade 'UN' como padrão")
        
        for item in itens_sem_produto[:5]:  # Mostrar apenas os primeiros 5
            print(f"   • Item {item.id}: {item.descricao[:50]}... (Unidade: {item.unidade})")
        
        if itens_sem_produto.count() > 5:
            print(f"   ... e mais {itens_sem_produto.count() - 5} itens")

if __name__ == "__main__":
    corrigir_unidades_orcamento()
    print("\n🎉 Correção de unidades concluída!")