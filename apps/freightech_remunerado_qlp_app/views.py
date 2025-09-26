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
    Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm, Registros_Plan_Remunerado_Freightech_Rota_Qlp_Equipe_Entrega
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



        obj_arquivo = Plan_Remunerada_Freightech(
            data_arq_imp = data_hora_atual,
            desc_layout_arq = tipo_planilha_frm,
            nome_arq_imp = plan_rem_frm,
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
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        cod_unidade_senior_frm = request.GET['nome_unidade_freigh'].split('_')[0]
        nome_unidade_freigh_frm = request.GET['nome_unidade_freigh'].split('_')[1]
        data_1_frm = request.GET['data_1'] + '-01'
        quinz_1_frm = request.GET['quinz_1']
        data_2_frm = request.GET['data_2'] + '-01'
        quinz_2_frm = request.GET['quinz_2']


        lista_obj_rem_adm = self.remunerado_adm(nome_unidade_freigh_frm, data_1_frm, quinz_1_frm, data_2_frm, quinz_2_frm)
        lista_obj_rem_op = self.remunerado_op(nome_unidade_freigh_frm, data_1_frm, quinz_1_frm, data_2_frm,
                                                quinz_2_frm)




        if len(lista_obj_rem_adm) == 0 and len(lista_obj_rem_op) == 0:
            msg = 'Não foram encontrados registros importados para essa vigência!'
        else:
            msg = 'Registros gerados'

        data = dict()
        data = {
            'lista_obj_rem_adm': lista_obj_rem_adm,
            'lista_obj_rem_op': lista_obj_rem_op,
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def compara_valores(self, x, y):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        campo = locale.currency(x, grouping=True, symbol=None)
        if x != y:
            campo = f"<span style='background:#FF0000;color:#ffffff'>{locale.currency(x, grouping=True, symbol=None)}</span>"
        return campo

    def remunerado_adm(self, nome_unidade_freigh_frm, data_1_frm, quinz_1_frm, data_2_frm, quinz_2_frm):
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
                                     cod_cargo_freightech=reg1.cod_cargo_freightech,
                                     )
                             .first())

                dic_rem_1 = {
                    'cod_qlp_rem_rota_adm': reg1.cod_qlp_rem_rota_adm,
                    'vigencia': datetime.strftime(reg1.vigencia, '%m-%Y'),
                    'quinzena': reg1.quinzena,
                    'desc_grupo': reg1.cod_cargo_freightech.grupo_cargo,
                    'desc_cargo': reg1.cod_cargo_freightech.desc_cargo,
                    'qtd_qlp': self.compara_valores(reg1.qtd_qlp_bench, obj_rem_2.qtd_qlp_bench),
                    'qtd_encargos': self.compara_valores(reg1.qtd_encargos, obj_rem_2.qtd_encargos),
                    'val_unit_encargos': self.compara_valores(reg1.val_unit_encargos, obj_rem_2.val_unit_encargos),
                    'qtd_ordenados': self.compara_valores(reg1.qtd_ordenados, obj_rem_2.qtd_ordenados),
                    'val_unit_ordenados': self.compara_valores(reg1.val_unit_ordenados, obj_rem_2.val_unit_ordenados),
                    'qtd_frota_leve': self.compara_valores(reg1.qtd_frota_leve, obj_rem_2.qtd_frota_leve),
                    'val_unit_frota_leve': self.compara_valores(reg1.val_unit_frota_leve,
                                                                obj_rem_2.val_unit_frota_leve),
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
                    'val_unit_frota_leve': self.compara_valores(obj_rem_2.val_unit_frota_leve,
                                                                reg1.val_unit_frota_leve),
                    'qtd_beneficios': self.compara_valores(obj_rem_2.qtd_beneficios, reg1.qtd_beneficios),
                    'val_unit_beneficio': self.compara_valores(obj_rem_2.val_unit_beneficio, reg1.val_unit_beneficio),
                    'qtd_telefonia': self.compara_valores(obj_rem_2.qtd_telefonia, reg1.qtd_telefonia),
                    'val_unit_telefonia': self.compara_valores(obj_rem_2.val_unit_telefonia, reg1.val_unit_telefonia),
                    'qtd_uniformes': self.compara_valores(obj_rem_2.qtd_uniformes, reg1.qtd_uniformes),
                    'val_unit_uniformes': self.compara_valores(obj_rem_2.val_unit_uniformes, reg1.val_unit_uniformes)
                }
                lista_obj_rem.append(dic_rem_2)

        return lista_obj_rem

    def remunerado_op(self, nome_unidade_freigh_frm, data_1_frm, quinz_1_frm, data_2_frm, quinz_2_frm):
        lista_obj_rem = []
        obj_rem_1 = (Registros_Plan_Remunerado_Freightech_Rota_Qlp_Equipe_Entrega.objects
                     .filter(nome_unidade=nome_unidade_freigh_frm,
                             vigencia=data_1_frm,
                             quinzena=quinz_1_frm))

        if len(obj_rem_1) > 0:
            for reg1 in obj_rem_1:
                obj_rem_2 = (Registros_Plan_Remunerado_Freightech_Rota_Qlp_Equipe_Entrega.objects
                             .filter(nome_unidade=nome_unidade_freigh_frm,
                                     vigencia=data_2_frm,
                                     quinzena=quinz_2_frm,
                                     cod_cargo_freightech=reg1.cod_cargo_freightech,
                                     turno= reg1.turno
                                     )
                             .first())

                dic_rem_1 = {
                    'cod_qlp_rem_rota_adm': reg1.cod_qlp_rem_rota_adm,
                    'vigencia': datetime.strftime(reg1.vigencia, '%m-%Y'),
                    'quinzena': reg1.quinzena,
                    'desc_grupo': reg1.cod_cargo_freightech.grupo_cargo,
                    'desc_cargo': reg1.cod_cargo_freightech.desc_cargo,
                    'turno': reg1.turno,
                    'qtd_qlp': self.compara_valores(
                        reg1.qtd_por_caminhao * reg1.qtd_total_por_caminhao_ativo,
                        obj_rem_2.qtd_por_caminhao * obj_rem_2.qtd_total_por_caminhao_ativo),
                    'dsr': self.compara_valores(reg1.qtd_dsr, obj_rem_2.qtd_dsr),
                    'hora_extra_fixa': self.compara_valores(reg1.hora_extra_fixa, obj_rem_2.hora_extra_fixa),
                    'perc_encargo_prov': self.compara_valores(reg1.perc_encargo_prov, obj_rem_2.perc_encargo_prov),
                    'perc_hora_extra': self.compara_valores(reg1.perc_hora_extra, obj_rem_2.perc_hora_extra),
                    'premiacao_plus': self.compara_valores(reg1.premiacao_plus, obj_rem_2.premiacao_plus),
                    'val_rem_fixa_contra_cheque': self.compara_valores(reg1.val_rem_fixa_contra_cheque, obj_rem_2.val_rem_fixa_contra_cheque),
                    'val_total_ordenado': self.compara_valores(reg1.val_total_ordenado, obj_rem_2.val_total_ordenado),
                    'val_total_remuneracao': self.compara_valores(reg1.val_total_remuneracao, obj_rem_2.val_total_remuneracao),
                    'val_total_remuneracao_com_beneficio': self.compara_valores(reg1.val_total_remuneracao_com_beneficio,
                                                                  obj_rem_2.val_total_remuneracao_com_beneficio)
                }
                lista_obj_rem.append(dic_rem_1)

                dic_rem_2 = {
                    'cod_qlp_rem_rota_adm': obj_rem_2.cod_qlp_rem_rota_adm,
                    'vigencia': datetime.strftime(obj_rem_2.vigencia, '%m-%Y'),
                    'quinzena': obj_rem_2.quinzena,
                    'desc_grupo': obj_rem_2.cod_cargo_freightech.grupo_cargo,
                    'desc_cargo': obj_rem_2.cod_cargo_freightech.desc_cargo,
                    'turno': obj_rem_2.turno,
                    'qtd_qlp': self.compara_valores(
                        obj_rem_2.qtd_por_caminhao * obj_rem_2.qtd_total_por_caminhao_ativo,
                        reg1.qtd_por_caminhao * reg1.qtd_total_por_caminhao_ativo),
                    'dsr': self.compara_valores(obj_rem_2.qtd_dsr, reg1.qtd_dsr),
                    'hora_extra_fixa': self.compara_valores(obj_rem_2.hora_extra_fixa, reg1.hora_extra_fixa),
                    'perc_encargo_prov': self.compara_valores(obj_rem_2.perc_encargo_prov, reg1.perc_encargo_prov),
                    'perc_hora_extra': self.compara_valores(obj_rem_2.perc_hora_extra, reg1.perc_hora_extra),
                    'premiacao_plus': self.compara_valores(obj_rem_2.premiacao_plus, reg1.premiacao_plus),
                    'val_rem_fixa_contra_cheque': self.compara_valores(obj_rem_2.val_rem_fixa_contra_cheque, reg1.val_rem_fixa_contra_cheque),
                    'val_total_ordenado': self.compara_valores(obj_rem_2.val_total_ordenado, reg1.val_total_ordenado),
                    'val_total_remuneracao': self.compara_valores(obj_rem_2.val_total_remuneracao, reg1.val_total_remuneracao),
                    'val_total_remuneracao_com_beneficio': self.compara_valores(obj_rem_2.val_total_remuneracao_com_beneficio,
                                                                                reg1.val_total_remuneracao_com_beneficio)
                }
                lista_obj_rem.append(dic_rem_2)

        return lista_obj_rem


