from django.urls import path

from apps.ti_comitec_app import views

urlpatterns = [
    path('', views.Frm_Cad_Ideias_View.as_view(), name='frm_cad_ideia'),
    path('abre_modal_itens_gut', views.Frm_Cad_Item_Gut_View.as_view(), name='abre_modal_itens_gut'),
    path('add_item_gut', views.Frm_Cad_Item_Gut_View.as_view(), name='add_item_gut'),
    path('add_nova_ideia_comitec', views.Frm_Cad_Ideias_View.as_view(), name='add_nova_ideia_comitec'),
    path('retorna_dados_chamados', views.Comp_Input_Chamado_View.as_view(), name='retorna_dados_chamados'),
    path('retorna_ideia_comitec_by_id', views.Frm_Edit_Ideia_View.as_view(), name='Frm_Edit_Ideia_View'),
    path('abre_modal_peso_item_gut_ideia', views.Frm_Pontua_Item_Gut_View.as_view(), name='abre_modal_peso_item_gut_ideia'),
    path('pontua_ideia_nota_gut', views.Frm_Pontua_Item_Gut_View.as_view(), name='pontua_ideia_nota_gut'),
]