from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('empilhadeira_check', csrf_exempt(views.Form_Gerar_Gab_Emp.as_view()), name='empilhadeira_check'),
    path('operador_colaborador', csrf_exempt(views.Colaborador_Portal.as_view()), name='operador_colaborador'),
    path('operacao_empilhadeira', csrf_exempt(views.Tipos_Operacao.as_view()), name='operacao_empilhadeira'),
    path('item_check_empilhadeira', csrf_exempt(views.Item_Check_Aplicado.as_view()), name='item_check_empilhadeira'),
]