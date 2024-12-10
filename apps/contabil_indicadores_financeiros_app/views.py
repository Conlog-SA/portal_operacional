from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.utils import timezone

from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario



class Acessa_Form_Strut_Contas(View):
    def get(self, request):
        print('###Codigo aqui')

    def post(self, request):
        print('###Codigo aqui')

class Estrutura_Contas(View):
    def get(self, request):
        print('###Codigo aqui')

    def post(self, request):
        print('###Codigo aqui')

class Conta(View):
    def get(self, request):
        print('###Codigo aqui')

    def post(self, request):
        print('###Codigo aqui')