from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.estrut_org_app.models import Filial



class Frm_Analise_Vagas_View(View):
    def get(self, request):
        filiais = list((Filial.objects.filter(desc_filial__contains="AMBEV", cod_empresa=12)))
        context = {
            'filiais': filiais
        }

        return render(request, 'dp_quadro_vagas_app/frm_analise_vagas.html', context)

