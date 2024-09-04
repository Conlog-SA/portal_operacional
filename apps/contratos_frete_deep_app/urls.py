from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.contratos_frete_deep_app import views

urlpatterns = [
    path('', csrf_exempt(views.Processa_Contrato.as_view()), name='contratos_frete_deep'),
]