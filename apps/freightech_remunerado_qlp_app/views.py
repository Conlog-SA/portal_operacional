import calendar
from datetime import datetime
import locale

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.calendario_app.models import Calendario_Dias
from apps.conecta_senior_app.views import Conexao_Senior_BD
from apps.freightech_remunerado_qlp_app.importador_plan_freitech import Importador_Plan_Freightech
from apps.freightech_remunerado_qlp_app.models import Plan_Remunerada_Freightech, \
    Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm
from apps.usuario_app.models import Usuario


# Create your views here.

class Frm_Importa_Plan_Remunerado_Freightech_View(View):
    def get(self, request):
        return render(request, 'freightech_remunerado_qlp_app/frm_importa_plan_freightech.html')

    def post(self, request):
        plan_rem_frm = request.FILES['file']
        tipo_planilha_frm = request.POST['tipo_planilha']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu_logado = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')

        caminho_arq_importado = 'docs/plan_rem_freightech/'  + str(plan_rem_frm.name).replace('.xlsx', '') + '_' + \
                                obj_usu_logado.login_usu.replace('.', '_') + '_' + str(data_atual_dd_mm_yyyy).replace('/', '_') \
                                + '_' + str(hota_atual).replace(':', '_') + '.xlsx'

        obj_arquivo = Plan_Remunerada_Freightech(
            data_arq_imp = data_hora_atual,
            desc_layout_arq = tipo_planilha_frm,
            nome_arq_original = plan_rem_frm.name,
            nome_arq_imp = caminho_arq_importado,
            cod_usu = obj_usu_logado
        )
        obj_arquivo.save()
        obj_importador = Importador_Plan_Freightech(plan_rem_frm, tipo_planilha_frm, obj_arquivo)




        data = dict()
        data = {
            'msg': 'Importação realizada com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Frm_Pesq_Dados_Comparacao_Quinzenas_View(View):
    def get(self, request):
        cod_unidade_senior_frm = request.GET['nome_unidade_freigh'].split('_')[0]
        nome_unidade_freigh_frm = request.GET['nome_unidade_freigh'].split('_')[1]
        data_1_frm = request.GET['data_1'] + '-01'
        quinz_1_frm = request.GET['quinz_1']
        data_2_frm = request.GET['data_2'] + '-01'
        quinz_2_frm = request.GET['quinz_2']
        lista_obj_rem = []
        obj_rem_1 = (Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm.objects
                     .filter(nome_unidade=nome_unidade_freigh_frm,
                             vigencia=data_1_frm,
                             quinzena=quinz_1_frm))


        if len(obj_rem_1) > 0:
            for reg1 in obj_rem_1:
                obj_rem_2 = (Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm.objects
                             .filter(nome_unidade=nome_unidade_freigh_frm,
                                     vigencia=data_2_frm,
                                     quinzena=quinz_2_frm,
                                     cod_cargo_freightech=reg1.cod_cargo_freightech)
                             .first())

                dic_rem_1 = {
                    'cod_qlp_rem_rota_adm': reg1.cod_qlp_rem_rota_adm ,
                    'vigencia': datetime.strftime(reg1.vigencia, '%m-%Y'),
                    'quinzena': reg1.quinzena,
                    'desc_grupo': reg1.cod_cargo_freightech.grupo_cargo,
                    'desc_cargo': reg1.cod_cargo_freightech.desc_cargo,
                    'qtd_qlp':  self.compara_valores(reg1.qtd_qlp_bench, obj_rem_2.qtd_qlp_bench),
                    'qtd_encargos': self.compara_valores(reg1.qtd_encargos, obj_rem_2.qtd_encargos),
                    'val_unit_encargos': self.compara_valores(reg1.val_unit_encargos, obj_rem_2.val_unit_encargos),
                    'qtd_ordenados': self.compara_valores(reg1.qtd_ordenados, obj_rem_2.qtd_ordenados),
                    'val_unit_ordenados': self.compara_valores(reg1.val_unit_ordenados, obj_rem_2.val_unit_ordenados),
                    'qtd_frota_leve': self.compara_valores(reg1.qtd_frota_leve, obj_rem_2.qtd_frota_leve),
                    'val_unit_frota_leve': self.compara_valores(reg1.val_unit_frota_leve, obj_rem_2.val_unit_frota_leve),
                    'qtd_beneficios': self.compara_valores(reg1.qtd_beneficios, obj_rem_2.qtd_beneficios),
                    'val_unit_beneficio': self.compara_valores(reg1.val_unit_beneficio, obj_rem_2.val_unit_beneficio),
                    'qtd_telefonia': self.compara_valores(reg1.qtd_telefonia, obj_rem_2.qtd_telefonia),
                    'val_unit_telefonia': self.compara_valores(reg1.val_unit_telefonia, obj_rem_2.val_unit_telefonia),
                    'qtd_uniformes': self.compara_valores(reg1.qtd_uniformes, obj_rem_2.qtd_uniformes),
                    'val_unit_uniformes': self.compara_valores(reg1.val_unit_uniformes, obj_rem_2.val_unit_uniformes)
                }
                lista_obj_rem.append(dic_rem_1)

                dic_rem_2 = {
                    'cod_qlp_rem_rota_adm': obj_rem_2.cod_qlp_rem_rota_adm,
                    'vigencia': datetime.strftime(obj_rem_2.vigencia, '%m-%Y'),
                    'quinzena': obj_rem_2.quinzena,
                    'desc_grupo': obj_rem_2.cod_cargo_freightech.grupo_cargo,
                    'desc_cargo': obj_rem_2.cod_cargo_freightech.desc_cargo,
                    'qtd_qlp': self.compara_valores(obj_rem_2.qtd_qlp_bench, reg1.qtd_qlp_bench),
                    'qtd_encargos': self.compara_valores(obj_rem_2.qtd_encargos, reg1.qtd_encargos),
                    'val_unit_encargos': self.compara_valores(obj_rem_2.val_unit_encargos, reg1.val_unit_encargos),
                    'qtd_ordenados': self.compara_valores(obj_rem_2.qtd_ordenados, reg1.qtd_ordenados),
                    'val_unit_ordenados': self.compara_valores(obj_rem_2.val_unit_ordenados, reg1.val_unit_ordenados),
                    'qtd_frota_leve': self.compara_valores(obj_rem_2.qtd_frota_leve, reg1.qtd_frota_leve),
                    'val_unit_frota_leve': self.compara_valores(obj_rem_2.val_unit_frota_leve, reg1.val_unit_frota_leve) ,
                    'qtd_beneficios': self.compara_valores(obj_rem_2.qtd_beneficios, reg1.qtd_beneficios),
                    'val_unit_beneficio': self.compara_valores(obj_rem_2.val_unit_beneficio, reg1.val_unit_beneficio),
                    'qtd_telefonia': self.compara_valores(obj_rem_2.qtd_telefonia, reg1.qtd_telefonia),
                    'val_unit_telefonia': self.compara_valores(obj_rem_2.val_unit_telefonia, reg1.val_unit_telefonia),
                    'qtd_uniformes': self.compara_valores(obj_rem_2.qtd_uniformes, reg1.qtd_uniformes),
                    'val_unit_uniformes': self.compara_valores(obj_rem_2.val_unit_uniformes, reg1.val_unit_uniformes)
                }
                lista_obj_rem.append(dic_rem_2)

        '''Ordenados'''
        con_ordenados_1 = Conexao_Senior_BD(12)
        data_ref_1 = data_1_frm + '-01'
        df_ordenados_cargo_1 = con_ordenados_1.retorna_df_ordenados_por_periodo_e_filial(data_1_frm,cod_unidade_senior_frm)
        df_ordenados_cargo_1['vigencia'] = data_1_frm
        df_ordenados_cargo_1['quinz'] = quinz_1_frm

        con_ordenados_2 = Conexao_Senior_BD(12)
        data_ref_2 = data_2_frm + '-01'
        df_ordenados_cargo_2 = con_ordenados_2.retorna_df_ordenados_por_periodo_e_filial(data_2_frm,cod_unidade_senior_frm)
        df_ordenados_cargo_2['vigencia'] = data_2_frm
        df_ordenados_cargo_2['quinz'] = quinz_2_frm
        df_ordenados_cargo = pd.concat([df_ordenados_cargo_1, df_ordenados_cargo_2]).reset_index()
        df_ordenados_cargo_fil = df_ordenados_cargo.groupby(
            ['vigencia', 'quinz', 'cod_filial', 'cod_cargo'])[
            ['val_evento']].sum().reset_index()
        df_ordenados_cargo_proj = df_ordenados_cargo.groupby(
            ['vigencia', 'quinz', 'cod_filial', 'cod_ccu_colab', 'cod_cargo' ])[
            ['val_evento']].sum().reset_index()

        '''QLP Senior'''
        '''Seleciona data 1'''
        data_1 = None
        if quinz_1_frm == '1':
            data_1 = (Calendario_Dias.objects
                      .filter(data_dia__year=data_1_frm.split('-')[0],
                                                    data_dia__month=data_1_frm.split('-')[1], data_dia__day__range=[1,15])
                      .order_by('-data_dia').first())

        else:
            ano = int(data_1_frm.split('-')[0])
            mes = int(data_1_frm.split('-')[1])
            _, ultimo_dia_mes = calendar.monthrange(ano, mes)
            data_1 = (Calendario_Dias.objects
                      .filter(data_dia__year=data_1_frm.split('-')[0],
                              data_dia__month=data_1_frm.split('-')[1], data_dia__day__range=[16, ultimo_dia_mes])
                      .order_by('-data_dia').first())


        con_senior_1 = Conexao_Senior_BD(12)
        df_qlp_senior_1 = con_senior_1.retorna_qlp_por_periodo_e_filial(data_1.data_dia, cod_unidade_senior_frm)
        df_qlp_senior_1['quinz'] = quinz_1_frm
        df_qlp_senior_1['vigencia'] = data_1_frm
        df_qtd_qlp_cargo_1 = df_qlp_senior_1.groupby(['data_qlp', 'vigencia', 'quinz', 'cod_filial', 'nome_filial', 'cod_ccu_colab', 'nome_ccu_colab', 'cod_cargo', 'nome_cargo_colab', 'desc_cargo_freightech'])[['matricula_colab']].count().reset_index()

        #print(df_qtd_qlp_cargo_1)


        '''Seleciona data 2,'''
        data_2 = None
        if quinz_2_frm == '1':
            data_2 = (Calendario_Dias.objects
                      .filter(data_dia__year=data_2_frm.split('-')[0],
                              data_dia__month=data_2_frm.split('-')[1], data_dia__day__range=[1, 15])
                      .order_by('-data_dia').first())

        else:
            ano = int(data_2_frm.split('-')[0])
            mes = int(data_2_frm.split('-')[1])
            _, ultimo_dia_mes = calendar.monthrange(ano, mes)
            data_2 = (Calendario_Dias.objects
                      .filter(data_dia__year=data_2_frm.split('-')[0],
                              data_dia__month=data_2_frm.split('-')[1], data_dia__day__range=[16, ultimo_dia_mes])
                      .order_by('-data_dia').first())

        con_senior_2 = Conexao_Senior_BD(12)
        df_qlp_senior_2 = con_senior_2.retorna_qlp_por_periodo_e_filial(data_2.data_dia, cod_unidade_senior_frm)
        df_qlp_senior_2['quinz'] = quinz_2_frm
        df_qlp_senior_2['vigencia'] = data_2_frm
        df_qtd_qlp_cargo_2 = df_qlp_senior_2.groupby(['data_qlp', 'vigencia', 'quinz','cod_filial', 'nome_filial', 'cod_ccu_colab', 'nome_ccu_colab', 'cod_cargo', 'nome_cargo_colab', 'desc_cargo_freightech'])[
            ['matricula_colab']].count().reset_index()


        df_qlp_total = pd.concat([df_qtd_qlp_cargo_1, df_qtd_qlp_cargo_2]).reset_index()
        df_qlp_total = pd.merge(df_qlp_total, df_ordenados_cargo_proj,
                                how='left',
                                on=['vigencia', 'quinz', 'cod_filial', 'cod_ccu_colab', 'cod_cargo'] )
        lista_qlp = []
        for index, row in df_qlp_total.iterrows():
            reg = {
                'quinz': df_qlp_total.loc[index, 'quinz'],
                'periodo': df_qlp_total.loc[index, 'data_qlp'],
                'nome_filial': df_qlp_total.loc[index, 'nome_filial'],
                'desc_proj': df_qlp_total.loc[index, 'nome_ccu_colab'],
                'desc_cargo_senior': df_qlp_total.loc[index, 'nome_cargo_colab'],
                'desc_cargo_freightech': df_qlp_total.loc[index, 'desc_cargo_freightech'],
                'qlp': int(df_qlp_total.loc[index, 'matricula_colab']),
                'val_ordenados': float(df_qlp_total.loc[index, 'val_evento'])
            }
            lista_qlp.append(reg)

        lista_qlp_filial = []
        df_qlp_filial = df_qlp_total.groupby(['data_qlp', 'vigencia', 'quinz','cod_filial', 'nome_filial', 'cod_cargo', 'nome_cargo_colab', 'desc_cargo_freightech'])[
            ['matricula_colab']].sum().reset_index()
        df_qlp_filial = pd.merge(df_qlp_filial, df_ordenados_cargo_fil,
                                how='left',
                                on=['vigencia', 'quinz', 'cod_filial', 'cod_cargo'])
        for index, row in df_qlp_filial.iterrows():
            reg = {
                'quinz': df_qlp_filial.loc[index, 'quinz'],
                'periodo': df_qlp_filial.loc[index, 'data_qlp'],
                'nome_filial': df_qlp_filial.loc[index, 'nome_filial'],
                'desc_cargo_senior': df_qlp_filial.loc[index, 'nome_cargo_colab'],
                'desc_cargo_freightech': df_qlp_filial.loc[index, 'desc_cargo_freightech'],
                'qlp': int(df_qlp_filial.loc[index, 'matricula_colab']),
                'val_ordenados': float(df_qlp_filial.loc[index, 'val_evento'])
            }
            lista_qlp_filial.append(reg)






        if len(lista_obj_rem) == 0:
            msg = 'Não foram encontrados registros importados para essa vigência!'
        else:
            msg = 'Registros gerados'

        data = dict()
        data = {
            'lista_qlp': lista_qlp,
            'lista_qlp_filial': lista_qlp_filial,
            'lista_obj_rem': lista_obj_rem,
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def compara_valores(self, x, y):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        campo = locale.currency(x, grouping=True, symbol=None)
        if x != y:
            campo = f"<span style='background:#FF0000;color:#ffffff'>{locale.currency(x, grouping=True, symbol=None)}</span>"
        return campo




