#!/usr/bin/env python3
"""
Script para atualizar a base de impostos com os dados corretos da tabela
"""

import requests
import json

# Estados faltantes e suas alíquotas conforme a tabela
estados_para_adicionar = {
    'AC': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'AL': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2}, 
    'AM': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'AP': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'DF': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'ES': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'GO': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'MA': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'MS': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'MT': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'PA': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'PB': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'PI': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'RN': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'RO': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'RR': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'SE': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
    'TO': {'interno': 7.0, 'interestadual': 12.0, 'consumo': 7.2},
}

# Correções para estados existentes
correcoes = {
    'BA': {'interno': 7.0},  # Corrigir de 7.2 para 7.0
}

def atualizar_base_impostos():
    print("=== ATUALIZANDO BASE DE IMPOSTOS ===\n")
    
    # 1. Verificar impostos atuais
    print("1. Carregando impostos atuais...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/impostos/')
        impostos_atuais = response.json()
        print(f"✅ {len(impostos_atuais)} impostos carregados")
        
        # Mapear impostos existentes
        impostos_por_id = {imp['id']: imp for imp in impostos_atuais}
        impostos_por_nome = {imp['nome']: imp for imp in impostos_atuais}
        
    except Exception as e:
        print(f"❌ Erro ao carregar impostos: {e}")
        return
    
    print("\n" + "="*60)
    
    # 2. Aplicar correções aos impostos existentes
    print("2. Aplicando correções aos impostos existentes...")
    
    for estado, dados in correcoes.items():
        for tipo, aliquota in dados.items():
            nome_imposto = f"{estado} - ICMS {tipo.title()}"
            
            if nome_imposto in impostos_por_nome:
                imposto_id = impostos_por_nome[nome_imposto]['id']
                aliquota_atual = impostos_por_nome[nome_imposto]['aliquota']
                
                print(f"🔧 Corrigindo {nome_imposto}: {aliquota_atual}% → {aliquota}%")
                
                # Simular atualização (descomente para executar)
                # try:
                #     update_response = requests.patch(
                #         f'http://127.0.0.1:8000/api/impostos/{imposto_id}/',
                #         json={'aliquota': aliquota},
                #         headers={'Content-Type': 'application/json'}
                #     )
                #     if update_response.ok:
                #         print(f"  ✅ Atualizado com sucesso")
                #     else:
                #         print(f"  ❌ Erro na atualização: {update_response.status_code}")
                # except Exception as e:
                #     print(f"  ❌ Erro: {e}")
            else:
                print(f"⚠️  Imposto não encontrado: {nome_imposto}")
    
    print("\n" + "="*60)
    
    # 3. Adicionar novos estados
    print("3. Adicionando novos estados...")
    
    novos_impostos = []
    
    for estado, dados in estados_para_adicionar.items():
        for tipo, aliquota in dados.items():
            nome_imposto = f"{estado} - ICMS {tipo.title()}"
            
            if nome_imposto not in impostos_por_nome:
                novo_imposto = {
                    'nome': nome_imposto,
                    'descricao': f'ICMS {tipo.title()} do estado {estado}',
                    'aliquota': aliquota,
                    'ativo': True
                }
                novos_impostos.append(novo_imposto)
                print(f"➕ Novo imposto: {nome_imposto} - {aliquota}%")
            else:
                print(f"⚠️  Já existe: {nome_imposto}")
    
    print(f"\n📊 Total de novos impostos a criar: {len(novos_impostos)}")
    
    # Simular criação (descomente para executar)
    # for novo_imposto in novos_impostos:
    #     try:
    #         create_response = requests.post(
    #             'http://127.0.0.1:8000/api/impostos/',
    #             json=novo_imposto,
    #             headers={'Content-Type': 'application/json'}
    #         )
    #         if create_response.ok:
    #             print(f"  ✅ Criado: {novo_imposto['nome']}")
    #         else:
    #             print(f"  ❌ Erro ao criar {novo_imposto['nome']}: {create_response.status_code}")
    #     except Exception as e:
    #         print(f"  ❌ Erro: {e}")
    
    print("\n" + "="*60)
    
    # 4. Resumo das mudanças
    print("4. RESUMO DAS MUDANÇAS PROPOSTAS:")
    print(f"🔧 Correções: {len(correcoes)} estados")
    print(f"➕ Novos estados: {len(estados_para_adicionar)} estados")
    print(f"📝 Novos impostos: {len(novos_impostos)} registros")
    
    total_final = len(impostos_atuais) + len(novos_impostos)
    print(f"📊 Total final esperado: {total_final} impostos")
    
    print("\n🚨 ATENÇÃO: Este script está em modo SIMULAÇÃO")
    print("Para executar as mudanças, descomente as linhas de atualização/criação")
    
    # 5. Mostrar comandos para execução manual
    print("\n" + "="*60)
    print("5. COMANDOS PARA EXECUÇÃO MANUAL:")
    
    print("\n# Correções:")
    for estado, dados in correcoes.items():
        for tipo, aliquota in dados.items():
            nome_imposto = f"{estado} - ICMS {tipo.title()}"
            if nome_imposto in impostos_por_nome:
                imposto_id = impostos_por_nome[nome_imposto]['id']
                print(f'# Corrigir {nome_imposto}')
                print(f'curl -X PATCH "http://127.0.0.1:8000/api/impostos/{imposto_id}/" -H "Content-Type: application/json" -d \'{{"aliquota": {aliquota}}}\'')
    
    print("\n# Novos impostos:")
    for novo_imposto in novos_impostos[:5]:  # Mostrar apenas alguns exemplos
        print(f'# Criar {novo_imposto["nome"]}')
        print(f'curl -X POST "http://127.0.0.1:8000/api/impostos/" -H "Content-Type: application/json" -d \'{json.dumps(novo_imposto)}\'')
    
    if len(novos_impostos) > 5:
        print(f'# ... e mais {len(novos_impostos) - 5} impostos')

if __name__ == "__main__":
    atualizar_base_impostos()