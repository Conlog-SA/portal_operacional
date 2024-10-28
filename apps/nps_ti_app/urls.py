from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', csrf_exempt(views.Form_Nps_Ti_Redirect.as_view()), name='nps_ti_redirect'),
    path('form/', csrf_exempt(views.Form_Nps_Ti.as_view()), name='form'),
    path('email/', csrf_exempt(views.Envio_Email_Nps.as_view()), name='email'),
]