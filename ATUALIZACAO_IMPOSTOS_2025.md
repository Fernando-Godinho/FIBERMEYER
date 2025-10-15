# 📊 ATUALIZAÇÃO DOS IMPOSTOS ICMS - 2025

## ✅ RESUMO DA ATUALIZAÇÃO

### 📈 Dados Importados
- **Total de impostos adicionados**: 106 novos registros
- **Estados cobertos**: 27 (todos os estados brasileiros + DF)
- **Modalidades por estado**: 4 (exceto RS que tem 2)

### 🏛️ Modalidades Cadastradas

#### Para cada estado foram criados os seguintes impostos:

1. **ICMS [ESTADO] - Contribuinte Industrialização**
   - Alíquota na NF: 7% ou 12% (conforme tabela)
   
2. **ICMS [ESTADO] - Contribuinte Uso/Consumo**  
   - Alíquota de cálculo: 7.2% ou 12.4% (conforme tabela)
   
3. **ICMS [ESTADO] - Não Contribuinte Industrialização**
   - Alíquotas variadas de 17.55% a 22.72%
   
4. **ICMS [ESTADO] - Não Contribuinte Uso/Consumo**
   - Alíquota de cálculo: 7.2% ou 12.4% (conforme tabela)

### 🏆 Destaques das Alíquotas

#### Estados com maiores alíquotas para não contribuintes:
- **MA (Maranhão)**: 22.72%
- **PI (Piauí)**: 21.68%
- **BA (Bahia)**: 21.17%
- **PE (Pernambuco)**: 21.17%
- **AM (Amazonas)**: 20.65%

#### Estados com alíquota de 12% para contribuintes:
- MG, PR, RJ, RS, SC, SP

#### Estados com alíquota de 7% para contribuintes:
- AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MT, MS, PA, PB, PE, PI, RN, RO, RR, SE, TO

### 📋 Estrutura dos Dados

Cada imposto foi cadastrado com:
- **Nome**: Identificação única (ex: "ICMS SP - Contribuinte Industrialização")
- **Descrição**: Explicação detalhada do imposto
- **Alíquota**: Percentual conforme tabela fornecida
- **Status**: Todos ativos

### 🎯 Caso Especial - Rio Grande do Sul (RS)

O RS não possui valores para "Uso/Consumo" na tabela original, portanto foram criados apenas:
- ICMS RS - Contribuinte Industrialização: 12%
- ICMS RS - Não Contribuinte Industrialização: 17.55%

### 🔧 Arquivos Modificados

1. **main/templates/main/impostos.html**
   - Atualizado array `icmsData2024` com dados de 2025

2. **atualizar_impostos_2025.py** (novo)
   - Script para importar dados na base

3. **verificar_impostos_2025.py** (novo)
   - Script de verificação e relatório

### 📊 Como Usar

#### Na Interface Web:
1. Acesse a página de Impostos
2. Clique em "Importar ICMS 2024" 
3. Os dados serão importados via JavaScript

#### Via Script Python:
```bash
python atualizar_impostos_2025.py
```

### ✅ Verificação da Importação

Para verificar se tudo foi importado corretamente:
```bash
python verificar_impostos_2025.py
```

### 🎉 Status Final

- ✅ 106 impostos ICMS criados com sucesso
- ✅ Todos os 27 estados cobertos
- ✅ Todas as modalidades necessárias cadastradas
- ✅ Dados prontos para uso no sistema de orçamentos

Os impostos agora estão disponíveis para seleção automática nos orçamentos, baseados na UF do cliente e tipo de contribuinte.