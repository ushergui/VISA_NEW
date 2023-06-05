from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Paciente, Fisioterapeuta, Equipamento, Descartavel, Cid, Prescricao, Usf, Atendimento, ModoDeUso, Finalidade
from .forms import PacienteForm, FisioterapeutaForm, EquipamentoForm, DescartavelForm, CidForm, PrescricaoForm, AtendimentoForm, UsfForm, AtendimentoForm, ModoDeUsoForm, FinalidadeForm
from cadastros.models import Logradouro
from django.shortcuts import render
from django.db.models import Count, F, Q, Max
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import FileResponse, HttpResponse
import datetime
from django.utils import timezone
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.db import transaction
from datetime import datetime, timedelta
import calendar
import locale


class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('paciente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Cadastro de Paciente"
        context["botao"] = "Cadastrar"
        return context

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('paciente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Edição de Paciente"
        context["botao"] = "Salvar"
        return context
    

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'oxigenoterapia/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

class FisioterapeutaListView(ListView):
    model = Fisioterapeuta
    template_name = 'oxigenoterapia/fisioterapeuta_list.html'

class FisioterapeutaCreateView(CreateView):
    model = Fisioterapeuta
    form_class = FisioterapeutaForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('fisioterapeuta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Novo Fisioterapeuta"
        context["botao"] = "Cadastrar"
        return context

class FisioterapeutaUpdateView(UpdateView):
    model = Fisioterapeuta
    form_class = FisioterapeutaForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('fisioterapeuta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Fisioterapeuta"
        context["botao"] = "Salvar"
        return context

class FisioterapeutaDeleteView(DeleteView):
    model = Fisioterapeuta
    template_name = 'oxigenoterapia/fisioterapeuta_confirm_delete.html'
    success_url = reverse_lazy('fisioterapeuta_list')


class EquipamentoListView(ListView):
    model = Equipamento
    template_name = 'oxigenoterapia/equipamento_list.html'
    context_object_name = 'equipamentos'

class EquipamentoCreateView(CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('equipamento_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Novo Equipamento'
        data['botao'] = 'Salvar'
        return data

class EquipamentoUpdateView(UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('equipamento_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar Equipamento'
        data['botao'] = 'Atualizar'
        return data

class EquipamentoDeleteView(DeleteView):
    model = Equipamento
    template_name = 'oxigenoterapia/equipamento_confirm_delete.html'
    success_url = reverse_lazy('equipamento_list')

class DescartavelListView(ListView):
    model = Descartavel
    template_name = 'oxigenoterapia/descartavel_list.html'
    context_object_name = 'descartavels'


class DescartavelCreateView(CreateView):
    model = Descartavel
    form_class = DescartavelForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('descartavel_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Novo Descartável'
        data['botao'] = 'Salvar'
        return data

class DescartavelUpdateView(UpdateView):
    model = Descartavel
    form_class = DescartavelForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('descartavel_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar Descartável'
        data['botao'] = 'Atualizar'
        return data

class DescartavelDeleteView(DeleteView):
    model = Descartavel
    template_name = 'oxigenoterapia/descartavel_confirm_delete.html'
    success_url = reverse_lazy('descartavel_list')

class FinalidadeListView(ListView):
    model = Finalidade
    template_name = 'oxigenoterapia/finalidade_list.html'
    context_object_name = 'finalidade'


class FinalidadeCreateView(CreateView):
    model = Finalidade
    form_class = FinalidadeForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('finalidade_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Nova Finalidade'
        data['botao'] = 'Salvar'
        return data

class FinalidadeUpdateView(UpdateView):
    model = Finalidade
    form_class = FinalidadeForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('finalidade_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar Finalidade'
        data['botao'] = 'Atualizar'
        return data

class FinalidadeDeleteView(DeleteView):
    model = Finalidade
    template_name = 'oxigenoterapia/finalidade_confirm_delete.html'
    success_url = reverse_lazy('finalidade_list')

class CidListView(ListView):
    model = Cid
    template_name = 'oxigenoterapia/cid_list.html'
    context_object_name = 'descartavels'


class CidCreateView(CreateView):
    model = Cid
    form_class = CidForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('cid_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Novo CID'
        data['botao'] = 'Salvar'
        return data

class CidUpdateView(UpdateView):
    model = Cid
    form_class = CidForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('cid_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar CID'
        data['botao'] = 'Atualizar'
        return data

class CidDeleteView(DeleteView):
    model = Cid
    template_name = 'oxigenoterapia/cid_confirm_delete.html'
    success_url = reverse_lazy('cid_list')




class PrescricaoListView(ListView):
    model = Prescricao
    template_name = 'oxigenoterapia/prescricao_list.html'

class PrescricaoCreateView(CreateView):
    model = Prescricao
    form_class = PrescricaoForm
    template_name = 'oxigenoterapia/form_prescricao.html'

    def get_success_url(self):
        return reverse_lazy('prescricoes_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Cadastrar Prescrição'
        data['botao'] = 'Cadastrar'
        return data

    @transaction.atomic  # Garante que ambos os objetos sejam criados ou nenhum seja
    def form_valid(self, form):
        response = super().form_valid(form)
        # Uma vez que a instância de Prescricao é criada, podemos usar seus dados para criar ModoDeUso
        modo_de_uso = ModoDeUso(
            paciente=self.object.paciente,
            data_inicio_uso=self.object.data_inicio_uso,
            tempo_de_uso=self.object.tempo_de_uso,
            cid=self.object.cid,
            litros=self.object.litros,
            parametros=self.object.parametros
        )
        modo_de_uso.save()
        modo_de_uso.equipamento.set(self.object.equipamento.all())  # Adiciona os mesmos equipamentos
        return response

class PrescricaoUpdateView(UpdateView):
    model = Prescricao
    form_class = PrescricaoForm
    template_name = 'oxigenoterapia/form_prescricao.html'

    def get_success_url(self):
        return reverse_lazy('prescricoes_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar Prescrição'
        data['botao'] = 'Gravar'
        return data

class PrescricaoDeleteView(DeleteView):
    model = Prescricao
    template_name = 'oxigenoterapia/prescricao_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('prescricoes_list')


class ModoDeUsoListView(ListView):
    model = ModoDeUso
    template_name = 'oxigenoterapia/mododeuso_list.html'

class ModoDeUsoCreateView(CreateView):
    model = ModoDeUso
    form_class = ModoDeUsoForm
    template_name = 'oxigenoterapia/form_prescricao.html'

    def get_success_url(self):
        return reverse_lazy('mododeuso_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Cadastrar Modo de Uso'
        data['botao'] = 'Cadastrar'
        return data

class ModoDeUsoUpdateView(UpdateView):
    model = ModoDeUso
    form_class = ModoDeUsoForm
    template_name = 'oxigenoterapia/form_prescricao.html'

    def get_success_url(self):
        return reverse_lazy('mododeuso_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar Modo de Uso'
        data['botao'] = 'Gravar'
        return data

class ModoDeUsoDeleteView(DeleteView):
    model = ModoDeUso
    template_name = 'oxigenoterapia/mododeuso_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('mododeuso_list')

class AtendimentoCreateView(CreateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('atendimento_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Cadastro de atendimento'
        data['botao'] = 'Gravar'
        return data

    def get_initial(self):
        initial = super().get_initial()

        # Obtém o id da prescrição da URL
        prescricao_id = self.kwargs.get('prescricao_id')

        # Preenche os campos da prescrição com os dados do banco de dados
        if prescricao_id:
            prescricao = ModoDeUso.objects.get(id=prescricao_id)
            initial['equipamento'] = prescricao.equipamento.values_list('id', flat=True)
            initial['tempo_de_uso'] = prescricao.tempo_de_uso
            initial['litros'] = prescricao.litros
            initial['parametros'] = prescricao.parametros
            initial['prescricao'] = prescricao_id

        return initial

    def form_valid(self, form):
        # Obtém o id da prescrição da URL
        prescricao_id = self.kwargs.get('prescricao_id')

        # Atribui o valor do campo 'prescricao' antes de salvar o formulário
        if prescricao_id:
            form.instance.prescricao = ModoDeUso.objects.get(id=prescricao_id)
        return super().form_valid(form)

    
class AtendimentoUpdateView(UpdateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('atendimento_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar Atendimento'
        data['botao'] = 'Atualizar'
        return data
    def form_valid(self, form):
        # Primeiro, chame a implementação padrão para salvar o objeto Atendimento
        response = super().form_valid(form)
        
        # Em seguida, obtenha os dados do formulário para o ModoDeUso
        equipamento = form.cleaned_data['equipamento']
        tempo_de_uso = form.cleaned_data['tempo_de_uso']
        litros = form.cleaned_data['litros']
        parametros = form.cleaned_data['parametros']
        
        # Obtenha o objeto ModoDeUso relacionado
        mododeuso = self.object.prescricao

        # Atualize os campos de ModoDeUso
        mododeuso.equipamento.set(equipamento)
        mododeuso.tempo_de_uso = tempo_de_uso
        mododeuso.litros = litros
        mododeuso.parametros = parametros
        
        # Salve o objeto ModoDeUso
        mododeuso.save()
        
        # Retorne a resposta
        return response

class AtendimentoDeleteView(DeleteView):
    model = Atendimento
    template_name = 'oxigenoterapia/atendimento_confirm_delete.html'
    success_url = reverse_lazy('atendimento_list')

class AtendimentoListView(ListView):
    model = Atendimento
    template_name = 'oxigenoterapia/atendimento_list.html'


class UsfListView(ListView):
    model = Usf
    template_name = 'oxigenoterapia/usf_list.html'
    context_object_name = "Usf's"


class UsfCreateView(CreateView):
    model = Usf
    form_class = UsfForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('usf_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Nova USF'
        data['botao'] = 'Salvar'
        return data

class UsfUpdateView(UpdateView):
    model = Usf
    form_class = UsfForm
    template_name = 'oxigenoterapia/form.html'

    def get_success_url(self):
        return reverse_lazy('usf_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Editar USF'
        data['botao'] = 'Atualizar'
        return data

class UsfDeleteView(DeleteView):
    model = Usf
    template_name = 'oxigenoterapia/usf_confirm_delete.html'
    success_url = reverse_lazy('usf_list')


def consulta_atendimentos(request):
    ano_atual = datetime.date.today().year
    mes_atual = datetime.date.today().month
    ano = int(request.GET.get('year'))
    mes = int(request.GET.get('month'))
    nome_fisioterapeuta = request.GET.get('fisioterapeuta')
    esconde_ativos_periodo = False
    if ano > ano_atual or (ano == ano_atual and mes >= mes_atual):
        esconde_ativos_periodo = True
    total_ativos = Paciente.objects.filter(status="ATIVO").count()
    
    if ano and mes:
        total_obitos = Paciente.objects.filter(status="ÓBITO", data_obito__year=ano, data_obito__month=mes).count()
        total_altas = Paciente.objects.filter(status="ALTA", data_alta__year=ano, data_alta__month=mes).count()
        total_ativos_periodo = ModoDeUso.objects.filter(Q(data_inicio_uso__year=ano), Q(data_inicio_uso__month=mes)).count() - total_obitos - total_altas
    else:
        total_obitos = Paciente.objects.filter(status="ÓBITO").count()
        total_altas = Paciente.objects.filter(status="ALTA").count()
        total_ativos_periodo = 0

    atendimentos = Atendimento.objects.all()

    if ano:
        atendimentos = atendimentos.filter(data_atendimento__year=ano)
    if mes:
        atendimentos = atendimentos.filter(data_atendimento__month=mes)
    if nome_fisioterapeuta:
        atendimentos = atendimentos.filter(fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta=nome_fisioterapeuta)

    # Nesse ponto, precisamos primeiramente fazer um pré-filtro dos atendimentos que estamos interessados
    ids_atendimentos_interesse = atendimentos.values_list('id', flat=True)

    # Agora precisamos pegar todos os ModosDeUso que foram associados com esses atendimentos
    modos_de_uso = ModoDeUso.objects.filter(atendimentos__id__in=ids_atendimentos_interesse)

    # Agora conseguimos realizar a agregação por finalidade do equipamento
    atendimentos_por_finalidade = modos_de_uso.values(
        finalidade=F('equipamento__finalidade_equipamento__finalidade')
    ).annotate(total=Count('atendimentos'))

    total_geral = sum(atendimento['total'] for atendimento in atendimentos_por_finalidade)

    context = {
        'ano_pesquisa': ano,
        'mes_pesquisa': mes,
        'fisioterapeuta_pesquisa': nome_fisioterapeuta,
        'atendimentos_por_finalidade': atendimentos_por_finalidade,
        'total_geral': total_geral,
        'total_ativos': total_ativos,
        'total_obitos': total_obitos,
        'total_altas': total_altas,
        'total_ativos_periodo': total_ativos_periodo,
        'esconde_ativos_periodo': esconde_ativos_periodo,
    }

    return render(request, 'oxigenoterapia/consulta_atendimentos.html', context)


def consulta_atendimentos_pdf(request):
    ano_atual = datetime.date.today().year
    mes_atual = datetime.date.today().month
    ano = int(request.GET.get('year'))
    mes = int(request.GET.get('month'))
    nome_fisioterapeuta = request.GET.get('fisioterapeuta')
    esconde_ativos_periodo = False
    if ano > ano_atual or (ano == ano_atual and mes >= mes_atual):
        esconde_ativos_periodo = True
    total_ativos = Paciente.objects.filter(status="ATIVO").count()
    
    if ano and mes:
        total_obitos = Paciente.objects.filter(status="ÓBITO", data_obito__year=ano, data_obito__month=mes).count()
        total_altas = Paciente.objects.filter(status="ALTA", data_alta__year=ano, data_alta__month=mes).count()
        total_ativos_periodo = ModoDeUso.objects.filter(Q(data_inicio_uso__year=ano), Q(data_inicio_uso__month=mes)).count() - total_obitos - total_altas
    else:
        total_obitos = Paciente.objects.filter(status="ÓBITO").count()
        total_altas = Paciente.objects.filter(status="ALTA").count()
        total_ativos_periodo = 0

    atendimentos = Atendimento.objects.all()

    if ano:
        atendimentos = atendimentos.filter(data_atendimento__year=ano)
    if mes:
        atendimentos = atendimentos.filter(data_atendimento__month=mes)
    if nome_fisioterapeuta:
        atendimentos = atendimentos.filter(fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta=nome_fisioterapeuta)

    # Nesse ponto, precisamos primeiramente fazer um pré-filtro dos atendimentos que estamos interessados
    ids_atendimentos_interesse = atendimentos.values_list('id', flat=True)

    # Agora precisamos pegar todos os ModosDeUso que foram associados com esses atendimentos
    modos_de_uso = ModoDeUso.objects.filter(atendimentos__id__in=ids_atendimentos_interesse)

    # Agora conseguimos realizar a agregação por finalidade do equipamento
    atendimentos_por_finalidade = modos_de_uso.values(
        finalidade=F('equipamento__finalidade_equipamento__finalidade')
    ).annotate(total=Count('atendimentos'))

    total_geral = sum(atendimento['total'] for atendimento in atendimentos_por_finalidade)

    context = {
        'ano_pesquisa': ano,
        'mes_pesquisa': mes,
        'fisioterapeuta_pesquisa': nome_fisioterapeuta,
        'atendimentos_por_finalidade': atendimentos_por_finalidade,
        'total_geral': total_geral,
        'total_ativos': total_ativos,
        'total_obitos': total_obitos,
        'total_altas': total_altas,
        'total_ativos_periodo': total_ativos_periodo,
        'esconde_ativos_periodo': esconde_ativos_periodo,
    }
    html_string = render_to_string('oxigenoterapia/consulta_atendimentos_pdf.html', context)

    # Em seguida, vamos transformar essa string em um objeto HTML do WeasyPrint
    html = HTML(string=html_string)

    # Agora podemos gerar o PDF
    pdf = html.write_pdf()

    # E finalmente, retornamos o PDF como uma resposta de arquivo
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=consulta_atendimentos.pdf'
    return response


def relatorio_pacientes_ativos_oxigenoterapia(request):
    fisioterapeutas = Fisioterapeuta.objects.all()
    fisioterapeuta_nome = request.GET.get('fisioterapeuta')

    # Alterar a forma como filtramos os pacientes
    modo_de_uso = ModoDeUso.objects.filter(
        equipamento__finalidade_equipamento__finalidade='OXIGENOTERAPIA').values_list('paciente_id', flat=True)
    pacientes = Paciente.objects.filter(status='ATIVO', id__in=modo_de_uso)

    if fisioterapeuta_nome:
        pacientes = pacientes.filter(
            usf_paciente__nome_fisioterapeuta__primeiro_nome_fisioterapeuta=fisioterapeuta_nome)
    
    for paciente in pacientes:
        ultimo_atendimento = Atendimento.objects.filter(
            prescricao__paciente=paciente).order_by('data_atendimento').last()
        if ultimo_atendimento:
            paciente.data_ultima_visita = ultimo_atendimento.data_atendimento
            paciente.total_dias_ultima_visita = (
                timezone.now().date() - ultimo_atendimento.data_atendimento).days - 1
        else:
            paciente.data_ultima_visita = "-----------------"
            paciente.total_dias_ultima_visita = "Não foi atendido ainda"

    context = {
        'fisioterapeutas': fisioterapeutas,
        'pacientes': pacientes,
        'fisioterapeuta_pesquisa': fisioterapeuta_nome
    }

    return render(request, 'oxigenoterapia/relatorio_pacientes_ativos_oxigenoterapia.html', context)

def relatorio_pacientes_ativos_oxigenoterapia_pdf(request):
    fisioterapeutas = Fisioterapeuta.objects.all()
    fisioterapeuta_nome = request.GET.get('fisioterapeuta')

    modo_de_uso = ModoDeUso.objects.filter(
        equipamento__finalidade_equipamento__finalidade='OXIGENOTERAPIA').values_list('paciente_id', flat=True)
    pacientes = Paciente.objects.filter(status='ATIVO', id__in=modo_de_uso)

    if fisioterapeuta_nome:
        pacientes = pacientes.filter(
            usf_paciente__nome_fisioterapeuta__primeiro_nome_fisioterapeuta=fisioterapeuta_nome)
    
    for paciente in pacientes:
        ultimo_atendimento = Atendimento.objects.filter(
            prescricao__paciente=paciente).order_by('data_atendimento').last()
        if ultimo_atendimento:
            paciente.data_ultima_visita = ultimo_atendimento.data_atendimento
            paciente.total_dias_ultima_visita = (
                timezone.now().date() - ultimo_atendimento.data_atendimento).days - 1
        else:
            paciente.data_ultima_visita = "-----------------"
            paciente.total_dias_ultima_visita = "Não foi atendido ainda"

    context = {
        'fisioterapeutas': fisioterapeutas,
        'pacientes': pacientes,
        'fisioterapeuta_pesquisa': fisioterapeuta_nome
    }

    # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('oxigenoterapia/relatorio_pacientes_ativos_oxigenoterapia_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])  # Adicione esta linha

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=relatorio_pacientes_ativos_oxigenoterapia.pdf'
    return response


def relatorio_pacientes_ativos_ventilacao(request):
    fisioterapeutas = Fisioterapeuta.objects.all()
    fisioterapeuta_nome = request.GET.get('fisioterapeuta')

    # Filtramos os pacientes que usam os equipamentos desejados
    modo_de_uso_desejado = ModoDeUso.objects.filter(
        equipamento__finalidade_equipamento__finalidade__in=['BiPAP', 'VENTILADOR', 'CPAP']).values_list('paciente_id', flat=True)

    # Filtramos os pacientes que usam exclusivamente 'OXIGENOTERAPIA'
    modo_de_uso_oxigenoterapia = ModoDeUso.objects.filter(
        equipamento__finalidade_equipamento__finalidade='OXIGENOTERAPIA').exclude(
        paciente_id__in=modo_de_uso_desejado).values_list('paciente_id', flat=True)

    pacientes = Paciente.objects.filter(status='ATIVO', id__in=modo_de_uso_desejado).exclude(id__in=modo_de_uso_oxigenoterapia)

    if fisioterapeuta_nome:
        pacientes = pacientes.filter(
            usf_paciente__nome_fisioterapeuta__primeiro_nome_fisioterapeuta=fisioterapeuta_nome)
    
    for paciente in pacientes:
        ultimo_atendimento = Atendimento.objects.filter(
            prescricao__paciente=paciente).order_by('data_atendimento').last()
        if ultimo_atendimento:
            paciente.data_ultima_visita = ultimo_atendimento.data_atendimento
            paciente.total_dias_ultima_visita = (
                timezone.now().date() - ultimo_atendimento.data_atendimento).days - 1
        else:
            paciente.data_ultima_visita = "-----------------"
            paciente.total_dias_ultima_visita = "Não foi atendido ainda"

        # Aqui você recupera os equipamentos do paciente
        equipamentos = ModoDeUso.objects.filter(paciente=paciente).values_list('equipamento__nome_equipamento', flat=True)
        # E transforma a lista em uma string separada por vírgulas
        paciente.equipamentos = ', '.join(equipamentos)

    context = {
        'fisioterapeutas': fisioterapeutas,
        'pacientes': pacientes,
        'fisioterapeuta_pesquisa': fisioterapeuta_nome
    }

    return render(request, 'oxigenoterapia/relatorio_pacientes_ativos_ventilacao.html', context)


def relatorio_pacientes_ativos_ventilacao_pdf(request):
    fisioterapeutas = Fisioterapeuta.objects.all()
    fisioterapeuta_nome = request.GET.get('fisioterapeuta')

    # Filtramos os pacientes que usam os equipamentos desejados
    modo_de_uso_desejado = ModoDeUso.objects.filter(
        equipamento__finalidade_equipamento__finalidade__in=['BiPAP', 'VENTILADOR', 'CPAP']).values_list('paciente_id', flat=True)

    # Filtramos os pacientes que usam exclusivamente 'OXIGENOTERAPIA'
    modo_de_uso_oxigenoterapia = ModoDeUso.objects.filter(
        equipamento__finalidade_equipamento__finalidade='OXIGENOTERAPIA').exclude(
        paciente_id__in=modo_de_uso_desejado).values_list('paciente_id', flat=True)

    pacientes = Paciente.objects.filter(status='ATIVO', id__in=modo_de_uso_desejado).exclude(id__in=modo_de_uso_oxigenoterapia)
    if fisioterapeuta_nome:
        pacientes = pacientes.filter(
            usf_paciente__nome_fisioterapeuta__primeiro_nome_fisioterapeuta=fisioterapeuta_nome)
    
    for paciente in pacientes:
        ultimo_atendimento = Atendimento.objects.filter(
            prescricao__paciente=paciente).order_by('data_atendimento').last()
        if ultimo_atendimento:
            paciente.data_ultima_visita = ultimo_atendimento.data_atendimento
            paciente.total_dias_ultima_visita = (
                timezone.now().date() - ultimo_atendimento.data_atendimento).days - 1
        else:
            paciente.data_ultima_visita = "-----------------"
            paciente.total_dias_ultima_visita = "Não foi atendido ainda"

        # Aqui você recupera os equipamentos do paciente
        equipamentos = ModoDeUso.objects.filter(paciente=paciente).values_list('equipamento__nome_equipamento', flat=True)
        # E transforma a lista em uma string separada por vírgulas
        paciente.equipamentos = ', '.join(equipamentos)

    context = {
        'fisioterapeutas': fisioterapeutas,
        'pacientes': pacientes,
        'fisioterapeuta_pesquisa': fisioterapeuta_nome
    }

    # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('oxigenoterapia/relatorio_pacientes_ativos_ventilacao_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])  # Adicione esta linha

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=relatorio_pacientes_ativos_ventilacao.pdf'
    return response

def relatorio_para_visita(request):
    usf_id = request.GET.get('usf', None)
    equipamento = request.GET.get('equipamento', None)
    busca_submetida = False  # Inicializando como False

    # Recuperar opções de seleção
    usfs = Usf.objects.all()
    equipamentos = Finalidade.objects.values_list('agrupamento', flat=True).distinct()

    # Iniciar com todos os objetos ModoDeUso onde o paciente está ativo
    modos_uso = ModoDeUso.objects.filter(paciente__status='ATIVO')

    # Aplicar filtros se eles foram fornecidos
    if usf_id:
        modos_uso = modos_uso.filter(paciente__usf_paciente__id=usf_id)

    if equipamento:
        modos_uso = modos_uso.filter(equipamento__finalidade_equipamento__agrupamento=equipamento)

    if request.GET:  # Verificar se a requisição é do tipo GET
        busca_submetida = True

    context = {
        'modos_uso': modos_uso,
        'usfs': usfs,
        'equipamentos': equipamentos,
        'usf_pesquisa': usf_id,
        'equipamento_pesquisa': equipamento,
        'busca_submetida': busca_submetida,  # Adicionando a variável no contexto
    }

    return render(request, 'oxigenoterapia/relatorio_para_visita.html', context)



def relatorio_para_visita_pdf(request):
    usf_id = request.GET.get('usf', None)
    equipamento = request.GET.get('equipamento', None)
    busca_submetida = False  # Inicializando como False

    # Recuperar opções de seleção
    usfs = Usf.objects.all()
    equipamentos = Finalidade.objects.values_list('agrupamento', flat=True).distinct()

    # Iniciar com todos os objetos ModoDeUso onde o paciente está ativo
    modos_uso = ModoDeUso.objects.filter(paciente__status='ATIVO')

    # Aplicar filtros se eles foram fornecidos
    if usf_id:
        modos_uso = modos_uso.filter(paciente__usf_paciente__id=usf_id)

    if equipamento:
        modos_uso = modos_uso.filter(equipamento__finalidade_equipamento__agrupamento=equipamento)

    if request.GET:  # Verificar se a requisição é do tipo GET
        busca_submetida = True

    usf = None
    if usf_id:
        try:
            usf = Usf.objects.get(id=usf_id)
        except Usf.DoesNotExist:
            pass  # ou lidar com a situação em que usf_id não corresponde a nenhum Usf

    context = {
        'modos_uso': modos_uso,
        'usfs': usfs,
        'equipamentos': equipamentos,
        'usf': usf,  # passando o objeto Usf para o contexto
        'usf_pesquisa': usf_id,
        'equipamento_pesquisa': equipamento,
        'busca_submetida': busca_submetida,
    }

 # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('oxigenoterapia/relatorio_para_visita_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])  # Adicione esta linha

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=relatorio_para_visita_pdf.html'
    return response


def relatorio_troca_de_filtro(request):
    cutoff_date = datetime.now() - timedelta(days=6*30)

    prescricoes = ModoDeUso.objects.filter(
        Q(data_inicio_uso__lt=cutoff_date) &
        ~Q(atendimentos__data_atendimento__gt=cutoff_date, atendimentos__troca_de_filtro=True)
    ).values('paciente')

    pacientes = Paciente.objects.filter(id__in=prescricoes)

    relatorio = []
    for paciente in pacientes:
        prescricao_recente = ModoDeUso.objects.filter(paciente=paciente).order_by('-data_inicio_uso').first()
        atendimento_recente = Atendimento.objects.filter(prescricao__paciente=paciente).order_by('-data_atendimento').first()
    
        data_recente = max(prescricao_recente.data_inicio_uso, atendimento_recente.data_atendimento) if atendimento_recente else prescricao_recente.data_inicio_uso
    
        nome_equipamentos = ", ".join([equipamento.nome_equipamento for equipamento in prescricao_recente.equipamento.all()])
    
        relatorio.append({
            'nome_paciente': paciente.nome_paciente,
            'telefone_1': paciente.telefone_paciente1,
            'telefone_2': paciente.telefone_paciente2,
            'data_recente': data_recente,
            'nome_equipamentos': nome_equipamentos,
        })

    return render(request, 'oxigenoterapia/relatorio_troca_de_filtro.html', {'relatorio': relatorio})


def aparelhos_alugados(request):
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    if mes and ano:
        mes = int(mes)
        ano = int(ano)
        filter_criteria = [
            Q(equipamento__finalidade_equipamento__agrupamento='VENTILAÇÃO'),
            ~Q(equipamento__empresa_equipamento__iexact='PREFEITURA DE SÃO SEBASTIÃO DO PARAÍSO'),
            (
                Q(paciente__status='ATIVO') | 
                (Q(paciente__status='ÓBITO', paciente__data_obito__year=ano, paciente__data_obito__month=mes)) |
                (Q(paciente__status='ALTA', paciente__data_alta__year=ano, paciente__data_alta__month=mes))
            )
        ]

        pacientes = ModoDeUso.objects.filter(*filter_criteria).select_related('paciente').prefetch_related('equipamento')

        cpap_count = pacientes.filter(equipamento__finalidade_equipamento__finalidade='CPAP').count()
        bipap_count = pacientes.filter(equipamento__finalidade_equipamento__finalidade='BiPAP').count()
        ventilador_count = pacientes.filter(equipamento__finalidade_equipamento__finalidade='VENTILADOR').count()

        return render(
            request, 
            'oxigenoterapia/aparelhos_alugados.html', 
            {'pacientes': pacientes, 'cpap_count': cpap_count, 'bipap_count': bipap_count, 'ventilador_count': ventilador_count}
        )
    
    return render(request, 'oxigenoterapia/aparelhos_alugados.html')


def aparelhos_alugados_pdf(request):
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    if mes and ano:
        mes = int(mes)
        ano = int(ano)
        filter_criteria = [
            Q(equipamento__finalidade_equipamento__agrupamento='VENTILAÇÃO'),
            ~Q(equipamento__empresa_equipamento__iexact='PREFEITURA DE SÃO SEBASTIÃO DO PARAÍSO'),
            (
                Q(paciente__status='ATIVO') | 
                (Q(paciente__status='ÓBITO', paciente__data_obito__year=ano, paciente__data_obito__month=mes)) |
                (Q(paciente__status='ALTA', paciente__data_alta__year=ano, paciente__data_alta__month=mes))
            )
        ]

        pacientes = ModoDeUso.objects.filter(*filter_criteria).select_related('paciente').prefetch_related('equipamento')

        cpap_count = pacientes.filter(equipamento__finalidade_equipamento__finalidade='CPAP').count()
        bipap_count = pacientes.filter(equipamento__finalidade_equipamento__finalidade='BiPAP').count()
        ventilador_count = pacientes.filter(equipamento__finalidade_equipamento__finalidade='VENTILADOR').count()
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

        mes_nome = calendar.month_name[mes].capitalize()

        context = {
        'pacientes': pacientes,
        'cpap_count': cpap_count,
        'bipap_count': bipap_count, 'ventilador_count': ventilador_count,
        'mes': mes_nome,
        'ano': ano,
        }
    
 # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('oxigenoterapia/aparelhos_alugados_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])  # Adicione esta linha

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=aparelhos_alugados_pdf.html'
    return response