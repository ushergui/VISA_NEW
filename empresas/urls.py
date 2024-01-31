from django.urls import path
from . import views
from .views import GetRisco, listar_protocolos, novo_protocolo, editar_protocolo, excluir_protocolo, get_pontos, EmpresasView, listar_risco_um, listar_risco_um_pdf, listar_risco_dois, listar_risco_dois_pdf, listar_risco_tres, listar_risco_tres_pdf
from .views import listar_nao_planejadas, ListarPlanejamentoIndividualView, lista_correcao_cnae

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
    path('empresas/editar_observacoes/<int:id>/', views.editar_observacoes, name='editar_observacoes'),
    path('empresas/editar_inscricao_estadual/<int:id>/', views.editar_inscricao_estadual, name='editar_inscricao_estadual'),
    path('empresas/excluir/<int:id>/', views.excluir_empresa, name='excluir_empresa'),
    path('empresa/<int:empresa_id>/', views.detalhe_empresa, name='detalhe_empresa'),

    path('create_produtividade/<int:inspecao_id>/', views.CreateProdutividade, name='create_produtividade'),
    

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


    path('inspecao/', views.listar_inspecao, name='listar_inspecao'),
    path('inspecao/novo/<int:protocolo_id>/', views.cadastrar_inspecao, name='cadastrar_inspecao'),
    path('inspecao/editar/<int:id>', views.alterar_inspecao, name='alterar_inspecao'),
    path('inspecao/excluir/<int:id>', views.excluir_inspecao, name='excluir_inspecao'),

    path('acao-produtividade/', views.listar_acao_produtividade, name='listar_acao_produtividade'),
    path('acao-produtividade/novo', views.criar_acao_produtividade, name='criar_acao_produtividade'),
    path('acao-produtividade/excluir/<int:id>/', views.excluir_acao_produtividade, name='excluir_acao_produtividade'),
    path('acao-produtividade/editar/<int:id>/', views.editar_acao_produtividade, name='editar_acao_produtividade'),
    path('produtividade/', views.listar_produtividade, name='listar_produtividade'),


    path('get_pontos/', get_pontos, name='get_pontos'),
    path('lista_empresas_cnae/', views.EmpresasCnaeListView.as_view(), name='lista_empresas_cnae'),
    path('lista_empresas_endereco/', views.EmpresasEnderecoListView.as_view(), name='lista_empresas_endereco'),
    path('editar_empresa_cnae/<int:id>/', views.editar_empresa_cnae, name='editar_empresa_cnae'),
    path('empresas-cnae-pdf/', views.empresas_cnae_pdf, name='empresas_cnae_pdf'),
    path('empresas-endereco-pdf/', views.empresas_endereco_pdf, name='empresas_endereco_pdf'),

    path('empresas/', EmpresasView.as_view(), name='empresas'),
    path('listar_risco_um/', listar_risco_um, name='listar_risco_um'),
    path('listar_risco_um_pdf/', listar_risco_um_pdf, name='listar_risco_um_pdf'),
    path('listar_risco_dois/', listar_risco_dois, name='listar_risco_dois'),
    path('listar_risco_dois_pdf/', listar_risco_dois_pdf, name='listar_risco_dois_pdf'),
    path('listar_risco_tres/', listar_risco_tres, name='listar_risco_tres'),
    path('listar_risco_tres_pdf/', listar_risco_tres_pdf, name='listar_risco_tres_pdf'),
    path('listar_vigiriscos_2023/', views.listar_vigiriscos_2023, name='listar_vigiriscos_2023'),
    path('listar_vigiriscos_2023_pdf/', views.listar_vigiriscos_2023_pdf, name='listar_vigiriscos_2023_pdf'),

    path('fechamento/', views.fechamento, name='fechamento'),
    path('painel/', views.painel, name='painel'),
    path('listar-planejamento-individual/', ListarPlanejamentoIndividualView.as_view(), name='listar_planejamento_individual'),
    path('empresas/<int:empresa_id>/alvara', views.gerar_alvara, name='gerar_alvara'),


    path('planejamentos/', views.listar_planejamentos, name='listar_planejamentos'),
    path('planejamento/criar/', views.criar_planejamento, name='criar_planejamento'),
    path('planejamento/editar/<int:pk>/', views.editar_planejamento, name='editar_planejamento'),
    path('planejamento/excluir/<int:pk>/', views.excluir_planejamento, name='excluir_planejamento'),
    path('empresas/listar_empresas_inscricao', views.listar_empresas_inscricao, name='listar_empresas_inscricao'),
    path('empresas/nao-planejadas/', listar_nao_planejadas, name='listar_nao_planejadas'),
    path('lista_correcao_cnae/', lista_correcao_cnae, name='lista_correcao_cnae'),

]
