from django.urls import path
from apps.ti_gera_consultas_app import views

urlpatterns = [
    path('', views.Frm_Criar_Consulta_View.as_view(), name='frm_criar_consulta'),
    path('gera_nova_consulta', views.Frm_Criar_Consulta_View.as_view(), name='gera_nova_consulta'),
    path('salva_param', views.Frm_Parametro_View.as_view(), name='salva_param'),
    path('vincula_usuario_consulta', views.Frm_Acesso_Consulta_View.as_view(), name='vincula_usuario_consulta'),
    path('acessa_consulta', views.Frm_Acesso_Consulta_View.as_view(), name='acessa_consulta'),
    path('frm_consultas_disponiveis', views.Frm_Consulta_Disponivel_View.as_view(), name='frm_consultas_disponiveis'),
    path('abre_modal_com_param_script', views.Frm_Param_Consulta_View.as_view(), name='abre_modal_com_param_script'),
    path('executa_consulta', views.Frm_Executa_Consulta_View.as_view(), name='executa_consulta'),
    path('exclui_parametro_consulta/<int:pk>/', views.Frm_Parametro_View.as_view(),name='exclui_parametro_consulta'),
]
