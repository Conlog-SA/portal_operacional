from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('check_aplicado', csrf_exempt(views.Check_Aplicado_View.as_view()), name='check_aplicado'),
    path('item_aplicado', csrf_exempt(views.Item_Check_Aplicado.as_view()), name='item_aplicado'),
    path('itens_check_aplicado', csrf_exempt(views.Itens_Check_Aplicado.as_view()), name='itens_check_aplicado'),
    path('acao_check_aplicado', csrf_exempt(views.Acao_Check_Aplicado.as_view()), name='acao_check_aplicado'),

]