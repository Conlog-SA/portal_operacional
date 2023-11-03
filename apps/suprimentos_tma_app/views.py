import locale
from datetime import datetime

import pyodbc
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.calendario_app.models import Calendario_Dias
from apps.estrut_org_app.models import Filial, Empresa
from apps.suprimentos_rel_filial_comprador_app.models import Relacao_Filial_Comprador
from apps.suprimentos_tma_app.models import Requisicao_Atendida_TMA


class Form_Requisicao_Gera_Tma_View(View):
    def get(self, request):
        context = {
            'desc_menu_principal': 'Gera TMA',
            'id_menu_pai': 45
        }
        return render(request, 'suprimentos_tma_app/form_requisicoes_gera_tma.html', context)


class Requisicao_Atendida_View(View):
    def get(self, request):
        data_inicial = request.GET['data_ini']
        data_fim = request.GET['data_fim']
        lista_req_atendidas = []
        msg = ''
        # locale.setlocale(locale.LC_TIME, 'pt-BR')
        # timezone.now()

        '''conn_producao = pyodbc.connect('DRIVER={SQL Server};'
                                       'SERVER=CDA-SRV-MSSQL-2;'
                                       'DATABASE=TRANSPORTES_PRODUCAO;'
                                       'UID=sa;'
                                       'PWD=@#tp4m800p7;')'''
        conexaoBancoBenner = ConexaoBancoBenner()
        lista_req_atendidas = conexaoBancoBenner.retorna_requisicoes_atendidas_tma(data_inicial, data_fim)

        '''try:
            conn_producao = pyodbc.connect('DRIVER={SQL Server};'
                                           'SERVER=CDA-SRV-MSSQL-2;'
                                           'DATABASE=TRANSPORTES_PRODUCAO;'
                                           'UID=sa;'
                                           'PWD=@#tp4m800p7;')
            conexaoBancoBenner = ConexaoBancoBenner(conn_producao)
            lista_req_atendidas = conexaoBancoBenner.retorna_requisicoes_atendidas_tma(data_inicial, data_fim)
        except:
            msg = 'Erro ao conectar com o Benner. Verifique com o Administrador do sistema!'
            '''

        tab_req_atendidas = []
        for req in lista_req_atendidas:

            obj_req_atendida_busca = Requisicao_Atendida_TMA.objects.filter(
                chave_busca=str(req.handle_req_pai) + str(req.handle_filial) + str(req.handle_familia) + str(
                    req.cod_comprador)).first()

            if obj_req_atendida_busca == None:

                obj_filial = Filial.objects.filter(handle_benner=req.handle_filial).first()
                if obj_filial == None:
                    obj_filial = Filial(
                        cod_operacao = None,
                        cod_empresa = Empresa.objects.filter(handle_benner=req.cod_empresa).first(),
                        cnpj_filial = req.cnpj_filial,
                        desc_filial = req.nome_filial,
                        handle_benner = req.handle_filial,
                        estrutura_benner = '',
                        unidade_abrev = '',
                        cod_filial_senior = 0,
                        cod_promax = 0,
                        cod_filial_tracking = 0,
                        ativo = 1,
                        regiao = None,
                        handle_gn_proj_benner = None
                    )
                    obj_filial.save()


                obj_atendente = None
                obj_filial_comprador = Relacao_Filial_Comprador.objects.filter(cod_filial=obj_filial) \
                    .extra(where=[" '" + str(req.data_confirmada) + "' BETWEEN data_ini AND data_fim OR " +
                                  " '" + str(req.data_confirmada) + "' > data_ini AND data_fim is null "]).first()
                if obj_filial_comprador != None:
                    obj_atendente = obj_filial_comprador.cod_usu

                req.nome_filial = obj_filial.desc_filial
                obj_dia_calendario = Calendario_Dias.objects.filter(data_dia=req.data_confirmada).first()

                prazo_atendida_dias_previsto = 0
                '''if req.planejado == 'S':
                    req.data_atendida_prevista = obj_dia_calendario.data_prevista_req_plan
                    prazo_atendida_dias_previsto = 20
                elif req.status_ordem == 'E' and req.planejado == 'N': #elif req.planejado == 'N' and req.status_ordem == 'E':
                    req.data_atendida_prevista = obj_dia_calendario.data_prevista_req_e
                    prazo_atendida_dias_previsto = 2
                elif req.status_ordem == 'NE' and req.planejado == 'N':
                    req.data_atendida_prevista = obj_dia_calendario.data_prevista_req_ne
                    prazo_atendida_dias_previsto = 4'''

                if req.status_ordem == 'P':
                    req.data_atendida_prevista = obj_dia_calendario.data_prevista_req_plan
                    prazo_atendida_dias_previsto = obj_dia_calendario.qtd_dias_data_prevista_req_plan
                elif req.status_ordem == 'E':  # elif req.planejado == 'N' and req.status_ordem == 'E':
                    req.data_atendida_prevista = obj_dia_calendario.data_prevista_req_e
                    prazo_atendida_dias_previsto = obj_dia_calendario.qtd_dias_data_prevista_req_e
                elif req.status_ordem == 'NE':
                    req.data_atendida_prevista = obj_dia_calendario.data_prevista_req_ne
                    prazo_atendida_dias_previsto = obj_dia_calendario.qtd_dias_data_prevista_req_ne

                '''
                    TMA em horas 
                    calc_tma_aux = req.data_atendida - req.data_confirmada
                    sec_tma = int(calc_tma_aux.total_seconds())
                    dias_tma, sec_tma = divmod(sec_tma, 24 * 3600)
                    horas_tma, sec_tma = divmod(sec_tma, 3600)
                    min_tma, sec_tma = divmod(sec_tma, 60)
                    req.tma = str(dias_tma)+':'+str(horas_tma)+':'+str(min_tma)            

                '''

                status_atendimento_calc = 'P'
                req.status_atendimento = 'No Prazo'
                data_time_atendida_prevista_str = str(req.data_atendida_prevista) + ' 23:59'
                data_time_atendida_prevista_datetime = datetime.strptime(data_time_atendida_prevista_str,
                                                                         '%Y-%m-%d %H:%M')
                req.data_atendida_prevista = data_time_atendida_prevista_datetime
                if req.data_atendida > data_time_atendida_prevista_datetime:
                    status_atendimento_calc = 'F'
                    req.status_atendimento = 'Fora do Prazo'

                prazo_atendida_dias = Calendario_Dias.objects.filter(
                    data_dia__range=[req.data_confirmada, req.data_atendida], classificacao_dia='U').count()
                req.tma = prazo_atendida_dias

                '''prazo_atendida_dias_previsto = Dia_Calendario.objects.filter(
                    data_dia__range=[req.data_confirmada, req.data_atendida_prevista], classificacao_dia='U'
                ).count() '''
                req.tma_previsto = prazo_atendida_dias_previsto

                obj_req_atendidas = Requisicao_Atendida_TMA(
                    handle_req_pai=req.handle_req_pai,
                    num_req_pai=req.num_req_pai,
                    data_inclusao=req.data_inclusao,  # datetime.strptime(req.data_inclusao, '%d-%m-%Y %HH:%MM'),
                    data_confirmada=req.data_confirmada,  # datetime.strptime(req.data_confirmada, '%d-%m-%Y %HH:%MM'),
                    data_atendida=req.data_atendida,  # datetime.strptime(req.data_atendida, '%d-%m-%Y %HH:%MM'),
                    handle_usu_incluiu=req.handle_usu_incluiu,
                    nome_usu_incluiu=req.nome_usu_incluiu,
                    handle_comprador=req.cod_comprador,
                    nome_comprador=req.nome_comprador,
                    handle_familia=req.handle_familia,
                    desc_familia=req.desc_familia,
                    status_ordem=req.status_ordem,
                    status_atendimento=status_atendimento_calc,
                    tma=req.tma,
                    tma_previsto=req.tma_previsto,
                    chave_busca=str(req.handle_req_pai) + str(req.handle_filial) + str(req.handle_familia) + str(
                        req.cod_comprador),
                    cod_dia_calendario=obj_dia_calendario,
                    cod_usu=obj_atendente,
                    cod_filial=obj_filial
                )
                obj_req_atendidas.save()
                req.status_importacao = 'Importado'

            else:
                if obj_req_atendida_busca.cod_usu != None:
                    req.cod_comprador = obj_req_atendida_busca.cod_usu.cod_usu
                    req.nome_comprador = obj_req_atendida_busca.cod_usu.nome_usu
                else:
                    obj_filial_comprador = Relacao_Filial_Comprador.objects.filter(
                        cod_filial=obj_req_atendida_busca.cod_filial.cod_filial) \
                        .extra(where=[" '" + str(req.data_confirmada) + "' BETWEEN data_ini AND data_fim OR " +
                                      " '" + str(req.data_confirmada) + "' > data_ini AND data_fim is null "]).first()
                    if obj_filial_comprador != None:
                        obj_atendente = obj_filial_comprador.cod_usu
                        req.cod_comprador = obj_atendente.cod_usu
                        req.nome_comprador = obj_atendente.nome_usu
                        obj_req_atendida_busca.cod_usu = obj_atendente
                req.nome_filial = obj_req_atendida_busca.cod_filial.desc_filial
                req.status_importacao = 'Atualizado'

                data_time_atendida_prevista_datetime = ''
                prazo_atendida_dias_previsto = 0
                if req.status_ordem == 'P':
                    # req.data_atendida_prevista = obj_req_atendida_busca.cod_dia_calendario.data_prevista_req_plan
                    data_time_atendida_prevista_str = str(
                        obj_req_atendida_busca.cod_dia_calendario.data_prevista_req_plan) + ' 23:59'
                    data_time_atendida_prevista_datetime = datetime.strptime(data_time_atendida_prevista_str,
                                                                             '%Y-%m-%d %H:%M')
                    prazo_atendida_dias_previsto = 20
                elif req.status_ordem == 'E':
                    # req.data_atendida_prevista = obj_req_atendida_busca.cod_dia_calendario.data_prevista_req_e
                    data_time_atendida_prevista_str = str(
                        obj_req_atendida_busca.cod_dia_calendario.data_prevista_req_e) + ' 23:59'
                    data_time_atendida_prevista_datetime = datetime.strptime(data_time_atendida_prevista_str,
                                                                             '%Y-%m-%d %H:%M')
                    prazo_atendida_dias_previsto = 2
                elif req.status_ordem == 'NE':
                    # req.data_atendida_prevista = obj_req_atendida_busca.cod_dia_calendario.data_prevista_req_ne
                    data_time_atendida_prevista_str = str(
                        obj_req_atendida_busca.cod_dia_calendario.data_prevista_req_ne) + ' 23:59'
                    data_time_atendida_prevista_datetime = datetime.strptime(data_time_atendida_prevista_str,
                                                                             '%Y-%m-%d %H:%M')
                    prazo_atendida_dias_previsto = 4
                req.data_atendida_prevista = data_time_atendida_prevista_datetime

                obj_req_atendida_busca.status_ordem = req.status_ordem
                obj_req_atendida_busca.tma_previsto = prazo_atendida_dias_previsto
                obj_req_atendida_busca.save(update_fields=['cod_usu', 'tma_previsto', 'status_ordem'])

                if obj_req_atendida_busca.status_atendimento == 'P':
                    req.status_atendimento = 'No Prazo'
                else:
                    req.status_atendimento = 'Fora do Prazo'

                req.tma = obj_req_atendida_busca.tma
                req.tma_previsto = obj_req_atendida_busca.tma_previsto

            data_confirmada_formatada = req.data_confirmada.strftime('%d/%m/%Y %H:%M')
            req.data_confirmada = data_confirmada_formatada

            data_prevista_formatada = req.data_atendida_prevista.strftime('%d/%m/%Y %H:%M')
            req.data_atendida_prevista = data_prevista_formatada

            data_atendida_formatada = req.data_atendida.strftime('%d/%m/%Y %H:%M')
            req.data_atendida = data_atendida_formatada

            # req.num_req_pai = str(req.handle_req) + str(req.handle_prod) + str(req.handle_filial)

            tab_req_atendidas.append(req.__dict__)

        data = dict()
        data = {
            'tab_req_atendidas': tab_req_atendidas,
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        lista_req_comprador_null = Requisicao_Atendida_TMA.objects.filter(cod_usu__isnull=True)
        for req in lista_req_comprador_null:
            obj_filial_comprador = Relacao_Filial_Comprador.objects.filter(cod_filial=req.cod_filial) \
                .extra(where=[" '" + str(req.data_confirmada) + "' BETWEEN data_ini AND data_fim OR " +
                              " '" + str(req.data_confirmada) + "' > data_ini AND data_fim is null "]).first()
            req.cod_us = obj_filial_comprador
            req.save(update_fields=['cod_usu'])
        data = dict()
        data = {

        }
        return JsonResponse(data, safe=False)

