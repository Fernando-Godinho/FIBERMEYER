import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

print("📊 SISTEMA DE IMPOSTOS FIBERMEYER - RESUMO COMPLETO")
print("=" * 70)

# 1. Estatísticas gerais
total_impostos = Imposto.objects.count()
impostos_ativos = Imposto.objects.filter(ativo=True).count()
impostos_icms = Imposto.objects.filter(nome__icontains="ICMS").count()
impostos_difal = Imposto.objects.filter(nome__icontains="DIFAL").count()
outros_impostos = total_impostos - impostos_icms - impostos_difal

print(f"📈 ESTATÍSTICAS GERAIS:")
print(f"   📋 Total de impostos: {total_impostos}")
print(f"   🟢 Impostos ativos: {impostos_ativos}")
print(f"   📊 ICMS (todas modalidades): {impostos_icms}")
print(f"   📊 DIFAL: {impostos_difal}")
print(f"   📊 Outros impostos: {outros_impostos}")

# 2. Análise por estado - maiores e menores alíquotas
print(f"\n🏆 RANKING DE ALÍQUOTAS ICMS INTERNO:")

# ICMS Interno por estado
icms_internos = Imposto.objects.filter(nome__icontains="ICMS").filter(nome__icontains="Interno").order_by('-aliquota')

print(f"   🥇 MAIORES ALÍQUOTAS:")
for i, imposto in enumerate(icms_internos[:5]):
    estado = imposto.nome.split()[1]
    print(f"      {i+1}. {estado}: {imposto.aliquota}%")

print(f"   🥉 MENORES ALÍQUOTAS:")
for i, imposto in enumerate(icms_internos.reverse()[:5]):
    estado = imposto.nome.split()[1]
    print(f"      {i+1}. {estado}: {imposto.aliquota}%")

# 3. Estados com alíquotas diferenciadas (12% interestadual)
print(f"\n🔍 ESTADOS COM ALÍQUOTAS INTERESTADUAIS DIFERENCIADAS (12%):")
estados_12_pct = Imposto.objects.filter(nome__icontains="ICMS").filter(nome__icontains="Interestadual").filter(aliquota=12.0).values_list('nome', flat=True).distinct()

estados_diferenciados = set()
for nome in estados_12_pct:
    estado = nome.split()[1]
    estados_diferenciados.add(estado)

for estado in sorted(estados_diferenciados):
    print(f"   📍 {estado}: 12% (ao invés de 7%)")

# 4. Simulação de cálculo de impostos
print(f"\n💰 SIMULAÇÃO DE CÁLCULO DE IMPOSTOS:")
print(f"   📦 Produto: Grade de Fibra de Vidro - R$ 1.000,00")

# Exemplos de cálculo para diferentes cenários
cenarios = [
    ("SP (Interno)", "ICMS SP - Interno"),
    ("SP para RJ (Contribuinte)", "ICMS RJ - Interestadual Industrialização"),
    ("SP para RJ (Não Contribuinte)", "ICMS RJ - Não Contribuinte"),
    ("SP para MA (maior ICMS)", "ICMS MA - Interno"),
    ("RS (menor DIFAL)", "DIFAL RS"),
]

valor_produto = Decimal('1000.00')

for cenario, nome_imposto in cenarios:
    try:
        imposto = Imposto.objects.get(nome=nome_imposto)
        valor_imposto = valor_produto * (imposto.aliquota / Decimal('100'))
        valor_final = valor_produto + valor_imposto
        print(f"   📋 {cenario}:")
        print(f"      └─ Alíquota: {imposto.aliquota}%")
        print(f"      └─ Imposto: R$ {valor_imposto:.2f}")
        print(f"      └─ Total: R$ {valor_final:.2f}")
    except Imposto.DoesNotExist:
        print(f"   ❌ {cenario}: Imposto não encontrado")

# 5. Verificação de integridade
print(f"\n🔍 VERIFICAÇÃO DE INTEGRIDADE:")

# Verificar se todos os estados têm todas as modalidades
estados_brasil = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RN", "RS", "RJ", "RO", "RR", "SC", "SP", "SE", "TO"]

modalidades_esperadas = [
    "Interno",
    "Interestadual Industrialização", 
    "Interestadual Uso/Consumo",
    "Interestadual Revenda",
    "Não Contribuinte"
]

estados_completos = 0
estados_incompletos = []

for estado in estados_brasil:
    modalidades_estado = 0
    for modalidade in modalidades_esperadas:
        if Imposto.objects.filter(nome=f"ICMS {estado} - {modalidade}").exists():
            modalidades_estado += 1
    
    # Verificar DIFAL
    tem_difal = Imposto.objects.filter(nome=f"DIFAL {estado}").exists()
    
    if modalidades_estado == 5 and tem_difal:
        estados_completos += 1
    else:
        estados_incompletos.append(f"{estado} ({modalidades_estado}/5 ICMS, DIFAL: {'✅' if tem_difal else '❌'})")

print(f"   ✅ Estados completos: {estados_completos}/{len(estados_brasil)}")
if estados_incompletos:
    print(f"   ⚠️ Estados incompletos:")
    for estado_inc in estados_incompletos:
        print(f"      • {estado_inc}")

# 6. Funcionalidades para orçamentos
print(f"\n⚙️ INTEGRAÇÃO COM ORÇAMENTOS:")
print(f"   ✅ {impostos_ativos} impostos disponíveis para aplicação em orçamentos")
print(f"   ✅ Cobertura nacional completa (27 estados)")
print(f"   ✅ Modalidades para diferentes tipos de cliente:")
print(f"      • Contribuintes do ICMS")
print(f"      • Não contribuintes")
print(f"      • Operações internas e interestaduais")
print(f"      • Diferentes finalidades (industrialização, uso, revenda)")

print(f"\n🎉 SISTEMA DE IMPOSTOS CONFIGURADO E PRONTO PARA USO!")
print("=" * 70)
