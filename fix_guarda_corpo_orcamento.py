#!/usr/bin/env python3
"""
Script para corrigir os produtos do Guarda Corpo Horizontal no orçamento
"""

import re

# Ler o arquivo
with open(r'c:\Users\ferna\OneDrive\Área de Trabalho\FIBERMEYER\main\templates\main\orcamento.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Substitutições específicas para Guarda Corpo Horizontal no orçamento
# Encontrar e substituir apenas na seção do Guarda Corpo Horizontal

# Pattern para encontrar a função calcularGuardaCorpoHorizontalOrcamento
horizontal_pattern = r'(function calcularGuardaCorpoHorizontalOrcamento\(\)[\s\S]*?)(tubo.*quadrado.*includes\(tipoTuboQuad\.replace\(\'x\', \'x\'\)\))'
replacement_tubo = r'\1tubo.*quadrado.*includes(\'50\')'

content = re.sub(horizontal_pattern, replacement_tubo, content)

# Substituir sapata
horizontal_sapata_pattern = r'(function calcularGuardaCorpoHorizontalOrcamento\(\)[\s\S]*?sapata.*includes\(tipoSapata\.toLowerCase\(\)\))'
replacement_sapata = lambda m: m.group(0).replace("includes(tipoSapata.toLowerCase())", "includes('inox')")

content = re.sub(r'(function calcularGuardaCorpoHorizontalOrcamento\(\)[\s\S]*?)(sapata.*includes\(tipoSapata\.toLowerCase\(\)\))', 
                r'\1sapata.*includes(\'inox\')', content)

# Substituir parafusos M8 por M6
content = re.sub(r'(function calcularGuardaCorpoHorizontalOrcamento\(\)[\s\S]*?paraf.*includes\(\'m8x70\'\))', 
                lambda m: m.group(0).replace("includes('m8x70')", "includes('m6x70')"), content)

content = re.sub(r'(function calcularGuardaCorpoHorizontalOrcamento\(\)[\s\S]*?porca.*includes\(\'m8\'\))', 
                lambda m: m.group(0).replace("includes('m8')", "includes('m6')"), content)

content = re.sub(r'(function calcularGuardaCorpoHorizontalOrcamento\(\)[\s\S]*?paraf.*aa.*includes\(\'m6x25\'\))', 
                lambda m: m.group(0).replace("includes('m6x25')", "includes('aa')"), content)

# Salvar o arquivo
with open(r'c:\Users\ferna\OneDrive\Área de Trabalho\FIBERMEYER\main\templates\main\orcamento.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo orcamento.html atualizado com sucesso!")
print("   - Tubo quadrado: agora busca por '50mm'")
print("   - Sapata: agora busca por 'inox'") 
print("   - Parafusos: agora busca por M6X70, porca M6, parafuso AA")