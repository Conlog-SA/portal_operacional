from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('relatos_check', csrf_exempt(views.Form_Gerar_Relatos_Check.as_view()), name='relatos_check'),
    path('lista_atividades', csrf_exempt(views.Lista_Atividades.as_view()), name='lista_atividades'),
    path('acao_check_aplicado', csrf_exempt(views.Acao_Relato_Aplicado.as_view()), name='acao_check_aplicado'),

]