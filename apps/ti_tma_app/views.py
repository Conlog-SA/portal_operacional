from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime
from datetime import timedelta
import simplejson as json

from apps.calendario_app.models import Calendario_Dias
from apps.help_desk_app.views import ConexaoHelpDesk


class Form_Gera_Tma_TI_View(View):
    def get(self, request):
        return render(request, 'ti_tma_app/form_gera_tma_ti.html')

    def post(self, request):
        data_inicio_periodo = request.POST.get('data_inicio')
        data_fim_periodo = request.POST.get('data_fim')
        print(data_inicio_periodo)
        print(data_fim_periodo)

        dic_chamados_atendidos = ConexaoHelpDesk().retorna_chamados_atendidos(data_inicio_periodo, data_fim_periodo)
        for chamado in dic_chamados_atendidos:
            data_ini = datetime.strftime(chamado['data_abertura'], '%Y-%m-%d')
            data_fim = datetime.strftime(chamado['data_fechamento'], '%Y-%m-%d')

            data_ini = datetime.strptime(data_ini, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

            print(chamado['data_abertura'])
            print(chamado['data_fechamento'])
            data_prevista_sql = (Calendario_Dias.objects
                                 .filter(data_dia__range=[data_ini, data_fim], classificacao_dia='U'))

            SLA = timedelta()
            for data in data_prevista_sql:
                sla_dia = timedelta()
                inicio_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=27000)
                inicio_horario_almoco = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=43200)
                fim_horario_almoco = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=46800)
                fim_expediente = datetime.combine(data.data_dia, datetime.min.time()) + timedelta(seconds=63000)
                print(datetime.combine(data.data_dia, datetime.min.time()))
                print(data_ini)
                if data_ini == datetime.combine(data.data_dia, datetime.min.time()) and data_fim == datetime.combine(data.data_dia, datetime.min.time()):
                    if chamado['data_abertura'] > fim_horario_almoco or chamado['data_fechamento'] < inicio_horario_almoco:
                        sla_dia += chamado['data_fechamento'] - chamado['data_abertura']
                    else:
                        sla_dia += (inicio_horario_almoco - chamado['data_abertura']) + (chamado['data_fechamento'] - fim_horario_almoco)
                elif data_ini == datetime.combine(data.data_dia, datetime.min.time()):
                    if chamado['data_abertura'] > fim_horario_almoco:
                        sla_dia += fim_expediente - chamado['data_abertura']
                        print('entrou data ini >')
                    elif chamado['data_abertura'] < inicio_horario_almoco:
                        print('entrou data ini <')
                        sla_dia += (fim_expediente - fim_horario_almoco) + (inicio_horario_almoco - chamado['data_abertura'])
                elif data_fim == datetime.combine(data.data_dia, datetime.min.time()):
                    if chamado['data_fechamento'] > fim_horario_almoco:
                        print('entrou data fim >')
                        sla_dia += (inicio_horario_almoco - inicio_expediente) + (chamado['data_fechamento'] - fim_horario_almoco)
                    elif chamado['data_fechamento'] < inicio_horario_almoco:
                        print('entrou data fim <')
                        sla_dia += (chamado['data_fechamento'] - inicio_expediente)
                else:
                    sla_dia += (inicio_horario_almoco - inicio_expediente) + (fim_expediente - fim_horario_almoco)
                    #print('entrou else')
            SLA += sla_dia
            print(SLA)
        data = {
            'dic_chamados_atendidos': dic_chamados_atendidos
        }
        return JsonResponse(data, safe=False)
