import pyodbc
import pandas as pd
import calendar
from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


class Conexao_Senior_BD():
    empresa = None
    def __init__(self, empresa):
        if empresa == 12:
            self.__conn = pyodbc.connect(
                'Driver={SQL Server};'
                'Server=itjm-srv-018;'
                'Database=vetorh;'
                'UID=servico.portais;'
                'PWD=qm@WHpAWwb')
        elif empresa == 17:
            self.__conn = pyodbc.connect(
                'Driver={SQL Server};'
                'Server=itjm-srv-018;'
                'Database=vetorh_deep;'
                'UID=servico.portais;'
                'PWD=qm@WHpAWwb')

    def listar_colaboradores_filial(self, id_empresa_senior, id_filial_senior):
        lista_colabs = {}
        cursor = self.__conn.cursor()
        cursor.execute(f'''SELECT DISTINCT A.NUMCAD   AS ID, 
                A.NOMFUN   AS NOME_FUNC,
                A.SITAFA   AS  cod_situacao,
                CASE WHEN A.SITAFA = 7
                        THEN 'Desligado'
                        ELSE 'Ativo' END
                        AS  SITUACAO_COLAB
                FROM R034FUN A (NOLOCK)
                LEFT JOIN R030FIL C (NOLOCK) ON ( C.CODFIL = A.CODFIL AND C.NUMEMP = A.NUMEMP)
                WHERE A.TIPCOL = 1
                AND C.CODFIL = {id_filial_senior}
                ORDER BY A.SITAFA ASC, A.NOMFUN''')
        if cursor is not None:
            data = []
            for row in cursor:
                colab = {
                    'cod_colab': row.ID,
                    'nome_colab': row.NOME_FUNC,
                    'status_colab': row.SITUACAO_COLAB
                }
                data.append(colab)
            cursor.close()
            self.__conn.close()
            return data

    def listar_dados_colaborador(self, id_senior_colab):
        lista_colabs = {}
        cursor = self.__conn.cursor()
        cursor.execute(f'''SELECT DISTINCT A.NUMCAD   AS ID, 
                A.NOMFUN   AS NOME_FUNC,
                A.NUMCPF   AS CPF,
                A.DATADM   AS DATA_ADMISSAO,
                A.CODCAR   AS COD_CARGO,
                B.TITCAR   AS DESC_CARGO,
                CASE WHEN A.SITAFA = 7
                        THEN 'Desligado'
                        ELSE 'Ativo' END
                        AS  SITUACAO_COLAB,
                        A.SITAFA   AS  cod_situacao
                FROM R034FUN A (NOLOCK)
                LEFT JOIN R024CAR B (NOLOCK) ON B.CODCAR = A.CODCAR 
                LEFT JOIN R030FIL C (NOLOCK) ON ( C.CODFIL = A.CODFIL AND C.NUMEMP = A.NUMEMP)
                WHERE A.NUMCAD = {id_senior_colab}
                ORDER BY A.SITAFA, A.NOMFUN DESC''')
        if cursor is not None:
            data = []
            for row in cursor:
                colab = {
                    'nome_colab': row.NOME_FUNC,
                    'cod_cargo_colab': row.COD_CARGO,
                    'desc_cargo_colab': row.DESC_CARGO,
                    'data_admissao_colab': row.DATA_ADMISSAO,
                    'cpf_colab': row.CPF,
                    'matricula_colab': row.ID,
                    'situacao_colab': row.SITUACAO_COLAB
                }
                data.append(colab)
            cursor.close()
            self.__conn.close()
            return data

    def pesquisar_dados_colaborador_por_cpf_emp(self, cpf, cod_empresa):
        cursor = self.__conn.cursor()
        cursor.execute(f'''SELECT DISTINCT A.NUMCAD   AS ID, 
                A.NOMFUN   AS NOME_FUNC,
                A.NUMCPF   AS CPF,
                B.TITCAR   AS DESC_CARGO,
                C.CODFIL   AS COD_FIL,
                C.NOMFIL   AS NOM_FIL,
                A.SITAFA 	AS  SITUACAO_COLAB,
                A.CODCCU AS COD_PROJ,
                D.NOMCCU AS NOM_PROJ,
                (SELECT COUNT(NUMCPF) FROM r034fun (NOLOCK) GROUP BY NUMCPF HAVING NUMCPF = ?) AS QTD_REGISTROS_COL
                
                FROM R034FUN A (NOLOCK)
                LEFT JOIN R024CAR B (NOLOCK) ON B.CODCAR = A.CODCAR 
                LEFT JOIN R030FIL C (NOLOCK) ON ( C.CODFIL = A.CODFIL AND C.NUMEMP = A.NUMEMP)
                LEFT JOIN R018CCU D (NOLOCK) ON (D.NUMEMP = A.NUMEMP AND D.CODCCU = A.CODCCU)
                WHERE A.NUMCPF = ?
                AND C.NUMEMP = ?
                GROUP BY 
                        A.NUMCAD, 
                        A.NOMFUN,
                        A.NUMCPF,
                        B.TITCAR,
                        C.CODFIL,
                        C.NOMFIL,
                        A.SITAFA,
                        A.CODCCU,
                        D.NOMCCU''', [int(cpf.split('.')[0]), int(cpf.split('.')[0]), int(cod_empresa)])
        result = list(cursor.fetchall())
        result = [reg for reg in result if reg.QTD_REGISTROS_COL == 1 or reg.QTD_REGISTROS_COL > 1 and reg.SITUACAO_COLAB == 1]
        if cursor is not None and len(result) == 1:
            colaborador = result[0]
            data = {
                    'nome_colab': colaborador.NOME_FUNC,
                    'desc_cargo_colab': colaborador.DESC_CARGO,
                    'cod_filial_colab': colaborador.COD_FIL,
                    'nom_filial_colab': colaborador.NOM_FIL,
                    'cod_projeto_colab': colaborador.COD_PROJ,
                    'nom_projeto_colab': colaborador.NOM_PROJ,
                    'cpf_colab': colaborador.CPF,
                    'matricula_colab': colaborador.ID,
                    'situacao_colab': colaborador.SITUACAO_COLAB,
            }
            cursor.close()
            self.__conn.close()
            return data

        else:
            if len(cursor.fetchall()) == 0 or cursor is None:
                print('nao achou')
                data = {
                    'erro': 'Colaborador não encontrado'
                }
                return data
            if len(cursor.fetchall()) > 1:
                print('achou mais de 1')
                data = {
                    'erro': 'Colaborador duplicado'
                }
                return data

    def pesquisar_dados_dependente_por_cpf_emp(self, cpf):
        cursor = self.__conn.cursor()
        cursor.execute(f'''SELECT 
                                dep.numemp AS NUMEMP,
                                col.numcpf AS CPF
                            FROM vetorh.dbo.r036dep dep
                            LEFT JOIN R034FUN col (NOLOCK)
                            ON (col.numcad = dep.numcad AND col.tipcol = dep.tipcol)
                            WHERE dep.numemp = 1
                            AND dep.numcpf = ?
                            ''', [int(cpf.split('.')[0])])
        result = cursor.fetchall()
        if cursor is not None and len(result) == 1:
            dependente = result[0]
            if dependente.NUMEMP == 1:
                numemp = 12
            elif dependente.NUMEMP == 2:
                numemp = 17
            info_titular = self.pesquisar_dados_colaborador_por_cpf_emp(dependente.CPF, numemp)

            return info_titular

    def pesquisar_dados_por_matricula(self, matricula, cod_empresa):
        cursor = self.__conn.cursor()
        cursor.execute(f'''SELECT DISTINCT A.NUMCAD   AS ID, 
                A.NOMFUN   AS NOME_FUNC,
                A.NUMCPF   AS CPF,
                B.TITCAR   AS DESC_CARGO,
                C.CODFIL   AS COD_FIL,
                C.NOMFIL   AS NOM_FIL,
                CASE WHEN A.SITAFA = 7
                        THEN 'Desligado'
                        ELSE 'Ativo' END
                        AS  SITUACAO_COLAB,
                A.CODCCU AS COD_PROJ,
                D.NOMCCU AS NOM_PROJ

                FROM R034FUN A (NOLOCK)
                LEFT JOIN R024CAR B (NOLOCK) ON B.CODCAR = A.CODCAR 
                LEFT JOIN R030FIL C (NOLOCK) ON ( C.CODFIL = A.CODFIL AND C.NUMEMP = A.NUMEMP)
                LEFT JOIN R018CCU D (NOLOCK) ON (D.NUMEMP = A.NUMEMP AND D.CODCCU = A.CODCCU)
                WHERE A.NUMCAD = ?
                AND C.NUMEMP = ?''', [int(matricula), int(cod_empresa)])
        result = cursor.fetchall()
        if cursor is not None and len(result) == 1:
            colaborador = result[0]
            data = {
                'nome_colab': colaborador.NOME_FUNC,
                'desc_cargo_colab': colaborador.DESC_CARGO,
                'cod_filial_colab': colaborador.COD_FIL,
                'nom_filial_colab': colaborador.NOM_FIL,
                'cod_projeto_colab': colaborador.COD_PROJ,
                'nom_projeto_colab': colaborador.NOM_PROJ,
                'cpf_colab': colaborador.CPF,
                'matricula_colab': colaborador.ID,
                'situacao_colab': colaborador.SITUACAO_COLAB,
            }
            cursor.close()
            self.__conn.close()
            return data
        else:
            columns = [column[0] for column in cursor.description]
            print(columns)
            if len(cursor.fetchall()) == 0 or cursor is None:
                data = {
                    'erro': 'Colaborador não encontrado'
                }
                return data
            if len(cursor.fetchall()) > 1:
                data = {
                    'erro': 'Colaborador duplicado'
                }
                return data

    def retorna_df_folha_pagamento(self, data_ref, lista_handle_proj):
        sql_query_folha_pagamento_proeventos = (
                '''
                    SELECT 
                        val_folha.tipcol		AS	tip_col,
                        val_folha.numemp		AS	cod_empresa,
                        val_folha.numcad		AS	mat_colab,
                        fun.nomfun				AS	nome_colab,
                        hist_cargo.CODCAR		AS	cod_cargo,
                        cargo.TITRED			AS	desc_cargo,
                        hist_filial.codfil		AS	cod_filial,
                        fil.nomfil				AS	nome_filial,
                        hist_cc.CODCCU			AS	cod_projeto,
                        cc.nomccu				AS	nome_projeto,
                        cc.usu_handle   		AS	handle_proj_benner,
                        val_folha.codcal		AS	cod_cal,
                        eve.codclc 				AS	cod_conta_contabil,
                        CASE WHEN eve.codclc = 0 
                            THEN 'Sem Conta Vinculada'
                            ELSE conta.nomcon	
                        END						AS	desc_conta_contabil,
                        val_folha.codeve		AS	cod_evento,
                        eve.deseve				AS	evento,
                        CASE WHEN eve.tipeve = 3
                             THEN val_folha.valeve * -1
                             ELSE val_folha.valeve
                        END               		AS	val_evento,
                        CASE WHEN eve.tipeve in (1,2)
                             THEN val_folha.refeve
                             ELSE 0.00                   
                        END             		AS	horas_ref,
                        cal.perref				AS	periodo_ref,
                        cal.inicmp				AS	inicio_periodo_ref,
                        cal.fimcmp				AS	fim_periodo_ref, 
                        fun.sitafa				AS	cod_atual_sit,
                        sit_atual.dessit		AS	desc_atual_sit
                    FROM r046ver val_folha(NOLOCK)
                    LEFT JOIN r034fun fun (NOLOCK)
                      ON (fun.numemp = val_folha.numemp 
                     AND fun.tipcol = val_folha.tipcol 
                     AND fun.numcad = val_folha.numcad)
                    LEFT JOIN r044cal cal (NOLOCK)
                      ON (cal.numemp = fun.numemp
                     AND cal.codcal = val_folha.codcal)
                    LEFT JOIN r008evc eve (NOLOCK)
                      ON (eve.codeve = val_folha.codeve
                     AND eve.codtab = val_folha.tabeve)
                    LEFT JOIN r048clc conta (NOLOCK)
                      ON (conta.tabeve = eve.codtab
                     AND conta.codclc = eve.codclc)
                    LEFT JOIN R038HCA hist_cargo(NOLOCK)
                      ON (hist_cargo.NUMEMP = fun.NUMEMP
                     AND hist_cargo.TIPCOL = fun.TIPCOL 
                     AND hist_cargo.NUMCAD = fun.NUMCAD)
                    LEFT JOIN R024CAR cargo (NOLOCK)
                      ON (cargo.ESTCAR = hist_cargo.ESTCAR
                     AND cargo.CODCAR = hist_cargo.CODCAR)
                    LEFT JOIN R038HFI hist_filial (NOLOCK)
                      ON (hist_filial.NUMEMP = fun.NUMEMP
                     AND hist_filial.TIPCOL = fun.TIPCOL 
                     AND hist_filial.NUMCAD = fun.NUMCAD)
                    LEFT JOIN R030FIL fil (NOLOCK)
                      ON (fil.NUMEMP = hist_filial.NUMEMP
                     AND fil.CODFIL = hist_filial.CODFIL)
                    LEFT JOIN R038HCC hist_cc (NOLOCK)
                      ON (hist_cc.NUMEMP = fun.NUMEMP
                     AND hist_cc.TIPCOL = fun.TIPCOL
                     AND hist_cc.NUMCAD = fun.NUMCAD)
                    LEFT JOIN R018CCU cc (NOLOCK)
                      ON (cc.NUMEMP = hist_cc.NUMEMP
                     AND cc.CODCCU = hist_cc.CODCCU)             
    
                    LEFT JOIN R010SIT sit_atual (NOLOCK)
                      ON sit_atual.CODSIT = fun.sitafa
                   WHERE eve.tipeve in (1,2,3,4,5)
                     AND hist_filial.DATALT = (SELECT MAX(DATALT) 
                                                    FROM R038HFI TABELA001 (NOLOCK) 
                                                   WHERE TABELA001.NUMEMP = hist_filial.NUMEMP 
                                                     AND TABELA001.TIPCOL = hist_filial.TIPCOL 
                                                     AND TABELA001.NUMCAD = hist_filial.NUMCAD 
                                                     AND TABELA001.DATALT <= cal.fimcmp)
                     AND hist_cc.DATALT = (SELECT MAX(DATALT) 
                                                    FROM R038HCC TABELA002 (NOLOCK) 
                                                   WHERE TABELA002.NUMEMP = hist_cc.NUMEMP 
                                                     AND TABELA002.TIPCOL = hist_cc.TIPCOL 
                                                     AND TABELA002.NUMCAD = hist_cc.NUMCAD 
                                                     AND TABELA002.DATALT <= cal.fimcmp)                                  
                     AND hist_cargo.DATALT = (SELECT MAX(DATALT) 
                                                    FROM R038HCA TABELA003 (NOLOCK) 
                                                   WHERE TABELA003.NUMEMP = hist_cargo.NUMEMP 
                                                     AND TABELA003.TIPCOL = hist_cargo.TIPCOL 
                                                     AND TABELA003.NUMCAD = hist_cargo.NUMCAD 
                                                     AND TABELA003.DATALT <= cal.fimcmp) 
    
                ''' +
                " AND cal.perref = '" + data_ref + "' " +
                " AND cc.usu_handle in (" + str(lista_handle_proj).replace('[', '').replace(']', '') + ") " +
                '''           
                    ORDER BY 4, 17 DESC
                '''
        )
        df_folha_pag_proeventos = pd.read_sql(sql_query_folha_pagamento_proeventos, self.__conn)
        self.__conn.close()
        return df_folha_pag_proeventos

    def retorna_df_provisao_folha_senior(self, data_ref, lista_handle_proj, cod_tipo_provisao):
        data_ref_fim_date = datetime.strptime(data_ref, '%Y-%m-%d')
        data_ref_fim_str = datetime.strftime(
            data_ref_fim_date.replace(day = calendar.monthrange(data_ref_fim_date.year, data_ref_fim_date.month)[1]),
            '%Y-%m-%d')
        sql_query_provisao_folha = (
            '''
                SELECT	CAST(prov_mestre.MESANO AS DATE)	
                                            as	periodo,
                    emp.numemp				as	cod_emp,
                    emp.nomemp				as	nome_emp,
                    fil.codfil				as	cod_filial,
                    fil.nomfil				as	nome_filial,
                    ccu.codccu				as 	cod_ccu,
                    ccu.nomccu				as 	desc_ccu,
                    ccu.usu_handle			as 	handle_proj,
                    fun.numcad				as	mat_fun,
                    fun.nomfun				as 	nome_fun,
                    hist_cargo.CODCAR		AS	cod_cargo,
                    cargo.TITRED			AS	desc_cargo,
                    CAST(fun.datadm AS DATE)				
                                            as	data_adm,
                    tipo_prov.desval		as	desc_prov,
                    prov.basprv				as	val_base_prov,
                    prov.perval				as	perc_dias_prov,
                    prov.salant				as	val_anterior_prov,
                    prov.saltrf				as	val_transf_prov,
                    prov.ajuprv				as	val_ajuste_prov,
                    prov.prvmes				as	val_prov,
                    prov.valpag				as	val_pag_prov,
                    prov.valind				as	val_indenizado_prov,
                    prov.sldatu				as	val_saldo_prov	
                FROM R146PRV prov (NOLOCK)
                LEFT JOIN R030EMP emp (NOLOCK)
                    ON (emp.numemp = prov.numemp)
                LEFT JOIN R034FUN fun (NOLOCK)
                    ON (fun.numcad = prov.numcad
                    AND fun.tipcol = prov.tipcol
                    AND fun.numemp = prov.numemp)
                LEFT JOIN R146DET tipo_prov (NOLOCK)
                    ON (tipo_prov.tipprv = prov.tipprv
                   AND tipo_prov.tipval = prov.tipval)
                LEFT JOIN R146DEF def_prov (NOLOCK)
                    ON (def_prov.tipprv = tipo_prov.tipprv)
                LEFT JOIN R146PRM prov_mestre (NOLOCK)
                    ON (prov_mestre.numcad = prov.numcad
                    AND prov_mestre.numemp = prov.numemp
                    AND prov_mestre.tipcol = prov.tipcol	
                    AND prov_mestre.mesano = prov.mesano
                    AND prov_mestre.tipprv = prov.tipprv
                    AND prov_mestre.seqprv = prov.seqprv)
                LEFT JOIN R038HCC hist_ccu (NOLOCK)
                    ON (hist_ccu.NUMEMP = prov_mestre.NUMEMP
                    AND hist_ccu.TIPCOL = prov_mestre.TIPCOL
                    AND hist_ccu.NUMCAD = prov_mestre.NUMCAD
                    AND hist_ccu.CODCCU = prov_mestre.CODCCU)   
                LEFT JOIN R018CCU ccu (NOLOCK)
                    ON (ccu.NUMEMP = hist_ccu.NUMEMP
                    AND ccu.CODCCU = hist_ccu.CODCCU)
                LEFT JOIN R038HFI hist_filial (NOLOCK)
                    ON (hist_filial.NUMEMP = fun.NUMEMP
                    AND hist_filial.TIPCOL = fun.TIPCOL 
                    AND hist_filial.NUMCAD = fun.NUMCAD)
                LEFT JOIN R030FIL fil (NOLOCK)
                    ON (fil.NUMEMP = hist_filial.NUMEMP
                    AND fil.CODFIL = hist_filial.CODFIL)
                LEFT JOIN R038HCA hist_cargo(NOLOCK)
                  ON (hist_cargo.NUMEMP = fun.NUMEMP
                 AND hist_cargo.TIPCOL = fun.TIPCOL 
                 AND hist_cargo.NUMCAD = fun.NUMCAD)
                LEFT JOIN R024CAR cargo (NOLOCK)
                  ON (cargo.ESTCAR = hist_cargo.ESTCAR
                 AND cargo.CODCAR = hist_cargo.CODCAR)
                WHERE ((prov_mestre.SEQPRV = 2) OR ((prov_mestre.SEQPRV = 1) AND (prov_mestre.TIPTRF <> 4)))
                    AND hist_ccu.DATALT = (SELECT MAX (HCC.DATALT) 
                                           FROM R038HCC HCC 
                                           WHERE HCC.NUMEMP = hist_ccu.NUMEMP 
                                            AND HCC.TIPCOL = hist_ccu.TIPCOL 
                                            AND HCC.NUMCAD = hist_ccu.NUMCAD 
                                            AND HCC.DATALT <= ''' + " '" + data_ref_fim_str + "' " +
                                            ''' AND HCC.CODCCU = hist_ccu.CODCCU )
                    AND hist_filial.DATALT = (SELECT MAX(DATALT) 
                                              FROM R038HFI TABELA001 (NOLOCK) 
                                              WHERE TABELA001.NUMEMP = hist_filial.NUMEMP 
                                                AND TABELA001.TIPCOL = hist_filial.TIPCOL 
                                                AND TABELA001.NUMCAD = hist_filial.NUMCAD 
                                                AND TABELA001.DATALT <= ''' + " '" + data_ref_fim_str + "' " + ') ' +
                    ''' AND hist_cargo.DATALT = (SELECT MAX(DATALT) 
                                               FROM R038HCA TABELA003 (NOLOCK) 
                                               WHERE TABELA003.NUMEMP = hist_cargo.NUMEMP 
                                                 AND TABELA003.TIPCOL = hist_cargo.TIPCOL 
                                                 AND TABELA003.NUMCAD = hist_cargo.NUMCAD 
                                                 AND TABELA003.DATALT <= ''' + " '" + data_ref_fim_str + "' " + ') ' +
                    ''' AND prov_mestre.TIPPRV = ''' + cod_tipo_provisao +
                    ''' AND prov_mestre.MESANO = ''' + " '" + data_ref + "' " +
                    ''' AND  fun.DATADM <= ''' + " '" + data_ref_fim_str + "' " +
                      " AND ccu.usu_handle in (" + str(lista_handle_proj).replace('[', '').replace(']', '') + ") " +
                    ''' AND EXISTS (SELECT 1 
                                 FROM R038HFI TAB2 
                                 WHERE TAB2.NUMEMP = fun.NUMEMP 
                                    AND TAB2.TIPCOL = fun.TIPCOL 
                                    AND TAB2.NUMCAD = fun.NUMCAD 
                                    AND TAB2.DATALT <= ''' + " '" + data_ref_fim_str + "' " + ') ' +
                '''ORDER BY emp.NUMEMP,
                    ccu.FILGRP,
                    ccu.CODCCU,
                    prov.NUMCAD,
                    prov.SEQPRV,
                    tipo_prov.TIPVAL;
            '''
        )
        df_provisao_folha_senior = pd.read_sql(sql_query_provisao_folha, self.__conn)
        self.__conn.close()
        return df_provisao_folha_senior

    def retorna_nome_filial_senior(self, codfil):
        cursor = self.__conn.cursor()
        cursor.execute(f'''SELECT DISTINCT 
                    NOMFIL
                FROM R030FIL A (NOLOCK)
                WHERE CODFIL = {codfil}''')
        result = cursor.fetchall()
        if cursor is not None and len(result) == 1:
            filial = result[0]
            data = {
                'nome_fil': filial.NOMFIL
            }
            cursor.close()
            self.__conn.close()
            return data
        else:
            columns = [column[0] for column in cursor.description]
            if len(cursor.fetchall()) == 0 or cursor is None:
                data = {
                    'erro': 'Filial não encontrada'
                }
                return data
            if len(cursor.fetchall()) > 1:
                data = {
                    'erro': 'Filial duplicada'
                }
                return data

    def retorna_qlp_por_periodo_e_filial(self, data_ref, cod_filial):
        sql_qlp= (
        f'''
           SELECT	distinct
                    R034FUN.NUMCAD		AS	matricula_colab,
                    R034FUN.NOMFUN		AS	nome_colab,
                    CAST(R034FUN.DATADM AS DATE)
                                        AS	dt_adm_colab,
                    CASE WHEN SIT_APU.CODSIT IN (7,22) 
                         THEN CAST(USU_TDIAEMP.USU_DIADAT AS DATE)
                         ELSE NULL 
                    END					AS	dt_demissao_colab,
                    CASE WHEN SIT_APU.CODSIT in (7 , 22)
                         THEN 'Inativo'
                         ELSE 'Ativo'
                    END					AS	status_colab,
                    CAST(USU_TDIAEMP.USU_DIADAT AS DATE)
                                        AS	data_qlp,
                    R030FIL.CODFIL		AS	cod_filial,
                    R030FIL.NOMFIL		AS	nome_filial,
                    R018CCU.CODCCU		AS 	cod_ccu_colab,
                    R018CCU.NOMCCU		AS	nome_ccu_colab,
                    R038HCA.CODCAR		AS	cod_cargo,
                    R024CAR.TITRED		AS	nome_cargo_colab,
                    COALESCE(frei.usu_codcar, 0)
                    	                AS	cod_cargo_freightech,
                    COALESCE(frei.usu_descar, '')
                    	                AS	desc_cargo_freightech    	           
             FROM	vetorh.dbo.R034FUN (NOLOCK)            
        LEFT JOIN	USU_TDIAEMP (NOLOCK)
               ON	(USU_TDIAEMP.USU_NUMEMP = R034FUN.NUMEMP)
        LEFT JOIN	R038HFI (NOLOCK)
               ON	(R038HFI.NUMEMP = R034FUN.NUMEMP) 
              AND	(R038HFI.TIPCOL = R034FUN.TIPCOL) 
              AND 	(R038HFI.NUMCAD = R034FUN.NUMCAD)
        LEFT JOIN	R030FIL (NOLOCK)
               ON	(R030FIL.NUMEMP = R038HFI.NUMEMP) 
              AND 	(R030FIL.CODFIL = R038HFI.CODFIL) 
        LEFT JOIN	R038HCC (NOLOCK)
               ON	(R038HCC.NUMEMP = R034FUN.NUMEMP) 
              AND 	(R038HCC.TIPCOL = R034FUN.TIPCOL) 
              AND	(R038HCC.NUMCAD = R034FUN.NUMCAD)
        LEFT JOIN	R018CCU (NOLOCK)
               ON	(R018CCU.NUMEMP = R038HCC.NUMEMP) 
              AND	(R018CCU.CODCCU = R038HCC.CODCCU)
        LEFT JOIN	R038HCA (NOLOCK)
               ON	(R038HCA.NUMEMP = R034FUN.NUMEMP) 
              AND	(R038HCA.TIPCOL = R034FUN.TIPCOL) 
              AND	(R038HCA.NUMCAD = R034FUN.NUMCAD)
        LEFT JOIN	R024CAR (NOLOCK)
               ON	(R024CAR.ESTCAR = R038HCA.ESTCAR) 
              AND	(R024CAR.CODCAR = R038HCA.CODCAR)
        LEFT JOIN	usu_tdesfre frei 
               ON	frei.usu_codcar = R024CAR.usu_desfre
        LEFT JOIN	R038HLO (NOLOCK)
               ON	(R038HLO.NUMEMP = R034FUN.NUMEMP) 
              AND	(R038HLO.TIPCOL = R034FUN.TIPCOL) 
              AND	(R038HLO.NUMCAD = R034FUN.NUMCAD)
        LEFT JOIN	R016ORN (NOLOCK)
               ON	(R016ORN.TABORG = R038HLO.TABORG) 
              AND	(R016ORN.NUMLOC = R038HLO.NUMLOC)
        LEFT JOIN	R038HES (NOLOCK)
               ON	(R038HES.NUMEMP = R034FUN.NUMEMP) 
              AND	(R038HES.TIPCOL = R034FUN.TIPCOL) 
              AND	(R038HES.NUMCAD = R034FUN.NUMCAD)
              
        LEFT JOIN	R038HPO (NOLOCK) 
               ON	(R038HPO.NUMEMP = R034FUN.NUMEMP) 
              AND	(R038HPO.TIPCOL = R034FUN.TIPCOL) 
              AND	(R038HPO.NUMCAD = R034FUN.NUMCAD) 
        LEFT JOIN	R017POS (NOLOCK)
               ON	(R017POS.ESTPOS = R038HPO.ESTPOS) 
              AND	(R017POS.POSTRA = R038HPO.POSTRA)    
        LEFT JOIN	R010SIT SIT_ATUAL (NOLOCK)
               ON	SIT_ATUAL.CODSIT = R034FUN.SITAFA    
               
        LEFT JOIN	r066apu (NOLOCK) 
               ON	(r066apu.NUMEMP = R034FUN.NUMEMP) 
              AND	(r066apu.TIPCOL = R034FUN.TIPCOL) 
              AND	(r066apu.NUMCAD = R034FUN.NUMCAD) 
              AND	(r066apu.DATAPU = USU_TDIAEMP.USU_DIADAT)
        LEFT JOIN	R004HOR HORA_APU (NOLOCK)
               ON	(HORA_APU.CODHOR = r066apu.HORDAT)
        LEFT JOIN	R066SIT (NOLOCK)  apu_sit 
               ON	(apu_sit.NUMEMP = r066apu.NUMEMP) 
              AND	(apu_sit.TIPCOL = r066apu.TIPCOL) 
              AND	(apu_sit.NUMCAD = r066apu.NUMCAD) 
              AND	(apu_sit.DATAPU = USU_TDIAEMP.USU_DIADAT)
        LEFT JOIN	R010SIT SIT_APU (NOLOCK)
               ON	SIT_APU.CODSIT = apu_sit.CODSIT  
              
            WHERE	USU_TDIAEMP.USU_DIADAT = '{data_ref}'     
              AND	R034FUN.NUMEMP = 1      
              AND	R034FUN.DATADM <= '{data_ref}' 
              AND	((R034FUN.SITAFA <> 7) OR ((R034FUN.SITAFA in (7,22)) AND (R034FUN.DATAFA >= '{data_ref}' )))
              AND	R034FUN.TIPCOL = 1
              AND	R030FIL.CODFIL = {cod_filial}
              AND	SIT_APU.CODSIT NOT IN (7,22) 
              AND 	R017POS.POSTRA <> '99_9999'
              AND	R038HFI.DATALT = (SELECT MAX(DATALT) 
                                        FROM R038HFI TABELA001 (NOLOCK) 
                                       WHERE TABELA001.NUMEMP = R038HFI.NUMEMP 
                                         AND TABELA001.TIPCOL = R038HFI.TIPCOL 
                                         AND TABELA001.NUMCAD = R038HFI.NUMCAD 
                                         AND TABELA001.DATALT <= USU_TDIAEMP.USU_DIADAT) 
              AND	R038HCC.DATALT = (SELECT MAX(DATALT) 
                                        FROM R038HCC TABELA002 (NOLOCK) 
                                       WHERE TABELA002.NUMEMP = R038HCC.NUMEMP 
                                         AND TABELA002.TIPCOL = R038HCC.TIPCOL AND TABELA002.NUMCAD = R038HCC.NUMCAD 
                                         AND TABELA002.DATALT <= USU_TDIAEMP.USU_DIADAT) 
              AND	R038HCA.DATALT = (SELECT MAX(DATALT) 
                                        FROM R038HCA TABELA003 (NOLOCK) 
                                       WHERE TABELA003.NUMEMP = R038HCA.NUMEMP 
                                         AND TABELA003.TIPCOL = R038HCA.TIPCOL 
                                         AND TABELA003.NUMCAD = R038HCA.NUMCAD 
                                         AND TABELA003.DATALT <= USU_TDIAEMP.USU_DIADAT) 
              AND	R038HLO.DATALT = (SELECT MAX(DATALT) 
                                        FROM R038HLO TABELA004 (NOLOCK) 
                                       WHERE TABELA004.NUMEMP = R038HLO.NUMEMP 
                                         AND TABELA004.TIPCOL = R038HLO.TIPCOL 
                                         AND TABELA004.NUMCAD = R038HLO.NUMCAD 
                                         AND TABELA004.DATALT <= USU_TDIAEMP.USU_DIADAT)
              AND	R038HES.DATALT = (SELECT MAX(DATALT) 
                                        FROM R038HES TABELA005 (NOLOCK) 
                                       WHERE TABELA005.NUMEMP = R038HES.NUMEMP 
                                         AND TABELA005.TIPCOL = R038HES.TIPCOL 
                                         AND TABELA005.NUMCAD = R038HES.NUMCAD 
                                         AND TABELA005.DATALT <= USU_TDIAEMP.USU_DIADAT)
              AND	R038HPO.INIATU = (SELECT MAX(INIATU) 
                                        FROM R038HPO TABELA006 (NOLOCK) 
                                       WHERE TABELA006.NUMEMP = R038HPO.NUMEMP 
                                         AND TABELA006.TIPCOL = R038HPO.TIPCOL 
                                         AND TABELA006.NUMCAD = R038HPO.NUMCAD 
                                         AND TABELA006.INIATU <= USU_TDIAEMP.USU_DIADAT)
            ORDER	BY R034FUN.NOMFUN
        '''
        )
        df_qlp = pd.read_sql(sql_qlp, self.__conn)
        self.__conn.close()
        return df_qlp


    def retorna_df_ordenados_por_periodo_e_filial(self, data_ref, cod_filial):
        sql_ordenados = (
            f'''
            SELECT  val_folha.tipcol		AS	tip_col,
                    val_folha.numemp		AS	cod_empresa,
                    val_folha.numcad		AS	mat_colab,
                    fun.nomfun				AS	nome_colab,
                    hist_cargo.CODCAR		AS	cod_cargo,
                    cargo.TITRED			AS	desc_cargo,
                    hist_filial.codfil		AS	cod_filial,
                    fil.nomfil				AS	nome_filial,
                    hist_cc.CODCCU			AS	cod_ccu_colab,
                    cc.nomccu				AS	nome_projeto,
                    sum(val_folha.valeve)	AS	val_evento
                FROM r046ver val_folha(NOLOCK)
                LEFT JOIN r034fun fun (NOLOCK)
                  ON (fun.numemp = val_folha.numemp 
                 AND fun.tipcol = val_folha.tipcol 
                 AND fun.numcad = val_folha.numcad)
                LEFT JOIN r044cal cal (NOLOCK)
                  ON (cal.numemp = fun.numemp
                 AND cal.codcal = val_folha.codcal)
                LEFT JOIN r008evc eve (NOLOCK)
                  ON (eve.codeve = val_folha.codeve
                 AND eve.codtab = val_folha.tabeve)
                LEFT JOIN r048clc conta (NOLOCK)
                  ON (conta.tabeve = eve.codtab
                 AND conta.codclc = eve.codclc)
                LEFT JOIN R038HCA hist_cargo(NOLOCK)
                  ON (hist_cargo.NUMEMP = fun.NUMEMP
                 AND hist_cargo.TIPCOL = fun.TIPCOL 
                 AND hist_cargo.NUMCAD = fun.NUMCAD)
                LEFT JOIN R024CAR cargo (NOLOCK)
                  ON (cargo.ESTCAR = hist_cargo.ESTCAR
                 AND cargo.CODCAR = hist_cargo.CODCAR)
                LEFT JOIN R038HFI hist_filial (NOLOCK)
                  ON (hist_filial.NUMEMP = fun.NUMEMP
                 AND hist_filial.TIPCOL = fun.TIPCOL 
                 AND hist_filial.NUMCAD = fun.NUMCAD)
                LEFT JOIN R030FIL fil (NOLOCK)
                  ON (fil.NUMEMP = hist_filial.NUMEMP
                 AND fil.CODFIL = hist_filial.CODFIL)
                LEFT JOIN R038HCC hist_cc (NOLOCK)
                  ON (hist_cc.NUMEMP = fun.NUMEMP
                 AND hist_cc.TIPCOL = fun.TIPCOL
                 AND hist_cc.NUMCAD = fun.NUMCAD)
                LEFT JOIN R018CCU cc (NOLOCK)
                  ON (cc.NUMEMP = hist_cc.NUMEMP
                 AND cc.CODCCU = hist_cc.CODCCU)             
            
                LEFT JOIN R010SIT sit_atual (NOLOCK)
                  ON sit_atual.CODSIT = fun.sitafa
               WHERE eve.tipeve = 1 /* Horas Normais Diurnas */
                 AND	val_folha.codeve = 1
                 AND	eve.codclc = 1 /*Salários e Ordenados (D) */
                     AND hist_filial.DATALT = (SELECT MAX(DATALT) 
                                                    FROM R038HFI TABELA001 (NOLOCK) 
                                                   WHERE TABELA001.NUMEMP = hist_filial.NUMEMP 
                                                     AND TABELA001.TIPCOL = hist_filial.TIPCOL 
                                                     AND TABELA001.NUMCAD = hist_filial.NUMCAD 
                                                     AND TABELA001.DATALT <= cal.fimcmp)
                     AND hist_cc.DATALT = (SELECT MAX(DATALT) 
                                                    FROM R038HCC TABELA002 (NOLOCK) 
                                                   WHERE TABELA002.NUMEMP = hist_cc.NUMEMP 
                                                     AND TABELA002.TIPCOL = hist_cc.TIPCOL 
                                                     AND TABELA002.NUMCAD = hist_cc.NUMCAD 
                                                     AND TABELA002.DATALT <= cal.fimcmp)                                  
                     AND hist_cargo.DATALT = (SELECT MAX(DATALT) 
                                                    FROM R038HCA TABELA003 (NOLOCK) 
                                                   WHERE TABELA003.NUMEMP = hist_cargo.NUMEMP 
                                                     AND TABELA003.TIPCOL = hist_cargo.TIPCOL 
                                                     AND TABELA003.NUMCAD = hist_cargo.NUMCAD 
                                                     AND TABELA003.DATALT <= cal.fimcmp) 
            
               
                    AND cal.perref = '{data_ref}'
                AND fil.CODFIL = {cod_filial}
                GROUP BY val_folha.tipcol,
                    val_folha.numemp,
                    val_folha.numcad,
                    fun.nomfun,
                    hist_cargo.CODCAR,
                    cargo.TITRED,
                    hist_filial.codfil,
                    fil.nomfil,
                    hist_cc.CODCCU,
                    cc.nomccu
                ORDER BY val_folha.numcad ASC;
            '''
        )
        df_ordenados = pd.read_sql(sql_ordenados, self.__conn)
        self.__conn.close()
        return df_ordenados

