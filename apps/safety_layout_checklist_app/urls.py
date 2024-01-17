from django.urls import path
from . import views

urlpatterns = [
    path('seguranca_check', views.Form_Seguranca_Check.as_view(), name='seguranca_check'),
    path('registra_check', views.Form_Cadastro_Check.as_view(), name='registra_check'),
    path('filiais_check', views.Form_Filial_Check.as_view(), name='filiais_check'),
    path('registra_item', views.Form_Item_Check.as_view(), name='registra_item'),
    path('sortable', views.Sortable_View.as_view(), name='sortable')
]