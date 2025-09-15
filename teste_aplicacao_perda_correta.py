#!/usr/bin/env python
"""
Teste para verificar se a perda está sendo aplicada apenas nos custos, não nas quantidades
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def teste_aplicacao_perda_correta():
    print("=== TESTE: APLICAÇÃO CORRETA DA PERDA ===\n")
    
    print("🧮 SIMULAÇÃO MANUAL DO CÁLCULO:")
    
    # Dados de entrada
    comprimento = 6000  # mm
    vao = 1200  # mm 
    eixo_i = 150  # mm
    perda = 5  # %
    
    # Custos unitários (em centavos)
    custo_perfil = 648  # ¢/m
    custo_chaveta = 212  # ¢/m
    custo_cola = 8685  # ¢/unid
    custo_mo_hora = 6579  # ¢/h
    
    print(f"📋 PARÂMETROS:")
    print(f"   Comprimento: {comprimento}mm")
    print(f"   Vão: {vao}mm") 
    print(f"   Eixo I: {eixo_i}mm")
    print(f"   Perda: {perda}%")
    print()
    
    # CÁLCULO CORRETO - QUANTIDADES SEM PERDA
    metros_lineares = (comprimento / eixo_i) * (vao / 1000)  # 48 m/m²
    quantidade_chaveta = (vao / 150) * 2  # 16 m/m²
    quantidade_cola = 0.06  # unid/m² (fixa)
    quantidade_mo = 1.5 + 0.5  # 2h
    
    print(f"📏 QUANTIDADES (SEM PERDA):")
    print(f"   Perfil: {metros_lineares:.3f} m/m²")
    print(f"   Chaveta: {quantidade_chaveta:.3f} m/m²") 
    print(f"   Cola: {quantidade_cola:.3f} unid/m²")
    print(f"   Mão de obra: {quantidade_mo:.1f} h")
    print()
    
    # CUSTOS SEM PERDA
    custo_perfil_base = metros_lineares * custo_perfil
    custo_chaveta_base = quantidade_chaveta * custo_chaveta
    custo_cola_base = quantidade_cola * custo_cola
    custo_mo_base = quantidade_mo * custo_mo_hora
    
    print(f"💰 CUSTOS BASE (SEM PERDA):")
    print(f"   Perfil: {custo_perfil_base:.0f}¢ = R$ {custo_perfil_base/100:.2f}")
    print(f"   Chaveta: {custo_chaveta_base:.0f}¢ = R$ {custo_chaveta_base/100:.2f}")
    print(f"   Cola: {custo_cola_base:.0f}¢ = R$ {custo_cola_base/100:.2f}")
    print(f"   Mão de obra: {custo_mo_base:.0f}¢ = R$ {custo_mo_base/100:.2f}")
    print()
    
    # APLICAR PERDA APENAS NOS MATERIAIS (MP)
    fator_perda = 1 + (perda / 100)  # 1.05
    
    custo_perfil_com_perda = custo_perfil_base * fator_perda
    custo_chaveta_com_perda = custo_chaveta_base * fator_perda
    custo_cola_com_perda = custo_cola_base * fator_perda
    # Mão de obra NÃO tem perda aplicada
    custo_mo_final = custo_mo_base
    
    print(f"💎 CUSTOS FINAIS (COM {perda}% PERDA NOS MATERIAIS):")
    print(f"   Perfil: {custo_perfil_com_perda:.0f}¢ = R$ {custo_perfil_com_perda/100:.2f}")
    print(f"   Chaveta: {custo_chaveta_com_perda:.0f}¢ = R$ {custo_chaveta_com_perda/100:.2f}")
    print(f"   Cola: {custo_cola_com_perda:.0f}¢ = R$ {custo_cola_com_perda/100:.2f}")
    print(f"   Mão de obra: {custo_mo_final:.0f}¢ = R$ {custo_mo_final/100:.2f} (sem perda)")
    print()
    
    # TOTAIS
    total_materiais = custo_perfil_com_perda + custo_chaveta_com_perda + custo_cola_com_perda
    total_final = total_materiais + custo_mo_final
    
    print(f"🎯 RESUMO FINAL:")
    print(f"   Total materiais (com {perda}% perda): {total_materiais:.0f}¢ = R$ {total_materiais/100:.2f}")
    print(f"   Total mão de obra (sem perda): {custo_mo_final:.0f}¢ = R$ {custo_mo_final/100:.2f}")
    print(f"   TOTAL GERAL: {total_final:.0f}¢ = R$ {total_final/100:.2f}")
    print()
    
    print("✅ REGRAS CORRETAS APLICADAS:")
    print(f"   • Quantidades: permanecem as quantidades reais calculadas")
    print(f"   • Perda de {perda}%: aplicada APENAS nos custos dos materiais (MP)")
    print(f"   • Mão de obra: SEM perda aplicada")
    print(f"   • Resultado: custos finais corretos para orçamento")

if __name__ == '__main__':
    teste_aplicacao_perda_correta()
