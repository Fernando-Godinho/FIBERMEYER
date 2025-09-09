#!/usr/bin/env python
"""
Script para adicionar parâmetros de mão de obra ao template 'Novo Perfil'
Adiciona: VELOCIDADE M/H, N° MATRIZES, N° DE MAQUINAS UTILIZADAS
"""
import os
import sys
import django

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate

def atualizar_novo_perfil_mao_obra():
    print("=== ATUALIZANDO TEMPLATE 'NOVO PERFIL' COM MÃO DE OBRA ===")
    
    try:
        # Buscar o template 'Novo Perfil'
        template = ProdutoTemplate.objects.filter(produto_base__descricao__icontains='Novo Perfil').first()
        
        if not template:
            # Tentar encontrar por nome do produto base ou criar novo
            from main.models import MP_Produtos
            
            # Procurar produto base existente
            produto_base = MP_Produtos.objects.filter(
                descricao__icontains='perfil'
            ).first()
            
            if not produto_base:
                print("❌ Nenhum produto base encontrado para 'Novo Perfil'")
                print("Criando produto base...")
                
                produto_base = MP_Produtos.objects.create(
                    descricao='Novo Perfil',
                    unidade='M',
                    custo_centavos=0,
                    peso_und=0.000,
                    referencia='PERFIL-TEMPLATE',
                    tipo_produto='parametrizado',
                    categoria='Perfil',
                    subcategoria='Template'
                )
                print(f"✅ Produto base criado: {produto_base.descricao}")
            
            # Criar template
            template = ProdutoTemplate.objects.create(
                produto_base=produto_base,
                parametros_obrigatorios=['roving_4400', 'manta_300', 'veu', 'peso_m'],
                parametros_opcionais={
                    'tipo_resina': '1269',
                    'perda_processo': '3'
                }
            )
            print(f"✅ Template criado: {template}")
        
        print(f"📋 Template encontrado: {template}")
        print(f"   ID: {template.id}")
        print(f"   Produto base: {template.produto_base.descricao}")
        
        # Parâmetros atuais
        print(f"\n📝 Parâmetros obrigatórios atuais: {template.parametros_obrigatorios}")
        print(f"📝 Parâmetros opcionais atuais: {template.parametros_opcionais}")
        
        # Adicionar novos parâmetros de mão de obra aos parâmetros opcionais
        novos_parametros_opcionais = template.parametros_opcionais.copy()
        
        # Parâmetros de mão de obra com valores padrão
        parametros_mao_obra = {
            'velocidade_m_h': '1.0',           # 1.0 m/h como padrão
            'num_matrizes': '1',               # 1 matriz como padrão
            'num_maquinas_utilizadas': '1'     # 1 máquina como padrão
        }
        
        # Adicionar os novos parâmetros
        for param, valor_default in parametros_mao_obra.items():
            novos_parametros_opcionais[param] = valor_default
            print(f"➕ Adicionando parâmetro: {param} = {valor_default}")
        
        # Atualizar o template
        template.parametros_opcionais = novos_parametros_opcionais
        template.save()
        
        print(f"\n✅ Template atualizado com sucesso!")
        print(f"📝 Novos parâmetros opcionais: {template.parametros_opcionais}")
        
        # Verificar se existe mão de obra de Pultrusão
        from main.models import MaoObra
        
        pultrusao = MaoObra.objects.filter(nome__icontains='pultrusão').first()
        if not pultrusao:
            pultrusao = MaoObra.objects.filter(nome__icontains='pultrusao').first()
        
        if pultrusao:
            print(f"\n🏭 Mão de obra 'Pultrusão' encontrada:")
            print(f"   Nome: {pultrusao.nome}")
            print(f"   Valor: R$ {pultrusao.valor_real:.2f}")
            print(f"   Unidade: {pultrusao.unidade}")
        else:
            print(f"\n⚠️ Mão de obra 'Pultrusão' não encontrada!")
            print(f"   Criando entrada padrão...")
            
            pultrusao = MaoObra.objects.create(
                nome='Pultrusão',
                descricao='Processo de pultrusão para perfis de fibra de vidro',
                valor_centavos=5000,  # R$ 50,00
                unidade='H',
                ativo=True
            )
            print(f"✅ Mão de obra criada: {pultrusao.nome} - R$ {pultrusao.valor_real:.2f}/H")
        
        print(f"\n🎯 FÓRMULA DE CÁLCULO IMPLEMENTADA:")
        print(f"   Custo MO = ((custo_pultrusao / 3) * num_maquinas_utilizadas) /")
        print(f"              (velocidade_m_h * num_matrizes * 24 * 21 * 0.5)")
        print(f"   Onde:")
        print(f"   - custo_pultrusao = valor da base de mão de obra")
        print(f"   - 3 = quantidade total de máquinas")
        print(f"   - 24 = horas por dia")
        print(f"   - 21 = dias por mês")
        print(f"   - 0.5 = rendimento")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar template: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    atualizar_novo_perfil_mao_obra()
