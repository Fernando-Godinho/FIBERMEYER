#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MaoObra

print("=== TESTANDO CÁLCULO DE MÃO DE OBRA (CORRIGIDO) ===")

# Parâmetros de teste (valores similares aos do console)
velocidade_m_h = 24.0
num_matrizes = 2.0  
num_maquinas_utilizadas = 1.0

# Constantes do sistema
qtd_maquinas_total = 3
horas_dia = 24
dias_mes = 21
rendimento = 0.5

print(f"Parâmetros:")
print(f"  Velocidade: {velocidade_m_h} m/h")
print(f"  Número de matrizes: {num_matrizes}")
print(f"  Máquinas utilizadas: {num_maquinas_utilizadas}")

# Buscar custo da Pultrusão
pultrusao = MaoObra.objects.filter(nome='Pultrusão').first()
custo_pultrusao = pultrusao.valor_centavos if pultrusao else 5000

print(f"  Custo Pultrusão: {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")

# Aplicar fórmula
if velocidade_m_h > 0 and num_matrizes > 0:
    numerador = (custo_pultrusao / qtd_maquinas_total) * num_maquinas_utilizadas
    denominador = velocidade_m_h * num_matrizes * horas_dia * dias_mes * rendimento
    custo_mao_obra = numerador / denominador
    
    # Garantir que o custo seja pelo menos 1 centavo se > 0 (nova lógica)
    custo_mao_obra_centavos = max(1, int(custo_mao_obra)) if custo_mao_obra > 0 else 0
    
    print(f"\nCálculo:")
    print(f"  Numerador = {numerador}")
    print(f"  Denominador = {denominador}")
    print(f"  Custo mão de obra (raw) = {custo_mao_obra}")
    print(f"  Custo mão de obra (centavos ajustado) = {custo_mao_obra_centavos}")
    print(f"  Custo mão de obra (R$) = R$ {custo_mao_obra_centavos/100:.2f}")
    
    # Criar componente
    componente = {
        'nome': 'Mão de Obra - Pultrusão',
        'produto': f'Pultrusão ({num_maquinas_utilizadas} máq, {velocidade_m_h} m/h, {num_matrizes} matrizes)',
        'quantidade': 1.0,
        'custo_unitario': custo_mao_obra_centavos,
        'custo_total': custo_mao_obra_centavos
    }
    
    print(f"\nComponente gerado:")
    print(f"  Nome: {componente['nome']}")
    print(f"  Produto: {componente['produto']}")
    print(f"  Custo unitário: {componente['custo_unitario']} centavos")
    print(f"  Custo total: {componente['custo_total']} centavos")

# Testar com diferentes velocidades para ver impacto
print(f"\n=== TESTES COM DIFERENTES VELOCIDADES ===")
for vel in [5, 10, 15, 20, 30]:
    numerador = (custo_pultrusao / qtd_maquinas_total) * num_maquinas_utilizadas
    denominador = vel * num_matrizes * horas_dia * dias_mes * rendimento
    custo = numerador / denominador
    custo_centavos = max(1, int(custo)) if custo > 0 else 0
    print(f"  Vel {vel} m/h: {custo:.6f} → {custo_centavos} centavos = R$ {custo_centavos/100:.2f}")
