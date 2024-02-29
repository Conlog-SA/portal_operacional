from django.urls import path
from . import views

urlpatterns = [
    path('relatos_check', views.Form_Gerar_Relatos_Check.as_view(), name='relatos_check'),
]