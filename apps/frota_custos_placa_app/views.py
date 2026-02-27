import locale
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.estrut_org_app.models import Filial
from apps.frota_custos_placa_app.models import Razao_Frota, Item_Cluster, Os_Razao_Frota
from apps.usuario_app.models import Usuario


# Create your views here.

class Frm_Custos_Placa_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_dic_filiais = []
        logo_empresa = ''
        cor_padrao = ''
        if obj_usuario_logado.cod_filial.cod_empresa.cod_empresa == 12:
            logo_empresa = 'icons/logo-branca.png'
            cor_padrao = '#f46424'
            lista_obj_filiais = Filial.objects.filter(cod_empresa=12, ativo=1).exclude(cod_filial__in=[34,57,89])
            for fil in lista_obj_filiais:
                f = {
                    'handle_filial': fil.handle_benner,
                    'nome_filial': fil.desc_filial
                }
                lista_dic_filiais.append(f)
        elif obj_usuario_logado.cod_filial.cod_empresa.cod_empresa == 17:
            logo_empresa = 'icons/logo-small-deep.png'
            cor_padrao = '#3b8eed' ##3378ad
            lista_obj_filiais_deep = Filial.objects.filter(cod_empresa=17, ativo=1).exclude(cod_filial__in=[34, 57, 89])
            lista_obj_filiais_conlog = Filial.objects.filter(cod_empresa=12, ativo=1, cod_filial__in=[34, 57, 89])
            for fil in lista_obj_filiais_deep:
                f = {
                    'handle_filial': fil.handle_benner,
                    'nome_filial': fil.desc_filial
                }
                lista_dic_filiais.append(f)
            for fil in lista_obj_filiais_conlog:
                f = {
                    'handle_filial': fil.handle_benner,
                    'nome_filial': fil.desc_filial
                }
                lista_dic_filiais.append(f)


        context = {
            'cod_empresa': obj_usuario_logado.cod_filial.cod_empresa.cod_empresa,
            'logo_empresa': logo_empresa,
            'cor_padrao': cor_padrao,
            'lista_dic_filiais': lista_dic_filiais
        }
        return render(request, 'frota_custos_placa_app/frm_custos_placa.html', context)

class Frm_Custos_Placa_Proj_View(View):
    def get(self, request):
        transacao_frm = request.GET['transacao']
        handle_filial_frm = request.GET['handle_filial']
        comp_frm = request.GET['comp']

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        data = dict()
        if transacao_frm == 'pesquisa_filial_projeto_placa':
            lista_handle_contas_frm = request.GET['lista_handle_contas']

            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], lista_handle_contas_frm, transacao_frm,
                                                        None, None)

            #lista_cluster = list(Item_Cluster.objects.all().order_by('desc_item_cluster').values('cod_item_cluster', 'desc_item_cluster'))



            data = {
                'total_real_filial': locale.currency(dados_custos[0], grouping=True, symbol=None),
                'total_orc_filial': locale.currency(dados_custos[1], grouping=True, symbol=None),
                'total_rem_filial': locale.currency(dados_custos[2], grouping=True, symbol=None),
                'dic_resumo_filial': dados_custos[3].to_dict(orient='records'),
                'dic_resumo_projeto': dados_custos[4].to_dict(orient='records'),
                'dic_resumo_placas': dados_custos[5].to_dict(orient='records'),
                #'dic_projeto_placa': dados_custos[].to_dict(orient='records'),

            }
        elif transacao_frm == 'pesquisa_fil_conta_projetos':
            handle_conta_frm = request.GET['handle_conta']

            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], handle_conta_frm, transacao_frm,
                                                        None, None)
            data = {
                'dic_resumo_projetos': dados_custos.to_dict(orient='records')
            }

        elif transacao_frm == 'pesquisa_fil_conta_projeto_placas':
            handle_proj_frm = request.GET['handle_proj']
            handle_conta_frm = request.GET['handle_conta']
            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], handle_conta_frm, transacao_frm,
                                                        handle_proj_frm, None)
            data = {
                'dic_resumo_placas': dados_custos.to_dict(orient='records')
            }

        elif transacao_frm == 'pesquisa_projeto_contas':
            handle_proj_frm = request.GET['handle_proj']
            lista_handle_contas_frm = request.GET['lista_handle_contas']
            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], lista_handle_contas_frm, transacao_frm,
                                                        handle_proj_frm, None)
            data = {
                'dic_resumo_projeto_contas': dados_custos.to_dict(orient='records')
            }

        elif transacao_frm == 'pesquisa_proj_conta_placas':
            handle_proj_frm = request.GET['handle_proj']
            handle_contas_frm = request.GET['handle_conta']
            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], handle_contas_frm, transacao_frm,
                                                        handle_proj_frm, None)
            data = {
                'dic_resumo_placas': dados_custos.to_dict(orient='records')
            }

        elif transacao_frm == 'pesquisa_placas_contas':
            lista_handle_contas_frm = request.GET['lista_handle_contas']
            placa_frm = request.GET['placa']

            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], lista_handle_contas_frm, transacao_frm,
                                                        None, placa_frm)
            data = {
                'dic_resumo_contas': dados_custos.to_dict(orient='records')
            }
        elif transacao_frm == 'pesquisa_razao_filial_conta_proj_placa':
            handle_proj_frm = request.GET['handle_proj']
            handle_conta_frm = request.GET['handle_conta']
            placa_frm = request.GET['placa']

            dados_custos = self.gera_dados_custos_frota(handle_filial_frm, comp_frm.split('-')[0],
                                                        comp_frm.split('-')[1], handle_conta_frm, transacao_frm,
                                                        handle_proj_frm, placa_frm)
            data = {
                'dic_resumo_razao': dados_custos
            }



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


    def gera_dados_custos_frota(self, handle_filial, ano, mes, lista_handle_contas, formulario, projeto, placa):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')


        if formulario == 'pesquisa_filial_projeto_placa':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_frota(handle_filial, ano, mes, lista_handle_contas, None, None))

            df_group_placas_contas = df_custos_placas[['PLACA', 'NOME_PROJETO', 'HANDLE_CONTA', 'NOME_CONTA', 'VAL_LANC',
                                                       'HANDLE_PROJETO', 'COMPETENCIA', 'handle_filial']].reset_index()

            total_real_filial = df_group_placas_contas['VAL_LANC'].sum()
            total_orc_filial = 0.00
            total_rem_filial = 0.00

            df_resumo_filial_conta = df_group_placas_contas.groupby(['handle_filial', 'HANDLE_CONTA', 'NOME_CONTA'])[
                ['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_filial_conta['perc_realizado'] = df_resumo_filial_conta['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_filial) * 100, grouping=True, symbol=None))
            df_resumo_filial_conta['VAL_LANC'] = df_resumo_filial_conta['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            df_resumo_projeto = df_group_placas_contas.groupby(['HANDLE_PROJETO', 'NOME_PROJETO'])[
                ['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_projeto['perc_realizado'] = df_resumo_projeto['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_filial) * 100, grouping=True, symbol=None))
            df_resumo_projeto['VAL_LANC'] = df_resumo_projeto['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            df_resumo_placa = df_group_placas_contas.groupby(['PLACA'])[
                ['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_placa['perc_realizado'] = df_resumo_placa['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_filial) * 100, grouping=True, symbol=None))
            df_resumo_placa['VAL_LANC'] = df_resumo_placa['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))


            return total_real_filial, total_orc_filial, total_rem_filial, df_resumo_filial_conta, df_resumo_projeto, df_resumo_placa

        elif formulario == 'pesquisa_fil_conta_projetos':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_frota(handle_filial, ano, mes, lista_handle_contas,
                                                        None, None))
            df_group_placas_contas = df_custos_placas[
                ['NOME_PROJETO', 'HANDLE_CONTA', 'NOME_CONTA', 'VAL_LANC',
                 'HANDLE_PROJETO', 'COMPETENCIA', 'handle_filial']].reset_index()

            total_real_conta = df_group_placas_contas['VAL_LANC'].sum()

            df_resumo_projeto = df_group_placas_contas.groupby(['HANDLE_PROJETO', 'NOME_PROJETO'])[
                ['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_projeto['perc_realizado'] = df_resumo_projeto['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_conta) * 100, grouping=True, symbol=None))
            df_resumo_projeto['VAL_LANC'] = df_resumo_projeto['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            return df_resumo_projeto

        elif formulario == 'pesquisa_fil_conta_projeto_placas':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_frota(handle_filial, ano, mes, lista_handle_contas,
                                                        None, None))
            df_group_placas_contas = df_custos_placas[
                ['HANDLE_PROJETO', 'HANDLE_CONTA', 'PLACA', 'VAL_LANC', 'COMPETENCIA', 'handle_filial']].reset_index()

            total_real_projeto = df_group_placas_contas['VAL_LANC'].sum()

            df_resumo_placas = df_group_placas_contas.groupby(['handle_filial', 'HANDLE_PROJETO', 'HANDLE_CONTA', 'PLACA'])[
                ['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_placas['perc_realizado'] = df_resumo_placas['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_projeto) * 100, grouping=True, symbol=None))
            df_resumo_placas['VAL_LANC'] = df_resumo_placas['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            return df_resumo_placas

        elif formulario == 'pesquisa_projeto_contas':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_frota(handle_filial, ano, mes, lista_handle_contas, projeto, None))

            df_group_placas_contas = df_custos_placas[['HANDLE_PROJETO', 'NOME_PROJETO', 'HANDLE_CONTA', 'NOME_CONTA',
                                                       'VAL_LANC','COMPETENCIA']].reset_index()

            total_real_projeto = df_group_placas_contas['VAL_LANC'].sum()

            df_resumo_projeto_conta = df_group_placas_contas.groupby(['HANDLE_PROJETO', 'HANDLE_CONTA', 'NOME_CONTA'])[['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_projeto_conta['perc_realizado'] = df_resumo_projeto_conta['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_projeto) * 100, grouping=True, symbol=None))
            df_resumo_projeto_conta['VAL_LANC'] = df_resumo_projeto_conta['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            return df_resumo_projeto_conta

        elif formulario == 'pesquisa_proj_conta_placas':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_frota(handle_filial, ano, mes, lista_handle_contas,
                                                        None, None))
            df_group_placas_contas = df_custos_placas[
                ['HANDLE_PROJETO', 'HANDLE_CONTA', 'PLACA', 'VAL_LANC', 'COMPETENCIA', 'handle_filial']].reset_index()

            total_real_conta = df_group_placas_contas['VAL_LANC'].sum()

            df_resumo_placas = df_group_placas_contas.groupby(['handle_filial', 'HANDLE_PROJETO', 'HANDLE_CONTA', 'PLACA'])[
                ['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_placas['perc_realizado'] = df_resumo_placas['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_conta) * 100, grouping=True, symbol=None))
            df_resumo_placas['VAL_LANC'] = df_resumo_placas['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            return df_resumo_placas

        elif formulario == 'pesquisa_placas_contas':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_frota(handle_filial, ano, mes, lista_handle_contas, projeto, placa))

            df_group_placas_contas = df_custos_placas[['handle_filial', 'HANDLE_PROJETO', 'HANDLE_CONTA', 'NOME_CONTA', 'PLACA', 'VAL_LANC','COMPETENCIA']].reset_index()

            total_real_placa = df_group_placas_contas['VAL_LANC'].sum()


            df_resumo_placa_contas = df_group_placas_contas.groupby(['PLACA', 'handle_filial', 'HANDLE_PROJETO', 'HANDLE_CONTA', 'NOME_CONTA'])[['VAL_LANC']].sum().reset_index().sort_values(by='VAL_LANC', ascending=False)
            df_resumo_placa_contas['perc_realizado'] = df_resumo_placa_contas['VAL_LANC'].apply(
                lambda x: locale.currency((x / total_real_placa) * 100, grouping=True, symbol=None))
            df_resumo_placa_contas['VAL_LANC'] = df_resumo_placa_contas['VAL_LANC'].apply(
                lambda x: locale.currency(x, grouping=True, symbol=None))

            return df_resumo_placa_contas

        elif formulario == 'pesquisa_razao_filial_conta_proj_placa':
            dic_dados_razao = (ConexaoBancoBenner()
                                .retorna_df_razao_placas(handle_filial, ano, mes, lista_handle_contas, projeto, placa))


            for razao in dic_dados_razao:
                '''
                cod_cluster = 0
                desc_cluster = razao['desc_cluster']
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
                                     .filter(handle_lanc=razao['handle_lan']).first())

                if obj_razao_cluster == None:
                    obj_razao_cluster = Razao_Frota(
                        data_comp=razao['COMPETENCIA'],
                        data_lancamento=razao['DATA_LANC'],
                        handle_lanc=razao['handle_lan'],
                        handle_lanc_cc=df_group_placas_contas.loc[index, 'handle_lanc_cc'],
                        handle_fn_doc=df_group_placas_contas.loc[index, 'handle_fn_doc'],
                        placa=df_group_placas_contas.loc[index, 'PLACA'],
                        handle_projeto=df_group_placas_contas.loc[index, 'HANDLE_PROJETO'],
                        desc_projeto=df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                        desc_conta=df_group_placas_contas.loc[index, 'NOME_CONTA'],
                        desc_tipo_conta=df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                        doc_contabil=df_group_placas_contas.loc[index, 'num_doc_contabil'],
                        valor=df_group_placas_contas.loc[index, 'VAL_LANC'],
                        historico=df_group_placas_contas.loc[index, 'HISTORICO'],
                        nome_fornecedor=df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                        cod_item_cluster=obj_item_cluster
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
                for obj_os in lista_obj_os_razao_frota:
                    obj_os.cod_razao_frota = obj_razao_cluster
                    obj_os.save()
                '''

                '''tem_os = 'N'
                if df_group_placas_contas.loc[index, 'cod_os_razao_frota'] > 0:
                    obj_os_razao_frota = Os_Razao_Frota.objects.get(
                        pk=int(df_group_placas_contas.loc[index, 'cod_os_razao_frota']))
                    obj_os_razao_frota.eh_cluster = 1
                    obj_os_razao_frota.save()
                    tem_os = 'S'''
                tem_os = 'N'
                if len(razao['dic_os_razao']) > 0:
                    tem_os = 'S'
                razao['tem_os'] = tem_os
                razao['val_lanc'] = locale.currency(razao['val_lanc'], grouping=True, symbol=None)

                '''placa_razao = {
                    'placa': df_group_placas_contas.loc[index, 'PLACA'],
                    'nome_projeto': df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                    'conta': df_group_placas_contas.loc[index, 'NOME_CONTA'],
                    'desc_tipo_conta': df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                    'num_doc': df_group_placas_contas.loc[index, 'NUM_DOC'],
                    'num_doc_contabil': df_group_placas_contas.loc[index, 'num_doc_contabil'],
                    'nome_fornec': df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                    'tipo_lancamento': df_group_placas_contas.loc[index, 'tipo_lancamento'],
                    'desc_tipo_doc': df_group_placas_contas.loc[index, 'desc_tipo_doc'],
                    'val_lanc': locale.currency(df_group_placas_contas.loc[index, 'VAL_LANC'], grouping=True, symbol=None),
                    'obs': df_group_placas_contas.loc[index, 'HISTORICO'],
                    'cod_cluster': cod_cluster,
                    'desc_cluster': desc_cluster,
                    'handle_lanc_cc': int(df_group_placas_contas.loc[index, 'handle_lanc_cc']),
                    'desc_tipo_os': df_group_placas_contas.loc[index, 'desc_tipo_os'],
                    'codigo_os': df_group_placas_contas.loc[index, 'codigo_os'],
                    'handle_fn_doc': int(df_group_placas_contas.loc[index, 'handle_fn_doc']),
                    'data_lancamento': datetime.strptime(df_group_placas_contas.loc[index, 'DATA_LANC'],
                                                         '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'tem_os': tem_os,
                    'cod_razao_frota': obj_razao_cluster.cod_razao_frota,
                    'handle_lanc_cc': int(df_group_placas_contas.loc[index, 'handle_lanc_cc']),
                }
                dic_dados_razao.append(placa_razao)'''
            return dic_dados_razao
        elif formulario == 'pesquisa_razao_placa_conta':
            df_custos_placas = (ConexaoBancoBenner()
                                .retorna_df_razao_placas(handle_filial, ano, mes, lista_handle_contas, projeto, placa))

            df_group_placas_contas = df_custos_placas[['PLACA', 'NOME_PROJETO', 'desc_tipo_conta', 'HANDLE_CONTA',
                                                       'NOME_CONTA', 'tipo_lancamento', 'NUM_DOC', 'num_doc_contabil',
                                                       'desc_tipo_doc', 'HISTORICO', 'VAL_LANC', 'desc_cluster',
                                                       'NOME_FORNECEDOR', 'handle_lan', 'HANDLE_PROJETO', 'COMPETENCIA',
                                                       'DATA_LANC', 'handle_fn_doc', 'codigo_os', 'desc_tipo_os',
                                                       'cod_os_razao_frota', 'handle_lanc_cc',
                                                       'handle_filial']].reset_index()


            #df_contas_placa_periodo = df_custos_placas[['HANDLE_CONTA', 'NOME_CONTA']].drop_duplicates().reset_index()
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
                        data_comp=df_group_placas_contas.loc[index, 'COMPETENCIA'],
                        data_lancamento=df_group_placas_contas.loc[index, 'DATA_LANC'],
                        handle_lanc=df_group_placas_contas.loc[index, 'handle_lan'],
                        handle_lanc_cc=df_group_placas_contas.loc[index, 'handle_lanc_cc'],
                        handle_fn_doc=df_group_placas_contas.loc[index, 'handle_fn_doc'],
                        placa=df_group_placas_contas.loc[index, 'PLACA'],
                        handle_projeto=df_group_placas_contas.loc[index, 'HANDLE_PROJETO'],
                        desc_projeto=df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                        desc_conta=df_group_placas_contas.loc[index, 'NOME_CONTA'],
                        desc_tipo_conta=df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                        doc_contabil=df_group_placas_contas.loc[index, 'num_doc_contabil'],
                        valor=df_group_placas_contas.loc[index, 'VAL_LANC'],
                        historico=df_group_placas_contas.loc[index, 'HISTORICO'],
                        nome_fornecedor=df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                        cod_item_cluster=obj_item_cluster
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
                for obj_os in lista_obj_os_razao_frota:
                    obj_os.cod_razao_frota = obj_razao_cluster
                    obj_os.save()

                tem_os = 'N'
                if df_group_placas_contas.loc[index, 'cod_os_razao_frota'] > 0:
                    obj_os_razao_frota = Os_Razao_Frota.objects.get(
                        pk=int(df_group_placas_contas.loc[index, 'cod_os_razao_frota']))
                    obj_os_razao_frota.eh_cluster = 1
                    obj_os_razao_frota.save()
                    tem_os = 'S'

                placa_razao = {
                    'placa': df_group_placas_contas.loc[index, 'PLACA'],
                    'nome_projeto': df_group_placas_contas.loc[index, 'NOME_PROJETO'],
                    'conta': df_group_placas_contas.loc[index, 'NOME_CONTA'],
                    'desc_tipo_conta': df_group_placas_contas.loc[index, 'desc_tipo_conta'],
                    # 'num_doc': df_group_placas_contas.loc[index, 'NUM_DOC'],
                    'num_doc_contabil': df_group_placas_contas.loc[index, 'num_doc_contabil'],
                    'nome_fornec': df_group_placas_contas.loc[index, 'NOME_FORNECEDOR'],
                    'tipo_lancamento': df_group_placas_contas.loc[index, 'tipo_lancamento'],
                    # 'desc_tipo_doc': df_group_placas_contas.loc[index, 'desc_tipo_doc'],
                    'val_lanc': locale.currency(df_group_placas_contas.loc[index, 'VAL_LANC'], grouping=True, symbol=None),
                    'obs': df_group_placas_contas.loc[index, 'HISTORICO'],
                    'cod_cluster': cod_cluster,
                    'desc_cluster': desc_cluster,
                    'handle_lanc_cc': int(df_group_placas_contas.loc[index, 'handle_lanc_cc']),
                    'desc_tipo_os': df_group_placas_contas.loc[index, 'desc_tipo_os'],
                    'codigo_os': df_group_placas_contas.loc[index, 'codigo_os'],
                    'handle_fn_doc': int(df_group_placas_contas.loc[index, 'handle_fn_doc']),
                    'data_lancamento': datetime.strptime(df_group_placas_contas.loc[index, 'DATA_LANC'],
                                                         '%Y-%m-%d').strftime('%d-%m-%Y'),
                    'tem_os': tem_os,
                    'cod_razao_frota': obj_razao_cluster.cod_razao_frota,
                    'handle_lanc_cc': int(df_group_placas_contas.loc[index, 'handle_lanc_cc']),
                }
                dic_dados_razao.append(placa_razao)
            return dic_dados_razao

class Frm_OS_Razao_Conta_View(View):
    def get(self, request):
        cod_razao_frota_frm = request.GET['cod_razao_frota']

        obj_razao_conta = Razao_Frota.objects.get(pk=int(cod_razao_frota_frm))
        lista_obj_os_razao_conta = list(Os_Razao_Frota.objects.filter(cod_razao_frota = obj_razao_conta)
                                        .values('desc_tipo_os', 'cod_os', 'desc_os', 'desc_prod', 'qtd_prod',
                                                'desc_conj', 'obs_os', 'cod_os_razao_frota', 'eh_cluster',
                                                'cod_razao_frota__historico', 'desc_tipo_os', 'cod_razao_frota__nome_fornecedor',
                                                'cod_razao_frota__doc_contabil', 'cod_razao_frota__desc_projeto',
                                                'cod_razao_frota__desc_tipo_conta'))
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
        handle_filial_frm = request.GET['handle_filial']
        #lista_handle_tipo_contas_frm = request.GET['lista_handle_tipo_contas']
        comp_frm = request.GET['comp']

        lista_contas_periodo = (ConexaoBancoBenner()
                            .retorna_contas_razao_placas_do_periodo(handle_filial_frm,
                                                     comp_frm.split('-')[0], comp_frm.split('-')[1]))
        dados = dict()
        dados = {
            'lista_contas_periodo': lista_contas_periodo
        }
        return JsonResponse(dados, safe=False)
