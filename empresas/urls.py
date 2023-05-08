from django.urls import path
from . import views

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
    path('empresas/', views.listar_empresas, name='listar_empresas'),
    path('empresas/novo/', views.criar_empresa, name='criar_empresa'),
    path('empresas/editar/<int:id>/', views.editar_empresa, name='editar_empresa'),
    path('empresas/excluir/<int:id>/', views.excluir_empresa, name='excluir_empresa'),


    path('risco/listar/', views.listar_risco, name='listar_risco'),
    path('risco/cadastrar/', views.cadastrar_risco, name='cadastrar_risco'),
    path('risco/editar/<int:id>/', views.editar_risco, name='editar_risco'),
    path('risco/excluir/<int:id>/', views.excluir_risco, name='excluir_risco'),
]
