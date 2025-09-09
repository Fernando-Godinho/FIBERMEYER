#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualizador do Banco de Dados SQLite - FIBERMEYER
"""

import sqlite3
import pandas as pd
import os

def conectar_banco():
    """Conecta ao banco de dados SQLite"""
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Arquivo {db_path} não encontrado!")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ Conectado ao banco: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def listar_tabelas(conn):
    """Lista todas as tabelas do banco"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tabelas = cursor.fetchall()
        
        print("\n" + "="*60)
        print("📊 TABELAS DO BANCO DE DADOS")
        print("="*60)
        
        for i, (tabela,) in enumerate(tabelas, 1):
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            print(f"{i:2d}. {tabela:<30} ({count} registros)")
        
        return [t[0] for t in tabelas]
    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")
        return []

def mostrar_estrutura_tabela(conn, tabela):
    """Mostra a estrutura de uma tabela"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = cursor.fetchall()
        
        print(f"\n📋 ESTRUTURA DA TABELA: {tabela}")
        print("-" * 80)
        print(f"{'Campo':<25} {'Tipo':<15} {'Nulo':<8} {'Chave':<8} {'Padrão':<15}")
        print("-" * 80)
        
        for col in colunas:
            cid, name, type_, notnull, default_value, pk = col
            nulo = "NÃO" if notnull else "SIM"
            chave = "PK" if pk else ""
            padrao = str(default_value) if default_value is not None else ""
            print(f"{name:<25} {type_:<15} {nulo:<8} {chave:<8} {padrao:<15}")
        
    except Exception as e:
        print(f"❌ Erro ao mostrar estrutura: {e}")

def mostrar_dados_tabela(conn, tabela, limit=10):
    """Mostra os dados de uma tabela"""
    try:
        df = pd.read_sql_query(f"SELECT * FROM {tabela} LIMIT {limit}", conn)
        
        if df.empty:
            print(f"\n📝 TABELA {tabela} - VAZIA")
            return
        
        print(f"\n📝 DADOS DA TABELA: {tabela} (primeiros {limit} registros)")
        print("-" * 100)
        
        # Configurar pandas para mostrar todas as colunas
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)
        
        print(df.to_string(index=False))
        
        # Mostrar total de registros
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        total = cursor.fetchone()[0]
        print(f"\nTotal de registros na tabela: {total}")
        
    except Exception as e:
        print(f"❌ Erro ao mostrar dados: {e}")

def menu_principal():
    """Menu principal interativo"""
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        while True:
            print("\n" + "="*60)
            print("🗄️  VISUALIZADOR DO BANCO FIBERMEYER")
            print("="*60)
            print("1. Listar todas as tabelas")
            print("2. Ver estrutura de uma tabela")
            print("3. Ver dados de uma tabela")
            print("4. Consulta personalizada")
            print("5. Relatório completo")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "0":
                print("👋 Saindo...")
                break
            
            elif opcao == "1":
                tabelas = listar_tabelas(conn)
            
            elif opcao == "2":
                tabelas = listar_tabelas(conn)
                if tabelas:
                    nome_tabela = input("\nDigite o nome da tabela: ").strip()
                    if nome_tabela in tabelas:
                        mostrar_estrutura_tabela(conn, nome_tabela)
                    else:
                        print("❌ Tabela não encontrada!")
            
            elif opcao == "3":
                tabelas = listar_tabelas(conn)
                if tabelas:
                    nome_tabela = input("\nDigite o nome da tabela: ").strip()
                    if nome_tabela in tabelas:
                        try:
                            limit = int(input("Quantos registros mostrar? (padrão 10): ") or "10")
                        except:
                            limit = 10
                        mostrar_dados_tabela(conn, nome_tabela, limit)
                    else:
                        print("❌ Tabela não encontrada!")
            
            elif opcao == "4":
                sql = input("\nDigite sua consulta SQL: ").strip()
                if sql:
                    executar_consulta_personalizada(conn, sql)
            
            elif opcao == "5":
                gerar_relatorio_completo(conn)
            
            else:
                print("❌ Opção inválida!")
                
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário")
    finally:
        conn.close()
        print("🔒 Conexão com o banco fechada")

def executar_consulta_personalizada(conn, sql):
    """Executa uma consulta SQL personalizada"""
    try:
        df = pd.read_sql_query(sql, conn)
        
        if df.empty:
            print("📝 Consulta retornou resultado vazio")
            return
        
        print(f"\n📊 RESULTADO DA CONSULTA:")
        print("-" * 100)
        print(df.to_string(index=False))
        
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")

def gerar_relatorio_completo(conn):
    """Gera um relatório completo do banco"""
    print("\n" + "="*80)
    print("📊 RELATÓRIO COMPLETO DO BANCO DE DADOS")
    print("="*80)
    
    tabelas = listar_tabelas(conn)
    
    for tabela in tabelas:
        print(f"\n{'='*20} {tabela.upper()} {'='*20}")
        mostrar_estrutura_tabela(conn, tabela)
        mostrar_dados_tabela(conn, tabela, 5)  # Mostra apenas 5 registros por tabela

if __name__ == "__main__":
    print("🗄️ VISUALIZADOR DO BANCO FIBERMEYER")
    print("Certifique-se de que o arquivo db.sqlite3 esteja no mesmo diretório")
    menu_principal()
