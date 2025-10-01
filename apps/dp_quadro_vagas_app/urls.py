from django.urls import path

from apps.dp_quadro_vagas_app import views

urlpatterns = [
    path('analise_vagas', views.Frm_Analise_Vagas_View.as_view(),
         name='analise_vagas'),
]