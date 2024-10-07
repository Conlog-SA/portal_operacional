import locale
import os
from datetime import datetime

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db.models import Value, Q, F, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.conecta_senior_app.views import Conexao_Senior_BD
from apps.estrut_org_app.models import Filial, Projeto
from apps.gente_gestao_rateio_unimed_app.models import Arquivo_Despesas, Despesa_Unimed, Plano_Saude, Operadora_Plano, \
    Colaborador_Excecao, Projetos_Senior
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR


class Form_Importa_Plan_Despesas_View(View):
    def get(self, request):
        cod_usu_session = request.session['cod_usuario_logado']

        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        cod_empresa_filtro = 0
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_filtro = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_filtro = 2

        #
        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro, cod_arq_despesa__status_arquivo=1).values_list(
            'cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})

        lista_filiais_notas_plano = [1, 2, 3, 5, 9, 36, 62, 93]
        lista_todas_filiais = Filial.objects.filter(cod_filial__in=lista_filiais_notas_plano).values_list(
            'cod_filial', 'desc_filial').distinct()
        lista_todas_filiais_dict = []
        for filial in lista_todas_filiais:
            lista_todas_filiais_dict.append({'cod_filial': filial[0], 'desc_filial': filial[1]})

        lista_codigos_usuarios_importacao = Arquivo_Despesas.objects.filter(cod_usu__cod_filial__cod_empresa__cod_empresa=obj_usu.cod_filial.cod_empresa.cod_empresa).values_list(
            'cod_usu').distinct()
        usuarios_importacao = Usuario.objects.filter(cod_usu__in=lista_codigos_usuarios_importacao)

        planos_saude = Plano_Saude.objects.all()
        lista_planos_dict = []
        for plano in planos_saude:
            if plano.especificacao != None:
                str_especificacao = '- ' + plano.especificacao
            else:
                str_especificacao = ''
            lista_planos_dict.append({'cod_plano_saude': plano.cod_plano_saude, 'desc_plano': plano.operadora_plano.desc_operadora_plano + '-' + plano.filial + str_especificacao})

        contexto = {
            'lista_filiais': lista_filiais_dict,
            'lista_todas_filiais': lista_todas_filiais_dict,
            'desc_menu': 'Rateio Despesas Unimed',
            'usuarios_importacao': usuarios_importacao,
            'lista_planos': lista_planos_dict
        }
        return render(request, 'gente_gestao_rateio_unimed_app/form_rateio_despesa_unimed.html', contexto)

    def post(self, request):
        myfile = request.FILES['file']
        cod_plano = request.POST['cod_plano']
        cod_usu_session = request.session['cod_usuario_logado']

        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')

        caminho_arq_importado = 'docs/rateio_unimed/' + obj_usu.cod_filial.unidade_abrev + '/rateio_unimed_' + obj_usu.cod_filial.unidade_abrev + '_' + \
                                obj_usu.login_usu.replace('.', '_') + '_' + str(data_atual_dd_mm_yyyy).replace('/', '_') \
                                + '_' + str(hota_atual).replace(':', '_') + '.xlsx'
        plano_saude = Plano_Saude.objects.filter(cod_plano_saude=cod_plano).first()

        if plano_saude == None:
            response = HttpResponse('Plano de saúde não informado/encontrado!')
            # response = HttpResponse(e)
            response.status_code = 500
            return response

        arquivo_despesa = Arquivo_Despesas(
            nome_arq_imp=caminho_arq_importado,
            nome_arq_original=str(myfile.name),
            cod_usu=obj_usu,
            qtd_registros=0,
            status_arquivo=1,
            cod_plano_saude=plano_saude
        )

        arquivo_despesa.save()

        fs = FileSystemStorage()
        filename = fs.save(caminho_arq_importado, myfile)
        uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado)
        tab_rateio_despesas_nao_importadas = []
        conteudo_arq_plan_unimed = pd.read_excel(uploaded_file_url)
        conteudo_arq_plan_unimed = conteudo_arq_plan_unimed.dropna(how='all')
        conteudo_arq_plan_unimed.rename(columns=lambda x: str(x).strip(), inplace=True)

        colunas_planilha = ['BENEFICIARIO', 'DEPENDENCIA', 'TITULAR', 'CPF_TITULAR',
                            'DESC_DESPESA', 'VL_FATURADO', 'CPF_BENEFICIARIO', 'COMPETENCIA',
                            'PERCENTUAL_EMPRESA']
        try:
            for index, row in conteudo_arq_plan_unimed.iterrows():

                flag_coluna_com_erro = False
                erro_colunas_retorno = ''
                erro_retorno = ''
                for coluna in colunas_planilha:
                    if coluna not in conteudo_arq_plan_unimed.columns.values.tolist():
                        flag_coluna_com_erro = True
                        erro_colunas_retorno += '<br>' + coluna
                if flag_coluna_com_erro == True:
                    erro_retorno = 'Colunas com nome incorreto/não constam:' + erro_colunas_retorno

                if '/' not in str(row['COMPETENCIA']):
                    erro_retorno = 'Valores de competência não estão no formato correto! (mm/aaaa)'

                if erro_retorno != '':
                    response = HttpResponse(erro_retorno)
                    response.status_code = 500
                    return response

                #if 'CPF_TITULAR' in conteudo_arq_plan_unimed.columns.values.tolist():
                #    cpf_titular = str(row['CPF_TITULAR']).strip()
                #else:
                #    nome_conteudo_arq_plan_unimed[(conteudo_arq_plan_unimed['NOME'] == row['NOME_TITULAR']) & (
                #                conteudo_arq_plan_unimed['NOME'] == conteudo_arq_plan_unimed['NOME_TITULAR'])]
                #    cpf_titular = str(conteudo_arq_plan_unimed[(conteudo_arq_plan_unimed['NOME'] == row['NOME_TITULAR']) & (conteudo_arq_plan_unimed['NOME'] == conteudo_arq_plan_unimed['NOME_TITULAR'])]['CPF'].iloc[0]).strip()

                nome_beneficiario = str(row['BENEFICIARIO']).strip()
                tipo_depencencia = str(row['DEPENDENCIA']).strip()
                nome_titular = str(row['TITULAR']).strip()
                desc_despesa = str(row['DESC_DESPESA']).strip()
                valor = float(row['VL_FATURADO'])
                cpf_beneficiario = str(row['CPF_BENEFICIARIO']).strip().zfill(11)
                cpf_titular = str(row['CPF_TITULAR']).strip().zfill(11)
                percentual_empresa = str(row['PERCENTUAL_EMPRESA']).strip()
                if float(percentual_empresa) < 0 or float(percentual_empresa) > 1:
                    raise Exception('Porcentagem inválida informada.')
                if percentual_empresa == 'nan':
                    percentual_empresa = None
                else:
                    percentual_empresa = int(float(percentual_empresa)*100)

                competencia_split = str(row['COMPETENCIA']).strip().split('/')

                competencia = competencia_split[1] + '-' + competencia_split[0]

                conexao_senior = Conexao_Senior_BD(obj_usu.cod_filial.cod_empresa.cod_empresa)
                cod_empresa_senior = None
                if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
                    cod_empresa_senior = 1
                elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
                    cod_empresa_senior = 2
                titular_senior = conexao_senior.pesquisar_dados_colaborador_por_cpf_emp(cpf_titular, cod_empresa_senior)
                if 'erro' not in titular_senior:
                    excecoes = Colaborador_Excecao.objects.all()
                    cod_projeto = titular_senior['cod_projeto_colab']
                    desc_projeto = titular_senior['nom_projeto_colab']
                    cod_filial = titular_senior['cod_filial_colab']
                    desc_filial = titular_senior['nom_filial_colab']
                    for exc in excecoes.values_list('cpf_colab_excecao', 'cod_proj_colab_excecao',
                                                    'desc_proj_colab_excecao', 'cod_filial_colab_excecao',
                                                    'desc_filial_colab_excecao').distinct():
                        if str(exc[0]).zfill(11) == str(cpf_titular).zfill(11):
                            cod_projeto = exc[1]
                            desc_projeto = exc[2]
                            cod_filial = exc[3]
                            desc_filial = exc[4]

                    obj_registro_despesa_new = Despesa_Unimed(
                        competencia=competencia,
                        cpf_beneficiario=cpf_beneficiario,
                        nome_beneficiario=nome_beneficiario,
                        tipo_depencencia=tipo_depencencia,
                        nome_titular=nome_titular,
                        cpf_titular=cpf_titular,
                        desc_despesa=desc_despesa,
                        valor=valor,
                        cod_arq_despesa=arquivo_despesa,
                        nome_titular_senior=titular_senior['nome_colab'],
                        matricula_titular=titular_senior['matricula_colab'],
                        cod_filial_senior=cod_filial,
                        desc_filial_senior=desc_filial,
                        cod_projeto_senior=cod_projeto,
                        desc_projeto_senior=desc_projeto,
                        cod_empresa_senior=cod_empresa_senior,
                        percentual_empresa=percentual_empresa
                    )

                    obj_registro_despesa_new.save()
                    '''  tab_rateio_despesas_importadas.append(
                        'Competencia: ' + str(row['COMPETENCIA']).strip() + ' Beneficiário: ' + str(row['NOME']).strip().replace(' ', '_') +
                        ' Cpf: ' + str(row['CPF']).strip() + ' Dependencia: ' + str(row['DEPENDENCIA']).strip() +
                        ' Titular: ' + str(row['NOME_TITULAR']).strip().replace(' ', '_') + ' Cpf_Titular: ' + str(row['CPF_TITULAR']).strip() +
                        ' Desc_Despesa: ' + str(row['DESC_DESPESA']).strip().replace(' ', '_') +
                        ' Valor: ' + str(row['VL_FATURADO']) + ' Nome Titular Senior: ' + titular_senior['nome_colab'] +
                        ' Matrícula Titular: ' + titular_senior['matricula_colab'] +
                        ' Cód. Filial Titular Senior: ' + titular_senior['cod_filial_colab'] +
                        ' Desc. Filial Titular Senior: ' + titular_senior['nom_filial_colab'] +
                        ' Cód. Projeto Titular Senior: ' + titular_senior['cod_projeto_colab'] +
                        ' Desc. Projeto Titular Senior: ' + titular_senior['nom_projeto_colab']
                    )'''
                else:
                    obj_registro_despesa_new = Despesa_Unimed(
                        competencia=competencia,
                        cpf_beneficiario=cpf_beneficiario,
                        nome_beneficiario=nome_beneficiario,
                        tipo_depencencia=tipo_depencencia,
                        nome_titular=nome_titular,
                        cpf_titular=cpf_titular,
                        desc_despesa=desc_despesa,
                        valor=valor,
                        cod_arq_despesa=arquivo_despesa,
                        percentual_empresa=percentual_empresa
                    )
                    obj_registro_despesa_new.save()

                    '''tab_rateio_despesas_nao_importadas.append(
                        'Competencia: ' + competencia + ' Beneficiário: ' + nome_beneficiario.strip().replace(' ', '_') +
                        ' Cpf: ' + cpf_beneficiario.strip() + ' Dependencia: ' + tipo_depencencia.strip() +
                        ' Titular: ' + nome_titular.strip().replace(' ', '_') + ' Cpf_Titular: ' + cpf_titular.strip() +
                        ' Desc_Despesa: ' + desc_despesa.strip().replace(' ', '_') +
                        ' Valor: ' + str(valor) + ' Cod_Despesa: ' + str(obj_registro_despesa_new.cod_despesa_unimed)
                    )'''
                    tab_rateio_despesas_nao_importadas.append({
                        'competencia': competencia,
                        'beneficiario': nome_beneficiario.strip().replace(' ', '_'),
                        'cpf': cpf_beneficiario.strip(),
                        'dependencia': tipo_depencencia.strip(),
                        'titular': nome_titular.strip().replace(' ', '_'),
                        'cpf_titular': cpf_titular.strip(),
                        'desc_despesa': desc_despesa.strip().replace(' ', '_'),
                        'valor': str(valor),
                        'cod_despesa': str(obj_registro_despesa_new.cod_despesa_unimed)
                    })
        except Exception as e:
            lista_despesas = Despesa_Unimed.objects.filter(cod_arq_despesa=arquivo_despesa)
            for despesa in lista_despesas:
                despesa.delete()
            arquivo_despesa.delete()
            #response = HttpResponse('Erro durante importação, contate o administrador!')
            print(e)
            response = HttpResponse(e)
            response.status_code = 500
            return response

        arquivo_despesa.qtd_registros = conteudo_arq_plan_unimed.shape[0]
        arquivo_despesa.save()

        cod_empresa_filtro = 0
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_filtro = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_filtro = 2
        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro, cod_arq_despesa__status_arquivo=1).values_list(
            'cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})

        data = {
            'tab_rateio_despesas_nao_importadas': tab_rateio_despesas_nao_importadas,
            'lista_filiais': lista_filiais_dict,
            'qtd_total_reg': conteudo_arq_plan_unimed.shape[0]
        }
        return JsonResponse(data)

class Form_Filial_Despesas(View):
    def get(self, request):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_filtro = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_filtro = 2

        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro, cod_arq_despesa__status_arquivo=1).values_list('cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})
        contexto = {
            'lista_filiais': lista_filiais_dict,
        }
        return JsonResponse(contexto)
class Preenche_Colaborador(View):
    def get(self, request):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_senior = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_senior = 2

        matricula = request.GET['matricula']
        conexao_senior = Conexao_Senior_BD(obj_usu.cod_filial.cod_empresa.cod_empresa)
        titular_senior = conexao_senior.pesquisar_dados_por_matricula(matricula, cod_empresa_senior)
        if 'erro' not in titular_senior:
            excecoes = Colaborador_Excecao.objects.all().values_list('cpf_colab_excecao').distinct()
            cod_projeto = titular_senior['cod_projeto_colab']
            desc_projeto = titular_senior['nom_projeto_colab']
            cod_filial = titular_senior['cod_filial_colab']
            desc_filial = titular_senior['nom_filial_colab']
            for exc in excecoes.values_list('cpf_colab_excecao', 'cod_proj_colab_excecao',
                                            'cod_filial_colab_excecao', 'desc_filial_colab_excecao').distinct():
                if str(exc[0]).zfill(11) == str(titular_senior['cpf_colab']).zfill(11):
                    cod_projeto = exc[1]
                    projeto = Projetos_Senior.objects.filter(cod_senior_projeto=cod_projeto).first()
                    desc_projeto = projeto.desc_projeto

                    cod_filial = exc[2]
                    desc_filial = exc[3]
            data = {
                'nome_titular_senior': titular_senior['nome_colab'],
                'cod_filial_colab': cod_filial,
                'nom_filial_colab': desc_filial,
                'cod_projeto_colab': cod_projeto,
                'nom_projeto_colab': desc_projeto
            }
            return JsonResponse(data)
        else:
            return HttpResponse('erro')
    def post(self, request):
        matricula = request.POST['matricula']
        nome_titular = request.POST['nome_titular']
        cod_filial = request.POST['cod_filial']
        desc_filial = request.POST['desc_filial']
        cod_projeto = request.POST['cod_projeto']
        desc_projeto = request.POST['desc_projeto']
        cod_despesa = request.POST['cod_despesa']
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        despesa_selecionada = Despesa_Unimed.objects.get(cod_despesa_unimed=cod_despesa)

        despesa_selecionada.nome_titular_senior = nome_titular
        despesa_selecionada.matricula_titular = matricula
        despesa_selecionada.cod_filial_senior = cod_filial
        despesa_selecionada.desc_filial_senior = desc_filial
        despesa_selecionada.cod_projeto_senior = cod_projeto
        despesa_selecionada.desc_projeto_senior = desc_projeto
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            despesa_selecionada.cod_empresa_senior = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            despesa_selecionada.cod_empresa_senior = 2

        despesa_selecionada.save()

        return HttpResponse('Sucesso!')

class Busca_Despesas(View):
    def get(self, request):
        competencia_busca = request.GET['competencia']
        filial_busca = request.GET['filial']
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_senior = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_senior = 2

        tab_rateio_despesas_busca = []

        #lista_despesas_sem_filial = Despesa_Unimed.objects.filter(competencia=competencia_busca)

        lista_despesas_pesquisa_com_filial = (Despesa_Unimed.objects
                                     .filter(cod_filial_senior=filial_busca,cod_empresa_senior=cod_empresa_senior,
                                             competencia=competencia_busca, cod_arq_despesa__status_arquivo=1))

        lista_despesas_pesquisa_sem_filial = (Despesa_Unimed.objects
                                     .filter(cod_filial_senior__isnull=True,cod_empresa_senior__isnull=True,
                                             competencia=competencia_busca, cod_arq_despesa__status_arquivo=1))

        lista_despesas = lista_despesas_pesquisa_com_filial.union(lista_despesas_pesquisa_sem_filial).order_by('desc_filial_senior', 'nome_beneficiario')

        valor_total_despesas_atribuidas = lista_despesas_pesquisa_com_filial.aggregate(Sum('valor'))

        for despesa in lista_despesas:
            despesa_dict = {
                           'Competencia': str(despesa.competencia).strip(),
                           'Beneficiario': str(despesa.nome_beneficiario).strip(),
                           'Cpf': str(despesa.cpf_beneficiario).strip(),
                           'Dependencia': str(despesa.tipo_depencencia).strip(),
                           'Titular': str(despesa.nome_titular).strip(),
                           'Cpf_Titular': str(despesa.cpf_titular).strip(),
                           'Desc_Despesa': str(despesa.desc_despesa).strip(),
                           'Valor': str(despesa.valor).strip(),
                           'Cod_Despesa': str(despesa.cod_despesa_unimed).strip()
                           }
            if despesa.matricula_titular is None:
                despesa_dict.update({'Matricula_Titular': '',
                                    'Nome_Titular_Senior': '',
                                    'Cod_Projeto_Senior': '',
                                    'Desc_Projeto_Senior': '',
                                    'Cod_Filial_Senior': '',
                                    'Desc_Filial_Senior': '',
                                    'Cod_Empresa_Senior': ''
                                    })
            else:
                despesa_dict.update({'Matricula_Titular': str(despesa.matricula_titular),
                                     'Nome_Titular_Senior': str(despesa.nome_titular_senior),
                                     'Cod_Projeto_Senior': str(despesa.cod_projeto_senior),
                                     'Desc_Projeto_Senior': str(despesa.desc_projeto_senior),
                                     'Cod_Filial_Senior': str(despesa.cod_filial_senior),
                                     'Desc_Filial_Senior': str(despesa.desc_filial_senior),
                                     'Cod_Empresa_Senior': str(despesa.cod_empresa_senior)
                                     })

            tab_rateio_despesas_busca.append(despesa_dict)

        if valor_total_despesas_atribuidas['valor__sum'] is not None:
            custo_total = float(valor_total_despesas_atribuidas['valor__sum'])
        else:
            custo_total = 0

        data = {
            'tab_rateio_despesas_busca': tab_rateio_despesas_busca,
            'valor_total_despesas_atribuidas': custo_total

        }
        return JsonResponse(data)

class Calcula_Rateio(View):
    def get(self, request):
        #RECEBE OS PARAMETROS DO FORM
        competencia_busca = request.GET['competencia']
        cod_filial_busca = request.GET['cod_filial']
        cod_plano_saude = request.GET['cod_plano_saude']
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        #DEFINE O CÓDIGO DA EMPRESA NO SENIOR DE ACORDO COM CÓDIGO DA EMPRESA DO PORTAL OP.
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_senior = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_senior = 2

        tab_rateio_despesas_busca = []
        lista_despesas_pesquisa_sem_filial = (Despesa_Unimed.objects
                                     .filter(cod_filial_senior__isnull=True,cod_empresa_senior__isnull=True,
                                             competencia=competencia_busca, cod_arq_despesa__status_arquivo=1))

        #VERIFICA SE EXISTEM DESPESAS SEM COLABORADOR ENCONTRADO NO SENIOR.
        if lista_despesas_pesquisa_sem_filial.first() == None:
            plano_saude = Plano_Saude.objects.filter(cod_plano_saude=cod_plano_saude).first()
            despesas_filial_plano_filtro = (Despesa_Unimed.objects
                                      .filter(cod_filial_senior=cod_filial_busca, cod_empresa_senior=cod_empresa_senior,
                                              competencia=competencia_busca, cod_arq_despesa__status_arquivo=1,
                                              cod_arq_despesa__cod_plano_saude__cod_plano_saude=cod_plano_saude))

            calculo_filial = despesas_filial_plano_filtro.aggregate(Sum('valor'))

            despesas_titulares = despesas_filial_plano_filtro.filter(cpf_beneficiario__in=despesas_filial_plano_filtro.values('cpf_titular'))
            despesas_titulares_porcentagem_excecao = despesas_titulares.exclude(percentual_empresa__isnull=True)
            despesas_titulares = despesas_titulares.filter(percentual_empresa__isnull=True).aggregate(Sum('valor'))

            # DEFINE OS VALORES DAS DESPESAS DE TITULARES COM PORCENTAGEM INFORMADA
            custo_empresa_titulares_excecao = 0
            custo_colaborador_titulares_excecao = 0
            for despesa in despesas_titulares_porcentagem_excecao:
                if despesa.percentual_empresa is not None:
                    custo_empresa_titulares_excecao += float(despesa.valor)*float(despesa.percentual_empresa)/100
                    custo_colaborador_titulares_excecao += float(despesa.valor)*(100-float(despesa.percentual_empresa))/100
            if despesas_titulares['valor__sum'] == None:
                custo_total_empresa_titular = custo_empresa_titulares_excecao
                custo_total_colaborador_titular = custo_colaborador_titulares_excecao
            else:
                custo_total_empresa_titular = custo_empresa_titulares_excecao + float(despesas_titulares['valor__sum'])*(plano_saude.percentual_empresa_titular/100)
                custo_total_colaborador_titular = custo_colaborador_titulares_excecao + float(despesas_titulares['valor__sum'])*((100-plano_saude.percentual_empresa_titular)/100)

            despesas_dependentes = despesas_filial_plano_filtro.exclude(cpf_beneficiario__in=despesas_filial_plano_filtro.values('cpf_titular'))
            despesas_dependentes_porcentagem_excecao = despesas_dependentes.exclude(percentual_empresa__isnull=True)
            despesas_dependentes = despesas_dependentes.filter(percentual_empresa__isnull=True).aggregate(Sum('valor'))

            # DEFINE OS VALORES DAS DESPESAS DE DEPENDENTES COM PORCENTAGEM INFORMADA
            custo_empresa_dependentes_excecao = 0
            custo_colaborador_dependentes_excecao = 0
            for despesa in despesas_dependentes_porcentagem_excecao:
                if despesa.percentual_empresa is not None:
                    custo_empresa_dependentes_excecao += float(despesa.valor)*float(despesa.percentual_empresa)/100
                    custo_colaborador_dependentes_excecao += float(despesa.valor)*(100-float(despesa.percentual_empresa))/100
            if despesas_dependentes['valor__sum'] == None:
                custo_total_empresa_dependente = custo_empresa_dependentes_excecao
                custo_total_colaborador_dependente = custo_colaborador_dependentes_excecao
            else:
                custo_total_empresa_dependente = custo_empresa_dependentes_excecao + float(despesas_dependentes['valor__sum'])*(plano_saude.percentual_empresa_dependente/100)
                custo_total_colaborador_dependente = custo_colaborador_dependentes_excecao + float(despesas_dependentes['valor__sum'])*((100-plano_saude.percentual_empresa_dependente)/100)

            custo_empresa_total = custo_total_empresa_titular + custo_total_empresa_dependente

            despesas_projetos_lista = despesas_filial_plano_filtro.values('desc_projeto_senior')

            custo_titulares_empresa_por_projeto = (despesas_projetos_lista
                                                   .filter(cpf_beneficiario__in=despesas_filial_plano_filtro.values('cpf_titular'))
                                                   .annotate(valor_total=Sum('valor')))
            custo_titulares_empresa_por_projeto = list(custo_titulares_empresa_por_projeto.filter(percentual_empresa__isnull=True))

            custo_titulares_por_projeto_percentual_informado = (despesas_filial_plano_filtro
                                                               .filter(cpf_beneficiario__in=despesas_filial_plano_filtro.values('cpf_titular'))
                                                               .exclude(percentual_empresa__isnull=True))
            #CRIA UMA LISTA DE DICIONÁRIOS COM AS DESPESAS DE TITULARES COM PORCENTAGEM INFORMADA
            lista_dict_titulares_percentual_informado = []
            for despesa in custo_titulares_por_projeto_percentual_informado:
                valor_empresa = float(despesa.valor) * float(despesa.percentual_empresa)/100
                valor_colaborador = float(despesa.valor) * (100-float(despesa.percentual_empresa))/100
                desc_projeto = despesa.desc_projeto_senior

                disc_despesa_percentual_informado = {
                    'valor_empresa': valor_empresa,
                    'valor_colaborador': valor_colaborador,
                    'desc_projeto': desc_projeto
                }
                lista_dict_titulares_percentual_informado.append(disc_despesa_percentual_informado)

            custo_dependentes_empresa_por_projeto = (despesas_projetos_lista
                                                   .exclude(cpf_beneficiario__in=despesas_filial_plano_filtro.values('cpf_titular'))
                                                   .annotate(valor_total=Sum('valor')))
            custo_dependentes_empresa_por_projeto = list(custo_dependentes_empresa_por_projeto)

            custo_dependentes_por_projeto_percentual_informado = (despesas_filial_plano_filtro
                                                                 .exclude(cpf_beneficiario__in=despesas_filial_plano_filtro.values('cpf_titular'))
                                                                 .exclude(percentual_empresa__isnull=True))
            # CRIA UMA LISTA DE DICIONÁRIOS COM AS DESPESAS DE DEPENDENTES COM PORCENTAGEM INFORMADA
            lista_dict_dependentes_percentual_informado = []
            for despesa in custo_dependentes_por_projeto_percentual_informado:
                valor_empresa = float(despesa.valor) * float(despesa.percentual_empresa)/100
                valor_colaborador = float(despesa.valor) * (float(despesa.percentual_empresa)/100)
                desc_projeto = despesa.desc_projeto_senior

                disc_despesa_percentual_informado = {
                    'valor_empresa': valor_empresa,
                    'valor_colaborador': valor_colaborador,
                    'desc_projeto': desc_projeto
                }
                lista_dict_dependentes_percentual_informado.append(disc_despesa_percentual_informado)
            # PARA CADA PROJETO COM DESPESAS NA FILIAL DO RATEIO, SOMA TODOS OS CUSTOS DE PORCENTAGEM INFORMADA,
            # DE PORCENTAGEM DO PLANO E CALCULA AS PARCELAS TOTAIS DE CADA PROJETO.
            for projeto in despesas_projetos_lista.distinct():
                despesa_titulares_empresa_do_projeto = [reg for reg in custo_titulares_empresa_por_projeto if reg['desc_projeto_senior'] == projeto['desc_projeto_senior']]
                lista_custo_titulares_porcentagem_informado_do_projeto = [d for d in
                                                                        lista_dict_titulares_percentual_informado if
                                                                        d['desc_projeto'] ==
                                                                        despesa_titulares_empresa_do_projeto[0][
                                                                            'desc_projeto_senior']]
                if len(lista_custo_titulares_porcentagem_informado_do_projeto) > 0:
                    custo_total_titulares_do_projeto_porcentagem_informada = float(lista_custo_titulares_porcentagem_informado_do_projeto[0]['valor_empresa']) + float(lista_custo_titulares_porcentagem_informado_do_projeto[0]['valor_colaborador'])
                    custo_titulares_do_projeto_porcentagem_informada_parcela_empresa = float(lista_custo_titulares_porcentagem_informado_do_projeto[0]['valor_empresa'])
                    custo_titulares_do_projeto_porcentagem_informada_parcela_colaborador = float(lista_custo_titulares_porcentagem_informado_do_projeto[0]['valor_colaborador'])
                else:
                    custo_total_titulares_do_projeto_porcentagem_informada = 0
                    custo_titulares_do_projeto_porcentagem_informada_parcela_empresa = 0
                    custo_titulares_do_projeto_porcentagem_informada_parcela_colaborador = 0

                if despesa_titulares_empresa_do_projeto != []:
                    custo_total_titulares_do_projeto_porcentagem_plano = float(despesa_titulares_empresa_do_projeto[0]['valor_total'])
                    custo_titulares_do_projeto_porcentagem_plano_parcela_empresa = float((custo_total_titulares_do_projeto_porcentagem_plano)*(plano_saude.percentual_empresa_titular/100))
                    custo_titulares_do_projeto_porcentagem_plano_parcela_colaborador = float((custo_total_titulares_do_projeto_porcentagem_plano)*(100-plano_saude.percentual_empresa_titular)/100)
                else:
                    custo_total_titulares_do_projeto_porcentagem_plano = 0
                    custo_titulares_do_projeto_porcentagem_plano_parcela_empresa = 0
                    custo_titulares_do_projeto_porcentagem_plano_parcela_colaborador = 0


                custo_total_titulares_do_projeto = custo_total_titulares_do_projeto_porcentagem_informada + custo_total_titulares_do_projeto_porcentagem_plano
                custo_titulares_do_projeto_parcela_empresa = custo_titulares_do_projeto_porcentagem_informada_parcela_empresa + custo_titulares_do_projeto_porcentagem_plano_parcela_empresa
                custo_titulares_do_projeto_parcela_colaborador = custo_titulares_do_projeto_porcentagem_informada_parcela_colaborador + custo_titulares_do_projeto_porcentagem_plano_parcela_colaborador

                despesa_dependentes_empresa_do_projeto = [reg for reg in custo_dependentes_empresa_por_projeto if reg['desc_projeto_senior'] == projeto['desc_projeto_senior']]
                if len(despesa_dependentes_empresa_do_projeto) > 0:
                    lista_custo_dependentes_porcentagem_informado_do_projeto = [d for d in
                                                                            lista_dict_dependentes_percentual_informado if
                                                                            d['desc_projeto'] ==
                                                                            despesa_dependentes_empresa_do_projeto[0][
                                                                                'desc_projeto_senior']]
                    if len(lista_custo_dependentes_porcentagem_informado_do_projeto) > 0:
                        custo_total_dependentes_do_projeto_porcentagem_informada = float(
                            lista_custo_dependentes_porcentagem_informado_do_projeto[0]['valor_empresa']) + float(lista_custo_dependentes_porcentagem_informado_do_projeto[0]['valor_colaborador'])
                        custo_dependentes_do_projeto_porcentagem_informada_parcela_empresa = float(
                            lista_custo_dependentes_porcentagem_informado_do_projeto[0]['valor_empresa'])
                        custo_dependentes_do_projeto_porcentagem_informada_parcela_colaborador = float(
                            lista_custo_dependentes_porcentagem_informado_do_projeto[0]['valor_colaborador'])
                    else:
                        custo_total_dependentes_do_projeto_porcentagem_informada = 0
                        custo_dependentes_do_projeto_porcentagem_informada_parcela_empresa = 0
                        custo_dependentes_do_projeto_porcentagem_informada_parcela_colaborador = 0

                    if despesa_dependentes_empresa_do_projeto != []:
                        custo_total_dependentes_do_projeto_porcentagem_plano = float(
                            despesa_dependentes_empresa_do_projeto[0]['valor_total'])
                        custo_dependentes_do_projeto_porcentagem_plano_parcela_empresa = float(
                            (custo_total_dependentes_do_projeto_porcentagem_plano) * (plano_saude.percentual_empresa_dependente / 100))
                        custo_dependentes_do_projeto_porcentagem_plano_parcela_colaborador = float(
                            (custo_total_dependentes_do_projeto_porcentagem_plano) * (100 - plano_saude.percentual_empresa_dependente) / 100)
                else:
                    custo_total_dependentes_do_projeto_porcentagem_informada = 0
                    custo_dependentes_do_projeto_porcentagem_informada_parcela_empresa = 0
                    custo_dependentes_do_projeto_porcentagem_informada_parcela_colaborador = 0
                    custo_total_dependentes_do_projeto_porcentagem_plano = 0
                    custo_dependentes_do_projeto_porcentagem_plano_parcela_empresa = 0
                    custo_dependentes_do_projeto_porcentagem_plano_parcela_colaborador = 0

                custo_total_dependentes_do_projeto = custo_total_dependentes_do_projeto_porcentagem_informada + custo_total_dependentes_do_projeto_porcentagem_plano
                custo_dependentes_do_projeto_parcela_empresa = custo_dependentes_do_projeto_porcentagem_informada_parcela_empresa + custo_dependentes_do_projeto_porcentagem_plano_parcela_empresa
                custo_dependentes_do_projeto_parcela_colaborador = custo_dependentes_do_projeto_porcentagem_informada_parcela_colaborador + custo_dependentes_do_projeto_porcentagem_plano_parcela_colaborador
                #DICT COM DADOS DE CADA PROJETO.
                despesa_dict = {
                               'desc_projeto_senior': projeto['desc_projeto_senior'],
                               'valor_total_empresa': custo_titulares_do_projeto_parcela_empresa + custo_dependentes_do_projeto_parcela_empresa,
                               'valor_total_colaborador': custo_titulares_do_projeto_parcela_colaborador + custo_dependentes_do_projeto_parcela_colaborador,
                               #'custo_total_titulares_do_projeto': custo_total_titulares_do_projeto,
                               #'custo_total_dependentes_do_projeto': custo_total_dependentes_do_projeto,
                               'custo_titulares_do_projeto_parcela_empresa': custo_titulares_do_projeto_parcela_empresa,
                               'custo_titulares_do_projeto_parcela_colaborador': custo_titulares_do_projeto_parcela_colaborador,
                               'custo_dependentes_do_projeto_parcela_empresa': custo_dependentes_do_projeto_parcela_empresa,
                               'custo_dependentes_do_projeto_parcela_colaborador': custo_dependentes_do_projeto_parcela_colaborador
                               }

                tab_rateio_despesas_busca.append(despesa_dict)
        else:
            response = HttpResponse('Resolva as despesas sem titular antes de fazer o rateio!')
            response.status_code = 405
            return response

        #DICT COM SOMA DOS DADOS ANTERIORES, DE TODOS OS PROJETOS DA FILIAL.
        despesa_total = {
            'desc_projeto_senior': 'TOTAL',
            'valor_total_empresa': custo_total_empresa_titular + custo_total_empresa_dependente,
            'valor_total_colaborador': custo_total_colaborador_titular + custo_total_colaborador_dependente,
            #'custo_total_titulares_do_projeto': custo_total_titulares_do_projeto,
            #'custo_total_dependentes_do_projeto': custo_total_dependentes_do_projeto,
            'custo_titulares_do_projeto_parcela_empresa': custo_total_empresa_titular,
            'custo_titulares_do_projeto_parcela_colaborador': custo_total_colaborador_titular,
            'custo_dependentes_do_projeto_parcela_empresa': custo_total_empresa_dependente,
            'custo_dependentes_do_projeto_parcela_colaborador': custo_total_colaborador_dependente
        }
        tab_rateio_despesas_busca.insert(0, despesa_total)

        if calculo_filial['valor__sum'] is not None:
            custo_total = float(calculo_filial['valor__sum'])
        else:
            custo_total = 0

        data = {
            #'custo_total_empresa_titular': custo_total_empresa_titular,
            #'custo_total_empresa_dependente': custo_total_empresa_dependente,
            #'custo_total_colaborador_titular': custo_total_colaborador_titular,
            #'custo_total_colaborador_dependente': custo_total_colaborador_dependente,
            #'custo_empresa_total': custo_empresa_total,
            'custo_total': custo_total,
            'tab_rateio_despesas_busca': tab_rateio_despesas_busca
        }
        return JsonResponse(data)

class Obter_Filiais(View):
    def get(self, request):
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_filtro = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_filtro = 2
        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro, cod_arq_despesa__status_arquivo=1).values_list(
            'cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})
        return JsonResponse(lista_filiais_dict, safe=False)

class Historico_Importacoes(View):
    def get(self, request):
        #cod_usu_session = request.session['cod_usuario_logado']
        cod_colaborador = request.GET['id_colaborador']
        colaborador_historico = Usuario.objects.filter(cod_usu=cod_colaborador).first()
        lista_importacoes_colaborador = Arquivo_Despesas.objects.filter(cod_usu=colaborador_historico.cod_usu).order_by('cod_arq_despesa')
        lista_arquivos_importacao = []

        for arq in lista_importacoes_colaborador:
            data_importacao = arq.nome_arq_imp.split('_')[6:12]
            data_hora_importacao = datetime(day=int(data_importacao[0]), month=int(data_importacao[1]), year=int(data_importacao[2]), hour=int(data_importacao[3]), minute=int(data_importacao[4]), second=int(data_importacao[5].split('.')[0]))
            plano = Plano_Saude.objects.get(cod_plano_saude=arq.cod_plano_saude.cod_plano_saude)
            if plano.especificacao != None:
                str_especificacao = '- ' + plano.especificacao
            else:
                str_especificacao = ''
            lista_arquivos_importacao.append({
                'nome_arq_original': arq.nome_arq_original,
                'plano_saude': plano.operadora_plano.desc_operadora_plano + '-' + plano.filial + str_especificacao,
                'data': data_hora_importacao,
                'qtd_registros': arq.qtd_registros,
                'id_importacao_cancelamento': str(arq.status_arquivo) + '--' + str(arq.cod_arq_despesa)
            })

        return JsonResponse(lista_arquivos_importacao, safe=False)

    def post(self, request):
        cod_usu_session = request.session['cod_usuario_logado']
        cod_arq_importacao = request.POST['id_importacao']
        arquivo = Arquivo_Despesas.objects.filter(cod_arq_despesa=cod_arq_importacao).first()
        arquivo.status_arquivo = 0
        arquivo.data_desativacao = datetime.now()
        arquivo.cod_usu_desativacao = cod_usu_session
        arquivo.save()

        retorno = 'Ok'
        return HttpResponse(retorno)

class Projeto_Filial(View):
    def get(self, request):
        #cod_usu_session = request.session['cod_usuario_logado']
        cod_filial = request.GET['cod_filial']
        projetos = Projetos_Senior.objects.exclude(desc_projeto__contains="INATIVO")
        projetos_dict = []


        for proj in projetos:
            desc_proj = proj.desc_projeto
            if proj.usu_desc_projeto != '' and proj.usu_desc_projeto != ' ' and proj.usu_desc_projeto is not None:
                print(proj.usu_desc_projeto)
                desc_proj += ' - ' + proj.usu_desc_projeto
            projetos_dict.append({
                'cod_projeto': proj.cod_senior_projeto,
                'desc_proj': desc_proj,
            })

        return JsonResponse(projetos_dict, safe=False)

class Colaborador_Excecao_View(View):
    def get(self, request):
        #cod_usu_session = request.session['cod_usuario_logado']
        colaboradores_excecao = list(Colaborador_Excecao.objects.all().order_by('cod_colab_excecao'))
        colaboradores_excecao_dict = []

        for col in colaboradores_excecao:
            colaboradores_excecao_dict.append({
                'cod_colab_excecao': col.cod_colab_excecao,
                'nome_colab_excecao': col.nome_colab_excecao,
                'cpf_colab_excecao': col.cpf_colab_excecao,
                'projeto_col': col.desc_proj_colab_excecao,
            })

        return JsonResponse(colaboradores_excecao_dict, safe=False)
    def post(self, request):
        nome_colab_excecao = request.POST['nome_colab_excecao']
        cpf_colab_excecao = request.POST['cpf_colab_excecao']
        cod_projeto_colab_excecao = request.POST['cod_projeto_colab_excecao']
        cod_filial_colab_excecao = request.POST['cod_filial_colab_excecao']
        competencia_inicio_vigencia = request.POST['competencia_inicio_vigencia']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        conexao_senior = Conexao_Senior_BD(obj_usu.cod_filial.cod_empresa.cod_empresa)
        cod_filial_senior = Filial.objects.filter(cod_filial=cod_filial_colab_excecao).first().cod_filial_senior
        desc_filial_senior = conexao_senior.retorna_nome_filial_senior(cod_filial_colab_excecao)['nome_fil']

        desc_proj = Projetos_Senior.objects.filter(cod_senior_projeto=cod_projeto_colab_excecao).first().desc_projeto

        colab_excecao = Colaborador_Excecao(
            nome_colab_excecao=nome_colab_excecao,
            cpf_colab_excecao=cpf_colab_excecao,
            cod_filial_colab_excecao=cod_filial_senior,
            desc_filial_colab_excecao=desc_filial_senior,
            cod_proj_colab_excecao=cod_projeto_colab_excecao,
            desc_proj_colab_excecao=desc_proj,
            competencia_inicio=competencia_inicio_vigencia,
            status_ativo=1
        )
        colab_excecao.save()

        return HttpResponse('Sucesso!')
