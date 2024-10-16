import locale
from datetime import datetime

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.calendario_app.models import Calendario_Dias
from apps.plan_controle_folha_pag_analitico_app.models import Confirma_Periodo_Fechamento_Folha
from apps.estrut_org_app.models import Filial, Projeto
from apps.usuario_app.models import Usuario, Proj_Usu, Liberacao_Usuario_Projeto_Benner
from apps.conecta_senior_app.models import Registro_Folha_Pagamento
from apps.conecta_senior_app.views import Conexao_Senior_BD


class Form_Libera_Periodo_Fechamento_Folha_View(View):
    def get(self, request):
        data_hora_atual = datetime.now()
        ano_atual = data_hora_atual.strftime('%Y')
        obj_calendario = Calendario_Dias.objects.filter(ano_competencia_periodo=ano_atual).distinct()\
                              .values('ano_competencia_periodo','mes_competencia_periodo')
        lista_competencias = []
        for reg in obj_calendario:
            obj_comp_liberada = Confirma_Periodo_Fechamento_Folha.objects.filter(
                ano_competencia_periodo=reg['ano_competencia_periodo'],
                mes_competencia_periodo=reg['mes_competencia_periodo']
            ).first()
            ativa = ''
            if obj_comp_liberada != None:
                acao_obj = obj_comp_liberada.ativa
                if acao_obj == 'S':
                    ativa = " checked='checked'"
            comp = {
                'mes_competencia_periodo': reg['mes_competencia_periodo'],
                'ano_competencia_periodo': reg['ano_competencia_periodo'],
                'acao': ativa
            }
            lista_competencias.append(comp)

        context = {
            'lista_competencias': lista_competencias,
            'desc_menu_principal' : 'Confirma Período Fechamento Folha',
            'id_menu_pai' : 58
        }
        return render(request, 'plan_controle_folha_pag_analitico_app/form_libera_periodo_fechamento_folha.html',
                      context)



class Pesq_Periodo_Fechamento_Folha_View(View):
    def get(self, request):
        ano_form = request.GET['ano']

        obj_calendario = Calendario_Dias.objects.filter(ano_competencia_periodo=ano_form).distinct() \
            .values('ano_competencia_periodo','mes_competencia_periodo')

        lista_competencias = []
        for reg in obj_calendario:
            obj_comp_liberada = Confirma_Periodo_Fechamento_Folha.objects.filter(
                ano_competencia_periodo=reg['ano_competencia_periodo'],
                mes_competencia_periodo=reg['mes_competencia_periodo']
            ).first()
            ativa = ''
            if obj_comp_liberada != None:
                acao_obj = obj_comp_liberada.ativa
                if acao_obj == 'S':
                    ativa = " checked='checked'"
            comp = {
                'mes_competencia_periodo': reg['mes_competencia_periodo'],
                'ano_competencia_periodo': reg['ano_competencia_periodo'],
                'acao': ativa
            }
            lista_competencias.append(comp)
        data = dict()
        data = {
            'lista_competencias': lista_competencias
        }
        return JsonResponse(data, safe=False)


class Cad_Liberacao_Comp_Fecha_Folha_View(View):
    def post(self, request):
        competencia_form = request.POST['competencia']
        ano_form = request.POST['ano']
        acao_form = request.POST['acao']

        obj_comp_liberada = Confirma_Periodo_Fechamento_Folha.objects.filter(
            ano_competencia_periodo=ano_form,
            mes_competencia_periodo=competencia_form
        ).first()
        if obj_comp_liberada != None:
            obj_comp_liberada.ativa = acao_form
            obj_comp_liberada.save(update_fields=['ativa'])
        else:
            add_obj_comp_liberada =  Confirma_Periodo_Fechamento_Folha(
                mes_competencia_periodo = competencia_form,
                ano_competencia_periodo = ano_form,
                ativa = acao_form
            ).save()
        if acao_form == 'S':
            msg = 'Liberado'
        else:
            msg = 'Bloqueado'
        #Dicionario
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Form_Rel_Folha_Pagamento_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.get(pk=id_usu_session)
        #lista_projetos = Proj_Usu.objects.filter(cod_usu=obj_usuario, status_proj_usu_folha_pag='S')
        lista_periodos_liberados = Confirma_Periodo_Fechamento_Folha.objects.filter(ativa='S')
        lista_projetos_pagina = Liberacao_Usuario_Projeto_Benner.objects.filter(cod_usu=obj_usuario, ativo_app_folha_pagamento='S')

        context = {
            'lista_periodos_liberados': lista_periodos_liberados,
            'lista_projetos_pagina': lista_projetos_pagina,
            'desc_menu_principal' : 'Rel. Folha Pagamento',
            'id_menu_pai' : 58
        }
        return render(request, 'plan_controle_folha_pag_analitico_app/form_rel_folha_pagamento.html', context)

class Gera_Rel_Folha_Pagamento_View(View):
    def get(self, request):
        cod_comp_form = request.GET['cod_competencia']
        lista_handle_proj_form = request.GET['lista_handle_proj']

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        obj_competencia = Confirma_Periodo_Fechamento_Folha.objects.get(pk=cod_comp_form)
        str_data_ref = str(obj_competencia.ano_competencia_periodo) + '/' + \
            str(obj_competencia.mes_competencia_periodo) + \
            '/1'
        dados_folha = []
        lista_handle_projetos_conlog = []
        lista_handle_projetos_deep = []
        for proj_emp in lista_handle_proj_form.split(','):
            if proj_emp.split('_')[1] == '12':
                lista_handle_projetos_conlog.append(proj_emp.split('_')[0])
            elif proj_emp.split('_')[1] == '17':
                lista_handle_projetos_deep.append(proj_emp.split('_')[0])

        df_dados_folha_pag = None
        df_dados_folha_pag_conlog = None
        if len(lista_handle_projetos_conlog) > 0:
            df_dados_folha_pag_conlog = (Conexao_Senior_BD(12)
                                         .retorna_df_folha_pagamento(str_data_ref, lista_handle_projetos_conlog))

        df_dados_folha_pag_deep = None
        if len(lista_handle_projetos_deep) > 0:
            df_dados_folha_pag_deep = (Conexao_Senior_BD(17)
                                       .retorna_df_folha_pagamento(str_data_ref, lista_handle_projetos_deep))

        df_dados_folha_pag = pd.concat([df_dados_folha_pag_conlog, df_dados_folha_pag_deep]).reset_index()

        '''if df_dados_folha_pag_conlog != None and  df_dados_folha_pag_deep != None:
            
        elif df_dados_folha_pag_conlog != None and  df_dados_folha_pag_deep == None:
            df_dados_folha_pag = df_dados_folha_pag_conlog
        elif df_dados_folha_pag_conlog == None and  df_dados_folha_pag_deep != None:
            df_dados_folha_pag = df_dados_folha_pag_deep'''


        for index, row in df_dados_folha_pag.iterrows():
                if df_dados_folha_pag.loc[index, 'mat_colab'] != None:
                    reg = Registro_Folha_Pagamento(
                        matricula_colab = str(df_dados_folha_pag.loc[index, 'mat_colab']),
                        nome_colab = str(df_dados_folha_pag.loc[index, 'nome_colab']),
                        desc_cargo = str(df_dados_folha_pag.loc[index, 'desc_cargo']),
                        desc_filial = str(df_dados_folha_pag.loc[index, 'nome_filial']),
                        desc_projeto = str(df_dados_folha_pag.loc[index, 'nome_projeto']),
                        desc_conta_contabil = str(df_dados_folha_pag.loc[index, 'desc_conta_contabil']),
                        cod_evento = str(df_dados_folha_pag.loc[index, 'cod_evento']),
                        desc_evento = str(df_dados_folha_pag.loc[index, 'evento']),
                        proeventos = locale.currency(round(df_dados_folha_pag.loc[index, 'val_evento'], 2), grouping=True, symbol=None),
                        hora_min_ref = locale.currency(round(df_dados_folha_pag.loc[index, 'horas_ref'], 2), grouping=True, symbol=None),
                        desc_sit_atual = str(df_dados_folha_pag.loc[index, 'desc_atual_sit'])
                    )
                    dados_folha.append(reg.__dict__)

        data = dict()
        data = {
            'msg': 'ok',
            'dados_folha_pag': dados_folha
        }
        return JsonResponse(data, safe=False)

class Form_Libera_Proj_Usu_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.get(pk=id_usu_session)

        lista_usuarios_ativos = (Usuario.objects
                                 .filter(status_usu='A', cod_filial__cod_empresa = obj_usuario.cod_filial.cod_empresa))
        lista_empresas_benner = ConexaoBancoBenner().retornaEmpresasBenner()
        lista_operacoes_benner = ConexaoBancoBenner().retornaTodasOperacoesBenner()
        #lista_filiais_benner = ConexaoBancoBenner().retornaTodasFilialBenner()
        #lista_projetos_benner = ConexaoBancoBenner().retornaTodosProjetosBenner()
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.get(pk=id_usu_session)
        lista_projetos_pagina = []
        if obj_usuario.cod_filial.cod_empresa.cod_empresa == 12:
            lista_projetos = list(Liberacao_Usuario_Projeto_Benner.objects
                                  .filter(cod_empresa=12)
                                  .values('handle_benner', 'desc_proj_benner', 'cod_empresa').distinct())
            for proj in lista_projetos:
                reg = {
                    'handle_benner': proj['handle_benner'],
                    'desc_proj_benner': proj['desc_proj_benner'],
                    'cod_empresa': proj['cod_empresa'],
                    'nome_empresa': 'CONLOG'
                }
                lista_projetos_pagina.append(reg)
        elif obj_usuario.cod_filial.cod_empresa.cod_empresa == 17:
            lista_projetos = list(Liberacao_Usuario_Projeto_Benner.objects
                                  .filter(cod_empresa=17)
                                  .values('handle_benner', 'desc_proj_benner', 'cod_empresa').distinct())
            for proj in lista_projetos:
                reg = {
                    'handle_benner': proj['handle_benner'],
                    'desc_proj_benner': proj['desc_proj_benner'],
                    'cod_empresa': proj['cod_empresa'],
                    'nome_empresa': 'DEEP'
                }
                lista_projetos_pagina.append(reg)
            ''' 
            60	- DEPOT - IOA
            869	- ARMAZÉM - IOA
            910 - ADMINISTRATIVO - CAL
            912 - OPERACIONAL - CAL
            915 - ADMINISTRATIVO - UTS
            916 - OPERACIONAL - UTS
            143 - OPERACIONAL UEL - GLD
            300 - ADMINISTRATIVO - GLD
            1060 - OPERACIONAL RIO BRILHANTE - GLD
            '''
            lista_projetos_conlog = list(Liberacao_Usuario_Projeto_Benner.objects
                                         .filter(handle_benner__in=[60, 869, 910, 912, 915, 916, 143, 300, 1060])
                                         .values('handle_benner', 'desc_proj_benner', 'cod_empresa').distinct())
            for proj in lista_projetos_conlog:
                reg = {
                    'handle_benner': proj['handle_benner'],
                    'desc_proj_benner': proj['desc_proj_benner'],
                    'cod_empresa': proj['cod_empresa'],
                    'nome_empresa': 'CONLOG'
                }
                lista_projetos_pagina.append(reg)
        context = {
            'lista_usuarios_ativos': lista_usuarios_ativos,
            'lista_empresas_benner': lista_empresas_benner,
            'lista_operacoes_benner': lista_operacoes_benner,
            #'lista_filiais_benner': lista_filiais_benner,
            'lista_projetos_benner': lista_projetos_pagina,
            'desc_menu_principal' : 'Libera Projetos x Usuários',
            'id_menu_pai' : 58
        }
        return render(request, 'plan_controle_folha_pag_analitico_app/form_libera_projetos_usuario_folha_pag.html', context)

class Form_Libera_Proj_Usu_Tab_Usu_View(View):
    def get(self, request):
        cod_usu_form = request.GET['cod_usuario']
        obj_usu = Usuario.objects.get(pk=cod_usu_form)
        lista_liberacoes_usu = list(Liberacao_Usuario_Projeto_Benner.objects.filter(cod_usu=obj_usu)
                                    .values('cod_libera_usu_proj', 'handle_benner', 'desc_proj_benner',
                                            'cod_empresa', 'ativo_app_folha_pagamento'))
        data = dict()
        data = {
            'lista_liberacoes_usu': lista_liberacoes_usu
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_liberacao_form = request.POST['cod_liberacao']
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        msg = ''
        if cod_liberacao_form == '0':
            cod_usuario_form = request.POST['cod_usuario']
            lista_projetos_form = request.POST['lista_projetos'].split(',')
            obj_usuario = Usuario.objects.get(pk=cod_usuario_form)
            for proj in lista_projetos_form:
                handle = proj.split('_')[0]
                cod_empresa = proj.split('_')[2]
                if handle != '0' and len(lista_projetos_form) > 0:
                    desc_proj = proj.split('_')[1]
                    obj_liberacao = Liberacao_Usuario_Projeto_Benner.objects.filter(cod_usu=obj_usuario, handle_benner=handle).first()
                    if obj_liberacao != None:
                        obj_liberacao.ativo_app_folha_pagamento = 'S'
                        obj_liberacao.save()
                    else:
                        nova_liberacao = Liberacao_Usuario_Projeto_Benner(
                            handle_benner = handle,
                            desc_proj_benner = desc_proj,
                            ativo_app_folha_pagamento = 'S',
                            cod_usu = obj_usuario,
                            cod_empresa= cod_empresa
                        )
                        nova_liberacao.save()
                    msg =  'Liberações efetuadas !!!'
                else:
                    msg = 'Informe o(s) Projetos(s) para liberação !!!'
        else:
            acao_form = request.POST['acao']
            obj_liberacao = Liberacao_Usuario_Projeto_Benner.objects.get(pk=cod_liberacao_form)
            obj_liberacao.ativo_app_folha_pagamento = acao_form
            obj_liberacao.save()
            if acao_form == 'S':
                msg = 'Projeto liberado !!!'
            else:
                msg = 'Projeto bloqueado !!!'
        data = dict()
        data = {
            'msg': msg,
        }
        return JsonResponse(data, safe=False)

class Form_Libera_Proj_Usu_Tab_Proj_View(View):
    def get(self, request):
        handle_proj_form = request.GET['handle_proj']
        lista_liberacoes_proj = list(Liberacao_Usuario_Projeto_Benner.objects.filter(handle_benner=handle_proj_form)
                                     .values('cod_libera_usu_proj', 'cod_usu__nome_usu', 'ativo_app_folha_pagamento'))
        data = dict()
        data = {
            'lista_liberacoes_proj': lista_liberacoes_proj
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_liberacao_form = request.POST['cod_liberacao']
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        msg = ''
        if cod_liberacao_form == '0':
            dados_proj_form = request.POST['dados_proj']
            lista_usuarios_form = request.POST['lista_usuarios'].split(',')
            for usu in lista_usuarios_form:
                if usu != '0' and len(lista_usuarios_form) >0:
                    handle = dados_proj_form.split('_')[0]
                    desc_proj = dados_proj_form.split('_')[1]
                    obj_usuario = Usuario.objects.get(pk=usu)
                    obj_liberacao = Liberacao_Usuario_Projeto_Benner.objects.filter(cod_usu=obj_usuario, handle_benner=handle).first()
                    if obj_liberacao != None:
                        obj_liberacao.ativo_app_folha_pagamento = 'S'
                        obj_liberacao.save()
                    else:
                        nova_liberacao = Liberacao_Usuario_Projeto_Benner(
                            handle_benner = handle,
                            desc_proj_benner = desc_proj,
                            ativo_app_folha_pagamento = 'S',
                            cod_usu = obj_usuario,
                            cod_empresa=obj_usuario_logado.cod_filial.cod_empresa.cod_empresa
                        )
                        nova_liberacao.save()
                    msg =  'Liberações efetuadas !!!'
                else:
                    msg = 'Informe o(s) Usuário(s) para liberação !!!'
        else:
            acao_form = request.POST['acao']
            obj_liberacao = Liberacao_Usuario_Projeto_Benner.objects.get(pk=cod_liberacao_form)
            obj_liberacao.ativo_app_folha_pagamento = acao_form
            obj_liberacao.save()
            if acao_form == 'S':
                msg = 'Usuário liberado !!!'
            else:
                msg = 'Usuário bloqueado !!!'
        data = dict()
        data = {
            'msg': msg,
        }
        return JsonResponse(data, safe=False)


'''class Comp_Select_Empresa_View(View):
    def get(self, request):
        cod_empresa_frm = request.GET['cod_empresa']
        

        data = dict()
        data = {
            'lista_projetos': lista_projetos
        }
        return JsonResponse(data, safe=False)'''














