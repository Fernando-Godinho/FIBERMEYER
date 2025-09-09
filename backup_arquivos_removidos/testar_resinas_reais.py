#!/usr/bin/env python
"""
Teste real com as resinas do sistema
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ParametroTemplate
import json

def testar_resinas_reais():
    """Testa a atualização automática com as resinas reais do sistema"""
    
    print("🧪 TESTANDO COM RESINAS REAIS DO SISTEMA")
    print("="*50)
    
    # Buscar resinas reais
    resina_poliester = MP_Produtos.objects.filter(descricao__icontains='Resina Poliéster').first()
    
    if not resina_poliester:
        print("❌ Resina Poliéster não encontrada!")
        return
    
    print(f"✅ Encontrada: {resina_poliester.descricao}")
    print(f"   Preço atual: R$ {resina_poliester.custo_centavos/100:.2f}")
    
    # Verificar se existe no template
    parametros_com_resina = ParametroTemplate.objects.filter(
        tipo='selecao',
        opcoes_selecao__icontains=str(resina_poliester.id)
    )
    
    print(f"\n🎯 Templates que usam esta resina:")
    for param in parametros_com_resina:
        print(f"   📋 {param.template.nome} - parâmetro '{param.label}'")
        
        # Mostrar opções atuais
        try:
            opcoes = json.loads(param.opcoes_selecao)
            for opcao in opcoes:
                if opcao.get('id') == resina_poliester.id:
                    print(f"      💰 Preço no template: R$ {opcao.get('preco', 'N/A')}")
        except:
            print(f"      ⚠️  Erro ao ler opções")
    
    # Buscar produtos dependentes
    dependentes = resina_poliester.get_produtos_dependentes()
    print(f"\n🔗 Produtos que dependem desta resina:")
    if dependentes.exists():
        for produto in dependentes:
            print(f"   📦 {produto.descricao} - R$ {produto.custo_centavos/100:.2f}")
    else:
        print("   (Nenhum produto composto encontrado)")
    
    # Alterar preço da resina
    preco_original = resina_poliester.custo_centavos
    novo_preco = 1400  # R$ 14,00
    
    print(f"\n🔄 ALTERANDO PREÇO DA RESINA PARA R$ {novo_preco/100:.2f}...")
    resina_poliester.custo_centavos = novo_preco
    resina_poliester.save()
    
    # Verificar templates após alteração
    print(f"\n📊 VERIFICANDO TEMPLATES APÓS ALTERAÇÃO:")
    for param in parametros_com_resina:
        param.refresh_from_db()
        try:
            opcoes = json.loads(param.opcoes_selecao)
            for opcao in opcoes:
                if opcao.get('id') == resina_poliester.id:
                    print(f"   📋 {param.template.nome}: R$ {opcao.get('preco', 'N/A')}")
        except:
            print(f"   ⚠️  Erro ao ler opções do {param.template.nome}")
    
    # Restaurar preço original
    print(f"\n🔄 RESTAURANDO PREÇO ORIGINAL...")
    resina_poliester.custo_centavos = preco_original
    resina_poliester.save()
    
    print(f"✅ Teste concluído!")

if __name__ == "__main__":
    testar_resinas_reais()
