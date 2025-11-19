from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.estrut_org_app.models import Filial, Projeto



class Frm_Analise_Vagas_View(View):
    def get(self, request):
        filiais = list((Filial.objects.filter(desc_filial__contains="AMBEV", cod_empresa=12)))

        context = {
            'filiais': filiais
        }

        return render(request, 'dp_quadro_vagas_app/frm_analise_vagas.html', context)

    def post(self, request):
        cod_vaga_ad_frm = request.POST['cod_vaga_ad']
        cod_projeto_frm = request.POST['cod_projeto']
        periodo_vig = request.POST['periodo_vig']
        mes_frm = periodo_vig.split("-")[1]
        ano_frm = periodo_vig.split("-")[0]
        quinzena_frm = request.POST['quinzena']

        obj_vaga = None
        obj_proj = Projeto.objects.get(pk=cod_projeto_frm)
        if cod_vaga_ad_frm == 0:
            obj_vaga = Vagas_adicionais(
                ano=ano_frm,
                mes=mes_frm,
                quinzena=quinzena_frm,
                cod_projeto=obj_proj,
            )
            obj_param.save()
            msg = 'Buscando dados'

        data = dict()
        data = {
            'msg': msg,
            'filial': obj_proj.cod_filial
        }

        return JsonResponse(data, safe=False)

class Frm_Carrega_Projeto_View(View):

    def get(self, request):
        cod_filial_frm = request.GET['cod_filial']

        filial = Filial.objects.get(pk=cod_filial_frm)

        lista_proj = list(Projeto.objects.filter(cod_filial=filial).values('cod_projeto', 'desc_proj' ))

        data = dict()
        data = {
            'lista_proj': lista_proj
        }
        return JsonResponse(data)
        print('Teste')
        print(lista_proj)