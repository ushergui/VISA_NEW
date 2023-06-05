from django.urls import path
from . import views
from .views import GetRisco, listar_protocolos, novo_protocolo, editar_protocolo, excluir_protocolo


urlpatterns = [
    # Contabilidade
    path('contabilidades/', views.listar_contabilidades, name='listar_contabilidades'),
    path('contabilidades/novo/', views.criar_contabilidade, name='criar_contabilidade'),
    path('contabilidades/editar/<int:id>/', views.editar_contabilidade, name='editar_contabilidade'),
    path('contabilidades/excluir/<int:id>/', views.excluir_contabilidade, name='excluir_contabilidade'),

    # Cnae
    path('cnaes/', views.listar_cnaes, name='listar_cnaes'),
    path('cnaes/novo/', views.criar_cnae, name='criar_cnae'),
    path('cnaes/editar/<int:id>/', views.editar_cnae, name='editar_cnae'),
    path('cnaes/excluir/<int:id>/', views.excluir_cnae, name='excluir_cnae'),

    # Empresas
    path('empresas/listar', views.listar_empresas, name='listar_empresas'),
    path('empresas/novo/', views.criar_empresa, name='criar_empresa'),
    path('empresas/editar/<int:id>/', views.editar_empresa, name='editar_empresa'),
    path('empresas/excluir/<int:id>/', views.excluir_empresa, name='excluir_empresa'),
    path('empresa/<int:empresa_id>/', views.detalhe_empresa, name='detalhe_empresa'),


    path('risco/listar/', views.listar_risco, name='listar_risco'),
    path('risco/cadastrar/', views.cadastrar_risco, name='cadastrar_risco'),
    path('risco/editar/<int:id>/', views.editar_risco, name='editar_risco'),
    path('risco/excluir/<int:id>/', views.excluir_risco, name='excluir_risco'),

    path('api/get_risco/', GetRisco.as_view(), name='get_risco'),

    path('legislacao/', views.listar_legislacao, name='listar_legislacao'),
    path('legislacao/criar/', views.criar_legislacao, name='criar_legislacao'),
    path('legislacao/editar/<int:id>/', views.editar_legislacao, name='editar_legislacao'),
    path('legislacao/excluir/<int:id>/', views.excluir_legislacao, name='excluir_legislacao'),

    path('protocolos/', listar_protocolos, name='listar_protocolos'),
    path('protocolo/novo', novo_protocolo, name='novo_protocolo'),
    path('protocolo/editar/<int:id>', editar_protocolo, name='editar_protocolo'),
    path('protocolo/excluir/<int:id>', excluir_protocolo, name='excluir_protocolo'),


]
