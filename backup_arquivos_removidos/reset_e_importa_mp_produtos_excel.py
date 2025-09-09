import pandas as pd
import requests
import os

API_URL = 'http://127.0.0.1:8000/api/produtos/'
FILE_PATH = os.path.join(os.path.dirname(__file__), 'MP-PRODUTOS.xlsx')

# 1. Deleta todos os produtos existentes
print('Deletando todos os produtos...')
resp = requests.get(API_URL)
if resp.status_code == 200:
    produtos = resp.json()
    for produto in produtos:
        del_resp = requests.delete(f"{API_URL}{produto['id']}/")
        if del_resp.status_code == 204:
            print(f"Deletado: {produto['descricao']}")
        else:
            print(f"Erro ao deletar {produto['descricao']}: {del_resp.text}")
else:
    print('Erro ao buscar produtos para deletar:', resp.text)

# 2. Reinsere os produtos do Excel
if not os.path.exists(FILE_PATH):
    print('Arquivo MP-PRODUTOS.xlsx não encontrado na raiz.')
    exit(1)

df = pd.read_excel(FILE_PATH)
print('Incluindo produtos do Excel...')
for idx, row in df.iterrows():
    try:
        custo_raw = str(row['custo']).strip()
        # Se tem vírgula ou ponto, é valor em reais, multiplica por 100
        if ',' in custo_raw or '.' in custo_raw:
            custo_str = custo_raw.replace('.', '').replace(',', '.')
            custo_centavos = int(float(custo_str) * 100)
        else:
            # Se não tem vírgula/ponto e tem 5 ou 6 dígitos, já está em centavos
            try:
                custo_centavos = int(custo_raw)
            except:
                custo_centavos = 0
        peso_und = row['peso'] if 'peso' in row else 0.0
        try:
            peso_und = float(peso_und)
        except:
            peso_und = 0.0
        from datetime import datetime
        now = datetime.now()
        pad = lambda n: str(n).zfill(2)
        data_revisao = f"{pad(now.day)}/{pad(now.month)}/{now.year} {pad(now.hour)}:{pad(now.minute)}:{pad(now.second)}"
        data = {
            'descricao': str(row['descricao']),
            'custo_centavos': custo_centavos,
            'unidade': str(row['unidade']),
            'referencia': str(row['referencia']),
            'peso_und': peso_und,
            'data_revisao': data_revisao,
        }
        resp = requests.post(API_URL, json=data)
        if resp.status_code == 201:
            print(f"Produto inserido: {data['descricao']}, {data['peso_und']}")
        else:
            print(f"Erro ao inserir {data['descricao']}: {resp.text}")
    except Exception as e:
        print(f"Erro na linha {idx+1}: {e}")
print('Processo concluído.')
