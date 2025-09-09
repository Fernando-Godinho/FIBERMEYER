import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos
from main.views import calcular_custos_template

def test_selecao_resina():
    """Testa a seleção de diferentes tipos de resina"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    
    # Obter IDs das resinas
    resina_poliester = MP_Produtos.objects.get(descricao='Resina Poliéster')
    resina_isoftalica = MP_Produtos.objects.get(descricao='Resina Isoftálica')
    resina_ester_vinilica = MP_Produtos.objects.get(descricao='Resina Éster Vinílica')
    
    print("=== TESTE DE SELEÇÃO DE RESINA ===\n")
    print(f"Resinas disponíveis:")
    print(f"  Poliéster (ID {resina_poliester.id}): R$ {resina_poliester.custo_centavos/100:.2f}")
    print(f"  Isoftálica (ID {resina_isoftalica.id}): R$ {resina_isoftalica.custo_centavos/100:.2f}")
    print(f"  Éster Vinílica (ID {resina_ester_vinilica.id}): R$ {resina_ester_vinilica.custo_centavos/100:.2f}")
    
    # Parâmetros base para teste
    parametros_base = {
        'roving_4400': 0.35,
        'manta_300': 0.24,
        'veu_qtd': 0.41,
        'peso_m': 4.0,
        'perda_processo': 3,
        'descricao': 'Teste seleção resina'
    }
    
    resinas_teste = [
        ('Poliéster', resina_poliester.id),
        ('Isoftálica', resina_isoftalica.id),
        ('Éster Vinílica', resina_ester_vinilica.id)
    ]
    
    resultados = []
    
    for nome_resina, id_resina in resinas_teste:
        # Criar parâmetros com a resina específica
        parametros = parametros_base.copy()
        parametros['tipo_resina_id'] = id_resina
        
        # Calcular custos
        resultado = calcular_custos_template(template, parametros)
        
        # Encontrar componente resina no resultado
        componente_resina = None
        for comp in resultado['componentes']:
            if comp['nome'].lower() == 'resina':
                componente_resina = comp
                break
        
        resultados.append({
            'nome': nome_resina,
            'custo_total': resultado['custo_total'],
            'componente_resina': componente_resina
        })
        
        print(f"\n=== {nome_resina.upper()} ===")
        print(f"Resina usada: {componente_resina['produto'] if componente_resina else 'Não encontrada'}")
        print(f"Custo unitário resina: R$ {componente_resina['custo_unitario']:.2f}" if componente_resina else "N/A")
        print(f"Quantidade resina: {componente_resina['quantidade']:.4f} kg" if componente_resina else "N/A")
        print(f"Custo da resina: R$ {componente_resina['custo_total']:.2f}" if componente_resina else "N/A")
        print(f"CUSTO TOTAL: R$ {resultado['custo_total']:.2f}")
    
    # Comparação
    print(f"\n=== COMPARAÇÃO ===")
    resultado_base = resultados[0]  # Poliéster como base
    for resultado in resultados[1:]:
        diferenca = resultado['custo_total'] - resultado_base['custo_total']
        print(f"{resultado['nome']} vs Poliéster: {'+' if diferenca > 0 else ''}R$ {diferenca:.2f}")
    
    # Verificar se as resinas estão sendo trocadas corretamente
    print(f"\n=== VERIFICAÇÕES ===")
    produtos_usados = [r['componente_resina']['produto'] for r in resultados if r['componente_resina']]
    if len(set(produtos_usados)) == len(produtos_usados):
        print("✓ Cada teste usou um tipo diferente de resina")
    else:
        print("✗ Alguns testes usaram a mesma resina")
        
    custos_diferentes = len(set([r['custo_total'] for r in resultados])) == len(resultados)
    if custos_diferentes:
        print("✓ Custos totais diferentes para cada tipo de resina")
    else:
        print("✗ Alguns custos totais são iguais")

if __name__ == "__main__":
    test_selecao_resina()
