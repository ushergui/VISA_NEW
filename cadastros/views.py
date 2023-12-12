from django.forms import forms
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseDetailView
from django.views.generic.list import ListView
from django.db.models import Q
from django.db.models import F
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from braces.views import LoginRequiredMixin
from datetime import datetime, date
from .models import Estado, Cidade, Bairro, Logradouro, Proprietario, Terreno, Protocolo, Infracao, Inspecao, Fiscal, FeriadoRecesso, ValorVRM
# Método para redirecionar o usuário após ele efetuar um cadastro
from django.urls import reverse_lazy
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # Importa views que protege o acesso de usuário não autenticado
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import admin
from .forms import LogradouroForm, LogradouroUpdateForm, ProprietarioForm, ProprietarioUpdateForm, \
    ProtocoloForm, ProtocoloUpdateForm, TerrenoForm, TerrenoUpdateForm, InspecaoForm, InspecaoUpdateForm, \
    InfracaoCreateForm, InfracaoUpdateForm, FeriadoRecessoForm, InfracaoForm, InfracaoFormDefesa, ARForm, ValorVRMForm, ReinspecaoForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from datetime import timedelta
from django.http import QueryDict
from django.views import View
from decimal import Decimal




def get_queryset(self):
    txt_nome = self.request.GET.get('nome')

    if txt_nome:
        terrenos = Terreno.objects.filter(inscricao__icontains=txt_nome)
    else:
        terrenos = Terreno.objects.all()

    return terrenos


class ProtocoloDetalhes(LoginRequiredMixin, DetailView):
    model = Protocolo
    template_name = 'detalhes-protocolo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        protocolo = self.object

        inspecoes = Inspecao.objects.filter(protocolo=protocolo).order_by('-data_inspecao1')
        infracoes = Infracao.objects.filter(inspecao__protocolo=protocolo).order_by('-id')

        context['inspecoes'] = inspecoes
        context['infracoes'] = infracoes

        return context

class InspecaoDetalhes(LoginRequiredMixin, DetailView):
    model = Inspecao
    template_name = 'detalhes-inspecao.html'

class InfracaoDetalhes(LoginRequiredMixin, DetailView):
    model = Infracao
    template_name = 'detalhes-infracao.html'


class EstadoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Estado
    fields = ['nome_estado', 'sigla_estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-estados')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de estado"
        context['botao'] = "Cadastrar"
        return context


class CidadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Cidade
    fields = ['nome_cidade', 'estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-cidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de cidade"
        context['botao'] = "Cadastrar"
        return context


class BairroCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Bairro
    fields = ['nome_bairro', 'cidade']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-bairros')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de bairro"
        context['botao'] = "Cadastrar"
        return context


class LogradouroCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Logradouro
    form_class = LogradouroForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-logradouros')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastros de logradouro"
        context['botao'] = "Cadastrar"
        return context



class ProprietarioCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Proprietario
    form_class = ProprietarioForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-proprietarios')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de proprietário"
        context['botao'] = "Cadastrar"
        return context

class TerrenoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Terreno
    form_class = TerrenoForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-terrenos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de terreno"
        context['botao'] = "Cadastrar"
        return context

class ProtocoloCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Protocolo
    form_class = ProtocoloForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-protocolos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de protocolo"
        context['botao'] = "Cadastrar"
        return context


class FiscalCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Fiscal
    fields = ['nome_fiscal', 'matricula_fiscal', 'nivel', 'primeiro_nome']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-fiscais')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de fiscal"
        context['botao'] = "Cadastrar"
        return context


class InspecaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Inspecao
    form_class = InspecaoForm
    template_name = 'form-upload.html'
    ordering = ['terreno']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastro de inspeção"
        context['botao'] = "Cadastrar"
        return context

    def form_valid(self, form):
        inspecao = form.save(commit=False)
        if not inspecao.limpo:
            # se o atributo limpo estiver vazio, redireciona para a página de cadastro de infrações
            inspecao.save()
            return redirect('cadastrar-infracao')
        else:
            inspecao.save()
            pk = inspecao.pk # id da inspeção criada
            return redirect('detalhes-inspecao', pk=pk)

    def get_success_url(self):
        # redireciona para listar-inspecoes quando o formulário for válido
        return reverse('listar-inspecoes')



class InfracaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Infracao
    form_class = InfracaoCreateForm
    template_name = 'form5.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            data_auto_str = self.request.POST.get('data_auto')
            data_auto = datetime.strptime(data_auto_str, "%d/%m/%Y").date()
        else:
            data_auto = datetime.today().date()

        is_pre_june_2023 = data_auto <= date(2023, 6, 2)

        context['is_pre_june_2023'] = is_pre_june_2023
        context['titulo'] = "Cadastro de infração"
        context['botao'] = "Cadastrar"
        return context

    def get_success_url(self):
        return reverse('detalhes-infracao', kwargs={'pk': self.object.pk})
    
def verificar_infracao_existente(request):
    inscricao = request.GET.get('inscricao', None)
    if not inscricao:
        return JsonResponse({'status': 'fail', 'message': 'Inscrição não fornecida'})

    try:
        ultima_infracao = Infracao.objects.filter(inspecao__terreno__inscricao=inscricao).latest('data_auto')
        data = {
            'status': 'found',
            'data_auto': ultima_infracao.data_auto.strftime('%d/%m/%Y'),
            'numero_format_ano': ultima_infracao.numero_format_ano,
            'julgamento': ultima_infracao.julgamento.strftime('%d/%m/%Y') if ultima_infracao.julgamento else None,
        }
        return JsonResponse(data)
    except Infracao.DoesNotExist:
        return JsonResponse({'status': 'not_found'})

def get_terreno_inscricao(request):
    inspecao_id = request.GET.get('inspecao_id')
    try:
        inspecao = Inspecao.objects.get(pk=inspecao_id)
        terreno_inscricao = inspecao.terreno.inscricao
        return JsonResponse({'inscricao': terreno_inscricao})
    except Inspecao.DoesNotExist:
        return JsonResponse({'error': 'Inspeção não encontrada'}, status=404)
        
class GetTerrenoObservacoes(View):
    def get(self, request, *args, **kwargs):
        inspecao_id = request.GET.get('inspecao_id', None)
        observacoes = ''
        if inspecao_id:
            inspecao = get_object_or_404(Inspecao, id=inspecao_id)
            observacoes = inspecao.terreno.observacoes_terreno
        return JsonResponse({'observacoes': observacoes})

class EstadoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Estado
    fields = ['nome_estado', 'sigla_estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-estados')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de estado"
        context["botao"] = "Gravar"

        return context


class CidadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Cidade
    fields = ['nome_cidade', 'estado']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-cidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de cidade"
        context["botao"] = "Gravar"

        return context


class BairroUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Bairro
    fields = ['nome_bairro', 'cidade']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-bairros')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de bairro"
        context["botao"] = "Gravar"

        return context


class LogradouroUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Logradouro
    form_class = LogradouroUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-logradouros')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de logradouro"
        context["botao"] = "Gravar"
        return context


class ProprietarioUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Proprietario
    form_class = ProprietarioUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-proprietarios')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de proprietário"
        context["botao"] = "Gravar"
        return context

class TerrenoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Terreno
    form_class = TerrenoUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-terrenos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = "Edição de terreno"
        context["botao"] = "Gravar"
        return context

class ProtocoloUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Protocolo
    form_class = ProtocoloUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('listar-protocolos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de protocolo"
        context["botao"] = "Gravar"
        return context

class FiscalUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Fiscal
    fields = ['nome_fiscal', 'matricula_fiscal', 'nivel', 'primeiro_nome']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-fiscais')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de fiscal"
        context["botao"] = "Gravar"
        return context


class InspecaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Inspecao
    form_class = InspecaoUpdateForm
    template_name = 'form-upload.html'
    success_url = reverse_lazy('listar-inspecoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição da inspeção"
        context["botao"] = "Gravar"
        return context


class InfracaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    form_class = InfracaoUpdateForm
    template_name = 'form-upload2.html'
    success_url = reverse_lazy('gerenciar-infracoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de infração"
        context["botao"] = "Gravar"
        return context

class ProdutividadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano','produtividade_infracao', 'produtividade_manifesto']
    template_name = 'form-upload2.html'
    success_url = reverse_lazy('listar-produtividades2')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Edição de produtividade"
        context["botao"] = "Gravar"
        return context

class DefesasCreate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano', 'protocolo_defesa', 'entrada_protocolo', 'quem', 'prazo_manifesto', 'email']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-infracoes-ativos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Controle de defesas"
        context["botao"] = "Gravar"
        return context

class ReinspecoesCreate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    form_class = ReinspecaoForm
    template_name = 'form-upload2.html'
    success_url = reverse_lazy('listar-infracoes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar reinspeção"
        context["botao"] = "Gravar"
        return context

class ARJulgamento(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    fields = ['numero_format_ano', 'rastreio_julgamento', 'status_rastreio_julgamento', 'data_entrega_julgamento']
    template_name = 'form.html'
    success_url = reverse_lazy('listar-infracoes-ativos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Controle de AR's julgamento"
        context["botao"] = "Gravar"
        return context

class EstadoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = u"Administrador"
    login_url = reverse_lazy('login')
    model = Estado
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-estados')


class CidadeDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Cidade
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-cidades')


class BairroDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Bairro
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-bairros')


class LogradouroDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Logradouro
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-logradouros')


class ProprietarioDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Proprietario
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-proprietarios')


class TerrenoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Terreno
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-terrenos')


class ProtocoloDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Protocolo
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-protocolos')


class FiscalDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Fiscal
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-fiscais')


class InspecaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Inspecao
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-inspecoes')


class InfracaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'form-excluir.html'
    success_url = reverse_lazy('listar-infracoes-ativos')


class EstadoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Estado
    template_name = 'listar-estados.html'


class CidadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Cidade
    template_name = 'listar-cidades.html'


class BairroList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Bairro
    template_name = 'listar-bairros.html'


class LogradouroList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Logradouro
    template_name = 'listar-logradouros.html'


class ProprietarioList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Proprietario
    template_name = 'listar-proprietarios.html'


class TerrenoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Terreno
    template_name = 'listar-terrenos.html'


class ProtocoloList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Protocolo
    template_name = 'listar-protocolos.html'


class FiscalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Fiscal
    template_name = 'listar-fiscais.html'
    ordering = ['nome_fiscal']


class InspecaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Inspecao
    template_name = 'listar-inspecoes.html'
    permission_required = 'app.view_inspecao'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(protocolo__protocolo__icontains=q) | queryset.filter(terreno__inscricao__icontains=q) \
                       | queryset.filter(fiscal__primeiro_nome__icontains=q) | queryset.filter(terreno__logradouro_terreno__nome_logradouro__icontains=q)\
                       | queryset.filter(terreno__proprietario__nome_proprietario__icontains=q) | queryset.filter(terreno__logradouro_terreno__bairro__nome_bairro__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['termo_pesquisa'] = self.request.GET.get('q')
        return context

class InfracaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-infracoes.html'
    permission_required = 'app.view_infracao'

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'inspecao__protocolo',
            'inspecao__terreno',
            'inspecao__fiscal',
            'inspecao__terreno__logradouro_terreno',
            'inspecao__terreno__proprietario'
        )
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(inspecao__protocolo__protocolo__icontains=q) |
                Q(inspecao__terreno__inscricao__icontains=q) |
                Q(inspecao__fiscal__primeiro_nome__icontains=q) |
                Q(inspecao__terreno__logradouro_terreno__nome_logradouro__icontains=q) |
                Q(inspecao__terreno__proprietario__nome_proprietario__icontains=q) |
                Q(inspecao__terreno__logradouro_terreno__bairro__nome_bairro__icontains=q) |
                Q(numero_format_ano__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['termo_pesquisa'] = self.request.GET.get('q')
        return context

    
class InfracaoPrintList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'imprimir-infracoes.html'

class InfracaoListFilterAtivos(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-infracoes-ativos.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(julgamento__isnull=True)
        queryset = queryset.select_related('inspecao__protocolo', 'inspecao__fiscal', 'inspecao__terreno').prefetch_related('inspecao__terreno__logradouro_terreno', 'inspecao__terreno__logradouro_correspondencia', 'inspecao__terreno__proprietario')
        return queryset



class ProdutividadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Inspecao
    template_name = 'listar-produtividades.html'
    ordering = ['data_inspecao1']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(protocolo__protocolo__icontains=q) | queryset.filter(terreno__inscricao__icontains=q) \
                       | queryset.filter(fiscal__primeiro_nome__icontains=q) | queryset.filter(terreno__logradouro_terreno__nome_logradouro__icontains=q)\
                       | queryset.filter(terreno__proprietario__nome_proprietario__icontains=q) | queryset.filter(terreno__logradouro_terreno__bairro__nome_bairro__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['termo_pesquisa'] = self.request.GET.get('q')
        return context



class ProdutividadeList2(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-produtividades2.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(inspecao__protocolo__protocolo__icontains=q) | queryset.filter(inspecao__terreno__inscricao__icontains=q) \
                       | queryset.filter(inspecao__fiscal__primeiro_nome__icontains=q) | queryset.filter(inspecao__terreno__logradouro_terreno__nome_logradouro__icontains=q)\
                       | queryset.filter(inspecao__terreno__proprietario__nome_proprietario__icontains=q) | queryset.filter(inspecao__terreno__logradouro_terreno__bairro__nome_bairro__icontains=q) \
                       | queryset.filter(numero_format_ano__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['termo_pesquisa'] = self.request.GET.get('q')
        return context


class ProdutividadeList3(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-produtividades3.html'

class GerenciarList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'gerenciar-infracoes.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            words = q.split()  # quebra a string de entrada em palavras
            queryset = super().get_queryset().select_related(
                'inspecao__protocolo',
                'inspecao__terreno',
                'inspecao__fiscal',
                'inspecao__terreno__logradouro_terreno',
                'inspecao__terreno__proprietario'
            )

            querysets = []  # lista para armazenar os resultados de cada palavra

            # para cada palavra, adiciona na consulta
            for word in words:
                query = Q()
                query |= Q(inspecao__protocolo__protocolo__icontains=word)
                query |= Q(inspecao__terreno__inscricao__icontains=word)
                query |= Q(inspecao__fiscal__primeiro_nome__icontains=word)
                query |= Q(inspecao__terreno__logradouro_terreno__nome_logradouro__icontains=word)
                query |= Q(inspecao__terreno__proprietario__nome_proprietario__icontains=word)
                query |= Q(inspecao__terreno__logradouro_terreno__bairro__nome_bairro__icontains=word)
                query |= Q(numero_format_ano__icontains=word)

                querysets.append(queryset.filter(query))

            # encontra a interseção de todas as consultas
            result_queryset = querysets[0]
            for qs in querysets[1:]:
                result_queryset = result_queryset.intersection(qs)

            return result_queryset
        else:
            return Infracao.objects.none()  # retorna uma queryset vazia



class MultadosList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'multados.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(situacao__in=["3", "8"])
        queryset = queryset.order_by('julgamento')
        return queryset



class InformacoesList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Infracao
    template_name = 'listar-infracoes2.html'

def gerar_relatorio(request, pk, template_name="gerar_relatorio.html"):
    inspecao = get_object_or_404(Inspecao, pk=pk)
    return render(request, template_name, {'inspecao': inspecao})


def gerar_manifestacao(request, pk, template_name="gerar_manifestacao.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    is_pre_june_2023 = infracao.is_pre_june_2023
    return render(request, template_name, {'infracao': infracao, 'is_pre_june_2023': is_pre_june_2023})


def gerar_julgamento(request, pk, template_name="gerar_julgamento.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    is_pre_june_2023 = infracao.is_pre_june_2023
    return render(request, template_name, {'infracao': infracao, 'is_pre_june_2023': is_pre_june_2023})
    
    
def gerar_ar1(request, pk, template_name="gerar_ar1.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_ar2(request, pk, template_name="gerar_ar2.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_ar3(request, pk, template_name="gerar_ar3.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_ar4(request, pk, template_name="gerar_ar4.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_ar5(request, pk, template_name="gerar_ar5.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_ar6(request, pk, template_name="gerar_ar6.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_ar7(request, pk, template_name="gerar_ar7.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    return render(request, template_name, {'infracao': infracao})


def gerar_auto(request, pk, template_name="auto_infracao.html"):
    infracao = get_object_or_404(Infracao, pk=pk)
    is_pre_june_2023 = infracao.is_pre_june_2023
    return render(request, template_name, {'infracao': infracao, 'is_pre_june_2023': is_pre_june_2023})


def calcular_dias_uteis(data_inicial, quantidade_dias, feriados_recessos):
    data_atual = data_inicial
    dias_uteis = 0

    while dias_uteis < quantidade_dias:
        data_atual += timedelta(days=1)
        if data_atual.weekday() >= 5:  # Sábado ou domingo
            continue
        if data_atual in feriados_recessos:
            continue
        dias_uteis += 1
    return data_atual

def calcular_prazo_defesa(request):
    data_entrega_autuacao = request.GET.get('data_entrega_autuacao', None)
    if data_entrega_autuacao:
        data_entrega_autuacao = datetime.strptime(data_entrega_autuacao, "%Y-%m-%d").date()
        feriados_recessos = FeriadoRecesso.objects.all().values_list('data', flat=True)
        prazo_defesa = calcular_dias_uteis(data_entrega_autuacao, 10, feriados_recessos)
        return JsonResponse({"prazo_defesa": prazo_defesa.strftime("%d/%m/%Y")})
    else:
        return JsonResponse({"error": "Data de entrega da autuação não fornecida."})

class FeriadoRecessoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = FeriadoRecesso
    template_name = 'lista_feriados.html'

class FeriadoRecessoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = FeriadoRecesso
    form_class = FeriadoRecessoForm
    template_name = 'form.html'
    success_url = reverse_lazy('lista_feriados')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de feriado"
        context['botao'] = "Cadastrar"
        return context

class FeriadoRecessoUpdate(LoginRequiredMixin, UpdateView):
    model = FeriadoRecesso
    form_class = FeriadoRecessoForm
    template_name = 'form.html'
    success_url = reverse_lazy('lista_feriados')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Alteração de feriado"
        context['botao'] = "Gravar"
        return context

class FeriadoRecessoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = FeriadoRecesso
    success_url = reverse_lazy('lista_feriados')
    template_name = 'form-excluir.html'


def atualizar_infracoes_relacionadas(infracao, form_data):
    inspecao = infracao.inspecao
    terreno = inspecao.terreno
    proprietario = terreno.proprietario
    protocolo = inspecao.protocolo

    infracoes_relacionadas = Infracao.objects.filter(inspecao__protocolo=protocolo, inspecao__terreno__proprietario=proprietario)

    for infracao_relacionada in infracoes_relacionadas:
        form = InfracaoForm(form_data, instance=infracao_relacionada)
        if form.is_valid():
            form.save()


def editar_infracao(request, pk):
    infracao = get_object_or_404(Infracao, pk=pk)

    if request.method == 'POST':
        form = InfracaoForm(request.POST, instance=infracao)
        if form.is_valid():
            atualizar_infracoes_relacionadas(infracao, request.POST)
            return redirect(reverse_lazy('listar-infracoes-ativos'))
    else:
        form = InfracaoForm(instance=infracao)

    infracoes_relacionadas = Infracao.objects.filter(inspecao__protocolo=infracao.inspecao.protocolo, inspecao__terreno__proprietario=infracao.inspecao.terreno.proprietario)
    numeros_relacionados = [infracao_relacionada.numero_format_ano for infracao_relacionada in infracoes_relacionadas]

    context = {
        'form': form,
        'titulo': 'Controle coletivo de recebimento',
        'botao': 'Salvar',
        'numeros_relacionados': ' - '.join(numeros_relacionados),
        'numero_format_ano': infracao.numero_format_ano,
    }

    return render(request, 'editar_infracao.html', context)


def atualizar_infracoes_relacionadas_defesa(infracao, form_data):
    inspecao = infracao.inspecao
    terreno = inspecao.terreno
    proprietario = terreno.proprietario
    protocolo = inspecao.protocolo

    infracoes_relacionadas = Infracao.objects.filter(inspecao__protocolo=protocolo,
                                                     inspecao__terreno__proprietario=proprietario)

    for infracao_relacionada in infracoes_relacionadas:
        form = InfracaoFormDefesa(form_data, instance=infracao_relacionada)
        if form.is_valid():
            form.save()


def gerenciar_defesa(request, pk):
    infracao = get_object_or_404(Infracao, pk=pk)

    if request.method == 'POST':
        form = InfracaoFormDefesa(request.POST, instance=infracao)
        if form.is_valid():
            atualizar_infracoes_relacionadas_defesa(infracao, request.POST)
            return redirect(reverse_lazy('listar-infracoes-ativos'))
    else:
        form = InfracaoFormDefesa(instance=infracao)

    infracoes_relacionadas = Infracao.objects.filter(inspecao__protocolo=infracao.inspecao.protocolo,
                                                     inspecao__terreno__proprietario=infracao.inspecao.terreno.proprietario)
    numeros_relacionados = [infracao_relacionada.numero_format_ano for infracao_relacionada in infracoes_relacionadas]

    context = {
        'form': form,
        'titulo': 'Gerenciar defesa',
        'botao': 'Salvar',
        'numeros_relacionados': ' - '.join(numeros_relacionados),
        'numero_format_ano': infracao.numero_format_ano,
    }

    return render(request, 'gerenciar_defesa.html', context)


def calcular_prazo_manifesto(request):
    entrada_protocolo = request.GET.get('entrada_protocolo', None)
    if entrada_protocolo:
        entrada_protocolo = datetime.strptime(entrada_protocolo, "%Y-%m-%d").date()
        feriados_recessos = FeriadoRecesso.objects.all().values_list('data', flat=True)
        prazo_manifesto = calcular_dias_uteis(entrada_protocolo, 10, feriados_recessos)
        return JsonResponse({"prazo_manifesto": prazo_manifesto.strftime("%d/%m/%Y")})
    else:
        return JsonResponse({"error": "Data de entrada não fornecida."})


class ARCreate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Infracao
    form_class = ARForm
    template_name = 'form4.html'
    success_url = reverse_lazy('listar-infracoes-ativos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Criar o helper e definir o layout
        helper = FormHelper()
        form_fields = self.get_form().fields
        helper.layout = Layout(*[field for field in form_fields if field != 'data_entrega_autuacao'])

        context['helper'] = helper
        context['titulo'] = "Controle de AR's"
        context["botao"] = "Gravar"

        return context

    def form_valid(self, form):
        infracao = form.save(commit=False)
        data_entrega_autuacao = infracao.data_entrega_autuacao
        if data_entrega_autuacao:
            feriados_recessos = FeriadoRecesso.objects.all().values_list('data', flat=True)
            prazo_defesa = calcular_dias_uteis(data_entrega_autuacao, 10, feriados_recessos)
            infracao.prazo_defesa = prazo_defesa
        infracao.save()
        return HttpResponseRedirect(self.get_success_url())
    

def vrm_list(request):
    vrms = ValorVRM.objects.all()
    return render(request, 'vrm_list.html', {'vrms': vrms})

class VRMCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = ValorVRM
    form_class = ValorVRMForm
    template_name = 'form.html'
    success_url = reverse_lazy('vrm_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar VRM"
        context["botao"] = "Adicionar"
        return context

class VRMUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = ValorVRM
    form_class = ValorVRMForm
    template_name = 'form.html'
    success_url = reverse_lazy('vrm_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar VRM"
        context["botao"] = "Salvar"
        return context

def vrm_delete(request, pk):
    vrm = get_object_or_404(ValorVRM, pk=pk)

    if request.method=='POST':
        vrm.delete()
        return redirect('vrm_list')

    return render(request, 'form-excluir.html', {'item': vrm})

def dados_multados(request):
    search_year = request.GET.get('q')
    infracoes = None
    total_count = 0
    total_value = Decimal(0)

    if search_year:
        # Filtra infrações baseadas no ano inserido no campo de pesquisa e nas situações 3 ou 8
        infracoes = Infracao.objects.filter(
            data_auto__year=search_year,
            situacao__in=["3", "8"]  # isso fará a filtragem para os códigos de situação
        )

        # Calcula o número total de terrenos multados
        total_count = infracoes.count()

        # Calcula o valor total das multas
        for infracao in infracoes:
            total_value += infracao.get_vrm

    context = {
        'object_list': infracoes,
        'total_count': total_count,
        'total_value': total_value,
        'search_year': search_year,
    }

    return render(request, 'dados_multados.html', context)