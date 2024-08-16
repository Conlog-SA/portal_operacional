from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('blitz_trajeto_moto_check', csrf_exempt(views.Form_Gerar_Check_Blitz_Trajeto_Moto.as_view()), name='blitz_trajeto_moto_check'),
]