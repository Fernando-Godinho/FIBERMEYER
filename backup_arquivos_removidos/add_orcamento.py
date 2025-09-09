import sqlite3
from datetime import datetime

DB_PATH = 'db.sqlite3'
TABLE = 'main_orcamento'

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now()
    data = (
        '2025-08-03',   # validade
        'Novo Cliente 2', # cliente
        'SP',           # uf
        'Contato Teste',# contato
        '11999999999',  # telefone
        'teste@exemplo.com', # email
        0.0,            # frete
        0.0,            # instalacao
        'Indústria',    # venda_destinada
        1,              # cliente_contrib_icms
        '12.345.678/0001-99', # cnpj_faturamento
        18.0,           # icms
        'Rascunho',     # status
        'Observação teste', # observacoes
        1000.0,         # total_bruto
        0.0,            # desconto_total
        180.0,          # imposto_total
        820.0,          # total_liquido
        1,              # revisao
        now.strftime('%Y-%m-%d %H:%M:%S'), # criado_em
        now.strftime('%Y-%m-%d %H:%M:%S'), # atualizado_em
        'ORC-TESTE-001' # numero_orcamento
    )

    cursor.execute(f'''
        INSERT INTO {TABLE} (
            validade, cliente, uf, contato, telefone, email, frete, instalacao, venda_destinada,
            cliente_contrib_icms, cnpj_faturamento, icms, status, observacoes, total_bruto,
            desconto_total, imposto_total, total_liquido, revisao, criado_em, atualizado_em, numero_orcamento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

    print('Orçamento inserido com sucesso!')

    conn.close()

def listar_orcamentos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Busca todos os registros da tabela de orçamentos
    cursor.execute(f"SELECT * FROM {TABLE}")
    rows = cursor.fetchall()

    # Imprime os registros
    print("Itens da tabela de orçamentos:")
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()
    listar_orcamentos()
