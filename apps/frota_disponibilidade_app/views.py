import calendar
import os
from datetime import datetime

import xlrd
from django.core.files.storage import FileSystemStorage
from django.db.models import Max
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views import View

from apps.frota_disponibilidade_app.models import Apontamento_Promax, Grupo_Indisponibilidade, \
    Sigla_Status_Disponibilidade_Frota, Frota_Contratada
from apps.usuario_app.models import Usuario, Proj_Usu
from apps.estrut_org_app.models import Projeto
from proj_portal_operacional.settings import BASE_DIR


class Form_Imp_Apontamento_Promax(View):
    def get(self, request):
        context = {
            "desc_menu_principal": 'Importa Arquivos Disponibilidade Frota',
            "id_menu_pai": 8
        }
        return render(request, 'frota_disponibilidade_app/form_importa_plan_promax_apontamento.html', context)

class Linha_Excel_Apontamento_Promax():
    def __init__(self, data, placa, status, num_os, justificativa, sigla, grupo_disponibilidade,
                 projeto, status_leitura_importacao):
        self.data = data
        self.placa = placa
        self.status = status
        self.num_os = num_os
        self.justificativa = justificativa
        self.sigla = sigla
        self.grupo_disponibilidade = grupo_disponibilidade
        self.projeto = projeto
        self.status_leitura_importacao = status_leitura_importacao


class Linha_Excel_Frota_Contratada():
    def __init__(self, data, num_sem, qtd_ativa, qtd_parada, cod_projeto, turno, status_leitura_importacao):
        self.data = data
        self.num_sem = num_sem
        self.qtd_ativa = qtd_ativa
        self.qtd_parada = qtd_parada
        self.cod_projeto = cod_projeto
        self.turno = turno
        self.status_leitura_importacao = status_leitura_importacao

class Importa_Dispobilidade_Frota():
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
            elif plan_disponibilidade.row_values(0)[2] != 'status':
                status_leitura = 'Não encontrada coluna status!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[3] != 'nº os':
                status_leitura = 'Não encontrada coluna nº os!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[4] != 'justificativa':
                status_leitura = 'Não encontrada coluna justificativa!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[5] != 'sigla':
                status_leitura = 'Não encontrada coluna sigla!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[6] != 'grupo da indisponibilidade':
                status_leitura = 'Não encontrada coluna grupo da indisponibilidade!'
                erros_encontrado+=1
            elif plan_disponibilidade.row_values(0)[7] != 'projeto':
                status_leitura = 'Não encontrada coluna projeto!'
                erros_encontrado+=1

            if erros_encontrado == 0:
                for i in range(plan_disponibilidade.nrows):
                    if i > 0:
                        if i == plan_disponibilidade.nrows:
                            break
                        else:
                            reg_lanc = Linha_Excel_Apontamento_Promax(
                                plan_disponibilidade.row_values(i)[0],
                                plan_disponibilidade.row_values(i)[1],
                                plan_disponibilidade.row_values(i)[2],
                                plan_disponibilidade.row_values(i)[3],
                                plan_disponibilidade.row_values(i)[4],
                                plan_disponibilidade.row_values(i)[5],
                                plan_disponibilidade.row_values(i)[6],
                                plan_disponibilidade.row_values(i)[7],
                                'L'
                            )

                            lista_registros.append(reg_lanc)
            else:
                reg_lanc = Linha_Excel_Apontamento_Promax(
                    None, None, None, None, None, None, None, None, status_leitura
                )
                lista_registros.append(reg_lanc)
        else:
            reg_lanc = Linha_Excel_Apontamento_Promax(
                None, None, None, None, None, None, None, None, 'Planilha DISPONIBILIDADE não identificada!'
            )
            lista_registros.append(reg_lanc)
        return lista_registros


class Importa_Frota_Contratada():
    def le_arquivo_frota_contratada(self, arq_xlsx):
        arquivo_xlsx = xlrd.open_workbook(str(arq_xlsx))
        lista_plan_arquivo = arquivo_xlsx.sheet_names()
        tipo_plan = 'rota'

        plan_frota_contratada = ''
        for plan in lista_plan_arquivo:
            if plan == 'FROTA CONTRATADA':
                plan_frota_contratada = arquivo_xlsx.sheet_by_name(plan)
                break
        lista_registros = []
        if plan_frota_contratada != '':
            status_leitura = ''
            erros_encontrado = 0
            if plan_frota_contratada.row_values(0)[0] != 'data':
                status_leitura = 'Não encontrada coluna data!'
                erros_encontrado+=1
            elif plan_frota_contratada.row_values(0)[1] != 'ativa':
                status_leitura = 'Não encontrada coluna ativa!'
                erros_encontrado+=1
            elif plan_frota_contratada.row_values(0)[2] != 'parada' and plan_frota_contratada.row_values(0)[2] != 'contratada':
                status_leitura = 'Não encontrada coluna parada para rota e contratada para empilhadeiras'
                erros_encontrado+=1
            elif plan_frota_contratada.row_values(0)[3] != 'projeto':
                status_leitura = 'Não encontrada coluna projeto'
                erros_encontrado+=1
            elif len(plan_frota_contratada.row_values(0)) == 5 and plan_frota_contratada.row_values(0)[4] == 'turno':
                tipo_plan = 'emp'

            if erros_encontrado == 0:
                for i in range(plan_frota_contratada.nrows):
                    if i > 0:
                        if i == plan_frota_contratada.nrows:
                            break
                        else:
                            data_ref_frota_contratada = datetime.strptime(plan_frota_contratada.row_values(i)[0], '%d/%m/%Y')
                            dia_semana_num = data_ref_frota_contratada.isoweekday()

                            reg_lanc = ''
                            if tipo_plan == 'rota':
                                reg_lanc = Linha_Excel_Frota_Contratada(
                                    plan_frota_contratada.row_values(i)[0],
                                    dia_semana_num,
                                    plan_frota_contratada.row_values(i)[1],
                                    plan_frota_contratada.row_values(i)[2],
                                    plan_frota_contratada.row_values(i)[3],
                                    'D',
                                    'L'
                                )
                            elif tipo_plan == 'emp':
                                reg_lanc = Linha_Excel_Frota_Contratada(
                                    plan_frota_contratada.row_values(i)[0],
                                    dia_semana_num,
                                    plan_frota_contratada.row_values(i)[1],
                                    plan_frota_contratada.row_values(i)[2],
                                    plan_frota_contratada.row_values(i)[3],
                                    plan_frota_contratada.row_values(i)[4],
                                    'L'
                                )
                            lista_registros.append(reg_lanc)
            else:
                reg_lanc = Linha_Excel_Frota_Contratada(
                    None, None, None, None, None, status_leitura
                )
                lista_registros.append(reg_lanc)
        else:
            reg_lanc = Linha_Excel_Frota_Contratada(
                None, None, None, None, None, 'Planilha FROTA CONTRATADA não identificada!'
            )
            lista_registros.append(reg_lanc)


        return lista_registros



class Imp_Apontamento_Promax_View(View):
    def post(self, request):
        myfile = request.FILES['file']
        id_usu_session = request.session['cod_usuario_logado']

        obj_usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_dd = data_hora_atual.strftime('%Y-%m-%d')
        hora_atual = data_hora_atual.strftime('%H:%M')

        fs = FileSystemStorage()
        caminho_arq_importado_server = 'docs/apontamento_promax_rota/Lanc_Apontamento_Promax_'+str(obj_usuario.login_usu)+\
                                       "_"+str(data_atual_yyyy_mm_dd).replace('/', '_')+\
                                       '_'+str(hora_atual.replace(':', '_'))+myfile.name
        filename = fs.save(caminho_arq_importado_server, myfile)
        #uploaded_file_url = fs.url(filename)
        uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado_server)

        obj_imp_arq_apontamento_promax = Importa_Dispobilidade_Frota()
        lista_apontamentos_promax = obj_imp_arq_apontamento_promax.le_arquivo_apontamento_promax(uploaded_file_url)
        msg = ''
        tab_lanc_apontados = []
        if len(lista_apontamentos_promax) > 0 and lista_apontamentos_promax[0].status_leitura_importacao == 'L':
            for reg in lista_apontamentos_promax:
                obj_projeto = None
                obj_sigla = None
                obj_grupo_indisp = None

                if reg.projeto != '':
                    obj_projeto = Projeto.objects.filter(cod_projeto=reg.projeto).first()
                if reg.sigla != '':
                    obj_sigla = Sigla_Status_Disponibilidade_Frota.objects.filter(
                        sigla=reg.sigla
                    ).first()
                if reg.grupo_disponibilidade != '':
                    obj_grupo_indisp = Grupo_Indisponibilidade.objects.filter(
                        desc_grupo_indisp=reg.grupo_disponibilidade).first()

                if obj_sigla == None and reg.sigla != '':
                    reg.sigla = "<span style='background:#fa6163;color:#FFFFFF'>"+reg.sigla+"</span>"
                elif obj_sigla == None and reg.sigla == '':
                    reg.sigla = "<span style='background:#fa6163;color:#FFFFFF'>Não informado</span>"

                if obj_grupo_indisp == None and reg.grupo_disponibilidade != '':
                    reg.grupo_disponibilidade = "<span style='background:#fa6163;color:#FFFFFF'>"+reg.grupo_disponibilidade+"</span>"
                elif obj_grupo_indisp == None and reg.grupo_disponibilidade == '':
                    reg.grupo_disponibilidade = "<span style='background:#fa6163;color:#FFFFFF'></span>"

                if obj_projeto == None and reg.projeto != '':
                    reg.projeto = "<span style='background:#fa6163;color:#FFFFFF'>"+reg.projeto+"</span>"
                elif obj_projeto == None and reg.projeto == '':
                    reg.projeto = "<span style='background:#fa6163;color:#FFFFFF'>Não informado</span>"

                if obj_projeto != None and obj_sigla != None:
                    reg_apont_promax_busca = Apontamento_Promax.objects.filter(
                        data_apontamento=datetime.strptime(reg.data, '%d/%m/%Y'),
                        placa=reg.placa,
                        cod_projeto=obj_projeto).first()

                    if reg_apont_promax_busca == None:
                        reg_apont_promax = Apontamento_Promax(
                            data_lancamento = data_atual_yyyy_mm_dd,
                            data_apontamento = datetime.strptime(reg.data, '%d/%m/%Y'),
                            placa = reg.placa,
                            status_placa = reg.status,
                            numero_os = reg.num_os,
                            justificativa = reg.justificativa,
                            status_lanc='S',
                            cod_sigla = obj_sigla,
                            cod_grupo_indisponibilidade = obj_grupo_indisp,
                            cod_projeto = obj_projeto,
                            cod_usu = obj_usuario
                        )
                        reg_apont_promax.save()
                        reg.status_leitura_importacao  ='I'
                    else:
                        reg_apont_promax_busca.data_lancamento = data_atual_yyyy_mm_dd
                        reg_apont_promax_busca.status_placa = reg.status
                        reg_apont_promax_busca.numero_os = reg.num_os
                        reg_apont_promax_busca.justificativa = reg.justificativa
                        reg_apont_promax_busca.status_lanc = 'A'
                        reg_apont_promax_busca.cod_sigla = obj_sigla
                        reg_apont_promax_busca.cod_grupo_indisponibilidade = obj_grupo_indisp
                        reg_apont_promax_busca.cod_projeto = obj_projeto
                        reg_apont_promax_busca.cod_usu = obj_usuario
                        reg_apont_promax_busca.save(update_fields=['data_lancamento', 'status_placa', 'numero_os',
                                                                   'justificativa', 'status_lanc', 'cod_sigla',
                                                                   'cod_grupo_indisponibilidade', 'cod_projeto',
                                                                   'cod_usu'])
                        reg.status_leitura_importacao = 'A'
                else:
                    reg.status_leitura_importacao = 'Grupo de indisponibilidade, código do projeto ou sigla não registrado. Verifique!'
                tab_lanc_apontados.append(reg.__dict__)
            msg = 'Arquivo importado com sucesso !'
        elif len(lista_apontamentos_promax) > 0:
            tab_lanc_apontados.append(lista_apontamentos_promax[0].__dict__)
            msg = 'O arquivo contem erros de padrão de layout!'

        data = dict()
        data = {
            'msg': msg,
            'lista_apontamentos_promax': tab_lanc_apontados,
        }
        return JsonResponse(data, safe=False)


class Imp_Frota_Contratada_View(View):
    def post(self, request):
        myfile = request.FILES['file']
        id_usu_session = request.session['cod_usuario_logado']

        obj_usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_dd = data_hora_atual.strftime('%Y-%m-%d')
        hora_atual = data_hora_atual.strftime('%H:%M')

        fs = FileSystemStorage()
        caminho_arq_importado_server = 'docs/frota_contratada/Lan_Frota_Contratada_'+\
            str(obj_usuario.login_usu)+'_'+str(data_atual_yyyy_mm_dd)\
            .replace('/','_')+'_'+str(hora_atual.replace(':','_')) + myfile.name
        filename = fs.save(caminho_arq_importado_server, myfile)
        #uploaded_file_url = fs.url(filename)
        uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado_server)

        obj_imp_frota_contratada = Importa_Frota_Contratada()
        lista_frota_contratada = obj_imp_frota_contratada.le_arquivo_frota_contratada(uploaded_file_url)
        #for a in lista_frota_contratada:
        #    print('Dados : ' + a.data)
        msg = ''
        tab_lanc_frota_contratada = []
        desc_atividade_projeto = 'Rota'
        if len(lista_frota_contratada) > 0 and lista_frota_contratada[0].status_leitura_importacao == 'L':
            for reg in lista_frota_contratada:
                obj_projeto = None

                if reg.cod_projeto != '':
                    obj_projeto = Projeto.objects.filter(cod_projeto=reg.cod_projeto).first()
                    desc_atividade_projeto = obj_projeto.cod_atividade.desc2_atividade
                if obj_projeto == None and reg.cod_projeto != '':
                    reg.cod_projeto = "<span style='background:#fa6163;color:#FFFFFF'>" + reg.cod_projeto + "</span>"
                elif obj_projeto == None and reg.cod_projeto == '':
                    reg.cod_projeto = "<span style='background:#fa6163;color:#FFFFFF'>Não informado</span>"

                if obj_projeto != None:

                    reg_frota_contratada_busca = Frota_Contratada.objects.filter(
                        data_ref=datetime.strptime(reg.data, '%d/%m/%Y'),
                        turno=reg.turno,
                        cod_projeto=obj_projeto).first()

                    if reg_frota_contratada_busca == None:
                        data_ref_frota_contratada = datetime.strptime(reg.data, '%d/%m/%Y')
                        dia_semana_num = data_ref_frota_contratada.isoweekday()

                        reg_frota_contratada = Frota_Contratada(
                            data_lancamento= data_atual_yyyy_mm_dd,
                            data_ref = datetime.strptime(reg.data, '%d/%m/%Y'),
                            dia_semana = dia_semana_num,
                            turno=reg.turno,
                            qtd_frota_contratada_ativa = reg.qtd_ativa,
                            qtd_frota_contratada_parada = reg.qtd_parada,
                            cod_projeto = obj_projeto,
                            cod_usu = obj_usuario
                        )
                        reg_frota_contratada.save()
                        reg.status_leitura_importacao = 'I'
                    else:
                        reg_frota_contratada_busca.data_lancamento = data_atual_yyyy_mm_dd
                        reg_frota_contratada_busca.qtd_frota_contratada_ativa = reg.qtd_ativa
                        reg_frota_contratada_busca.qtd_frota_contratada_parada = reg.qtd_parada
                        reg_frota_contratada_busca.cod_projeto = obj_projeto
                        reg_frota_contratada_busca.cod_usu = obj_usuario
                        reg_frota_contratada_busca.save(update_fields=['data_lancamento', 'qtd_frota_contratada_ativa',
                                                                       'qtd_frota_contratada_parada', 'cod_projeto',
                                                                       'cod_usu'])
                        reg.status_leitura_importacao = 'A'
                else:
                    reg.status_leitura_importacao = 'Cód. Projeto não registrado. Verifique !'
                tab_lanc_frota_contratada.append(reg.__dict__)
        elif len(lista_frota_contratada) > 0:
            tab_lanc_frota_contratada.append(lista_frota_contratada[0].__dict__)
            msg = 'O arquivo contem erros de padrão de layout!'

        data = dict()
        data = {
            'msg': msg,
            'desc_atividade_projeto': desc_atividade_projeto,
            'lista_frota_contratada': tab_lanc_frota_contratada
        }
        return JsonResponse(data, safe=False)







class Form_Lanc_Frota_Contratada(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_projetos = ''
        tipo_usuario = ''
        if usuario_portal.corporativo == 'S':
            lista_projetos = Projeto.objects.filter(data_inativado__isnull=True,
                                                    cod_atividade__desc2_atividade__in=['Rota', 'AS', 'Apoio'],
                                                    cod_empresa__cod_empresa = 12)
            tipo_usuario = 'C'
        else:
            lista_projetos = Proj_Usu.objects.filter(cod_usu=usuario_portal,
                                           cod_projeto__cod_atividade__desc2_atividade__in=['Rota', 'AS', 'Apoio'],
                                           cod_projeto__data_inativado__isnull=True,
                                           cod_projeto__cod_empresa__cod_empresa = 12,
                                           status_proj_usu='S')
            tipo_usuario='U'


        context = {
            'tipo_usuario': tipo_usuario,
            'lista_projetos': lista_projetos,
            "desc_menu_principal": 'Lançamento Frota Contratada',
            "id_menu_pai": 8
        }
        return render(request, 'frota_disponibilidade_app/form_lanc_frota_contratada.html', context)

class Lanc_Frota_Contratada_View(View):
    def post(self, request):
        cod_frota_contratada_form = request.POST['cod_frota_contratada']
        cod_projeto = request.POST['cod_projeto']
        periodo = request.POST['periodo']
        qtd_ativa = request.POST['qtd_ativa']
        qtd_parada = request.POST['qtd_parada']

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_dd = data_hora_atual.strftime('%Y-%m-%d')

        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()

        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto).first()

        data_periodo = periodo.split('-')[0] + '/' + periodo.split('-')[1] + '/' + periodo.split('-')[2]
        data_pesq_yyyy_mm_dd = datetime.strptime(data_periodo, '%Y/%m/%d')
        dia_semana_num = data_pesq_yyyy_mm_dd.isoweekday()


        #obj_frota_contratada = Frota_Contratada.objects.filter(data_ref=periodo, cod_projeto=cod_projeto).first()
        obj_frota_contratada = Frota_Contratada.objects.filter(cod_frota_contratada=cod_frota_contratada_form).first()
        msg = ''
        if obj_frota_contratada == None:
            novo_registro = Frota_Contratada(
                data_lancamento = data_atual_yyyy_mm_dd,
                data_ref=periodo,
                dia_semana=dia_semana_num,
                qtd_frota_contratada_ativa=qtd_ativa,
                qtd_frota_contratada_parada=qtd_parada,
                cod_projeto=obj_projeto,
                cod_usu=usuario_portal
            )
            novo_registro.save()
            msg = 'Registro salvo com sucesso !'
        else:
            obj_frota_contratada.data_lancamento = data_atual_yyyy_mm_dd
            obj_frota_contratada.qtd_frota_contratada_ativa = qtd_ativa
            obj_frota_contratada.qtd_frota_contratada_parada = qtd_parada
            obj_frota_contratada.cod_usu = usuario_portal
            obj_frota_contratada.save(update_fields=['data_lancamento', 'qtd_frota_contratada_ativa',
                                                     'qtd_frota_contratada_parada', 'cod_usu'])
            msg = 'Registro atualizado com sucesso !'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)


    def get(self, request):
        cod_projeto = request.GET['cod_projeto']
        periodo = request.GET['periodo']

        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual = data_hora_atual.strftime('%Y-%m-%d')

        mes = periodo.split('-')[1]
        ano = periodo.split('-')[0]
        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto).first()


        lista_form_lanc_frota_contrat = []
        ultimo_dia_do_mes = calendar.monthrange(int(ano), int(mes))
        for dia in range(ultimo_dia_do_mes[1]):
            #data_pesq = str(dia+1) + '/' + periodo
            data_pesq = periodo.split('-')[0]+'-'+periodo.split('-')[1]+'-'+str(dia + 1)
            data_pesq_yyyy_mm_dd = datetime.strptime(data_pesq,'%Y-%m-%d')
            dia_semana_num = data_pesq_yyyy_mm_dd.isoweekday()

            if obj_projeto.cod_atividade.desc2_atividade != 'Apoio':
                obj_frota_contrat_pesq = Frota_Contratada.objects.filter(cod_projeto=obj_projeto,
                                                                    data_ref=data_pesq).first()
                if obj_frota_contrat_pesq == None:
                    obj_frota_contrat = Frota_Contratada(
                        #cod_frota_contratada = 0,
                        data_lancamento = data_atual,
                        data_ref = data_pesq,
                        dia_semana=dia_semana_num,
                        turno='D',
                        qtd_frota_contratada_ativa = 0,
                        qtd_frota_contratada_parada = 0,
                        cod_usu = obj_usuario,
                        cod_projeto = obj_projeto
                    )
                    obj_frota_contrat.save()
            else:
                turno_semana = [{'T': 'M', 'I': '06:00', 'F': '13:59'}, {'T': 'T', 'I': '14:00', 'F': '21:59'},
                                {'T': 'N', 'I': '22:00', 'F': '05:59'}]



                for t in turno_semana:
                    obj_frota_contrat_pesq = Frota_Contratada.objects.filter(cod_projeto=obj_projeto,
                                                                             data_ref=data_pesq,
                                                                             turno=t['T']).first()
                    if obj_frota_contrat_pesq == None:
                        obj_frota_contrat = Frota_Contratada(
                            # cod_frota_contratada = 0,
                            data_lancamento=data_atual,
                            data_ref=data_pesq,
                            dia_semana=dia_semana_num,
                            turno=t['T'],
                            qtd_frota_contratada_ativa=0,
                            qtd_frota_contratada_parada=0,
                            cod_usu=obj_usuario,
                            cod_projeto=obj_projeto
                        )
                        obj_frota_contrat.save()

        lista_form_lanc_frota_contrat = list(Frota_Contratada.objects.filter(cod_projeto=obj_projeto,
                                                                             data_ref__month=mes,
                                                                             data_ref__year=ano) \
                                             .values('cod_frota_contratada', 'data_ref', 'dia_semana', 'turno',
                                                     'qtd_frota_contratada_ativa',
                                                     'qtd_frota_contratada_parada'))
        data = dict()
        data = {
            'lista_form_lanc_frota_contrat': lista_form_lanc_frota_contrat,
            'desc_atividade_projeto':obj_projeto.cod_atividade.desc2_atividade
        }
        return JsonResponse(data, safe=False)


class Form_Cad_Comp_Sigla_Disp_Frota_View(View):
    def get(self, request):
        lista_siglas = list(Sigla_Status_Disponibilidade_Frota.objects.all().values())

        data = dict()
        data = {
            'lista_siglas': lista_siglas,
        }
        return JsonResponse(data, safe=False)


class Form_Cad_Comp_Grupo_Disp_Frota_View(View):
    def get(self, request):
        lista_grupos = list(Grupo_Indisponibilidade.objects.all().values())

        data = dict()
        data = {
            'lista_grupos': lista_grupos,
        }
        return JsonResponse(data, safe=False)



class Cad_Comp_Sigla_Disp_Frota_View(View):
    def get_object(self, pk):
        try:
            return Sigla_Status_Disponibilidade_Frota.objects.get(pk=pk)
        except Sigla_Status_Disponibilidade_Frota.DoesNotExist:
            raise Http404

    def post(self, request):
        sigla_form = request.POST['sigla']
        desc_sigla_form = request.POST['desc_sigla']

        obj_sigla = Sigla_Status_Disponibilidade_Frota(
            sigla=sigla_form,
            desc_sigla=desc_sigla_form
        )
        obj_sigla.save()
        msg = 'Registro salvo com sucesso';
        data = dict()
        data = {
            'msg': msg,
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_sigla = self.get_object(pk)
        lista_lanc_apont_promax = Apontamento_Promax.objects.filter(cod_sigla=obj_sigla)
        if len(lista_lanc_apont_promax) > 0:
            msg = 'Não é possivel excluir a sigla, pois ela possui registros no apontamento do promax!'
        else:
            obj_sigla.delete()
            msg='Registro excluído com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)



class Cad_Comp_Grupo_Disp_Frota_View(View):
    def get_object(self, pk):
        try:
            return Grupo_Indisponibilidade.objects.get(pk=pk)
        except Grupo_Indisponibilidade.DoesNotExist:
            raise Http404

    def post(self, request):
        desc_grupo_form = request.POST['desc_grupo']

        obj_sigla = Grupo_Indisponibilidade(
            desc_grupo_indisp=desc_grupo_form
        )
        obj_sigla.save()
        msg = 'Registro salvo com sucesso';
        data = dict()
        data = {
            'msg': msg,
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_grupo = self.get_object(pk)
        msg = ''
        lista_lanc_apont_promax = Apontamento_Promax.objects.filter(cod_grupo_indisponibilidade=obj_grupo)
        if len(lista_lanc_apont_promax) > 0:
            msg = 'Não é possivel excluir o grupo, pois ele possui registros no apontamento do promax!'
        else:
            obj_grupo.delete()
            msg='Registro excluído com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)



class Form_Pesq_Apontamento_Promax(View):
    def get_object(self, pk):
        try:
            return Apontamento_Promax.objects.get(pk=pk)
        except Apontamento_Promax.DoesNotExist:
            raise Http404

    def post(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_projetos_pesq = None
        indica_obj_pesquisado = ''
        if usuario_portal.corporativo == 'S':
            indica_obj_pesquisado = 'C'
            lista_projetos_pesq = list(Projeto.objects.filter(data_inativado__isnull=True,
                                                    cod_atividade__desc2_atividade__in=['Rota', 'AS'])
                                       .values('cod_projeto', 'desc_proj'))


        else:
            indica_obj_pesquisado = 'U'
            lista_projetos_pesq = list(Proj_Usu.objects.filter(cod_usu=usuario_portal,
                                                     cod_projeto__cod_atividade__desc2_atividade__in=['Rota', 'AS'],
                                                     cod_projeto__data_inativado__isnull=True,
                                                     cod_projeto__cod_empresa__cod_empresa = 12,
                                                     status_proj_usu='S')
                                       .values('cod_projeto__cod_projeto', 'cod_projeto__desc_proj'))


        data = dict()
        data = {
            'lista_projetos': lista_projetos_pesq,
            'indica_obj_pesquisado': indica_obj_pesquisado
        }
        return JsonResponse(data, safe=False)

    def get(self, request):
        cod_proj = request.GET['cod_proj']
        periodo = request.GET['periodo']

        mes = periodo.split('-')[1]
        ano = periodo.split('-')[0]

        obj_projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
        lista_apontamentos_promax_importados = list(Apontamento_Promax.objects.filter(cod_projeto=obj_projeto,
                                                                                 data_apontamento__month=mes,
                                                                                 data_apontamento__year=ano)
                                                    .values('cod_apontamento_promax', 'data_apontamento', 'placa',
                                                            'status_placa', 'numero_os', 'justificativa', 'status_lanc',
                                                            'cod_sigla__sigla', 'cod_projeto__desc_proj',
                                                            'cod_grupo_indisponibilidade__desc_grupo_indisp'))
        data = dict()
        data = {
            'lista_apontamentos_promax_importados': lista_apontamentos_promax_importados,
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_lanc_apont_promax = self.get_object(pk)
        obj_lanc_apont_promax.status_lanc = 'E'
        obj_lanc_apont_promax.save(update_fields=['status_lanc'])
        msg='Registro estornado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)















