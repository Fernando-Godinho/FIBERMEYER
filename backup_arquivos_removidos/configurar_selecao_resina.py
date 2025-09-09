import django
import os
import sys
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate, MP_Produtos

def atualizar_parametro_resina():
    """Atualiza o parâmetro de resina para ser uma seleção com apenas as resinas"""
    
    # Buscar o template
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    
    # Buscar as resinas disponíveis (apenas as que criamos)
    resinas = MP_Produtos.objects.filter(
        descricao__in=[
            'Resina Poliéster',
            'Resina Isoftálica', 
            'Resina Éster Vinílica'
        ]
    ).order_by('custo_centavos')
    
    print("=== ATUALIZANDO PARÂMETRO DE RESINA ===\n")
    
    print("Resinas encontradas:")
    opcoes_resina = []
    for resina in resinas:
        opcao = {
            'id': resina.id,
            'descricao': resina.descricao,
            'preco': resina.custo_centavos / 100
        }
        opcoes_resina.append(opcao)
        print(f"  ID {resina.id}: {resina.descricao} - R$ {resina.custo_centavos/100:.2f}")
    
    # Buscar o parâmetro de resina
    parametro_resina = ParametroTemplate.objects.get(
        template=template,
        nome='tipo_resina_id'
    )
    
    print(f"\nParâmetro atual:")
    print(f"  Nome: {parametro_resina.nome}")
    print(f"  Label: {parametro_resina.label}")
    print(f"  Tipo: {parametro_resina.tipo}")
    print(f"  Valor padrão: {parametro_resina.valor_padrao}")
    print(f"  Opções: {parametro_resina.opcoes_selecao}")
    
    # Atualizar o parâmetro
    parametro_resina.tipo = 'selecao'
    parametro_resina.opcoes_selecao = json.dumps(opcoes_resina, ensure_ascii=False)
    parametro_resina.valor_padrao = str(resinas.first().id)  # Resina mais barata como padrão
    parametro_resina.save()
    
    print(f"\n=== PARÂMETRO ATUALIZADO ===")
    print(f"  Tipo: {parametro_resina.tipo}")
    print(f"  Valor padrão: {parametro_resina.valor_padrao} ({resinas.first().descricao})")
    print(f"  Opções configuradas: {len(opcoes_resina)} resinas")
    
    # Verificar as opções
    opcoes_carregadas = json.loads(parametro_resina.opcoes_selecao)
    print(f"\nOpções disponíveis no formulário:")
    for opcao in opcoes_carregadas:
        print(f"  {opcao['id']}: {opcao['descricao']} - R$ {opcao['preco']:.2f}")
    
    print(f"\n✅ Parâmetro de resina configurado como seleção!")
    print(f"Agora o formulário mostrará apenas as 3 opções de resina.")

if __name__ == "__main__":
    atualizar_parametro_resina()
