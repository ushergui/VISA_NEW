from django.urls import path
from . import views

urlpatterns = [
    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),
    path('notificacoes_gerais/', views.listar_notificacoes_gerais, name='listar_notificacoes_gerais'),
    path('notificacoes_recentes/', views.notificacoes_recentes, name='notificacoes_recentes'),
    path('chikungunya/', views.chikungunya, name='chikungunya'),
    path('internados/', views.internados, name='internados'),
    path('obitos/', views.obitos, name='obitos'),
    path('positivos_recentes/', views.positivos_recentes, name='positivos_recentes'),
    path('total_bairros/', views.total_bairros, name='total_bairros'),
    path('total_usf/', views.total_usf, name='total_usf'),
    path('positivos_bairros/', views.positivos_bairros, name='positivos_bairros'),
    path('notificacoes/criar/', views.criar_notificacao, name='criar_notificacao'),
    path('notificacoes/editar/<int:pk>/', views.editar_notificacao, name='editar_notificacao'),
    path('notificacoes/deletar/<int:pk>/', views.deletar_notificacao, name='deletar_notificacao'),
    path('boletim_resumo/', views.boletim_resumo, name='boletim_resumo'),
    path('boletim_resumo_totais/', views.boletim_resumo_totais, name='boletim_resumo_totais'),
    path('semana_epidemiologica/', views.semana_epidemiologica, name='semana_epidemiologica'),
    path('check_duplicate/', views.check_duplicate, name='check_duplicate'),
    path('listar_semanas/', views.listar_semanas, name='listar_semanas'),
    path('form_semana/', views.form_semana, name='form_semana'),
    path('form_semana/<int:semana_id>/', views.form_semana, name='editar_semana'),
    path('excluir_semana/<int:semana_id>/', views.excluir_semana, name='excluir_semana'),
    path('api/semanas/', views.api_semanas, name='api_semanas'),
    path('motorista/', views.motorista, name='motorista'),
    path('agendados/', views.agendados, name='agendados'),
    path('aguardando_resultados/', views.aguardando_resultados, name='aguardando_resultados'),
    path('aguardando_ou_nao_agendado/', views.aguardando_ou_nao_agendado, name='aguardando_ou_nao_agendado'),
    path('casos_abertos/', views.casos_abertos, name='casos_abertos'),
    path('pesquisar_notificacoes/', views.pesquisar_notificacoes, name='pesquisar_notificacoes'),
    path('listar_casos_abertos/', views.listar_casos_abertos, name='listar_casos_abertos'),
    path('encerrar_notificacao/<int:pk>/', views.encerrar_notificacao, name='encerrar_notificacao'),
    path('notificacao/<int:id_notificacao>/', views.detalhes_notificacao, name='detalhes_notificacao'),
    path('listar_notificacoes_data', views.listar_notificacoes_data, name='listar_notificacoes_data'),
]
