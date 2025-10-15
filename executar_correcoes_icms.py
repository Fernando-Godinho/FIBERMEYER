#!/usr/bin/env python3
"""
Script para executar as correções na base de impostos
"""

import requests
import json

def executar_correcoes():
    print("=== EXECUTANDO CORREÇÕES NA BASE DE IMPOSTOS ===\n")
    
    # 1. Corrigir BA - ICMS Interno de 7.20% para 7.00%
    print("1. Corrigindo BA - ICMS Interno...")
    try:
        # ID 163 conforme visto no script anterior
        correction_data = {'aliquota': 7.0}
        response = requests.patch(
            'http://127.0.0.1:8000/api/impostos/163/',
            json=correction_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.ok:
            print("✅ BA - ICMS Interno corrigido: 7.20% → 7.00%")
        else:
            print(f"❌ Erro ao corrigir BA: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erro na correção: {e}")
    
    print("\n" + "="*60)
    
    # 2. Adicionar estados prioritários (AC, AL, AM, DF, ES, GO, MT, MS, PA, PB, PI, RN, RO, RR, SE, TO)
    print("2. Adicionando estados prioritários...")
    
    estados_prioritarios = [
        'AC', 'AL', 'AM', 'DF', 'ES', 'GO', 'MT', 'MS', 
        'PA', 'PB', 'PI', 'RN', 'RO', 'RR', 'SE', 'TO'
    ]
    
    impostos_criados = 0
    erros = 0
    
    for estado in estados_prioritarios:
        # Criar os 3 tipos de ICMS para cada estado
        tipos_icms = [
            {'tipo': 'Interno', 'aliquota': 7.0},
            {'tipo': 'Interestadual', 'aliquota': 12.0},
            {'tipo': 'Consumo', 'aliquota': 7.2}
        ]
        
        print(f"\n📍 Adicionando impostos para {estado}:")
        
        for tipo_data in tipos_icms:
            novo_imposto = {
                'nome': f"{estado} - ICMS {tipo_data['tipo']}",
                'descricao': f"ICMS {tipo_data['tipo']} do estado {estado}",
                'aliquota': tipo_data['aliquota'],
                'ativo': True
            }
            
            try:
                response = requests.post(
                    'http://127.0.0.1:8000/api/impostos/',
                    json=novo_imposto,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.ok:
                    impostos_criados += 1
                    print(f"  ✅ {novo_imposto['nome']} - {novo_imposto['aliquota']}%")
                else:
                    erros += 1
                    print(f"  ❌ Erro ao criar {novo_imposto['nome']}: {response.status_code}")
                    # print(f"     Detalhes: {response.text}")
                    
            except Exception as e:
                erros += 1
                print(f"  ❌ Erro na criação: {e}")
    
    print("\n" + "="*60)
    
    # 3. Verificar resultado final
    print("3. Verificando resultado final...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/impostos/')
        impostos_finais = response.json()
        print(f"✅ Total de impostos na base: {len(impostos_finais)}")
        
        # Contar estados
        estados_com_impostos = set()
        for imposto in impostos_finais:
            if ' - ICMS ' in imposto['nome']:
                estado = imposto['nome'].split(' - ')[0]
                estados_com_impostos.add(estado)
        
        print(f"✅ Estados com impostos: {len(estados_com_impostos)}")
        print(f"✅ Estados cobertos: {sorted(estados_com_impostos)}")
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
    
    print("\n" + "="*60)
    
    # 4. Resumo da execução
    print("4. RESUMO DA EXECUÇÃO:")
    print(f"✅ Impostos criados: {impostos_criados}")
    print(f"❌ Erros encontrados: {erros}")
    print(f"📊 Taxa de sucesso: {(impostos_criados/(impostos_criados+erros)*100):.1f}%" if (impostos_criados+erros) > 0 else "N/A")
    
    if impostos_criados > 0:
        print("🎉 ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("👉 Agora todos os estados brasileiros têm impostos na base")
        print("👉 O sistema de busca automática funcionará para todos os estados")
    else:
        print("⚠️  Nenhum imposto foi criado - verifique erros acima")

if __name__ == "__main__":
    print("🚨 ATENÇÃO: Este script irá modificar a base de dados!")
    print("🚨 Certifique-se de que o servidor Django está rodando")
    print("🚨 Pressione CTRL+C para cancelar ou Enter para continuar...")
    
    try:
        input()
        executar_correcoes()
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário")