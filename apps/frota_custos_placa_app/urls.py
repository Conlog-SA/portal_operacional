from django.urls import path

from apps.frota_custos_placa_app import views

urlpatterns = [
    path('', views.Frm_Custos_Placa_View.as_view(),
             name='acessa_frm_custos_placa'),
    path('gera_dados_razao_placas_proj', views.Frm_Custos_Placa_Proj_View.as_view(),
             name='gera_dados_razao_placas_proj'),
    path('altera_item_cluster_lancamento', views.Frm_Custos_Placa_Proj_View.as_view(), name='altera_item_cluster_lancamento'),
    path('retorna_oss_razao_conta', views.Frm_OS_Razao_Conta_View.as_view(), name='retorna_oss_razao_conta'),
    path('altera_status_cluster_razao', views.Frm_OS_Razao_Conta_View.as_view(), name='altera_status_cluster_razao'),
    path('atualiza_comp_sl_contas', views.Comp_SL_Contas_View.as_view(), name='atualiza_comp_sl_contas')
]