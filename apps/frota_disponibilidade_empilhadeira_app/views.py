from datetime import datetime, timedelta, date
import os as os_local

import pyodbc
import xlrd
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_disponibilidade_empilhadeira_app.models import Apontamento_Disp_Empilhadeira, \
    OS_Apontamento_Disp_Empilhadeira, Linha_Excel_Apontamento_Promax_Empilhadeira
from apps.frota_disponibilidade_app.models import Sigla_Status_Disponibilidade_Frota, Grupo_Indisponibilidade
from apps.usuario_app.models import Usuario, Proj_Usu
from apps.estrut_org_app.models import Projeto
from proj_portal_operacional.settings import BASE_DIR



class Form_Gera_Disp_Emp_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_projetos = ''
        tipo_usuario = ''
        if usuario_portal.corporativo == 'S':
            lista_projetos = Projeto.objects.filter(data_inativado__isnull=True,
                                                    cod_atividade__desc2_atividade__in=['Apoio'],
                                                    cod_empresa__cod_empresa = 12)
            tipo_usuario = 'C'
        else:
            lista_projetos = Proj_Usu.objects.filter(cod_usu=usuario_portal,
                                                     cod_projeto__cod_atividade__desc2_atividade__in=['Apoio'],
                                                     cod_projeto__data_inativado__isnull=True,
                                                     cod_projeto__cod_empresa__cod_empresa = 12,
                                                     status_proj_usu='S')
            tipo_usuario = 'U'

        context = {
            'tipo_usuario': tipo_usuario,
            'lista_projetos': lista_projetos,
            "id_menu_pai": 8
        }
        return render(request, 'frota_disponibilidade_empilhadeira_app/form_gera_disp_empilhadeira.html', context)
        #return render(request, 'frota_disponibilidade_empilhadeira_app_errado/teste.html', context)





class Form_Param_Geracao_Disp_Emp_View(View):
    def post(self, request):
        handle_proj = request.POST['handle_proj']
        status_placa = request.POST['status_placa']
        '''conn_producao = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ITJM-SRV-018;'
            'DATABASE=TRANSPORTES_PRODUCAO;'
            'UID=servico.portais;'
            'PWD=qm@WHpAWwb;'
        )'''
        lista_empilhadeiras = ConexaoBancoBenner().retorna_empilhadeiras_por_filial(handle_proj, status_placa)
        data = dict()
        data = {
            'lista_empilhadeiras' : lista_empilhadeiras
        }
        return JsonResponse(data, safe=False)



class Gera_Dados_Disponibilidade_Empilhadeira_View(View):
    def get(self, request):
        handle_proj_form = request.GET['handle_proj']
        periodo_form = request.GET['periodo']

        mes_periodo = periodo_form.split('-')[1]
        ano_periodo = periodo_form.split('-')[0]
        obj_projeto = Projeto.objects.filter(handle_benner=handle_proj_form).first()
        lista_apontamentos_indisp_emp = Apontamento_Disp_Empilhadeira.objects.filter(
            cod_projeto=obj_projeto, data_apontamento__month=mes_periodo, data_apontamento__year=ano_periodo
        )
        lista_apontamentos_tabela_form = []
        for reg in lista_apontamentos_indisp_emp:
            #qtd_os_obj_apont_disp_emp = 0
            horas_paradas = '00:00:00'
            data_ini = ''
            data_fim = ''
            #motivo_indisp_emp = ''
            #desc_grupo_insdisp_emp = ''
            #num_os = ''
            lista_os = OS_Apontamento_Disp_Empilhadeira.objects.filter(
                cod_apontamento_disp_emp=reg.cod_apontamento_disp_emp
            )
            total_horas_paradas = None
            if len(lista_os) > 0:
                for os in lista_os:

                    # Calculo das horas paradas
                    calc_horas_paradas_aux = os.parada_fim_aud - os.parada_ini_aud
                    if total_horas_paradas == None:
                        total_horas_paradas = calc_horas_paradas_aux
                    else:
                        total_horas_paradas += calc_horas_paradas_aux

                sec_parada = int(total_horas_paradas.total_seconds())
                dias_parada, sec_tma = divmod(sec_parada, 24 * 3600)
                horas_parada, sec_tma = divmod(sec_parada, 3600)
                min_parada, sec_tma = divmod(sec_parada, 60)
                horas_paradas = str(dias_parada) + ':' + str(horas_parada) + ':' + str(min_parada)

            #Verifica se o apontamento é uma parada e não tem os vinculado
            os_vinculada = ''
            if reg.cod_sigla.cod_sigla in (1,2,6,7) and len(lista_os) > 0:
                os_vinculada = 'ok'
            elif reg.cod_sigla.cod_sigla in (1,2,6,7) and len(lista_os) == 0:
                os_vinculada = 'nok'


            #Calcular qtd de os emitidas para a placa no turno do apontamento
            turno_semana = [{'T': 'M', 'I': '06:00', 'F': '13:59'}, {'T': 'T', 'I': '14:00', 'F': '21:59'},
                            {'T': 'N', 'I': '22:00', 'F': '05:59'}]
            #turno_sab = [{'T': 'M', 'I': '06:00', 'F': '13:59'}, {'T': 'T', 'I': '14:00', 'F': '21:59'}]
            #turno_dom = [{'T': 'N', 'I': '22:00', 'F': '05:59'}]

            # Periodo pesquisa OS
            param_data_ini = ''
            param_data_fim = ''
            hora_turno = ''


            for t in turno_semana:
                if t['T'] == reg.turno:
                    param_data_ini = datetime.strftime(reg.data_apontamento, '%Y-%m-%d') + ' ' + t['I']
                    param_data_fim = datetime.strftime(reg.data_apontamento, '%Y-%m-%d') + ' ' + t['F']
                    if t['T'] == 'N':
                        data_pesq_yyyy_mm_dd_dt_plus_one_day_date = reg.data_apontamento + timedelta(days=1)
                        data_pesq_yyyy_mm_dd_dt_plus_one_day_str = str(data_pesq_yyyy_mm_dd_dt_plus_one_day_date)
                        # data_pesq_yyyy_mm_dd_str
                        param_data_fim = str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[0]) + '-' + \
                                            str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[1]) + '-' + \
                                            str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[2]) + \
                                            ' ' + str(t['F'])
                    hora_turno = t['I'] + ' - ' + t['F']
                    data_ini = param_data_ini
                    data_fim = param_data_fim

            lista_os_benner = ConexaoBancoBenner().retorna_os_by_projeto_placa_data(
                reg.cod_projeto.handle_benner, reg.handle_emp_benner, param_data_ini,
                param_data_fim)
            qtd_os_benner = len(lista_os_benner)

            obj_dicionario = {
                'cod_apontamento_disp_emp': reg.cod_apontamento_disp_emp,
                'dia': reg.data_apontamento,
                'dia_semana_num': reg.data_apontamento.isoweekday(),
                'turno': reg.turno,
                'hora_turno': hora_turno,
                'placa': reg.placa_emp_benner,
                'status_sigla': reg.cod_sigla.sigla,
                #'motivo': motivo_indisp_emp,
                #'grupo': desc_grupo_insdisp_emp,
                'qtd_os_benner': qtd_os_benner,
                'qtd_os_vinculada': len(lista_os),
                #'num_os': num_os,
                'horas_paradas': horas_paradas,
                'os_vinculada': os_vinculada,
                'data_ini' : data_ini,
                'data_fim' : data_fim
            }
            lista_apontamentos_tabela_form.append(obj_dicionario)
        data = {
            'lista_apontamentos_tabela_form': lista_apontamentos_tabela_form,
        }
        return JsonResponse(data, safe=False)
    def post(self, request):
        cod_projeto_form = request.POST['cod_projeto']
        info_emp_form = request.POST['info_emp']
        data_ini = request.POST['data_ini']
        data_fim = request.POST['data_fim']

        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual = data_hora_atual.strftime('%Y-%m-%d')

        mes = data_ini.split('-')[1]
        ano = data_ini.split('-')[0]

        obj_projeto = Projeto.objects.filter(handle_benner=cod_projeto_form).first()

        for dados_emp in info_emp_form.split(','):
            handle_emp = dados_emp.split('_')[0]
            placa_emp = dados_emp.split('_')[1]
            ano_emp = dados_emp.split('_')[2]
            modelo_emp = dados_emp.split('_')[3]
            placa_anterior_emp = dados_emp.split('_')[4]
            ativo_emp = dados_emp.split('_')[5]

            for i in range(int(data_fim.split('-')[2])):
                turno_semana = [{'T': 'M', 'I': '06:00', 'F': '13:59'}, {'T': 'T', 'I': '14:00', 'F': '21:59'},
                                {'T': 'N', 'I': '22:00', 'F': '05:59'}]


                data_pesq = str(i + 1) + '-' + str(mes) + '-' + str(ano)
                data_pesq_yyyy_mm_dd_str = str(ano) + '-' + str(mes) + '-' + str(i + 1)
                data_pesq_yyyy_mm_dd = datetime.strptime(data_pesq_yyyy_mm_dd_str, '%Y-%m-%d')
                dia_semana_num = data_pesq_yyyy_mm_dd.isoweekday()

                obj_apont_disp_emp = None
                qtd_os_obj_apont_disp_emp = 0
                #Verifica se há OS emitida para a empilhadeira no dia

                obj_sigla_disp = Sigla_Status_Disponibilidade_Frota.objects.filter(cod_sigla=4).first()

                for t in turno_semana:
                    obj_apont_disp_emp_pesq = Apontamento_Disp_Empilhadeira.objects.filter(cod_projeto=obj_projeto,
                                                                   data_apontamento=data_pesq_yyyy_mm_dd,
                                                                   handle_emp_benner=handle_emp,
                                                                   turno=t['T']).first()

                    if obj_apont_disp_emp_pesq == None:
                        obj_apont_disp_emp = Apontamento_Disp_Empilhadeira(
                            handle_emp_benner = handle_emp,
                            placa_emp_benner = placa_emp,
                            ano_emp_benner = ano_emp,
                            modelo_emp_benner = modelo_emp,
                            placa_emp_anterior_benner = placa_anterior_emp,
                            ativo_benner = ativo_emp,
                            data_apontamento = data_pesq_yyyy_mm_dd,
                            dia_semana = dia_semana_num,
                            turno = t['T'],
                            cod_usu = obj_usuario,
                            cod_sigla = obj_sigla_disp,
                            cod_projeto = obj_projeto
                        )
                        obj_apont_disp_emp.save()

                        datatime_pesq_ini = str(data_pesq_yyyy_mm_dd_str) + ' ' + str(t['I'])
                        datatime_pesq_fim = str(data_pesq_yyyy_mm_dd_str) + ' ' + str(t['F'])
                        if t['T'] == 'N':
                            data_pesq_yyyy_mm_dd_dt_plus_one_day_date = \
                                datetime.strptime(data_pesq_yyyy_mm_dd_str, '%Y-%m-%d') + timedelta(days=1)
                            data_pesq_yyyy_mm_dd_dt_plus_one_day_str = str(
                                datetime.strftime(data_pesq_yyyy_mm_dd_dt_plus_one_day_date, '%Y-%m-%d'))
                            # data_pesq_yyyy_mm_dd_str
                            datatime_pesq_fim = str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[0]) + '-' + \
                                                str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[1]) + '-' + \
                                                str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[2]) + \
                                                ' ' + str(t['F'])

                        lista_os_apontamento = ConexaoBancoBenner().retorna_os_by_projeto_placa_data(
                                obj_projeto.handle_benner, handle_emp, datatime_pesq_ini, datatime_pesq_fim)

                        qtd_os_obj_apont_disp_emp = len('lista_os_apontamento')
                        # verificar se a qtd de os for maior que 1. se igual a 1 já salver no banco
                        #if qtd_os_obj_apont_disp_emp == 1:
                        if qtd_os_obj_apont_disp_emp > 0:
                            for os in lista_os_apontamento:
                                obj_os_apontamento = OS_Apontamento_Disp_Empilhadeira(
                                    handle_os_benner=os.handle,
                                    num_os_benner=os.numero,
                                    tipo_os_benner=os.handle_tipo,
                                    data_inicial_os_benner=os.data_ini,
                                    data_final_os_benner=os.data_fim,
                                    handle_conjunto_manut_benner=os.handle_conjunto,
                                    desc_conj_manut_benner=os.desc_conjunto,
                                    desc_os_benner=os.desc_os,
                                    # dados para auditoria
                                    motivo=os.desc_os,
                                    parada_ini_aud=os.data_ini,
                                    parada_fim_aud=os.data_fim,
                                    # foreign key
                                    cod_apontamento_disp_emp=obj_apont_disp_emp
                                )
                                obj_os_apontamento.save()
                                obj_sigla_disp_parada = None
                                if os.handle_tipo in (1,22):
                                    obj_sigla_disp_parada = Sigla_Status_Disponibilidade_Frota.objects.filter(
                                        cod_sigla=7).first()
                                else:
                                    obj_sigla_disp_parada = Sigla_Status_Disponibilidade_Frota.objects.filter(
                                        cod_sigla=2).first()
                                obj_apont_disp_emp.cod_sigla = obj_sigla_disp_parada
                                obj_apont_disp_emp.save(update_fields=['cod_sigla'])

        data = dict()
        data = {
            'msg':   'Geração realizada com sucesso!'
        }
        return JsonResponse(data, safe=False)


class Form_Edit_Apont_Disp_Emp_View(View):
    def post(self, request):
        cod_apontamento_form = request.POST['cod_apontamento']
        cod_sigla_status_form = request.POST['cod_sigla_status']
        obs_form = request.POST['obs']

        obj_sigla = Sigla_Status_Disponibilidade_Frota.objects.filter(cod_sigla=cod_sigla_status_form).first()
        obj_apontamento = Apontamento_Disp_Empilhadeira.objects.filter(cod_apontamento_disp_emp=cod_apontamento_form).first()
        obj_apontamento.cod_sigla = obj_sigla
        obj_apontamento.obs = obs_form
        obj_apontamento.save(update_fields=['cod_sigla', 'obs'])

        obj_os_vinculada = OS_Apontamento_Disp_Empilhadeira.objects.filter(cod_apontamento_disp_emp=obj_apontamento).first()
        if obj_os_vinculada != None:
            motivo_aud_form = request.POST['motivo_aud']
            data_ini_aud_form = request.POST['data_ini_aud']
            data_fim_aud_form = request.POST['data_fim_aud']

            obj_os_vinculada.motivo = motivo_aud_form
            obj_os_vinculada.parada_ini_aud = data_ini_aud_form
            obj_os_vinculada.parada_fim_aud = data_fim_aud_form
            obj_os_vinculada.save(update_fields=['motivo', 'parada_ini_aud', 'parada_fim_aud'])

        data = dict()
        data = {
            'msg': 'Registro atualizado com sucesso!'
        }
        return JsonResponse(data, safe=False)


    def get_object(self, pk):
        try:
            return OS_Apontamento_Disp_Empilhadeira.objects.get(pk=pk)
        except OS_Apontamento_Disp_Empilhadeira.DoesNoExist:
            return Http404


    def get(self, request):
        cod_apontamento_form = request.GET['cod_apontamento']
        obj_apont_disp_emp = Apontamento_Disp_Empilhadeira.objects.filter(
            cod_apontamento_disp_emp=cod_apontamento_form).first()
        dic_obj_apont_disp_emp = {
            'cod_apontamento': obj_apont_disp_emp.cod_apontamento_disp_emp,
            'data_apontamento': obj_apont_disp_emp.data_apontamento,
            'placa_emp': obj_apont_disp_emp.placa_emp_benner,
            'modelo_emp': obj_apont_disp_emp.modelo_emp_benner,
            'ano_emp': obj_apont_disp_emp.ano_emp_benner,
            'ativo_emp': obj_apont_disp_emp.ativo_benner,
            'dia_semana': obj_apont_disp_emp.dia_semana,
            'turno': obj_apont_disp_emp.turno,
            'obs': obj_apont_disp_emp.obs,
            'cod_sigla': obj_apont_disp_emp.cod_sigla.cod_sigla,
            'desc_sigla': obj_apont_disp_emp.cod_sigla.desc_sigla

        }
        lista_obj_os_apontamento = []
        obj_os_apontamento = OS_Apontamento_Disp_Empilhadeira.objects.filter(
            cod_apontamento_disp_emp=obj_apont_disp_emp)
        for os_ap in obj_os_apontamento:
            reg = {
                'cod_os_apontamento_disp_emp': os_ap.cod_os_apontamento_disp_emp,
                'num_os_benner': os_ap.num_os_benner,
                'tipo_os_benner': os_ap.tipo_os_benner,
                'data_inicial_os_benner': datetime.strftime(os_ap.data_inicial_os_benner, '%d-%m-%Y %H:%M'),
                'data_final_os_benner': datetime.strftime(os_ap.data_final_os_benner, '%d-%m-%Y %H:%M'),
                'desc_conj_manut_benner': os_ap.desc_conj_manut_benner,
                'desc_os_benner': os_ap.desc_os_benner,
                'motivo': os_ap.motivo,
                'parada_ini_aud': datetime.strftime(os_ap.parada_ini_aud, '%Y-%m-%d %H:%M'),
                'parada_fim_aud': datetime.strftime(os_ap.parada_fim_aud, '%Y-%m-%d %H:%M')

            }
            lista_obj_os_apontamento.append(reg)

        lista_siglas = list(Sigla_Status_Disponibilidade_Frota.objects.all().values('cod_sigla', 'desc_sigla', 'sigla'))
        data = dict()
        data = {
            'dic_obj_apont_disp_emp': dic_obj_apont_disp_emp,
            'obj_os_apontamento': lista_obj_os_apontamento,
            'lista_siglas': lista_siglas
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_os = self.get_object(pk)
        msg = ''
        obj_os.delete()
        msg = 'OS devinculada com sucesso !'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Form_Os_Benner_View(View):
    def post(self, request):
        cod_apontamento_form = request.POST['cod_apontamento']
        handle_os_form = request.POST['handle_os']
        num_os_form = request.POST['num_os']
        tipo_os_form = request.POST['tipo_os']
        desc_tipo_os_form = request.POST['desc_tipo_os']
        data_ini_os_form = request.POST['data_ini_os']
        data_fim_os_form = request.POST['data_fim_os']
        desc_os_form = request.POST['desc_os']
        handle_conj_form = request.POST['handle_conj']
        desc_conj_form = request.POST['desc_conj']

        obj_apontamento = Apontamento_Disp_Empilhadeira.objects.get(pk=cod_apontamento_form)
        '''obj_os = OS_Apontamento_Disp_Empilhadeira.objects.filter(
            cod_apontamento_disp_emp=obj_apontamento).first()
        if obj_os != None:
            obj_os.delete()'''

        obj_os_new = OS_Apontamento_Disp_Empilhadeira(
            handle_os_benner=handle_os_form,
            num_os_benner=num_os_form,
            tipo_os_benner=tipo_os_form,
            data_inicial_os_benner=data_ini_os_form,
            data_final_os_benner=data_fim_os_form,
            handle_conjunto_manut_benner=handle_conj_form,
            desc_conj_manut_benner=desc_conj_form,
            desc_os_benner=desc_os_form,
            # dados para auditoria
            motivo=desc_os_form,
            parada_ini_aud=data_ini_os_form,
            parada_fim_aud=data_fim_os_form,
            # foreign key
            cod_apontamento_disp_emp=obj_apontamento
        )
        obj_os_new.save()
        if obj_apontamento.cod_sigla.cod_sigla in (3, 4, 5, 8):
            obj_sigla_disp = Sigla_Status_Disponibilidade_Frota.objects.filter(
                cod_sigla=7).first()
            obj_apontamento.cod_sigla = obj_sigla_disp
            obj_apontamento.save(update_fields=['cod_sigla'])
        data = dict()
        data = {
            'msg': 'OS vinculada com sucesso!'
        }
        return JsonResponse(data, safe=False)






    def get(self, request, pk):
        turno_semana = [{'T': 'M', 'I': '06:00', 'F': '13:59'}, {'T': 'T', 'I': '14:00', 'F': '21:59'},
                        {'T': 'N', 'I': '22:00', 'F': '05:59'}]

        obj_apont_emp = Apontamento_Disp_Empilhadeira.objects.get(pk=pk)
        dic_obj_apont_disp_emp = {
            'cod_apontamento': obj_apont_emp.cod_apontamento_disp_emp,
            'data_apontamento': obj_apont_emp.data_apontamento,
            'placa_emp': obj_apont_emp.placa_emp_benner,
            'modelo_emp': obj_apont_emp.modelo_emp_benner,
            'ano_emp': obj_apont_emp.ano_emp_benner,
            'ativo_emp': obj_apont_emp.ativo_benner,
            'dia_semana': obj_apont_emp.dia_semana,
            'turno': obj_apont_emp.turno,
            'obs': obj_apont_emp.obs,
            'cod_sigla': obj_apont_emp.cod_sigla.cod_sigla,
            'desc_sigla': obj_apont_emp.cod_sigla.desc_sigla

        }
        #Periodo pesquisa OS
        param_data_ini = ''
        param_data_fim = ''
        for reg in turno_semana:
            if reg['T'] == obj_apont_emp.turno:
                param_data_ini = datetime.strftime(obj_apont_emp.data_apontamento, '%Y-%m-%d')+' '+reg['I']
                param_data_fim = datetime.strftime(obj_apont_emp.data_apontamento, '%Y-%m-%d')+' '+reg['F']
                if reg['T'] == 'N':
                    data_pesq_yyyy_mm_dd_dt_plus_one_day_date = obj_apont_emp.data_apontamento + timedelta(days=1)
                    data_pesq_yyyy_mm_dd_dt_plus_one_day_str = str(
                        datetime.strftime(data_pesq_yyyy_mm_dd_dt_plus_one_day_date, '%Y-%m-%d'))
                    # data_pesq_yyyy_mm_dd_str
                    param_data_fim = str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[0]) + '-' + \
                                        str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[1]) + '-' + \
                                        str(data_pesq_yyyy_mm_dd_dt_plus_one_day_str.split('-')[2]) + \
                                        ' ' + str(reg['F'])



        conn_producao = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ITJM-SRV-018;'
            'DATABASE=TRANSPORTES_PRODUCAO;'
            'UID=servico.portais;'
            'PWD=qm@WHpAWwb;'
        )

        lista_os_benner = ConexaoBancoBenner().retorna_os_by_projeto_placa_data(
            obj_apont_emp.cod_projeto.handle_benner, obj_apont_emp.handle_emp_benner, param_data_ini, param_data_fim)


        lista_os_benner_dic = []
        for os in lista_os_benner:
            lista_os_benner_dic.append(os.__dict__)


        data = dict()
        data = {
            'lista_os_benner': lista_os_benner_dic,
            'dic_obj_apont_disp_emp': dic_obj_apont_disp_emp
        }
        return JsonResponse(data, safe=False)


class Importa_Dispobilidade_Empilhadeira():
    def le_arquivo_apontamento_promax(self, arq_xlsx):
        arquivo_xlsx = xlrd.open_workbook(str(arq_xlsx))
        lista_plan_arquivo = arquivo_xlsx.sheet_names()

        plan_disponibilidade = ''
        for plan in lista_plan_arquivo:
            if plan == 'DISPONIBILIDADE':
                plan_disponibilidade = arquivo_xlsx.sheet_by_name(plan)
                break
        lista_registros = []
        if plan_disponibilidade != '':
            status_leitura = ''
            erros_encontrado = 0
            if plan_disponibilidade.row_values(0)[0] != 'data':
                status_leitura = 'Não encontrada coluna data!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[1] != 'placa':
                status_leitura = 'Não encontrada coluna placa!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[2] != 'nº os':
                status_leitura = 'Não encontrada coluna nº os!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[3] != 'justificativa':
                status_leitura = 'Não encontrada coluna justificativa!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[4] != 'sigla':
                status_leitura = 'Não encontrada coluna sigla!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[5] != 'projeto':
                status_leitura = 'Não encontrada coluna projeto!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[6] != 'turno':
                status_leitura = 'Não encontrada coluna turno!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[7] != 'handle_placa':
                status_leitura = 'Não encontrada coluna handle_placa!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[8] != 'ano_placa':
                status_leitura = 'Não encontrada coluna ano_placa!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[9] != 'modelo_placa':
                status_leitura = 'Não encontrada coluna modelo_placa!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[10] != 'ativo':
                status_leitura = 'Não encontrada coluna ativo!'
                erros_encontrado+=1

            if erros_encontrado == 0:
                for i in range(plan_disponibilidade.nrows):
                    if i > 0:
                        if i == plan_disponibilidade.nrows:
                            break
                        else:
                            reg_lanc = Linha_Excel_Apontamento_Promax_Empilhadeira(
                                plan_disponibilidade.row_values(i)[0],
                                plan_disponibilidade.row_values(i)[1],
                                plan_disponibilidade.row_values(i)[2],
                                plan_disponibilidade.row_values(i)[3],
                                plan_disponibilidade.row_values(i)[4],
                                int(plan_disponibilidade.row_values(i)[5]),
                                plan_disponibilidade.row_values(i)[6],
                                plan_disponibilidade.row_values(i)[7],
                                plan_disponibilidade.row_values(i)[8],
                                plan_disponibilidade.row_values(i)[9],
                                plan_disponibilidade.row_values(i)[10],
                                'L'
                            )

                            lista_registros.append(reg_lanc)
            else:
                reg_lanc = Linha_Excel_Apontamento_Promax_Empilhadeira(
                    None, None, None, None, None, None, None, None, None, None, None, status_leitura
                )
                lista_registros.append(reg_lanc)
        else:
            reg_lanc = Linha_Excel_Apontamento_Promax_Empilhadeira(
                None, None, None, None, None, None, None, None, None, None, None, 'Planilha DISPONIBILIDADE não identificada!'
            )
            lista_registros.append(reg_lanc)
        return lista_registros



class Imp_Apontamento_Promax_Empilhadeira_View(View):
    def post(self, request):
        myfile = request.FILES['file']
        id_usu_session = request.session['cod_usuario_logado']

        obj_usuario = Usuario.objects.get(pk=id_usu_session)

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_dd = data_hora_atual.strftime('%Y-%m-%d')
        hora_atual = data_hora_atual.strftime('%H:%M')

        fs = FileSystemStorage()
        caminho_arq_importado_server = 'docs/apontamento_promax_emp/Lanc_Apontamento_Promax_Emp_'+\
            str(obj_usuario.login_usu)+"_"+str(data_atual_yyyy_mm_dd).replace('/', '_')+\
                                       '_'+str(hora_atual.replace(':', '_'))+myfile.name
        filename = fs.save(caminho_arq_importado_server, myfile)
        #uploaded_file_url = fs.url(filename)
        uploaded_file_url = os_local.path.join(BASE_DIR, 'media/' + caminho_arq_importado_server)

        obj_imp_arq_apontamento_promax = Importa_Dispobilidade_Empilhadeira()
        lista_apontamentos_promax = obj_imp_arq_apontamento_promax.le_arquivo_apontamento_promax(uploaded_file_url)
        msg = ''
        tab_lanc_apontados = []
        if len(lista_apontamentos_promax) > 0 and lista_apontamentos_promax[0].status_leitura_importacao == 'L':
            for reg in lista_apontamentos_promax:
                obj_projeto = None
                obj_sigla = None
                dia_semana_num = datetime.strptime(reg.data, '%d/%m/%Y').isoweekday()

                ano_modelo_emp_benner = reg.ano_emp
                if reg.ano_emp == '':
                    ano_modelo_emp_benner = 0

                if reg.projeto != '':
                    obj_projeto = Projeto.objects.filter(cod_projeto=reg.projeto).first()
                if reg.sigla != '':
                    obj_sigla = Sigla_Status_Disponibilidade_Frota.objects.filter(
                        sigla=reg.sigla
                    ).first()


                if obj_sigla == None and reg.sigla != '':
                    reg.sigla = "<span style='background:#fa6163;color:#FFFFFF'>"+reg.sigla+"</span>"
                elif obj_sigla == None and reg.sigla == '':
                    reg.sigla = "<span style='background:#fa6163;color:#FFFFFF'>Não informado</span>"

                if obj_projeto == None and reg.projeto != '':
                    reg.projeto = "<span style='background:#fa6163;color:#FFFFFF'>"+str(reg.projeto)+"</span>"
                elif obj_projeto == None and reg.projeto == '':
                    reg.projeto = "<span style='background:#fa6163;color:#FFFFFF'>Não informado</span>"

                if obj_projeto != None and obj_sigla != None:
                    reg_apont_promax_busca = Apontamento_Disp_Empilhadeira.objects.filter(
                        data_apontamento=datetime.strptime(reg.data, '%d/%m/%Y'),
                        turno=reg.turno,
                        placa_emp_benner=reg.placa,
                        cod_projeto=obj_projeto).first()

                    if reg_apont_promax_busca == None:
                        turno_semana = [{'T': 'M', 'I': '06:00', 'F': '13:59'}, {'T': 'T', 'I': '14:00', 'F': '21:59'},
                                        {'T': 'N', 'I': '22:00', 'F': '05:59'}]


                        reg_apont_promax = Apontamento_Disp_Empilhadeira(
                            handle_emp_benner = 0,
                            placa_emp_benner = reg.placa,
                            ano_emp_benner = ano_modelo_emp_benner,
                            modelo_emp_benner = reg.modelo_emp,
                            placa_emp_anterior_benner = '',
                            ativo_benner = reg.ativo,
                            data_apontamento = datetime.strptime(reg.data, '%d/%m/%Y'),
                            dia_semana = dia_semana_num,
                            turno = reg.turno,
                            cod_usu = obj_usuario,
                            cod_sigla = obj_sigla,
                            cod_projeto = obj_projeto
                        )
                        reg_apont_promax.save()
                        lista_os = reg.num_os.split(",")
                        lista_num_os_str = str(lista_os).replace('[','').replace(']','')
                        if lista_num_os_str != None or lista_num_os_str != '':
                            lista_os_apontamento = ConexaoBancoBenner().retorna_os_by_num_os(
                                obj_projeto.handle_benner, lista_num_os_str)
                            for os in lista_os_apontamento:
                                obj_os_apontamento = OS_Apontamento_Disp_Empilhadeira(
                                    handle_os_benner = os.handle,
                                    num_os_benner = os.numero,
                                    tipo_os_benner = os.handle_tipo,
                                    data_inicial_os_benner = os.data_ini,
                                    data_final_os_benner = os.data_fim,
                                    handle_conjunto_manut_benner = os.handle_conjunto,
                                    desc_conj_manut_benner = os.desc_conjunto,
                                    desc_os_benner = os.desc_os,
                                    # dados para auditoria
                                    motivo = reg.justificativa,
                                    parada_ini_aud = os.data_ini,
                                    parada_fim_aud = os.data_fim,
                                    # foreign key
                                    cod_apontamento_disp_emp = reg_apont_promax
                                )
                                cod_sigla_status = os.handle_tipo
                                obj_os_apontamento.save()
                        reg.status_leitura_importacao  ='I'

                    else:
                        reg_apont_promax_busca.handle_emp_benner = 0
                        #reg_apont_promax_busca.placa_emp_benner = reg.placa
                        reg_apont_promax_busca.ano_emp_benner = ano_modelo_emp_benner
                        reg_apont_promax_busca.modelo_emp_benner = reg.modelo_emp
                        reg_apont_promax_busca.placa_emp_anterior_benner = ''
                        reg_apont_promax_busca.ativo_benner = reg.ativo
                        #reg_apont_promax_busca.data_apontamento = reg.data
                        reg_apont_promax_busca.dia_semana = dia_semana_num
                        #reg_apont_promax_busca.turno = reg.turno
                        reg_apont_promax_busca.cod_usu = obj_usuario
                        reg_apont_promax_busca.cod_sigla = obj_sigla
                        #reg_apont_promax_busca.cod_projeto = obj_projeto
                        reg_apont_promax_busca.save(update_fields=['handle_emp_benner','ano_emp_benner',
                                                                   'modelo_emp_benner','placa_emp_anterior_benner','ativo_benner',
                                                                   'dia_semana','cod_usu',
                                                                   'cod_sigla'])
                        reg.status_leitura_importacao = 'A'

                        if reg_apont_promax_busca.cod_sigla.cod_sigla in (1,2,6,7):
                            lista_os = OS_Apontamento_Disp_Empilhadeira.objects.filter(
                                cod_apontamento_disp_emp=reg_apont_promax_busca)
                            if len(lista_os) > 0:
                                for os in lista_os:
                                    os.delete()

                            lista_os = reg.num_os.split(",")
                            lista_num_os_str = str(lista_os).replace('[','').replace(']','')
                            if lista_num_os_str != None or lista_num_os_str != '':
                                lista_os_apontamento = ConexaoBancoBenner().retorna_os_by_num_os(
                                    obj_projeto.handle_benner, lista_num_os_str)

                                for os in lista_os_apontamento:
                                    obj_os_apontamento = OS_Apontamento_Disp_Empilhadeira(
                                        handle_os_benner = os.handle,
                                        num_os_benner = os.numero,
                                        tipo_os_benner = os.handle_tipo,
                                        data_inicial_os_benner = os.data_ini,
                                        data_final_os_benner = os.data_fim,
                                        handle_conjunto_manut_benner = os.handle_conjunto,
                                        desc_conj_manut_benner = os.desc_conjunto,
                                        desc_os_benner = os.desc_os,
                                        # dados para auditoria
                                        motivo = reg.justificativa,
                                        parada_ini_aud = os.data_ini,
                                        parada_fim_aud = os.data_fim,
                                        # foreign key
                                        cod_apontamento_disp_emp = reg_apont_promax_busca
                                    )
                                    cod_sigla_status = os.handle_tipo
                                    obj_os_apontamento.save()

                            reg.status_leitura_importacao  ='I'
                    msg = 'Arquivo importado com sucesso !'
                else:
                    reg.status_leitura_importacao = 'Grupo de indisponibilidade, código do projeto ou sigla não registrado. Verifique!'
                tab_lanc_apontados.append(reg.__dict__)

        elif len(lista_apontamentos_promax) > 0:
            tab_lanc_apontados.append(lista_apontamentos_promax[0].__dict__)
            msg = 'O arquivo contem erros de padrão de layout!'

        data = dict()
        data = {
            'msg': msg,
            'lista_apontamentos_promax': tab_lanc_apontados,
        }
        return JsonResponse(data, safe=False)