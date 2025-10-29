#!/usr/bin/env python
"""
Teste das observações personalizadas no PDF do orçamento
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento
from django.test import RequestFactory
from main.views_pdf import gerar_pdf_orcamento
import tempfile

def test_observacoes_pdf():
    """Testa a geração do PDF com observações personalizadas"""
    print("🧪 Testando PDF com observações personalizadas...")
    
    try:
        # Buscar um orçamento existente
        orcamento = Orcamento.objects.first()
        if not orcamento:
            print("❌ Nenhum orçamento encontrado no banco de dados")
            return
        
        # Adicionar observações de teste
        observacoes_teste = """Observações específicas para este orçamento:

• Produto deve ser entregue em embalagem especial
• Instalação deve ser agendada com 48h de antecedência
• Cliente solicita pintura personalizada nas cores azul e branco
• Garantia estendida de 24 meses para este projeto específico

Dados técnicos adicionais:
- Resistência mínima: 500kg/m²
- Temperatura de operação: -10°C a +60°C
- Certificação NBR 15575 obrigatória"""

        orcamento.observacoes = observacoes_teste
        orcamento.save()
        
        print(f"✅ Orçamento {orcamento.id} atualizado com observações")
        print(f"   Cliente: {orcamento.cliente}")
        print(f"   Itens: {orcamento.itens.count()}")
        print(f"   Tamanho das observações: {len(observacoes_teste)} caracteres")
        
        # Criar requisição fake
        factory = RequestFactory()
        request = factory.get(f'/pdf/{orcamento.id}/')
        
        # Gerar PDF
        response = gerar_pdf_orcamento(request, orcamento.id)
        
        if response.status_code == 200:
            print("✅ PDF gerado com sucesso!")
            print(f"   Content-Type: {response.get('Content-Type')}")
            print(f"   Tamanho: {len(response.content)} bytes")
            
            # Salvar o PDF para visualização
            filename = f'orcamento_{orcamento.id}_com_observacoes.pdf'
            with open(filename, 'wb') as f:
                f.write(response.content)
                print(f"   Arquivo salvo em: {os.path.abspath(filename)}")
                
                # Tentar abrir o PDF
                try:
                    os.startfile(filename)
                    print("📄 PDF aberto automaticamente!")
                except:
                    print("📄 PDF salvo (abra manualmente)")
                    
            print("\n📋 Instruções para verificar:")
            print("1. Abra o PDF gerado")
            print("2. Vá até a última página")
            print("3. Procure pela seção 'OBSERVAÇÕES ADICIONAIS'")
            print("4. Verifique se as observações personalizadas aparecem formatadas")
            
        else:
            print(f"❌ Erro na geração: Status {response.status_code}")
            print(f"   Conteúdo: {response.content}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_observacoes_pdf()