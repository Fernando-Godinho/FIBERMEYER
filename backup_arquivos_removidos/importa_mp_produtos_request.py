import requests
import os

API_URL = 'http://127.0.0.1:8000/api/produtos/'
FILE_PATH = os.path.join(os.path.dirname(__file__), 'mp-produtos')

if not os.path.exists(FILE_PATH):
    print('Arquivo mp-produtos não encontrado na raiz.')
    exit(1)

with open(FILE_PATH, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # descricao;custo_centavos;peso_und;unidade;referencia
        parts = line.split(';')
        if len(parts) < 5:
            print(f'Linha ignorada (formato inválido): {line}')
            continue
        descricao, custo_centavos, peso_und, unidade, referencia = parts[:5]
        try:
            data = {
                'descricao': descricao,
                'custo_centavos': int(custo_centavos),
                'peso_und': float(peso_und),
                'unidade': unidade,
                'referencia': referencia,
                # data_revisao será preenchida automaticamente pelo backend
            }
            resp = requests.post(API_URL, json=data)
            if resp.status_code == 201:
                print(f'Produto inserido: {descricao}')
            else:
                print(f'Erro ao inserir {descricao}: {resp.text}')
        except Exception as e:
            print(f'Erro ao processar linha: {line} - {e}')
print('Importação concluída.')
