from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Form_Gera_Disp_Emp_View.as_view(), name='form_gera_disp_empilhadeira'),
    path('abre_modal_param_geracao_disp_emp', views.Form_Param_Geracao_Disp_Emp_View.as_view(),
         name='abre_modal_param_geracao_disp_emp'),
    path('gera_dados_disp_emp', views.Gera_Dados_Disponibilidade_Empilhadeira_View.as_view(),
         name='gera_dados_disp_emp'),
    path('pesq_dados_indisp_emp', views.Gera_Dados_Disponibilidade_Empilhadeira_View.as_view(),
         name='pesq_dados_indisp_emp'),
    path('retorna_reg_apont_disp_emp', views.Form_Edit_Apont_Disp_Emp_View.as_view(),
         name='retorna_reg_apont_disp_emp'),
    path('deleta_reg_os_apont_disp_emp/<int:pk>', views.Form_Edit_Apont_Disp_Emp_View.as_view(),
         name='deleta_reg_os_apont_disp_emp'),
    path('retorna_os_da_placa_do_turno_do_apondamento_selecionado/<int:pk>', views.Form_Os_Benner_View.as_view(),
         name='retorna_os_da_placa_do_turno_do_apondamento_selecionado'),
    path('vincula_os_apont_disp_emp', views.Form_Os_Benner_View.as_view(),
         name='vincula_os_apont_disp_emp'),
    path('retorna_todas_placas_ativa_form_gera_disp_emp', views.Form_Param_Geracao_Disp_Emp_View.as_view(),
         name='retorna_todas_placas_ativa_form_gera_disp_emp'),
    path('atualiza_dados_apontamento_os_vinculada', views.Form_Edit_Apont_Disp_Emp_View.as_view(),
         name='atualiza_dados_apontamento_os_vinculada'),
    path('importa_arquivo_apontamento_promax_empilhadeira', views.Imp_Apontamento_Promax_Empilhadeira_View.as_view(),
         name='importa_arquivo_apontamento_promax_empilhadeira'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)