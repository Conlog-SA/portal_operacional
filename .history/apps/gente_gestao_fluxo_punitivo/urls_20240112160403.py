from django.urls import path

from apps.gente_gestao_fluxo_punitivo import views

urlpatterns = [
    path('fluxo_punitivo', views.Form_Fluxo_Punitivo.as_view(), name='fluxo_punitivo'),
    path('listar_colaboradores', views.Listar_Colaboradores.as_view(), name='listar_colaboradores'),
    path('cria_motivo', views.Criacao_Motivos.as_view(), name='cria_motivo'),
    path('tabela_fluxos', views.Tabelaa_Fluxos.as_view(), name='tabela_fluxo'),
    path('cancela_punicao', views.Cancela_Punicao.as_view(), name='cancela_punicao')
]