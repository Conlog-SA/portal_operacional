from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', csrf_exempt(views.Entrevista_Desligamento_Gerencial.as_view()), name='entrevista_desligamento'),
    path('pesquisa_desligamentos', csrf_exempt(views.Frm_Consulta_Entrevista_Desligamento.as_view()), name='pesquisa_desligamentos'),
    path('entrevista_desligamento', csrf_exempt(views.Frm_Resposta_Entrevista_Desligamento.as_view()), name='entrevista_desligamento'),
]