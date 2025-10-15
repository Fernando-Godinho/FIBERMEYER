#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para testar se o perfil está sendo salvo corretamente como composto
"""

import sqlite3
import json
from datetime import datetime

def testar_ultimo_perfil():
    print("=== TESTE DO ÚLTIMO PERFIL CRIADO ===")
    print()
    
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('c:/Users/ferna/OneDrive/Área de Trabalho/FIBERMEYER/db.sqlite3')
        cursor = conn.cursor()
        
        # Buscar o último produto criado
        print("🔍 Buscando último produto criado...")
        cursor.execute("""
            SELECT id, descricao, custo_centavos, tipo_produto, is_composto, 
                   categoria, subcategoria, referencia, data_revisao
            FROM main_mp_produtos 
            ORDER BY id DESC
            LIMIT 1
        """)
        
        produto = cursor.fetchone()
        
        if not produto:
            print("⚠️ Nenhum produto encontrado")
            return
            
        id_prod, desc, custo, tipo_produto, is_composto, categoria, subcategoria, ref, data_rev = produto
        custo_reais = custo / 100 if custo else 0
        
        print(f"📦 ÚLTIMO PRODUTO CRIADO:")
        print(f"  ID: {id_prod}")
        print(f"  Descrição: {desc}")
        print(f"  Custo: R$ {custo_reais:.2f}")
        print(f"  Tipo Produto: {tipo_produto}")
        print(f"  É Composto: {'✅ SIM' if is_composto else '❌ NÃO'}")
        print(f"  Categoria: {categoria}")
        print(f"  Subcategoria: {subcategoria}")
        print(f"  Referência: {ref}")
        print()
        
        # Verificar componentes
        cursor.execute("""
            SELECT pc.quantidade, p.descricao, pc.observacao
            FROM main_produtocomponente pc
            JOIN main_mp_produtos p ON pc.produto_componente_id = p.id
            WHERE pc.produto_principal_id = ?
            ORDER BY pc.id
        """, (id_prod,))
        
        componentes = cursor.fetchall()
        
        if componentes:
            print(f"🔧 COMPONENTES ({len(componentes)}):")
            total_custo_componentes = 0
            
            for i, comp in enumerate(componentes, 1):
                qtd, desc_comp, obs = comp
                
                print(f"  {i}. {desc_comp}")
                print(f"     Quantidade: {qtd}")
                
                if obs:
                    try:
                        obs_data = json.loads(obs)
                        if 'custo_total' in obs_data:
                            custo_comp = obs_data['custo_total'] / 100
                            total_custo_componentes += custo_comp
                            print(f"     Custo total: R$ {custo_comp:.2f}")
                        if 'custo_unitario' in obs_data:
                            custo_unit = obs_data['custo_unitario'] / 100
                            print(f"     Custo unitário: R$ {custo_unit:.2f}")
                    except Exception as e:
                        print(f"     Observação: {obs[:50]}...")
                
                print()
            
            print(f"💰 TOTAL DOS COMPONENTES: R$ {total_custo_componentes:.2f}")
            print(f"💰 CUSTO DO PRODUTO: R$ {custo_reais:.2f}")
            
            diferenca = abs(total_custo_componentes - custo_reais)
            if diferenca < 0.01:
                print("✅ Custos batem perfeitamente!")
            else:
                print(f"⚠️ Diferença de R$ {diferenca:.2f}")
                
        else:
            if is_composto:
                print("❌ ERRO: Produto marcado como composto mas sem componentes!")
            else:
                print("ℹ️ Produto simples - sem componentes")
        
        # Verificar últimos 3 produtos para contexto
        print("\n" + "="*60)
        print("📋 ÚLTIMOS 3 PRODUTOS PARA CONTEXTO:")
        
        cursor.execute("""
            SELECT id, descricao, tipo_produto, is_composto
            FROM main_mp_produtos 
            ORDER BY id DESC
            LIMIT 3
        """)
        
        ultimos = cursor.fetchall()
        for prod in ultimos:
            id_p, desc_p, tipo_p, composto_p = prod
            status = "✅ Composto" if composto_p else "❌ Simples"
            print(f"  ID {id_p}: {desc_p[:40]}... | {tipo_p} | {status}")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar produto: {e}")

if __name__ == "__main__":
    testar_ultimo_perfil()