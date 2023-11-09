from django.shortcuts import render
from django.views import View

from apps.help_desk_app.views import ConexaoHelpDesk


class Form_Gera_Tma_TI_View(View):
    def get(self, request):
        return render(request, 'ti_tma_app/form_gera_tma_ti.html')

    def post(self, request):
        conecao_help_desk = ConexaoHelpDesk().retorna_chamados_atendidos()
