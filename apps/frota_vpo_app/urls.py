from django.urls import path

from apps.frota_vpo_app import views

urlpatterns = [
    path('', views.Form_Vincula_Roteiro_Pecas_View.as_view(),
        name='acessa_form_gera_compras_diesel'),
    path('retorna_descricao_item', views.Comp_Descricao_Prod_Benner_View.as_view(),
        name='retorna_descricao_item'),
    path('vincula_roteiro_peca', views.Vincular_Roteiro_Peca_View.as_view(),
        name='vincula_roteiro_peca'),
    path('lista_roteiro_peca', views.Vincular_Roteiro_Peca_View.as_view(),
        name='lista_roteiro_peca'),
    path('desvincular_roteiro_peca/<int:pk>/', views.Vincular_Roteiro_Peca_View.as_view(),
        name='desvincular_roteiro_peca'),

]