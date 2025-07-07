import os
import locale
import decimal
from datetime import datetime, date
import json
from math import trunc

import pandas as pd
import xlrd
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from django.http import JsonResponse, Http404, FileResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.estrut_org_app.models import Projeto
from apps.plan_controle_fat_2art_terc_app.models import BeneficiarioTerceiro, Registro2ArtTerceirosFinanceiro, \
    HistAcaoMapas2ArtTerceiros, CadastroPlacaTerceiro, CadFreteSpot, TipoOcorrenciasFinanceiroTerceiros, \
    Pagamento2ArtTerceirosFinanceiro, LancamentosRegistro2ArtTerceirosFinanceiro, Tab_Cad_Placa_Terc_Financ, \
    LinhaExcelArquivoLanAcresDesc, LinhaExcelArquivoPagamentosExtra, LancamentoPagamentoExtras, \
    Tab_Pagamentos_Terceiros, Render, Tab_Lancamentos_Pagamento_Terceiros, Estorno_Pagamentos_2Art_Terc, \
    Arq_Update_Cad_Frete
from apps.plan_controle_fat_2art_terc_app.uteis import Uteis
from apps.usuario_app.models import Usuario, Proj_Usu
from proj_portal_operacional import settings
from proj_portal_operacional.settings import BASE_DIR


class Form_Gerar_Pag_2Art_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        lista_projetos = Proj_Usu.objects.filter(cod_usu=obj_usuario_sessao,
                                               cod_projeto__cod_atividade__desc2_atividade='Terceiro',
                                               cod_projeto__data_inativado__isnull=True,
                                               status_proj_usu='S')
        contexto = {
            'lista_projetos': lista_projetos,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'plan_controle_fat_2art_terc_app/form_gerar_pag_2art_terc.html', contexto)

    def post(self, request):
        cod_reg_2art_terc_financ = request.POST['cod_reg_2art_terc_financ']

        id_usu_session = request.session['cod_usuario_logado']
        usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_aa = data_hora_atual.strftime('%Y-%m-%d')
        hota_atual = data_hora_atual.strftime('%H:%M')

        obj_reg_2art_ter_financ = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_reg_2art_terc_financ=cod_reg_2art_terc_financ).first()
        obj_reg_2art_ter_financ.transp_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.transp
        obj_reg_2art_ter_financ.entrega_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.entrega
        obj_reg_2art_ter_financ.cargaatual_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.cargaatual
        obj_reg_2art_ter_financ.custospot_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.custospot
        obj_reg_2art_ter_financ.regiaospot_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.regiaospot
        obj_reg_2art_ter_financ.placa_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.placa
        obj_reg_2art_ter_financ.entregas_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.entregas
        obj_reg_2art_ter_financ.valorfrete_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.valorfrete
        obj_reg_2art_ter_financ.tipoimposto_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.tipoimposto
        obj_reg_2art_ter_financ.percimposto_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.percimposto
        obj_reg_2art_ter_financ.valorimposto_2art_tercfinanc = obj_reg_2art_ter_financ.cod_reg_2art.valorimposto
        obj_reg_2art_ter_financ.valorfaturado_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.valorfaturado

        if (obj_reg_2art_ter_financ.nomespot_2art_terc_financ != obj_reg_2art_ter_financ.cod_reg_2art.nomespot) or (
                obj_reg_2art_ter_financ.placa_2art_terc_financ != obj_reg_2art_ter_financ.cod_reg_2art.placa):
            obj_cad_placa_terc = (CadastroPlacaTerceiro.objects
                                  .filter(cod_projeto=obj_reg_2art_ter_financ.cod_projeto,
                                          placa_cad_placa_terc=obj_reg_2art_ter_financ.cod_reg_2art.placa,
                                          perfil_veiculo_cad_placa_terc=obj_reg_2art_ter_financ.cod_reg_2art.nomespot)
                                  .extra(where=["'" + str(obj_reg_2art_ter_financ.data_2art_terc_financ) +
                                                "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first())

            obj_cad_frete_terc = None
            if obj_cad_placa_terc is not None:
                obj_reg_2art_ter_financ.cod_cad_placa_terc = obj_cad_placa_terc
                obj_cad_frete_terc = (CadFreteSpot.objects.filter(cod_projeto=obj_reg_2art_ter_financ.cod_projeto,
                                                                 tipo_perfil_veiculo=obj_reg_2art_ter_financ.cod_reg_2art.nomespot,
                                                                 cod_regiao=obj_reg_2art_ter_financ.regiaospot_2art_terc_financ,
                                                                 tipo_entrega=obj_reg_2art_ter_financ.entrega_2art_terc_financ, )
                                      .extra(where=["'" + str(obj_reg_2art_ter_financ.data_2art_terc_financ) +
                                                    "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first())
                if obj_cad_frete_terc is not None:
                    obj_reg_2art_ter_financ.cod_cad_frete_spot = obj_cad_frete_terc
                else:
                    obj_reg_2art_ter_financ.cod_cad_frete_spot = None
            else:
                obj_reg_2art_ter_financ.cod_cad_placa_terc = None
                obj_reg_2art_ter_financ.cod_cad_frete_spot = None

        obj_reg_2art_ter_financ.nomespot_2art_terc_financ = obj_reg_2art_ter_financ.cod_reg_2art.nomespot
        obj_reg_2art_ter_financ.cod_usu = usuario
        obj_reg_2art_ter_financ.qtd_subscrita_2art_terc_financ += 1
        obj_reg_2art_ter_financ.data_ultima_subscricao_2art_terc_financ = data_atual_yyyy_mm_aa
        obj_reg_2art_ter_financ.save()

        data = dict()
        data = {
            'msg': 'Dados do mapa ' + str(
                obj_reg_2art_ter_financ.mapa_2art_terc_financ) + ', atualizado com sucesso !!!'
        }
        return JsonResponse(data, safe=False)

class Componente_Benef_Terc_View(View):
    def get(self, request):
        cod_projeto_form = request.GET['cod_projeto']
        data_ini_form = request.GET['data_ini']
        data_fim_form = request.GET['data_fim']

        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto_form).first()
        lista_beneficiarios = list(Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_projeto=obj_projeto, data_2art_terc_financ__range=[data_ini_form, data_fim_form])
                                   .values('cod_cad_placa_terc__cod_benef_terc__cod_benef_terc',
                                           'cod_cad_placa_terc__cod_benef_terc__nome_benef_terc',
                                           'cod_cad_placa_terc__cod_benef_terc__doc_benef_terc',
                                           'cod_cad_placa_terc__cod_benef_terc__tipo_pessoa_benef_terc')
                                   .distinct())

        data = dict()
        data = {
            'lista_beneficiarios': lista_beneficiarios
        }
        return JsonResponse(data, safe=False)

class Mapas_Terc_2Art_View(View):
    def get(self, request):
        cod_projeto_form = request.GET['cod_projeto']
        cod_beneficiario_form = request.GET['cod_beneficiario']
        check_mapas_ativos_form = request.GET['check_mapas_ativos']
        data_inicial_form = request.GET['data_inicial']
        data_final_form = request.GET['data_final']

        obj_uteis = Uteis()
        tab_mapas_terceiros = obj_uteis\
            .tab_2art_comparacao_tab_terceiros(cod_projeto_form, data_inicial_form, data_final_form,
                                                                          cod_beneficiario_form, check_mapas_ativos_form)

        data = dict()
        data = {
            'tab_mapas_terceiros': tab_mapas_terceiros
        }
        return JsonResponse(data)

    def post(self, request):
        cod_2art_terc_financ_form = request.POST['cod_2art_terc_financ']
        status_mapa_form = request.POST['status_mapa']
        justificativa_status_mapa_form = request.POST['justificativa_status_mapa']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        obj_2art_terc_financ = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_reg_2art_terc_financ=cod_2art_terc_financ_form).first()
        obj_2art_terc_financ.status_mapa_2art_terc_financ = status_mapa_form
        obj_2art_terc_financ.cod_usu = obj_usuario_sessao
        obj_2art_terc_financ.save()

        obj_hist_acao_mapas_2art_terc = HistAcaoMapas2ArtTerceiros(
            acao_hist_acao_mapa_terc=status_mapa_form,
            obs_hist_acao_mapa_terc=justificativa_status_mapa_form,
            cod_usu=obj_usuario_sessao,
            cod_reg_2art_terc_financ=obj_2art_terc_financ
        )
        obj_hist_acao_mapas_2art_terc.save()

        status_mapa = 'ativado'
        if status_mapa_form == 'N':
            status_mapa = 'desativado'
        data = dict()
        data = {
            'msg': 'Mapa ' + str(obj_2art_terc_financ.mapa_2art_terc_financ) + ', ' + status_mapa + ' com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Btn_Form_Gerar_Pag_2Art_View(View):
    def get(self, request):
        nome_componente_form = request.GET['nome_componente']

        data = dict()
        if nome_componente_form == 'btn_verifica_placas_inativas_benner':
            cod_proj_form = request.GET.get('cod_proj')
            data_ini_form = request.GET.get('data_ini')
            data_fim_form = request.GET.get('data_fim')

            obj_proj = Projeto.objects.get(pk=cod_proj_form)
            lista_placas_2art_periodo = Registro2ArtTerceirosFinanceiro.objects.filter(
                cod_projeto=obj_proj, data_2art_terc_financ__range=[data_ini_form, data_fim_form],
                status_financeiro_2art_terc_financ='A', cod_pag_2art_terc_financ__isnull=True
            )
            # status_mapa_2art_terc_financ = 'S'
            lista_placas_inativas_benner = []
            for p in lista_placas_2art_periodo:
                placas_benner = ConexaoBancoBenner().retorna_dados_placa_benef_a_sincronizar(
                    obj_proj.handle_benner, p.placa_2art_terc_financ, p.nomespot_2art_terc_financ)
                if len(placas_benner) > 0:
                    for placa in placas_benner:
                        if (placa.status_placa == 'S' and p.status_mapa_2art_terc_financ == 'S') \
                                or (placa.status_placa == 'N' and p.status_mapa_2art_terc_financ == 'N'):
                            reg = {
                                'cod_reg_2art_terc_financ': p.cod_reg_2art_terc_financ,
                                'data_2art_terc_financ': p.data_2art_terc_financ,
                                'placa_2art_terc_financ': p.placa_2art_terc_financ,
                                'mapa_2art_terc_financ': p.mapa_2art_terc_financ,
                                'nome_benef': p.cod_cad_placa_terc.cod_benef_terc.nome_benef_terc,
                                'status_mapa_2art_terc_financ': p.status_mapa_2art_terc_financ,
                                'status_benner': placa.status_placa
                            }
                            lista_placas_inativas_benner.append(reg)
            data = {
                'lista_placas_inativas_benner': lista_placas_inativas_benner,
            }
        elif nome_componente_form == 'btn_sincroniza_beneficiarios_benner':
            cod_proj_form = request.GET.get('cod_proj')
            data_ini_form = request.GET.get('data_ini')
            data_fim_form = request.GET.get('data_fim')

            obj_proj = Projeto.objects.get(pk=cod_proj_form)
            list_placas_terc_sem_cad = Registro2ArtTerceirosFinanceiro.objects \
                .filter(cod_projeto=obj_proj,
                        data_2art_terc_financ__range=[data_ini_form, data_fim_form],
                        cod_cad_placa_terc__isnull=True) \
                .values('placa_2art_terc_financ', 'nomespot_2art_terc_financ').distinct()

            lista_dados_tab_placa_a_sincronizar = []
            for p in list_placas_terc_sem_cad:
                lista_dados_benner_placa_a_sincronizar = ConexaoBancoBenner().retorna_dados_placa_benef_a_sincronizar(
                    obj_proj.handle_benner, p['placa_2art_terc_financ'], p['nomespot_2art_terc_financ'])
                for reg in lista_dados_benner_placa_a_sincronizar:
                    obj_benef_pesq = BeneficiarioTerceiro.objects.filter(handle_benner=reg.handle_benef).first()
                    if obj_benef_pesq != None:
                        reg.status_cadastro_bd_operacional = 'S'
                    else:
                        reg.status_cadastro_bd_operacional = 'N'
                    lista_dados_tab_placa_a_sincronizar.append(reg.__dict__)

            data = {
                'lista_dados_tab_placa_a_sincronizar': lista_dados_tab_placa_a_sincronizar
            }
        elif nome_componente_form == 'btn_vincula_beneficiario':
            cod_projeto_form = request.GET['codprojeto']
            data_inicial_form = request.GET['datainicial']
            data_final_form = request.GET['datafinal']

            obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto_form).first()

            lista_mapas_filial_periodo = Registro2ArtTerceirosFinanceiro.objects\
                .filter(cod_projeto=obj_projeto,
                        cod_cad_placa_terc__isnull=True,
                        data_2art_terc_financ__range=[data_inicial_form, data_final_form])
            for reg in lista_mapas_filial_periodo:
                obj_cad_placa_terc = CadastroPlacaTerceiro.objects \
                    .filter(
                    cod_projeto=reg.cod_projeto,
                    placa_cad_placa_terc=reg.placa_2art_terc_financ,
                    perfil_veiculo_cad_placa_terc=reg.nomespot_2art_terc_financ) \
                    .extra(
                    where=["'" + str(reg.data_2art_terc_financ) + "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]) \
                    .first()
                obj_cad_frete_terc = None
                if obj_cad_placa_terc is not None:
                    reg.cod_cad_placa_terc = obj_cad_placa_terc
                    obj_cad_frete_terc = (CadFreteSpot.objects.filter(cod_projeto=reg.cod_projeto,
                                                                     tipo_perfil_veiculo=reg.nomespot_2art_terc_financ,
                                                                     cod_regiao=reg.regiaospot_2art_terc_financ,
                                                                     tipo_entrega=reg.entrega_2art_terc_financ, )
                                          .extra(where=["'" + str(reg.data_2art_terc_financ) +
                                                        "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first())
                    if obj_cad_frete_terc is not None:
                        reg.cod_cad_frete_spot = obj_cad_frete_terc
                reg.save()

            data = {
                'msg': 'Vinculo Atualizado!'
            }
        elif nome_componente_form == 'btn_atualiza_fretes_mapas_terc':
            cod_projeto_form = request.GET.get('cod_projeto', None)
            data_ini_form = request.GET.get('data_ini', None)
            data_fim_form = request.GET.get('data_fim', None)

            obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto_form).first()

            lista_mapas_filial_periodo = Registro2ArtTerceirosFinanceiro.objects \
                .filter(cod_projeto=obj_projeto, cod_pag_2art_terc_financ__isnull=True,
                        status_financeiro_2art_terc_financ='A',
                        data_2art_terc_financ__range=[data_ini_form, data_fim_form],)
            for reg in lista_mapas_filial_periodo:
                obj_cad_frete_terc = None
                if reg.cod_cad_placa_terc is not None:
                    obj_cad_frete_terc = (CadFreteSpot.objects\
                        .filter(cod_projeto=reg.cod_projeto,
                                tipo_perfil_veiculo=reg.nomespot_2art_terc_financ,
                                cod_regiao=reg.regiaospot_2art_terc_financ,
                                tipo_entrega=reg.entrega_2art_terc_financ,)
                        .extra(where=["'" + str(reg.data_2art_terc_financ) +
                                      "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first())
                    if obj_cad_frete_terc is not None:
                        reg.cod_cad_frete_spot = obj_cad_frete_terc
                reg.save()
            data = {
                'msg': 'Fretes vinculados atualizados!'
            }

        return JsonResponse(data, safe=False)

    def post(self, request):
        nome_componente_form = request.POST['nome_componente']
        data = dict()
        if nome_componente_form == 'btn_altera_status_mapa_com_benner':
            cod_2art_terc_financ_form = request.POST['cod_2art_terc_financ']
            status_reg_form = request.POST['status_registro']

            obj_2art_financ_form = Registro2ArtTerceirosFinanceiro.objects.get(pk=cod_2art_terc_financ_form)
            obj_2art_financ_form.status_mapa_2art_terc_financ = status_reg_form
            obj_2art_financ_form.save(update_fields=['status_mapa_2art_terc_financ'])

            data = {
                'msg': 'Status do mapa alterado com sucesso !'
            }
        if nome_componente_form == 'btn_cad_placa_benef_sinc_benner':
            cod_projeto_form = request.POST['cod_projeto']
            nome_benef_form = request.POST['nome_benef']
            doc_benef_form = request.POST['doc_benef']
            tipo_pessoa_form = request.POST['tipo_pessoa']
            handle_benef_form = request.POST['handle_benef']
            status_benef_form = request.POST['status_benef']
            handle_placa_form = request.POST['handle_placa']
            placa_benner_form = request.POST['placa_benner']
            perfil_placa_form = request.POST['perfil_placa']
            data_ini_vig_form = request.POST['data_ini_vig']
            data_fim_vig_form = request.POST['data_fim_vig']


            obj_projeto = Projeto.objects.get(pk=cod_projeto_form)
            id_usu_session = request.session['cod_usuario_logado']
            obj_usuario = Usuario.objects.get(pk=id_usu_session)
            msg = ''
            obj_benef = BeneficiarioTerceiro.objects.filter(
                Q(handle_benner=handle_benef_form) | Q(doc_benef_terc=doc_benef_form)).first()
            if obj_benef == None:
                obj_benef_novo = BeneficiarioTerceiro(
                    nome_benef_terc=nome_benef_form,
                    doc_benef_terc=doc_benef_form,
                    tipo_pessoa_benef_terc=tipo_pessoa_form,
                    cod_projeto=obj_projeto,
                    status_benef=status_benef_form,
                    handle_benner=handle_benef_form,
                    cod_usu=obj_usuario
                ).save()
            elif obj_benef.handle_benner == None or obj_benef.handle_benner == 0:
                obj_benef.handle_benner = handle_benef_form
                obj_benef.save()

            obj_cad_placa_terc = CadastroPlacaTerceiro.objects \
                .filter(
                Q(data_ini_vigencia__range=[data_ini_vig_form, data_fim_vig_form]) |
                Q(data_fim_vigencia__range=[data_ini_vig_form, data_fim_vig_form]),
                cod_projeto=obj_projeto,
                placa_cad_placa_terc=placa_benner_form,
                perfil_veiculo_cad_placa_terc=perfil_placa_form,
            ).first()



            if obj_cad_placa_terc == None:
                obj_cad_placa_terc = CadastroPlacaTerceiro(
                    placa_cad_placa_terc=placa_benner_form,
                    perfil_veiculo_cad_placa_terc=perfil_placa_form,
                    handle_benner=handle_placa_form,
                    data_ini_vigencia=data_ini_vig_form,
                    data_fim_vigencia=data_fim_vig_form,
                    cod_projeto=obj_projeto,
                    cod_benef_terc=obj_benef
                ).save()
                obj_cad_placa_terc_pesq = CadastroPlacaTerceiro.objects.filter(
                    handle_benner=handle_placa_form,
                    cod_projeto=obj_projeto,
                    data_ini_vigencia=data_ini_vig_form,
                    data_fim_vigencia=data_fim_vig_form
                ).first()
                '''Vincula mapas da placa cadastrada'''
                lista_mapas_filial_periodo = Registro2ArtTerceirosFinanceiro.objects. \
                    filter(cod_projeto=obj_projeto,
                           cod_cad_placa_terc__isnull=True,
                           placa_2art_terc_financ=placa_benner_form,
                           nomespot_2art_terc_financ=perfil_placa_form,
                           data_2art_terc_financ__range=[data_ini_vig_form, data_fim_vig_form]
                           )
                for mapa in lista_mapas_filial_periodo:
                    mapa.cod_cad_placa_terc = obj_cad_placa_terc_pesq
                    mapa.save()
                msg = 'Placa cadastrada e mapas vinculados!'
            else:
                msg = 'Placa já cadastrada na vigência!'

            data = {
                'msg': msg
            }

        return JsonResponse(data, safe=False)

class Form_Pag_Mapas_Terc_2Art_Views(View):
    def get(self, request):
        cod_projeto_form = request.GET.get('cod_projeto', None)
        data_ini_form = request.GET.get('data_ini', None)
        data_fim_form = request.GET.get('data_fim', None)

        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto_form).first()

        obj_uteis = Uteis()
        tab_mapas_terceiros = obj_uteis\
            .tab_2art_terc_agrupado_por_beneficiario(cod_projeto_form, data_ini_form, data_fim_form)

        data = dict()
        data = {
            'cod_projeto': obj_projeto.cod_projeto,
            'desc_projeto': obj_projeto.desc_proj,
            'tab_mapas_terceiros': tab_mapas_terceiros
        }
        return JsonResponse(data, safe=False)

    @csrf_exempt
    def post(self, request):
        dados_json_ajax = json.loads(request.body)

        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()
        obj_tipo_ocorrencia = TipoOcorrenciasFinanceiroTerceiros.objects.filter(desc_ocorrencia='Mapas',
                                                                                tipo_lancamento='M').first()
        listaRegistro = dados_json_ajax['lista_registros_json']
        for reg in listaRegistro:
            obj_beneficiario = BeneficiarioTerceiro.objects.filter(cod_benef_terc=reg['cod_beneficiario']).first()
            nome_beneficiario = obj_beneficiario.nome_benef_terc
            obj_pagamento = Pagamento2ArtTerceirosFinanceiro(
                valor_frete_calc_pag=reg['val_ff_calc'],
                desc_pag=reg['val_tt_desc'],
                acresc_pag=reg['val_tt_acres'],
                val_pago=reg['val_tt_pagar'],
                val_conlog=reg['val_tt_conlog'],
                periodo_ref_pag=datetime.strptime(reg['data_referencia'], '%Y-%m'),
                data_geracao_pag=date.today(),
                obs_pag=reg['obs'],
                complemento_pag='',
                cod_tipo_ocor_financ_terc=obj_tipo_ocorrencia,
                cod_benef_terc=obj_beneficiario,
                cod_usu=obj_usuario
            )
            obj_pagamento.save()
            cod_2art_terc_financ = str(reg['cod_2art_terc_financ']).replace('[', '').replace(']', '').split(',')
            for info_cod in cod_2art_terc_financ:
                obj_2art_terc_financ = Registro2ArtTerceirosFinanceiro.objects.filter(
                    cod_reg_2art_terc_financ=info_cod.split('_')[0].replace("'", "")).first()
                obj_2art_terc_financ.status_financeiro_2art_terc_financ = 'P'
                obj_2art_terc_financ.data_status_financeiro_2art_terc_financ = date.today()
                obj_2art_terc_financ.cod_pag_2art_terc_financ = obj_pagamento
                obj_2art_terc_financ.valor_frete_calculado_pago = info_cod.split('_')[1]
                obj_2art_terc_financ.val_a_pagar_pago = info_cod.split('_')[2]
                obj_2art_terc_financ.val_conlog_pago = info_cod.split('_')[3].replace("'", "")
                obj_2art_terc_financ.save()

            data = dict()
            data = {
                'msg': 'Pagamento(s) processado com sucesso !'
            }

        return JsonResponse(data, safe=False)

class Form_Lanc_Terc_2Art_View(View):
    def get_object(self, pk):
        try:
            return LancamentosRegistro2ArtTerceirosFinanceiro.objects.get(pk=pk)
        except LancamentosRegistro2ArtTerceirosFinanceiro.DoesNotExist:
            return Http404
    def get(self, request):
        cod_reg_2art_terc_financ_form = request.GET['cod_reg_2art_terc_financ']
        uteis = Uteis()
        lista_lancamentos_mapa = uteis.retorna_lancamentos_mapa_2art_terc_financ(cod_reg_2art_terc_financ_form)
        data = dict()
        data = {
            'lista_lancamentos_mapa': lista_lancamentos_mapa
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_registro_2art_terc_financ_form = request.POST['cod_registro_2art_terc_financ']
        tipo_lancamento_form = request.POST['tipo_lancamento']
        tipo_ocorrencia_form = request.POST['tipo_ocorrencia']
        mapa_ocorrencia_form = request.POST['mapa_ocorrencia']
        placa_lanc_form = request.POST['placa_lanc']
        data_ocorrencia_form = request.POST['data_ocorrencia']
        valor_form = request.POST['valor']
        obs_form = request.POST['obs']

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        id_usu_session = request.session['cod_usuario_logado']
        usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()
        tipo_ocorrencia = TipoOcorrenciasFinanceiroTerceiros.objects.filter(
            cod_tipo_ocor_financ_terc=tipo_ocorrencia_form).first()
        obj_reg_2art_terc_finan = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_reg_2art_terc_financ=cod_registro_2art_terc_financ_form).first()
        reg_lanc_2art_terc = LancamentosRegistro2ArtTerceirosFinanceiro(
            cod_reg_2art_terc_financ=obj_reg_2art_terc_finan,
            mapa_ocorrencia=mapa_ocorrencia_form,
            placa_lanc=placa_lanc_form,
            cod_tipo_ocor_financ_terc=tipo_ocorrencia,
            data_ocorrencia=datetime.strptime(data_ocorrencia_form, '%Y-%m-%d'),
            valor_lanc=valor_form,
            obs_lanc=obs_form,
            tipo_lancamento=tipo_lancamento_form,
            data_lanc=data_atual_dd_mm_yyyy,
            cod_usu=usuario,
            status_exclusao='N'
        )
        reg_lanc_2art_terc.save()

        uteis = Uteis()
        lista_lancamentos_mapa = uteis.retorna_lancamentos_mapa_2art_terc_financ(cod_registro_2art_terc_financ_form)

        msg = 'Registro cadastrado com sucesso!'

        data = dict()
        data = {
            'msg': msg,
            'lista_lancamentos_mapa': lista_lancamentos_mapa
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        id_usu_session = request.session['cod_usuario_logado']
        usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')
        hota_atual = data_hora_atual.strftime('%H:%M')

        obj_lanc = self.get_object(pk)
        obj_lanc.status_exclusao = 'S'
        obj_lanc.obs_lanc += '/Registro excluído por ' + usuario.login_usu + ', em ' + str(
            data_atual_dd_mm_yyyy) + ' às ' + str(hota_atual)
        obj_lanc.save()

        data = dict()
        data = {
            'msg': 'Registro excluído com sucesso !',
            'cod_reg_2art_financ': obj_lanc.cod_reg_2art_terc_financ.cod_reg_2art_terc_financ
        }
        return JsonResponse(data, safe=False)

class Comp_Select_Tipo_Ocorrencias_Lanc_2Art_Terc_View(View):
    def get(self, request):
        tipo_lancamento_form = request.GET['tipo_lancamento']
        lista_ocorrencia = list(
            TipoOcorrenciasFinanceiroTerceiros.objects.filter(tipo_lancamento=tipo_lancamento_form).values())
        data = dict()
        data = {
            'lista_ocorrencia': lista_ocorrencia
        }
        return JsonResponse(data, safe=False)

class Form_Cad_Placa_2Art_Terc_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        lista_projetos = Proj_Usu.objects.filter(cod_usu=obj_usuario_sessao,
                                               cod_projeto__cod_atividade__desc2_atividade='Terceiro',
                                               cod_projeto__data_inativado__isnull=True,
                                               status_proj_usu='S')
        lista_beneficiarios_terceiro = BeneficiarioTerceiro.objects.filter(status_benef='A')

        contexto = {
            'lista_projetos': lista_projetos,
            'lista_beneficiarios_terceiro': lista_beneficiarios_terceiro,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'plan_controle_fat_2art_terc_app/form_cad_placas_fat_2art_terc.html', contexto)

    def post(self, request):
        tipo_transacao_frm = request.POST['tipo_transacao']

        msg = ''
        if tipo_transacao_frm == 'novo':
            id_benef = request.POST['id_benef']
            placa = request.POST['placa']
            perfil_veic = request.POST['perfil_veic']
            inicio_vigencia = request.POST['inicio_vig']
            fim_vigencia = request.POST['fim_vig']
            cod_proj = request.POST['cod_proj']

            projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
            obj_beneficiario = BeneficiarioTerceiro.objects.filter(cod_benef_terc=id_benef).first()
            handle_benner_placa = ConexaoBancoBenner().retorna_dados_placa_benef_a_sincronizar(projeto.handle_benner,
                                                                                               placa,
                                                                                               '')[0].handle_placa
            obj_cad_placa_pesq = CadastroPlacaTerceiro.objects.filter(
                Q(data_ini_vigencia__range=[inicio_vigencia, fim_vigencia]) | Q(data_fim_vigencia__range=[inicio_vigencia, fim_vigencia]),
                placa_cad_placa_terc=placa, cod_projeto=projeto, cod_benef_terc=obj_beneficiario,
                perfil_veiculo_cad_placa_terc=perfil_veic,
            ).first()
            if obj_cad_placa_pesq == None:
                reg_cad_placa_terc = CadastroPlacaTerceiro(
                    placa_cad_placa_terc=placa,
                    cod_benef_terc=obj_beneficiario,
                    perfil_veiculo_cad_placa_terc=perfil_veic,
                    cod_projeto=projeto,
                    handle_benner=handle_benner_placa,
                    data_ini_vigencia=datetime.strptime(inicio_vigencia, '%Y-%m-%d'),
                    data_fim_vigencia=datetime.strptime(fim_vigencia, '%Y-%m-%d')
                )
                reg_cad_placa_terc.save()
                msg = 'Placa ' + placa + ', cadastrada com sucesso!'
            else:
                msg = 'Já possui a placa ' + placa + ', cadastrada nesta mesma vigência. Verifique!'
        elif tipo_transacao_frm == 'editar':
            cod_cad_placa_frm = request.POST['cod_cad_placa']
            dt_fim_vigencia_placa_frm = request.POST['dt_fim_vigencia_placa']
            obj_plca = CadastroPlacaTerceiro.objects.get(pk=cod_cad_placa_frm)
            obj_plca.data_fim_vigencia = dt_fim_vigencia_placa_frm
            obj_plca.save()
            msg = 'Placa editada com sucesso'


        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Tab_Cad_Placa_2Art_Terc_View(View):
    def get_object(self, pk):
        try:
            return CadastroPlacaTerceiro.objects.get(pk=pk)
        except CadastroPlacaTerceiro.DoesNotExist:
            raise Http404

    def get(self, request):
        cod_proj = request.GET['cod_proj']
        periodo_vigencia = request.GET['periodo_vig']
        mes_vigencia = periodo_vigencia.split("-")[1]
        ano_vigencia = periodo_vigencia.split("-")[0]
        data_vigencia = ano_vigencia + '-' + mes_vigencia + "-01"

        projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
        registros_cad_placa_terc = CadastroPlacaTerceiro.objects.filter(
            cod_projeto=projeto).extra(
            where=[f" '{data_vigencia}' BETWEEN data_ini_vigencia AND data_fim_vigencia"])

        '''registros_cad_placa_terc = CadastroPlacaTerceiro.objects.filter(
            cod_projeto=projeto).extra(
            where=[
                " ( MONTH(data_ini_vigencia) = " + mes_vigencia + " AND YEAR(data_ini_vigencia) = " + ano_vigencia + " ) " +
                " OR (MONTH(data_fim_vigencia) = " + mes_vigencia + " AND YEAR(data_fim_vigencia) = " + ano_vigencia + " ) "])'''
        tab_form_cad_placa_terc = []
        for reg in registros_cad_placa_terc:
            campo_readonly = ''
            if reg.data_fim_vigencia < datetime.now().date():
                campo_readonly = 'readonly'
            reg_tab_cad_placa = Tab_Cad_Placa_Terc_Financ(
                id_cad_placa_terc=reg.cod_cad_placa_terc,
                placa=reg.placa_cad_placa_terc,
                handle_placa=reg.handle_benner,
                perfil_veic=reg.perfil_veiculo_cad_placa_terc,
                nome_beneficiario=reg.cod_benef_terc.nome_benef_terc,
                doc_benef=reg.cod_benef_terc.doc_benef_terc,
                tipo_pessoa_benef=reg.cod_benef_terc.tipo_pessoa_benef_terc,
                handle_benef=reg.cod_benef_terc.handle_benner,
                data_ini=reg.data_ini_vigencia,
                data_fim=reg.data_fim_vigencia,
                campo_readonly = campo_readonly
            )
            tab_form_cad_placa_terc.append(reg_tab_cad_placa.__dict__)

        data = dict()
        data = {
            'registros_cad_placa_terc': tab_form_cad_placa_terc
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_registro_cad_placa_terc = request.POST['cod_registro_cad_placa_terc']
        qtd_mapas_vinculados = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_cad_placa_terc__cod_cad_placa_terc=cod_registro_cad_placa_terc,
            cod_pag_2art_terc_financ__isnull=True).count()

        indica_exclusao = 'S'
        if qtd_mapas_vinculados > 0:
            indica_exclusao = 'N'
        data = dict()
        data = {
            'qtd_mapas_pagos': qtd_mapas_vinculados,
            'indica_exclusao': indica_exclusao
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        registro_selecionado = self.get_object(pk)
        placa = registro_selecionado.placa_cad_placa_terc
        mapas_placa_selecionada = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_cad_placa_terc=registro_selecionado,
            data_2art_terc_financ__range=[registro_selecionado.data_ini_vigencia,
                                          registro_selecionado.data_fim_vigencia])

        for mapa in mapas_placa_selecionada:
            mapa.cod_cad_placa_terc = None
            mapa.save()
        registro_selecionado.delete()

        data = dict()
        data = {
            'msg': 'Placa ' + str(placa) + ', excluída com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Form_Replica_Cad_Placas_2Art_Terc_View(View):
    def get(self, request):
        comp_form = request.GET['comp']
        cod_proj_form = request.GET['cod_proj']
        lista_datas_comp = list(CadastroPlacaTerceiro.objects.filter(
            Q(data_ini_vigencia__month=comp_form.split('-')[1], data_ini_vigencia__year=comp_form.split('-')[0]) |
            Q(data_fim_vigencia__month=comp_form.split('-')[1], data_fim_vigencia__year=comp_form.split('-')[0]),
            cod_projeto__cod_projeto=cod_proj_form
        ).values('data_ini_vigencia', 'data_fim_vigencia').distinct())
        '''for reg in lista_datas_comp:
            print(reg.data_ini_vigencia__month + ' : ' + reg.data_fim_vigencia__month)'''
        data = dict()
        data = {
            'lista_datas_comp': lista_datas_comp
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_proj = request.POST['cod_proj']
        periodo_vigencia = request.POST['data_vigencia']
        data_vigencia_origem_ini = periodo_vigencia.split("_")[0]
        data_vigencia_origem_fim = periodo_vigencia.split("_")[1]

        data_ini_vigencia_YYYY_MM_DD = request.POST['data_ini_vigencia']
        data_fim_vigencia_YYYY_MM_DD = request.POST['data_fim_vigencia']



        projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
        msg = ''
        registros_cad_placa_terc = CadastroPlacaTerceiro.objects.filter(cod_projeto=projeto,
                                                                        data_ini_vigencia=data_vigencia_origem_ini,
                                                                        data_fim_vigencia=data_vigencia_origem_fim)

        count_reg_replicados = 0
        for reg in registros_cad_placa_terc:
            verifica_reg_cadastrado = CadastroPlacaTerceiro.objects.filter(cod_projeto=projeto,
                                                                           placa_cad_placa_terc=reg.placa_cad_placa_terc,
                                                                           perfil_veiculo_cad_placa_terc=reg.perfil_veiculo_cad_placa_terc,
                                                                           cod_benef_terc=reg.cod_benef_terc) \
                .extra(where=[
                " '" + str(data_ini_vigencia_YYYY_MM_DD) + "' BETWEEN data_ini_vigencia AND data_fim_vigencia OR " +
                " '" + str(data_fim_vigencia_YYYY_MM_DD) + "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first()

            if verifica_reg_cadastrado == None:
                reg_cad_placa = CadastroPlacaTerceiro(
                    placa_cad_placa_terc=reg.placa_cad_placa_terc,
                    cod_benef_terc=reg.cod_benef_terc,
                    # tipo_pessoa_cad_placa_terc=reg.tipo_pessoa_cad_placa_terc,
                    perfil_veiculo_cad_placa_terc=reg.perfil_veiculo_cad_placa_terc,
                    cod_projeto=projeto,
                    handle_benner=reg.handle_benner,
                    data_ini_vigencia=datetime.strptime(data_ini_vigencia_YYYY_MM_DD, '%Y-%m-%d'),
                    data_fim_vigencia=datetime.strptime(data_fim_vigencia_YYYY_MM_DD, '%Y-%m-%d')
                )
                reg_cad_placa.save()
                count_reg_replicados += 1

        if count_reg_replicados == 0:
            msg = 'Verifique o periodo informado. Talvez já tenha registros no período!'
        else:
            msg = str(count_reg_replicados) + ' registros replicados com sucesso!'

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Form_Cad_Beneficiarios_View(View):
    def get_object(self, pk):
        try:
            return BeneficiarioTerceiro.objects.get(pk=pk)
        except BeneficiarioTerceiro.DoesNotExist:
            raise Http404

    def get(self, request):
        cod_projeto = request.GET.get('cod_projeto', None)

        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto).first()
        lista_beneficiarios_do_projeto = list(BeneficiarioTerceiro.objects.filter(cod_projeto=obj_projeto).values())

        data = dict()
        data = {
            'lista_beneficiarios_do_projeto': lista_beneficiarios_do_projeto
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_projeto = request.POST['cod_projeto']
        nome_benef = request.POST['nome_benef']
        doc_benef = request.POST['doc_benef']
        tipo_benef = request.POST['tipo_benef']
        handle_benner_form = request.POST['handle_benner']
        status_benner_form = request.POST['status_benef']

        id_usu_session = request.session['cod_usuario_logado']
        usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_aa = data_hora_atual.strftime('%Y-%m-%d')

        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto).first()
        obj_benf_pesq = BeneficiarioTerceiro.objects.filter(
            doc_benef_terc=doc_benef, tipo_pessoa_benef_terc=tipo_benef, cod_projeto=obj_projeto
        ).first()
        msg = ''
        if obj_benf_pesq == None:
            novo_benef_terc = BeneficiarioTerceiro(
                nome_benef_terc=nome_benef,
                doc_benef_terc=doc_benef,
                tipo_pessoa_benef_terc=tipo_benef,
                status_benef=status_benner_form,
                data_status=data_atual_yyyy_mm_aa,
                handle_benner=handle_benner_form,
                cod_usu=usuario,
                cod_projeto=obj_projeto
            )
            novo_benef_terc.save()
            msg = 'Beneficiário ' + novo_benef_terc.nome_benef_terc + ', adicionado com sucesso !!!'
        else:
            msg = 'Beneficiário ' + nome_benef + ', já cadastrado. Verifique !!!'

        lista_beneficiarios_atualizada = list(
            BeneficiarioTerceiro.objects.filter(cod_projeto=obj_projeto, status_benef='A').values())
        data = dict()
        data = {
            'msg': msg,
            'lista_beneficiarios_atualizada': lista_beneficiarios_atualizada
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_benef_terc = self.get_object(pk)

        id_usu_session = request.session['cod_usuario_logado']
        usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_aa = data_hora_atual.strftime('%Y-%m-%d')

        msgAcao = ''
        if (obj_benef_terc.status_benef == 'A'):
            obj_benef_terc.status_benef = 'D'
            obj_benef_terc.data_status = data_atual_yyyy_mm_aa
            obj_benef_terc.cod_usu = usuario
            msgAcao = 'Beneficiário ' + obj_benef_terc.nome_benef_terc + ', desativado com sucesso!'
        elif (obj_benef_terc.status_benef == 'D'):
            obj_benef_terc.status_benef = 'A'
            obj_benef_terc.data_status = data_atual_yyyy_mm_aa
            obj_benef_terc.cod_usu = usuario
            msgAcao = 'Beneficiário ' + obj_benef_terc.nome_benef_terc + ', ativo com sucesso!'
        obj_benef_terc.save()

        data = dict()
        data = {
            'msg': msgAcao
        }
        return JsonResponse(data, safe=False)

class Comp_Beneficiarios_Terc_2Art_View(View):
    def get(self, request):
        tipo_cad_form = request.GET['tipo_cad']
        cod_projeto_form = request.GET['cod_proj']
        obj_projeto = Projeto.objects.get(pk=cod_projeto_form)
        lista_benef_benner_dic = []
        if tipo_cad_form == 'benef':
            lista_benef_benner = ConexaoBancoBenner().retornaBenefTerceiroByProjeto(obj_projeto.handle_benner)
            for benef in lista_benef_benner:
                benef_pesq = BeneficiarioTerceiro.objects.filter(handle_benner=benef.handle,
                                                                 cod_projeto=obj_projeto).first()
                if (benef_pesq == None):
                    lista_benef_benner_dic.append(benef.__dict__)
        elif tipo_cad_form == 'placa':
            lista_benef_benner_dic = list(BeneficiarioTerceiro.objects.filter(cod_projeto=obj_projeto)
                                      .values('cod_benef_terc', 'doc_benef_terc', 'nome_benef_terc', 'status_benef'))
        data = dict()
        data = {
            'lista_benef_benner_dic': lista_benef_benner_dic
        }
        return JsonResponse(data, safe=False)


class Form_Cad_Fretes_Terc_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        cad_projetos = Proj_Usu.objects.filter(cod_usu=usuario_portal,
                                               cod_projeto__cod_atividade__desc2_atividade='Terceiro',
                                               status_proj_usu='S')

        context = {
            'cad_projetos': cad_projetos,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'plan_controle_fat_2art_terc_app/form_cad_frete_spot.html', context)

    def post(self, request):
        cod_registro = request.POST['cod_registro']
        cod_proj = request.POST['cod_proj']
        inicio_vigencia = request.POST['inicio_vig']
        fim_vigencia = request.POST['fim_vig']
        tipo_pessoa = request.POST['tipo_pessoa']
        tipo_entrega = request.POST['tipo_entrega']
        perfil_veic = request.POST['perfil_veic']
        cod_regiao = request.POST['cod_regiao']
        desc_regiao = request.POST['desc_regiao']
        qtd_min = request.POST['qtd_min']
        frete_carreteiro_min = request.POST['frete_carreteiro_min']
        descarga_min = request.POST['descarga_min']
        pedagio_min = request.POST['pedagio_min']
        cpbr_min = request.POST['cpbr_min']
        lucro_min = request.POST['lucro_min']
        qtd_max = request.POST['qtd_max']
        frete_carreteiro_max = request.POST['frete_carreteiro_max']
        descarga_max = request.POST['descarga_max']
        pedagio_max = request.POST['pedagio_max']
        cpbr_max = request.POST['cpbr_max']
        lucro_max = request.POST['lucro_max']

        msg = ''
        projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
        reg_cad_frete = ''
        if cod_registro == '0':
            reg_cad_frete = CadFreteSpot(
                cod_projeto=projeto,
                tipo_entrega=tipo_entrega,
                data_ini_vigencia=datetime.strptime(inicio_vigencia, '%Y-%m-%d'),
                data_fim_vigencia=datetime.strptime(fim_vigencia, '%Y-%m-%d'),
                tipo_perfil_veiculo=perfil_veic,
                cod_regiao=cod_regiao,
                nome_regiao=desc_regiao,
                qtd_min=qtd_min,
                val_frete_carreteiro_min=frete_carreteiro_min,
                val_descarga_min=descarga_min,
                val_pedagio_min=pedagio_min,
                val_cprb_min=cpbr_min,
                val_lucro_min=lucro_min,
                qtd_max=qtd_max,
                val_frete_carreteiro_max=frete_carreteiro_max,
                val_descarga_max=descarga_max,
                val_pedagio_max=pedagio_max,
                val_cprb_max=cpbr_max,
                val_lucro_max=lucro_max,
                tipo_pessoa=tipo_pessoa
            )
            reg_cad_frete.save()
            msg = 'Registro cadastrado com sucesso!'
        else:
            reg_cad_frete = CadFreteSpot.objects.filter(cod_cad_frete_spot=cod_registro).first()
            reg_cad_frete.cod_projeto = projeto
            reg_cad_frete.tipo_entrega = tipo_entrega
            reg_cad_frete.data_ini_vigencia = datetime.strptime(inicio_vigencia, '%Y-%m-%d')
            reg_cad_frete.data_fim_vigencia = datetime.strptime(fim_vigencia, '%Y-%m-%d')
            reg_cad_frete.tipo_perfil_veiculo = perfil_veic
            reg_cad_frete.cod_regiao = cod_regiao
            reg_cad_frete.nome_regiao = desc_regiao
            reg_cad_frete.qtd_min = qtd_min
            reg_cad_frete.val_frete_carreteiro_min = frete_carreteiro_min
            reg_cad_frete.val_descarga_min = descarga_min
            reg_cad_frete.val_pedagio_min = pedagio_min
            reg_cad_frete.val_cprb_min = cpbr_min
            reg_cad_frete.val_lucro_min = lucro_min
            reg_cad_frete.qtd_max = qtd_max
            reg_cad_frete.val_frete_carreteiro_max = frete_carreteiro_max
            reg_cad_frete.val_descarga_max = descarga_max
            reg_cad_frete.val_pedagio_max = pedagio_max
            reg_cad_frete.val_cprb_max = cpbr_max
            reg_cad_frete.val_lucro_max = lucro_max
            reg_cad_frete.tipo_pessoa = tipo_pessoa
            reg_cad_frete.save()
            msg = 'Registro alterado com sucesso!'

        registros_2art_terc_do_frete_salvo = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_cad_placa_terc__cod_benef_terc__tipo_pessoa_benef_terc=reg_cad_frete.tipo_pessoa,
            entrega_2art_terc_financ=reg_cad_frete.tipo_entrega,
            nomespot_2art_terc_financ=reg_cad_frete.tipo_perfil_veiculo,
            regiaospot_2art_terc_financ=reg_cad_frete.cod_regiao,
            cod_projeto=reg_cad_frete.cod_projeto,
            cod_cad_frete_spot__isnull=True) \
            .extra(where=["data_2art_terc_financ BETWEEN '" + str(reg_cad_frete.data_ini_vigencia) + "' AND '" + str(
            reg_cad_frete.data_fim_vigencia) + "'"])

        if len(registros_2art_terc_do_frete_salvo) > 0:
            for reg_2art_terc in registros_2art_terc_do_frete_salvo:
                reg_2art_terc.cod_cad_frete_spot = reg_cad_frete
                reg_2art_terc.save()

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Tab_Cad_Fretes_Terc_View(View):
    def get_object(self, pk):
        try:
            return CadFreteSpot.objects.get(pk=pk)
        except CadFreteSpot.DoesNotExist:
            raise Http404

    def get(self, request):
        cod_proj = request.GET['cod_proj']
        periodo_vigencia = request.GET['periodo_vig']
        mes_vigencia = periodo_vigencia.split("-")[1]
        ano_vigencia = periodo_vigencia.split("-")[0]
        data_vigencia = ano_vigencia + '-' + mes_vigencia + '-01'

        projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
        registros_cad_frete_terc = list(CadFreteSpot.objects.filter(
            cod_projeto=projeto).extra(
            where=[f" '{data_vigencia}' BETWEEN data_ini_vigencia AND data_fim_vigencia "]).values())

        for cad_frete in registros_cad_frete_terc:
            campo_readonly = ''
            if cad_frete['data_fim_vigencia'] < datetime.now().date():
                campo_readonly = 'readonly'
            cad_frete['campo_readonly'] = campo_readonly



        data = dict()
        data = {
            'registros_cad_frete_terc': registros_cad_frete_terc
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_registro_cad_frete_spot = request.POST['cod_registro_cad_frete_spot']
        qtd_mapas_vinculados = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_cad_frete_spot__cod_cad_frete_spot=cod_registro_cad_frete_spot,
            cod_pag_2art_terc_financ__isnull=False).count()
        indica_exclusao = 'S'
        if qtd_mapas_vinculados > 0:
            indica_exclusao = 'N'
        data = dict()
        data = {
            'qtd_mapas_pagos': qtd_mapas_vinculados,
            'indica_exclusao': indica_exclusao
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        registro_selecionado = self.get_object(pk)

        mapas_placa_selecionada = Registro2ArtTerceirosFinanceiro.objects.filter(
            cod_cad_frete_spot=registro_selecionado,
            data_2art_terc_financ__range=[
                registro_selecionado.data_ini_vigencia,
                registro_selecionado.data_fim_vigencia])

        for mapa in mapas_placa_selecionada:
            mapa.cod_cad_frete_spot = None
            mapa.save()

        registro_selecionado.delete()

        data = dict()
        data = {
            'msg': 'Registro excluído com sucesso!'
        }
        return JsonResponse(data, safe=False)


class Form_Replica_Cad_Frete_2Art_Terc_View(View):
    def get(self, request):
        comp_form = request.GET['comp']
        cod_proj_form = request.GET['cod_proj']
        lista_datas_comp = list(CadFreteSpot.objects.filter(
            Q(data_ini_vigencia__month=comp_form.split('-')[1], data_ini_vigencia__year=comp_form.split('-')[0]) |
            Q(data_fim_vigencia__month=comp_form.split('-')[1], data_fim_vigencia__year=comp_form.split('-')[0]),
            cod_projeto__cod_projeto=cod_proj_form
        ).values('data_ini_vigencia', 'data_fim_vigencia').distinct())
        '''for reg in lista_datas_comp:
            print(reg.data_ini_vigencia__month + ' : ' + reg.data_fim_vigencia__month)'''
        data = dict()
        data = {
            'lista_datas_comp': lista_datas_comp
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_proj = request.POST['cod_proj']
        periodo_vigencia = request.POST['data_vigencia']
        data_vigencia_origem_ini = periodo_vigencia.split("_")[0]
        data_vigencia_origem_fim = periodo_vigencia.split("_")[1]

        # data_ini_vigencia = request.GET.get('data_ini_vigencia', None)
        # data_fim_vigencia = request.GET.get('data_fim_vigencia', None)

        data_ini_vigencia_YYYY_MM_DD = request.POST['data_ini_vigencia']
        data_fim_vigencia_YYYY_MM_DD = request.POST['data_fim_vigencia']

        projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
        msg = ''
        registros_cad_frete_terc = CadFreteSpot.objects.filter(cod_projeto=projeto,
                                                               data_ini_vigencia=data_vigencia_origem_ini,
                                                               data_fim_vigencia=data_vigencia_origem_fim)
        count_reg_replicados = 0
        for reg in registros_cad_frete_terc:
            verifica_reg_cadastrado = (CadFreteSpot.objects.filter(cod_projeto=reg.cod_projeto,
                                                                  tipo_entrega=reg.tipo_entrega,
                                                                  tipo_perfil_veiculo=reg.tipo_perfil_veiculo,
                                                                  cod_regiao=reg.cod_regiao,
                                                                  qtd_min=reg.qtd_min,
                                                                  qtd_max=reg.qtd_max)
                                       .extra(where=[" '" + str(data_ini_vigencia_YYYY_MM_DD) +
                                                     "' BETWEEN data_ini_vigencia AND data_fim_vigencia OR " +
                                                     " '" + str(data_fim_vigencia_YYYY_MM_DD) +
                                                     "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first())
            if verifica_reg_cadastrado == None:
                reg_cad_frete = CadFreteSpot(
                    cod_projeto=projeto,
                    tipo_entrega=reg.tipo_entrega,
                    data_ini_vigencia=datetime.strptime(data_ini_vigencia_YYYY_MM_DD, '%Y-%m-%d'),
                    data_fim_vigencia=datetime.strptime(data_fim_vigencia_YYYY_MM_DD, '%Y-%m-%d'),
                    tipo_perfil_veiculo=reg.tipo_perfil_veiculo,
                    cod_regiao=reg.cod_regiao,
                    nome_regiao=reg.nome_regiao,
                    qtd_min=reg.qtd_min,
                    val_frete_carreteiro_min=reg.val_frete_carreteiro_min,
                    val_descarga_min=reg.val_descarga_min,
                    val_pedagio_min=reg.val_pedagio_min,
                    val_cprb_min=reg.val_cprb_min,
                    val_lucro_min=reg.val_lucro_min,
                    qtd_max=reg.qtd_max,
                    val_frete_carreteiro_max=reg.val_frete_carreteiro_max,
                    val_descarga_max=reg.val_descarga_max,
                    val_pedagio_max=reg.val_pedagio_max,
                    val_cprb_max=reg.val_cprb_max,
                    val_lucro_max=reg.val_lucro_max,
                    tipo_pessoa=reg.tipo_pessoa
                )
                reg_cad_frete.save()
                count_reg_replicados += 1

                registros_2art_terc_do_frete_salvo = Registro2ArtTerceirosFinanceiro.objects.filter(
                    cod_cad_placa_terc__cod_benef_terc__tipo_pessoa_benef_terc=reg_cad_frete.tipo_pessoa,
                    entrega_2art_terc_financ=reg_cad_frete.tipo_entrega,
                    nomespot_2art_terc_financ=reg_cad_frete.tipo_perfil_veiculo,
                    regiaospot_2art_terc_financ=reg_cad_frete.cod_regiao,
                    cod_projeto=reg_cad_frete.cod_projeto,
                    cod_cad_frete_spot__isnull=True) \
                    .extra(where=[
                    "data_2art_terc_financ BETWEEN '" + str(reg_cad_frete.data_ini_vigencia) + "' AND '" + str(
                        reg_cad_frete.data_fim_vigencia) + "'"])

                if len(registros_2art_terc_do_frete_salvo) > 0:
                    for reg_2art_terc in registros_2art_terc_do_frete_salvo:
                        reg_2art_terc.cod_cad_frete_spot = reg_cad_frete
                        reg_2art_terc.save()
        if count_reg_replicados == 0:
            msg = 'Verifique o periodo informado. Talvez já tenha registros no período!'
        else:
            msg = str(count_reg_replicados) + ' registros replicados com sucesso!'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Form_Importa_Arquivo_Fat_Terc_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cad_projetos = Projeto.objects.filter(cod_atividade__desc2_atividade='Terceiro').order_by('cod_projeto')

        context = {
            "cad_projetos": cad_projetos,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request,
                      'plan_controle_fat_2art_terc_app/form_importa_arquivo_faturamento_terceiros.html',
                      context)

    def post(self, request):
        tipo_arq_form = request.POST['tipo_arq']
        myfile = request.FILES['file']

        id_usu_session = request.session['cod_usuario_logado']
        obj_usu_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')
        hota_atual = data_hora_atual.strftime('%H:%M')
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        data = dict()
        if tipo_arq_form == 'arq_acresc_desc':
            lista_form_lanc_tab = []
            msg = ''
            try:
                fs = FileSystemStorage()
                caminho_arq_importado_server = 'docs/fat_terceiros_lan_desc_acres/Lan_Desc_Acres_' + str(
                    obj_usu_logado.login_usu) + '_' + \
                                               str(data_atual_dd_mm_yyyy).replace('/', '_') + '_' + str(hota_atual).replace(
                    ':', '_') + '_' + myfile.name
                filename = fs.save(caminho_arq_importado_server, myfile)
                # uploaded_file_url = fs.url(filename)
                uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado_server)

                obj_imp_arquivo_lanc_ter = ImportaArquivosFatTer()
                tab_lancamentos_fat_terc = obj_imp_arquivo_lanc_ter.le_arquivo_acres_desc_v1(uploaded_file_url)
                indica_erro = 'N'
                lista_obj_lanc = []
                for reg in tab_lancamentos_fat_terc:
                    tipo_lan_def = 'I'
                    if reg.desc_tipo_lanc == 'Descontos':
                        tipo_lan_def = 'D'
                    elif reg.desc_tipo_lanc == 'Acrescimos':
                        tipo_lan_def = 'A'
                    else:
                        tipo_lan_def = None
                        indica_erro = 'S'
                        msg = 'Tipo de lançamento não informado. Verifique!'
                    '''obj_ocorrencia = TipoOcorrenciasFinanceiroTerceiros.objects.filter(tipo_lancamento=tipo_lan_def,
                                                                                       desc_ocorrencia=reg.desc_ocorrencia_lan).first()'''
                    obj_ocorrencia = TipoOcorrenciasFinanceiroTerceiros.objects.filter(tipo_lancamento=tipo_lan_def).first()
                    obj_projeto = Projeto.objects.filter(cod_serial_pag_terc=str(int(reg.serial_proj))).first()
                    id_obj_2art = str(reg.mapa) + str(obj_projeto.cod_filial.cod_promax)
                    obj_2art_terc_financ = Registro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art__cod_reg_2art=id_obj_2art, status_financeiro_2art_terc_financ='A').first()

                    id_obj_2art_ocorrencia = str(reg.mapa_ocorrencia) + str(obj_projeto.cod_filial.cod_promax)
                    obj_2art_terc_ocorrencia_financ = Registro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art__cod_reg_2art=id_obj_2art_ocorrencia).first()
                    #status_financeiro_2art_terc_financ='P'


                    lanc = LancamentosRegistro2ArtTerceirosFinanceiro(
                        mapa_ocorrencia=obj_2art_terc_ocorrencia_financ.mapa_2art_terc_financ,
                        placa_lanc=obj_2art_terc_financ.placa_2art_terc_financ,
                        data_ocorrencia=obj_2art_terc_ocorrencia_financ.data_2art_terc_financ,
                        valor_lanc=reg.valor,
                        tipo_lancamento=tipo_lan_def,
                        data_lanc=data_atual_dd_mm_yyyy,
                        obs_lanc=reg.observacao,
                        cod_reg_2art_terc_financ=obj_2art_terc_financ,
                        cod_tipo_ocor_financ_terc=obj_ocorrencia,
                        cod_usu=obj_usu_logado,
                        status_exclusao='N'
                    )
                    lista_obj_lanc.append(lanc)
                    reg.id_lanc_banco = lanc.cod_lanc_2art_terc_financ
                    reg.placa = lanc.placa_lanc
                    reg.data_ocorrencia = datetime.strftime(lanc.data_ocorrencia, '%d-%m-%Y')
                    reg.valor = locale.currency(reg.valor, grouping=True, symbol=None)
                    lista_form_lanc_tab.append(reg.__dict__)

            except Exception as e:
                indica_erro = 'S'
                if 'NoneType' in str(e):
                    msg = 'Verifique se o mapa de ocorrência e/ou o mapa de origem existem!'
                else:
                    msg = str(e)

            if indica_erro == 'N':
                for obj_lanc in lista_obj_lanc:
                    obj_lanc.save()
                msg = 'Arquivo importado com sucesso!'
            else:
                lista_form_lanc_tab = []





            data = {
                'msg': msg,
                'lista_form_lanc_tab': lista_form_lanc_tab
            }

        elif tipo_arq_form == 'arq_pag_extras':
            lista_form_pagamentos_extra_tab = []
            try:
                fs = FileSystemStorage()
                caminho_arq_importado_server = 'docs/fat_terceiros_pag_extra/Pag_Extra_' + str(
                    obj_usu_logado.login_usu) + '_' + \
                                               str(data_atual_dd_mm_yyyy).replace('/', '_') + '_' + str(hota_atual).replace(
                    ':', '_') + '_' + myfile.name
                filename = fs.save(caminho_arq_importado_server, myfile)
                # uploaded_file_url = fs.url(filename)
                uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado_server)

                obj_imp_arquivo_pag_extra_ter = ImportaArquivosFatTer()
                tab_pagamentos_extra_fat_terc = obj_imp_arquivo_pag_extra_ter.le_arquivo_pagamentos_extra_v1(uploaded_file_url)

                lista_obj_pag_extra = []
                desc_tt = 0.00
                acres_tt = 0.00
                val_tt = 0.00
                for reg in tab_pagamentos_extra_fat_terc:
                    # obj_beneficiario = BeneficiarioTerceiro.objects.filter(doc_benef_terc=reg.doc_benef).first()
                    #data_str = reg.data[6:10] + '-' + reg.data[3:5] + "-" + reg.data[0:2]
                    data_str = reg.data

                    obj_placa = CadastroPlacaTerceiro.objects.filter(placa_cad_placa_terc=reg.placa) \
                        .extra(where=["' " + data_str + "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first()

                    obj_tipo_ocorrencia = TipoOcorrenciasFinanceiroTerceiros.objects.filter(
                        desc_ocorrencia=reg.tipo_ocorrencia, tipo_lancamento='E').first()

                    reg.nome_benef = obj_placa.cod_benef_terc.nome_benef_terc
                    obj_pag_extra = LancamentoPagamentoExtras(
                        data_pag_extra=datetime.strptime(reg.data, '%Y-%m-%d'),
                        mapa_pag_extra=reg.mapa,
                        placa_pag_extra=reg.placa,
                        desc_pag_extra=reg.desc,
                        acresc_pag_extra=reg.acres,
                        val_pag_extra=reg.valor,
                        periodo_ref_pag_extra=datetime.strptime(reg.periodo_ref, '%Y-%m-%d'),
                        obs_pag_extra=reg.observacao,
                        cod_usu=obj_usu_logado,
                        cod_tipo_ocor_financ_terc=obj_tipo_ocorrencia,
                        cod_pag_2art_terc_financ=None
                    )
                    desc_tt += reg.desc
                    acres_tt += reg.acres
                    val_tt += reg.valor
                    lista_obj_pag_extra.append(obj_pag_extra)
                    # obj_pag_extra.save()
                    # reg.id_lanc_banco = pag.cod_pag_2art_terc_financ
                    reg.doc_benef = obj_placa.cod_benef_terc.doc_benef_terc + '-' + obj_placa.cod_benef_terc.nome_benef_terc
                    reg.status_importacao = 'I'


                    lista_form_pagamentos_extra_tab.append(reg.__dict__)

                if len(lista_obj_pag_extra) > 0:
                    obj_placa = CadastroPlacaTerceiro.objects.filter(
                        placa_cad_placa_terc=lista_obj_pag_extra[0].placa_pag_extra).extra(
                        where=["' " + datetime.strftime(lista_obj_pag_extra[0].data_pag_extra,
                                                        '%Y-%m-%d') + "' BETWEEN data_ini_vigencia AND data_fim_vigencia"]).first()
                    obj_projeto = obj_placa.cod_benef_terc.cod_projeto
                    cod_ultimo_pagamento = obj_projeto.ultimo_num_pagamento
                    pag = Pagamento2ArtTerceirosFinanceiro(
                        valor_frete_calc_pag=0.00,
                        desc_pag=desc_tt,
                        acresc_pag=acres_tt,
                        val_pago=val_tt,
                        val_conlog=0.00,
                        periodo_ref_pag=lista_obj_pag_extra[0].periodo_ref_pag_extra,
                        data_geracao_pag=datetime.strptime(data_atual_dd_mm_yyyy, '%Y-%m-%d'),
                        obs_pag='',
                        complemento_pag='',
                        cod_tipo_ocor_financ_terc=lista_obj_pag_extra[0].cod_tipo_ocor_financ_terc,
                        cod_benef_terc=obj_placa.cod_benef_terc,
                        cod_usu=obj_usu_logado,
                        num_doc_pagamento=cod_ultimo_pagamento + 1
                    )
                    pag.save()
                    obj_projeto.ultimo_num_pagamento = cod_ultimo_pagamento + 1
                    obj_projeto.save()

                    for p in lista_obj_pag_extra:
                        p.cod_pag_2art_terc_financ = pag
                        p.save()

                msg = 'Arquivo importado com sucesso!'
            except Exception as e:
                lista_form_pagamentos_extra_tab = []
                if 'cod_benef_terc' in str(e):
                    msg = 'Nenhum beneficiário vinculado na vigência. Verifique !'
                else:
                    msg = str(e)


            data = {
                'msg': msg,
                'lista_form_pagamentos_extra_tab': lista_form_pagamentos_extra_tab
            }

        return JsonResponse(data, safe=False)



class ImportaArquivosFatTer():
    def le_arquivo_acres_desc(self, arq_xlsx):
        xls = xlrd.open_workbook(str(arq_xlsx))
        plan = xls.sheet_by_index(0)



        lancamentos = []
        for i in range(plan.nrows):
            if i > 0:
                if i == plan.nrows:
                    break
                else:
                    row_lanc = LinhaExcelArquivoLanAcresDesc(
                        cod_lanc_banco=None,
                        serial_proj=plan.row_values(i)[0],
                        desc_tipo_lanc=plan.row_values(i)[1],
                        desc_ocorrencia_lan=plan.row_values(i)[2],
                        mapa_ocorrencia=int(plan.row_values(i)[3]),
                        data_ocorrencia=plan.row_values(i)[4],
                        mapa=int(plan.row_values(i)[5]),
                        placa=plan.row_values(i)[6],
                        valor=plan.row_values(i)[7],
                        observacao=plan.row_values(i)[8],
                        status_importacao=None
                    )
                    lancamentos.append(row_lanc)
        return lancamentos

    def le_arquivo_acres_desc_v1(self, arq_xlsx):
        xls = xlrd.open_workbook(str(arq_xlsx))
        plan = xls.sheet_by_index(0)

        data_atual = datetime.now()

        lancamentos = []
        for i in range(plan.nrows):
            if i > 0:
                if i == plan.nrows:
                    break
                else:
                    row_lanc = LinhaExcelArquivoLanAcresDesc(
                        cod_lanc_banco=None,
                        serial_proj=plan.row_values(i)[0],
                        desc_tipo_lanc=plan.row_values(i)[1],
                        desc_ocorrencia_lan='',
                        mapa_ocorrencia=int(plan.row_values(i)[2]),
                        data_ocorrencia=None,
                        mapa=int(plan.row_values(i)[3]),
                        placa='',
                        valor=plan.row_values(i)[4],
                        observacao=plan.row_values(i)[5],
                        status_importacao=None
                    )
                    lancamentos.append(row_lanc)
        return lancamentos

    def le_arquivo_pagamentos_extra(self, arq_xlsx):
        xls = xlrd.open_workbook(str(arq_xlsx))
        plan = xls.sheet_by_index(0)


        lancamentos = []
        for i in range(plan.nrows):
            if i > 0:
                if i == plan.nrows:
                    break
                else:
                    row_lanc = LinhaExcelArquivoPagamentosExtra(
                        cod_lanc_banco=None,
                        doc_benef='',
                        data=plan.row_values(i)[0],
                        mapa=int(plan.row_values(i)[1]),
                        tipo_ocorrencia=plan.row_values(i)[2],
                        placa=plan.row_values(i)[3],
                        desc=plan.row_values(i)[4],
                        acres=plan.row_values(i)[5],
                        valor=plan.row_values(i)[6],
                        periodo_ref=plan.row_values(i)[7],
                        observacao=plan.row_values(i)[8],
                        status_importacao=None
                    )
                    lancamentos.append(row_lanc)
        return lancamentos

    def le_arquivo_pagamentos_extra_v1(self, arq_xlsx):
        xls = xlrd.open_workbook(str(arq_xlsx))
        plan = xls.sheet_by_index(0)

        data_atual = datetime.now()
        competencia = datetime.strftime(data_atual, '%Y-%m') + '-01'

        lancamentos = []
        for i in range(plan.nrows):
            if i > 0:
                if i == plan.nrows:
                    break
                else:
                    row_lanc = LinhaExcelArquivoPagamentosExtra(
                        cod_lanc_banco=None,
                        doc_benef='',
                        data=datetime.strftime(data_atual, '%Y-%m-%d'),
                        mapa=0,
                        tipo_ocorrencia='Apoio',
                        placa=plan.row_values(i)[0],
                        desc=0,
                        acres=0,
                        valor=plan.row_values(i)[1],
                        periodo_ref=competencia,
                        observacao=plan.row_values(i)[2],
                        status_importacao=None
                    )
                    lancamentos.append(row_lanc)
        return lancamentos


class Form_Relatorio_Pagamentos_Terc_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        cad_projetos = Proj_Usu.objects.filter(cod_usu=usuario_portal,
                                               cod_projeto__cod_atividade__desc2_atividade='Terceiro',
                                               status_proj_usu='S')

        context = {
            "cad_projetos": cad_projetos,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'plan_controle_fat_2art_terc_app/form_relatorio_pagamento_terceiros.html', context)



class Tab_Relatorio_Pagamentos_Terc_View(View):
    def get(self, request):
        cod_projeto = request.GET['cod_projeto']
        cod_benef = request.GET['cod_benef']
        periodo_ref = request.GET['periodo_ref']
        cod_pag = request.GET['cod_pag']
        tipo_ocorr = request.GET['tipo_ocorr']
        tipo_relatorio = request.GET['tipo_relatorio']
        quinzena = request.GET['quinzena']

        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()

        tipo_tabela = ''
        registros_tab_pagamentos_terc = self.gera_dados_pagamento_terceiro(cod_projeto, cod_benef, periodo_ref,
                                                                              cod_pag, tipo_ocorr, tipo_relatorio,
                                                                              quinzena)
        '''for reg in registros_tab_pagamentos_terc_gerados:
            registros_tab_pagamentos_terc.append(reg.__dict__)'''

        if tipo_relatorio == 'rel_proj_periodo_tipo':
            tipo_tabela = tipo_ocorr

        #lista_itens_mapas_pagos_pagamento = self.retorna_itens_mapa_pagamento(cod_pag)

        context = {
            'tipo_ocorr': tipo_ocorr,
            'tipo_tabela': tipo_tabela,
            'registros_tab_pagamentos_terc': registros_tab_pagamentos_terc,
            'tipo_corporativo_usuario': usuario_portal.corporativo,
            #'lista_itens_mapas_pagos_pagamento': lista_itens_mapas_pagos_pagamento
        }
        #return JsonResponse(data, safe=False)
        return render(request, 'plan_controle_fat_2art_terc_app/lista_pagamentos_fat_benef_terc.html', context)

    def gera_dados_pagamento_terceiro(self, cod_projeto, cod_benef, periodo_ref, cod_pag, tipo_ocorr, tipo_relatorio,quinzena):
        obj_beneficiario = BeneficiarioTerceiro.objects.filter(cod_benef_terc=cod_benef).first()
        obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto).first()
        periodo_ref_str = '01/' + periodo_ref.split('-')[1] + '/' + periodo_ref.split('-')[0]

        dia_inicial = quinzena.split(',')[0]
        dia_final = quinzena.split(',')[1]

        periodo_ref_date = datetime.strptime(periodo_ref_str, '%d/%m/%Y')
        tipo_tabela = ''
        registros_tab_pagamentos_terc = []
        # uteis = Uteis()
        # registros = uteis.retorna_pagamentos_beneficiario_terc_finan(obj_beneficiario, periodo_ref_date, cod_pag, tipo_ocorr)
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        if tipo_relatorio == 'rel_proj_periodo_tipo':
            obj_projeto = Projeto.objects.filter(cod_projeto=cod_projeto).first()
            pagamentos = Pagamento2ArtTerceirosFinanceiro.objects.filter(periodo_ref_pag=periodo_ref_date,
                                                                         cod_benef_terc__cod_projeto=obj_projeto,
                                                                         cod_tipo_ocor_financ_terc__tipo_lancamento=tipo_ocorr,
                                                                         data_geracao_pag__day__range=[dia_inicial,
                                                                                                       dia_final]
                                                                         ).order_by('num_doc_pagamento')
            if tipo_ocorr == 'E':
                for pagamento in pagamentos:

                    nome_usu_estorno = ''
                    data_estorno = ''
                    justificativa_estorno = ''
                    obj_estorno = (Estorno_Pagamentos_2Art_Terc.objects
                                   .filter(tipo_pagamento='E', cod_pagamento_referente=pagamento.cod_pag_2art_terc_financ)
                                   .first())
                    if obj_estorno != None:
                        nome_usu_estorno = obj_estorno.cod_usu.login_usu
                        data_estorno = datetime.strftime(obj_estorno.data_hora_estorno, '%d-%m-%Y %H:%M')
                        justificativa_estorno = obj_estorno.justificativa

                    lista_itens_mapas_pagamento = []
                    lista_obj_pag_extra = LancamentoPagamentoExtras.objects.filter(cod_pag_2art_terc_financ=pagamento)
                    for pag_extra in lista_obj_pag_extra:
                        registro = {
                            'data': datetime.strftime(pag_extra.data_pag_extra, '%d-%m-%y'),
                            'placa': pag_extra.placa_pag_extra,
                            'val_pagar': locale.currency(round(pag_extra.val_pag_extra, 2), grouping=True, symbol=None),
                            'obs':  pag_extra.obs_pag_extra,
                        }
                        lista_itens_mapas_pagamento.append(registro)


                    linha_tab_pagamentos_terc = {
                        'cod_pag': pagamento.cod_pag_2art_terc_financ,
                        'cod_benef': pagamento.cod_benef_terc.cod_benef_terc,
                        'doc_benef': pagamento.cod_benef_terc.doc_benef_terc,
                        'nome_beneficiario': pagamento.cod_benef_terc.nome_benef_terc,
                        'data': datetime.strftime(pagamento.data_geracao_pag, '%d-%m-%y'),
                        'desc': locale.currency(round(pagamento.desc_pag, 2), grouping=True, symbol=None),
                        'acres':locale.currency(round(pagamento.acresc_pag, 2), grouping=True, symbol=None),
                        'val_pagar': locale.currency(round(pagamento.val_pago, 2), grouping=True, symbol=None),
                        'complemento': pagamento.complemento_pag,
                        'serial_pag_proj': pagamento.cod_benef_terc.cod_projeto.cod_serial_pag_terc,
                        'status_pag': pagamento.status_pagamento,
                        'nome_usu_status': pagamento.cod_usu.nome_usu,
                        'num_doc_pagamento': pagamento.num_doc_pagamento,
                        'nome_usu_estorno': nome_usu_estorno,
                        'data_estorno': data_estorno,
                        'justificativa_estorno': justificativa_estorno,
                        'lista_itens_mapas_pagamento': lista_itens_mapas_pagamento
                    }
                    registros_tab_pagamentos_terc.append(linha_tab_pagamentos_terc)
            elif tipo_ocorr == 'M':
                for pagamento in pagamentos:

                    nome_usu_estorno = ''
                    data_estorno = ''
                    justificativa_estorno = ''
                    obj_estorno = (Estorno_Pagamentos_2Art_Terc.objects
                                   .filter(tipo_pagamento='M', cod_pagamento_referente=pagamento.cod_pag_2art_terc_financ)
                                   .first())
                    if obj_estorno != None:
                        nome_usu_estorno = obj_estorno.cod_usu.login_usu
                        data_estorno = datetime.strftime(obj_estorno.data_hora_estorno, '%d-%m-%Y %H:%M')
                        justificativa_estorno = obj_estorno.justificativa

                    lista_itens_mapas_pagamento = []
                    mapas = Registro2ArtTerceirosFinanceiro.objects.filter(cod_pag_2art_terc_financ=pagamento)
                    locale.setlocale(locale.LC_MONETARY, 'pt-BR')
                    for mapa in mapas:
                        cont_item = 1
                        val_total_desc_mapa = 0.00
                        lanc_desc_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                            cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                            tipo_lancamento='D',
                            status_exclusao='N').aggregate(total_valor_lanc=Sum('valor_lanc'))
                        if lanc_desc_mapa['total_valor_lanc'] is not None:
                            val_total_desc_mapa = lanc_desc_mapa['total_valor_lanc']

                        val_total_acresc_mapa = 0.00
                        lanc_acres_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                            cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                            tipo_lancamento='A', status_exclusao='N').aggregate(
                            total_valor_lanc=Sum('valor_lanc'))
                        if lanc_acres_mapa['total_valor_lanc'] is not None:
                            val_total_acresc_mapa = lanc_acres_mapa['total_valor_lanc']

                        concatena_obs_lanc_desc = ''
                        obj_lanc_obs_desc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                            cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                            tipo_lancamento='D', status_exclusao='N').values('obs_lanc')
                        for text in obj_lanc_obs_desc:
                            concatena_obs_lanc_desc += text['obs_lanc']

                        concatena_obs_lanc_acres = ''
                        obj_lanc_obs_acresc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                            cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                            tipo_lancamento='A', status_exclusao='N').values('obs_lanc')
                        for text in obj_lanc_obs_acresc:
                            concatena_obs_lanc_acres += text['obs_lanc']

                        linha_tab_pagamentos_terc = {
                            'cod_pag': mapa.cod_pag_2art_terc_financ.cod_pag_2art_terc_financ,
                            'cod_benef': mapa.cod_pag_2art_terc_financ.cod_benef_terc.cod_benef_terc,
                            'doc_benef': mapa.cod_pag_2art_terc_financ.cod_benef_terc.doc_benef_terc,
                            'nome_beneficiario': mapa.cod_pag_2art_terc_financ.cod_benef_terc.nome_benef_terc,
                            'data': datetime.strftime(mapa.data_2art_terc_financ, '%d-%m-%y'),
                            'mapa': mapa.mapa_2art_terc_financ,
                            'placa': mapa.placa_2art_terc_financ,
                            'val_frete': locale.currency(round(mapa.val_a_pagar_pago, 2), grouping=True, symbol=None),
                            'desc': locale.currency(round(val_total_desc_mapa, 2), grouping=True, symbol=None),
                            'acres': locale.currency(round(val_total_acresc_mapa, 2), grouping=True, symbol=None),
                            'val_pagar': locale.currency(round((decimal.Decimal(mapa.val_a_pagar_pago) - decimal.Decimal(
                                val_total_desc_mapa)) + decimal.Decimal(val_total_acresc_mapa), 2), grouping=True,
                                                      symbol=None),
                            'complemento': '',
                            'tipo_ocorrencia': '',
                            'serial_pag_proj': mapa.cod_projeto.cod_serial_pag_terc,
                            'obs_desc': concatena_obs_lanc_desc,
                            'obs_acresc': concatena_obs_lanc_acres,
                            'seq_item': cont_item,
                            'status_pag': mapa.cod_pag_2art_terc_financ.status_pagamento,
                            'nome_usu_status': mapa.cod_pag_2art_terc_financ.cod_usu.nome_usu,
                            'num_doc_pagamento': mapa.cod_pag_2art_terc_financ.num_doc_pagamento
                        }
                        cont_item += 1
                        lista_itens_mapas_pagamento.append(linha_tab_pagamentos_terc)


                    linha_tab_pagamentos_terc = {
                        'cod_pag': pagamento.cod_pag_2art_terc_financ,
                        'cod_benef': pagamento.cod_benef_terc.cod_benef_terc,
                        'doc_benef': pagamento.cod_benef_terc.doc_benef_terc,
                        'nome_beneficiario': pagamento.cod_benef_terc.nome_benef_terc,
                        'data': datetime.strftime(pagamento.data_geracao_pag, '%d-%m-%y'),
                        'val_frete': locale.currency(round((decimal.Decimal(pagamento.val_pago) + decimal.Decimal(
                            pagamento.desc_pag)) - decimal.Decimal(pagamento.acresc_pag), 2), grouping=True,
                                                  symbol=None),
                        'desc': locale.currency(round(pagamento.desc_pag, 2), grouping=True, symbol=None),
                        'acres': locale.currency(round(pagamento.acresc_pag, 2), grouping=True, symbol=None),
                        'val_pagar': locale.currency(round(pagamento.val_pago, 2), grouping=True, symbol=None),
                        'complemento': '',
                        'tipo_ocorrencia': pagamento.cod_tipo_ocor_financ_terc.desc_ocorrencia,
                        'serial_pag_proj': pagamento.cod_benef_terc.cod_projeto.cod_serial_pag_terc,
                        'obs_desc': pagamento.obs_pag,
                        'obs_acresc': '',
                        'status_pag': pagamento.status_pagamento,
                        'nome_usu_status': pagamento.cod_usu.nome_usu,
                        'num_doc_pagamento': pagamento.num_doc_pagamento,
                        'nome_usu_estorno': nome_usu_estorno,
                        'data_estorno': data_estorno,
                        'justificativa_estorno': justificativa_estorno,
                        'lista_itens_mapas_pagamento': lista_itens_mapas_pagamento
                    }
                    # print('Cód. pag '+str(pagamento.cod_pag_2art_terc_financ)+' status: '+str(pagamento.status_pagamento))
                    registros_tab_pagamentos_terc.append(linha_tab_pagamentos_terc)

        return registros_tab_pagamentos_terc

    def retorna_itens_mapa_pagamento(self, cod_2art_terc_financ):
        lista_mapas_pagos_pagamento = []
        obj_pag_terc = Pagamento2ArtTerceirosFinanceiro.objects.filter(
            cod_pag_2art_terc_financ=cod_2art_terc_financ).first()
        if obj_pag_terc.cod_tipo_ocor_financ_terc.tipo_lancamento == 'M':
            mapas = Registro2ArtTerceirosFinanceiro.objects.filter(
                cod_pag_2art_terc_financ__cod_pag_2art_terc_financ=cod_2art_terc_financ)
            locale.setlocale(locale.LC_MONETARY, 'pt-BR')
            for mapa in mapas:
                cont_item = 1
                val_total_desc_mapa = 0.00
                lanc_desc_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                    cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                    tipo_lancamento='D',
                    status_exclusao='N').aggregate(total_valor_lanc=Sum('valor_lanc'))
                if lanc_desc_mapa['total_valor_lanc'] is not None:
                    val_total_desc_mapa = lanc_desc_mapa['total_valor_lanc']

                val_total_acresc_mapa = 0.00
                lanc_acres_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                    cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                    tipo_lancamento='A', status_exclusao='N').aggregate(
                    total_valor_lanc=Sum('valor_lanc'))
                if lanc_acres_mapa['total_valor_lanc'] is not None:
                    val_total_acresc_mapa = lanc_acres_mapa['total_valor_lanc']

                concatena_obs_lanc_desc = ''
                obj_lanc_obs_desc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                    cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                    tipo_lancamento='D', status_exclusao='N').values('obs_lanc')
                for text in obj_lanc_obs_desc:
                    concatena_obs_lanc_desc += text['obs_lanc']

                concatena_obs_lanc_acres = ''
                obj_lanc_obs_acresc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                    cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                    tipo_lancamento='A', status_exclusao='N').values('obs_lanc')
                for text in obj_lanc_obs_acresc:
                    concatena_obs_lanc_acres += text['obs_lanc']

                linha_tab_pagamentos_terc = Tab_Pagamentos_Terceiros(
                    cod_pag=mapa.cod_pag_2art_terc_financ.cod_pag_2art_terc_financ,
                    cod_benef=mapa.cod_pag_2art_terc_financ.cod_benef_terc.cod_benef_terc,
                    doc_benef=mapa.cod_pag_2art_terc_financ.cod_benef_terc.doc_benef_terc,
                    nome_beneficiario=mapa.cod_pag_2art_terc_financ.cod_benef_terc.nome_benef_terc,
                    data=datetime.strftime(mapa.data_2art_terc_financ, '%d-%m-%y'),
                    mapa=mapa.mapa_2art_terc_financ,
                    placa=mapa.placa_2art_terc_financ,
                    val_frete=locale.currency(round(mapa.val_a_pagar_pago, 2), grouping=True, symbol=None),
                    desc=locale.currency(round(val_total_desc_mapa, 2), grouping=True, symbol=None),
                    acres=locale.currency(round(val_total_acresc_mapa, 2), grouping=True, symbol=None),
                    val_pagar=locale.currency(round((decimal.Decimal(mapa.val_a_pagar_pago) - decimal.Decimal(
                        val_total_desc_mapa)) + decimal.Decimal(val_total_acresc_mapa), 2), grouping=True, symbol=None),
                    complemento='',
                    tipo_ocorrencia='',
                    serial_pag_proj=mapa.cod_projeto.cod_serial_pag_terc,
                    obs_desc=concatena_obs_lanc_desc,
                    obs_acresc=concatena_obs_lanc_acres,
                    seq_item=cont_item,
                    status_pag=mapa.cod_pag_2art_terc_financ.status_pagamento,
                    nome_usu_status=mapa.cod_pag_2art_terc_financ.cod_usu.nome_usu,
                    num_doc_pagamento=mapa.cod_pag_2art_terc_financ.num_doc_pagamento
                )
                cont_item += 1
                lista_mapas_pagos_pagamento.append(linha_tab_pagamentos_terc.__dict__)
        elif obj_pag_terc.cod_tipo_ocor_financ_terc.tipo_lancamento == 'E':
            cont_item = 1
            lista_obj_pag_extra = LancamentoPagamentoExtras.objects.filter(cod_pag_2art_terc_financ=obj_pag_terc)
            for pag_extra in lista_obj_pag_extra:
                nome_usu_estorno = ''
                data_estorno = ''
                justificativa_estorno = ''
                obj_estorno = (Estorno_Pagamentos_2Art_Terc.objects
                               .filter(tipo_pagamento='E',
                                       cod_pagamento_referente=pag_extra.cod_pag_2art_terc_financ.cod_pag_2art_terc_financ)
                               .first())
                if obj_estorno != None:
                    nome_usu_estorno = obj_estorno.cod_usu.login_usu
                    data_estorno = datetime.strftime(obj_estorno.data_hora_estorno, '%d-%m-%Y %H:%M')
                    justificativa_estorno = obj_estorno.justificativa

                linha_tab_pagamentos_terc = Tab_Pagamentos_Terceiros(
                    cod_pag=pag_extra.cod_pag_2art_terc_financ.cod_pag_2art_terc_financ,
                    cod_benef=obj_pag_terc.cod_benef_terc.cod_benef_terc,
                    doc_benef=obj_pag_terc.cod_benef_terc.doc_benef_terc,
                    nome_beneficiario=obj_pag_terc.cod_benef_terc.nome_benef_terc,
                    data=datetime.strftime(pag_extra.data_pag_extra, '%d-%m-%y'),
                    mapa=pag_extra.mapa_pag_extra,
                    placa=pag_extra.placa_pag_extra,
                    val_frete=0.00,
                    desc=locale.currency(round(pag_extra.desc_pag_extra, 2), grouping=True, symbol=None),
                    acres=locale.currency(round(pag_extra.acresc_pag_extra, 2), grouping=True, symbol=None),
                    val_pagar=locale.currency(round(pag_extra.val_pag_extra, 2), grouping=True, symbol=None),
                    complemento='',
                    tipo_ocorrencia=pag_extra.cod_tipo_ocor_financ_terc.tipo_lancamento,
                    serial_pag_proj=obj_pag_terc.cod_benef_terc.cod_projeto.cod_serial_pag_terc,
                    obs_desc='',
                    obs_acresc=pag_extra.obs_pag_extra,
                    seq_item=cont_item,
                    status_pag=obj_pag_terc.status_pagamento,
                    nome_usu_status=pag_extra.cod_pag_2art_terc_financ.cod_usu.nome_usu,
                    num_doc_pagamento=obj_pag_terc.num_doc_pagamento,
                    nome_usu_estorno=nome_usu_estorno,
                    data_estorno=data_estorno,
                    justificativa_estorno=justificativa_estorno
                )
                cont_item += 1
                lista_mapas_pagos_pagamento.append(linha_tab_pagamentos_terc.__dict__)


        return lista_mapas_pagos_pagamento


class Tab_Relatorio_Mapas_Pagamentos_Terc_View(View):
    def get_object(self, pk):
        try:
            return Pagamento2ArtTerceirosFinanceiro.objects.get(pk=pk)
        except Pagamento2ArtTerceirosFinanceiro.DoesNotExist:
            raise Http404




    def delete(self, request, pk):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.filter(cod_usu=id_usu_session).first()


        data_hora_atual = datetime.now()
        data_atual_yyyy_mm_aa = data_hora_atual.strftime('%Y-%m-%d')
        obs_pagamento = ''
        pagamento = self.get_object(pk)
        if pagamento.cod_tipo_ocor_financ_terc.tipo_lancamento == 'M':
            mapas = Registro2ArtTerceirosFinanceiro.objects.filter(cod_pag_2art_terc_financ=pagamento)
            mapas_atualizados = []
            for reg in mapas:
                reg.status_financeiro_2art_terc_financ = 'A'
                reg.data_status_financeiro_2art_terc_financ = data_atual_yyyy_mm_aa
                reg.valor_frete_calculado_pago = None
                reg.val_a_pagar_pago = None
                reg.val_conlog_pago = None
                reg.cod_pag_2art_terc_financ = None
                reg.save()
                mapas_atualizados.append(reg.mapa_2art_terc_financ)
            obs_pagamento = '.Pagamento excluído em ' + str(data_hora_atual) + '. Referente aos mapas : ' + str(
                mapas_atualizados) + ' Por: ' + obj_usuario.nome_usu
        else:
            obs_pagamento = '.Pagamento excluído em ' + str(data_hora_atual) + ' Por: ' + obj_usuario.nome_usu

        pagamento.status_pagamento = 'E'
        pagamento.cod_usu = obj_usuario
        pagamento.obs_pag += obs_pagamento
        pagamento.save()

        '''Registra o registro do estorno'''
        data = json.loads(request.body)
        justificativa_frm = data.get("justificativa")
        tipo_pagamento_frm = data.get("tipo_pagamento")
        obj_estorno = Estorno_Pagamentos_2Art_Terc(
            tipo_pagamento=tipo_pagamento_frm,
            cod_pagamento_referente=pk,
            data_hora_estorno=data_hora_atual,
            justificativa=justificativa_frm,
            cod_usu=obj_usuario
        ).save()


        data = dict()
        data = {
            'msg': 'Pagamento ' + str(pagamento.cod_pag_2art_terc_financ) + ' estornado com sucesso.',
        }
        return JsonResponse(data, safe=False)



class Pdf_Rel_Pagamento_Terc(View):
    def get(self, request):
        cod_2art_terc_financ = request.GET.get('cod_pagamento', None)
        tipo_relatorio = request.GET.get('tipo_relatorio', None)
        tipo_pagamento = request.GET.get('tipo_pagamento', None)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        tipo_tabela = ''
        periodo_ref_date = ''
        nome_beneficiario = ''
        nome_filial = ''
        serial_projeto = ''
        cod_pagamento = ''
        num_doc_pagamento = ''
        total_val_frete = 0.00
        total_descontos = 0.00
        total_acrescimos = 0.00
        total_a_pagar = 0.
        registros_tab_pagamentos_terc = []
        qtd_pagina = []



        if tipo_relatorio == 'rel_proj_periodo_tipo':
            if tipo_pagamento == 'M':
                tipo_tabela = 'M'
                pagamento = Pagamento2ArtTerceirosFinanceiro.objects.filter(cod_pag_2art_terc_financ=cod_2art_terc_financ).first()
                periodo_ref_date = datetime.strftime(pagamento.periodo_ref_pag, '%m/%Y')
                nome_beneficiario = pagamento.cod_benef_terc.doc_benef_terc + ' - '+pagamento.cod_benef_terc.nome_benef_terc
                nome_filial = pagamento.cod_benef_terc.cod_projeto.desc_proj
                cod_pagamento = pagamento.cod_pag_2art_terc_financ
                num_doc_pagamento = pagamento.num_doc_pagamento
                serial_projeto = pagamento.cod_benef_terc.cod_projeto.cod_serial_pag_terc
                total_val_frete = round((pagamento.val_pago + pagamento.desc_pag) - pagamento.acresc_pag, 2)
                total_descontos = round(pagamento.desc_pag, 2)
                total_acrescimos = round(pagamento.acresc_pag, 2)
                total_a_pagar = round(pagamento.val_pago, 2)
                mapas = Registro2ArtTerceirosFinanceiro.objects.filter(cod_pag_2art_terc_financ=pagamento)
                cont_item = 1
                pagina_atual = 1
                qtd_pagina.append(pagina_atual)
                for mapa in mapas:
                    #print('Item = ' + str(cont_item))
                    pagina_nova = 0
                    #print('Pagina atual = ' + str(pagina_atual))
                    #print('trunc cont_item / 20 = ' + str(trunc(cont_item / 20)))

                    if (trunc(cont_item / 12)) < 1:
                        pagina_nova = 1
                    else:
                        pagina_nova = trunc(cont_item / 12) + 1
                    #print('Pagina nova : ' + str(pagina_nova))
                    if pagina_nova != pagina_atual:
                        pagina_atual = pagina_nova
                        qtd_pagina.append(pagina_atual)
                    val_total_desc_mapa = 0.00
                    lanc_desc_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                        tipo_lancamento='D',
                        status_exclusao='N').aggregate(total_valor_lanc=Sum('valor_lanc'))
                    if lanc_desc_mapa['total_valor_lanc'] is not None:
                        val_total_desc_mapa = lanc_desc_mapa['total_valor_lanc']

                    val_total_acresc_mapa = 0.00
                    lanc_acres_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                        tipo_lancamento='A', status_exclusao='N').aggregate(
                        total_valor_lanc=Sum('valor_lanc'))
                    if lanc_acres_mapa['total_valor_lanc'] is not None:
                        val_total_acresc_mapa = lanc_acres_mapa['total_valor_lanc']

                    #concatena_obs_lanc_desc = ''
                    obj_lanc_obs_desc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                        tipo_lancamento='D', status_exclusao='N').values('obs_lanc')
                    #for text in obj_lanc_obs_desc:
                    #    concatena_obs_lanc_desc += text['obs_lanc']

                    #concatena_obs_lanc_acres = ''
                    obj_lanc_obs_acresc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art_terc_financ=mapa.cod_reg_2art_terc_financ,
                        tipo_lancamento='A', status_exclusao='N').values('obs_lanc')
                    #for text in obj_lanc_obs_acresc:
                    #    concatena_obs_lanc_acres += text['obs_lanc']

                    linha_tab_pagamentos_terc = Tab_Pagamentos_Terceiros(
                        cod_pag=cod_pagamento,
                        cod_benef=mapa.cod_pag_2art_terc_financ.cod_benef_terc.cod_benef_terc,
                        doc_benef=mapa.cod_pag_2art_terc_financ.cod_benef_terc.doc_benef_terc,
                        nome_beneficiario=mapa.cod_pag_2art_terc_financ.cod_benef_terc.nome_benef_terc,
                        data=datetime.strftime(mapa.data_2art_terc_financ, '%d-%m-%y'),
                        mapa=mapa.mapa_2art_terc_financ,
                        placa=mapa.placa_2art_terc_financ,
                        val_frete=round(mapa.val_a_pagar_pago, 2),
                        desc=round(val_total_desc_mapa, 2),
                        acres=round(val_total_acresc_mapa, 2),
                        val_pagar=round((decimal.Decimal(mapa.val_a_pagar_pago) - decimal.Decimal(val_total_desc_mapa)) + decimal.Decimal(val_total_acresc_mapa), 2),
                        complemento='',
                        tipo_ocorrencia='',
                        serial_pag_proj=serial_projeto,
                        obs_desc=pagamento.obs_pag,
                        obs_acresc='',
                        seq_item=pagina_atual,
                        status_pag=pagamento.status_pagamento,
                        nome_usu_status=pagamento.cod_usu.nome_usu,
                        num_doc_pagamento=pagamento.num_doc_pagamento,
                        nome_usu_estorno='',
                        data_estorno='',
                        justificativa_estorno=''
                    )
                    cont_item += 1
                    registros_tab_pagamentos_terc.append(linha_tab_pagamentos_terc)
            elif tipo_pagamento == 'E':
                tipo_tabela = 'E'
                pagamento = Pagamento2ArtTerceirosFinanceiro.objects.filter(
                    cod_pag_2art_terc_financ=cod_2art_terc_financ).first()
                periodo_ref_date = datetime.strftime(pagamento.periodo_ref_pag, '%m/%Y')
                nome_beneficiario = pagamento.cod_benef_terc.doc_benef_terc + ' - ' + pagamento.cod_benef_terc.nome_benef_terc
                nome_filial = pagamento.cod_benef_terc.cod_projeto.desc_proj
                cod_pagamento = pagamento.cod_pag_2art_terc_financ
                num_doc_pagamento = pagamento.num_doc_pagamento
                serial_projeto = pagamento.cod_benef_terc.cod_projeto.cod_serial_pag_terc
                total_val_frete = round((pagamento.val_pago + pagamento.desc_pag) - pagamento.acresc_pag, 2)
                total_descontos = round(pagamento.desc_pag, 2)
                total_acrescimos = round(pagamento.acresc_pag, 2)
                total_a_pagar = round(pagamento.val_pago, 2)
                pag_extras = LancamentoPagamentoExtras.objects.filter(cod_pag_2art_terc_financ=pagamento)
                cont_item = 1
                pagina_atual = 1
                qtd_pagina.append(pagina_atual)
                for extra in pag_extras:
                    # print('Item = ' + str(cont_item))
                    pagina_nova = 0
                    # print('Pagina atual = ' + str(pagina_atual))
                    # print('trunc cont_item / 20 = ' + str(trunc(cont_item / 20)))

                    if (trunc(cont_item / 12)) < 1:
                        pagina_nova = 1
                    else:
                        pagina_nova = trunc(cont_item / 12) + 1
                    # print('Pagina nova : ' + str(pagina_nova))
                    if pagina_nova != pagina_atual:
                        pagina_atual = pagina_nova
                        qtd_pagina.append(pagina_atual)



                    linha_tab_pagamentos_terc = Tab_Pagamentos_Terceiros(
                        cod_pag=cod_pagamento,
                        cod_benef=pagamento.cod_benef_terc.cod_benef_terc,
                        doc_benef=pagamento.cod_benef_terc.doc_benef_terc,
                        nome_beneficiario=pagamento.cod_benef_terc.nome_benef_terc,
                        data=datetime.strftime(extra.data_pag_extra, '%d-%m-%y'),
                        mapa=extra.mapa_pag_extra,
                        placa=extra.placa_pag_extra,
                        val_frete=round(0.00, 2),
                        desc=extra.desc_pag_extra,
                        acres=extra.acresc_pag_extra,
                        val_pagar=round(extra.val_pag_extra, 2),
                        complemento='',
                        tipo_ocorrencia=extra.cod_tipo_ocor_financ_terc.desc_ocorrencia,
                        serial_pag_proj=serial_projeto,
                        obs_desc=extra.obs_pag_extra,
                        obs_acresc='',
                        seq_item=pagina_atual,
                        status_pag=pagamento.status_pagamento,
                        nome_usu_status=pagamento.cod_usu.nome_usu,
                        num_doc_pagamento=pagamento.num_doc_pagamento,
                        nome_usu_estorno= '',
                        data_estorno='',
                        justificativa_estorno=''
                    )
                    cont_item += 1
                    registros_tab_pagamentos_terc.append(linha_tab_pagamentos_terc)

        if tipo_tabela == 'M':
            params = {
                'serial_projeto' : serial_projeto,
                'periodo_ref' : periodo_ref_date,
                'nome_beneficiario' : nome_beneficiario,
                'nome_filial' : nome_filial,
                'cod_pagamento' : cod_pagamento,
                'num_doc_pagamento' : num_doc_pagamento,
                'registros_tab_pagamentos_terc' : registros_tab_pagamentos_terc,
                'total_val_frete' : locale.currency(total_val_frete, grouping=True, symbol=None),
                'total_descontos' : locale.currency(total_descontos, grouping=True, symbol=None),
                'total_acrescimos' : locale.currency(total_acrescimos, grouping=True, symbol=None),
                'total_a_pagar' : locale.currency(total_a_pagar, grouping=True, symbol=None),
                'qtd_pagina' : qtd_pagina,
                'ultima_pagina':str(len(qtd_pagina)),
                'tipo_pag' : 'M'
            }
            return Render.render('plan_controle_fat_2art_terc_app/rel_pdf_pagamentos_2art_terc.html', params, 'myfile')
        elif tipo_tabela == 'E':
            params = {
                'serial_projeto': serial_projeto,
                'periodo_ref' : periodo_ref_date,
                'nome_beneficiario' : nome_beneficiario,
                'nome_filial' : nome_filial,
                'cod_pagamento': cod_pagamento,
                'num_doc_pagamento': num_doc_pagamento,
                'registros_tab_pagamentos_terc' : registros_tab_pagamentos_terc,
                'total_a_pagar' : locale.currency(total_a_pagar,grouping=True, symbol=None),
                'total_val_frete': locale.currency(total_a_pagar,grouping=True, symbol=None),
                'total_descontos': locale.currency(0.00, grouping=True, symbol=None),
                'total_acrescimos': locale.currency(0.00, grouping=True, symbol=None),
                'qtd_pagina': qtd_pagina,
                'ultima_pagina': str(len(qtd_pagina)),
                'tipo_pag': 'E'
            }
            #return Render.render('rel_pdf_pagamentos_extras_terc.html', params, 'myfile')
            return Render.render('plan_controle_fat_2art_terc_app/rel_pdf_pagamentos_2art_terc.html', params, 'myfile')


class Pdf_Rel_Acres_Desc_Pagamento_Terc(View):
    def get(self, request):
        cod_pag_2art_terc_financ_form = request.GET.get('cod_pagamento', None)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        periodo_ref_date = ''
        nome_beneficiario = ''
        nome_filial = ''
        serial_projeto = ''
        cod_pagamento = ''
        num_doc_pagamento = ''
        total_val_frete = 0.00
        total_descontos = 0.00
        registros_tab_lancamento_terc = []
        qtd_pagina = []



        pagamento = Pagamento2ArtTerceirosFinanceiro.objects.filter(cod_pag_2art_terc_financ=cod_pag_2art_terc_financ_form).first()
        periodo_ref_date = datetime.strftime(pagamento.periodo_ref_pag, '%m/%Y')
        nome_beneficiario = pagamento.cod_benef_terc.doc_benef_terc + ' - '+pagamento.cod_benef_terc.nome_benef_terc
        nome_filial = pagamento.cod_benef_terc.cod_projeto.desc_proj
        cod_pagamento = pagamento.cod_pag_2art_terc_financ
        num_doc_pagamento = pagamento.num_doc_pagamento
        serial_projeto = pagamento.cod_benef_terc.cod_projeto.cod_serial_pag_terc
        total_descontos = round(pagamento.desc_pag, 2)
        total_acrescimos = round(pagamento.acresc_pag, 2)
        tab_lancamentos_pagamento_terc = []

        #mapas = Registro2ArtTerceirosFinanceiro.objects.filter(cod_pag_2art_terc_financ=pagamento)
        registros_tab_lancamento_terc = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
            cod_reg_2art_terc_financ__cod_pag_2art_terc_financ=pagamento, status_exclusao='N')
        #for r in registros_tab_lancamento_terc:

        cont_item = 1
        pagina_atual = 1
        qtd_pagina.append(pagina_atual)

        lanc_desc_mapa = registros_tab_lancamento_terc.filter(tipo_lancamento='D')\
            .aggregate(total_valor_lanc=Sum('valor_lanc'))
        if lanc_desc_mapa['total_valor_lanc'] is not None:
            total_descontos = lanc_desc_mapa['total_valor_lanc']

        lanc_asc_mapa = registros_tab_lancamento_terc.filter(tipo_lancamento='A') \
            .aggregate(total_valor_lanc=Sum('valor_lanc'))
        if lanc_asc_mapa['total_valor_lanc'] is not None:
            total_acrescimos = lanc_asc_mapa['total_valor_lanc']

        for lancamento in registros_tab_lancamento_terc:

            if (trunc(cont_item / 12)) < 1:
                pagina_nova = 1
            else:
                pagina_nova = trunc(cont_item / 12) + 1
            #print('Pagina nova : ' + str(pagina_nova))
            if pagina_nova != pagina_atual:
                pagina_atual = pagina_nova
                qtd_pagina.append(pagina_atual)
            #val_total_desc_mapa = 0.00

            desc_extenso_tipo_lanc = ''
            if lancamento.tipo_lancamento == 'A':
                desc_extenso_tipo_lanc = 'Acréscimo'
            elif lancamento.tipo_lancamento == 'D':
                desc_extenso_tipo_lanc = 'Desconto'

            linha_tab_pagamentos_terc = Tab_Lancamentos_Pagamento_Terceiros(
                tipo_lancamento = desc_extenso_tipo_lanc,
                desc_ocorrencia = lancamento.cod_tipo_ocor_financ_terc.desc_ocorrencia,
                mapa_ocorrencia = lancamento.mapa_ocorrencia,
                data_ocorrencia = datetime.strftime(lancamento.data_ocorrencia, '%d-%m-%y'),
                mapa = lancamento.cod_reg_2art_terc_financ.mapa_2art_terc_financ,
                placa = lancamento.placa_lanc,
                valor_lanc = round(lancamento.valor_lanc, 2),
                obs = lancamento.obs_lanc,
                seq_item=pagina_atual
            )
            cont_item += 1
            tab_lancamentos_pagamento_terc.append(linha_tab_pagamentos_terc)
        #for r in tab_lancamentos_pagamento_terc:
        #    print(r.mapa_ocorrencia)
        params = {
            'serial_projeto' : serial_projeto,
            'periodo_ref' : periodo_ref_date,
            'nome_beneficiario' : nome_beneficiario,
            'nome_filial' : nome_filial,
            'cod_pagamento' : cod_pagamento,
            'num_doc_pagamento' : num_doc_pagamento,
            'tab_lancamentos_pagamento_terc' : tab_lancamentos_pagamento_terc,
            'total_val_frete' : locale.currency(total_val_frete, grouping=True, symbol=None),
            'total_descontos' : locale.currency(total_descontos, grouping=True, symbol=None),
            'total_acrescimos' : locale.currency(total_acrescimos, grouping=True, symbol=None),
            'qtd_pagina' : qtd_pagina,
            'ultima_pagina':str(len(qtd_pagina)),
        }

        return Render.render('plan_controle_fat_2art_terc_app/rel_pdf_acresc_desc_pagamento_2art_terc.html', params, 'myfile')


class Frm_Upload_Layout_Cad_Frete_View(View):
    def get(self, request):
        file_path = os.path.join(BASE_DIR, 'media/docs/layouts/Layout_Atualizacao_Fretes_Plan_Controle_Pag_Terc.xlsx')
        return FileResponse(open(file_path, 'rb'), as_attachment=True)

    def post(self, request):
        file_update_fretes_frm = request.FILES['file_update_fretes']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')
        caminho_arq_importado = ('docs/fat_terceiros_update_fretes/' + obj_usu.login_usu.replace('.', '_') + '_' +
                                 str(data_atual_dd_mm_yyyy).replace('/', '_') + '_' +
                                 str(hota_atual).replace(':', '_') + '.xlsx')

        obj_arq_update_cad_frete = Arq_Update_Cad_Frete(
            tipo_update = 'A',
            arq_update = caminho_arq_importado,
            cod_usu = obj_usu
        ).save()
        fs = FileSystemStorage()
        filename = fs.save(caminho_arq_importado, file_update_fretes_frm)
        upload_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado)
        df_conteudo_arq = pd.read_excel(upload_file_url)
        df_conteudo_arq.rename(columns=lambda x : str(x).strip(), inplace=True)
        df_conteudo_arq.reset_index()
        lista_cod_frete = df_conteudo_arq['cod_cad_frete_spot'].unique().tolist()
        lista_obj_terc_financ_pago = (Registro2ArtTerceirosFinanceiro
                                      .objects
                                      .filter(cod_cad_frete_spot__in=lista_cod_frete,
                                              status_financeiro_2art_terc_financ='P'))
        msg = ''
        if len(lista_obj_terc_financ_pago) == 0:
            for index, row in df_conteudo_arq.iterrows():
                cod_frete = df_conteudo_arq.loc[index, 'cod_cad_frete_spot']
                obj_frete = CadFreteSpot.objects.get(pk=cod_frete)
                obj_frete.qtd_min = int(df_conteudo_arq.loc[index, 'qtd_min'])
                obj_frete.val_frete_carreteiro_min = float(df_conteudo_arq.loc[index, 'val_frete_carreteiro_min'])
                obj_frete.val_descarga_min = float(df_conteudo_arq.loc[index, 'val_descarga_min'])
                obj_frete.val_pedagio_min = float(df_conteudo_arq.loc[index, 'val_pedagio_min'])
                obj_frete.val_cprb_min = float(df_conteudo_arq.loc[index, 'val_cprb_min'])
                obj_frete.val_lucro_min = float(df_conteudo_arq.loc[index, 'val_lucro_min'])
                obj_frete.qtd_max = int(df_conteudo_arq.loc[index, 'qtd_max'])
                obj_frete.val_frete_carreteiro_max = float(df_conteudo_arq.loc[index, 'val_frete_carreteiro_max'])
                obj_frete.val_descarga_max = float(df_conteudo_arq.loc[index, 'val_descarga_max'])
                obj_frete.val_pedagio_max = float(df_conteudo_arq.loc[index, 'val_pedagio_max'])
                obj_frete.val_cprb_max = float(df_conteudo_arq.loc[index, 'val_cprb_max'])
                obj_frete.val_lucro_max = float(df_conteudo_arq.loc[index, 'val_lucro_max'])
                obj_frete.save()
                msg = 'Fretes atualizados!'
        else:
            msg = 'Atualização abortada. Há fretes informados que possui mapas pagos. Verifique!'

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


