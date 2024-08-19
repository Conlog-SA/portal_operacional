from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('blitz_trajeto_outros_meios_check', csrf_exempt(views.Form_Gerar_Check_Blitz_Trajeto_Outros_Meios.as_view()), name='blitz_trajeto_outros_meios_check'),
]