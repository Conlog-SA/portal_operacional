from django.urls import path

from apps.frota_vendas_veic_app import views

urlpatterns = [
    path('', views.Form_Venda_Veic_View.as_view(),
         name='acessa_form_venda_veic'),
    path('retorna_placas_benner_vincula_a_tabela_selecionada', views.Form_Venda_Veic_View.as_view(),
         name='retorna_placas_benner_vincula_a_tabela_selecionada'),
    path('retorna_marcas_modelo_tipo_veic_selecionado', views.Form_Componente_Select_Tipo_Veic_Marcas_Modelo_View.as_view(),
         name='retorna_marcas_modelo_tipo_veic_selecionado'),
    path('vincula_veic_tab_preco', views.Form_Vincula_Veic_Tab_Precos_View.as_view(),
         name='vincula_veic_tab_preco'),


]