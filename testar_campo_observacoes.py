#!/usr/bin/env python
"""
Script para testar se o campo de observações está funcionando no formulário
"""

import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from main.views import OrcamentoForm
from main.models import Orcamento

def testar_campo_observacoes():
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
        print(f"📏 Max length: {getattr(observacoes_field, 'max_length', 'Ilimitado')}")
        print(f"✅ Required: {observacoes_field.required}")
        
        # Verificar no modelo
        print("\n📊 VERIFICANDO NO MODELO ORCAMENTO:")
        print("=" * 40)
        
        try:
            # Buscar um orçamento existente para teste
            orcamento_teste = Orcamento.objects.first()
            if orcamento_teste:
                print(f"🎯 Orçamento encontrado: {orcamento_teste.numero_orcamento}")
                print(f"📝 Observações atuais: '{orcamento_teste.observacoes or 'Vazio'}'")
                
                # Testar se consegue salvar observações
                observacoes_teste = "Teste de observações para verificar se está funcionando!\n\nEsta é uma observação de múltiplas linhas."
                orcamento_teste.observacoes = observacoes_teste
                orcamento_teste.save()
                
                # Recarregar e verificar
                orcamento_teste.refresh_from_db()
                print(f"✅ Observações salvas com sucesso!")
                print(f"📄 Conteúdo salvo: '{orcamento_teste.observacoes}'")
                
            else:
                print("⚠️ Nenhum orçamento encontrado para teste")
                
        except Exception as e:
            print(f"❌ Erro ao testar modelo: {e}")
        
        # Mostrar como usar no template
        print("\n🌐 COMO USAR NO TEMPLATE:")
        print("=" * 40)
        print("No orcamento_form.html, o campo deve aparecer assim:")
        print()
        print("{{ form.observacoes.label }}")
        print("{{ form.observacoes }}")
        print()
        print("Ou com mais controle:")
        print()
        print('<label for="id_observacoes" class="form-label">Observações</label>')
        print('<textarea name="observacoes" class="form-control" rows="3" placeholder="Digite suas observações aqui..."></textarea>')
        
    else:
        print("❌ Campo 'observacoes' NÃO encontrado no formulário!")
        print("📋 Campos disponíveis:")
        for field_name in form.fields.keys():
            print(f"  - {field_name}")

if __name__ == "__main__":
    testar_campo_observacoes()