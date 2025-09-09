
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
import json
from decimal import Decimal

class Imposto(models.Model):
    nome = model# Choices para Tipos de Inox
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

class Orcamento(models.Model):ld(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    aliquota = models.DecimalField(max_digits=5, decimal_places=2, help_text="% sobre o valor")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.aliquota}%)"


class MaoObra(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, help_text="Descrição detalhada da mão de obra")
    valor_centavos = models.BigIntegerField(help_text="Valor em centavos para maior precisão")
    unidade = models.CharField(max_length=20, default="HORA", help_text="Unidade de cobrança (HORA, DIA, M², etc.)")
    categoria = models.CharField(max_length=50, blank=True, help_text="Ex: Pultrusão, Processamento/Montagem, Operações")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mão de Obra"
        verbose_name_plural = "Mão de Obra"
        ordering = ['categoria', 'nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.valor_centavos/100:.2f}/{self.unidade}"

    @property
    def valor_real(self):
        """Retorna o valor em reais"""
        return self.valor_centavos / 100

    @valor_real.setter
    def valor_real(self, valor):
        """Define o valor em reais, convertendo para centavos"""
        self.valor_centavos = int(valor * 100)


# Choices para tipos de produto
TIPO_PRODUTO_CHOICES = [
    ('simples', 'Produto Simples (Matéria-Prima Básica)'),
    ('composto', 'Produto Composto'),
    ('parametrizado', 'Produto Parametrizado (Template)'),
]

class MP_Produtos(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    custo_centavos = models.BigIntegerField()
    peso_und = models.DecimalField(max_digits=12, decimal_places=6)
    unidade = models.CharField(max_length=10)
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
    ('REVENDA', 'REVENDA'),
    ('CONSUMO_PROPRIO', 'CONSUMO PRÓPRIO'),
    ('EXPORTACAO', 'EXPORTAÇÃO'),
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
    ('VINILÉSTER', 'VINILÉSTER'),
]

# Choices para Tipo de Inox
TIPO_INOX_CHOICES = [
    ('AISI_304', 'AISI 304'),
    ('AISI_316', 'AISI 316'),
    ('AISI_316L', 'AISI 316L'),
    ('OUTROS', 'OUTROS'),
]

class Orcamento(models.Model):
    id = models.AutoField(primary_key=True)
    numero_orcamento = models.CharField(max_length=50, default='PADRÃO')
    revisao = models.IntegerField(default=1)
    cliente = models.CharField(max_length=200, blank=True)
    uf = models.CharField(max_length=2, default='BA')
    contato = models.CharField(max_length=150, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=150, blank=True)
    
    # Campos de frete e instalação como choices
    frete = models.CharField(max_length=50, choices=FRETE_CHOICES, default='CIF')
    instalacao = models.CharField(max_length=20, choices=INSTALACAO_CHOICES, default='NAO_INCLUSA')
    
    # Campos de venda e contribuinte como choices
    venda_destinada = models.CharField(max_length=50, choices=VENDA_DESTINADA_CHOICES, default='REVENDA')
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
    tipo_item = models.CharField(max_length=10, choices=ITEM_TIPO_CHOICES)
    descricao = models.CharField(max_length=250)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    desconto_item = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    imposto_item = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.tipo_item}: {self.descricao} (Qtd: {self.quantidade})"

class OrcamentoParametro(models.Model):
    id = models.AutoField(primary_key=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='parametros')
    chave = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.chave}: {self.valor}"

class OrcamentoHistorico(models.Model):
    id = models.AutoField(primary_key=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='historico')
    versao = models.IntegerField()
    status = models.CharField(max_length=15, choices=ORCAMENTO_STATUS_CHOICES)
    alterado_por = models.CharField(max_length=150)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    descricao_mudanca = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Histórico {self.orcamento.numero_orcamento} v{self.versao} - {self.status}"


# Novos modelos para produtos parametrizáveis
class ProdutoTemplate(models.Model):
    """Template para produtos parametrizáveis como grades, estruturas, etc."""
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=100)  # Ex: 'Grade', 'Estrutura', 'Cobertura'
    unidade_final = models.CharField(max_length=10, default='M²')  # Unidade do produto final
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.categoria})"


TIPO_PARAMETRO_CHOICES = [
    ('decimal', 'Número Decimal'),
    ('inteiro', 'Número Inteiro'),
    ('selecao', 'Seleção (Lista)'),
    ('produto', 'Produto/Material'),
]

class ParametroTemplate(models.Model):
    """Parâmetros configuráveis para um template de produto"""
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(ProdutoTemplate, on_delete=models.CASCADE, related_name='parametros')
    nome = models.CharField(max_length=100)  # Ex: 'vao', 'comprimento', 'perfil'
    label = models.CharField(max_length=150)  # Ex: 'Vão (m)', 'Comprimento (m)', 'Tipo de Perfil'
    tipo = models.CharField(max_length=10, choices=TIPO_PARAMETRO_CHOICES)
    obrigatorio = models.BooleanField(default=True)
    valor_padrao = models.CharField(max_length=100, blank=True, null=True)
    opcoes_selecao = models.TextField(blank=True, null=True)  # JSON para opções de seleção
    ordem = models.IntegerField(default=0)  # Ordem de exibição
    ajuda = models.CharField(max_length=300, blank=True, null=True)  # Texto de ajuda

    class Meta:
        ordering = ['ordem', 'nome']

    def __str__(self):
        return f"{self.template.nome} - {self.label}"


class ComponenteTemplate(models.Model):
    """Define que materiais/produtos são usados no template e como calcular as quantidades"""
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(ProdutoTemplate, on_delete=models.CASCADE, related_name='componentes')
    produto = models.ForeignKey(MP_Produtos, on_delete=models.CASCADE)
    nome_componente = models.CharField(max_length=150)  # Ex: 'Perfil Principal', 'Barra Vertical'
    formula_quantidade = models.TextField()  # Fórmula para calcular quantidade ex: "vao * 2 + comprimento"
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordem', 'nome_componente']

    def __str__(self):
        return f"{self.template.nome} - {self.nome_componente}"


class ProdutoParametrizado(models.Model):
    """Instância de um produto criado a partir de um template com parâmetros específicos"""
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(ProdutoTemplate, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=250)
    parametros = models.JSONField()  # Armazena os valores dos parâmetros
    custo_total_centavos = models.BigIntegerField()
    detalhes_calculo = models.JSONField(blank=True, null=True)  # Detalhes do cálculo para auditoria
    area_total = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    custo_por_unidade = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_produto


# Signals para atualização automática de preços
# Sistema de propagação de preços com controle de recursão
_updating_prices = set()  # Controla produtos sendo atualizados para evitar loops

@receiver(pre_save, sender=MP_Produtos)
def store_old_price(sender, instance, **kwargs):
    """Armazena o preço antigo antes de salvar para comparação"""
    if instance.pk:
        try:
            old_instance = MP_Produtos.objects.get(pk=instance.pk)
            instance._old_custo_centavos = old_instance.custo_centavos
        except MP_Produtos.DoesNotExist:
            instance._old_custo_centavos = None
    else:
        instance._old_custo_centavos = None


def propagar_mudanca_preco(produto_origem, nivel=0, produtos_processados=None):
    """
    Propaga mudanças de preço através de toda a cadeia de dependências
    """
    if produtos_processados is None:
        produtos_processados = set()
    
    # Evitar loops infinitos
    if produto_origem.id in produtos_processados:
        return
    
    produtos_processados.add(produto_origem.id)
    indent = "  " * nivel
    
    print(f"{indent}� Propagando mudanças do produto: {produto_origem.descricao}")
    
    # 1. Atualizar templates que usam este produto diretamente
    atualizar_templates_dependentes(produto_origem, nivel + 1)
    
    # 2. Atualizar produtos compostos que usam este produto
    produtos_dependentes = produto_origem.get_produtos_dependentes()
    
    if produtos_dependentes.exists():
        print(f"{indent}� Atualizando {produtos_dependentes.count()} produto(s) composto(s):")
        
        for produto in produtos_dependentes:
            if produto.id in _updating_prices:
                continue  # Já está sendo atualizado
                
            _updating_prices.add(produto.id)
            
            try:
                custo_antigo = produto.custo_centavos
                produto.recalcular_custo_composto()
                produto.refresh_from_db()
                custo_novo = produto.custo_centavos
                
                print(f"{indent}   📦 {produto.descricao}: R$ {custo_antigo/100:.2f} → R$ {custo_novo/100:.2f}")
                
                # Se o preço mudou, propagar recursivamente
                if custo_antigo != custo_novo:
                    # Salvar sem disparar signals para evitar loops
                    MP_Produtos.objects.filter(id=produto.id).update(
                        custo_centavos=custo_novo
                    )
                    
                    # Propagar para próximo nível
                    propagar_mudanca_preco(produto, nivel + 1, produtos_processados.copy())
                    
            finally:
                _updating_prices.discard(produto.id)


@receiver(post_save, sender=MP_Produtos)
def update_dependent_products(sender, instance, **kwargs):
    """Atualiza produtos dependentes quando o preço de uma matéria-prima muda"""
    # Verificar se está em uma atualização automática
    if instance.id in _updating_prices:
        return
    
    # Verificar se o custo mudou
    if hasattr(instance, '_old_custo_centavos') and instance._old_custo_centavos is not None:
        if instance._old_custo_centavos != instance.custo_centavos:
            # Preço mudou, iniciar propagação
            print(f"💰 Preço de '{instance.descricao}' mudou de R$ {instance._old_custo_centavos/100:.2f} para R$ {instance.custo_centavos/100:.2f}")
            
            # Iniciar propagação em cascata
            propagar_mudanca_preco(instance)


def atualizar_templates_dependentes(produto, nivel=0):
    """Atualiza parâmetros de templates que usam este produto como opção de seleção"""
    from django.db import transaction
    
    indent = "  " * nivel
    
    # Buscar parâmetros de templates que podem usar este produto
    parametros_resina = ParametroTemplate.objects.filter(
        tipo='selecao',
        opcoes_selecao__icontains=str(produto.id)
    )
    
    if parametros_resina.exists():
        print(f"{indent}🎯 Atualizando {parametros_resina.count()} template(s) que usam este produto:")
    
    for parametro in parametros_resina:
        try:
            opcoes = json.loads(parametro.opcoes_selecao) if parametro.opcoes_selecao else []
            opcoes_atualizadas = False
            
            for opcao in opcoes:
                if isinstance(opcao, dict) and opcao.get('id') == produto.id:
                    preco_antigo = opcao.get('preco', 0)
                    opcao['preco'] = float(produto.custo_centavos / 100)
                    opcoes_atualizadas = True
                    print(f"{indent}   📋 Template '{parametro.template.nome}' - parâmetro '{parametro.label}': R$ {preco_antigo:.2f} → R$ {opcao['preco']:.2f}")
            
            if opcoes_atualizadas:
                parametro.opcoes_selecao = json.dumps(opcoes)
                parametro.save()
                
        except (json.JSONDecodeError, KeyError) as e:
            print(f"{indent}   ⚠️  Erro ao atualizar template {parametro.template.nome}: {e}")


# Fim dos sinais de propagação de preços
