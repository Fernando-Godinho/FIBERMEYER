from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import views_pdf


router = DefaultRouter()
router.register(r'produtos', views.MP_ProdutosViewSet)
router.register(r'orcamentos', views.OrcamentoViewSet)
router.register(r'componentes', views.ProdutoComponenteViewSet)
router.register(r'templates', views.ProdutoTemplateViewSet)
router.register(r'produtos-parametrizados', views.ProdutoParametrizadoViewSet)
router.register(r'parametro-formulas', views.ParametroFormulaViewSet)
router.register(r'impostos', views.ImpostoViewSet)
router.register(r'mao-obra', views.MaoObraViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('mp/', views.mp, name='mp'),
    path('mao_de_obra/', views.mao_de_obra, name='mao_de_obra'),
    path('about/', views.about, name='about'),
    path('orcamento/', views.orcamentos, name='orcamentos'),
    path('orcamento_form/', views.orcamento_form, name='orcamento_form'),
    path('orcamento/<int:orcamento_id>/', views.orcamento, name='orcamento'),
    path('calcular-produto/', views.calcular_produto_parametrizado, name='calcular_produto'),
    path('impostos/', views.impostos, name='impostos'),
    path('api/calcular-produto-parametrizado/', views.calcular_produto_parametrizado, name='calcular_produto_parametrizado_api'),
    path('api/tipos-resina/', views.tipos_resina, name='tipos_resina'),
    path('api/mao-obra/', views.mao_obra_lista, name='mao_obra_lista'),
    path('orcamento/<int:orcamento_id>/pdf/', views_pdf.gerar_pdf_orcamento, name='gerar_pdf_orcamento'),
    path('orcamento/<int:orcamento_id>/preview/', views_pdf.preview_pdf_orcamento, name='preview_pdf_orcamento'),
    path('api/', include(router.urls)),
]
