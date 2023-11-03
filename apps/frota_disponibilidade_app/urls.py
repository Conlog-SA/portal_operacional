from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Form_Imp_Apontamento_Promax.as_view(), name='app_frota_disponibilidade_frota'),
    path('importa_arquivo_apontamento_promax', views.Imp_Apontamento_Promax_View.as_view(),
         name='importa_arquivo_apontamento_promax'),
    path('form_lanc_frota_contratada', views.Form_Lanc_Frota_Contratada.as_view(), name='form_lanc_frota_contratada'),
    path('retorna_lanc_data_frota_contratada', views.Lanc_Frota_Contratada_View.as_view(),
         name='retorna_lanc_data_frota_contratada'),
    path('salva_atualiza_dados_lanc_frota_contratada', views.Lanc_Frota_Contratada_View.as_view(),
         name='salva_atualiza_dados_lanc_frota_contratada'),
    path('retorna_lista_siglas_disp_frota', views.Form_Cad_Comp_Sigla_Disp_Frota_View.as_view(),
        name='retorna_lista_siglas_disp_frota'),
    path('retorna_lista_grupos_disp_frota', views.Form_Cad_Comp_Grupo_Disp_Frota_View.as_view(),
        name='retorna_lista_grupos_disp_frota'),
    path('salva_reg_sigla_disp_frota', views.Cad_Comp_Sigla_Disp_Frota_View.as_view(),
         name='salva_reg_sigla_disp_frota'),
    path('exclui_reg_sigla_disp_frota/<int:pk>/', views.Cad_Comp_Sigla_Disp_Frota_View.as_view(),
        name='exclui_reg_sigla_disp_frota'),
    path('salva_reg_grupo_disp_frota', views.Cad_Comp_Grupo_Disp_Frota_View.as_view(),
        name='salva_reg_grupo_disp_frota'),
    path('exclui_reg_grupo_disp_frota/<int:pk>/', views.Cad_Comp_Grupo_Disp_Frota_View.as_view(),
        name='exclui_reg_grupo_disp_frota'),
    path('carrega_projetos_form_pesq_apont_promax', views.Form_Pesq_Apontamento_Promax.as_view(),
         name='carrega_projetos_form_pesq_apont_promax'),
    path('retorna_lanc_apontamentos_promax_importados', views.Form_Pesq_Apontamento_Promax.as_view(),
         name='retorna_lanc_apontamentos_promax_importados'),
    path('exclui_reg_lanc_apont_promax_disp_frota/<int:pk>/', views.Form_Pesq_Apontamento_Promax.as_view() ,
         name='exclui_reg_lanc_apont_promax_disp_frota'),
    path('importa_arquivo_frota_contratada', views.Imp_Frota_Contratada_View.as_view() ,
         name='importa_arquivo_frota_contratada')

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)