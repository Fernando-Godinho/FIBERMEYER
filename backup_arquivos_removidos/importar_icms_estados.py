import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import Imposto

print("📊 IMPORTANDO TABELA DE ICMS POR ESTADO")
print("=" * 60)

# Dados da tabela de ICMS por estado
dados_icms = [
    # ESTADO, ALÍQUOTA_INTERNA, ALÍQUOTA_INTERESTADUAL_CONTRIB, ALÍQUOTA_INDUSTRIALIZAÇÃO, ALÍQUOTA_USO_CONSUMO, ALÍQUOTA_REVENDA, ALÍQUOTA_NAO_CONTRIB_INDUSTRIALIZAÇÃO, DIFAL
    ("AC", 19.0, 7.0, 7.0, 7.2, 7.0, 19.6, 12),
    ("AL", 19.0, 7.0, 7.0, 7.2, 7.0, 19.6, 12),
    ("AM", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
    ("AP", 18.0, 7.0, 7.0, 7.2, 7.0, 18.6, 11),
    ("BA", 20.5, 7.0, 7.0, 7.2, 7.0, 21.2, 14),
    ("CE", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
    ("DF", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
    ("ES", 17.0, 7.0, 7.0, 7.2, 7.0, 17.6, 10),
    ("GO", 19.0, 7.0, 7.0, 7.2, 7.0, 19.6, 12),
    ("MA", 22.0, 7.0, 7.0, 7.2, 7.0, 22.7, 15),
    ("MT", 17.0, 7.0, 7.0, 7.2, 7.0, 17.6, 10),
    ("MS", 17.0, 7.0, 7.0, 7.2, 7.0, 17.6, 10),
    ("MG", 18.0, 12.0, 12.0, 12.4, 12.0, 18.6, 6),
    ("PA", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
    ("PB", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
    ("PR", 19.5, 12.0, 12.0, 12.4, 12.0, 20.1, 8),
    ("PE", 20.5, 7.0, 7.0, 7.2, 7.0, 21.2, 14),
    ("PI", 21.0, 7.0, 7.0, 7.2, 7.0, 21.7, 14),
    ("RN", 18.0, 7.0, 7.0, 7.2, 7.0, 18.6, 11),
    ("RS", 17.0, 12.0, 12.0, 17.6, 12.0, 17.6, 5),
    ("RJ", 20.0, 12.0, 12.0, 12.4, 12.0, 20.7, 8),
    ("RO", 19.5, 7.0, 7.0, 7.2, 7.0, 20.1, 13),
    ("RR", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
    ("SC", 17.0, 12.0, 12.0, 12.4, 12.0, 17.6, 5),
    ("SP", 18.0, 12.0, 12.0, 12.4, 12.0, 18.6, 6),
    ("SE", 19.0, 7.0, 7.0, 7.2, 7.0, 19.6, 12),
    ("TO", 20.0, 7.0, 7.0, 7.2, 7.0, 20.7, 13),
]

# Limpar impostos existentes de ICMS se necessário
impostos_icms_existentes = Imposto.objects.filter(nome__icontains="ICMS")
if impostos_icms_existentes.exists():
    print(f"⚠️ Encontrados {impostos_icms_existentes.count()} impostos ICMS existentes")
    resposta = input("Deseja remover e recriar? (s/N): ")
    if resposta.lower() == 's':
        impostos_icms_existentes.delete()
        print("🗑️ Impostos ICMS existentes removidos")

print(f"\n📥 Importando {len(dados_icms)} estados...")

impostos_criados = 0

for estado, aliq_interna, aliq_inter_contrib, aliq_indust, aliq_uso, aliq_revenda, aliq_nao_contrib, difal in dados_icms:
    
    # 1. ICMS Interno (operações dentro do estado)
    nome_interno = f"ICMS {estado} - Interno"
    imposto_interno, criado = Imposto.objects.get_or_create(
        nome=nome_interno,
        defaults={
            'descricao': f'ICMS interno para operações dentro do estado {estado}',
            'aliquota': aliq_interna,
            'ativo': True
        }
    )
    if criado:
        impostos_criados += 1
        print(f"   ✅ {nome_interno}: {aliq_interna}%")
    
    # 2. ICMS Interestadual - Contribuinte Industrialização
    nome_inter_indust = f"ICMS {estado} - Interestadual Industrialização"
    imposto_inter_indust, criado = Imposto.objects.get_or_create(
        nome=nome_inter_indust,
        defaults={
            'descricao': f'ICMS interestadual para industrialização - {estado} (contribuinte)',
            'aliquota': aliq_indust,
            'ativo': True
        }
    )
    if criado:
        impostos_criados += 1
        print(f"   ✅ {nome_inter_indust}: {aliq_indust}%")
    
    # 3. ICMS Interestadual - Contribuinte Uso/Consumo
    nome_inter_uso = f"ICMS {estado} - Interestadual Uso/Consumo"
    imposto_inter_uso, criado = Imposto.objects.get_or_create(
        nome=nome_inter_uso,
        defaults={
            'descricao': f'ICMS interestadual para uso/consumo - {estado} (contribuinte)',
            'aliquota': aliq_uso,
            'ativo': True
        }
    )
    if criado:
        impostos_criados += 1
        print(f"   ✅ {nome_inter_uso}: {aliq_uso}%")
    
    # 4. ICMS Interestadual - Contribuinte Revenda
    nome_inter_revenda = f"ICMS {estado} - Interestadual Revenda"
    imposto_inter_revenda, criado = Imposto.objects.get_or_create(
        nome=nome_inter_revenda,
        defaults={
            'descricao': f'ICMS interestadual para revenda - {estado} (contribuinte)',
            'aliquota': aliq_revenda,
            'ativo': True
        }
    )
    if criado:
        impostos_criados += 1
        print(f"   ✅ {nome_inter_revenda}: {aliq_revenda}%")
    
    # 5. ICMS Não Contribuinte
    nome_nao_contrib = f"ICMS {estado} - Não Contribuinte"
    imposto_nao_contrib, criado = Imposto.objects.get_or_create(
        nome=nome_nao_contrib,
        defaults={
            'descricao': f'ICMS para não contribuinte - {estado}',
            'aliquota': aliq_nao_contrib,
            'ativo': True
        }
    )
    if criado:
        impostos_criados += 1
        print(f"   ✅ {nome_nao_contrib}: {aliq_nao_contrib}%")
    
    # 6. DIFAL (Diferencial de Alíquota)
    nome_difal = f"DIFAL {estado}"
    imposto_difal, criado = Imposto.objects.get_or_create(
        nome=nome_difal,
        defaults={
            'descricao': f'Diferencial de Alíquota para {estado}',
            'aliquota': difal,
            'ativo': True
        }
    )
    if criado:
        impostos_criados += 1
        print(f"   ✅ {nome_difal}: {difal}%")

print(f"\n📊 RESUMO DA IMPORTAÇÃO:")
print(f"   ✅ {impostos_criados} novos impostos criados")
print(f"   📋 Total de impostos ICMS no sistema: {Imposto.objects.filter(nome__icontains='ICMS').count()}")
print(f"   📋 Total de DIFAL no sistema: {Imposto.objects.filter(nome__icontains='DIFAL').count()}")

# Mostrar alguns exemplos
print(f"\n📋 EXEMPLOS DE IMPOSTOS CRIADOS:")
exemplos = Imposto.objects.filter(nome__icontains="ICMS SP").order_by('nome')
for imposto in exemplos:
    status = "🟢" if imposto.ativo else "🔴"
    print(f"   {status} {imposto.nome}: {imposto.aliquota}%")

print(f"\n🎉 Importação de ICMS por estado concluída!")
print("=" * 60)
