#!/usr/bin/env python
"""
Teste completo do fluxo ICMS: Criar orçamento > Verificar exibição > Editar > Verificar novamente
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

def testar_fluxo_completo():
    """Testar todo o fluxo de ICMS no orçamento"""
    try:
        print("=== TESTE COMPLETO DO FLUXO ICMS ===\n")
        
        # 1. Criar orçamento com ICMS específico
        print("1️⃣ CRIANDO ORÇAMENTO COM ICMS PERSONALIZADO...")
        
        # Deletar teste anterior se existir
        Orcamento.objects.filter(numero_orcamento='TESTE-FLUXO-ICMS').delete()
        
        orcamento = Orcamento.objects.create(
            numero_orcamento='TESTE-FLUXO-ICMS',
            revisao=1,
            cliente='EMPRESA TESTE LTDA',
            uf='RJ',
            contato='Maria Silva',
            telefone='(21) 98888-7777',
            email='teste@empresa.com.br',
            frete='CIF',
            instalacao='INCLUSA',
            venda_destinada='USO_CONSUMO',
            cliente_contrib_icms='NAO_CONTRIBUINTE',
            cnpj_faturamento='11.222.333/0001-44',
            tipo_resina='ISOFTALICA',
            tipo_inox='AISI_316',
            comissao=8.5,
            icms=21.17,  # ICMS para não contribuinte RJ
            validade=date.today() + timedelta(days=45),
            observacoes='Teste completo do fluxo ICMS - Não contribuinte do RJ'
        )
        
        print(f"   ✅ Orçamento criado: ID {orcamento.id}")
        print(f"   📋 Número: {orcamento.numero_orcamento}")
        print(f"   🏢 Cliente: {orcamento.cliente}")
        print(f"   📍 UF: {orcamento.uf}")
        print(f"   💰 ICMS: {orcamento.icms}%")
        print(f"   💼 Comissão: {orcamento.comissao}%")
        print(f"   🏭 Venda: {orcamento.venda_destinada}")
        print(f"   👤 Contribuinte: {orcamento.cliente_contrib_icms}")
        
        # 2. Verificar se os dados estão corretos
        print(f"\n2️⃣ VERIFICANDO DADOS SALVOS...")
        orcamento_db = Orcamento.objects.get(id=orcamento.id)
        
        assert float(orcamento_db.icms) == 21.17, f"ICMS incorreto: esperado 21.17, encontrado {orcamento_db.icms}"
        assert float(orcamento_db.comissao) == 8.5, f"Comissão incorreta: esperado 8.5, encontrado {orcamento_db.comissao}"
        assert orcamento_db.uf == 'RJ', f"UF incorreta: esperado RJ, encontrado {orcamento_db.uf}"
        assert orcamento_db.venda_destinada == 'USO_CONSUMO', f"Venda incorreta"
        assert orcamento_db.cliente_contrib_icms == 'NAO_CONTRIBUINTE', f"Contribuinte incorreto"
        
        print(f"   ✅ Todos os campos salvos corretamente!")
        
        # 3. Simular edição - alterar ICMS e comissão
        print(f"\n3️⃣ SIMULANDO EDIÇÃO DO ORÇAMENTO...")
        orcamento_db.icms = 18.0  # Alterar ICMS
        orcamento_db.comissao = 10.0  # Alterar comissão
        orcamento_db.uf = 'SP'  # Alterar UF
        orcamento_db.save()
        
        print(f"   ✅ Orçamento editado!")
        print(f"   💰 Novo ICMS: {orcamento_db.icms}%")
        print(f"   💼 Nova Comissão: {orcamento_db.comissao}%")
        print(f"   📍 Nova UF: {orcamento_db.uf}")
        
        # 4. Verificar se as alterações foram salvas
        print(f"\n4️⃣ VERIFICANDO ALTERAÇÕES...")
        orcamento_final = Orcamento.objects.get(id=orcamento.id)
        
        assert float(orcamento_final.icms) == 18.0, f"ICMS não foi atualizado"
        assert float(orcamento_final.comissao) == 10.0, f"Comissão não foi atualizada"
        assert orcamento_final.uf == 'SP', f"UF não foi atualizada"
        
        print(f"   ✅ Todas as alterações salvas corretamente!")
        
        # 5. Exibir URLs para teste manual
        print(f"\n5️⃣ URLS PARA TESTE MANUAL:")
        print(f"   🔗 Ver Orçamento: http://127.0.0.1:8000/orcamento/{orcamento.id}/")
        print(f"   ✏️  Editar Orçamento: http://127.0.0.1:8000/orcamento/{orcamento.id}/edit/")
        
        # 6. Verificar template de exibição
        print(f"\n6️⃣ CAMPOS QUE DEVEM APARECER NA TELA:")
        print(f"   📋 Número: {orcamento_final.numero_orcamento}")
        print(f"   🏢 Cliente: {orcamento_final.cliente}")
        print(f"   📞 Contato: {orcamento_final.contato}")
        print(f"   📱 Telefone: {orcamento_final.telefone}")
        print(f"   📧 Email: {orcamento_final.email}")
        print(f"   📍 UF: {orcamento_final.uf}")
        print(f"   💰 ICMS: {orcamento_final.icms}% (badge azul)")
        print(f"   💼 Comissão: {orcamento_final.comissao}% (badge cinza)")
        print(f"   📊 Status: {orcamento_final.status} (badge amarelo)")
        
        print(f"\n✅ TESTE COMPLETO FINALIZADO COM SUCESSO!")
        print(f"🎯 O ICMS e Comissão devem aparecer nos detalhes do orçamento!")
        
        return orcamento.id
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    orcamento_id = testar_fluxo_completo()
    
    if orcamento_id:
        print(f"\n🚀 Abra o navegador e acesse:")
        print(f"   http://127.0.0.1:8000/orcamento/{orcamento_id}/")
        print(f"\n🔍 Verifique se o ICMS e Comissão aparecem nos detalhes!")
        print(f"✏️  Teste também o botão 'Editar Orçamento' para ver se funciona!")