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
                    'situacao_colab': row.SITUACAO_COLAB,

                }
                data.append(colab)
            cursor.close()
            self.__conn.close()
            return data

    def pesquisar_dados_colaborador_por_cpf_emp(self, cpf, cod_empresa):
        lista_colabs = {}
        print(cpf)
        print(cod_empresa)
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
                WHERE A.NUMCPF = ?
                AND C.NUMEMP = ?''', [int(cpf.split('.')[0]), int(cod_empresa)])
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



