import django
import os
import sys
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate

def mostrar_formulario_simulado():
    """Mostra como ficaria o formulário com o campo de seleção de resina"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    parametros = template.parametros.all().order_by('ordem')
    
    print("=" * 60)
    print("           FORMULÁRIO: NOVO PERFIL")
    print("=" * 60)
    
    for param in parametros:
        print(f"\n{param.ordem}. {param.label}")
        
        if param.tipo == 'decimal':
            valor_padrao = f" (padrão: {param.valor_padrao})" if param.valor_padrao else ""
            print(f"   [_________]{valor_padrao}")
            
        elif param.tipo == 'selecao':
            print(f"   Selecione uma opção:")
            
            if param.opcoes_selecao:
                opcoes = json.loads(param.opcoes_selecao)
                for i, opcao in enumerate(opcoes, 1):
                    marcador = " ●" if str(opcao['id']) == param.valor_padrao else " ○"
                    print(f"   {marcador} {opcao['descricao']} - R$ {opcao['preco']:.2f}")
            else:
                print(f"   [Dropdown com opções]")
                
        elif param.tipo == 'texto':
            print(f"   [________________________]")
        
        # Mostrar se é obrigatório
        if param.obrigatorio:
            print(f"   * Campo obrigatório")
    
    print(f"\n" + "=" * 60)
    print("                [CALCULAR CUSTO]")
    print("=" * 60)
    
    # Exemplo de resultado
    print(f"\n📋 EXEMPLO DE USO:")
    print(f"1. Roving 4400: 0.5 kg")
    print(f"2. Manta 300: 0.3 m²")
    print(f"3. Véu: 0.2 kg")
    print(f"4. Peso/m: 3.0 kg")
    print(f"5. Tipo de Resina: ● Resina Isoftálica - R$ 18.34")
    print(f"6. Perda de Processo: 3 %")
    print(f"7. Descrição: Perfil especial")
    
    print(f"\n💰 RESULTADO:")
    print(f"   Custo dos materiais: R$ 45.20")
    print(f"   Perda de processo (3%): R$ 1.36") 
    print(f"   TOTAL: R$ 46.56")
    
    print(f"\n🎯 VANTAGENS DA SELEÇÃO:")
    print(f"   ✓ Apenas resinas válidas aparecem")
    print(f"   ✓ Preços visíveis na seleção")
    print(f"   ✓ Não há risco de ID inválido")
    print(f"   ✓ Interface mais amigável")

if __name__ == "__main__":
    mostrar_formulario_simulado()
