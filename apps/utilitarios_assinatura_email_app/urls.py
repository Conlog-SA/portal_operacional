from django.urls import path

from apps.utilitarios_assinatura_email_app import views

urlpatterns = [
    path('', views.Frm_Assinatura_Email_View.as_view(), name='acessa_frm_assinatura_email'),
    path('carrega_salva_foto_colab', views.Frm_Assinatura_Email_View.as_view(), name='carrega_salva_foto_colab'),
    path('update_tel_colab', views.Frm_Assinatura_Email_View.as_view(), name='update_tel_colab')
]