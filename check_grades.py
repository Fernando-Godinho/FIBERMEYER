#!/usr/bin/env python
"""
Verificação simples das grades
"""

import os, sys, django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibermeyer_project.settings')
django.setup()

from main.models import MP_Produtos, ProdutoComponente
from django.db import models
import json

grades = MP_Produtos.objects.filter(
    models.Q(descricao__icontains='grade') | 
    models.Q(categoria__icontains='grade')
).order_by('-id')

print(f'=== GRADES NO SISTEMA ({grades.count()}) ===')

for grade in grades:
    componentes = ProdutoComponente.objects.filter(produto_principal=grade)
    tem_mo = any('mão de obra' in c.produto_componente.descricao.lower() or 'processamento' in c.produto_componente.descricao.lower() for c in componentes)
    mo_status = "✅" if tem_mo else "❌"
    
    print(f'ID {grade.id}: {grade.descricao[:40]}')
    print(f'  Tipo: {grade.tipo_produto} | Custo: R$ {grade.custo_centavos/100:.2f}')
    print(f'  Componentes: {componentes.count()} | Mão Obra: {mo_status}')
    print()
