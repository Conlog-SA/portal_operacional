from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class Frm_Importa_Plan_Remunerado_Freightech_View(View):
    def get(self, request):
        return render(request, 'freightech_remunerado_qlp_app/frm_importa_plan_freightech.html')

    def post(self, request):
        plan_rem_frm = request.FILES['file']
        tipo_planilha_frm = request.POST['tipo_planilha']

        data = dict()
        data = {
            'tipo_planilha_frm': tipo_planilha_frm
        }
        return JsonResponse(data, safe=False)

