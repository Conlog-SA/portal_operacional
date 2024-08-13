from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('seguranca_check', csrf_exempt(views.Form_Seguranca_Check.as_view()), name='seguranca_check'),
    path('lista_check', csrf_exempt(views.Lista_Check.as_view()), name='lista_check'),
    path('registra_check', csrf_exempt(views.Form_Cadastro_Check.as_view()), name='registra_check'),
    path('filiais_check', csrf_exempt(views.Form_Filial_Check.as_view()), name='filiais_check'),
    path('registra_item', csrf_exempt(views.Form_Item_Check.as_view()), name='registra_item'),
    path('sortable', csrf_exempt(views.Sortable_View.as_view()), name='sortable'),
    path('cadastro_colaborador', csrf_exempt(views.Form_Cadastro_Colaborador.as_view()), name='cadastro_colaborador'),
    path('edita_check', csrf_exempt(views.Check_Aplicado_Editar.as_view()), name='edita_check'),

]