#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MaoObra

print("=== TESTANDO CÁLCULO DE MÃO DE OBRA ===")

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
print(f"  Total de máquinas: {qtd_maquinas_total}")
print(f"  Horas/dia: {horas_dia}")
print(f"  Dias/mês: {dias_mes}")
print(f"  Rendimento: {rendimento}")

# Buscar custo da Pultrusão
try:
    pultrusao = MaoObra.objects.filter(nome='Pultrusão').first()
    if pultrusao:
        custo_pultrusao = pultrusao.valor_centavos
        print(f"  Custo Pultrusão: {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")
    else:
        custo_pultrusao = 5000
        print(f"  Custo Pultrusão (fallback): {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")
        
except Exception as e:
    custo_pultrusao = 5000
    print(f"  Custo Pultrusão (erro): {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")
    print(f"  Erro: {e}")

print(f"\nCálculo:")

# Aplicar fórmula
if velocidade_m_h > 0 and num_matrizes > 0:
    numerador = (custo_pultrusao / qtd_maquinas_total) * num_maquinas_utilizadas
    denominador = velocidade_m_h * num_matrizes * horas_dia * dias_mes * rendimento
    custo_mao_obra = numerador / denominador
    
    print(f"  Numerador = ({custo_pultrusao} / {qtd_maquinas_total}) * {num_maquinas_utilizadas} = {numerador}")
    print(f"  Denominador = {velocidade_m_h} * {num_matrizes} * {horas_dia} * {dias_mes} * {rendimento} = {denominador}")
    print(f"  Custo mão de obra = {numerador} / {denominador} = {custo_mao_obra}")
    print(f"  Custo mão de obra (centavos) = {int(custo_mao_obra)}")
    print(f"  Custo mão de obra (R$) = R$ {custo_mao_obra/100:.4f}")
    
    # Criar componente como no código original
    componente = {
        'nome': 'Mão de Obra - Pultrusão',
        'produto': f'Pultrusão ({num_maquinas_utilizadas} máq, {velocidade_m_h} m/h, {num_matrizes} matrizes)',
        'quantidade': 1.0,
        'custo_unitario': int(custo_mao_obra),
        'custo_total': int(custo_mao_obra)
    }
    
    print(f"\nComponente gerado:")
    print(f"  Nome: {componente['nome']}")
    print(f"  Produto: {componente['produto']}")
    print(f"  Quantidade: {componente['quantidade']}")
    print(f"  Custo unitário: {componente['custo_unitario']} centavos")
    print(f"  Custo total: {componente['custo_total']} centavos")
    
else:
    print("  Erro: Velocidade ou número de matrizes é zero")
