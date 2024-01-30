from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime
from datetime import timedelta

from apps.calendario_app.models import Calendario_Dias
from apps.help_desk_app.views import ConexaoHelpDesk
from apps.ti_tma_app.models import Chamado_Atendido_TMA


class Form_Gera_Tma_TI_View(View):
    def get(self, request):
        return render(request, 'ti_tma_app/form_gera_tma_ti.html')

    def post(self, request):
        lista_chamados_retorno = []
        data_inicio_periodo = request.POST.get('data_inicio')
        #data_fim_periodo = datetime.strptime(request.POST.get('data_fim'), '%Y-%m-%d') + timedelta(days=1)
        #data_fim_periodo = datetime.strftime(data_fim_periodo, '%Y-%m-%d')
        data_fim_periodo = request.POST.get('data_fim')

        dic_chamados_atendidos = ConexaoHelpDesk().retorna_chamados_atendidos(data_inicio_periodo, data_fim_periodo)
        for chamado in dic_chamados_atendidos:
            #print('começou o chamado: ' + str(chamado['num_chamado']))
            tempo_atendimento = timedelta()
            sla = chamado['sla_hora']
            data_ini_chamado = datetime.strftime(chamado['data_abertura'] - timedelta(hours=3), '%Y-%m-%d')
            data_fim_chamado = datetime.strftime(chamado['data_fechamento'] - timedelta(hours=3), '%Y-%m-%d')
            data_ini_chamado = datetime.strptime(data_ini_chamado, '%Y-%m-%d')
            data_fim_chamado = datetime.strptime(data_fim_chamado, '%Y-%m-%d')

            data_inicio_fim_chamado = {'data_ini': data_ini_chamado,
                               'data_fim': data_fim_chamado}
            data_hora_inicio_fim_chamado = {'data_hora_ini': chamado['data_abertura'] - timedelta(hours=3),
                                    'data_hora_fim': chamado['data_fechamento'] - timedelta(hours=3)}

            if chamado['status_ch_espera'] == 'N':
                tempo_atendimento = calcula_tempo_util(data_inicio_fim_chamado, data_hora_inicio_fim_chamado)

            elif chamado['status_ch_espera'] == 'S':
                tempo_atendimento = calcula_tempo_util(data_inicio_fim_chamado, data_hora_inicio_fim_chamado)
                dic_status_chamado = ConexaoHelpDesk().retorna_status_chamado(chamado['num_chamado'])
                flag_espera = 0
                armazena_data = None
                for status in dic_status_chamado:
                    if status['id_status'] == 4:
                        flag_espera = 1
                        armazena_data = status['data_status']
                    elif flag_espera == 1:
                        data_ini_status = datetime.strftime(armazena_data - timedelta(hours=3), '%Y-%m-%d')
                        data_fim_status = datetime.strftime(status['data_status'] - timedelta(hours=3), '%Y-%m-%d')
                        data_ini_status = datetime.strptime(data_ini_status, '%Y-%m-%d')
                        data_fim_status = datetime.strptime(data_fim_status, '%Y-%m-%d')
                        data_inicio_fim_status = {'data_ini': data_ini_status,
                                                   'data_fim': data_fim_status}
                        data_hora_inicio_fim_status = {'data_hora_ini': armazena_data - timedelta(hours=3),
                                                        'data_hora_fim': status['data_status'] - timedelta(hours=3)}
                        tempo_atendimento = tempo_atendimento - calcula_tempo_util(data_inicio_fim_status, data_hora_inicio_fim_status)
                        flag_espera = 0
                        armazena_data = None

            atendente = ConexaoHelpDesk().retorna_atendente(chamado['num_chamado'])
            data_sla = calcula_data_sla(data_hora_inicio_fim_chamado['data_hora_ini'], sla)
            #print('data do sla estimado: ' + str(data_sla))
            tempo_atendimento = int(tempo_atendimento.total_seconds() / 3600)
            if (tempo_atendimento > chamado['sla_hora']):
                status = 'style="color: #fa0000"'
            else:
                status = 'style="color: #63E6BE"'


            lista_chamados_retorno.append({'chamado' : chamado['num_chamado'],
                                           'usuario' : chamado['login_usuario'],
                                           'topico' : chamado['desc_topico'],
                                           'subtopico' : chamado['desc_subtopico'],
                                           'dt_abertura' : (chamado['data_abertura'] - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M"),
                                           'dt_fechamento' : (chamado['data_fechamento'] - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M"),
                                           'data_sla' : data_sla.strftime("%d/%m/%Y %H:%M"),
                                           'horas_atendimento' : tempo_atendimento,
                                           'sla' : chamado['sla_hora'],
                                           'status' : status,
                                           'atendente' : atendente})
            chamado_atendido = Chamado_Atendido_TMA.objects.filter(pk=chamado['num_chamado']).first()
            if chamado_atendido == None:
                obj_cham_atendido = Chamado_Atendido_TMA(
                    num_chamado=chamado['num_chamado'],
                    nome_usu=chamado['login_usuario'],
                    desc_topico=chamado['desc_topico'],
                    desc_sub_topico=chamado['desc_subtopico'],
                    aberto_em=chamado['data_abertura'] - timedelta(hours=3),
                    fechado_em=chamado['data_fechamento'] - timedelta(hours=3),
                    sla=chamado['sla_hora'],
                    data_sla=data_sla,
                    login_atendente=atendente,
                    horas_atendimento=tempo_atendimento
                )
                obj_cham_atendido.save()

        data = {
            'lista_chamados_retorno': lista_chamados_retorno
        }

        return JsonResponse(data, safe=False)

def calcula_tempo_util(data_inicio_fim, data_hora_inicio_fim):
    data_ini = data_inicio_fim['data_ini']
    data_fim = data_inicio_fim['data_fim']
    data_hora_ini = data_hora_inicio_fim['data_hora_ini']
    data_hora_fim = data_hora_inicio_fim['data_hora_fim']
    #print(data_hora_ini)
    #print(data_hora_fim)

    data_prevista_sql = (Calendario_Dias.objects
                         .filter(data_dia__range=[data_ini, data_fim], classificacao_dia='U'))
    tempo_util = timedelta()
    for data in data_prevista_sql:
        inicio_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=27000)
        inicio_horario_almoco = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=43200)
        fim_horario_almoco = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=46800)
        if data.dia_semana != 6:
            fim_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=63000)
        if data.dia_semana == 6:
            fim_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=59400)

        if data_ini == datetime.combine(data.data_dia, datetime.min.time()) and data_fim == datetime.combine(
                data.data_dia, datetime.min.time()):
            if data_hora_ini < inicio_expediente:
                data_hora_ini = inicio_expediente
            elif data_hora_ini > fim_expediente:
                data_hora_ini = fim_expediente
            elif data_hora_ini >= inicio_horario_almoco and data_hora_ini < fim_horario_almoco:
                data_hora_ini = fim_horario_almoco

            if data_hora_fim < inicio_expediente:
                data_hora_fim = inicio_expediente
            elif data_hora_fim > fim_expediente:
                data_hora_fim = fim_expediente
            elif data_hora_fim >= inicio_horario_almoco and data_hora_fim < fim_horario_almoco:
                data_hora_fim = fim_horario_almoco

            if data_hora_ini >= fim_horario_almoco or data_hora_fim <= inicio_horario_almoco:
                tempo_util += data_hora_fim - data_hora_ini
            else:
                tempo_util += (inicio_horario_almoco - data_hora_ini) + (data_hora_fim - fim_horario_almoco)
        elif data_ini == datetime.combine(data.data_dia, datetime.min.time()):
            if data_hora_ini < inicio_expediente:
                data_hora_ini = inicio_expediente
            elif data_hora_ini > fim_expediente:
                data_hora_ini = fim_expediente
            elif data_hora_ini >= inicio_horario_almoco and data_hora_ini < fim_horario_almoco:
                data_hora_ini = fim_horario_almoco

            if data_hora_ini >= fim_horario_almoco:
                tempo_util += fim_expediente - data_hora_ini
            elif data_hora_ini < inicio_horario_almoco:
                tempo_util += (fim_expediente - fim_horario_almoco) + (inicio_horario_almoco - data_hora_ini)

        elif data_fim == datetime.combine(data.data_dia, datetime.min.time()):
            if data_hora_fim < inicio_expediente:
                data_hora_fim = inicio_expediente
            elif data_hora_fim > fim_expediente:
                data_hora_fim = fim_expediente
            elif data_hora_fim >= inicio_horario_almoco and data_hora_fim < fim_horario_almoco:
                data_hora_fim = inicio_horario_almoco

            if data_hora_fim >= fim_horario_almoco:
                tempo_util += (inicio_horario_almoco - inicio_expediente) + (data_hora_fim - fim_horario_almoco)
            elif data_hora_fim <= inicio_horario_almoco:
                tempo_util += (data_hora_fim - inicio_expediente)

        else:
            tempo_util += (inicio_horario_almoco - inicio_expediente) + (fim_expediente - fim_horario_almoco)
            # print('entrou else')
    return tempo_util

def calcula_data_sla(data_hora_inicio, sla):
    data_ini = datetime.strftime(data_hora_inicio, '%Y-%m-%d')
    data_final_periodo = datetime.strftime(data_hora_inicio + timedelta(days=48), '%Y-%m-%d')
    data_ini = datetime.strptime(data_ini, '%Y-%m-%d')
    data_final_periodo = datetime.strptime(data_final_periodo, '%Y-%m-%d')

    data_prevista_sql = (Calendario_Dias.objects
                         .filter(data_dia__range=[data_ini, data_final_periodo], classificacao_dia='U'))
    flag_primeiro_dia = True

    for data in data_prevista_sql:
        if data.dia_semana == 6:
            horas_uteis = 8
            segundos_fim_expediente = 59400
        if data.dia_semana != 6:
            horas_uteis = 9
            segundos_fim_expediente = 63000

        if flag_primeiro_dia == False:
            if sla > horas_uteis:
                sla = sla - horas_uteis
            elif sla <= horas_uteis:
                inicio_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=27000)
                if sla > 4:
                    return (inicio_expediente + timedelta(hours=1)) + timedelta(hours=sla)
                else:
                    return inicio_expediente + timedelta(hours=sla)
        elif flag_primeiro_dia == True:
            inicio_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=27000)
            inicio_horario_almoco = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=43200)
            fim_horario_almoco = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=46800)
            fim_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=segundos_fim_expediente)

            if data_hora_inicio < inicio_expediente:
                data_hora_inicio = inicio_expediente
            elif data_hora_inicio > fim_expediente:
                data_hora_inicio = fim_expediente
            elif data_hora_inicio >= inicio_horario_almoco and data_hora_inicio < fim_horario_almoco:
                data_hora_inicio = fim_horario_almoco

            if data_hora_inicio < inicio_horario_almoco:
                if sla > ((fim_expediente - timedelta(hours=1) - data_hora_inicio)).total_seconds()/3600:
                    sla = sla - ((fim_expediente - timedelta(hours=1)) - data_hora_inicio).total_seconds()/3600
                    flag_primeiro_dia = False
                else:
                    return data_hora_inicio + timedelta(hours=sla-1)
            if data_hora_inicio >= fim_horario_almoco:
                if sla > (fim_expediente - data_hora_inicio).total_seconds()/3600:
                    sla = sla - (fim_expediente - data_hora_inicio).total_seconds()/3600
                    flag_primeiro_dia = False
                else:
                    return data_hora_inicio + timedelta(hours=sla)