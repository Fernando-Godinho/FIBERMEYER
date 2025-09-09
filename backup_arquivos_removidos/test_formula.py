#!/usr/bin/env python
"""
Teste da fórmula do véu
"""

# Simular o que acontece na substituição de parâmetros
formula_original = "veu * (1 + perda_veu / 100)"

parametros = {
    'veu': '0.3',
    'perda_veu': '3'
}

print(f"Fórmula original: {formula_original}")

# Simular a substituição que acontece no views.py
formula_substituida = formula_original
for param_nome, param_valor in parametros.items():
    formula_substituida = formula_substituida.replace(param_nome, str(param_valor))

print(f"Fórmula substituída: {formula_substituida}")

# Testar se a fórmula funciona
try:
    resultado = eval(formula_substituida)
    print(f"Resultado: {resultado}")
except Exception as e:
    print(f"ERRO: {e}")
    
# Testar uma versão que deveria funcionar
formula_correta = "0.3 * (1 + 3 / 100)"
print(f"Fórmula correta manual: {formula_correta}")
print(f"Resultado da fórmula correta: {eval(formula_correta)}")
