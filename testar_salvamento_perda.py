#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def testar_salvamento_com_perda():
    print("=== TESTE DE SALVAMENTO COM PERCENTUAL DE PERDA ===")
    print()
    
    # Verificar produtos compostos recentes
    produtos_compostos = MP_Produtos.objects.filter(tipo_produto='composto').order_by('-id')[:5]
    
    print("🔍 PRODUTOS COMPOSTOS MAIS RECENTES:")
    if not produtos_compostos:
        print("❌ Nenhum produto composto encontrado")
        return
        
    for produto in produtos_compostos:
        custo_reais = produto.custo_centavos / 100 if produto.custo_centavos else 0
        print(f"├─ ID {produto.id}: {produto.descricao}")
        print(f"│  ├─ Custo: R$ {custo_reais:.2f}")
        print(f"│  ├─ Referência: {produto.referencia or 'N/A'}")
        print(f"│  └─ Template: {produto.template[:100] if produto.template else 'N/A'}...")
        
        # Analisar template se existir
        if produto.template:
            try:
                import json
                template_data = json.loads(produto.template)
                
                if 'percentual_perda' in template_data:
                    percentual = template_data.get('percentual_perda', 0)
                    custo_base = template_data.get('custo_base', 0)
                    valor_perda = template_data.get('valor_perda', 0)
                    
                    print(f"│      ├─ 📊 ANÁLISE DE PERDA:")
                    print(f"│      ├─ Percentual: {percentual}%")
                    print(f"│      ├─ Custo Base: R$ {custo_base:.2f}")
                    print(f"│      ├─ Valor Perda: R$ {valor_perda:.2f}")
                    print(f"│      ├─ Total Calculado: R$ {(custo_base + valor_perda):.2f}")
                    print(f"│      └─ Total Salvo: R$ {custo_reais:.2f}")
                    
                    # Verificar se o cálculo está correto
                    total_esperado = custo_base + valor_perda
                    diferenca = abs(total_esperado - custo_reais)
                    
                    if diferenca < 0.01:  # Diferença menor que 1 centavo
                        print(f"│      ✅ CÁLCULO CORRETO (diferença: R$ {diferenca:.4f})")
                    else:
                        print(f"│      ❌ CÁLCULO INCORRETO (diferença: R$ {diferenca:.2f})")
                else:
                    print(f"│      ⚠️  Template sem dados de perda")
                    
            except json.JSONDecodeError:
                print(f"│      ❌ Template JSON inválido")
        print()
    
    # Verificar componentes do produto mais recente
    if produtos_compostos:
        produto_recente = produtos_compostos[0]
        componentes = ProdutoComponente.objects.filter(produto_principal=produto_recente)
        
        print(f"🔗 COMPONENTES DO PRODUTO {produto_recente.id}:")
        if componentes:
            custo_componentes = 0
            for comp in componentes:
                produto_comp = comp.produto_componente
                custo_unit = produto_comp.custo_centavos / 100 if produto_comp.custo_centavos else 0
                custo_total_comp = custo_unit * comp.quantidade
                custo_componentes += custo_total_comp
                
                print(f"├─ {produto_comp.descricao} x{comp.quantidade}")
                print(f"│  └─ R$ {custo_unit:.2f} × {comp.quantidade} = R$ {custo_total_comp:.2f}")
            
            print(f"└─ TOTAL DOS COMPONENTES: R$ {custo_componentes:.2f}")
            
            # Comparar com o template
            if produto_recente.template:
                try:
                    template_data = json.loads(produto_recente.template)
                    custo_base_template = template_data.get('custo_base', 0)
                    print(f"├─ CUSTO BASE NO TEMPLATE: R$ {custo_base_template:.2f}")
                    
                    diferenca_base = abs(custo_componentes - custo_base_template)
                    if diferenca_base < 0.01:
                        print(f"└─ ✅ CUSTO BASE CORRETO")
                    else:
                        print(f"└─ ❌ CUSTO BASE INCORRETO (diferença: R$ {diferenca_base:.2f})")
                except:
                    pass
        else:
            print("├─ ❌ Nenhum componente encontrado")
        print()
    
    print("🛠️  PONTOS DE VERIFICAÇÃO:")
    print("├─ 1. JavaScript calcula corretamente o custo com perda?")
    print("├─ 2. O valor é convertido corretamente para centavos?")
    print("├─ 3. O template JSON contém os dados de perda?")
    print("├─ 4. O custo final salvo corresponde ao calculado?")
    print("└─ 5. Os componentes estão sendo salvos corretamente?")

if __name__ == '__main__':
    testar_salvamento_com_perda()