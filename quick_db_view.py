#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick DB Viewer - FIBERMEYER
Visualização rápida e simples do banco
"""

import sqlite3
import pandas as pd

def quick_view():
    """Visualização rápida do banco"""
    try:
        # Conectar ao banco
        conn = sqlite3.connect('db.sqlite3')
        print("🗄️ BANCO DE DADOS FIBERMEYER - VISÃO GERAL")
        print("=" * 60)
        
        # Listar tabelas com contadores
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"\n📊 RESUMO ({len(tables)} tabelas):")
        print("-" * 60)
        
        for table, in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📋 {table:<25} {count:>8} registros")
        
        print("\n" + "=" * 60)
        
        # Mostrar dados das tabelas principais
        main_tables = ['main_produto', 'main_componenteproduto', 'main_template', 'main_maodeobra']
        
        for table in main_tables:
            if any(t[0] == table for t in tables):
                print(f"\n📝 ÚLTIMOS REGISTROS - {table.upper()}")
                print("-" * 80)
                
                try:
                    df = pd.read_sql_query(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 5", conn)
                    if not df.empty:
                        pd.set_option('display.max_columns', None)
                        pd.set_option('display.width', None)
                        pd.set_option('display.max_colwidth', 30)
                        print(df.to_string(index=False))
                    else:
                        print("   (Tabela vazia)")
                except Exception as e:
                    print(f"   Erro ao ler tabela: {e}")
        
        conn.close()
        print(f"\n✅ Visualização concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    quick_view()
