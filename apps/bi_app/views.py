from django.shortcuts import render
from django.views import View

class Form_Bi_View(View):
    def get(self, request):
        return render(request, 'bi_app/cco_entrega_documentos_bi.html')
