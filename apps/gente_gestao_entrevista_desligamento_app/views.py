import json
import os

from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from datetime import datetime, timedelta, date

from django.views.decorators.csrf import csrf_exempt
from pyhtml2pdf import converter

from apps.envio_email_app.views import Envio_Email
from apps.estrut_org_app.models import Filial, Empresa
from apps.gente_gestao_entrevista_desligamento_app.models import Desligamento, Respostas_Entrevista_Desligamento, \
    Render, Secao_Entrevista_Desligamento
from apps.usuario_app.models import Usuario
from apps.conecta_senior_app.views import Conexao_Senior_BD
import secrets

# Create your views here.
class Entrevista_Desligamento_Gerencial(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        contexto = {
            'obj_usuario_logado': obj_usuario_logado
        }

        return render(request,'gente_gestao_entrevista_desligamento_app/form_lista_desligados.html', contexto)

class Frm_Busca_Desligamentos_Periodo(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        inicio_periodo = request.GET.get('inicio_periodo_desligamentos')
        fim_periodo = request.GET.get('fim_periodo_desligamentos')
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        data_atual = datetime.now()

        conexao = Conexao_Senior_BD(12)
        desligamentos = conexao.retorna_desligamentos_periodo(inicio_periodo, fim_periodo)

        print(desligamentos)
        cargos_lideranca = ['Coordenador', 'Supervisor', 'Gerente', 'Diretor', 'Head', 'Presidente']
        empresa_conlog = Empresa.objects.filter(cod_empresa=12).first()

        for desligamento in desligamentos:
            if desligamento[2] == 2 or any(car.lower() in desligamento[7].lower() for car in cargos_lideranca):
                filial_desligamento = Filial.objects.filter(cod_filial_senior=desligamento[2],cod_empresa=empresa_conlog).first()

                if filial_desligamento is None:
                    desc_filial = desligamento[3]
                else:
                    desc_filial = filial_desligamento.desc_filial

                if desligamento[8] is None or desligamento[8] == '' or len(desligamento[8]) < 3:
                    telefone = 'Não encontrado'
                else:
                    print(desligamento[8])
                    telefone = (str(desligamento[9]) + desligamento[8].replace(' ', ''))


                desligamento_obj = Desligamento(
                    matricula = desligamento[0],
                    nome=desligamento[1],
                    cod_unidade=filial_desligamento,
                    unidade=desc_filial,
                    data_admissao=desligamento[4],
                    data_desligamento=desligamento[5],
                    cargo=desligamento[7],
                    contato_telefone=telefone
                )
                desligamento_obj.save()

        lista_desligamentos = Desligamento.objects.filter(data_desligamento__gte=date(int(inicio_periodo.split('-')[0]),
                                                                                                   int(inicio_periodo.split('-')[1]),
                                                                                                   int(inicio_periodo.split('-')[2])),
                                                             data_desligamento__lte=date(int(fim_periodo.split('-')[0]),
                                                                                              int(fim_periodo.split('-')[1]),
                                                                                              int(fim_periodo.split('-')[2])))

        lista_desligamentos_dict = []
        for desligamento in lista_desligamentos:
            resposta = Respostas_Entrevista_Desligamento.objects.filter(matricula=desligamento.matricula,parcial=0).first()
            if resposta is not None:
                flag_existe_resposta_final = True
            else:
                flag_existe_resposta_final = False

            lista_desligamentos_dict.append({'matricula': desligamento.matricula,
                                             'nome': desligamento.nome,
                                             'unidade': desligamento.unidade,
                                             'data_admissao': desligamento.data_admissao+timedelta(hours=3),
                                             'data_desligamento': desligamento.data_desligamento+timedelta(hours=3),
                                             'cargo': desligamento.cargo,
                                             'contato_telefone': desligamento.contato_telefone,
                                             'contato_email': desligamento.contato_email,
                                             'existe_resposta': flag_existe_resposta_final})

        contexto = {
            'lista_desligamentos': lista_desligamentos_dict
        }

        return JsonResponse(contexto, safe=False)

class Frm_Gerar_Link_Entrevista_Desligamento(View):
    def get(self, request):
        matricula_desligamento = request.GET.get('matricula_colab')

        desligamento = Desligamento.objects.filter(matricula=int(matricula_desligamento)).first()
        token = ''
        print(matricula_desligamento)
        if desligamento is not None:
            if desligamento.token_acesso is None and desligamento.token_data_expiracao is None:
                token = secrets.token_urlsafe(32)
                data_expiracao = timezone.now() - timedelta(hours=3) + timedelta(days=15)

                desligamento.token_acesso = token
                desligamento.token_data_expiracao = data_expiracao
                desligamento.save()

                msg_retorno = 'Link emitido! Copiado para transferência'

            elif desligamento.token_acesso is not None and desligamento.token_data_expiracao is not None:
                if desligamento.token_data_expiracao > timezone.now():
                    token = desligamento.token_acesso
                    msg_retorno = 'Link copiado para transferência'

                else:
                    token = secrets.token_urlsafe(32)
                    data_expiracao = datetime.now(timezone.utc) + timedelta(days=7)

                    desligamento.token_acesso = token
                    desligamento.token_data_expiracao = data_expiracao
                    desligamento.save()

                    msg_retorno = 'Link renovado! Copiado para área de transferência'
            else:
                msg_retorno = 'Erro de registro de desligamento, contate um administrador!'
        else:
            msg_retorno = 'Esse desligamento não foi encontrado, atualize a página ou contate um administrador!'

        data = {
            'msg_retorno': msg_retorno
        }
        if token != '':
            data['token'] = token


        return JsonResponse(data)

class Frm_Consulta_Entrevista_Desligamento(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        id_desligamento = request.GET.get('id_desligamento')
        desligamento = Desligamento.objects.filter(matricula=id_desligamento).first()

        filiais = list(
            Filial.objects.filter(cod_empresa=desligamento.cod_unidade.cod_empresa, ativo=1).values('cod_filial',
                                                                                                    'desc_filial'))

        if id_desligamento is not None and id_desligamento != '':
            resposta_desligamento = Respostas_Entrevista_Desligamento.objects.filter(matricula=id_desligamento, parcial=0).first()
            if resposta_desligamento is not None:
                respostas_json = resposta_desligamento.resposta

                '''if isinstance(respostas_list_dicts, list) and all(isinstance(item, dict) for item in respostas_list_dicts):
                    relatorio_desligamento = {'matricula': resposta_desligamento.matricula,
                                              'data_preenchimento': resposta_desligamento.data_preenchimento,
                                              'respostas_formulario': respostas_list_dicts,
                                              'data_anotacoes_especialista': resposta_desligamento.data_anotacoes_especialista,
                                              'cod_secao': 'teste'}#resposta_desligamento.}
                    lista_secoes = Secao_Entrevista_Desligamento.objects.all()
                    lista_secoes_dict = []
                    for secao in lista_secoes:
                        lista_secoes_dict.append({
                            'cod_secao': secao.cod_secao,
                            'descricao': secao.descricao
                        })
                else:
                    raise Exception('Formato incorreto das respostas de questionário')'''
            else:
                raise Exception('Questionário não respondido pela matricula informada')
        else:
            raise Exception('Matricula não informada')

        '''contexto = {
            'relatorio_desligamento': relatorio_desligamento,
            'lista_secoes': lista_secoes
        }'''

        obj_respostas = json.loads(respostas_json)
        ultimo_dia_trab_split = obj_respostas['ultimo_dia'].split('-')
        obj_respostas['ultimo_dia'] = ultimo_dia_trab_split[2] + '/' + ultimo_dia_trab_split[1] + '/' + ultimo_dia_trab_split[0]
        #print(obj_respostas['ultimo_dia'])

        dados = {
            'matricula': desligamento.matricula,
            'nome': desligamento.nome,
            'contato_email': desligamento.contato_email,
            'cod_unidade': desligamento.cod_unidade,
            'unidade': desligamento.unidade,
            'cargo': desligamento.cargo,
            'contato_telefone': desligamento.contato_telefone,
            'token_acesso': desligamento.token_acesso,
            'filiais': filiais,
            'preenchimento_parcial': obj_respostas
        }
        print(render(request, 'gente_gestao_entrevista_desligamento_app/form_relatorio_entrevista_desligamentos.html',
                      dados).content.decode('utf-8'))

        #print(dados['preenchimento_parcial']['token'])
        html_relatorio = render(request, 'gente_gestao_entrevista_desligamento_app/form_relatorio_entrevista_desligamentos.html',
                      dados).content.decode('utf-8')

        current_app_directory = os.path.dirname(os.path.abspath(__file__))
        temp_html_path = os.path.join(current_app_directory, r'html_relatorio_entrevista_temp.html')
        #temp_pdf_path = os.path.join(current_app_directory, r'pdf_relatorio_entrevista_temp.pdf')

        with open(temp_html_path, "w", encoding='utf-8') as file:
            file.write(html_relatorio)
        return Render.render('gente_gestao_entrevista_desligamento_app/form_relatorio_entrevista_desligamentos.html',
                             dados,
                             'myfile')
        #print(temp_html_path)
        #print(os.path.abspath(__file__))

        #converter.convert(f'www.google.com', 'teste.pdf')

        #with open(temp_pdf_path, 'r') as f:
        #    file_data = f.read()

        #response = HttpResponse(file_data, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="pdf_relatorio_entrevista_temp.pdf"'

        #pdf = open(temp_pdf_path, 'rb')

        #response = HttpResponse(pdf.read())
        #response['Content-Type'] = 'application/pdf'
        #response['Content-disposition'] = 'attachment'
        #response = FileResponse(open(temp_pdf_path, 'rb'), content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="pdf_relatorio_entrevista_temp.pdf"'  # Optional: suggest filename
        #return response


class Registra_Desligamentos(View):
    @csrf_exempt
    def get(self, request):
        token_link = request.GET.get('token')

        desligamento = Desligamento.objects.filter(token_acesso=token_link).first()
        if desligamento is None:
            return JsonResponse({'msg': 'Erro: Colaborador desligado não encontrado'})

        resposta = Respostas_Entrevista_Desligamento.objects.filter(matricula=desligamento.matricula).first()

        if desligamento.token_data_expiracao < timezone.now() and resposta is None:
            return JsonResponse({ 'msg': 'Erro: Link da entrevista expirado, solicite um link novo caso deseje realiza-la!' })
        elif resposta is not None:
            if resposta.parcial == 0:
                return render(request, 'gente_gestao_entrevista_desligamento_app/msg_ja_realizada_entrevista_desligamento.html')
            else:
                preenchimento_parcial = resposta.resposta
        else:
            preenchimento_parcial = None

        filiais = list(Filial.objects.filter(cod_empresa=desligamento.cod_unidade.cod_empresa,ativo=1).values('cod_filial', 'desc_filial'))

        dados = {
            'matricula': desligamento.matricula,
            'nome': desligamento.nome,
            'contato_email': desligamento.contato_email,
            'cod_unidade': desligamento.cod_unidade,
            'unidade': desligamento.unidade,
            'cargo': desligamento.cargo,
            'contato_telefone': desligamento.contato_telefone,
            'token_acesso': desligamento.token_acesso,
            'filiais': filiais,
            'preenchimento_parcial': preenchimento_parcial
        }

        return render(request, 'gente_gestao_entrevista_desligamento_app/form_resposta_entrevista_desligamentos.html', dados)

    @csrf_exempt
    def post(self, request):
        token = request.POST['token']
        desligamento = Desligamento.objects.filter(token_acesso=token).first()
        resposta = Respostas_Entrevista_Desligamento.objects.filter(matricula=desligamento.matricula).first()
        if resposta is not None:
            if resposta.parcial == 0:
                return render(request,'gente_gestao_entrevista_desligamento_app/msg_ja_realizada_entrevista_desligamento.html')

        json_respostas = request.POST['json_respostas']
        entrevista_finalizada = request.POST['finalizada']
        if entrevista_finalizada == 'true':
            resposta_parcial = 0
        elif entrevista_finalizada == 'false':
            resposta_parcial = 1

        resposta = Respostas_Entrevista_Desligamento(
            matricula=desligamento.matricula,
            resposta=json_respostas,
            parcial=resposta_parcial
        )
        resposta.save()

        desligamento.data_preenchimento = datetime.now()
        desligamento.save()

        server_email = Envio_Email()
        obj_usuario_resposta = {
            'nome': desligamento.nome
        }

        if resposta_parcial == 0:
            server_email.envia_email_preenchimento_entrevista_desligamento(obj_usuario_resposta)
            return render(request, 'gente_gestao_entrevista_desligamento_app/msg_finalizada_entrevista_desligamento.html')
        else:
            return HttpResponse('Ok')