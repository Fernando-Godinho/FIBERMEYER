#!/usr/bin/env python
"""
Teste com diferentes cenários de mão de obra para o template 'Novo Perfil'
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MaoObra, MP_Produtos

def calcular_custo_mo(velocidade_m_h, num_matrizes, num_maquinas_utilizadas, custo_pultrusao_centavos):
    """Calcula o custo de mão de obra usando a fórmula"""
    qtd_maquinas_total = 3
    horas_dia = 24
    dias_mes = 21
    rendimento = 0.5
    
    if velocidade_m_h > 0 and num_matrizes > 0:
        numerador = (custo_pultrusao_centavos / qtd_maquinas_total) * num_maquinas_utilizadas
        denominador = velocidade_m_h * num_matrizes * horas_dia * dias_mes * rendimento
        return numerador / denominador
    return 0

def test_cenarios_mao_obra():
    print("=== TESTE DE CENÁRIOS DE MÃO DE OBRA - TEMPLATE 'NOVO PERFIL' ===\n")
    
    # Buscar custo de pultrusão
    pultrusao = MaoObra.objects.filter(nome__icontains='pultrusão').first() or MaoObra.objects.filter(nome__icontains='pultrusao').first()
    custo_pultrusao = pultrusao.valor_centavos if pultrusao else 5000
    
    print(f"💰 Custo Pultrusão: R$ {custo_pultrusao/100:.2f}")
    print(f"🏭 Constantes: 3 máquinas totais, 24h/dia, 21 dias/mês, rendimento 0.5\n")
    
    # Cenários de teste
    cenarios = [
        {
            'nome': 'Produção Rápida - Alta Velocidade',
            'velocidade_m_h': 5.0,
            'num_matrizes': 4,
            'num_maquinas_utilizadas': 2,
            'descricao': 'Perfil complexo com múltiplas matrizes'
        },
        {
            'nome': 'Produção Média - Velocidade Normal', 
            'velocidade_m_h': 2.0,
            'num_matrizes': 2,
            'num_maquinas_utilizadas': 1,
            'descricao': 'Perfil padrão'
        },
        {
            'nome': 'Produção Lenta - Perfil Complexo',
            'velocidade_m_h': 0.5,
            'num_matrizes': 1,
            'num_maquinas_utilizadas': 1,
            'descricao': 'Perfil muito complexo, baixa velocidade'
        },
        {
            'nome': 'Máxima Capacidade - 3 Máquinas',
            'velocidade_m_h': 3.0,
            'num_matrizes': 2,
            'num_maquinas_utilizadas': 3,
            'descricao': 'Usando toda a capacidade disponível'
        },
        {
            'nome': 'Produção Mínima - 1 Máquina Lenta',
            'velocidade_m_h': 0.2,
            'num_matrizes': 1,
            'num_maquinas_utilizadas': 1,
            'descricao': 'Perfil super complexo ou protótipo'
        }
    ]
    
    print("| Cenário                        | Veloc. | Matr. | Máq. | Custo MO/m | Impacto    |")
    print("|--------------------------------|--------|-------|------|------------|------------|")
    
    for i, cenario in enumerate(cenarios, 1):
        custo_mo = calcular_custo_mo(
            cenario['velocidade_m_h'],
            cenario['num_matrizes'], 
            cenario['num_maquinas_utilizadas'],
            custo_pultrusao
        )
        
        # Calcular custo por metro (baseado em 8kg/m como exemplo)
        custo_mo_por_metro = custo_mo
        
        # Classificar impacto
        if custo_mo_por_metro < 50:  # < R$ 0.50
            impacto = "Baixo"
        elif custo_mo_por_metro < 200:  # < R$ 2.00
            impacto = "Médio"
        else:
            impacto = "Alto"
        
        print(f"| {cenario['nome']:<30} | {cenario['velocidade_m_h']:6.1f} | {cenario['num_matrizes']:5.0f} | {cenario['num_maquinas_utilizadas']:4.0f} | R$ {custo_mo_por_metro/100:7.2f} | {impacto:<10} |")
    
    print(f"\n📊 ANÁLISE DOS RESULTADOS:")
    print(f"• Velocidade baixa = maior custo de MO")
    print(f"• Mais matrizes = menor custo de MO por matriz")  
    print(f"• Mais máquinas = maior custo de MO (mais recursos)")
    print(f"• Fórmula permite balancear produtividade vs custo")
    
    print(f"\n💡 DICAS DE OTIMIZAÇÃO:")
    print(f"• Para reduzir custo MO: aumentar velocidade ou número de matrizes")
    print(f"• Para aumentar produção: usar mais máquinas (aumenta custo MO)")
    print(f"• Perfis simples = alta velocidade = baixo custo MO")
    print(f"• Perfis complexos = baixa velocidade = alto custo MO")
    
    # Exemplo com custo total
    print(f"\n🧮 EXEMPLO DE CUSTO TOTAL (8 kg/m):")
    cenario_exemplo = cenarios[1]  # Produção média
    custo_mo_exemplo = calcular_custo_mo(
        cenario_exemplo['velocidade_m_h'],
        cenario_exemplo['num_matrizes'],
        cenario_exemplo['num_maquinas_utilizadas'], 
        custo_pultrusao
    )
    
    custo_materiais_exemplo = 14500  # R$ 145.00 (do teste anterior)
    custo_total_exemplo = custo_materiais_exemplo + custo_mo_exemplo
    
    print(f"  Materiais: R$ {custo_materiais_exemplo/100:.2f}")
    print(f"  Mão de Obra: R$ {custo_mo_exemplo/100:.2f}")
    print(f"  TOTAL: R$ {custo_total_exemplo/100:.2f}")
    print(f"  Participação MO: {(custo_mo_exemplo/custo_total_exemplo)*100:.2f}%")

if __name__ == '__main__':
    test_cenarios_mao_obra()
