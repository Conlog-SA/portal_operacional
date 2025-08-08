from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('empilhadeira_gso_check', csrf_exempt(views.Form_Gerar_Gab_GSO_Emp.as_view()), name='empilhadeira_gso_check'),
    path('operador_colaborador', csrf_exempt(views.Colaborador_Portal.as_view()), name='operador_colaborador'),
    path('empilhadeiras_filial', csrf_exempt(views.Empilhadeiras_Filial.as_view()), name='empilhadeiras_filial'),
]