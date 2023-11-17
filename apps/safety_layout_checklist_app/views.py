from django.shortcuts import render
from django.views import View
# Create your views here.

class Form_Seguranca_Check(View):
    def get(self,request):
        return render(request,'safety_layout_checklist_app/form_cad_layout_checklist.html')