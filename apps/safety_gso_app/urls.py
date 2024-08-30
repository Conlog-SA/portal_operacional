from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('gso_check', csrf_exempt(views.Form_Gerar_Check_Gso.as_view()), name='gso_check'),
]