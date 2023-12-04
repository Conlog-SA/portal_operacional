from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.Multas_View.as_view(), name='multas_form'),
    path('cadastro_multas', views.Cadastro_Multas_View.as_view(), name='cadastro_multas'),
    path('pesquisa_multas', views.Pesquisa_Multa_View.as_view(), name='pesquisa_multas'),
    path('exclui_multa/<int:pk>/', views.Exclui_Multa_View.as_view(),name='exclui_multa'),
    path('salva_anexo', views.Anexa_Doc_View.as_view(),name='salva_anexo'),
    path('exclui_anexo/<int:cod_anexo_cco>', views.Anexa_Doc_View.as_view(),name='exclui_anexo'),
    path('pesquisa_anexo', views.Pesquisa_Anexo_View.as_view(), name='pesquisa_anexo'),
    path('atualiza_placa', views.Atualiza_Placa_View.as_view(), name='atualiza_placa')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
