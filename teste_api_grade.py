#!/usr/bin/env python
"""
Teste da função calcularGrade via API REST
Simula uma chamada AJAX para testar a lógica
"""

import requests
import json

def testar_api_produtos():
    """Testa se a API de produtos está funcionando"""
    print("=== TESTE DA API /api/produtos/ ===")
    
    try:
        response = requests.get('http://127.0.0.1:8000/api/produtos/')
        if response.status_code == 200:
            produtos = response.json()
            print(f"✅ API funcionando! {len(produtos)} produtos encontrados")
            
            # Verificar produtos específicos
            perfil_1328 = next((p for p in produtos if p['id'] == 1328), None)
            chaveta_1332 = next((p for p in produtos if p['id'] == 1332), None)
            cola_1183 = next((p for p in produtos if p['id'] == 1183), None)
            
            print(f"Perfil 1328: {'✅' if perfil_1328 else '❌'} {perfil_1328['descricao'] if perfil_1328 else 'Não encontrado'}")
            print(f"Chaveta 1332: {'✅' if chaveta_1332 else '❌'} {chaveta_1332['descricao'] if chaveta_1332 else 'Não encontrada'}")
            print(f"Cola 1183: {'✅' if cola_1183 else '❌'} {cola_1183['descricao'] if cola_1183 else 'Não encontrada'}")
            
            return True
        else:
            print(f"❌ Erro na API: Status {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor Django")
        print("Certifique-se de que o servidor está rodando em http://127.0.0.1:8000/")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def simular_calculo_javascript():
    """Simula o que acontece na função JavaScript"""
    print("\n=== SIMULAÇÃO DA LÓGICA JAVASCRIPT ===")
    
    # Dados que vêm do formulário (como na função JavaScript)
    dados = {
        'nome_grade': 'GRADE TESTE 40x40',
        'vao': 400.0,
        'comprimento': 1000.0,
        'eixo_i': 40.0,
        'perfil_id': 1328,
        'perda': 3.0,
        'tempo_proc': 1.5,
        'tempo_mtg': 0.5
    }
    
    print(f"1. Dados coletados: {dados}")
    
    # Buscar produtos (como faz o fetch na função JavaScript)
    try:
        response = requests.get('http://127.0.0.1:8000/api/produtos/')
        produtos = response.json()
        
        print(f"2. Produtos carregados: {len(produtos)} itens")
        
        # Encontrar perfil selecionado
        perfil_selecionado = next((p for p in produtos if p['id'] == dados['perfil_id']), None)
        if not perfil_selecionado:
            print(f"❌ Perfil ID {dados['perfil_id']} não encontrado!")
            return
        
        # Encontrar chaveta
        chaveta = next((p for p in produtos if p['id'] == 1332), None)
        if not chaveta:
            print("❌ Chaveta ID 1332 não encontrada!")
            return
            
        # Encontrar cola
        cola = next((p for p in produtos if p['id'] == 1183), None)
        if not cola:
            print("❌ Cola ID 1183 não encontrada!")
            return
        
        print(f"3. Produtos encontrados:")
        print(f"   Perfil: {perfil_selecionado['descricao']} - R$ {perfil_selecionado['custo_centavos']/100:.2f}")
        print(f"   Chaveta: {chaveta['descricao']} - R$ {chaveta['custo_centavos']/100:.2f}")
        print(f"   Cola: {cola['descricao']} - R$ {cola['custo_centavos']/100:.2f}")
        
        # Aplicar fórmula (exatamente como no JavaScript)
        metros_lineares_por_m2 = (dados['comprimento'] / dados['eixo_i']) * (dados['vao'] / 1000)
        print(f"4. Fórmula aplicada:")
        print(f"   ({dados['comprimento']}/{dados['eixo_i']}) * ({dados['vao']}/1000) = {metros_lineares_por_m2:.4f} m/m²")
        
        # Calcular custos (CONVERSÃO CORRETA DOS TIPOS)
        peso_perfil_kg = metros_lineares_por_m2 * float(perfil_selecionado['peso_und'])
        custo_perfil_centavos = metros_lineares_por_m2 * perfil_selecionado['custo_centavos']
        
        quantidade_chaveta = (dados['vao'] / 150) * 2
        peso_chaveta = quantidade_chaveta * float(chaveta['peso_und'])
        custo_chaveta = quantidade_chaveta * chaveta['custo_centavos']
        
        quantidade_cola = 0.06
        peso_cola = quantidade_cola * float(cola['peso_und'])
        custo_cola = quantidade_cola * cola['custo_centavos']
        
        print(f"5. Cálculos de componentes:")
        print(f"   Perfil: {peso_perfil_kg:.3f} kg/m² - R$ {custo_perfil_centavos/100:.2f}/m²")
        print(f"   Chaveta: {peso_chaveta:.3f} kg/m² - R$ {custo_chaveta/100:.2f}/m²")
        print(f"   Cola: {peso_cola:.3f} kg/m² - R$ {custo_cola/100:.2f}/m²")
        
        # Aplicar perda
        fator_perda = 1 + (dados['perda'] / 100)
        peso_total_kg = (peso_perfil_kg + peso_chaveta + peso_cola) * fator_perda
        
        # Mão de obra
        valor_hora_mo = 65.79
        tempo_total = dados['tempo_proc'] + dados['tempo_mtg']
        custo_mao_obra_total = tempo_total * valor_hora_mo * 100
        
        custo_total_centavos = (custo_perfil_centavos + custo_chaveta + custo_cola) * fator_perda + custo_mao_obra_total
        
        print(f"6. Resultado final:")
        print(f"   Peso total: {peso_total_kg:.3f} kg/m²")
        print(f"   Custo total: R$ {custo_total_centavos/100:.2f}/m²")
        print(f"   ✅ Cálculo simulado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na simulação: {e}")
        return False

if __name__ == "__main__":
    # Teste 1: Verificar se API está funcionando
    api_ok = testar_api_produtos()
    
    if api_ok:
        # Teste 2: Simular lógica JavaScript
        simular_calculo_javascript()
    else:
        print("\n❌ Não é possível continuar sem a API funcionando")
        print("Verifique se o servidor Django está rodando")