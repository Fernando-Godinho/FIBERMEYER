#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos

def main():
    print("=== CONFIGURANDO PARÂMETROS DO TEMPLATE 'NOVO PERFIL' ===")
    
    # Busca o template do Novo Perfil
    novo_perfil = MP_Produtos.objects.filter(descricao="Novo Perfil").first()
    
    if not novo_perfil:
        print("❌ Produto 'Novo Perfil' não encontrado!")
        return
    
    template = novo_perfil.template
    print(f"📋 Template encontrado: ID {template.id}")
    print(f"📦 Produto base: {novo_perfil.descricao} (ID: {novo_perfil.id})")
    
    # Configurar parâmetros padrão para perfis pultrudados
    parametros_obrigatorios = [
        "comprimento",  # em metros
        "largura",      # em mm  
        "altura",       # em mm
        "espessura"     # em mm
    ]
    
    parametros_opcionais = {
        "tolerancia": 0.5,           # tolerância em mm
        "acabamento": "padrao",      # padrao, liso, rugoso
        "cor": "natural",            # natural, branco, cinza
        "densidade": 1.8,            # g/cm³ - densidade típica de compositos
        "fator_perda": 0.05,         # 5% de perda no processo
        "tipo_resina": "poliester"   # poliester, isoftalica, ester_vinilica
    }
    
    formula_principal = """
    # Fórmula para cálculo de custos do perfil
    # Volume = (comprimento * largura * altura * espessura) / 1000000  # cm³
    # Peso = Volume * densidade  # gramas
    # Custo_material = Peso * custo_por_grama_material
    # Custo_total = Custo_material * (1 + fator_perda) + custo_mao_obra
    """
    
    print("🛠️  Atualizando parâmetros do template...")
    
    template.parametros_obrigatorios = parametros_obrigatorios
    template.parametros_opcionais = parametros_opcionais
    template.formula_principal = formula_principal
    template.save()
    
    print("✅ Template atualizado com sucesso!")
    print()
    print("📋 CONFIGURAÇÃO FINAL:")
    print(f"Parâmetros obrigatórios: {template.parametros_obrigatorios}")
    print(f"Parâmetros opcionais: {list(template.parametros_opcionais.keys())}")
    print()
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. O template 'Novo Perfil' está configurado")
    print("2. Você pode usar este template como base para criar outros perfis")
    print("3. Os parâmetros incluem dimensões, materiais e processo")
    print("4. A fórmula considera volume, densidade e perdas do processo")
    
    # Verificar quantos templates restaram
    total_templates = ProdutoTemplate.objects.count()
    print(f"\n📊 RESUMO: {total_templates} template(s) no sistema")
    
    if total_templates == 1:
        print("✅ Sistema limpo - apenas o template 'Novo Perfil' permanece")
    else:
        print("⚠️  Ainda existem outros templates:")
        for t in ProdutoTemplate.objects.exclude(id=template.id):
            nome = t.produto_base.descricao if t.produto_base else f"Template {t.id}"
            print(f"  - {nome}")

if __name__ == "__main__":
    main()
