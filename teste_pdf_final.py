#!/usr/bin/env python
"""
Teste do PDF final com layout FIBERMEYER
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

def test_pdf_generation():
    """Testa a geração do PDF"""
    print("🧪 Testando geração do PDF com layout FIBERMEYER...")
    
    try:
        # Buscar um orçamento existente
        orcamento = Orcamento.objects.first()
        if not orcamento:
            print("❌ Nenhum orçamento encontrado no banco de dados")
            return
        
        print(f"✅ Orçamento encontrado: ID {orcamento.id}")
        print(f"   Cliente: {orcamento.cliente}")
        print(f"   Itens: {orcamento.itens.count()}")
        
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
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(response.content)
                print(f"   Arquivo salvo em: {tmp.name}")
                
                # Tentar abrir o PDF
                try:
                    os.startfile(tmp.name)
                    print("📄 PDF aberto automaticamente!")
                except:
                    print("📄 PDF salvo (abra manualmente)")
        else:
            print(f"❌ Erro na geração: Status {response.status_code}")
            print(f"   Conteúdo: {response.content}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()