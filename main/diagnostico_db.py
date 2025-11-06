"""
Endpoint de diagnóstico para verificar conexão do banco de dados
Adicione ao urls.py:
    path('diagnostico-db/', diagnostico_db, name='diagnostico_db'),
"""

from django.http import JsonResponse
from django.db import connection
from main.models import MP_Produtos, Orcamento, Imposto

def diagnostico_db(request):
    """Mostra informações sobre a conexão do banco de dados"""
    
    db_settings = connection.settings_dict
    
    # Contar registros
    total_produtos = MP_Produtos.objects.count()
    total_orcamentos = Orcamento.objects.count()
    total_impostos = Imposto.objects.count()
    
    # Pegar últimos produtos
    ultimos_produtos = list(MP_Produtos.objects.order_by('-id')[:5].values('id', 'descricao'))
    
    diagnostico = {
        'banco': {
            'engine': db_settings['ENGINE'],
            'nome': str(db_settings['NAME']),  # Converter PosixPath para string
            'host': db_settings.get('HOST', 'N/A'),
            'porta': db_settings.get('PORT', 'N/A'),
            'usuario': db_settings.get('USER', 'N/A'),
        },
        'dados': {
            'total_produtos': total_produtos,
            'total_orcamentos': total_orcamentos,
            'total_impostos': total_impostos,
        },
        'ultimos_produtos': ultimos_produtos,
        'status': 'Neon Online' if 'neon.tech' in db_settings.get('HOST', '') else 'Banco Local',
    }
    
    return JsonResponse(diagnostico, json_dumps_params={'indent': 2})
