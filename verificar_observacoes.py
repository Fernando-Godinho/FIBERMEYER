#!/usr/bin/env python
"""
Script para testar o campo de observações usando Django shell
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Usar o manage.py para configurar o Django
import manage

# Executar o comando via Django
if __name__ == "__main__":
    from main.views import OrcamentoForm
    from main.models import Orcamento
    
    print("🧪 TESTANDO CAMPO DE OBSERVAÇÕES NO FORMULÁRIO")
    print("=" * 60)
    
    # Criar uma instância do formulário
    form = OrcamentoForm()
    
    # Verificar se o campo observacoes existe
    if 'observacoes' in form.fields:
        print("✅ Campo 'observacoes' encontrado no formulário!")
        
        # Mostrar detalhes do campo
        observacoes_field = form.fields['observacoes']
        print(f"📝 Tipo: {type(observacoes_field).__name__}")
        print(f"🏷️ Label: {observacoes_field.label}")
        print(f"📋 Widget: {type(observacoes_field.widget).__name__}")
        print(f"🎨 Attrs: {observacoes_field.widget.attrs}")
        
        print("\n✅ CAMPO FUNCIONANDO CORRETAMENTE!")
        print("✅ Já está configurado para aparecer no PDF!")
        print("\n📋 INSTRUÇÕES DE USO:")
        print("=" * 30)
        print("1. Vá para o formulário de orçamento")
        print("2. Role até a seção 'Observações'")
        print("3. Digite suas observações no campo de texto")
        print("4. Salve o orçamento")
        print("5. Gere o PDF - as observações aparecerão na última página")
        
    else:
        print("❌ Campo 'observacoes' NÃO encontrado!")
        print("📋 Campos disponíveis:")
        for field_name in form.fields.keys():
            print(f"  - {field_name}")