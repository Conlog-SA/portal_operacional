from datetime import datetime

import pyodbc
from django.shortcuts import render

from apps.calendario_app.models import Calendario_Dias
from apps.ti_tma_app.models import Chamado_Atendido_TMA


class ConexaoHelpDesk():
    def __init__(self):
        self.__conn = pyodbc.connect(
            'DRIVER={MySQL };'
            'SERVER=itjm-srv-250;'
            'DATABASE=bd_portal_chamados;'
            'UID=danilo.costa;'
            'PWD=dap@1104!;'
        )

        '''DRIVER={MySQL ODBC 8.0 ANSI Driver};'''

    def retorna_chamados_atendidos(self):
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
                    )								AS	login_atend_ch
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
               
             WHERE	ch.id_status = 5               
               AND  ch.id_chamado = 99920766
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
        for row in chamados_cursor:

            data_ini = datetime.strptime(row.data_abertura_ch, '%Y-%m-%d')
            data_fim = datetime.strptime(row.data_atendido_ch, '%Y-%m-%d')
            print(f'Data ini: {data_ini}, data fim: {data_fim}')
            data_prevista_sql = (Calendario_Dias.objects
                                 .filter(data_dia__range=[data_ini,data_fim], classificacao_dia='U'))
            for data in data_prevista_sql:
                print(data)
            '''obj_chamado = Chamado_Atendido_TMA(
                row.id_ch,
                row.login_usu_abr_ch,
                row.desc_top_ch,
                row.desc_sub_topico_ch,
                row.data_abertura_ch,
                row.data_atendido_ch,
                row.sla_horas_ch,
                data_sla = data_prevista_sql,
                login_atendente = row.login_atend_ch
            )'''

        return None


