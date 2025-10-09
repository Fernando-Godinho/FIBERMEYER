#!/usr/bin/env python
"""
Teste completo da lógica de cálculo de grade
Simula uma requisição para verificar se a função calcularGrade() está funcionando
"""

import os
import django
import sys

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos

def testar_calculo_grade():
    print("=== TESTE DE CÁLCULO DE GRADE ===")
    
    # Buscar produtos necessários
    print("\n1. Verificando produtos na base:")
    
    # Verificar perfis I
    perfis_i = MP_Produtos.objects.filter(descricao__icontains='I25')
    print(f"   Perfis I25 encontrados: {perfis_i.count()}")
    for perfil in perfis_i:
        print(f"   - ID {perfil.id}: {perfil.descricao} - R$ {perfil.custo_centavos/100:.2f} - {perfil.peso_und} kg/m")
    
    # Verificar chaveta
    chaveta = MP_Produtos.objects.filter(id=1332).first()
    if chaveta:
        print(f"   ✅ Chaveta ID 1332: {chaveta.descricao} - R$ {chaveta.custo_centavos/100:.2f} - {chaveta.peso_und} kg/m")
    else:
        print("   ❌ Chaveta ID 1332 não encontrada!")
    
    # Verificar cola
    cola = MP_Produtos.objects.filter(id=1183).first()
    if cola:
        print(f"   ✅ Cola ID 1183: {cola.descricao} - R$ {cola.custo_centavos/100:.2f} - {cola.peso_und} kg/unid")
    else:
        print("   ❌ Cola ID 1183 não encontrada!")
    
    # Verificar mão de obra
    mao_obra = MP_Produtos.objects.filter(
        descricao__icontains='mão de obra'
    ).filter(
        descricao__icontains='processamento'
    ).first()
    if mao_obra:
        print(f"   ✅ Mão de obra: {mao_obra.descricao} - R$ {mao_obra.custo_centavos/100:.2f}")
    else:
        print("   ❌ Mão de obra Processamento/Montagem não encontrada!")
    
    print("\n2. Simulando cálculo de grade:")
    
    # Dados de exemplo
    dados = {
        'nome_grade': 'GRADE TESTE 40x40',
        'vao': 400.0,  # mm
        'comprimento': 1000.0,  # mm
        'eixo_i': 40.0,  # mm
        'perfil_id': perfis_i.first().id if perfis_i.exists() else None,
        'perda': 3.0,  # %
        'tempo_proc': 1.5,  # horas
        'tempo_mtg': 0.5,  # horas
    }
    
    print(f"   Dados: {dados}")
    
    if not dados['perfil_id']:
        print("   ❌ Erro: Perfil não encontrado!")
        return
    
    # Buscar o perfil selecionado
    perfil_selecionado = MP_Produtos.objects.get(id=dados['perfil_id'])
    
    print(f"\n3. Perfil selecionado:")
    print(f"   ID: {perfil_selecionado.id}")
    print(f"   Descrição: {perfil_selecionado.descricao}")
    print(f"   Peso: {perfil_selecionado.peso_und} kg/m")
    print(f"   Custo: R$ {perfil_selecionado.custo_centavos/100:.2f}/m")
    
    print(f"\n4. Aplicando fórmula:")
    
    # FÓRMULA: (((comprimento/eixo i)*vão/1000)* peso do perfil)
    metros_lineares_por_m2 = (dados['comprimento'] / dados['eixo_i']) * (dados['vao'] / 1000)
    print(f"   Fórmula: ({dados['comprimento']}/{dados['eixo_i']}) * ({dados['vao']}/1000)")
    print(f"   Metros lineares/m²: {metros_lineares_por_m2:.4f} m/m²")
    
    # Calcular para o perfil
    peso_perfil_kg = metros_lineares_por_m2 * float(perfil_selecionado.peso_und)
    custo_perfil_centavos = metros_lineares_por_m2 * float(perfil_selecionado.custo_centavos)
    print(f"   Perfil - Peso: {peso_perfil_kg:.3f} kg/m² | Custo: R$ {custo_perfil_centavos/100:.2f}/m²")
    
    # Calcular para a chaveta - FÓRMULA ESPECÍFICA: vão / 150 * 2 * preço do perfil
    quantidade_chaveta = (dados['vao'] / 150) * 2
    peso_chaveta = quantidade_chaveta * float(chaveta.peso_und)
    custo_chaveta = quantidade_chaveta * float(chaveta.custo_centavos)
    print(f"   Chaveta - Fórmula: ({dados['vao']}/150) * 2 = {quantidade_chaveta:.4f} m/m²")
    print(f"   Chaveta - Peso: {peso_chaveta:.3f} kg/m² | Custo: R$ {custo_chaveta/100:.2f}/m²")
    
    # Calcular para a cola - FÓRMULA: quantidade fixa 0.06 unid/m²
    quantidade_cola = 0.06  # Quantidade fixa
    peso_cola = quantidade_cola * float(cola.peso_und)
    custo_cola = quantidade_cola * float(cola.custo_centavos)
    print(f"   Cola - Quantidade fixa: {quantidade_cola:.4f} unid/m²")
    print(f"   Cola - Peso: {peso_cola:.3f} kg/m² | Custo: R$ {custo_cola/100:.2f}/m²")
    
    # Aplicar perda aos materiais
    fator_perda = 1 + (dados['perda'] / 100)
    print(f"\n5. Aplicando perda de {dados['perda']}% (fator: {fator_perda}):")
    
    # Calcular mão de obra - R$ 65.79/hora
    valor_hora_mo = 65.79  # R$/hora
    tempo_total = dados['tempo_proc'] + dados['tempo_mtg']
    custo_mao_obra_total = tempo_total * valor_hora_mo * 100  # em centavos
    mao_obra_descricao = f"Processamento/Montagem ({tempo_total}h)"
    print(f"   Mão de Obra: {mao_obra_descricao} - R$ {custo_mao_obra_total/100:.2f}/m²")
    
    # CUSTO TOTAL = Materiais com perda + Mão de obra (sem perda)
    peso_total_kg = (peso_perfil_kg + peso_chaveta + peso_cola) * fator_perda
    custo_total_centavos = (custo_perfil_centavos + custo_chaveta + custo_cola) * fator_perda + custo_mao_obra_total
    
    print(f"\n6. RESUMO FINAL:")
    print(f"   Materiais (com {dados['perda']}% perda): R$ {((custo_perfil_centavos + custo_chaveta + custo_cola) * fator_perda)/100:.2f}/m²")
    print(f"   Mão de Obra (sem perda): R$ {custo_mao_obra_total/100:.2f}/m²")
    print(f"   TOTAL FINAL: R$ {custo_total_centavos/100:.2f}/m² | Peso: {peso_total_kg:.3f} kg/m²")
    
    print(f"\n✅ Teste concluído com sucesso!")

if __name__ == "__main__":
    testar_calculo_grade()