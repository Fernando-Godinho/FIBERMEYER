#!/usr/bin/env python
"""
Teste específico para verificar aplicação da perda na Tampa Montada
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def teste_perda_tampa_montada():
    print("=== TESTE APLICAÇÃO PERDA - TAMPA MONTADA ===\n")
    
    # Buscar produtos necessários
    perfil_i25 = MP_Produtos.objects.filter(descricao__icontains='I25').first()
    chaveta = MP_Produtos.objects.filter(id=1332).first()
    cola = MP_Produtos.objects.filter(id=1183).first()
    chapa_lisa = MP_Produtos.objects.filter(id=1381).first()
    perfil_u4 = MP_Produtos.objects.filter(id=1382).first()
    alca = MP_Produtos.objects.filter(id=1383).first()
    chapa_ev = MP_Produtos.objects.filter(id=1384).first()
    
    print("📋 PRODUTOS BASE:")
    produtos = [
        ("Perfil I25", perfil_i25),
        ("Chaveta", chaveta),
        ("Cola", cola),
        ("Chapa Lisa 2,5mm", chapa_lisa),
        ("Perfil U4\"", perfil_u4),
        ("Alça Metálica", alca),
        ("Chapa EV", chapa_ev)
    ]
    
    for nome, produto in produtos:
        if produto:
            print(f"   {nome}: R$ {produto.custo_centavos/100:.2f}")
        else:
            print(f"   {nome}: ❌ NÃO ENCONTRADO")
    
    if not all(p[1] for p in produtos):
        print("\n❌ Produtos faltando - não é possível fazer o teste")
        return
    
    print(f"\n🧮 SIMULAÇÃO TAMPA MONTADA (exemplo da imagem):")
    print(f"   Comprimento: 1000mm | Vão: 1000mm")
    print(f"   Opções: Quadro U4\" + Alça")
    print(f"   Perda: 5%")
    
    # Simular cálculos da Tampa Montada
    comprimento = 1000  # mm
    vao = 1000  # mm
    eixo_i = 150  # mm
    fator_perda = 1.05  # 5%
    
    # Cálculos base (sem perda)
    metros_lineares = (comprimento / eixo_i) * (vao / 1000)  # ~6.67 m/m²
    area_chapa = (vao / 1000) * (comprimento / 1000)  # 1 m²
    
    print(f"\n💰 CUSTOS SEM PERDA:")
    custo_perfil_base = metros_lineares * perfil_i25.custo_centavos
    custo_chaveta_base = ((vao / 150) * 2) * chaveta.custo_centavos
    custo_cola_base = 0.1 * cola.custo_centavos  # quantidade fixa
    custo_chapa_base = area_chapa * chapa_lisa.custo_centavos
    custo_u4_base = 2 * perfil_u4.custo_centavos  # 2 unidades
    custo_alca_base = 2 * alca.custo_centavos  # 2 unidades
    
    print(f"   Perfil I25: R$ {custo_perfil_base/100:.2f}")
    print(f"   Chaveta: R$ {custo_chaveta_base/100:.2f}")
    print(f"   Cola: R$ {custo_cola_base/100:.2f}")
    print(f"   Chapa Lisa: R$ {custo_chapa_base/100:.2f}")
    print(f"   Perfil U4\": R$ {custo_u4_base/100:.2f}")
    print(f"   Alça: R$ {custo_alca_base/100:.2f}")
    
    print(f"\n🎯 CUSTOS COM 5% PERDA (esperados):")
    print(f"   Perfil I25: R$ {custo_perfil_base * fator_perda/100:.2f}")
    print(f"   Chaveta: R$ {custo_chaveta_base * fator_perda/100:.2f}")
    print(f"   Cola: R$ {custo_cola_base * fator_perda/100:.2f}")
    print(f"   Chapa Lisa: R$ {custo_chapa_base * fator_perda/100:.2f}")
    print(f"   Perfil U4\": R$ {custo_u4_base * fator_perda/100:.2f}")
    print(f"   Alça: R$ {custo_alca_base * fator_perda/100:.2f}")
    
    # Mão de obra (sem perda)
    tempo_proc = 1.0
    tempo_mtg = 0.5
    valor_hora = 65.79
    multiplicador_mo = 2.0  # Quadro U4" + Alça
    custo_mo = (tempo_proc + tempo_mtg) * valor_hora * multiplicador_mo
    print(f"   Mão de Obra: R$ {custo_mo:.2f} (SEM perda)")
    
    total_materiais_com_perda = (custo_perfil_base + custo_chaveta_base + custo_cola_base + 
                                custo_chapa_base + custo_u4_base + custo_alca_base) * fator_perda
    total_geral = total_materiais_com_perda + (custo_mo * 100)
    
    print(f"\n📊 TOTAIS:")
    print(f"   Materiais (com 5% perda): R$ {total_materiais_com_perda/100:.2f}")
    print(f"   Mão de Obra (sem perda): R$ {custo_mo:.2f}")
    print(f"   TOTAL GERAL: R$ {total_geral/100:.2f}")
    
    print(f"\n✅ Agora teste na interface e compare os valores!")

if __name__ == '__main__':
    teste_perda_tampa_montada()
