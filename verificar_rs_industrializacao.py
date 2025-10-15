#!/usr/bin/env python3
"""
Verificar percentual para RS - Industrialização - Contribuinte
"""

import requests

def verificar_rs_industrializacao():
    print("=== VERIFICAÇÃO: RS - INDUSTRIALIZAÇÃO - CONTRIBUINTE ===\n")
    
    # 1. Verificar na base de dados atual
    print("1. Consultando base de dados atual...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/impostos/')
        impostos = response.json()
        
        # Buscar impostos do RS
        impostos_rs = [i for i in impostos if i['nome'].startswith('RS - ICMS')]
        
        print("Impostos do RS na base:")
        for imposto in impostos_rs:
            print(f"  {imposto['nome']}: {imposto['aliquota']}%")
            
    except Exception as e:
        print(f"❌ Erro ao acessar base: {e}")
        return
    
    print("\n" + "="*60)
    
    # 2. Consultar tabela fornecida pelo usuário
    print("2. Consultando tabela de referência...")
    
    # Da tabela fornecida:
    # RS	12,0%		0,175525	0,17
    # CONTRIBUINTE INDUSTRIALIZAÇÃO = 12,0% (% na NF)
    
    print("Tabela de referência para RS:")
    print("  CONTRIBUINTE - INDUSTRIALIZAÇÃO: 12,0% (% na NF)")
    print("  CONTRIBUINTE - USO/CONSUMO: (não especificado)")
    print("  NÃO CONTRIBUINTE - CÁLCULO: 0,175525")
    print("  NÃO CONTRIBUINTE - % na NF: 0,17")
    
    print("\n" + "="*60)
    
    # 3. Lógica do sistema atual
    print("3. Lógica do sistema implementado...")
    
    print("Para RS - Industrialização - Contribuinte:")
    print("  🔍 Cenário: Estado=RS, Venda=REVENDA, Cliente=CONTRIBUINTE")
    print("  📋 Lógica: Revenda + Contribuinte = ICMS Interno")
    print("  🎯 Imposto buscado: 'RS - ICMS Interno'")
    
    # Verificar se existe o imposto correto
    icms_interno_rs = next((i for i in impostos_rs if 'Interno' in i['nome']), None)
    
    if icms_interno_rs:
        print(f"  ✅ Encontrado: {icms_interno_rs['nome']} = {icms_interno_rs['aliquota']}%")
        
        # Verificar se está correto conforme a tabela
        if icms_interno_rs['aliquota'] == 12.0:
            print("  ✅ CORRETO! Bate com a tabela de referência (12,0%)")
        else:
            print(f"  ❌ INCORRETO! Deveria ser 12,0% mas está {icms_interno_rs['aliquota']}%")
    else:
        print("  ❌ NÃO ENCONTRADO! Imposto RS - ICMS Interno não existe na base")
    
    print("\n" + "="*60)
    
    # 4. Teste prático da lógica
    print("4. Simulação da lógica JavaScript...")
    
    # Simular a lógica do formulário
    uf = 'RS'
    venda_destinada = 'REVENDA'  # Industrialização = Revenda
    contribuinte = 'CONTRIBUINTE'
    
    print(f"Parâmetros: UF={uf}, Venda={venda_destinada}, Cliente={contribuinte}")
    
    # Lógica do JavaScript
    if venda_destinada == 'REVENDA' and contribuinte == 'CONTRIBUINTE':
        tipo_icms = 'interno'
        print(f"Resultado: Buscar '{uf} - ICMS {tipo_icms.title()}'")
        
        if icms_interno_rs:
            aliquota_final = icms_interno_rs['aliquota']
            print(f"Alíquota final: {aliquota_final}%")
        else:
            print("Alíquota final: 7.20% (padrão - imposto não encontrado)")
    
    print("\n" + "="*60)
    
    # 5. Resposta final
    print("5. RESPOSTA FINAL:")
    print("🎯 Para RS - INDUSTRIALIZAÇÃO - CONTRIBUINTE:")
    
    if icms_interno_rs and icms_interno_rs['aliquota'] == 12.0:
        print(f"✅ PERCENTUAL CORRETO: {icms_interno_rs['aliquota']}%")
        print("✅ Conforme tabela de referência")
        print("✅ Sistema funcionando corretamente")
    elif icms_interno_rs:
        print(f"⚠️  PERCENTUAL ATUAL: {icms_interno_rs['aliquota']}%")
        print("❌ DEVERIA SER: 12.0%")
        print("🔧 Necessita correção na base")
    else:
        print("❌ IMPOSTO NÃO ENCONTRADO")
        print("🔧 Necessita criar: RS - ICMS Interno = 12.0%")
    
    print("\n📝 MAPEAMENTO CONCEITUAL:")
    print("   INDUSTRIALIZAÇÃO (tabela) = REVENDA + CONTRIBUINTE (sistema)")
    print("   USO/CONSUMO (tabela) = CONSUMO_PROPRIO (sistema)")
    print("   NÃO CONTRIBUINTE (tabela) = REVENDA + NAO_CONTRIBUINTE (sistema)")

if __name__ == "__main__":
    verificar_rs_industrializacao()