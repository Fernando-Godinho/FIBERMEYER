#!/usr/bin/env python
"""
Teste automatizado para criar uma grade com mão de obra via API
"""
import os
import sys
import django
import requests
import json
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos, ProdutoComponente

def test_grade_creation_api():
    print("=== TESTE AUTOMATIZADO DE CRIAÇÃO DE GRADE ===")
    
    base_url = "http://127.0.0.1:8000"
    
    # Dados para criar uma nova grade
    nome_grade = f"GRADE TESTE AUTO {datetime.now().strftime('%H%M%S')}"
    
    dados_grade = {
        "descricao": nome_grade,
        "peso_und": 15.850,  # Será recalculado
        "custo_centavos": 3062,  # Será recalculado
        "unidade": "m²",
        "referencia": f"GRADE-{datetime.now().strftime('%H%M%S')}",
        "tipo_produto": "composto",
        "categoria": "PRODUTO_FINAL"
    }
    
    print(f"1. Criando produto: {nome_grade}")
    
    # Criar o produto
    try:
        response = requests.post(f"{base_url}/api/produtos/", json=dados_grade)
        response.raise_for_status()
        produto = response.json()
        produto_id = produto['id']
        print(f"   ✅ Produto criado: ID {produto_id}")
    except Exception as e:
        print(f"   ❌ Erro ao criar produto: {e}")
        return
    
    # Definir componentes baseados no cálculo de grade
    componentes = [
        {
            "produto_principal": produto_id,
            "produto_componente": 1328,  # I25 Normal
            "quantidade": 0.240,  # Metros lineares por m²
            "observacao": json.dumps({
                "custo_unitario": 1277,
                "custo_total": 306,
                "nome_componente": "Perfil I25 Normal (com 3% perda)",
                "calculated_at": datetime.now().isoformat()
            })
        },
        {
            "produto_principal": produto_id,
            "produto_componente": 1332,  # Chaveta
            "quantidade": 0.016,
            "observacao": json.dumps({
                "custo_unitario": 1277,
                "custo_total": 20,
                "nome_componente": "Chaveta Perfil I (com 3% perda)",
                "calculated_at": datetime.now().isoformat()
            })
        },
        {
            "produto_principal": produto_id,
            "produto_componente": 1183,  # Cola
            "quantidade": 0.062,
            "observacao": json.dumps({
                "custo_unitario": 4500,
                "custo_total": 279,
                "nome_componente": "COLA ESTRUTURAL 4500 A/B (com 3% perda)",
                "calculated_at": datetime.now().isoformat()
            })
        },
        {
            "produto_principal": produto_id,
            "produto_componente": 1374,  # Mão de obra processamento/montagem
            "quantidade": 2.0,  # 1.5h proc + 0.5h montagem
            "observacao": json.dumps({
                "custo_unitario": 6579,  # R$ 65.79/h em centavos
                "custo_total": 1316,  # 2h * R$ 65.79
                "nome_componente": "MÃO DE OBRA Processamento/Montagem",
                "calculated_at": datetime.now().isoformat()
            })
        }
    ]
    
    print(f"\n2. Salvando {len(componentes)} componentes:")
    componentes_salvos = 0
    
    for comp in componentes:
        try:
            response = requests.post(f"{base_url}/api/componentes/", json=comp)
            response.raise_for_status()
            componente_salvo = response.json()
            produto_comp = MP_Produtos.objects.get(id=comp['produto_componente'])
            print(f"   ✅ Componente: {produto_comp.descricao} - Qtd: {comp['quantidade']}")
            componentes_salvos += 1
        except Exception as e:
            print(f"   ❌ Erro ao salvar componente {comp['produto_componente']}: {e}")
    
    print(f"\n3. Forçando recalculação do produto...")
    
    # Forçar recálculo do produto
    try:
        response = requests.patch(f"{base_url}/api/produtos/{produto_id}/", 
                                json={"forcar_recalculo": True})
        response.raise_for_status()
        produto_atualizado = response.json()
        print(f"   ✅ Recálculo concluído")
        print(f"   • Custo atualizado: R$ {produto_atualizado['custo_centavos']/100:.2f}")
        print(f"   • Peso atualizado: {produto_atualizado['peso_und']} kg")
    except Exception as e:
        print(f"   ❌ Erro no recálculo: {e}")
    
    print(f"\n4. Verificação final:")
    
    # Verificar componentes salvos
    componentes_db = ProdutoComponente.objects.filter(produto_principal=produto_id)
    print(f"   • Componentes no banco: {componentes_db.count()}")
    
    custo_total_componentes = 0
    tem_mao_obra = False
    
    for comp in componentes_db:
        if comp.observacao:
            try:
                obs = json.loads(comp.observacao)
                custo_comp = obs.get('custo_total', 0)
                custo_total_componentes += custo_comp
                print(f"     - {obs.get('nome_componente', comp.produto_componente.descricao)}: R$ {custo_comp/100:.2f}")
                
                if 'mão de obra' in obs.get('nome_componente', '').lower():
                    tem_mao_obra = True
                    
            except:
                custo_total_componentes += comp.produto_componente.custo_centavos * comp.quantidade
                print(f"     - {comp.produto_componente.descricao}: R$ {(comp.produto_componente.custo_centavos * comp.quantidade)/100:.2f}")
    
    print(f"\n✅ RESULTADO:")
    print(f"   • Produto criado: {nome_grade}")
    print(f"   • Componentes salvos: {componentes_salvos}/{len(componentes)}")
    print(f"   • Custo total dos componentes: R$ {custo_total_componentes/100:.2f}")
    print(f"   • Mão de obra incluída: {'✅ SIM' if tem_mao_obra else '❌ NÃO'}")
    
    # Verificar se o produto final tem o custo correto
    produto_final = MP_Produtos.objects.get(id=produto_id)
    print(f"   • Custo final do produto: R$ {produto_final.custo_centavos/100:.2f}")
    
    if abs(produto_final.custo_centavos - custo_total_componentes) <= 10:  # Tolerância de 10 centavos
        print(f"   ✅ Custo do produto confere com soma dos componentes!")
    else:
        diferenca = abs(produto_final.custo_centavos - custo_total_componentes)
        print(f"   ⚠️  Diferença de {diferenca} centavos entre produto e componentes")

if __name__ == '__main__':
    test_grade_creation_api()
