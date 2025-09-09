import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate
from main.views import calcular_custos_template

# Buscar o template "Novo Perfil"
try:
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    print(f"Template encontrado: {template.nome}")
    
    # Parâmetros de exemplo
    parametros = {
        'roving_4400': 0.35,
        'manta_300': 0.24,
        'veu_qtd': 0.41,
        'peso_m': 4.0,
        'perda_processo': 3,  # 3% de perda
        'descricao': 'Teste perda'
    }
    
    print(f"\nParâmetros de entrada:")
    for param, valor in parametros.items():
        print(f"  {param}: {valor}")
    
    # Calcular custos
    resultado = calcular_custos_template(template, parametros)
    
    print(f"\n=== RESULTADO DO CÁLCULO ===")
    print(f"Total sem perda: R$ {resultado['custo_total_sem_perda']:.2f}")
    print(f"Perda de processo ({parametros['perda_processo']}%): R$ {resultado['perda_processo']:.2f}")
    print(f"CUSTO TOTAL FINAL: R$ {resultado['custo_total']:.2f}")
    
    print(f"\nDetalhes dos componentes:")
    for item in resultado['componentes']:
        print(f"  {item['nome']}: {item['quantidade']:.4f} x R$ {item['custo_unitario']:.2f} = R$ {item['custo_total']:.2f}")
    
    # Verificação
    total_verificacao = sum(item['custo_total'] for item in resultado['componentes'])
    print(f"\nVerificação:")
    print(f"Soma dos componentes: R$ {total_verificacao:.2f}")
    print(f"Custo sem perda (do resultado): R$ {resultado['custo_total_sem_perda']:.2f}")
    print(f"Diferença: R$ {abs(total_verificacao - resultado['custo_total_sem_perda']):.4f}")
    
except ProdutoTemplate.DoesNotExist:
    print("Template 'Novo Perfil' não encontrado!")
