from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from apps.contratos_frete_deep_app.models import Contrato_Processado

class Processa_Contrato(View):

    @csrf_exempt
    def post(self, request):
        nro_contrato = request.POST['usuario']
        razao_social_contratado = request.POST['senha']
        data_contrato = request.POST['email']
        status = request.POST['usuario']
        nome_arquivo = request.POST['senha']
        data_processamento = datetime.now()

        objeto = Contrato_Processado(
            nro_contrato=nro_contrato,
            razao_social_contratado=razao_social_contratado,
            data_contrato=data_contrato,
            status=status,
            nome_arquivo=nome_arquivo,
            data_processamento=data_processamento
        )

        objeto.save()

        return JsonResponse('Ok', safe=False)