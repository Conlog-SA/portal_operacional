from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.usuario_app.models import Usuario


# Create your views here.

class Frm_Custos_Placa_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_projetos_benner = (ConexaoBancoBenner()
                                 .retorna_projetos_by_empresa(obj_usuario_logado.cod_filial.cod_empresa.cod_empresa))

        context = {
            'cod_empresa': obj_usuario_logado.cod_filial.cod_empresa.cod_empresa,
            'lista_projetos_benner': lista_projetos_benner
        }
        return render(request, 'frota_custos_placa_app/frm_custos_placa.html', context)

class Frm_Custos_Placa_Proj_View(View):
    def get(self, request):
        lista_handle_proj_frm = request.GET['lista_handle_proj']
        lista_handle_contas_frm = request.GET['lista_handle_contas']
        comp_frm = request.GET['comp']

        df_custos_placas = ConexaoBancoBenner().retorna_df_razao_placas(lista_handle_proj_frm, lista_handle_contas_frm,
                                                                        comp_frm.split('-')[0], comp_frm.split('-')[1])
        df_custos_placas.to_excel('df_custos_placas.xlsx')

        df_group_desc_tipo_placa = df_custos_placas.groupby(['desc_tipo_veic'])[['VAL_LANC']].sum().reset_index()
        df_group_desc_tipo_placa.to_excel('df_group_desc_tipo_placa.xlsx')

        df_group_placas = df_custos_placas.groupby(['desc_tipo_veic', 'PLACA'])[['VAL_LANC']].sum().reset_index()
        df_group_placas.to_excel('df_group_placas.xlsx')

        df_group_placas_contas = df_custos_placas.groupby(['desc_tipo_veic', 'PLACA', 'HANDLE_CONTA', 'NOME_CONTA'])[['VAL_LANC']].sum().reset_index()
        df_group_placas_contas.to_excel('df_group_placas_contas.xlsx')

        context = {
            'df_custos_placas': df_custos_placas,
            'df_group_desc_tipo_placa': df_group_desc_tipo_placa,
            'df_group_placas': df_group_placas,
            'df_group_placas_contas': df_group_placas_contas
        }
        return render(request, 'frota_custos_placa_app/frm_lista_placas_proj.html', context)


