import json
import os
import random

import decimal
import shutil
import traceback

from _decimal import getcontext, Context
from django.db.models import Q, Count
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import locale
import pandas as pd

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Q, Sum, Min, Max
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.contabil_composicao_app.models import Pacote_Conta, Conta, Contrato, Parcela_Contrato, Responsaveis_Conta, \
    Anexos_Contrato, Auditoria_Status_Composicao_Competencia, \
    Layout_Campos_Contas_Modelo_1, Arquivo_Docs_Contas_Modelo_1, Registros_Arqv_Docs_Contas_Modelo_1, \
    Arquivo_Docs_Pac_Contas_Modelo_1, Docs_Pac_Contas_Pagar_Receber_M1, Docs_Pac_Estoque_M1, \
    Docs_Pac_Folha_Pag_M1, Docs_Pac_Contas_Compensacao_M1, Docs_Pac_Tributos_M1, \
    Docs_Pac_Finac_Disponib_M1, Docs_Pac_Intercompany_M1, Docs_Pac_Imobilizado_M1, \
    Docs_Pac_Consorcio_Ativo_M1, Docs_Demais_Contas_M1, Docs_Pac_Contas_Pagar_Receber_M1
from apps.estrut_org_app.models import Empresa, Filial
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR


class Form_Imp_Cad_Conta_View(View):
    def get(self, request):
        # lista_contas_benner = ConexaoBancoBenner().retorna_dados_contas()
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=cod_usuario_sessao)
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_contas = Conta.objects.filter(tipo_modelo=1)
        lista_pacotes_conta = Pacote_Conta.objects.filter(cod_modelo=1)
        lista_usuarios_contabil = (Usuario
                                   .objects
                                   .filter(sala='CON',
                                           cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))
        lista_filiais = Filial.objects.filter(cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                              cod_reduzido__isnull=False)


        # diretorio_arquivos_postados = 'media/docs/contabil_composicao_app/anexos_pendentes_importacao'
        nome_pasta_empresa = ''
        # qtd_arquivos_postados = 0
        if obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa == 17:
            nome_pasta_empresa = 'Deep_Anexos_Pendentes'
            logo_empresa = 'icons/logo-small-deep.png'
            cor_padrao = '#3b8eed'  ##3378ad
        elif obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa == 12:
            nome_pasta_empresa = 'Conlog_Anexos_Pendentes'
            logo_empresa = 'icons/logo-branca.png'
            cor_padrao = '#f46424'
        diretorio_arquivos_postados = os.path.join(BASE_DIR,
                                                   f'media\\docs\\contabil_composicao_app\\anexos_pendentes_importacao\\{nome_pasta_empresa}\\')

        lista_arquivos = os.listdir(diretorio_arquivos_postados)
        qtd_arquivos_postados = 0
        for arq in lista_arquivos:
            if '.pdf' in arq or '.PDF' in arq:
                qtd_arquivos_postados += 1

        # if len(lista_arquivos) > 0:
        #    qtd_arquivos_postados = len(lista_arquivos)

        lista_usuarios_contabil = (Usuario.objects
                                   .filter(sala='CON',
                                           cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))



        contexto = {
            'lista_contas': lista_contas,
            'lista_filiais': lista_filiais,
            'lista_pacotes_conta': lista_pacotes_conta,
            'lista_usuarios_contabil': lista_usuarios_contabil,
            'desc_menu': 'Cadastro de contas composição',
            'qtd_arquivos_postados': qtd_arquivos_postados,
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_usuarios_contabil': lista_usuarios_contabil,
<<<<<<< HEAD
            'obj_usuario_logado': obj_usuario_logado
=======
            'cod_empresa': obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa,
            'logo_empresa': logo_empresa,
            'cor_padrao': cor_padrao,
>>>>>>> 28e0528e8f17883d8ea40a6a642bfd1c6f7199c3

        }
        return render(request, 'contabil_composicao_app/form_cad_contas.html', contexto)

class Form_Imp_Contratos_Conta_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        tipo_pesq_form = request.GET['tipo_pesq']
        num_contrato_form = request.GET['num_contrato']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        dados = self.atualiza_dados_contratos_parcelas(cod_conta_form, num_contrato_form, tipo_pesq_form,
                                                       obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa, obj_usuario_sessao)


        data = dict()
        data = {
            'lista_contratos': dados[0],
            'msg': dados[1]
        }
        return JsonResponse(data, safe=False)


    def atualiza_dados_contratos_parcelas(self, cod_conta_form, num_contrato_form, tipo_pesq_form, cod_empresa,obj_usuario_sessao):
        obj_conta = Conta.objects.get(pk=cod_conta_form)
        handle_conta_cp = obj_conta.handle_conta_contabil_cp
        handle_conta_lp = obj_conta.handle_conta_contabil_lp
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        lista_contratos = []
        lista_parcelas_atualizadas = []
        lista_contratos_benner = ConexaoBancoBenner() \
            .retorna_dados_contratos_conta(tipo_pesq_form, num_contrato_form, handle_conta_cp, handle_conta_lp,
                                           cod_empresa)
        if lista_contratos_benner != None:
            for contrato in lista_contratos_benner:
                obj_empresa = Empresa.objects.filter(cod_empresa=contrato['cod_empresa']).first()
                prox_parc_pendente = 0
                if contrato['proxima_parc_pendente'] != None:
                    #prox_parc_pendente = contrato['proxima_parc_pendente'].split('/')[1]
                    prox_parc_pendente = contrato['proxima_parc_pendente']
                qtd_parcela = 0
                if contrato['qtd_parc'] != None:
                    qtd_parcela = contrato['qtd_parc']
                obj_contrato = Contrato.objects.filter(handle_fn_doc=contrato['handle_fn_doc'],
                                                       cod_empresa__cod_empresa=cod_empresa).first()
                if obj_contrato == None:
                    obj_contrato = Contrato(
                        handle_fn_doc=contrato['handle_fn_doc'],
                        num_contrato=contrato['num_contrato'],
                        data_emissao_contrato=contrato['data_emissao_contrato'],
                        nome_fornecedor=contrato['fornecedor'],
                        handle_operacao=contrato['handle_operacao'],
                        desc_op=contrato['nome_operacao'],
                        num_doc_contabil=contrato['doc_contabil'],
                        val_nominal=contrato['val_nominal'],
                        val_liquido=contrato['val_liquido'],
                        cod_conta=obj_conta,
                        sincronizar_benner='S',
                        dia_util=None,
                        qtd_parcelas=qtd_parcela,
                        cod_empresa=obj_empresa
                    )
                    obj_contrato.save()
                else:
                    obj_contrato.num_contrato = contrato['num_contrato']
                    obj_contrato.data_emissao_contrato = contrato['data_emissao_contrato']
                    obj_contrato.nome_fornecedor = contrato['fornecedor']
                    obj_contrato.handle_operacao = contrato['handle_operacao']
                    obj_contrato.desc_op = contrato['nome_operacao']
                    obj_contrato.num_doc_contabil = contrato['doc_contabil']
                    obj_contrato.val_nominal = contrato['val_nominal']
                    obj_contrato.val_liquido = contrato['val_liquido']
                    # obj_contrato.cod_conta = obj_conta
                    # obj_contrato.sincronizar_benner = 'S'
                    # obj_contrato.dia_util = None
                    obj_contrato.qtd_parcelas = qtd_parcela
                    # obj_contrato.cod_empresa = obj_empresa
                    obj_contrato.save()

                data_emissao = datetime.strptime(contrato['data_emissao_contrato'], "%Y-%m-%d")
                data_emissao_formatada = data_emissao.strftime("%d-%m-%Y")

                data_vencimento_formatada = ''
                if contrato['data_venc_proxima_parc_pendente'] != None:
                    data_vencimento = datetime.strptime(contrato['data_venc_proxima_parc_pendente'], "%Y-%m-%d")
                    data_vencimento_formatada = data_vencimento.strftime("%d-%m-%Y")

                lista_parcelas_contrato_form = []
                lista_parcelas_contrato = ConexaoBancoBenner().retorna_dados_parcelas_contrato(
                    contrato['handle_fn_doc'])
                # lista_contratos_benner.append(lista_parcelas_contrato)
                val_tt_contrato_reajustado = 0
                val_tt_liq_cp = 0
                val_tt_contrato_reajustado_cp = 0
                val_tt_pago_contrato_cp = 0
                val_tt_a_pagar_cp = 0
                val_tt_liq_lp = 0
                val_tt_contrato_reajustado_lp = 0
                val_tt_pago_contrato_lp = 0
                val_tt_a_pagar_lp = 0
                num_parc = 0
                if lista_parcelas_contrato != None:
                    for parcela in lista_parcelas_contrato:
                        val_pago = decimal.Decimal(0.00)
                        if parcela['val_total_pago'] != None:
                            val_pago = decimal.Decimal(parcela['val_total_pago'])

                        tipo_prazo_parc = ''
                        if parcela['data_liquidacao'] != None and val_pago >= decimal.Decimal(parcela['val_principal']):
                            tipo_prazo_parc = 'PG'
                        elif datetime.strptime(parcela['data_vencimento'], '%Y-%m-%d') <= data_hora_atual:
                            tipo_prazo_parc = 'CP'
                        else:
                            num_parc += 1
                            if num_parc <= 12:
                                tipo_prazo_parc = 'CP'
                            else:
                                tipo_prazo_parc = 'LP'

                        val_taxas = 0.00
                        if parcela['val_taxas'] != None:
                            val_taxas = parcela['val_taxas']

                        val_fundo = 0.00
                        if parcela['val_fundo'] != None:
                            val_fundo = parcela['val_fundo']

                        val_corrigido = decimal.Decimal(0.00)
                        if parcela['valor_corrigido'] != None:
                            val_corrigido = decimal.Decimal(parcela['valor_corrigido'])



                        obj_parcela = Parcela_Contrato.objects.filter(handle_parcela=parcela['handle_parc']).first()
                        if obj_parcela == None:
                            val_corrigido = decimal.Decimal(0.00)
                            if parcela['valor_corrigido'] != None:
                                val_corrigido = decimal.Decimal(parcela['valor_corrigido'])

                            val_pago = decimal.Decimal(0.00)
                            if parcela['val_total_pago'] != None:
                                val_pago = decimal.Decimal(parcela['val_total_pago'])

                            obj_parcela = Parcela_Contrato(
                                handle_parcela=parcela['handle_parc'],
                                ap_parcela=parcela['ap_parcela'],
                                ordem_parcela=parcela['ordem_parcela'],
                                val_conta=decimal.Decimal(parcela['valor_conta']),
                                val_corrigido=val_corrigido,
                                val_principal=decimal.Decimal(parcela['val_principal']),
                                val_fundo=decimal.Decimal(val_fundo),
                                val_taxas=decimal.Decimal(val_taxas),
                                natureza=parcela['natureza'],
                                data_vencimento=parcela['data_vencimento'],
                                tipo_prazo=tipo_prazo_parc,
                                data_liquidacao=parcela['data_liquidacao'],
                                val_pago=val_pago,
                                cod_contrato=obj_contrato,
                                cod_usu=obj_usuario_sessao,
                                data_ultima_atualizacao=data_atual_dd_mm_yyyy,
                                val_desc_taxas = 0,
                                val_acres_taxas=0,
                                val_desc_principal = 0,
                                val_acres_principal=0
                            )
                            obj_parcela.save()
                        elif obj_contrato.sincronizar_benner == 'S' and (
                                obj_parcela.data_liquidacao == None or obj_parcela.data_liquidacao == ''):
                            # obj_parcela.ap_parcela = parcela['ap_parcela']
                            # obj_parcela.ordem_parcela = parcela['ordem_parcela']
                            obj_parcela.val_conta = decimal.Decimal(parcela['valor_conta'])
                            obj_parcela.val_corrigido = val_corrigido
                            obj_parcela.val_principal = decimal.Decimal(parcela['val_principal'])
                            obj_parcela.val_taxas = decimal.Decimal(val_taxas)
                            obj_parcela.val_fundo = decimal.Decimal(val_fundo)
                            obj_parcela.natureza = parcela['natureza']
                            obj_parcela.data_vencimento = parcela['data_vencimento']
                            obj_parcela.tipo_prazo = tipo_prazo_parc
                            obj_parcela.data_liquidacao = parcela['data_liquidacao']
                            obj_parcela.val_pago = val_pago
                            obj_parcela.data_ultima_atualizacao = data_atual_dd_mm_yyyy
                            obj_parcela.val_desc_taxas = 0
                            obj_parcela.val_acres_taxas = 0
                            obj_parcela.val_desc_principal = 0
                            obj_parcela.val_acres_principal = 0
                            # obj_parcela.cod_contrato = obj_contrato
                            obj_parcela.save()

                            lista_parcelas_atualizadas.append(obj_parcela)
                        val_principal_parc = 0
                        if parcela['val_principal'] != None:
                            val_principal_parc = parcela['val_principal']

                        val_pago_parc = 0
                        if parcela['val_total_pago'] != None:
                            val_pago_parc = parcela['val_total_pago']

                        val_tt_contrato_reajustado += (val_principal_parc + val_taxas)

                        if obj_parcela.tipo_prazo == 'CP':
                            val_tt_liq_cp += parcela['valor_conta']
                            val_tt_contrato_reajustado_cp += (val_principal_parc + val_taxas)
                            val_tt_pago_contrato_cp += val_pago_parc
                            if val_pago_parc == 0:
                                val_tt_a_pagar_cp += (val_principal_parc + val_taxas)

                        if obj_parcela.tipo_prazo == 'LP':
                            val_tt_liq_lp += parcela['valor_conta']
                            val_tt_contrato_reajustado_lp += (val_principal_parc + val_taxas)
                            val_tt_pago_contrato_lp += val_pago_parc
                            if val_pago_parc == 0:
                                val_tt_a_pagar_lp += (val_principal_parc + val_taxas)

                        data_vencimento_formatada = ''
                        if parcela['data_vencimento'] != None:
                            data_vencimento = datetime.strptime(parcela['data_vencimento'], "%Y-%m-%d")
                            data_vencimento_formatada = data_vencimento.strftime("%d-%m-%Y")

                        data_liquidacao_formatada = ''
                        valor_corrigido = 0.00
                        val_total_pago = 0.00
                        if parcela['data_liquidacao'] != None:
                            data_liquidacao = datetime.strptime(parcela['data_liquidacao'], "%Y-%m-%d")
                            data_liquidacao_formatada = data_liquidacao.strftime("%Y-%m-%d")
                            # data_liquidacao_formatada = parcela['data_liquidacao']

                        if parcela['valor_corrigido'] != None:
                            valor_corrigido = locale.currency(parcela['valor_corrigido'], grouping=True, symbol=None)
                        if parcela['val_total_pago'] != None:
                            val_total_pago = locale.currency(parcela['val_total_pago'], grouping=True, symbol=None)

                        val_taxa_parcela = decimal.Decimal(0.00)
                        if obj_parcela.val_taxas != None:
                            val_taxa_parcela = obj_parcela.val_taxas

                        val_fundo_parcela = decimal.Decimal(0.00)
                        if obj_parcela.val_fundo != None:
                            val_fundo_parcela = obj_parcela.val_fundo

                        parcela_form = {
                            'handle_fn_doc': obj_contrato.handle_fn_doc,
                            'handle_parc': obj_parcela.handle_parcela,
                            'ap_parcela': obj_parcela.ap_parcela,
                            'ordem_parcela': obj_parcela.ordem_parcela,
                            'valor_conta': locale.currency(obj_parcela.val_conta, grouping=True, symbol=None),
                            'valor_corrigido': valor_corrigido,
                            'valor_principal': locale.currency(obj_parcela.val_principal, grouping=True, symbol=None),
                            'valor_fundo': locale.currency(val_fundo_parcela, grouping=True, symbol=None),
                            'valor_taxas': locale.currency(obj_parcela.val_taxas, grouping=True, symbol=None),
                            'valor_total': locale.currency(
                                obj_parcela.val_principal + val_taxa_parcela + val_fundo_parcela, grouping=True,
                                symbol=None),
                            'natureza': obj_parcela.natureza,
                            'data_vencimento': data_vencimento_formatada,
                            'tipo_prazo': obj_parcela.tipo_prazo,
                            'data_liquidacao': data_liquidacao_formatada,
                            'val_total_pago': val_total_pago,
                            'data_ultima_atualizacao': parcela['data_ultima_atualizacao'],
                            'val_desc_taxas': parcela['val_desc_taxas'],
                            'val_acres_taxas': parcela['val_acres_taxas'],
                            'val_desc_principal': parcela['val_desc_principal'],
                            'val_acres_principal': parcela['val_acres_principal']
                        }
                        lista_parcelas_contrato_form.append(parcela_form)

                val_proxima_parc_pendente = 0
                if contrato['val_proxima_parc_pendente'] != None:
                    val_proxima_parc_pendente = contrato['val_proxima_parc_pendente']

                data_venc_proxima_parc_pendente = None
                if contrato['data_venc_proxima_parc_pendente'] != None:
                    data_venc_proxima_parc = datetime.strptime(contrato['data_venc_proxima_parc_pendente'], "%Y-%m-%d")
                    data_venc_proxima_parc_pendente = data_venc_proxima_parc.strftime("%d-%m-%Y")

                '''Configura os campos retornador como Null'''
                val_nominal_var = 0.00
                if contrato['val_nominal'] != None:
                    val_nominal_var = locale.currency(contrato['val_nominal'], grouping=True, symbol=None)

                val_liquido_var = 0.00
                if contrato['val_liquido'] != None:
                    val_liquido_var = locale.currency(contrato['val_liquido'], grouping=True, symbol=None)

                total_pago_var = 0.00
                if contrato['total_pago'] != None:
                    total_pago_var = locale.currency(contrato['total_pago'], grouping=True, symbol=None)


                atualiza_benner = 'SIM'
                if obj_contrato.sincronizar_benner == 'N':
                    atualiza_benner = 'NÃO'

                contrato_form = {
                    'cod_contrato': obj_contrato.cod_contrato,
                    'handle_fn_doc': contrato['handle_fn_doc'],
                    'num_contrato': contrato['num_contrato'],
                    'atualiza_benner': atualiza_benner,
                    'data_emissao_contrato': data_emissao_formatada,
                    'val_nominal': val_nominal_var,
                    'val_liquido': val_liquido_var,
                    'fornecedor': contrato['fornecedor'],
                    'handle_operacao': contrato['handle_operacao'],
                    'nome_operacao': contrato['nome_operacao'],
                    'doc_contabil': contrato['doc_contabil'],
                    'cod_empresa': contrato['cod_empresa'],
                    'proxima_parc_pendente': contrato['proxima_parc_pendente'],
                    'data_venc_proxima_parc_pendente': data_venc_proxima_parc_pendente,
                    'val_proxima_parc_pendente': locale.currency(val_proxima_parc_pendente, grouping=True,
                                                                 symbol=None),
                    'total_pago': total_pago_var,
                    'nome_empresa': obj_empresa.desc_empresa,
                    'val_tt_contrato_reajustado': locale.currency(val_tt_contrato_reajustado, grouping=True,
                                                                  symbol=None),
                    'val_tt_liq_cp': locale.currency(val_tt_liq_cp, grouping=True,
                                                     symbol=None),
                    'val_tt_contrato_reajustado_cp': locale.currency(val_tt_contrato_reajustado_cp, grouping=True,
                                                                     symbol=None),
                    'val_tt_pago_contrato_cp': locale.currency(val_tt_pago_contrato_cp, grouping=True,
                                                               symbol=None),
                    'val_tt_a_pagar_cp': locale.currency(val_tt_a_pagar_cp, grouping=True,
                                                         symbol=None),
                    'val_tt_liq_lp': locale.currency(val_tt_liq_lp, grouping=True,
                                                     symbol=None),
                    'val_tt_contrato_reajustado_lp': locale.currency(val_tt_contrato_reajustado_lp, grouping=True,
                                                                     symbol=None),
                    'val_tt_pago_contrato_lp': locale.currency(val_tt_pago_contrato_lp, grouping=True,
                                                               symbol=None),
                    'val_tt_a_pagar_lp': locale.currency(val_tt_a_pagar_lp, grouping=True,
                                                         symbol=None)
                }
                dic_contrato_parcelas = {
                    'contrato': contrato_form,
                    'lista_parcelas_contrato': lista_parcelas_contrato_form
                }
                lista_contratos.append(dic_contrato_parcelas)


        msg = 'Processo finalizado'

        return lista_contratos, msg, lista_parcelas_atualizadas

class Form_Cad_Conta_View(View):
    def get(self, request):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        tipo_return_form = request.GET['tipo_return']
        obj_conta_pesq = Conta.objects.get(pk=cod_conta_form)

        empresas_usam_conta = (Responsaveis_Conta
                               .objects
                               .filter(cod_conta=obj_conta_pesq).values('cod_empresa__cod_empresa')
                               .distinct())
        conlog_usa = 'N'
        deep_usa = 'N'
        for emp in empresas_usam_conta:
            if emp['cod_empresa__cod_empresa'] == 12:
                conlog_usa = 'S'
            elif emp['cod_empresa__cod_empresa'] == 17:
                deep_usa = 'S'
        data_ini_atv = None
        if obj_conta_pesq.data_ini_atividade != None:
            data_ini_atv = datetime.strftime(obj_conta_pesq.data_ini_atividade, '%Y-%m-%d')
        data_fim_atv = None
        if obj_conta_pesq.data_fim_atividade != None:
            data_fim_atv = datetime.strftime(obj_conta_pesq.data_fim_atividade, '%Y-%m-%d')
        nome_pacote = None
        if obj_conta_pesq.cod_pacote_conta != None:
            nome_pacote = obj_conta_pesq.cod_pacote_conta.cod_pacote_conta
        dic_conta = {
            'cod_conta': obj_conta_pesq.cod_conta,
            'desc_conta': obj_conta_pesq.desc_conta,
            'handle_benner_cp': obj_conta_pesq.handle_conta_contabil_cp,
            'cod_red_benner_cp': obj_conta_pesq.cod_red_conta_contabil_cp,
            'cod_estrut_cp': obj_conta_pesq.cod_estrut_cp,
            'handle_benner_lp': obj_conta_pesq.handle_conta_contabil_lp,
            'cod_red_benner_lp': obj_conta_pesq.cod_red_conta_contabil_lp,
            'cod_estrut_lp': obj_conta_pesq.cod_estrut_lp,
            'tipo_modelo': obj_conta_pesq.tipo_modelo,
            'data_ini_atividade': data_ini_atv,
            'data_fim_atividade': data_fim_atv,
            'status_comp': obj_conta_pesq.status_comp,
            'cod_pacote_conta': nome_pacote,
            'conlog_usa': conlog_usa,
            'deep_usa': deep_usa
        }


        lista_pacotes = list(Pacote_Conta.objects
                             .filter(cod_modelo=cod_modelo_conta_selecionado)
                             .values('cod_pacote_conta', 'desc_pacote_conta'))

        data = dict()
        if tipo_return_form == 'J':
            data = {
                'dic_conta': dic_conta,
                'lista_pacotes': lista_pacotes,
                'usu_iscorporativo': obj_usu.corporativo
            }
            return JsonResponse(data, safe=False)
        else:
            return redirect('acessa_form_cadastros_comp')



    def post(self, request):
        transacao_form = request.POST['transacao']
        desc_conta_form = request.POST['desc_conta']
        handle_cp_form = request.POST['handle_cp']
        cod_red_cp_form = request.POST['cod_red_cp']
        str_cp_form = request.POST['str_cp']
        handle_lp_form = request.POST['handle_lp']
        cod_red_lp_form = request.POST['cod_red_lp']
        str_lp_form = request.POST['str_lp']
        cod_pac_conta_form = request.POST['cod_pac_conta']
        cod_modelo_form = request.POST['cod_modelo']
        ini_atv_form = request.POST['ini_atv']
        fim_atv_form = request.POST['fim_atv']
        status_conta_comp_form = request.POST['status_conta_comp']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        obj_pacote_conta = None
        if cod_pac_conta_form != '':
            obj_pacote_conta = Pacote_Conta.objects.get(pk=cod_pac_conta_form)

        data_ini_atv = None
        if ini_atv_form != '':
            data_ini_atv = ini_atv_form

        data_fim_atv = None
        if fim_atv_form != '':
            data_fim_atv = fim_atv_form

        msg = ''
        if transacao_form == 'U':
            cod_conta_form = request.POST['cod_conta']
            obj_conta = Conta.objects.get(pk=cod_conta_form)
            obj_conta.desc_conta = desc_conta_form

            obj_conta.handle_conta_contabil_cp = handle_cp_form
            obj_conta.cod_red_conta_contabil_cp = cod_red_cp_form
            obj_conta.cod_estrut_cp = str_cp_form

            obj_conta.handle_conta_contabil_lp = handle_lp_form
            obj_conta.cod_red_conta_contabil_lp = cod_red_lp_form
            obj_conta.cod_estrut_lp = str_lp_form

            obj_conta.tipo_modelo = cod_modelo_form
            obj_conta.data_ini_atividade = data_ini_atv
            obj_conta.data_fim_atividade = data_fim_atv
            obj_conta.status_comp = status_conta_comp_form


            obj_conta.cod_empresa = obj_usuario_sessao.cod_filial.cod_empresa
            obj_conta.cod_pacote_conta = obj_pacote_conta
            obj_conta.save()
            msg = 'Dados da conta atualizados com sucesso!'
        elif transacao_form == 'N':
            obj_conta = Conta(
                desc_conta = desc_conta_form,
                handle_conta_contabil_cp = handle_cp_form,
                cod_red_conta_contabil_cp = cod_red_cp_form,
                cod_estrut_cp = str_cp_form,
                handle_conta_contabil_lp = handle_lp_form,
                cod_red_conta_contabil_lp = cod_red_lp_form,
                cod_estrut_lp = str_lp_form,
                tipo_modelo = cod_modelo_form,
                data_ini_atividade = data_ini_atv,
                data_fim_atividade = data_fim_atv,
                status_comp = status_conta_comp_form,
                cod_pacote_conta = obj_pacote_conta
            )
            obj_conta.save()
            msg = 'Cadastro realizado com sucesso!'

        lista_contas = list(Conta.objects.filter(tipo_modelo = cod_modelo_form, status_comp='A').values('cod_conta', 'desc_conta', 'tipo_modelo'))

        data = dict()
        data = {
            'cod_conta': obj_conta.cod_conta,
            'lista_contas': lista_contas,
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Form_Cad_Contrato_View(View):
    def get_object(self, pk):
        try:
            return Contrato.objects.get(pk=pk)
        except Contrato.DoesNotExists:
            return Http404

    def post(self, request):
        transacao_form = request.POST['transacao']
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        msg = ''
        data = dict()
        if transacao_form == 'cadastro':
            cod_conta_form = request.POST['cod_conta']
            num_contrato_form = request.POST['num_contrato']
            nome_fornecedor_form = request.POST['nome_fornecedor']
            data_emissao_form = request.POST['data_emissao']
            handle_contrato_form = request.POST['handle_contrato']
            doc_contabil_form = request.POST['doc_contabil']
            val_nominal_form = request.POST['val_nominal']
            val_liquido_form = request.POST['val_liquido']
            dia_util_form = request.POST['dia_util']
            qtd_parcelas_form = request.POST['qtd_parcelas']
            data_primeira_parcela_form = request.POST['data_primeira_parcela']
            handle_operacao_form = request.POST['handle_operacao']
            desc_operacao_form = request.POST['desc_operacao']
            check_atualiza_benner_form = request.POST['check_atualiza_benner']

            handle_fn_doc = 0
            if handle_contrato_form != '':
                handle_fn_doc = handle_contrato_form

            handle_operacao = 0
            if handle_operacao_form != '':
                handle_operacao = handle_operacao_form



            obj_conta = Conta.objects.get(pk=cod_conta_form)
            obj_contrato = Contrato(
                handle_fn_doc = handle_fn_doc,
                num_contrato = num_contrato_form,
                data_emissao_contrato = data_emissao_form,
                nome_fornecedor = nome_fornecedor_form,
                handle_operacao = handle_operacao,
                desc_op = desc_operacao_form,
                num_doc_contabil = doc_contabil_form,
                val_nominal = val_nominal_form.replace('.', '').replace(',','.'),
                val_liquido = val_liquido_form.replace('.', '').replace(',','.'),
                sincronizar_benner = check_atualiza_benner_form,
                dia_util = dia_util_form,
                data_primeira_parcela= data_primeira_parcela_form,
                qtd_parcelas = qtd_parcelas_form,
                cod_conta = obj_conta,
                cod_empresa = obj_usuario_sessao.cod_filial.cod_empresa
            )
            obj_contrato.save()
            '''Gera parcelas'''
            valor_parcela = float(val_liquido_form.replace('.', '').replace(',','.')) / int(qtd_parcelas_form)
            data_ini = datetime(int(data_primeira_parcela_form.split('-')[0]), int(data_primeira_parcela_form.split('-')[1]),
                                int(data_primeira_parcela_form.split('-')[2]))
            num_parc = 0
            for parc in range(int(qtd_parcelas_form)):
                primeiro_dia_mes = None
                if int(dia_util_form) in (29, 30, 31):
                    ultimo_dia_mes = calendar.monthrange(int(data_ini.year), int(data_ini.month))[1]
                    primeiro_dia_mes = data_ini.replace(day=int(ultimo_dia_mes))
                else:
                    primeiro_dia_mes = data_ini.replace(day=int(dia_util_form))


                handle_parc_random = ''.join(str(random.randint(1,9))  for _ in range(6))
                num_parc += 1
                tipo_prazo = ''
                if num_parc <= 12:
                    tipo_prazo = 'CP'
                else:
                    tipo_prazo = 'LP'
                '''tipo_prazo = 'CP'
                if parc > int(qtd_parcelas_form) / 2:
                    tipo_prazo = 'LP'''

                obj_parcela = Parcela_Contrato(
                    handle_parcela = handle_parc_random, #parc + 1,
                    ap_parcela = handle_parc_random, #parc + 1,
                    ordem_parcela = str(parc + 1) + '/' + str(qtd_parcelas_form),
                    val_conta = valor_parcela,
                    val_corrigido = None,
                    val_principal = valor_parcela,
                    val_fundo = 0,
                    val_taxas = None,
                    natureza = None,
                    data_vencimento = primeiro_dia_mes,
                    tipo_prazo = tipo_prazo,
                    data_liquidacao = None,
                    val_pago = None,
                    cod_contrato = obj_contrato
                )
                obj_parcela.save()

                # Avança para o próximo mês
                if data_ini.month == 12:
                    data_ini = data_ini.replace(year=data_ini.year + 1, month=1)
                else:
                    if int(dia_util_form) in (29, 30, 31):
                        ultimo_dia_mes = calendar.monthrange(int(data_ini.year), int(data_ini.month + 1))[1]
                        data_ini = data_ini.replace(day=ultimo_dia_mes,month=data_ini.month + 1)
                    else:
                        data_ini = data_ini.replace(month=data_ini.month + 1)

            msg = 'Contrato associado com sucesso. Parcelas criadas com sucesso !!!'
            data = {
                'msg': msg
            }

        elif transacao_form == 'status_sincronia_benner':
            handle_contrato_form = request.POST['handle_contrato']
            status_sincronia_contrato_benner_form = request.POST['status_sincronia_contrato_benner']

            obj_contrato = Contrato.objects.get(pk=handle_contrato_form)
            obj_contrato.sincronizar_benner = status_sincronia_contrato_benner_form
            obj_contrato.save()

            lista_contas_para_atualizar_benner = list(Contrato.objects
                                                     .filter(cod_conta__tipo_modelo=obj_contrato.cod_conta.tipo_modelo,
                                                             cod_conta__status_comp='A',
                                                             sincronizar_benner='S',
                                                             cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                     .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                                             'cod_conta__cod_red_conta_contabil_cp',
                                                             'cod_conta__cod_red_conta_contabil_lp')
                                                     .distinct())
            msg = 'Status alterado com sucesso !'
            data = {
                'msg': msg,
                'lista_contas_para_atualizar_benner' : lista_contas_para_atualizar_benner
            }



        return JsonResponse(data, safe=False)

    def get(self, request):
        tipo_transacao_frm = request.GET['tipo_transacao']
        if tipo_transacao_frm == 'cadastro':
            return render(request, 'contabil_composicao_app/form_cad_contratos.html')
        elif tipo_transacao_frm == 'retornar_dados_cadastro':
            locale.setlocale(locale.LC_MONETARY, 'pt-BR')
            cod_conta_form = request.GET['cod_conta']
            num_contrato_frm = request.GET['num_contrato']
            obj_conta_pesq = Conta.objects.get(pk=cod_conta_form)

            cod_usuario_sessao = request.session['cod_usuario_logado']
            obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

            lista_contratos = []
            lista_contratos_banco = Contrato.objects.filter(cod_conta=obj_conta_pesq,
                                                            cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
            dic_contrato = None
            lista_parcelas_contrato = None
            for contrato in lista_contratos_banco:
                lista_parcelas_contrato = []
                lista_parcelas = Parcela_Contrato.objects.filter(cod_contrato=contrato).order_by('cod_parcela_contrato')
                val_total_pago = 0

                val_tt_contrato_reajustado = 0
                val_tt_liq_cp = 0
                val_tt_contrato_reajustado_cp = 0
                val_tt_liq_lp = 0
                val_tt_contrato_reajustado_lp = 0
                dic_val_total_ctr_principal = lista_parcelas.aggregate(val_total_principal=Sum('val_principal'))
                val_total_ctr_principal = 0
                if dic_val_total_ctr_principal['val_total_principal'] != None:
                    val_total_ctr_principal = dic_val_total_ctr_principal['val_total_principal']
                dic_val_total_ctr_taxas = lista_parcelas.aggregate(val_total_taxas=Sum('val_taxas'))

                val_total_ctr_taxas = 0
                if dic_val_total_ctr_taxas['val_total_taxas'] != None:
                    val_total_ctr_taxas = dic_val_total_ctr_taxas['val_total_taxas']

                dic_val_total_ctr_fundo = lista_parcelas.aggregate(val_total_fundo=Sum('val_fundo'))
                val_total_ctr_fundo = 0
                if dic_val_total_ctr_fundo['val_total_fundo'] != None:
                    val_total_ctr_fundo = dic_val_total_ctr_fundo['val_total_fundo']

                val_tt_contrato_reajustado = val_total_ctr_principal + val_total_ctr_taxas
                val_balancete = val_tt_contrato_reajustado
                if lista_parcelas != None:
                    for parc in lista_parcelas:
                        val_principal_parc = 0
                        if parc.val_principal != None:
                            val_principal_parc = parc.val_principal
                        val_fundo_parc = 0
                        if parc.val_fundo != None:
                            val_fundo_parc = parc.val_fundo
                        val_taxas_parc = 0
                        if parc.val_taxas != None:
                            val_taxas_parc = parc.val_taxas
                        val_pago_parc = 0
                        if parc.val_pago != None:
                            val_pago_parc = parc.val_pago

                        #val_tt_contrato_reajustado += (val_principal_parc + val_taxas_parc)

                        if parc.tipo_prazo == 'CP':
                            val_tt_liq_cp += parc.val_principal
                            val_tt_contrato_reajustado_cp += (val_principal_parc + val_taxas_parc + val_fundo_parc)

                        if parc.tipo_prazo == 'LP':
                            val_tt_liq_lp += parc.val_principal
                            val_tt_contrato_reajustado_lp += (val_principal_parc + val_taxas_parc + val_fundo_parc)

                        val_corrigido = 0
                        if parc.val_corrigido != None:
                            val_corrigido = parc.val_corrigido

                        data_liquidacao = ''
                        if parc.data_liquidacao != None:
                            data_liquidacao = datetime.strftime(parc.data_liquidacao, '%Y-%m-%d')
                            val_total_pago += parc.val_pago

                        val_principal = 0
                        if parc.val_principal != None:
                            val_principal = parc.val_principal

                        val_taxas = 0
                        if parc.val_taxas != None:
                            val_taxas = parc.val_taxas

                        val_fundo = 0
                        if parc.val_fundo != None:
                            val_fundo = parc.val_fundo

                        val_tt_parc = val_principal + val_taxas + val_fundo
                        #val_balancete = val_balancete - val_corrigido
                        val_balancete = val_balancete - (val_principal_parc + val_taxas_parc)
                        parcela = {
                            'handle_fn_doc': parc.cod_contrato.handle_fn_doc,
                            'handle_parc': parc.handle_parcela,
                            'ap_parcela': parc.ap_parcela,
                            'ordem_parcela': parc.ordem_parcela.split('/')[0],
                            'valor_conta': locale.currency(parc.val_conta, grouping=True, symbol=None),
                            'valor_corrigido': val_corrigido,
                            'valor_principal': locale.currency(val_principal_parc, grouping=True, symbol=None),
                            'valor_taxas': locale.currency(val_taxas_parc, grouping=True, symbol=None),
                            'valor_fundo': locale.currency(val_fundo, grouping=True, symbol=None),
                            'valor_total': locale.currency(val_tt_parc, grouping=True, symbol=None),
                            'natureza': parc.natureza,
                            'data_vencimento': datetime.strftime(parc.data_vencimento, '%d-%m-%Y'),
                            'tipo_prazo': parc.tipo_prazo,
                            'data_liquidacao': data_liquidacao,
                            'val_total_pago': locale.currency(val_pago_parc, grouping=True, symbol=None),
                            'val_balancete': locale.currency(val_balancete, grouping=True, symbol=None),
                            'obs_parcela': parc.obs_parcela
                        }
                        lista_parcelas_contrato.append(parcela)

                proxima_parc_pendente = ''
                data_venc_proxima_parc_pendente = ''
                val_proxima_parc_pendente = ''
                proxima_parcela_pagar = Parcela_Contrato.objects \
                    .filter(cod_contrato=contrato, data_liquidacao__isnull=True) \
                    .order_by('cod_parcela_contrato') \
                    .first()
                if proxima_parcela_pagar != None:
                    proxima_parc_pendente = proxima_parcela_pagar.ordem_parcela
                    data_venc_proxima_parc_pendente = datetime.strftime(proxima_parcela_pagar.data_vencimento, '%d-%m-%Y')
                    val_proxima_parc_pendente = locale.currency(proxima_parcela_pagar.val_principal, grouping=True, symbol=None)

                atualiza_benner = 'SIM'
                if contrato.sincronizar_benner == 'N':
                    atualiza_benner = 'NÃO'

                dic_contrato = {
                    'cod_contrato': contrato.cod_contrato,
                    'handle_fn_doc': contrato.handle_fn_doc,
                    'num_contrato': contrato.num_contrato,
                    'atualiza_benner' : atualiza_benner,
                    'data_emissao_contrato': datetime.strftime(contrato.data_emissao_contrato, '%d-%m-%Y'),
                    'val_nominal': locale.currency(contrato.val_nominal, grouping=True, symbol=None),
                    'val_liquido': locale.currency(contrato.val_liquido, grouping=True, symbol=None),
                    'fornecedor': contrato.nome_fornecedor,
                    'handle_operacao': contrato.handle_operacao,
                    'nome_operacao': contrato.desc_op,
                    'doc_contabil': contrato.num_doc_contabil,
                    'proxima_parc_pendente': proxima_parc_pendente,
                    'data_venc_proxima_parc_pendente': data_venc_proxima_parc_pendente,
                    'val_proxima_parc_pendente': val_proxima_parc_pendente,
                    'total_pago': locale.currency(val_total_pago, grouping=True, symbol=None),
                    'cod_empresa': contrato.cod_empresa.cod_empresa,
                    'nome_empresa': contrato.cod_empresa.desc_empresa,
                    'val_tt_contrato_reajustado': locale.currency(val_tt_contrato_reajustado, grouping=True,
                                                                  symbol=None),
                    'val_tt_liq_cp': locale.currency(val_tt_liq_cp, grouping=True,
                                                     symbol=None),
                    'val_tt_contrato_reajustado_cp': locale.currency(val_tt_contrato_reajustado_cp, grouping=True,
                                                                     symbol=None),
                    'val_tt_liq_lp': locale.currency(val_tt_liq_lp, grouping=True,
                                                     symbol=None),
                    'val_tt_contrato_reajustado_lp': locale.currency(val_tt_contrato_reajustado_lp, grouping=True,
                                                                     symbol=None),
                    'lista_parcelas_contrato': lista_parcelas_contrato
                }
                lista_contratos.append(dic_contrato)

            lista_contratos_filtrados = []
            if num_contrato_frm == 'todos':
                lista_contratos_filtrados = lista_contratos
            else:
                for contrato in lista_contratos:
                    if contrato['num_contrato'] == num_contrato_frm:
                        lista_contratos_filtrados.append(contrato)

            #data = dict()
            data = {
                'lista_contratos': lista_contratos_filtrados, # lista_contratos,
                'obj_usuario_sessao': obj_usuario_sessao
            }
            #return JsonResponse(data, safe=False)
            return render(request, 'contabil_composicao_app/frm_lista_contratos.html', data)

    def delete(self, request, pk):
        obj_contrato = self.get_object(pk)
        cod_conta = obj_contrato.cod_conta.cod_conta
        lista_parcelas_contrato = Parcela_Contrato.objects.filter(cod_contrato=obj_contrato)
        if len(lista_parcelas_contrato) > 0:
            for parc in lista_parcelas_contrato:
                parc.delete()
        lista_anexos_contrato = Anexos_Contrato.objects.filter(cod_contrato=obj_contrato)
        if len(lista_anexos_contrato) > 0:
            for anexo in lista_anexos_contrato:
                anexo.delete()
        lista_auditoria = Auditoria_Status_Composicao_Competencia.objects.filter(cod_contrato=obj_contrato)
        if len(lista_auditoria) > 0:
            for auditoria in lista_auditoria:
                auditoria.delete()
        obj_contrato.delete()
        data = {
            'cod_conta': cod_conta,
            'msg': 'Contrato excluído com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Form_Associa_Resp_Conta_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_dic_resp_conta = []
        lista_responsaveis_conta = Responsaveis_Conta.objects.filter(cod_conta=cod_conta_form,
                                                                     cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
        for resp in lista_responsaveis_conta:
            data_ini_atv = ''
            if resp.data_ini_atividade != None:
                data_ini_atv = datetime.strftime(resp.data_ini_atividade, '%d-%m-%Y')
            data_fim_atv = ''
            if resp.data_fim_atividade != None:
                data_fim_atv = datetime.strftime(resp.data_fim_atividade, '%d-%m-%Y')
            reg = {
                'cod_resp_conta': resp.cod_resp_conta,
                'resp_composicao': resp.resp_composicao,
                'resp_validacao': resp.resp_validacao,
                'data_ini_atividade': data_ini_atv,
                'data_fim_atividade': data_fim_atv,
                'nome_empresa': resp.cod_empresa.desc_empresa
            }
            lista_dic_resp_conta.append(reg)

        data = dict()
        data = {
            'lista_dic_resp_conta': lista_dic_resp_conta
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        tipo_transacao_form = request.POST['tipo_transacao']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        msg = ''
        cod_conta = 0
        if tipo_transacao_form == 'C':
            cod_conta_form = request.POST['cod_conta']
            resp_com_form = request.POST['resp_com']
            resp_val_form = request.POST['resp_val']
            data_ini_form = request.POST['data_ini']
            data_fim_form = request.POST['data_fim']


            obj_conta = Conta.objects.get(pk=cod_conta_form)
            data_ini_atv = None
            if data_ini_form != '':
                data_ini_atv = data_ini_form

            data_fim_atv = None
            if data_fim_form != '':
                data_fim_atv = data_fim_form

            obj_resp_conta = Responsaveis_Conta(
                resp_composicao= resp_com_form,
                resp_validacao= resp_val_form,
                data_ini_atividade = data_ini_atv,
                data_fim_atividade = data_fim_atv,
                cod_empresa = obj_usuario_sessao.cod_filial.cod_empresa,
                cod_conta = obj_conta
            )
            obj_resp_conta.save()
            cod_conta  =obj_conta.cod_conta
            msg = 'Responsaveis associados com sucesso!'
        elif tipo_transacao_form == 'U':
            cod_resp_conta_form = request.POST['cod_resp_conta']
            resp_com_form = request.POST['resp_com']
            resp_val_form = request.POST['resp_val']
            data_ini_form = request.POST['data_ini']
            data_fim_form = request.POST['data_fim']

            data_ini_atv = None
            if data_ini_form != '':
                data_ini_atv = data_ini_form

            data_fim_atv = None
            if data_fim_form != '':
                data_fim_atv = data_fim_form

            obj_resp_conta = Responsaveis_Conta.objects.get(pk=cod_resp_conta_form)
            obj_resp_conta.resp_composicao = resp_com_form
            obj_resp_conta.resp_validacao = resp_val_form
            obj_resp_conta.data_ini_atividade = data_ini_atv
            obj_resp_conta.data_fim_atividade = data_fim_atv
            obj_resp_conta.cod_empresa = obj_usuario_sessao.cod_filial.cod_empresa
            obj_resp_conta.save()


            cod_conta = obj_resp_conta.cod_conta.cod_conta
            msg = 'Dados atualizados com sucesso!'
        elif tipo_transacao_form == 'L':
            lista_cod_contas_frm = request.POST['lista_cod_contas']
            nome_resp_comp_frm = request.POST['nome_resp_comp']
            nome_resp_val_frm = request.POST['nome_resp_val']
            ini_atv_frm = request.POST['ini_atv']
            fim_atv_frm = request.POST['fim_atv']

            for cod_conta in lista_cod_contas_frm.split(','):
                obj_conta = Conta.objects.get(pk=cod_conta)
                data_ini_atv = None
                if ini_atv_frm != '':
                    data_ini_atv = ini_atv_frm

                data_fim_atv = None
                if fim_atv_frm != '':
                    data_fim_atv = fim_atv_frm

                obj_resp_conta = Responsaveis_Conta(
                    resp_composicao=nome_resp_comp_frm,
                    resp_validacao=nome_resp_val_frm,
                    data_ini_atividade=data_ini_atv,
                    data_fim_atividade=data_fim_atv,
                    cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                    cod_conta=obj_conta
                )
                obj_resp_conta.save()
            msg = 'Responsaveis associados com sucesso!'

        data = dict()
        data = {
            'msg': msg,
            'cod_conta': cod_conta
        }
        return JsonResponse(data, safe=False)

class Form_Cad_Parcelas_Contrato_View(View):
    def get_object(self, pk):
        try:
            return Parcela_Contrato.objects.filter(handle_parcela=pk).first()
        except Parcela_Contrato.DoesNotExists:
            return Http404
    def post(self, request):
        transacao_form = request.POST['transacao']
        handle_parcela_form = request.POST['handle_parcela']
        obj_parcela = Parcela_Contrato.objects.filter(handle_parcela=handle_parcela_form).first()
        msg = ''
        if transacao_form == 'pagamento':
            data_pag_form = request.POST['data_pag']
            val_pag_form = request.POST['val_pag']

            if data_pag_form != '':
                obj_parcela.data_liquidacao = data_pag_form
                obj_parcela.tipo_prazo = 'PG'

            obj_parcela.val_pago = val_pag_form.replace('.','').replace(',','.')
            obj_parcela.save()
            msg = 'Pagamento efetivado com sucesso!'

            num_parc = 0
            lista_parcelas = (Parcela_Contrato.objects.filter(cod_contrato=obj_parcela.cod_contrato,
                                                              tipo_prazo__in=['CP', 'LP'])
                              .order_by('cod_parcela_contrato'))
            for parc in lista_parcelas:
                num_parc += 1
                tipo_prazo = ''
                if num_parc <= 12:
                    tipo_prazo = 'CP'
                else:
                    tipo_prazo = 'LP'
                parc.tipo_prazo = tipo_prazo
                parc.save(update_fields=['tipo_prazo'])

        elif transacao_form == 'atualiza_dados':
            val_conta_form = request.POST['val_conta']
            val_principal_form = request.POST['val_principal']
            val_taxas_form = request.POST['val_taxas']
            val_fundo_form = request.POST['val_fundo']

            obj_parcela.val_conta = val_conta_form
            obj_parcela.val_principal = val_principal_form
            obj_parcela.val_taxas = val_taxas_form
            obj_parcela.val_fundo = val_fundo_form
            obj_parcela.val_corrigido = float(val_principal_form) + float(val_taxas_form)
            obj_parcela.save(update_fields=['val_conta', 'val_principal', 'val_taxas', 'val_fundo', 'val_corrigido'])
            msg = 'Dados atualizados com sucesso!'

        data = dict()
        data = {
            'msg': msg,
            'cod_conta': obj_parcela.cod_contrato.cod_conta.cod_conta
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_parc = self.get_object(int(pk.split('_')[0]))
        obj_parc.val_pago = None
        obj_parc.data_liquidacao = None
        obj_parc.tipo_prazo  ='E'
        obj_parc.obs_parcela = (' / estorno:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_parc.save(update_fields=['val_pago', 'data_liquidacao', 'obs_parcela', 'tipo_prazo'])
        msg = 'Registro estornado com sucesso!'

        num_parc = 0
        lista_parcelas = (Parcela_Contrato.objects.filter(cod_contrato=obj_parc.cod_contrato,
                                                          tipo_prazo__in=['CP', 'LP', 'E'])
                          .order_by('cod_parcela_contrato'))
        for parc in lista_parcelas:
            num_parc += 1
            tipo_prazo = ''
            if num_parc <= 12:
                tipo_prazo = 'CP'
            else:
                tipo_prazo = 'LP'
            parc.tipo_prazo = tipo_prazo
            parc.save(update_fields=['tipo_prazo'])
        data = dict()
        data = {
            'msg' : msg,
            'cod_conta': obj_parc.cod_contrato.cod_conta.cod_conta
        }
        return JsonResponse(data, safe=False)

class Form_Conciliacao_Comp_Benner_Resumo_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_usuarios_contabil = (Usuario.objects
                                   .filter(sala='CON',
                                           cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))

        lista_contas_modelo_1 = Conta.objects.filter(tipo_modelo=1, status_comp='A')

        lista_pacotes = Pacote_Conta.objects.all()

        contexto = {
            'lista_contas_modelo_1': lista_contas_modelo_1,
            'desc_menu': 'Conciliação Composição x Benner Resumido',
            'lista_usuarios_contabil': lista_usuarios_contabil,
            'lista_pacotes': lista_pacotes,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'contabil_composicao_app/form_conciliacao_composicao_benner.html', contexto)

class Form_Conciliacao_Comp_Benner_Detalhado_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_usuarios_contabil = (Usuario.objects
                                   .filter(sala='CON',
                                           cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))

        lista_contas_modelo_1 = Conta.objects.filter(tipo_modelo=1, status_comp='A')

        lista_pacotes = Pacote_Conta.objects.all()
        contexto = {
            'lista_contas_modelo_1': lista_contas_modelo_1,
            'desc_menu': 'Conciliação Composição x Benner Detalhado',
            'lista_usuarios_contabil': lista_usuarios_contabil,
            'lista_pacotes': lista_pacotes,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'contabil_composicao_app/form_conciliacao_composicao_benner_detalhado.html', contexto)

    def post(self, request):
        dados_json_ajax = json.loads(request.body)
        lista_registros_contas = dados_json_ajax['let_lista_registros_json']

        for reg in lista_registros_contas:
            cod_contrato_form = reg['cod_contrato']
            tipo_prazo_form = reg['tipo_prazo']
            cod_status_form = reg['cod_status']
            obs_status_form = reg['obs_status']
            competencia_form = reg['competencia']
            val_composicao_form = reg['val_composicao']
            val_balancete_form = reg['val_balancete']
            val_diferenca_form = reg['val_diferenca']

            competencia_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), 1)
            data_hora_atual = datetime.now()
            data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

            cod_usuario_sessao = request.session['cod_usuario_logado']
            obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

            obj_status_competencia = None
            obj_contrato = None
            obj_conta = None
            if tipo_prazo_form == 'm1':
                obj_conta = Conta.objects.get(pk=cod_contrato_form)
                obj_status_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                    cod_conta=obj_conta, data_competencia=competencia_date, tipo_prazo=tipo_prazo_form,
                    cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa
                ).first()
            else:
                obj_contrato = Contrato.objects.get(pk=cod_contrato_form)
                obj_conta = obj_contrato.cod_conta
                obj_status_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                    cod_contrato=obj_contrato, data_competencia=competencia_date, tipo_prazo=tipo_prazo_form,
                    cod_contrato__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa
                ).first()

            val_comp_dec = decimal.Decimal(val_composicao_form)
            val_bal_dec = decimal.Decimal(val_balancete_form)
            val_dif_dec  = decimal.Decimal(val_diferenca_form)


            if obj_status_competencia != None:
                obj_status_competencia.status = cod_status_form
                obj_status_competencia.data_lan_auditoria = data_hora_atual
                obj_status_competencia.data_competencia = competencia_date
                obj_status_competencia.obs_status = obs_status_form.strip()
                obj_status_competencia.val_composicao = val_comp_dec
                obj_status_competencia.val_balancete = val_bal_dec
                obj_status_competencia.val_diferenca = val_dif_dec
                obj_status_competencia.cod_usu = obj_usuario_sessao
                obj_status_competencia.save()
            else:
                obj_status_competencia = Auditoria_Status_Composicao_Competencia(
                    status = cod_status_form,
                    tipo_prazo = tipo_prazo_form,
                    data_competencia = competencia_date,
                    val_composicao = val_comp_dec,
                    val_balancete = val_bal_dec ,
                    val_diferenca = val_dif_dec,
                    obs_status = obs_status_form.strip(),
                    cod_usu = obj_usuario_sessao,
                    cod_contrato = obj_contrato,
                    cod_conta= obj_conta
                ).save()

        data = dict()
        data = {
            'msg': 'Status registrado com sucesso !!'
        }
        return JsonResponse(data, safe=False)

class Comp_Cb_Contas_Conciliacao_Comp_Benner_View(View):
    def get(self, request):
        tipo_rel = request.GET['tipo_rel']
        cod_tipo_modelo_form = request.GET['cod_modelo_conta']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_contas = []
        lista_contas_para_atualizar_benner = None
        if tipo_rel in ('R', 'D', 'C'):
            if tipo_rel == 'C':
                nome_resp_frm = request.GET['nome_resp']
                if nome_resp_frm != '':
                    lista_resp_contas = (Responsaveis_Conta.objects
                                    .filter((Q(resp_composicao__in=nome_resp_frm.split(',')) | Q(resp_validacao__in=nome_resp_frm.split(','))),
                                            cod_conta__tipo_modelo=cod_tipo_modelo_form) #cod_conta__status_comp='A'
                                    .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                            'cod_conta__cod_red_conta_contabil_cp','cod_conta__cod_red_conta_contabil_lp').distinct())
                    for reg in lista_resp_contas:
                        conta = {
                            'cod_conta': reg['cod_conta__cod_conta'],
                            'desc_conta': reg['cod_conta__desc_conta'],
                            'cod_red_conta_contabil_cp': reg['cod_conta__cod_red_conta_contabil_cp'],
                            'cod_red_conta_contabil_lp': reg['cod_conta__cod_red_conta_contabil_lp']
                        }
                        lista_contas.append(conta)
                else:
                    lista_contas = list(Conta.objects.filter(tipo_modelo=cod_tipo_modelo_form) #status_comp='A'
                                        .values('cod_conta', 'desc_conta', 'cod_red_conta_contabil_cp',
                                                'cod_red_conta_contabil_lp'))
            elif tipo_rel in ('D', 'R'):
                nome_resp_frm = request.GET['nome_resp']
                lista_pacotes = request.GET['lista_pacotes']

                lista_resp_contas = (Responsaveis_Conta.objects
                                     .filter(
                    (Q(resp_composicao__in=nome_resp_frm.split(',')) | Q(resp_validacao__in=nome_resp_frm.split(','))),
                    cod_conta__tipo_modelo=cod_tipo_modelo_form, cod_conta__status_comp='A',
                    cod_conta__cod_pacote_conta__cod_pacote_conta__in=lista_pacotes.split(','))
                                     .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                             'cod_conta__cod_red_conta_contabil_cp',
                                             'cod_conta__cod_red_conta_contabil_lp').distinct())
                for reg in lista_resp_contas:
                    conta = {
                        'cod_conta': reg['cod_conta__cod_conta'],
                        'desc_conta': reg['cod_conta__desc_conta'],
                        'cod_red_conta_contabil_cp': reg['cod_conta__cod_red_conta_contabil_cp'],
                        'cod_red_conta_contabil_lp': reg['cod_conta__cod_red_conta_contabil_lp']
                    }
                    lista_contas.append(conta)
            else:
                lista_contas = list(Conta.objects.filter(tipo_modelo=cod_tipo_modelo_form, status_comp='A')
                                    .values('cod_conta', 'desc_conta', 'cod_red_conta_contabil_cp',
                                            'cod_red_conta_contabil_lp'))

            lista_contas_para_atualizar_benner = list(Contrato.objects
                                                  .filter(cod_conta__tipo_modelo=cod_tipo_modelo_form,
                                                          cod_conta__status_comp='A',
                                                          sincronizar_benner='S',
                                                          cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                  .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                                          'cod_conta__cod_red_conta_contabil_cp',
                                                          'cod_conta__cod_red_conta_contabil_lp')
                                                  .distinct())
        elif tipo_rel == 'A':
            competencia_form = request.GET['data_competencia']
            competencia_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), 1)
            lista_contas = list(Auditoria_Status_Composicao_Competencia.objects
                                .filter(cod_conta__tipo_modelo=cod_tipo_modelo_form, cod_conta__status_comp='A',
                                        status=1, data_competencia=competencia_date,
                                        cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                         'cod_conta__cod_red_conta_contabil_cp', 'cod_conta__cod_red_conta_contabil_lp')
                                .distinct())
        elif tipo_rel == 'P':
            nome_resp_frm = request.GET['nome_resp']
            if nome_resp_frm != '':
                lista_resp_contas = (Responsaveis_Conta.objects
                                     .filter(
                    (Q(resp_composicao__in=nome_resp_frm.split(',')) | Q(resp_validacao__in=nome_resp_frm.split(','))),
                    cod_conta__tipo_modelo=cod_tipo_modelo_form, cod_conta__status_comp='A')
                                     .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                             'cod_conta__cod_red_conta_contabil_cp',
                                             'cod_conta__cod_red_conta_contabil_lp')
                                     .distinct())
                for reg in lista_resp_contas:
                    conta = {
                        'cod_conta': reg['cod_conta__cod_conta'],
                        'desc_conta': reg['cod_conta__desc_conta'],
                        'cod_red_conta_contabil_cp': reg['cod_conta__cod_red_conta_contabil_cp'],
                        'cod_red_conta_contabil_lp': reg['cod_conta__cod_red_conta_contabil_lp']
                    }
                    lista_contas.append(conta)
            else:
                lista_contas = list(Conta.objects.filter(tipo_modelo=cod_tipo_modelo_form, status_comp='A')
                                    .values('cod_conta', 'desc_conta', 'cod_red_conta_contabil_cp',
                                            'cod_red_conta_contabil_lp'))
                '''for nome in nome_resp_frm.split(','):
                    lista_resp_contas = (Responsaveis_Conta.objects
                                    .filter((Q(resp_composicao=nome) | Q(resp_validacao=nome)),
                                            cod_conta__tipo_modelo=cod_tipo_modelo_form, cod_conta__status_comp='A')
                                    .values('cod_conta__cod_conta', 'cod_conta__desc_conta', 'cod_conta__cod_red_conta_contabil_cp',
                                            'cod_conta__cod_red_conta_contabil_lp'))
                    for reg in lista_resp_contas:
                        conta = {
                            'cod_conta': reg['cod_conta__cod_conta'],
                            'desc_conta': reg['cod_conta__desc_conta'],
                            'cod_red_conta_contabil_cp': reg['cod_conta__cod_red_conta_contabil_cp'],
                            'cod_red_conta_contabil_lp': reg['cod_conta__cod_red_conta_contabil_lp']
                        }
                        lista_contas.append(conta)'''


        lista_pacotes_conta = list(Pacote_Conta.objects.filter(cod_modelo=cod_tipo_modelo_form)
                                   .values('cod_pacote_conta', 'desc_pacote_conta'))
        data = dict()
        data = {
            'lista_contas': lista_contas,
            'lista_pacotes_conta': lista_pacotes_conta,
            'lista_contas_para_atualizar_benner': lista_contas_para_atualizar_benner
        }
        return JsonResponse(data, safe=False)

class Gera_Conciliacao_Comp_Benner_View(View):
    def get(self, request):
        cod_modelo_selecionado_form = request.GET['cod_modelo_selecionado']
        lista_cod_conta_form = request.GET['cod_conta']
        competencia_form = request.GET['competencia']
        tipo_visualizacao_form = request.GET['tipo_visualizacao']

        data_competencia = competencia_form + '-01'
        ultimo_dia_mes_calendar = calendar.monthrange(int(competencia_form.split('-')[0]),
                                                      int(competencia_form.split('-')[1]))[1]
        ultimo_dia_mes_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]),
                                       ultimo_dia_mes_calendar)
        primeiro_dia_ano = datetime(int(competencia_form.split('-')[0]), 1, 1)
        ultimo_dia_ano = datetime(int(competencia_form.split('-')[0]), 12, 31)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_contas_conciliacao = []
        #for cod_conta_form in lista_cod_conta_form.split(','):
        if tipo_visualizacao_form == 'R':
            if cod_modelo_selecionado_form == '1':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    registros_tabela = []
                    val_composicao = 0
                    val_dif = 0
                    val_balancete = 0
                    conta_auditada = (Auditoria_Status_Composicao_Competencia.objects
                                      .filter(cod_conta=obj_conta,data_competencia=data_competencia,
                                              cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,status=1)
                                      .first())
                    if conta_auditada == None:
                        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
                            registros_tabela = list(Docs_Pac_Contas_Pagar_Receber_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
                            registros_tabela = list(Docs_Pac_Estoque_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
                            registros_tabela = list(Docs_Pac_Folha_Pag_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
                            registros_tabela = list(Docs_Pac_Contas_Compensacao_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
                            registros_tabela = list(Docs_Pac_Tributos_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
                            registros_tabela = list(Docs_Pac_Finac_Disponib_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
                            registros_tabela = list(Docs_Pac_Intercompany_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
                            registros_tabela = list(Docs_Pac_Imobilizado_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
                            registros_tabela = list(Docs_Pac_Consorcio_Ativo_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 14:
                            registros_tabela = list(Docs_Demais_Contas_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))

                        for reg in registros_tabela:
                            val_composicao += float(reg.tt_val_rel)

                        val_balancete = ConexaoBancoBenner() \
                            .retorna_balancete_conta(obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa,
                                                     obj_conta.handle_conta_contabil_cp,
                                                     primeiro_dia_ano,
                                                     ultimo_dia_mes_date)

                        if val_balancete < 0 and val_composicao < 0:
                            val_dif = val_composicao - val_balancete
                        elif val_balancete < 0 and val_composicao > 0:
                            val_dif = val_composicao + val_balancete
                        else:
                            val_dif = val_composicao - val_balancete
                    else:
                        #Se existir registro na conta_auditada
                        val_composicao = float(conta_auditada.val_composicao)
                        val_balancete = float(conta_auditada.val_balancete)
                        val_dif = float(conta_auditada.val_diferenca)


                    #cod_anexo_competencia = 0
                    lista_anexos_competencia = list(Anexos_Contrato.objects
                                             .filter(cod_conta=obj_conta,
                                                     data_competencia=datetime.strptime(competencia_form + '-01','%Y-%m-%d'),
                                                     cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                                     eh_anexo_principal_competencia='S').values('cod_anexo_contrato', 'desc_anexo'))
                    '''if obj_anexo_competencia != None:
                        cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato'''

                    linha = []
                    linha.append(obj_conta.cod_conta) #0
                    linha.append(str(obj_conta.cod_conta)+'-'+obj_conta.desc_conta) #1
                    linha.append(locale.currency(round(val_composicao,2), grouping=True, symbol=None)) #2
                    linha.append(locale.currency(round(val_balancete,2), grouping=True, symbol=None)) #3
                    linha.append(locale.currency(round(val_dif,2), grouping=True, symbol=None)) #4
                    linha.append(lista_anexos_competencia) #5
                    linha.append(obj_conta.cod_red_conta_contabil_cp) #6
                    linha.append(obj_conta.cod_estrut_cp) #7
                    lista_contas_conciliacao.append(linha)

            elif cod_modelo_selecionado_form == '3':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    conta = Conta.objects.get(pk=int(cod_conta_form))
                    lista_contratos = Contrato.objects.filter(cod_conta=conta, cod_conta__status_comp='A',
                                                              cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                    for contrato in lista_contratos:
                        '''Calcula dados CP'''
                        dados_conciliacao_cp = self.gera_reg_conciliacao_por_tipo_prazo(conta, contrato,
                                                                                        primeiro_dia_ano,
                                                                                        ultimo_dia_ano,
                                                                                        ultimo_dia_mes_date,
                                                                                        'CP',
                                                                                        competencia_form)

                        '''Calcula dados LP'''
                        dados_conciliacao_lp = self.gera_reg_conciliacao_por_tipo_prazo(conta, contrato,
                                                                                        primeiro_dia_ano,
                                                                                        ultimo_dia_ano,
                                                                                        ultimo_dia_mes_date,
                                                                                        'LP',
                                                                                        competencia_form)

                        val_comp_cp = float(dados_conciliacao_cp[7].replace('.','')
                                            .replace(',','.'))

                        val_comp_lp = float(dados_conciliacao_lp[7].replace('.','')
                                            .replace(',','.'))

                        val_tt_comp = val_comp_cp + val_comp_lp

                        val_bal_cp = float(dados_conciliacao_cp[8].replace('.','')
                                           .replace(',','.'))

                        val_bal_lp = float(dados_conciliacao_lp[8].replace('.','')
                                           .replace(',','.'))

                        val_tt_bal = val_bal_cp + val_bal_lp



                        val_df_tt_comp_bal = 0
                        if val_tt_bal < 0 and val_tt_comp < 0:
                            val_df_tt_comp_bal = val_tt_comp - val_tt_bal
                        elif val_tt_bal < 0 and val_tt_comp > 0:
                            val_df_tt_comp_bal = val_tt_comp + val_tt_bal
                        else:
                            val_df_tt_comp_bal = val_tt_comp - val_tt_bal

                        #cod_anexo_competencia = 0
                        lista_anexos_competencia = list(Anexos_Contrato.objects
                                                 .filter(cod_contrato=contrato,
                                                         data_competencia=datetime.strptime(competencia_form+'-01', '%Y-%m-%d'),
                                                         cod_contrato__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                                         eh_anexo_principal_competencia='S').values('cod_anexo_contrato', 'desc_anexo'))
                        '''if obj_anexo_competencia != None:
                            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato'''

                        linha = []
                        linha.append(conta.cod_conta) #0
                        linha.append(str(conta.cod_conta)+'-'+conta.desc_conta) #1
                        linha.append(contrato.num_contrato) #2
                        linha.append(contrato.num_doc_contabil) #3
                        linha.append(locale.currency(
                            round(float(dados_conciliacao_cp[7].replace('.', '').replace(',', '.')), 2),
                            grouping=True, symbol=None)) #4
                        linha.append(locale.currency(
                            round(float(dados_conciliacao_cp[8].replace('.', '').replace(',', '.')),
                                  2),
                            grouping=True, symbol=None)) #5
                        linha.append(locale.currency(
                            round(float(
                                dados_conciliacao_cp[9].replace('.', '').replace(',', '.')), 2),
                            grouping=True, symbol=None)) #6
                        linha.append(locale.currency(
                            round(float(dados_conciliacao_lp[7].replace('.', '').replace(',', '.')), 2),
                            grouping=True, symbol=None)) #7
                        linha.append(locale.currency(
                            round(float(dados_conciliacao_lp[8].replace('.', '').replace(',', '.')),
                                  2),
                            grouping=True, symbol=None)) #8
                        linha.append(locale.currency(
                            round(float(
                                dados_conciliacao_lp[9].replace('.', '').replace(',', '.')), 2),
                            grouping=True, symbol=None)) #9
                        linha.append(locale.currency(round(val_tt_comp, 2), grouping=True, symbol=None)) #10
                        linha.append(locale.currency(round(val_tt_bal, 2), grouping=True, symbol=None)) #11
                        linha.append(locale.currency(round(val_df_tt_comp_bal, 2), grouping=True, symbol=None)) #12
                        linha.append(lista_anexos_competencia) #13
                        lista_contas_conciliacao.append(linha)

        elif tipo_visualizacao_form == 'D':
            lista_contas = []
            competencia_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), 1)
            cod_status_analise_form = request.GET['cod_status_analise']
            if cod_status_analise_form == '0':
                lista_contas = lista_cod_conta_form.split(',')
            elif cod_status_analise_form == '5':
                for reg in lista_cod_conta_form.split(','):
                    conta_auditada = Auditoria_Status_Composicao_Competencia.objects.filter(
                        data_competencia=competencia_date, cod_conta__cod_conta=reg,
                        cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa
                    ).first()
                    if conta_auditada == None:
                        lista_contas.append(reg)
            else:
                lista_contas_auditadas = Auditoria_Status_Composicao_Competencia.objects.filter(
                        data_competencia=competencia_date, status=int(cod_status_analise_form),
                    cod_conta__tipo_modelo=cod_modelo_selecionado_form,
                    cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa
                )
                for reg in lista_contas_auditadas:
                    lista_contas.append(reg.cod_conta.cod_conta)

            if cod_modelo_selecionado_form == '1':
                for cod_conta_form in lista_contas:
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    registros_tabela = []
                    val_composicao = 0
                    val_dif = 0
                    val_balancete = 0
                    conta_auditada = (Auditoria_Status_Composicao_Competencia.objects
                                      .filter(cod_conta=obj_conta,
                                              data_competencia=data_competencia,
                                              cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                              status=1).first())
                    if conta_auditada == None:
                        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
                            registros_tabela = list(Docs_Pac_Contas_Pagar_Receber_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
                            registros_tabela = list(Docs_Pac_Estoque_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
                            registros_tabela = list(Docs_Pac_Folha_Pag_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
                            registros_tabela = list(Docs_Pac_Contas_Compensacao_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
                            registros_tabela = list(Docs_Pac_Tributos_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
                            registros_tabela = list(Docs_Pac_Finac_Disponib_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
                            registros_tabela = list(Docs_Pac_Intercompany_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
                            registros_tabela = list(Docs_Pac_Imobilizado_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
                            registros_tabela = list(Docs_Pac_Consorcio_Ativo_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))
                        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 14:
                            registros_tabela = list(Docs_Demais_Contas_M1.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_arquivo__data_competencia=data_competencia,
                                                            ativo='S',
                                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                                    .annotate(tt_val_rel=Sum('val_rel')))


                        for reg in registros_tabela:
                            val_composicao += float(reg.tt_val_rel)

                        val_balancete = ConexaoBancoBenner() \
                            .retorna_balancete_conta(obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa,
                                                     obj_conta.handle_conta_contabil_cp,
                                                     primeiro_dia_ano,
                                                     ultimo_dia_mes_date)

                        if val_balancete < 0 and val_composicao < 0:
                            val_dif = val_composicao - val_balancete
                        elif val_balancete < 0 and val_composicao > 0:
                            val_dif = val_composicao + val_balancete
                        else:
                            val_dif = val_composicao - val_balancete
                    else:
                        # Se existir registro na conta_auditada
                        val_composicao = float(conta_auditada.val_composicao)
                        val_balancete = float(conta_auditada.val_balancete)
                        val_dif = float(conta_auditada.val_diferenca)

                    #cod_anexo_competencia = 0
                    lista_anexos_competencia = list(Anexos_Contrato.objects.filter(cod_conta=obj_conta,
                                                                           data_competencia=datetime.strptime(
                                                                               competencia_form + '-01',
                                                                               '%Y-%m-%d'),
                                                                           cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                                                           eh_anexo_principal_competencia='S').values('cod_anexo_contrato', 'desc_anexo'))
                    '''if obj_anexo_competencia != None:
                        cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato'''


                    '''Verifica se há status da conta na competencia'''
                    cod_status_auditoria_comp = 0
                    obs_status_auditoria_comp = ''
                    obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                        cod_conta=obj_conta, data_competencia=competencia_date,
                        cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa
                    ).first()
                    if obj_status_contrato_competencia != None:
                        cod_status_auditoria_comp = obj_status_contrato_competencia.status
                        obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status


                    linha = []
                    linha.append(obj_conta.cod_conta) #0
                    linha.append(obj_conta.cod_red_conta_contabil_cp) #1
                    linha.append(obj_conta.cod_estrut_cp) #2
                    linha.append(str(obj_conta.cod_conta) + '-' + obj_conta.desc_conta) #3
                    linha.append(locale.currency(round(val_composicao, 2), grouping=True, symbol=None)) #4
                    linha.append(locale.currency(round(val_balancete, 2), grouping=True, symbol=None)) #5
                    linha.append(locale.currency(round(val_dif, 2), grouping=True, symbol=None)) #6
                    linha.append(cod_status_auditoria_comp) #7
                    linha.append(obs_status_auditoria_comp) #8
                    linha.append(lista_anexos_competencia) #9
                    lista_contas_conciliacao.append(linha) #10

            elif cod_modelo_selecionado_form == '3':
                for cod_conta_form in lista_contas:
                    conta = Conta.objects.get(pk=int(cod_conta_form))
                    lista_contratos = Contrato.objects.filter(cod_conta=conta.cod_conta, cod_conta__status_comp='A',
                                                              cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                    for contrato in lista_contratos:
                        '''Calcula dados CP'''
                        dados_conciliacao_cp = self.gera_reg_conciliacao_por_tipo_prazo(conta, contrato, primeiro_dia_ano,
                                                                 ultimo_dia_ano, ultimo_dia_mes_date,'CP', competencia_form)
                        lista_contas_conciliacao.append(dados_conciliacao_cp)

                        '''Calcula dados LP'''
                        dados_conciliacao_lp = self.gera_reg_conciliacao_por_tipo_prazo(conta, contrato,
                                                                                        primeiro_dia_ano,
                                                                                        ultimo_dia_ano,
                                                                                        ultimo_dia_mes_date, 'LP', competencia_form)
                        lista_contas_conciliacao.append(dados_conciliacao_lp)

        elif tipo_visualizacao_form == 'A':
            competencia_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), 1)
            if cod_modelo_selecionado_form == '1':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    '''Mostra somente as contas que estão com status da composição ok'''
                    lista_composicao = (Auditoria_Status_Composicao_Competencia.objects
                                        .filter(cod_conta=obj_conta, status=1, data_competencia=competencia_date,
                                                cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))

                    for reg in lista_composicao:
                        #cod_anexo_competencia = 0
                        lista_anexos_competencia = list(Anexos_Contrato.objects
                                                 .filter(cod_conta=obj_conta,
                                                         data_competencia=datetime.strptime(competencia_form + '-01','%Y-%m-%d'),
                                                         cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                                         eh_anexo_principal_competencia='S').values('cod_anexo_contrato', 'desc_anexo'))
                        '''if obj_anexo_competencia != None:
                            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato'''

                        linha = []
                        linha.append(obj_conta.cod_conta)  # 0
                        linha.append(obj_conta.cod_red_conta_contabil_cp)  # 1
                        linha.append(obj_conta.cod_estrut_cp)  # 2
                        linha.append(str(obj_conta.cod_conta) + '-' + obj_conta.desc_conta)  # 3
                        linha.append(locale.currency(round(reg.val_composicao, 2), grouping=True, symbol=None))  # 4
                        linha.append(locale.currency(round(reg.val_balancete, 2), grouping=True, symbol=None))  # 5
                        linha.append(locale.currency(round(reg.val_diferenca, 2), grouping=True, symbol=None))  # 6
                        linha.append(lista_anexos_competencia)  # 7
                        lista_contas_conciliacao.append(linha)

            elif cod_modelo_selecionado_form == '3':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    lista_composicao = (Auditoria_Status_Composicao_Competencia.objects
                                        .filter(cod_conta=obj_conta, status=1, data_competencia=competencia_date,
                                                cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))

                    for reg in lista_composicao:
                        cod_reduzido = '0'
                        cod_estrutura = '0'
                        if reg.tipo_prazo == 'CP':
                            cod_estrutura = obj_conta.cod_estrut_cp
                            cod_reduzido = obj_conta.cod_red_conta_contabil_cp

                        elif reg.tipo_prazo == 'LP':
                            cod_estrutura = obj_conta.cod_estrut_lp
                            cod_reduzido = obj_conta.cod_red_conta_contabil_lp



                        #cod_anexo_competencia = 0
                        lista_anexos_competencia = list(Anexos_Contrato.objects.filter(cod_contrato=reg.cod_contrato,
                                                                               data_competencia=datetime.strptime(
                                                                                   competencia_form + '-01',
                                                                                   '%Y-%m-%d'),
                                                                               cod_contrato__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                                                               eh_anexo_principal_competencia='S').values('cod_anexo_contrato', 'desc_anexo'))
                        '''if obj_anexo_competencia != None:
                            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato'''

                        linha = []
                        linha.append(obj_conta.cod_conta)  # 0
                        linha.append(cod_reduzido)  # 1
                        linha.append(cod_estrutura)  # 2
                        linha.append(str(obj_conta.cod_conta) + '-'+ obj_conta.desc_conta)  # 3
                        linha.append(reg.cod_contrato.cod_contrato)  # 4
                        linha.append(reg.cod_contrato.num_contrato)  # 5
                        linha.append(reg.cod_contrato.num_doc_contabil)  # 6
                        linha.append(locale.currency(round(reg.val_composicao, 2), grouping=True, symbol=None))  # 7
                        linha.append(locale.currency(round(reg.val_balancete, 2), grouping=True, symbol=None))  # 8
                        linha.append(locale.currency(round(reg.val_diferenca, 2), grouping=True, symbol=None))  # 9
                        linha.append(reg.tipo_prazo)  # 10
                        linha.append(lista_anexos_competencia)  # 11
                        lista_contas_conciliacao.append(linha)


        data = dict()
        data = {
            'lista_contas_conciliacao': lista_contas_conciliacao
        }
        return JsonResponse(data, safe=False)


    def gera_reg_conciliacao_por_tipo_prazo(self, conta, contrato, primeiro_dia_ano, ultimo_dia_ano,
                                            ultimo_dia_periodo,tipo_prazo, competencia):
        cod_red = 0
        cod_estrutura = 0
        val_composicao = 0
        val_balancete = 0
        val_dif_comp_balanc = 0
        cod_status_auditoria_comp = 0
        obs_status_auditoria_comp = ''

        data_competencia = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
        data_competencia_mais_um = data_competencia + relativedelta(months=1)
        data_competencia_mais_12_meses = data_competencia + relativedelta(months=12)

        ultimo_dia_competencia_calendar = \
        calendar.monthrange(data_competencia_mais_12_meses.year, data_competencia_mais_12_meses.month)[1]
        ultimo_dia_data_competencia_mais_12_meses_date = datetime(data_competencia_mais_12_meses.year,
                                                                  data_competencia_mais_12_meses.month,
                                                                  ultimo_dia_competencia_calendar)


        if tipo_prazo == 'CP':
            cod_red = conta.cod_red_conta_contabil_cp
            cod_estrutura = conta.cod_estrut_cp
            conta_cp_auditada = (Auditoria_Status_Composicao_Competencia.objects
                              .filter(status=1, tipo_prazo=tipo_prazo, data_competencia=competencia + '-01',
                                      cod_usu__cod_filial__cod_empresa=contrato.cod_empresa,
                                      cod_contrato=contrato, cod_conta=conta).first())
            val_composicao = 0
            val_balancete = 0
            val_dif_comp_bal = 0
            if conta_cp_auditada == None:
                val_composicao_ano_dic = Parcela_Contrato.objects \
                    .filter(cod_contrato=contrato,
                            data_vencimento__range=[data_competencia_mais_um,
                                                    ultimo_dia_data_competencia_mais_12_meses_date]) \
                    .aggregate(sum_principal=Sum('val_principal'), sum_val_pago=Sum('val_pago'))


                '''parcelas = Parcela_Contrato.objects \
                    .filter(cod_contrato=contrato,
                            data_vencimento__range=[data_competencia_mais_um,
                                                    ultimo_dia_data_competencia_mais_12_meses_date])

                for parc in parcelas:
                    print(f'Parcela {parc.ordem_parcela}, data venc {parc.data_vencimento}, val. principal {parc.val_principal}, val pago {parc.val_pago}')'''


                val_parcelas_atrasadas = Parcela_Contrato.objects \
                    .filter(cod_contrato=contrato,  #val_pago=0
                            data_vencimento__lte=data_competencia_mais_um) \
                    .extra(where=["data_liquidacao is null or data_liquidacao > '" + str(data_competencia_mais_um) + "' "]) \
                    .aggregate(sum_principal_parc_atrasadas=Sum('val_principal'), sum_val_pago_parc_atrasadas=Sum('val_pago'))

                '''val_parc_atrasadas = Parcela_Contrato.objects \
                    .filter(cod_contrato=contrato,  # val_pago=0
                            data_vencimento__lte=data_competencia_mais_um) \
                    .extra(where=["data_liquidacao is null or data_liquidacao > '" + str(data_competencia_mais_um) + "' "])
                print('Atrasadas')
                for parc_atr in val_parc_atrasadas:
                    print(f'Parcela {parc_atr.ordem_parcela}, data venc {parc_atr.data_vencimento}, val. principal {parc_atr.val_principal}, val pago {parc_atr.val_pago}')'''



                val_composicao_ano = 0
                if val_composicao_ano_dic['sum_principal'] != None:
                    val_composicao_ano = val_composicao_ano_dic['sum_principal']

                val_pago = 0
                if val_composicao_ano_dic['sum_val_pago'] != None:
                    val_pago = val_composicao_ano_dic['sum_val_pago']

                if val_parcelas_atrasadas['sum_principal_parc_atrasadas'] != None:
                    val_composicao_ano += val_parcelas_atrasadas['sum_principal_parc_atrasadas'] - val_parcelas_atrasadas['sum_val_pago_parc_atrasadas']


                val_composicao = val_composicao_ano - val_pago

                val_balancete = ConexaoBancoBenner() \
                                    .retorna_balancete_conta(contrato.cod_empresa.cod_empresa,
                                                             conta.handle_conta_contabil_cp,
                                                             primeiro_dia_ano,
                                                             ultimo_dia_periodo)

                if val_balancete < 0:
                    val_dif_comp_bal = float(val_composicao) + val_balancete
                else:
                    val_dif_comp_bal = float(val_composicao) - val_balancete

            else:
                #Se conta_cp_auditada diferente de None
                val_composicao = conta_cp_auditada.val_composicao
                val_balancete = conta_cp_auditada.val_balancete
                val_dif_comp_bal = conta_cp_auditada.val_diferenca



            '''Verifica se há status da conta na competencia'''
            competencia_date = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
            obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=contrato, tipo_prazo=tipo_prazo, data_competencia=competencia_date,
                cod_usu__cod_filial__cod_empresa=contrato.cod_empresa
            ).first()
            if obj_status_contrato_competencia != None:
                cod_status_auditoria_comp = obj_status_contrato_competencia.status
                obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status

        elif tipo_prazo == 'LP':
            cod_red = conta.cod_red_conta_contabil_lp
            cod_estrutura = conta.cod_estrut_lp
            conta_lp_auditada = (Auditoria_Status_Composicao_Competencia.objects
                                 .filter(status=1, tipo_prazo=tipo_prazo, data_competencia=competencia + '-01',
                                         cod_usu__cod_filial__cod_empresa=contrato.cod_empresa,
                                         cod_contrato=contrato, cod_conta=conta).first())
            val_composicao = 0
            val_balancete = 0
            val_dif_comp_bal = 0
            if conta_lp_auditada == None:
                val_composicao_ano_dic = (Parcela_Contrato.objects \
                    .filter(cod_contrato=contrato, data_vencimento__gt=ultimo_dia_data_competencia_mais_12_meses_date)
                                          .exclude(tipo_prazo='PG') \
                    .aggregate(sum_principal=Sum('val_principal'), sum_val_pago=Sum('val_pago')))

                val_composicao_ano = 0
                if val_composicao_ano_dic['sum_principal'] != None:
                    val_composicao_ano = val_composicao_ano_dic['sum_principal']

                val_pago = 0
                if val_composicao_ano_dic['sum_val_pago'] != None:
                    val_pago = val_composicao_ano_dic['sum_val_pago']


                val_composicao = val_composicao_ano - val_pago
                '''if val_composicao < 0:
                    val_composicao *= -1'''

                val_balancete = ConexaoBancoBenner() \
                                    .retorna_balancete_conta(contrato.cod_empresa.cod_empresa,
                                                             conta.handle_conta_contabil_lp,
                                                             primeiro_dia_ano,
                                                             ultimo_dia_periodo)


                if val_balancete < 0:
                    val_dif_comp_bal = float(val_composicao) + val_balancete
                else:
                    val_dif_comp_bal = float(val_composicao) - val_balancete

            else:
                # Se conta_cp_auditada diferente de None
                val_composicao = conta_lp_auditada.val_composicao
                val_balancete = conta_lp_auditada.val_balancete
                val_dif_comp_bal = conta_lp_auditada.val_diferenca



            '''Verifica se há status da conta na competencia'''
            competencia_date = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
            obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=contrato, tipo_prazo=tipo_prazo, data_competencia=competencia_date,
                cod_usu__cod_filial__cod_empresa=contrato.cod_empresa
            ).first()
            if obj_status_contrato_competencia != None:
                cod_status_auditoria_comp = obj_status_contrato_competencia.status
                obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status



        #cod_anexo_competencia = 0
        lista_anexos_competencia = list(Anexos_Contrato.objects.filter(cod_contrato=contrato,
                                                               data_competencia=datetime.strptime(
                                                                   competencia + '-01', '%Y-%m-%d'),
                                                               cod_contrato__cod_empresa=contrato.cod_empresa.cod_empresa,
                                                               eh_anexo_principal_competencia='S').values('cod_anexo_contrato', 'desc_anexo'))
        '''if obj_anexo_competencia != None:
            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato'''

        linha = []
        linha.append(conta.cod_conta) #0
        linha.append(cod_red) #1
        linha.append(cod_estrutura) #2
        linha.append(str(conta.cod_conta)+'-'+conta.desc_conta) #3
        linha.append(contrato.cod_contrato) #4
        linha.append(contrato.num_contrato) #5
        linha.append(contrato.num_doc_contabil) #6
        linha.append(locale.currency(round(val_composicao, 2), grouping=True, symbol=None)) #7
        linha.append(locale.currency(round(val_balancete, 2), grouping=True, symbol=None)) #8
        linha.append(locale.currency(round(val_dif_comp_bal, 2), grouping=True, symbol=None)) #9
        linha.append(tipo_prazo) #10
        linha.append(cod_status_auditoria_comp) #11
        linha.append(obs_status_auditoria_comp) #12
        linha.append(lista_anexos_competencia) #13

        return linha

class Form_Anexos_Conta_View(View):
    def get_object(self, pk):
        try:
            return Anexos_Contrato.objects.get(pk=pk)
        except Anexos_Contrato.DoesNotExists:
            return Http404

    def post(self, request):
        file_form = request.FILES['file']
        competencia_doc_form = request.POST['competencia_doc']
        cod_conta_form = request.POST['cod_conta']
        cod_contrato_form = request.POST['cod_contrato']
        desc_arq_anexo_frm = request.POST['desc_arq_anexo']
        eh_anexo_principal_frm = request.POST['eh_anexo_principal']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)


        obj_conta_pesq = Conta.objects.get(pk=cod_conta_form)
        msg = self.anexa_arq_conta(obj_usuario_sessao, obj_conta_pesq, cod_contrato_form,
                                   competencia_doc_form, file_form, file_form.name,eh_anexo_principal_frm,
                                   desc_arq_anexo_frm)



        data = dict()
        data = {
            'cod_conta': obj_conta_pesq.cod_conta,
            'msg': msg
        }
        return JsonResponse(data, safe=False)


    def anexa_arq_conta(self, obj_usuario, obj_conta_pesq, cod_contrato_form, competencia_doc_form, file_form,
                        desc_doc_form, eh_anexo_principal_competencia, desc_arq_anexo_frm):
        msg = ''
        obj_contrato_pesq = None
        ordem_max = 0
        ultimo_anexo_conta = 0
        obj_anexo_conta_pesq = None
        novo_nome_arq = ''
        if obj_conta_pesq.tipo_modelo == 3:
            obj_contrato_pesq = Contrato.objects.get(pk=cod_contrato_form)

            ordem_max = Anexos_Contrato.objects \
                .filter(cod_contrato=obj_contrato_pesq, cod_contrato__cod_empresa=obj_usuario.cod_filial.cod_empresa) \
                .aggregate(max_odem_anexo=Max('ordem_anexo'))

            '''obj_anexo_conta_pesq = Anexos_Contrato.objects.filter(cod_contrato=obj_contrato_pesq,
                                                                  data_competencia=datetime.strptime(
                                                                      competencia_doc_form + '-01', '%Y-%m-%d'),
                                                                  cod_contrato__cod_empresa=obj_usuario.cod_filial.cod_empresa).first()'''
            if ordem_max['max_odem_anexo'] != None:
                ultimo_anexo_conta = ordem_max['max_odem_anexo'] + 1

            novo_nome_arq = (str(obj_conta_pesq.cod_conta) + '_' + str(obj_contrato_pesq.num_contrato) + '_' +
                             str(ultimo_anexo_conta) + '_' + competencia_doc_form.split('-')[1] + '_' +
                             competencia_doc_form.split('-')[0] + '_' + eh_anexo_principal_competencia + '.pdf')
        else:

            ordem_max = Anexos_Contrato.objects \
                .filter(cod_conta=obj_conta_pesq, cod_usu__cod_filial__cod_empresa=obj_usuario.cod_filial.cod_empresa) \
                .aggregate(max_odem_anexo=Max('ordem_anexo'))

            '''obj_anexo_conta_pesq = (Anexos_Contrato.objects
                                    .filter(cod_conta=obj_conta_pesq,
                                            data_competencia=datetime.strptime(competencia_doc_form + '-01', '%Y-%m-%d'),
                                            cod_usu__cod_filial__cod_empresa=obj_usuario.cod_filial.cod_empresa).first())'''

            if ordem_max['max_odem_anexo'] != None:
                ultimo_anexo_conta = ordem_max['max_odem_anexo'] + 1

            novo_nome_arq = (str(obj_conta_pesq.cod_conta) + '_X_' +
                             str(ultimo_anexo_conta) + '_' + competencia_doc_form.split('-')[1] + '_' +
                             competencia_doc_form.split('-')[0] + '_' + eh_anexo_principal_competencia +'.pdf')

        fs = FileSystemStorage()
        nome_arquivo = ''
        caminho_arq_importado = ''
        anexo_emp = 'Conlog'
        if obj_usuario.cod_filial.cod_empresa.cod_empresa == 17:
            anexo_emp = 'Deep'

        '''if obj_anexo_conta_pesq != None:
            arquivo_anterior_a_deletar = str(obj_anexo_conta_pesq.caminho_anexo).replace('/', '\\')
            os.remove(arquivo_anterior_a_deletar)'''

        if type(file_form) == str:
            '''arq = (str(obj_conta_pesq.cod_conta) + '_X_' +
                   str(ultimo_anexo_conta) + '_' +
                   competencia_doc_form.split('-')[1] + '_' +
                   competencia_doc_form.split('-')[0] + '_' +
                   eh_anexo_principal_competencia +'.pdf')'''

            caminho_arq_importado = os.path.join(BASE_DIR,
                                                 f'media\\docs\\contabil_composicao_app\\anexos_conta\\{anexo_emp}\\' + novo_nome_arq)
            # caminho_arq_importado = f'docs/contabil_composicao_app/anexos_conta/{anexo_emp}/' + arq

            nome_arquivo = desc_doc_form
            shutil.move(file_form, caminho_arq_importado)  # shutil.move(file_form, '/'+caminho_arq_importado)
        else:
            nome_arquivo = file_form.name
            caminho_arq_importado = os.path.join(BASE_DIR,
                                                 f'media\\docs\\contabil_composicao_app\\anexos_conta\\{anexo_emp}\\' + novo_nome_arq)

            # caminho_arq_importado = f'docs/contabil_composicao_app/anexos_conta/{anexo_emp}/' + novo_nome_arq
            filename = fs.save(caminho_arq_importado, file_form)
            uploaded_file_url = fs.url(filename)
        msg = ''

        desc_arq_validado = desc_arq_anexo_frm
        if desc_arq_validado == None or desc_arq_validado == '':
            desc_arq_validado = novo_nome_arq


        obj_anexo_conta = Anexos_Contrato(
            desc_anexo=desc_arq_validado,
            data_competencia=competencia_doc_form + '-01',
            caminho_anexo=caminho_arq_importado,
            cod_contrato=obj_contrato_pesq,
            cod_conta=obj_conta_pesq,
            ordem_anexo=ultimo_anexo_conta,
            eh_anexo_principal_competencia=eh_anexo_principal_competencia,
            cod_usu=obj_usuario
        ).save()
        msg = 'Doc anexado com sucesso !'

        '''if obj_anexo_conta_pesq == None:
            obj_anexo_conta = Anexos_Contrato(
                desc_anexo=nome_arquivo,
                data_competencia=competencia_doc_form + '-01',
                caminho_anexo=caminho_arq_importado,
                cod_contrato=obj_contrato_pesq,
                cod_conta=obj_conta_pesq,
                ordem_anexo=ultimo_anexo_conta,
                cod_usu=obj_usuario
            ).save()
            msg = 'Doc anexado com sucesso !'
        else:
            #arquivo_anterior_a_deletar = os.path.join(BASE_DIR, 'media\\' + str(obj_anexo_conta_pesq.caminho_anexo).replace('/', '\\'))
            #os.remove(arquivo_anterior_a_deletar)

            obj_anexo_conta_pesq.desc_anexo = nome_arquivo
            obj_anexo_conta_pesq.caminho_anexo = caminho_arq_importado
            obj_anexo_conta_pesq.ordem_anexo = ultimo_anexo_conta
            obj_anexo_conta_pesq.cod_usu=obj_usuario
            obj_anexo_conta_pesq.save()
            msg = 'Registro atualizado com sucesso!'''
        return msg

    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        obj_conta = Conta.objects.get(pk=cod_conta_form)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_contratos = []
        lista_anexos = []
        if obj_conta.tipo_modelo == 1:
            lista_anexos = list(Anexos_Contrato.objects\
                .filter(cod_conta = obj_conta,
                        cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)\
                .values('cod_anexo_contrato', 'desc_anexo', 'caminho_anexo', 'data_competencia', 'eh_anexo_principal_competencia'))
        elif obj_conta.tipo_modelo == 3:
            lista_contratos = list(Contrato.objects.filter(cod_conta=obj_conta).values('cod_contrato', 'num_contrato'))
            lista_anexos = list(Anexos_Contrato.objects\
                .filter(cod_contrato__cod_conta = obj_conta,
                        cod_contrato__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)\
                .values('cod_contrato__num_contrato', 'cod_anexo_contrato', 'desc_anexo', 'caminho_anexo',
                        'data_competencia', 'eh_anexo_principal_competencia'))

        if len(lista_anexos) > 0:
            for anx in lista_anexos:
                anx['data_competencia'] = datetime.strftime(anx['data_competencia'], '%m-%Y')



        data = dict()
        data = {
            'lista_anexos': lista_anexos,
            'lista_contratos': lista_contratos,
            'status_corporativo_usu': obj_usuario_sessao.corporativo
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_anexo_conta = self.get_object(pk)
        cod_conta = 0
        obj_contrato = obj_anexo_conta.cod_contrato
        if obj_contrato == None:
            cod_conta = obj_anexo_conta.cod_conta.cod_conta
        else:
            cod_conta = obj_contrato.cod_conta.cod_conta
        caminho_completo = str(obj_anexo_conta.caminho_anexo).replace('/', '\\')
        os.remove(caminho_completo)
        obj_anexo_conta.delete()
        data = dict()
        data = {
            'cod_conta': cod_conta,
            'msg': 'Anexo excluído com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Form_Visualiza_Doc_Contrato_View(View):
    def get(self, request):
        cod_anexo_contrato_form = request.GET['cod_anexo_contrato']

        obj_anexo_contrato = Anexos_Contrato.objects.get(pk=cod_anexo_contrato_form)

        '''dados = {
            'caminho_doc': obj_anexo_contrato.caminho_anexo
        }'''
        #return render(request, 'contabil_composicao_app/pag_exibe_doc_contrato.html', dados)
        return JsonResponse(obj_anexo_contrato.caminho_anexo, safe=False)

    def post(self, request):
        cod_anexo_contrato_frm = request.POST['cod_anexo_contrato']
        status_anexo_frm = request.POST['status_anexo']

        obj_anexo_contrato = Anexos_Contrato.objects.get(pk=cod_anexo_contrato_frm)
        obj_anexo_contrato.eh_anexo_principal_competencia = status_anexo_frm
        obj_anexo_contrato.save()
        
        msg = ''
        if status_anexo_frm == 'S':
            msg = 'Anexo selecionado para visualização na composição'
        else:
            msg = 'Anexo selecionado como secundário'
        
        data = dict()
        data = {
            'cod_conta': obj_anexo_contrato.cod_conta.cod_conta,
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Form_Status_Contrato_Composicao_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        obj_conta = Conta.objects.get(pk=cod_conta_form)
        lista_status_contratos_comp = list(Auditoria_Status_Composicao_Competencia.objects
                                           .filter(cod_conta=obj_conta,
                                                   cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                           .order_by('cod_contrato__cod_contrato', 'tipo_prazo', 'data_competencia')
                                           .values('cod_auditoria_composicao', 'status', 'data_lan_auditoria',
                                                   'data_competencia', 'obs_status', 'cod_usu__nome_usu',
                                                   'cod_contrato__cod_contrato', 'cod_contrato__num_contrato',
                                                   'tipo_prazo', 'val_composicao', 'val_balancete', 'val_diferenca'))
        for reg in lista_status_contratos_comp:
            reg['val_composicao'] = locale.currency(round(float(reg['val_composicao']), 2), grouping=True, symbol=None)
            reg['val_balancete'] = locale.currency(round(float(reg['val_balancete']), 2), grouping=True, symbol=None)
            reg['val_diferenca'] = locale.currency(round(float(reg['val_diferenca']), 2), grouping=True, symbol=None)
        data = dict()
        data = {
            'lista_status_contratos_comp': lista_status_contratos_comp
        }
        return JsonResponse(data, safe=False)

class Tabela_Pac_Contas_Modelo_1_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        lista_campos_layout_tab = []
        desc_pacote_conta = ''
        cod_pacote_conta = 0
        if cod_conta_form != '0':
            obj_conta = Conta.objects.get(pk=cod_conta_form)
            lista_campos_layout_tab = list(Layout_Campos_Contas_Modelo_1.objects
                              .filter((Q(cod_layout__data_fim_vig__lte=data_atual_dd_mm_yyyy) | Q(cod_layout__data_fim_vig__isnull=True)),
                                             cod_layout__cod_pacote_conta=obj_conta.cod_pacote_conta)
                              .values('cod_campo__desc_campo', 'cod_layout__tipo_pesq').order_by('num_posicao_campo'))
            desc_pacote_conta = obj_conta.cod_pacote_conta.desc_pacote_conta
            cod_pacote_conta = obj_conta.cod_pacote_conta.cod_pacote_conta
        else:
            cod_pacote_conta_form = request.GET['cod_pacote_conta']
            obj_pacote = Pacote_Conta.objects.get(pk=cod_pacote_conta_form)
            lista_campos_layout_tab = list(Layout_Campos_Contas_Modelo_1.objects
                                           .filter(
                (Q(cod_layout__data_fim_vig__lte=data_atual_dd_mm_yyyy) | Q(cod_layout__data_fim_vig__isnull=True)),
                cod_layout__cod_pacote_conta=obj_pacote)
                                           .values('cod_campo__desc_campo', 'cod_layout__tipo_pesq')
                                           .order_by('num_posicao_campo'))
            desc_pacote_conta = obj_pacote.desc_pacote_conta
            cod_pacote_conta = obj_pacote.cod_pacote_conta
        data = dict()
        data = {
            'lista_campos_layout_tab': lista_campos_layout_tab,
            'desc_pacote_conta': desc_pacote_conta,
            'cod_pacote_conta': cod_pacote_conta,
            'tipo_pesquisa': lista_campos_layout_tab[0]['cod_layout__tipo_pesq']
        }
        return JsonResponse(data, safe=False)

class Form_Imp_Arq_Contas_M1_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        lista_contas = Conta.objects.filter(tipo_modelo=1, status_comp= 'A')
        context = {
            'lista_contas': lista_contas,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'contabil_composicao_app/form_importa_arquivo_modelo_1.html', context)

    def post(self, request):
        arquivo_form = request.FILES['file']
        cod_pacote_conta_form = request.POST['cod_pacote_conta']
        competencia_form = request.POST['competencia']

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_pac_conta = Pacote_Conta.objects.get(pk=cod_pacote_conta_form)
        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')
        hora_atual = data_hora_atual.strftime('%H:%M:%S')

        caminho_arq_imp = ('docs/contabil_composicao_app/arq_pac_docs_m1/' + str(obj_pac_conta.desc_pacote_conta) +
                           '/' + competencia_form + '/' +obj_pac_conta.desc_pacote_conta + '_' +
                           str(data_hora_atual_h_m_y).replace('/', '_')  +
                           '_' + str(hora_atual).replace(':', '_') + '.xlsx')

        fs = FileSystemStorage()
        filename = fs.save(caminho_arq_imp, arquivo_form)
        uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_imp)
        df_conteudo_arqv = pd.read_excel(uploaded_file_url)
        df_conteudo_arqv.fillna('', inplace=True)

        obj_arqv_pesq = (Arquivo_Docs_Pac_Contas_Modelo_1.objects
                         .filter(
            nome_arqv_original = str(arquivo_form.name),
            cod_pacote_conta = obj_pac_conta,
            data_competencia = competencia_form + '-01')).first()
        if obj_arqv_pesq != None:
            lista_registros_arqv = None
            if obj_pac_conta.cod_pacote_conta == 3:
                lista_registros_arqv = Docs_Pac_Contas_Pagar_Receber_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 4:
                lista_registros_arqv = Docs_Pac_Estoque_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 5:
                lista_registros_arqv = Docs_Pac_Folha_Pag_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 6:
                lista_registros_arqv = Docs_Pac_Contas_Compensacao_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 7:
                lista_registros_arqv = Docs_Pac_Tributos_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 9:
                lista_registros_arqv = Docs_Pac_Finac_Disponib_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 10:
                lista_registros_arqv = Docs_Pac_Intercompany_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 11:
                lista_registros_arqv = Docs_Pac_Imobilizado_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 13:
                lista_registros_arqv = Docs_Pac_Consorcio_Ativo_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 14:
                lista_registros_arqv = Docs_Demais_Contas_M1.objects.filter(cod_arquivo=obj_arqv_pesq)
            for reg in lista_registros_arqv:
                reg.delete()

            obj_arqv_pesq.delete()
        msg = ''
        obj_arqv = None
        #try:
        obj_arqv = Arquivo_Docs_Pac_Contas_Modelo_1(
            qtd_reg_imp= df_conteudo_arqv.shape[0],
            nome_arqv_original = str(arquivo_form.name),
            nome_arquivo_importado = caminho_arq_imp,
            erro = 'N',
            data_competencia = competencia_form + '-01',
            cod_usu = obj_usu,
            cod_pacote_conta = obj_pac_conta
        )
        obj_arqv.save()


        doc = None
        if obj_pac_conta.cod_pacote_conta == 3:
            for index, row in df_conteudo_arqv.iterrows():
                data_lancto = None
                if row['Data Lançto'] != '':
                    if type(row['Data Lançto']) == str:
                        data_lancto = datetime.strptime(row['Data Lançto'], '%d/%m/%Y')
                    else:
                        data_lancto = row['Data Lançto']

                data_venc = None
                if row['Data Vencim.'] != '':
                    if type(row['Data Vencim.']) == str:
                        data_venc = datetime.strptime(row['Data Vencim.'], '%d/%m/%Y')
                    else:
                        data_venc = row['Data Vencim.']

                doc = Docs_Pac_Contas_Pagar_Receber_M1 (
                    data_lancto= data_lancto,
                    cnpj = row['CNPJ'],
                    nome_fornecedor = row['Nome Fornecedor'],
                    num_doc = row['Nº Documento'],
                    num_ap = row['Nº AP'],
                    num_parc = row['Nº Parc'],
                    data_venc = data_venc,
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    obs = row['Observação'],
                    cod_conta = Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                       cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo = obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 4:
            for index, row in df_conteudo_arqv.iterrows():
                doc = Docs_Pac_Estoque_M1(
                    nome_almoxarifado=row['Nome Almoxarifado'],
                    cod_produto = row['Código Produto'],
                    desc_produto = row['Descrição Produto'],
                    qtd_prod = row['Qtd'],
                    custo_medio = row['Custo Médio'],
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    obs = row['Observação'],
                    cod_conta = Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                       cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo = obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 5:
            for index, row in df_conteudo_arqv.iterrows():
                data_lancto = None
                if row['Data Lançto'] != '':
                    if type(row['Data Lançto']) == str:
                        data_lancto = datetime.strptime(row['Data Lançto'], '%d/%m/%Y')
                    else:
                        data_lancto = row['Data Lançto']

                doc = Docs_Pac_Folha_Pag_M1(
                    data_lancto=data_lancto,
                    matricula = row['Matrícula'],
                    historico = row['Histórico'],
                    num_doc = row['Nº Documento'],
                    num_doc_contabil = row['Documento Contábil'],
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    obs = row['Observação'],
                    cod_conta = Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                       cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo = obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 6:
            for index, row in df_conteudo_arqv.iterrows():
                data_emissao = None
                if row['Data Emissão'] != '':
                    if type(row['Data Emissão']) == str:
                        data_emissao = datetime.strptime(row['Data Emissão'], '%d/%m/%Y')
                    else:
                        data_emissao = row['Data Emissão']

                data_entrada = None
                if row['Data Entrada'] != '':
                    if type(row['Data Entrada']) == str:
                        data_entrada = datetime.strptime(row['Data Entrada'], '%d/%m/%Y')
                    else:
                        data_entrada = row['Data Entrada']

                doc = Docs_Pac_Contas_Compensacao_M1(
                    data_emissao = data_emissao,
                    data_entrada = data_entrada,
                    cnpj = row['CNPJ'],
                    nome_fornecedor = row['Nome Fornecedor'],
                    num_doc = row['Nº Documento'],
                    num_doc_contabil = row['Documento Contábil'],
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    obs = row['Observação'],
                    historico = row['Histórico'],
                    cod_conta = Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                       cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo = obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 7:
            for index, row in df_conteudo_arqv.iterrows():
                data_entr = None
                if row['Data Entrada'] != '':
                    if type(row['Data Entrada']) == str:
                        data_entr = datetime.strptime(row['Data Entrada'], '%d/%m/%Y')
                    else:
                        data_entr = row['Data Entrada']

                data_emissao = None
                if row['Data Emissão'] != '':
                    if type(row['Data Emissão']) == str:
                        data_emissao = datetime.strptime(row['Data Emissão'], '%d/%m/%Y')
                    else:
                        data_emissao = row['Data Emissão']

                doc = Docs_Pac_Tributos_M1(
                    data_emissao=data_emissao,
                    data_entrada=data_entr,
                    nome_fornecedor=row['Nome Fornecedor'],
                    num_doc=row['Nº Documento'],
                    num_doc_contabil=row['Documento Contábil'],
                    val_rel=row['Valor Relatório'],
                    val_razao=row['Valor Razão'],
                    val_dif=row['Diferença'],
                    obs=row['Observação'],
                    historico=row['Histórico'],
                    cod_conta=Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                     cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo=obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 9:
            for index, row in df_conteudo_arqv.iterrows():
                data_lancto = None
                if row['Data Lançto'] != '':
                    if type(row['Data Lançto']) == str:
                        data_lancto = datetime.strptime(row['Data Lançto'], '%d/%m/%Y')
                    else:
                        data_lancto = row['Data Lançto']

                doc = Docs_Pac_Finac_Disponib_M1(
                    num_doc = row['Nº Documento'],
                    data_lancto = data_lancto,
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    historico = row['Histórico'],
                    obs = row['Observação'],
                    cod_conta=Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                     cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo=obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 10:
            for index, row in df_conteudo_arqv.iterrows():
                data_lancto = None
                if row['Data Lançto'] != '':
                    if type(row['Data Lançto']) == str:
                        data_lancto = datetime.strptime(row['Data Lançto'], '%d/%m/%Y')
                    else:
                        data_lancto = row['Data Lançto']

                doc = Docs_Pac_Intercompany_M1(
                    num_doc=row['Nº Documento'],
                    data_lancto=data_lancto,
                    val_rel=row['Valor Relatório'],
                    val_razao=row['Valor Razão'],
                    val_dif=row['Diferença'],
                    historico=row['Histórico'],
                    obs=row['Observação'],
                    cod_conta=Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                     cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo=obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 11:
            for index, row in df_conteudo_arqv.iterrows():
                data_entrada = None
                if row['Data Entrada'] != '':
                    if type(row['Data Entrada']) == str:
                        data_entrada = datetime.strptime(row['Data Entrada'], '%d/%m/%Y')
                    else:
                        data_entrada = row['Data Entrada']

                decimal_places = 2
                context = decimal.Context(prec=12)

                val_depreciacao_acum = 0.00
                if row['Depreciação Acumulada'] != None:
                    val_depreciacao_acum = decimal.Decimal(row['Depreciação Acumulada'])
                    val_depreciacao_acum = val_depreciacao_acum.quantize(decimal.Decimal(1).scaleb(-decimal_places),
                                                                         context=context)

                val_rel = 0.00
                if row['Valor Relatório'] != None:
                    val_rel = decimal.Decimal(row['Valor Relatório'])
                    val_rel = val_rel.quantize(decimal.Decimal(1).scaleb(-decimal_places),
                                                                         context=context)

                val_razao = 0.00
                if row['Valor Razão'] != None:
                    val_razao = decimal.Decimal(row['Valor Razão'])
                    val_razao = val_razao.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=Context(prec=12))

                val_aquisicao = 0.00
                if row['Valor aquisição'] != None:
                    val_aquisicao = decimal.Decimal(row['Valor aquisição'])
                    val_aquisicao = val_aquisicao.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=context)

                val_liq = 0.00
                if row['Valor Liquido'] != None:
                    val_liq = decimal.Decimal(row['Valor Liquido'])
                    val_liq = val_liq.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=context)

                taxa_depreciacao = 0.00
                if row['Taxa Depreciação'] != None:
                    taxa_depreciacao = decimal.Decimal(row['Taxa Depreciação'])
                    taxa_depreciacao = taxa_depreciacao.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=context)



                val_dif = 0.00
                if row['Diferença'] != None:
                    val_dif = decimal.Decimal(row['Diferença'])
                    val_dif = val_dif.quantize(decimal.Decimal(1).scaleb(-decimal_places), context=context)

                doc = Docs_Pac_Imobilizado_M1(
                    data_entrada=data_entrada,
                    plaqueta = row['Plaqueta'],
                    desc_imobilizado = row['Descrição Imobilizado'],
                    val_aquisicao = val_aquisicao,
                    num_doc = row['Nº Documento'],
                    nome_fornecedor = row['Nome Fornecedor'],
                    depreciacao_acum = val_depreciacao_acum,
                    val_liq = val_liq,
                    taxa_depreciacao = taxa_depreciacao,
                    val_rel = val_rel,
                    val_razao = val_razao,
                    val_dif = val_dif,
                    obs = row['Observação'],
                    cod_conta=Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                     cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo=obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 13:
            for index, row in df_conteudo_arqv.iterrows():
                data_lancto = None
                if row['Data Lançto'] != '':
                    if type(row['Data Lançto']) == str:
                        data_lancto = datetime.strptime(row['Data Lançto'], '%d/%m/%Y')
                    else:
                        data_lancto = row['Data Lançto']

                doc = Docs_Pac_Consorcio_Ativo_M1(
                    historico = row['Histórico'],
                    num_doc = row['Nº Documento'],
                    data_lancto = data_lancto,
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    obs = row['Observação'],
                    cod_conta = Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                       cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo = obj_arqv
                ).save()
        elif obj_pac_conta.cod_pacote_conta == 14:
            for index, row in df_conteudo_arqv.iterrows():
                data_lancto = None
                if row['Data Lançto'] != '':
                    if type(row['Data Lançto']) == str:
                        data_lancto = datetime.strptime(row['Data Lançto'], '%d/%m/%Y')
                    else:
                        data_lancto = row['Data Lançto']

                data_entrada = None
                if row['Data Entrada'] != '':
                    if type(row['Data Entrada']) == str:
                        data_entrada = datetime.strptime(row['Data Entrada'], '%d/%m/%Y')
                    else:
                        data_entrada = row['Data Entrada']

                doc = Docs_Demais_Contas_M1(
                    data_lancto = data_lancto,
                    data_entrada = data_entrada,
                    num_doc = row['Nº Documento'],
                    num_doc_contabil = row['Documento Contábil'],
                    val_rel = row['Valor Relatório'],
                    val_razao = row['Valor Razão'],
                    val_dif = row['Diferença'],
                    obs = row['Observação'],
                    historico = row['Histórico'],
                    cod_conta = Conta.objects.filter(Q(cod_red_conta_contabil_cp = row['Cód. Conta'])).first(),
                    cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                       cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                    cod_arquivo = obj_arqv
                ).save()

        msg = 'Arquivo importado com sucesso'
        '''except Exception as erro:
            obj_arqv.delete()
            traceback_str = traceback.format_exc()
            msg = f'Erro ao importar arquivo. Contate o desenvolvedor. Erro: {erro}!'
            print(traceback_str)'''

        dados = dict()
        dados = {
            'msg': msg
        }
        return JsonResponse(dados, safe=False)



class Form_Pesq_Arq_Contas_M1_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        competencia_form  = request.GET['competencia'] + '-01'
        tipo_pesquisa = request.GET['tipo_pesquisa']

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        obj_conta = Conta.objects.get(pk=cod_conta_form)
        obj_tab = None
        if tipo_pesquisa == 'D':
            data_ini_form = request.GET['data_ini']
            data_fim_form = request.GET['data_fim']
            lista_obj_reg_pesq = None
            if obj_conta.cod_pacote_conta.cod_pacote_conta in (3,9,10,13):
                lista_obj_reg_pesq = (Registros_Arqv_Docs_Contas_Modelo_1.objects
                           .filter(cod_arquivo__cod_conta=obj_conta,
                                   cod_arquivo__data_competencia=competencia_form,
                                   cod_lay_pac_camp__cod_campo__cod_campo=3,
                                   val_linha__range=[data_ini_form, data_fim_form]
                                   )
                           .order_by('cod_arquivo__cod_arquivo', 'num_linha', 'cod_lay_pac_camp__num_posicao_campo'))

            elif obj_conta.cod_pacote_conta.cod_pacote_conta in (6,7):
                lista_obj_reg_pesq = (Registros_Arqv_Docs_Contas_Modelo_1.objects
                           .filter(cod_arquivo__cod_conta=obj_conta,
                                   cod_arquivo__data_competencia=competencia_form,
                                   cod_lay_pac_camp__cod_campo__cod_campo=24,
                                   val_linha__range=[data_ini_form, data_fim_form]
                                   )
                           .order_by('cod_arquivo__cod_arquivo', 'num_linha', 'cod_lay_pac_camp__num_posicao_campo'))

            elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
                lista_obj_reg_pesq = (Registros_Arqv_Docs_Contas_Modelo_1.objects
                           .filter(cod_arquivo__cod_conta=obj_conta,
                                   cod_arquivo__data_competencia=competencia_form,
                                   cod_lay_pac_camp__cod_campo__cod_campo=25,
                                   val_linha__range=[data_ini_form, data_fim_form]
                                   )
                           .order_by('cod_arquivo__cod_arquivo', 'num_linha', 'cod_lay_pac_camp__num_posicao_campo'))
            elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
                lista_obj_reg_pesq = (Registros_Arqv_Docs_Contas_Modelo_1.objects
                           .filter(cod_arquivo__cod_conta=obj_conta,
                                   cod_arquivo__data_competencia=competencia_form,
                                   cod_lay_pac_camp__cod_campo__cod_campo=3
                                   )
                           .order_by('cod_arquivo__cod_arquivo', 'num_linha', 'cod_lay_pac_camp__num_posicao_campo'))
        elif tipo_pesquisa == 'T':
            txt_param_pesq_doc_m_1_form = request.GET['txt_param_pesq_doc_m_1']
            lista_obj_reg_pesq = (Registros_Arqv_Docs_Contas_Modelo_1.objects
                                  .filter(cod_arquivo__cod_conta=obj_conta,
                                          cod_arquivo__data_competencia=competencia_form,
                                          cod_lay_pac_camp__cod_campo__cod_campo=16,
                                          val_linha=txt_param_pesq_doc_m_1_form)
                                  .order_by('cod_arquivo__cod_arquivo', 'num_linha',
                                            'cod_lay_pac_camp__num_posicao_campo'))


        lista_linhas = []
        for obj_reg in lista_obj_reg_pesq:
            todas_colunas = (Registros_Arqv_Docs_Contas_Modelo_1.objects
                             .filter(cod_arquivo=obj_reg.cod_arquivo, num_linha=obj_reg.num_linha)
                             .order_by('cod_arquivo__cod_arquivo', 'num_linha',
                                            'cod_lay_pac_camp__num_posicao_campo'))
            num_linha = 1
            linha = []
            for reg in todas_colunas:
                if num_linha <= reg.cod_arquivo.qtd_reg_imp:
                    #linha[str(reg.cod_lay_pac_camp.cod_campo.desc_campo)] = reg.val_linha
                    valor_campo = reg.val_linha
                    if reg.cod_lay_pac_camp.cod_campo.cod_campo in (11, 12, 13, 20, 28, 30) and valor_campo != '':
                        valor_campo = locale.currency(round(float(valor_campo), 2), grouping=True, symbol=None)
                    elif reg.cod_lay_pac_camp.cod_campo.cod_campo in (3,9, 15, 24, 25) and valor_campo != '':
                        valor_campo = datetime.strptime(valor_campo, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                    linha.append(valor_campo)

                if reg.cod_lay_pac_camp.num_posicao_campo == reg.cod_lay_pac_camp.cod_layout.qtd_campos:
                    num_linha += 1
                    lista_linhas.append(linha)
                    linha = []

        dados = dict()
        dados = {
            'lista_linhas': lista_linhas
        }
        return JsonResponse(dados, safe=False)

class Form_Pesq_Arq_Pac_Contas_M1_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        competencia_form = request.GET['competencia'] + '-01'
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        obj_conta = Conta.objects.get(pk=cod_conta_form)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        '''Calcula valor do balancete da conta'''
        ultimo_dia_mes_calendar = calendar.monthrange(int(competencia_form.split('-')[0]),
                                                      int(competencia_form.split('-')[1]))[1]
        ultimo_dia_mes_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]),
                                       ultimo_dia_mes_calendar)
        primeiro_dia_ano = datetime(int(competencia_form.split('-')[0]), 1, 1)

        val_balancete = ConexaoBancoBenner() \
            .retorna_balancete_conta(obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa,
                                     obj_conta.handle_conta_contabil_cp,
                                     primeiro_dia_ano,
                                     ultimo_dia_mes_date)
        if val_balancete < 0:
            val_balancete = val_balancete * -1

        lista_docs = None
        resumo_docs = None
        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
            lista_docs = list(Docs_Pac_Contas_Pagar_Receber_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_contas_pagar_receber', 'cod_filial__desc_filial','data_lancto',
                                      'cnpj', 'nome_fornecedor', 'num_doc', 'num_ap', 'data_venc', 'num_parc',
                                      'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Contas_Pagar_Receber_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_contas_pagar_receber'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')
                if doc['data_venc'] != None:
                    doc['data_venc'] = datetime.strftime(doc['data_venc'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
            lista_docs = list(Docs_Pac_Estoque_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_estoque', 'cod_filial__desc_filial', 'nome_almoxarifado',
                                      'cod_produto', 'desc_produto', 'qtd_prod', 'custo_medio', 'val_rel','val_razao',
                                      'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Estoque_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_estoque'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['custo_medio'] != None:
                    doc['custo_medio'] = locale.currency(round(float(doc['custo_medio']), 2), grouping=True, symbol=None)

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
            lista_docs = list(Docs_Pac_Folha_Pag_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_folha_pag', 'cod_filial__desc_filial', 'matricula', 'historico',
                                      'num_doc', 'num_doc_contabil', 'data_lancto',  'val_rel', 'val_razao', 'val_dif',
                                      'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Folha_Pag_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_folha_pag'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
            lista_docs = list(Docs_Pac_Contas_Compensacao_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_contas_compensacao', 'cod_filial__desc_filial', 'historico', 'cnpj',
                                      'nome_fornecedor', 'num_doc', 'num_doc_contabil', 'data_emissao', 'data_entrada',
                                      'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Contas_Compensacao_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_contas_compensacao'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_emissao'] != None:
                    doc['data_emissao'] = datetime.strftime(doc['data_emissao'], '%d-%m-%Y')
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
            lista_docs = list(Docs_Pac_Tributos_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_tributos', 'cod_filial__desc_filial', 'historico', 'nome_fornecedor',
                                      'num_doc', 'num_doc_contabil', 'data_emissao', 'data_entrada',
                                      'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Tributos_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_tributos'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_emissao'] != None:
                    doc['data_emissao'] = datetime.strftime(doc['data_emissao'], '%d-%m-%Y')
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
            lista_docs = list(Docs_Pac_Finac_Disponib_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_financ_disp', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Finac_Disponib_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_financ_disp'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
            lista_docs = list(Docs_Pac_Intercompany_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_intercompany', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Intercompany_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_intercompany'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
            lista_docs = list(Docs_Pac_Imobilizado_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_imobilizado', 'data_entrada', 'cod_filial__desc_filial', 'plaqueta',
                                      'desc_imobilizado', 'val_aquisicao', 'num_doc', 'nome_fornecedor',
                                      'depreciacao_acum', 'val_liq', 'taxa_depreciacao', 'val_rel', 'val_razao',
                                      'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Imobilizado_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_imobilizado'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')
                if doc['val_aquisicao'] != None:
                    doc['val_aquisicao'] = locale.currency(round(float(doc['val_aquisicao']), 2), grouping=True,
                                                           symbol=None)
                if doc['depreciacao_acum'] != None:
                    doc['depreciacao_acum'] = locale.currency(round(float(doc['depreciacao_acum']), 2), grouping=True,
                                                           symbol=None)
                if doc['val_liq'] != None:
                    doc['val_liq'] = locale.currency(round(float(doc['val_liq']), 2), grouping=True,symbol=None)
                if doc['taxa_depreciacao'] != None:
                    doc['taxa_depreciacao'] = locale.currency(round(float(doc['taxa_depreciacao']), 2), grouping=True,
                                                              symbol=None)
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
            lista_docs = list(Docs_Pac_Consorcio_Ativo_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_consorcio_ativo', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))

            resumo_docs = list(Docs_Pac_Consorcio_Ativo_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_consorcio_ativo'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 14:
            lista_docs = list(Docs_Demais_Contas_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_outros', 'data_entrada', 'data_lancto', 'cod_filial__desc_filial',
                                      'historico', 'num_doc', 'num_doc_contabil', 'val_rel', 'val_razao', 'val_dif',
                                      'obs', 'ativo'))
            
            resumo_docs = list(Docs_Demais_Contas_M1.objects
                               .filter(cod_conta=obj_conta, ativo='S', cod_arquivo__data_competencia=competencia_form,
                                       cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                               .values('cod_conta__cod_conta')
                               .annotate(qtd_registros=Count('cod_pac_doc_outros'),
                                         tt_val_rel=Sum('val_rel'),
                                         tt_val_razao=Sum('val_razao'),
                                         tt_dif=Sum('val_dif')))

            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        if len(resumo_docs) > 0:
            for reg in resumo_docs:
                reg['val_balancete'] = locale.currency(round(float(val_balancete), 2), grouping=True,
                                                            symbol=None)
                val_composicao = 0
                '''Configura campos data e valores'''
                if reg['tt_val_rel'] != None:
                    if type(reg['tt_val_rel']) == str:
                        val_composicao = float(reg['tt_val_rel'].replace('.', '').replace(',', '.'))
                        if val_composicao < 0:
                            val_composicao = val_composicao * -1
                        reg['tt_val_rel'] = locale.currency(
                            round(float(val_composicao), 2), grouping=True,symbol=None)
                    else:
                        val_composicao = float(reg['tt_val_rel'])
                        if val_composicao < 0:
                            val_composicao = val_composicao * -1
                        reg['tt_val_rel'] = locale.currency(round(val_composicao, 2), grouping=True, symbol=None)

                if reg['tt_val_razao'] != None:
                    if type(reg['tt_val_razao']) == str:
                        val_razao = float(reg['tt_val_razao'].replace('.', '').replace(',', '.'))
                        if val_razao < 0:
                            val_razao = val_razao * -1
                        reg['tt_val_razao'] = locale.currency(round(val_razao, 2), grouping=True,symbol=None)
                    else:
                        val_razao = float(reg['tt_val_razao'])
                        if val_razao < 0:
                            val_razao = val_razao * -1
                        reg['tt_val_razao'] = locale.currency(round(val_razao, 2), grouping=True,
                                                              symbol=None)
                if reg['tt_dif'] != None:
                    if type(reg['tt_dif']) == str:
                        reg['tt_dif'] = locale.currency(
                            round(float(reg['tt_dif'].replace('.', '').replace(',', '.')), 2), grouping=True,
                            symbol=None)
                    else:
                        reg['tt_dif'] = locale.currency(round(float(reg['tt_dif']), 2), grouping=True,
                                                        symbol=None)

                val_dif_comp_bal = 0
                val_dif_comp_bal = val_balancete - val_composicao
                reg['val_dif_comp_bal'] = locale.currency(round(float(val_dif_comp_bal), 2), grouping=True,
                                                        symbol=None)



        dados = dict()
        dados = {
            'lista_docs': lista_docs,
            'resumo_docs': resumo_docs
        }
        return JsonResponse(dados, safe=False)

class Tabela_Doc_Contas_Modelo_1_View(View):
    def get_object(self, pk):
        try:
            return Arquivo_Docs_Pac_Contas_Modelo_1.objects.get(pk=pk)
        except Arquivo_Docs_Pac_Contas_Modelo_1.DoesNotExists:
            return Http404


    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        competencia_form = request.GET['competencia']
        obj_conta = Conta.objects.get(pk=cod_conta_form)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        registros_tabela = []
        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
            registros_tabela = list(Docs_Pac_Contas_Pagar_Receber_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_contas_pagar_receber'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 3


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
            registros_tabela = list(Docs_Pac_Estoque_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_estoque'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 4


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
            registros_tabela = list(Docs_Pac_Folha_Pag_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_folha_pag'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 5


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
            registros_tabela = list(Docs_Pac_Contas_Compensacao_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_contas_compensacao'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 6


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
            registros_tabela = list(Docs_Pac_Tributos_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_tributos'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 7


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
            registros_tabela = list(Docs_Pac_Finac_Disponib_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_financ_disp'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 9


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
            registros_tabela = list(Docs_Pac_Intercompany_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_intercompany'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 10


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
            registros_tabela = list(Docs_Pac_Imobilizado_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_imobilizado'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 11


        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
            registros_tabela = list(Docs_Pac_Consorcio_Ativo_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_consorcio_ativo'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 13

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 14:
            registros_tabela = list(Docs_Demais_Contas_M1.objects
                                    .filter(cod_conta=obj_conta, ativo='S',
                                            cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp', 'cod_conta__cod_conta',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_outros'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao'),
                                        tt_dif=Sum('val_dif')))
            for arq in registros_tabela:
                arq['pacote'] = 14


        if len(registros_tabela) > 0:
            for reg in registros_tabela:

                '''Configura campos data e valores'''
                if reg['tt_val_rel'] != None:
                    if type(reg['tt_val_rel']) == str:
                        reg['tt_val_rel'] = locale.currency(round(float(reg['tt_val_rel'].replace('.','').replace(',','.')), 2), grouping=True,
                                                            symbol=None)
                    else:
                        reg['tt_val_rel'] = locale.currency(round(float(reg['tt_val_rel']), 2), grouping=True, symbol=None)
                if reg['tt_val_razao'] != None:
                    if type(reg['tt_val_razao']) == str:
                        reg['tt_val_razao'] = locale.currency(
                            round(float(reg['tt_val_razao'].replace('.', '').replace(',', '.')), 2), grouping=True,
                            symbol=None)
                    else:
                        reg['tt_val_razao'] = locale.currency(round(float(reg['tt_val_razao']), 2), grouping=True,
                                                          symbol=None)
                if reg['tt_dif'] != None:
                    if type(arq['tt_dif']) == str:
                        reg['tt_dif'] = locale.currency(
                            round(float(reg['tt_dif'].replace('.', '').replace(',', '.')), 2), grouping=True,
                            symbol=None)
                    else:
                        reg['tt_dif'] = locale.currency(round(float(reg['tt_dif']), 2), grouping=True,
                                                          symbol=None)
                if reg['cod_arquivo__data_imp'] != None:
                    if type(reg['cod_arquivo__data_imp']) == str:
                        reg['cod_arquivo__data_imp'] = datetime.strftime(datetime.strptime(reg['cod_arquivo__data_imp'], '%d-%m-%Y'), '%d-%m-%Y')
                    else:
                        reg['cod_arquivo__data_imp'] = datetime.strftime(reg['cod_arquivo__data_imp'], '%d-%m-%Y')

                if reg['cod_arquivo__data_competencia'] != None:
                    if type(reg['cod_arquivo__data_competencia']) == str:
                        reg['cod_arquivo__data_competencia'] = datetime.strftime(datetime.strptime(reg['cod_arquivo__data_competencia'], '%m-%Y'), '%m-%Y')
                    else:

                        reg['cod_arquivo__data_competencia'] = datetime.strftime(reg['cod_arquivo__data_competencia'], '%m-%Y')


        lista_registros_tabela = []
        if competencia_form != 'todas':
            competencia_form = competencia_form.split('-')[1] + '-' + competencia_form.split('-')[0]
            for reg in registros_tabela:
                if reg['cod_arquivo__data_competencia'] == competencia_form:
                    lista_registros_tabela.append(reg)

        else:
            lista_registros_tabela = registros_tabela



        dados = {
            'registros_tabela': lista_registros_tabela,
        }
        return render(request, 'contabil_composicao_app/frm_resumo_arq_lista_docs_m1.html', dados)

    def delete(self, request, pk):
        obj_arquivo = self.get_object(pk.split('_')[0])
        obj_conta = Conta.objects.get(pk=pk.split('_')[1])
        motivo_frm = pk.split('_')[2]
        cod_pacote = obj_conta.cod_pacote_conta.cod_pacote_conta

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')
        msg = ''
        if cod_pacote == 3:
            docs = Docs_Pac_Contas_Pagar_Receber_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                                + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 4:
            docs = Docs_Pac_Estoque_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 5:
            docs = Docs_Pac_Folha_Pag_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 6:
            docs = Docs_Pac_Contas_Compensacao_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 7:
            docs = Docs_Pac_Tributos_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 9:
            docs = Docs_Pac_Finac_Disponib_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 10:
            docs = Docs_Pac_Intercompany_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 11:
            docs = Docs_Pac_Imobilizado_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 13:
            docs = Docs_Pac_Consorcio_Ativo_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'

        elif cod_pacote == 14:
            docs = Docs_Demais_Contas_M1.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.ativo = 'N'
                doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                            + data_hora_atual_h_m_y)
                doc.save()
            msg = 'Registros inativados com sucesso!'


        data = dict()
        data = {
            'cod_conta': obj_conta.cod_conta,
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Form_Composicao_Auditoria_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        # lista_contas_benner = ConexaoBancoBenner().retorna_dados_contas()
        '''lista_contas_modelo_1 = (Auditoria_Status_Composicao_Competencia.objects.filter(tipo_prazo='m1')
                                 .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                         'cod_conta__cod_red_conta_contabil_cp', 'cod_conta__cod_red_conta_contabil_lp'))'''
        contexto = {
            #'lista_contas_modelo_1': lista_contas_modelo_1,
            'desc_menu': 'Composição Auditoria',
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'contabil_composicao_app/form_composicao_auditoria.html',
                      contexto)

class Form_Vincula_Resp_Contas_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_pacotes = Pacote_Conta.objects.all()

        lista_usuarios_contabil = (Usuario.objects
                                   .filter(sala='CON',
                                           cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))

        contexto = {
            'lista_pacotes': lista_pacotes,
            'lista_usuarios_contabil': lista_usuarios_contabil,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'contabil_composicao_app/form_vincula_resp_contas.html', contexto)


    def post(self, request):
        lista_nome_responsavel_frm = request.POST['lista_nome_responsavel']
        lista_cod_contas_frm = request.POST['lista_cod_contas']
        dt_fim_atividade_frm = request.POST['dt_fim_atividade']
        msg = ''
        try:
            lista_resp = (Responsaveis_Conta.objects
                                .filter((Q(resp_composicao__in=lista_nome_responsavel_frm.split(',')) |
                                         Q(resp_validacao__in=lista_nome_responsavel_frm.split(','))),
                                        data_fim_atividade__isnull=True,
                                        cod_conta__cod_conta__in=lista_cod_contas_frm.split(',')))
            for reg in lista_resp:
                reg.data_fim_atividade = dt_fim_atividade_frm
                reg.save()
            msg = 'Contas desativadas com sucesso!'
        except Exception as e:
            msg = f'Algo interrompeu o processo. Conta o Adm. {e}'

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)



class Importa_Anexos_Contas_View(View):
    def post(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        nome_pasta_empresa = 'Conlog_Anexos_Pendentes'
        if obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa == 17:
            nome_pasta_empresa = 'Deep_Anexos_Pendentes'

        #diretorio_arquivos_postados = f'media\\docs\\contabil_composicao_app\\anexos_pendentes_importacao\\{nome_pasta_empresa}'
                                      #f'media/docs/contabil_composicao_app/anexos_pendentes_importacao/{nome_pasta_empresa}/'
        diretorio_arquivos_postados = os.path.join(BASE_DIR, f'media\\docs\\contabil_composicao_app\\anexos_pendentes_importacao\\{nome_pasta_empresa}\\')
        lista_todos_arquivos = os.listdir(diretorio_arquivos_postados)
        qtd_arquivos_postados = 0
        lista_arquivos = []
        for arq in lista_todos_arquivos:
            if '.pdf' in arq or '.PDF' in arq:
                lista_arquivos.append(arq)
                qtd_arquivos_postados += 1
        #qtd_arquivos_postados = len(lista_arquivos)

        msg = ''
        for arq in lista_arquivos:
            #caminho_arq = f'media/docs/contabil_composicao_app/anexos_pendentes_importacao/' + arq
            caminho_arq = diretorio_arquivos_postados + arq
            #cod_conta = arq.split('_')[0]
            cod_red_conta_contabil = arq.split('_')[0]
            cod_contrato = arq.split('_')[1]
            competencia_str = arq.split('_')[3] + '-' + arq.split('_')[2]
            competencia_str_dt = arq.split('_')[3] + '-' + arq.split('_')[2] + '-01'
            ordem_arq = 0
            desc_arq = ''
            if len(arq.split('_')) == 5:
                ordem_arq = arq.split('_')[4].split('.')[0]
            elif len(arq.split('_')) > 5:
                ordem_arq = arq.split('_')[4]
                desc_arq = arq.split('_')[5].split('.')[0]

            #obj_conta = Conta.objects.get(pk=cod_conta)
            obj_conta = Conta.objects.filter(
                (Q(cod_red_conta_contabil_cp=cod_red_conta_contabil) | Q(cod_red_conta_contabil_lp=cod_red_conta_contabil))).first()
            obj_contrato = None
            cod_contrato_param = ''
            eh_arquivo_principal_comp = 'N'
            if obj_conta.tipo_modelo == 1:
                cod_contrato_param = cod_contrato
                if ordem_arq == '1':
                    eh_arquivo_principal_comp = 'S'
                    '''obj_anexo_principal_da_conta = (Anexos_Contrato.objects
                                                    .filter(cod_conta=obj_conta,
                                                            data_competencia=competencia_str_dt,
                                                            eh_anexo_principal_competencia='S')).first()
                    if obj_anexo_principal_da_conta != None:
                        obj_anexo_principal_da_conta.eh_anexo_principal_competencia='N'
                        obj_anexo_principal_da_conta.save()'''
            else:
                obj_contrato = (Contrato.objects
                                .filter(cod_conta=obj_conta, num_contrato=cod_contrato,
                                        cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa).first())
                cod_contrato_param = obj_contrato.cod_contrato
                if ordem_arq == '1':
                    eh_arquivo_principal_comp = 'S'
                    obj_anexo_principal_da_conta = (Anexos_Contrato.objects
                                                    .filter(cod_conta=obj_conta,
                                                            cod_contrato=obj_contrato,
                                                            data_competencia=competencia_str_dt,
                                                            eh_anexo_principal_competencia='S')).first()
                    '''if obj_anexo_principal_da_conta != None:
                        obj_anexo_principal_da_conta.eh_anexo_principal_competencia = 'N'
                        obj_anexo_principal_da_conta.save()'''
            obj_form_anexos_conta_view = Form_Anexos_Conta_View()

            msg = obj_form_anexos_conta_view.anexa_arq_conta(obj_usuario_sessao,obj_conta, cod_contrato_param,
                                                             competencia_str,caminho_arq, arq,
                                                             eh_arquivo_principal_comp,desc_arq)
            #os.remove(os.path.join(diretorio_arquivos_postados, arq))


        lista_arquivos_depois_imp = os.listdir(diretorio_arquivos_postados)
        qtd_arquivos_postados_depois_imp = len(lista_arquivos_depois_imp)


        data = dict()
        data = {
            'msg': msg,
            'qtd_arquivos_postados': qtd_arquivos_postados_depois_imp
        }
        return JsonResponse(data, safe=False)

class Form_Doc_Pac_Modelo_1_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        dic_pacotes = Pacote_Conta.objects.filter(cod_modelo=1)
        lista_filiais = Filial.objects.filter(cod_empresa=obj_usu.cod_filial.cod_empresa, cod_reduzido__isnull=False)
        contexto = {
            'dic_pacotes': dic_pacotes,
            'lista_filiais': lista_filiais,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'contabil_composicao_app/form_importa_arquivo_por_pac_modelo_1.html', contexto)

class Comp_Cb_Contas_Imp_Docs_Pac_M1_View(View):
    def get(self, request):
        cod_pacote_form = request.GET['cod_pacote_conta']
        obj_pac = Pacote_Conta.objects.get(pk=cod_pacote_form)
        lista_contas = list(Conta.objects.filter(cod_pacote_conta=obj_pac)
                        .values('cod_conta', 'desc_conta','cod_red_conta_contabil_cp', 'cod_red_conta_contabil_lp'))
        data = dict()
        data = {
            'lista_contas': lista_contas
        }
        return JsonResponse(data, safe=False)

class Form_Atualiza_Contratos_Benner_View(View):
    def post(self, request):
        lista_cod_contas = request.POST['lista_cod_contas']
        data_corte_frm = request.POST['data_corte']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_parcelas_atualizadas_form = []
        for cod_conta in lista_cod_contas.split(','):
            obj_conta = Conta.objects.get(pk=cod_conta)
            lista_contratos_para_atualizar = (Parcela_Contrato.objects
                                                 .filter(data_liquidacao__isnull=True,
                                                         cod_contrato__cod_conta=obj_conta,
                                                         cod_contrato__sincronizar_benner='S',
                                                         cod_contrato__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                              .values('cod_contrato__num_contrato').distinct())



            for contrato in lista_contratos_para_atualizar:
                lista_parcelas_atualizadas = Form_Imp_Contratos_Conta_View().atualiza_dados_contratos_parcelas(
                    obj_conta.cod_conta, contrato['cod_contrato__num_contrato'],'C',
                    obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa,obj_usuario_sessao )[2]
                for parc in lista_parcelas_atualizadas:
                    val_pago = 0.00
                    if parc.val_corrigido != None:
                        val_pago = locale.currency(round(parc.val_corrigido, 2), grouping=True, symbol=None)

                    val_principal = 0.00
                    if parc.val_principal != None:
                        val_principal = locale.currency(round(parc.val_principal, 2), grouping=True, symbol=None)

                    val_taxas = 0.00
                    if parc.val_taxas != None:
                        val_taxas = locale.currency(round(parc.val_taxas, 2), grouping=True, symbol=None)

                    val_fundo = 0.00
                    if parc.val_fundo != None:
                        val_fundo = locale.currency(round(parc.val_fundo, 2), grouping=True, symbol=None)

                    data_liquidacao = 0.00
                    if parc.data_liquidacao != None:
                        data_liquidacao = (datetime.strptime(parc.data_liquidacao, '%Y-%m-%d')
                                           .strftime('%d-%m-%Y'))

                    reg_parc = {
                        'cod_conta': parc.cod_contrato.cod_conta.cod_conta,
                        'desc_conta': parc.cod_contrato.cod_conta.desc_conta,
                        'num_contrato': parc.cod_contrato.num_contrato,
                        'num_parcela': parc.ordem_parcela,
                        'val_pago': val_pago,
                        'val_principal': val_principal,
                        'val_taxas': val_taxas,
                        'val_fundo': val_fundo,
                        'data_vencimento': datetime.strptime(parc.data_vencimento, '%Y-%m-%d')\
                            .strftime('%d-%m-%Y'),
                        'data_liquidacao': data_liquidacao,
                        'handle_parcela': parc.handle_parcela
                    }
                    lista_parcelas_atualizadas_form.append(reg_parc)
                '''
                lista_parcelas_atualizados.append(reg_contrato)'''
        data = dict()
        data = {
            'lista_parcelas_atualizados': lista_parcelas_atualizadas_form
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Contas_Pagar_Receber_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Pac_Contas_Pagar_Receber_M1.objects.get(pk=pk)
        except Docs_Pac_Contas_Pagar_Receber_M1.DoesNotExists:
            return Http404

    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Contas_Pagar_Receber_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        cod_red_fil = 'Não vinculada'
        if obj_doc.cod_filial != None:
            cod_red_fil = obj_doc.cod_filial.cod_reduzido


        doc_dic = {
            'cod_red_fil': cod_red_fil,
            'cnpj_fornec': obj_doc.cnpj,
            'nome_fornec': obj_doc.nome_fornecedor,
            'num_doc': obj_doc.num_doc,
            'num_ap': obj_doc.num_ap,
            'data_lancto': obj_doc.data_lancto,
            'data_venc': obj_doc.data_venc,
            'num_parc': obj_doc.num_parc,
            'val_rel': locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'obs': obj_doc.obs,
            'cod_pac_doc_contas_pagar_receber': obj_doc.cod_pac_doc_contas_pagar_receber
        }
        data = dict()
        data = {
            'doc_dic': doc_dic,
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        cnpj_fornec_frm = request.POST['cnpj_fornec']
        nome_fornec_frm = request.POST['nome_fornec']
        num_doc_frm = request.POST['num_doc']
        num_ap_frm = request.POST['num_ap']
        data_lancto_frm = request.POST['data_lancto']
        data_venc_frm = request.POST['data_venc']
        num_parc_frm = request.POST['num_parc']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        data_lancto = None
        if data_lancto_frm != '':
            data_lancto = data_lancto_frm

        data_venc = None
        if data_venc_frm != '':
            data_venc = data_venc_frm

        obj_doc = Docs_Pac_Contas_Pagar_Receber_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.data_lancto = data_lancto
        obj_doc.cnpj = cnpj_fornec_frm
        obj_doc.nome_fornecedor = nome_fornec_frm
        obj_doc.num_doc = num_doc_frm
        obj_doc.num_ap = num_ap_frm
        obj_doc.num_parc = num_parc_frm
        obj_doc.data_venc = data_venc
        obj_doc.val_rel = val_rel_frm
        obj_doc.val_razao = val_razao_frm
        obj_doc.val_dif = val_dif_frm
        obj_doc.obs = obs_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Estoque_M1_View(View):

    def get_object(self, pk):
        try:
            return Docs_Pac_Estoque_M1.objects.get(pk=pk)
        except Docs_Pac_Estoque_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Estoque_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'nome_almoxarifado': obj_doc.nome_almoxarifado,
            'cod_produto': obj_doc.cod_produto,
            'desc_produto': obj_doc.desc_produto,
            'qtd_prod': obj_doc.qtd_prod,
            'custo_medio': locale.currency(round(obj_doc.custo_medio, 2), grouping=True, symbol=None),
            'val_rel': locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'obs': obj_doc.obs,
            'cod_pac_doc_estoque': obj_doc.cod_pac_doc_estoque
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        nome_almoxarifado_frm = request.POST['nome_almoxarifado']
        cod_prod_frm = request.POST['cod_prod']
        desc_prod_frm = request.POST['desc_prod']
        qtd_frm = request.POST['qtd']
        custo_medio_frm = request.POST['custo_medio']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Estoque_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.nome_almoxarifado = nome_almoxarifado_frm
        obj_doc.cod_produto = cod_prod_frm
        obj_doc.desc_produto = desc_prod_frm
        obj_doc.qtd_prod = qtd_frm
        obj_doc.custo_medio = custo_medio_frm
        obj_doc.val_rel = val_rel_frm
        obj_doc.val_razao = val_razao_frm
        obj_doc.val_dif = val_dif_frm
        obj_doc.obs = obs_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Folha_Pag_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Pac_Folha_Pag_M1.objects.get(pk=pk)
        except Docs_Pac_Estoque_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Folha_Pag_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_lancto': obj_doc.data_lancto,
            'matricula': obj_doc.matricula,
            'historico': obj_doc.historico,
            'num_doc': obj_doc.num_doc,
            'num_doc_contabil': obj_doc.num_doc_contabil,
            'val_rel': locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'obs': obj_doc.obs,
            'cod_pac_doc_folha_pag': obj_doc.cod_pac_doc_folha_pag
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        matricula_frm = request.POST['matricula']
        historico_frm = request.POST['historico']
        num_doc_frm = request.POST['num_doc']
        num_doc_contabil_frm = request.POST['num_doc_contabil']
        data_lancto_frm = request.POST['data_lancto']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Folha_Pag_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.matricula = matricula_frm
        obj_doc.historico = historico_frm
        obj_doc.num_doc = num_doc_frm
        obj_doc.num_doc_contabil = num_doc_contabil_frm
        obj_doc.data_lancto = data_lancto_frm
        obj_doc.val_rel = val_rel_frm
        obj_doc.val_razao = val_razao_frm
        obj_doc.val_dif = val_dif_frm
        obj_doc.obs = obs_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)


    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Contas_Compensacao_M1_View(View):

    def get_object(self, pk):
        try:
            return Docs_Pac_Contas_Compensacao_M1.objects.get(pk=pk)
        except Docs_Pac_Contas_Compensacao_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Contas_Compensacao_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_emissao': obj_doc.data_emissao,
            'data_entrada': obj_doc.data_entrada,
            'cnpj': obj_doc.cnpj,
            'nome_fornecedor': obj_doc.nome_fornecedor,
            'num_doc': obj_doc.num_doc,
            'num_doc_contabil': obj_doc.num_doc_contabil,
            'val_rel': obj_doc.val_rel, # locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': obj_doc.val_razao, # locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': obj_doc.val_dif, #locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'historico': obj_doc.historico,
            'obs': obj_doc.obs,
            'cod_pac_doc_contas_compensacao': obj_doc.cod_pac_doc_contas_compensacao
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)



    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        data_emissao_frm = request.POST['data_emissao']
        data_entrada_frm = request.POST['data_entrada']
        cnpj_frm = request.POST['cnpj']
        nome_fornecedor_frm = request.POST['nome_fornecedor']
        num_doc_frm = request.POST['num_doc']
        num_doc_contabil_frm = request.POST['num_doc_contabil']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']
        historico_frm = request.POST['historico']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Contas_Compensacao_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.data_emissao = data_emissao_frm
        obj_doc.data_entrada = data_entrada_frm
        obj_doc.cnpj = cnpj_frm
        obj_doc.nome_fornecedor = nome_fornecedor_frm
        obj_doc.num_doc = num_doc_frm
        obj_doc.num_doc_contabil = num_doc_contabil_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.obs = obs_frm
        obj_doc.historico = historico_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)


    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Tributos_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Pac_Tributos_M1.objects.get(pk=pk)
        except Docs_Pac_Tributos_M1.DoesNotExists:
            return Http404

    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Tributos_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_emissao': obj_doc.data_emissao,
            'data_entrada': obj_doc.data_entrada,
            'nome_fornecedor': obj_doc.nome_fornecedor,
            'num_doc': obj_doc.num_doc,
            'num_doc_contabil': obj_doc.num_doc_contabil,
            'val_rel': obj_doc.val_rel, # locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': obj_doc.val_razao, # locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': obj_doc.val_dif, #locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'historico': obj_doc.historico,
            'obs': obj_doc.obs,
            'cod_pac_doc_tributos': obj_doc.cod_pac_doc_tributos
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        data_emissao_frm = request.POST['data_emissao']
        data_entrada_frm = request.POST['data_entrada']
        nome_fornecedor_frm = request.POST['nome_fornecedor']
        num_doc_frm = request.POST['num_doc']
        num_doc_contabil_frm = request.POST['num_doc_contabil']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']
        historico_frm = request.POST['historico']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Tributos_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.data_emissao = data_emissao_frm
        obj_doc.data_entrada = data_entrada_frm
        obj_doc.nome_fornecedor = nome_fornecedor_frm
        obj_doc.num_doc = num_doc_frm
        obj_doc.num_doc_contabil = num_doc_contabil_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.obs = obs_frm
        obj_doc.historico = historico_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Finac_Disponib_M1_View(View):

    def get_object(self, pk):
        try:
            return Docs_Pac_Finac_Disponib_M1.objects.get(pk=pk)
        except Docs_Pac_Finac_Disponib_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Finac_Disponib_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_lancto': obj_doc.data_lancto,
            'num_doc': obj_doc.num_doc,
            'val_rel': obj_doc.val_rel,  # locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': obj_doc.val_razao,  # locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': obj_doc.val_dif,  # locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'historico': obj_doc.historico,
            'obs': obj_doc.obs,
            'cod_pac_doc_financ_disp': obj_doc.cod_pac_doc_financ_disp
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)
    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        data_lancto_frm = request.POST['data_lancto']
        num_doc_frm = request.POST['num_doc']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']
        historico_frm = request.POST['historico']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Finac_Disponib_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.data_lancto = data_lancto_frm
        obj_doc.num_doc = num_doc_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.obs = obs_frm
        obj_doc.historico = historico_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)
    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Intercompany_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Pac_Intercompany_M1.objects.get(pk=pk)
        except Docs_Pac_Intercompany_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Intercompany_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_lancto': obj_doc.data_lancto,
            'num_doc': obj_doc.num_doc,
            'val_rel': obj_doc.val_rel,  # locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': obj_doc.val_razao,  # locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': obj_doc.val_dif,  # locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'historico': obj_doc.historico,
            'obs': obj_doc.obs,
            'cod_pac_doc_intercompany': obj_doc.cod_pac_doc_intercompany
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)
    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        data_lancto_frm = request.POST['data_lancto']
        num_doc_frm = request.POST['num_doc']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']
        historico_frm = request.POST['historico']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Intercompany_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.data_lancto = data_lancto_frm
        obj_doc.num_doc = num_doc_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.obs = obs_frm
        obj_doc.historico = historico_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)
    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Imobilizado_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Pac_Imobilizado_M1.objects.get(pk=pk)
        except Docs_Pac_Imobilizado_M1.DoesNotExists:
            return Http404

    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Imobilizado_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_entrada': obj_doc.data_entrada,
            'plaqueta': obj_doc.plaqueta,
            'desc_imobilizado': obj_doc.desc_imobilizado,
            'val_aquisicao': locale.currency(round(obj_doc.val_aquisicao, 2), grouping=True, symbol=None),
            'num_doc': obj_doc.num_doc,
            'nome_fornecedor': obj_doc.nome_fornecedor,
            'depreciacao_acum': locale.currency(round(obj_doc.depreciacao_acum, 2), grouping=True, symbol=None),
            'val_liq': locale.currency(round(obj_doc.val_liq, 2), grouping=True, symbol=None),
            'taxa_depreciacao': locale.currency(round(obj_doc.taxa_depreciacao, 2), grouping=True, symbol=None),
            'val_rel': locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'obs': obj_doc.obs,
            'cod_pac_doc_imobilizado': obj_doc.cod_pac_doc_imobilizado
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        plaqueta_frm = request.POST['plaqueta']
        desc_imobilizado_frm = request.POST['desc_imobilizado']
        val_aquisicao_frm = request.POST['val_aquisicao']
        num_doc_frm = request.POST['num_doc']
        nome_fornec_frm = request.POST['nome_fornec']
        data_entrada_frm = request.POST['data_entrada']
        deprec_acum_frm = request.POST['deprec_acum']
        val_liq_frm = request.POST['val_liq']
        taxa_deprec_frm = request.POST['taxa_deprec']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Imobilizado_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.plaqueta = plaqueta_frm
        obj_doc.desc_imobilizado = desc_imobilizado_frm
        obj_doc.val_aquisicao = val_aquisicao_frm.replace('.', '').replace(',', '.')
        obj_doc.num_doc = num_doc_frm
        obj_doc.nome_fornecedor = nome_fornec_frm
        obj_doc.depreciacao_acum = deprec_acum_frm.replace('.', '').replace(',', '.')
        obj_doc.val_liq = val_liq_frm.replace('.', '').replace(',', '.')
        obj_doc.taxa_depreciacao = taxa_deprec_frm.replace('.', '').replace(',', '.')
        obj_doc.data_entrada = data_entrada_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.obs = obs_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)


    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Pac_Consorcio_Ativo_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Pac_Consorcio_Ativo_M1.objects.get(pk=pk)
        except Docs_Pac_Consorcio_Ativo_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Pac_Consorcio_Ativo_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'num_doc': obj_doc.num_doc,
            'data_lancto': obj_doc.data_lancto,
            'val_rel': locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'historico': obj_doc.historico,
            'obs': obj_doc.obs,
            'cod_pac_doc_consorcio_ativo': obj_doc.cod_pac_doc_consorcio_ativo
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)
    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        data_lancto_frm = request.POST['data_lancto']
        num_doc_frm = request.POST['num_doc']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']
        historico_frm = request.POST['historico']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Pac_Consorcio_Ativo_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.num_doc = num_doc_frm
        obj_doc.data_lancto = data_lancto_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.historico = historico_frm
        obj_doc.obs = obs_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)
    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Docs_Demais_Contas_M1_View(View):
    def get_object(self, pk):
        try:
            return Docs_Demais_Contas_M1.objects.get(pk=pk)
        except Docs_Demais_Contas_M1.DoesNotExists:
            return Http404
    def get(self, request):
        cod_doc_frm = request.GET['cod_doc']
        obj_doc = Docs_Demais_Contas_M1.objects.get(pk=cod_doc_frm)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        doc_dic = {
            'cod_red_fil': obj_doc.cod_filial.cod_reduzido,
            'data_entrada': obj_doc.data_entrada,
            'data_lancto': obj_doc.data_lancto,
            'historico': obj_doc.historico,
            'num_doc': obj_doc.num_doc,
            'num_doc_contabil': obj_doc.num_doc_contabil,
            'val_rel': locale.currency(round(obj_doc.val_rel, 2), grouping=True, symbol=None),
            'val_razao': locale.currency(round(obj_doc.val_razao, 2), grouping=True, symbol=None),
            'val_dif': locale.currency(round(obj_doc.val_dif, 2), grouping=True, symbol=None),
            'obs': obj_doc.obs,
            'cod_pac_doc_outros': obj_doc.cod_pac_doc_outros
        }
        data = dict()
        data = {
            'doc_dic': doc_dic
        }
        return JsonResponse(data, safe=False)
    def post(self, request):
        let_cod_doc_frm = request.POST['let_cod_doc']
        cod_red_fil_frm = request.POST['cod_red_fil']
        data_lancto_frm = request.POST['data_lancto']
        data_entrada_frm = request.POST['data_entrada']
        num_doc_frm = request.POST['num_doc']
        num_doc_contabil_frm = request.POST['num_doc_contabil']
        val_rel_frm = request.POST['val_rel']
        val_razao_frm = request.POST['val_razao']
        val_dif_frm = request.POST['val_dif']
        obs_frm = request.POST['obs']
        historico_frm = request.POST['historico']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        obj_filial = (Filial.objects
                      .filter(cod_reduzido=cod_red_fil_frm, cod_empresa=obj_usu.cod_filial.cod_empresa)
                      .first())

        obj_doc = Docs_Demais_Contas_M1.objects.get(pk=let_cod_doc_frm)
        obj_doc.num_doc = num_doc_frm
        obj_doc.num_doc_contabil = num_doc_contabil_frm
        obj_doc.data_entrada = data_entrada_frm
        obj_doc.data_lancto = data_lancto_frm
        obj_doc.val_rel = val_rel_frm.replace('.', '').replace(',', '.')
        obj_doc.val_razao = val_razao_frm.replace('.', '').replace(',', '.')
        obj_doc.val_dif = val_dif_frm.replace('.', '').replace(',', '.')
        obj_doc.historico = historico_frm
        obj_doc.obs = obs_frm
        obj_doc.cod_filial = obj_filial
        obj_doc.save()

        data = dict()
        data = {
            'msg': 'Doc alterado com sucesso!'
        }
        return JsonResponse(data, safe=False)
    def delete(self, request, pk):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%d/%m/%Y')

        obj_doc = self.get_object(pk.split('_')[0])
        obj_doc.obs += (' / desativação:' + pk.split('_')[1] + ', por: ' + obj_usu.login_usu + ', em: '
                        + data_hora_atual_h_m_y)
        obj_doc.ativo = 'N'
        obj_doc.save()
        msg = 'Registro inativado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)

class Form_Docs_Conta_M1_View(View):
    def get(self, request):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        cod_arq_frm = request.GET['cod_arq']
        cod_conta_frm = request.GET['cod_conta']

        obj_arq = Arquivo_Docs_Pac_Contas_Modelo_1.objects.get(pk=cod_arq_frm)
        obj_conta = Conta.objects.get(pk=cod_conta_frm)

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_docs = None
        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
            lista_docs = list(Docs_Pac_Contas_Pagar_Receber_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_contas_pagar_receber', 'cod_filial__desc_filial', 'data_lancto',
                                      'cnpj', 'nome_fornecedor', 'num_doc', 'num_ap', 'data_venc', 'num_parc',
                                      'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')
                if doc['data_venc'] != None:
                    doc['data_venc'] = datetime.strftime(doc['data_venc'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
            lista_docs = list(Docs_Pac_Estoque_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_estoque', 'cod_filial__desc_filial', 'nome_almoxarifado',
                                      'cod_produto', 'desc_produto', 'qtd_prod', 'custo_medio', 'val_rel', 'val_razao',
                                      'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['custo_medio'] != None:
                    doc['custo_medio'] = locale.currency(round(float(doc['custo_medio']), 2), grouping=True,
                                                         symbol=None)

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
            lista_docs = list(Docs_Pac_Folha_Pag_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_folha_pag', 'cod_filial__desc_filial', 'matricula', 'historico',
                                      'num_doc', 'num_doc_contabil', 'data_lancto', 'val_rel', 'val_razao', 'val_dif',
                                      'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
            lista_docs = list(Docs_Pac_Contas_Compensacao_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_contas_compensacao', 'cod_filial__desc_filial', 'historico', 'cnpj',
                                      'nome_fornecedor', 'num_doc', 'num_doc_contabil', 'data_emissao', 'data_entrada',
                                      'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_emissao'] != None:
                    doc['data_emissao'] = datetime.strftime(doc['data_emissao'], '%d-%m-%Y')
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
            lista_docs = list(Docs_Pac_Tributos_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_tributos', 'cod_filial__desc_filial', 'historico', 'nome_fornecedor',
                                      'num_doc', 'num_doc_contabil', 'data_emissao', 'data_entrada',
                                      'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_emissao'] != None:
                    doc['data_emissao'] = datetime.strftime(doc['data_emissao'], '%d-%m-%Y')
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
            lista_docs = list(Docs_Pac_Finac_Disponib_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_financ_disp', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
            lista_docs = list(Docs_Pac_Intercompany_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_intercompany', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
            lista_docs = list(Docs_Pac_Imobilizado_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_imobilizado', 'data_entrada', 'cod_filial__desc_filial', 'plaqueta',
                                      'desc_imobilizado', 'val_aquisicao', 'num_doc', 'nome_fornecedor',
                                      'depreciacao_acum', 'val_liq', 'taxa_depreciacao', 'val_rel', 'val_razao',
                                      'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'

                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')
                if doc['val_aquisicao'] != None:
                    doc['val_aquisicao'] = locale.currency(round(float(doc['val_aquisicao']), 2), grouping=True,
                                                           symbol=None)
                if doc['depreciacao_acum'] != None:
                    doc['depreciacao_acum'] = locale.currency(round(float(doc['depreciacao_acum']), 2), grouping=True,
                                                              symbol=None)
                if doc['val_liq'] != None:
                    doc['val_liq'] = locale.currency(round(float(doc['val_liq']), 2), grouping=True, symbol=None)
                if doc['taxa_depreciacao'] != None:
                    doc['taxa_depreciacao'] = locale.currency(round(float(doc['taxa_depreciacao']), 2), grouping=True,
                                                              symbol=None)
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
            lista_docs = list(Docs_Pac_Consorcio_Ativo_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_consorcio_ativo', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 14:
            lista_docs = list(Docs_Demais_Contas_M1.objects
                              .filter(cod_conta=obj_conta, cod_arquivo=obj_arq,
                                      cod_arquivo__cod_usu__cod_filial__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                              .values('cod_pac_doc_outros', 'data_entrada', 'data_lancto', 'cod_filial__desc_filial',
                                      'historico', 'num_doc', 'num_doc_contabil', 'val_rel', 'val_razao', 'val_dif',
                                      'obs', 'ativo'))
            for doc in lista_docs:
                if doc['cod_filial__desc_filial'] == None:
                    doc['cod_filial__desc_filial'] = 'Não informada'
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')


        dados = {
            'cod_conta': cod_conta_frm,
            'cod_arq': cod_arq_frm,
            'lista_docs': lista_docs,
            'obj_usuario_sessao': obj_usuario_sessao,
            'cod_pacote': obj_conta.cod_pacote_conta.cod_pacote_conta
        }
        return render(request, 'contabil_composicao_app/frm_docs_arq_competencia.html', dados)


class Form_Detalhes_Conta_Composicao_View(View):
    def get(self, request):
        cod_conta_frm = request.GET['cod_conta']
        competencia_frm = request.GET['compentencia']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        obj_conta = Conta.objects.get(pk=cod_conta_frm)
        data_competencia_str = competencia_frm + '-01'
        data_competencia_date = datetime.strptime(data_competencia_str, '%Y-%m-%d')


        data_hora_atual = datetime.now()
        data_hora_atual_h_m_y = data_hora_atual.strftime('%Y-%m-%d')

        '''resp_conta = (Responsaveis_Conta.objects.filter(cod_conta=obj_conta,cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                            .extra(where=[ " ('" + data_competencia + "' BETWEEN data_ini_atividade AND  data_fim_atividade) OR ( '" + data_competencia + "' >= data_ini_atividade AND data_fim_atividade is null) "]).first())'''

        resp_conta = (Responsaveis_Conta.objects.filter(
            ((Q(data_ini_atividade__lte=data_competencia_date) & Q(data_fim_atividade__gte=data_competencia_date)) | (Q(data_ini_atividade__lte=data_competencia_date) & Q(data_fim_atividade__isnull=True))),
            cod_conta=obj_conta,cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa).first())

        resp_composicao = 'Não informado'
        resp_validacao = 'Não informado'
        if resp_conta != None:
            resp_composicao = resp_conta.resp_composicao
            resp_validacao = resp_conta.resp_validacao

        desc_conta = ''
        if obj_conta.tipo_modelo == 1:
            desc_conta = (str(obj_conta.cod_conta) + ' - ' + obj_conta.desc_conta + ' - Modelo 1 - ' +
                          'Cód. red. CP : ' + str(obj_conta.cod_red_conta_contabil_cp))
        elif obj_conta.tipo_modelo == 3:
            desc_conta = (str(obj_conta.cod_conta) + ' - ' + obj_conta.desc_conta + ' - Modelo 3 - ' +
                          'Cód. red. CP : ' + str(obj_conta.cod_red_conta_contabil_cp) + ' - Cód. red. LP : ' +
                          str(obj_conta.cod_red_conta_contabil_lp))

        data = dict()
        data = {
            'cod_conta': obj_conta.cod_conta,
            'cod_modelo_conta': obj_conta.tipo_modelo,
            'desc_conta': desc_conta,
            'desc_pacote': obj_conta.cod_pacote_conta.desc_pacote_conta,
            'resp_composicao': resp_composicao,
            'resp_validacao': resp_validacao
        }
        return JsonResponse(data, safe=False)


class Form_Contas_Resp_View(View):
    def get_object(self, pk):
        try:
            return Responsaveis_Conta.objects.get(pk=pk)
        except Responsaveis_Conta.DoesNotExists:
            return Http404

    def get(self, request):
        lista_cod_usuarios = request.GET['lista_cod_usuario']
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        dic_lista_contas_resp = []
        lista_pacotes_resp = []
        lista_pacotes_resp = list(Responsaveis_Conta.objects
                                  .filter((Q(resp_composicao__in=lista_cod_usuarios.split(',')) | Q(resp_validacao__in=lista_cod_usuarios.split(','))),
                                          cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                          cod_conta__status_comp='A')
                                  .values('cod_conta__cod_pacote_conta__cod_pacote_conta',
                                          'cod_conta__cod_pacote_conta__desc_pacote_conta').distinct())
        for nome_usu in lista_cod_usuarios.split(','):
            lista_contas_resp = (Responsaveis_Conta.objects
                                 .filter( (Q(resp_composicao=nome_usu) | Q(resp_validacao=nome_usu)),
                                          cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                          cod_conta__status_comp='A' )
                                 .values('cod_resp_conta', 'cod_conta__cod_pacote_conta__desc_pacote_conta',
                                         'cod_conta__desc_conta', 'cod_conta__cod_conta',
                                         'cod_conta__cod_red_conta_contabil_cp', 'cod_conta__cod_red_conta_contabil_lp',
                                         'cod_conta__tipo_modelo',
                                         'resp_composicao', 'resp_validacao', 'data_ini_atividade',
                                         'data_fim_atividade', 'cod_conta__cod_pacote_conta__cod_pacote_conta'))



            for reg in lista_contas_resp:
                if reg['data_ini_atividade'] != None:
                    reg['data_ini_atividade'] = datetime.strftime(reg['data_ini_atividade'], '%d-%m-%Y')
                if reg['data_fim_atividade'] != None:
                    reg['data_fim_atividade'] = datetime.strftime(reg['data_fim_atividade'], '%Y-%m-%d')
                dic_lista_contas_resp.append(reg)
        data = dict()
        data = {
            'dic_lista_contas_resp': dic_lista_contas_resp,
            'lista_pacotes_resp': lista_pacotes_resp
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_resp_conta_frm = request.POST['cod_resp_conta']
        data_fim_frm = request.POST['data_fim']

        obj_resp_conta = Responsaveis_Conta.objects.get(pk=cod_resp_conta_frm)
        obj_resp_conta.data_fim_atividade = data_fim_frm
        obj_resp_conta.save()
        msg = 'Registro alterado com sucesso !!'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_doc = self.get_object(pk)
        obj_doc.delete()
        msg = 'Registro excluído com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)


class Form_Vincula_Contas_Resp_View(View):
    def get(self, request):
        cod_pacote_frm = request.GET['cod_pacote']
        tipo_transacao_frm = request.GET['tipo_transacao']

        lista_resp_contas = []
        lista_contas_pac = []
        obj_pacote = Pacote_Conta.objects.get(pk=cod_pacote_frm)
        if tipo_transacao_frm == 'retorna_lista_contas':
            lista_contas_pac = list(Conta.objects
                                    .filter(cod_pacote_conta=obj_pacote, status_comp='A')
                                    .values('tipo_modelo', 'cod_conta', 'desc_conta', 'cod_red_conta_contabil_cp',
                                            'cod_red_conta_contabil_lp'))
        elif tipo_transacao_frm == 'retorna_dados_contas_resp':
            cod_usuario_sessao = request.session['cod_usuario_logado']
            obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)


            lista_resp_contas = list(Responsaveis_Conta.objects
                                 .filter(cod_conta__cod_pacote_conta=obj_pacote, cod_conta__status_comp='A',
                                         cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa)
                                 .values('cod_resp_conta', 'resp_composicao', 'resp_validacao', 'data_ini_atividade',
                                         'data_fim_atividade', 'cod_conta__cod_conta', 'cod_conta__tipo_modelo',
                                         'cod_conta__desc_conta', 'cod_conta__cod_red_conta_contabil_cp',
                                         'cod_conta__cod_red_conta_contabil_lp'))
            for reg in lista_resp_contas:
                if reg['data_ini_atividade'] != None:
                    reg['data_ini_atividade'] = datetime.strftime(reg['data_ini_atividade'], '%d-%m-%Y')

        data = dict()
        data = {
            'lista_resp_contas' :   lista_resp_contas,
            'lista_contas_pac'  : lista_contas_pac
        }
        return JsonResponse(data, safe=False)


class Comp_Pac_Contas_Comp_Detalhado_View(View):
    def get(self, request):
        lista_nome_resp_frm = request.GET['lista_nome_resp']

        lista_pacote = list(Responsaveis_Conta.objects.filter(
            Q(resp_composicao__in=lista_nome_resp_frm.split(',')) | Q(resp_validacao__in=lista_nome_resp_frm.split(','))
        ).values('cod_conta__cod_pacote_conta__cod_pacote_conta', 'cod_conta__cod_pacote_conta__desc_pacote_conta').distinct())
        data = dict()
        data = {
            'lista_pacote': lista_pacote
        }
        return JsonResponse(data, safe=False)



class Form_Renegociacao_Contrato_View(View):
    def post(self, request):
        cod_contrato_frm = request.POST['cod_contrato']
        justificativa_frm = request.POST['justificativa']
        data_renegociacao_frm = request.POST['data_renegociacao']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        data_hora_atual = datetime.now()
        data_hora_atual_y_m_d = data_hora_atual.strftime('%Y-%m-%d')
        data_hora_atual_d_m_y = data_hora_atual.strftime('%d-%m-%Y')

        obj_contrato = Contrato.objects.get(pk=cod_contrato_frm)
        lista_obj_parcelas = Parcela_Contrato.objects.filter(cod_contrato=obj_contrato, tipo_prazo__in=['CP', 'LP'])
        for obj_parcela in lista_obj_parcelas:
            obj_parcela.val_conta = 0
            obj_parcela.val_principal = 0
            obj_parcela.val_taxas = 0
            obj_parcela.tipo_prazo = 'RN'
            obj_parcela.data_liquidacao = data_renegociacao_frm
            obj_parcela.val_pago = 0
            obj_parcela.val_fundo = 0
            obj_parcela.obs_parcela = f"/Operação de renegociação executada em {datetime.strptime(data_renegociacao_frm,'%Y-%m-%d').strftime('%d-%m-%Y')} por {obj_usuario_sessao.login_usu}/"
            obj_parcela.save()
        msg = 'Operação de renegociação, realizada com sucesso !'

        data = dict()
        data = {
            'msg': msg,
            'cod_conta': obj_contrato.cod_conta.cod_conta
        }
        return JsonResponse(data, safe=False)




class Form_Atualiza_Parcelas_Data_Corte(View):
    def post(self, request):
        lista_cod_contas = request.POST['lista_cod_contas']
        data_corte_frm = request.POST['data_corte']
        competencia_aud = data_corte_frm.split('-')[0] + '-' + data_corte_frm.split('-')[1] + '-01'
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        lista_parcelas_atualizadas_form = []
        for cod_conta in lista_cod_contas.split(','):
            obj_conta = Conta.objects.get(pk=cod_conta)

            lista_parcelas_para_atualizar = (Parcela_Contrato.objects
                                                 .filter(data_liquidacao__isnull=True,
                                                         cod_contrato__cod_conta=obj_conta,
                                                         cod_contrato__sincronizar_benner='S',
                                                         cod_contrato__cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa))


            for parcela in lista_parcelas_para_atualizar:
                verifica_se_contrato_auditada = (Auditoria_Status_Composicao_Competencia.objects
                                                 .filter(cod_conta=parcela.cod_contrato.cod_conta,
                                                         cod_contrato=parcela.cod_contrato,
                                                         data_competencia=competencia_aud, status=1))

                if len(verifica_se_contrato_auditada) == 0:
                    conexao_benner = ConexaoBancoBenner()
                    lista_parcelas_atualizadas = (conexao_benner
                                                  .atualiza_parcelas_data_corte(parcela.handle_parcela, data_corte_frm))

                    for parc in lista_parcelas_atualizadas:
                        obj_parcela = Parcela_Contrato.objects.filter(handle_parcela=parc['handle_parc']).first()

                        val_principal_anterior = ''
                        if obj_parcela.val_principal != None:
                            val_principal_anterior = str(obj_parcela.val_principal)

                        val_taxa_anterior = ''
                        if obj_parcela.val_taxas > 0:
                            val_taxa_anterior = str(obj_parcela.val_taxas)


                        data_liquidacao = None
                        if parc['data_liquidacao'] != None:
                            data_liquidacao = (datetime.strptime(parc['data_liquidacao'], '%Y-%m-%d')
                                               .strftime('%d-%m-%Y'))
                            obj_parcela.tipo_prazo = 'PG'
                            obj_parcela.data_liquidacao = parc['data_liquidacao']

                        val_pago = 0.00
                        val_pago_bd = 0.00
                        if parc['valor_corrigido'] > 0:
                            val_pago = locale.currency(round(parc['valor_corrigido'], 2), grouping=True, symbol=None)
                            val_pago_bd = parc['val_total_pago']
                        else:
                            val_pago = locale.currency(round(parc['pag_parcial'], 2), grouping=True, symbol=None)
                            val_pago_bd = parc['pag_parcial']

                        obj_parcela.data_vencimento = parc['data_vencimento']
                        obj_parcela.val_corrigido = parc['valor_corrigido']
                        obj_parcela.val_pago = val_pago_bd
                        obj_parcela.val_principal = parc['val_principal']
                        obj_parcela.val_taxas = parc['val_taxas']
                        obj_parcela.val_fundo = parc['val_fundo']
                        obj_parcela.data_ultima_atualizacao = parc['data_ultima_atualizacao']
                        obj_parcela.val_desc_taxas = parc['val_desc_taxas']
                        obj_parcela.val_acres_taxas = parc['val_acres_taxas']
                        obj_parcela.val_desc_principal = parc['val_desc_principal']
                        obj_parcela.val_acres_principal = parc['val_acres_principal']
                        obj_parcela.cod_usu = obj_usuario_sessao
                        obj_parcela.obs_parcela = f'''/Atualização realizada em {parc['data_ultima_atualizacao']}.Por {obj_usuario_sessao.login_usu}.Principal estava em R$ {val_principal_anterior} e R$ Taxas {val_taxa_anterior}/ '''
                        obj_parcela.save()


                        val_principal = 0.00
                        if parc['val_principal'] != None:
                            val_principal = locale.currency(round(parc['val_principal'], 2), grouping=True, symbol=None)

                        val_taxas = 0.00
                        if parc['val_taxas'] != None:
                            val_taxas = locale.currency(round(parc['val_taxas'], 2), grouping=True, symbol=None)

                        val_fundo = 0.00
                        if parc['val_fundo'] != None:
                            val_fundo = locale.currency(round(parc['val_fundo'], 2), grouping=True, symbol=None)



                        reg_parc = {
                            'cod_conta': obj_parcela.cod_contrato.cod_conta.cod_conta,
                            'desc_conta': obj_parcela.cod_contrato.cod_conta.desc_conta,
                            'num_contrato': obj_parcela.cod_contrato.num_contrato,
                            'num_parcela': obj_parcela.ordem_parcela,
                            'val_pago': val_pago,
                            'val_principal': val_principal,
                            'val_taxas': val_taxas,
                            'val_fundo': val_fundo,
                            'data_vencimento': (datetime.strptime(obj_parcela.data_vencimento, '%Y-%m-%d').strftime('%d-%m-%Y')),
                            'data_liquidacao': data_liquidacao,
                            'handle_parcela': obj_parcela.handle_parcela
                        }
                        lista_parcelas_atualizadas_form.append(reg_parc)


        data = dict()
        data = {
            'lista_parcelas_atualizados': lista_parcelas_atualizadas_form
        }
        return JsonResponse(data, safe=False)


class Comp_Contas_Resp_View(View):
    def get(self, request):
        lista_nome_responsavel_frm = request.GET['lista_nome_responsavel']
        lista_cod_pacote_frm = request.GET['lista_cod_pacote']

        lista_contas = list(Responsaveis_Conta.objects
                        .filter((Q(resp_composicao__in=lista_nome_responsavel_frm.split(',')) |
                                 Q(resp_validacao__in=lista_nome_responsavel_frm.split(','))),
                                cod_conta__cod_pacote_conta__cod_pacote_conta__in=lista_cod_pacote_frm.split(','))
                        .values('cod_conta__cod_conta', 'cod_conta__desc_conta','cod_conta__cod_red_conta_contabil_cp',
                                'cod_conta__cod_red_conta_contabil_lp').distinct())
        data = dict()
        data = {
            'lista_contas': lista_contas
        }
        return JsonResponse(data, safe=False)