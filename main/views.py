from .models import Imposto, MaoObra
from .serializers import ImpostoSerializer, MaoObraSerializer
# ...existing code...

from rest_framework import viewsets, status
from rest_framework.response import Response

def safe_float(value, default=0.0):
    """Converte um valor para float de forma segura"""
    try:
        if value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

class ImpostoViewSet(viewsets.ModelViewSet):
    queryset = Imposto.objects.all()
    serializer_class = ImpostoSerializer


class MaoObraViewSet(viewsets.ModelViewSet):
    queryset = MaoObra.objects.all()
    serializer_class = MaoObraSerializer


def impostos(request):
    """View para a tela de impostos"""
    # Implementação da tela de impostos - a ser desenvolvida
    return render(request, 'main/impostos.html')
    # Buscar estatísticas dos impostos
    total_impostos = Imposto.objects.count()
    impostos_ativos = Imposto.objects.filter(ativo=True).count()
    impostos_icms = Imposto.objects.filter(nome__icontains="ICMS").count()
    impostos_difal = Imposto.objects.filter(nome__icontains="DIFAL").count()
    
    # Estados com maior e menor ICMS interno
    icms_internos = Imposto.objects.filter(nome__icontains="ICMS").filter(nome__icontains="Interno").order_by('-aliquota')
    maior_icms = icms_internos.first()
    menor_icms = icms_internos.last()
    
    # Estados com alíquota 12% interestadual
    estados_12_pct = Imposto.objects.filter(nome__icontains="Interestadual", aliquota=12.0).count()
    
    context = {
        'total_impostos': total_impostos,
        'impostos_ativos': impostos_ativos,
        'impostos_icms': impostos_icms,
        'impostos_difal': impostos_difal,
        'maior_icms': maior_icms,
        'menor_icms': menor_icms,
        'estados_12_pct': estados_12_pct,
    }
    
    return render(request, 'main/impostos.html', context)


def mao_de_obra(request):
    """View para a tela de mão de obra"""
    # Buscar estatísticas da mão de obra
    total_mao_obra = MaoObra.objects.count()
    mao_obra_ativa = MaoObra.objects.filter(ativo=True).count()
    
    # Valores extremos
    maior_valor = MaoObra.objects.order_by('-valor_centavos').first()
    menor_valor = MaoObra.objects.order_by('valor_centavos').first()
    
    # Valor médio
    from django.db.models import Avg
    valor_medio = MaoObra.objects.aggregate(media=Avg('valor_centavos'))['media']
    valor_medio = valor_medio / 100 if valor_medio else 0
    
    context = {
        'total_mao_obra': total_mao_obra,
        'mao_obra_ativa': mao_obra_ativa,
        'maior_valor': maior_valor,
        'menor_valor': menor_valor,
        'valor_medio': valor_medio,
    }
    
    return render(request, 'main/mao_de_obra.html', context)
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import (
    MP_Produtos, Orcamento, OrcamentoItem, ProdutoComponente,
    ProdutoTemplate, ProdutoParametrizado, ParametroFormula
)
from .serializers import (
    MP_ProdutosSerializer, OrcamentoSerializer, ProdutoComponenteSerializer,
    ProdutoTemplateSerializer, ProdutoParametrizadoSerializer, ParametroFormulaSerializer
)


def home(request):
    return render(request, 'main/home.html')


def about(request):
    """View para a página sobre"""
    return HttpResponse("<h1>Sobre o FIBERMEYER</h1><p>Esta é uma página sobre o projeto.</p>")


# View para tela de Produtos / MP
def mp(request):
    return render(request, 'main/mp.html')

# View para tela de Produtos Compostos
def produtos_compostos(request):
    return render(request, 'main/produtos_compostos.html')


# API REST para MP_Produtos
class MP_ProdutosViewSet(viewsets.ModelViewSet):
    queryset = MP_Produtos.objects.all()
    serializer_class = MP_ProdutosSerializer
    
    # Método partial_update removido - lógica de recálculo forçado desabilitada
    def partial_update_removido(self, request, *args, **kwargs):
        """REMOVIDO: Sobrescrevendo PATCH para forçar recálculo quando necessário"""
        if False:  # Desabilitado
            # Forçar recálculo do produto composto
            try:
                produto = self.get_object()
                if produto.tipo_produto in ['composto', 'parametrizado']:
                    print(f"🔄 Forçando recálculo do produto: {produto.descricao}")
                    
                    # Usar a mesma lógica da ProdutoComponenteViewSet
                    componentes = ProdutoComponente.objects.filter(produto_principal=produto)
                    custo_total = 0
                    peso_total = 0
                    
                    print(f"=== RECALCULANDO PRODUTO COMPOSTO: {produto.descricao} ===")
                    
                    for comp in componentes:
                        produto_comp = comp.produto_componente
                        if produto_comp:
                            # Verificar se há custos customizados na observação
                            custo_componente_centavos = produto_comp.custo_centavos
                            
                            if comp.observacao:
                                try:
                                    import json
                                    custos_salvos = json.loads(comp.observacao)
                                    if 'custo_total' in custos_salvos:
                                        # Usar custo total salvo na observação (já calculado)
                                        custo_componente_centavos = custos_salvos['custo_total']
                                        print(f"   • {produto_comp.descricao}: usando custo salvo R$ {custo_componente_centavos/100:.2f}")
                                    else:
                                        # Usar custo padrão do produto
                                        custo_componente_centavos = produto_comp.custo_centavos * float(comp.quantidade)
                                        print(f"   • {produto_comp.descricao}: usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                                except (json.JSONDecodeError, KeyError):
                                    # Se erro na observação, usar cálculo padrão
                                    custo_componente_centavos = produto_comp.custo_centavos * float(comp.quantidade)
                                    print(f"   • {produto_comp.descricao}: erro na observação, usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                            else:
                                # Sem observação, usar cálculo padrão
                                custo_componente_centavos = produto_comp.custo_centavos * float(comp.quantidade)
                                print(f"   • {produto_comp.descricao}: sem observação, usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                            
                            custo_total += custo_componente_centavos  # Manter em centavos
                            peso_total += float(produto_comp.peso_und) * float(comp.quantidade)
                   
                    print(f"   💰 Custo total calculado: R$ {custo_total/100:.2f}")
                    
                    produto.custo_centavos = int(round(custo_total))
                    produto.peso_und = peso_total
                    produto.save()
                    
                    # Retornar produto atualizado
                    serializer = self.get_serializer(produto)
                    return Response(serializer.data)
                else:
                    return Response({'error': 'Produto não é composto'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"❌ Erro no recálculo forçado: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Comportamento normal do PATCH
            return super().partial_update(request, *args, **kwargs)

# API REST para Orcamento
class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer

# API REST para ProdutoComponente
class ProdutoComponenteViewSet(viewsets.ModelViewSet):
    queryset = ProdutoComponente.objects.all()
    serializer_class = ProdutoComponenteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        produto_principal = self.request.query_params.get('produto_principal')
        if produto_principal:
            queryset = queryset.filter(produto_principal=produto_principal)
        return queryset
    
    def create(self, request, *args, **kwargs):
        print(f"=== CRIANDO COMPONENTE ===")
        print(f"Dados recebidos: {request.data}")
        
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                print(f"❌ Erros de validação: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar se o componente já existe
            produto_principal = serializer.validated_data['produto_principal']
            produto_componente = serializer.validated_data['produto_componente']
            
            componente_existente = ProdutoComponente.objects.filter(
                produto_principal=produto_principal,
                produto_componente=produto_componente
            ).first()
            
            if componente_existente:
                print(f"⚠️ Componente já existe, atualizando quantidade...")
                nova_quantidade = float(componente_existente.quantidade) + float(serializer.validated_data['quantidade'])
                componente_existente.quantidade = nova_quantidade
                componente_existente.observacao = f"Quantidade atualizada automaticamente para {nova_quantidade}"
                componente_existente.save()
                
                self.recalcular_preco_produto_composto(produto_principal)
                serializer_response = ProdutoComponenteSerializer(componente_existente)
                return Response(serializer_response.data, status=status.HTTP_200_OK)
            
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            print(f"✅ Componente criado com sucesso")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        except Exception as e:
            print(f"❌ Erro na criação do componente: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        self.recalcular_preco_produto_composto(instance.produto_principal)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.recalcular_preco_produto_composto(instance.produto_principal)

    def perform_destroy(self, instance):
        produto_principal = instance.produto_principal
        instance.delete()
        self.recalcular_preco_produto_composto(produto_principal)

    def recalcular_preco_produto_composto(self, produto_principal):
        # Recalcula o custo total e peso do produto composto
        componentes = ProdutoComponente.objects.filter(produto_principal=produto_principal)
        custo_total = 0
        peso_total = 0
        
        print(f"=== RECALCULANDO PRODUTO COMPOSTO: {produto_principal.descricao} ===")
        
        for comp in componentes:
            produto = comp.produto_componente
            if produto:
                # Verificar se há custos customizados na observação
                custo_componente_centavos = produto.custo_centavos
                
                if comp.observacao:
                    try:
                        import json
                        custos_salvos = json.loads(comp.observacao)
                        if 'custo_total' in custos_salvos:
                            # Usar custo total salvo na observação (já calculado)
                            custo_componente_centavos = custos_salvos['custo_total']
                            print(f"   • {produto.descricao}: usando custo salvo R$ {custo_componente_centavos/100:.2f}")
                        else:
                            # Usar custo padrão do produto
                            custo_componente_centavos = produto.custo_centavos * float(comp.quantidade)
                            print(f"   • {produto.descricao}: usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                    except (json.JSONDecodeError, KeyError):
                        # Se erro na observação, usar cálculo padrão
                        custo_componente_centavos = produto.custo_centavos * float(comp.quantidade)
                        print(f"   • {produto.descricao}: erro na observação, usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                else:
                    # Sem observação, usar cálculo padrão
                    custo_componente_centavos = produto.custo_centavos * float(comp.quantidade)
                    print(f"   • {produto.descricao}: sem observação, usando custo padrão R$ {custo_componente_centavos/100:.2f}")
                
                custo_total += custo_componente_centavos / 100
                peso_total += float(produto.peso_und) * float(comp.quantidade)
        
        print(f"   💰 Custo total calculado: R$ {custo_total:.2f}")
        
        produto_principal.custo_centavos = int(round(custo_total * 100))
        produto_principal.peso_und = peso_total
        produto_principal.save()

# API REST para Templates de Produtos Parametrizáveis
class ProdutoTemplateViewSet(viewsets.ModelViewSet):
    queryset = ProdutoTemplate.objects.all()
    serializer_class = ProdutoTemplateSerializer

class ProdutoParametrizadoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoParametrizado.objects.all()
    serializer_class = ProdutoParametrizadoSerializer

class ParametroFormulaViewSet(viewsets.ModelViewSet):
    queryset = ParametroFormula.objects.all()
    serializer_class = ParametroFormulaSerializer

# View para tela principal de orçamentos (lista)
def orcamentos(request):
    if request.method == 'POST' and request.POST.get('delete_orcamento'):
        orcamento_id = request.POST.get('orcamento_id')
        if orcamento_id:
            try:
                Orcamento.objects.get(id=orcamento_id).delete()
            except Orcamento.DoesNotExist:
                pass
    orcamentos = Orcamento.objects.all()
    return render(request, 'main/orcamentos.html', {'orcamentos': orcamentos})

# View para tela de cadastro de orçamento
from .models import Orcamento
from django.shortcuts import redirect
from django import forms

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = [
            'numero_orcamento', 'revisao', 'cliente', 'uf', 'contato', 'telefone', 'email',
            'frete', 'instalacao', 'venda_destinada', 'cliente_contrib_icms', 'cnpj_faturamento',
            'tipo_resina', 'tipo_inox', 'comissao', 'icms', 'validade', 'observacoes'
        ]
        widgets = {
            'validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_orcamento': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'style': 'background-color: #f8f9fa;'}),
            'revisao': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-select'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'frete': forms.Select(attrs={'class': 'form-select'}),
            'instalacao': forms.Select(attrs={'class': 'form-select'}),
            'venda_destinada': forms.Select(attrs={'class': 'form-select'}),
            'cliente_contrib_icms': forms.Select(attrs={'class': 'form-select'}),
            'cnpj_faturamento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_resina': forms.Select(attrs={'class': 'form-select'}),
            'tipo_inox': forms.Select(attrs={'class': 'form-select'}),
            'comissao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'icms': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'readonly': True, 'style': 'background-color: #e8f5e8;'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'numero_orcamento': 'Orçamento nº',
            'revisao': 'Revisão',
            'cliente': 'Cliente',
            'uf': 'UF',
            'contato': 'Contato',
            'telefone': 'Telefone',
            'email': 'Email',
            'frete': 'Frete',
            'instalacao': 'Instalação',
            'venda_destinada': 'Venda Destinada a',
            'cliente_contrib_icms': 'Cliente Contribuinte de ICMS',
            'cnpj_faturamento': 'CNPJ de Faturamento',
            'tipo_resina': 'Tipo de Resina',
            'tipo_inox': 'Tipo de Inox',
            'comissao': 'Comissão (%)',
            'icms': 'ICMS (%)',
            'validade': 'Validade',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar choices de UF do modelo
        from .models import UF_CHOICES
        self.fields['uf'].choices = UF_CHOICES
        
        # Gerar número do orçamento automaticamente
        from datetime import datetime
        ano_atual = datetime.now().year
        ultimo_orcamento = Orcamento.objects.filter(
            numero_orcamento__startswith=f'{ano_atual}-'
        ).order_by('-id').first()
        
        if ultimo_orcamento:
            try:
                ultimo_numero = int(ultimo_orcamento.numero_orcamento.split('-')[1])
                proximo_numero = ultimo_numero + 1
            except:
                proximo_numero = 1
        else:
            proximo_numero = 1
        
        numero_automatico = f'{ano_atual}-{proximo_numero:04d}'
        
        # Adicionar placeholder e valores padrão
        self.fields['numero_orcamento'].initial = numero_automatico
        self.fields['uf'].initial = 'BA'
        self.fields['frete'].initial = 'CIF'
        self.fields['instalacao'].initial = 'NAO_INCLUSA'
        self.fields['venda_destinada'].initial = 'REVENDA'
        self.fields['cliente_contrib_icms'].initial = 'CONTRIBUINTE'
        self.fields['tipo_resina'].initial = 'POLIESTER'
        self.fields['tipo_inox'].initial = 'AISI_304'
        self.fields['comissao'].initial = 0.0
        self.fields['icms'].initial = 7.2

def orcamento_form(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orcamentos')
    else:
        form = OrcamentoForm()
    return render(request, 'main/orcamento_form.html', {'form': form})

# View para tela de detalhes do orçamento
from .models import MP_Produtos

def orcamento(request, orcamento_id):
    orcamento = Orcamento.objects.get(id=orcamento_id)
    itens = list(orcamento.itens.all())
    produtos = MP_Produtos.objects.all()

    # Adiciona ou edita produto no orçamento ou altera status
    if request.method == 'POST':
        # Controle de status
        status_action = request.POST.get('status_action')
        if status_action:
            if status_action == 'enviar' and orcamento.status == 'Rascunho':
                orcamento.status = 'Enviado'
                orcamento.save()
            elif status_action == 'revisar' and orcamento.status in ['Enviado', 'Rascunho']:
                orcamento.status = 'Em revisão'
                orcamento.revisao += 1
                orcamento.save()
            elif status_action == 'enviar_revisao' and orcamento.status == 'Em revisão':
                orcamento.status = 'Enviado'
                orcamento.save()
            elif status_action == 'ganha' and orcamento.status == 'Enviado':
                orcamento.status = 'Ganha'
                orcamento.save()
            elif status_action == 'perda' and orcamento.status == 'Enviado':
                orcamento.status = 'Perda'
                orcamento.save()
            return redirect('orcamento', orcamento_id=orcamento_id)
        edit_item_id = request.POST.get('edit_item_id')
        if edit_item_id:
            # Edição de item existente
            from .models import OrcamentoItem
            item = OrcamentoItem.objects.get(id=edit_item_id)
            item.quantidade = request.POST.get('quantidade', item.quantidade)
            item.valor_unitario = request.POST.get('valor_unitario', item.valor_unitario)
            item.desconto_item = request.POST.get('desconto', item.desconto_item)
            item.imposto_item = request.POST.get('imposto', item.imposto_item)
            # Recalcula valores se necessário
            try:
                # Validar e converter todos os valores
                valor_unitario = safe_float(item.valor_unitario)
                quantidade = safe_float(item.quantidade, 1.0)
                desconto = safe_float(request.POST.get('desconto', item.desconto_item))
                imposto = safe_float(request.POST.get('imposto', item.imposto_item))
                
                valor_bruto = valor_unitario * quantidade
                valor_desconto = valor_bruto * (desconto / 100)
                valor_imposto = (valor_bruto - valor_desconto) * (imposto / 100)
                valor_total = valor_bruto - valor_desconto + valor_imposto
                item.desconto_item = valor_desconto
                item.imposto_item = valor_imposto
                item.valor_total = valor_total
            except Exception:
                pass
            item.save()
            # Atualiza totais do orçamento
            itens = list(orcamento.itens.all())
            orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
            orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
            orcamento.save()
            return redirect('orcamento', orcamento_id=orcamento_id)
        delete_item_id = request.POST.get('delete_item_id')
        if delete_item_id:
            from .models import OrcamentoItem
            try:
                item = OrcamentoItem.objects.get(id=delete_item_id)
                item.delete()
                # Atualiza totais do orçamento após remoção
                itens = list(orcamento.itens.all())
                orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                orcamento.save()
            except OrcamentoItem.DoesNotExist:
                pass
            # Não faz redirect, apenas segue para o render abaixo
        else:
            # Adição de novo item
            produto_id = request.POST.get('produto_id')
            produto_parametrizado = request.POST.get('produto_parametrizado')
            quantidade = request.POST.get('quantidade')
            desconto = request.POST.get('desconto') or 0
            imposto = request.POST.get('imposto') or 0
            
            if produto_parametrizado:
                # Processar produto parametrizado
                try:
                    data = json.loads(produto_parametrizado)
                    descricao = data.get('nome', 'Produto Parametrizado')
                    
                    # Validar e converter valores
                    valor_unitario = safe_float(data.get('preco_total', 0))
                    quantidade_valor = safe_float(quantidade, 1.0)
                    desconto_num = safe_float(desconto)
                    imposto_num = safe_float(imposto)
                    
                    valor_bruto = valor_unitario * quantidade_valor
                    valor_desconto = valor_bruto * (desconto_num / 100)
                    valor_imposto = (valor_bruto - valor_desconto) * (imposto_num / 100)
                    valor_total = valor_bruto - valor_desconto + valor_imposto
                    
                    from .models import OrcamentoItem
                    OrcamentoItem.objects.create(
                        orcamento=orcamento,
                        tipo_item='Parametrizado',
                        descricao=descricao,
                        quantidade=quantidade_valor,
                        valor_unitario=valor_unitario,
                        desconto_item=valor_desconto,
                        imposto_item=valor_imposto,
                        valor_total=valor_total
                    )
                    
                    # Atualiza totais do orçamento
                    itens = list(orcamento.itens.all())
                    orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                    orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                    orcamento.save()
                    return redirect('orcamento', orcamento_id=orcamento_id)
                except Exception as e:
                    # Em caso de erro, continue para o processamento normal
                    pass
            elif produto_id and quantidade:
                produto = MP_Produtos.objects.get(id=produto_id)
                valor_unitario = produto.custo_centavos / 100.0
                
                # Validar e converter quantidade
                quantidade_num = safe_float(quantidade, 1.0)
                
                # Validar e converter desconto
                desconto_num = safe_float(desconto)
                
                # Validar e converter imposto
                imposto_num = safe_float(imposto)
                
                valor_bruto = valor_unitario * quantidade_num
                valor_desconto = valor_bruto * (desconto_num / 100)
                valor_imposto = (valor_bruto - valor_desconto) * (imposto_num / 100)
                valor_total = valor_bruto - valor_desconto + valor_imposto
                from .models import OrcamentoItem
                OrcamentoItem.objects.create(
                    orcamento=orcamento,
                    tipo_item='Produto',
                    descricao=produto.descricao,
                    quantidade=quantidade_num,
                    valor_unitario=valor_unitario,
                    desconto_item=valor_desconto,
                    imposto_item=valor_imposto,
                    valor_total=valor_total
                )
                # Atualiza totais do orçamento
                itens = list(orcamento.itens.all())
                orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                orcamento.save()
                return redirect('orcamento', orcamento_id=orcamento_id)

    # Calcula total_liquido e total_desconto dos itens
    total_liquido = sum([safe_float(item.valor_total) for item in itens])
    total_desconto = sum([safe_float(item.desconto_item) for item in itens])

    return render(request, 'main/orcamento.html', {
        'orcamento': orcamento,
        'itens': itens,
        'produtos': produtos,
        'total_liquido': total_liquido,
        'total_desconto': total_desconto
    })


# View para calcular produto parametrizado
@csrf_exempt
def calcular_produto_parametrizado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template_id = data.get('template_id')
            parametros = data.get('parametros', {})
            
            # Buscar template
            template = ProdutoTemplate.objects.get(id=template_id, ativo=True)
            
            # Calcular quantidades e custos
            resultado = calcular_custos_template(template, parametros)
            
            return JsonResponse(resultado)
            
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405)


def calcular_custos_template(template, parametros):
    """Calcula custos baseado no template e parâmetros fornecidos"""
    componentes_calculados = []
    custo_total = 0
    
    # Resolver produtos selecionados nos parâmetros
    produtos_parametros = {}
    for param_nome, param_valor in parametros.items():
        if param_nome.endswith('_id') and param_valor:
            try:
                produto = MP_Produtos.objects.get(id=param_valor)
                # Remover '_id' do nome para usar na fórmula
                param_base = param_nome.replace('_id', '')
                produtos_parametros[param_base] = produto
            except MP_Produtos.DoesNotExist:
                pass
    
    for componente in template.componentes.filter(ativo=True):
        try:
            # Decidir qual produto usar
            produto_usar = componente.produto
            
            # Se há um parâmetro de produto que pode substituir, usar ele
            # Por exemplo, se param perfil_id foi selecionado, usar esse produto
            for param_key, produto_param in produtos_parametros.items():
                if 'perfil' in param_key.lower() and any(palavra in componente.nome_componente.lower() for palavra in ['perfil', 'barra']):
                    produto_usar = produto_param
                    break
                # Especial para resina: se componente é "Resina" e temos tipo_resina selecionado
                elif 'tipo_resina' in param_key.lower() and componente.nome_componente.lower() == 'resina':
                    produto_usar = produto_param
                    break
            
            # Substituir variáveis na fórmula pelos valores dos parâmetros
            formula = componente.formula_quantidade
            for param_nome, param_valor in parametros.items():
                # Não incluir parâmetros de ID na fórmula
                if not param_nome.endswith('_id'):
                    formula = formula.replace(param_nome, str(param_valor))
            
            # Calcular quantidade (usando eval - cuidado em produção!)
            quantidade_calculada = eval(formula)
            
            # Calcular custo
            custo_unitario = produto_usar.custo_centavos / 100
            custo_item = quantidade_calculada * custo_unitario
            custo_total += custo_item
            
            componente_info = {
                'nome': componente.nome_componente,
                'produto': produto_usar.descricao,
                'formula': componente.formula_quantidade,
                'formula_calculada': formula,
                'quantidade': quantidade_calculada,
                'custo_unitario': custo_unitario,
                'custo_total': custo_item,
                'unidade': produto_usar.unidade
            }
            
            componentes_calculados.append(componente_info)
            
        except Exception as e:
            return {
                'erro': f'Erro no componente {componente.nome_componente}: {str(e)}'
            }
    
    # Aplicar perda de processo se especificada
    perda_processo = 0
    if 'perda_processo' in parametros:
        try:
            perda_processo = float(parametros['perda_processo'])
        except:
            perda_processo = 0
    
    # Custo total com perda de processo
    custo_total_com_perda = custo_total * (1 + perda_processo / 100)
    valor_perda_processo = custo_total_com_perda - custo_total
    
    # Calcular área se for em mm
    area_m2 = 0
    if 'largura' in parametros and 'altura' in parametros:
        try:
            largura_mm = float(parametros['largura'])
            altura_mm = float(parametros['altura'])
            area_m2 = (largura_mm * altura_mm) / 1000000  # Converter mm² para m²
        except:
            pass
    
    return {
        'template': template.nome,
        'componentes': componentes_calculados,
        'custo_total_sem_perda': custo_total,
        'perda_processo': valor_perda_processo,
        'custo_total': custo_total_com_perda,
        'custo_total_centavos': int(custo_total_com_perda * 100),
        'area_m2': area_m2,
        'custo_por_m2': custo_total_com_perda / area_m2 if area_m2 > 0 else 0
    }


@require_http_methods(["POST"])
@csrf_exempt
def calcular_produto_parametrizado(request):
    """API para calcular o custo de um produto parametrizado"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        parametros = data.get('parametros', {})
        
        # Buscar template
        template = ProdutoTemplate.objects.get(id=template_id)
        
        # Mapeamento dos componentes para IDs na tabela MP_Produtos
        componentes_mp_ids = {
            'roving_4400': 1237,      # Roving 4400 - R$ 4.81
            'manta_300': 1238,        # Manta 300 - R$ 12.13
            'veu': 1239,              # Véu - R$ 44.54
            'monomero_estireno': 1266, # Monômero de estireno - R$ 12.80
            'anti_uv': 1243,          # Anti UV - R$ 163.79
            'anti_ox': 1244,          # Anti OX - R$ 59.28
            'bpo': 1245,              # BPO - R$ 58.57
            'tbpb': 1246,             # TBPB - R$ 67.56
            'desmoldante': 1247,       # Desmoldante - R$ 112.62
            'antichama': 1248,         # Antichama - R$ 5.76
            'carga_mineral': 1249,     # Carga mineral - R$ 1.31
            'pigmento': 1250,          # Pigmento - R$ 49.40
        }
        
        # Buscar preços e nomes dos produtos MP
        produtos_mp = {}
        for componente, mp_id in componentes_mp_ids.items():
            try:
                produto = MP_Produtos.objects.get(id=mp_id)
                produtos_mp[componente] = {
                    'nome': produto.descricao,
                    'preco_centavos': produto.custo_centavos
                }
            except MP_Produtos.DoesNotExist:
                # Fallback se produto não existir
                produtos_mp[componente] = {
                    'nome': componente.replace('_', ' ').title(),
                    'preco_centavos': 1000  # R$ 10.00 como fallback
                }
        
        # Buscar tipo de resina selecionada
        tipo_resina_id = parametros.get('tipo_resina', '1269')  # Default Poliéster
        try:
            resina_mp = MP_Produtos.objects.get(id=int(tipo_resina_id))
            produtos_mp['resina'] = {
                'nome': resina_mp.descricao,
                'preco_centavos': resina_mp.custo_centavos
            }
        except MP_Produtos.DoesNotExist:
            # Fallback para resina padrão
            produtos_mp['resina'] = {
                'nome': "Resina Poliéster",
                'preco_centavos': 1296
            }
        
        # Cálculo básico baseado nos parâmetros do "Novo Perfil"
        custo_total = 0
        peso_total = 0
        componentes = []
        
        # Componentes diretos (roving, manta, véu) - quantidade = valor do parâmetro
        if 'roving_4400' in parametros and 'roving_4400' in produtos_mp:
            roving_qtd = float(parametros['roving_4400'])
            produto_info = produtos_mp['roving_4400']
            custo_roving = roving_qtd * produto_info['preco_centavos']
            custo_total += custo_roving
            peso_total += roving_qtd
            componentes.append({
                'nome': produto_info['nome'],
                'produto': produto_info['nome'],
                'quantidade': roving_qtd,
                'custo_unitario': produto_info['preco_centavos'],
                'custo_total': custo_roving
            })
        
        if 'manta_300' in parametros and 'manta_300' in produtos_mp:
            manta_qtd = float(parametros['manta_300'])
            produto_info = produtos_mp['manta_300']
            custo_manta = manta_qtd * produto_info['preco_centavos']
            custo_total += custo_manta
            peso_total += manta_qtd
            componentes.append({
                'nome': produto_info['nome'],
                'produto': produto_info['nome'],
                'quantidade': manta_qtd,
                'custo_unitario': produto_info['preco_centavos'],
                'custo_total': custo_manta
            })
        
        if 'veu' in parametros and 'veu' in produtos_mp:
            veu_qtd = float(parametros['veu'])
            produto_info = produtos_mp['veu']
            custo_veu = veu_qtd * produto_info['preco_centavos']
            custo_total += custo_veu
            peso_total += veu_qtd
            componentes.append({
                'nome': produto_info['nome'],
                'produto': produto_info['nome'],
                'quantidade': veu_qtd,
                'custo_unitario': produto_info['preco_centavos'],
                'custo_total': custo_veu
            })
        
        # Calcular peso base para os componentes calculados
        peso_base = 0
        if 'peso_m' in parametros:
            peso_m = float(parametros['peso_m'])
            peso_base = peso_m
            peso_total = peso_m  # Ajustar peso total para o peso informado
        else:
            # Se não há peso_m especificado, usar peso total dos componentes diretos
            peso_base = peso_total
        
        # Componentes calculados baseados no peso base com fatores corretos
        if peso_base > 0:
            componentes_calculados = [
                ('resina', 0.6897),                    # 68.97% do peso residual
                ('monomero_estireno', 0.0213),         # 2.13% do peso residual
                ('anti_uv', 0.0028),                   # 0.28% do peso residual
                ('anti_ox', 0.0028),                   # 0.28% do peso residual
                ('bpo', 0.0172),                       # 1.72% do peso residual
                ('tbpb', 0.0086),                      # 0.86% do peso residual
                ('desmoldante', 0.0086),               # 0.86% do peso residual
                ('antichama', 0.0430),                 # 4.30% do peso residual
                ('carga_mineral', 0.0645),             # 6.45% do peso residual
                ('pigmento', 0.0086),                  # 0.86% do peso residual
            ]
            
            for componente_key, fator in componentes_calculados:
                if componente_key in produtos_mp:
                    produto_info = produtos_mp[componente_key]
                    quantidade = peso_base * fator
                    custo_componente = quantidade * produto_info['preco_centavos']
                    custo_total += custo_componente
                    
                    componentes.append({
                        'nome': produto_info['nome'],
                        'produto': produto_info['nome'],
                        'quantidade': round(quantidade, 4),
                        'custo_unitario': produto_info['preco_centavos'],
                        'custo_total': round(custo_componente, 2)
                    })
        
        # Aplicar perda de processo se especificada
        if 'perda_processo' in parametros:
            try:
                perda = float(parametros['perda_processo'])
                custo_total = custo_total * (1 + perda / 100)
            except:
                pass
        
        # CÁLCULO DE MÃO DE OBRA PARA NOVO PERFIL
        custo_mao_obra = 0
        if ('velocidade_m_h' in parametros and 
            'num_matrizes' in parametros and 
            'num_maquinas_utilizadas' in parametros):
            
            try:
                # Parâmetros de mão de obra
                velocidade_m_h = float(parametros['velocidade_m_h'])
                num_matrizes = float(parametros['num_matrizes'])
                num_maquinas_utilizadas = float(parametros['num_maquinas_utilizadas'])
                
                # Buscar custo de Pultrusão na base de mão de obra (ID = 1)
                try:
                    from .models import MaoObra
                    
                    # DEBUG: Mostrar qual valor está sendo buscado
                    print("=== DEBUG MÃO DE OBRA ===")
                    print("Buscando registro ID=1 na tabela main_maoobra...")
                    
                    # Buscar diretamente por ID = 1 conforme especificado
                    pultrusao = MaoObra.objects.get(id=1)
                    mo_pultrusao = pultrusao.valor_centavos
                    
                    print(f"✅ REGISTRO ENCONTRADO:")
                    print(f"   ID: {pultrusao.id}")
                    print(f"   Nome: {pultrusao.nome}")
                    print(f"   Valor: {mo_pultrusao} centavos = R$ {mo_pultrusao/100:.2f}")
                        
                except Exception as e:
                    # Fallback se não encontrar ID=1
                    mo_pultrusao = 9976258  # R$ 99.762,58 como padrão (valor mensal)
                    print(f"❌ ERRO AO BUSCAR MÃO DE OBRA ID=1: {e}")
                    print(f"   Usando fallback: {mo_pultrusao} centavos = R$ {mo_pultrusao/100:.2f}")
                
                # Aplicar nova fórmula: ((mo_pultrusao / 3) * n° de máquinas) / (VELOCIDADE M/H * N° MATRIZES * 24 * 21 * 0,5)
                if velocidade_m_h > 0 and num_matrizes > 0:
                    numerador = (mo_pultrusao / 3) * num_maquinas_utilizadas
                    denominador = velocidade_m_h * num_matrizes * 24 * 21 * 0.5
                    custo_mao_obra = numerador / denominador
                    
                    # Garantir que o custo seja pelo menos 1 centavo se > 0
                    custo_mao_obra_centavos = max(1, int(custo_mao_obra)) if custo_mao_obra > 0 else 0
                    
                    # DEBUG: Mostrar cálculo detalhado
                    print(f"\n=== CÁLCULO MÃO DE OBRA (NOVA FÓRMULA) ===")
                    print(f"Parâmetros:")
                    print(f"   Velocidade: {velocidade_m_h} m/h")
                    print(f"   N° Matrizes: {num_matrizes}")
                    print(f"   Máquinas utilizadas: {num_maquinas_utilizadas}")
                    print(f"   Valor base (mo_pultrusao): {mo_pultrusao} centavos = R$ {mo_pultrusao/100:.2f}")
                    print(f"\nFórmula: ((mo_pultrusao / 3) * n° máquinas) / (velocidade * n° matrizes * 24 * 21 * 0.5)")
                    print(f"   Numerador = ({mo_pultrusao} / 3) * {num_maquinas_utilizadas} = {numerador:.2f}")
                    print(f"   Denominador = {velocidade_m_h} * {num_matrizes} * 24 * 21 * 0.5 = {denominador}")
                    print(f"   Custo raw = {numerador:.2f} / {denominador} = {custo_mao_obra:.6f}")
                    print(f"   Custo final = {custo_mao_obra_centavos} centavos = R$ {custo_mao_obra_centavos/100:.2f}")
                    
                    # Adicionar mão de obra aos componentes para visualização
                    componentes.append({
                        'nome': 'Mão de Obra - Pultrusão',
                        'produto': f'Pultrusão ({num_maquinas_utilizadas} máq, {velocidade_m_h} m/h, {num_matrizes} matrizes)',
                        'quantidade': 1.0,
                        'custo_unitario': custo_mao_obra_centavos,
                        'custo_total': custo_mao_obra_centavos
                    })
                    
                    print(f"\n✅ COMPONENTE CRIADO:")
                    print(f"   Nome: Mão de Obra - Pultrusão")
                    print(f"   Custo: {custo_mao_obra_centavos} centavos = R$ {custo_mao_obra_centavos/100:.2f}")
                    
                    # Adicionar ao custo total
                    custo_total += custo_mao_obra_centavos
                    
                else:
                    print(f"❌ ERRO: Velocidade ({velocidade_m_h}) ou matrizes ({num_matrizes}) inválidas")
                    
            except (ValueError, ZeroDivisionError) as e:
                # Se houver erro nos cálculos, ignora mão de obra
                pass
        
        return JsonResponse({
            'success': True,
            'custo_total': int(custo_total),
            'peso_total': round(peso_total, 3),
            'componentes': componentes,
            'parametros_utilizados': parametros
        })
        
    except ProdutoTemplate.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Template não encontrado'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["GET"])
def tipos_resina(request):
    """API para buscar tipos de resina disponíveis no banco"""
    try:
        # Buscar produtos que contenham "resina" na descrição
        resinas = MP_Produtos.objects.filter(
            descricao__icontains='resina'
        ).order_by('descricao')
        
        resinas_data = []
        for resina in resinas:
            resinas_data.append({
                'id': resina.id,
                'descricao': resina.descricao,
                'custo_centavos': resina.custo_centavos,
                'custo_reais': resina.custo_centavos / 100,
                'unidade': resina.unidade,
                'referencia': resina.referencia or ''
            })
        
        return JsonResponse({
            'success': True,
            'resinas': resinas_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def mao_obra_lista(request):
    """API para buscar mão de obra disponível no banco"""
    try:
        from .models import MaoObra
        
        # Buscar todas as mãos de obra ativas
        mao_obra_list = MaoObra.objects.filter(ativo=True).order_by('nome')
        
        mo_data = []
        for mo in mao_obra_list:
            mo_data.append({
                'id': mo.id,
                'nome': mo.nome,
                'descricao': mo.descricao,
                'valor_centavos': mo.valor_centavos,
                'valor_real': mo.valor_real,
                'unidade': mo.unidade
            })
        
        return JsonResponse({
            'success': True,
            'mao_obra': mo_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
