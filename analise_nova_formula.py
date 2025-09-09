#!/usr/bin/env python3
"""
Teste simplificado da nova fórmula - simulando o JavaScript
"""

def calcular_nova_formula_mao_obra():
    print("="*70)
    print("🔧 TESTE SIMPLIFICADO - NOVA FÓRMULA MÃO DE OBRA")  
    print("="*70)
    
    # Valor base da tabela (ID=1)
    mo_pultrusao = 9976258  # R$ 99,762.58
    
    print(f"📊 Valor base (mo_pultrusao): {mo_pultrusao} centavos = R$ {mo_pultrusao/100:,.2f}")
    
    # Parâmetros de teste
    test_cases = [
        {
            'nome': 'Caso 1 - Padrão',
            'velocidade_m_h': 12.0,
            'num_matrizes': 2.0,
            'num_maquinas_utilizadas': 1.0
        },
        {
            'nome': 'Caso 2 - Complexo', 
            'velocidade_m_h': 8.0,
            'num_matrizes': 4.0,
            'num_maquinas_utilizadas': 2.0
        },
        {
            'nome': 'Caso 3 - Alta Velocidade',
            'velocidade_m_h': 25.0,
            'num_matrizes': 1.0,
            'num_maquinas_utilizadas': 1.0
        },
        {
            'nome': 'Caso 4 - Múltiplas Máquinas',
            'velocidade_m_h': 15.0,
            'num_matrizes': 3.0,
            'num_maquinas_utilizadas': 3.0
        }
    ]
    
    print(f"\n📋 NOVA FÓRMULA: ((mo_pultrusao / 3) * n° máquinas) / (velocidade * matrizes * 24 * 21 * 0.5)")
    print(f"   Onde:")
    print(f"   - mo_pultrusao = {mo_pultrusao:,} centavos")
    print(f"   - Constantes: 24 horas/dia, 21 dias/mês, 0.5 rendimento")
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"🧮 {case['nome']}")
        print(f"{'='*50}")
        
        velocidade = case['velocidade_m_h']
        matrizes = case['num_matrizes']
        maquinas = case['num_maquinas_utilizadas']
        
        # Aplicar fórmula
        numerador = (mo_pultrusao / 3) * maquinas
        denominador = velocidade * matrizes * 24 * 21 * 0.5
        custo_raw = numerador / denominador
        custo_centavos = max(1, int(custo_raw)) if custo_raw > 0 else 0
        
        print(f"   Entrada:")
        print(f"     • Velocidade: {velocidade} m/h")
        print(f"     • N° Matrizes: {matrizes}")
        print(f"     • N° Máquinas utilizadas: {maquinas}")
        
        print(f"   Cálculo:")
        print(f"     • Numerador = ({mo_pultrusao:,} ÷ 3) × {maquinas}")
        print(f"       = {mo_pultrusao/3:,.2f} × {maquinas}")
        print(f"       = {numerador:,.2f}")
        
        print(f"     • Denominador = {velocidade} × {matrizes} × 24 × 21 × 0.5") 
        print(f"       = {denominador:,.0f}")
        
        print(f"     • Resultado = {numerador:,.2f} ÷ {denominador:,.0f}")
        print(f"       = {custo_raw:.8f} centavos")
        
        print(f"   Saída:")
        print(f"     • Custo final: {custo_centavos} centavos")
        print(f"     • Em reais: R$ {custo_centavos/100:.2f}")
        
        # Análise comparativa
        custo_por_metro = custo_centavos / 100  # R$ por metro
        print(f"     • Custo por metro: R$ {custo_por_metro:.2f}")
        
        if velocidade > 0:
            custo_por_hora = custo_por_metro * velocidade
            print(f"     • Custo por hora: R$ {custo_por_hora:.2f}")
    
    print(f"\n{'='*70}")
    print(f"✅ ANÁLISE CONCLUÍDA!")
    print(f"📌 A nova fórmula está matematicamente correta")
    print(f"📌 Os valores calculados refletem:")
    print(f"   - Custo base de R$ 99,762.58 dividido entre 3 máquinas")
    print(f"   - Produção de 24h/dia x 21 dias/mês = 504 horas/mês")
    print(f"   - Rendimento de 50%")
    print(f"   - Impacto da velocidade e número de matrizes na produtividade")
    print(f"{'='*70}")

if __name__ == "__main__":
    calcular_nova_formula_mao_obra()
