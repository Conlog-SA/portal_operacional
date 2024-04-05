from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('safe_login_colab', csrf_exempt(views.Login_Colaborador.as_view()), name='safe_login_colab'),
    path('safe_login_colab_deep', csrf_exempt(views.Login_Colaborador_Deep.as_view()), name='safe_login_colab_deep'),
    path('safe_main_menu', csrf_exempt(views.Menu_Safe.as_view()), name='safe_main_menu'),
    path('lista_colaboradores', csrf_exempt(views.Lista_Colaboradores.as_view()), name='lista_colaboradores'),
    path('documento_colaborador', csrf_exempt(views.Documento_Colaborador.as_view()), name='documento_colaborador'),
]