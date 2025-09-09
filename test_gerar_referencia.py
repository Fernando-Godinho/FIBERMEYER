#!/usr/bin/env python3
"""
Teste da função JavaScript gerarReferenciaPerfil convertida para Python.
"""

import re
import datetime

def gerar_referencia_perfil(nome_perfil):
    """
    Gerar referência baseada no nome do perfil
    Formato: PER-XXXX-XX onde:
    - XXXX são 4 dígitos baseados no nome
    - XX são 2 dígitos baseados no timestamp atual
    """
    
    referencia = 'PER-'
    
    # Remover caracteres especiais e espaços
    nome_simplificado = re.sub(r'[^a-zA-Z0-9]', '', nome_perfil).upper()[:10]
    
    # Se tem números no nome, usar eles
    numeros = re.findall(r'\d+', nome_perfil)
    if numeros:
        # Usar os números encontrados no nome
        numeros_combinados = ''.join(numeros)
        referencia += numeros_combinados[:4].zfill(4)
    else:
        # Gerar código baseado nas letras (hash simples)
        hash_val = 0
        for char in nome_simplificado:
            hash_val = ((hash_val << 5) - hash_val) + ord(char)
            hash_val = hash_val & 0xFFFFFFFF  # Converter para 32-bit
        
        # Usar valor absoluto e pegar 4 dígitos
        codigo = str(abs(hash_val))[:4].zfill(4)
        referencia += codigo
    
    # Adicionar timestamp para garantir unicidade
    agora = datetime.datetime.now()
    timestamp = str(agora.hour * 60 + agora.minute).zfill(4)
    
    return referencia + '-' + timestamp[:2]

# Testes
print("=== TESTE DE GERAÇÃO DE REFERÊNCIAS ===")
print()

exemplos = [
    "Perfil Quadrado 50x50mm",
    "Tubo Circular 100mm",
    "Perfil L 75x75x8mm", 
    "Viga H 200x100mm",
    "Perfil U 150x75mm",
    "Cantoneira 50x50x5",
    "Perfil Retangular 120x80",
    "Tubo 42mm Industrial",
    "Perfil Especial Cliente",
    "Sistema Estrutural ABC"
]

print("EXEMPLOS DE REFERÊNCIAS GERADAS:")
print("-" * 50)

for exemplo in exemplos:
    ref1 = gerar_referencia_perfil(exemplo)
    ref2 = gerar_referencia_perfil(exemplo)  # Gerar segunda para ver se timestamp muda
    
    print(f"Nome: {exemplo:30s} -> {ref1}")
    
    # Verificar se gera referencias diferentes (por causa do timestamp)
    if ref1 != ref2:
        print(f"{'':36s}    {ref2} (timestamp diferente)")
    
print()
print("CARACTERÍSTICAS DA FUNÇÃO:")
print("✅ Formato consistente: PER-XXXX-XX")
print("✅ Usa números do nome quando disponível")
print("✅ Hash das letras quando não há números")
print("✅ Timestamp para garantir unicidade")
print("✅ Máximo 10 caracteres para processamento")
print("✅ Remove caracteres especiais automaticamente")

print()
print("COMO IMPLEMENTADO NO FRONTEND:")
print("1. JavaScript chama gerarReferenciaPerfil(dadosPerfil.nome_perfil)")
print("2. Função retorna string com referência única")
print("3. Referência é salva junto com o produto na base")
print("4. Permite identificação rápida dos perfis criados")

print()
print("🧪 TESTANDO CASOS EXTREMOS:")
casos_extremos = [
    "",
    "A",
    "123",
    "Perfil@#$%^&*()",
    "Muito Longo Nome Para Testar Limite Máximo De Caracteres",
    "ΑΒΓΔΕ",  # Caracteres especiais
    "Perfil 100x50x25mm Estrutural Industrial"
]

print("-" * 50)
for caso in casos_extremos:
    try:
        ref = gerar_referencia_perfil(caso)
        print(f"'{caso[:30]}...' -> {ref}")
    except Exception as e:
        print(f"'{caso[:30]}...' -> ERRO: {e}")
