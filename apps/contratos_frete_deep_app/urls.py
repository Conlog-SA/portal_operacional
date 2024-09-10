from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('contratos_frete_deep', csrf_exempt(views.Processa_Contrato.as_view()), name='contratos_frete_deep'),
]