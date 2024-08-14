from django.urls import path

from apps.conecta_as_app import views

urlpatterns = [
    path('', views.Frm_Params_RV_AS_View.as_view(),
         name='acessa_frm_params_rv_as'),
]