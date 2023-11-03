from django.conf import settings
from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path, include
from apps.conecta_senior_app import views

urlpatterns = [
    # path('listar_colaboradores', views.Listar_Colaboradores.as_view(), name='listar_colaboradores'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)