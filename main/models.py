from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
import json
from decimal import Decimal

class Imposto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    aliquota = models.DecimalField(max_digits=5, decimal_places=2, help_text="% sobre o valor")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.aliquota}%)"


class MaoObra(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, help_text="Descrição detalhada da mão de obra")
    valor_centavos = models.BigIntegerField(help_text="Valor em centavos para maior precisão")
    unidade = models.CharField(max_length=10, default='H', help_text="Unidade de medida (H=Hora, D=Dia, etc)")
    ativo = models.BooleanField(default=True)

    @property
    def valor_real(self):
        return self.valor_centavos / 100

    @valor_real.setter
    def valor_real(self, value):
        self.valor_centavos = int(float(value) * 100)

    def __str__(self):
        return f"{self.nome} - R$ {self.valor_real:.2f}/{self.unidade}"

    class Meta:
        verbose_name = "Mão de Obra"
        verbose_name_plural = "Mão de Obra"


# Choices para tipo de produto
TIPO_PRODUTO_CHOICES = [
    ('simples', 'Matéria-Prima Simples'),
    ('composto', 'Produto Composto'),
    ('parametrizado', 'Template Parametrizado'),
]

class MP_Produtos(models.Model):
    """Tabela principal de produtos com suporte a hierarquia"""
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    unidade = models.CharField(max_length=10, default='UN')
    custo_centavos = models.BigIntegerField(default=0, help_text="Custo em centavos para precisão")
    peso_und = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, help_text="Peso por unidade em kg")
    referencia = models.CharField(max_length=100, blank=True, null=True)
    data_revisao = models.DateTimeField(blank=True, null=True)
    
    # Estrutura hierárquica de produtos
    tipo_produto = models.CharField(
        max_length=15, 
        choices=TIPO_PRODUTO_CHOICES, 
        default='simples',
        help_text="Tipo do produto na hierarquia"
    )
    
    # Campo compatível com código existente
    is_composto = models.BooleanField(default=False, help_text="Calculado automaticamente baseado no tipo")
    
    # Metadados para categorização
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Resinas, Fibras, Cargas Minerais")
    subcategoria = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Poliéster, Isoftálica, Epóxi")

    def save(self, *args, **kwargs):
        # Sincronizar is_composto com tipo_produto para compatibilidade
        self.is_composto = self.tipo_produto in ['composto', 'parametrizado']
        super().save(*args, **kwargs)

    def __str__(self):
        tipo_icon = {
            'simples': '🧪',
            'composto': '🏗️',
            'parametrizado': '📐'
        }
        icon = tipo_icon.get(self.tipo_produto, '📦')
        return f"{icon} {self.descricao} ({self.referencia or 'N/A'})"

    def get_custo_total(self):
        """
        Calcula o custo total baseado no tipo de produto:
        - Simples: retorna o custo direto
        - Composto/Parametrizado: soma dos componentes
        """
        if self.tipo_produto == 'simples':
            return self.custo_centavos
        elif self.tipo_produto in ['composto', 'parametrizado']:
            total_centavos = 0
            for componente in self.componentes.all():
                total_centavos += componente.produto_componente.custo_centavos * float(componente.quantidade)
            return int(total_centavos)
        return self.custo_centavos

    def get_peso_total(self):
        """
        Calcula o peso total baseado no tipo de produto:
        - Simples: retorna o peso direto
        - Composto/Parametrizado: soma ponderada dos componentes
        """
        if self.tipo_produto == 'simples':
            return float(self.peso_und)
        elif self.tipo_produto in ['composto', 'parametrizado']:
            peso_total = 0
            for componente in self.componentes.all():
                peso_total += float(componente.produto_componente.peso_und) * float(componente.quantidade)
            return peso_total
        return float(self.peso_und)

    def recalcular_custo_composto(self):
        """
        Recalcula o custo para produtos compostos e parametrizados
        baseado nos custos atuais dos componentes
        """
        if self.tipo_produto in ['composto', 'parametrizado']:
            custo_total_centavos = 0
            for componente in self.componentes.all():
                custo_componente = componente.produto_componente.custo_centavos * float(componente.quantidade)
                custo_total_centavos += custo_componente
            
            # Atualizar o custo sem disparar signals recursivos
            MP_Produtos.objects.filter(id=self.id).update(custo_centavos=int(custo_total_centavos))
            return int(custo_total_centavos)
        return self.custo_centavos

    def get_produtos_dependentes(self):
        """
        Retorna produtos compostos e parametrizados que dependem deste produto
        """
        return MP_Produtos.objects.filter(
            componentes__produto_componente=self,
            tipo_produto__in=['composto', 'parametrizado']
        ).distinct()

    def get_hierarquia_dependencias(self, nivel=0, visitados=None):
        """
        Retorna a hierarquia completa de dependências deste produto
        """
        if visitados is None:
            visitados = set()
        
        if self.id in visitados:
            return []
        
        visitados.add(self.id)
        dependencias = []
        
        for dependente in self.get_produtos_dependentes():
            dependencias.append({
                'produto': dependente,
                'nivel': nivel,
                'filhos': dependente.get_hierarquia_dependencias(nivel + 1, visitados.copy())
            })
        
        return dependencias

    def is_materia_prima_basica(self):
        """Verifica se é uma matéria-prima básica (produto simples)"""
        return self.tipo_produto == 'simples'

    def is_produto_composto(self):
        """Verifica se é um produto composto"""
        return self.tipo_produto == 'composto'

    def is_produto_parametrizado(self):
        """Verifica se é um produto parametrizado (template)"""
        return self.tipo_produto == 'parametrizado'

    def atualizar_dependencias(self):
        """Atualiza todos os produtos que dependem deste produto"""
        produtos_dependentes = self.get_produtos_dependentes()
        for produto in produtos_dependentes:
            produto.recalcular_custo_composto()
            # Propagar recursivamente para produtos que dependem dos dependentes
            produto.atualizar_dependencias()


class ProdutoComponente(models.Model):
    """Modelo para componentes de produtos compostos"""
    produto_principal = models.ForeignKey(MP_Produtos, on_delete=models.CASCADE, related_name='componentes')
    produto_componente = models.ForeignKey(MP_Produtos, on_delete=models.CASCADE, related_name='usado_em')
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    observacao = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('produto_principal', 'produto_componente')

    def __str__(self):
        return f"{self.produto_principal.descricao} -> {self.quantidade} {self.produto_componente.unidade} de {self.produto_componente.descricao}"


# Status choices para orçamento
ORCAMENTO_STATUS_CHOICES = [
    ('Rascunho', 'Rascunho'),
    ('Enviado', 'Enviado'),
    ('Ajuste', 'Ajuste'),
    ('Aprovado', 'Aprovado'),
    ('Rejeitado', 'Rejeitado'),
    ('Convertido', 'Convertido'),
]

# Tipo de item
ITEM_TIPO_CHOICES = [
    ('Produto', 'Produto'),
    ('Serviço', 'Serviço'),
    ('Parametrizado', 'Produto Parametrizado'),
]

# Choices para Frete
FRETE_CHOICES = [
    ('CIF', 'CIF - ENTREGA NAS DEPENDÊNCIAS DO CLIENTE'),
    ('FOB', 'FOB'),
]

# Choices para Instalação
INSTALACAO_CHOICES = [
    ('NAO_INCLUSA', 'NÃO INCLUSA'),
    ('INCLUSA', 'INCLUSA'),
]

# Choices para Venda Destinada
VENDA_DESTINADA_CHOICES = [
    ('INDUSTRIALIZACAO', 'INDUSTRIALIZAÇÃO'),
    ('USO_CONSUMO', 'USO/CONSUMO'),
]

# Choices para Contribuinte ICMS
CONTRIBUINTE_ICMS_CHOICES = [
    ('CONTRIBUINTE', 'CONTRIBUINTE'),
    ('NAO_CONTRIBUINTE', 'NÃO CONTRIBUINTE'),
]

# Choices para Tipo de Resina
TIPO_RESINA_CHOICES = [
    ('POLIESTER', 'POLIÉSTER'),
    ('ISOFTALICA', 'ISOFTÁLICA'),
    ('EPOXI', 'EPÓXI'),
    ('VINILESTER', 'VINILÉSTER'),
]

# Choices para Tipos de Inox
TIPO_INOX_CHOICES = [
    ('AISI_304', 'AISI 304'),
    ('AISI_316', 'AISI 316'),
    ('AISI_316L', 'AISI 316L'),
    ('OUTROS', 'OUTROS'),
]

# Choices para UF (Estados Brasileiros)
UF_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]

class Orcamento(models.Model):
    id = models.AutoField(primary_key=True)
    numero_orcamento = models.CharField(max_length=50, default='PADRÃO')
    revisao = models.IntegerField(default=1)
    cliente = models.CharField(max_length=200, blank=True)
    uf = models.CharField(max_length=2, choices=UF_CHOICES, default='BA')
    contato = models.CharField(max_length=150, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=150, blank=True)
    
    # Campos de frete e instalação como choices
    frete = models.CharField(max_length=50, choices=FRETE_CHOICES, default='CIF')
    instalacao = models.CharField(max_length=20, choices=INSTALACAO_CHOICES, default='NAO_INCLUSA')
    
    # Campos de venda e contribuinte como choices
    venda_destinada = models.CharField(max_length=50, choices=VENDA_DESTINADA_CHOICES, default='INDUSTRIALIZACAO')
    cliente_contrib_icms = models.CharField(max_length=20, choices=CONTRIBUINTE_ICMS_CHOICES, default='CONTRIBUINTE')
    
    cnpj_faturamento = models.CharField(max_length=20, blank=True)
    
    # Novos campos para tipo de resina e inox
    tipo_resina = models.CharField(max_length=20, choices=TIPO_RESINA_CHOICES, default='POLIESTER')
    tipo_inox = models.CharField(max_length=20, choices=TIPO_INOX_CHOICES, default='AISI_304')
    
    # Campo de comissão
    comissao = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Percentual de comissão (%)")
    
    icms = models.DecimalField(max_digits=5, decimal_places=2, default=7.2)
    status = models.CharField(max_length=15, choices=ORCAMENTO_STATUS_CHOICES, default='Rascunho')
    validade = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    total_bruto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    desconto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    imposto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_liquido = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orçamento {self.numero_orcamento} (Rev. {self.revisao})"

class OrcamentoItem(models.Model):
    id = models.AutoField(primary_key=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='itens')
    tipo_item = models.CharField(max_length=20, choices=ITEM_TIPO_CHOICES)
    descricao = models.CharField(max_length=250)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    desconto_item = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    imposto_item = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Cálculo correto: Custo + Lucro + Imposto
        # desconto_item agora representa o LUCRO total, não desconto
        self.valor_total = (self.quantidade * self.valor_unitario) + self.desconto_item + self.imposto_item
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descricao} - Qtd: {self.quantidade}"

class OrcamentoParametro(models.Model):
    id = models.AutoField(primary_key=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='parametros')
    chave = models.CharField(max_length=50)
    valor = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.chave}: {self.valor}"

class OrcamentoHistorico(models.Model):
    id = models.AutoField(primary_key=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='historico')
    acao = models.CharField(max_length=50, default='Criado')
    usuario = models.CharField(max_length=100, blank=True, default='Sistema')
    data_acao = models.DateTimeField(auto_now_add=True)
    detalhes = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.acao} - {self.data_acao.strftime('%d/%m/%Y %H:%M')}"


# Signals para manter a hierarquia de produtos atualizada
@receiver(post_save, sender=MP_Produtos)
def atualizar_produtos_dependentes(sender, instance, **kwargs):
    """
    Atualiza automaticamente o custo de produtos que dependem deste produto
    quando uma matéria-prima básica tem seu custo alterado
    """
    if instance.tipo_produto == 'simples':
        # Buscar produtos compostos e parametrizados que usam este produto
        produtos_afetados = MP_Produtos.objects.filter(
            componentes__produto_componente=instance,
            tipo_produto__in=['composto', 'parametrizado']
        ).distinct()
        
        for produto in produtos_afetados:
            produto.recalcular_custo_composto()


# Produto Template (Parametrizado)
class ProdutoTemplate(models.Model):
    """Template para produtos parametrizados"""
    produto_base = models.OneToOneField(MP_Produtos, on_delete=models.CASCADE, related_name='template', null=True, blank=True)
    parametros_obrigatorios = models.JSONField(default=list, help_text="Lista de parâmetros obrigatórios")
    parametros_opcionais = models.JSONField(default=dict, help_text="Parâmetros opcionais com valores padrão")
    formula_principal = models.TextField(blank=True, help_text="Fórmula principal de cálculo")

    def __str__(self):
        return f"Template: {self.produto_base.descricao if self.produto_base else 'Sem produto'}"


class ProdutoParametrizado(models.Model):
    """Instância específica de um produto parametrizado"""
    template = models.ForeignKey(ProdutoTemplate, on_delete=models.CASCADE, related_name='instancias')
    parametros = models.JSONField(help_text="Valores específicos dos parâmetros")
    custo_calculado = models.BigIntegerField(default=0, help_text="Custo calculado em centavos")
    data_calculo = models.DateTimeField(auto_now=True)
    observacoes = models.TextField(blank=True)

    def calcular_custo(self):
        """Calcula o custo baseado nos parâmetros e fórmulas do template"""
        # Implementação do cálculo baseado nos parâmetros
        pass

    def __str__(self):
        return f"{self.template.produto_base.descricao} - Instância {self.id}"


class ParametroFormula(models.Model):
    """Fórmulas específicas para parâmetros de templates"""
    template = models.ForeignKey(ProdutoTemplate, on_delete=models.CASCADE, related_name='formulas')
    nome_parametro = models.CharField(max_length=50)
    formula = models.TextField(help_text="Fórmula matemática para calcular o valor")
    descricao = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.template.produto_base.descricao} - {self.nome_parametro}"
