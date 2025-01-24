from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.utils import timezone

from apps.contabil_indicadores_financeiros_app.models import Estrutura_Contas
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario



class Acessa_Form_Strut_Contas(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        lista_estruturas_contas = Estrutura_Contas.objects.filter(cod_usu__cod_filial__cod_empresa=obj_usuario_logado.cod_filial.cod_empresa)

        context = {
            'lista_tipos': lista_estruturas_contas,
        }

        return render(request,  'menu_app/form_cadastro_estrut_contas.html', context)
    def post(self, request):
        print('###Codigo aqui')

class Estrutura_Conta(View):
    def get(self, request):
        print('###Codigo aqui')

    def post(self, request):
        print('###Codigo aqui')

class Conta(View):
    def get(self, request):
        print('###Codigo aqui')

    def post(self, request):
        print('###Codigo aqui')