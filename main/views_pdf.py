#!/usr/bin/env python
"""
Views para geração de PDF de orçamentos
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
from datetime import datetime
import json
import io

try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from .models import Orcamento

def gerar_pdf_orcamento(request, orcamento_id):
    """
    Gera PDF do orçamento com layout FIBERMEYER usando ReportLab
    """
    if not REPORTLAB_AVAILABLE:
        return HttpResponse(
            "Biblioteca ReportLab não está instalada. Execute: pip install reportlab",
            status=500
        )
    
    # Buscar orçamento
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    
    # Criar PDF em memória com orientação paisagem
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=1*cm, leftMargin=1*cm, 
                           topMargin=1*cm, bottomMargin=1*cm)
    
    # Lista para armazenar elementos do PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Dados do cliente
    cliente_nome = orcamento.cliente
    cliente_uf = orcamento.uf
    cliente_contato = orcamento.contato
    cliente_telefone = orcamento.telefone
    cliente_email = orcamento.email
    cliente_cnpj = orcamento.cnpj_faturamento if orcamento.cnpj_faturamento else '00.000.000/0000-00'
    
    # Estilo personalizado para cabeçalho da empresa
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    # Estilo para título
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.white,
        backColor=colors.HexColor('#4a5568'),
        spaceAfter=6,
        spaceBefore=6
    )
    
    # Cabeçalho com layout FIBERMEYER exato do modelo
    page_width = landscape(A4)[0] - 2*cm  # largura total menos margens
    
    # Criar dados do cabeçalho em 3 colunas como no modelo
    header_data = [
        [
            'FIBERMEYER IND E COM\nDE ARTEFATOS\nEM FIBRA DE VIDRO LTDA\nCNPJ: 89.671.812/0001-72 | I.E. 152/0016453\nFone/WhatsApp: (51) 3451-6619\ncomercial@fibermeyer.com.br\nwww.fibermeyer.com.br\nRodovia RS 118 n° 6611 - Sapucaia do Sul/RS\nCEP: 93230-390',
            'FIBERMEYER',
            f'Cliente: {cliente_nome}\nUF: {cliente_uf}\nContato: {cliente_contato}\nTelefone: {cliente_telefone}\nEmail: {cliente_email}\nCNPJ: {cliente_cnpj}'
        ]
    ]
    
    # Larguras das colunas: esquerda 35%, centro 30%, direita 35%
    header_table = Table(header_data, colWidths=[page_width * 0.35, page_width * 0.30, page_width * 0.35])
    
    # Estilo para texto da empresa (esquerda)
    company_left_style = ParagraphStyle(
        'CompanyLeft',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        leading=12
    )
    
    # Estilo para logo FIBERMEYER (centro) - tamanho reduzido
    logo_style = ParagraphStyle(
        'LogoStyle',
        parent=styles['Normal'],
        fontSize=24,  # Reduzido de 32 para 24
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=26   # Ajustado proporcionalmente
    )
    
    # Criar texto da logo com cores (F em laranja, resto em azul)
    logo_text = '<font color="#ff6600">F</font><font color="#1e40af">IBERMEYER</font>'
    
    # Estilo para contatos (direita) - texto menor para caber mais informação
    company_right_style = ParagraphStyle(
        'CompanyRight',
        parent=styles['Normal'],
        fontSize=9,  # Reduzido para caber mais informação
        alignment=TA_RIGHT,
        leading=10
    )
    
    # Reformatar os dados com estilos - informações do cliente mais centralizadas
    formatted_header_data = [[
        Paragraph('FIBERMEYER IND E COM<br/>DE ARTEFATOS<br/>EM FIBRA DE VIDRO LTDA<br/>CNPJ: 89.671.812/0001-72 | I.E. 152/0016453<br/>Fone/WhatsApp: (51) 3451-6619<br/>comercial@fibermeyer.com.br<br/><b>www.fibermeyer.com.br</b><br/>Rodovia RS 118 n° 6611 - Sapucaia do Sul/RS<br/>CEP: 93230-390', company_left_style),
        Paragraph(f'<b>{logo_text}</b>', logo_style),
        Paragraph(f'<b>Cliente:</b> {cliente_nome}<br/><b>UF:</b> {cliente_uf}<br/><b>Contato:</b> {cliente_contato}<br/><b>Telefone:</b> {cliente_telefone}<br/><b>Email:</b> {cliente_email}<br/><b>CNPJ:</b> {cliente_cnpj}<br/><br/><b>Proposta n°:</b> 00.{orcamento.id:04d}<br/><b>Revisão:</b> 0<br/><b>Data:</b> {datetime.now().strftime("%d/%m/%Y")}', company_right_style)
    ]]
    
    # Larguras das colunas: esquerda 30%, centro 25%, direita 45% (mais espaço à direita)
    header_table = Table(formatted_header_data, colWidths=[page_width * 0.30, page_width * 0.25, page_width * 0.45])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Título PROPOSTA COMERCIAL com faixa azul mais fina
    proposta_title = ParagraphStyle(
        'PropostaTitle',
        parent=styles['Normal'],
        fontSize=12,  # Reduzido de 14 para 12
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=0.4*cm,  # Aumentado para dar mais espaço após a faixa
        spaceBefore=0.1*cm,
        textColor=colors.white,
        backColor=colors.HexColor('#2563eb'),  # Azul da faixa
        borderPadding=4  # Reduzido de 6 para 4 (faixa mais fina)
    )
    elements.append(Paragraph('<b>PROPOSTA COMERCIAL</b>', proposta_title))
    
    # Processar produtos com as 5 colunas essenciais
    produtos_data = []
    
    # Buscar itens do orçamento
    itens = orcamento.itens.all()
    for i, item in enumerate(itens, 1):
        produtos_data.append([
            str(i),
            str(item.quantidade),
            item.descricao,
            f"R$ {float(item.valor_unitario):.2f}".replace('.', ','),
            f"R$ {float(item.valor_total):.2f}".replace('.', ',')
        ])
    
    # Adicionar linhas vazias para completar a tabela (mínimo 8 linhas)
    while len(produtos_data) < 8:
        produtos_data.append(['', '', '', '', ''])
    
    # Cabeçalho da tabela com as mesmas colunas do orçamento
    table_header = [
        ['ITEM', 'QTDE', 'DESCRIÇÃO DOS PRODUTOS', 'VALOR UNIT.', 'VALOR TOTAL']
    ]
    
    # Dados completos da tabela
    table_data = table_header + produtos_data
    
    # Criar tabela com layout das 5 colunas essenciais
    table = Table(table_data, colWidths=[
        1.5*cm,   # ITEM
        2*cm,     # QTDE
        11*cm,    # DESCRIÇÃO DOS PRODUTOS (mais espaço)
        3*cm,     # VALOR UNIT.
        3*cm      # VALOR TOTAL
    ])
    
    # Estilo da tabela com faixa azul mais fina no cabeçalho
    table.setStyle(TableStyle([
        # Cabeçalho - faixa azul mais fina
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),  # Reduzido de 8 para 7
        
        # Corpo da tabela - apenas 5 colunas
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ITEM
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # QTDE
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # DESCRIÇÃO DOS PRODUTOS
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),   # VALOR UNIT.
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),   # VALOR TOTAL
        
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        
        # Bordas
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Padding ainda menor para faixa mais fina
        ('TOPPADDING', (0, 0), (-1, -1), 2),  # Reduzido de 3 para 2
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # Reduzido de 3 para 2
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Observações no final do PDF mais próximas do modelo
    observacoes_style = ParagraphStyle(
        'ObservacoesStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_LEFT,
        spaceAfter=3,
        leading=11
    )
    
    observacoes_text = """
    <b>OBSERVAÇÕES:</b><br/>
    • Valores válidos por 30 dias a partir da data de emissão.<br/>
    • Condições de pagamento: A combinar.<br/>
    • Frete por conta do cliente.<br/>
    • Prazo de entrega: Sob consulta após confirmação do pedido.
    """
    
    elements.append(Paragraph(observacoes_text, observacoes_style))
    elements.append(Spacer(1, 0.2*cm))
    
    # Rodapé minimalista
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=7,
        alignment=TA_CENTER,
        textColor=colors.grey,
        leading=9
    )
    
    footer_text = f"""
    Orçamento gerado em {datetime.now().strftime('%d/%m/%Y')} - FIBERMEYER Soluções em Fibra de Vidro
    """
    
    elements.append(Paragraph(footer_text, footer_style))
    
    # Construir PDF
    doc.build(elements)
    
    # Obter PDF
    pdf = buffer.getvalue()
    buffer.close()
    
    # Retornar PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="orcamento_{orcamento.id}.pdf"'
    
    return response

def preview_pdf_orcamento(request, orcamento_id):
    """
    Preview HTML do orçamento (antes de gerar PDF)
    """
    # Buscar orçamento
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    
    # Processar itens
    produtos = []
    itens = orcamento.itens.all()
    for i, item in enumerate(itens, 1):
        produtos.append({
            'item': i,
            'qtd': item.quantidade,
            'descricao': item.descricao,
            'unid': 'unid',
            'rs_unit': f"R$ {float(item.valor_unitario):.2f}".replace('.', ','),
            'rs_total': f"R$ {float(item.valor_total):.2f}".replace('.', ','),
            'ipi': '3,25',
            'ncm': '3925.90.90',
            'observacoes': ''
        })
    
    # Dados do orçamento
    context = {
        'orcamento': orcamento,
        'produtos': produtos,
        'data_atual': datetime.now().strftime('%d/%m/%Y'),
        'proposta_numero': f"00.{orcamento.id:04d}",
        'cliente': {
            'nome': orcamento.cliente,
            'uf': orcamento.uf,
            'contato': orcamento.contato,
            'telefone': orcamento.telefone,
            'email': orcamento.email,
            'cnpj': orcamento.cnpj_faturamento if orcamento.cnpj_faturamento else '00.000.000/0000-00',
        }
    }
    
    # Renderizar template HTML
    return render(request, 'main/pdf_orcamento.html', context)

def preview_pdf_orcamento(request, orcamento_id):
    """
    Preview do PDF em HTML (para desenvolvimento)
    """
    # Buscar orçamento
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    
    # Processar produtos JSON
    produtos = []
    if orcamento.produtos:
        try:
            produtos_data = json.loads(orcamento.produtos) if isinstance(orcamento.produtos, str) else orcamento.produtos
            for i, produto in enumerate(produtos_data, 1):
                produtos.append({
                    'item': i,
                    'qtd': produto.get('quantidade', 1),
                    'descricao': produto.get('nome', produto.get('descricao', 'Produto')),
                    'unid': produto.get('unidade', 'unid'),
                    'rs_unit': f"R$ {float(produto.get('custo_unitario', 0)) / 100:.2f}".replace('.', ','),
                    'rs_total': f"R$ {float(produto.get('custo_total', 0)) / 100:.2f}".replace('.', ','),
                    'ipi': produto.get('ipi', '3,25'),
                    'ncm': produto.get('ncm', '3925.90.90'),
                    'observacoes': produto.get('observacoes', '')
                })
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Erro ao processar produtos: {e}")
    
    # Dados do orçamento
    context = {
        'orcamento': orcamento,
        'produtos': produtos,
        'data_atual': datetime.now().strftime('%d/%m/%Y'),
        'proposta_numero': f"00.{orcamento.id:04d}",
        'cliente': {
            'nome': getattr(orcamento, 'cliente_nome', ''),
            'uf': getattr(orcamento, 'cliente_uf', ''),
            'contato': getattr(orcamento, 'cliente_contato', ''),
            'telefone': getattr(orcamento, 'cliente_telefone', ''),
            'email': getattr(orcamento, 'cliente_email', ''),
            'cnpj': getattr(orcamento, 'cliente_cnpj', '00.000.000/0000-00'),
        }
    }
    
    return render(request, 'main/pdf_orcamento.html', context)