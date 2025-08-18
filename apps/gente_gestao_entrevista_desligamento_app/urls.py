from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.Entrevista_Desligamento_Gerencial.as_view(),name='entrevista_desligamento_gerencial'),
    #path('frm_entrevista_desligamentos', views.Registra_Desligamentos.as_view(),name='frm_entrevista_desligamentos'),
    path('pesquisa_desligamentos', views.Frm_Busca_Desligamentos_Periodo.as_view(),name='pesquisa_desligamentos'),
    path('relatorio_entrevista', views.Frm_Consulta_Entrevista_Desligamento.as_view(),name='relatorio_entrevista'),
    path('gerar_link_entrevista', views.Frm_Gerar_Link_Entrevista_Desligamento.as_view(), name='gerar_link_entrevista'),
    path('frm_entrevista_desligamento', csrf_exempt(views.Registra_Desligamentos.as_view()), name='frm_entrevista_desligamento'),
]