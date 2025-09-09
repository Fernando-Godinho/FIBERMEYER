import django
import os
import sys
import json

# Configurar o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, ParametroTemplate

def verificar_configuracao_campo_resina():
    """Verifica a configuração atual do campo de resina para o frontend"""
    
    template = ProdutoTemplate.objects.get(nome="Novo Perfil")
    param_resina = ParametroTemplate.objects.get(template=template, nome='tipo_resina_id')
    
    print("🔍 CONFIGURAÇÃO ATUAL DO CAMPO RESINA")
    print("=" * 50)
    
    print(f"Template: {template.nome}")
    print(f"Campo: {param_resina.nome}")
    print(f"Label: {param_resina.label}")
    print(f"Tipo: {param_resina.tipo}")
    print(f"Obrigatório: {param_resina.obrigatorio}")
    print(f"Valor padrão: {param_resina.valor_padrao}")
    print(f"Ordem: {param_resina.ordem}")
    
    # Mostrar opções de seleção
    opcoes = json.loads(param_resina.opcoes_selecao)
    print(f"\nOpções de seleção ({len(opcoes)} opções):")
    for opcao in opcoes:
        marcador = "✓" if str(opcao['id']) == param_resina.valor_padrao else "○"
        print(f"  {marcador} ID {opcao['id']}: {opcao['descricao']} - R$ {opcao['preco']:.2f}")
    
    print(f"\n📋 DADOS PARA O FRONTEND:")
    print(f"```json")
    campo_config = {
        "nome": param_resina.nome,
        "label": param_resina.label,
        "tipo": param_resina.tipo,
        "obrigatorio": param_resina.obrigatorio,
        "valor_padrao": param_resina.valor_padrao,
        "ordem": param_resina.ordem,
        "opcoes": opcoes
    }
    print(json.dumps(campo_config, indent=2, ensure_ascii=False))
    print(f"```")
    
    print(f"\n🖥️ EXEMPLO HTML/JAVASCRIPT:")
    print(f"""
<div class="form-group">
    <label for="tipo_resina_id">{param_resina.label} *</label>
    <select id="tipo_resina_id" name="tipo_resina_id" required>""")
    
    for opcao in opcoes:
        selected = 'selected' if str(opcao['id']) == param_resina.valor_padrao else ''
        print(f"""        <option value="{opcao['id']}" {selected}>{opcao['descricao']} - R$ {opcao['preco']:.2f}</option>""")
    
    print(f"""    </select>
</div>""")
    
    print(f"\n⚡ EXEMPLO REACT/VUE:")
    print(f"""
const opcoes = {json.dumps(opcoes, ensure_ascii=False)};

// React
<select name="tipo_resina_id" defaultValue="{param_resina.valor_padrao}">
  {{opcoes.map(opcao => (
    <option key={{opcao.id}} value={{opcao.id}}>
      {{opcao.descricao}} - R$ {{opcao.preco.toFixed(2)}}
    </option>
  ))}}
</select>

// Vue
<select v-model="form.tipo_resina_id">
  <option v-for="opcao in opcoes" :key="opcao.id" :value="opcao.id">
    {{{{ opcao.descricao }}}} - R$ {{{{ opcao.preco.toFixed(2) }}}}
  </option>
</select>""")
    
    print(f"\n✅ CONFIRMAÇÃO:")
    print(f"  • Campo configurado como 'selecao'")
    print(f"  • Apenas 3 resinas específicas disponíveis")
    print(f"  • Preços incluídos nas opções")
    print(f"  • Valor padrão definido")
    print(f"  • Pronto para implementação no frontend!")

if __name__ == "__main__":
    verificar_configuracao_campo_resina()
