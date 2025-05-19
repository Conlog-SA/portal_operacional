from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

from apps.nps_ti_app.models import Filial_Nps, Pesquisa_Satisfacao, Email_Enviado_Nps


class Form_Nps_Ti_Redirect(View):
    def get(self, request):
        email = request.GET.get('email')

        if email is None:
            return render(request, 'nps_ti_app/erro_param_email.html')

        request.session['email'] = email

        return HttpResponseRedirect(redirect_to='form/')
        #context = {'email': email, 'flag_empresa': flag_empresa}
        #return render(request, 'nps_ti_app/form_nps_ti.html', context)

class Form_Nps_Ti(View):
    def get(self, request):
        if 'email' not in request.session:
            return render(request, 'nps_ti_app/erro_param_email.html')
        email = request.session['email']
        del request.session['email']

        if '@deeplogistica.com.br' in email:
            flag_empresa = 1
            cod_empresa = 17
        else:
            flag_empresa = 0
            cod_empresa = 12

        filiais_nps = Filial_Nps.objects.filter(Q(cod_empresa_nps=cod_empresa) | Q(cod_empresa_nps=18))

        context = {'email': email, 'flag_empresa': flag_empresa, 'filiais_nps': filiais_nps}
        return render(request, 'nps_ti_app/form_nps_ti.html', context)


    @csrf_exempt
    def post(self, request):
        email = request.POST['email']
        cod_filial_nps = request.POST['cod_filial_nps']
        json_respostas = request.POST['json_respostas']

        filial_nps = Filial_Nps.objects.filter(cod_filial_nps=cod_filial_nps).first()
        pesquisa_respondida = Pesquisa_Satisfacao(
            cod_filial_nps=filial_nps,
            questoes_respondidas=json_respostas,
            email=email,
            data_resposta=datetime.now(),
        )
        pesquisa_respondida.save()

        if '@deeplogistica.com.br' in email:
            flag_empresa = 1
        else:
            flag_empresa = 0

        context = {
            'flag_empresa': flag_empresa
        }

        return render(request, 'nps_ti_app/msg_finalizada_nps_ti.html', context)

class Envio_Email_Nps(View):

    @csrf_exempt
    def get(self, request):
        usuario = request.GET['email'].split('@')[0]
        status = request.GET['status']
        data_envio = datetime.now()

        objeto = Email_Enviado_Nps(
            usuario=usuario,
            data_envio=data_envio,
            status=status
        )
        objeto.save()

        return JsonResponse('Ok', safe=False)