import locale
from datetime import datetime

import pyodbc
import pandas as pd
from django.shortcuts import render

from apps.benner_app.models import Placa_Beneficiario_Terceiro, Empilhadeira, Ordens_Servico, Familia, Compras_Item, \
    Produto, Empresa_Benner, Operacao_Benner, Filial_Benner, Projeto_Benner, Beneficiario_Terceiro, \
    Requisicao_Atendidas_TMA
from apps.frota_disponibilidade_empilhadeira_app.models import OS_Apontamento_Disp_Empilhadeira
from apps.suprimentos_evolucao_precos_app.models import Compra_Auditada


class ConexaoBancoBenner():
    def __init__(self):
        self.__conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ITJM-SRV-018;'
            'DATABASE=TRANSPORTES_PRODUCAO;'
            'UID=servico.portais;'
            'PWD=qm@WHpAWwb;'
        )

    def retorna_dados_placa_benef_a_sincronizar(self, handle_proj, placa, perfil):
        '''Objeto a retornar'''
        lista_placa_benef = []

        '''Processamento'''
        cursor = self.__conn.cursor()
        sql_placa_benef = (
            '''
            SELECT  DISTINCT
                    gn_p.handle     AS  handle_benef,
                    gn_p.nome       AS  nome_benef,
                    gn_p.tipo       AS  tipo_pessoa,
                    gn_p.inativo    AS  status_pessoa,
                    gn_p.CGCCPF     AS  doc_benef,
                    ma.handle       AS  handle_placa,
                    ma.codigo       AS  placa,
                    ma.inativo      AS  status_placa
              FROM  gn_pessoas gn_p (NOLOCK)
             RIGHT  JOIN ma_recursos ma (NOLOCK)
                ON  (ma.proprietario = gn_p.handle)
             WHERE  ma.projeto = 
            '''
            + str(handle_proj) +
            "   AND ma.CODIGO = '" + placa + "' "
        )
        cursor.execute(sql_placa_benef)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            reg = Placa_Beneficiario_Terceiro(row.handle_benef, row.nome_benef, row.tipo_pessoa, row.status_pessoa,
                                              row.doc_benef, row.handle_placa, row.placa, row.status_placa, perfil, '')
            lista_placa_benef.append(reg)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_placa_benef

    def retorna_dados_contas(self):
        '''Objeto a retornar'''
        lista_contas_benner = []

        '''Processamento'''
        cursor = self.__conn.cursor()
        sql_contas = (
            '''
            SELECT	DISTINCT
                    ct_con_lp.NOME 	AS	desc_conta	                 
            FROM	CT_CONTAS ct_con_lp (NOLOCK) 
            LEFT	JOIN FN_CONTACONTASCONTABEIS fn_con_lp (NOLOCK) 
              ON	(fn_con_lp.CONTACONTABIL = ct_con_lp.HANDLE)   
           WHERE	ct_con_lp.ULTIMONIVEL = 'S'              
             AND    ct_con_lp.EMPRESA in (12, 17)
             AND	fn_con_lp.CONTAFINANCEIRA IS NOT NULL
             AND	ct_con_lp.INICIOINATIVIDADE IS null;
            '''
        )

        cursor.execute(sql_contas)
        registros_cursor = cursor.fetchall()

        for row in registros_cursor:
            nome_empresa = ''
            if row.cod_empresa == 12:
                nome_empresa = 'Conlog'
            elif row.cod_empresa == 17:
                nome_empresa = 'Deep'

            handle_conta_contabil_cp = 0
            cod_red_conta_contabil_cp = 0
            cod_estrut_cp = 0
            handle_conta_financeira_cp = 0
            if row.dados_conta_curto_prazo != None:
                handle_conta_contabil_cp = row.dados_conta_curto_prazo.split('_')[0]
                cod_red_conta_contabil_cp = row.dados_conta_curto_prazo.split('_')[1]
                cod_estrut_cp = row.dados_conta_curto_prazo.split('_')[2]
                handle_conta_financeira_cp = row.dados_conta_curto_prazo.split('_')[3]

            handle_conta_contabil_lp = 0
            cod_red_conta_contabil_lp = 0
            cod_estrut_lp = 0
            handle_conta_financeira_lp = 0
            if row.dados_conta_longo_prazo != None:
                handle_conta_contabil_lp =  row.dados_conta_longo_prazo.split('_')[0]
                cod_red_conta_contabil_lp = row.dados_conta_longo_prazo.split('_')[1]
                cod_estrut_lp = row.dados_conta_longo_prazo.split('_')[2]
                handle_conta_financeira_lp = row.dados_conta_longo_prazo.split('_')[3]

            conta = {
                'desc': row.desc_conta
            }
            lista_contas_benner.append(conta)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_contas_benner

    def retorna_dados_contratos_conta(self, tipo_pesquisa, num_contrato, handle_conta_cp, handle_conta_lp, cod_empresa):
        '''Objeto a retornar'''
        lista_contratos_conta_benner = []

        '''Processamento'''
        cursor = self.__conn.cursor()
        param_num_contrato = ''
        if tipo_pesquisa == 'C':
            param_num_contrato = f" AND fn_doc.DOCUMENTODIGITADO = '{num_contrato}' "
        sql_contratos = (
            f'''
            SELECT	distinct
                    fn_doc.HANDLE					    AS	handle_fn_doc,
                    fn_doc.DOCUMENTODIGITADO	        AS	num_contrato,
                    CAST(fn_doc.DATAEMISSAO AS DATE)    AS	data_emissao_contrato,
                    fn_doc.VALORNOMINAL			        AS	val_nominal,
                    fn_doc.VALORLIQUIDO			        AS	val_liquido,                    
                    fornec.NOME						    AS	fornecedor,
                    gn_op.NOME                          AS  nome_operacao,
                    gn_op.HANDLE                        AS  handle_operacao,
                    gn_op.CODIGOREDUZIDO			    AS	cod_red_operacao,
                    fn_doc.DOCUMENTOCONTABIL	        AS	doc_contabil,
                    fn_doc.EMPRESA                      AS  cod_empresa,
                    (SELECT TOP 1 ordem.PARCELADIGITADA
                       FROM	FN_PARCELAS ordem (NOLOCK)
                      WHERE	ordem.DOCUMENTO = fn_doc.handle
							   AND	ordem.DATALIQUIDACAO IS null
								ORDER BY ordem.handle ASC)
                                                        AS	proxima_parc_pendente,
                    (SELECT TOP 1 CAST(ordem.DATAVENCIMENTO AS DATE)
                       FROM	FN_PARCELAS ordem (NOLOCK)
                      WHERE	ordem.DOCUMENTO = fn_doc.handle
							   AND	ordem.DATALIQUIDACAO IS null
								ORDER BY ordem.handle ASC) 
                                                        AS	data_venc_proxima_parc_pendente,
                  	(SELECT SUM(fn_mov_par_pagas.VALORTOTAL)
					   FROM FN_MOVIMENTACOES fn_mov_par_pagas (NOLOCK)
					  WHERE fn_mov_par_pagas.DOCUMENTO = fn_doc.handle
					    AND	fn_mov_par_pagas.tipomovimento = 1
						AND	fn_mov_par_pagas.AUTORIZACAOPAGAMENTO IS NOT NULL)
                    				                    AS	total_pago,
                    (SELECT TOP 1 ordem.VALOR
                       FROM	FN_PARCELAS ordem (NOLOCK)
                      WHERE	ordem.DOCUMENTO = fn_doc.handle
							   AND	ordem.DATALIQUIDACAO IS null
								ORDER BY ordem.handle ASC)
                                                        AS	val_proxima_parc_pendente,
                    COUNT(DISTINCT fn_parc.handle) 		AS  qtd_parc                                                         
              FROM	FN_DOCUMENTOS fn_doc (NOLOCK)
              LEFT	JOIN FN_PARCELAS fn_parc (NOLOCK) 
                 ON	fn_parc.DOCUMENTO = fn_doc.HANDLE
              LEFT	JOIN GN_PESSOAS fornec (NOLOCK) 
                ON	fn_doc.PESSOA = fornec.HANDLE 
              LEFT	JOIN GN_OPERACOES gn_op (NOLOCK) 
                ON	gn_op.HANDLE = fn_doc.OPERACAO 
              LEFT	JOIN FN_LANCAMENTOS fn_lan (NOLOCK) 
                ON	fn_lan.PARCELA = fn_parc.HANDLE 
              LEFT	JOIN FN_CONTAS fn_con (NOLOCK) 
                ON	fn_con.HANDLE = fn_lan.CONTA
              LEFT  JOIN FN_CONTACONTASCONTABEIS ct_con
                ON  (ct_con.CONTAFINANCEIRA = fn_con.HANDLE) 
              LEFT	JOIN FN_MOVIMENTACOES fn_mov (NOLOCK)
                ON	(fn_mov.DOCUMENTO = fn_doc.HANDLE
                AND	fn_mov.tipomovimento = 1
                AND	fn_mov.AUTORIZACAOPAGAMENTO IS NOT NULL)
             WHERE	1 = 1
               AND	fn_doc.ENTRADASAIDA IN ('E','I')
               AND	fn_doc.TIPODEMOVIMENTO IN(1,2)
               AND	fn_parc.PREVISAO = 'N'
               AND	fn_parc.VALOR > 0
               AND	fn_doc.ABRANGENCIA <> 'R'
               AND	fn_lan.TIPO = '3'
               AND 	fn_lan.ORIGEM = 2
               AND	((fn_doc.DATACANCELAMENTO IS NULL) OR(fn_doc.DATACANCELAMENTO > CONVERT(DATETIME,'20221231',103)))
               AND	(fn_parc.DATALIQUIDACAO > CONVERT(DATETIME,'20221231',103) OR fn_parc.DATALIQUIDACAO IS NULL)               
               AND 	fn_doc.DOCUMENTOCONTABIL NOT IN ('CPA-108413')
               AND  fn_doc.EMPRESA = {cod_empresa}
               AND	(ct_con.CONTACONTABIL in ({handle_conta_cp}, {handle_conta_lp}) 
                OR  fn_doc.CONTACONTABILESPECIAL in ({handle_conta_cp}, {handle_conta_lp})) 
               {param_num_contrato}
             GROUP	BY fn_doc.HANDLE,
                    fn_doc.DOCUMENTODIGITADO,
                    fn_doc.DATAEMISSAO,
                    fn_doc.VALORNOMINAL,
                    fn_doc.VALORLIQUIDO,
                    fornec.NOME,
                    gn_op.NOME,
                    gn_op.HANDLE, 
                    gn_op.CODIGOREDUZIDO,
                    fn_doc.DOCUMENTOCONTABIL,
                    fn_doc.EMPRESA
             ORDER	BY 3;
            '''
        )
        cursor.execute(sql_contratos)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            contrato = {
                'handle_fn_doc': row.handle_fn_doc,
                'num_contrato': row.num_contrato,
                'data_emissao_contrato': row.data_emissao_contrato,
                'val_nominal': row.val_nominal,
                'val_liquido': row.val_liquido,
                'fornecedor': row.fornecedor,
                'handle_operacao': row.handle_operacao,
                'nome_operacao':    row.nome_operacao,
                'cod_red_operacao': row.cod_red_operacao,
                'doc_contabil': row.doc_contabil,
                'cod_empresa': row.cod_empresa,
                'proxima_parc_pendente': row.proxima_parc_pendente,
                'data_venc_proxima_parc_pendente': row.data_venc_proxima_parc_pendente,
                'val_proxima_parc_pendente': row.val_proxima_parc_pendente,
                'total_pago': row.total_pago,
                'qtd_parc': row.qtd_parc
            }
            lista_contratos_conta_benner.append(contrato)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_contratos_conta_benner

    def retorna_dados_parcelas_contrato(self, handle_contrato, data_corte):
        '''Objeto a retornar'''
        lista_parcelas_contrato_benner = []

        param_data_corte = ''
        if data_corte != None:
            param_data_corte = f" AND CAST(fn_parc.VCTOPRORROGADO AS DATE) <= '{data_corte}' "

        '''Processamento'''
        cursor = self.__conn.cursor()
        sql_parcelas = (
            f'''
            SELECT  fn_doc.HANDLE                   AS  handle_fn_doc,
                    fn_parc.handle				    AS	handle_parc,
                    fn_parc.AP						AS	ap_parcela,
                    fn_parc.PARCELADIGITADA		    AS	ordem_parcela,
                    fn_parc.VALOR 					AS	val_conta,
                    sum(fn_mov.ABATIMENTO)	        AS	val_abatimentos,
                    sum(fn_mov.ACRESCIMOS)	        AS	val_acrescimos,
                    sum(fn_mov.MULTA)			    AS	val_multas,
                    sum(fn_mov.JUROS)			    AS	val_juros,
                    sum(fn_mov.DESCONTO)		    AS	val_descontos,
					sum(fn_mov.VALORTOTAL)	        AS	val_corrigido,
					gn_op.NOME				        AS	natureza,
                    CAST(fn_parc.VCTOPRORROGADO AS DATE)		
                                                    AS data_vencimento,
                    CASE	WHEN DATEDIFF(MONTH,'20221231',fn_parc.VCTOPRORROGADO) > 12 
                        THEN	'LP'
                     ELSE 'CP'
                    END 							AS	tipo_prazo,
                    CAST(fn_parc.DATALIQUIDACAO AS DATE)		
                                                    AS	data_liquidacao,
                    (SELECT MAX(lan_principal.VALOR)
                       FROM FN_LANCAMENTOS lan_principal (NOLOCK)
                       LEFT JOIN FN_CONTAS con_principal (NOLOCK)
                         ON (con_principal.HANDLE = lan_principal.CONTA)
                      WHERE lan_principal.PARCELA = fn_parc.handle
                        AND	lan_principal.TIPO = '3'
                        AND lan_principal.ORIGEM = 2)	AS	val_fn_principal,
			        (SELECT MIN(lan_taxas.VALOR)
                       FROM FN_LANCAMENTOS lan_taxas (NOLOCK)
                       LEFT JOIN FN_CONTAS con_taxas (NOLOCK)
                         ON (con_taxas.HANDLE = lan_taxas.CONTA)
                      WHERE lan_taxas.PARCELA = fn_parc.handle
                        AND	lan_taxas.TIPO = '3'
                        AND lan_taxas.ORIGEM = 2
                        AND	con_taxas.NOME LIKE '%TAXA%')	AS	val_fn_taxas,
                    (SELECT MIN(lan_fundo.VALOR)
                       FROM FN_LANCAMENTOS lan_fundo (NOLOCK)
                       LEFT JOIN FN_CONTAS con_fundo (NOLOCK)
                         ON (con_fundo.HANDLE = lan_fundo.CONTA)
                      WHERE lan_fundo.PARCELA = fn_parc.handle
                        AND	lan_fundo.TIPO = '3'
                        AND lan_fundo.ORIGEM = 2
                        AND	con_fundo.NOME LIKE '%FUNDO%')	AS	val_fn_fundo
              FROM	FN_PARCELAS fn_parc (NOLOCK) 
              LEFT	JOIN	FN_DOCUMENTOS fn_doc (NOLOCK) 
                 ON	fn_parc.DOCUMENTO = fn_doc.HANDLE 
              LEFT	JOIN GN_OPERACOES gn_op (NOLOCK) 
                ON	gn_op.HANDLE = fn_doc.OPERACAO 
              LEFT	JOIN FN_MOVIMENTACOES fn_mov (NOLOCK) 
                ON	(fn_mov.PARCELA = fn_parc.HANDLE 
                AND	fn_mov.tipomovimento = 1
                AND	fn_mov.AUTORIZACAOPAGAMENTO IS NOT NULL)              
             WHERE	1 = 1
               AND	fn_doc.ENTRADASAIDA IN ('E','I')
               AND	fn_doc.TIPODEMOVIMENTO IN(1,2)
               AND	fn_parc.PREVISAO = 'N'
               AND	fn_parc.VALOR > 0
               AND	fn_doc.ABRANGENCIA <> 'R'
               AND	((fn_doc.DATACANCELAMENTO IS NULL) OR(fn_doc.DATACANCELAMENTO > CONVERT(DATETIME,'20221231',103)))
               AND	fn_doc.HANDLE = {handle_contrato}
               {param_data_corte}
             GROUP	BY fn_doc.HANDLE,
                    fn_parc.handle,
                    fn_parc.AP,
                    fn_parc.PARCELADIGITADA,
                    fn_parc.VALOR,                   
                    gn_op.NOME,
                    fn_parc.VCTOPRORROGADO,
                    fn_parc.DATALIQUIDACAO
             ORDER	BY fn_parc.AP;
               '''
        )
        cursor.execute(sql_parcelas)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            parcela = {
                'handle_fn_doc': row.handle_fn_doc,
                'handle_parc': row.handle_parc,
                'ap_parcela': row.ap_parcela,
                'ordem_parcela': row.ordem_parcela,
                'valor_conta': row.val_conta,
                'valor_corrigido': row.val_corrigido,
                'natureza': row.natureza,
                'data_vencimento': row.data_vencimento,
                'tipo_prazo': row.tipo_prazo,
                'data_liquidacao': row.data_liquidacao,
                'val_total_pago': row.val_corrigido,
                'val_principal': row.val_fn_principal,
                'val_taxas': row.val_fn_taxas,
                'val_fundo': row.val_fn_fundo
            }
            lista_parcelas_contrato_benner.append(parcela)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_parcelas_contrato_benner

    def retorna_balancete_conta(self, cod_empresa, handle_conta, data_ini, data_fim):
        '''A data inicial é setada aki 01/01/2023 até fizerem o processo de abertura do balence para 2024 segundo o Talison Brisola'''
        '''if cod_empresa == 12:
            data_ini = '2023-01-01'''
        '''Objeto a retornar'''
        val_balancete_benner = 0

        '''Processamento'''
        cursor = self.__conn.cursor()
        sql_balancete_benner = (
            f'''
            SELECT	
                    ROUND(ISNULL(SUM(TOTAIS.DEBITOS) ,0) - ISNULL(SUM(TOTAIS.CREDITOS) ,0) ,2)	AS	saldo_conta
              FROM	CT_CONTATOTAIS TOTAIS(NOLOCK) 
              LEFT	JOIN CT_CONTAS CONTA (NOLOCK) 
                ON	TOTAIS.CONTA = CONTA.HANDLE
                    /* Colocar o primeiro mÃªs do ano atÃ© a data do saldo atual requerido */
             WHERE	TOTAIS.COMPETENCIA BETWEEN '{data_ini}' AND '{data_fim}' 
               AND	CONTA.HANDLE = {handle_conta} 
               AND	TOTAIS.TIPO IN ('A','N')
               AND	TOTAIS.EMPRESA = {cod_empresa} 
               AND	CONTA.INDNATUREZA  IN(1,2,3)
            '''
        )
        cursor.execute(sql_balancete_benner)
        val_balancete_benner = cursor.fetchval()

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return val_balancete_benner

    def retorna_empilhadeiras_por_filial(self, handle_proj, status_ativo):
        param_ativo = ''
        if status_ativo == 'S':
            param_ativo = " AND ma_rec.ATIVO = 'S'"
        lista_empilhadeiras = []
        cursor = self.__conn.cursor()
        sql_string = (
                "SELECT	ma_rec.HANDLE	AS	handle, " +
                "       ma_rec.CODIGO	AS	placa, " +
                "       ma_rec.NOME		AS	desc_placa, " +
                "       YEAR(ma_rec.ANO) AS	ano_placa, " +
                "       mf_model.NOME	AS	modelo_placa, " +
                "       ma_rec.K_PLACAANTERIOR " +
                "                       AS	placa_anterior, " +
                "       ma_rec.ATIVO	AS	ativo " +
                " FROM	MA_RECURSOS ma_rec (NOLOCK)" +
                " LEFT	JOIN MF_VEICULOMODELOS mf_model (NOLOCK) " +
                "   ON	(mf_model.HANDLE = ma_rec.MODELOVEICULO) " +
                "WHERE	ma_rec.PROJETO =  " + handle_proj +
                "  AND	ma_rec.TIPOVEICULO = 4 " +
                param_ativo
        )
        cursor.execute(sql_string)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            obj_empilhadeira = Empilhadeira(
                row.handle,
                row.placa,
                row.desc_placa.replace(',', '.'),
                row.ano_placa,
                row.modelo_placa.replace(',', '.'),
                row.placa_anterior,
                row.ativo
            )
            lista_empilhadeiras.append(obj_empilhadeira.__dict__)
        cursor.close()
        self.__conn.close()
        return lista_empilhadeiras

    def retorna_os_by_projeto_placa_data(self, handle_proj, handle_placa, datatime_ini, datatime_fim):
        lista_os = []
        cursor = self.__conn.cursor()
        sql_string = (
                "SELECT	os.HANDLE	AS	handle, " +
                "       os.CODIGO	AS	num_os, " +
                "       os.TIPOORDEMSERVICO     " +
                "                   AS	handle_tipo_os_int, " +
                "       tipo_os.NOME                        " +
                "                   AS	desc_tipo_os,       " +
                "       os.DATAINICIAL                      " +
                "                   AS	data_ini,           " +
                "       os.DATAFINAL                        " +
                "                   AS	data_fim,           " +
                "       os.CONJUNTOMANUTENCAO               " +
                "                   AS	handle_conj_man,    " +
                "       partes.NOME	AS	desc_conj,          " +
                "       os.DESCRICAO                        " +
                "                   AS	desc_os,            " +
                "       os.SITUACAO	AS	situacao            " +
                "FROM	MF_ORDEMSERVICOS os  (NOLOCK)               " +
                "LEFT	JOIN MA_RECURSOS ma_rec  (NOLOCK)           " +
                "  ON	(ma_rec.HANDLE = os.VEICULO)        " +
                "LEFT	JOIN MF_TIPOORDEMSERVICOS tipo_os (NOLOCK)  " +
                "  ON	(tipo_os.HANDLE = os.TIPOORDEMSERVICO)  " +
                "LEFT	JOIN MA_RECURSOPARTES partes (NOLOCK)           " +
                "  ON	(partes.HANDLE = os.CONJUNTOMANUTENCAO) " +
                "WHERE	os.TIPOORDEMSERVICO in (1,3,22)           " +
                " AND	os.STATUS = 4                           " +
                " AND	ma_rec.HANDLE = "+str(handle_placa)+"               " +
                " AND	os.PROJETO = "+ str(handle_proj) + "           " +
                " AND	os.DATAINICIAL BETWEEN '"+str(datatime_ini)+"' AND '"+str(datatime_fim)+"';"
        )
        cursor.execute(sql_string)
        os_cursor = cursor.fetchall()
        for row in os_cursor:
            obj_os_vinculada = OS_Apontamento_Disp_Empilhadeira.objects.filter(handle_os_benner=row.handle).first()
            verifica_se_vinculada = 'N'
            if obj_os_vinculada != None:
                verifica_se_vinculada = 'S'
            obj_ordem_servico = Ordens_Servico(
                row.handle,
                row.num_os,
                row.handle_tipo_os_int,
                row.desc_tipo_os,
                row.data_ini,
                row.data_fim,
                row.handle_conj_man,
                row.desc_conj,
                row.desc_os,
                row.situacao,
                verifica_se_vinculada
            )
            lista_os.append(obj_ordem_servico)
        cursor.close()
        self.__conn.close()
        return lista_os

    def retorna_os_by_num_os(self, handle_proj, num_os):
        lista_os = []
        cursor = self.__conn.cursor()
        sql_string = (
                "SELECT	os.HANDLE	AS	handle, " +
                "       os.CODIGO	AS	num_os, " +
                "       os.TIPOORDEMSERVICO     " +
                "                   AS	handle_tipo_os_int, " +
                "       tipo_os.NOME                        " +
                "                   AS	desc_tipo_os,       " +
                "       os.DATAINICIAL                      " +
                "                   AS	data_ini,           " +
                "       os.DATAFINAL                        " +
                "                   AS	data_fim,           " +
                "       os.CONJUNTOMANUTENCAO               " +
                "                   AS	handle_conj_man,    " +
                "       partes.NOME	AS	desc_conj,          " +
                "       os.DESCRICAO                        " +
                "                   AS	desc_os,            " +
                "       os.SITUACAO	AS	situacao            " +
                "FROM	MF_ORDEMSERVICOS os (NOLOCK)                " +
                "LEFT	JOIN MA_RECURSOS ma_rec  (NOLOCK)           " +
                "  ON	(ma_rec.HANDLE = os.VEICULO)        " +
                "LEFT	JOIN MF_TIPOORDEMSERVICOS tipo_os (NOLOCK)  " +
                "  ON	(tipo_os.HANDLE = os.TIPOORDEMSERVICO)  " +
                "LEFT	JOIN MA_RECURSOPARTES partes  (NOLOCK)          " +
                "  ON	(partes.HANDLE = os.CONJUNTOMANUTENCAO) " +
                "WHERE	os.TIPOORDEMSERVICO in (1,3,22)           " +
                " AND	os.STATUS = 4                           " +
                " AND	os.PROJETO = "+ str(handle_proj) +
                " AND	os.CODIGO in ( "+ str(num_os) +") ;"
        )
        cursor.execute(sql_string)
        os_cursor = cursor.fetchall()
        for row in os_cursor:
            obj_os_vinculada = OS_Apontamento_Disp_Empilhadeira.objects.filter(handle_os_benner=row.handle).first()
            verifica_se_vinculada = 'N'
            if obj_os_vinculada != None:
                verifica_se_vinculada = 'S'
            obj_ordem_servico = Ordens_Servico(
                row.handle,
                row.num_os,
                row.handle_tipo_os_int,
                row.desc_tipo_os,
                row.data_ini,
                row.data_fim,
                row.handle_conj_man,
                row.desc_conj,
                row.desc_os,
                row.situacao,
                verifica_se_vinculada
            )
            lista_os.append(obj_ordem_servico)
        cursor.close()
        self.__conn.close()
        return lista_os

    def retornaTabFiliaisBennerByEmpresa(self, cod_empresa):
        cursor = self.__conn.cursor()
        sql_filiais = (
            f'''
                SELECT  HANDLE,
                        EMPRESA,
                        NOME,
                        CGC
                  FROM	FILIAIS (NOLOCK)
                 WHERE	nome NOT LIKE '%x--%'
                   AND  empresa = {cod_empresa};
            '''
        )
        cursor.execute(sql_filiais)
        lista_filiais = cursor.fetchall()
        cursor.close()
        self.__conn.close()
        return lista_filiais

    def retorna_familias(self, filtro_lista_handle_familias):
        cursor = self.__conn.cursor()
        lista_familias = []
        sql_pd_familias = (
            f'''
            SELECT 	distinct	
                handle,
                nome
            FROM PD_FAMILIASPRODUTOS (NOLOCK) 
            {filtro_lista_handle_familias}
            '''
        )
        cursor.execute(sql_pd_familias)
        familias_cursor = cursor.fetchall()
        for row in familias_cursor:
            familia = Familia(row.handle, row.nome)
            lista_familias.append(familia)
        cursor.close()
        self.__conn.close()
        return lista_familias

    def retorna_df_ultimas_compras(self, handle_filial, data_ini, data_fim, handle_familia, cod_ref_item,
                                       num_requisicao):
        # param_familia = ' AND	prod_itens_compra.familia not in (12,18,23,25,28,29,34,35,36,37,39,53,66,71,75,92) '
        param_familia = ''
        param_item = ''
        if str(handle_familia) != '0':
            param_familia = ' AND prod_itens_compra.familia in (' + str(handle_familia) + ') '

        if str(cod_ref_item) != '0' and num_requisicao == '0':
            param_item = " AND prod_itens_compra.codigoreferencia = '" + str(cod_ref_item) + "' "
        elif str(num_requisicao) != '0':
            lista_handle_str = self.retorna_lista_handle_itens_requisicao_str(handle_filial, num_requisicao)

            param_item = ' AND prod_itens_compra.handle in (' + \
                         str(lista_handle_str).replace('[', '').replace(']','') + ') '

        '''Zerbone(1600), Spall(2529), Franaciele(2933), Natan(3820), Rafael(1651), Raquel(3831), 
        Samanta(3274), Valquiria(1484), Titon(65), Marcionei(2614), Fernanda(2616), Larissa(3344),
        Lucas.Fernandes(4128)'''
        handle_atendentes = '65,1484,1600,1651,2529,2614,2616,2933,3274,3344,3820,3831,4128'

        sql_evolucao_ultimas_compras = (
            f'''
            SELECT	compra.filial							AS	handle_filial_compra,
                    filial_compra.NOME						AS	nome_filial_compra,
                    compra.HANDLE							AS	handle_compra,
                    compra.numero					    	AS	numero_compra,
                    compra.DATADAORDEM						AS	data_compra,
                    compra.fornecedor						AS	handle_fornecedor_comra,
                    fornecedor_compra.nome					AS	nome_fornecedor_compra,
                    fornecedor_compra.cgccpf				AS	doc_fornecedor_compra,
                    compra.usuarioincluiu					AS	handle_usuario_incluiu_compra,
                    usuario_incluiu_compra.nome 			AS	nome_usuario_incluiu_compra,
                    prod_itens_compra.codigoreferencia  	AS	cod_ref_prod,			 
                    itens_compra.produto					AS	handle_produto,					
                    prod_itens_compra.nome					AS	nome_produto,
                    itens_compra.variacao					AS	handle_variacao,
                    un_med.NOME                             AS  nome_un_medida,
                    PDV.CONJUNTOVARIACOES					AS	desc_variacao,
                    prod_itens_compra.familia				AS	handle_familia,
                    familia_prod_itens_compra.nome		    AS	desc_familia,
                    ROW_NUMBER() OVER (PARTITION BY prod_itens_compra.codigoreferencia,PDV.CONJUNTOVARIACOES,
                        compra.filial ORDER BY compra.HANDLE DESC ) 
                                                            AS seq_item,
                    avg(itens_compra.valorunitario)		    AS	val_unit,   
                    sum(itens_compra.quantidade)			AS	qtd_item,
                    sum(itens_compra.VALORTOTAL)			AS	val_tt_item,
                    COALESCE ((SELECT   TOP 1 avg(itens_compra.valorunitario) -  item_ant.valorunitario
                                 FROM	cp_ordenscompraitens item_ant (NOLOCK)
                                 LEFT	JOIN pd_produtos prod_ant	(NOLOCK)
                                   ON	( prod_ant.handle = item_ant.produto)	
                                 LEFT 	JOIN PD_PRODUTOVARIACOESMESTRE variacao_ant (NOLOCK) 
                                   ON	(variacao_ant.HANDLE = item_ant.VARIACAO) 
                                 LEFT	JOIN CP_ORDENSCOMPRA com_ant (NOLOCK)
                                   ON	(com_ant.HANDLE = item_ant.ORDEMCOMPRA)
                                WHERE   prod_ant.codigoreferencia =  prod_itens_compra.codigoreferencia
                                  AND	variacao_ant.HANDLE =  itens_compra.variacao
                                  AND	com_ant.filial = compra.filial
                                  AND	com_ant.HANDLE < compra.HANDLE
                                  AND	com_ant.datadaordem BETWEEN '{data_ini}' AND compra.DATADAORDEM
                                  AND	com_ant.usuarioincluiu in ({handle_atendentes})
                                  AND	prod_ant.tipo = 1
                                  AND	com_ant.status = 4                                     	
                                ORDER	BY item_ant.HANDLE DESC
                    ) , 0 )						            AS	val_disp_atual_menos_anterior,

                    sum(itens_compra.quantidade) * COALESCE ((SELECT   TOP 1 avg(itens_compra.valorunitario) -  item_ant.valorunitario
                                                                FROM	cp_ordenscompraitens item_ant (NOLOCK)
                                                                LEFT	JOIN pd_produtos prod_ant	(NOLOCK)
                                                                 ON	    ( prod_ant.handle = item_ant.produto)	
                                                               LEFT 	JOIN PD_PRODUTOVARIACOESMESTRE variacao_ant (NOLOCK) 
                                                                 ON	    (variacao_ant.HANDLE = item_ant.VARIACAO) 
                                                                LEFT	JOIN CP_ORDENSCOMPRA com_ant (NOLOCK)
                                                                  ON	(com_ant.HANDLE = item_ant.ORDEMCOMPRA)
                                                               WHERE    prod_ant.codigoreferencia =  prod_itens_compra.codigoreferencia
                                                                 AND	variacao_ant.HANDLE =  itens_compra.variacao
                                                                 AND	com_ant.filial = compra.filial
                                                                 AND	com_ant.HANDLE < compra.HANDLE
                                                                 AND	com_ant.datadaordem BETWEEN '{data_ini}' AND compra.DATADAORDEM
                                                                 AND	com_ant.usuarioincluiu in ({handle_atendentes})
                                                                 AND	prod_ant.tipo = 1
                                                                 AND	com_ant.status = 4                                     	
                                                               ORDER	BY item_ant.HANDLE DESC
                                                                ) , 0 )						
                                                            AS	val_disp_total,

                    COALESCE ((SELECT   TOP 1 com_ant.handle
                            FROM	cp_ordenscompraitens item_ant (NOLOCK)
                            LEFT	JOIN pd_produtos prod_ant	(NOLOCK)
                             ON	    ( prod_ant.handle = item_ant.produto)	
                           LEFT 	JOIN PD_PRODUTOVARIACOESMESTRE variacao_ant (NOLOCK) 
                             ON	    (variacao_ant.HANDLE = item_ant.VARIACAO) 
                            LEFT	JOIN CP_ORDENSCOMPRA com_ant (NOLOCK)
                              ON	(com_ant.HANDLE = item_ant.ORDEMCOMPRA)
                           WHERE    prod_ant.codigoreferencia =  prod_itens_compra.codigoreferencia
                             AND	variacao_ant.HANDLE =  itens_compra.variacao
                             AND	com_ant.filial = compra.filial
                             AND	com_ant.HANDLE < compra.HANDLE
                             AND	com_ant.datadaordem BETWEEN '{data_ini}' AND compra.DATADAORDEM
                             AND	com_ant.usuarioincluiu in ({handle_atendentes})
                             AND	prod_ant.tipo = 1
                             AND	com_ant.status = 4                                     	
                           ORDER	BY item_ant.HANDLE DESC
                            ) , 0 )						AS	handle_compra_anterior
            FROM	cp_ordenscompraitens itens_compra (NOLOCK) 
            LEFT	JOIN cp_ordenscompra compra (NOLOCK)
              ON	(compra.handle = itens_compra.ordemcompra)
            LEFT	JOIN pd_produtos prod_itens_compra	(NOLOCK)
              ON	(prod_itens_compra.handle = itens_compra.produto)	
            LEFT    JOIN PD_PRODUTOVARIACOESMESTRE PDV (NOLOCK) 
              ON	PDV.HANDLE = itens_compra.VARIACAO
            LEFT	JOIN pd_familiasprodutos familia_prod_itens_compra (NOLOCK)
              ON	(familia_prod_itens_compra.handle = prod_itens_compra.familia)
            LEFT	JOIN gn_pessoas fornecedor_compra (NOLOCK)
              ON	(fornecedor_compra.handle = compra.fornecedor)
            LEFT	JOIN filiais filial_compra (NOLOCK)
              ON	(filial_compra.handle = compra.filial)
            LEFT	JOIN z_grupousuarios usuario_incluiu_compra (NOLOCK)
              ON	(usuario_incluiu_compra.handle = compra.usuarioincluiu)
            LEFT    JOIN CM_UNIDADESMEDIDA un_med (NOLOCK)
              ON    (un_med.HANDLE = itens_compra.UNIDADE)
           WHERE	compra.datadaordem BETWEEN '{data_ini}' AND '{data_fim}'
             AND	compra.usuarioincluiu in ({handle_atendentes})
             AND	prod_itens_compra.tipo = 1
             AND	compra.status = 4 /* status 4 : compra encerrada */
             AND    compra.filial in ({handle_filial})
             AND    prod_itens_compra.familia NOT IN (42)
             AND    (familia_prod_itens_compra.nome not like '%SERVIÇO%' AND familia_prod_itens_compra.nome not like '%SERVICO%')
             /* AND	prod_itens_compra.codigoreferencia = '22183' */
             {param_familia}	
             {param_item}
           GROUP    BY compra.filial,
                    filial_compra.NOME,
                    compra.HANDLE,
                    compra.numero,
                    compra.DATADAORDEM,
                    compra.fornecedor,
                    fornecedor_compra.nome,
                    fornecedor_compra.cgccpf,
                    compra.usuarioincluiu,
                    usuario_incluiu_compra.nome,
                    prod_itens_compra.codigoreferencia,			 
                    itens_compra.produto,					
                    prod_itens_compra.nome,
                    itens_compra.variacao,
                    un_med.NOME,
                    PDV.CONJUNTOVARIACOES,
                    prod_itens_compra.familia,
                    familia_prod_itens_compra.nome
            ORDER	BY 1, 19 ASC;
        '''
        )
        df_evolucao_preco = pd.read_sql(sql_evolucao_ultimas_compras, self.__conn)

        for index, row in df_evolucao_preco.iterrows():
            compra_aud = Compra_Auditada.objects.filter(
                handle_filial_compra=df_evolucao_preco.loc[index, 'handle_filial_compra'],
                handle_itens_compra=df_evolucao_preco.loc[index, 'handle_compra']).first()
            val_unit_atual = 0
            val_unit_ant = 0
            qtd_item_compra_aud = 0

            if compra_aud != None:
                df_evolucao_preco.loc[index, 'val_unit'] = float(compra_aud.val_unit)
                df_evolucao_preco.loc[index, 'qtd_item'] = float(compra_aud.qtd_item)
                val_unit_atual = compra_aud.val_unit
                qtd_item_compra_aud = compra_aud.qtd_item

            compra_aud_anterior = Compra_Auditada.objects.filter(
                handle_filial_compra=df_evolucao_preco.loc[index, 'handle_filial_compra'],
                handle_itens_compra=df_evolucao_preco.loc[index, 'handle_compra_anterior']).first()

            if compra_aud_anterior != None:
                df_evolucao_preco.loc[index, 'val_disp_atual_menos_anterior'] = \
                    float(val_unit_atual - compra_aud_anterior.val_unit)
                val_unit_ant = compra_aud_anterior.val_unit

                df_evolucao_preco.loc[index, 'val_disp_total'] = \
                    float(qtd_item_compra_aud * (val_unit_atual - val_unit_ant))

            '''if compra_aud_anterior != None:
                df_evolucao_preco.loc[index, 'val_disp_total'] = \
                    float(compra_aud.qtd_item * (val_unit_atual - val_unit_ant))
'''
        # df_evolucao_preco.to_csv(r'C:\Danilo - C\Projetos_Jupter\df_evolucao_preco.csv',sep=';')

        self.__conn.close()
        return df_evolucao_preco

    def retorna_compras_by_item_filial(self, handle_filial, cod_ref_item, data_ini, data_fim):
        cursor = self.__conn.cursor()
        '''Zerbone(1600), Spall(2529), Franaciele(2933), Natan(3820), Rafael(1651), Raquel(3831), 
                Samanta(3274), Valquiria(1484), Titon(65), Marcionei(2614), Fernanda(2616), Larissa(3344),
                Lucas.Fernandes(4128)'''
        handle_atendentes = '65,1484,1600,1651,2529,2614,2616,2933,3274,3344,3820,3831,4128'
        sql_compras_item = (
            f'''
            SELECT	compra.filial							AS	handle_filial_compra,
                    filial_compra.NOME						AS	nome_filial_compra,
                    prod_itens_compra.codigoreferencia		AS	cod_ref_prod,			 
                    itens_compra.produto					AS	handle_produto,					
                    prod_itens_compra.nome					AS	nome_produto,
                    PDV.CONJUNTOVARIACOES					AS	desc_variacao,
                    prod_itens_compra.familia				AS	handle_familia,
                    familia_prod_itens_compra.nome			AS	desc_familia,
                    itens_compra.valorunitario				AS	val_unit,
                    itens_compra.variacao					AS	handle_variacao,
                    compra.HANDLE							AS	handle_compra,
                    compra.numero						    AS	numero_compra,
                    compra.DATADAORDEM						AS	data_compra,
                    compra.usuarioincluiu					AS	handle_usuario_incluiu_compra,
                    usuario_incluiu_compra.nome				AS	nome_usuario_incluiu_compra,

                    compra.fornecedor						AS	handle_fornecedor_comra,
                    fornecedor_compra.nome					AS	nome_fornecedor_compra,
                    fornecedor_compra.cgccpf				AS	doc_fornecedor_compra,

                    itens_compra.quantidade					AS	qtd_item,
                    itens_compra.VALORTOTAL					AS	val_tt_item,
                    un_med.NOME                             AS  nome_un_medida,

                    req_pai.NUMERO			                AS	numero_req,
                    req_pai.DATAINCLUSAO					AS	data_req,
                    CASE WHEN req_pai.K_TIPODECOMPRA = 4 THEN 'P'
                         WHEN req_pai.K_TIPODECOMPRA IN (1,3,5,6) THEN 'E'
                         WHEN req_pai.K_TIPODECOMPRA IS NULL THEN ''
                         ELSE 'NE' END						AS	status_req,
                    tipo_compra.NOME 						AS	desc_tipo_compra_req,
                    itens_compra.handle					    AS	handle_itens_compra,
                    req.handle                              AS  handle_req,
                    req_pai.handle                          AS  handle_req_pai,
                    fornecedor_compra.MUNICIPIO				AS	handle_cidade_fornecedor,
                    municipio.NOME							AS	nome_cidade_fornecedor,
                    uf.SIGLA								AS	uf_fornecedor
               FROM	cp_ordenscompraitens itens_compra (NOLOCK) 
               LEFT	JOIN cp_ordenscompra compra (NOLOCK)
                 ON	(compra.handle = itens_compra.ordemcompra)
               LEFT	JOIN pd_produtos prod_itens_compra	(NOLOCK)
                 ON	(prod_itens_compra.handle = itens_compra.produto)	
               LEFT JOIN PD_PRODUTOVARIACOESMESTRE PDV (NOLOCK) 
                 ON	PDV.HANDLE = itens_compra.VARIACAO
               LEFT	JOIN pd_familiasprodutos familia_prod_itens_compra (NOLOCK)
                 ON	(familia_prod_itens_compra.handle = prod_itens_compra.familia)
               LEFT	JOIN gn_pessoas fornecedor_compra (NOLOCK)
                 ON	(fornecedor_compra.handle = compra.fornecedor)
               LEFT	JOIN MUNICIPIOS municipio
                 ON	(municipio.HANDLE = fornecedor_compra.MUNICIPIO)
               LEFT	JOIN ESTADOS uf
                 ON	(uf.HANDLE = municipio.ESTADO)
               LEFT	JOIN filiais filial_compra (NOLOCK)
                 ON	(filial_compra.handle = compra.filial)
               LEFT	JOIN z_grupousuarios usuario_incluiu_compra (NOLOCK)
                 ON	(usuario_incluiu_compra.handle = compra.usuarioincluiu)
               LEFT JOIN CM_UNIDADESMEDIDA un_med (NOLOCK)
                 ON (un_med.HANDLE = itens_compra.UNIDADE)

                /* ligação com requisições */
               LEFT JOIN CP_REQUISICOES req (NOLOCK)
                 ON (req.ordemcompraitem = itens_compra.handle
                AND	req.TABTIPO = 1
                AND	req.STATUS = 4)
               LEFT	JOIN CP_REQUISICOESPAI req_pai (NOLOCK)
                 ON	(req_pai.HANDLE = req.REQUISICAOPAI
                AND	req_pai.STATUS = 4) 
               LEFT	JOIN K_TIPODECOMPRA tipo_compra
                 ON	(tipo_compra.HANDLE = req_pai.K_TIPODECOMPRA) 
              WHERE	compra.datadaordem BETWEEN '{data_ini}' AND '{data_fim}'
                AND	compra.usuarioincluiu in ({handle_atendentes})  
                AND prod_itens_compra.familia NOT IN (42)
                AND (familia_prod_itens_compra.nome not like '%SERVIÇO%' AND familia_prod_itens_compra.nome not like '%SERVICO%')              
                AND	prod_itens_compra.tipo = 1
                AND	compra.status = 4 /* status 4 : compra encerrada */
                AND compra.filial = {handle_filial}
                AND prod_itens_compra.codigoreferencia = '{cod_ref_item}'
              ORDER	BY 13 ASC;
            '''
        )
        cursor.execute(sql_compras_item)
        compras_cursor = cursor.fetchall()
        lista_compras_item = []
        for row in compras_cursor:
            compra_aud = Compra_Auditada.objects.filter(
                handle_filial_compra=row.handle_filial_compra,
                handle_itens_compra=row.handle_itens_compra).first()
            val_unit_atual = row.val_unit
            qtd_item_atual = row.qtd_item
            if compra_aud != None:
                val_unit_atual = compra_aud.val_unit
                qtd_item_atual = compra_aud.qtd_item
            reg = Compras_Item(row.handle_filial_compra, row.nome_filial_compra, row.cod_ref_prod,
                               row.handle_produto, row.nome_produto, row.desc_variacao, row.handle_familia,
                               row.desc_familia,
                               val_unit_atual, row.handle_variacao, row.handle_compra, row.numero_compra,
                               row.data_compra,
                               row.handle_usuario_incluiu_compra, row.nome_usuario_incluiu_compra,
                               row.handle_fornecedor_comra, row.nome_fornecedor_compra, row.doc_fornecedor_compra,
                               qtd_item_atual, row.val_tt_item, row.nome_un_medida, row.numero_req, row.data_req,
                               row.status_req, row.desc_tipo_compra_req, row.handle_itens_compra, row.handle_req,
                               row.handle_req_pai, row.handle_cidade_fornecedor, row.nome_cidade_fornecedor,
                               row.uf_fornecedor)
            lista_compras_item.append(reg)
        cursor.close()
        self.__conn.close()
        return lista_compras_item

    def retorna_itens_by_familia_filial(self, handle_familia, handle_filial):
        param_handle_familia = ''
        if handle_familia != '0':
            param_handle_familia = ' AND p.FAMILIA in (' + handle_familia + ') '
        cursor = self.__conn.cursor()
        lista_itens = []
        sql_pd_produtos = (
            f'''
            SELECT 	distinct	
                    p.handle    AS  handle,
                    p.nome      AS  nome,
                    p.codigoreferencia
                                AS  codigoreferencia
              FROM  PD_PRODUTOS p (NOLOCK)
             WHERE  p.FILIAL in ( {handle_filial} )
            {param_handle_familia}
            '''
        )
        cursor.execute(sql_pd_produtos)
        produtos_cursor = cursor.fetchall()
        for row in produtos_cursor:
            prod = Produto(row.handle, row.nome, row.codigoreferencia)
            lista_itens.append(prod)
        cursor.close()
        self.__conn.close()
        return lista_itens

    def retorna_lista_handle_itens_requisicao_str(self, handle_filial, numero_req):
        cursor = self.__conn.cursor()
        sql_req = (
                f'''
                SELECT	DISTINCT R.PRODUTO AS handle_prod
                  FROM	CP_REQUISICOES R (NOLOCK)
                  LEFT	JOIN CP_REQUISICOESPAI RP (NOLOCK) 
                    ON	(RP.HANDLE = R.REQUISICAOPAI)
                 WHERE	RP.FILIAL = {handle_filial}
                   AND	RP.NUMERO = {numero_req}
                '''
        )
        cursor.execute(sql_req)
        registros_cursor = cursor.fetchall()
        lista_handle_prod = []
        for row in registros_cursor:
            lista_handle_prod.append(row.handle_prod)
        cursor.close()
        #self.__conn.close()
        return lista_handle_prod

    def retornaEmpresasBenner(self):
        cursor = self.__conn.cursor()
        lista_empresas = []
        sql_empresa = ("SELECT "+
                       "         HANDLE, " +
                       "         EMPRESA, " +
                       "         ESTRUTURA, " +
                       "         NOME    " +
                       "  FROM   GN_PROJETOS (NOLOCK) " +
                       "  WHERE  LEN(ESTRUTURA)= 1")
        cursor.execute(sql_empresa)
        lista_cursor = cursor.fetchall()
        for row in lista_cursor:
            empresa = Empresa_Benner(row.HANDLE, row.EMPRESA, row.ESTRUTURA, row.NOME)
            lista_empresas.append(empresa)
        cursor.close()
        self.__conn.close()
        return lista_empresas


    def retornaTodasOperacoesBenner(self):
        cursor = self.__conn.cursor()
        lista_operacoes = []
        sql_op = ("SELECT "+
                  "         HANDLE, " +
                  "         EMPRESA, " +
                  "         ESTRUTURA, " +
                  "         NOME,    " +
                  "         SUBSTRING(estrutura, 1,1) AS ESTRUT_EMP"
                  "  FROM   GN_PROJETOS (NOLOCK) " +
                  " WHERE   (LEN(ESTRUTURA)= 4) ")
        cursor.execute(sql_op)
        operacoes_cursor = cursor.fetchall()
        for row in operacoes_cursor:
            operacao = Operacao_Benner(row.HANDLE, row.EMPRESA, row.ESTRUT_EMP, row.ESTRUTURA, row.NOME)
            lista_operacoes.append(operacao)
        cursor.close()
        self.__conn.close()
        return lista_operacoes


    def retornaTodasFilialBenner(self):
        cursor = self.__conn.cursor()
        lista_filiais = []
        sql_op = ("SELECT "+
                  "         HANDLE, " +
                  "         EMPRESA, " +
                  "         ESTRUTURA, " +
                  "         NOME,    " +
                  "         SUBSTRING(estrutura, 1,1) AS ESTRUT_EMP, "
                  "         SUBSTRING(estrutura, 1,4) AS ESTRUT_OP"
                  "  FROM   GN_PROJETOS (NOLOCK) " +
                  " WHERE   LEN(ESTRUTURA)= 7 ")
        cursor.execute(sql_op)
        filiais_cursor = cursor.fetchall()
        for row in filiais_cursor:
            filial = Filial_Benner(row.HANDLE, row.EMPRESA, row.ESTRUT_EMP, row.ESTRUT_OP, row.ESTRUTURA, row.NOME)
            lista_filiais.append(filial)
        cursor.close()
        self.__conn.close()
        return lista_filiais



    def retornaTodosProjetosBenner(self):
        cursor = self.__conn.cursor()
        lista_projetos = []
        sql_op = ("SELECT "+
                  "         HANDLE, " +
                  "         EMPRESA, " +
                  "         ESTRUTURA, " +
                  "         NOME,    " +
                  "         SUBSTRING(estrutura, 1,1) AS ESTRUT_EMP, "
                  "         SUBSTRING(estrutura, 1,4) AS ESTRUT_OP, "
                  "         SUBSTRING(estrutura, 1,7) AS ESTRUT_FIL "
                  "  FROM   GN_PROJETOS (NOLOCK) " +
                  " WHERE   LEN(ESTRUTURA)= 11 " )
        cursor.execute(sql_op)
        projetos_cursor = cursor.fetchall()
        for row in projetos_cursor:
            projeto = Projeto_Benner(row.HANDLE, row.EMPRESA, row.ESTRUT_EMP, row.ESTRUT_OP, row.ESTRUT_FIL,
                                     row.ESTRUTURA, row.NOME)
            lista_projetos.append(projeto)
        cursor.close()
        self.__conn.close()
        return lista_projetos


    def retornaBenefTerceiroByProjeto(self, handle_projeto):
        cursor = self.__conn.cursor()
        lista_beneficiarios = []
        sql_beneficiarios = (
                '''
                    SELECT DISTINCT
                            gn_p.handle,
                            gn_p.nome,
                            gn_p.tipo,
                            gn_p.inativo,
                            gn_p.CGCCPF,
                            COUNT(ma.codigo)	AS	qtd_placa
                        FROM gn_pessoas gn_p (NOLOCK)
                        RIGHT JOIN ma_recursos ma (NOLOCK)
                        ON (ma.proprietario = gn_p.handle)
                        WHERE gn_p.ehfornecedor = 'S'
                        AND gn_p.ehtransportador = 'S'
                        /* AND ma.origem = 2 */
                        AND ma.projeto = ''' + str(handle_projeto) +
                    '''
                        GROUP BY 	gn_p.handle,
                            gn_p.nome,
                            gn_p.tipo,
                            gn_p.inativo,
                            gn_p.CGCCPF
                        ORDER BY 2;
                '''
        )
        cursor.execute(sql_beneficiarios)
        beneficiarios_cursor = cursor.fetchall()
        for row in beneficiarios_cursor:
            benef = Beneficiario_Terceiro(row.handle, row.nome, row.tipo, row.inativo, row.CGCCPF, row.qtd_placa)
            lista_beneficiarios.append(benef)
        cursor.close()
        self.__conn.close()
        return lista_beneficiarios



    def retorna_requisicoes_atendidas_tma(self, data_ini, data_fim):
        '''param_data_inicial = data_ini.split('/')[2] + '- ' + data_ini.split('/')[1] + '-' + \
                             data_ini.split('/')[0]
        param_data_final = data_fim.split('/')[2] + '- ' + data_fim.split('/')[1] + '-' + \
                           data_fim.split('/')[0]'''

        param_data_inicial = data_ini
        param_data_final = data_fim


        lista_req_atendidas  = []
        cursor = self.__conn.cursor()
        sql_string = ("SELECT	distinct " +
                      "         req.FILIAL				 AS	handle_filial, " +
                      "         fil.NOME                 AS nome_filial, " +
                      "         fil.EMPRESA              AS cod_empresa, " +
                      "         fil.CGC                  AS cnpj_filial, " +
                      "         req_pai.HANDLE  		 AS	handle_req, " +
                      "         req_pai.NUMERO			 AS	num_req_pai, " +
                      "         req_pai.DATAINCLUSAO	 AS	data_inclusao, " +
                      "         pd_data_confirmada.DATAINCLUSAO           " +
                      "                                  AS data_confirmada, " +
                      "         ordem_compra.datadaordem " +
                      "                                  AS data_atendida, " +
                      "         usu.HANDLE				 AS	handle_usu_incluiu, " +
                      "         usu.NOME				 AS	nome_usu_incluiu, " +
                      "         prod.FAMILIA			 AS	handle_familia, " +
                      "         familia.NOME			 AS	desc_familia, " +
                      "         CASE WHEN req_pai.K_TIPODECOMPRA = 4 THEN 'P'  " +
                      "              WHEN req_pai.K_TIPODECOMPRA IN (1,3,5,6) THEN 'E' " +
                      "              ELSE 'NE' END " +
                      "                                  AS	status_ordem, " +
                      "         req.COMPRADOR            AS handle_comprador, " +
                      "         comprador.NOME           AS nome_comprador " +
                      "   FROM 	CP_REQUISICOESPAI req_pai (NOLOCK) " +
                      "   LEFT	JOIN CP_REQUISICOES req (NOLOCK) " +
                      "     ON	(req.REQUISICAOPAI = req_pai.HANDLE) " +
                      "   LEFT  JOIN FILIAIS fil (NOLOCK) " +
                      "     ON  (fil.HANDLE = req.FILIAL) " +
                      "   LEFT	JOIN CP_ORDENSCOMPRA ordem_compra (NOLOCK)  " +
                      "     ON	(ordem_compra.handle = req.ordemcompra) " +
                      "   LEFT	JOIN CP_ORDENSCOMPRAITENS itens_ordem_compra (NOLOCK) " +
                      "     ON	((itens_ordem_compra.ordemcompra = ordem_compra.handle) " +
                      "    AND	(itens_ordem_compra.produto = req.produto)) " +
                      "   LEFT	JOIN Z_GRUPOUSUARIOS usu (NOLOCK) " +
                      "     ON	(usu.HANDLE = req.USUARIOINCLUIU) " +
                      "   LEFT	JOIN PD_PRODUTOS prod (NOLOCK) " +
                      "     ON	(prod.handle  = req.produto) " +
                      "   LEFT	JOIN PD_FAMILIASPRODUTOS familia (NOLOCK) " +
                      "     ON	(familia.handle = prod.FAMILIA) " +
                      "   LEFT	JOIN PD_STATUS pd_data_confirmada  (NOLOCK) " +
                      "     ON	(pd_data_confirmada.HANDLEREGISTROORIGEM = req_pai.HANDLE) " +
                      "   LEFT	JOIN PD_STATUS pd_data_atendida  (NOLOCK) " +
                      "     ON	(pd_data_atendida.HANDLEREGISTROORIGEM = req_pai.HANDLE) "  +
                      "   LEFT	JOIN Z_GRUPOUSUARIOS comprador (NOLOCK) " +
                      "     ON	(comprador.HANDLE = req.COMPRADOR) " +
                      "  WHERE	req.TABTIPO = 1 " +
                      "    AND	req_pai.status = 4 " +
                      "    AND	req.status = 4 " +
                      "    AND	ordem_compra.numero is not null " +
                      "    AND  pd_data_confirmada.DATAINCLUSAO = (SELECT MAX(pd_st_conf.DATAINCLUSAO) " +
                      "  from PD_STATUS pd_st_conf (NOLOCK) "+
                      " WHERE pd_st_conf.STATUS = 2 " +
                      "   AND pd_st_conf.HANDLETABELAORIGEM = 2329 " +
                      "   AND pd_st_conf.HANDLEREGISTROORIGEM = req_pai.HANDLE " +
                      "   AND pd_st_conf.nomestatus in ('Atendida', 'Confirmada')) " +
                      "    AND  pd_data_atendida.DATAINCLUSAO = (SELECT MAX(pd_st_atend.DATAINCLUSAO) " +
                      " FROM PD_STATUS pd_st_atend (NOLOCK) " +
                      " WHERE pd_st_atend.STATUS = 4 " +
                      "  AND pd_st_atend.HANDLETABELAORIGEM = 2329 " +
                      "  AND pd_st_atend.HANDLEREGISTROORIGEM = req_pai.HANDLE " +
                      "  AND pd_st_atend.nomestatus in ('Atendida', 'Confirmada')) " +
                      "    AND	ordem_compra.datadaordem BETWEEN '"+param_data_inicial+" 00:00' AND '"+param_data_final+" 23:59' " +
                      #"    //Respectivo : Eduardo Spall, Fernanda Anibal, Rafael Lemos, Marcionei Finger, Franciele Rodrigues, Valquiria Silva, Kathleen Goedert, Larissa(3344)  " +
                      "    AND	comprador.handle in (2529, 2616, 1651, 2614, 2933, 1484, 2646, 3344) " +
                      "  ORDER	BY ordem_compra.datadaordem")
        cursor.execute(sql_string)
        requisicoes_cursor = cursor.fetchall()
        for row in requisicoes_cursor:
            obj_req_atendida_tma = Requisicao_Atendidas_TMA(
                row.handle_filial,
                row.nome_filial,
                row.cod_empresa,
                row.cnpj_filial.replace('.','').replace('/','').replace('-',''),
                row.handle_req,
                row.num_req_pai,
                row.data_inclusao,
                row.data_confirmada,
                row.data_atendida,
                row.handle_usu_incluiu,
                row.nome_usu_incluiu,
                row.handle_familia,
                row.desc_familia,
                row.status_ordem,
                row.handle_comprador,
                row.nome_comprador,
                None,
                None,
                None,
                None,
                'Não Importado'
            )
            lista_req_atendidas.append(obj_req_atendida_tma)
        cursor.close()
        self.__conn.close()
        return lista_req_atendidas


    def retorna_natureza_operacoes_distintas_proc_nfe(self):
        '''Define ano da data atual como ponteiro para não trazer as naturezas de anos muito retrógrados'''
        ano_data_atual = datetime.now().year
        lista_operacoes = []
        cursor = self.__conn.cursor()
        sql_str = (
            f'''
            SELECT	DISTINCT
                    nota.natOp		AS	desc_natureza_nota
              FROM	K_Conlog_ProcNFe nota (NOLOCK)
              WHERE YEAR(nota.dhEmi) = {ano_data_atual}
            '''
        )
        cursor.execute(sql_str)
        notas_cursor = cursor.fetchall()
        for row in notas_cursor:
            op = {
                'desc_operacao': row.desc_natureza_nota
            }
            lista_operacoes.append(op)
        cursor.close()
        self.__conn.close()
        return lista_operacoes

    def retorna_dados_nota_proc_nfe(self, numero_nota, data_ini, data_fim, chave_nota):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        lista_notas = []
        cursor = self.__conn.cursor()
        param_num_nota = ''
        if numero_nota != '':
            param_num_nota = f'AND	nota.nNF = {numero_nota}'
        sql_str = ''
        if numero_nota != 0:
            sql_str = (f'''
                SELECT	DISTINCT
                        nota.nNF		AS	num_nota,
                        nota.serie		AS	serie_nota,
                        nota.chNFe		AS	chave_nota,
                        nota.natOp		AS	natureza_nota,
                        nota.dhEmi		AS	emissao_nota,
                        nota.emit_cnpj	AS	doc_fornecedor_nota,
                        nota.emit_nome	AS	nome_fornec_nota,
                        nota.vNF		AS	valor_nota,
                        fil.EMPRESA		AS	handle_empresa_nota,
                        fil.HANDLE      AS  handle_filial_nota,
                        fil.NOME		AS	nome_filial_nota
                  FROM	K_Conlog_ProcNFe nota (NOLOCK)
                  LEFT	JOIN FILIAIS fil (NOLOCK)
                    ON	((REPLACE(REPLACE(REPLACE(fil.CGC,'.',''),'-',''),'/','')) = nota.dest_cnpj)            
                 WHERE	CAST(nota.dhEmi AS DATE) BETWEEN '{data_ini}'	AND	'{data_fim}'
                        {param_num_nota}

                '''
                       )
        else:
            sql_str = (f'''
                SELECT	DISTINCT
                        nota.nNF		AS	num_nota,
                        nota.serie		AS	serie_nota,
                        nota.chNFe		AS	chave_nota,
                        nota.natOp		AS	natureza_nota,
                        nota.dhEmi		AS	emissao_nota,
                        nota.emit_cnpj	AS	doc_fornecedor_nota,
                        nota.emit_nome	AS	nome_fornec_nota,
                        nota.vNF		AS	valor_nota,
                        fil.EMPRESA		AS	handle_empresa_nota,
                        fil.HANDLE      AS  handle_filial_nota,
                        fil.NOME		AS	nome_filial_nota
                  FROM	K_Conlog_ProcNFe nota (NOLOCK)
                  LEFT	JOIN FILIAIS fil (NOLOCK)
                    ON	((REPLACE(REPLACE(REPLACE(fil.CGC,'.',''),'-',''),'/','')) = nota.dest_cnpj)            
                 WHERE	nota.chNFe = '{chave_nota}'
                '''
                       )
        cursor.execute(sql_str)
        notas_cursor = cursor.fetchall()
        for row in notas_cursor:
            nome_empresa = 'Conlog'
            if row.handle_empresa_nota == 17:
                nome_empresa = 'Deep'

            nota = {
                'num_nota': row.num_nota,
                'serie_nota': row.serie_nota,
                'chave_nota': row.chave_nota,
                'natureza_nota': row.natureza_nota,
                'emissao_nota': datetime.strftime(row.emissao_nota, '%d-%m-%Y'),
                'doc_fornecedor_nota': row.doc_fornecedor_nota,
                'nome_fornec_nota': row.nome_fornec_nota,
                'valor_nota': locale.currency(row.valor_nota, grouping=True, symbol=None),
                'handle_empresa_nota': row.handle_empresa_nota,
                'nome_empresa_nota': nome_empresa,
                'handle_filial_nota': row.handle_filial_nota,
                'nome_filial_nota': row.nome_filial_nota
            }
            lista_notas.append(nota)
        cursor.close()
        self.__conn.close()
        return lista_notas

    def compras_diesel(self, handle_filial, data_ini, data_fim):
        cursor = self.__conn.cursor()
        sql_compras_diesel = (
            f'''
                SELECT  itens_compra.handle						AS	handle_itens_compra,
                        itens_compra.ordemcompra				AS	handle_compra_itens_compra,         
                        compra.numero							AS	numero_compra,
                        compra.datadaordem						AS	data_ordem_compra,
                        compra.FILIAL				 			AS	handle_filial_compra,  
                        fil.NOME					 			AS	nome_filial_compra,         
                        receb_fisico_pai.numeronotafiscal		AS	numero_nota_fiscal_compra,
                        receb_fisico_pai.dataemissao			AS	data_emissao_nf_compra,     		
                        itens_compra.quantidade					AS	qtd_compra_itens_compra,            
                        itens_compra.valortotal					AS	val_total_itens_compra,            
                        itens_compra.produto					AS	handle_produto_itens_compra,
                        prod_itens_compra.nome					AS	desc_produto_itens_compra,
                        prod_itens_compra.codigo				AS	cod_produto_itens_compra,
                        prod_itens_compra.codigoreferencia		AS	cod_ref_produto_itens_compra,
                        prod_itens_compra.tipo					AS	tipo_produto_itens_compra,
                        itens_compra.unidade					AS	unid_medida_prod_itens_compra,
                        unid_medida_itens_compra.abreviatura	AS	abrev_unid_medida_prod_itens_compra,
                        itens_compra.descontosvalor				AS	desconto_val_itens_compra,                     
                        compra.fornecedor						AS	handle_fornecedor_comra,
                        fornecedor.nome							AS	nome_fornecedor_compra,
                        fornecedor.cgccpf						AS	doc_fornecedor_compra,
                        itens_compra.valorunitario				AS	val_unit_itens_compra,

                        COALESCE((SELECT	TOP 1 oci.valorunitario
                                    FROM	cp_ordenscompraitens oci (NOLOCK)
                               LEFT JOIN 	CP_ORDENSCOMPRA oc (NOLOCK)
                                      ON	(oc.handle = oci.ordemcompra)
                               LEFT	JOIN	pd_produtos prod	(NOLOCK)
                                      ON	(prod.handle = oci.produto) 
                                LEFT JOIN	gn_pessoas forn (NOLOCK)
                                       ON	(forn.handle = oc.fornecedor)
                                    WHERE	oci.handle < itens_compra.handle
                                      AND	prod.handle = prod_itens_compra.handle
                                      AND	forn.handle = fornecedor.handle
                                      AND	oc.FILIAL = compra.FILIAL
                                      AND	oc.status = 4    
                                 ORDER BY   oci.handle desc)
                            ,0)									AS	val_anterior_item_compra              

                FROM    cp_ordenscompraitens itens_compra (NOLOCK)
           LEFT	JOIN    cp_ordenscompra compra (NOLOCK)
                  ON	(compra.handle = itens_compra.ordemcompra)
           LEFT	JOIN    FILIAIS fil (NOLOCK)
                  ON	(fil.handle = compra.FILIAL)
           LEFT	JOIN    gn_pessoas fornecedor (NOLOCK)
                  ON	(fornecedor.handle = compra.fornecedor)
           LEFT	JOIN    CP_RECEBIMENTOFISICO receb_fisico (NOLOCK)
                  ON	((receb_fisico.ordemcompraitem = itens_compra.handle)
                 AND	(receb_fisico.produto = itens_compra.produto))
           LEFT	JOIN    CP_RECEBIMENTOFISICOPAI receb_fisico_pai (NOLOCK)
                  ON	(receb_fisico_pai.handle = receb_fisico.recebimentofisicopai)
           LEFT	JOIN    pd_produtos prod_itens_compra	(NOLOCK)
                  ON	(prod_itens_compra.handle = itens_compra.produto)      
           LEFT	JOIN    cm_unidadesmedida unid_medida_itens_compra (NOLOCK)
                  ON	(unid_medida_itens_compra.handle = itens_compra.unidade)
           LEFT	JOIN    gn_projetos proj_itens_compra (NOLOCK)
                  ON	(proj_itens_compra.handle = itens_compra.projeto)      
               WHERE	compra.datadaordem BETWEEN '{data_ini}' AND '{data_fim}'
                 AND	prod_itens_compra.familia in (5)
                 AND	prod_itens_compra.nome like '%OLEO DIESEL%'
                 AND	compra.FILIAL = {handle_filial}
                 AND	compra.status = 4 /* compra encerrada */
           ORDER  BY    fil.NOME, fornecedor.nome, prod_itens_compra.nome,compra.handle, itens_compra.handle  ;
                            '''
        )
        cursor.execute(sql_compras_diesel)
        lista_compras = cursor.fetchall()
        cursor.close()
        self.__conn.close()
        return lista_compras


    def retorna_roteiros_frota(self):
        cursor = self.__conn.cursor()
        lista_roteiros = []
        sql_roteiros = (
            f'''
            SELECT	distinct
                    roteiro.handle					AS	handle_roteiro,	
                    roteiro.nome		        	AS	nome_roteiro,
                    pm.handle						AS	handle_marca,
                    pm.NOME							AS	marca,
                    model.handle					AS	handle_modelo,
                    model.NOME						AS	modelo_placa,
                    tipo.HANDLE					    AS	handle_tipo_veic,
                    tipo.NOME						AS	desc_tipo_veic
          FROM	MA_ROTEIROMANUTENCAO roteiro (NOLOCK)
          LEFT	JOIN MF_VEICULOMANUTENCAOPREVENTIVA vmp (NOLOCK)
            ON	(vmp.MANUTENCAO = roteiro.HANDLE)
          LEFT	JOIN MA_RECURSOS veic (NOLOCK)
            ON	(veic.HANDLE = vmp.VEICULO
           AND	veic.ATIVO = 'S')
          LEFT	JOIN FILIAIS fil (NOLOCK)
            ON	(fil.HANDLE = veic.LOCALFILIAL) 
          LEFT  JOIN MF_PARTEMARCAS pm (NOLOCK)  
            ON	pm.HANDLE = veic.MARCAVEICULO
          LEFT	JOIN MF_VEICULOMODELOS model (NOLOCK)
            ON	model.HANDLE = veic.MODELOVEICULO
          LEFT  JOIN MF_VEICULOTIPOS tipo (NOLOCK)
            ON	(tipo.handle = model.TIPOVEICULO)
         WHERE	veic.EMPRESA IS NOT NULL 
           AND	(roteiro.nome LIKE '%PREV%' OR roteiro.nome LIKE '%REVISÃO%')
           AND	roteiro.INUTILIZAR = 'N'
           AND	fil.NOME LIKE '%AMBEV%'
         GROUP	BY roteiro.handle	,
                    roteiro.nome,
                    veic.FILIAL,
                    fil.NOME,
                    pm.handle,
                    pm.NOME,
                    model.handle,
                    model.NOME,
                    tipo.HANDLE,
                    tipo.NOME;
            '''
        )
        cursor.execute(sql_roteiros)
        roteiro_cursor = cursor.fetchall()
        for row in roteiro_cursor:
            roteiro = {
                'chave_reg': str(row.handle_roteiro)+'_'+str(row.handle_marca)+'_'+str(row.handle_modelo)+'_'+\
                    str(row.handle_tipo_veic),
                'handle_roteiro': row.handle_roteiro,
                'nome_roteiro': row.nome_roteiro,
                'handle_marca': row.handle_marca,
                'marca': row.marca,
                'handle_modelo': row.handle_modelo,
                'modelo': row.modelo_placa,
                'desc_tipo_veic': row.desc_tipo_veic
            }
            lista_roteiros.append(roteiro)
        cursor.close()
        self.__conn.close()
        return lista_roteiros


    def retorna_descricao_prod_cod_ref(self, cod_ref):
        cursor = self.__conn.cursor()
        lista_roteiros = []
        sql_roteiros = (
            f'''
            SELECT	distinct cast(item.DESCRICAO AS VARCHAR(MAX))	
								AS descricao,
                    un.NOME			AS	unidade
              FROM	PD_PRODUTOS item (NOLOCK)
              LEFT	JOIN CM_UNIDADESMEDIDA un (NOLOCK)
                ON	( un.HANDLE = item.UNIDADEMEDIDAESTOQUE)
             WHERE	item.CODIGOREFERENCIA = '{cod_ref}'
               AND  item.EMPRESA = 12;
            '''
        )
        cursor.execute(sql_roteiros)
        item = cursor.fetchone()
        cursor.close()
        self.__conn.close()
        desc_item = ''
        if item != None:
            desc_item = item.descricao+'_'+item.unidade
        return desc_item

    def atualiza_dados_parcela(self, handle_parcela):
        '''Objeto a retornar'''
        lista_parcelas_contrato_benner = []

        '''Processamento'''
        cursor = self.__conn.cursor()
        sql_parcelas = (
            f'''
            SELECT  fn_parc.VALOR 					AS	val_conta,
                    CAST(fn_parc.VCTOPRORROGADO AS DATE)		
                                                    AS data_vencimento,
                    CASE	WHEN DATEDIFF(MONTH,'20221231',fn_parc.VCTOPRORROGADO) > 12 
                        THEN	'LP'
                     ELSE 'CP'
                    END 							AS	tipo_prazo,
                    CAST(fn_parc.DATALIQUIDACAO AS DATE)		
                                                    AS	data_liquidacao,
                    fn_mov.VALORTOTAL		        AS	val_corrigido,
                    MAX(fn_lan_principal.VALOR)		AS	val_fn_principal,
                    (SELECT MIN(lan_taxas.VALOR)
                       FROM FN_LANCAMENTOS lan_taxas (NOLOCK)
                       LEFT JOIN FN_CONTAS con_taxas (NOLOCK)
                         ON (con_taxas.HANDLE = lan_taxas.CONTA)
                      WHERE lan_taxas.PARCELA = fn_parc.handle
                        AND	lan_taxas.TIPO = '3'
                        AND lan_taxas.ORIGEM = 2
                        AND	con_taxas.NOME LIKE '%TAXA%')	AS	val_fn_taxas
              FROM	FN_PARCELAS fn_parc (NOLOCK)
              LEFT	JOIN FN_MOVIMENTACOES fn_mov (NOLOCK) 
                ON	(fn_mov.PARCELA = fn_parc.HANDLE 
                AND	fn_mov.tipomovimento = 1
                AND	fn_mov.AUTORIZACAOPAGAMENTO IS NOT NULL)
              LEFT	JOIN FN_LANCAMENTOS fn_lan_principal (NOLOCK) 
                ON	(fn_lan_principal.PARCELA = fn_parc.HANDLE
               AND	fn_lan_principal.TIPO = '3'
               AND 	fn_lan_principal.ORIGEM = 2	)
             WHERE	1 = 1
               AND	fn_parc.handle = {handle_parcela}
             GROUP	BY fn_parc.VALOR,
                    fn_parc.VCTOPRORROGADO,
                    fn_parc.DATALIQUIDACAO,
                    fn_mov.VALORTOTAL
             ORDER	BY fn_parc.AP;
               '''
        )
        cursor.execute(sql_parcelas)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            parcela = {
                'valor_conta': row.val_conta,
                'valor_corrigido': row.val_corrigido,
                'data_vencimento': row.data_vencimento,
                'tipo_prazo': row.tipo_prazo,
                'data_liquidacao': row.data_liquidacao,
                'val_total_pago': row.val_corrigido,
                'val_principal': row.val_fn_principal,
                'val_taxas': row.val_fn_taxas
            }
            lista_parcelas_contrato_benner.append(parcela)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_parcelas_contrato_benner

    def retorna_veiculos_proj_vendas(self, mostra_veic_vendidos):
        '''Objeto a retornar'''
        lista_veiculos_venda = []

        '''Processamento'''
        cursor = self.__conn.cursor()
        param_mostra_veic_vendidos = ''
        if mostra_veic_vendidos == 'N':
            param_mostra_veic_vendidos = (" AND (veic.K_DATADEVENDA is Null AND veic.k_valordevenda is Null AND "
                                          " (veic.k_numnf = '' OR veic.k_numnf is Null) AND (comprador.NOME = '' OR comprador.NOME is Null))")


        sql_veic_venda = (
            f'''
            SELECT	veic.HANDLE			AS	handle_veic,
                    veic.PLACANUMERO	AS	placa_veic,
                    veic.TIPOVEICULO	AS	handle_tipo_veic,
                    tipo_veic.NOME 		AS	desc_tipo_veic,
                    veic.MARCA 			AS	handle_marca_veic,
                    marca.NOME 			AS	desc_marca_veic,
                    veic.MODELOVEICULO 	AS	handle_modelo_veic,
                    modelos.NOME 		AS	desc_modelo_veic,
                    YEAR(veic.ANO) 		AS	ano_veic,
                    veic.RENAVAM 		AS	renavam_veic,
                    veic.ESTADOCOMPRA 	AS	handle_estado_compra_veic,
                    uf.SIGLA  			AS	estado_compra_veic,
                    veic.FILIALMANUTENCAO 
                                        AS	handle_filial_veic,
                    fil.NOME 			AS	nome_filial_veic,
                    veic.K_EIXO 		AS	eixo_veic,
                    veic.ATIVO 			AS	status_ativo_veic,
                    CAST(veic.K_DATADEVENDA AS DATE)
                                        AS	data_venda_veic,
                    veic.k_valordevenda
                                        AS	val_venda_veic,
                    veic.k_numnf		AS	num_nf_veic,
                    veic.k_comprador	AS	handle_comprador_veic,		
		            comprador.NOME		AS	nome_comprador_veic,
		            veic.K_VALORCOMPRACAMI 
		            					AS	val_compra_veic
              FROM	MA_RECURSOS veic (NOLOCK)
              LEFT	JOIN MF_VEICULOTIPOS tipo_veic (NOLOCK)
                ON	(tipo_veic.HANDLE = veic.TIPOVEICULO)
              LEFT 	JOIN MF_PARTEMARCAS marca (NOLOCK) 
                ON	(marca.HANDLE = veic.MARCA)
              LEFT 	JOIN MF_VEICULOMODELOS modelos (NOLOCK)
                ON	(modelos.HANDLE = veic.MODELOVEICULO)
              LEFT 	JOIN ESTADOS uf (NOLOCK)
                ON	(uf.HANDLE = veic.ESTADOCOMPRA)
              LEFT 	JOIN FILIAIS fil (NOLOCK)
                ON	(fil.HANDLE = veic.FILIALMANUTENCAO)
              LEFT 	JOIN GN_PESSOAS comprador (NOLOCK)
                ON	(comprador.HANDLE = veic.k_comprador)
             WHERE	veic.PROJETO = 128
               AND  veic.EMPRESA  = 12
               AND  (tipo_veic.NOME like '%CAMINHAO%'
                OR  tipo_veic.NOME in ( 'CAVALO MECANICO'))
               {param_mostra_veic_vendidos};
             '''
        )
        cursor.execute(sql_veic_venda)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            placa = {
                'handle_veic': row.handle_veic,
                'placa_veic': row.placa_veic,
                'handle_tipo_veic': row.handle_tipo_veic,
                'desc_tipo_veic': row.desc_tipo_veic,
                'handle_marca_veic': row.handle_marca_veic,
                'desc_marca_veic': row.desc_marca_veic,
                'handle_modelo_veic': row.handle_modelo_veic,
                'desc_modelo_veic': row.desc_modelo_veic,
                'ano_veic': row.ano_veic,
                'renavam_veic': row.renavam_veic,
                'handle_estado_compra_veic': row.handle_estado_compra_veic,
                'estado_compra_veic': row.estado_compra_veic,
                'handle_filial_veic': row.handle_filial_veic,
                'nome_filial_veic': row.nome_filial_veic,
                'eixo_veic': row.eixo_veic,
                'status_ativo_veic': row.status_ativo_veic,
                'data_venda_veic': row.data_venda_veic,
                'val_venda_veic': row.val_venda_veic,
                'num_nf_veic': row.num_nf_veic,
                'handle_comprador': row.handle_comprador_veic,
                'nome_comprador': row.nome_comprador_veic,
                'val_compra_veic': row.val_compra_veic
            }
            lista_veiculos_venda.append(placa)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_veiculos_venda

