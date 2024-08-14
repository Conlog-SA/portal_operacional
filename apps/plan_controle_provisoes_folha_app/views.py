import locale
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.plan_controle_folha_pag_analitico_app.models import Confirma_Periodo_Fechamento_Folha
from apps.estrut_org_app.models import Filial, Projeto
from apps.usuario_app.models import Usuario, Proj_Usu, Liberacao_Usuario_Projeto_Benner
from apps.conecta_senior_app.models import Registro_Provisao_Folha_Analitico_Colab, Registro_Provisao_Folha_Analitico_Proevento
from apps.conecta_senior_app.views import Conexao_Senior_BD


class Form_Rel_Prov_Sernior_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']

        obj_usuario = Usuario.objects.get(pk=id_usu_session)
        # lista_projetos = Proj_Usu.objects.filter(cod_usu=obj_usuario, status_proj_usu_folha_pag='S')
        lista_projetos = Liberacao_Usuario_Projeto_Benner.objects.filter(cod_usu=obj_usuario,
                                                                         ativo_app_folha_pagamento='S')
        lista_periodos_liberados = Confirma_Periodo_Fechamento_Folha.objects.filter(ativa='S')
        context = {
            'lista_periodos_liberados': lista_periodos_liberados,
            'desc_menu_principal': 'Rel. Provisões Folha',
            'lista_projetos': lista_projetos,
            'id_menu_pai': 58
        }
        return render(request, 'plan_controle_provisoes_folha_app/form_rel_provisoes_senior.html', context)

class Gera_Rel_Prov_Sernior_View(View):
    def get(self, request):
        cod_tipo_prov_form = request.GET['cod_tipo_provisao']
        cod_comp_form = request.GET['cod_competencia']
        lista_handle_proj_form = request.GET['lista_handle_proj']
        cod_empresa_frm = request.GET['cod_empresa']
        desc_tipo_proevento_pesq = 'Férias'
        if cod_tipo_prov_form == 2:
            desc_tipo_proevento_pesq = '13º Salário'


        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        obj_competencia = Confirma_Periodo_Fechamento_Folha.objects.get(pk=cod_comp_form)
        str_data_ref = str(obj_competencia.ano_competencia_periodo) + '-' + \
                       str(obj_competencia.mes_competencia_periodo) + \
                       '-1'

        df_dados_proeventos = Conexao_Senior_BD(cod_empresa_frm).retorna_df_provisao_folha_senior(str_data_ref, lista_handle_proj_form, cod_tipo_prov_form)

        df_dados_proeventos_total_item = df_dados_proeventos[['desc_prov','val_base_prov','perc_dias_prov',
                                                              'val_anterior_prov','val_transf_prov','val_ajuste_prov',
                                                              'val_prov','val_pag_prov','val_indenizado_prov',
                                                              'val_saldo_prov']]\
            .groupby('desc_prov')\
            .sum()\
            .sort_values('val_base_prov', ascending=True)
        dados_proeventos_itens = []
        for index, row in df_dados_proeventos_total_item.iterrows():
            reg_prov_item = Registro_Provisao_Folha_Analitico_Proevento(
                #desc_prov=str(df_dados_proeventos_total_item.loc[index, 'desc_prov']),
                desc_prov=index,
                val_base_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_base_prov'], 2),
                                              grouping=True, symbol=None),
                perc_dias_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'perc_dias_prov'], 2),
                                               grouping=True, symbol=None),
                val_anterior_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_anterior_prov']
                                                        , 2), grouping=True, symbol=None),
                val_transf_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_transf_prov'], 2),
                                                grouping=True, symbol=None),
                val_ajuste_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_ajuste_prov'], 2),
                                                grouping=True, symbol=None),
                val_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_prov'], 2),
                                         grouping=True, symbol=None),
                val_pag_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_pag_prov'], 2),
                                             grouping=True, symbol=None),
                val_indenizado_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_indenizado_prov'], 2),
                                                    grouping=True, symbol=None),
                val_saldo_prov=locale.currency(round(df_dados_proeventos_total_item.loc[index, 'val_saldo_prov'], 2),
                                               grouping=True, symbol=None),
                tipo_provisao=desc_tipo_proevento_pesq
            )
            dados_proeventos_itens.append(reg_prov_item.__dict__)

        dados_proeventos_colabs = []
        for index, row in df_dados_proeventos.iterrows():
            if df_dados_proeventos.loc[index, 'mat_fun'] != None:
                reg_prov = Registro_Provisao_Folha_Analitico_Colab(
                    periodo = str(df_dados_proeventos.loc[index, 'periodo']),
                    cod_emp = str(df_dados_proeventos.loc[index, 'cod_emp']),
                    nome_emp = str(df_dados_proeventos.loc[index, 'nome_emp']),
                    cod_filial = str(df_dados_proeventos.loc[index, 'cod_filial']),
                    nome_filial = str(df_dados_proeventos.loc[index, 'nome_filial']),
                    cod_ccu = str(df_dados_proeventos.loc[index, 'cod_ccu']),
                    desc_ccu = str(df_dados_proeventos.loc[index, 'desc_ccu']),
                    handle_proj = str(df_dados_proeventos.loc[index, 'handle_proj']),
                    mat_fun = str(df_dados_proeventos.loc[index, 'mat_fun']),
                    nome_fun=str(df_dados_proeventos.loc[index, 'nome_fun']),
                    cod_cargo = str(df_dados_proeventos.loc[index, 'cod_cargo']),
                    desc_cargo = str(df_dados_proeventos.loc[index, 'desc_cargo']),
                    data_adm = str(df_dados_proeventos.loc[index, 'data_adm']),
                    desc_prov = str(df_dados_proeventos.loc[index, 'desc_prov']),
                    val_base_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_base_prov'],2),
                                                    grouping=True, symbol=None),
                    perc_dias_prov = locale.currency(round(df_dados_proeventos.loc[index, 'perc_dias_prov'],2),
                                                     grouping=True, symbol=None),
                    val_anterior_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_anterior_prov']
                                                               ,2), grouping=True, symbol=None),
                    val_transf_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_transf_prov'],2),
                                                      grouping=True, symbol=None)                    ,
                    val_ajuste_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_ajuste_prov'],2),
                                                      grouping=True, symbol=None),
                    val_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_prov'],2),
                                               grouping=True, symbol=None),
                    val_pag_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_pag_prov'], 2),
                                                   grouping=True, symbol=None),
                    val_indenizado_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_indenizado_prov'],2),
                                                          grouping=True, symbol=None),
                    val_saldo_prov = locale.currency(round(df_dados_proeventos.loc[index, 'val_saldo_prov'],2),
                                                     grouping=True, symbol=None),
                    tipo_provisao = desc_tipo_proevento_pesq
                )
                dados_proeventos_colabs.append(reg_prov.__dict__)
        data = dict()
        data = {
            'msg': 'ok',
            'dados_proeventos_colabs' : dados_proeventos_colabs,
            'dados_proeventos_itens' : dados_proeventos_itens
        }
        return JsonResponse(data, safe=False)