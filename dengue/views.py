from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notificacao, Semana
from .forms import NotificacaoForm, SemanaForm, EncerrarNotificacaoForm
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
    
def positivos_bairros(request):
    semana = request.GET.get('semana')
    ano = request.GET.get('ano')
    
    notificacoes = None
    pesquisa_realizada = False  # Inicializa a variável como False
    if semana and ano:
        pesquisa_realizada = True
        try:
            semana = int(semana)
            ano = int(ano)
            notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__semana=semana,
                semana_epidemiologica__ano=ano,
                resultado__in=["Positivo NS1", "Positivo sorologia", "Isolamento viral positivo"]
            ).values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()

    semana_menos_1 = semana - 1 if semana else None
    semana_menos_2 = semana - 2 if semana else None
    semana_menos_3 = semana - 3 if semana else None
    
    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': semana,
        'ano_pesquisa': ano,
        'semana': semana,
        'semana_menos_1': semana_menos_1,
        'semana_menos_2': semana_menos_2,
        'semana_menos_3': semana_menos_3,
        'pesquisa_realizada': pesquisa_realizada,
        'ano': ano,
    }

    return render(request, 'dengue/positivos_bairros.html', context)


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
            return redirect('index_dengue') # Substitua 'listar_notificacoes' pelo nome da URL da lista de notificações, se necessário.
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
    agendamentos = None  # Altere para None

    desconhecidos = None  # Adicione esta linha
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
        desconhecidos = (
            Notificacao.objects
            .filter(data_agendamento=data_formatada, usf__isnull=True)
            
        )

    context = {
        'termo_pesquisa': termo_pesquisa,
        'agendamentos': agendamentos,
        'desconhecidos': desconhecidos,
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
        notificacoes = Notificacao.objects.none()

    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': termo_pesquisa,
    }

    return render(request, 'dengue/agendados.html', context)


def aguardando_resultados(request):
    notificacoes = Notificacao.objects.filter(resultado='Aguardando resultado')
    return render(request, 'dengue/aguardando_resultados.html', {'notificacoes': notificacoes})

def aguardando_ou_nao_agendado(request):
    notificacoes = Notificacao.objects.filter(
        Q(resultado='Aguardando resultado') | 
        Q(resultado='Aguardando agendamento') |
        Q(resultado='Aguardando coleta') |
        Q(resultado='Não agendado')
    )
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

def listar_casos_abertos(request):
    query = request.GET.get('q')
    notificacoes = Notificacao.objects.none()  # Inicializa como um queryset vazio
    total_registros = 0

    if query:  # Se um termo de pesquisa foi fornecido
        notificacoes = Notificacao.objects.filter(
            Q(data_encerramento__isnull=True),
            Q(sinan__icontains=query) | Q(nome__icontains=query)
        )
        total_registros = notificacoes.count()

    return render(request, 'dengue/listar_casos_abertos.html', {'notificacoes': notificacoes, 'total_registros': total_registros})

def encerrar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)
    if request.method == 'POST':
        form = EncerrarNotificacaoForm(request.POST, instance=notificacao)
        if form.is_valid():
            form.save()
            return redirect('listar_casos_abertos')  # Redireciona para a página de listagem após o encerramento
    else:
        form = EncerrarNotificacaoForm(instance=notificacao)
    return render(request, 'dengue/form_encerramento.html', {'form': form})


def notificacoes_recentes(request):
    erro_msg = None
    tabela_notificacoes = []

    if request.method == 'GET' and 'semana' in request.GET and 'ano' in request.GET:
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')

        if semana and ano:
            semanas_pesquisa = [int(semana) - i for i in range(4) if int(semana) - i > 0]
            tabela_notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__semana__in=semanas_pesquisa,
                semana_epidemiologica__ano=ano
            ).order_by('nome')

            if not tabela_notificacoes:
                erro_msg = "Nenhuma notificação encontrada no período"
        else:
            erro_msg = "Ambos os campos, semana e ano, são obrigatórios."

    return render(request, 'dengue/notificacoes_recentes.html', {
        'tabela_notificacoes': tabela_notificacoes,
        'erro_msg': erro_msg
    })

def chikungunya(request):
    erro_msg = None
    tabela_notificacoes = None  # Inicialmente definido como None

    if request.method == 'GET':
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')

        if semana and ano:
            semanas_pesquisa = [int(semana) - i for i in range(4) if int(semana) - i > 0]
            tabela_notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__semana__in=semanas_pesquisa,
                semana_epidemiologica__ano=ano,
                classificacao='Chikungunya'
            ).order_by('nome')

            if not tabela_notificacoes:
                erro_msg = "Nenhuma notificação encontrada no período"

        elif semana and not ano:
            erro_msg = "É necessário digitar um ano."

        elif ano and not semana:
            tabela_notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__ano=ano,
                classificacao='Chikungunya'
            ).order_by('nome')

            if not tabela_notificacoes:
                erro_msg = "Nenhuma notificação encontrada no período"

        elif not semana and not ano and request.GET:
            erro_msg = "É necessário digitar pelo menos o ano."

    return render(request, 'dengue/chikungunya.html', {
        'tabela_notificacoes': tabela_notificacoes,
        'erro_msg': erro_msg
    })

def internados(request):
    erro_msg = None
    tabela_notificacoes = None

    formulario_enviado = 'semana' in request.GET or 'ano' in request.GET  # Aqui é onde detectamos se o formulário foi enviado

    if request.method == 'GET':
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')

        # Base para todas as queries
        base_query = Notificacao.objects.exclude(internacao__isnull=True).order_by('nome')

        if semana and ano:
            semanas_pesquisa = [int(semana) - i for i in range(4) if int(semana) - i > 0]
            tabela_notificacoes = base_query.filter(
                semana_epidemiologica__semana__in=semanas_pesquisa,
                semana_epidemiologica__ano=ano,
            )
        elif semana and not ano:
            erro_msg = "É necessário digitar um ano."
        elif ano and not semana:
            tabela_notificacoes = base_query.filter(
                semana_epidemiologica__ano=ano,
            )
        elif not semana and not ano and formulario_enviado:
            erro_msg = "É necessário digitar pelo menos o ano."

        if tabela_notificacoes and not tabela_notificacoes.exists():
            erro_msg = "Nenhuma notificação encontrada no período"

    return render(request, 'dengue/internados.html', {
        'tabela_notificacoes': tabela_notificacoes,
        'erro_msg': erro_msg,
        'formulario_enviado': formulario_enviado
    })


def positivos_recentes(request):
    erro_msg = None
    tabela_notificacoes = []
    total_notificacoes = 0
    formulario_submetido = False
    
    if request.method == 'GET':
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')
        print(semana, ano)
        
        if semana is not None or ano is not None:
            formulario_submetido = True

        if semana and ano:
            try:
                semana = int(semana)
                ano = int(ano)
            except ValueError:
                erro_msg = "Os campos semana e ano devem ser numéricos."
                return render(request, 'dengue/positivos_recentes.html', {'erro_msg': erro_msg})
            
            # Validação de semana e ano
            if semana < 1 or semana > 52:
                erro_msg = "A semana deve estar entre 1 e 52."
            elif ano < 2022:  # Supondo que 2022 é o ano mínimo permitido
                erro_msg = "O ano não pode ser menor que 2022."
            
            if erro_msg is None:
                semanas_pesquisa = [semana - i for i in range(4) if semana - i > 0]
                tabela_notificacoes = Notificacao.objects.filter(
                    semana_epidemiologica__semana__in=semanas_pesquisa,
                    semana_epidemiologica__ano=ano,
                    resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo']
                ).order_by('nome')
                total_notificacoes = tabela_notificacoes.count()
                if total_notificacoes == 0:
                        erro_msg = "Nenhuma notificação encontrada no período especificado."
        elif formulario_submetido:
            erro_msg = "Ambos os campos, semana e ano, são obrigatórios."
    
    return render(request, 'dengue/positivos_recentes.html', {
    'tabela_notificacoes': tabela_notificacoes,
    'erro_msg': erro_msg,
    'total_notificacoes': total_notificacoes if erro_msg is None else 0,
    'semana': semana,
    'ano' : ano,
})
