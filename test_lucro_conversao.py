#!/usr/bin/env python
"""
Teste rápido para verificar conversão de lucro
"""

def safe_float(value, default=0.0):
    """Converte um valor para float de forma segura"""
    try:
        if value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

# Testes
test_values = ['22.5', '22,5', 22.5, '23', 23]

print("=== TESTE DE CONVERSÃO DE LUCRO ===")
for value in test_values:
    result = safe_float(value)
    print(f"Valor: {repr(value)} -> Resultado: {result}")

# Teste específico do problema
lucro_from_form = '22.5'  # como vem do formulário
lucro_default = 22.5  # valor padrão
lucro_final = lucro_from_form or lucro_default

print(f"\nTeste específico:")
print(f"Do formulário: '{lucro_from_form}' -> {safe_float(lucro_final)}")

# Teste com None/vazio
lucro_empty = ''
lucro_final_empty = lucro_empty or 22.5
print(f"Vazio: '{lucro_empty}' -> {safe_float(lucro_final_empty)}")