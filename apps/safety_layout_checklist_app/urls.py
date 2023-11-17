from django.urls import path
from . import views

urlpatterns = [
    path('seguranca_check', views.Form_Seguranca_Check.as_view(), name='seguranca_check'),
]