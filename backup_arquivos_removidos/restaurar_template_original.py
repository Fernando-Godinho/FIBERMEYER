#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos, ProdutoComponente

def main():
    print("=== RECUPERANDO TEMPLATE ORIGINAL 'NOVO PERFIL' ===")
    print("Parâmetros corretos: peso_roving, peso_veu, peso_manta")
    print()
    
    # Buscar o template atual
    novo_perfil = MP_Produtos.objects.filter(descricao="Novo Perfil").first()
    
    if not novo_perfil:
        print("❌ Produto 'Novo Perfil' não encontrado!")
        return
    
    template = novo_perfil.template
    print(f"📋 Template atual encontrado (ID: {template.id})")
    print(f"   Parâmetros atuais obrigatórios: {template.parametros_obrigatorios}")
    print(f"   Parâmetros atuais opcionais: {template.parametros_opcionais}")
    print()
    
    # Corrigir parâmetros para a versão original
    print("🔄 Corrigindo parâmetros para versão original...")
    
    # Parâmetros obrigatórios originais - peso dos materiais principais
    parametros_obrigatorios_originais = [
        "peso_roving",    # kg de Roving 4400
        "peso_veu",       # kg de Véu  
        "peso_manta"      # kg de Manta 300
    ]
    
    # Parâmetros opcionais originais - configurações do processo
    parametros_opcionais_originais = {
        "tipo_resina": "poliester",          # tipo de resina a usar
        "fator_resina": 0.4,                 # proporção de resina (40%)
        "velocidade_m_h": 10.0,              # velocidade de produção
        "num_operadores": 2,                 # número de operadores
        "tempo_cura_h": 1.5,                 # tempo de cura em horas
        "tolerancia_peso": 0.05,             # tolerância de 5% no peso
        "adicionar_aditivos": True,          # incluir aditivos químicos
        "acabamento_superficie": "padrao"     # tipo de acabamento
    }
    
    # Fórmula original para cálculo baseado em peso
    formula_original = """
    # Fórmula original baseada em peso dos materiais
    # Custo_materiais = (peso_roving * custo_roving) + (peso_veu * custo_veu) + (peso_manta * custo_manta)
    # Custo_resina = (peso_roving + peso_veu + peso_manta) * fator_resina * custo_resina
    # Custo_aditivos = peso_total * percentual_aditivos * custo_medio_aditivos  
    # Custo_mao_obra = tempo_producao * num_operadores * custo_hora_operador
    # Custo_total = Custo_materiais + Custo_resina + Custo_aditivos + Custo_mao_obra
    """
    
    # Atualizar template
    template.parametros_obrigatorios = parametros_obrigatorios_originais
    template.parametros_opcionais = parametros_opcionais_originais
    template.formula_principal = formula_original
    template.save()
    
    print("✅ Template corrigido com parâmetros originais!")
    print()
    
    print("📋 PARÂMETROS CORRETOS RESTAURADOS:")
    print("🔴 Obrigatórios:")
    for param in parametros_obrigatorios_originais:
        print(f"   - {param}")
    
    print()
    print("🔵 Opcionais:")
    for param, valor in parametros_opcionais_originais.items():
        print(f"   - {param}: {valor}")
    
    print()
    print("💡 LÓGICA ORIGINAL:")
    print("   • Usuário informa peso desejado de cada material")
    print("   • Sistema calcula resina proporcional aos materiais") 
    print("   • Aditivos calculados baseado no peso total")
    print("   • Mão de obra baseada no tempo de produção")
    print("   • Resultado: custo total do perfil")
    
    print()
    print("🎯 COMO USAR AGORA:")
    print("   1. Acesse o modal 'Produto Parametrizado'")
    print("   2. Selecione 'Novo Perfil'")
    print("   3. Informe:")
    print("      - peso_roving (kg): Ex: 0.5")
    print("      - peso_veu (kg): Ex: 0.2") 
    print("      - peso_manta (kg): Ex: 0.3")
    print("   4. Configure opcionais se necessário")
    print("   5. Calcule o produto")
    
    print()
    print("✅ TEMPLATE ORIGINAL RESTAURADO!")
    print("   Agora os parâmetros são baseados em peso dos materiais como estava antes")

if __name__ == "__main__":
    main()
