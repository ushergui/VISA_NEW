from django.shortcuts import render, redirect, get_object_or_404
from .models import Contabilidade, Cnae, Empresas, Risco, Legislacao, ProtocoloEmpresa, Inspecao, AcaoProdutividade, Produtividade, FiscalAuxiliarRel, AcaoProdutividadeRel
from .forms import ContabilidadeForm, CnaeForm, EmpresasForm, RiscoForm, LegislacaoForm, ProtocoloEmpresaForm, InspecaoForm, ProdutividadeAcaoForm, ProdutividadeForm, EmpresasObservacoesForm, EmpresaCnaeForm, ProdutividadeFiscalAuxiliarForm, AcaoProdutividadeForm
from django.views import View
from django.db.models import Max
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from datetime import date, datetime
from django.db.models import Max, Subquery, OuterRef, Prefetch, Case, When, Value, CharField
from cadastros.models import Fiscal
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.db.models.functions import Concat





# Contabilidade
def listar_contabilidades(request):
    contabilidades = Contabilidade.objects.all()
    return render(request, 'empresas/listar_contabilidades.html', {'contabilidades': contabilidades})

def criar_contabilidade(request):
    form = ContabilidadeForm(request.POST or None)
    titulo = "Cadastro de Contabilidade"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_contabilidades')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def editar_contabilidade(request, id):
    contabilidade = Contabilidade.objects.get(id=id)
    form = ContabilidadeForm(request.POST or None, instance=contabilidade)
    titulo = "Edição de Contabilidade"
    botao = "Gravar"

    if form.is_valid():
        form.save()
        return redirect('listar_contabilidades')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def excluir_contabilidade(request, id):
    contabilidade = Contabilidade.objects.get(id=id)

    if request.method == 'POST':
        contabilidade.delete()
        return redirect('listar_contabilidades')

    return render(request, 'empresas/confirmar_exclusao.html', {'obj': contabilidade})

# Cnae
def listar_cnaes(request):
    cnaes = Cnae.objects.all()
    return render(request, 'empresas/listar_cnaes.html', {'cnaes': cnaes})

def criar_cnae(request):
    form = CnaeForm(request.POST or None)
    titulo = "Cadastrar CNAE"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_cnae(request, id):
    cnae = Cnae.objects.get(id=id)
    form = CnaeForm(request.POST or None, instance=cnae)
    titulo = "Edição de Cnae"
    botao = "Gravar"

    if form.is_valid():
        form.save()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def excluir_cnae(request, id):
    cnae = Cnae.objects.get(id=id)

    if request.method == 'POST':
        cnae.delete()
        return redirect('listar_cnaes')

    return render(request, 'empresas/form-excluir.html', {'obj': cnae})

# Empresas
def listar_empresas(request):
    termo_pesquisa = request.GET.get('termo_pesquisa', '')
    if termo_pesquisa:
        empresas = Empresas.objects.filter(
            Q(razao__icontains=termo_pesquisa) |
            Q(nome_fantasia__icontains=termo_pesquisa) |
            Q(cnpj__icontains=termo_pesquisa) |
            Q(responsavel_legal__icontains=termo_pesquisa)
        )
    else:
        empresas = Empresas.objects.all()

    return render(request, 'empresas/listar_empresas.html', {'empresas': empresas, 'termo_pesquisa': termo_pesquisa})


def criar_empresa(request):
    form = EmpresasForm(request.POST or None)
    titulo = "Cadastrar empresa"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('novo_protocolo')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    form = EmpresasForm(request.POST or None, instance=empresa)
    titulo = "Edição de empresa"
    botao = "Gravar"
    
    if form.is_valid():
        form.save()
        return redirect('detalhe_empresa', empresa_id=id)  # Passa o ID da empresa como argumento

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_observacoes(request, id):
    empresa = Empresas.objects.get(id=id)
    form = EmpresasObservacoesForm(request.POST or None, instance=empresa)
    titulo = f"Edição da observação"
    titulo2 = f"Empresa {empresa.razao}"
    botao = "Gravar"
    
    if form.is_valid():
        form.save()
        return redirect('detalhe_empresa', empresa_id=id)  # Passa o ID da empresa como argumento

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao, 'titulo2': titulo2})


def excluir_empresa(request, id):
    empresa = Empresas.objects.get(id=id)

    if request.method == 'POST':
        empresa.delete()
        return redirect('listar_empresas')

    return render(request, 'empresas/form-excluir.html', {'obj': empresa})

def detalhe_empresa(request, empresa_id):
    empresa = Empresas.objects.get(id=empresa_id)
    cnaes_ordenados = empresa.cnae.order_by('-risco_cnae__valor_risco')
    protocolos = ProtocoloEmpresa.objects.filter(empresa=empresa)
    
    try:
        inspecao_mais_recente = Inspecao.objects.filter(protocolo__empresa=empresa).latest('data_inspecao')
    except Inspecao.DoesNotExist:
        inspecao_mais_recente = None

    return render(request, 'empresas/detalhe_empresa.html', {'empresa': empresa, 'cnaes_ordenados': cnaes_ordenados, 'protocolos': protocolos, 'inspecao_mais_recente': inspecao_mais_recente})



def listar_risco(request):
    riscos = Risco.objects.all()
    return render(request, 'empresas/listar_risco.html', {'riscos': riscos})

def cadastrar_risco(request):
    form = RiscoForm(request.POST or None)
    titulo = "Cadastrar risco"
    botao = "Cadastrar"

    if form.is_valid():
        form.save()
        return redirect('listar_risco')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def editar_risco(request, id):
    risco = get_object_or_404(Risco, id=id)
    form = RiscoForm(request.POST or None, instance=risco)
    titulo = "Editar risco"
    botao = "Gravar"

    if form.is_valid():
        form.save()
        return redirect('listar_risco')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})

def excluir_risco(request, id):
    risco = get_object_or_404(Risco, id=id)

    if request.method == 'POST':
        risco.delete()
        return redirect('listar_risco')

    return render(request, 'empresas/form-excluir.html', {'risco': risco})

class GetRisco(View):
    def get(self, request, *args, **kwargs):
        cnaes = [int(i) for i in request.GET.getlist('cnaes')]
        max_risco = Cnae.objects.filter(id__in=cnaes).aggregate(Max('risco_cnae__valor_risco'))['risco_cnae__valor_risco__max']
        return JsonResponse({'risco': max_risco})


def listar_legislacao(request):
    legislacao = Legislacao.objects.all()
    return render(request, 'empresas/listar_legislacao.html', {'object_list': legislacao})

def criar_legislacao(request):
    form = LegislacaoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('listar_legislacao')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Nova Legislação', 'botao': 'Criar'})

def editar_legislacao(request, id):
    legislacao = Legislacao.objects.get(id=id)
    form = LegislacaoForm(request.POST or None, instance=legislacao)

    if form.is_valid():
        form.save()
        return redirect('listar_legislacao')

    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Editar Legislação', 'botao': 'Editar'})

def excluir_legislacao(request, id):
    legislacao = get_object_or_404(Legislacao, id=id)

    if request.method == 'POST':
        legislacao.delete()
        return redirect('listar_legislacao')

    return render(request, 'empresas/form-excluir.html', {'legislacao': legislacao})

def listar_protocolos(request):
    protocolos = ProtocoloEmpresa.objects.all()
    return render(request, 'empresas/listar_protocolos.html', {'protocolos': protocolos})



def novo_protocolo(request):
    if request.method == "POST":
        form = ProtocoloEmpresaForm(request.POST)
        if form.is_valid():
            protocolo = form.save()  # Salva o protocolo e obtém o objeto ProtocoloEmpresa criado
            empresa_id = protocolo.empresa_id  # Obtém o ID da empresa associada ao protocolo
            return redirect('detalhe_empresa', empresa_id=empresa_id)  # Redireciona para a página de detalhes da empresa
            
    else:
        form = ProtocoloEmpresaForm()
        
    titulo = "Cadastrar protocolo"
    botao = "Cadastrar"
    
    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


def editar_protocolo(request, id):
    protocolo = get_object_or_404(ProtocoloEmpresa, id=id)
    if request.method == "POST":
        form = ProtocoloEmpresaForm(request.POST, instance=protocolo)
        if form.is_valid():
            form.save()
            return redirect('detalhe_empresa', empresa_id=protocolo.empresa.id)
    else:
        form = ProtocoloEmpresaForm(instance=protocolo)
    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Editar protocolo', 'botao': 'Atualizar'})

   
def excluir_protocolo(request, id):
    protocolo = get_object_or_404(ProtocoloEmpresa, id=id)
    if request.method == "POST":
        protocolo.delete()
        return redirect('listar_protocolos')
    return render(request, 'empresas/form-excluir.html', {'protocolo': protocolo})

def listar_inspecao(request):
    inspecoes = Inspecao.objects.all()
    return render(request, 'empresas/listar_inspecao.html', {'inspecoes': inspecoes})

def cadastrar_inspecao(request, protocolo_id):
    protocolo = ProtocoloEmpresa.objects.get(id=protocolo_id)
    empresa_id = protocolo.empresa.id
    titulo = "Cadastro de Inspeção"
    botao = "Cadastrar"

    if request.method == "POST":
        form = InspecaoForm(request.POST, request.FILES)
        if form.is_valid():
            inspecao = form.save(commit=False)
            inspecao.protocolo = protocolo
            inspecao.save()
            return redirect('detalhe_empresa', empresa_id=empresa_id)
    else:
        form = InspecaoForm()

    return render(request, 'empresas/form-upload.html', {'form': form, 'titulo': titulo, 'botao': botao, 'protocolo': protocolo})


def alterar_inspecao(request, id):
    titulo = "Alterar Inspeção"
    botao = "Gravar"
    inspecao = Inspecao.objects.get(id=id)
    protocolo = inspecao.protocolo  # Pegando o protocolo a partir da inspeção
    empresa_id = protocolo.empresa.id  # Pegando o ID da empresa a partir do protocolo

    if request.method == "POST":
        form = InspecaoForm(request.POST, request.FILES, instance=inspecao)
        if form.is_valid():
            form.save()
            return redirect('detalhe_empresa', empresa_id=empresa_id)  # Modificado para redirecionar para detalhe_empresa
    else:
        form = InspecaoForm(instance=inspecao)

    return render(request, 'empresas/form-upload.html', {'form': form, 'titulo':titulo, 'botao':botao, 'protocolo': protocolo})  # Adicionado 'protocolo': protocolo


def excluir_inspecao(request, id):
    inspecao = Inspecao.objects.get(id=id)
    if request.method == "POST":
        inspecao.delete()
        return redirect('listar_inspecao')
    return render(request, 'empresas/form-excluir.html', {'obj': inspecao})

def listar_acao_produtividade(request):
    acoes = AcaoProdutividade.objects.all()
    return render(request, 'empresas/listar_acao_produtividade.html', {'acoes': acoes})

def criar_acao_produtividade(request):
    if request.method == "POST":
        form = AcaoProdutividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_acao_produtividade')
    else:
        form = AcaoProdutividadeForm()
    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Criar Ação de Produtividade', 'botao': 'Salvar'})

def editar_acao_produtividade(request, id):
    acao = get_object_or_404(AcaoProdutividade, id=id)
    if request.method == "POST":
        form = AcaoProdutividadeForm(request.POST, instance=acao)
        if form.is_valid():
            form.save()
            return redirect('listar_acao_produtividade')
    else:
        form = AcaoProdutividadeForm(instance=acao)
    return render(request, 'empresas/form.html', {'form': form, 'titulo': 'Editar Ação de Produtividade', 'botao': 'Atualizar'})

def excluir_acao_produtividade(request, id):
    acao = get_object_or_404(AcaoProdutividade, id=id)
    if request.method == "POST":
        acao.delete()
        return redirect('listar_acao_produtividade')
    return render(request, 'empresas/form-excluir.html', {'obj': acao})

def listar_produtividade(request):
    produtividades = Produtividade.objects.all()
    return render(request, 'empresas/listar_produtividade.html', {'produtividades': produtividades})

def CreateProdutividade(request, inspecao_id):
    inspecao = Inspecao.objects.get(id=inspecao_id)
    ProdutividadeAcaoFormSet = formset_factory(ProdutividadeAcaoForm, extra=1)
    ProdutividadeFiscalAuxiliarFormSet = formset_factory(ProdutividadeFiscalAuxiliarForm, extra=1)
    
    if request.method == 'POST':
        form = ProdutividadeForm(request.POST)
        acao_formset = ProdutividadeAcaoFormSet(request.POST, prefix='acoes')
        fiscal_formset = ProdutividadeFiscalAuxiliarFormSet(request.POST, prefix='fiscais')
        
        if form.is_valid() and acao_formset.is_valid() and fiscal_formset.is_valid():
            produtividade = form.save(commit=False)
            produtividade.inspecao = inspecao
            produtividade.save()
            
            for acao_form in acao_formset:
                prod_acao = acao_form.save(commit=False)
                prod_acao.produtividade = produtividade
                prod_acao.save()
                
            for fiscal_form in fiscal_formset:
                prod_fiscal = fiscal_form.save(commit=False)
                prod_fiscal.produtividade = produtividade
                prod_fiscal.save()

            return redirect('empresas/listar_produtividade.html')
            
    else:
        form = ProdutividadeForm(initial={'inspecao': inspecao})
        acao_formset = ProdutividadeAcaoFormSet(prefix='acoes')
        fiscal_formset = ProdutividadeFiscalAuxiliarFormSet(prefix='fiscais')
        
    return render(request, 'empresas/form-produtividade.html', {'form': form, 'acao_formset': acao_formset, 'fiscal_formset': fiscal_formset})

def get_pontos(request):
    acao_id = request.GET.get('acao_id', None)
    pontos = 0
    if acao_id is not None:
        try:
            acao = AcaoProdutividade.objects.get(id=acao_id)
            pontos = acao.pontos
        except AcaoProdutividade.DoesNotExist:
            pass
    return JsonResponse({'pontos': str(pontos)})

def listar_produtividade(request):
    produtividades = Produtividade.objects.all()
    return render(request, 'empresas/listar_produtividade.html', {'produtividades': produtividades})

def excluir_produtividade(request, id):
    produtividade = get_object_or_404(Produtividade, id=id)
    if request.method == "POST":
        produtividade.delete()
        return redirect('listar_produtividade')
    return render(request, 'empresas/form-excluir.html', {'obj': produtividade})


class EmpresasCnaeListView(ListView):
    model = Empresas
    template_name = 'empresas/lista_empresas_cnae.html'
    context_object_name = 'empresas'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            empresas = Empresas.objects.filter(
                Q(cnae_principal__codigo_cnae__icontains=query) |
                Q(cnae_principal__descricao_cnae__icontains=query)
            ).distinct()

            return empresas.order_by('razao')
        else:
            return Empresas.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')

        if query:
            empresas = Empresas.objects.filter(
                Q(cnae_principal__codigo_cnae__icontains=query) |
                Q(cnae_principal__descricao_cnae__icontains=query)
            ).distinct()

            context['total_registros'] = empresas.count()

        return context
    
class EmpresasEnderecoListView(ListView):
    model = Empresas
    template_name = 'empresas/lista_empresas_endereco.html'
    context_object_name = 'empresas'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            empresas = Empresas.objects.filter(
                Q(logradouro_empresa__nome_logradouro__icontains=query) |
                Q(numero_empresa__icontains=query) |
                Q(logradouro_empresa__bairro__nome_bairro__icontains=query) |
                Q(cnae_principal__codigo_cnae__icontains=query) |
                Q(cnae_principal__descricao_cnae__icontains=query)
            ).distinct()

            return empresas.order_by('razao')
        else:
            return Empresas.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')

        if query:
            empresas = Empresas.objects.filter(
                Q(logradouro_empresa__nome_logradouro__icontains=query) |
                Q(numero_empresa__icontains=query) |
                Q(logradouro_empresa__bairro__nome_bairro__icontains=query) |
                Q(cnae_principal__codigo_cnae__icontains=query) |
                Q(cnae_principal__descricao_cnae__icontains=query)
            ).distinct()

            context['total_registros'] = empresas.count()

        return context


def empresas_endereco_pdf(request):
    # Recupera o parâmetro da URL
    query = request.GET.get('q')
    # Inicia a query como vazia
    empresas = Empresas.objects.none()

    if query:
        # Faz a consulta caso a query tenha sido preenchida
        empresas = Empresas.objects.filter(
            Q(logradouro_empresa__nome_logradouro__icontains=query) |
            Q(numero_empresa__icontains=query) |
            Q(logradouro_empresa__bairro__nome_bairro__icontains=query) 
        ).distinct().order_by(
            'cnae_principal__descricao_cnae', 
            'logradouro_empresa__bairro__nome_bairro', 
            'logradouro_empresa__nome_logradouro', 
            'numero_empresa'
        )

    context = {
        'empresas': empresas,
        'total_registros': empresas.count(),
    }
    
    # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('empresas/empresas_endereco_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=empresas_endereco_pdf.html'
    return response



def empresas_cnae_pdf(request):
    # Recupera o parâmetro da URL
    query = request.GET.get('q')
    # Inicia a query como vazia
    empresas = Empresas.objects.none()

    if query:
        # Faz a consulta caso a query tenha sido preenchida
        empresas = Empresas.objects.filter(
            Q(cnae_principal__codigo_cnae__icontains=query) |
            Q(cnae_principal__descricao_cnae__icontains=query)
        ).distinct().order_by(
            'cnae_principal__descricao_cnae', 
            'logradouro_empresa__bairro__nome_bairro', 
            'logradouro_empresa__nome_logradouro', 
            'numero_empresa'
        )

    context = {
        'empresas': empresas,
        'total_registros': empresas.count(),
    }
    
    # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('empresas/empresas_cnae_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=empresas_cnae_pdf.html'
    return response


def editar_empresa_cnae(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = "Edição Cnae principal"
    botao = "Gravar"
    if request.method == "POST":
        form = EmpresaCnaeForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('listar_empresas2')
    else:
        form = EmpresaCnaeForm(instance=empresa)
    return render(request, 'empresas/form.html', {'form': form, 'titulo': titulo, 'botao': botao})


class EmpresasView(TemplateView):
    template_name = 'empresas/empresas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nivel_risco_i'] = Empresas.objects.filter(Q(status_funcionamento='ATIVA') | Q(status_funcionamento='DISPENSADA'),cnae_principal__risco_cnae__valor_risco=3).count()
        context['executado_i'] = Empresas.objects.filter(cnae_principal__risco_cnae__valor_risco=3, protocoloempresa__inspecao__data_inspecao__range=(datetime(2023, 1, 1), datetime(2023, 12, 31))).count()
        context['porcentagem_i'] = round(context['executado_i'] / context['nivel_risco_i'] * 100, 1) if context['nivel_risco_i'] > 0 else 0

        context['nivel_risco_ii'] = Empresas.objects.filter(cnae_principal__risco_cnae__valor_risco=4).count()
        context['executado_ii'] = Empresas.objects.filter(cnae_principal__risco_cnae__valor_risco=4, protocoloempresa__inspecao__data_inspecao__range=(datetime(2023, 1, 1), datetime(2023, 12, 31))).count()
        context['porcentagem_ii'] = round(context['executado_ii'] / context['nivel_risco_ii'] * 100, 1) if context['nivel_risco_ii'] > 0 else 0

        context['nivel_risco_iii'] = Empresas.objects.filter(cnae_principal__risco_cnae__valor_risco=5).count()
        context['executado_iii'] = Empresas.objects.filter(cnae_principal__risco_cnae__valor_risco=5, protocoloempresa__inspecao__data_inspecao__range=(datetime(2023, 1, 1), datetime(2023, 12, 31))).count()
        context['porcentagem_iii'] = round(context['executado_iii'] / context['nivel_risco_iii'] * 100, 1) if context['nivel_risco_iii'] > 0 else 0

        return context
    

def listar_risco_um(request):
    ultimo_protocolo_subquery = ProtocoloEmpresa.objects.filter(
        empresa=OuterRef('pk')
    ).order_by(
        '-inspecao__data_inspecao'
    ).values('inspecao__data_inspecao')[:1]

    empresas = Empresas.objects.filter(
        Q(status_funcionamento='ATIVA') | Q(status_funcionamento='DISPENSADA'),
        cnae_principal__risco_cnae__valor_risco=3
    ).annotate(
        inspecao_mais_recente=Subquery(ultimo_protocolo_subquery),
        status_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
             ).order_by('-entrada_fiscal').values('status_protocolo')[:1]
        ),
        numero_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
            ).order_by('-entrada_fiscal').values('numero_protocolo')[:1]
         ),
         primeiro_nome_fiscal=Subquery(
             ProtocoloEmpresa.objects.filter(
             empresa=OuterRef('pk')
         ).order_by('-entrada_fiscal').values('fiscal_responsavel__primeiro_nome')[:1]
         ),
     ).annotate(
         protocolo_aberto_fiscal=Case(
         When(status_protocolo=4, then=Value('')),
         default=Concat('numero_protocolo', Value(' - '), 'primeiro_nome_fiscal'),
         output_field=CharField()
         )
     ).order_by('cnae_principal__descricao_cnae', 'razao')

    return render(request, 'empresas/listar_riscos_um.html', {'empresas': empresas})



def listar_risco_um_pdf(request):
    ultimo_protocolo_subquery = ProtocoloEmpresa.objects.filter(
        empresa=OuterRef('pk')
    ).order_by(
        '-inspecao__data_inspecao'
    ).values('inspecao__data_inspecao')[:1]

    empresas = Empresas.objects.filter(
        Q(status_funcionamento='ATIVA') | Q(status_funcionamento='DISPENSADA'),
        cnae_principal__risco_cnae__valor_risco=3
    ).annotate(
        inspecao_mais_recente=Subquery(ultimo_protocolo_subquery),
        status_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
             ).order_by('-entrada_fiscal').values('status_protocolo')[:1]
        ),
        numero_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
            ).order_by('-entrada_fiscal').values('numero_protocolo')[:1]
         ),
         primeiro_nome_fiscal=Subquery(
             ProtocoloEmpresa.objects.filter(
             empresa=OuterRef('pk')
         ).order_by('-entrada_fiscal').values('fiscal_responsavel__primeiro_nome')[:1]
         ),
     ).annotate(
         protocolo_aberto_fiscal=Case(
         When(status_protocolo=4, then=Value('')),
         default=Concat('numero_protocolo', Value(' - '), 'primeiro_nome_fiscal'),
         output_field=CharField()
         )
     ).order_by('cnae_principal__descricao_cnae', 'razao')

    context = {
        'empresas': empresas,
    }

    html_template = get_template('empresas/listar_riscos_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=empresas_cnae_pdf.html'
    return response

def listar_risco_dois(request):
    ultimo_protocolo_subquery = ProtocoloEmpresa.objects.filter(
        empresa=OuterRef('pk')
    ).order_by(
        '-inspecao__data_inspecao'
    ).values('inspecao__data_inspecao')[:1]

    empresas = Empresas.objects.filter(
        Q(status_funcionamento='ATIVA'),
        cnae_principal__risco_cnae__valor_risco=4
    ).annotate(
        inspecao_mais_recente=Subquery(ultimo_protocolo_subquery),
        status_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
             ).order_by('-entrada_fiscal').values('status_protocolo')[:1]
        ),
        numero_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
            ).order_by('-entrada_fiscal').values('numero_protocolo')[:1]
         ),
         primeiro_nome_fiscal=Subquery(
             ProtocoloEmpresa.objects.filter(
             empresa=OuterRef('pk')
         ).order_by('-entrada_fiscal').values('fiscal_responsavel__primeiro_nome')[:1]
         ),
     ).annotate(
         protocolo_aberto_fiscal=Case(
         When(status_protocolo=4, then=Value('')),
         default=Concat('numero_protocolo', Value(' - '), 'primeiro_nome_fiscal'),
         output_field=CharField()
         )
     ).order_by('cnae_principal__descricao_cnae', 'razao')

    return render(request, 'empresas/listar_riscos_dois.html', {'empresas': empresas})


def listar_risco_dois_pdf(request):
    ultimo_protocolo_subquery = ProtocoloEmpresa.objects.filter(
        empresa=OuterRef('pk')
    ).order_by(
        '-inspecao__data_inspecao'
    ).values('inspecao__data_inspecao')[:1]

    empresas = Empresas.objects.filter(
        Q(status_funcionamento='ATIVA'),
        cnae_principal__risco_cnae__valor_risco=4
    ).annotate(
        inspecao_mais_recente=Subquery(ultimo_protocolo_subquery),
        status_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
             ).order_by('-entrada_fiscal').values('status_protocolo')[:1]
        ),
        numero_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
            ).order_by('-entrada_fiscal').values('numero_protocolo')[:1]
         ),
         primeiro_nome_fiscal=Subquery(
             ProtocoloEmpresa.objects.filter(
             empresa=OuterRef('pk')
         ).order_by('-entrada_fiscal').values('fiscal_responsavel__primeiro_nome')[:1]
         ),
     ).annotate(
         protocolo_aberto_fiscal=Case(
         When(status_protocolo=4, then=Value('')),
         default=Concat('numero_protocolo', Value(' - '), 'primeiro_nome_fiscal'),
         output_field=CharField()
         )
     ).order_by('cnae_principal__descricao_cnae', 'razao')

    context = {
        'empresas': empresas,
    }

    html_template = get_template('empresas/listar_riscos_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=empresas_cnae_pdf.html'
    return response


def listar_risco_tres(request):
    ultimo_protocolo_subquery = ProtocoloEmpresa.objects.filter(
        empresa=OuterRef('pk')
    ).order_by(
        '-inspecao__data_inspecao'
    ).values('inspecao__data_inspecao')[:1]

    empresas = Empresas.objects.filter(
        Q(status_funcionamento='ATIVA'),
        cnae_principal__risco_cnae__valor_risco=5
    ).annotate(
        inspecao_mais_recente=Subquery(ultimo_protocolo_subquery),
        status_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
             ).order_by('-entrada_fiscal').values('status_protocolo')[:1]
        ),
        numero_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
            ).order_by('-entrada_fiscal').values('numero_protocolo')[:1]
         ),
         primeiro_nome_fiscal=Subquery(
             ProtocoloEmpresa.objects.filter(
             empresa=OuterRef('pk')
         ).order_by('-entrada_fiscal').values('fiscal_responsavel__primeiro_nome')[:1]
         ),
     ).annotate(
         protocolo_aberto_fiscal=Case(
         When(status_protocolo=4, then=Value('')),
         default=Concat('numero_protocolo', Value(' - '), 'primeiro_nome_fiscal'),
         output_field=CharField()
         )
     ).order_by('cnae_principal__descricao_cnae', 'razao')

    return render(request, 'empresas/listar_riscos_tres.html', {'empresas': empresas})


def listar_risco_tres_pdf(request):
    ultimo_protocolo_subquery = ProtocoloEmpresa.objects.filter(
        empresa=OuterRef('pk')
    ).order_by(
        '-inspecao__data_inspecao'
    ).values('inspecao__data_inspecao')[:1]

    empresas = Empresas.objects.filter(
        Q(status_funcionamento='ATIVA'),
        cnae_principal__risco_cnae__valor_risco=5
    ).annotate(
        inspecao_mais_recente=Subquery(ultimo_protocolo_subquery),
        status_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
             ).order_by('-entrada_fiscal').values('status_protocolo')[:1]
        ),
        numero_protocolo=Subquery(
            ProtocoloEmpresa.objects.filter(
                empresa=OuterRef('pk')
            ).order_by('-entrada_fiscal').values('numero_protocolo')[:1]
         ),
         primeiro_nome_fiscal=Subquery(
             ProtocoloEmpresa.objects.filter(
             empresa=OuterRef('pk')
         ).order_by('-entrada_fiscal').values('fiscal_responsavel__primeiro_nome')[:1]
         ),
     ).annotate(
         protocolo_aberto_fiscal=Case(
         When(status_protocolo=4, then=Value('')),
         default=Concat('numero_protocolo', Value(' - '), 'primeiro_nome_fiscal'),
         output_field=CharField()
         )
     ).order_by('cnae_principal__descricao_cnae', 'razao')

    context = {
        'empresas': empresas,
    }

    html_template = get_template('empresas/listar_riscos_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=empresas_cnae_pdf.html'
    return response


def listar_vigiriscos_2023(request):
    inspecoes_2023 = Inspecao.objects.filter(data_inspecao__year=2023)
    protocolos_com_inspecoes_2023 = ProtocoloEmpresa.objects.filter(
        inspecao__in=inspecoes_2023
    )
    empresas = Empresas.objects.prefetch_related(
        Prefetch('protocoloempresa_set', queryset=protocolos_com_inspecoes_2023, to_attr='protocolos_2023')
    ).order_by('razao')
    context = {'empresas': empresas}
    return render(request, 'empresas/listar_vigiriscos_2023.html', context)


def listar_vigiriscos_2023_pdf(request):
    inspecoes_2023 = Inspecao.objects.filter(data_inspecao__year=2023)
    protocolos_com_inspecoes_2023 = ProtocoloEmpresa.objects.filter(
        inspecao__in=inspecoes_2023
    )
    empresas = Empresas.objects.prefetch_related(
        Prefetch('protocoloempresa_set', queryset=protocolos_com_inspecoes_2023, to_attr='protocolos_2023')
    ).order_by('razao')
    context = {'empresas': empresas}
    html_template = get_template('empresas/listar_vigiriscos_2023_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=vigiriscos_2023_pdf.html'
    return response


