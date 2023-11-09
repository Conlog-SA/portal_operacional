from django.urls import path

from . import views

urlpatterns = [
   path('', views.Form_Bi_View.as_view(),
        name='bi_app'),
]