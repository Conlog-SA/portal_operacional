import locale
from datetime import datetime
import pyodbc
import pandas as pd
from django.shortcuts import render


class ConexaoBancoConecta():
    def __init__(self):
        self.__conn = pyodbc.connect(
            'DRIVER={MySQL ODBC 8.0 Unicode Driver};'
            'SERVER=172.16.40.13;'
            'DATABASE=conecta;'
            'UID=ti;'
            'PWD=ti@con.01;'
        )

    def retorna_dados_mapas(self, cod_promax, data_ini, data_final):
        '''Objeto a retornar'''
        lista_mapas = []

        '''Processamento'''
        cursor = self.__conn.cursor()
        sql_mapas = (
            f'''
            SELECT  id,
                    data,
                    entrega,
                    placa,
                    mapa,
                    codfilial
              FROM mapas_2art map
              LEFT JOIN filiais fil
                ON (fil.cod_filial_promax = map.codfilial)
             WHERE map.codfilial = {cod_promax}
               AND map.data BETWEEN '{data_ini}' AND '{data_final}';
            '''

        )
        cursor.execute(sql_mapas)
        registros_cursor = cursor.fetchall()
        for row in registros_cursor:
            reg = {
                'id' : row.id,
                'data' : row.data,
                'entrega': row.entrega,
                'placa': row.placa,
                'mapa': row.mapa,
                'cod_filial_promax': row.codfilial
            }
            lista_mapas.append(reg)

        '''Fecha componentes'''
        cursor.close()
        self.__conn.close()

        return lista_mapas

    def existe_mapa(self, cod_promax, mapa):
        cursor = self.__conn.cursor()

        sql = f"""
            SELECT mapa,
                   codfilial
            FROM mapas_2art
            WHERE codfilial = {cod_promax}
              AND mapa = '{mapa}'
            LIMIT 1;
        """

        cursor.execute(sql)
        resultado = cursor.fetchone()

        cursor.close()
        self.__conn.close()

        return resultado is not None


