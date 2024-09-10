from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.freightech_remunerado_qlp_app.importador_plan_freitech import Importador_Plan_Freightech
from apps.freightech_remunerado_qlp_app.models import Plan_Remunerada_Freightech
from apps.usuario_app.models import Usuario


# Create your views here.

class Frm_Importa_Plan_Remunerado_Freightech_View(View):
    def get(self, request):
        return render(request, 'freightech_remunerado_qlp_app/frm_importa_plan_freightech.html')

    def post(self, request):
        plan_rem_frm = request.FILES['file']
        tipo_planilha_frm = request.POST['tipo_planilha']

        cod_usu_session = request.session['cod_usuario_logado']
        obj_usu_logado = Usuario.objects.filter(cod_usu=cod_usu_session).first()
        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d/%m/%Y')
        hota_atual = data_hora_atual.strftime('%H:%M:%S')

        caminho_arq_importado = 'docs/plan_rem_freightech/'  + str(plan_rem_frm.name).replace('.xlsx', '') + '_' + \
                                obj_usu_logado.login_usu.replace('.', '_') + '_' + str(data_atual_dd_mm_yyyy).replace('/', '_') \
                                + '_' + str(hota_atual).replace(':', '_') + '.xlsx'

        obj_arquivo = Plan_Remunerada_Freightech(
            data_arq_imp = data_hora_atual,
            desc_layout_arq = tipo_planilha_frm,
            nome_arq_original = plan_rem_frm.name,
            nome_arq_imp = caminho_arq_importado,
            cod_usu = obj_usu_logado
        )
        obj_arquivo.save()
        obj_importador = Importador_Plan_Freightech(plan_rem_frm, tipo_planilha_frm, obj_arquivo)




        data = dict()
        data = {
            'msg': 'Importação realizada com sucesso!'
        }
        return JsonResponse(data, safe=False)

