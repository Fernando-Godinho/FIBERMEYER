#!/usr/bin/env python
"""
Script para testar o cálculo do template 'Novo Perfil' com mão de obra
"""
import os
import sys
import django
import json

# Adicionar o projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MaoObra

def test_novo_perfil_com_mao_obra():
    print("=== TESTE DE CÁLCULO DO TEMPLATE 'NOVO PERFIL' COM MÃO DE OBRA ===\n")
    
    # Buscar o template
    template = ProdutoTemplate.objects.filter(produto_base__descricao__icontains='Novo Perfil').first()
    if not template:
        print("❌ Template 'Novo Perfil' não encontrado!")
        return
    
    print(f"✅ Template encontrado: {template}")
    print(f"   ID: {template.id}")
    print(f"   Produto base: {template.produto_base.descricao}")
    print(f"   Parâmetros obrigatórios: {template.parametros_obrigatorios}")
    print(f"   Parâmetros opcionais: {template.parametros_opcionais}")
    
    # Verificar mão de obra de pultrusão
    pultrusao = MaoObra.objects.filter(nome__icontains='pultrusão').first()
    if not pultrusao:
        pultrusao = MaoObra.objects.filter(nome__icontains='pultrusao').first()
    
    if pultrusao:
        print(f"\n🏭 Mão de obra encontrada:")
        print(f"   Nome: {pultrusao.nome}")
        print(f"   Valor: R$ {pultrusao.valor_real:.2f}")
        print(f"   Valor em centavos: {pultrusao.valor_centavos}")
        print(f"   Unidade: {pultrusao.unidade}")
    else:
        print(f"\n⚠️ Mão de obra 'Pultrusão' não encontrada!")
        return
    
    # Parâmetros de teste com mão de obra
    parametros_teste = {
        'roving_4400': '2.5',              # 2.5 kg de roving
        'manta_300': '1.2',                # 1.2 kg de manta  
        'veu': '0.3',                      # 0.3 kg de véu
        'peso_m': '8.0',                   # 8.0 kg/m peso total
        'tipo_resina': '1269',             # Resina Poliéster
        'perda_processo': '3',             # 3% de perda
        'velocidade_m_h': '2.0',           # 2.0 m/h
        'num_matrizes': '2',               # 2 matrizes
        'num_maquinas_utilizadas': '1',    # 1 máquina
        'descricao': 'Perfil teste com mão de obra'
    }
    
    print(f"\n📝 Parâmetros de teste:")
    for param, valor in parametros_teste.items():
        print(f"   {param}: {valor}")
    
    # Simular cálculo manualmente usando a mesma lógica da view
    try:
        print(f"\n=== SIMULANDO CÁLCULO MANUAL ===")
        
        # Importar modelos necessários
        from main.models import MP_Produtos
        
        # Mapeamento dos componentes (mesmo da view)
        componentes_mp_ids = {
            'roving_4400': 1237,
            'manta_300': 1238,
            'veu': 1239,
            'monomero_estireno': 1266,
            'anti_uv': 1243,
            'anti_ox': 1244,
            'bpo': 1245,
            'tbpb': 1246,
            'desmoldante': 1247,
            'antichama': 1248,
            'carga_mineral': 1249,
            'pigmento': 1250,
        }
        
        # Buscar preços dos produtos
        produtos_mp = {}
        for componente, mp_id in componentes_mp_ids.items():
            try:
                produto = MP_Produtos.objects.get(id=mp_id)
                produtos_mp[componente] = {
                    'nome': produto.descricao,
                    'preco_centavos': produto.custo_centavos
                }
            except MP_Produtos.DoesNotExist:
                produtos_mp[componente] = {
                    'nome': componente.replace('_', ' ').title(),
                    'preco_centavos': 1000
                }
        
        # Buscar resina selecionada
        tipo_resina_id = parametros_teste.get('tipo_resina', '1269')
        try:
            resina_mp = MP_Produtos.objects.get(id=int(tipo_resina_id))
            produtos_mp['resina'] = {
                'nome': resina_mp.descricao,
                'preco_centavos': resina_mp.custo_centavos
            }
        except MP_Produtos.DoesNotExist:
            produtos_mp['resina'] = {
                'nome': "Resina Poliéster",
                'preco_centavos': 1296
            }
        
        # Calcular custos dos materiais
        custo_total = 0
        peso_total = 0
        componentes = []
        
        # Componentes diretos
        for comp_nome, param_nome in [('roving_4400', 'roving_4400'), ('manta_300', 'manta_300'), ('veu', 'veu')]:
            if param_nome in parametros_teste and comp_nome in produtos_mp:
                qtd = float(parametros_teste[param_nome])
                produto_info = produtos_mp[comp_nome]
                custo_comp = qtd * produto_info['preco_centavos']
                custo_total += custo_comp
                peso_total += qtd
                
                componentes.append({
                    'nome': produto_info['nome'],
                    'quantidade': qtd,
                    'custo_unitario': produto_info['preco_centavos'],
                    'custo_total': custo_comp
                })
        
        # Peso base
        peso_base = float(parametros_teste['peso_m'])
        peso_total = peso_base
        
        # Componentes calculados
        componentes_calculados = [
            ('resina', 0.6897),
            ('monomero_estireno', 0.0213),
            ('anti_uv', 0.0028),
            ('anti_ox', 0.0028),
            ('bpo', 0.0172),
            ('tbpb', 0.0086),
            ('desmoldante', 0.0086),
            ('antichama', 0.0430),
            ('carga_mineral', 0.0645),
            ('pigmento', 0.0086),
        ]
        
        for componente_key, fator in componentes_calculados:
            if componente_key in produtos_mp:
                produto_info = produtos_mp[componente_key]
                quantidade = peso_base * fator
                custo_componente = quantidade * produto_info['preco_centavos']
                custo_total += custo_componente
                
                componentes.append({
                    'nome': produto_info['nome'],
                    'quantidade': round(quantidade, 4),
                    'custo_unitario': produto_info['preco_centavos'],
                    'custo_total': round(custo_componente, 2)
                })
        
        # Aplicar perda de processo
        perda = float(parametros_teste.get('perda_processo', 0))
        custo_total = custo_total * (1 + perda / 100)
        
        # CALCULAR MÃO DE OBRA
        custo_mao_obra = 0
        velocidade_m_h = float(parametros_teste['velocidade_m_h'])
        num_matrizes = float(parametros_teste['num_matrizes'])
        num_maquinas_utilizadas = float(parametros_teste['num_maquinas_utilizadas'])
        
        # Constantes
        qtd_maquinas_total = 3
        horas_dia = 24
        dias_mes = 21
        rendimento = 0.5
        
        custo_pultrusao = pultrusao.valor_centavos
        
        if velocidade_m_h > 0 and num_matrizes > 0:
            numerador = (custo_pultrusao / qtd_maquinas_total) * num_maquinas_utilizadas
            denominador = velocidade_m_h * num_matrizes * horas_dia * dias_mes * rendimento
            custo_mao_obra = numerador / denominador
            
            componentes.append({
                'nome': 'Mão de Obra - Pultrusão',
                'quantidade': 1.0,
                'custo_unitario': int(custo_mao_obra),
                'custo_total': int(custo_mao_obra)
            })
            
            custo_total += custo_mao_obra
        
        # Mostrar resultados
        print(f"💰 Custo total: R$ {custo_total/100:.2f}")
        print(f"⚖️ Peso total: {peso_total} kg")
        print(f"📦 Componentes: {len(componentes)}")
        
        print(f"\n=== DETALHES DOS COMPONENTES ===")
        custo_materiais = 0
        custo_mo = 0
        
        for comp in componentes:
            custo = comp['custo_total']
            print(f"{comp['nome']:25} | Qtd: {comp['quantidade']:8.3f} | Custo Unit: R$ {comp['custo_unitario']/100:6.2f} | Total: R$ {custo/100:8.2f}")
            
            if 'Mão de Obra' in comp['nome']:
                custo_mo += custo
            else:
                custo_materiais += custo
        
        print(f"\n=== RESUMO DE CUSTOS ===")
        print(f"💧 Materiais:     R$ {custo_materiais/100:.2f}")
        print(f"👷 Mão de Obra:  R$ {custo_mo/100:.2f}")
        print(f"💰 TOTAL:        R$ {custo_total/100:.2f}")
        
        # Verificação do cálculo de MO
        print(f"\n🔍 VERIFICAÇÃO DO CÁLCULO DE MÃO DE OBRA:")
        print(f"   Custo Pultrusão: R$ {custo_pultrusao/100:.2f} ({custo_pultrusao} centavos)")
        print(f"   Fórmula: (({custo_pultrusao} / {qtd_maquinas_total}) * {num_maquinas_utilizadas}) / ({velocidade_m_h} * {num_matrizes} * {horas_dia} * {dias_mes} * {rendimento})")
        print(f"   Numerador: {numerador:.2f}")
        print(f"   Denominador: {denominador}")
        print(f"   Resultado: R$ {custo_mao_obra/100:.2f}")
        print(f"   ✅ Mão de obra adicionada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na simulação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_novo_perfil_com_mao_obra()
