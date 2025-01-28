import decimal
import locale

from django.db.models import Sum
from datetime import datetime

from apps.plan_controle_fat_2art_terc_app.models import Registro2ArtTerceirosFinanceiro, BeneficiarioTerceiro, \
    LancamentosRegistro2ArtTerceirosFinanceiro, HistAcaoMapas2ArtTerceiros


class Uteis():
    def tab_2art_comparacao_tab_terceiros(self, cod_projeto, data_inicial, data_final, cod_beneficiario,
                                          check_mapas_ativos):
        lista_registros = []
        #data_inicial_str = data_inicial[6:10 ] +'-' +data_inicial[3:5 ] +'-' +data_inicial[0:2]
        #data_final_str = data_final[6:10 ] +'-' +data_final[3:5 ] +'-' +data_final[0:2]
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        if cod_beneficiario == '0':
            registros_tab_terceiros = Registro2ArtTerceirosFinanceiro.objects.filter(
                cod_projeto__cod_projeto = cod_projeto, data_2art_terc_financ__range=[data_inicial ,data_final],
                status_mapa_2art_terc_financ=check_mapas_ativos)
        else:
            obj_beneficiario = BeneficiarioTerceiro.objects.filter(cod_benef_terc=cod_beneficiario).first()
            registros_tab_terceiros = Registro2ArtTerceirosFinanceiro.objects.filter(
                cod_projeto__cod_projeto = cod_projeto, data_2art_terc_financ__range=[data_inicial ,data_final],
                cod_cad_placa_terc__cod_benef_terc=obj_beneficiario, status_mapa_2art_terc_financ=check_mapas_ativos)
        for reg_ter in registros_tab_terceiros:
            nome_beneficiario = 'Inexistente'
            tipo_pessoa = 'Inexistente'
            perfil_veic = 'Inexistente'
            val_calc_mapa = 0.00
            val_pagar_terc = 0.00
            val_pagar_conlog = 0.00
            val_total_desc_mapa = 0.00
            lanc_desc_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects\
                .filter(cod_reg_2art_terc_financ=reg_ter, tipo_lancamento='D', status_exclusao='N')\
                .aggregate(total_valor_lanc=Sum('valor_lanc'))
            if lanc_desc_mapa['total_valor_lanc'] is not None:
                val_total_desc_mapa = lanc_desc_mapa['total_valor_lanc']
            val_total_acres_mapa = 0.00
            lanc_acres_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects\
                .filter(cod_reg_2art_terc_financ=reg_ter, tipo_lancamento='A', status_exclusao='N')\
                .aggregate(total_valor_lanc=Sum('valor_lanc'))
            if lanc_acres_mapa['total_valor_lanc'] is not None:
                val_total_acres_mapa = lanc_acres_mapa['total_valor_lanc']

            if reg_ter.cod_cad_placa_terc is not None:
                nome_beneficiario = reg_ter.cod_cad_placa_terc.cod_benef_terc.nome_benef_terc
                tipo_pessoa = reg_ter.cod_cad_placa_terc.cod_benef_terc.tipo_pessoa_benef_terc
            else:
                nome_beneficiario = 'Placa não cadastrada'
                tipo_pessoa = 'Placa não cadastrada'

            if reg_ter.cod_cad_frete_spot is not None:
                if float(reg_ter.entregas_2art_terc_financ) <= reg_ter.cod_cad_frete_spot.qtd_min:
                    val_calc_mapa = reg_ter.cod_cad_frete_spot.val_frete_carreteiro_min + \
                                    reg_ter.cod_cad_frete_spot.val_descarga_min + \
                                    reg_ter.cod_cad_frete_spot.val_pedagio_min + \
                                    reg_ter.cod_cad_frete_spot.val_cprb_min + reg_ter.cod_cad_frete_spot.val_lucro_min
                    val_pagar_terc = reg_ter.cod_cad_frete_spot.val_frete_carreteiro_min + \
                                     reg_ter.cod_cad_frete_spot.val_descarga_min + \
                                     reg_ter.cod_cad_frete_spot.val_pedagio_min

                elif float(reg_ter.entregas_2art_terc_financ) >= reg_ter.cod_cad_frete_spot.qtd_max:
                    val_calc_mapa = reg_ter.cod_cad_frete_spot.val_frete_carreteiro_max + \
                                    reg_ter.cod_cad_frete_spot.val_descarga_max + \
                                    reg_ter.cod_cad_frete_spot.val_pedagio_max + \
                                    reg_ter.cod_cad_frete_spot.val_cprb_max + reg_ter.cod_cad_frete_spot.val_lucro_max
                    val_pagar_terc = reg_ter.cod_cad_frete_spot.val_frete_carreteiro_max + \
                                     reg_ter.cod_cad_frete_spot.val_descarga_max + \
                                     reg_ter.cod_cad_frete_spot.val_pedagio_max

            val_pagar_terc = (decimal.Decimal(val_pagar_terc) + decimal.Decimal(val_total_acres_mapa)) - \
                             decimal.Decimal(val_total_desc_mapa)
            
            val_pagar_conlog = decimal.Decimal(str(reg_ter.valorfrete_2art_terc_financ).replace(',','.')) - val_pagar_terc

            calc_dif_frete_val_calc = decimal.Decimal(str(reg_ter.valorfrete_2art_terc_financ).replace(',','.')) - \
                                      decimal.Decimal(val_calc_mapa)
            val_dif_frete_val_calc = 0.00
            if calc_dif_frete_val_calc > 0.1 or calc_dif_frete_val_calc < -0.5:
                val_dif_frete_val_calc = calc_dif_frete_val_calc

            cod_serial_pagamento = 0
            if reg_ter.cod_pag_2art_terc_financ is not None:
                #cod_serial_pagamento = str(reg_ter.cod_pag_2art_terc_financ.cod_pag_2art_terc_financ ) +'- ' +reg_ter.cod_projeto.cod_serial_pag_terc
                cod_serial_pagamento = str(
                    reg_ter.cod_pag_2art_terc_financ.num_doc_pagamento) + '- ' + reg_ter.cod_projeto.cod_serial_pag_terc


            '''Retorna o último histórico da acao Ativa/Desativa mapa'''
            motivo_acao_mapa = '(Última ação: '
            obj_acao_ativa_desativa_mapa = (HistAcaoMapas2ArtTerceiros.objects
                                            .filter(cod_reg_2art_terc_financ=reg_ter).last())
            if obj_acao_ativa_desativa_mapa != None:
                motivo_acao_mapa += obj_acao_ativa_desativa_mapa.obs_hist_acao_mapa_terc + ')'


            reg_tec_tab = Tab_Dados_Terc_Ultimo_2Art(
                cod_idreg2arttercfinanc = reg_ter.cod_reg_2art_terc_financ,
                data = datetime.strftime(reg_ter.data_2art_terc_financ ,'%d-%m-%y'),
                mapa = reg_ter.mapa_2art_terc_financ,
                placa_reg_terc = reg_ter.placa_2art_terc_financ,
                tipo_entrega_reg_terc = reg_ter.entrega_2art_terc_financ,
                nome_doc_beneficiorio = nome_beneficiario,
                tipo_pessoa = tipo_pessoa,
                perfil_veic_reg_terc = reg_ter.nomespot_2art_terc_financ,
                regiao_reg_terc = reg_ter.regiaospot_2art_terc_financ,
                qtd_entr_reg_terc = reg_ter.entregas_2art_terc_financ,
                tipo_imp_reg_terc = reg_ter.tipoimposto_2art_terc_financ,
                perc_imposto_reg_terc = round(float(str(reg_ter.percimposto_2art_terc_financ).replace(',','.')),2),
                val_frete_reg_terc = round(float(str(reg_ter.valorfrete_2art_terc_financ).replace(',','.')),2),
                val_calculado = round(float(val_calc_mapa),2),
                diferenca = locale.currency(round(val_dif_frete_val_calc,2), grouping=True, symbol=None),
                val_faturado_reg_terc = round(float(reg_ter.cod_reg_2art.valorfaturado),2),
                desconto = round(float(val_total_desc_mapa),2),
                acrescimo = round(float(val_total_acres_mapa),2),
                val_pagar = round(float(val_pagar_terc),2),
                val_conlog = round(float(val_pagar_conlog),2),
                placa_reg_2art = reg_ter.cod_reg_2art.placa,
                tipo_entrega_2art = reg_ter.cod_reg_2art.entrega,
                perfil_veic_2art = reg_ter.cod_reg_2art.nomespot,
                regiao_2art = reg_ter.cod_reg_2art.regiaospot,
                qtd_entr_2art = reg_ter.cod_reg_2art.entregas,
                tipo_imp_2art = reg_ter.cod_reg_2art.tipoimposto,
                perc_imposto_2art = round(float(reg_ter.cod_reg_2art.percimposto),2),
                val_frete_2art = round(float(reg_ter.cod_reg_2art.valorfrete),2),
                val_faturado_2art = round(float(reg_ter.cod_reg_2art.valorfaturado),2),
                status_mapa = reg_ter.status_mapa_2art_terc_financ,
                status_financeiro = reg_ter.status_financeiro_2art_terc_financ,
                id_pagamento_serial = cod_serial_pagamento,
                motivo_ultima_acao_mapa=motivo_acao_mapa
            )
            lista_registros.append(reg_tec_tab.__dict__)
        return lista_registros


    def tab_2art_terc_agrupado_por_beneficiario(self, cod_projeto, data_inicial, data_final):
        lista_registros_tab_2art_agrupado_benef = []
        mapas_2art_terc_periodo = Registro2ArtTerceirosFinanceiro.objects\
            .filter(cod_projeto__cod_projeto = cod_projeto,
                 data_2art_terc_financ__range=[data_inicial ,data_final],
                 status_mapa_2art_terc_financ='S', status_financeiro_2art_terc_financ='A',
                 cod_pag_2art_terc_financ__isnull=True, cod_cad_placa_terc__isnull=False)

        lista_beneficiarios_tab_2art_terc_periodo = mapas_2art_terc_periodo\
            .values('cod_cad_placa_terc__cod_benef_terc').distinct()
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        if lista_beneficiarios_tab_2art_terc_periodo != None:
            for cod_benef in lista_beneficiarios_tab_2art_terc_periodo:
                obj_beneficiario = BeneficiarioTerceiro.objects\
                    .filter(cod_benef_terc=cod_benef['cod_cad_placa_terc__cod_benef_terc']).first()
                mapas_do_beneficiario = mapas_2art_terc_periodo.filter(
                    cod_cad_placa_terc__cod_benef_terc__cod_benef_terc=cod_benef['cod_cad_placa_terc__cod_benef_terc'])
                qtd_mapas = mapas_do_beneficiario.count()
                val_tt_frete = mapas_do_beneficiario.aggregate(total_valor_frete=Sum('valorfrete_2art_terc_financ'))
                val_tt_faturado = mapas_do_beneficiario.aggregate(
                    total_valor_faturado=Sum('valorfaturado_2art_terc_financ'))

                val_tt_desc = 0.00
                val_tt_acres = 0.00
                val_tt_calc = 0.00
                val_tt_pagar_benef = 0.00
                val_tt_conlog = 0.00
                cod_mapas_selecionados_do_beneficiario = []
                for reg in mapas_do_beneficiario:
                    #val_total_desc_mapa = 0.00
                    lanc_desc_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art_terc_financ=reg.cod_reg_2art_terc_financ,
                        tipo_lancamento='D',
                        status_exclusao='N').aggregate(total_valor_lanc=Sum('valor_lanc'))
                    if lanc_desc_mapa['total_valor_lanc'] is not None:
                        val_tt_desc = decimal.Decimal(val_tt_desc) + decimal.Decimal(lanc_desc_mapa['total_valor_lanc'])

                    lanc_acres_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(
                        cod_reg_2art_terc_financ=reg.cod_reg_2art_terc_financ,
                        tipo_lancamento='A', status_exclusao='N').aggregate(
                        total_valor_lanc=Sum('valor_lanc'))
                    if lanc_acres_mapa['total_valor_lanc'] is not None:
                        val_tt_acres = decimal.Decimal(val_tt_acres) + \
                                       decimal.Decimal(lanc_acres_mapa['total_valor_lanc'])

                    val_calc_mapa = 0.00
                    val_pagar_terc = 0.00
                    val_conlog_mapa = 0.00
                    if reg.cod_cad_frete_spot is not None:
                        if int(reg.entregas_2art_terc_financ) <= reg.cod_cad_frete_spot.qtd_min:
                            val_calc_mapa = reg.cod_cad_frete_spot.val_frete_carreteiro_min + \
                                            reg.cod_cad_frete_spot.val_descarga_min + \
                                            reg.cod_cad_frete_spot.val_pedagio_min + \
                                            reg.cod_cad_frete_spot.val_cprb_min + \
                                            reg.cod_cad_frete_spot.val_lucro_min
                            val_pagar_terc = reg.cod_cad_frete_spot.val_frete_carreteiro_min + \
                                             reg.cod_cad_frete_spot.val_descarga_min + \
                                             reg.cod_cad_frete_spot.val_pedagio_min

                        elif int(reg.entregas_2art_terc_financ) >= reg.cod_cad_frete_spot.qtd_max:
                            val_calc_mapa = reg.cod_cad_frete_spot.val_frete_carreteiro_max + \
                                            reg.cod_cad_frete_spot.val_descarga_max + \
                                            reg.cod_cad_frete_spot.val_pedagio_max + \
                                            reg.cod_cad_frete_spot.val_cprb_max + \
                                            reg.cod_cad_frete_spot.val_lucro_max
                            val_pagar_terc = reg.cod_cad_frete_spot.val_frete_carreteiro_max + \
                                             reg.cod_cad_frete_spot.val_descarga_max + \
                                             reg.cod_cad_frete_spot.val_pedagio_max

                        val_tt_calc = decimal.Decimal(val_tt_calc) + decimal.Decimal(val_calc_mapa)
                        val_tt_pagar_benef = decimal.Decimal(val_tt_pagar_benef) + decimal.Decimal(val_pagar_terc)
                        val_conlog_mapa = round(float(reg.valorfrete_2art_terc_financ) - float(val_pagar_terc),2)
                    cod_mapas_selecionados_do_beneficiario.append(str(reg.cod_reg_2art_terc_financ)+'_'+
                                                                  str(val_calc_mapa)+'_'+str(round(val_pagar_terc,2))+
                                                                  '_'+str(round(val_conlog_mapa,2)))
                valor_total_frete = val_tt_frete['total_valor_frete']
                if val_tt_frete['total_valor_frete'] == None:
                    valor_total_frete = 0.00
                val_tt_conlog = decimal.Decimal(round(valor_total_frete,2))  - decimal.Decimal(val_tt_pagar_benef)
                valor_total_faturado = val_tt_faturado['total_valor_faturado']
                if val_tt_faturado['total_valor_faturado'] == None:
                    valor_total_faturado = 0.00
                reg_tab_2art_agrupado_benef = Tab_2Art_Agrupado_Beneficiario(
                    cod_2art_terc_financ = cod_mapas_selecionados_do_beneficiario,
                    cod_beneficiario = obj_beneficiario.cod_benef_terc,
                    nome_beneficiario = obj_beneficiario.nome_benef_terc,
                    qtd_mapas = qtd_mapas,
                    val_tt_frete = round(float(valor_total_frete),2),
                    val_ff_calc = round(float(val_tt_calc),2),
                    val_tt_fat = round(float(valor_total_faturado),2),
                    val_tt_acres = round(float(val_tt_acres),2),
                    val_tt_desc = round(float(val_tt_desc),2),
                    val_tt_pagar = locale.currency(round((decimal.Decimal(val_tt_pagar_benef) -
                                                          decimal.Decimal(val_tt_desc)) +
                                                         decimal.Decimal(val_tt_acres),2),grouping=True, symbol=None),
                    val_tt_conlog = round(float(val_tt_conlog),2)
                )
                lista_registros_tab_2art_agrupado_benef.append(reg_tab_2art_agrupado_benef.__dict__)
        return lista_registros_tab_2art_agrupado_benef


    def retorna_lancamentos_mapa_2art_terc_financ(self, id_reg_2art_terc_financ):
        obj_reg_2art_terc_finan = Registro2ArtTerceirosFinanceiro.objects.filter(cod_reg_2art_terc_financ=id_reg_2art_terc_financ).first()
        lista_lancamentos_mapa = LancamentosRegistro2ArtTerceirosFinanceiro.objects.filter(cod_reg_2art_terc_financ=obj_reg_2art_terc_finan, status_exclusao='N')
        lista_lancamentos_mapa_tab = []
        if lista_lancamentos_mapa is not None:
            for reg in lista_lancamentos_mapa:
                obj = Tab_Lancamentos_2Art_Terc_Financ_Mapa(
                    id_registro_bd=reg.cod_lanc_2art_terc_financ,
                    tipo_lanc=reg.tipo_lancamento,
                    desc_ocorrencia=reg.cod_tipo_ocor_financ_terc.desc_ocorrencia,
                    data_ocorrencia=datetime.strftime(reg.data_ocorrencia, '%d-%m-%y'),
                    mapa_ocorrencia=reg.mapa_ocorrencia,
                    placa_lanc=reg.placa_lanc,
                    valor=round(float(reg.valor_lanc),2),
                    obs=reg.obs_lanc
                )
                lista_lancamentos_mapa_tab.append(obj.__dict__)
        return lista_lancamentos_mapa_tab



class Tab_Dados_Terc_Ultimo_2Art():
    def __init__(self, cod_idreg2arttercfinanc,  data, mapa, placa_reg_terc, tipo_entrega_reg_terc, nome_doc_beneficiorio, tipo_pessoa, perfil_veic_reg_terc, regiao_reg_terc, qtd_entr_reg_terc,
        tipo_imp_reg_terc, perc_imposto_reg_terc, val_frete_reg_terc,  val_calculado, diferenca, val_faturado_reg_terc, desconto, acrescimo, val_pagar, val_conlog,
        placa_reg_2art, tipo_entrega_2art, perfil_veic_2art, regiao_2art, qtd_entr_2art, tipo_imp_2art, perc_imposto_2art, val_frete_2art,val_faturado_2art, status_mapa, status_financeiro,
        id_pagamento_serial, motivo_ultima_acao_mapa):

        self.cod_idreg2arttercfinanc = cod_idreg2arttercfinanc
        self.data = data
        self.mapa = mapa
        self.placa_reg_terc = placa_reg_terc
        self.tipo_entrega_reg_terc = tipo_entrega_reg_terc
        self.nome_doc_beneficiorio = nome_doc_beneficiorio
        self.tipo_pessoa = tipo_pessoa
        self.perfil_veic_reg_terc = perfil_veic_reg_terc
        self.regiao_reg_terc = regiao_reg_terc
        self.qtd_entr_reg_terc = qtd_entr_reg_terc
        self.tipo_imp_reg_terc = tipo_imp_reg_terc
        self.perc_imposto_reg_terc = perc_imposto_reg_terc
        self.val_frete_reg_terc = val_frete_reg_terc
        self.val_calculado = val_calculado
        self.diferenca = diferenca
        self.val_faturado_reg_terc = val_faturado_reg_terc
        self.desconto = desconto
        self.acrescimo = acrescimo
        self.val_pagar = val_pagar
        self.val_conlog = val_conlog
        self.placa_reg_2art = placa_reg_2art
        self.tipo_entrega_2art = tipo_entrega_2art
        self.perfil_veic_2art = perfil_veic_2art
        self.regiao_2art = regiao_2art
        self.qtd_entr_2art = qtd_entr_2art
        self.tipo_imp_2art = tipo_imp_2art
        self.perc_imposto_2art = perc_imposto_2art
        self.val_frete_2art = val_frete_2art
        self.val_faturado_2art = val_faturado_2art
        self.status_mapa = status_mapa
        self.status_financeiro = status_financeiro
        self.id_pagamento_serial = id_pagamento_serial
        self.motivo_ultima_acao_mapa = motivo_ultima_acao_mapa


class Tab_2Art_Agrupado_Beneficiario():
    def __init__(self, cod_2art_terc_financ, cod_beneficiario,  nome_beneficiario, qtd_mapas, val_tt_frete, val_ff_calc, val_tt_fat, val_tt_acres, val_tt_desc, val_tt_pagar, val_tt_conlog):
        self.cod_2art_terc_financ = cod_2art_terc_financ
        self.cod_beneficiario = cod_beneficiario
        self.nome_beneficiario = nome_beneficiario
        self.qtd_mapas = qtd_mapas
        self.val_tt_frete = val_tt_frete
        self.val_ff_calc = val_ff_calc
        self.val_tt_fat = val_tt_fat
        self.val_tt_acres = val_tt_acres
        self.val_tt_desc = val_tt_desc
        self.val_tt_pagar = val_tt_pagar
        self.val_tt_conlog = val_tt_conlog


class Tab_Lancamentos_2Art_Terc_Financ_Mapa():
    def __init__(self, id_registro_bd, tipo_lanc, desc_ocorrencia, data_ocorrencia, mapa_ocorrencia, placa_lanc, valor, obs):
        self.id_registro_bd = id_registro_bd
        self.tipo_lanc = tipo_lanc
        self.desc_ocorrencia = desc_ocorrencia
        self.data_ocorrencia = data_ocorrencia
        self.mapa_ocorrencia = mapa_ocorrencia
        self.placa_lanc = placa_lanc
        self.valor = valor
        self.obs = obs