import django
import os
import sys
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate

def verificar_campo_resina_frontend():
    """Verifica como o campo de resina deve ser renderizado no frontend"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    param_resina = ParametroTemplate.objects.get(template=template, nome='tipo_resina_id')
    
    print("🔍 DIAGNÓSTICO DO CAMPO RESINA NO FRONTEND")
    print("=" * 60)
    
    print(f"📋 Dados do parâmetro:")
    print(f"   Nome: {param_resina.nome}")
    print(f"   Label: {param_resina.label}")
    print(f"   Tipo: {param_resina.tipo}")
    print(f"   Obrigatório: {param_resina.obrigatorio}")
    print(f"   Valor padrão: {param_resina.valor_padrao}")
    
    if param_resina.opcoes_selecao:
        opcoes = json.loads(param_resina.opcoes_selecao)
        print(f"   Opções configuradas: {len(opcoes)}")
        for opcao in opcoes:
            print(f"     • ID {opcao['id']}: {opcao['descricao']} - R$ {opcao['preco']:.2f}")
    else:
        print(f"   ❌ PROBLEMA: Opções não configuradas!")
    
    print(f"\n🖥️ COMO O FRONTEND DEVE RENDERIZAR:")
    
    if param_resina.tipo == 'selecao' and param_resina.opcoes_selecao:
        print(f"✅ Campo deve ser renderizado como SELECT/DROPDOWN")
        print(f"")
        print(f"HTML correto:")
        print(f"```html")
        print(f'<label for="tipo_resina_id">{param_resina.label} *</label>')
        print(f'<select id="tipo_resina_id" name="tipo_resina_id" required>')
        
        opcoes = json.loads(param_resina.opcoes_selecao)
        for opcao in opcoes:
            selected = 'selected' if str(opcao['id']) == param_resina.valor_padrao else ''
            print(f'  <option value="{opcao['id']}" {selected}>{opcao['descricao']} - R$ {opcao['preco']:.2f}</option>')
        
        print(f'</select>')
        print(f"```")
        
    else:
        print(f"❌ PROBLEMA: Campo não está configurado corretamente")
        if param_resina.tipo != 'selecao':
            print(f"   • Tipo incorreto: {param_resina.tipo} (deveria ser 'selecao')")
        if not param_resina.opcoes_selecao:
            print(f"   • Opções não configuradas")
    
    print(f"\n🔧 CÓDIGO JAVASCRIPT PARA O FRONTEND:")
    print(f"```javascript")
    print(f"// Dados que chegam do backend")
    param_data = {
        "nome": param_resina.nome,
        "label": param_resina.label,
        "tipo": param_resina.tipo,
        "obrigatorio": param_resina.obrigatorio,
        "valor_padrao": param_resina.valor_padrao,
        "opcoes": json.loads(param_resina.opcoes_selecao) if param_resina.opcoes_selecao else []
    }
    print(f"const parametro = {json.dumps(param_data, indent=2, ensure_ascii=False)};")
    print(f"")
    print(f"// Função para renderizar o campo")
    print(f"function renderizarCampoResina(param) {{")
    print(f"  if (param.tipo === 'selecao') {{")
    print(f"    const select = document.createElement('select');")
    print(f"    select.id = param.nome;")
    print(f"    select.name = param.nome;")
    print(f"    select.required = param.obrigatorio;")
    print(f"    ")
    print(f"    param.opcoes.forEach(opcao => {{")
    print(f"      const option = document.createElement('option');")
    print(f"      option.value = opcao.id;")
    print(f"      option.textContent = `${{opcao.descricao}} - R$ ${{opcao.preco.toFixed(2)}}`;")
    print(f"      option.selected = opcao.id.toString() === param.valor_padrao;")
    print(f"      select.appendChild(option);")
    print(f"    }});")
    print(f"    ")
    print(f"    return select;")
    print(f"  }}")
    print(f"}}")
    print(f"```")
    
    print(f"\n❗ PROBLEMA IDENTIFICADO:")
    print(f"O frontend está renderizando o campo como INPUT em vez de SELECT!")
    print(f"")
    print(f"📝 SOLUÇÃO:")
    print(f"1. Verificar o código do frontend que renderiza os parâmetros")
    print(f"2. Adicionar condição para tipo 'selecao'")
    print(f"3. Renderizar como <select> quando tipo === 'selecao'")
    print(f"4. Usar as opções em 'opcoes_selecao' para popular o select")

if __name__ == "__main__":
    verificar_campo_resina_frontend()
