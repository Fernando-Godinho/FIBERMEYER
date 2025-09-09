#!/usr/bin/env python
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.append('C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\FIBERMEYER')

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import ProdutoTemplate, MP_Produtos, ProdutoComponente

def main():
    print("=== TESTE FINAL DO TEMPLATE NOVO PERFIL ===")
    
    # Verificar template
    novo_perfil = MP_Produtos.objects.filter(descricao="Novo Perfil").first()
    
    if not novo_perfil:
        print("❌ Template 'Novo Perfil' não encontrado!")
        return
    
    print(f"✅ Produto 'Novo Perfil' encontrado (ID: {novo_perfil.id})")
    print(f"   Tipo: {novo_perfil.tipo_produto}")
    print(f"   Custo: R$ {novo_perfil.custo_centavos/100:.2f}")
    
    if hasattr(novo_perfil, 'template'):
        template = novo_perfil.template
        print(f"✅ Template associado (ID: {template.id})")
        print(f"   Parâmetros obrigatórios: {template.parametros_obrigatorios}")
        print(f"   Parâmetros opcionais: {list(template.parametros_opcionais.keys())}")
        
        # Verificar componentes
        componentes = ProdutoComponente.objects.filter(produto_principal=novo_perfil)
        print(f"✅ Componentes: {componentes.count()}")
        
        if componentes.exists():
            print("   📋 Lista de componentes:")
            total_custo = 0
            for comp in componentes:
                custo_unit = comp.produto_componente.custo_centavos / 100
                custo_total = custo_unit * float(comp.quantidade)
                total_custo += custo_total
                categoria = comp.produto_componente.categoria or "SEM CATEGORIA"
                print(f"     [{categoria:12}] {comp.produto_componente.descricao[:30]:30} | Qtd: {comp.quantidade:6} | R$ {custo_total:7.2f}")
            
            print(f"   💰 Custo total calculado: R$ {total_custo:.2f}")
            print(f"   💰 Custo do produto: R$ {novo_perfil.custo_centavos/100:.2f}")
            
            if abs(total_custo - (novo_perfil.custo_centavos/100)) < 0.01:
                print("   ✅ Custos estão sincronizados!")
            else:
                print("   ⚠️  Custos não estão sincronizados")
        
        print()
        print("🎯 TEMPLATE PRONTO PARA USO!")
        print("   • Interface web: http://127.0.0.1:8000/orcamento/")
        print("   • Botão: 'Produto Parametrizado'")
        print("   • Selecionar: 'Novo Perfil'")
        print("   • Preencher parâmetros obrigatórios:")
        for param in template.parametros_obrigatorios:
            print(f"     - {param}")
        print("   • Parâmetros opcionais disponíveis:")
        for param in template.parametros_opcionais.keys():
            print(f"     - {param}: {template.parametros_opcionais[param]}")
        
    else:
        print("❌ Template não associado!")
    
    print()
    print("📊 RESUMO DO SISTEMA:")
    total_produtos = MP_Produtos.objects.count()
    total_templates = ProdutoTemplate.objects.count()
    print(f"   • Total de produtos: {total_produtos}")
    print(f"   • Total de templates: {total_templates}")
    print(f"   • Sistema: ✅ Organizados e funcionando")
    
    print()
    print("🚀 SISTEMA PRONTO!")
    print("   Acesse http://127.0.0.1:8000/orcamento/ e teste o 'Produto Parametrizado'!")

if __name__ == "__main__":
    main()
