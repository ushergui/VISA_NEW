from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Paciente, Fisioterapeuta, Equipamento, Descartavel, Cid, Prescricao, Usf, Atendimento, ModoDeUso, Finalidade
from .forms import PacienteForm, FisioterapeutaForm, EquipamentoForm, DescartavelForm, CidForm, PrescricaoForm, AtendimentoForm, UsfForm, AtendimentoForm, ModoDeUsoForm, FinalidadeForm
from cadastros.models import Logradouro
from django.shortcuts import render, redirect
from django.db.models import Count, F, Q, Max
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
import datetime
from datetime import date
from django.utils import timezone
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.db import transaction
from datetime import datetime, timedelta
import calendar
import locale
from django.contrib import messages
from collections import defaultdict


class PacienteListView(ListView):
    model = Paciente
    template_name = 'paciente_list.html'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('prescricao_new')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Cadastro de Paciente"
        context["botao"] = "Cadastrar"
        return context

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'oxigenoterapia/form.html'

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
        return reverse('detalhes_paciente', args=[self.object.paciente.id])
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Cadastrar Prescrição'
        data['botao'] = 'Cadastrar'
        data['form_class'] = self.form_class.__name__
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
        paciente_id = self.object.paciente.id  # Pegar o id do paciente a partir da prescrição
        return reverse_lazy('detalhes_paciente', kwargs={'paciente_id': paciente_id})  # Redirecionar para a página de detalhes do paciente

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
    template_name = 'oxigenoterapia/form_mododeuso.html'

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
    template_name = 'oxigenoterapia/form_mododeuso.html'

    def get_success_url(self):
        paciente_id = self.object.paciente.id  # Pegar o id do paciente a partir da prescrição
        return reverse_lazy('detalhes_paciente', kwargs={'paciente_id': paciente_id})  # Redirecionar para a página de detalhes do paciente
    
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

        # Atribui o valor do campo 'prescrição' antes de salvar o formulário
        if prescricao_id:
            prescricao = ModoDeUso.objects.get(id=prescricao_id)
            form.instance.prescricao = prescricao

        # Chama o método form_valid da classe base e salva o formulário
        response = super().form_valid(form)

        # Atualiza o objeto ModoDeUso com os novos valores
        if prescricao_id:
            prescricao.equipamento.set(form.cleaned_data['equipamento'])
            prescricao.tempo_de_uso = form.cleaned_data['tempo_de_uso']
            prescricao.litros = form.cleaned_data['litros']
            prescricao.parametros = form.cleaned_data['parametros']
            prescricao.save()

        # Redireciona para a página de detalhes do paciente
        paciente_id = self.object.prescricao.paciente.id
        return HttpResponseRedirect(reverse('detalhes_paciente', kwargs={'paciente_id': paciente_id}))


    
class AtendimentoUpdateView(UpdateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'oxigenoterapia/form.html'
    success_url = reverse_lazy('atendimento_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Alteração de atendimento'
        data['botao'] = 'Alterar'
        return data

    def form_valid(self, form):
        # Chama o método form_valid da classe base e salva o formulário
        response = super().form_valid(form)

        # Obtém o objeto prescricao diretamente da instância do atendimento
        prescricao = self.object.prescricao  # Aqui é a mudança chave

        # Atualiza o objeto ModoDeUso com os novos valores
        prescricao.equipamento.set(form.cleaned_data['equipamento'])
        prescricao.tempo_de_uso = form.cleaned_data['tempo_de_uso']
        prescricao.litros = form.cleaned_data['litros']
        prescricao.parametros = form.cleaned_data['parametros']
        prescricao.save()

        # Redireciona para a página de detalhes do paciente
        paciente_id = self.object.prescricao.paciente.id
        return HttpResponseRedirect(reverse('detalhes_paciente', kwargs={'paciente_id': paciente_id}))



class AtendimentoDeleteView(DeleteView):
    model = Atendimento
    template_name = 'oxigenoterapia/atendimento_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        # Guarda o objeto em uma variável antes dele ser deletado
        self.object = self.get_object()

        # Chama o método delete da superclasse
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        # Obtendo o id do paciente relacionado ao atendimento
        paciente_id = self.object.prescricao.paciente.id

        # Retornando a URL de redirecionamento após a exclusão
        return reverse('detalhes_paciente', kwargs={'paciente_id': paciente_id})



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
    mes = int(request.GET.get('month'))
    ano = int(request.GET.get('year'))
    nome_fisioterapeuta = request.GET.get('fisioterapeuta')
    data_inicial = date(ano, mes, 1)
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    data_final = date(ano, mes, ultimo_dia)

    atendimentos = Atendimento.objects.filter(data_atendimento__range=[data_inicial, data_final])
    total_obitos_periodo = Paciente.objects.filter(status="ÓBITO", data_obito__range=[data_inicial, data_final]).count()
    total_altas_periodo = Paciente.objects.filter(status="ALTA", data_alta__range=[data_inicial, data_final]).count()
    
    detalhes_atendimentos = Atendimento.objects.filter(
    data_atendimento__range=[data_inicial, data_final]
    ).values(
    'data_atendimento',
    'prescricao__paciente__nome_paciente',
    'fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta'
    ).order_by('data_atendimento', 'prescricao__paciente__nome_paciente') 

    if nome_fisioterapeuta:
        detalhes_atendimentos = detalhes_atendimentos.filter(fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta=nome_fisioterapeuta)
   
    ids_atendimentos_interesse = atendimentos.values_list('id', flat=True)

    modos_de_uso = ModoDeUso.objects.filter(atendimentos__id__in=ids_atendimentos_interesse)

    # Inicialmente, crie um conjunto vazio para armazenar os IDs dos pacientes atendidos.
    pacientes_atendidos = set()

    # Filtre todos os atendimentos no período desejado.
    atendimentos_no_periodo = Atendimento.objects.filter(data_atendimento__range=[data_inicial, data_final])

    if nome_fisioterapeuta:
        atendimentos_no_periodo = atendimentos_no_periodo.filter(fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta=nome_fisioterapeuta)

    # Obtenha os IDs de pacientes únicos desse filtro.
    ids_pacientes_unicos = atendimentos_no_periodo.values_list('prescricao__paciente__id', flat=True).distinct()

    # Atualize o conjunto com esses IDs.
    pacientes_atendidos.update(ids_pacientes_unicos)

    # O total de atendimentos agora será o tamanho deste conjunto.
    total_atendimentos = atendimentos_no_periodo.count()

    inicio_contagem = date(2013, 1, 1)
    total_ativos_periodo = ModoDeUso.objects.filter(data_inicio_uso__range=[inicio_contagem, data_final]).count()
    #total_ativos_periodo = ModoDeUso.objects.filter(data_inicio_uso__range=[inicio_contagem, data_final]).exclude(paciente__status__in=["ÓBITO", "ALTA"]).count()
    
    total_ativos_periodo -= Paciente.objects.filter(data_obito__range=[inicio_contagem, data_final]).count()
   
    total_ativos_periodo -= Paciente.objects.filter(data_alta__range=[inicio_contagem, data_final]).count()
    
    
    total_ativos = Paciente.objects.filter(status="ATIVO").count()
    fisioterapeutas = Fisioterapeuta.objects.all()

    context = {
        'ano_pesquisa': ano,
        'mes_pesquisa': mes,
        'fisioterapeuta_pesquisa': nome_fisioterapeuta,
        'total_atendimentos': total_atendimentos,
        'total_obitos_periodo': total_obitos_periodo,
        'detalhes_atendimentos': detalhes_atendimentos,
        'total_altas_periodo': total_altas_periodo,
        'total_ativos_periodo': total_ativos_periodo,
        'total_ativos': total_ativos,
        'fisioterapeutas': fisioterapeutas,
    }

    return render(request, 'oxigenoterapia/consulta_atendimentos.html', context)

def consulta_atendimentos_pdf(request):
    mes = int(request.GET.get('month'))
    ano = int(request.GET.get('year'))
    nome_fisioterapeuta = request.GET.get('fisioterapeuta')
    data_inicial = date(ano, mes, 1)
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    data_final = date(ano, mes, ultimo_dia)

    atendimentos = Atendimento.objects.filter(data_atendimento__range=[data_inicial, data_final])
    total_obitos_periodo = Paciente.objects.filter(status="ÓBITO", data_obito__range=[data_inicial, data_final]).count()
    total_altas_periodo = Paciente.objects.filter(status="ALTA", data_alta__range=[data_inicial, data_final]).count()
    
    detalhes_atendimentos = Atendimento.objects.filter(
    data_atendimento__range=[data_inicial, data_final]
    ).values(
    'data_atendimento',
    'prescricao__paciente__nome_paciente',
    'fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta'
    ).order_by('data_atendimento', 'prescricao__paciente__nome_paciente') 

    if nome_fisioterapeuta:
        detalhes_atendimentos = detalhes_atendimentos.filter(fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta=nome_fisioterapeuta)
   
    ids_atendimentos_interesse = atendimentos.values_list('id', flat=True)

    modos_de_uso = ModoDeUso.objects.filter(atendimentos__id__in=ids_atendimentos_interesse)

    # Inicialmente, crie um conjunto vazio para armazenar os IDs dos pacientes atendidos.
    pacientes_atendidos = set()

    # Filtre todos os atendimentos no período desejado.
    atendimentos_no_periodo = Atendimento.objects.filter(data_atendimento__range=[data_inicial, data_final])

    if nome_fisioterapeuta:
        atendimentos_no_periodo = atendimentos_no_periodo.filter(fisioterapeuta_atendimento__primeiro_nome_fisioterapeuta=nome_fisioterapeuta)

    # Obtenha os IDs de pacientes únicos desse filtro.
    ids_pacientes_unicos = atendimentos_no_periodo.values_list('prescricao__paciente__id', flat=True).distinct()

    # Atualize o conjunto com esses IDs.
    pacientes_atendidos.update(ids_pacientes_unicos)

    # O total de atendimentos agora será o tamanho deste conjunto.
    total_atendimentos = atendimentos_no_periodo.count()

    inicio_contagem = date(2013, 1, 1)
    total_ativos_periodo = ModoDeUso.objects.filter(data_inicio_uso__range=[inicio_contagem, data_final]).count()
    #total_ativos_periodo = ModoDeUso.objects.filter(data_inicio_uso__range=[inicio_contagem, data_final]).exclude(paciente__status__in=["ÓBITO", "ALTA"]).count()
    
    total_ativos_periodo -= Paciente.objects.filter(data_obito__range=[inicio_contagem, data_final]).count()
   
    total_ativos_periodo -= Paciente.objects.filter(data_alta__range=[inicio_contagem, data_final]).count()
    
    
    total_ativos = Paciente.objects.filter(status="ATIVO").count()
    fisioterapeutas = Fisioterapeuta.objects.all()

    context = {
        'ano_pesquisa': ano,
        'mes_pesquisa': mes,
        'fisioterapeuta_pesquisa': nome_fisioterapeuta,
        'total_atendimentos': total_atendimentos,
        'total_obitos_periodo': total_obitos_periodo,
        'detalhes_atendimentos': detalhes_atendimentos,
        'total_altas_periodo': total_altas_periodo,
        'total_ativos_periodo': total_ativos_periodo,
        'total_ativos': total_ativos,
        'fisioterapeutas': fisioterapeutas,
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
        equipamento__finalidade_equipamento__finalidade='OXIGENOTERAPIA').values_list('paciente_id', flat=True).distinct()
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
        equipamento__finalidade_equipamento__finalidade='OXIGENOTERAPIA').values_list('paciente_id', flat=True).distinct()
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
    fisioterapeuta_id = request.GET.get('fisioterapeuta', None)
    
    equipamento = request.GET.get('equipamento', None)
    busca_submetida = False  # Inicializando como False

    # Recuperar opções de seleção
    fisioterapeutas = Fisioterapeuta.objects.all()
    equipamentos = Finalidade.objects.values_list('agrupamento', flat=True).distinct()

    # Iniciar com todos os objetos ModoDeUso onde o paciente está ativo
    modos_uso = ModoDeUso.objects.filter(paciente__status='ATIVO').annotate(
        nome_fantasia_usf=F('paciente__usf_paciente__nome_fantasia_usf'),
        nome_paciente=F('paciente__nome_paciente')
    ).order_by('nome_fantasia_usf', 'nome_paciente')

    # Aplicar filtros se eles foram fornecidos
    if fisioterapeuta_id:
        modos_uso = modos_uso.filter(paciente__usf_paciente__nome_fisioterapeuta__id=fisioterapeuta_id)
        fisioterapeuta_nome = Fisioterapeuta.objects.get(id=fisioterapeuta_id).nome_fisioterapeuta
    else:
        fisioterapeuta_nome = None

    if equipamento:
        modos_uso = modos_uso.filter(equipamento__finalidade_equipamento__agrupamento=equipamento)

    if request.GET:  # Verificar se a requisição é do tipo GET
        busca_submetida = True
    
    modos_uso_por_paciente = defaultdict(list)
    for modo_uso in modos_uso:
        modos_uso_por_paciente[modo_uso.paciente].append(modo_uso)
    data_atendimento_recente = ModoDeUso.objects.filter(paciente__status='ATIVO').annotate(
        data_atendimento_recente=Max('atendimentos__data_atendimento')
    ).values('paciente__id', 'data_atendimento_recente')

    data_atendimento_dict = {item['paciente__id']: item['data_atendimento_recente'] for item in data_atendimento_recente}

    context = {
        'modos_uso_por_paciente': dict(modos_uso_por_paciente),
        'modos_uso': modos_uso,
        'fisioterapeutas': fisioterapeutas,
        'equipamentos': equipamentos,
        'fisioterapeuta_pesquisa': fisioterapeuta_id,
        'fisioterapeuta_nome': fisioterapeuta_nome,
        'equipamento_pesquisa': equipamento,
        'busca_submetida': busca_submetida,  # Adicionando a variável no contexto
        'data_atendimento_dict': data_atendimento_dict,
    }

    return render(request, 'oxigenoterapia/relatorio_para_visita.html', context)



def relatorio_para_visita_pdf(request):
    fisioterapeuta_id = request.GET.get('fisioterapeuta', None)
    
    equipamento = request.GET.get('equipamento', None)
    busca_submetida = False  # Inicializando como False

    # Recuperar opções de seleção
    fisioterapeutas = Fisioterapeuta.objects.all()
    equipamentos = Finalidade.objects.values_list('agrupamento', flat=True).distinct()

    # Iniciar com todos os objetos ModoDeUso onde o paciente está ativo
    modos_uso = ModoDeUso.objects.filter(paciente__status='ATIVO').annotate(
        nome_fantasia_usf=F('paciente__usf_paciente__nome_fantasia_usf'),
        nome_paciente=F('paciente__nome_paciente')
    ).order_by('nome_fantasia_usf', 'nome_paciente')

    # Aplicar filtros se eles foram fornecidos
    if fisioterapeuta_id:
        modos_uso = modos_uso.filter(paciente__usf_paciente__nome_fisioterapeuta__id=fisioterapeuta_id)
        fisioterapeuta_nome = Fisioterapeuta.objects.get(id=fisioterapeuta_id).primeiro_nome_fisioterapeuta
    else:
        fisioterapeuta_nome = None

    if equipamento:
        modos_uso = modos_uso.filter(equipamento__finalidade_equipamento__agrupamento=equipamento)

    if request.GET:  # Verificar se a requisição é do tipo GET
        busca_submetida = True
    
    modos_uso_por_paciente = defaultdict(list)
    for modo_uso in modos_uso:
        modos_uso_por_paciente[modo_uso.paciente].append(modo_uso)
    data_atendimento_recente = ModoDeUso.objects.filter(paciente__status='ATIVO').annotate(
        data_atendimento_recente=Max('atendimentos__data_atendimento')
    ).values('paciente__id', 'data_atendimento_recente')

    data_atendimento_dict = {item['paciente__id']: item['data_atendimento_recente'] for item in data_atendimento_recente}

    context = {
        'modos_uso_por_paciente': dict(modos_uso_por_paciente),
        'modos_uso': modos_uso,
        'fisioterapeutas': fisioterapeutas,
        'equipamentos': equipamentos,
        'fisioterapeuta_pesquisa': fisioterapeuta_id,
        'fisioterapeuta_nome': fisioterapeuta_nome,
        'equipamento_pesquisa': equipamento,
        'busca_submetida': busca_submetida,  # Adicionando a variável no contexto
        'data_atendimento_dict': data_atendimento_dict,
    }
 # Aqui o código renderiza o HTML e cria o PDF
    html_template = get_template('oxigenoterapia/relatorio_para_visita_pdf.html').render(context)
    html = HTML(string=html_template)
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])  # Adicione esta linha

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=relatorio_para_visita_pdf.html'
    return response


class AtendimentosRealizados(TemplateView):
    template_name = "oxigenoterapia/atendimentos_realizados.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fisioterapeutas'] = Fisioterapeuta.objects.all()
        return context


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
        
        equipamentos = prescricao_recente.equipamento.all()
        nome_equipamentos = ", ".join([equipamento.nome_equipamento for equipamento in equipamentos])
        
        if any(equipamento.finalidade_equipamento.agrupamento == "VENTILAÇÃO" for equipamento in equipamentos):
            relatorio.append({
                'nome_paciente': paciente.nome_paciente,
                'telefone_1': paciente.telefone_paciente1,
                'telefone_2': paciente.telefone_paciente2,
                'data_recente': data_recente,
                'nome_equipamentos': nome_equipamentos,
            })

    return render(request, 'oxigenoterapia/relatorio_troca_de_filtro.html', {'relatorio': relatorio})

def relatorio_troca_de_mascara(request):
    cutoff_date = datetime.now() - timedelta(days=6*30)

    prescricoes = ModoDeUso.objects.filter(
        Q(data_inicio_uso__lt=cutoff_date) &
        ~Q(atendimentos__data_atendimento__gt=cutoff_date, atendimentos__troca_de_mascara=True)
    ).values('paciente')

    pacientes = Paciente.objects.filter(id__in=prescricoes)

    relatorio = []
    for paciente in pacientes:
        prescricao_recente = ModoDeUso.objects.filter(paciente=paciente).order_by('-data_inicio_uso').first()
        atendimento_recente = Atendimento.objects.filter(prescricao__paciente=paciente).order_by('-data_atendimento').first()
        
        data_recente = max(prescricao_recente.data_inicio_uso, atendimento_recente.data_atendimento) if atendimento_recente else prescricao_recente.data_inicio_uso
        
        equipamentos = prescricao_recente.equipamento.all()
        nome_equipamentos = ", ".join([equipamento.nome_equipamento for equipamento in equipamentos])
        
        if any(equipamento.finalidade_equipamento.agrupamento == "VENTILAÇÃO" for equipamento in equipamentos):
            relatorio.append({
                'nome_paciente': paciente.nome_paciente,
                'telefone_1': paciente.telefone_paciente1,
                'telefone_2': paciente.telefone_paciente2,
                'data_recente': data_recente,
                'nome_equipamentos': nome_equipamentos,
            })

    return render(request, 'oxigenoterapia/relatorio_troca_de_mascara.html', {'relatorio': relatorio})


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
        
        context = {
            'pacientes': pacientes, 
            'cpap_count': cpap_count, 
            'bipap_count': bipap_count, 
            'ventilador_count': ventilador_count,
            'mes': mes,
            'ano': ano
        }

        # Aqui o código renderiza o HTML e cria o PDF
        html_template = get_template('oxigenoterapia/aparelhos_alugados_pdf.html').render(context)
        html = HTML(string=html_template)
        pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=aparelhos_alugados_pdf.html'
        return response
    else:
        # Se mes e ano não forem passados, renderiza um PDF em branco ou com um template padrão
        html_template = get_template('oxigenoterapia/aparelhos_alugados_pdf.html').render()
        html = HTML(string=html_template)
        pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')])

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=aparelhos_alugados_pdf.html'
        return response

def pesquisa_paciente(request):
    termo_pesquisa = request.GET.get('q', '')
    modos_uso = []
    if termo_pesquisa:
        modos_uso = ModoDeUso.objects.filter(
            Q(paciente__nome_paciente__icontains=termo_pesquisa) | 
            Q(paciente__prontuario_paciente__icontains=termo_pesquisa)
        )
    return render(request, 'oxigenoterapia/pesquisa_paciente.html', {'modos_uso': modos_uso})


def detalhes_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    prescricao = Prescricao.objects.filter(paciente=paciente).order_by('-data_inicio_uso').first()
    mododeuso = ModoDeUso.objects.filter(paciente=paciente).order_by('-data_inicio_uso').first()
    atendimentos = Atendimento.objects.filter(prescricao=mododeuso).order_by('-data_atendimento')
    return render(request, 'oxigenoterapia/detalhes_paciente.html', {'paciente': paciente, 'prescricao': prescricao, 'mododeuso': mododeuso, 'atendimentos': atendimentos})

def termo_de_uso(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    # Obtém o ModoDeUso mais recente para este paciente que está no agrupamento "VENTILAÇÃO"
    mododeuso = ModoDeUso.objects.filter(paciente=paciente, equipamento__finalidade_equipamento__agrupamento="VENTILAÇÃO").order_by('-data_inicio_uso').first()

    context = {
        'paciente': paciente,
        'mododeuso': mododeuso  # passa a informação do ModoDeUso para o contexto
    }
    
    html_template = get_template('oxigenoterapia/termo_de_uso_de_bem_publico.html').render(context)
    html = HTML(string=html_template, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')]) 

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=termo_de_uso.html'
    return response

def oficio_cpap_bipap(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    # Obtém o ModoDeUso mais recente para este paciente que está no agrupamento "VENTILAÇÃO"
    mododeuso = ModoDeUso.objects.filter(paciente=paciente, equipamento__finalidade_equipamento__agrupamento="VENTILAÇÃO").order_by('-data_inicio_uso').first()
    prescricao = Prescricao.objects.filter(paciente=paciente).order_by('-data_inicio_uso').first()
    context = {
        'paciente': paciente,
        'mododeuso': mododeuso,
        'prescricao': prescricao  # passa a informação do ModoDeUso para o contexto
    }
    
    html_template = get_template('oxigenoterapia/oficio_cpap_bipap.html').render(context)
    html = HTML(string=html_template, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4 landscape; }')]) 

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=oficio_cpap_bipap.html'
    return response