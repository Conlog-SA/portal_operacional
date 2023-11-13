from django.urls import path

from . import views


urlpatterns = [
    path('', views.Multas_View.as_view(), name='multas_form'),
    path('cadastro_multas', views.Cadastro_Multas_View.as_view(), name='cadastro_multas'),
    path('pesquisa_multas', views.Pesquisa_Multa_View.as_view(), name='pesquisa_multas'),
    path('exclui_multa/<int:pk>/', views.Exclui_Multa_View.as_view(),name='exclui_multa'),
    path('anexar_itens/', views.Anexar_Itens, name='anexar_itens'),
    path('download_arquivo/<str:tipo>/', views.download_arquivo, name='download_arquivo')

]
