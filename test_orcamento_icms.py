#!/usr/bin/env python
"""
Script para testar se o ICMS está sendo salvo e exibido corretamente no orçamento
"""
import os
import sys
import django
from datetime import date, timedelta

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import Orcamento

def criar_orcamento_teste():
    """Criar um orçamento de teste com ICMS específico"""
    try:
        # Deletar orçamento de teste anterior se existir
        Orcamento.objects.filter(numero_orcamento='TESTE-ICMS').delete()
        
        # Criar novo orçamento
        orcamento = Orcamento.objects.create(
            numero_orcamento='TESTE-ICMS',
            revisao=1,
            cliente='Cliente Teste ICMS',
            uf='SP',
            contato='João Teste',
            telefone='(11) 99999-9999',
            email='teste@teste.com',
            frete='CIF',
            instalacao='NAO_INCLUSA',
            venda_destinada='INDUSTRIALIZACAO',
            cliente_contrib_icms='CONTRIBUINTE',
            cnpj_faturamento='12.345.678/0001-90',
            tipo_resina='POLIESTER',
            tipo_inox='AISI_304',
            comissao=5.0,
            icms=18.0,  # ICMS específico para teste
            validade=date.today() + timedelta(days=30),
            observacoes='Orçamento de teste para validar ICMS'
        )
        
        print(f"✅ Orçamento criado com sucesso!")
        print(f"   ID: {orcamento.id}")
        print(f"   Número: {orcamento.numero_orcamento}")
        print(f"   Cliente: {orcamento.cliente}")
        print(f"   UF: {orcamento.uf}")
        print(f"   ICMS: {orcamento.icms}%")
        print(f"   Comissão: {orcamento.comissao}%")
        print(f"   Status: {orcamento.status}")
        
        return orcamento.id
        
    except Exception as e:
        print(f"❌ Erro ao criar orçamento: {e}")
        return None

def verificar_orcamento(orcamento_id):
    """Verificar se o orçamento foi salvo com os dados corretos"""
    try:
        orcamento = Orcamento.objects.get(id=orcamento_id)
        
        print(f"\n=== VERIFICAÇÃO DO ORÇAMENTO ===")
        print(f"ID: {orcamento.id}")
        print(f"Número: {orcamento.numero_orcamento}")
        print(f"Cliente: {orcamento.cliente}")
        print(f"UF: {orcamento.uf}")
        print(f"ICMS: {orcamento.icms}% (tipo: {type(orcamento.icms)})")
        print(f"Comissão: {orcamento.comissao}% (tipo: {type(orcamento.comissao)})")
        print(f"Venda Destinada: {orcamento.venda_destinada}")
        print(f"Cliente Contrib ICMS: {orcamento.cliente_contrib_icms}")
        print(f"Status: {orcamento.status}")
        print(f"Criado em: {orcamento.criado_em}")
        
        # Verificar se os campos estão sendo salvos corretamente
        assert orcamento.icms == 18.0, f"ICMS esperado: 18.0, encontrado: {orcamento.icms}"
        assert orcamento.comissao == 5.0, f"Comissão esperada: 5.0, encontrada: {orcamento.comissao}"
        assert orcamento.uf == 'SP', f"UF esperada: SP, encontrada: {orcamento.uf}"
        
        print(f"\n✅ Todos os testes passaram!")
        print(f"📋 URL para visualizar: http://127.0.0.1:8000/orcamento/{orcamento.id}/")
        
        return True
        
    except Orcamento.DoesNotExist:
        print(f"❌ Orçamento ID {orcamento_id} não encontrado")
        return False
    except AssertionError as e:
        print(f"❌ Teste falhou: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def listar_orcamentos():
    """Listar todos os orçamentos para verificar"""
    try:
        orcamentos = Orcamento.objects.all().order_by('-id')[:5]
        
        print(f"\n=== ÚLTIMOS 5 ORÇAMENTOS ===")
        for orc in orcamentos:
            print(f"ID: {orc.id} | {orc.numero_orcamento} | {orc.cliente} | UF: {orc.uf} | ICMS: {orc.icms}% | Comissão: {orc.comissao}%")
            
    except Exception as e:
        print(f"❌ Erro ao listar orçamentos: {e}")

if __name__ == "__main__":
    print("=== TESTE DE SALVAMENTO E EXIBIÇÃO DO ICMS ===\n")
    
    # Listar orçamentos existentes
    listar_orcamentos()
    
    # Criar orçamento de teste
    print(f"\n=== CRIANDO ORÇAMENTO DE TESTE ===")
    orcamento_id = criar_orcamento_teste()
    
    if orcamento_id:
        # Verificar se foi salvo corretamente
        verificar_orcamento(orcamento_id)
        
        # Listar novamente para ver o novo
        listar_orcamentos()
    
    print(f"\n=== TESTE CONCLUÍDO ===")