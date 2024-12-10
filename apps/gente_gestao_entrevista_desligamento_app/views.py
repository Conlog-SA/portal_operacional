from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta

from django.views.decorators.csrf import csrf_exempt

from apps.phishing_app import models

# Create your views here.
class Entrevista_Desligamento(View):
    def get(self, request):
        print('texto aqui!')