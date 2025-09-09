#!/usr/bin/env python3
"""
Teste para verificar o impacto dos 3% de perda aplicados nas matérias-primas.
"""

print("=== TESTE: APLICAÇÃO DE 3% DE PERDA ===")
print("Verificando o impacto dos 3% de perda aplicados nas matérias-primas")
print()

# Simulação de um cálculo típico
dados_exemplo = {
    'nome_perfil': 'Perfil Teste 100x50mm',
    'roving_4400_kg': 0.5,
    'manta_300_kg': 0.3,
    'veu_kg': 0.1,
    'peso_metro_kg': 1.2,
    'area_pintura_m2': 0.8,
    'metros_produzidos_h': 12,
    'n_matrizes': 2,
    'n_maquinas': 1
}

# Preços atualizados da base (do teste anterior)
precos_atuais = {
    'roving': 4.81,
    'manta': 10.00,
    'veu': 25.00,  # padrão (não encontrado)
    'resina': 12.96,
    'monomero': 12.80,
    'anti_uv': 163.79,
    'anti_ox': 59.28,
    'bpo': 58.57,
    'tbpb': 67.56,
    'desmoldante': 112.62,
    'antichama': 5.76,
    'carga_mineral': 1.31,
    'pigmento': 49.40,
    'pintura': 15.00  # padrão (não encontrado)
}

# Calcular peso da resina base
peso_resina_base = dados_exemplo['peso_metro_kg'] - (
    dados_exemplo['roving_4400_kg'] + 
    dados_exemplo['manta_300_kg'] + 
    dados_exemplo['veu_kg']
)

print(f"📊 DADOS DO PERFIL: {dados_exemplo['nome_perfil']}")
print(f"Peso total: {dados_exemplo['peso_metro_kg']} kg")
print(f"Peso resina base: {peso_resina_base:.3f} kg")
print()

# Fatores de composição da resina
fatores = {
    'resina': 0.6897,
    'monomero': 0.0213,
    'anti_uv': 0.0028,
    'anti_ox': 0.0011,
    'bpo': 0.0071,
    'tbpb': 0.0043,
    'desmoldante': 0.0071,
    'antichama': 0.1777,
    'carga_mineral': 0.0711,
    'pigmento': 0.0178
}

print("💰 CÁLCULO DE CUSTOS POR COMPONENTE:")
print("-" * 70)

componentes = []

# Componentes diretos (fibras)
componentes_diretos = [
    ('Roving 4400 KG', dados_exemplo['roving_4400_kg'], precos_atuais['roving']),
    ('Manta 300 KG', dados_exemplo['manta_300_kg'], precos_atuais['manta']),
    ('Véu KG', dados_exemplo['veu_kg'], precos_atuais['veu'])
]

# Componentes da resina
componentes_resina = [
    ('Resina PET', peso_resina_base * fatores['resina'], precos_atuais['resina']),
    ('Monômero de estireno', peso_resina_base * fatores['monomero'], precos_atuais['monomero']),
    ('Anti UV', peso_resina_base * fatores['anti_uv'], precos_atuais['anti_uv']),
    ('Anti OX', peso_resina_base * fatores['anti_ox'], precos_atuais['anti_ox']),
    ('BPO', peso_resina_base * fatores['bpo'], precos_atuais['bpo']),
    ('TBPB', peso_resina_base * fatores['tbpb'], precos_atuais['tbpb']),
    ('Desmoldante', peso_resina_base * fatores['desmoldante'], precos_atuais['desmoldante']),
    ('Antichama', peso_resina_base * fatores['antichama'], precos_atuais['antichama']),
    ('Carga mineral', peso_resina_base * fatores['carga_mineral'], precos_atuais['carga_mineral']),
    ('Pigmento', peso_resina_base * fatores['pigmento'], precos_atuais['pigmento'])
]

# Pintura
pintura = ('Área pintura (m²)', dados_exemplo['area_pintura_m2'], precos_atuais['pintura'])

total_materias_primas = 0

print("MATÉRIAS-PRIMAS:")
for nome, quantidade, preco in componentes_diretos + componentes_resina + [pintura]:
    custo = quantidade * preco
    total_materias_primas += custo
    componentes.append((nome, quantidade, preco, custo, True))  # True = é matéria-prima
    print(f"  {nome:25s}: {quantidade:6.4f} x R$ {preco:7.2f} = R$ {custo:8.2f}")

# Cálculo da mão de obra
mo_pultrusao = 9976258  # centavos
numerador = (mo_pultrusao / 3) * dados_exemplo['n_maquinas']
denominador = dados_exemplo['metros_produzidos_h'] * dados_exemplo['n_matrizes'] * 24 * 21 * 0.5
custo_mao_obra = numerador / denominador / 100

componentes.append(('Mão de Obra - Pultrusão', 1.0, custo_mao_obra, custo_mao_obra, False))  # False = não é matéria-prima

print(f"\nMÃO DE OBRA:")
print(f"  Mão de Obra - Pultrusão   : {1.0:6.4f} x R$ {custo_mao_obra:7.2f} = R$ {custo_mao_obra:8.2f}")

print("\n" + "=" * 70)

# Aplicar 3% de perda
perda_3_pct = total_materias_primas * 0.03
total_materias_com_perda = total_materias_primas * 1.03
total_final = total_materias_com_perda + custo_mao_obra

print("📈 APLICAÇÃO DE 3% DE PERDA:")
print(f"Subtotal matérias-primas:     R$ {total_materias_primas:8.2f}")
print(f"3% de perda:                  R$ {perda_3_pct:8.2f}")
print(f"Matérias-primas com perda:    R$ {total_materias_com_perda:8.2f}")
print(f"Mão de obra:                  R$ {custo_mao_obra:8.2f}")
print(f"TOTAL FINAL:                  R$ {total_final:8.2f}")

print("\n" + "=" * 70)

# Comparação com cálculo sem perda
total_sem_perda = total_materias_primas + custo_mao_obra
diferenca_absoluta = total_final - total_sem_perda
diferenca_percentual = (diferenca_absoluta / total_sem_perda) * 100

print("📊 IMPACTO DOS 3% DE PERDA:")
print(f"Custo sem perda:              R$ {total_sem_perda:8.2f}")
print(f"Custo com 3% perda:           R$ {total_final:8.2f}")
print(f"Diferença:                    R$ {diferenca_absoluta:8.2f} (+{diferenca_percentual:.2f}%)")

print("\n" + "=" * 70)

# Análise por categoria de custo
custo_fibras = sum([c[3] for c in componentes if 'KG' in c[0] and c[4]])  # Roving, Manta, Véu
custo_resina_mix = sum([c[3] for c in componentes if c[0] in ['Resina PET', 'Monômero de estireno', 'Anti UV', 'Anti OX', 'BPO', 'TBPB', 'Desmoldante', 'Antichama', 'Carga mineral', 'Pigmento']])
custo_pintura_val = sum([c[3] for c in componentes if 'pintura' in c[0].lower()])

print("🎯 BREAKDOWN POR CATEGORIA:")
print(f"Fibras (Roving/Manta/Véu):    R$ {custo_fibras:8.2f} ({(custo_fibras/total_materias_primas)*100:5.1f}%)")
print(f"Sistema de resina:            R$ {custo_resina_mix:8.2f} ({(custo_resina_mix/total_materias_primas)*100:5.1f}%)")
print(f"Pintura:                      R$ {custo_pintura_val:8.2f} ({(custo_pintura_val/total_materias_primas)*100:5.1f}%)")
print(f"Mão de obra (sem perda):      R$ {custo_mao_obra:8.2f}")

perda_fibras = custo_fibras * 0.03
perda_resina = custo_resina_mix * 0.03
perda_pintura = custo_pintura_val * 0.03

print(f"\nPERDA 3% POR CATEGORIA:")
print(f"Perda em fibras:              R$ {perda_fibras:8.2f}")
print(f"Perda em resina:              R$ {perda_resina:8.2f}")
print(f"Perda em pintura:             R$ {perda_pintura:8.2f}")
print(f"Total da perda:               R$ {perda_3_pct:8.2f}")

print("\n" + "=" * 70)
print("🚀 STATUS DA IMPLEMENTAÇÃO:")
print()
print("✅ Aplicação de 3% de perda implementada em:")
print("   - main/templates/main/mp.html")
print("     • calcularNovoPerfil() - função principal")
print("     • calcularNovoPerfilComPrecosDefault() - fallback")
print("   - main/templates/main/orcamento.html")
print("     • calcularNovoPerfilOrcamento() - função principal")
print("     • calcularNovoPerfilOrcamentoComPrecosDefault() - fallback")
print()
print("✅ Características da implementação:")
print("   - Aplica 3% apenas nas matérias-primas")
print("   - Mão de obra não sofre perda")
print("   - Logs detalhados para debug")
print("   - Indicação visual '(com 3% perda)' nos resultados")
print()
print("🧪 COMO TESTAR:")
print("1. Executar 'python manage.py runserver'")
print("2. Acessar http://127.0.0.1:8000/mp/ ou /orcamento/")
print("3. Selecionar 'Novo Perfil' no dropdown")
print("4. Preencher campos e calcular")
print("5. Verificar logs no console (F12):")
print("   - '=== APLICAÇÃO DE 3% DE PERDA ==='")
print("   - Valores antes e depois da perda")
print("   - Separação matérias-primas vs mão de obra")
print("6. Verificar mensagem '(com 3% perda)' no resultado")

print(f"\n💡 EXEMPLO PRÁTICO:")
print(f"Para o perfil teste calculado, a diferença de R$ {diferenca_absoluta:.2f}")
print(f"representa um acréscimo de {diferenca_percentual:.1f}% no custo total,")
print(f"garantindo margem adequada para perdas no processo produtivo.")
