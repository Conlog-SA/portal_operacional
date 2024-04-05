from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.estrut_org_app.models import Filial
from apps.safety_login_colaboradores_app.models import Colaborador
from apps.usuario_app.models import Usu_Menu


class Login_Colaborador(View):
    @csrf_exempt
    def get(self, request):
        return render(request, 'safety_login_colaboradores_app/safe_base_container.html')

    @csrf_exempt
    def post(self, request):
        flag_voltar = request.POST.get('flag_voltar', '0')
        if '1' in flag_voltar:
            return redirect('safe_main_menu')
        cpf_colaborador = request.POST['cpf_colaborador']
        data_nasc_colab = request.POST['data_nasc_colaborador']
        data_nasc_array = data_nasc_colab.split('-')
        data_nasc_colab = datetime(int(data_nasc_array[0]), int(data_nasc_array[1]), int(data_nasc_array[2]))

        colaboradores = Colaborador.objects.filter(cpf=cpf_colaborador, data_nascimento=data_nasc_colab)
        if colaboradores.first() != None and colaboradores.count() == 1:
            request.session['cod_colaborador'] = colaboradores.first().cod_colaborador
            return redirect('safe_main_menu')
        else:
            msg_erro = 'Colaborador não existente/cadastrado.'
        return HttpResponse(msg_erro, status=401)

class Login_Colaborador_Deep(View):
    @csrf_exempt
    def get(self, request):
        return render(request, 'safety_login_colaboradores_app/safe_base_container_deep.html')

class Menu_Safe(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(pk=cod_colaborador)
        primeiro_nome_colaborador = colaborador.nome_colaborador.split(' ')[0].upper()
        desc_filial_colaborador = Filial.objects.get(pk=colaborador.cod_filial).desc_filial
        context = {
            'nome_colaborador': primeiro_nome_colaborador,
            'desc_filial_colaborador': desc_filial_colaborador
        }
        return render(request, 'safety_login_colaboradores_app/safe_main_menu.html', context)

    @csrf_exempt
    def post(self, request):
        tipo_check = request.POST.get('tipo_check', '')

        url = ''
        if tipo_check == '999':
            return render(request, 'safety_login_colaboradores_app/form_safe_login.html')
        elif tipo_check == '0':
            url = 'empilhadeira_check'
        elif tipo_check == '1':
            url = 'relatos_check'
        return redirect(url)

class Lista_Colaboradores(View):
    @csrf_exempt
    def get(self, request):
        cod_unidade = request.GET['cod_unidade']

        lista_colaboradores = (Colaborador.objects.filter(cod_filial=cod_unidade))
        #                       | Colaborador.objects.filter(cod_filial=cod_unidade,perfil_usu='T'))
        dict_colaboradores_options = []
        for colaborador in lista_colaboradores:
            dict_colaboradores_options.append({'cod_colaborador': colaborador.cod_colaborador, 'nome_colaborador': colaborador.nome_colaborador, 'desc_cargo': colaborador.desc_cargo}) #f'<option value="{operador.cod_colaborador}">{operador.nome_colaborador}</option>'

        #if not dict_colaboradores_options:
        #    data = {
        #        'error_message': 'Não foram encontrados colaboradores para a unidade selecionada!'
        #    }
        #    return JsonResponse(data, status=404)

        #return HttpResponse(str_operadores_options)

        data = {
            'lista_colaboradores': dict_colaboradores_options
        }
        return JsonResponse(data)

class Documento_Colaborador(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.GET['cod_colaborador']

        colab_informado = Colaborador.objects.get(pk=cod_colaborador)
        cpf_colab_informado = colab_informado.cpf
        if len(cpf_colab_informado) < 11:
            cpf_colab_informado = '0' + cpf_colab_informado
        return JsonResponse(cpf_colab_informado, safe=False)