from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notificacao, Semana
from .forms import NotificacaoForm, SemanaForm
from django.db.models import Q, Count
from django.core.exceptions import ValidationError
from cadastros.models import Logradouro
from django.http import JsonResponse
from datetime import datetime

def check_duplicate(request):
    nome = request.GET.get("nome")
    logradouro = request.GET.get("logradouro")
    notificacao_id = request.GET.get("notificacao_id")

    if nome and logradouro:
        if notificacao_id and notificacao_id != 'None':
            notificacoes = Notificacao.objects.filter(nome=nome, logradouro_paciente_id=logradouro).exclude(pk=notificacao_id)
        else:
            notificacoes = Notificacao.objects.filter(nome=nome, logradouro_paciente_id=logradouro)

        if notificacoes.exists():
            notificacao = notificacoes.first()
            mensagem = f"Existe uma notificação deste paciente na data: {notificacao.data_notificacao.strftime('%d/%m/%Y')} com resultado: {notificacao.resultado}. Deseja continuar?"
            return JsonResponse({"exists": True, "message": mensagem})
        else:
            return JsonResponse({"exists": False})
    else:
        return JsonResponse({"exists": False})


def listar_notificacoes(request):
    search_query = request.GET.get('q')
    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__in=ultimas_4_semanas,
                resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo']
            )
        except ValueError:
            notificacoes = Notificacao.objects.all()
    else:
        notificacoes = Notificacao.objects.all()

    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': search_query
    }

    return render(request, 'dengue/listar_notificacoes.html', context)

def listar_notificacoes_gerais(request):
    search_query = request.GET.get('q')
    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__in=ultimas_4_semanas            )
        except ValueError:
            notificacoes = Notificacao.objects.all()
    else:
        notificacoes = Notificacao.objects.all()

    context = {
        'notificacoes': notificacoes,
        'termo_pesquisas': search_query
    }

    return render(request, 'dengue/listar_notificacoes.html', context)


def total_bairros(request):
    search_query = request.GET.get('q')
    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__in=ultimas_4_semanas
            ).values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()
    else:
        notificacoes = Notificacao.objects.all().values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')

    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': search_query
    }

    return render(request, 'dengue/total_por_bairros.html', context)
    
def total_bairros_positivos(request):
    search_query = request.GET.get('q')
    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__in=ultimas_4_semanas,
                resultado__in=["Positivo NS1", "Positivo sorologia", "Isolamento viral positivo"]
            ).values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()
    else:
        notificacoes = Notificacao.objects.filter(
            resultado__in=["Positivo NS1", "Positivo sorologia", "Isolamento viral positivo"]
        ).values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')

    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': search_query
    }

    return render(request, 'dengue/total_por_bairros.html', context)

def criar_notificacao(request):
    if request.method == 'POST':
        form = NotificacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('criar_notificacao')  # Modifique esta linha
    else:
        form = NotificacaoForm()

    return render(request, 'dengue/form_dengue.html', {'form': form})


def editar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)

    if request.method == 'POST':
        form = NotificacaoForm(request.POST, instance=notificacao)
        if form.is_valid():
            form.save()
            return redirect('listar_notificacoes') # Substitua 'listar_notificacoes' pelo nome da URL da lista de notificações, se necessário.
    else:
        form = NotificacaoForm(instance=notificacao)

    return render(request, 'dengue/form_dengue.html', {'form': form})


def deletar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)
    notificacao.delete()
    messages.success(request, 'Notificação excluída com sucesso!')
    return redirect('listar_notificacoes')

def boletim_resumo(request):
    search_query = request.GET.get('q')
    search_year = request.GET.get('year')
    notificacoes = Notificacao.objects.all()

    if search_year:
        try:
            year = int(search_year)
            notificacoes = notificacoes.filter(semana_epidemiologica__ano=year)
        except ValueError:
            notificacoes = Notificacao.objects.none()

    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = notificacoes.filter(
                semana_epidemiologica__semana__in=ultimas_4_semanas
            )
        except ValueError:
            notificacoes = Notificacao.objects.none()

    resultado_agrupado = notificacoes.values('semana_epidemiologica').annotate(
        casos_positivos=Count('pk', filter=Q(
            resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo'])),
        casos_negativos=Count('pk', filter=Q(
            resultado__in=['Negativo NS1', 'Negativo sorologia', 'Isolamento viral negativo'])),
        aguardando=Count('pk', filter=Q(
            resultado__in=['Aguardando coleta', 'Aguardando agendamento', 'Aguardando resultado', 'Não agendado'])),
        faltas_recusa=Count('pk', filter=Q(resultado__in=['Faltou', 'Recusou'])),
        total_internacao=Count('pk', filter=Q(internacao__isnull=False)),
        total_obito=Count('pk', filter=Q(obito__isnull=False)),
    ).order_by('semana_epidemiologica')
    total_casos_positivos = sum(item['casos_positivos'] for item in resultado_agrupado)
    total_casos_negativos = sum(item['casos_negativos'] for item in resultado_agrupado)
    total_aguardando = sum(item['aguardando'] for item in resultado_agrupado)
    total_faltas_recusa = sum(item['faltas_recusa'] for item in resultado_agrupado)
    total_internacao = sum(item['total_internacao'] for item in resultado_agrupado)
    total_obito = sum(item['total_obito'] for item in resultado_agrupado)

    context = {
        'resultado_agrupado': resultado_agrupado,
        'termo_pesquisa': search_query,
        'total_casos_positivos': total_casos_positivos,
        'total_casos_negativos': total_casos_negativos,
        'total_aguardando': total_aguardando,
        'total_faltas_recusa': total_faltas_recusa,
        'total_internacao': total_internacao,
        'total_obito': total_obito,
    }
    return render(request, 'dengue/boletim_resumo.html', context)

def semana_epidemiologica(request):
    search_query = request.GET.get('q2')
    search_year = request.GET.get('ano_pesquisa')
    notificacoes = Notificacao.objects.values('semana_epidemiologica', 'semana_epidemiologica__data_inicio_semana',
                                              'semana_epidemiologica__data_fim_semana').annotate(quantidade=Count('semana_epidemiologica')).order_by('semana_epidemiologica')

    if search_year:
        try:
            year = int(search_year)
            notificacoes = notificacoes.filter(semana_epidemiologica__ano=year)
        except ValueError:
            notificacoes = Notificacao.objects.none()

    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = notificacoes.filter(semana_epidemiologica__semana__in=ultimas_4_semanas)
        except ValueError:
            notificacoes = Notificacao.objects.none()

    return render(request, 'dengue/semana_epidemiologica.html', {'notificacoes': notificacoes, 'termo_pesquisa': search_query, 'ano_pesquisa': search_year})


def boletim_resumo_totais(request):
    search_query = request.GET.get('q')
    search_year = request.GET.get('year')
    notificacoes = Notificacao.objects.all()

    if search_year:
        try:
            year = int(search_year)
            notificacoes = notificacoes.filter(semana_epidemiologica__ano=year)
        except ValueError:
            notificacoes = Notificacao.objects.none()

    if search_query:
        try:
            semana_atual = int(search_query)
            ultimas_4_semanas = [semana_atual - i for i in range(4)]
            notificacoes = notificacoes.filter(
                semana_epidemiologica__semana__in=ultimas_4_semanas
            )
        except ValueError:
            notificacoes = Notificacao.objects.none()

    resultado_agrupado = notificacoes.values('semana_epidemiologica').annotate(
        casos_positivos=Count('pk', filter=Q(
            resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo'])),
        casos_negativos=Count('pk', filter=Q(
            resultado__in=['Negativo NS1', 'Negativo sorologia', 'Isolamento viral negativo'])),
        aguardando=Count('pk', filter=Q(
            resultado__in=['Aguardando coleta', 'Aguardando agendamento', 'Aguardando resultado'])),
        faltas_recusa=Count('pk', filter=Q(resultado__in=['Faltou', 'Recusou'])),
        total_internacao=Count('pk', filter=Q(internacao__isnull=False)),
        total_obito=Count('pk', filter=Q(obito__isnull=False)),
    ).order_by('semana_epidemiologica')

    total_casos_positivos = sum(item['casos_positivos'] for item in resultado_agrupado)
    total_casos_negativos = sum(item['casos_negativos'] for item in resultado_agrupado)
    total_aguardando = sum(item['aguardando'] for item in resultado_agrupado)
    total_faltas_recusa = sum(item['faltas_recusa'] for item in resultado_agrupado)
    total_internacao = sum(item['total_internacao'] for item in resultado_agrupado)
    total_obito = sum(item['total_obito'] for item in resultado_agrupado)
    total_notificacoes = notificacoes.count()

    context = {
        'termo_pesquisa': search_query,
        'total_casos_positivos': total_casos_positivos,
        'total_casos_negativos': total_casos_negativos,
        'total_aguardando': total_aguardando,
        'total_faltas_recusa': total_faltas_recusa,
        'total_internacao': total_internacao,
        'total_obito': total_obito,
        'total_notificacoes': total_notificacoes,
    }

    return render(request, 'dengue/boletim_resumo_totais.html', context)


def listar_semanas(request):
    semanas = Semana.objects.all()
    return render(request, 'dengue/listar_semanas.html', {'semanas': semanas})


def form_semana(request, semana_id=None):
    if semana_id:
        semana = get_object_or_404(Semana, id=semana_id)
    else:
        semana = None

    if request.method == 'POST':
        form = SemanaForm(request.POST, instance=semana)
        if form.is_valid():
            form.save()
            return redirect('listar_semanas')
    else:
        form = SemanaForm(instance=semana)

    return render(request, 'dengue/form_semana.html', {'form': form})


def excluir_semana(request, semana_id):
    semana = get_object_or_404(Semana, id=semana_id)
    semana.delete()
    return redirect('listar_semanas')

def api_semanas(request):
    semanas = Semana.objects.all().values('id', 'data_inicio_semana', 'data_fim_semana')
    return JsonResponse(list(semanas), safe=False)

def motorista(request):
    termo_pesquisa = request.GET.get('q', None)
    agendamentos = []

    if termo_pesquisa:
        try:
            data_formatada = datetime.strptime(termo_pesquisa, '%d/%m/%Y').date()
            agendamentos = (
                Notificacao.objects
                .filter(data_agendamento=data_formatada)
                .values('usf')
                .annotate(total_agendamentos=Count('id'))
                .order_by('usf')
            )
        except ValueError:
            # Você pode definir uma mensagem de erro para exibir no template, se desejar.
            pass

    context = {
        'termo_pesquisa': termo_pesquisa,
        'agendamentos': agendamentos,
    }

    return render(request, 'dengue/motorista.html', context)


def agendados(request):
    termo_pesquisa = request.GET.get('q', None)

    if termo_pesquisa:
        try:
            data_agendamento = datetime.strptime(termo_pesquisa, '%d/%m/%Y').date()
            notificacoes = Notificacao.objects.filter(data_agendamento=data_agendamento)
        except ValueError:
            notificacoes = Notificacao.objects.none()
            messages.error(request, "O valor informado tem um formato de data inválido. Deve ser no formato DD/MM/YYYY.")
    else:
        notificacoes = Notificacao.objects.all()

    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': termo_pesquisa,
    }

    return render(request, 'dengue/agendados.html', context)


def aguardando_resultados(request):
    notificacoes = Notificacao.objects.filter(resultado='Aguardando resultado')
    return render(request, 'dengue/aguardando_resultados.html', {'notificacoes': notificacoes})

def pesquisar_notificacoes(request):
    termo_buscas = request.GET.get('q')

    if termo_buscas:
        notificacoes = Notificacao.objects.filter(nome__icontains=termo_buscas) | Notificacao.objects.filter(logradouro_paciente__nome_logradouro__icontains=termo_buscas) |  Notificacao.objects.filter(sinan__icontains=termo_buscas)
    else:
        notificacoes = Notificacao.objects.all()

    context = {
        'notificacoes': notificacoes,
        'termo_buscas': termo_buscas,
    }

    return render(request, 'dengue/listar_notificacoes.html', context)
