#!/usr/bin/env python
"""
Teste para validar correção da perda dupla na Tampa Montada
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from main.models import MP_Produtos

def validar_correcao_tampa_montada():
    print("=== VALIDAÇÃO: CORREÇÃO PERDA DUPLA - TAMPA MONTADA ===\n")
    
    try:
        # Buscar produtos (mesmos da imagem)
        perfil_i25 = MP_Produtos.objects.filter(descricao__icontains='I25').first()
        chaveta = MP_Produtos.objects.get(id=1332)
        cola = MP_Produtos.objects.get(id=1183)
        chapa25 = MP_Produtos.objects.get(id=1381)
        perfil_u4 = MP_Produtos.objects.get(id=1382)
        alca = MP_Produtos.objects.get(id=1383)
        
        print("📋 PRODUTOS (valores unitários):")
        print(f"   I25: R$ {perfil_i25.custo_centavos/100:.2f}/m")
        print(f"   Chaveta: R$ {chaveta.custo_centavos/100:.2f}/m")
        print(f"   Cola: R$ {cola.custo_centavos/100:.2f}/unid")
        print(f"   Chapa 2,5mm: R$ {chapa25.custo_centavos/100:.2f}/m²")
        print(f"   Perfil U4\": R$ {perfil_u4.custo_centavos/100:.2f}/m")
        print(f"   Alça: R$ {alca.custo_centavos/100:.2f}/unid")
        
        # Simular dados da interface (da imagem)
        # Baseado nas quantidades mostradas: I25=20m, Chaveta=13.33m, etc.
        print(f"\n🧮 CÁLCULOS BASEADOS NA IMAGEM:")
        
        # Dados simulados (deduzidos da imagem)
        qtd_i25 = 20.0    # metros
        qtd_chaveta = 13.3333  # metros 
        qtd_cola = 0.1    # unidades
        area_chapa = 1.0  # m²
        qtd_u4 = 2.0      # unidades
        qtd_alca = 2.0    # unidades
        
        # Custos base (sem perda)
        custo_i25_base = qtd_i25 * perfil_i25.custo_centavos
        custo_chaveta_base = qtd_chaveta * chaveta.custo_centavos
        custo_cola_base = qtd_cola * cola.custo_centavos
        custo_chapa_base = area_chapa * chapa25.custo_centavos
        custo_u4_base = qtd_u4 * perfil_u4.custo_centavos
        custo_alca_base = qtd_alca * alca.custo_centavos
        
        # Custos com 5% perda (uma vez)
        fator_perda = 1.05
        custo_i25_perda = custo_i25_base * fator_perda
        custo_chaveta_perda = custo_chaveta_base * fator_perda
        custo_cola_perda = custo_cola_base * fator_perda
        custo_chapa_perda = custo_chapa_base * fator_perda
        custo_u4_perda = custo_u4_base * fator_perda
        custo_alca_perda = custo_alca_base * fator_perda
        
        print(f"\n✅ VALORES CORRETOS (com 5% perda aplicada UMA vez):")
        print(f"   I25: {qtd_i25:.1f}m × R${perfil_i25.custo_centavos/100:.2f} = R${custo_i25_base/100:.2f} → R${custo_i25_perda/100:.2f}")
        print(f"   Chaveta: {qtd_chaveta:.2f}m × R${chaveta.custo_centavos/100:.2f} = R${custo_chaveta_base/100:.2f} → R${custo_chaveta_perda/100:.2f}")
        print(f"   Cola: {qtd_cola:.1f}un × R${cola.custo_centavos/100:.2f} = R${custo_cola_base/100:.2f} → R${custo_cola_perda/100:.2f}")
        print(f"   Chapa: {area_chapa:.1f}m² × R${chapa25.custo_centavos/100:.2f} = R${custo_chapa_base/100:.2f} → R${custo_chapa_perda/100:.2f}")
        print(f"   U4\": {qtd_u4:.1f}un × R${perfil_u4.custo_centavos/100:.2f} = R${custo_u4_base/100:.2f} → R${custo_u4_perda/100:.2f}")
        print(f"   Alça: {qtd_alca:.1f}un × R${alca.custo_centavos/100:.2f} = R${custo_alca_base/100:.2f} → R${custo_alca_perda/100:.2f}")
        
        # Comparar com os valores da imagem
        print(f"\n📊 COMPARAÇÃO COM A IMAGEM:")
        valores_imagem = {
            'I25': 142.88,
            'Chaveta': 31.16,
            'Cola': 9.12,
            'Chapa': 84.00,
            'U4': 46.64,
            'Alca': 63.00
        }
        
        valores_corretos = {
            'I25': custo_i25_perda/100,
            'Chaveta': custo_chaveta_perda/100,
            'Cola': custo_cola_perda/100,
            'Chapa': custo_chapa_perda/100,
            'U4': custo_u4_perda/100,
            'Alca': custo_alca_perda/100
        }
        
        for item in valores_imagem:
            img_val = valores_imagem[item]
            correct_val = valores_corretos[item]
            diff = abs(img_val - correct_val)
            status = "✅" if diff < 0.50 else "❌"
            
            print(f"   {item}: Imagem=R${img_val:.2f} | Correto=R${correct_val:.2f} | Diff=R${diff:.2f} {status}")
        
        print(f"\n🎯 RESUMO:")
        total_imagem = sum(valores_imagem.values())
        total_correto = sum(valores_corretos.values())
        print(f"   Total imagem: R$ {total_imagem:.2f}")
        print(f"   Total correto: R$ {total_correto:.2f}")
        print(f"   Diferença: R$ {abs(total_imagem - total_correto):.2f}")
        
        if abs(total_imagem - total_correto) < 2.0:
            print(f"   ✅ Valores muito próximos - correção funcionou!")
        else:
            print(f"   ❌ Ainda há diferenças significativas")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    validar_correcao_tampa_montada()
