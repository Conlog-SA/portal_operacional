from django.urls import path

from . import views

urlpatterns = [

   path('', views.Form_5s_View.as_view(),
        name='acessa_form_5s'),
   path('salva_reg_5s_app', views.Cadastro_5s_View.as_view(),
      name='salva_reg_5s_app'),
]