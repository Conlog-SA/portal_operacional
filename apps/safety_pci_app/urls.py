from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('pci_check', csrf_exempt(views.Form_Gerar_Check_Pci.as_view()), name='pci_check'),
    #path('lista_atividades', csrf_exempt(views.Lista_Atividades.as_view()), name='lista_atividades'),
]