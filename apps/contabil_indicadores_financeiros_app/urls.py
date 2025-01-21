from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', csrf_exempt(views.Acessa_Form_Strut_Contas.as_view()), name='acessa_estrutura_contas'),
   # path('cadastra_conta', csrf_exempt(views.Insere_Conta.as_view()), name='cadastra_conta'),

]