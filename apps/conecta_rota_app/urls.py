from django.urls import path

from apps.conecta_rota_app import views

urlpatterns = [
    path('', views.Frm_Params_RV_Rota_View.as_view(),
         name='acessa_frm_params_rv_rota'),
]