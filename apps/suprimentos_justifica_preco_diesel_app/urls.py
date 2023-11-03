from django.urls import path

from apps.suprimentos_justifica_preco_diesel_app import views

urlpatterns = [
    path('', views.Form_Gera_Compras_Diesel_View.as_view(),
         name='acessa_form_gera_compras_diesel'),
    path('povoa_cd_filial_por_empresa', views.Comp_Filial_Form_Just_Preco_Diesel_View.as_view(),
         name='povoa_cd_filial_por_empresa'),
    path('retorna_compras_diesel', views.Gera_Compras_Diesel_View.as_view(),
         name='retorna_compras_diesel'),
    path('salva_novo_motivo_just_preco_diesel', views.Form_Motivo_Just_Preco_Diesel_View.as_view(),
         name='salva_novo_motivo_just_preco_diesel'),
    path('salva_justificativa_compra_diesel', views.Form_Justificativa_Preco_Diesel_View.as_view(),
         name='salva_justificativa_compra_diesel'),
    path('retorna_justificativa_compra_diesel_registrada', views.Form_Justificativa_Preco_Diesel_View.as_view(),
         name='retorna_justificativa_compra_diesel_registrada'),
]