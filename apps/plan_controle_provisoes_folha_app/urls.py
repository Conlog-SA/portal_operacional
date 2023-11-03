from django.urls import path
from . import views

urlpatterns = [
    path('', views.Form_Rel_Prov_Sernior_View.as_view(),
         name='acessa_form_rel_provisoes_senior'),
    path('gera_dados_provisoes_senior', views.Gera_Rel_Prov_Sernior_View.as_view(),
         name='gera_dados_provisoes_senior'),
]