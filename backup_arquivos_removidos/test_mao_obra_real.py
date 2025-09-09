#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MaoObra

print("=== TESTANDO COM MÃO DE OBRA PULTRUSÃO REAL ===")

# Parâmetros de teste
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

# Buscar custo da Pultrusão com a nova lógica
try:
    pultrusao = MaoObra.objects.filter(
        nome='MÃO DE OBRA PULTRUSÃO'
    ).first() or MaoObra.objects.filter(
        nome__icontains='pultrusão'
    ).first() or MaoObra.objects.filter(
        nome__icontains='pultrusao'
    ).first()
    
    if pultrusao:
        custo_pultrusao = pultrusao.valor_centavos
        print(f"  ✅ Encontrado: {pultrusao.nome}")
        print(f"  Custo Pultrusão: {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")
    else:
        custo_pultrusao = 9976258  # R$ 99.762,58 como padrão (valor mensal)
        print(f"  ⚠️ Usando fallback: {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")
        
except Exception as e:
    custo_pultrusao = 9976258
    print(f"  ❌ Erro: {e}")
    print(f"  Usando fallback: {custo_pultrusao} centavos = R$ {custo_pultrusao/100:.2f}")

# Aplicar fórmula
if velocidade_m_h > 0 and num_matrizes > 0:
    numerador = (custo_pultrusao / qtd_maquinas_total) * num_maquinas_utilizadas
    denominador = velocidade_m_h * num_matrizes * horas_dia * dias_mes * rendimento
    custo_mao_obra = numerador / denominador
    
    # Garantir que o custo seja pelo menos 1 centavo se > 0
    custo_mao_obra_centavos = max(1, int(custo_mao_obra)) if custo_mao_obra > 0 else 0
    
    print(f"\nCálculo:")
    print(f"  Numerador = ({custo_pultrusao} / {qtd_maquinas_total}) * {num_maquinas_utilizadas} = {numerador:.2f}")
    print(f"  Denominador = {velocidade_m_h} * {num_matrizes} * {horas_dia} * {dias_mes} * {rendimento} = {denominador}")
    print(f"  Custo mão de obra (raw) = {numerador:.2f} / {denominador} = {custo_mao_obra:.2f}")
    print(f"  Custo mão de obra (centavos) = {custo_mao_obra_centavos}")
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
    print(f"  Custo unitário: {componente['custo_unitario']} centavos = R$ {componente['custo_unitario']/100:.2f}")
    print(f"  Custo total: {componente['custo_total']} centavos = R$ {componente['custo_total']/100:.2f}")

# Comparação com valores antigos
print(f"\n=== COMPARAÇÃO ===")
print(f"Valor antigo (R$ 50,00/H): R$ 0,01 por metro")
print(f"Valor novo (R$ {custo_pultrusao/100:.2f}/MÊS): R$ {custo_mao_obra_centavos/100:.2f} por metro")
print(f"Diferença: {custo_mao_obra_centavos/1:.0f}x maior custo de mão de obra")
