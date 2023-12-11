import os

import decimal
import shutil
import traceback

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
    Arquivo_Docs_Pac_Contas_Modelo_1, Docs_Pac_Contas_Pagar_Receber_M1_View, Docs_Pac_Estoque_M1_View, \
    Docs_Pac_Folha_Pag_M1_View, Docs_Pac_Contas_Compensacao_M1_View, Docs_Pac_Tributos_M1_View, \
    Docs_Pac_Finac_Disponib_M1_View, Docs_Pac_Intercompany_M1_View, Docs_Pac_Imobilizado_M1_View, \
    Docs_Pac_Consorcio_Ativo_M1_View
from apps.estrut_org_app.models import Empresa, Filial
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR


class Form_Imp_Cad_Conta_View(View):
    def get(self, request):
        #lista_contas_benner = ConexaoBancoBenner().retorna_dados_contas()
        lista_contas = Conta.objects.filter(tipo_modelo=1)
        lista_pacotes_conta = Pacote_Conta.objects.filter(cod_modelo=1)
        lista_usuarios_contabil = Usuario.objects.filter(sala='CON')

        #diretorio_arquivos_postados = 'media/docs/contabil_composicao_app/anexos_pendentes_importacao'
        diretorio_arquivos_postados = os.path.join(BASE_DIR, 'media\\docs\\contabil_composicao_app\\anexos_pendentes_importacao')
        lista_arquivos = os.listdir(diretorio_arquivos_postados)
        qtd_arquivos_postados = len(lista_arquivos)

        contexto = {
            'lista_contas': lista_contas,
            'lista_pacotes_conta': lista_pacotes_conta,
            'lista_usuarios_contabil': lista_usuarios_contabil,
            'desc_menu': 'Cadastro de contas composição',
            'qtd_arquivos_postados': qtd_arquivos_postados
        }
        return render(request, 'contabil_composicao_app/form_cad_contas.html', contexto)

class Form_Imp_Contratos_Conta_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        tipo_pesq_form = request.GET['tipo_pesq']
        num_contrato_form = request.GET['num_contrato']

        dados = self.atualiza_dados_contratos_parcelas(cod_conta_form, num_contrato_form, tipo_pesq_form)


        data = dict()
        data = {
            'lista_contratos': dados[0],
            'msg': dados[1]
        }
        return JsonResponse(data, safe=False)


    def atualiza_dados_contratos_parcelas(self, cod_conta_form, num_contrato_form, tipo_pesq_form):
        obj_conta = Conta.objects.get(pk=cod_conta_form)
        handle_conta_cp = obj_conta.handle_conta_contabil_cp
        handle_conta_lp = obj_conta.handle_conta_contabil_lp
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')


        lista_contratos = []
        lista_parcelas_atualizadas = []
        lista_contratos_benner = ConexaoBancoBenner() \
            .retorna_dados_contratos_conta(tipo_pesq_form, num_contrato_form, handle_conta_cp, handle_conta_lp)
        if lista_contratos_benner != None:
            for contrato in lista_contratos_benner:
                obj_empresa = Empresa.objects.filter(cod_empresa=contrato['cod_empresa']).first()
                prox_parc_pendente = 0
                if contrato['proxima_parc_pendente'] != None:
                    prox_parc_pendente = contrato['proxima_parc_pendente'].split('/')[1]
                obj_contrato = Contrato.objects.filter(handle_fn_doc=contrato['handle_fn_doc']).first()
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
                        qtd_parcelas=prox_parc_pendente,
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
                    obj_contrato.qtd_parcelas = prox_parc_pendente
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
                        tipo_prazo_parc = ''
                        if parcela['data_liquidacao'] != None:
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

                        val_pago = decimal.Decimal(0.00)
                        if parcela['val_total_pago'] != None:
                            val_pago = decimal.Decimal(parcela['val_total_pago'])

                        obj_parcela = Parcela_Contrato.objects.filter(handle_parcela=parcela['handle_parc']).first()
                        if obj_parcela == None:
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
                                cod_contrato=obj_contrato
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
                            'val_total_pago': val_total_pago
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
        cod_conta_form = request.GET['cod_conta']
        cod_modelo_conta_selecionado = request.GET['cod_modelo_conta_selecionado']

        tipo_return_form = request.GET['tipo_return']
        obj_conta_pesq = Conta.objects.get(pk=cod_conta_form)
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
            'cod_pacote_conta': nome_pacote
        }


        lista_pacotes = list(Pacote_Conta.objects
                             .filter(cod_modelo=cod_modelo_conta_selecionado)
                             .values('cod_pacote_conta', 'desc_pacote_conta'))

        data = dict()
        if tipo_return_form == 'J':
            data = {
                'dic_conta': dic_conta,
                'lista_pacotes': lista_pacotes
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

            cod_usuario_sessao = request.session['cod_usuario_logado']
            obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

            obj_conta = Conta.objects.get(pk=cod_conta_form)
            obj_contrato = Contrato(
                handle_fn_doc = handle_contrato_form,
                num_contrato = num_contrato_form,
                data_emissao_contrato = data_emissao_form,
                nome_fornecedor = nome_fornecedor_form,
                handle_operacao = handle_operacao_form,
                desc_op = desc_operacao_form,
                num_doc_contabil = doc_contabil_form,
                val_nominal = val_nominal_form,
                val_liquido = val_liquido_form,
                sincronizar_benner = check_atualiza_benner_form,
                dia_util = dia_util_form,
                data_primeira_parcela= data_primeira_parcela_form,
                qtd_parcelas = qtd_parcelas_form,
                cod_conta = obj_conta,
                cod_empresa = obj_usuario_sessao.cod_empresa
            )
            obj_contrato.save()
            '''Gera parcelas'''
            valor_parcela = float(val_liquido_form) / int(qtd_parcelas_form)
            data_ini = datetime(int(data_primeira_parcela_form.split('-')[0]), int(data_primeira_parcela_form.split('-')[1]),
                                int(data_primeira_parcela_form.split('-')[2]))

            for parc in range(int(qtd_parcelas_form)):
                primeiro_dia_mes = data_ini.replace(day=int(dia_util_form))
                #print(str(i) + ' - ' + str(primeiro_dia_mes.strftime('%Y-%m-%d')))  # Exibe a data formatada
                tipo_prazo = 'CP'
                if parc > int(qtd_parcelas_form) / 2:
                    tipo_prazo = 'LP'
                obj_parcela = Parcela_Contrato(
                    handle_parcela = parc + 1,
                    ap_parcela = parc + 1,
                    ordem_parcela = str(parc + 1) + '/' + str(qtd_parcelas_form),
                    val_conta = valor_parcela,
                    val_corrigido = None,
                    val_principal = None,
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
                                                             sincronizar_benner='S')
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
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        cod_conta_form = request.GET['cod_conta']
        obj_conta_pesq = Conta.objects.get(pk=cod_conta_form)
        lista_contratos = []
        lista_contratos_banco = Contrato.objects.filter(cod_conta=obj_conta_pesq)
        dic_contrato = None
        lista_parcelas_contrato = None
        for contrato in lista_contratos_banco:
            lista_parcelas_contrato = []
            lista_parcelas = Parcela_Contrato.objects.filter(cod_contrato=contrato)
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


                    val_fundo = 0
                    if parc.val_fundo != None:
                        val_fundo = parc.val_fundo

                    val_tt_parc = parc.val_principal + parc.val_taxas + val_fundo
                    #val_balancete = val_balancete - val_corrigido
                    val_balancete = val_balancete - (val_principal_parc + val_taxas_parc)
                    parcela = {
                        'handle_fn_doc': parc.cod_contrato.handle_fn_doc,
                        'handle_parc': parc.handle_parcela,
                        'ap_parcela': parc.ap_parcela,
                        'ordem_parcela': parc.ordem_parcela,
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
                        'val_balancete': locale.currency(val_balancete, grouping=True, symbol=None)
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
        data = dict()
        data = {
            'lista_contratos': lista_contratos,
        }
        return JsonResponse(data, safe=False)

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
        lista_dic_resp_conta = []
        lista_responsaveis_conta = Responsaveis_Conta.objects.filter(cod_conta=cod_conta_form)
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
        data = dict()
        data = {
            'msg': msg,
            'cod_conta': cod_conta
        }
        return JsonResponse(data, safe=False)

class Form_Cad_Parcelas_Contrato_View(View):
    def post(self, request):
        transacao_form = request.POST['transacao']
        handle_parcela_form = request.POST['handle_parcela']
        obj_parcela = Parcela_Contrato.objects.filter(handle_parcela=handle_parcela_form).first()
        msg = ''
        if transacao_form == 'pagamento':
            data_pag_form = request.POST['data_pag']
            val_pag_form = request.POST['val_pag']

            obj_parcela.data_liquidacao = data_pag_form
            obj_parcela.val_pago = val_pag_form.replace('.','').replace(',','.')
            obj_parcela.save()
            msg = 'Pagamento efetivado com sucesso!'
        elif transacao_form == 'atualiza_dados':
            val_principal_form = request.POST['val_principal']
            val_taxas_form = request.POST['val_taxas']
            val_fundo_form = request.POST['val_fundo']

            obj_parcela.val_principal = val_principal_form
            obj_parcela.val_taxas = val_taxas_form
            obj_parcela.val_fundo = val_fundo_form
            obj_parcela.val_corrigido = float(val_principal_form) + float(val_taxas_form)
            obj_parcela.save()
            msg = 'Dados atualizados com sucesso!'

        data = dict()
        data = {
            'msg': msg,
            'cod_conta': obj_parcela.cod_contrato.cod_conta.cod_conta
        }
        return JsonResponse(data, safe=False)

class Form_Conciliacao_Comp_Benner_Resumo_View(View):
    def get(self, request):
        #lista_contas_benner = ConexaoBancoBenner().retorna_dados_contas()
        lista_contas_modelo_1 = Conta.objects.filter(tipo_modelo=1, status_comp='A')
        contexto = {
            'lista_contas_modelo_1': lista_contas_modelo_1,
            'desc_menu': 'Conciliação Composição x Benner Resumido'
        }
        return render(request, 'contabil_composicao_app/form_conciliacao_composicao_benner.html', contexto)


class Form_Conciliacao_Comp_Benner_Detalhado_View(View):
    def get(self, request):
        #lista_contas_benner = ConexaoBancoBenner().retorna_dados_contas()
        lista_contas_modelo_1 = Conta.objects.filter(tipo_modelo=1, status_comp='A')
        contexto = {
            'lista_contas_modelo_1': lista_contas_modelo_1,
            'desc_menu': 'Conciliação Composição x Benner Detalhado'
        }
        return render(request, 'contabil_composicao_app/form_conciliacao_composicao_benner_detalhado.html', contexto)

    def post(self, request):
        cod_contrato_form = request.POST['cod_contrato']
        tipo_prazo_form = request.POST['tipo_prazo']
        cod_status_form = request.POST['cod_status']
        obs_status_form = request.POST['obs_status']
        competencia_form = request.POST['competencia']
        val_composicao_form = request.POST['val_composicao']
        val_balancete_form = request.POST['val_balancete']
        val_diferenca_form = request.POST['val_diferenca']

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
                cod_conta=obj_conta, data_competencia=competencia_date, tipo_prazo=tipo_prazo_form
            ).first()
        else:
            obj_contrato = Contrato.objects.get(pk=cod_contrato_form)
            obj_conta = obj_contrato.cod_conta
            obj_status_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=obj_contrato, data_competencia=competencia_date, tipo_prazo=tipo_prazo_form
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

        lista_contas = None
        lista_contas_para_atualizar_benner = None
        if tipo_rel in ('R', 'D', 'C'):
            lista_contas = list(Conta.objects.filter(tipo_modelo=cod_tipo_modelo_form, status_comp='A')
                                .values('cod_conta', 'desc_conta', 'cod_red_conta_contabil_cp',
                                        'cod_red_conta_contabil_lp'))

            lista_contas_para_atualizar_benner = list(Contrato.objects
                                                  .filter(cod_conta__tipo_modelo=cod_tipo_modelo_form,
                                                          cod_conta__status_comp='A',
                                                          sincronizar_benner='S')
                                                  .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                                          'cod_conta__cod_red_conta_contabil_cp',
                                                          'cod_conta__cod_red_conta_contabil_lp')
                                                  .distinct())
        elif tipo_rel == 'A':
            competencia_form = request.GET['data_competencia']
            competencia_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), 1)
            lista_contas = list(Auditoria_Status_Composicao_Competencia.objects
                                .filter(cod_conta__tipo_modelo=cod_tipo_modelo_form, cod_conta__status_comp='A',
                                        status=1, data_competencia=competencia_date)
                                .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                         'cod_conta__cod_red_conta_contabil_cp', 'cod_conta__cod_red_conta_contabil_lp')
                                .distinct())

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
        ultimo_dia_mes_calendar = calendar.monthrange(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]))[1]
        ultimo_dia_mes_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), ultimo_dia_mes_calendar)
        primeiro_dia_ano = datetime(int(competencia_form.split('-')[0]), 1, 1)
        ultimo_dia_ano = datetime(int(competencia_form.split('-')[0]), 12, 31)


        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        lista_contas_conciliacao = []
        #for cod_conta_form in lista_cod_conta_form.split(','):
        if tipo_visualizacao_form == 'R':
            if cod_modelo_selecionado_form == '1':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    registros_tabela = []
                    if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
                        registros_tabela = list(Docs_Pac_Contas_Pagar_Receber_M1_View.objects
                                                .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
                        registros_tabela = list(Docs_Pac_Estoque_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
                        registros_tabela = list(Docs_Pac_Folha_Pag_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
                        registros_tabela = list(Docs_Pac_Contas_Compensacao_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
                        registros_tabela = list(Docs_Pac_Tributos_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
                        registros_tabela = list(Docs_Pac_Finac_Disponib_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
                        registros_tabela = list(Docs_Pac_Intercompany_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
                        registros_tabela = list(Docs_Pac_Imobilizado_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
                        registros_tabela = list(Docs_Pac_Consorcio_Ativo_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))



                    val_composicao = 0
                    for reg in registros_tabela:
                        val_composicao += float(reg.tt_val_rel)

                    cod_anexo_competencia = 0
                    obj_anexo_competencia = Anexos_Contrato.objects.filter(cod_conta=obj_conta,
                                                                           data_competencia=datetime.strptime(
                                                                               competencia_form + '-01',
                                                                               '%Y-%m-%d')).first()
                    if obj_anexo_competencia != None:
                        cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato

                    val_balancete = ConexaoBancoBenner() \
                                        .retorna_balancete_conta(obj_conta.handle_conta_contabil_cp,
                                                                 primeiro_dia_ano,
                                                                 ultimo_dia_mes_date)


                    val_dif = 0
                    if val_balancete < 0 and val_composicao < 0:
                        val_dif = val_composicao - val_balancete
                    elif val_balancete < 0 and val_composicao > 0:
                        val_dif = val_composicao + val_balancete
                    else:
                        val_dif = val_composicao - val_balancete

                    linha = []
                    linha.append(obj_conta.cod_conta) #0
                    linha.append(str(obj_conta.cod_conta)+'-'+obj_conta.desc_conta) #1
                    linha.append(locale.currency(round(val_composicao,2), grouping=True, symbol=None)) #2
                    linha.append(locale.currency(round(val_balancete,2), grouping=True, symbol=None)) #3
                    linha.append(locale.currency(round(val_dif,2), grouping=True, symbol=None)) #4
                    linha.append(cod_anexo_competencia) #5
                    linha.append(obj_conta.cod_red_conta_contabil_cp) #6
                    linha.append(obj_conta.cod_estrut_cp) #7
                    lista_contas_conciliacao.append(linha)

            elif cod_modelo_selecionado_form == '3':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    conta = Conta.objects.get(pk=int(cod_conta_form))
                    lista_contratos = Contrato.objects.filter(cod_conta=conta)
                    for contrato in lista_contratos:
                        '''Calcula dados CP'''
                        dados_conciliacao_cp = self.gera_reg_conciliacao_por_tipo_prazo(conta, contrato,
                                                                                        primeiro_dia_ano,
                                                                                        ultimo_dia_ano,
                                                                                        ultimo_dia_mes_date, 'CP',
                                                                                        competencia_form)

                        '''Calcula dados LP'''
                        dados_conciliacao_lp = self.gera_reg_conciliacao_por_tipo_prazo(conta, contrato,
                                                                                        primeiro_dia_ano,
                                                                                        ultimo_dia_ano,
                                                                                        ultimo_dia_mes_date, 'LP',
                                                                                        competencia_form)

                        val_comp_cp = float(dados_conciliacao_cp[7].replace('.','').replace(',','.'))
                        '''if val_comp_cp < 0:
                            val_comp_cp *= -1'''
                        val_comp_lp = float(dados_conciliacao_lp[7].replace('.','').replace(',','.'))
                        '''if val_comp_lp < 0:
                            val_comp_lp *= -1'''
                        val_tt_comp = val_comp_cp + val_comp_lp

                        val_bal_cp = float(dados_conciliacao_cp[8].replace('.','').replace(',','.'))
                        '''if val_bal_cp < 0:
                            val_bal_cp *= -1'''
                        val_bal_lp = float(dados_conciliacao_lp[8].replace('.','').replace(',','.'))
                        '''if val_bal_lp < 0:
                            val_bal_lp *= -1'''
                        val_tt_bal = val_bal_cp + val_bal_lp

                        '''val_df_tt_comp_bal = 0
                        if val_tt_bal < 0:
                            val_df_tt_comp_bal = val_tt_comp +  val_tt_bal
                        else:
                            val_df_tt_comp_bal = val_tt_comp -  val_tt_bal'''

                        val_df_tt_comp_bal = 0
                        if val_tt_bal < 0 and val_tt_comp < 0:
                            val_df_tt_comp_bal = val_tt_comp - val_tt_bal
                        elif val_tt_bal < 0 and val_tt_comp > 0:
                            val_df_tt_comp_bal = val_tt_comp + val_tt_bal
                        else:
                            val_df_tt_comp_bal = val_tt_comp - val_tt_bal

                        cod_anexo_competencia = 0
                        obj_anexo_competencia = Anexos_Contrato.objects.filter(cod_contrato=contrato,data_competencia=datetime.strptime(competencia_form+'-01', '%Y-%m-%d')).first()
                        if obj_anexo_competencia != None:
                            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato

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
                        linha.append(cod_anexo_competencia) #13
                        lista_contas_conciliacao.append(linha)


                        '''dados_conciliacao = {
                            'cod_conta': conta.cod_conta,
                            'desc_conta': conta.desc_conta,
                            'num_contrato': contrato.num_contrato,
                            'doc_contabil': contrato.num_doc_contabil,
                            'val_comp_cp': locale.currency(
                                round(float(dados_conciliacao_cp['val_comp'].replace('.','').replace(',','.')),2),
                                grouping=True, symbol=None),
                            'val_balancete_cp': locale.currency(
                                round(float(dados_conciliacao_cp['val_balancete'].replace('.','').replace(',','.')) ,2),
                                grouping=True, symbol=None),
                            'val_dif_comp_balanc_cp': locale.currency(
                                round(float(dados_conciliacao_cp['val_dif_comp_balanc'].replace('.','').replace(',','.')) ,2),
                                grouping=True, symbol=None),
                            'val_comp_lp': locale.currency(
                                round(float(dados_conciliacao_lp['val_comp'].replace('.','').replace(',','.')),2),
                                grouping=True, symbol=None),
                            'val_balancete_lp': locale.currency(
                                round(float(dados_conciliacao_lp['val_balancete'].replace('.','').replace(',','.')),2),
                                grouping=True, symbol=None),
                            'val_dif_comp_bal_lp': locale.currency(
                                round(float(dados_conciliacao_lp['val_dif_comp_balanc'].replace('.','').replace(',','.')),2),
                                grouping=True, symbol=None),
                            'val_tt_comp': locale.currency(round(val_tt_comp,2), grouping=True, symbol=None),
                            'val_tt_balan': locale.currency(round(val_tt_bal,2), grouping=True,
                                                            symbol=None),
                            'val_dif_tt_comp_bal': locale.currency(
                                round(val_df_tt_comp_bal,2), grouping=True, symbol=None),
                            'cod_anexo_contrato_competencia': cod_anexo_competencia
                        }
                        lista_contas_conciliacao.append(dados_conciliacao)'''

        elif tipo_visualizacao_form == 'D':
            lista_contas = []
            competencia_date = datetime(int(competencia_form.split('-')[0]), int(competencia_form.split('-')[1]), 1)
            cod_status_analise_form = request.GET['cod_status_analise']
            if cod_status_analise_form == '0':
                lista_contas = lista_cod_conta_form.split(',')
            elif cod_status_analise_form == '5':
                for reg in lista_cod_conta_form.split(','):
                    conta_auditada = Auditoria_Status_Composicao_Competencia.objects.filter(
                        data_competencia=competencia_date, cod_conta__cod_conta=reg
                    ).first()
                    if conta_auditada == None:
                        lista_contas.append(reg)
            else:
                lista_contas_auditadas = Auditoria_Status_Composicao_Competencia.objects.filter(
                        data_competencia=competencia_date, status=int(cod_status_analise_form),
                    cod_conta__tipo_modelo=cod_modelo_selecionado_form)
                for reg in lista_contas_auditadas:
                    lista_contas.append(reg.cod_conta.cod_conta)

            if cod_modelo_selecionado_form == '1':
                for cod_conta_form in lista_contas:
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    registros_tabela = []
                    if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
                        registros_tabela = list(Docs_Pac_Contas_Pagar_Receber_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
                        registros_tabela = list(Docs_Pac_Estoque_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
                        registros_tabela = list(Docs_Pac_Folha_Pag_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
                        registros_tabela = list(Docs_Pac_Contas_Compensacao_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
                        registros_tabela = list(Docs_Pac_Tributos_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
                        registros_tabela = list(Docs_Pac_Finac_Disponib_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
                        registros_tabela = list(Docs_Pac_Intercompany_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
                        registros_tabela = list(Docs_Pac_Imobilizado_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
                        registros_tabela = list(Docs_Pac_Consorcio_Ativo_M1_View.objects
                                                .filter(cod_conta=obj_conta,
                                                        cod_arquivo__data_competencia=data_competencia)
                                                .annotate(tt_val_rel=Sum('val_rel')))
                    val_composicao = 0
                    for reg in registros_tabela:
                        val_composicao += float(reg.tt_val_rel)

                    cod_anexo_competencia = 0
                    obj_anexo_competencia = Anexos_Contrato.objects.filter(cod_conta=obj_conta,
                                                                           data_competencia=datetime.strptime(
                                                                               competencia_form + '-01',
                                                                               '%Y-%m-%d')).first()
                    if obj_anexo_competencia != None:
                        cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato

                    val_balancete = ConexaoBancoBenner() \
                                        .retorna_balancete_conta(obj_conta.handle_conta_contabil_cp,
                                                                 primeiro_dia_ano,
                                                                 ultimo_dia_mes_date)
                    '''if val_balancete < 0:
                        val_balancete *= -1
                    if val_composicao < 0:
                        val_composicao *= -1'''
                    val_dif = 0
                    if val_balancete < 0 and val_composicao < 0:
                        val_dif = val_composicao - val_balancete
                    elif val_balancete < 0 and val_composicao > 0:
                        val_dif = val_composicao + val_balancete
                    else:
                        val_dif = val_composicao - val_balancete

                    '''Verifica se há status da conta na competencia'''
                    cod_status_auditoria_comp = 0
                    obs_status_auditoria_comp = ''
                    obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                        cod_conta=obj_conta, data_competencia=competencia_date
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
                    linha.append(cod_anexo_competencia) #9
                    lista_contas_conciliacao.append(linha) #10

            elif cod_modelo_selecionado_form == '3':
                for cod_conta_form in lista_contas:
                    conta = Conta.objects.get(pk=int(cod_conta_form))
                    lista_contratos = Contrato.objects.filter(cod_conta=conta.cod_conta)
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
                                        .filter(cod_conta=obj_conta, status=1, data_competencia=competencia_date))

                    for reg in lista_composicao:
                        cod_anexo_competencia = 0
                        obj_anexo_competencia = Anexos_Contrato.objects.filter(cod_conta=obj_conta,
                                                                               data_competencia=datetime.strptime(
                                                                                   competencia_form + '-01',
                                                                                   '%Y-%m-%d')).first()
                        if obj_anexo_competencia != None:
                            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato

                        linha = []
                        linha.append(obj_conta.cod_conta)  # 0
                        linha.append(obj_conta.cod_red_conta_contabil_cp)  # 1
                        linha.append(obj_conta.cod_estrut_cp)  # 2
                        linha.append(str(obj_conta.cod_conta) + '-' + obj_conta.desc_conta)  # 3
                        linha.append(locale.currency(round(reg.val_composicao, 2), grouping=True, symbol=None))  # 4
                        linha.append(locale.currency(round(reg.val_balancete, 2), grouping=True, symbol=None))  # 5
                        linha.append(locale.currency(round(reg.val_diferenca, 2), grouping=True, symbol=None))  # 6
                        linha.append(cod_anexo_competencia)  # 7
                        lista_contas_conciliacao.append(linha)

            elif cod_modelo_selecionado_form == '3':
                for cod_conta_form in lista_cod_conta_form.split(','):
                    obj_conta = Conta.objects.get(pk=int(cod_conta_form))
                    lista_composicao = (Auditoria_Status_Composicao_Competencia.objects
                                        .filter(cod_conta=obj_conta, status=1, data_competencia=competencia_date))

                    for reg in lista_composicao:
                        cod_reduzido = '0'
                        cod_estrutura = '0'
                        if reg.tipo_prazo == 'CP':
                            cod_estrutura = obj_conta.cod_estrut_cp
                            cod_reduzido = obj_conta.cod_red_conta_contabil_cp

                        elif reg.tipo_prazo == 'LP':
                            cod_estrutura = obj_conta.cod_estrut_lp
                            cod_reduzido = obj_conta.cod_red_conta_contabil_lp



                        cod_anexo_competencia = 0
                        obj_anexo_competencia = Anexos_Contrato.objects.filter(cod_contrato=reg.cod_contrato,
                                                                               data_competencia=datetime.strptime(
                                                                                   competencia_form + '-01',
                                                                                   '%Y-%m-%d')).first()
                        if obj_anexo_competencia != None:
                            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato

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
                        linha.append(cod_anexo_competencia)  # 11
                        lista_contas_conciliacao.append(linha)


        data = dict()
        data = {
            'lista_contas_conciliacao': lista_contas_conciliacao
        }
        return JsonResponse(data, safe=False)

    '''def gera_reg_conciliacao_por_tipo_prazo_bkup(self, conta, contrato, primeiro_dia_ano, ultimo_dia_ano,
                                            ultimo_dia_periodo, tipo_prazo, competencia):
        cod_red = 0
        cod_estrutura = 0
        val_composicao = 0
        val_balancete = 0
        val_dif_comp_balanc = 0
        cod_status_auditoria_comp = 0
        obs_status_auditoria_comp = ''
        if tipo_prazo == 'CP':
            cod_red = conta.cod_red_conta_contabil_cp
            cod_estrutura = conta.cod_estrut_cp
            val_composicao_ano_dic = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_vencimento__range=[primeiro_dia_ano, ultimo_dia_ano]) \
                .aggregate(sum_principal=Sum('val_principal'))
            val_composicao_ano = 0
            if val_composicao_ano_dic['sum_principal'] != None:
                val_composicao_ano = val_composicao_ano_dic['sum_principal']

            val_comp_pago_periodo_dic = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_vencimento__range=[primeiro_dia_ano, ultimo_dia_periodo], tipo_prazo='PG') \
                .aggregate(sum_principal=Sum('val_principal'))
            val_comp_pago_periodo = 0
            if val_comp_pago_periodo_dic['sum_principal'] != None:
                val_comp_pago_periodo = val_comp_pago_periodo_dic['sum_principal']


            val_composicao = val_composicao_ano - val_comp_pago_periodo

            val_balancete = ConexaoBancoBenner() \
                                .retorna_balancete_conta(conta.handle_conta_contabil_cp,
                                                         primeiro_dia_ano,
                                                         ultimo_dia_periodo) * -1
            #Verifica se há status da conta na competencia
            competencia_date = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
            obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=contrato, tipo_prazo=tipo_prazo, data_competencia=competencia_date
            ).first()
            if obj_status_contrato_competencia != None:
                cod_status_auditoria_comp = obj_status_contrato_competencia.status
                obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status

        elif tipo_prazo == 'LP':
            cod_red = conta.cod_red_conta_contabil_lp
            cod_estrutura = conta.cod_estrut_lp
            val_composicao_ano_dic = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_vencimento__gte=ultimo_dia_ano) \
                .aggregate(sum_principal=Sum('val_principal'))
            val_composicao_ano = 0
            if val_composicao_ano_dic['sum_principal'] != None:
                val_composicao_ano = val_composicao_ano_dic['sum_principal']

            val_comp_pago_periodo_dic = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_vencimento__gte=ultimo_dia_ano, tipo_prazo='PG') \
                .aggregate(sum_principal=Sum('val_principal'))
            val_comp_pago_periodo = 0
            if val_comp_pago_periodo_dic['sum_principal'] != None:
                val_comp_pago_periodo = val_comp_pago_periodo_dic['sum_principal']

            val_composicao = val_composicao_ano - val_comp_pago_periodo

            val_balancete = ConexaoBancoBenner() \
                                .retorna_balancete_conta(conta.handle_conta_contabil_lp,
                                                         primeiro_dia_ano,
                                                         ultimo_dia_periodo) * -1

            #Verifica se há status da conta na competencia
            competencia_date = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
            obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=contrato, tipo_prazo=tipo_prazo, data_competencia=competencia_date
            ).first()
            if obj_status_contrato_competencia != None:
                cod_status_auditoria_comp = obj_status_contrato_competencia.status
                obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status



        val_dif_comp_bal = float(val_composicao) - val_balancete

        dados_conciliacao = {
            'cod_conta': conta.cod_conta,
            'cod_red': cod_red,
            'cod_estrutura': cod_estrutura,
            'desc_conta': conta.desc_conta,
            'cod_contrato': contrato.cod_contrato,
            'num_contrato': contrato.num_contrato,
            'doc_contabil': contrato.num_doc_contabil,
            'val_comp': locale.currency(round(val_composicao, 2), grouping=True, symbol=None),
            'val_balancete': locale.currency(round(val_balancete, 2), grouping=True, symbol=None),
            'val_dif_comp_balanc': locale.currency(round(val_dif_comp_bal, 2), grouping=True, symbol=None),
            'tipo_prazo': tipo_prazo,
            'cod_status_auditoria_comp': cod_status_auditoria_comp,
            'obs_status_auditoria_comp': obs_status_auditoria_comp,
        }

        return dados_conciliacao'''


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
        ultimo_dia_data_competencia_mais_12_meses_date = datetime(data_competencia_mais_12_meses.year, data_competencia_mais_12_meses.month,
                                       ultimo_dia_competencia_calendar)


        if tipo_prazo == 'CP':
            cod_red = conta.cod_red_conta_contabil_cp
            cod_estrutura = conta.cod_estrut_cp
            val_composicao_ano_dic = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_vencimento__range=[data_competencia_mais_um, ultimo_dia_data_competencia_mais_12_meses_date]) \
                .aggregate(sum_principal=Sum('val_principal'))

            val_parcelas_atrasadas = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_liquidacao__isnull=True, val_pago=0, data_vencimento__lte=data_competencia_mais_um) \
                .aggregate(sum_principal_parc_atrasadas=Sum('val_principal'))

            val_composicao_ano = 0
            if val_composicao_ano_dic['sum_principal'] != None:
                val_composicao_ano = val_composicao_ano_dic['sum_principal']

            if val_parcelas_atrasadas['sum_principal_parc_atrasadas'] != None:
                val_composicao_ano += val_parcelas_atrasadas['sum_principal_parc_atrasadas']


            val_composicao = val_composicao_ano
            '''if val_composicao < 0:
                val_composicao *= -1'''

            val_balancete = ConexaoBancoBenner() \
                                .retorna_balancete_conta(conta.handle_conta_contabil_cp,
                                                         primeiro_dia_ano,
                                                         ultimo_dia_periodo)
            '''if val_balancete < 0:
                val_balancete *= -1'''

            '''Verifica se há status da conta na competencia'''
            competencia_date = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
            obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=contrato, tipo_prazo=tipo_prazo, data_competencia=competencia_date
            ).first()
            if obj_status_contrato_competencia != None:
                cod_status_auditoria_comp = obj_status_contrato_competencia.status
                obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status

        elif tipo_prazo == 'LP':
            cod_red = conta.cod_red_conta_contabil_lp
            cod_estrutura = conta.cod_estrut_lp
            val_composicao_ano_dic = Parcela_Contrato.objects \
                .filter(cod_contrato=contrato, data_vencimento__gte=ultimo_dia_data_competencia_mais_12_meses_date) \
                .aggregate(sum_principal=Sum('val_principal'))
            val_composicao_ano = 0
            if val_composicao_ano_dic['sum_principal'] != None:
                val_composicao_ano = val_composicao_ano_dic['sum_principal']



            val_composicao = val_composicao_ano
            '''if val_composicao < 0:
                val_composicao *= -1'''

            val_balancete = ConexaoBancoBenner() \
                                .retorna_balancete_conta(conta.handle_conta_contabil_lp,
                                                         primeiro_dia_ano,
                                                         ultimo_dia_periodo)
            '''if val_balancete < 0:
                val_balancete *= -1'''

            '''Verifica se há status da conta na competencia'''
            competencia_date = datetime(int(competencia.split('-')[0]), int(competencia.split('-')[1]), 1)
            obj_status_contrato_competencia = Auditoria_Status_Composicao_Competencia.objects.filter(
                cod_contrato=contrato, tipo_prazo=tipo_prazo, data_competencia=competencia_date
            ).first()
            if obj_status_contrato_competencia != None:
                cod_status_auditoria_comp = obj_status_contrato_competencia.status
                obs_status_auditoria_comp = obj_status_contrato_competencia.obs_status

        val_dif_comp_bal = 0
        if val_balancete < 0:
            val_dif_comp_bal = float(val_composicao) + val_balancete
        else:
            val_dif_comp_bal = float(val_composicao) - val_balancete

        cod_anexo_competencia = 0
        obj_anexo_competencia = Anexos_Contrato.objects.filter(cod_contrato=contrato,
                                                               data_competencia=datetime.strptime(
                                                                   competencia + '-01', '%Y-%m-%d')).first()
        if obj_anexo_competencia != None:
            cod_anexo_competencia = obj_anexo_competencia.cod_anexo_contrato

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
        linha.append(cod_anexo_competencia) #13

        '''dados_conciliacao = {
            'cod_conta': conta.cod_conta,
            'cod_red': cod_red,
            'cod_estrutura': cod_estrutura,
            'desc_conta': conta.desc_conta,
            'cod_contrato': contrato.cod_contrato,
            'num_contrato': contrato.num_contrato,
            'doc_contabil': contrato.num_doc_contabil,
            'val_comp': locale.currency(round(val_composicao, 2), grouping=True, symbol=None),
            'val_balancete': locale.currency(round(val_balancete, 2), grouping=True, symbol=None),
            'val_dif_comp_balanc': locale.currency(round(val_dif_comp_bal, 2), grouping=True, symbol=None),
            'tipo_prazo': tipo_prazo,
            'cod_status_auditoria_comp': cod_status_auditoria_comp,
            'obs_status_auditoria_comp': obs_status_auditoria_comp,
            'cod_anexo_contrato_competencia': cod_anexo_competencia
        }'''

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

        obj_conta_pesq = Conta.objects.get(pk=cod_conta_form)
        msg = self.anexa_arq_conta(obj_conta_pesq, cod_contrato_form, competencia_doc_form, file_form, file_form.name)



        data = dict()
        data = {
            'cod_conta': obj_conta_pesq.cod_conta,
            'msg': msg
        }
        return JsonResponse(data, safe=False)


    def anexa_arq_conta(self, obj_conta_pesq, cod_contrato_form, competencia_doc_form, file_form, desc_doc_form):
        msg = ''
        obj_contrato_pesq = None
        ordem_max = 0
        ultimo_anexo_conta = 0
        obj_anexo_conta_pesq = None
        if obj_conta_pesq.tipo_modelo == 3:
            obj_contrato_pesq = Contrato.objects.get(pk=cod_contrato_form)

            ordem_max = Anexos_Contrato.objects \
                .filter(cod_contrato=obj_contrato_pesq) \
                .aggregate(max_odem_anexo=Max('ordem_anexo'))

            obj_anexo_conta_pesq = Anexos_Contrato.objects.filter(cod_contrato=obj_contrato_pesq,
                                                                  data_competencia=datetime.strptime(
                                                                      competencia_doc_form + '-01', '%Y-%m-%d')).first()
        else:
            ordem_max = Anexos_Contrato.objects \
                .filter(cod_conta=obj_conta_pesq) \
                .aggregate(max_odem_anexo=Max('ordem_anexo'))

            obj_anexo_conta_pesq = Anexos_Contrato.objects.filter(cod_conta=obj_conta_pesq,
                                                                  data_competencia=datetime.strptime(
                                                                      competencia_doc_form + '-01', '%Y-%m-%d')).first()

        if ordem_max['max_odem_anexo'] != None:
            ultimo_anexo_conta = ordem_max['max_odem_anexo'] + 1

        fs = FileSystemStorage()
        nome_arquivo = ''
        caminho_arq_importado = ''
        if type(file_form) == str:
            caminho_arq_importado = 'docs/contabil_composicao_app/anexos_conta/' + str(obj_conta_pesq.cod_conta) + '_' + \
                                    str(ultimo_anexo_conta) + '_' + desc_doc_form
            nome_arquivo = desc_doc_form
            shutil.move(file_form, 'media/'+caminho_arq_importado)
        else:
            nome_arquivo = file_form.name
            caminho_arq_importado = 'docs/contabil_composicao_app/anexos_conta/' + str(obj_conta_pesq.cod_conta) + '_' + \
                                    str(ultimo_anexo_conta) + '' + file_form.name.replace(' ', '_')
            filename = fs.save(caminho_arq_importado, file_form)
            uploaded_file_url = fs.url(filename)
        msg = ''

        if obj_anexo_conta_pesq == None:
            obj_anexo_conta = Anexos_Contrato(
                desc_anexo=nome_arquivo,
                data_competencia=competencia_doc_form + '-01',
                caminho_anexo=caminho_arq_importado,
                cod_contrato=obj_contrato_pesq,
                cod_conta=obj_conta_pesq,
                ordem_anexo=ultimo_anexo_conta
            ).save()
            msg = 'Doc anexado com sucesso !'
        else:
            arquivo_anterior_a_deletar = os.path.join(BASE_DIR, 'media\\' + str(obj_anexo_conta_pesq.caminho_anexo).replace('/', '\\'))
            os.remove(arquivo_anterior_a_deletar)

            obj_anexo_conta_pesq.desc_anexo = nome_arquivo
            obj_anexo_conta_pesq.caminho_anexo = caminho_arq_importado
            obj_anexo_conta_pesq.ordem_anexo = ultimo_anexo_conta
            obj_anexo_conta_pesq.save()
            msg = 'Registro atualizado com sucesso!'
        return msg

    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        obj_conta = Conta.objects.get(pk=cod_conta_form)

        lista_contratos = []
        lista_anexos = []
        if obj_conta.tipo_modelo == 1:
            lista_anexos = list(Anexos_Contrato.objects\
                .filter(cod_conta = obj_conta)\
                .values('cod_anexo_contrato', 'desc_anexo', 'caminho_anexo', 'data_competencia'))
        elif obj_conta.tipo_modelo == 3:
            lista_contratos = list(Contrato.objects.filter(cod_conta=obj_conta).values('cod_contrato', 'num_contrato'))
            lista_anexos = list(Anexos_Contrato.objects\
                .filter(cod_contrato__cod_conta = obj_conta)\
                .values('cod_contrato__num_contrato', 'cod_anexo_contrato', 'desc_anexo', 'caminho_anexo', 'data_competencia'))



        data = dict()
        data = {
            'lista_anexos': lista_anexos,
            'lista_contratos': lista_contratos
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
        caminho_completo = os.path.join(BASE_DIR,'media\\' + str(obj_anexo_conta.caminho_anexo).replace('/', '\\'))
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


class Form_Status_Contrato_Composicao_View(View):
    def get(self, request):
        cod_conta_form = request.GET['cod_conta']
        obj_conta = Conta.objects.get(pk=cod_conta_form)
        lista_status_contratos_comp = list(Auditoria_Status_Composicao_Competencia.objects\
            .filter(cod_conta=obj_conta).order_by('cod_contrato__cod_contrato', 'tipo_prazo', 'data_competencia')
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
        #lista_pacotes_conta = Pacote_Conta.objects.filter(cod_modelo=1)
        lista_contas = Conta.objects.filter(tipo_modelo=1, status_comp= 'A')
        context = {
            'lista_contas': lista_contas
            #'lista_pacotes_conta': lista_pacotes_conta
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
        #print(df_conteudo_arqv)
        obj_arqv_pesq = (Arquivo_Docs_Pac_Contas_Modelo_1.objects
                         .filter(
            nome_arqv_original = str(arquivo_form.name),
            cod_pacote_conta = obj_pac_conta,
            data_competencia = competencia_form + '-01')).first()
        if obj_arqv_pesq != None:
            lista_registros_arqv = None
            if obj_pac_conta.cod_pacote_conta == 3:
                lista_registros_arqv = Docs_Pac_Contas_Pagar_Receber_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 4:
                lista_registros_arqv = Docs_Pac_Estoque_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 5:
                lista_registros_arqv = Docs_Pac_Folha_Pag_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 6:
                lista_registros_arqv = Docs_Pac_Contas_Compensacao_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 7:
                lista_registros_arqv = Docs_Pac_Tributos_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 9:
                lista_registros_arqv = Docs_Pac_Finac_Disponib_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 10:
                lista_registros_arqv = Docs_Pac_Intercompany_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 11:
                lista_registros_arqv = Docs_Pac_Imobilizado_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            elif obj_pac_conta.cod_pacote_conta == 13:
                lista_registros_arqv = Docs_Pac_Consorcio_Ativo_M1_View.objects.filter(cod_arquivo=obj_arqv_pesq)
            for reg in lista_registros_arqv:
                reg.delete()

            obj_arqv_pesq.delete()
        msg = ''
        obj_arqv = None
        try:
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
                    data_venc = None
                    if row['Data Vencim.'] != '':
                        data_venc = row['Data Vencim.']

                    doc = Docs_Pac_Contas_Pagar_Receber_M1_View (
                        data_lancto=row['Data Lançto'],
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
                        cod_conta = Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                           cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo = obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 4:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Estoque_M1_View(
                        nome_almoxarifado=row['Nome Almoxarifado'],
                        cod_produto = row['Código Produto'],
                        desc_produto = row['Descrição Produto'],
                        qtd_prod = row['Qtd'],
                        custo_medio = row['Custo Médio'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        obs = row['Observação'],
                        cod_conta = Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                           cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo = obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 5:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Folha_Pag_M1_View(
                        data_lancto=row['Data Lançto'],
                        matricula = row['Matrícula'],
                        historico = row['Histórico'],
                        num_doc = row['Nº Documento'],
                        num_doc_contabil = row['Documento Contábil'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        obs = row['Observação'],
                        cod_conta = Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                           cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo = obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 6:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Contas_Compensacao_M1_View(
                        data_emissao = row['Data Emissão'],
                        data_entrada = row['Data Entrada'],
                        cnpj = row['CNPJ'],
                        nome_fornecedor = row['Nome Fornecedor'],
                        num_doc = row['Nº Documento'],
                        num_doc_contabil = row['Documento Contábil'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        obs = row['Observação'],
                        historico = row['Histórico'],
                        cod_conta = Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                           cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo = obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 7:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Tributos_M1_View(
                        data_emissao= row['Data Emissão'],
                        data_entrada = row['Data Entrada'],
                        nome_fornecedor = row['Nome Fornecedor'],
                        num_doc = row['Nº Documento'],
                        num_doc_contabil = row['Documento Contábil'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        obs = row['Observação'],
                        historico = row['Histórico'],
                        cod_conta = Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                           cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo = obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 9:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Finac_Disponib_M1_View(
                        num_doc = row['Nº Documento'],
                        data_lancto = row['Data Lançto'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        historico = row['Histórico'],
                        obs = row['Observação'],
                        cod_conta=Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                         cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo=obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 10:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Intercompany_M1_View(
                        num_doc=row['Nº Documento'],
                        data_lancto=row['Data Lançto'],
                        val_rel=row['Valor Relatório'],
                        val_razao=row['Valor Razão'],
                        val_dif=row['Diferença'],
                        historico=row['Histórico'],
                        obs=row['Observação'],
                        cod_conta=Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                         cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo=obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 11:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Imobilizado_M1_View(
                        data_entrada=row['Data Entrada'],
                        plaqueta = row['Plaqueta'],
                        desc_imobilizado = row['Descrição Imobilizado'],
                        val_aquisicao = row['Valor aquisição'],
                        num_doc = row['Nº Documento'],
                        nome_fornecedor = row['Nome Fornecedor'],
                        depreciacao_acum = row['Depreciação Acumulada'],
                        val_liq = row['Valor Liquido'],
                        taxa_depreciacao = row['Taxa Depreciação'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        obs = row['Observação'],
                        cod_conta=Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial=Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                         cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo=obj_arqv
                    ).save()
            elif obj_pac_conta.cod_pacote_conta == 13:
                for index, row in df_conteudo_arqv.iterrows():
                    doc = Docs_Pac_Consorcio_Ativo_M1_View(
                        historico = row['Histórico'],
                        num_doc = row['Nº Documento'],
                        data_lancto = row['Data Lançto'],
                        val_rel = row['Valor Relatório'],
                        val_razao = row['Valor Razão'],
                        val_dif = row['Diferença'],
                        obs = row['Observação'],
                        cod_conta = Conta.objects.get(pk=row['Cód. Conta']),
                        cod_filial = Filial.objects.filter(cod_reduzido=row['Nº Filial(Cód. Reduzido)'],
                                                           cod_empresa=obj_usu.cod_filial.cod_empresa).first(),
                        cod_arquivo = obj_arqv
                    ).save()
            msg = 'Arquivo importado com sucesso'
        except Exception as erro:
            obj_arqv.delete()
            traceback_str = traceback.format_exc()
            msg = f'Erro ao importar arquivo. Contate o desenvolvedor. Erro: {erro}!'
            print(traceback_str)




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

        lista_docs = None
        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
            lista_docs = list(Docs_Pac_Contas_Pagar_Receber_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_contas_pagar_receber', 'cod_filial__desc_filial','data_lancto',
                                      'cnpj', 'nome_fornecedor', 'num_doc', 'num_ap', 'data_venc', 'num_parc',
                                      'val_rel', 'val_razao', 'val_dif', 'obs'))
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
            lista_docs = list(Docs_Pac_Estoque_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_estoque', 'cod_filial__desc_filial', 'nome_almoxarifado',
                                      'cod_produto', 'desc_produto', 'qtd_prod', 'custo_medio', 'val_rel','val_razao',
                                      'val_dif', 'obs'))
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
            lista_docs = list(Docs_Pac_Folha_Pag_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_folha_pag', 'cod_filial__desc_filial', 'matricula', 'historico',
                                      'num_doc', 'num_doc_contabil', 'data_lancto',  'val_rel', 'val_razao', 'val_dif',
                                      'obs'))
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
            lista_docs = list(Docs_Pac_Contas_Compensacao_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_contas_compensacao', 'cod_filial__desc_filial', 'historico', 'cnpj',
                                      'nome_fornecedor', 'num_doc', 'num_doc_contabil', 'data_emissao', 'data_entrada',
                                      'val_rel', 'val_razao', 'val_dif', 'obs'))
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
            lista_docs = list(Docs_Pac_Tributos_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_tributos', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'num_doc_contabil', 'data_emissao', 'data_entrada',
                                      'val_rel', 'val_razao', 'val_dif', 'obs'))
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
            lista_docs = list(Docs_Pac_Finac_Disponib_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_financ_disp', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs'))
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
            lista_docs = list(Docs_Pac_Intercompany_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_intercompany', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs'))
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
            lista_docs = list(Docs_Pac_Imobilizado_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_imobilizado', 'data_entrada', 'cod_filial__desc_filial', 'plaqueta',
                                      'desc_imobilizado', 'val_aquisicao', 'num_doc', 'nome_fornecedor',
                                      'depreciacao_acum', 'val_liq', 'taxa_depreciacao', 'val_rel', 'val_razao',
                                      'val_dif', 'obs'))
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
                if doc['data_entrada'] != None:
                    doc['data_entrada'] = datetime.strftime(doc['data_entrada'], '%d-%m-%Y')

        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
            lista_docs = list(Docs_Pac_Consorcio_Ativo_M1_View.objects
                              .filter(cod_conta=obj_conta, cod_arquivo__data_competencia=competencia_form)
                              .values('cod_pac_doc_consorcio_ativo', 'cod_filial__desc_filial', 'historico',
                                      'num_doc', 'data_lancto', 'val_rel', 'val_razao', 'val_dif', 'obs'))
            for doc in lista_docs:
                if doc['val_rel'] != None:
                    doc['val_rel'] = locale.currency(round(float(doc['val_rel']), 2), grouping=True, symbol=None)
                if doc['val_razao'] != None:
                    doc['val_razao'] = locale.currency(round(float(doc['val_razao']), 2), grouping=True, symbol=None)
                if doc['val_dif'] != None:
                    doc['val_dif'] = locale.currency(round(float(doc['val_dif']), 2), grouping=True, symbol=None)
                if doc['data_lancto'] != None:
                    doc['data_lancto'] = datetime.strftime(doc['data_lancto'], '%d-%m-%Y')


        dados = dict()
        dados = {
            'lista_docs': lista_docs
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
        obj_conta = Conta.objects.get(pk=cod_conta_form)

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        registros_tabela = []
        if obj_conta.cod_pacote_conta.cod_pacote_conta == 3:
            registros_tabela = list(Docs_Pac_Contas_Pagar_Receber_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_contas_pagar_receber'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 4:
            registros_tabela = list(Docs_Pac_Estoque_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_estoque'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 5:
            registros_tabela = list(Docs_Pac_Folha_Pag_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_folha_pag'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 6:
            registros_tabela = list(Docs_Pac_Contas_Compensacao_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_contas_compensacao'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 7:
            registros_tabela = list(Docs_Pac_Tributos_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_tributos'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 9:
            registros_tabela = list(Docs_Pac_Finac_Disponib_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_financ_disp'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 10:
            registros_tabela = list(Docs_Pac_Intercompany_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_intercompany'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 11:
            registros_tabela = list(Docs_Pac_Imobilizado_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_imobilizado'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))
        elif obj_conta.cod_pacote_conta.cod_pacote_conta == 13:
            registros_tabela = list(Docs_Pac_Consorcio_Ativo_M1_View.objects.filter(cod_conta=obj_conta)
                              .values('cod_arquivo__cod_arquivo', 'cod_arquivo__data_imp',
                                      'cod_arquivo__nome_arqv_original', 'cod_arquivo__data_competencia',
                                      'cod_arquivo__cod_usu__login_usu')
                              .annotate(qtd_registros=Count('cod_pac_doc_consorcio_ativo'),
                                        tt_val_rel=Sum('val_rel'),
                                        tt_val_razao=Sum('val_razao')))

        if len(registros_tabela) > 0:
            for reg in registros_tabela:
                reg['cod_arquivo__data_imp'] = datetime.strftime(reg['cod_arquivo__data_imp'], '%Y-%m-%d')
                reg['tt_val_rel'] = locale.currency(round(reg['tt_val_rel'],2), grouping=True, symbol=None)
                reg['tt_val_razao'] = locale.currency(round(reg['tt_val_razao'], 2), grouping=True, symbol=None)

        dados = dict()
        dados = {
            'registros_tabela': registros_tabela
        }
        return JsonResponse(dados, safe=False)

    def delete(self, request, pk):
        obj_arquivo = self.get_object(pk.split('_')[0])
        obj_conta = Conta.objects.get(pk=pk.split('_')[1])
        cod_pacote = obj_conta.cod_pacote_conta.cod_pacote_conta
        if cod_pacote == 3:
            docs = Docs_Pac_Contas_Pagar_Receber_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 4:
            docs = Docs_Pac_Estoque_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 5:
            docs = Docs_Pac_Folha_Pag_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 6:
            docs = Docs_Pac_Contas_Compensacao_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 7:
            docs = Docs_Pac_Tributos_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 9:
            docs = Docs_Pac_Finac_Disponib_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 10:
            docs = Docs_Pac_Intercompany_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 11:
            docs = Docs_Pac_Imobilizado_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()

        elif cod_pacote == 13:
            docs = Docs_Pac_Consorcio_Ativo_M1_View.objects.filter(cod_conta=obj_conta, cod_arquivo=obj_arquivo)
            for doc in docs:
                doc.delete()


        data = dict()
        data = {
            'cod_conta': obj_conta.cod_conta,
            'msg': 'Registros da conta excluídos com sucesso!'
        }
        return JsonResponse(data, safe=False)



class Form_Composicao_Auditoria_View(View):
    def get(self, request):
        # lista_contas_benner = ConexaoBancoBenner().retorna_dados_contas()
        '''lista_contas_modelo_1 = (Auditoria_Status_Composicao_Competencia.objects.filter(tipo_prazo='m1')
                                 .values('cod_conta__cod_conta', 'cod_conta__desc_conta',
                                         'cod_conta__cod_red_conta_contabil_cp', 'cod_conta__cod_red_conta_contabil_lp'))'''
        contexto = {
            #'lista_contas_modelo_1': lista_contas_modelo_1,
            'desc_menu': 'Composição Auditoria'
        }
        return render(request, 'contabil_composicao_app/form_composicao_auditoria.html',
                      contexto)


class Form_Vincula_Resp_Contas_View(View):
    def get(self, request):
        lista_pacotes = Pacote_Conta.objects.all()

        contexto = {
            'lista_pacotes': lista_pacotes
        }
        return render(request, 'contabil_composicao_app/form_vincula_resp_contas.html', contexto)



class Importa_Anexos_Contas_View(View):
    def post(self, request):
        diretorio_arquivos_postados = 'media/docs/contabil_composicao_app/anexos_pendentes_importacao'
        lista_arquivos = os.listdir(diretorio_arquivos_postados)
        msg = ''
        for arq in lista_arquivos:
            caminho_arq = 'media/docs/contabil_composicao_app/anexos_pendentes_importacao/' + arq
            cod_conta = arq.split('_')[0]
            cod_contrato = arq.split('_')[1]
            competencia_str = arq.split('_')[3].split('.')[0] + '-' + arq.split('_')[2]
            obj_conta = Conta.objects.get(pk=cod_conta)
            obj_contrato = None
            cod_contrato_param = ''
            if obj_conta.tipo_modelo == 1:
                cod_contrato_param = cod_contrato
            else:
                obj_contrato = Contrato.objects.filter(cod_conta=obj_conta, num_contrato=cod_contrato).first()
                cod_contrato_param = obj_contrato.cod_contrato
            obj_form_anexos_conta_view = Form_Anexos_Conta_View()
            msg = obj_form_anexos_conta_view.anexa_arq_conta(obj_conta, cod_contrato_param, competencia_str, caminho_arq, arq)
            #os.remove(os.path.join(diretorio_arquivos_postados, arq))

        diretorio_arquivos_postados = 'media/docs/contabil_composicao_app/anexos_pendentes_importacao'
        lista_arquivos = os.listdir(diretorio_arquivos_postados)
        qtd_arquivos_postados = len(lista_arquivos)

        data = dict()
        data = {
            'msg': msg,
            'qtd_arquivos_postados': qtd_arquivos_postados
        }
        return JsonResponse(data, safe=False)



class Form_Doc_Pac_Modelo_1_View(View):
    def get(self, request):
        dic_pacotes = Pacote_Conta.objects.filter(cod_modelo=1)
        contexto = {
            'dic_pacotes': dic_pacotes
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
        lista_parcelas_atualizadas_form = []
        for cod_conta in lista_cod_contas.split(','):
            obj_conta = Conta.objects.get(pk=cod_conta)
            lista_contratos_para_atualizar = (Parcela_Contrato.objects
                                                 .filter(data_liquidacao__isnull=True,
                                                         cod_contrato__cod_conta=obj_conta,
                                                         cod_contrato__sincronizar_benner='S')
                                              .values('cod_contrato__num_contrato').distinct())



            for contrato in lista_contratos_para_atualizar:
                lista_parcelas_atualizadas = Form_Imp_Contratos_Conta_View().\
                    atualiza_dados_contratos_parcelas(obj_conta.cod_conta, contrato['cod_contrato__num_contrato'],
                                                                                  'C')[2]
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


