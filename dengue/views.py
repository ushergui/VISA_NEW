from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notificacao, Semana
from .forms import NotificacaoForm, SemanaForm, EncerrarNotificacaoForm
from django.db.models import Q, Count, Max
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
            notificacoes = Notificacao.objects.filter(nome=nome, logradouro_paciente_id=logradouro)\
                                              .exclude(pk=notificacao_id)\
                                              .select_related('logradouro_paciente__bairro__cidade__estado')
        else:
            notificacoes = Notificacao.objects.filter(nome=nome, logradouro_paciente_id=logradouro)\
                                              .select_related('logradouro_paciente__bairro__cidade__estado')

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
            notificacoes = Notificacao.objects.select_related('semana_epidemiologica', 'logradouro_paciente').filter(
                semana_epidemiologica__in=ultimas_4_semanas,
                resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo']
            )
        except ValueError:
            notificacoes = Notificacao.objects.select_related('semana_epidemiologica', 'logradouro_paciente').all()
    else:
        notificacoes = Notificacao.objects.select_related('semana_epidemiologica', 'logradouro_paciente').all()

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
                semana_epidemiologica__semana__in=ultimas_4_semanas)\
                .select_related('semana_epidemiologica', 
                                'logradouro_paciente',
                                'logradouro_paciente__bairro',
                                'logradouro_paciente__bairro__cidade',
                                'logradouro_paciente__bairro__cidade__estado')
        except ValueError:
            notificacoes = Notificacao.objects.all()\
                .select_related('semana_epidemiologica', 
                                'logradouro_paciente',
                                'logradouro_paciente__bairro',
                                'logradouro_paciente__bairro__cidade',
                                'logradouro_paciente__bairro__cidade__estado')
    else:
        notificacoes = Notificacao.objects.all()\
            .select_related('semana_epidemiologica', 
                            'logradouro_paciente',
                            'logradouro_paciente__bairro',
                            'logradouro_paciente__bairro__cidade',
                            'logradouro_paciente__bairro__cidade__estado')

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

            # Utilizando a função para obter as semanas e anos
            semanas_e_anos = get_semanas_e_anos(semana_atual, ano_atual)

            # Criando um query complexa com Q objects
            query = Q()
            for semana, ano in semanas_e_anos:
                query |= Q(semana_epidemiologica__semana=semana, semana_epidemiologica__ano=ano)

            # Filtrar as notificações com base na query
            notificacoes = Notificacao.objects.filter(query)\
                                              .select_related('logradouro_paciente__bairro__cidade__estado', 'semana_epidemiologica')\
                                              .values('logradouro_paciente__bairro__nome_bairro')\
                                              .annotate(quantidade=Count('id'))\
                                              .order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()
    else:
        notificacoes = Notificacao.objects.all()\
                                      .select_related('logradouro_paciente__bairro__cidade__estado', 'semana_epidemiologica')\
                                      .values('logradouro_paciente__bairro__nome_bairro')\
                                      .annotate(quantidade=Count('id'))\
                                      .order_by('-quantidade')

    total_notificacoes = sum([notificacao['quantidade'] for notificacao in notificacoes])
    context = {
        'total_notificacoes': total_notificacoes,
        'notificacoes': notificacoes,
        'termo_pesquisa': f'Semana {semana_query} do ano {ano_query}' if semana_query and ano_query else ''
    }
    return render(request, 'dengue/total_por_bairros.html', context)

    
def total_usf(request):
    semana_query = request.GET.get('semana')
    ano_query = request.GET.get('ano')
    if semana_query and ano_query:
        try:
            semana_atual = int(semana_query)
            ano_atual = int(ano_query)

            # Utilizando a função para obter as semanas e anos
            semanas_e_anos = get_semanas_e_anos(semana_atual, ano_atual)

            # Criando um query complexa com Q objects
            query = Q()
            for semana, ano in semanas_e_anos:
                query |= Q(semana_epidemiologica__semana=semana, semana_epidemiologica__ano=ano)

            # Filtrar as notificações com base na query
            notificacoes = Notificacao.objects.filter(query).values('usf').annotate(quantidade=Count('id')).order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()
    else:
        notificacoes = Notificacao.objects.all().values('usf').annotate(quantidade=Count('id')).order_by('-quantidade')
    total_notificacoes = sum([notificacao['quantidade'] for notificacao in notificacoes])
    context = {
        'total_notificacoes': total_notificacoes,
        'notificacoes': notificacoes,
        'termo_pesquisa': f'Semana {semana_query} do ano {ano_query}' if semana_query and ano_query else ''
    }
    return render(request, 'dengue/total_por_usf.html', context)

def total_por_notificadora(request):
    semana_query = request.GET.get('semana')
    ano_query = request.GET.get('ano')

    if semana_query and ano_query:
        try:
            semana_atual = int(semana_query)
            ano_atual = int(ano_query)
            semanas_e_anos = get_semanas_e_anos(semana_atual, ano_atual)

            query = Q()
            for semana, ano in semanas_e_anos:
                query |= Q(semana_epidemiologica__semana=semana, semana_epidemiologica__ano=ano)

            notificacoes = Notificacao.objects.filter(query)\
                                              .select_related('semana_epidemiologica')\
                                              .values('notificadora')\
                                              .annotate(quantidade=Count('id'))\
                                              .order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()
    elif ano_query and not semana_query:
        ano_atual = int(ano_query)
        notificacoes = Notificacao.objects.filter(semana_epidemiologica__ano=ano_atual)\
                                          .select_related('semana_epidemiologica')\
                                          .values('notificadora')\
                                          .annotate(quantidade=Count('id'))\
                                          .order_by('-quantidade')
    elif semana_query and not ano_query:
        notificacoes = Notificacao.objects.none()
    else:
        notificacoes = Notificacao.objects.all()\
                                      .select_related('semana_epidemiologica')\
                                      .values('notificadora')\
                                      .annotate(quantidade=Count('id'))\
                                      .order_by('-quantidade')

    total_notificacoes = sum([notificacao['quantidade'] for notificacao in notificacoes])
    context = {
        'total_notificacoes': total_notificacoes,
        'notificacoes': notificacoes,
        'termo_pesquisa': f'Semana {semana_query} do ano {ano_query} e 3 anteriores' if semana_query and ano_query else (f'Registros do ano {ano_query}' if ano_query and not semana_query else 'Todos os registros')
    }
    return render(request, 'dengue/total_por_notificadora.html', context)
    
def get_semanas_e_anos(semana, ano):
    semanas_e_anos = []
    for i in range(4):
        semana_atual = semana - i
        ano_atual = ano

        # Se a semana retroceder antes do início do ano atual
        if semana_atual <= 0:
            ano_atual -= 1
            # Obter o total de semanas no ano anterior
            total_semanas_ano_anterior = Semana.objects.filter(ano=ano_atual).aggregate(Max('semana'))['semana__max']
            semana_atual = total_semanas_ano_anterior + semana_atual

        semanas_e_anos.append((semana_atual, ano_atual))

    return semanas_e_anos

def positivos_bairros(request):
    semana_query = request.GET.get('semana')
    ano_query = request.GET.get('ano')

    notificacoes = None
    total_geral = 0
    pesquisa_realizada = False
    if semana_query and ano_query:
        pesquisa_realizada = True
        try:
            semana_atual = int(semana_query)
            ano_atual = int(ano_query)
            semanas_e_anos = get_semanas_e_anos(semana_atual, ano_atual)

            semanas_filters = Q()
            for semana, ano in semanas_e_anos:
                semanas_filters |= Q(semana_epidemiologica__semana=semana, semana_epidemiologica__ano=ano)

            base_query = Notificacao.objects.filter(semanas_filters)\
                                            .select_related('logradouro_paciente__bairro__cidade__estado')\
                                            .filter(
                                                Q(classificacao__isnull=True, resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo']) |
                                                Q(classificacao__in=['Dengue', 'Dengue com Sinais de Alarme', 'Dengue Grave'])
                                            )

            total_geral = base_query.count()

            notificacoes = base_query.values('logradouro_paciente__bairro__nome_bairro')\
                                     .annotate(quantidade=Count('id'))\
                                     .order_by('-quantidade')
        except ValueError:
            notificacoes = Notificacao.objects.none()

    context = {
        'notificacoes': notificacoes,
        'total_geral': total_geral,
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
    notificacoes = Notificacao.objects.all()

    # Já temos a lógica para casos positivos, vamos manter e adicionar a lógica para casos negativos
    resultado_agrupado = notificacoes.values(
        'semana_epidemiologica__ano', 
        'semana_epidemiologica__semana'
    ).annotate(
        casos_positivos=Count(
            'pk', 
            filter=Q(classificacao__in=['Dengue', 'Dengue com Sinais de Alarme', 'Dengue Grave']) |
            Q(classificacao__isnull=True, resultado__in=['Positivo NS1', 'Positivo sorologia', 'Isolamento viral positivo'])
        ),
        casos_negativos=Count(
            'pk',
            filter=Q(classificacao__in=['Descartado', 'Chikungunya']) |
            Q(classificacao__isnull=True, resultado__in=['Negativo NS1', 'Negativo sorologia', 'Isolamento viral negativo'])
        ),
        total_notificacoes=Count('pk')
    ).order_by('semana_epidemiologica__ano', 'semana_epidemiologica__semana')

    dados_por_ano = {
        'positivos': {},
        'negativos': {},
        'total': {} 
    }
    for item in resultado_agrupado:
        ano = item['semana_epidemiologica__ano']
        semana = item['semana_epidemiologica__semana']
        casos_pos = item['casos_positivos']
        casos_neg = item['casos_negativos']
        total = item['total_notificacoes']  # Novo total

        if ano not in dados_por_ano['positivos']:
            dados_por_ano['positivos'][ano] = {}
            dados_por_ano['negativos'][ano] = {}
            dados_por_ano['total'][ano] = {}  # Inicialização para totais

        dados_por_ano['positivos'][ano][semana] = casos_pos
        dados_por_ano['negativos'][ano][semana] = casos_neg
        dados_por_ano['total'][ano][semana] = total 

    context = {
        'dados_por_ano': dados_por_ano,
    }
    return render(request, 'dengue/boletim_resumo.html', context)

def semana_epidemiologica(request):
    notificacoes = None
    termo_pesquisa = request.GET.get('semana')
    ano_pesquisa = request.GET.get('ano')
    
    if termo_pesquisa and ano_pesquisa:
        try:
            semana_atual = int(termo_pesquisa)
            ano_atual = int(ano_pesquisa)

            semanas_e_anos = get_semanas_e_anos(semana_atual, ano_atual)

                # Criando um query complexa com Q objects
            query = Q()
            for semana, ano in semanas_e_anos:
                query |= Q(semana_epidemiologica__semana=semana, semana_epidemiologica__ano=ano)

                # Filtrar as notificações com base na query
            notificacoes = Notificacao.objects.filter(query).values(
                    'semana_epidemiologica__semana', 
                    'semana_epidemiologica__ano', 
                    'semana_epidemiologica__data_inicio_semana',
                    'semana_epidemiologica__data_fim_semana'
            ).annotate(quantidade=Count('semana_epidemiologica')).order_by('semana_epidemiologica')
                
        except ValueError:
            notificacoes = None

        # Se não houver parâmetros de pesquisa, retorna todas as notificações por semana epidemiológica
    return render(request, 'dengue/semana_epidemiologica.html', {
        'notificacoes': notificacoes,
        'termo_pesquisa': termo_pesquisa,
        'ano_pesquisa': ano_pesquisa
    })

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

def sem_usf(request):
    notificacoes = Notificacao.objects.filter(
        usf=None
    ).order_by('nome') 
    
    # Contando o número total de notificações
    total_notificacoes = notificacoes.count()

    return render(request, 'dengue/sem_usf.html', {
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

        if data_inicial_str and data_final_str:
            try:
                data_inicial = datetime.strptime(data_inicial_str, '%d/%m/%Y').date()
                data_final = datetime.strptime(data_final_str, '%d/%m/%Y').date()

                notificacoes = Notificacao.objects.filter(
                    data_notificacao__range=(data_inicial, data_final)
                ).select_related('semana_epidemiologica', 'logradouro_paciente').order_by('data_notificacao')

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
