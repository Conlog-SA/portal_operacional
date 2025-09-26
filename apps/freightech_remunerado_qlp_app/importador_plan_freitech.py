import os
import pandas as pd
from datetime import datetime

from django.core.files.storage import FileSystemStorage

from apps.freightech_remunerado_qlp_app.models import Cargos_Freightech, \
    Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm, Registros_Plan_Remunerado_Freightech_Rota_Qlp_Equipe_Entrega, \
    Registros_Plan_Remunerado_Freightech_Rota_Equipe_Entrega_Beneficios
from proj_portal_operacional.settings import BASE_DIR


class Importador_Plan_Freightech():
    obj_arquivo = None
    arquivo_freightech = None
    uploaded_file_url = None
    desc_layout_arq = ''
    def __init__(self, arquivo_freightech, desc_layout_arq, obj_arquivo ):
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')

        caminho_arq_importado = 'docs/plan_rem_freightech/' + str(arquivo_freightech.name).replace('.xlsx', '') + '_' + \
                                str(data_atual_dd_mm_yyyy).replace('/', '_') \
                                + '_' + str(hota_atual).replace(':', '_') + '.xlsx'
        fs = FileSystemStorage()
        filename = fs.save(caminho_arq_importado, arquivo_freightech)
        self.uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado)

        if desc_layout_arq == 'QLP_ROTA_ADM_EQUIPE':
            self.rota_qlp_adm(obj_arquivo)
            self.rota_qlp_equipe_entrega(obj_arquivo)
            self.rota_beneficios_equipe_entrega(obj_arquivo)



    def rota_qlp_adm(self, obj_arquivo):
        df_qlp_adm = pd.read_excel(self.uploaded_file_url, 'QLP_ADM')
        df_qlp_adm.rename(columns=lambda x: str(x).strip(), inplace=True)
        for index, row in df_qlp_adm.iterrows():
            obj_cargo_freightech = (Cargos_Freightech.objects
                                    .filter(grupo_cargo=row['Cargo'].split(' | Classificação: ')[1],
                                            desc_cargo=row['Cargo'].split('|')[0].split(':')[1]).first())
            if obj_cargo_freightech == None:
                obj_cargo_freightech = Cargos_Freightech(
                    grupo_cargo = row['Cargo'].split(' | Classificação: ')[1],
                    desc_cargo = row['Cargo'].split('|')[0].split(':')[1]
                )
                obj_cargo_freightech.save()
            data_vigencia_reg = datetime.strptime(f'{row["Vigencia"].split("_")[3]}-{row["Vigencia"].split("_")[2]}-01', '%Y-%m-%d')
            quinzena_reg = row['Vigencia'].split('_')[1]
            obj_qlp_adm = ((Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm.objects
                           .filter(vigencia=data_vigencia_reg,
                                   quinzena=quinzena_reg,
                                   nome_unidade=row['Unidade - Nome'],
                                   cod_cargo_freightech=obj_cargo_freightech))
                           .first())
            if obj_qlp_adm == None:
                if row['QLP Benchmark Quantidade'] > 0:
                    obj_qlp_adm = Registros_Plan_Remunerado_Freightech_Rota_Qlp_Adm(
                        vigencia =  data_vigencia_reg,
                        quinzena = quinzena_reg,
                        nome_unidade =  row['Unidade - Nome'],
                        val_unit_beneficio =  row['Valor Benefício'],
                        val_unit_encargos = row['Salário Encargos'],
                        val_unit_frota_leve = row['Valor Frota Leve'],
                        val_unit_ordenados =  row['Salário Ordenados'],
                        val_unit_telefonia = row['Valor Telefonia'],
                        val_unit_uniformes = row['Valor Uniformes'],
                        val_bench_salarios = row['QLP Benchmark Salário'],
                        qtd_qlp_bench = row['QLP Benchmark Quantidade'],
                        qtd_beneficios = row['Quantidade Benefício'],
                        qtd_encargos = row['Quantidade Encargos'],
                        qtd_frota_leve = row['Quantidade Frota Leve'],
                        qtd_ordenados = row['Quantidade Ordenados'],
                        qtd_telefonia = row['Quantidade Telefonia'],
                        qtd_uniformes = row['Quantidade Uniformes'],
                        id_reg_plan = row['_id'],
                        cod_cargo_freightech = obj_cargo_freightech,
                        cod_plan_rem_freigh = obj_arquivo
                    )
                    obj_qlp_adm.save()
            else:
                if row['QLP Benchmark Quantidade'] == 0:
                    obj_qlp_adm.delete()
                else:
                    obj_qlp_adm.vigencia = data_vigencia_reg
                    obj_qlp_adm.quinzena = quinzena_reg
                    obj_qlp_adm.nome_unidade = row['Unidade - Nome']
                    obj_qlp_adm.val_unit_beneficio = row['Valor Benefício']
                    obj_qlp_adm.val_unit_encargos = row['Salário Encargos']
                    obj_qlp_adm.val_unit_frota_leve = row['Valor Frota Leve']
                    obj_qlp_adm.val_unit_ordenados = row['Salário Ordenados']
                    obj_qlp_adm.val_unit_telefonia = row['Valor Telefonia']
                    obj_qlp_adm.val_unit_uniformes = row['Valor Uniformes']
                    obj_qlp_adm.val_bench_salarios = row['QLP Benchmark Salário']
                    obj_qlp_adm.qtd_qlp_bench = row['QLP Benchmark Quantidade']
                    obj_qlp_adm.qtd_beneficios = row['Quantidade Benefício']
                    obj_qlp_adm.qtd_encargos = row['Quantidade Encargos']
                    obj_qlp_adm.qtd_frota_leve = row['Quantidade Frota Leve']
                    obj_qlp_adm.qtd_ordenados = row['Quantidade Ordenados']
                    obj_qlp_adm.qtd_telefonia = row['Quantidade Telefonia']
                    obj_qlp_adm.qtd_uniformes = row['Quantidade Uniformes']
                    obj_qlp_adm.id_reg_plan = row['_id']
                    obj_qlp_adm.cod_cargo_freightech = obj_cargo_freightech
                    obj_qlp_adm.cod_plan_rem_freigh = obj_arquivo
                    obj_qlp_adm.save()


    def rota_qlp_equipe_entrega(self, obj_arquivo):
        df_qlp_equipe_entrega = pd.read_excel(self.uploaded_file_url, 'QLP_EQUIPE_ENTREGA')
        df_qlp_equipe_entrega.rename(columns=lambda x: str(x).strip(), inplace=True)
        for index, row in df_qlp_equipe_entrega.iterrows():
            obj_cargo_freightech = (Cargos_Freightech.objects
                                    .filter(grupo_cargo='ENTREGA', desc_cargo=row['Cargo']).first())
            if obj_cargo_freightech == None:
                obj_cargo_freightech = Cargos_Freightech(
                    grupo_cargo = 'ENTREGA',
                    desc_cargo = row['Cargo']
                )
                obj_cargo_freightech.save()
            data_vigencia_reg = datetime.strptime(f'{row["Vigencia"].split("_")[3]}-{row["Vigencia"].split("_")[2]}-01',
                                      '%Y-%m-%d')
            quinzena_reg = row['Vigencia'].split('_')[1]
            obj_qlp_equipe_entrega = (Registros_Plan_Remunerado_Freightech_Rota_Qlp_Equipe_Entrega
                                      .objects.filter(vigencia=data_vigencia_reg,
                                                      quinzena=quinzena_reg,
                                                      nome_unidade=row['Unidade - Nome'],
                                                      cod_cargo_freightech=obj_cargo_freightech,
                                                      turno=row['Turno'])
                                      .first())
            if obj_qlp_equipe_entrega == None:
                obj_qlp_equipe_entrega = Registros_Plan_Remunerado_Freightech_Rota_Qlp_Equipe_Entrega(
                    nome_unidade = row['Unidade - Nome'],
                    vigencia = data_vigencia_reg,
                    quinzena = quinzena_reg,
                    turno = row['Turno'],
                    qtd_dsr = row['DSR'],
                    hora_extra_fixa = row['Hora Extra Fixa'],
                    qtd_horas_extra_fixa = row['Quantidade Hora Extra Fixa'],
                    val_outros = row['Outros'],
                    perc_abs = row['Percentual Absenteísmo'],
                    perc_encargo_prov = row['Percentual Encargo e Provisão'],
                    perc_hora_extra = row['Percentual Hora Extra'],
                    perc_turn_over = row['Percentual Turn Over Ano'],
                    premiacao_plus = row['Premiação Plus'],
                    qtd_total_por_caminhao_ativo = row['Quantidade Total x Caminhão Ativo'],
                    qtd_por_caminhao = row['Quantidade por Caminhão'],
                    val_rem_fixa_contra_cheque = row['Remuneração Fixa Contra Cheque'],
                    val_total_ordenado = row['Total Ordenado'],
                    val_total_remuneracao = row['Total Remuneração'],
                    val_total_remuneracao_com_beneficio = row['Total Remuneração Benefício'],
                    id_reg_plan = row['_id'],
                    cod_plan_rem_freigh = obj_arquivo,
                    cod_cargo_freightech = obj_cargo_freightech
                )
                obj_qlp_equipe_entrega.save()
            else:
                obj_qlp_equipe_entrega.nome_unidade = row['Unidade - Nome']
                obj_qlp_equipe_entrega.vigencia = data_vigencia_reg
                obj_qlp_equipe_entrega.quinzena = quinzena_reg
                obj_qlp_equipe_entrega.turno = row['Turno']
                obj_qlp_equipe_entrega.qtd_dsr = row['DSR']
                obj_qlp_equipe_entrega.hora_extra_fixa = row['Hora Extra Fixa']
                obj_qlp_equipe_entrega.qtd_horas_extra_fixa = row['Quantidade Hora Extra Fixa']
                obj_qlp_equipe_entrega.val_outros = row['Outros']
                obj_qlp_equipe_entrega.perc_abs = row['Percentual Absenteísmo']
                obj_qlp_equipe_entrega.perc_encargo_prov = row['Percentual Encargo e Provisão']
                obj_qlp_equipe_entrega.perc_hora_extra = row['Percentual Hora Extra']
                obj_qlp_equipe_entrega.perc_turn_over = row['Percentual Turn Over Ano']
                obj_qlp_equipe_entrega.premiacao_plus = row['Premiação Plus']
                obj_qlp_equipe_entrega.qtd_total_por_caminhao_ativo = row['Quantidade Total x Caminhão Ativo']
                obj_qlp_equipe_entrega.qtd_por_caminhao = row['Quantidade por Caminhão']
                obj_qlp_equipe_entrega.val_rem_fixa_contra_cheque = row['Remuneração Fixa Contra Cheque']
                obj_qlp_equipe_entrega.val_total_ordenado = row['Total Ordenado']
                obj_qlp_equipe_entrega.val_total_remuneracao = row['Total Remuneração']
                obj_qlp_equipe_entrega.val_total_remuneracao_com_beneficio = row['Total Remuneração Benefício']
                obj_qlp_equipe_entrega.cod_plan_rem_freigh = obj_arquivo
                obj_qlp_equipe_entrega.cod_cargo_freightech = obj_cargo_freightech
                obj_qlp_equipe_entrega.save()


    def rota_beneficios_equipe_entrega(self, obj_arquivo):
        df_benef_equipe_entrega = pd.read_excel(self.uploaded_file_url, 'BENEFICIOS_EQUIPE')
        df_benef_equipe_entrega.rename(columns=lambda x: str(x).strip(), inplace=True)
        for index, row in df_benef_equipe_entrega.iterrows():
            obj_cargo_freightech = (Cargos_Freightech.objects
                                    .filter(grupo_cargo='ENTREGA', desc_cargo=row['Cargo']).first())
            if obj_cargo_freightech == None:
                obj_cargo_freightech = Cargos_Freightech(
                    grupo_cargo = 'ENTREGA',
                    desc_cargo = row['Cargo']
                )
                obj_cargo_freightech.save()
            obj_benef_equipe_entrega = (Registros_Plan_Remunerado_Freightech_Rota_Equipe_Entrega_Beneficios
                                        .objects.filter(id_reg_plan=row['_id']).first())
            if obj_benef_equipe_entrega == None:
                obj_benef_equipe_entrega = Registros_Plan_Remunerado_Freightech_Rota_Equipe_Entrega_Beneficios(
                    nome_unidade = row['Unidade - Nome'],
                    desc_beneficio = row['Benefício'].split('|')[0].split(':')[1],
                    vigencia =  datetime.strptime(f'{row["Vigencia"].split("_")[3]}-{row["Vigencia"].split("_")[2]}-01',
                                      '%Y-%m-%d'),
                    quinzena = row['Vigencia'].split('_')[1],
                    turno = row['Turno'],
                    val_total_beneficio = row['Total Benefício'],
                    eh_noturna = 'N',
                    id_reg_plan = row['_id'],
                    cod_cargo_freightech = obj_cargo_freightech,
                    cod_plan_rem_freigh = obj_arquivo
                )
                obj_benef_equipe_entrega.save()
            else:
                obj_benef_equipe_entrega.nome_unidade = row['Unidade - Nome']
                obj_benef_equipe_entrega.desc_beneficio = row['Benefício'].split('|')[0].split(':')[1]
                obj_benef_equipe_entrega.vigencia = datetime.strptime(f'{row["Vigencia"].split("_")[3]}-{row["Vigencia"].split("_")[2]}-01',
                                      '%Y-%m-%d')
                obj_benef_equipe_entrega.quinzena = row['Vigencia'].split('_')[1]
                obj_benef_equipe_entrega.turno = row['Turno']
                obj_benef_equipe_entrega.val_total_beneficio = row['Total Benefício']
                obj_benef_equipe_entrega.eh_noturna = 'N'
                obj_benef_equipe_entrega.cod_cargo_freightech = obj_cargo_freightech
                obj_benef_equipe_entrega.cod_plan_rem_freigh = obj_arquivo
                obj_benef_equipe_entrega.save()





'''
    def retorna_cod_filial_erps(self, nome_unidade_arquivo):
        handle_unidade = 0
        cod_r018ccu_senior = 0
        if nome_unidade_arquivo == 'CDD CAMBORIU':
            handle_unidade = 870
            cod_r018ccu_senior = '1.01.01.006'
        elif nome_unidade_arquivo == 'CDD CUIABA':
            handle_unidade = 1050
            cod_r018ccu_senior = '1.01.14.004'
        elif nome_unidade_arquivo == 'CDD FLORIANOPOLIS':
            handle_unidade = 872
            cod_r018ccu_senior = '1.01.05.007'
        elif nome_unidade_arquivo == 'CDD GUARULHOS':
            handle_unidade = 19
            cod_r018ccu_senior = '1.01.03.001'
        elif nome_unidade_arquivo == 'CDD PELOTAS':
            handle_unidade = 874
            cod_r018ccu_senior = '1.01.09.005'
        elif nome_unidade_arquivo == 'CDD RIO DE JANEIRO':
            handle_unidade = 871
            cod_r018ccu_senior = '1.01.02.003'
        elif nome_unidade_arquivo == 'MACACU':
            handle_unidade = 1030
            cod_r018ccu_senior = '1.01.13.002'
        elif nome_unidade_arquivo == 'UDC GUARULHOS':
            handle_unidade = 921
            cod_r018ccu_senior = '1.01.03.007'

        return handle_unidade, cod_r018ccu_senior'''
