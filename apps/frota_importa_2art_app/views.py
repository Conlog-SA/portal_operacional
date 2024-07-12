from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.frota_importa_2art_app.models import Arquivo2Art, IndicaProjReg2Art, Registro2Art
from apps.usuario_app.models import Usuario

from datetime import datetime, date
import pandas as pd
import os

from proj_portal_operacional.settings import BASE_DIR


class Form_Importa_2art_View(View):
    def get(self, request):
        contexto = {
            'desc_menu': 'Importa 2art'
        }
        return render(request, 'frota_importa_2art_app/form_importa_2art.html', contexto)

    def post(self, request):
        myfile = request.FILES['file']
        cod_usu_session = request.session['cod_usuario_logado']

        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')
        caminho_arq_importado = 'docs/2art/' +obj_usu.cod_filial.unidade_abrev + '/2art_' + obj_usu.cod_filial.unidade_abrev + '_' + \
                                obj_usu.login_usu.replace('.', '_') + '_' + str(data_atual_dd_mm_yyyy).replace('/', '_') \
                                + '_' + str(hota_atual).replace(':', '_')+'.xlsx'
        arquivo_2art = Arquivo2Art(
            nome_arq_imp=caminho_arq_importado,
            nome_arq_original=str(myfile.name),
            cod_usu=obj_usu,
            qtd_registros=0,
            qtd_importados=0,
            qtd_atualizados=0
        )
        arquivo_2art.save()

        fs = FileSystemStorage()
        filename = fs.save(caminho_arq_importado, myfile)
        uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado)
        tab_mapas_nao_importados_2art = []
        conteudo_arq_2art = pd.read_excel(uploaded_file_url)
        conteudo_arq_2art.rename(columns=lambda x: str(x).strip(), inplace=True)
        count_reg_imp = 0
        count_reg_up = 0
        for index, row in conteudo_arq_2art.iterrows():
            data_mapa_str_sql = ''
            data_mapa_int = int(row['Data'])
            if len(str(data_mapa_int)) == 7:
                data_mapa_str_sql = str(data_mapa_int)[3:] + '/' + str(data_mapa_int)[1:3] + "/0" + str(data_mapa_int)[0:1]
            else:
                data_mapa_str_sql = str(data_mapa_int)[4:] + '/' + str(data_mapa_int)[2:4] + "/" + str(data_mapa_int)[0:2]
       

            obj_ind_proj = IndicaProjReg2Art.objects.filter(
                cod_filial_promax=str(int(row['CodFilial'])).strip(), tipo_entrega=str(row['Entrega']).strip(),
                tipo_frota=str(row['Frota']).strip()).first()

            if obj_ind_proj != None:
                try:
                    cod_reg_2art = int(str(int(row['Mapa'])) + str(int(row['CodFilial'])))
                    obj_registro_2art = Registro2Art.objects.filter(cod_reg_2art=cod_reg_2art).first()
                    if obj_registro_2art == None:

                        obj_registro_2art_new = Registro2Art(
                            cod_reg_2art=int(str(int(row['Mapa'])) + str(int(row['CodFilial']))),
                            data=datetime.strptime(data_mapa_str_sql, '%Y/%m/%d'),
                            transp=str(row['Transp']).strip(),
                            entrega=str(row['Entrega']).strip(),
                            cargaatual=str(row['CargaAtual']).strip(),
                            frota=str(row['Frota']).strip(),
                            custospot=str(row['CustoSpot']).strip(),
                            regiaospot=str(row['RegiaoSpot']).strip(),
                            veiculo=str(row['Veiculo']).strip(),
                            placa=str(row['Placa']).strip(),
                            veiculoindisp=str(row['VeiculoIndisp']).strip(),
                            placaindisp=str(row['PlacaIndisp']).strip(),
                            frotaindisp=str(row['FrotaIndisp']).strip(),
                            tipoindisp=str(row['TipoIndisp']).strip(),
                            mapa=str(int(row['Mapa'])).strip(),
                            entregas=str(row['Entregas']).strip(),
                            cxcarreg=str(row['CxCarreg']).strip(),
                            cxentreg=str(row['CxEntreg']).strip(),
                            ocupacao=str(row['Ocupacao']).strip(),
                            cxrota=str(row['CxRota']).strip(),
                            cxas=str(row['CxAS']).strip(),
                            veicbm=str(row['VeicBM']).strip(),
                            rshow=str(row['RShow']).strip(),
                            entrvol=str(row['EntrVol']).strip(),
                            hrsai=str(row['HrSai']).strip(),
                            hrentr=str(row['HrEntr']).strip(),
                            kmsai=str(row['KmSai']).strip(),
                            kmentr=str(row['KmEntr']).strip(),
                            custovariavel=str(row['CustoVariavel']).strip(),
                            lucro=str(row['Lucro']).strip(),
                            lucrounit=str(row['LucroUnit']).strip(),
                            valorfrete=str(row['ValorFrete']).strip(),
                            tipoimposto=str(row['TipoImposto']).strip(),
                            percimposto=str(row['PercImposto']).strip(),
                            valorimposto=str(row['ValorImposto']).strip(),
                            valorfaturado=str(row['ValorFaturado']).strip(),
                            valorunitcxentregue=str(row['ValorUnitCxEntregue']).strip(),
                            valorpgcxentregsemimp=str(row['ValorPgCxEntregSemImp']).strip(),
                            valorpgcxentregcomimp=str(row['ValorPgCxEntregComImp']).strip(),
                            tempoprevistoroad=str(row['TempoPrevistoRoad']).strip(),
                            kmprevistoroad=str(row['KmPrevistoRoad']).strip(),
                            valorunitpontomot=str(row['ValorUnitPontoMot']).strip(),
                            valorunitpontoajd=str(row['ValorUnitPontoAjd']).strip(),
                            valorequipeentrmot=str(row['ValorEquipeEntrMot']).strip(),
                            valorequipeentrajd=str(row['ValorEquipeEntrAjd']).strip(),
                            custovlc=str(row['CustoVLC']).strip(),
                            lucrounitcedbz=str(row['LucroUnitCEDBZ']).strip(),
                            custovlccxentr=str(row['CustoVlcCxEntr']).strip(),
                            tempointerno=str(row['TempoInterno']).strip(),
                            valordropdown=str(row['ValorDropDown']).strip(),
                            veiccaddd=str(row['VeicCadDD']).strip(),
                            kmlaco=str(row['KmLaco']).strip(),
                            kmdeslocamento=str(row['KmDeslocamento']).strip(),
                            tempolaco=str(row['TempoLaco']).strip(),
                            tempodeslocamento=str(row['TempoDeslocamento']).strip(),
                            sitmulticdd=str(row['SitMultiCDD']).strip(),
                            unborigem=str(row['UnbOrigem']).strip(),
                            matricmotorista=row['MatricMotorista'],
                            matricajud1=str(row['MatricAjud1']).strip(),
                            matricajud2=str(row['MatricAjud2']).strip(),
                            valorctedifere=str(row['ValorCTEDifere']).strip(),
                            qtnfcarregadas=str(row['QtNfCarregadas']).strip(),
                            qtnfentregues=str(row['QtNfEntregues']).strip(),
                            inddevcx=str(row['IndDevCx']).strip(),
                            inddevnf=str(row['IndDevNf']).strip(),
                            fator=str(row['Fator']).strip(),
                            recarga=str(row['Recarga']).strip(),
                            hrmatinal=str(row['HrMatinal']).strip(),
                            hrjornadaliq=str(row['HrJornadaLiq']).strip(),
                            hrmetajornada=str(row['HrMetaJornada']).strip(),
                            vlbateujornmot=str(row['VlBateuJornMot']).strip(),
                            vlnaobateujornmot=str(row['VlNaoBateuJornMot']).strip(),
                            vlrecargamot=str(row['VlRecargaMot']).strip(),
                            vlbateujornaju=str(row['VlBateuJornAju']).strip(),
                            vlnaobateujornaju=str(row['VlNaoBateuJornAju']).strip(),
                            vlrecargaaju=str(row['VlRecargaAju']).strip(),
                            vltotalmapa=str(row['VlTotalMapa']).strip(),
                            qthlcarregados=str(row['QtHlCarregados']).strip(),
                            qthlentregues=str(row['QtHlEntregues']).strip(),
                            indicedevhl=str(row['IndiceDevHl']).strip(),
                            regiao=str(row['Regiao']).strip(),
                            qtnfcarreggeral=str(row['QtNfCarregGeral']).strip(),
                            qtnfentreggeral=str(row['QtNfEntregGeral']).strip(),
                            capacidadeveiculokg=str(row['CapacidadeVeiculoKG']).strip(),
                            pesocargakg=str(row['PesoCargaKG']).strip(),
                            capacveiculocx=str(row['CapacVeiculoCx']).strip(),
                            entregascompletas=str(row['EntregasCompletas']).strip(),
                            entregasparciais=str(row['EntregasParciais']).strip(),
                            entregasnaorealizadas=str(row['EntregasNaoRealizadas']).strip(),
                            codfilial=str(row['CodFilial']).strip(),
                            nomefilial=str(row['NomeFilial']).strip(),
                            codsupervtrs=str(row['CodSupervTrs']).strip(),
                            nomesupervtrs=str(row['NomeSupervTrs']).strip(),
                            codspot=str(row['CodSpot']).strip(),
                            nomespot=str(row['NomeSpot']).strip(),
                            equipcarregados=str(row['EquipCarregados']).strip(),
                            equipdevolvidos=str(row['EquipDevolvidos']).strip(),
                            equiprecolhidos=str(row['EquipRecolhidos']).strip(),
                            cxentregtracking=str(row['CxEntregTracking']).strip(),
                            hrcarreg=str(row['HrCarreg']).strip(),
                            hrpcfisica=str(row['HrPCFisica']).strip(),
                            hrpcfinanceira=str(row['HrPCFinanceira']).strip(),
                            stmapa=str(row['StMapa']).strip(),
                            qtentregascarregrv=str(row['QtEntregasCarreg(RV)']).strip(),
                            qtentregasentregrv=str(row['QtEntregasEntreg(RV)']).strip(),
                            indicedeventregasrv=str(row['IndiceDevEntregas(RV)']).strip(),
                            cpfmotorista=str(row['CPFMotorista']).strip(),
                            cpfajudante1=str(row['CPFAjudante1']).strip(),
                            cpfajudante2=str(row['CPFAjudante2']).strip(),
                            alterado='N',
                            acao='I',
                            cod_reg_arq_imp=arquivo_2art,
                            cod_reg_indc_cod_reg_2art=obj_ind_proj
                        )
                        obj_registro_2art_new.save()
                        count_reg_imp += 1
                    else:
                        obj_registro_2art.transp=str(row['Transp']).strip()
                        obj_registro_2art.entrega=str(row['Entrega']).strip()
                        obj_registro_2art.cargaatual=str(row['CargaAtual']).strip()
                        obj_registro_2art.frota=str(row['Frota']).strip()
                        obj_registro_2art.custospot = str(row['CustoSpot']).strip()
                        obj_registro_2art.regiaospot = str(row['RegiaoSpot']).strip()
                        obj_registro_2art.veiculo = str(row['Veiculo']).strip()
                        obj_registro_2art.placa = str(row['Placa']).strip()
                        obj_registro_2art.veiculoindisp = str(row['VeiculoIndisp']).strip()
                        obj_registro_2art.placaindisp = str(row['PlacaIndisp']).strip()
                        obj_registro_2art.frotaindisp = str(row['FrotaIndisp']).strip()
                        obj_registro_2art.tipoindisp = str(row['TipoIndisp']).strip()
                        obj_registro_2art.entregas = str(row['Entregas']).strip()
                        obj_registro_2art.cxcarreg = str(row['CxCarreg']).strip()
                        obj_registro_2art.cxentreg = str(row['CxEntreg']).strip()
                        obj_registro_2art.ocupacao = str(row['Ocupacao']).strip()
                        obj_registro_2art.cxrota = str(row['CxRota']).strip()
                        obj_registro_2art.cxas = str(row['CxAS']).strip()
                        obj_registro_2art.veicbm = str(row['VeicBM']).strip()
                        obj_registro_2art.rshow = str(row['RShow']).strip()
                        obj_registro_2art.entrvol = str(row['EntrVol']).strip()
                        obj_registro_2art.hrsai = str(row['HrSai']).strip()
                        obj_registro_2art.hrentr = str(row['HrEntr']).strip()
                        obj_registro_2art.kmsai = str(row['KmSai']).strip()
                        obj_registro_2art.kmentr = str(row['KmEntr']).strip()
                        obj_registro_2art.custovariavel = str(row['CustoVariavel']).strip()
                        obj_registro_2art.lucro = str(row['Lucro']).strip()
                        obj_registro_2art.lucrounit = str(row['LucroUnit']).strip()
                        obj_registro_2art.valorfrete = str(row['ValorFrete']).strip()
                        obj_registro_2art.tipoimposto = str(row['TipoImposto']).strip()
                        obj_registro_2art.percimposto = str(row['PercImposto']).strip()
                        obj_registro_2art.valorimposto = str(row['ValorImposto']).strip()
                        obj_registro_2art.valorfaturado = str(row['ValorFaturado']).strip()
                        obj_registro_2art.valorunitcxentregue = str(row['ValorUnitCxEntregue']).strip()
                        obj_registro_2art.valorpgcxentregsemimp = str(row['ValorPgCxEntregSemImp']).strip()
                        obj_registro_2art.valorpgcxentregcomimp = str(row['ValorPgCxEntregComImp']).strip()
                        obj_registro_2art.tempoprevistoroad = str(row['TempoPrevistoRoad']).strip()
                        obj_registro_2art.kmprevistoroad = str(row['KmPrevistoRoad']).strip()
                        obj_registro_2art.valorunitpontomot = str(row['ValorUnitPontoMot']).strip()
                        obj_registro_2art.valorunitpontoajd = str(row['ValorUnitPontoAjd']).strip()
                        obj_registro_2art.valorequipeentrmot = str(row['ValorEquipeEntrMot']).strip()
                        obj_registro_2art.valorequipeentrajd = str(row['ValorEquipeEntrAjd']).strip()
                        obj_registro_2art.custovlc = str(row['CustoVLC']).strip()
                        obj_registro_2art.lucrounitcedbz = str(row['LucroUnitCEDBZ']).strip()
                        obj_registro_2art.custovlccxentr = str(row['CustoVlcCxEntr']).strip()
                        obj_registro_2art.tempointerno = str(row['TempoInterno']).strip()
                        obj_registro_2art.valordropdown = str(row['ValorDropDown']).strip()
                        obj_registro_2art.veiccaddd = str(row['VeicCadDD']).strip()
                        obj_registro_2art.kmlaco = str(row['KmLaco']).strip()
                        obj_registro_2art.kmdeslocamento = str(row['KmDeslocamento']).strip()
                        obj_registro_2art.tempolaco = str(row['TempoLaco']).strip()
                        obj_registro_2art.tempodeslocamento = str(row['TempoDeslocamento']).strip()
                        obj_registro_2art.sitmulticdd = str(row['SitMultiCDD']).strip()
                        obj_registro_2art.unborigem = str(row['UnbOrigem']).strip()
                        obj_registro_2art.matricmotorista = str(row['MatricMotorista']).strip()
                        obj_registro_2art.matricajud1 = str(row['MatricAjud1']).strip()
                        obj_registro_2art.matricajud2 = str(row['MatricAjud2']).strip()
                        obj_registro_2art.valorctedifere = str(row['ValorCTEDifere']).strip()
                        obj_registro_2art.qtnfcarregadas = str(row['QtNfCarregadas']).strip()
                        obj_registro_2art.qtnfentregues = str(row['QtNfEntregues']).strip()
                        obj_registro_2art.inddevcx = str(row['IndDevCx']).strip()
                        obj_registro_2art.inddevnf = str(row['IndDevNf']).strip()
                        obj_registro_2art.fator = str(row['Fator']).strip()
                        obj_registro_2art.recarga = str(row['Recarga']).strip()
                        obj_registro_2art.hrmatinal = str(row['HrMatinal']).strip()
                        obj_registro_2art.hrjornadaliq = str(row['HrJornadaLiq']).strip()
                        obj_registro_2art.hrmetajornada = str(row['HrMetaJornada']).strip()
                        obj_registro_2art.vlbateujornmot = str(row['VlBateuJornMot']).strip()
                        obj_registro_2art.vlnaobateujornmot = str(row['VlNaoBateuJornMot']).strip()
                        obj_registro_2art.vlrecargamot = str(row['VlRecargaMot']).strip()
                        obj_registro_2art.vlbateujornaju = str(row['VlBateuJornAju']).strip()
                        obj_registro_2art.vlnaobateujornaju = str(row['VlNaoBateuJornAju']).strip()
                        obj_registro_2art.vlrecargaaju = str(row['VlRecargaAju']).strip()
                        obj_registro_2art.vltotalmapa = str(row['VlTotalMapa']).strip()
                        obj_registro_2art.qthlcarregados = str(row['QtHlCarregados']).strip()
                        obj_registro_2art.qthlentregues = str(row['QtHlEntregues']).strip()
                        obj_registro_2art.indicedevhl = str(row['IndiceDevHl']).strip()
                        obj_registro_2art.regiao = str(row['Regiao']).strip()
                        obj_registro_2art.qtnfcarreggeral = str(row['QtNfCarregGeral']).strip()
                        obj_registro_2art.qtnfentreggeral = str(row['QtNfEntregGeral']).strip()
                        obj_registro_2art.capacidadeveiculokg = str(row['CapacidadeVeiculoKG']).strip()
                        obj_registro_2art.pesocargakg = str(row['PesoCargaKG']).strip()
                        obj_registro_2art.capacveiculocx = str(row['CapacVeiculoCx']).strip()
                        obj_registro_2art.entregascompletas = str(row['EntregasCompletas']).strip()
                        obj_registro_2art.entregasparciais = str(row['EntregasParciais']).strip()
                        obj_registro_2art.entregasnaorealizadas = str(row['EntregasNaoRealizadas']).strip()
                        obj_registro_2art.codsupervtrs = str(row['CodSupervTrs']).strip()
                        obj_registro_2art.nomesupervtrs = str(row['NomeSupervTrs']).strip()
                        obj_registro_2art.codspot = str(row['CodSpot']).strip()
                        obj_registro_2art.nomespot = str(row['NomeSpot']).strip()
                        obj_registro_2art.equipcarregados = str(row['EquipCarregados']).strip()
                        obj_registro_2art.equipdevolvidos = str(row['EquipDevolvidos']).strip()
                        obj_registro_2art.equiprecolhidos = str(row['EquipRecolhidos']).strip()
                        obj_registro_2art.cxentregtracking = str(row['CxEntregTracking']).strip()
                        obj_registro_2art.hrcarreg = str(row['HrCarreg']).strip()
                        obj_registro_2art.hrpcfisica = str(row['HrPCFisica']).strip()
                        obj_registro_2art.hrpcfinanceira = str(row['HrPCFinanceira']).strip()
                        obj_registro_2art.stmapa = str(row['StMapa']).strip()
                        obj_registro_2art.qtentregascarregrv = str(row['QtEntregasCarreg(RV)']).strip()
                        obj_registro_2art.qtentregasentregrv = str(row['QtEntregasEntreg(RV)']).strip()
                        obj_registro_2art.indicedeventregasrv = str(row['IndiceDevEntregas(RV)']).strip()
                        obj_registro_2art.cpfmotorista = str(row['CPFMotorista']).strip()
                        obj_registro_2art.cpfajudante1 = str(row['CPFAjudante1']).strip()
                        obj_registro_2art.cpfajudante2 = str(row['CPFAjudante2']).strip()
                        obj_registro_2art.alterado='N'
                        obj_registro_2art.acao='U'
                        obj_registro_2art.cod_reg_arq_imp=arquivo_2art
                        obj_registro_2art.save()
                        count_reg_up += 1
                except Exception as e:
                    reg = {
                        'mapa': str(int(row['Mapa'])),
                        'msg': 'Mapa: '+str(int(row['Mapa']))+', Data: '+data_mapa_str_sql+
                                                         '.Erro: '+ str(e)
                    }
                    tab_mapas_nao_importados_2art.append(reg)
            else:
                tipo_entrega = str(row['Entrega'])
                tipo_frota = str(row['Frota'])
                reg = {
                    'mapa': str(int(row['Mapa'])),
                    'msg': 'Mapa: ' + str(int(row['Mapa'])) + ', Data: ' + data_mapa_str_sql +
                                                     f'.Erro: Projeto não identificado. Tipo de Entrega {tipo_entrega} '
                                                     f'e Frota {tipo_frota} não foram mapeados! Verifique com o Adm.'
                }
                tab_mapas_nao_importados_2art.append(reg)
        arquivo_2art.qtd_registros = conteudo_arq_2art.shape[0]
        arquivo_2art.qtd_importados = count_reg_imp
        arquivo_2art.qtd_atualizados = count_reg_up
        arquivo_2art.save()
        data = dict()
        data = {
            'tab_mapas_nao_importados_2art': tab_mapas_nao_importados_2art,
            'qtd_total_reg': conteudo_arq_2art.shape[0],
            'qtd_reg_imp': count_reg_imp,
            'qtd_reg_up': count_reg_up
        }
        return JsonResponse(data, safe=False)

