import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate
from main.views import calcular_custos_template

def test_exemplo_usuario():
    """Testa o exemplo que o usuário mencionou: custo de R$ 14,00 com 3% = R$ 14,42"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    
    # Vamos tentar parâmetros que resultem em algo próximo de R$ 14
    parametros = {
        'roving_4400': 0.10,    # Reduzindo quantidades para chegar perto de R$ 14
        'manta_300': 0.05,
        'veu_qtd': 0.08,
        'peso_m': 1.0,          # Peso menor
        'perda_processo': 3,
        'descricao': 'Teste exemplo usuário'
    }
    
    resultado = calcular_custos_template(template, parametros)
    
    print("=== TESTE EXEMPLO DO USUÁRIO ===\n")
    print(f"Parâmetros utilizados:")
    for param, valor in parametros.items():
        if param != 'descricao':
            print(f"  {param}: {valor}")
    
    print(f"\nResultado:")
    print(f"Custo dos materiais: R$ {resultado['custo_total_sem_perda']:.2f}")
    print(f"Perda de processo (3%): R$ {resultado['perda_processo']:.2f}")
    print(f"Custo total final: R$ {resultado['custo_total']:.2f}")
    
    # Verificar se 3% está sendo aplicado corretamente
    custo_base = resultado['custo_total_sem_perda']
    perda_esperada = custo_base * 0.03
    custo_final_esperado = custo_base + perda_esperada
    
    print(f"\nVerificação matemática:")
    print(f"R$ {custo_base:.2f} + 3% (R$ {perda_esperada:.2f}) = R$ {custo_final_esperado:.2f}")
    print(f"Resultado da função: R$ {resultado['custo_total']:.2f}")
    print(f"Diferença: R$ {abs(custo_final_esperado - resultado['custo_total']):.4f}")
    
    # Mostrar componentes que contribuem mais
    print(f"\nTop 5 componentes por custo:")
    componentes_ordenados = sorted(resultado['componentes'], key=lambda x: x['custo_total'], reverse=True)
    for i, comp in enumerate(componentes_ordenados[:5]):
        print(f"  {i+1}. {comp['nome']}: R$ {comp['custo_total']:.2f}")
    
    # Exemplo específico para R$ 14,00
    print(f"\n=== EXEMPLO ESPECÍFICO: R$ 14,00 ===")
    if custo_base != 0:
        fator_ajuste = 14.0 / custo_base
        print(f"Para obter R$ 14,00, multiplique as quantidades por {fator_ajuste:.3f}")
        
        # Calcular exemplo ajustado
        parametros_ajustados = parametros.copy()
        parametros_ajustados['roving_4400'] = round(parametros['roving_4400'] * fator_ajuste, 4)
        parametros_ajustados['manta_300'] = round(parametros['manta_300'] * fator_ajuste, 4)
        parametros_ajustados['veu_qtd'] = round(parametros['veu_qtd'] * fator_ajuste, 4)
        parametros_ajustados['peso_m'] = round(parametros['peso_m'] * fator_ajuste, 2)
        
        resultado_ajustado = calcular_custos_template(template, parametros_ajustados)
        
        print(f"\nCom parâmetros ajustados:")
        print(f"  roving_4400: {parametros_ajustados['roving_4400']}")
        print(f"  manta_300: {parametros_ajustados['manta_300']}")
        print(f"  veu_qtd: {parametros_ajustados['veu_qtd']}")
        print(f"  peso_m: {parametros_ajustados['peso_m']}")
        
        print(f"\nResultado próximo ao desejado:")
        print(f"Custo base: R$ {resultado_ajustado['custo_total_sem_perda']:.2f}")
        print(f"Perda 3%: R$ {resultado_ajustado['perda_processo']:.2f}")
        print(f"Total final: R$ {resultado_ajustado['custo_total']:.2f}")
        
        # Se está próximo de R$ 14, mostrar como ficaria R$ 14,42
        if abs(resultado_ajustado['custo_total_sem_perda'] - 14.0) < 1.0:
            print(f"\n✓ Com custo base de R$ 14,00:")
            print(f"  R$ 14,00 + 3% (R$ 0,42) = R$ 14,42")

if __name__ == "__main__":
    test_exemplo_usuario()
