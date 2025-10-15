#!/usr/bin/env python
"""
Script para atualizar a base de impostos ICMS com os dados de 2025
Baseado na tabela fornecida pelo usuário
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

def atualizar_impostos_2025():
    """Atualiza os impostos ICMS com as novas alíquotas de 2025"""
    
    # Dados fornecidos pelo usuário para 2025
    dados_icms_2025 = {
        # Estado: [CONTRIB_INDUSTRIALIZAÇÃO, CONTRIB_USO_CONSUMO, NAO_CONTRIB_INDUSTRIALIZAÇÃO, NAO_CONTRIB_USO_CONSUMO]
        'AC': [7.0, 7.2, 19.62, 7.2],
        'AL': [7.0, 7.2, 19.62, 7.2],
        'AM': [7.0, 7.2, 20.65, 7.2],
        'AP': [7.0, 7.2, 18.59, 7.2],
        'BA': [7.0, 7.2, 21.17, 7.2],
        'CE': [7.0, 7.2, 20.65, 7.2],
        'DF': [7.0, 7.2, 20.65, 7.2],
        'ES': [7.0, 7.2, 17.55, 7.2],
        'GO': [7.0, 7.2, 19.62, 7.2],
        'MA': [7.0, 7.2, 22.72, 7.2],
        'MT': [7.0, 7.2, 17.55, 7.2],
        'MS': [7.0, 7.2, 17.55, 7.2],
        'MG': [12.0, 12.4, 18.59, 12.4],
        'PA': [7.0, 7.2, 20.65, 7.2],
        'PB': [7.0, 7.2, 20.65, 7.2],
        'PR': [12.0, 12.4, 20.13, 12.4],
        'PE': [7.0, 7.2, 21.17, 7.2],
        'PI': [7.0, 7.2, 21.68, 7.2],
        'RN': [7.0, 7.2, 18.59, 7.2],
        'RS': [12.0, None, 17.55, None],  # RS não tem valores para uso/consumo
        'RJ': [12.0, 12.4, 20.65, 12.4],
        'RO': [7.0, 7.2, 20.13, 7.2],
        'RR': [7.0, 7.2, 20.65, 7.2],
        'SC': [12.0, 12.4, 17.55, 12.4],
        'SP': [12.0, 12.4, 18.59, 12.4],
        'SE': [7.0, 7.2, 19.62, 7.2],
        'TO': [7.0, 7.2, 20.65, 7.2],
    }
    
    print("🔄 ATUALIZANDO IMPOSTOS ICMS PARA 2025")
    print("=" * 60)
    
    impostos_atualizados = 0
    impostos_criados = 0
    
    for estado, valores in dados_icms_2025.items():
        contrib_indust, contrib_uso, nao_contrib_indust, nao_contrib_uso = valores
        
        # 1. ICMS Contribuinte Industrialização
        nome_contrib_indust = f"ICMS {estado} - Contribuinte Industrialização"
        imposto, criado = Imposto.objects.get_or_create(
            nome=nome_contrib_indust,
            defaults={
                'descricao': f'ICMS para {estado} - Contribuinte para Industrialização',
                'aliquota': Decimal(str(contrib_indust)),
                'ativo': True
            }
        )
        
        if not criado and imposto.aliquota != Decimal(str(contrib_indust)):
            old_aliquota = imposto.aliquota
            imposto.aliquota = Decimal(str(contrib_indust))
            imposto.save()
            print(f"   📝 {estado} - Contrib. Industrialização: {old_aliquota}% → {contrib_indust}%")
            impostos_atualizados += 1
        elif criado:
            print(f"   ✅ {estado} - Contrib. Industrialização: {contrib_indust}% (NOVO)")
            impostos_criados += 1
        
        # 2. ICMS Contribuinte Uso/Consumo (se existir)
        if contrib_uso is not None:
            nome_contrib_uso = f"ICMS {estado} - Contribuinte Uso/Consumo"
            imposto, criado = Imposto.objects.get_or_create(
                nome=nome_contrib_uso,
                defaults={
                    'descricao': f'ICMS para {estado} - Contribuinte para Uso/Consumo',
                    'aliquota': Decimal(str(contrib_uso)),
                    'ativo': True
                }
            )
            
            if not criado and imposto.aliquota != Decimal(str(contrib_uso)):
                old_aliquota = imposto.aliquota
                imposto.aliquota = Decimal(str(contrib_uso))
                imposto.save()
                print(f"   📝 {estado} - Contrib. Uso/Consumo: {old_aliquota}% → {contrib_uso}%")
                impostos_atualizados += 1
            elif criado:
                print(f"   ✅ {estado} - Contrib. Uso/Consumo: {contrib_uso}% (NOVO)")
                impostos_criados += 1
        
        # 3. ICMS Não Contribuinte Industrialização
        nome_nao_contrib_indust = f"ICMS {estado} - Não Contribuinte Industrialização"
        imposto, criado = Imposto.objects.get_or_create(
            nome=nome_nao_contrib_indust,
            defaults={
                'descricao': f'ICMS para {estado} - Não Contribuinte para Industrialização',
                'aliquota': Decimal(str(nao_contrib_indust)),
                'ativo': True
            }
        )
        
        if not criado and imposto.aliquota != Decimal(str(nao_contrib_indust)):
            old_aliquota = imposto.aliquota
            imposto.aliquota = Decimal(str(nao_contrib_indust))
            imposto.save()
            print(f"   📝 {estado} - Não Contrib. Industrialização: {old_aliquota}% → {nao_contrib_indust}%")
            impostos_atualizados += 1
        elif criado:
            print(f"   ✅ {estado} - Não Contrib. Industrialização: {nao_contrib_indust}% (NOVO)")
            impostos_criados += 1
        
        # 4. ICMS Não Contribuinte Uso/Consumo (se existir)
        if nao_contrib_uso is not None:
            nome_nao_contrib_uso = f"ICMS {estado} - Não Contribuinte Uso/Consumo"
            imposto, criado = Imposto.objects.get_or_create(
                nome=nome_nao_contrib_uso,
                defaults={
                    'descricao': f'ICMS para {estado} - Não Contribuinte para Uso/Consumo',
                    'aliquota': Decimal(str(nao_contrib_uso)),
                    'ativo': True
                }
            )
            
            if not criado and imposto.aliquota != Decimal(str(nao_contrib_uso)):
                old_aliquota = imposto.aliquota
                imposto.aliquota = Decimal(str(nao_contrib_uso))
                imposto.save()
                print(f"   📝 {estado} - Não Contrib. Uso/Consumo: {old_aliquota}% → {nao_contrib_uso}%")
                impostos_atualizados += 1
            elif criado:
                print(f"   ✅ {estado} - Não Contrib. Uso/Consumo: {nao_contrib_uso}% (NOVO)")
                impostos_criados += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DA ATUALIZAÇÃO:")
    print(f"   📝 Impostos atualizados: {impostos_atualizados}")
    print(f"   ✅ Impostos criados: {impostos_criados}")
    print(f"   📋 Total de impostos ICMS: {Imposto.objects.filter(nome__icontains='ICMS').count()}")
    
    # Mostrar alguns exemplos dos estados com maiores diferenças
    print("\n🏆 ESTADOS COM MAIORES ALÍQUOTAS PARA NÃO CONTRIBUINTES:")
    maiores_nao_contrib = Imposto.objects.filter(
        nome__icontains="Não Contribuinte Industrialização"
    ).order_by('-aliquota')[:5]
    
    for imposto in maiores_nao_contrib:
        estado = imposto.nome.split()[1]
        print(f"   🥇 {estado}: {imposto.aliquota}%")
    
    print("\n✅ Atualização concluída com sucesso!")

if __name__ == "__main__":
    try:
        atualizar_impostos_2025()
    except Exception as e:
        print(f"❌ Erro durante a atualização: {e}")
        raise