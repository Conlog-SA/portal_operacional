import pyodbc
import locale
from datetime import datetime
import pandas as pd


class ConexaoBancoNddWeb():
    def __init__(self):
        self.__conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ITJM-SRV-018;'
            'DATABASE=NDD_COLDWEB_420;'
            'UID=servico.ndd;'
            'PWD=JM@Jeg@v*z;'
        )


    def retorna_ctes(self, numero, data_ini, data_fim, chave):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        lista_ctes = []
        cursor = self.__conn.cursor()
        sql_cte_param = ''
        if numero !=  '' and numero != '0':
            sql_cte_param = (f"WHERE  CAST(IDE_DHEMI AS DATE) BETWEEN '{data_ini}' AND '{data_fim}'  "
                              f"AND IDE_NCT = {numero}")
        elif (numero == None or numero == '') and chave == '0':
            sql_cte_param = f"WHERE  CAST(IDE_DHEMI AS DATE) BETWEEN '{data_ini}' AND '{data_fim}'  "
        elif numero == '0' and chave != '0':
            sql_cte_param = f"WHERE  REPLACE(IDE_ID, 'CTe', '') = '{chave}' "

        sql_cte = (
            f'''
            SELECT  DISTINCT
                    IDE_NCT                     AS  NUMERO,
                    IDE_SERIE 					AS  SERIE,
                    REPLACE(IDE_ID, 'CTe', '') 	AS  CHAVE,
                    VPREST_VTPREST 				AS  VALOR,                    
                    IDE_DHEMI					AS  EMISSAO,
                    EMIT_CNPJ					AS	cnpj_cpf_fornecedor,
                    REM_CNPJ 					AS  REM_CNPJ,
                    DEST_CNPJ	 				AS  DEST_CNPJ,
                    TOMADOR_CNPJ				AS	cnpj_filial,
                    CASE WHEN STATUS_CTE=100 THEN 'Autorizado'
                         WHEN STATUS_CTE=101 THEN 'Cancelado'
                         WHEN STATUS_CTE=128 THEN 'Anulado'
                         WHEN STATUS_CTE=129 THEN 'Substituido'
                    END 						AS  STATUS 
              FROM  PRD_COLD_CTE_DEEP_ENTRY  (nolock)
              {sql_cte_param}
            '''
        )

        #cursor.execute(sql_cte)
        df_ctes = pd.read_sql(sql_cte, self.__conn)


        conn_benner = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ITJM-SRV-018;'
            'DATABASE=TRANSPORTES_PRODUCAO;'
            'UID=servico.portais;'
            'PWD=qm@WHpAWwb;'
        )
        sql_filiail_benner = (
            f'''
            SELECT  HANDLE		AS	handle_filial,
                    EMPRESA		AS	cod_emp_filial,
                    CASE WHEN EMPRESA = 12 THEN 'Conlog'
                         WHEN EMPRESA = 17 THEN 'Deep'
                    END         AS  nome_empresa,
                    NOME		AS	nome_filial,
                    CGC			AS	cnpj_filial
              FROM  FILIAIS (nolock)  
            '''
        )
        df_filiais = pd.read_sql(sql_filiail_benner, conn_benner)

        df_ctes_fillias = pd.merge(df_ctes, df_filiais,
                                   how='left',
                                   on=['cnpj_filial']).reset_index()

        sql_fornecedor_benner = (
            f'''
            SELECT	NOME			AS	nome_fornecedor,
                    CGCCPF			AS	cnpj_cpf_fornecedor                    
              FROM	GN_PESSOAS (nolock)
            '''
        )
        df_fornecedor = pd.read_sql(sql_fornecedor_benner, conn_benner)

        df_ctes_filiais_fornec = pd.merge(df_ctes_fillias, df_fornecedor,
                                          how='left',
                                          on=['cnpj_cpf_fornecedor']).reset_index()


        for index, row in df_ctes_filiais_fornec.iterrows():
            cte = {
                'num_nota': str(df_ctes_filiais_fornec.loc[index, 'NUMERO']),
                'serie_nota': str(df_ctes_filiais_fornec.loc[index, 'SERIE']),
                'chave_nota': str(df_ctes_filiais_fornec.loc[index, 'CHAVE']),
                'natureza_nota': 'CTe',
                'emissao_nota': datetime.strftime(df_ctes_filiais_fornec.loc[index, 'EMISSAO'], '%d-%m-%Y'),
                'doc_fornecedor_nota': str(df_ctes_filiais_fornec.loc[index, 'cnpj_cpf_fornecedor']),
                'nome_fornec_nota': str(df_ctes_filiais_fornec.loc[index, 'nome_fornecedor']),
                'valor_nota': locale.currency(df_ctes_filiais_fornec.loc[index, 'VALOR']),
                'handle_empresa_nota': str(df_ctes_filiais_fornec.loc[index, 'cod_emp_filial']),
                'nome_empresa_nota': str(df_ctes_filiais_fornec.loc[index, 'nome_empresa']),
                'handle_filial_nota': str(df_ctes_filiais_fornec.loc[index, 'handle_filial']),
                'nome_filial_nota': str(df_ctes_filiais_fornec.loc[index, 'nome_filial'])
            }
            lista_ctes.append(cte)
        return lista_ctes




