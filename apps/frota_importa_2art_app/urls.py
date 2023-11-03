from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.frota_importa_2art_app import views

urlpatterns = [
    path('acessar_form_imp_2art', views.Form_Importa_2art_View.as_view(), name='acessar_form_imp_2art'),
    path('carrega_salva_arquivo_2art', views.Form_Importa_2art_View.as_view(),
        name='carrega_salva_arquivo_2art'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)