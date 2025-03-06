import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta, date

from django.views.decorators.csrf import csrf_exempt

from apps.gente_gestao_entrevista_desligamento_app.models import Desligamento, Respostas_Entrevista_Desligamento, \
    Render, Secao_Entrevista_Desligamento
from apps.phishing_app import models
from apps.usuario_app.models import Usuario


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
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        data_atual = datetime.now()

        lista_desligamentos = Desligamento.objects.filter(data_desligamento__gte=date(data_atual.year,
                                                                                                   data_atual.month,
                                                                                                   data_atual.day),
                                                             data_desligamento__lte=date(data_atual.year,
                                                                                              data_atual.month,
                                                                                              data_atual.day))

        lista_desligamentos_dict = []
        for desligamento in lista_desligamentos:
            resposta = Respostas_Entrevista_Desligamento.objects.filter(matricula=desligamento.matricula).first()
            if resposta is not None:
                flag_existe_resposta = True
            else:
                flag_existe_resposta = False

            lista_desligamentos_dict.append({'matricula': desligamento.matricula,
                                             'nome': desligamento.nome,
                                             'unidade': desligamento.unidade,
                                             'data_admissao': desligamento.data_admissao,
                                             'data_desligamento': desligamento.data_desligamento,
                                             'cargo': desligamento.cargo,
                                             'contato_telefone': desligamento.contato_telefone,
                                             'contato_email': desligamento.contato_email,
                                             'existe_resposta': flag_existe_resposta})

        contexto = {
            'lista_desligamentos': lista_desligamentos_dict
        }

        return render(request,'gente_gestao_entrevista_desligamento_app/form_lista_desligados.html', contexto)

class Frm_Consulta_Entrevista_Desligamento(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        matricula_desligamento = request.GET.get('matricula')
        data_atual = datetime.now()

        if matricula_desligamento is not None:
            resposta_desligamento = Respostas_Entrevista_Desligamento.objects.filter(matricula=matricula_desligamento).first()
            if resposta_desligamento is not None:
                respostas_list_dicts = json.loads(resposta_desligamento.respostas_formulario)
                if isinstance(respostas_list_dicts, list) and all(isinstance(item, dict) for item in respostas_list_dicts):
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
                    raise Exception('Formato incorreto das respostas de questionário')
            else:
                raise Exception('Questionário não respondido pela matricula informada')
        else:
            raise Exception('Matricula não informada')

        contexto = {
            'relatorio_desligamento': relatorio_desligamento,
            'lista_secoes': lista_secoes
        }

        return Render.render('gente_gestao_entrevista_desligamento_app/form_lista_desligados.html', contexto, 'Myfile')

class Frm_Resposta_Entrevista_Desligamento(View):
    def get(self, request):
        return render(request, 'gente_gestao_entrevista_desligamento_app/form_resposta_entrevista_desligamentos.html')