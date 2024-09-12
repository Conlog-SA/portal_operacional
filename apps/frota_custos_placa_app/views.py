from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_custos_placa_app.models import Razao_Frota, Item_Cluster
from apps.usuario_app.models import Usuario


# Create your views here.

class Frm_Custos_Placa_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_projetos = []
        if obj_usuario_logado.cod_filial.cod_empresa.cod_empresa == 12:
            lista_projetos_benner = (ConexaoBancoBenner()
                                     .retorna_projetos_by_empresa(
                obj_usuario_logado.cod_filial.cod_empresa.cod_empresa))
            for proj in lista_projetos_benner:
                if any(x in proj.nome_proj for x in ('ROTA', 'TERCEIROS', 'ARMAZEM', 'EQUIPAMENTO', 'AUTO SERVIÇO', 'APOIO', 'UDC'))\
                        and '(INATIVO)' not in proj.nome_proj:
                    lista_projetos.append(proj)
        elif obj_usuario_logado.cod_filial.cod_empresa.cod_empresa == 17:
            lista_projetos_benner_deep = (ConexaoBancoBenner().retorna_projetos_by_empresa(
                obj_usuario_logado.cod_filial.cod_empresa.cod_empresa))
            for proj1 in lista_projetos_benner_deep:
                if any(x in proj1.nome_proj for x in
                       ('OPERACIONAL', 'TRANSPORTE')) and '(INATIVO)' not in proj1.nome_proj:
                    lista_projetos.append(proj1)

            lista_projetos_benner_na_conlog = (ConexaoBancoBenner()
                .retorna_projetos_by_empresa(12))
            for proj2 in lista_projetos_benner_na_conlog:
                if proj2.handle_proj in (380, 390, 875, 1060, 912, 916):
                    lista_projetos.append(proj2)

        context = {
            'cod_empresa': obj_usuario_logado.cod_filial.cod_empresa.cod_empresa,
            'lista_projetos_benner': lista_projetos
        }
        return render(request, 'frota_custos_placa_app/frm_custos_placa.html', context)

class Frm_Custos_Placa_Proj_View(View):
    def get(self, request):
        lista_handle_proj_frm = request.GET['lista_handle_proj']
        lista_handle_tipo_contas_frm = request.GET['lista_handle_tipo_contas']
        comp_frm = request.GET['comp']

        df_custos_placas = ConexaoBancoBenner().retorna_df_razao_placas(lista_handle_proj_frm, lista_handle_tipo_contas_frm, comp_frm.split('-')[0], comp_frm.split('-')[1])
        #df_custos_placas.to_excel('df_custos_placas.xlsx')
        df_group_placas_contas = df_custos_placas[['PLACA', 'NOME_PROJETO', 'desc_tipo_conta', 'HANDLE_CONTA', 'NOME_CONTA',
                                                   'tipo_lancamento','NUM_DOC', 'num_doc_contabil', 'desc_tipo_doc',
                                                   'HISTORICO', 'VAL_LANC', 'codigo_os', 'desc_os', 'desc_produto',
                                                   'desc_cluster', 'NOME_FORNECEDOR', 'handle_lan', 'HANDLE_PROJETO',
                                                   'desc_tipo_os', 'obs_os']].reset_index()

        df_contas_placa_periodo = df_custos_placas[['HANDLE_CONTA', 'NOME_CONTA']].drop_duplicates().reset_index()

        dic_dados_razao = []
        for index, row in df_group_placas_contas.iterrows():
            cod_cluster = 0
            desc_cluster = df_group_placas_contas.loc[index, 'desc_cluster']
            obj_item_cluster = Item_Cluster.objects.filter(desc_item_cluster=desc_cluster).first()
            if obj_item_cluster == None:
                obj_item_cluster = Item_Cluster(
                    desc_item_cluster=desc_cluster
                )
                obj_item_cluster.save()
            else:
                cod_cluster = obj_item_cluster.cod_item_cluster
                desc_cluster = obj_item_cluster.desc_item_cluster
            obj_razao_cluster = (Razao_Frota.objects
                                 .filter(handle_lanc=df_group_placas_contas.loc[index, 'handle_lan']).first())

            if obj_razao_cluster == None:
                obj_razao_cluster = Razao_Frota(
                    handle_lanc = df_group_placas_contas.loc[index, 'handle_lan'],
                    placa = df_group_placas_contas.loc[index, 'PLACA'],
                    handle_projeto = df_group_placas_contas.loc[index, 'HANDLE_PROJETO'],
                    desc_projeto = df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                    desc_tipo_conta = df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                    doc_contabil = df_group_placas_contas.loc[index, 'num_doc_contabil'],
                    valor = df_group_placas_contas.loc[index, 'VAL_LANC'],
                    historico = df_group_placas_contas.loc[index, 'HISTORICO'],
                    nome_fornecedor = df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                    codigo_os = df_group_placas_contas.loc[index, 'codigo_os'],
                    desc_os = df_group_placas_contas.loc[index, 'desc_os'],
                    obs_os = df_group_placas_contas.loc[index, 'obs_os'],
                    desc_tipo_os = df_group_placas_contas.loc[index, 'desc_tipo_os'],
                    itens_os = df_group_placas_contas.loc[index, 'desc_produto'],
                    cod_item_cluster = obj_item_cluster
                )
                obj_razao_cluster.save()
            else:
                obj_razao_cluster.handle_lanc = df_group_placas_contas.loc[index, 'handle_lan']
                obj_razao_cluster.placa = df_group_placas_contas.loc[index, 'PLACA']
                obj_razao_cluster.handle_projeto = df_group_placas_contas.loc[index, 'HANDLE_PROJETO']
                obj_razao_cluster.desc_projeto = df_group_placas_contas.loc[index, 'NOME_PROJETO']
                obj_razao_cluster.desc_tipo_conta = df_group_placas_contas.loc[index, 'desc_tipo_conta']
                obj_razao_cluster.doc_contabil = df_group_placas_contas.loc[index, 'num_doc_contabil']
                obj_razao_cluster.valor = df_group_placas_contas.loc[index, 'VAL_LANC']
                obj_razao_cluster.historico = df_group_placas_contas.loc[index, 'HISTORICO']
                obj_razao_cluster.nome_fornecedor = df_group_placas_contas.loc[index, 'NOME_FORNECEDOR']
                obj_razao_cluster.codigo_os = df_group_placas_contas.loc[index, 'codigo_os']
                obj_razao_cluster.desc_os = df_group_placas_contas.loc[index, 'desc_os']
                obj_razao_cluster.obs_os = df_group_placas_contas.loc[index, 'obs_os']
                obj_razao_cluster.desc_tipo_os = df_group_placas_contas.loc[index, 'desc_tipo_os']
                obj_razao_cluster.itens_os = df_group_placas_contas.loc[index, 'desc_produto']
                obj_razao_cluster.cod_item_cluster = obj_item_cluster
                obj_razao_cluster.save()

            placa_razao = {
                'placa': df_group_placas_contas.loc[index, 'PLACA'],
                'nome_projeto': df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                'conta': df_group_placas_contas.loc[index, 'NOME_CONTA'],
                'desc_tipo_conta': df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                #'num_doc': df_group_placas_contas.loc[index, 'NUM_DOC'],
                'num_doc_contabil': df_group_placas_contas.loc[index, 'num_doc_contabil'],
                'nome_fornec': df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                'tipo_lancamento': df_group_placas_contas.loc[index, 'tipo_lancamento'],
                #'desc_tipo_doc': df_group_placas_contas.loc[index, 'desc_tipo_doc'],
                'val_lanc':df_group_placas_contas.loc[index, 'VAL_LANC'],
                'obs': df_group_placas_contas.loc[index, 'HISTORICO'],
                'codigo_os': df_group_placas_contas.loc[index, 'codigo_os'],
                'desc_os': df_group_placas_contas.loc[index, 'desc_os'],
                'desc_produto': df_group_placas_contas.loc[index, 'desc_produto'],
                'cod_cluster': cod_cluster,
                'desc_cluster': desc_cluster,
                'handle_lan': int(df_group_placas_contas.loc[index, 'handle_lan']),
                'desc_tipo_os': df_group_placas_contas.loc[index, 'desc_tipo_os'],
                'obs_os': df_group_placas_contas.loc[index, 'obs_os']
            }
            dic_dados_razao.append(placa_razao)



        '''lista_contas = []
        for index, row in df_contas_placa_periodo.iterrows():
            dic_contas = {
                'handle_conta': int(df_contas_placa_periodo.loc[index, 'HANDLE_CONTA']),
                'desc_conta': df_contas_placa_periodo.loc[index, 'NOME_CONTA']
            }
            lista_contas.append(dic_contas)'''

        lista_cluster = list(Item_Cluster.objects.all().order_by('desc_item_cluster').values('cod_item_cluster', 'desc_item_cluster'))


        data = dict()
        data = {
            'dic_dados_razao': dic_dados_razao,
            'lista_cluster': lista_cluster
        }
        #return render(request, 'frota_custos_placa_app/frm_lista_placas_proj.html', context)
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_lan_frm = request.POST['cod_lan']
        cod_item_cluster_frm = request.POST['cod_item_cluster']

        obj_lan = Razao_Frota.objects.filter(handle_lanc=cod_lan_frm).first()
        obj_item_cluster = Item_Cluster.objects.get(pk=cod_item_cluster_frm)
        obj_lan.cod_item_cluster = obj_item_cluster
        obj_lan.save()
        data = dict()
        data = {
            'msg': 'Lançamento classificado com sucesso!'
        }
        return JsonResponse(data, safe=False)



