from django.urls import path

from apps.menu_app import views

urlpatterns = [
    path('acessa_menu', views.Menu_View.as_view(), name='acessa_menu'),
]

#a