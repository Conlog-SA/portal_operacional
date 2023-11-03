from django.urls import path
from apps.home_app import views as home_view


urlpatterns = [
    path('', home_view.Index_View.as_view(), name='index'),
    path('login',home_view.Index_View.as_view(), name='login'),
    path('solicita_acesso',home_view.Solicitacao_Acesso_View.as_view(), name='solicita_acesso'),
]