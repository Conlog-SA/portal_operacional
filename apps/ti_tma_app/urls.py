from django.urls import path
from . import views

urlpatterns = [
    path('', views.Form_Gera_Tma_TI_View.as_view(), name='acessa_frm_gera_tma_ti'),
    path('gera_tma_chamados_ti', views.Form_Gera_Tma_TI_View.as_view(), name='gera_tma_chamados_ti'),

]