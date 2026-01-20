from django.urls import path
from . import views

urlpatterns = [
    path('', views.Frm_Acesso_Despesa_View.as_view(), name='abre_frm_despesas'),
    path('frm_consulta_despesas', views.Frm_Despesa_View.as_view(), name='frm_consulta_despesas'),
    path('frm_salva_lancamento_despesa', views.Frm_Despesa_View.as_view(), name='frm_salva_lancamento_despesa'),
    path('frm_deleta_lancamento_despesa/<str:pk>', views.Frm_Despesa_View.as_view(), name='frm_deleta_lancamento_despesa'),
]
