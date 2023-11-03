from django.urls import path

from apps.suprimentos_rel_filial_comprador_app import views

urlpatterns=[
    path('', views.Form_Cad_Rel_Filial_Comprador_View.as_view(),
         name='carrega_form_cad_rel_filial_comprador'),
    path('retorna_registros_rel_filial_comprador', views.Table_Filial_Compradores_View.as_view(),
         name='retorna_registros_rel_filial_comprador'),
    path('add_rel_filial_comprador', views.Cad_Rel_Filial_Comprador_View.as_view(),
         name='add_rel_filial_comprador'),
    path('informar_data_desativacao_filial_comprador', views.Cad_Rel_Filial_Comprador_View.as_view(),
         name='Cad_Rel_Filial_Comprador_View'),
]