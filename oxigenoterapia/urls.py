from django.urls import path
from .views import PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView, FisioterapeutaListView, FisioterapeutaCreateView, FisioterapeutaUpdateView, FisioterapeutaDeleteView, EquipamentoCreateView, EquipamentoUpdateView
from .views import EquipamentoDeleteView, EquipamentoListView, DescartavelCreateView, DescartavelUpdateView, DescartavelDeleteView, DescartavelListView, CidCreateView, CidDeleteView, CidListView, CidUpdateView, PrescricaoCreateView
from .views import PrescricaoUpdateView, PrescricaoListView, PrescricaoDeleteView, AtendimentoUpdateView, AtendimentoListView, UsfCreateView, UsfListView, UsfDeleteView, UsfUpdateView, AtendimentoCreateView, AtendimentoDeleteView
from .views import ModoDeUsoCreateView, ModoDeUsoListView, ModoDeUsoUpdateView, ModoDeUsoDeleteView, FinalidadeCreateView, FinalidadeListView, FinalidadeUpdateView, FinalidadeDeleteView
from . import views
from .views import relatorio_pacientes_ativos_oxigenoterapia, relatorio_pacientes_ativos_ventilacao, relatorio_para_visita, relatorio_para_visita_pdf, aparelhos_alugados, aparelhos_alugados_pdf

urlpatterns = [
    path('pacientes', PacienteListView.as_view(), name='paciente_list'),
    path('cadastrar_paciente/', PacienteCreateView.as_view(), name='paciente_new'),
    path('editar_paciente/<int:pk>', PacienteUpdateView.as_view(), name='paciente_edit'),
    path('excluir_paciente/<int:pk>', PacienteDeleteView.as_view(), name='paciente_delete'),
    
    path('fisioterapeutas/', FisioterapeutaListView.as_view(), name='fisioterapeuta_list'),
    path('fisioterapeuta/new/', FisioterapeutaCreateView.as_view(), name='fisioterapeuta_new'),
    path('fisioterapeuta/edit/<int:pk>/', FisioterapeutaUpdateView.as_view(), name='fisioterapeuta_edit'),
    path('fisioterapeuta/delete/<int:pk>/', FisioterapeutaDeleteView.as_view(), name='fisioterapeuta_delete'),

    path('equipamentos', EquipamentoListView.as_view(), name='equipamento_list'),
    path('equipamento/new/', EquipamentoCreateView.as_view(), name='equipamento_new'),
    path('equipamento/edit/<int:pk>', EquipamentoUpdateView.as_view(), name='equipamento_edit'),
    path('equipamento/delete/<int:pk>', EquipamentoDeleteView.as_view(), name='equipamento_delete'),

    path('descartaveis', DescartavelListView.as_view(), name='descartavel_list'),
    path('descartavel/new/', DescartavelCreateView.as_view(), name='descartavel_new'),
    path('descartavel/edit/<int:pk>', DescartavelUpdateView.as_view(), name='descartavel_edit'),
    path('descartavel/delete/<int:pk>', DescartavelDeleteView.as_view(), name='descartavel_delete'),

    path('finalidade', FinalidadeListView.as_view(), name='finalidade_list'),
    path('finalidade/new/', FinalidadeCreateView.as_view(), name='finalidade_new'),
    path('finalidade/edit/<int:pk>', FinalidadeUpdateView.as_view(), name='finalidade_edit'),
    path('finalidade/delete/<int:pk>', FinalidadeDeleteView.as_view(), name='finalidade_delete'),

    path('cid', CidListView.as_view(), name='cid_list'),
    path('cid/new/', CidCreateView.as_view(), name='cid_new'),
    path('cid/edit/<int:pk>', CidUpdateView.as_view(), name='cid_edit'),
    path('cid/delete/<int:pk>', CidDeleteView.as_view(), name='cid_delete'),

    path('prescricoes', PrescricaoListView.as_view(), name='prescricoes_list'),
    path('prescricao/new/', PrescricaoCreateView.as_view(), name='prescricao_new'),
    path('prescricao/edit/<int:pk>/', PrescricaoUpdateView.as_view(), name='prescricao_edit'),
    path('prescricao/delete/<int:pk>/', PrescricaoDeleteView.as_view(), name='prescricao_delete'),

    path('mododeuso', ModoDeUsoListView.as_view(), name='mododeuso_list'),
    path('mododeuso/new/', ModoDeUsoCreateView.as_view(), name='mododeuso_new'),
    path('mododeuso/edit/<int:pk>/', ModoDeUsoUpdateView.as_view(), name='mododeuso_edit'),
    path('mododeuso/delete/<int:pk>/', ModoDeUsoDeleteView.as_view(), name='mododeuso_delete'),

    path('atendimento/edit/<int:pk>/', AtendimentoUpdateView.as_view(), name='atendimento_edit'),
    path('atendimento/new/<int:prescricao_id>/', AtendimentoCreateView.as_view(), name='atendimento_new'),
    path('atendimento/delete/<int:pk>/', AtendimentoDeleteView.as_view(), name='atendimento_delete'),
    path('atendimentos', AtendimentoListView.as_view(), name='atendimento_list'),

    path('usfs', UsfListView.as_view(), name='usf_list'),
    path('usf/new/', UsfCreateView.as_view(), name='usf_new'),
    path('usf/edit/<int:pk>', UsfUpdateView.as_view(), name='usf_edit'),
    path('usf/delete/<int:pk>', UsfDeleteView.as_view(), name='usf_delete'),


    path('consulta_atendimentos/', views.consulta_atendimentos, name='consulta_atendimentos'),
    path('consulta_atendimentos_pdf/', views.consulta_atendimentos_pdf, name='consulta_atendimentos_pdf'),
    path('relatorio_pacientes_ativos_oxigenoterapia/', relatorio_pacientes_ativos_oxigenoterapia, name='relatorio_pacientes_ativos_oxigenoterapia'),
    path('relatorio_pacientes_ativos_oxigenoterapia/pdf/', views.relatorio_pacientes_ativos_oxigenoterapia_pdf, name='relatorio_pacientes_ativos_oxigenoterapia_pdf'),
    path('relatorio_pacientes_ativos_ventilacao/', relatorio_pacientes_ativos_ventilacao, name='relatorio_pacientes_ativos_ventilacao'),
    path('relatorio_pacientes_ativos_ventilacao/pdf/', views.relatorio_pacientes_ativos_ventilacao_pdf, name='relatorio_pacientes_ativos_ventilacao_pdf'),
    path('relatorio_para_visita/', relatorio_para_visita, name='relatorio_para_visita'),
    path('relatorio_para_visita_pdf/', relatorio_para_visita_pdf, name='relatorio_para_visita_pdf'),
    path('aparelhos_alugados/', aparelhos_alugados, name='aparelhos_alugados'),
    path('aparelhos_alugados_pdf/', aparelhos_alugados_pdf, name='aparelhos_alugados_pdf'),
    path('relatorio_troca_de_filtro/', views.relatorio_troca_de_filtro, name='relatorio_troca_de_filtro'),

]