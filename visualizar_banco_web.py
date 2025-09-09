#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualizador Web do Banco SQLite - FIBERMEYER
Execute este arquivo e acesse http://localhost:5001
"""

from flask import Flask, render_template_string, request
import sqlite3
import pandas as pd
import json

app = Flask(__name__)

def get_db_connection():
    """Conecta ao banco SQLite"""
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def get_tables():
    """Retorna lista de tabelas"""
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    conn.close()
    return [table['name'] for table in tables]

def get_table_info(table_name):
    """Retorna informações da tabela"""
    conn = get_db_connection()
    info = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    count = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}").fetchone()
    conn.close()
    return info, count['count']

def get_table_data(table_name, limit=50):
    """Retorna dados da tabela"""
    conn = get_db_connection()
    data = conn.execute(f"SELECT * FROM {table_name} LIMIT {limit}").fetchall()
    conn.close()
    return data

# Template HTML
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizador DB - FIBERMEYER</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .table-container { max-height: 600px; overflow-y: auto; }
        .sidebar { min-height: 100vh; background-color: #f8f9fa; }
        .table-info { background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        pre { max-height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-3 col-lg-2 d-md-block sidebar p-3">
                <h4 class="text-primary"><i class="fas fa-database"></i> FIBERMEYER DB</h4>
                <hr>
                <div class="mb-3">
                    <h6>📊 Tabelas ({{ tables|length }})</h6>
                    <div class="list-group">
                        {% for table in tables %}
                        <a href="/?table={{ table }}" 
                           class="list-group-item list-group-item-action {% if selected_table == table %}active{% endif %}">
                            <i class="fas fa-table"></i> {{ table }}
                        </a>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="mb-3">
                    <h6>🔍 Consulta SQL</h6>
                    <form method="POST" action="/query">
                        <textarea name="sql" class="form-control" rows="4" placeholder="SELECT * FROM ..."></textarea>
                        <button type="submit" class="btn btn-primary btn-sm mt-2">
                            <i class="fas fa-play"></i> Executar
                        </button>
                    </form>
                </div>
            </nav>
            
            <!-- Main Content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">
                        {% if selected_table %}
                            <i class="fas fa-table"></i> {{ selected_table }}
                        {% else %}
                            <i class="fas fa-home"></i> Dashboard
                        {% endif %}
                    </h1>
                </div>
                
                {% if selected_table %}
                    <!-- Table Info -->
                    <div class="table-info">
                        <div class="row">
                            <div class="col-md-6">
                                <h5><i class="fas fa-info-circle"></i> Informações</h5>
                                <p><strong>Tabela:</strong> {{ selected_table }}</p>
                                <p><strong>Registros:</strong> {{ record_count }}</p>
                                <p><strong>Colunas:</strong> {{ table_info|length }}</p>
                            </div>
                            <div class="col-md-6">
                                <h5><i class="fas fa-columns"></i> Estrutura</h5>
                                <div style="max-height: 200px; overflow-y: auto;">
                                    {% for col in table_info %}
                                    <span class="badge bg-secondary me-1 mb-1">
                                        {{ col[1] }} ({{ col[2] }})
                                        {% if col[5] %}<i class="fas fa-key text-warning"></i>{% endif %}
                                    </span>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Table Data -->
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-list"></i> Dados (primeiros 50 registros)</h5>
                        </div>
                        <div class="card-body p-0">
                            <div class="table-container">
                                <table class="table table-striped table-hover mb-0">
                                    <thead class="table-dark sticky-top">
                                        <tr>
                                            {% for col in table_info %}
                                            <th>{{ col[1] }}{% if col[5] %} <i class="fas fa-key text-warning"></i>{% endif %}</th>
                                            {% endfor %}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for row in table_data %}
                                        <tr>
                                            {% for value in row %}
                                            <td title="{{ value }}">
                                                {% if value and value|string|length > 50 %}
                                                    {{ value|string|truncate(50) }}
                                                {% else %}
                                                    {{ value }}
                                                {% endif %}
                                            </td>
                                            {% endfor %}
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                {% elif query_result is defined %}
                    <!-- Query Result -->
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-search"></i> Resultado da Consulta</h5>
                        </div>
                        <div class="card-body">
                            {% if query_error %}
                                <div class="alert alert-danger">
                                    <i class="fas fa-exclamation-triangle"></i> {{ query_error }}
                                </div>
                            {% else %}
                                <div class="table-container">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                {% for col in query_result.columns %}
                                                <th>{{ col }}</th>
                                                {% endfor %}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {% for row in query_result.values %}
                                            <tr>
                                                {% for value in row %}
                                                <td>{{ value }}</td>
                                                {% endfor %}
                                            </tr>
                                            {% endfor %}
                                        </tbody>
                                    </table>
                                </div>
                                <p class="text-muted">
                                    {% if query_result is defined and query_result.values is defined %}
                                        {{ query_result.values|length }} registros retornados
                                    {% else %}
                                        Consulta executada
                                    {% endif %}
                                </p>
                            {% endif %}
                        </div>
                    </div>
                    
                {% else %}
                    <!-- Dashboard -->
                    <div class="row">
                        {% for table in tables %}
                        <div class="col-md-4 mb-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <i class="fas fa-table"></i> {{ table }}
                                    </h5>
                                    <p class="card-text">
                                        {% set ns = namespace() %}
                                        {% set ns.count = 0 %}
                                        {% for t, c in table_counts %}
                                            {% if t == table %}
                                                {% set ns.count = c %}
                                            {% endif %}
                                        {% endfor %}
                                        <span class="badge bg-primary">{{ ns.count }} registros</span>
                                    </p>
                                    <a href="/?table={{ table }}" class="btn btn-primary btn-sm">
                                        <i class="fas fa-eye"></i> Visualizar
                                    </a>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                {% endif %}
            </main>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    tables = get_tables()
    selected_table = request.args.get('table')
    
    # Contar registros de todas as tabelas para o dashboard
    table_counts = []
    for table in tables:
        _, count = get_table_info(table)
        table_counts.append((table, count))
    
    if selected_table:
        table_info, record_count = get_table_info(selected_table)
        table_data = get_table_data(selected_table)
        
        return render_template_string(HTML_TEMPLATE,
                                    tables=tables,
                                    selected_table=selected_table,
                                    table_info=table_info,
                                    table_data=table_data,
                                    record_count=record_count,
                                    table_counts=table_counts)
    
    return render_template_string(HTML_TEMPLATE,
                                tables=tables,
                                table_counts=table_counts)

@app.route('/query', methods=['POST'])
def query():
    tables = get_tables()
    sql = request.form.get('sql', '').strip()
    
    if not sql:
        return render_template_string(HTML_TEMPLATE,
                                    tables=tables,
                                    query_error="Consulta SQL vazia")
    
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(sql, conn)
        conn.close()
        
        return render_template_string(HTML_TEMPLATE,
                                    tables=tables,
                                    query_result=df)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
                                    tables=tables,
                                    query_error=str(e))

if __name__ == '__main__':
    print("🌐 Iniciando visualizador web do banco...")
    print("📱 Acesse: http://localhost:5001")
    print("⏹️  Para parar: Ctrl+C")
    app.run(debug=True, port=5001, host='0.0.0.0')
