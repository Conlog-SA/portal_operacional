from django.urls import path

from apps.gente_gestao_rateio_unimed_app import views

urlpatterns = [
    path('rateio_unimed', views.Form_Importa_Plan_Despesas_View.as_view(), name='rateio_unimed'),
    path('preenche_colab', views.Preenche_Colaborador.as_view(), name='preenche_colab'),

]