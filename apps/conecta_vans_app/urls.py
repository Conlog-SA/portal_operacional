from django.urls import path

from apps.conecta_vans_app import views

urlpatterns = [
    path('', views.Frm_Params_RV_Vans_View.as_view(),
         name='acessa_frm_params_rv_as'),
]