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

print("=== TESTE: SALVAMENTO DE MÃO DE OBRA COMO COMPONENTE ===")

# Criar uma requisição simulada
factory = RequestFactory()
request_data = {
    "template_id": 24,  # Template "Novo Perfil"
    "parametros": {
        "largura": "200",
        "altura": "100", 
        "comprimento": "2000",  # Produto maior para ter custo de mão de obra mais significativo
        "velocidade_m_h": "15",  # Velocidade menor = maior custo
        "num_matrizes": "1",     # Menos matrizes = maior custo
        "num_maquinas_utilizadas": "2"  # Mais máquinas = maior custo
    }
}

# Fazer requisição POST simulada
request = factory.post(
    '/api/calcular-produto-parametrizado/',
    data=json.dumps(request_data),
    content_type='application/json'
)

print("Calculando produto com parâmetros que geram maior custo de mão de obra...")
print("Parâmetros:")
for key, value in request_data["parametros"].items():
    print(f"  {key}: {value}")

print("\n" + "="*60)

try:
    # Chamar a função que irá gerar os logs
    response = calcular_produto_parametrizado(request)
    response_data = json.loads(response.content)
    
    if response_data.get('success'):
        print("✅ CÁLCULO REALIZADO COM SUCESSO")
        print(f"Custo Total: {response_data.get('custo_total', 0)/100:.2f}")
        print(f"Componentes calculados: {len(response_data.get('componentes', []))}")
        
        # Verificar se mão de obra está inclusa
        mao_obra_encontrada = False
        for comp in response_data.get('componentes', []):
            if 'Mão de Obra' in comp.get('nome', ''):
                mao_obra_encontrada = True
                print(f"\n🔧 COMPONENTE MÃO DE OBRA:")
                print(f"  Nome: {comp['nome']}")
                print(f"  Produto: {comp.get('produto', 'N/A')}")
                print(f"  Quantidade: {comp['quantidade']}")
                print(f"  Custo: {comp['custo_total']/100:.2f}")
                break
        
        if mao_obra_encontrada:
            print(f"\n✅ MÃO DE OBRA SERÁ INCLUÍDA NO SALVAMENTO!")
            print(f"   - Quando salvar como produto composto, a mão de obra será um componente")
            print(f"   - Sistema criará automaticamente produto 'Mão de Obra - Pultrusão' se necessário")
            print(f"   - Componente será salvo com observação especial")
        else:
            print(f"\n❌ MÃO DE OBRA NÃO ENCONTRADA!")
            print(f"   Verificar se o template possui parâmetros de mão de obra")
        
        print(f"\n📋 TODOS OS COMPONENTES:")
        for i, comp in enumerate(response_data.get('componentes', []), 1):
            nome = comp.get('nome', 'N/A')
            custo = comp.get('custo_total', 0) / 100
            qtd = comp.get('quantidade', 0)
            tipo = "MÃO DE OBRA" if 'Mão de Obra' in nome else "MATERIAL"
            print(f"  {i}. {nome} - R$ {custo:.2f} ({qtd:.3f}) [{tipo}]")
            
    else:
        print(f"❌ ERRO NO CÁLCULO: {response_data.get('error', 'Erro desconhecido')}")
        
except Exception as e:
    print(f"❌ ERRO DURANTE O TESTE: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*60)
print("CONCLUSÃO:")
print("- Se mão de obra apareceu na lista, ela será salva como componente")
print("- O sistema agora cria automaticamente o produto 'Mão de Obra - Pultrusão'")
print("- Cada produto parametrizado incluirá seus materiais + mão de obra")
print("- Teste agora no navegador salvando um produto na base!")
print("="*60)
