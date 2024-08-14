

from django.urls import path

from apps.conecta_rv_app import views

urlpatterns = [
    path('', views.Frm_Params_RV_View.as_view(),
         name='acessa_frm_params_rv'),
    path('tab_param_rv', views.Tab_Params_RV_View.as_view(),
         name='tab_param_rv'),
    path('salva_param_rv', views.Frm_Params_RV_View.as_view(),
         name='salva_param_rv'),
]