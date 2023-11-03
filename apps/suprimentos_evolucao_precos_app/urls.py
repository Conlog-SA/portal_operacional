from django.urls import path
#from apps.app_suprimentos_evolucao_precos.dash_apps.finished_apps import simpleexample
#from apps.suprimentos_evolucao_precos_app.dash_apps.finished_apps import simpleexample
from apps.suprimentos_evolucao_precos_app import views

urlpatterns = [
    path('', views.Form_Gera_Evolucao_Precos_View.as_view(),
         name='acessa_form_gera_evolucao_precos'),
    path('gera_dados_evolucao_precos', views.Gera_Evolucao_Precos_View.as_view(),
         name='gera_dados_evolucao_precos'),
    path('retorna_compras_item_filial', views.Form_Compras_Item_Filial_View.as_view(),
         name='retorna_compras_item_filial'),
    path('povoa_cd_filial_por_empresa', views.Comp_Filiais_Evolucao_Precos_View.as_view(),
         name='povoa_cd_filial_por_empresa'),
    path('salva_compras_auditadas', views.Form_Compras_Item_Filial_View.as_view(),
         name='salva_compras_auditadas'),
    path('povoa_cd_itens_by_familia', views.Comp_Itens_Evolucao_Precos_View.as_view(),
         name='povoa_cd_itens_by_familia'),
    path('acessa_dash', views.Dash_Evolucao_Precos_View.as_view(),
         name='acessa_dash'),
    path('gera_dash_evolucao_precos', views.Gera_Dash_Evolucao_Precos_View.as_view(),
         name='gera_dash_evolucao_precos'),
]
