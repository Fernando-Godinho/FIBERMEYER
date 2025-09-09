import sqlite3

DB_PATH = 'db.sqlite3'
TABLE = 'main_orcamento'  # Nome da tabela no banco SQLite

# Altere aqui o campo, valor e id desejado:
CAMPO = 'uf'
NOVO_VALOR = 'RJ'
ID = 2

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Apenas imprime todos os registros da tabela, sem alterar valores

    # Imprime todos os registros da tabela
    cursor.execute(f"SELECT * FROM {TABLE}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()
