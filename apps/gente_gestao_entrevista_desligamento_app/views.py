from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta, date

from django.views.decorators.csrf import csrf_exempt

from apps.gente_gestao_entrevista_desligamento_app.models import Desligamento
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

class Frm_Consulta_Entrevista_Desligamento(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        contexto = {
            'obj_usuario_logado': obj_usuario_logado
        }

        return render(request,'gente_gestao_entrevista_desligamento_app/form_lista_desligados.html', contexto)


class Frm_Resposta_Entrevista_Desligamento(View):
    def get(self, request):
        return render(request, 'gente_gestao_entrevista_desligamento_app/form_resposta_entrevista_desligamentos.html')