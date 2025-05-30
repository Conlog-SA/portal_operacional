from django.urls import path
from .views import *
from django.contrib.auth import views
from apps.ti_comitec_app import *

urlpatterns = [
    path('', views.Frm_Cad_Ideias_View.as_view(), name='frm_cad_ideia'),
    path('frm_lista_projetos', views.Frm_Lista_Projetos_View.as_view(), name='frm_lista_projetos'),
    path('modal_frm_lista_projetos', views.Frm_Lista_Projetos_View.as_view(), name='modal_frm_lista_projetos' ),
    path('modal_abrir_edita_projeto', views.Frm_Lista_Projetos_View.as_view(), name='modal_abrir_edita_projeto' ),
    path('abre_modal_itens_gut', views.Frm_Cad_Item_Gut_View.as_view(), name='abre_modal_itens_gut'),
    path('add_item_gut', views.Frm_Cad_Item_Gut_View.as_view(), name='add_item_gut'),
    path('add_nova_ideia_comitec', views.Frm_Cad_Ideias_View.as_view(), name='add_nova_ideia_comitec'),
    path('retorna_dados_chamados', views.Comp_Input_Chamado_View.as_view(), name='retorna_dados_chamados'),
    path('retorna_ideia_comitec_by_id', views.Frm_Edit_Ideia_View.as_view(), name='Frm_Edit_Ideia_View'),
    path('abre_modal_peso_item_gut_ideia', views.Frm_Pontua_Item_Gut_View.as_view(), name='abre_modal_peso_item_gut_ideia'),
    path('pontua_ideia_nota_gut', views.Frm_Pontua_Item_Gut_View.as_view(), name='pontua_ideia_nota_gut'),
    path('atualiza_parecer_tecnico_ideia', views.Frm_Avaliacao_Master_View.as_view(), name='atualiza_parecer_tecnico_ideia'),
    path('atualiza_parecer_head_ideia', views.Frm_Avaliacao_Head_View.as_view(), name='atualiza_parecer_head_ideia'),
    path('abrir_modal_edita_projeto', views.Frm_Edita_Projetos_Ideia_View.as_view(), name='abrir_modal_edita_projeto'),
    path('salva_edita_tarefa', views.Frm_Tarefa_View.as_view(), name='salva_edita_tarefa'),
    path('salva_edita_acao', views.Frm_Acao_View.as_view(), name='salva_edita_acao'),
    path('retorna_acoes_tarefa', views.Frm_Acao_View.as_view(), name='retorna_acoes_tarefa'),
    path('inicia_acao', views.Frm_Acao_View.as_view(), name='inicia_acao'),
    path('conclui_acao', views.Frm_Acao_View.as_view(), name='conclui_acao'),
    path('finaliza_projeto', views.Frm_Edita_Projetos_Ideia_View.as_view(), name='finaliza_projeto'),
    path('vincula_usuarios_projeto', views.Frm_Usuarios_Projeto_View.as_view(), name='vincula_usuarios_projeto'),
    path('atualiza_tab_prox_acoes_proj', views.Frm_Acoes_Usuario_View.as_view(), name='atualiza_tab_prox_acoes_proj'),

]