from django.http import JsonResponse
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
        #df_custos_placas.to_excel('df_custos_placas.xlsx')
        df_group_placas_contas = df_custos_placas[['PLACA', 'NOME_PROJETO', 'desc_tipo_conta', 'NOME_CONTA',
                                                   'tipo_lancamento','NUM_DOC', 'num_doc_contabil', 'desc_tipo_doc',
                                                   'HISTORICO', 'VAL_LANC', 'codigo_os', 'desc_os', 'desc_produto',
                                                   'desc_cluster']].reset_index()

        dic_dados_razao = []
        for index, row in df_group_placas_contas.iterrows():
            placa_razao = {
                'placa': df_group_placas_contas.loc[index, 'PLACA'],
                'nome_projeto': df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                'conta': df_group_placas_contas.loc[index, 'NOME_CONTA'],
                'desc_tipo_conta': df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                'num_doc': df_group_placas_contas.loc[index, 'NUM_DOC'],
                'num_doc_contabil': df_group_placas_contas.loc[index, 'num_doc_contabil'],
                'tipo_lancamento': df_group_placas_contas.loc[index, 'tipo_lancamento'],
                'desc_tipo_doc': df_group_placas_contas.loc[index, 'desc_tipo_doc'],
                'val_lanc':df_group_placas_contas.loc[index, 'VAL_LANC'],
                'obs': df_group_placas_contas.loc[index, 'HISTORICO'],
                'codigo_os': df_group_placas_contas.loc[index, 'codigo_os'],
                'desc_os': df_group_placas_contas.loc[index, 'desc_os'],
                'desc_produto': df_group_placas_contas.loc[index, 'desc_produto'],
                'desc_cluster': df_group_placas_contas.loc[index, 'desc_cluster']
            }
            dic_dados_razao.append(placa_razao)

        data = dict()
        data = {
            'dic_dados_razao': dic_dados_razao

        }
        #return render(request, 'frota_custos_placa_app/frm_lista_placas_proj.html', context)
        return JsonResponse(data, safe=False)


