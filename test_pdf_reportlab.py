#!/usr/bin/env python
"""
Teste da funcionalidade de PDF usando ReportLab
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Orcamento, OrcamentoItem
from django.test import RequestFactory
from main.views_pdf import gerar_pdf_orcamento

def test_pdf_generation():
    """Teste da geração de PDF com ReportLab"""
    print("=== TESTE DE GERAÇÃO DE PDF COM REPORTLAB ===")
    
    # Verificar se ReportLab está disponível
    try:
        import reportlab
        print(f"✅ ReportLab versão {reportlab.Version} encontrado")
    except ImportError:
        print("❌ ReportLab não está instalado")
        return False
    
    # Criar um orçamento de teste se não existir
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("Criando orçamento de teste...")
        from datetime import datetime, timedelta
        orcamento = Orcamento.objects.create(
            numero_orcamento="TESTE-001",
            cliente="Teste Cliente LTDA",
            uf="RS",
            contato="João Silva",
            telefone="(51) 99999-9999",
            email="joao@testecliente.com.br",
            cnpj_faturamento="12.345.678/0001-90",
            validade=datetime.now().date() + timedelta(days=30)
        )
        
        # Criar alguns itens para o orçamento
        OrcamentoItem.objects.create(
            orcamento=orcamento,
            tipo_item="Grade",
            descricao="Grade PFRV 25x38mm",
            quantidade=10.00,
            valor_unitario=150.00,
            valor_total=1500.00
        )
        
        OrcamentoItem.objects.create(
            orcamento=orcamento,
            tipo_item="Perfil",
            descricao="Perfil L 50x50x6mm",
            quantidade=5.00,
            valor_unitario=75.00,
            valor_total=375.00
        )
        
        print(f"✅ Orçamento criado com ID: {orcamento.id}")
    else:
        print(f"✅ Usando orçamento existente ID: {orcamento.id}")
        # Verificar se tem itens
        if not orcamento.itens.exists():
            print("Adicionando itens ao orçamento...")
            OrcamentoItem.objects.create(
                orcamento=orcamento,
                tipo_item="Grade",
                descricao="Grade PFRV 25x38mm",
                quantidade=10.00,
                valor_unitario=150.00,
                valor_total=1500.00
            )
    
    # Simular request
    factory = RequestFactory()
    request = factory.get(f'/pdf/orcamento/{orcamento.id}/')
    
    try:
        # Testar geração do PDF
        print("Gerando PDF...")
        response = gerar_pdf_orcamento(request, orcamento.id)
        
        if response.status_code == 200:
            print("✅ PDF gerado com sucesso!")
            print(f"✅ Content-Type: {response.get('Content-Type')}")
            print(f"✅ Tamanho do PDF: {len(response.content)} bytes")
            
            # Salvar PDF para verificação
            pdf_filename = f"teste_orcamento_{orcamento.id}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ PDF salvo como: {pdf_filename}")
            
            return True
        else:
            print(f"❌ Erro na geração: Status {response.status_code}")
            print(f"❌ Conteúdo: {response.content.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na geração do PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_reportlab_basic():
    """Teste básico do ReportLab"""
    print("\n=== TESTE BÁSICO DO REPORTLAB ===")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        import io
        
        # Criar PDF simples
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        story = [Paragraph("Teste ReportLab - FIBERMEYER", styles['Title'])]
        doc.build(story)
        
        pdf_content = buffer.getvalue()
        buffer.close()
        
        print(f"✅ PDF básico criado: {len(pdf_content)} bytes")
        
        # Salvar teste
        with open("teste_reportlab_basico.pdf", 'wb') as f:
            f.write(pdf_content)
        print("✅ PDF básico salvo como: teste_reportlab_basico.pdf")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste básico: {str(e)}")
        return False

if __name__ == "__main__":
    print("Iniciando testes de PDF com ReportLab...")
    
    # Teste básico primeiro
    basic_ok = test_reportlab_basic()
    
    if basic_ok:
        # Teste completo
        full_ok = test_pdf_generation()
        
        if full_ok:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ ReportLab está funcionando")
            print("✅ PDF de orçamento pode ser gerado")
        else:
            print("\n⚠️ Teste básico OK, mas teste completo falhou")
    else:
        print("\n❌ Teste básico falhou - ReportLab não está funcionando")