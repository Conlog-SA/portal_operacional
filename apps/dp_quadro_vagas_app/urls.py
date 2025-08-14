from django.urls import path

from apps.dp_quadro_vagas_app import views

urlpatterns = [
    path('', views.Frm_Importa_Plan_Quadro_View.as_view(),
         name='acessa_frm_importa_plan_quadro'),
    path('analise_vagas', views.Frm_Analise_Vagas_View.as_view(),
         name='analise_vagas'),
]