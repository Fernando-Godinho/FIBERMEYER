import os
import django
import requests
import json

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

# Dados de teste
dados_teste = {
    "tipo_calculo": "tampa_injetada",
    "nome_tampa": "Tampa Teste 50x40cm",
    "largura": 500,
    "comprimento": 400,
    "perda": 5,
    "grade_tipo": "GI25X38X38MM",
    "chapa_ev": True,
    "quadro_u4": True,
    "alca": False,
    "tempo_proc": 1.5,
    "tempo_mtg": 1.0
}

try:
    response = requests.post('http://localhost:8000/api/calcular_grade/', json=dados_teste, timeout=10)
    if response.status_code == 200:
        resultado = response.json()
        print('✅ Tampa Injetada funcionando!')
        print('💰 Total: R$', resultado['custo_total']/100)
        print('\n🧩 Componentes com descrições:')
        for i, comp in enumerate(resultado['componentes']):
            print(f"{i+1}. {comp['nome']}")
            desc = comp.get('descricao_produto', 'N/A')
            print(f"   Descrição: {desc}")
            print(f"   R$ {comp['custo_total']/100:.2f}")
            print()
    else:
        print('❌ Erro:', response.status_code)
        print(response.text)
except Exception as e:
    print('❌ Erro na requisição:', e)
