#!/usr/bin/env python
import os
import sys
import django
import json
from io import StringIO

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from django.test import RequestFactory
from main.views import calcular_produto_parametrizado

print("=== TESTANDO LOGS DE MÃO DE OBRA NO CONSOLE ===")

# Criar uma requisição simulada
factory = RequestFactory()
request_data = {
    "template_id": 24,  # Template "Novo Perfil"
    "parametros": {
        "largura": "100",
        "altura": "50", 
        "comprimento": "1000",
        "velocidade_m_h": "24",
        "num_matrizes": "2",
        "num_maquinas_utilizadas": "1"
    }
}

# Fazer requisição POST simulada
request = factory.post(
    '/api/calcular-produto-parametrizado/',
    data=json.dumps(request_data),
    content_type='application/json'
)

print("Fazendo chamada para calcular_produto_parametrizado()...")
print("Parâmetros:")
for key, value in request_data["parametros"].items():
    print(f"  {key}: {value}")

print("\n" + "="*60)
print("LOGS DO CONSOLE (capturados):")
print("="*60)

# Capturar output do console
old_stdout = sys.stdout
sys.stdout = captured_output = StringIO()

try:
    # Chamar a função que irá gerar os logs
    response = calcular_produto_parametrizado(request)
    
    # Restaurar stdout
    sys.stdout = old_stdout
    
    # Mostrar os logs capturados
    console_output = captured_output.getvalue()
    print(console_output)
    
    print("="*60)
    print("RESPOSTA DA API:")
    print("="*60)
    
    # Mostrar resposta da API
    response_data = json.loads(response.content)
    print(f"Success: {response_data.get('success')}")
    print(f"Custo Total: {response_data.get('custo_total')} centavos = R$ {response_data.get('custo_total', 0)/100:.2f}")
    print(f"Número de componentes: {len(response_data.get('componentes', []))}")
    
    # Encontrar e mostrar componente de mão de obra
    for comp in response_data.get('componentes', []):
        if 'Mão de Obra' in comp.get('nome', ''):
            print(f"\nComponente Mão de Obra:")
            print(f"  Nome: {comp['nome']}")
            print(f"  Produto: {comp['produto']}")
            print(f"  Custo: {comp['custo_total']} centavos = R$ {comp['custo_total']/100:.2f}")
            break
    
except Exception as e:
    sys.stdout = old_stdout
    print(f"Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()

print(f"\n✅ Teste concluído! Os logs acima mostram exatamente:")
print(f"   - Qual registro de mão de obra está sendo usado")
print(f"   - Valor exato em centavos e reais") 
print(f"   - Cálculo detalhado passo a passo")
print(f"   - Componente final gerado")
