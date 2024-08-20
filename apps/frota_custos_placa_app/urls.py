from django.urls import path

from apps.frota_custos_placa_app import views

urlpatterns = [
    path('', views.Frm_Custos_Placa_View.as_view(),
             name='acessa_frm_custos_placa'),
    path('gera_dados_razao_placas_proj', views.Frm_Custos_Placa_Proj_View.as_view(),
             name='gera_dados_razao_placas_proj'),

]