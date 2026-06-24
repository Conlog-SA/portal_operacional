from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('registro_de_ocorrencia_check', csrf_exempt(views.Frm_Gerar_Check_Registro_Ocorrencia.as_view()),
         name='registro_de_ocorrencia_check'),
    path('preencher_itens_check_reg_ocorrencia', csrf_exempt(views.Frm_Gerar_Check_Registro_Ocorrencia.as_view()),
         name='preencher_itens_check_reg_ocorrencia')
]