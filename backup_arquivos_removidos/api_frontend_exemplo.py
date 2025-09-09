import django
import os
import sys
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate

def gerar_api_frontend():
    """Gera exemplo de API para o frontend consumir"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    parametros = template.parametros.all().order_by('ordem')
    
    print("🚀 API PARA O FRONTEND IMPLEMENTAR")
    print("=" * 60)
    
    # Simular resposta da API
    response_api = {
        "template": {
            "id": template.id,
            "nome": template.nome,
            "categoria": template.categoria,
            "unidade_final": template.unidade_final
        },
        "parametros": []
    }
    
    for param in parametros:
        param_data = {
            "nome": param.nome,
            "label": param.label,
            "tipo": param.tipo,
            "obrigatorio": param.obrigatorio,
            "ordem": param.ordem,
            "valor_padrao": param.valor_padrao,
            "ajuda": param.ajuda
        }
        
        # Adicionar opções se for campo de seleção
        if param.tipo == 'selecao' and param.opcoes_selecao:
            param_data["opcoes"] = json.loads(param.opcoes_selecao)
        
        response_api["parametros"].append(param_data)
    
    print("📡 RESPOSTA DA API:")
    print("```json")
    print(json.dumps(response_api, indent=2, ensure_ascii=False))
    print("```")
    
    print(f"\n💻 EXEMPLO DE IMPLEMENTAÇÃO FRONTEND:")
    print(f"""
// 1. BUSCAR DADOS DO TEMPLATE
fetch('/api/templates/novo-perfil')
  .then(response => response.json())
  .then(data => {{
    renderizarFormulario(data.parametros);
  }});

// 2. FUNÇÃO PARA RENDERIZAR FORMULÁRIO
function renderizarFormulario(parametros) {{
  const form = document.getElementById('formulario-produto');
  
  parametros.forEach(param => {{
    const div = document.createElement('div');
    div.className = 'form-group';
    
    // Label
    const label = document.createElement('label');
    label.textContent = param.label + (param.obrigatorio ? ' *' : '');
    label.htmlFor = param.nome;
    
    // Campo de input
    let input;
    
    if (param.tipo === 'selecao') {{
      input = document.createElement('select');
      input.required = param.obrigatorio;
      
      // Adicionar opções
      param.opcoes.forEach(opcao => {{
        const option = document.createElement('option');
        option.value = opcao.id;
        option.textContent = `${{opcao.descricao}} - R$ ${{opcao.preco.toFixed(2)}}`;
        option.selected = opcao.id.toString() === param.valor_padrao;
        input.appendChild(option);
      }});
      
    }} else if (param.tipo === 'decimal') {{
      input = document.createElement('input');
      input.type = 'number';
      input.step = '0.01';
      input.placeholder = param.valor_padrao || '';
      input.required = param.obrigatorio;
      
    }} else if (param.tipo === 'texto') {{
      input = document.createElement('input');
      input.type = 'text';
      input.required = param.obrigatorio;
    }}
    
    input.id = param.nome;
    input.name = param.nome;
    
    div.appendChild(label);
    div.appendChild(input);
    form.appendChild(div);
  }});
}}

// 3. ENVIAR DADOS PARA CÁLCULO
function calcularCusto() {{
  const formData = new FormData(document.getElementById('formulario-produto'));
  const parametros = Object.fromEntries(formData.entries());
  
  fetch('/api/calcular-produto-parametrizado', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{
      template_id: {template.id},
      parametros: parametros
    }})
  }})
  .then(response => response.json())
  .then(resultado => {{
    exibirResultado(resultado);
  }});
}}""")
    
    print(f"\n🎨 EXEMPLO CSS PARA O CAMPO RESINA:")
    print(f"""
.form-group {{
  margin-bottom: 20px;
}}

.form-group label {{
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}}

.form-group select {{
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  background-color: white;
}}

.form-group select:focus {{
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}}

/* Destaque para o campo de resina */
.form-group select[name="tipo_resina_id"] {{
  border-color: #28a745;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}}""")
    
    print(f"\n📋 RESUMO PARA O DESENVOLVEDOR:")
    print(f"""
✅ CAMPO CONFIGURADO:
  • Nome: tipo_resina_id
  • Tipo: selecao (dropdown)
  • 3 opções fixas de resina
  • Preços visíveis na interface
  • Valor padrão: Resina Poliéster

🔧 IMPLEMENTAÇÃO:
  1. Fazer GET /api/templates/novo-perfil para pegar configuração
  2. Renderizar campo como <select> com as opções
  3. Mostrar: "Descrição - R$ Preço" para cada opção
  4. Pré-selecionar valor padrão (ID 1269)
  5. Enviar valor selecionado no POST para cálculo

💡 DICA: O campo já está pronto no backend, só precisa ser renderizado!""")

if __name__ == "__main__":
    gerar_api_frontend()
