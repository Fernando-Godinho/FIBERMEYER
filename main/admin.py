from django.contrib import admin
from .models import (
    MP_Produtos, ProdutoComponente, Orcamento, OrcamentoItem, 
    OrcamentoParametro, OrcamentoHistorico,
    ProdutoTemplate, ProdutoParametrizado, ParametroFormula,
    Imposto, MaoObra
)

@admin.register(Imposto)
class ImpostoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'aliquota', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(MaoObra)
class MaoObraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_real', 'unidade', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)

class ProdutoComponenteInline(admin.TabularInline):
    model = ProdutoComponente
    extra = 1
    fk_name = 'produto_principal'

@admin.register(MP_Produtos)
class MP_ProdutosAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'tipo_produto_icon', 'categoria', 'custo_reais', 'peso_und', 'unidade', 'referencia', 'produtos_dependentes_count')
    search_fields = ('descricao', 'referencia', 'categoria', 'subcategoria')
    list_filter = ('tipo_produto', 'categoria', 'subcategoria', 'unidade')
    inlines = [ProdutoComponenteInline]
    actions = ['atualizar_dependencias_acao', 'converter_para_composto', 'converter_para_parametrizado']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('descricao', 'referencia', 'tipo_produto')
        }),
        ('Categorização', {
            'fields': ('categoria', 'subcategoria'),
            'description': 'Use para organizar produtos: Resinas, Fibras, Cargas Minerais, etc.'
        }),
        ('Custos e Medidas', {
            'fields': ('custo_centavos', 'peso_und', 'unidade', 'data_revisao')
        }),
    )

    def tipo_produto_icon(self, obj):
        icons = {
            'simples': '🧪 Matéria-Prima',
            'composto': '🏗️ Composto', 
            'parametrizado': '📐 Parametrizado'
        }
        return icons.get(obj.tipo_produto, '📦 Indefinido')
    tipo_produto_icon.short_description = "Tipo"

    def custo_reais(self, obj):
        return f"R$ {obj.custo_centavos/100:.2f}"
    custo_reais.short_description = "Custo (R$)"
    
    def produtos_dependentes_count(self, obj):
        count = obj.get_produtos_dependentes().count()
        if count > 0:
            return f"🔗 {count} produto(s)"
        return "-"
    produtos_dependentes_count.short_description = "Dependências"
    
    def converter_para_composto(self, request, queryset):
        """Converte produtos simples para compostos"""
        count = 0
        for produto in queryset.filter(tipo_produto='simples'):
            produto.tipo_produto = 'composto'
            produto.save()
            count += 1
        self.message_user(request, f"{count} produto(s) convertido(s) para composto.")
    converter_para_composto.short_description = "Converter para Produto Composto"
    
    def converter_para_parametrizado(self, request, queryset):
        """Converte produtos para parametrizados"""
        count = 0
        for produto in queryset:
            produto.tipo_produto = 'parametrizado'
            produto.save()
            count += 1
        self.message_user(request, f"{count} produto(s) convertido(s) para parametrizado.")
    converter_para_parametrizado.short_description = "Converter para Produto Parametrizado"
    
    def atualizar_dependencias_acao(self, request, queryset):
        """Ação para forçar atualização das dependências"""
        total_atualizados = 0
        for produto in queryset:
            dependentes = produto.get_produtos_dependentes()
            for dep in dependentes:
                dep.recalcular_custo_composto()
                total_atualizados += 1
        
        self.message_user(request, f"Dependências atualizadas para {total_atualizados} produto(s).")
    atualizar_dependencias_acao.short_description = "Recalcular dependências"

@admin.register(ProdutoComponente)
class ProdutoComponenteAdmin(admin.ModelAdmin):
    list_display = ('produto_principal', 'produto_componente', 'quantidade', 'observacao')
    list_filter = ('produto_principal', 'produto_componente')

@admin.register(ProdutoTemplate)
class ProdutoTemplateAdmin(admin.ModelAdmin):
    list_display = ['produto_base', 'parametros_obrigatorios']
    search_fields = ['produto_base__descricao']

@admin.register(ProdutoParametrizado)
class ProdutoParametrizadoAdmin(admin.ModelAdmin):
    list_display = ['template', 'custo_calculado', 'data_calculo']
    list_filter = ['template', 'data_calculo']

@admin.register(ParametroFormula)
class ParametroFormulaAdmin(admin.ModelAdmin):
    list_display = ['template', 'nome_parametro', 'descricao']
    list_filter = ['template']

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ['numero_orcamento', 'cliente', 'status', 'total_liquido', 'criado_em']
    list_filter = ['status', 'uf']
    search_fields = ['numero_orcamento', 'cliente']

@admin.register(OrcamentoItem)
class OrcamentoItemAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'tipo_item', 'descricao', 'quantidade', 'valor_total']
    list_filter = ['tipo_item']

@admin.register(OrcamentoParametro)
class OrcamentoParametroAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'chave', 'valor']

@admin.register(OrcamentoHistorico)
class OrcamentoHistoricoAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'acao', 'usuario', 'data_acao']
    list_filter = ['acao']
