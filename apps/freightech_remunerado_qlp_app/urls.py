from django.urls import path

from apps.freightech_remunerado_qlp_app import views

urlpatterns = [
    path('', views.Frm_Importa_Plan_Remunerado_Freightech_View.as_view(),
                 name='acessa_frm_importa_plan_freightech'),
    path('importa_plan_remunerado_selecionada', views.Frm_Importa_Plan_Remunerado_Freightech_View.as_view(),
                 name='importa_plan_remunerado_selecionada'),

]