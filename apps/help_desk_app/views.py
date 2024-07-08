from datetime import datetime
import mariadb
from django.http import JsonResponse
from django.shortcuts import render

from apps.calendario_app.models import Calendario_Dias
from apps.ti_tma_app.models import Chamado_Atendido_TMA
from apps.usuario_app.models import Usuario


class ConexaoHelpDesk():
    def __init__(self):
        self.__conn = mariadb.connect(
            user="kaian.almeida",
            password="Knd@7880!",
            host="172.16.40.250",
            port=3306,
            database="bd_portal_chamados",
        )

    def retorna_chamados_atendidos(self, data_ini_periodo, data_fim_periodo):
        lista_chamados_atendidos = []

        cursor = self.__conn.cursor()
        sql_chamados_atendidos =  (
            f'''
            SELECT	ch.id_chamado					AS	id_ch,
                    usu_abr.usuario					AS	login_usu_abr_ch,
                    top.descricao					AS	desc_top_ch,
                    sub_top.descricao				AS	desc_sub_topico_ch,
                    ch.data_abertura 				AS 	data_abertura_ch,
                    hist_status_atendido.data_status			
                                                    AS	data_atendido_ch,
                    pri.horas_sla					AS	sla_horas_ch,
                    status.descricao				AS	desc_status_ch,
                    (SELECT	usu.usuario
                       FROM	chm_alteracoes_status_chamado alt_usu
                       LEFT	JOIN chm_usuarios usu
                         ON	(usu.id_usu = alt_usu.id_usu)
                      WHERE	alt_usu.id_historico_status_chamado = MAX(atend_chm_abr.id_historico_status_chamado)            
                    )								AS	login_atend_ch,
                    
                    CASE when hist_status_espera.id_historico_status_chamado IS NULL then
                    		'N' ELSE 'S' END 		AS	status_ch_espera
              FROM	chm_chamados ch
              LEFT	JOIN chm_status_chamado status
                ON	(status.id_status = ch.id_status)
            
              LEFT	JOIN chm_sub_topicos_chamado sub_top
                ON	(sub_top.id_sub_topico_chamado = ch.id_sub_topico_chamado)
              LEFT 	JOIN chm_topicos_chamado top
                ON 	(top.id_topico_chamado = sub_top.id_topico_chamado)
              LEFT	JOIN chm_niveis_prioridade pri
                ON	(pri.id_prioridade = sub_top.id_prioridade)
                 
                 /* Retorna usuario abertura */
              LEFT	JOIN chm_alteracoes_status_chamado usu_chm_abr
                ON	(usu_chm_abr.id_chamado = ch.id_chamado
               AND	usu_chm_abr.id_status = 7)
              LEFT	JOIN chm_usuarios usu_abr
                ON	(usu_abr.id_usu = usu_chm_abr.id_usu
               AND	usu_abr.id_perfil_usu = 1)
                
                /* Retorna atendente do chamado */
              LEFT	JOIN chm_alteracoes_status_chamado atend_chm_abr
                ON	(atend_chm_abr.id_chamado = ch.id_chamado
               AND	atend_chm_abr.id_status = 1)
                
              /* Definir data do status atendido*/
              LEFT	JOIN chm_alteracoes_status_chamado hist_status_atendido
                ON	(hist_status_atendido.id_chamado = ch.id_chamado
               AND	hist_status_atendido.id_status in (5))
               
              /* Definir data do status cancelado*/
              LEFT	JOIN chm_alteracoes_status_chamado hist_status_cancelado
                ON	(hist_status_cancelado.id_chamado = ch.id_chamado
               AND	hist_status_cancelado.id_status in (6))
               
            /* Definir data do status esperando*/
              LEFT	JOIN chm_alteracoes_status_chamado hist_status_espera
                ON	(hist_status_espera.id_chamado = ch.id_chamado
					AND	hist_status_espera.id_status = 4)
               
             WHERE	ch.id_status = 5
                    AND CAST(hist_status_atendido.data_status AS DATE) BETWEEN '{data_ini_periodo}' AND '{data_fim_periodo}'
                    
              GROUP BY ch.id_chamado,
                    usu_abr.usuario,
                    top.descricao,
                    sub_top.descricao,
                    ch.data_abertura,
                    hist_status_atendido.data_status,
                    pri.horas_sla,
                    status.descricao;
            '''
        )
        cursor.execute(sql_chamados_atendidos)
        chamados_cursor = cursor.fetchall()
        for chamado in chamados_cursor:
            reg = {
                'num_chamado' : chamado[0],
                'login_usuario': chamado[1],
                'desc_topico': chamado[2],
                'desc_subtopico': chamado[3],
                'data_abertura': chamado[4],
                'data_fechamento': chamado[5],
                'sla_hora': chamado[6],
                'login_atendente': chamado[8],
                'status_ch_espera': chamado[9]
            }
            lista_chamados_atendidos.append(reg)
        return lista_chamados_atendidos

    def retorna_status_chamado(self, num_chamado):
        lista_status_chamado = []

        cursor = self.__conn.cursor()
        sql_status_chamados_atendidos = (
            f'''
            SELECT
                a.data_status,
                a.id_status,
                b.usuario
            FROM 
                chm_alteracoes_status_chamado a
            LEFT JOIN 
                chm_usuarios b
            ON 
                (a.id_usu = b.id_usu)
            WHERE 
                id_chamado = {num_chamado}
            ORDER BY 
                data_status ASC;
            '''
        )
        cursor.execute(sql_status_chamados_atendidos)
        status_cursor = cursor.fetchall()

        for status in status_cursor:
            reg = {
                'data_status' : status[0],
                'id_status': status[1],
                'usuario': status[2]
            }
            lista_status_chamado.append(reg)
        return lista_status_chamado

    def retorna_atendente(self, num_chamado):
        cursor = self.__conn.cursor()
        sql_status_chamados_atendidos = (
            f'''
                    SELECT
                        b.usuario
                    FROM 
                        chm_alteracoes_status_chamado a
                    LEFT JOIN 
                        chm_usuarios b
                    ON 
                        (a.id_usu = b.id_usu)
                    WHERE 
                        id_chamado = {num_chamado}
                        AND id_status = 5;
                    '''
        )
        cursor.execute(sql_status_chamados_atendidos)
        status = cursor.fetchone()

        return status[0]

    def retorna_chamado_by_cod(self, num_chamado):
        obj_chamado = None

        cursor = self.__conn.cursor()
        sql_chamados = (
            f'''
                SELECT	ch.id_chamado		    AS	id_ch,
                        ch.problema             AS  desc_problema,
                        usu_abr.usuario         AS  login_usu_abertura,
                        ch.data_abertura        AS  data_chamado,
                        atend.usuario           AS  login_atendente
                  FROM	chm_chamados ch
                  
                    /* Retorna usuario abertura */
                  LEFT	JOIN chm_alteracoes_status_chamado usu_chm_abr
                    ON	(usu_chm_abr.id_chamado = ch.id_chamado
                   AND	usu_chm_abr.id_status = 7)
                  LEFT	JOIN chm_usuarios usu_abr
                    ON	(usu_abr.id_usu = usu_chm_abr.id_usu
                   AND	usu_abr.id_perfil_usu = 1)

                    /* Retorna atendente do chamado */
                  LEFT	JOIN chm_alteracoes_status_chamado atend_chm_abr
                    ON	(atend_chm_abr.id_chamado = ch.id_chamado
                   AND	atend_chm_abr.id_status = 1)
                  LEFT  JOIN chm_usuarios atend
                    ON  (atend.id_usu = atend_chm_abr.id_usu)
                 WHERE	ch.id_chamado = {num_chamado};
                    '''
        )
        cursor.execute(sql_chamados)
        chamados_cursor = cursor.fetchone()

        cod_usu_abertura = 0
        obj_usu_abertura = Usuario.objects.filter(login_usu=chamados_cursor[2]).first()
        if obj_usu_abertura != None:
            cod_usu_abertura = obj_usu_abertura.cod_usu

        cod_usu_atendente = 0
        obj_usu_atendente = Usuario.objects.filter(login_usu=chamados_cursor[4]).first()
        if obj_usu_atendente != None:
            cod_usu_atendente = obj_usu_atendente.cod_usu
        dic_chamado = {
            'desc_problema': chamados_cursor[1],
            'data_chamado': datetime.strftime(chamados_cursor[3], '%Y-%m-%d'),
            'cod_usu_abertura': cod_usu_abertura,
            'cod_usu_atendente': cod_usu_atendente
        }
        return dic_chamado
