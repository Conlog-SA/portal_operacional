from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('gsdpq_check', csrf_exempt(views.Form_Gerar_Check_Gsdpq.as_view()), name='gsdpq_check'),
]