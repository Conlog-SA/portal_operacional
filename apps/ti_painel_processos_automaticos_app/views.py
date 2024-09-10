from django.shortcuts import render
from django.views import View


class Frm_Painel_Processos_Automaticos_View(View):
    def get(self, request):
        context = {
            'desc_menu': 'Painel de Controle dos Processos - TI'
        }

        return render(request, 'ti_painel_processos_automaticos_app/frm_painel_processos_automaticos.html', context)

