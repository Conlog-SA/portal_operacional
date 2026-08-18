from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.frota_importa_2art_app.models import Arquivo2Art, IndicaProjReg2Art, Registro2Art
from apps.usuario_app.models import Usuario

from datetime import datetime, date
import pandas as pd
import traceback
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
        conteudo_arq_2art.rename(columns=lambda x: str(x).strip(), inplace=True),
        conteudo_arq_2art.columns = conteudo_arq_2art.columns.str.replace('_', '', regex=False)
        conteudo_arq_2art.columns = conteudo_arq_2art.columns.str.replace('(', '', regex=False)
        conteudo_arq_2art.columns = conteudo_arq_2art.columns.str.replace(')', '', regex=False)
        conteudo_arq_2art.columns = conteudo_arq_2art.columns.str.lower()
        count_reg_imp = 0
        count_reg_up = 0
        for index, row in conteudo_arq_2art.iterrows():
            data_mapa_str_sql = ''
            '''
            data_mapa_int = int(row['data'])
            if len(str(data_mapa_int)) == 7:
                data_mapa_str_sql = str(data_mapa_int)[3:] + '/' + str(data_mapa_int)[1:3] + "/0" + str(data_mapa_int)[0:1]
            else:
                data_mapa_str_sql = str(data_mapa_int)[4:] + '/' + str(data_mapa_int)[2:4] + "/" + str(data_mapa_int)[0:2]'''

            #data_original = str(row['data'])
            if isinstance(row['data'], (datetime, date)):
                '''dia = data_original.split('/')[1]
                mes = data_original.split('/')[0]
                ano = data_original.split('/')[2]
                data_mapa_str_sql = str(ano) + '/' + str(mes) + '/' + str(dia)'''
                data_mapa = datetime.strftime(row['data'], '%Y-%m-%d')

                cpfmotorista = '0'
                cpfajudante1 = '0'
                cpfajudante2 = '0'
            else:
                data_mapa = str(row['data'])
                if len(data_mapa) == 7:
                    data_mapa_str_sql = str(data_mapa)[3:] + '/' + str(data_mapa)[1:3] + "/0" + str(
                        data_mapa)[0:1]
                else:
                    data_mapa_str_sql = str(data_mapa)[4:] + '/' + str(data_mapa)[2:4] + "/" + str(
                        data_mapa)[0:2]
                data_mapa = datetime.strptime(data_mapa_str_sql, '%Y/%m/%d')


                cpfmotorista = str(row['cpfmotorista']).strip()
                cpfajudante1 = str(row['cpfajudante1']).strip()
                cpfajudante2 = str(row['cpfajudante2']).strip()

            obj_ind_proj = IndicaProjReg2Art.objects.filter(
                cod_filial_promax=str(int(row['codfilial'])).strip(), tipo_entrega=str(row['entrega']).strip(),
                tipo_frota=str(row['frota']).strip()).first()

            if obj_ind_proj != None:
                try:
                    cod_reg_2art = int(str(int(row['mapa'])) + str(int(row['codfilial'])))
                    obj_registro_2art = Registro2Art.objects.filter(cod_reg_2art=cod_reg_2art).first()
                    if obj_registro_2art == None:

                        obj_registro_2art_new = Registro2Art(
                            cod_reg_2art=int(str(int(row['mapa'])) + str(int(row['codfilial']))),
                            data=data_mapa,
                            transp=str(row['transp']).strip(),
                            entrega=str(row['entrega']).strip(),
                            cargaatual=str(row['cargaatual']).strip(),
                            frota=str(row['frota']).strip(),
                            custospot=str(row['custospot']).strip(),
                            regiaospot=str(row['regiaospot']).strip(),
                            veiculo=str(row['veiculo']).strip(),
                            placa=str(row['placa']).strip(),
                            veiculoindisp=str(row['veiculoindisp']).strip(),
                            placaindisp=str(row['placaindisp']).strip(),
                            frotaindisp=str(row['frotaindisp']).strip(),
                            tipoindisp=str(row['tipoindisp']).strip(),
                            mapa=str(int(row['mapa'])).strip(),
                            entregas=str(row['entregas']).strip(),
                            cxcarreg=str(row['cxcarreg']).strip(),
                            cxentreg=str(row['cxentreg']).strip(),
                            ocupacao=str(row['ocupacao']).strip(),
                            cxrota=str(row['cxrota']).strip(),
                            cxas=str(row['cxas']).strip(),
                            veicbm=str(row['veicbm']).strip(),
                            rshow=str(row['rshow']).strip(),
                            entrvol=str(row['entrvol']).strip(),
                            hrsai=str(row['hrsai']).strip(),
                            hrentr=str(row['hrentr']).strip(),
                            kmsai=str(row['kmsai']).strip(),
                            kmentr=str(row['kmentr']).strip(),
                            custovariavel=str(row['custovariavel']).strip(),
                            lucro=str(row['lucro']).strip(),
                            lucrounit=str(row['lucrounit']).strip(),
                            valorfrete=str(row['valorfrete']).strip(),
                            tipoimposto=str(row['tipoimposto']).strip(),
                            percimposto=str(row['percimposto']).strip(),
                            valorimposto=str(row['valorimposto']).strip(),
                            valorfaturado=str(row['valorfaturado']).strip(),
                            valorunitcxentregue=str(row['valorunitcxentregue']).strip(),
                            valorpgcxentregsemimp=str(row['valorpgcxentregsemimp']).strip(),
                            valorpgcxentregcomimp=str(row['valorpgcxentregcomimp']).strip(),
                            tempoprevistoroad=str(row['tempoprevistoroad']).strip(),
                            kmprevistoroad=str(row['kmprevistoroad']).strip(),
                            valorunitpontomot=str(row['valorunitpontomot']).strip(),
                            valorunitpontoajd=str(row['valorunitpontoajd']).strip(),
                            valorequipeentrmot=str(row['valorequipeentrmot']).strip(),
                            valorequipeentrajd=str(row['valorequipeentrajd']).strip(),
                            custovlc=str(row['custovlc']).strip(),
                            lucrounitcedbz=str(row['lucrounitcedbz']).strip(),
                            custovlccxentr=str(row['custovlccxentr']).strip(),
                            tempointerno=str(row['tempointerno']).strip(),
                            valordropdown=str(row['valordropdown']).strip(),
                            veiccaddd=str(row['veiccaddd']).strip(),
                            kmlaco=str(row['kmlaco']).strip(),
                            kmdeslocamento=str(row['kmdeslocamento']).strip(),
                            tempolaco=str(row['tempolaco']).strip(),
                            tempodeslocamento=str(row['tempodeslocamento']).strip(),
                            sitmulticdd=str(row['sitmulticdd']).strip(),
                            unborigem=str(row['unborigem']).strip(),
                            matricmotorista=row['matricmotorista'],
                            matricajud1=str(row['matricajud1']).strip(),
                            matricajud2=str(row['matricajud2']).strip(),
                            valorctedifere=str(row['valorctedifere']).strip(),
                            qtnfcarregadas=str(row['qtnfcarregadas']).strip(),
                            qtnfentregues=str(row['qtnfentregues']).strip(),
                            inddevcx=str(row['inddevcx']).strip(),
                            inddevnf=str(row['inddevnf']).strip(),
                            fator=str(row['fator']).strip(),
                            recarga=str(row['recarga']).strip(),
                            hrmatinal=str(row['hrmatinal']).strip(),
                            hrjornadaliq=str(row['hrjornadaliq']).strip(),
                            hrmetajornada=str(row['hrmetajornada']).strip(),
                            vlbateujornmot=str(row['vlbateujornmot']).strip(),
                            vlnaobateujornmot=str(row['vlnaobateujornmot']).strip(),
                            vlrecargamot=str(row['vlrecargamot']).strip(),
                            vlbateujornaju=str(row['vlbateujornaju']).strip(),
                            vlnaobateujornaju=str(row['vlnaobateujornaju']).strip(),
                            vlrecargaaju=str(row['vlrecargaaju']).strip(),
                            vltotalmapa=str(row['vltotalmapa']).strip(),
                            qthlcarregados=str(row['qthlcarregados']).strip(),
                            qthlentregues=str(row['qthlentregues']).strip(),
                            indicedevhl=str(row['indicedevhl']).strip(),
                            regiao=str(row['regiao']).strip(),
                            qtnfcarreggeral=str(row['qtnfcarreggeral']).strip(),
                            qtnfentreggeral=str(row['qtnfentreggeral']).strip(),
                            capacidadeveiculokg=str(row['capacidadeveiculokg']).strip(),
                            pesocargakg=str(row['pesocargakg']).strip(),
                            capacveiculocx=str(row['capacveiculocx']).strip(),
                            entregascompletas=str(row['entregascompletas']).strip(),
                            entregasparciais=str(row['entregasparciais']).strip(),
                            entregasnaorealizadas=str(row['entregasnaorealizadas']).strip(),
                            codfilial=str(row['codfilial']).strip(),
                            nomefilial=str(row['nomefilial']).strip(),
                            codsupervtrs=str(row['codsupervtrs']).strip(),
                            nomesupervtrs=str(row['nomesupervtrs']).strip(),
                            codspot=str(row['codspot']).strip(),
                            nomespot=str(row['nomespot']).strip(),
                            equipcarregados=str(row['equipcarregados']).strip(),
                            equipdevolvidos=str(row['equipdevolvidos']).strip(),
                            equiprecolhidos=str(row['equiprecolhidos']).strip(),
                            cxentregtracking=str(row['cxentregtracking']).strip(),
                            hrcarreg=str(row['hrcarreg']).strip(),
                            hrpcfisica=str(row['hrpcfisica']).strip(),
                            hrpcfinanceira=str(row['hrpcfinanceira']).strip(),
                            stmapa=str(row['stmapa']).strip(),
                            qtentregascarregrv=str(row['qtentregascarregrv']).strip(),
                            qtentregasentregrv=str(row['qtentregasentregrv']).strip(),
                            indicedeventregasrv=str(row['indicedeventregasrv']).strip(),
                            cpfmotorista=cpfmotorista,
                            cpfajudante1=cpfajudante1,
                            cpfajudante2=cpfajudante2,
                            alterado='N',
                            acao='I',
                            cod_reg_arq_imp=arquivo_2art,
                            cod_reg_indc_cod_reg_2art=obj_ind_proj
                        )
                        obj_registro_2art_new.save()
                        count_reg_imp += 1
                    else:
                        obj_registro_2art.transp=str(row['transp']).strip()
                        obj_registro_2art.entrega=str(row['entrega']).strip()
                        obj_registro_2art.cargaatual=str(row['cargaatual']).strip()
                        obj_registro_2art.frota=str(row['frota']).strip()
                        obj_registro_2art.custospot = str(row['custospot']).strip()
                        obj_registro_2art.regiaospot = str(row['regiaospot']).strip()
                        obj_registro_2art.veiculo = str(row['veiculo']).strip()
                        obj_registro_2art.placa = str(row['placa']).strip()
                        obj_registro_2art.veiculoindisp = str(row['veiculoindisp']).strip()
                        obj_registro_2art.placaindisp = str(row['placaindisp']).strip()
                        obj_registro_2art.frotaindisp = str(row['frotaindisp']).strip()
                        obj_registro_2art.tipoindisp = str(row['tipoindisp']).strip()
                        obj_registro_2art.entregas = str(row['entregas']).strip()
                        obj_registro_2art.cxcarreg = str(row['cxcarreg']).strip()
                        obj_registro_2art.cxentreg = str(row['cxentreg']).strip()
                        obj_registro_2art.ocupacao = str(row['ocupacao']).strip()
                        obj_registro_2art.cxrota = str(row['cxrota']).strip()
                        obj_registro_2art.cxas = str(row['cxas']).strip()
                        obj_registro_2art.veicbm = str(row['veicbm']).strip()
                        obj_registro_2art.rshow = str(row['rshow']).strip()
                        obj_registro_2art.entrvol = str(row['entrvol']).strip()
                        obj_registro_2art.hrsai = str(row['hrsai']).strip()
                        obj_registro_2art.hrentr = str(row['hrentr']).strip()
                        obj_registro_2art.kmsai = str(row['kmsai']).strip()
                        obj_registro_2art.kmentr = str(row['kmentr']).strip()
                        obj_registro_2art.custovariavel = str(row['custovariavel']).strip()
                        obj_registro_2art.lucro = str(row['lucro']).strip()
                        obj_registro_2art.lucrounit = str(row['lucrounit']).strip()
                        obj_registro_2art.valorfrete = str(row['valorfrete']).strip()
                        obj_registro_2art.tipoimposto = str(row['tipoimposto']).strip()
                        obj_registro_2art.percimposto = str(row['percimposto']).strip()
                        obj_registro_2art.valorimposto = str(row['valorimposto']).strip()
                        obj_registro_2art.valorfaturado = str(row['valorfaturado']).strip()
                        obj_registro_2art.valorunitcxentregue = str(row['valorunitcxentregue']).strip()
                        obj_registro_2art.valorpgcxentregsemimp = str(row['valorpgcxentregsemimp']).strip()
                        obj_registro_2art.valorpgcxentregcomimp = str(row['valorpgcxentregcomimp']).strip()
                        obj_registro_2art.tempoprevistoroad = str(row['tempoprevistoroad']).strip()
                        obj_registro_2art.kmprevistoroad = str(row['kmprevistoroad']).strip()
                        obj_registro_2art.valorunitpontomot = str(row['valorunitpontomot']).strip()
                        obj_registro_2art.valorunitpontoajd = str(row['valorunitpontoajd']).strip()
                        obj_registro_2art.valorequipeentrmot = str(row['valorequipeentrmot']).strip()
                        obj_registro_2art.valorequipeentrajd = str(row['valorequipeentrajd']).strip()
                        obj_registro_2art.custovlc = str(row['custovlc']).strip()
                        obj_registro_2art.lucrounitcedbz = str(row['lucrounitcedbz']).strip()
                        obj_registro_2art.custovlccxentr = str(row['custovlccxentr']).strip()
                        obj_registro_2art.tempointerno = str(row['tempointerno']).strip()
                        obj_registro_2art.valordropdown = str(row['valordropdown']).strip()
                        obj_registro_2art.veiccaddd = str(row['veiccaddd']).strip()
                        obj_registro_2art.kmlaco = str(row['kmlaco']).strip()
                        obj_registro_2art.kmdeslocamento = str(row['kmdeslocamento']).strip()
                        obj_registro_2art.tempolaco = str(row['tempolaco']).strip()
                        obj_registro_2art.tempodeslocamento = str(row['tempodeslocamento']).strip()
                        obj_registro_2art.sitmulticdd = str(row['sitmulticdd']).strip()
                        obj_registro_2art.unborigem = str(row['unborigem']).strip()
                        obj_registro_2art.matricmotorista = str(row['matricmotorista']).strip()
                        obj_registro_2art.matricajud1 = str(row['matricajud1']).strip()
                        obj_registro_2art.matricajud2 = str(row['matricajud2']).strip()
                        obj_registro_2art.valorctedifere = str(row['valorctedifere']).strip()
                        obj_registro_2art.qtnfcarregadas = str(row['qtnfcarregadas']).strip()
                        obj_registro_2art.qtnfentregues = str(row['qtnfentregues']).strip()
                        obj_registro_2art.inddevcx = str(row['inddevcx']).strip()
                        obj_registro_2art.inddevnf = str(row['inddevnf']).strip()
                        obj_registro_2art.fator = str(row['fator']).strip()
                        obj_registro_2art.recarga = str(row['recarga']).strip()
                        obj_registro_2art.hrmatinal = str(row['hrmatinal']).strip()
                        obj_registro_2art.hrjornadaliq = str(row['hrjornadaliq']).strip()
                        obj_registro_2art.hrmetajornada = str(row['hrmetajornada']).strip()
                        obj_registro_2art.vlbateujornmot = str(row['vlbateujornmot']).strip()
                        obj_registro_2art.vlnaobateujornmot = str(row['vlnaobateujornmot']).strip()
                        obj_registro_2art.vlrecargamot = str(row['vlrecargamot']).strip()
                        obj_registro_2art.vlbateujornaju = str(row['vlbateujornaju']).strip()
                        obj_registro_2art.vlnaobateujornaju = str(row['vlnaobateujornaju']).strip()
                        obj_registro_2art.vlrecargaaju = str(row['vlrecargaaju']).strip()
                        obj_registro_2art.vltotalmapa = str(row['vltotalmapa']).strip()
                        obj_registro_2art.qthlcarregados = str(row['qthlcarregados']).strip()
                        obj_registro_2art.qthlentregues = str(row['qthlentregues']).strip()
                        obj_registro_2art.indicedevhl = str(row['indicedevhl']).strip()
                        obj_registro_2art.regiao = str(row['regiao']).strip()
                        obj_registro_2art.qtnfcarreggeral = str(row['qtnfcarreggeral']).strip()
                        obj_registro_2art.qtnfentreggeral = str(row['qtnfentreggeral']).strip()
                        obj_registro_2art.capacidadeveiculokg = str(row['capacidadeveiculokg']).strip()
                        obj_registro_2art.pesocargakg = str(row['pesocargakg']).strip()
                        obj_registro_2art.capacveiculocx = str(row['capacveiculocx']).strip()
                        obj_registro_2art.entregascompletas = str(row['entregascompletas']).strip()
                        obj_registro_2art.entregasparciais = str(row['entregasparciais']).strip()
                        obj_registro_2art.entregasnaorealizadas = str(row['entregasnaorealizadas']).strip()
                        obj_registro_2art.codsupervtrs = str(row['codsupervtrs']).strip()
                        obj_registro_2art.nomesupervtrs = str(row['nomesupervtrs']).strip()
                        obj_registro_2art.codspot = str(row['codspot']).strip()
                        obj_registro_2art.nomespot = str(row['nomespot']).strip()
                        obj_registro_2art.equipcarregados = str(row['equipcarregados']).strip()
                        obj_registro_2art.equipdevolvidos = str(row['equipdevolvidos']).strip()
                        obj_registro_2art.equiprecolhidos = str(row['equiprecolhidos']).strip()
                        obj_registro_2art.cxentregtracking = str(row['cxentregtracking']).strip()
                        obj_registro_2art.hrcarreg = str(row['hrcarreg']).strip()
                        obj_registro_2art.hrpcfisica = str(row['hrpcfisica']).strip()
                        obj_registro_2art.hrpcfinanceira = str(row['hrpcfinanceira']).strip()
                        obj_registro_2art.stmapa = str(row['stmapa']).strip()
                        obj_registro_2art.qtentregascarregrv = str(row['qtentregascarregrv']).strip()
                        obj_registro_2art.qtentregasentregrv = str(row['qtentregasentregrv']).strip()
                        obj_registro_2art.indicedeventregasrv = str(row['indicedeventregasrv']).strip()
                        obj_registro_2art.cpfmotorista = cpfmotorista
                        obj_registro_2art.cpfajudante1 = cpfajudante1
                        obj_registro_2art.cpfajudante2 = cpfajudante2
                        obj_registro_2art.alterado='N'
                        obj_registro_2art.acao='U'
                        obj_registro_2art.cod_reg_arq_imp=arquivo_2art
                        obj_registro_2art.save()
                        count_reg_up += 1
                except Exception as e:
                    reg = {
                        'mapa': str(int(row['mapa'])),
                        'msg': 'Mapa: '+str(int(row['mapa']))+', Data: '+data_mapa_str_sql+
                                                         '.Erro: '+ str(e)
                    }
                    tab_mapas_nao_importados_2art.append(reg)
            else:
                tipo_entrega = str(row['entrega'])
                tipo_frota = str(row['frota'])
                cod_filial = str(row['codfilial'])
                reg = {
                    'mapa': str(int(row['mapa'])),
                    'msg': 'Mapa: ' + str(int(row['mapa'])) + ', Data: ' + data_mapa_str_sql +
                                                     f'.Erro: Projeto não identificado. Tipo de Entrega: {tipo_entrega}, '
                                                     f'e Frota: {tipo_frota} e Cod Filial: {cod_filial} não foram mapeados! Verifique com o Adm.'
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

