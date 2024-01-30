from django.urls import path
from . import views

urlpatterns = [
    path('empilhadeira_check', views.Form_Gab_Emp.as_view(), name='empilhadeira_check')
]