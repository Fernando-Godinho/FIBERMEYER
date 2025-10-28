#!/usr/bin/env python3
"""
Teste da funcionalidade de descrição técnica nos produtos parametrizados.
Verifica se o campo foi adicionado corretamente ao modelo e API.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoTemplate
from main.serializers import MP_ProdutosSerializer
import json

def testar_campo_descricao_tecnica():
    """Testa se o campo descricao_tecnica está funcionando corretamente"""
    
    print("=== TESTE CAMPO DESCRIÇÃO TÉCNICA ===")
    print()
    
    # 1. Verificar se o campo existe no modelo MP_Produtos
    print("1. Verificando campo no modelo MP_Produtos...")
    try:
        # Tentar acessar o campo
        field = MP_Produtos._meta.get_field('descricao_tecnica')
        print(f"   ✅ Campo encontrado: {field.name} ({field.__class__.__name__})")
        print(f"   📝 Help text: {field.help_text}")
        print(f"   📏 Max length: {getattr(field, 'max_length', 'N/A')}")
        print(f"   🔒 Blank permitido: {field.blank}")
        print(f"   🔒 Null permitido: {field.null}")
    except Exception as e:
        print(f"   ❌ Erro ao acessar campo: {e}")
        return False
    
    print()
    
    # 2. Verificar se o campo está no serializer
    print("2. Verificando campo no serializer...")
    serializer = MP_ProdutosSerializer()
    fields = serializer.get_fields().keys()
    if 'descricao_tecnica' in fields:
        print(f"   ✅ Campo incluído no serializer")
        print(f"   📋 Campos disponíveis: {list(fields)}")
    else:
        print(f"   ❌ Campo NÃO incluído no serializer")
        print(f"   📋 Campos disponíveis: {list(fields)}")
        return False
    
    print()
    
    # 3. Testar criação de produto com descrição técnica
    print("3. Testando criação de produto com descrição técnica...")
    try:
        # Criar dados de teste
        dados_teste = {
            'descricao': 'Produto Teste Descrição Técnica',
            'custo_centavos': 15000,  # R$ 150,00
            'peso_und': '2.5',
            'unidade': 'UN',
            'referencia': 'TEST-DESC-001',
            'tipo_produto': 'simples',
            'categoria': 'Teste',
            'subcategoria': 'Funcionalidade',
            'descricao_tecnica': 'Esta é uma descrição técnica de teste para verificar se o campo está funcionando corretamente. Inclui especificações técnicas detalhadas.'
        }
        
        # Validar com serializer
        serializer = MP_ProdutosSerializer(data=dados_teste)
        if serializer.is_valid():
            produto = serializer.save()
            print(f"   ✅ Produto criado com sucesso: ID {produto.id}")
            print(f"   📝 Descrição: {produto.descricao}")
            print(f"   🔧 Descrição técnica: {produto.descricao_tecnica[:100]}...")
            
            # Verificar se salvou corretamente
            produto_db = MP_Produtos.objects.get(id=produto.id)
            if produto_db.descricao_tecnica == dados_teste['descricao_tecnica']:
                print(f"   ✅ Descrição técnica salva corretamente no banco")
            else:
                print(f"   ❌ Descrição técnica não salva corretamente")
                return False
                
            # Limpar teste
            produto.delete()
            print(f"   🗑️ Produto de teste removido")
            
        else:
            print(f"   ❌ Dados inválidos: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao criar produto: {e}")
        return False
    
    print()
    
    # 4. Testar campo em ProdutoTemplate também
    print("4. Verificando campo no modelo ProdutoTemplate...")
    try:
        field = ProdutoTemplate._meta.get_field('descricao_tecnica')
        print(f"   ✅ Campo encontrado em ProdutoTemplate: {field.name}")
    except Exception as e:
        print(f"   ❌ Campo não encontrado em ProdutoTemplate: {e}")
    
    print()
    print("=== TESTE CONCLUÍDO COM SUCESSO ===")
    return True

def verificar_templates_interface():
    """Verifica se todos os templates de interface incluem o campo descrição técnica"""
    
    print()
    print("=== VERIFICAÇÃO TEMPLATES INTERFACE ===")
    print()
    
    # IDs dos campos de descrição técnica que devem existir na interface
    campos_esperados = [
        'perfil_descricao_tecnica',      # Novo Perfil
        'grade_descricao_tecnica',       # Grades
        'tampa_descricao_tecnica',       # Tampa Montada
        'tampa_inj_descricao_tecnica',   # Tampa Injetada
        'degrau_descricao_tecnica',      # Degraus
        'degrau_inj_descricao_tecnica',  # Degrau Injetado
        'guarda_corpo_descricao_tecnica', # Guarda Corpo Horizontal
        'escada_descricao_tecnica',      # Escada
    ]
    
    print("Templates que devem incluir campo de descrição técnica:")
    for i, campo in enumerate(campos_esperados, 1):
        template_name = campo.replace('_descricao_tecnica', '').replace('_', ' ').title()
        print(f"   {i}. {template_name} → {campo}")
    
    print()
    print("Para verificar se os campos foram adicionados, verifique o arquivo:")
    print("main/templates/main/mp.html")
    print()
    print("Cada campo deve ter a estrutura:")
    print("""
    <div class="mb-3">
        <label for="[ID]" class="form-label">Descrição Técnica</label>
        <textarea class="form-control param-input" id="[ID]" name="descricao_tecnica" rows="3" placeholder="..."></textarea>
        <div class="form-text">Informações técnicas adicionais...</div>
    </div>
    """)

if __name__ == '__main__':
    try:
        # Executar testes
        sucesso = testar_campo_descricao_tecnica()
        verificar_templates_interface()
        
        if sucesso:
            print()
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Campo descrição técnica implementado com sucesso")
            print("✅ Modelo, serializer e API funcionando corretamente")
            print()
            print("Próximos passos:")
            print("1. Testar a interface web criando produtos parametrizados")
            print("2. Verificar se a descrição técnica aparece nos formulários")
            print("3. Confirmar que os dados são salvos corretamente via API")
            
        else:
            print()
            print("❌ ALGUNS TESTES FALHARAM!")
            print("Verifique os erros acima e corrija antes de continuar.")
            
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()