#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def verificar_produtos_recentes():
    print("=== VERIFICAÇÃO DE PRODUTOS COMPOSTOS RECENTES ===")
    print()
    
    # Verificar produtos compostos criados
    produtos_compostos = MP_Produtos.objects.filter(tipo_produto='composto').order_by('-id')[:5]
    
    for produto in produtos_compostos:
        print(f"🏗️  PRODUTO ID {produto.id}: {produto.descricao}")
        print(f"├─ Custo Salvo: R$ {(produto.custo_centavos/100):.2f}")
        print(f"├─ Referência: {produto.referencia or 'N/A'}")
        print(f"├─ Data: {produto.data_revisao}")
        
        # Verificar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=produto)
        if componentes:
            print(f"├─ Componentes ({componentes.count()}):")
            custo_componentes_total = 0
            for comp in componentes:
                custo_unit = comp.produto_componente.custo_centavos / 100
                custo_total_comp = custo_unit * float(comp.quantidade)
                custo_componentes_total += custo_total_comp
                print(f"│  ├─ {comp.produto_componente.descricao[:40]}... × {comp.quantidade}")
                print(f"│  │  └─ R$ {custo_unit:.2f} × {comp.quantidade} = R$ {custo_total_comp:.2f}")
            
            print(f"├─ Custo Total dos Componentes: R$ {custo_componentes_total:.2f}")
            
            # Comparar com custo salvo
            custo_salvo = produto.custo_centavos / 100
            if abs(custo_salvo - custo_componentes_total) > 0.01:
                diferenca = custo_salvo - custo_componentes_total
                percentual_diferenca = (diferenca / custo_componentes_total) * 100
                print(f"├─ ⚠️  DIFERENÇA DETECTADA: R$ {diferenca:.2f} ({percentual_diferenca:.1f}%)")
                print(f"│  └─ Possível aplicação de perda ou margem")
            else:
                print(f"├─ ✅ Custo salvo = custo dos componentes")
        else:
            print(f"├─ ❌ Nenhum componente encontrado")
        
        print("└" + "─" * 60)
        print()

    print("📋 INSTRUÇÕES PARA TESTE:")
    print("1. Abra o navegador em http://127.0.0.1:8000/mp/")
    print("2. Vá para a aba 'Produto Composto'")
    print("3. Adicione alguns componentes")
    print("4. Defina um percentual de perda (ex: 10%)")
    print("5. Salve o produto")
    print("6. Execute este script novamente para verificar")

if __name__ == '__main__':
    verificar_produtos_recentes()