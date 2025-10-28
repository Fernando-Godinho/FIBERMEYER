from rest_framework import serializers
from .models import (
    MP_Produtos, Orcamento, OrcamentoItem, OrcamentoParametro, 
    OrcamentoHistorico, ProdutoComponente,
    ProdutoTemplate, ProdutoParametrizado, ParametroFormula,
    Imposto, MaoObra
)
from datetime import datetime

class ImpostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imposto
        fields = ['id', 'nome', 'descricao', 'aliquota', 'ativo']


class MaoObraSerializer(serializers.ModelSerializer):
    valor_real = serializers.SerializerMethodField()
    
    class Meta:
        model = MaoObra
        fields = ['id', 'nome', 'descricao', 'valor_centavos', 'valor_real', 'unidade', 'ativo']
    
    def get_valor_real(self, obj):
        return obj.valor_centavos / 100 if obj.valor_centavos else 0

class MP_ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MP_Produtos
        fields = ['id', 'descricao', 'custo_centavos', 'peso_und', 'unidade', 'referencia', 'data_revisao', 'is_composto', 'tipo_produto', 'categoria', 'subcategoria', 'descricao_tecnica']

class ProdutoComponenteSerializer(serializers.ModelSerializer):
    produto_componente_nome = serializers.CharField(source='produto_componente.descricao', read_only=True)
    produto_componente_unidade = serializers.CharField(source='produto_componente.unidade', read_only=True)
    
    class Meta:
        model = ProdutoComponente
        fields = ['id', 'produto_principal', 'produto_componente', 'produto_componente_nome', 'produto_componente_unidade', 'quantidade', 'observacao']

class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = '__all__'

class OrcamentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoItem
        fields = '__all__'

class OrcamentoParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoParametro
        fields = '__all__'

class OrcamentoHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoHistorico
        fields = '__all__'

class ProdutoTemplateSerializer(serializers.ModelSerializer):
    produto_base = MP_ProdutosSerializer(read_only=True)
    
    class Meta:
        model = ProdutoTemplate
        fields = ['id', 'produto_base', 'parametros_obrigatorios', 'parametros_opcionais', 'formula_principal']

class ProdutoParametrizadoSerializer(serializers.ModelSerializer):
    template = ProdutoTemplateSerializer(read_only=True)
    
    class Meta:
        model = ProdutoParametrizado
        fields = ['id', 'template', 'parametros', 'custo_calculado', 'data_calculo', 'observacoes']

class ParametroFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametroFormula
        fields = '__all__'
