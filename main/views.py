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
from django.shortcuts import redirect, get_object_or_404
from django import forms
from django.contrib import messages

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

def orcamento_edit(request, orcamento_id):
    """View para editar um orçamento existente"""
    orcamento = get_object_or_404(Orcamento, id=orcamento_id)
    
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Orçamento {orcamento.numero_orcamento} atualizado com sucesso!')
            return redirect('orcamento', orcamento_id=orcamento.id)
    else:
        form = OrcamentoForm(instance=orcamento)
    
    context = {
        'form': form,
        'orcamento': orcamento,
        'editing': True
    }
    return render(request, 'main/orcamento_form.html', context)

# View para tela de detalhes do orçamento
from .models import MP_Produtos

def orcamento(request, orcamento_id):
    from decimal import Decimal
    
    orcamento = Orcamento.objects.get(id=orcamento_id)
    itens = list(orcamento.itens.select_related('produto').all())
    
    # 🔄 APLICAR fórmula correta aos itens para exibição
    print(f"🔄 DEBUG: Aplicando fórmula correta aos {len(itens)} itens do orçamento {orcamento_id}")
    
    for item in itens:
        # Aplicar a mesma fórmula do modelo, mas sem salvar no banco
        print(f"� DEBUG: Calculando item {item.id} - {item.descricao}")
        
        # 1. Valor Base: Custo × Quantidade
        valor_base = Decimal(str(item.quantidade)) * Decimal(str(item.valor_unitario))
        print(f"1️⃣ DEBUG: Valor base = {item.quantidade} × {item.valor_unitario} = {valor_base}")
        
        # 2. Calcular impostos totais (do orçamento + item)
        impostos_orcamento = Decimal('0')
        if orcamento:
            # ICMS do orçamento
            icms = Decimal(str(orcamento.icms or 0))
            comissao = Decimal(str(orcamento.comissao or 0))
            
            # Outros impostos fixos
            simples_iss = icms  # Simples ISS = ICMS
            pis_confins = Decimal('3.65')
            ir_csocial = Decimal('2.28')
            embalagem = Decimal('1.0')
            frete = Decimal('0.0')
            desp_financ = Decimal('1.5')
            desp_adm = Decimal('18.0')
            
            # TOTAL DE IMPOSTOS = Comissão + ICMS + outros impostos
            outros_impostos = simples_iss + pis_confins + ir_csocial + embalagem + frete + desp_financ + desp_adm
            impostos_orcamento = comissao + outros_impostos
            print(f"💰 DEBUG: Comissão={comissao}, Outros impostos={outros_impostos}")
            print(f"💰 DEBUG: Total impostos orçamento = {impostos_orcamento}%")
        
        # Impostos totais = impostos do orçamento + impostos específicos do item
        impostos_totais = impostos_orcamento + Decimal(str(item.imposto_item or 0))
        print(f"🎯 DEBUG: Impostos totais (orçamento + item) = {impostos_totais}%")
        
        # Aplicar Impostos + Comissão: Valor Base × (1 + (Impostos+Comissão)/100)
        valor_com_impostos = valor_base * (Decimal('1') + impostos_totais / Decimal('100'))
        print(f"2️⃣ DEBUG: Valor com impostos+comissão = {valor_base} × (1 + {impostos_totais}/100) = {valor_com_impostos}")
        
        # 3. Aplicar Lucro: Valor com Impostos × (1 + Lucro/100)
        valor_com_lucro = valor_com_impostos * (Decimal('1') + Decimal(str(item.desconto_item)) / Decimal('100'))
        print(f"3️⃣ DEBUG: Valor com lucro = {valor_com_impostos} × (1 + {item.desconto_item}/100) = {valor_com_lucro}")
        
        # 4. Aplicar IPI: Valor com Lucro × (1 + IPI/100)
        valor_final = valor_com_lucro * (Decimal('1') + Decimal(str(item.ipi_item)) / Decimal('100'))
        print(f"4️⃣ DEBUG: Valor final com IPI = {valor_com_lucro} × (1 + {item.ipi_item}/100) = {valor_final}")
        
        # Atualizar o valor_total do item para exibição (e salvar no banco)
        item.valor_total = valor_final
        item.save()
        print(f"✅ DEBUG: Item {item.id} atualizado: R${item.valor_total}")
    
    # 🔄 RECARREGAR itens do banco para ter os valores atualizados
    itens = list(orcamento.itens.all())
    print(f"🔄 DEBUG: Itens recarregados do banco para exibição")
    
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
            # Agora usamos 'lucro' em vez de 'desconto'
            lucro_percentual = safe_float(request.POST.get('lucro', 0))
            item.imposto_item = request.POST.get('imposto', item.imposto_item)
            # Recalcula valores se necessário
            try:
                # Validar e converter todos os valores
                custo_unitario = safe_float(item.valor_unitario)  # agora é custo
                quantidade = safe_float(item.quantidade, 1.0)
                imposto = safe_float(request.POST.get('imposto', item.imposto_item))
                ipi_percentual = safe_float(item.ipi_item, 0)  # IPI atual do item
                
                # Calcular valor de venda baseado no lucro sobre o custo
                valor_lucro_unitario = custo_unitario * (lucro_percentual / 100)
                valor_venda_unitario = custo_unitario + valor_lucro_unitario
                
                valor_bruto = valor_venda_unitario * quantidade
                valor_imposto = valor_bruto * (imposto / 100)
                valor_sem_ipi = valor_bruto + valor_imposto
                
                # Calcular IPI sobre o valor sem IPI
                valor_ipi = valor_sem_ipi * (ipi_percentual / 100)
                valor_total = valor_sem_ipi + valor_ipi
                
                # Guardar o valor do lucro em valor monetário no campo desconto_item para compatibilidade
                item.desconto_item = valor_lucro_unitario * quantidade
                item.imposto_item = valor_imposto
                item.valor_total = valor_total
                
                # Debug log apenas se DEBUG=True
                from django.conf import settings
                if getattr(settings, 'DEBUG', False):
                    print(f"DEBUG - Item {item.id}: Custo={custo_unitario}, Lucro%={lucro_percentual}, IPI%={ipi_percentual}, Total={valor_total}")
            except Exception as e:
                # Log do erro apenas se DEBUG=True
                from django.conf import settings
                if getattr(settings, 'DEBUG', False):
                    print(f"ERRO no cálculo do item {item.id}: {e}")
                pass
            item.save()
            # Atualiza totais do orçamento
            itens = list(orcamento.itens.all())
            orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
            orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
            orcamento.save()
            
            # Se for uma requisição AJAX, retornar JSON
            if request.POST.get('ajax_update'):
                from django.http import JsonResponse
                return JsonResponse({
                    'success': True,
                    'total_lucro': f"{orcamento.desconto_total:.2f}",
                    'total_liquido': f"{orcamento.total_liquido:.2f}",
                    'item_total': f"{item.valor_total:.2f}",
                    'item_lucro': f"{item.desconto_item:.2f}"
                })
            
            return redirect('orcamento', orcamento_id=orcamento_id)
        
        # Tratamento específico para atualização de IPI
        if request.POST.get('ajax_update_ipi'):
            edit_item_id = request.POST.get('edit_item_id')
            if edit_item_id:
                from .models import OrcamentoItem
                from django.http import JsonResponse
                try:
                    item = OrcamentoItem.objects.get(id=edit_item_id)
                    
                    # Atualizar IPI se fornecido
                    if 'ipi' in request.POST:
                        novo_ipi = safe_float(request.POST.get('ipi', 0))
                        # Validar valor de IPI
                        if novo_ipi < 0:
                            novo_ipi = 0
                        elif novo_ipi > 100:
                            novo_ipi = 100
                        item.ipi_item = novo_ipi
                    
                    # Atualizar unidade se fornecida
                    if 'unidade' in request.POST:
                        item.unidade = request.POST.get('unidade', item.unidade)
                    
                    # Salvar item (isso irá recalcular o valor_total automaticamente)
                    item.save()
                    
                    # Atualizar totais do orçamento
                    itens = list(orcamento.itens.all())
                    orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                    orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                    orcamento.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'IPI e unidade atualizados com sucesso',
                        'novo_total': f"{item.valor_total:.2f}",
                        'total_orcamento': f"{orcamento.total_liquido:.2f}"
                    })
                except OrcamentoItem.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Item não encontrado'
                    })
                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Valor inválido: {str(e)}'
                    })
                except Exception as e:
                    # Log detalhado do erro
                    import traceback
                    error_details = traceback.format_exc()
                    print(f"❌ Erro na atualização de IPI: {error_details}")
                    
                    return JsonResponse({
                        'success': False,
                        'error': f'Erro interno: {str(e)}'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'ID do item não fornecido'
                })
        
        # Tratamento específico para atualização de LUCRO
        if request.POST.get('ajax_update_lucro'):
            edit_item_id = request.POST.get('edit_item_id')
            print(f"🔧 DEBUG: Iniciando atualização de lucro para item {edit_item_id}")
            
            if edit_item_id:
                from .models import OrcamentoItem
                from django.http import JsonResponse
                try:
                    print(f"🔍 DEBUG: Buscando item {edit_item_id}")
                    item = OrcamentoItem.objects.get(id=edit_item_id)
                    print(f"✅ DEBUG: Item encontrado: {item.descricao}")
                    
                    # Atualizar lucro se fornecido
                    if 'lucro' in request.POST:
                        novo_lucro = safe_float(request.POST.get('lucro', 0))
                        print(f"📊 DEBUG: Novo lucro recebido: {novo_lucro}%")
                        
                        # Validar valor de lucro (0-1000% para ser seguro)
                        if novo_lucro < 0:
                            novo_lucro = 0
                        elif novo_lucro > 1000:
                            novo_lucro = 1000
                        
                        print(f"✔️ DEBUG: Lucro validado: {novo_lucro}%")
                        
                        # O campo desconto_item representa o lucro percentual
                        item.desconto_item = novo_lucro
                        print(f"💾 DEBUG: Campo desconto_item atualizado para {item.desconto_item}")
                    
                    # Salvar item (isso irá recalcular o valor_total automaticamente)
                    print(f"💿 DEBUG: Salvando item...")
                    item.save()
                    print(f"✅ DEBUG: Item salvo com sucesso. Novo valor_total: {item.valor_total}")
                    
                    # Atualizar totais do orçamento
                    print(f"🔢 DEBUG: Atualizando totais do orçamento...")
                    itens = list(orcamento.itens.all())
                    orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                    orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                    orcamento.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Lucro atualizado com sucesso',
                        'novo_total': f"{item.valor_total:.2f}",
                        'total_orcamento': f"{orcamento.total_liquido:.2f}",
                        'lucro_percentual': f"{item.desconto_item:.2f}"
                    })
                except OrcamentoItem.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Item não encontrado'
                    })
                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Valor inválido: {str(e)}'
                    })
                except Exception as e:
                    # Log detalhado do erro
                    import traceback
                    error_details = traceback.format_exc()
                    print(f"❌ Erro na atualização de lucro: {error_details}")
                    
                    return JsonResponse({
                        'success': False,
                        'error': f'Erro interno: {str(e)}'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'ID do item não fornecido'
                })
        
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
                
                # Se for uma requisição AJAX, retornar JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': True, 'message': 'Item excluído com sucesso'})
                
                return redirect('orcamento', orcamento_id=orcamento_id)
            except OrcamentoItem.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': False, 'error': 'Item não encontrado'})
                pass
        else:
            # Adição de novo item
            produto_id = request.POST.get('produto_id')
            produto_parametrizado = request.POST.get('produto_parametrizado')
            quantidade = request.POST.get('quantidade')
            lucro = request.POST.get('lucro') or 0  # padrão 0% de lucro
            imposto = request.POST.get('imposto') or 0
            
            # Debug para verificar o valor do lucro recebido
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"🔍 DEBUG - Lucro recebido: '{request.POST.get('lucro')}' -> convertido: {lucro}")
            
            if produto_parametrizado:
                # Processar produto parametrizado
                try:
                    import logging
                    logger = logging.getLogger(__name__)
                    
                    data = json.loads(produto_parametrizado)
                    descricao = data.get('nome', 'Produto Parametrizado')
                    
                    logger.info(f"🔍 DEBUG - Processando produto parametrizado: {descricao}")
                    logger.info(f"🔍 DEBUG - Data recebida: {data}")
                    
                    # Validar e converter valores
                    custo_unitario = safe_float(data.get('preco_total', 0))  # agora é custo
                    quantidade_valor = safe_float(quantidade, 1.0)
                    lucro_num = safe_float(lucro)
                    imposto_num = safe_float(imposto)
                    
                    logger.info(f"🔍 DEBUG - Valores: custo={custo_unitario}, qtd={quantidade_valor}, lucro={lucro_num}%")
                    
                    # Calcular valor de venda baseado no lucro sobre o custo
                    valor_lucro_unitario = custo_unitario * (lucro_num / 100)
                    valor_venda_unitario = custo_unitario + valor_lucro_unitario
                    
                    valor_bruto = valor_venda_unitario * quantidade_valor
                    valor_imposto = valor_bruto * (imposto_num / 100)
                    valor_total = valor_bruto + valor_imposto
                    
                    # Guardar lucro total no campo desconto_item para compatibilidade
                    valor_lucro_total = valor_lucro_unitario * quantidade_valor
                    
                    from .models import OrcamentoItem
                    
                    # Obter produto se produto_id foi fornecido
                    produto_obj = None
                    if produto_id:
                        try:
                            produto_obj = MP_Produtos.objects.get(id=produto_id)
                        except MP_Produtos.DoesNotExist:
                            pass
                    
                    item = OrcamentoItem.objects.create(
                        orcamento=orcamento,
                        produto=produto_obj,  # relacionar com o produto
                        tipo_item='Parametrizado',
                        descricao=descricao,
                        quantidade=quantidade_valor,
                        valor_unitario=custo_unitario,  # guarda o custo unitário
                        desconto_item=valor_lucro_total,  # guarda o lucro total
                        imposto_item=valor_imposto,
                        valor_total=valor_total,
                        unidade=produto_obj.unidade if produto_obj else 'UN'  # usar unidade do produto
                    )
                    
                    logger.info(f"✅ Item criado com sucesso: ID={item.id}, Descrição={item.descricao}")
                    
                    # Atualiza totais do orçamento
                    itens = list(orcamento.itens.all())
                    orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                    orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                    orcamento.save()
                    
                    logger.info(f"✅ Orçamento atualizado com {len(itens)} itens")
                    return redirect('orcamento', orcamento_id=orcamento_id)
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"❌ Erro ao processar produto parametrizado: {str(e)}")
                    logger.exception("Detalhes do erro:")
                    # Em caso de erro, continue para o processamento normal
                    pass
            elif produto_id and quantidade:
                produto = MP_Produtos.objects.get(id=produto_id)
                custo_unitario = produto.custo_centavos / 100.0
                
                # Validar e converter quantidade
                quantidade_num = safe_float(quantidade, 1.0)
                
                # Validar e converter lucro
                lucro_num = safe_float(request.POST.get('lucro', 0))  # padrão 0%
                
                # Validar e converter imposto
                imposto_num = safe_float(imposto)
                
                # Calcular valor de venda baseado no lucro sobre o custo
                valor_lucro_unitario = custo_unitario * (lucro_num / 100)
                valor_venda_unitario = custo_unitario + valor_lucro_unitario
                
                valor_bruto = valor_venda_unitario * quantidade_num
                valor_imposto = valor_bruto * (imposto_num / 100)
                valor_total = valor_bruto + valor_imposto
                
                # Lucro total
                valor_lucro_total = valor_lucro_unitario * quantidade_num
                
                from .models import OrcamentoItem
                OrcamentoItem.objects.create(
                    orcamento=orcamento,
                    produto=produto,  # relacionar com o produto
                    tipo_item='Produto',
                    descricao=produto.descricao,
                    quantidade=quantidade_num,
                    valor_unitario=custo_unitario,  # guardar custo
                    desconto_item=valor_lucro_total,  # guardar lucro
                    imposto_item=valor_imposto,
                    valor_total=valor_total,
                    unidade=produto.unidade  # usar unidade do produto da base MP
                )
                # Atualiza totais do orçamento
                itens = list(orcamento.itens.all())
                orcamento.total_liquido = sum([safe_float(i.valor_total) for i in itens])
                orcamento.desconto_total = sum([safe_float(i.desconto_item) for i in itens])
                orcamento.save()
                return redirect('orcamento', orcamento_id=orcamento_id)

    # Calcula total_liquido e total_lucro dos itens
    total_liquido = sum([safe_float(item.valor_total) for item in itens])
    total_lucro = sum([safe_float(item.desconto_item) for item in itens])  # agora representa lucro

    return render(request, 'main/orcamento.html', {
        'orcamento': orcamento,
        'itens': itens,
        'produtos': produtos,
        'total_liquido': total_liquido,
        'total_lucro': total_lucro
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
                
                # Aplicar nova fórmula: ((mo_pultrusao / 3) * n° de máquinas) / (VELOCIDADE M/H * N° MATRIZES * 24 * 21 * 0,85)
                if velocidade_m_h > 0 and num_matrizes > 0:
                    numerador = (mo_pultrusao / 3) * num_maquinas_utilizadas
                    denominador = velocidade_m_h * num_matrizes * 24 * 21 * 0.85
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
                    print(f"\nFórmula: ((mo_pultrusao / 3) * n° máquinas) / (velocidade * n° matrizes * 24 * 21 * 0.85)")
                    print(f"   Numerador = ({mo_pultrusao} / 3) * {num_maquinas_utilizadas} = {numerador:.2f}")
                    print(f"   Denominador = {velocidade_m_h} * {num_matrizes} * 24 * 21 * 0.85 = {denominador}")
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


def ajax_update_lucro(request, orcamento_id):
    """Atualizar lucro de um item via AJAX"""
    print(f"🔧 DEBUG: Iniciando atualização de lucro para orçamento {orcamento_id}")
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})
    
    try:
        print(f"🔍 DEBUG: Buscando item")
        item_id = request.POST.get('edit_item_id')
        novo_lucro = safe_float(request.POST.get('lucro', 0))
        
        print(f"✅ DEBUG: Item ID: {item_id}, Novo lucro: {novo_lucro}")
        
        # Buscar o item
        from .models import OrcamentoItem
        item = OrcamentoItem.objects.get(id=item_id, orcamento_id=orcamento_id)
        print(f"✅ DEBUG: Item encontrado: {item.descricao}")
        
        # Atualizar o desconto_item (que representa o lucro)
        item.desconto_item = novo_lucro
        print(f"📊 DEBUG: Novo lucro definido: {item.desconto_item}")
        
        # Salvar - isso vai acionar o método save() com os cálculos
        print(f"💾 DEBUG: Salvando item")
        item.save()
        print(f"✅ DEBUG: Item salvo com valor total: {item.valor_total}")
        
        # Recalcular totais do orçamento
        print(f"🔄 DEBUG: Recalculando totais do orçamento")
        orcamento = item.orcamento
        total_itens = sum(item.valor_total for item in orcamento.itens.all())
        print(f"📊 DEBUG: Total recalculado: {total_itens}")
        
        return JsonResponse({
            'success': True,
            'item_total': float(item.valor_total),
            'total_orcamento': float(total_itens),
            'message': 'Lucro atualizado com sucesso'
        })
        
    except OrcamentoItem.DoesNotExist:
        print(f"❌ DEBUG: Item não encontrado")
        return JsonResponse({
            'success': False,
            'error': 'Item não encontrado'
        })
    except Exception as e:
        print(f"❌ DEBUG: Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def ajax_update_ipi(request, orcamento_id):
    """Atualizar IPI de um item via AJAX"""
    print(f"🔧 DEBUG: Iniciando atualização de IPI para orçamento {orcamento_id}")
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})
    
    try:
        print(f"🔍 DEBUG: Buscando item")
        item_id = request.POST.get('edit_item_id')
        novo_ipi = safe_float(request.POST.get('ipi', 0))
        
        print(f"✅ DEBUG: Item ID: {item_id}, Novo IPI: {novo_ipi}")
        
        # Buscar o item
        from .models import OrcamentoItem
        item = OrcamentoItem.objects.get(id=item_id, orcamento_id=orcamento_id)
        print(f"✅ DEBUG: Item encontrado: {item.descricao}")
        
        # Atualizar o IPI
        item.ipi_item = novo_ipi
        print(f"📊 DEBUG: Novo IPI definido: {item.ipi_item}")
        
        # Salvar - isso vai acionar o método save() com os cálculos
        print(f"💾 DEBUG: Salvando item")
        item.save()
        print(f"✅ DEBUG: Item salvo com valor total: {item.valor_total}")
        
        # Recalcular totais do orçamento
        print(f"🔄 DEBUG: Recalculando totais do orçamento")
        orcamento = item.orcamento
        total_itens = sum(item.valor_total for item in orcamento.itens.all())
        print(f"📊 DEBUG: Total recalculado: {total_itens}")
        
        return JsonResponse({
            'success': True,
            'novo_total': float(item.valor_total),
            'total_orcamento': float(total_itens),
            'message': 'IPI atualizado com sucesso'
        })
        
    except OrcamentoItem.DoesNotExist:
        print(f"❌ DEBUG: Item não encontrado")
        return JsonResponse({
            'success': False,
            'error': 'Item não encontrado'
        })
    except Exception as e:
        print(f"❌ DEBUG: Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
