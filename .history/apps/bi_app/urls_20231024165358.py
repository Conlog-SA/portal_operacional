from django.urls import path

from . import views

urlpatterns = [
   path('', views.Form_Bi_View.as_view(),
        name='acessa_app_powerbi_cco'),
]