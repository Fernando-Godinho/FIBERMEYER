import django
import os
import sys

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos
from main.views import calcular_custos_template

def demo_template_completo():
    """Demonstra o uso completo do template com seleção de resina"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    
    # Obter resinas disponíveis
    resinas = MP_Produtos.objects.filter(descricao__icontains='resina').order_by('custo_centavos')
    
    print("=== TEMPLATE 'NOVO PERFIL' COM SELEÇÃO DE RESINA ===\n")
    
    print("PARÂMETROS DISPONÍVEIS:")
    parametros_template = template.parametros.all().order_by('ordem')
    for param in parametros_template:
        valor_padrao = f" (padrão: {param.valor_padrao})" if param.valor_padrao else ""
        print(f"  {param.ordem}. {param.label} ({param.nome}){valor_padrao}")
    
    print(f"\nTIPOS DE RESINA DISPONÍVEIS:")
    for resina in resinas:
        print(f"  ID {resina.id}: {resina.descricao} - R$ {resina.custo_centavos/100:.2f}/kg")
    
    # Exemplo prático de uso
    print(f"\n=== EXEMPLO DE USO ===")
    
    # Usando Resina Isoftálica como exemplo
    resina_isoftalica = MP_Produtos.objects.get(descricao='Resina Isoftálica')
    
    parametros_exemplo = {
        'roving_4400': 0.5,           # 500g de roving
        'manta_300': 0.3,             # 300g de manta  
        'veu_qtd': 0.2,               # 200g de véu
        'peso_m': 3.5,                # 3.5kg por metro
        'tipo_resina_id': resina_isoftalica.id,  # Resina Isoftálica
        'perda_processo': 5,          # 5% de perda de processo
        'descricao': 'Perfil customizado com resina isoftálica'
    }
    
    print(f"\nParâmetros do exemplo:")
    for param, valor in parametros_exemplo.items():
        if param == 'tipo_resina_id':
            resina_nome = MP_Produtos.objects.get(id=valor).descricao
            print(f"  {param}: {valor} ({resina_nome})")
        else:
            print(f"  {param}: {valor}")
    
    # Calcular resultado
    resultado = calcular_custos_template(template, parametros_exemplo)
    
    print(f"\n=== RESULTADO DO CÁLCULO ===")
    print(f"Custo dos materiais: R$ {resultado['custo_total_sem_perda']:.2f}")
    print(f"Perda de processo ({parametros_exemplo['perda_processo']}%): R$ {resultado['perda_processo']:.2f}")
    print(f"CUSTO TOTAL FINAL: R$ {resultado['custo_total']:.2f}")
    
    print(f"\nDETALHE DOS COMPONENTES:")
    for comp in resultado['componentes']:
        print(f"  {comp['nome']}: {comp['quantidade']:.4f} {comp['unidade']} x R$ {comp['custo_unitario']:.2f} = R$ {comp['custo_total']:.2f}")
        if comp['nome'] == 'Resina':
            print(f"    ↳ Produto: {comp['produto']}")
    
    # Comparar com diferentes resinas
    print(f"\n=== COMPARAÇÃO RÁPIDA COM OUTRAS RESINAS ===")
    
    outras_resinas = [
        MP_Produtos.objects.get(descricao='Resina Poliéster'),
        MP_Produtos.objects.get(descricao='Resina Éster Vinílica')
    ]
    
    custo_base = resultado['custo_total']
    
    for resina in outras_resinas:
        params_teste = parametros_exemplo.copy()
        params_teste['tipo_resina_id'] = resina.id
        resultado_teste = calcular_custos_template(template, params_teste)
        
        diferenca = resultado_teste['custo_total'] - custo_base
        sinal = '+' if diferenca > 0 else ''
        print(f"  {resina.descricao}: R$ {resultado_teste['custo_total']:.2f} ({sinal}R$ {diferenca:.2f})")
    
    print(f"\n=== COMO USAR ===")
    print(f"1. Defina as quantidades de roving, manta e véu")
    print(f"2. Informe o peso total por metro do perfil")
    print(f"3. Escolha o tipo de resina (ID: {', '.join([str(r.id) for r in resinas])})")
    print(f"4. Ajuste a porcentagem de perda de processo se necessário")
    print(f"5. O sistema calculará automaticamente todos os componentes e custo final")

if __name__ == "__main__":
    demo_template_completo()
