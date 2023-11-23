from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.safety_layout_checklist_app.models import Layout_Check
from apps.usuario_app.models import Usuario


# Create your views here.

class Form_Seguranca_Check(View):
    def get(self, request):
        lista_checks = Layout_Check.objects.all()
        contexto = {
            'lista_checks': lista_checks
        }
        return render(request,'safety_layout_checklist_app/form_cad_layout_checklist.html', contexto)

class Form_Cadastro_Check(View):
    def get(self, request):
        cod_check = request.GET['cod_check']
        print(cod_check)
        check_selecionado = Layout_Check.objects.get(pk=cod_check)
        data = {
            'check_selecionado': {
                'desc_check': check_selecionado.desc_check,
                'versao': check_selecionado.versao,
                'data_desativacao': check_selecionado.data_desativacao,
                'periodicidade': check_selecionado.periodicidade,
                'medida_periodicidade': check_selecionado.medida_periodicidade,
            }
        }
        return JsonResponse(data)

    def post(self, request):
        desc_check = request.POST['desc_check']
        versao = request.POST['versao']
        data_desativacao = request.POST['data_desativacao']
        medida_periodicidade = request.POST['medida_periodicidade']
        periodicidade = request.POST['periodicidade']
        cod_usuario_sessao = request.session['cod_usuario_logado']

        obj_check = Layout_Check(
            desc_check = desc_check,
            versao = versao,
            data_desativacao = data_desativacao,
            medida_periodicidade = medida_periodicidade,
            periodicidade = periodicidade,
            cod_usu = Usuario.objects.get(cod_usu = cod_usuario_sessao),
            data_inclusao = datetime.now()
        )
        obj_check.save()
        teste = 'Deu bom'
        data = {
            'msg': teste
        }
        return JsonResponse(data, safe=False)