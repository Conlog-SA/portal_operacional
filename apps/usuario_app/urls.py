from django.urls import path

from apps.usuario_app import views

urlpatterns = [
    path('acessa_form_cad_usu', views.Form_Cad_Usu_View.as_view(), name='acessa_form_cad_usu'),
    path('add_novo_usu', views.Usuario_View.as_view(), name='add_novo_usu'),
    path('list_usuarios', views.Usuario_View.as_view(), name='Form_Cad_Usu_View'),
    path('libera_modulos_usuario', views.Form_Usuario_Menus_View.as_view(), name='libera_modulos_usuario'),
    path('menus_ativos_menus_usu', views.Usuario_Menu_View.as_view(), name='menus_ativos_menus_usu'),
    path('destativa_ativa_item_usuario_menu', views.Usuario_Menu_View.as_view(),
         name='destativa_ativa_item_usuario_menu'),
    path('replica_modulos_ativos_usuarios', views.Form_Replica_Acesso_Menus_View.as_view(),
         name='replica_modulos_ativos_usuarios'),
    path('libera_acesso_projetos', views.Form_Libera_Acesso_Projetos_View.as_view(),
         name='libera_acesso_projetos'),
    path('povoa_cd_filial_por_empresa', views.Componente_Empresa_View.as_view(),
         name='povoa_cd_filial_por_empresa'),
    path('povoa_cd_proj_por_filial', views.Componente_Proj_View.as_view(),
         name='povoa_cd_proj_por_filial'),
    path('retorna_proj_usu', views.Tab_Proj_Usu_View.as_view(),
         name='povoa_cd_proj_por_filial'),
    path('salva_permissoes_projeto_form_libera_proj', views.Form_Libera_Acesso_Projetos_View.as_view(),
         name='salva_permissoes_projeto_form_libera_proj'),
    path('bloqueia_desbloqueia_permissoes_projeto_form_libera_proj', views.Tab_Proj_Usu_View.as_view(),
         name='bloqueia_desbloqueia_permissoes_projeto_form_libera_proj'
        ),
]