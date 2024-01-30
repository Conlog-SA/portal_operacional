from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
class Form_Gab_Emp(View):
    def get(self, request):
        return render(request, 'safety_gab_op_emp_app/form_gab_op_emp.html')
