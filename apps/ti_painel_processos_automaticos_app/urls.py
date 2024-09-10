from apps.ti_painel_processos_automaticos_app import views
from django.urls import path

urlpatterns = [
    path('', views.Frm_Painel_Processos_Automaticos_View.as_view(), name='acesso_frm_painel_processos_automaticos'),

]

