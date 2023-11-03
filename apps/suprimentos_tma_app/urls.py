from django.urls import path
from . import views

urlpatterns = [
    path('', views.Form_Requisicao_Gera_Tma_View.as_view(), name='carrega_form_requisicoes_gera_tma'),
    path('retorna_requisicoes_atendidas_benner', views.Requisicao_Atendida_View.as_view(),
         name='Requisicao_Atendida_View'),
    path('vincula_comprador_req_atendida_tma', views.Requisicao_Atendida_View.as_view(),
        name='vincula_comprador_req_atendida_tma')
]