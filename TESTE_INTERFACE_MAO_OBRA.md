## 🧪 TESTE DA NOVA FÓRMULA DE MÃO DE OBRA NA INTERFACE WEB

### Passos para Testar:

1. **Acessar**: http://127.0.0.1:8000/mp/
2. **Selecionar**: "Novo Perfil" no dropdown
3. **Preencher campos obrigatórios**:
   - Nome do perfil: `Teste Nova Fórmula`
   - Roving 4400 KG: `0.5`
   - Manta 300 KG: `0.3` 
   - Véu KG: `0.1`
   - Peso do metro (kg): `1.2`
   - **N° matrizes**: `2`
   - **N° máquinas**: `1`
   - **Metros produzidos/h**: `12`
   - Perda %: `5`

4. **Clicar**: "Calcular"

### Resultado Esperado:

Na tabela "Componentes Calculados" deve aparecer:
- Todos os componentes normais (Roving, Manta, Véu, Resina, etc.)
- **NOVO**: `Mão de Obra - Pultrusão` com valor ~R$ 5,49

### Cálculo Esperado:
```
Parâmetros: velocidade=12, matrizes=2, máquinas=1
Fórmula: ((9.976.258 / 3) * 1) / (12 * 2 * 24 * 21 * 0.5)
Numerador: 3.325.419,33
Denominador: 6.048
Resultado: 549,84 centavos = R$ 5,49
```

### Debug no Console:
Abra DevTools (F12) → Console para ver:
```
=== CÁLCULO MÃO DE OBRA (NOVA FÓRMULA) ===
Parâmetros: velocidade=12, matrizes=2, máquinas=1
Numerador: (9976258 / 3) * 1 = 3325419.33
Denominador: 12 * 2 * 24 * 21 * 0.5 = 6048
Resultado: 3325419.33 / 6048 = 549.83785273
Custo final: 549 centavos = R$ 5.49
```

### ✅ Se aparecer o componente de mão de obra na tabela = SUCESSO!
