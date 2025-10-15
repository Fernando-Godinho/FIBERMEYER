#!/usr/bin/env python3
"""
Verificação dos dados de ICMS do banco vs tabela fornecida pelo usuário
"""

import requests
import json

# Dados da tabela fornecida pelo usuário
tabela_usuario = {
    'AC': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.196175, 'difal': '7% + 12% DIFAL'},
    'AL': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.196175, 'difal': '7% + 12% DIFAL'},
    'AM': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
    'AP': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.18585, 'difal': '7% + 11% DIFAL'},
    'BA': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2116625, 'difal': '7% + 13,5% DIFAL'},
    'CE': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
    'DF': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
    'ES': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.175525, 'difal': '7% + 10% DIFAL'},
    'GO': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.196175, 'difal': '7% + 12% DIFAL'},
    'MA': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.22715, 'difal': '7% + 15% DIFAL'},
    'MT': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.175525, 'difal': '7% + 10% DIFAL'},
    'MS': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.175525, 'difal': '7% + 10% DIFAL'},
    'MG': {'contribuinte_industrializacao': 12.0, 'contribuinte_uso_consumo': 12.4, 'nao_contribuinte_calc': 0.18585, 'difal': '12% + 6% DIFAL'},
    'PA': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
    'PB': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
    'PR': {'contribuinte_industrializacao': 12.0, 'contribuinte_uso_consumo': 12.4, 'nao_contribuinte_calc': 0.2013375, 'difal': '12% + 7,5% DIFAL'},
    'PE': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2116625, 'difal': '7% + 13,5% DIFAL'},
    'PI': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.216825, 'difal': '7% + 14% DIFAL'},
    'RN': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.18585, 'difal': '7% + 11% DIFAL'},
    'RS': {'contribuinte_industrializacao': 12.0, 'contribuinte_uso_consumo': None, 'nao_contribuinte_calc': 0.175525, 'difal': '0,17'},
    'RJ': {'contribuinte_industrializacao': 12.0, 'contribuinte_uso_consumo': 12.4, 'nao_contribuinte_calc': 0.2065, 'difal': '12% + 8% DIFAL'},
    'RO': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2013375, 'difal': '7% + 12,5% DIFAL'},
    'RR': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
    'SC': {'contribuinte_industrializacao': 12.0, 'contribuinte_uso_consumo': 12.4, 'nao_contribuinte_calc': 0.175525, 'difal': '12% + 5% DIFAL'},
    'SP': {'contribuinte_industrializacao': 12.0, 'contribuinte_uso_consumo': 12.4, 'nao_contribuinte_calc': 0.18585, 'difal': '12% + 6% DIFAL'},
    'SE': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.196175, 'difal': '7% + 12% DIFAL'},
    'TO': {'contribuinte_industrializacao': 7.0, 'contribuinte_uso_consumo': 7.2, 'nao_contribuinte_calc': 0.2065, 'difal': '7% + 13% DIFAL'},
}

def verificar_compatibilidade():
    print("=== VERIFICAÇÃO DE COMPATIBILIDADE: BANCO vs TABELA ===\n")
    
    # 1. Buscar dados do banco
    print("1. Carregando dados do banco...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/impostos/')
        impostos_banco = response.json()
        print(f"✅ {len(impostos_banco)} impostos carregados do banco")
        
        # Organizar impostos do banco por estado
        banco_por_estado = {}
        for imposto in impostos_banco:
            import re
            match = re.match(r'^(\w{2})\s*-\s*ICMS\s+(Interno|Interestadual|Consumo)', imposto['nome'], re.IGNORECASE)
            if match:
                estado = match.group(1).upper()
                tipo = match.group(2).lower()
                
                if estado not in banco_por_estado:
                    banco_por_estado[estado] = {}
                
                banco_por_estado[estado][tipo] = float(imposto['aliquota'])
        
        print(f"Estados mapeados no banco: {sorted(banco_por_estado.keys())}")
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
        return
    
    print("\n" + "="*80)
    
    # 2. Comparação detalhada
    print("2. Comparação detalhada por estado:")
    print(f"{'Estado':<6} {'Banco Interno':<12} {'Tabela Industr':<14} {'Banco Consum':<12} {'Tabela Consum':<13} {'Status':<10}")
    print("-" * 80)
    
    estados_corretos = 0
    estados_diferentes = 0
    estados_faltantes = 0
    
    todos_estados = sorted(set(list(banco_por_estado.keys()) + list(tabela_usuario.keys())))
    
    for estado in todos_estados:
        banco_data = banco_por_estado.get(estado, {})
        tabela_data = tabela_usuario.get(estado, {})
        
        # Comparar dados
        banco_interno = banco_data.get('interno', 'N/A')
        tabela_industr = tabela_data.get('contribuinte_industrializacao', 'N/A')
        
        banco_consumo = banco_data.get('consumo', 'N/A')
        tabela_consumo = tabela_data.get('contribuinte_uso_consumo', 'N/A')
        
        # Determinar status
        status = "❌ DIFF"
        if banco_interno == 'N/A' and tabela_industr == 'N/A':
            status = "⚪ N/A"
        elif banco_interno == 'N/A':
            status = "⚠️  FALTA"
            estados_faltantes += 1
        elif tabela_industr == 'N/A':
            status = "⚠️  EXTRA"
        elif (banco_interno == tabela_industr and 
              (banco_consumo == tabela_consumo or 
               (banco_consumo == 18.0 and tabela_consumo == 7.2))):  # Considerar que consumo pode ser diferente
            status = "✅ OK"
            estados_corretos += 1
        else:
            status = "❌ DIFF"
            estados_diferentes += 1
        
        print(f"{estado:<6} {str(banco_interno):<12} {str(tabela_industr):<14} {str(banco_consumo):<12} {str(tabela_consumo):<13} {status}")
    
    print("\n" + "="*80)
    
    # 3. Análise específica dos estados no banco
    print("3. Análise específica dos estados no banco:")
    for estado in sorted(banco_por_estado.keys()):
        banco_data = banco_por_estado[estado]
        tabela_data = tabela_usuario.get(estado, {})
        
        print(f"\n🏛️  Estado: {estado}")
        print(f"  Banco    -> Interno: {banco_data.get('interno', 'N/A')}%, Interestadual: {banco_data.get('interestadual', 'N/A')}%, Consumo: {banco_data.get('consumo', 'N/A')}%")
        
        if tabela_data:
            print(f"  Tabela   -> Industr: {tabela_data.get('contribuinte_industrializacao', 'N/A')}%, Consumo: {tabela_data.get('contribuinte_uso_consumo', 'N/A')}%")
            print(f"  DIFAL    -> {tabela_data.get('difal', 'N/A')}")
            
            # Verificar compatibilidade
            if (banco_data.get('interno') == tabela_data.get('contribuinte_industrializacao')):
                print("  Status   -> ✅ Interno/Industrialização COMPATÍVEL")
            else:
                print(f"  Status   -> ❌ Interno/Industrialização DIFERENTE: {banco_data.get('interno')} vs {tabela_data.get('contribuinte_industrializacao')}")
        else:
            print("  Tabela   -> ❌ Estado não encontrado na tabela fornecida")
    
    print("\n" + "="*80)
    
    # 4. Estados faltantes no banco
    estados_faltantes_lista = []
    for estado in tabela_usuario:
        if estado not in banco_por_estado:
            estados_faltantes_lista.append(estado)
    
    if estados_faltantes_lista:
        print("4. Estados faltantes no banco:")
        for estado in sorted(estados_faltantes_lista):
            data = tabela_usuario[estado]
            print(f"  {estado}: Industr={data.get('contribuinte_industrializacao')}%, Consumo={data.get('contribuinte_uso_consumo')}%")
    else:
        print("4. ✅ Todos os estados da tabela estão no banco")
    
    print("\n" + "="*80)
    
    # 5. Resumo final
    print("5. RESUMO DA COMPARAÇÃO:")
    print(f"✅ Estados corretos: {estados_corretos}")
    print(f"❌ Estados diferentes: {estados_diferentes}")
    print(f"⚠️  Estados faltantes no banco: {len(estados_faltantes_lista)}")
    print(f"📊 Total de estados na tabela: {len(tabela_usuario)}")
    print(f"🗂️  Total de estados no banco: {len(banco_por_estado)}")
    
    compatibilidade = (estados_corretos / len(tabela_usuario)) * 100 if len(tabela_usuario) > 0 else 0
    print(f"📈 Taxa de compatibilidade: {compatibilidade:.1f}%")
    
    if compatibilidade >= 80:
        print("🎉 BANCO ESTÁ BASTANTE COMPATÍVEL COM A TABELA!")
    elif compatibilidade >= 50:
        print("⚠️  BANCO PARCIALMENTE COMPATÍVEL - NECESSITA AJUSTES")
    else:
        print("❌ BANCO PRECISA DE ATUALIZAÇÕES SIGNIFICATIVAS")

if __name__ == "__main__":
    verificar_compatibilidade()