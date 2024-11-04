from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_custos_placa_app.models import Razao_Frota, Item_Cluster, Os_Razao_Frota
from apps.usuario_app.models import Usuario


# Create your views here.

class Frm_Custos_Placa_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_projetos = []
        logo_empresa = ''
        cor_padrao = ''
        if obj_usuario_logado.cod_filial.cod_empresa.cod_empresa == 12:
            logo_empresa = 'icons/logo-branca.png'
            cor_padrao = '#f46424'
            lista_projetos_benner = (ConexaoBancoBenner()
                                     .retorna_projetos_by_empresa(
                obj_usuario_logado.cod_filial.cod_empresa.cod_empresa))
            for proj in lista_projetos_benner:
                if any(x in proj.nome_proj for x in ('ROTA', 'TERCEIROS', 'ARMAZEM', 'EQUIPAMENTO', 'AUTO SERVIÇO', 'APOIO', 'UDC'))\
                        and '(INATIVO)' not in proj.nome_proj:
                    lista_projetos.append(proj)
        elif obj_usuario_logado.cod_filial.cod_empresa.cod_empresa == 17:
            logo_empresa = 'icons/logo-small-deep.png'
            cor_padrao = '#3b8eed' ##3378ad
            lista_projetos_benner_deep = (ConexaoBancoBenner().retorna_projetos_by_empresa(
                obj_usuario_logado.cod_filial.cod_empresa.cod_empresa))
            for proj1 in lista_projetos_benner_deep:
                if any(x in proj1.nome_proj for x in
                       ('OPERACIONAL', 'TRANSPORTE')) and '(INATIVO)' not in proj1.nome_proj:
                    lista_projetos.append(proj1)

            lista_projetos_benner_na_conlog = (ConexaoBancoBenner().retorna_projetos_by_empresa(12))
            '''143 - OPERACIONAL UEL - GLD
            1060 - OPERACIONAL RIO BRILHANTE - GLD'''
            for proj2 in lista_projetos_benner_na_conlog:
                if proj2.handle_proj in (143, 380, 390, 875, 1060, 912, 916):
                    lista_projetos.append(proj2)


        context = {
            'cod_empresa': obj_usuario_logado.cod_filial.cod_empresa.cod_empresa,
            'logo_empresa': logo_empresa,
            'cor_padrao': cor_padrao,
            'lista_projetos_benner': lista_projetos
        }
        return render(request, 'frota_custos_placa_app/frm_custos_placa.html', context)

class Frm_Custos_Placa_Proj_View(View):
    def get(self, request):
        lista_handle_proj_frm = request.GET['lista_handle_proj']
        lista_handle_tipo_contas_frm = request.GET['lista_handle_tipo_contas']
        lista_handle_contas_frm = request.GET['lista_handle_contas']
        comp_frm = request.GET['comp']

        df_custos_placas = (ConexaoBancoBenner()
                            .retorna_df_razao_placas(lista_handle_proj_frm, lista_handle_tipo_contas_frm,
                                                     comp_frm.split('-')[0], comp_frm.split('-')[1], lista_handle_contas_frm))
        #df_custos_placas.to_excel('df_custos_placas.xlsx')
        df_group_placas_contas = df_custos_placas[['PLACA', 'NOME_PROJETO', 'desc_tipo_conta', 'HANDLE_CONTA',
                                                   'NOME_CONTA','tipo_lancamento','NUM_DOC', 'num_doc_contabil',
                                                   'desc_tipo_doc','HISTORICO', 'VAL_LANC','desc_cluster',
                                                   'NOME_FORNECEDOR', 'handle_lan', 'HANDLE_PROJETO','COMPETENCIA',
                                                   'DATA_LANC', 'handle_fn_doc', 'codigo_os', 'desc_tipo_os',
                                                   'cod_os_razao_frota', 'handle_lanc_cc']].reset_index()

        df_contas_placa_periodo = df_custos_placas[['HANDLE_CONTA', 'NOME_CONTA']].drop_duplicates().reset_index()
        df_group_placas_contas.to_excel('df_group_placas_contas.xlsx')

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
                    data_comp = df_group_placas_contas.loc[index, 'COMPETENCIA'],
                    data_lancamento=df_group_placas_contas.loc[index, 'DATA_LANC'],
                    handle_lanc = df_group_placas_contas.loc[index, 'handle_lan'],
                    handle_lanc_cc= df_group_placas_contas.loc[index, 'handle_lanc_cc'],
                    handle_fn_doc=df_group_placas_contas.loc[index, 'handle_fn_doc'],
                    placa = df_group_placas_contas.loc[index, 'PLACA'],
                    handle_projeto = df_group_placas_contas.loc[index, 'HANDLE_PROJETO'],
                    desc_projeto = df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                    desc_conta = df_group_placas_contas.loc[index, 'NOME_CONTA'],
                    desc_tipo_conta = df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                    doc_contabil = df_group_placas_contas.loc[index, 'num_doc_contabil'],
                    valor = df_group_placas_contas.loc[index, 'VAL_LANC'],
                    historico = df_group_placas_contas.loc[index, 'HISTORICO'],
                    nome_fornecedor = df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                    cod_item_cluster = obj_item_cluster
                )
                obj_razao_cluster.save()


            else:
                obj_razao_cluster.handle_fn_doc = df_group_placas_contas.loc[index, 'handle_fn_doc']
                obj_razao_cluster.placa = df_group_placas_contas.loc[index, 'PLACA']
                obj_razao_cluster.handle_projeto = df_group_placas_contas.loc[index, 'HANDLE_PROJETO']
                obj_razao_cluster.desc_projeto = df_group_placas_contas.loc[index, 'NOME_PROJETO']
                obj_razao_cluster.desc_conta = df_group_placas_contas.loc[index, 'NOME_CONTA'],
                obj_razao_cluster.desc_tipo_conta = df_group_placas_contas.loc[index, 'desc_tipo_conta']
                obj_razao_cluster.doc_contabil = df_group_placas_contas.loc[index, 'num_doc_contabil']
                obj_razao_cluster.valor = df_group_placas_contas.loc[index, 'VAL_LANC']
                obj_razao_cluster.historico = df_group_placas_contas.loc[index, 'HISTORICO']
                obj_razao_cluster.nome_fornecedor = df_group_placas_contas.loc[index, 'NOME_FORNECEDOR']
                obj_razao_cluster.cod_item_cluster = obj_item_cluster
                obj_razao_cluster.save()


            lista_obj_os_razao_frota = (Os_Razao_Frota.objects
                                        .filter(handle_lanc_cc=df_group_placas_contas.loc[index, 'handle_lanc_cc'],
                                                cod_razao_frota__isnull=True))
            for obj_os  in lista_obj_os_razao_frota:
                obj_os.cod_razao_frota = obj_razao_cluster
                obj_os.save()

            tem_os = 'N'
            if df_group_placas_contas.loc[index, 'cod_os_razao_frota'] > 0:
                obj_os_razao_frota = Os_Razao_Frota.objects.get(pk=int(df_group_placas_contas.loc[index, 'cod_os_razao_frota']))
                obj_os_razao_frota.eh_cluster = 1
                obj_os_razao_frota.save()
                tem_os = 'S'

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
                'cod_cluster': cod_cluster,
                'desc_cluster': desc_cluster,
                'handle_lanc_cc': int(df_group_placas_contas.loc[index, 'handle_lanc_cc']),
                'desc_tipo_os': df_group_placas_contas.loc[index, 'desc_tipo_os'],
                'codigo_os': df_group_placas_contas.loc[index, 'codigo_os'],
                'handle_fn_doc': int(df_group_placas_contas.loc[index, 'handle_fn_doc']),
                'data_lancamento': datetime.strptime(df_group_placas_contas.loc[index, 'DATA_LANC'], '%Y-%m-%d').strftime('%d-%m-%Y'),
                'tem_os': tem_os,
                'cod_razao_frota': obj_razao_cluster.cod_razao_frota,
                'handle_lanc_cc': int(df_group_placas_contas.loc[index, 'handle_lanc_cc']),
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
        cod_razao_frota_frm = request.POST['cod_razao_frota']
        cod_item_cluster_frm = request.POST['cod_item_cluster']

        obj_razao_frota = Razao_Frota.objects.get(pk=cod_razao_frota_frm)
        obj_item_cluster = Item_Cluster.objects.get(pk=cod_item_cluster_frm)
        obj_razao_frota.cod_item_cluster = obj_item_cluster
        obj_razao_frota.save()
        data = dict()
        data = {
            'msg': 'Lançamento classificado com sucesso!'
        }
        return JsonResponse(data, safe=False)


class Frm_OS_Razao_Conta_View(View):
    def get(self, request):
        cod_razao_frota_frm = request.GET['cod_razao_frota']

        obj_razao_conta = Razao_Frota.objects.get(pk=int(cod_razao_frota_frm))
        lista_obj_os_razao_conta = list(Os_Razao_Frota.objects.filter(cod_razao_frota = obj_razao_conta)
                                        .values('desc_tipo_os', 'cod_os', 'desc_os', 'desc_prod', 'qtd_prod',
                                                'desc_conj', 'obs_os', 'cod_os_razao_frota', 'eh_cluster'))
        dados = dict()
        dados  = {
            'lista_obj_os_razao_conta': lista_obj_os_razao_conta
        }
        return JsonResponse(dados, safe=False)

    def post(self, request):
        cod_os_razao_conta_frm = request.POST['cod_os_razao_conta']
        status_check_comp_frm = request.POST['status_check_comp']
        obj_os_razao_conta = Os_Razao_Frota.objects.get(pk=cod_os_razao_conta_frm)
        obj_os_razao_conta.eh_cluster = status_check_comp_frm
        obj_os_razao_conta.save()

        obj_item_cluster = None
        if status_check_comp_frm == '1':
            desc_cluster = obj_os_razao_conta.desc_conj
            obj_item_cluster = Item_Cluster.objects.filter(desc_item_cluster=desc_cluster).first()
            if obj_item_cluster == None:
                obj_item_cluster = Item_Cluster(
                    desc_item_cluster=desc_cluster
                )
                obj_item_cluster.save()
        obj_razao_cluster = Razao_Frota.objects.get(pk=obj_os_razao_conta.cod_razao_frota.cod_razao_frota)
        obj_razao_cluster.cod_item_cluster = obj_item_cluster
        obj_razao_cluster.save()


        msg = 'Alterado com sucesso'
        dados = dict()
        dados = {
            'msg': msg
        }
        return JsonResponse(dados, safe=False)


class Comp_SL_Contas_View(View):
    def get(self, request):
        lista_handle_proj_frm = request.GET['lista_handle_proj']
        lista_handle_tipo_contas_frm = request.GET['lista_handle_tipo_contas']
        comp_frm = request.GET['comp']

        lista_contas_periodo = (ConexaoBancoBenner()
                            .retorna_contas_razao_placas_do_periodo(lista_handle_proj_frm, lista_handle_tipo_contas_frm,
                                                     comp_frm.split('-')[0], comp_frm.split('-')[1]))
        dados = dict()
        dados = {
            'lista_contas_periodo': lista_contas_periodo
        }
        return JsonResponse(dados, safe=False)
