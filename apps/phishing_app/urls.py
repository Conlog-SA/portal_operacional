from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', csrf_exempt(views.Phishing.as_view()), name='phishing'),
    path('phishing_enviados', csrf_exempt(views.Phishing_Enviados.as_view()), name='phishing_enviados')
]