import pandas as pd
import requests
import os

API_URL = 'http://127.0.0.1:8000/api/produtos/'
FILE_PATH = os.path.join(os.path.dirname(__file__), 'MP-PRODUTOS.xlsx')

if not os.path.exists(FILE_PATH):
    print('Arquivo MP-PRODUTOS.xlsx não encontrado na raiz.')
    exit(1)

# Lê o Excel (espera colunas: descricao, custo, unidade, referencia)
df = pd.read_excel(FILE_PATH)

for idx, row in df.iterrows():
    try:
        # Converte custo para centavos
        custo_str = str(row['custo']).replace('.', '').replace(',', '.')
        custo_centavos = int(float(custo_str) * 100)
        peso_und = row['peso_und'] if 'peso_und' in row else 0.0
        try:
            peso_und = float(peso_und)
        except:
            peso_und = 0.0
        data = {
            'descricao': str(row['descricao']),
            'custo_centavos': custo_centavos,
            'unidade': str(row['unidade']),
            'referencia': str(row['referencia']),
            'peso_und': peso_und,
        }
        resp = requests.post(API_URL, json=data)
        if resp.status_code == 201:
            print(f"Produto inserido: {data['descricao']}")
        else:
            print(f"Erro ao inserir {data['descricao']}: {resp.text}")
    except Exception as e:
        print(f"Erro na linha {idx+1}: {e}")
print('Importação concluída.')
