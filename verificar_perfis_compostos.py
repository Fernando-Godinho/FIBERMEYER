#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar se os produtos Novo Perfil estão sendo salvos como compostos
"""

import sqlite3
import json
from datetime import datetime

def verificar_produtos_perfil():
    print("=== VERIFICAÇÃO DOS PRODUTOS NOVO PERFIL ===")
    print()
    
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('c:/Users/ferna/OneDrive/Área de Trabalho/FIBERMEYER/db.sqlite3')
        cursor = conn.cursor()
        
        # Buscar produtos que podem ser do tipo perfil
        print("🔍 Buscando produtos relacionados a perfis...")
        cursor.execute("""
            SELECT id, descricao, custo_centavos, tipo_produto, categoria, subcategoria, 
                   referencia, data_revisao, is_composto
            FROM main_mp_produtos 
            WHERE (subcategoria = 'Pultrusão' OR 
                   categoria = 'Perfis' OR 
                   descricao LIKE '%perfil%' OR
                   referencia LIKE 'PERF-%')
            ORDER BY id DESC
            LIMIT 10
        """)
        
        produtos = cursor.fetchall()
        
        if not produtos:
            print("⚠️ Nenhum produto de perfil encontrado")
            return
            
        print(f"📦 {len(produtos)} produtos de perfil encontrados:")
        print("-" * 80)
        
        for produto in produtos:
            id_prod, desc, custo, tipo_produto, categoria, subcategoria, ref, data_rev, is_composto = produto
            
            custo_reais = custo / 100 if custo else 0
            
            print(f"ID: {id_prod}")
            print(f"  Descrição: {desc}")
            print(f"  Custo: R$ {custo_reais:.2f}")
            print(f"  Tipo Produto: {tipo_produto}")
            print(f"  É Composto: {'✅ Sim' if is_composto else '❌ Não'}")
            print(f"  Categoria: {categoria}")
            print(f"  Subcategoria: {subcategoria}")
            print(f"  Referência: {ref}")
            
            # Verificar componentes se for composto
            if is_composto:
                cursor.execute("""
                    SELECT pc.quantidade, p.descricao, pc.observacao
                    FROM main_produtocomponente pc
                    JOIN main_mp_produtos p ON pc.produto_componente_id = p.id
                    WHERE pc.produto_principal_id = ?
                """, (id_prod,))
                
                componentes = cursor.fetchall()
                
                if componentes:
                    print(f"  🔧 Componentes ({len(componentes)}):")
                    for comp in componentes:
                        qtd, desc_comp, obs = comp
                        print(f"    • {desc_comp}: {qtd}")
                        if obs:
                            try:
                                obs_data = json.loads(obs)
                                if 'custo_total' in obs_data:
                                    custo_comp = obs_data['custo_total'] / 100
                                    print(f"      R$ {custo_comp:.2f}")
                            except:
                                pass
                else:
                    print(f"  ⚠️ Produto marcado como composto mas sem componentes!")
            
            print("-" * 80)
        
        # Estatísticas
        print("\n📊 ESTATÍSTICAS:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN is_composto = 1 THEN 1 ELSE 0 END) as compostos,
                SUM(CASE WHEN is_composto = 0 THEN 1 ELSE 0 END) as simples
            FROM main_mp_produtos 
            WHERE (subcategoria = 'Pultrusão' OR categoria = 'Perfis')
        """)
        
        stats = cursor.fetchone()
        total, compostos, simples = stats
        
        print(f"  Total de perfis: {total}")
        print(f"  Produtos compostos: {compostos}")
        print(f"  Produtos simples: {simples}")
        
        if simples > 0:
            print(f"  ⚠️ {simples} perfis estão salvos como produtos simples!")
        else:
            print(f"  ✅ Todos os perfis estão corretamente salvos como compostos!")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar produtos: {e}")

if __name__ == "__main__":
    verificar_produtos_perfil()