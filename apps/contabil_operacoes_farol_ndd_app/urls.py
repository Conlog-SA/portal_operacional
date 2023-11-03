from django.urls import path

from apps.contabil_operacoes_farol_ndd_app import views

urlpatterns = [
    path('', views.Form_Registra_Notas_Tratadas_View.as_view(),
         name='acessa_form_form_notas_tratadas'),
    path('pesc_nota_proc_nfe', views.Registra_Notas_Tratadas_View.as_view(),
         name='pesc_nota_proc_nfe'),
    path('retorna_excecoes_lancadas', views.Form_Registra_Excecoes_Operacao_View.as_view(),
         name='retorna_excecoes_lancadas'),
    path('add_excecao_operacao', views.Form_Registra_Excecoes_Operacao_View.as_view(),
         name='add_excecao_operacao'),
    path('excluir_excecao_operacao/<int:pk>/', views.Form_Registra_Excecoes_Operacao_View.as_view(),
        name='excluir_excecao_operacao'),
    path('add_update_justificativa_nota_tratada', views.Cadastro_Justificativa_Nota_Tratada_View.as_view(),
        name='add_update_justificativa_nota_tratada'),
    path('excluir_nota_tratada/<int:pk>/', views.Cadastro_Justificativa_Nota_Tratada_View.as_view(),
        name='excluir_nota_tratada')
]