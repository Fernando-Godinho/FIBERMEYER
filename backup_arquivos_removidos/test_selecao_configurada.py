import django
import os
import sys
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate, MP_Produtos
from main.views import calcular_custos_template

def test_selecao_resina_configurada():
    """Testa se a seleção de resina está funcionando com o novo formato"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    
    # Verificar o parâmetro de resina
    parametro_resina = ParametroTemplate.objects.get(
        template=template,
        nome='tipo_resina_id'
    )
    
    print("=== TESTE SELEÇÃO DE RESINA CONFIGURADA ===\n")
    
    print(f"Parâmetro de resina:")
    print(f"  Nome: {parametro_resina.nome}")
    print(f"  Label: {parametro_resina.label}")
    print(f"  Tipo: {parametro_resina.tipo}")
    print(f"  Valor padrão: {parametro_resina.valor_padrao}")
    
    # Carregar opções de seleção
    opcoes = json.loads(parametro_resina.opcoes_selecao)
    print(f"\nOpções disponíveis ({len(opcoes)}):")
    for opcao in opcoes:
        print(f"  {opcao['id']}: {opcao['descricao']} - R$ {opcao['preco']:.2f}")
    
    # Testar com cada opção
    parametros_base = {
        'roving_4400': 0.3,
        'manta_300': 0.2,
        'veu_qtd': 0.1,
        'peso_m': 2.0,
        'perda_processo': 3,
        'descricao': 'Teste seleção resina'
    }
    
    print(f"\n=== TESTE COM CADA RESINA ===")
    
    for opcao in opcoes:
        resina_id = opcao['id']
        resina_nome = opcao['descricao']
        resina_preco = opcao['preco']
        
        # Criar parâmetros com a resina específica
        parametros = parametros_base.copy()
        parametros['tipo_resina_id'] = resina_id
        
        # Calcular custos
        resultado = calcular_custos_template(template, parametros)
        
        # Encontrar componente resina
        componente_resina = None
        for comp in resultado['componentes']:
            if comp['nome'].lower() == 'resina':
                componente_resina = comp
                break
        
        print(f"\n{resina_nome}:")
        if componente_resina:
            print(f"  ✓ Produto usado: {componente_resina['produto']}")
            print(f"  ✓ Preço unitário: R$ {componente_resina['custo_unitario']:.2f}")
            print(f"  ✓ Quantidade: {componente_resina['quantidade']:.4f} kg")
            print(f"  ✓ Custo resina: R$ {componente_resina['custo_total']:.2f}")
            
            # Verificar se o preço bate
            if abs(componente_resina['custo_unitario'] - resina_preco) < 0.01:
                print(f"  ✓ Preço correto!")
            else:
                print(f"  ✗ Preço incorreto! Esperado: R$ {resina_preco:.2f}, Obtido: R$ {componente_resina['custo_unitario']:.2f}")
        else:
            print(f"  ✗ Componente resina não encontrado!")
        
        print(f"  Total: R$ {resultado['custo_total']:.2f}")
    
    # Teste com valor padrão
    print(f"\n=== TESTE COM VALOR PADRÃO ===")
    parametros_padrao = parametros_base.copy()
    # Não definir tipo_resina_id para usar o padrão
    
    resultado_padrao = calcular_custos_template(template, parametros_padrao)
    print(f"Sem especificar resina - Total: R$ {resultado_padrao['custo_total']:.2f}")
    
    # Teste especificando o valor padrão
    parametros_padrao['tipo_resina_id'] = int(parametro_resina.valor_padrao)
    resultado_com_padrao = calcular_custos_template(template, parametros_padrao)
    print(f"Com resina padrão ({parametro_resina.valor_padrao}) - Total: R$ {resultado_com_padrao['custo_total']:.2f}")
    
    print(f"\n=== SIMULAÇÃO DE FORMULÁRIO ===")
    print(f"No formulário, o usuário verá um campo 'Tipo de Resina' com as opções:")
    for i, opcao in enumerate(opcoes, 1):
        marcador = " (padrão)" if str(opcao['id']) == parametro_resina.valor_padrao else ""
        print(f"  {i}. {opcao['descricao']} - R$ {opcao['preco']:.2f}{marcador}")

if __name__ == "__main__":
    test_selecao_resina_configurada()
