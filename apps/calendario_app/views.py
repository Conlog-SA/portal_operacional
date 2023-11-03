import calendar
from datetime import timedelta

from django.shortcuts import render

from apps.calendario_app.models import Calendario, Calendario_Dias


def gera_datas_previstas_requisicoes_frota():
    # lista_dias_calendario = Dia_Calendario.objects.all()
    print('Aguarde Metodo gera_datas_previstas_requisicoes_frota() rodando ... ')
    lista_dias_calendario = Calendario_Dias.objects.filter(data_dia__gt='2023-10-15')
    for dia in lista_dias_calendario:
        '''obj_dia_data_prev_e = Calendario_Dias.objects.filter(cod_calendario_dia__gt=dia.cod_calendario_dia,
                                                          classificacao_dia='U').order_by('cod_calendario_dia')[1]

        dia.data_prevista_req_e = obj_dia_data_prev_e.data_dia       
        
        obj_dia_data_prev_ne = Calendario_Dias.objects.filter(cod_calendario_dia__gt=dia.cod_calendario_dia,
                                                             classificacao_dia='U').order_by('cod_calendario_dia')[4]

        dia.data_prevista_req_ne = obj_dia_data_prev_ne.data_dia
        '''
        #Informar sempre a qtd de dias menos 1
        obj_dia_data_prev_plan = Calendario_Dias.objects.filter(cod_calendario_dia__gt=dia.cod_calendario_dia,
                                                               classificacao_dia='U').order_by('cod_calendario_dia')[9]
        dia.data_prevista_req_plan = obj_dia_data_prev_plan.data_dia

        dia.save()
    print('Fim')


def conta_qtd_semanas_mes():
    lista_dias_calendario = Calendario.objects.all().order_by('data_dia')
    mes_ref = ''
    # data_ini_semana = ''
    num_semana_mes_ref = 0

    for reg in lista_dias_calendario:
        if reg.dia_semana == 1:
            if int(reg.data_dia.month) == mes_ref:
                num_semana_mes_ref += 1
                reg.num_semana = num_semana_mes_ref
                reg.mes_ref_num_semana = mes_ref
            else:
                num_semana_mes_ref = 1
                mes_ref = int(reg.data_dia.month)
                reg.num_semana = num_semana_mes_ref
                reg.mes_ref_num_semana = mes_ref

        else:  # reg.dia_semana > 1 and reg.dia_semana < 8:
            reg.num_semana = num_semana_mes_ref
            reg.mes_ref_num_semana = mes_ref

        print(
            'Data: ' + str(reg.data_dia) + ' Num. dia da semana: ' + str(reg.dia_semana) + ' Mês ref: ' + str(mes_ref))
        reg.save(update_fields=['num_semana', 'mes_ref_num_semana'])








