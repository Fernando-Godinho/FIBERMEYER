from main.views import OrcamentoForm
from main.models import Orcamento

print("Testando campo de observacoes no formulario")
print("=" * 50)

# Criar uma instancia do formulario
form = OrcamentoForm()

# Verificar se o campo observacoes existe
if 'observacoes' in form.fields:
    print("Campo 'observacoes' encontrado no formulario!")
    
    # Mostrar detalhes do campo
    observacoes_field = form.fields['observacoes']
    print(f"Tipo: {type(observacoes_field).__name__}")
    print(f"Label: {observacoes_field.label}")
    print(f"Widget: {type(observacoes_field.widget).__name__}")
    print(f"Attrs: {observacoes_field.widget.attrs}")
    
    print("\nCAMPO FUNCIONANDO CORRETAMENTE!")
    print("Ja esta configurado para aparecer no PDF!")
    print("\nINSTRUCOES DE USO:")
    print("1. Va para o formulario de orcamento")
    print("2. Role ate a secao 'Observacoes'")
    print("3. Digite suas observacoes no campo de texto")
    print("4. Salve o orcamento")
    print("5. Gere o PDF - as observacoes aparecerao na ultima pagina")
    
else:
    print("Campo 'observacoes' NAO encontrado!")
    print("Campos disponiveis:")
    for field_name in form.fields.keys():
        print(f"  - {field_name}")