from django.urls import path
from . import views


urlpatterns = [
    path('', views.Form_Libera_Periodo_Fechamento_Folha_View.as_view(),
         name='acessa_form_libera_periodo_fechamento_folha'),
    path('retorna_periodos_liberados_do_ano', views.Pesq_Periodo_Fechamento_Folha_View.as_view(),
         name='retorna_periodos_liberados_do_ano'),
    path('libera_periodo_fecha_folha', views.Cad_Liberacao_Comp_Fecha_Folha_View.as_view(),
         name='libera_periodo_fecha_folha'),
    path('acessa_form_rel_folha_pagamento', views.Form_Rel_Folha_Pagamento_View.as_view(),
         name='acessa_form_rel_folha_pagamento'),
    path('pesquisa_folha_pag', views.Gera_Rel_Folha_Pagamento_View.as_view(),
         name='pesquisa_folha_pag'),
    path('acessa_form_libera_usu_x_proj', views.Form_Libera_Proj_Usu_View.as_view(),
         name='acessa_form_libera_usu_x_proj'),
    path('pesquisa_proj_liberados_do_usuario', views.Form_Libera_Proj_Usu_Tab_Usu_View.as_view(),
         name='pesquisa_proj_liberados_do_usuario'),
    path('libera_bloqueia_proj_usu_tab_usu', views.Form_Libera_Proj_Usu_Tab_Usu_View.as_view(),
         name='libera_bloqueia_proj_usu_tab_usu'),
    path('pesquisa_usu_liberados_do_projeto', views.Form_Libera_Proj_Usu_Tab_Proj_View.as_view(),
         name='pesquisa_usu_liberados_do_projeto'),
    path('libera_bloqueia_proj_usu_tab_proj', views.Form_Libera_Proj_Usu_Tab_Proj_View.as_view(),
         name='libera_bloqueia_proj_usu_tab_proj'),
    path('pesq_projetos_by_emp', views.Comp_Select_Empresa_View.as_view(),
         name='pesq_projetos_by_emp'),

]