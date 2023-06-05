from django.urls import path
from . import views

urlpatterns = [
    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),
    path('notificacoes_gerais/', views.listar_notificacoes_gerais, name='listar_notificacoes_gerais'),
    path('total_bairros/', views.total_bairros, name='total_bairros'),
    path('total_bairros_positivos/', views.total_bairros_positivos, name='total_bairros_positivos'),
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
    path('pesquisar_notificacoes/', views.pesquisar_notificacoes, name='pesquisar_notificacoes'),
]
