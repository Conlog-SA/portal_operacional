from django.urls import path
from . import views

urlpatterns = [
    path('empilhadeira_check', views.Form_Gerar_Gab_Emp.as_view(), name='empilhadeira_check'),
    path('operador_colaborador', views.Colaborador_Portal.as_view(), name='operador_colaborador'),
    path('operacao_empilhadeira', views.Tipos_Operacao.as_view(), name='operacao_empilhadeira'),
    path('item_check_empilhadeira', views.Item_Check_Aplicado.as_view(), name='item_check_empilhadeira'),
]