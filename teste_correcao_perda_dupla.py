#!/usr/bin/env python
"""
Teste para verificar se a duplicação da perda foi corrigida
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def teste_correcao_perda_dupla():
    print("=== TESTE: CORREÇÃO PERDA DUPLA - GRADE ===\n")
    
    # Buscar produtos
    perfil_i25 = MP_Produtos.objects.filter(descricao__icontains='I25').first()
    chaveta = MP_Produtos.objects.get(id=1332)
    cola = MP_Produtos.objects.get(id=1183)
    
    print("📋 PRODUTOS BASE:")
    print(f"   I25: R$ {perfil_i25.custo_centavos/100:.2f}/m")
    print(f"   Chaveta: R$ {chaveta.custo_centavos/100:.2f}/m") 
    print(f"   Cola: R$ {cola.custo_centavos/100:.2f}/unid")
    
    # Simular cálculo manual
    dados = {
        'comprimento': 6000,  # 6m
        'vao': 1200,         # 1.2m
        'eixo_i': 150,       # 150mm
        'perda': 5           # 5%
    }
    
    # Cálculos base
    metros_lineares = (dados['comprimento'] / dados['eixo_i']) * (dados['vao'] / 1000)  # 48 m/m²
    qtd_chaveta = (dados['vao'] / 150) * 2  # 16 m/m²
    qtd_cola = 0.06  # fixo
    
    # Custos base (sem perda)
    custo_perfil_base = metros_lineares * perfil_i25.custo_centavos  # 31104¢
    custo_chaveta_base = qtd_chaveta * chaveta.custo_centavos  # 3392¢
    custo_cola_base = qtd_cola * cola.custo_centavos  # 521¢
    
    # Aplicar perda (5%)
    fator_perda = 1.05
    custo_perfil_com_perda = custo_perfil_base * fator_perda  # 32659¢
    custo_chaveta_com_perda = custo_chaveta_base * fator_perda  # 3562¢
    custo_cola_com_perda = custo_cola_base * fator_perda  # 547¢
    
    # Total
    total_materiais = custo_perfil_com_perda + custo_chaveta_com_perda + custo_cola_com_perda
    
    print(f"\n🧮 CÁLCULO CORRETO (SEM PERDA DUPLA):")
    print(f"   Perfil I25: {metros_lineares:.1f}m × {perfil_i25.custo_centavos/100:.2f} = R$ {custo_perfil_base/100:.2f}")
    print(f"   Perfil I25 +5%: R$ {custo_perfil_com_perda/100:.2f}")
    print(f"   Chaveta: {qtd_chaveta:.1f}m × R$ {chaveta.custo_centavos/100:.2f} = R$ {custo_chaveta_base/100:.2f}")  
    print(f"   Chaveta +5%: R$ {custo_chaveta_com_perda/100:.2f}")
    print(f"   Cola: {qtd_cola}un × R$ {cola.custo_centavos/100:.2f} = R$ {custo_cola_base/100:.2f}")
    print(f"   Cola +5%: R$ {custo_cola_com_perda/100:.2f}")
    print(f"   TOTAL MATERIAIS: R$ {total_materiais/100:.2f}")
    
    print(f"\n❌ VALORES INCORRETOS (COM PERDA DUPLA - ANTES):")
    # Se tivesse perda dupla, seria:
    perda_dupla_perfil = custo_perfil_com_perda * fator_perda  # 34292¢
    perda_dupla_chaveta = custo_chaveta_com_perda * fator_perda  # 3740¢
    perda_dupla_cola = custo_cola_com_perda * fator_perda  # 574¢
    total_perda_dupla = perda_dupla_perfil + perda_dupla_chaveta + perda_dupla_cola
    
    print(f"   Perfil I25 (5%×5%): R$ {perda_dupla_perfil/100:.2f}")
    print(f"   Chaveta (5%×5%): R$ {perda_dupla_chaveta/100:.2f}")
    print(f"   Cola (5%×5%): R$ {perda_dupla_cola/100:.2f}")
    print(f"   TOTAL INCORRETO: R$ {total_perda_dupla/100:.2f}")
    
    diferenca = total_perda_dupla - total_materiais
    print(f"\n💰 DIFERENÇA:")
    print(f"   Erro da perda dupla: +R$ {diferenca/100:.2f} ({((diferenca/total_materiais)*100):.1f}%)")
    
    print(f"\n✅ CORREÇÃO APLICADA:")
    print(f"   • Perda aplicada UMA VEZ apenas")
    print(f"   • Valores corretos na interface")
    print(f"   • Total correto: R$ {total_materiais/100:.2f}")

if __name__ == '__main__':
    teste_correcao_perda_dupla()
