from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notificacao, Semana
from .forms import NotificacaoForm, SemanaForm, EncerrarNotificacaoForm
from django.db.models import Q, Count
from django.core.exceptions import ValidationError
from cadastros.models import Logradouro
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse

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
    semana_query = request.GET.get('semana')
    ano_query = request.GET.get('ano')
    if semana_query and ano_query:
        try:
            semana_atual = int(semana_query)
            ano_atual = int(ano_query)
            # Preparar uma lista para armazenar as semanas e anos
            semanas_e_anos = []

            for i in range(4):
                if semana_atual - i > 0:
                    # Adiciona a semana e o ano corrente
                    semanas_e_anos.append((semana_atual - i, ano_atual))
                else:
                    # Determinar o último ano e a última semana
                    ano_anterior = ano_atual - 1
                    ultima_semana_ano_anterior = Semana.objects.filter(ano=ano_anterior).order_by('-semana').first().semana
                    semanas_e_anos.append((ultima_semana_ano_anterior - (i - semana_atual), ano_anterior))

            # Filtrar as notificações com base nas semanas e anos
            notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__semana__in=[s[0] for s in semanas_e_anos],
                semana_epidemiologica__ano__in=[s[1] for s in semanas_e_anos]
            ).values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()
    else:
        notificacoes = Notificacao.objects.all().values('logradouro_paciente__bairro__nome_bairro').annotate(quantidade=Count('id')).order_by('-quantidade')
    context = {
        'notificacoes': notificacoes,
        'termo_pesquisa': f'Semana {semana_query} do ano {ano_query}' if semana_query and ano_query else ''
    }
    return render(request, 'dengue/total_por_bairros.html', context)
    
def get_semanas_e_anos(semana, ano):
    if semana >= 4:
        # Se a semana for maior ou igual a 4, simplesmente pegue as últimas 4 semanas do mesmo ano
        semanas = [semana - i for i in range(4)]
        anos = [ano] * 4
    else:
        # Se a semana for menor que 4, precisamos buscar as semanas do ano anterior também
        semanas = [semana - i for i in range(semana)] + [52, 51, 50][:4 - semana]
        ano_anterior = ano - 1
        anos = [ano] * semana + [ano_anterior] * (4 - semana)

    return list(zip(semanas, anos))

def positivos_bairros(request):
    semana_query = request.GET.get('semana')
    ano_query = request.GET.get('ano')
    
    notificacoes = None
    total_geral = 0  # Inicializa o contador geral
    pesquisa_realizada = False
    if semana_query and ano_query:
        pesquisa_realizada = True
        try:
            semana = int(semana_query)
            ano = int(ano_query)
            semanas_e_anos = get_semanas_e_anos(semana, ano)
            
            # Construir o Q object para as semanas e anos
            semanas_filters = Q()
            for semana, ano in semanas_e_anos:
                semanas_filters |= Q(semana_epidemiologica__semana=semana, semana_epidemiologica__ano=ano)
            
            # Query base que será usada para ambas as contagens
            base_query = Notificacao.objects.filter(semanas_filters).filter(
                Q(classificacao__isnull=True, resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo']) |
                Q(classificacao__in=['Dengue', 'Dengue com Sinais de Alarme', 'Dengue Grave'])
            )
            
            # Contagem total de casos positivos
            total_geral = base_query.count()

            # Filtro final incluindo as semanas e anos, agrupado por bairro
            notificacoes = base_query.values('logradouro_paciente__bairro__nome_bairro') \
                                     .annotate(quantidade=Count('id')) \
                                     .order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()

    context = {
        'notificacoes': notificacoes,
        'total_geral': total_geral,  # Adiciona o total geral no contexto
        'termo_pesquisa': semana_query,
        'ano_pesquisa': ano_query,
        'pesquisa_realizada': pesquisa_realizada,
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
            return redirect(reverse('detalhes_notificacao', args=[pk])) # redireciona para a página de detalhes
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
    ).order_by('semana_epidemiologica')
    total_casos_positivos = sum(item['casos_positivos'] for item in resultado_agrupado)
    total_casos_negativos = sum(item['casos_negativos'] for item in resultado_agrupado)

    context = {
        'resultado_agrupado': resultado_agrupado,
        'termo_pesquisa': search_query,
        'total_casos_positivos': total_casos_positivos,
        'total_casos_negativos': total_casos_negativos,
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
    erro_msg = None  # Inicializando a variável aqui
    if request.method == "POST":
        data_inicial = request.POST.get("data_inicial")
        data_final = request.POST.get("data_final")
        
        if not data_inicial or not data_final:
            erro_msg = "Deve digitar ambas as datas"
            
        else:
            try:
                data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').date()
                data_final = datetime.strptime(data_final, '%d/%m/%Y').date()
                
                if data_inicial > data_final:
                    erro_msg = "A data inicial não pode ser superior a data final"

            except ValueError:
                erro_msg = "Digite as datas completas"

        # Filtra as notificações pela data
        queryset = Notificacao.objects.filter(data_notificacao__range=[data_inicial, data_final])

        total_notificacoes = queryset.count()
        
        if total_notificacoes == 0:
            erro_msg = "Não há resultados para o período"

        total_casos_positivos = queryset.filter(
            Q(classificacao__in=['Dengue', 'Dengue com Sinais de Alarme', 'Dengue Grave']) |
            Q(classificacao__isnull=True, resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo'])
        ).count()

        total_casos_negativos = queryset.filter(
            Q(classificacao__in=['Descartado', 'Chikungunya']) |
            Q(classificacao__isnull=True, resultado__in=['Negativo NS1', 'Negativo sorologia', 'Isolamento viral negativo'])
        ).count()

        casos_aberto = queryset.filter(
            Q(classificacao__isnull=True,resultado__in=['Aguardando agendamento', 'Aguardando coleta', 'Aguardando resultado', 'Faltou', 'Recusou', 'Inconclusivo', 'Não agendado'])
        ).count()

        total_faltas = queryset.filter(
            resultado__in=['Faltou', 'Recusou']
        ).count()


        total_obito_investigacao = queryset.filter(obito__range=[data_inicial, data_final], evolucao="Óbito em investigação").count()
        total_obito_agravo = queryset.filter(obito__range=[data_inicial, data_final], evolucao="Óbito pelo agravo").count()
        total_chikungunya = queryset.filter(obito__range=[data_inicial, data_final], classificacao="Chikungunya").count()
        total_chikungunya = queryset.filter(
            Q(classificacao__in=['Chikungunya'])
        ).count()
        total_internacao = queryset.filter(internacao__range=[data_inicial, data_final]).count()

        context = {
            'total_notificacoes': total_notificacoes,
            'total_casos_positivos': total_casos_positivos,
            'total_casos_negativos': total_casos_negativos,
            'casos_aberto': casos_aberto,
            'total_faltas': total_faltas,
            'total_obito_investigacao': total_obito_investigacao,
            'total_obito_agravo': total_obito_agravo,
            'total_internacao': total_internacao,
            'total_chikungunya': total_chikungunya,
            'data_inicial': data_inicial,  
            'data_final': data_final,  
            'erro_msg': erro_msg,
        }

        return render(request, 'dengue/boletim_resumo_totais.html', context)

    return render(request, 'dengue/boletim_resumo_totais.html')




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
    ).order_by('nome')
    return render(request, 'dengue/aguardando_ou_nao_agendado.html', {'notificacoes': notificacoes})

def casos_abertos(request):
    notificacoes = Notificacao.objects.filter(
        classificacao=None
    ).order_by('resultado', 'nome')  # Ordena primeiro por 'resultado' e depois por 'nome'
    
    # Contando o número total de notificações
    total_notificacoes = notificacoes.count()

    return render(request, 'dengue/casos_abertos.html', {
        'notificacoes': notificacoes,
        'total_notificacoes': total_notificacoes  # passando o total como um contexto adicional
    })

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
            return redirect('casos_abertos')  # Redireciona para a página de listagem após o encerramento
    else:
        form = EncerrarNotificacaoForm(instance=notificacao)
    return render(request, 'dengue/form_encerramento.html', {'form': form})


def notificacoes_recentes(request):
    erro_msg = None
    tabela_notificacoes = []
    total_notificacoes = 0  # Inicialize a variável aqui

    if request.method == 'GET' and 'semana' in request.GET and 'ano' in request.GET:
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')

        if semana and ano:
            semanas_pesquisa = [int(semana) - i for i in range(4) if int(semana) - i > 0]
            tabela_notificacoes = Notificacao.objects.filter(
                semana_epidemiologica__semana__in=semanas_pesquisa,
                semana_epidemiologica__ano=ano
            ).order_by('nome')
            total_notificacoes = tabela_notificacoes.count()
            if not tabela_notificacoes:
                erro_msg = "Nenhuma notificação encontrada no período"
        else:
            erro_msg = "Ambos os campos, semana e ano, são obrigatórios."

    return render(request, 'dengue/notificacoes_recentes.html', {
        'tabela_notificacoes': tabela_notificacoes,
        'total_notificacoes': total_notificacoes,
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
    contador = 0  # Adicionado para contar o número de registros
    semana_pesquisada = None  # Adicionado para guardar a semana pesquisada
    ano_pesquisado = None  # Adicionado para guardar o ano pesquisado

    formulario_enviado = 'semana' in request.GET or 'ano' in request.GET

    if request.method == 'GET':
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')

        # Guardar os valores para usar no template
        semana_pesquisada = semana
        ano_pesquisado = ano

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

        # Contar o número de registros se existirem
        if tabela_notificacoes:
            contador = tabela_notificacoes.count()

    return render(request, 'dengue/internados.html', {
        'tabela_notificacoes': tabela_notificacoes,
        'erro_msg': erro_msg,
        'formulario_enviado': formulario_enviado,
        'contador': contador,  # Adicionado para usar no template
        'semana_pesquisada': semana_pesquisada,  # Adicionado para usar no template
        'ano_pesquisado': ano_pesquisado  # Adicionado para usar no template
    })


def obitos(request):
    erro_msg = None
    tabela_notificacoes = None

    formulario_enviado = 'semana' in request.GET or 'ano' in request.GET  # Aqui é onde detectamos se o formulário foi enviado

    if request.method == 'GET':
        semana = request.GET.get('semana')
        ano = request.GET.get('ano')

        # Base para todas as queries
        base_query = Notificacao.objects.exclude(obito__isnull=True).order_by('nome')

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

    return render(request, 'dengue/obitos.html', {
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

def detalhes_notificacao(request, id_notificacao):
    notificacao = get_object_or_404(Notificacao, id=id_notificacao)
    return render(request, 'dengue/detalhes_notificacao.html', {'notificacao': notificacao})

def listar_notificacoes_data(request):
    if request.method == 'GET':
        data_inicial_str = request.GET.get('data_inicial')
        data_final_str = request.GET.get('data_final')

        # Verifique se ambos os campos de data foram fornecidos
        if data_inicial_str and data_final_str:
            try:
                data_inicial = datetime.strptime(data_inicial_str, '%d/%m/%Y').date()
                data_final = datetime.strptime(data_final_str, '%d/%m/%Y').date()

                notificacoes = Notificacao.objects.filter(
                    data_notificacao__range=(data_inicial, data_final)
                ).order_by('data_notificacao')
                total_notificacoes = notificacoes.count()

                context = {
                    'notificacoes': notificacoes,
                    'total_notificacoes': total_notificacoes,
                    'data_inicial': data_inicial,
                    'data_final': data_final
                }

                return render(request, 'dengue/listar_notificacoes_data.html', context)
            except ValueError:
                # Trate o erro de conversão de data aqui
                return HttpResponseRedirect('alguma_url_de_erro')
        else:
            # Redirecionar ou mostrar uma mensagem de erro se os campos de data não forem fornecidos
            return HttpResponseRedirect('alguma_url_de_erro')

    return render(request, 'dengue/listar_notificacoes_data.html')