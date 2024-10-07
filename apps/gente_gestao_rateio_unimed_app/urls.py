from django.urls import path

from apps.gente_gestao_rateio_unimed_app import views

urlpatterns = [
    path('rateio_unimed', views.Form_Importa_Plan_Despesas_View.as_view(), name='rateio_unimed'),
    path('preenche_colab', views.Preenche_Colaborador.as_view(), name='preenche_colab'),
    path('busca_despesas', views.Busca_Despesas.as_view(), name='busca_despesas'),
    path('calcula_rateio', views.Calcula_Rateio.as_view(), name='calcula_rateio'),
    path('filiais_despesa', views.Form_Filial_Despesas.as_view(), name='filiais_despesa'),
    path('obter_filiais', views.Obter_Filiais.as_view(), name='obter_filiais'),
    path('historico_importacoes', views.Historico_Importacoes.as_view(), name='historico_importacoes'),
    path('projetos_filial', views.Projeto_Filial.as_view(), name='projetos_filial'),
    path('colaboradores_excecao', views.Colaborador_Excecao_View.as_view(), name='colaboradores_excecao'),
]