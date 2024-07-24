import locale
import os
from datetime import datetime

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db.models import Value, Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.conecta_senior_app.views import Conexao_Senior_BD
from apps.estrut_org_app.models import Filial
from apps.gente_gestao_rateio_unimed_app.models import Arquivo_Despesas, Despesa_Unimed
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
        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro).values_list(
            'cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            print(filial[0])
            print(filial[1])
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})
        #lista_filiais = Filial.objects.filter(cod_empresa__cod_empresa=obj_usu.cod_filial.cod_empresa.cod_empresa)
        contexto = {
            'lista_filiais': lista_filiais_dict,
            'desc_menu': 'Rateio Despesas Unimed',
            'lista_filiais': lista_filiais_dict,
        }
        return render(request, 'gente_gestao_rateio_unimed_app/form_rateio_despesa_unimed.html', contexto)

    def post(self, request):
        myfile = request.FILES['file']
        cod_usu_session = request.session['cod_usuario_logado']

        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')

        caminho_arq_importado = 'docs/rateio_unimed/' + obj_usu.cod_filial.unidade_abrev + '/rateio_unimed_' + obj_usu.cod_filial.unidade_abrev + '_' + \
                                obj_usu.login_usu.replace('.', '_') + '_' + str(data_atual_dd_mm_yyyy).replace('/', '_') \
                                + '_' + str(hota_atual).replace(':', '_') + '.xlsx'
        arquivo_despesa = Arquivo_Despesas(
            nome_arq_imp=caminho_arq_importado,
            nome_arq_original=str(myfile.name),
            cod_usu=obj_usu,
            qtd_registros=0,
            qtd_importados=0,
            qtd_atualizados=0
        )
        arquivo_despesa.save()

        fs = FileSystemStorage()
        filename = fs.save(caminho_arq_importado, myfile)
        uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado)
        tab_rateio_despesas_nao_importadas = []
        conteudo_arq_plan_unimed = pd.read_excel(uploaded_file_url)
        conteudo_arq_plan_unimed = conteudo_arq_plan_unimed.dropna(how='all')
        conteudo_arq_plan_unimed.rename(columns=lambda x: str(x).strip(), inplace=True)
        count_reg_imp = 0
        count_reg_up = 0
        print(conteudo_arq_plan_unimed.columns.values.tolist())
        for index, row in conteudo_arq_plan_unimed.iterrows():
            nome_beneficiario = str(row['NOME']).strip()
            tipo_depencencia = str(row['DEPENDENCIA']).strip()
            nome_titular = str(row['NOME_TITULAR']).strip()
            desc_despesa = str(row['DESC_DESPESA']).strip()
            valor = float(row['VL_FATURADO'])
            cpf_beneficiario = str(row['CPF']).strip()

            if 'CPF_TITULAR' in conteudo_arq_plan_unimed.columns.values.tolist():
                cpf_titular = str(row['CPF_TITULAR']).strip()
            else:
                print(str(row['NOME']).strip())
                cpf_titular = str(conteudo_arq_plan_unimed[(conteudo_arq_plan_unimed['NOME'] == row['NOME_TITULAR']) & (conteudo_arq_plan_unimed['NOME'] == conteudo_arq_plan_unimed['NOME_TITULAR'])]['CPF'].iloc[0]).strip()


            competencia_split = str(row['COMPETENCIA']).strip().split('/')
            competencia = competencia_split[1] + '-' + competencia_split[0]

            obj_registro_despesa = Despesa_Unimed.objects.filter(competencia=competencia,
                                                              cpf_beneficiario=cpf_beneficiario,
                                                              nome_beneficiario=nome_beneficiario,
                                                              tipo_depencencia=tipo_depencencia,
                                                              nome_titular=nome_titular,
                                                              cpf_titular=cpf_titular,
                                                              desc_despesa=desc_despesa).first()
            if obj_registro_despesa == None:
                conexao_senior = Conexao_Senior_BD()
                cod_empresa_senior = None
                if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
                    cod_empresa_senior = 1
                elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
                    cod_empresa_senior = 2
                titular_senior = conexao_senior.pesquisar_dados_colaborador_por_cpf_emp(cpf_titular, cod_empresa_senior)
                if 'erro' not in titular_senior:
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
                        cod_filial_senior=titular_senior['cod_filial_colab'],
                        desc_filial_senior=titular_senior['nom_filial_colab'],
                        cod_projeto_senior=titular_senior['cod_projeto_colab'],
                        desc_projeto_senior=titular_senior['nom_projeto_colab'],
                        cod_empresa_senior=cod_empresa_senior,
                    )
                    print(titular_senior['nom_projeto_colab'])
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
                    count_reg_imp += 1
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
                        cod_arq_despesa=arquivo_despesa
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

                    count_reg_imp += 1
            else:
                obj_registro_despesa.valor = float(row['VL_FATURADO'])

                obj_registro_despesa.save()
                count_reg_up += 1

            #except Exception as e:
            #    print(e)
            #    tab_rateio_despesas_nao_importadas.append(
            #        'Competencia: ' + str(row['COMPETENCIA']) + ', Beneficiário: ' + str(row['NOME']) +
            #        'Titular: ' + str((row['NOME_TITULAR']))
            #    )
        print('finalizou for')
        arquivo_despesa.qtd_registros = conteudo_arq_plan_unimed.shape[0]
        arquivo_despesa.qtd_importados = count_reg_imp
        arquivo_despesa.qtd_atualizados = count_reg_up
        arquivo_despesa.save()

        cod_empresa_filtro = 0
        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_filtro = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_filtro = 2
        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro).values_list(
            'cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            print(filial[0])
            print(filial[1])
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})

        data = {
            'tab_rateio_despesas_nao_importadas': tab_rateio_despesas_nao_importadas,
            'lista_filiais': lista_filiais_dict,
            'qtd_total_reg': conteudo_arq_plan_unimed.shape[0],
            'qtd_reg_imp': count_reg_imp,
            'qtd_reg_up': count_reg_up
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

        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro).values_list('cod_filial_senior', 'desc_filial_senior').distinct()
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
        conexao_senior = Conexao_Senior_BD()
        titular_senior = conexao_senior.pesquisar_dados_por_matricula(matricula, cod_empresa_senior)
        if 'erro' not in titular_senior:
            print(titular_senior['nome_colab'])
            print(titular_senior['cod_filial_colab'])
            print(titular_senior['nom_filial_colab'])
            print(titular_senior['cod_projeto_colab'])
            print(titular_senior['nom_projeto_colab'])
            data = {
                'nome_titular_senior': titular_senior['nome_colab'],
                'cod_filial_colab': titular_senior['cod_filial_colab'],
                'nom_filial_colab': titular_senior['nom_filial_colab'],
                'cod_projeto_colab': titular_senior['cod_projeto_colab'],
                'nom_projeto_colab': titular_senior['nom_projeto_colab']
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
                                             competencia=competencia_busca))

        lista_despesas_pesquisa_sem_filial = (Despesa_Unimed.objects
                                     .filter(cod_filial_senior__isnull=True,cod_empresa_senior__isnull=True,
                                             competencia=competencia_busca))

        lista_despesas = lista_despesas_pesquisa_com_filial.union(lista_despesas_pesquisa_sem_filial).order_by('desc_filial_senior', 'nome_beneficiario')

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

        data = {
            'tab_rateio_despesas_busca': tab_rateio_despesas_busca
        }
        return JsonResponse(data)

class Calcula_Rateio(View):
    def get(self, request):
        competencia_busca = request.GET['competencia']
        filial_busca = request.GET['filial']
        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu = Usuario.objects.filter(cod_usu=cod_usu_session).first()

        #locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        if obj_usu.cod_filial.cod_empresa.cod_empresa == 12:
            cod_empresa_senior = 1
        elif obj_usu.cod_filial.cod_empresa.cod_empresa == 17:
            cod_empresa_senior = 2

        tab_rateio_despesas_busca = []

        lista_despesas_pesquisa_sem_filial = (Despesa_Unimed.objects
                                     .filter(cod_filial_senior__isnull=True,cod_empresa_senior__isnull=True,
                                             competencia=competencia_busca))

        if lista_despesas_pesquisa_sem_filial.first() == None:

            calculo_projetos_lista = (Despesa_Unimed.objects
                                         .filter(cod_filial_senior=filial_busca,cod_empresa_senior=cod_empresa_senior,
                                                 competencia=competencia_busca).values('desc_projeto_senior').annotate(valor=Sum('valor'),quantidade_beneficiarios=Count('cpf_beneficiario')))
            print(calculo_projetos_lista)
            for projeto in calculo_projetos_lista:
                despesa_dict = {
                               'desc_projeto_senior': projeto['desc_projeto_senior'],
                               'valor': projeto['valor'], #locale.currency(projeto['valor'], grouping=True, symbol=None),
                               'quantidade_beneficiarios': projeto['quantidade_beneficiarios']
                               }

                tab_rateio_despesas_busca.append(despesa_dict)
        else:
            response = HttpResponse('Resolva as despesas sem titular antes de fazer o rateio!')
            response.status_code = 405
            return response

        data = {
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
        lista_filiais = Despesa_Unimed.objects.filter(cod_empresa_senior=cod_empresa_filtro).values_list(
            'cod_filial_senior', 'desc_filial_senior').distinct()
        lista_filiais_dict = []
        for filial in lista_filiais:
            print(filial[0])
            print(filial[1])
            lista_filiais_dict.append({'cod_filial_senior': filial[0], 'desc_filial_senior': filial[1]})
        return JsonResponse(lista_filiais_dict, safe=False)



