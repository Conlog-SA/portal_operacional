from django.urls import path

from apps.frota_vendas_veic_app import views

urlpatterns = [
    path('', views.Form_Venda_Veic_View.as_view(),
         name='acessa_form_venda_veic'),
    path('retorna_placas_benner_vincula_a_tabela_selecionada', views.Form_Venda_Veic_View.as_view(),
         name='retorna_placas_benner_vincula_a_tabela_selecionada'),


]