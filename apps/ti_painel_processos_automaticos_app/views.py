from django.shortcuts import render
from django.views import View
from apps.usuario_app.models import Usuario
from apps.ti_painel_processos_automaticos_app.models import Processo, Execucao_Processo
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta


class Frm_Painel_Processos_Automaticos_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)


        data_atual = datetime.now(timezone.utc) - timedelta(hours=3)

        lista_dic_proc_pri_0 = []
        lista_obj_proc_pri_0 = Processo.objects.filter(eh_ativo=1, cod_prioridade=0)
        contador = 0
        col = 0
        lista_col = []
        for proc in lista_obj_proc_pri_0:
            if contador % 3 == 0:
                col += 1
                lista_col.append(col)
            ultima_exec = (Execucao_Processo
                           .objects
                           .filter(cod_processo=proc)
                           .order_by('cod_exec_processo').last())

            data_ultima_exe = ''
            data_proxima_exe = ''
            hora_prox_exe = ''
            cor_status_ult_exec = '#FFFFFF';
            cor_status_prox_exec = '#FFFFFF';
            cod_status = 0
            if ultima_exec != None:
                data_ultima_exe = datetime.strftime(ultima_exec.data_status_exec, '%d-%m %H:%M')
                cod_status = ultima_exec.cod_status_exec_processo.cod_status_exec_processo
                data_prox_exe_completa = None
                if proc.periodicidade == 'S':
                    data_prox_exe_completa = ultima_exec.data_status_exec + timedelta(hours=168)
                elif proc.periodicidade == 'D':
                    data_prox_exe_completa = ultima_exec.data_status_exec + timedelta(hours=24)
                elif proc.periodicidade == 'H':
                    data_prox_exe_completa = ultima_exec.data_status_exec + timedelta(minutes=int(proc.frequencia))
                elif proc.periodicidade == 'M':
                    data_prox_exe_completa = ultima_exec.data_status_exec + relativedelta(months=1)

                '''Define cor da última execucao'''
                if ultima_exec.cod_status_exec_processo.cod_status_exec_processo == 4:
                    cor_status_ult_exec = '#FF0000'
                elif ultima_exec.cod_status_exec_processo.cod_status_exec_processo == 2:
                    cor_status_ult_exec = '#FFFF00'
                elif ultima_exec.cod_status_exec_processo.cod_status_exec_processo == 3:
                    cor_status_ult_exec = '#00FA9A'

                '''Define cor da próxima execução'''
                # data_prox_exec_compare = datetime.strptime(data_prox_exe_completa, '%d-%m-%Y %H:%M')
                if data_prox_exe_completa != None:
                    data_prox_exec_compare = data_prox_exe_completa.astimezone(timezone.utc)
                    data_proxima_exe = datetime.strftime(data_prox_exe_completa, '%d-%m %H:%M')
                if data_prox_exec_compare > data_atual:
                    cor_status_prox_exec = '#00FA9A'
                else:
                    cod_status = 5
                    cor_status_prox_exec = '#FF0000'



                dic_proc_info = {
                    'nome_proc': proc.desc_processo,
                    'data_ult_exec': data_ultima_exe,
                    'data_prox_exec': data_proxima_exe,
                    'cod_status': cod_status,
                    'col': col,
                    'cor_status_ult_exec': cor_status_ult_exec,
                    'cor_status_prox_exec': cor_status_prox_exec
                }
                lista_dic_proc_pri_0.append(dic_proc_info)
                contador += 1


        lista_dic_proc_pri_1 = []
        lista_obj_proc_pri_1 = Processo.objects.filter(eh_ativo=1, cod_prioridade=1)
        contador = 0
        col = 0
        lista_col = []
        for proc in lista_obj_proc_pri_1:
            if contador % 3 == 0:
                col += 1
                lista_col.append(col)
            ultima_exec = Execucao_Processo.objects.filter(cod_processo=proc).order_by('cod_exec_processo').last()

            data_ultima_exe = ''
            data_proxima_exe = ''
            hora_prox_exe = ''
            cor_status_ult_exec = '#FFFFFF';
            cor_status_prox_exec = '#FFFFFF';
            cod_status = 0
            if ultima_exec != None:
                data_ultima_exe = datetime.strftime(ultima_exec.data_status_exec, '%d-%m %H:%M')
                cod_status = ultima_exec.cod_status_exec_processo.cod_status_exec_processo
                data_prox_exe_completa = None
                if proc.periodicidade == 'S':
                    data_prox_exe_completa = ultima_exec.data_status_exec + timedelta(hours=168)
                elif proc.periodicidade == 'D':
                    data_prox_exe_completa = ultima_exec.data_status_exec + timedelta(hours=24)
                elif proc.periodicidade == 'H':
                    data_prox_exe_completa = ultima_exec.data_status_exec + timedelta(minutes=int(proc.frequencia))
                elif proc.periodicidade == 'M':
                    data_prox_exe_completa = ultima_exec.data_status_exec + relativedelta(months=1)

                '''Define cor da última execucao'''
                if ultima_exec.cod_status_exec_processo.cod_status_exec_processo == 4:
                    cor_status_ult_exec = '#FF0000'
                elif ultima_exec.cod_status_exec_processo.cod_status_exec_processo == 2:
                    cor_status_ult_exec = '#FFFF00'
                elif ultima_exec.cod_status_exec_processo.cod_status_exec_processo == 3:
                    cor_status_ult_exec = '#00FA9A'

                '''Define cor da próxima execução'''
                #data_prox_exec_compare = datetime.strptime(data_prox_exe_completa, '%d-%m-%Y %H:%M')
                data_prox_exec_compare = data_prox_exe_completa.astimezone(timezone.utc)
                if data_prox_exec_compare > data_atual:
                    cor_status_prox_exec = '#00FA9A'
                else:
                    cod_status = 5
                    cor_status_prox_exec = '#FF0000'

                data_proxima_exe = datetime.strftime(data_prox_exe_completa, '%d-%m')
                hora_prox_exe = datetime.strftime(data_prox_exe_completa, '%H:%M')
            dic_proc_info = {
                'nome_proc': proc.desc_processo,
                'data_ult_exec': data_ultima_exe,
                'data_prox_exec': data_proxima_exe,
                'hora_prox_exec': hora_prox_exe,
                'cod_status': cod_status,
                'col': col,
                'cor_status_ult_exec': cor_status_ult_exec,
                'cor_status_prox_exec': cor_status_prox_exec
            }

            lista_dic_proc_pri_1.append(dic_proc_info)
            contador += 1



        ordem_status = [5, 4, 2, 3, 1, 0]
        context = {
            'desc_menu': 'Painel de Controle dos Processos - TI',
            'obj_usuario_logado': obj_usuario_logado,
            'lista_col': lista_col,
            'lista_dic_proc_pri_0': sorted(lista_dic_proc_pri_0, key=lambda x: ordem_status.index(x['cod_status'])),
            'lista_dic_proc_pri_1': sorted(lista_dic_proc_pri_1, key=lambda x: ordem_status.index(x['cod_status'])),
            'dt_ultima_atualizacao': datetime.strftime(data_atual, '%d-%m-%Y %H:%M')
        }

        return render(request, 'ti_painel_processos_automaticos_app/frm_painel_processos_automaticos.html', context)

