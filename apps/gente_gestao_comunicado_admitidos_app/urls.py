from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', csrf_exempt(views.Preencher_Perfil.as_view()), name='preencher'),
    path('validar', csrf_exempt(views.Phishing_Enviados.as_view()), name='validar')
]