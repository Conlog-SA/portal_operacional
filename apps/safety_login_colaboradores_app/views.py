from datetime import datetime, date

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.estrut_org_app.models import Filial
from apps.safety_layout_checklist_app.models import Libera_Filial_Check
from apps.safety_login_colaboradores_app.models import Colaborador
from apps.usuario_app.models import Usu_Menu
from proj_portal_operacional.settings import VERSAO_SAFETY


class Login_Colaborador(View):
    @csrf_exempt
    def get(self, request):
        id_visitante = request.GET.get('id_visitante')
        if id_visitante is not None:
            colaborador = Colaborador.objects.get(cod_colaborador=id_visitante)
            if "Visitante" in colaborador.nome_colaborador:
                request.session['cod_colaborador'] = id_visitante
                return redirect('relatos_check')
        context = {
            'VERSAO_SAFETY': VERSAO_SAFETY,
        }
        return render(request, 'safety_login_colaboradores_app/safe_base_container.html', context)

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
        filial_colaborador = Filial.objects.get(pk=colaborador.cod_filial)
        desc_filial_colaborador = filial_colaborador.desc_filial

        if colaborador.perfil_usu == 'V':
            context = {
                'nome_colaborador': primeiro_nome_colaborador,
                'desc_filial_colaborador': desc_filial_colaborador,
                'id_relato': request.session['cod_relato'],
                'flag_visitante': True
            }

            return render(request, 'safety_login_colaboradores_app/safe_visitante_submit.html', context)

        data_atual = datetime.now()
        str_menu_colaborador = ''
        if colaborador.perfil_usu == 'U':
            check_ativo = Libera_Filial_Check.objects.filter(cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                                   data_atual.month,
                                                                                                   data_atual.day),
                                                             cod_check__data_inicio__lte=date(data_atual.year,
                                                                                              data_atual.month,
                                                                                              data_atual.day),
                                                             cod_filial=filial_colaborador).order_by(
                '-cod_check__data_desativacao')

            if check_ativo.filter(cod_check__tipo_check=1).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-empilhadeiras" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-dolly icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Empilhadeiras</b>
                                            </div>
                                        '''
            if check_ativo.filter(cod_check__tipo_check=2).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-relatos" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-file-signature icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Relatos</b>
                                            </div>
                                        '''
            if check_ativo.filter(cod_check__tipo_check=3).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-gsdpq" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-truck icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">GSDPQ</b>
                                            </div>
                                        '''
            if check_ativo.filter(cod_check__tipo_check=4).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-blitz-trajeto-carro" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-car icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Carro</b>
                                            </div>
                                        '''
            if check_ativo.filter(cod_check__tipo_check=5).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-blitz-trajeto-moto" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-motorcycle icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Moto</b>
                                            </div>
                                        '''
            if check_ativo.filter(cod_check__tipo_check=6).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-blitz-trajeto-bicicleta" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-bicycle icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Bicicleta</b>
                                            </div>
                                        '''
            if check_ativo.filter(cod_check__tipo_check=7).first() is not None:
                str_menu_colaborador += '''
                                            <div class="safety-container-app safety-app-blitz-trajeto-outros-meios" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-road icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Outros Meios</b>
                                        </div>
                                        '''
        elif colaborador.perfil_usu == 'G':
            str_menu_colaborador += '''
                                        <div class="safety-container-app safety-app-empilhadeiras" style="margin-bottom:0.4rem">
                                            <i class="fa-solid fa-dolly icon-menu-safety" style="margin-bottom:5px"></i>
                                            <b style="color:white;">Empilhadeiras</b>
                                        </div>
                                        <div class="safety-container-app safety-app-relatos" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-file-signature icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Relatos</b>
                                        </div>
                                        <div class="safety-container-app safety-app-gsdpq" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-truck icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">GSDPQ</b>
                                        </div>
                                        <div class="safety-container-app safety-app-blitz-trajeto-carro" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-car icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Carro</b>
                                        </div>
                                        <div class="safety-container-app safety-app-blitz-trajeto-moto" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-motorcycle icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Moto</b>
                                        </div>
                                        <div class="safety-container-app safety-app-blitz-trajeto-bicicleta" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-bicycle icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Bicicleta</b>
                                        </div>
                                        <div class="safety-container-app safety-app-blitz-trajeto-outros-meios" style="margin-bottom:0.4rem">
                                                <i class="fa-solid fa-road icon-menu-safety" style="margin-bottom:5px"></i>
                                                <b style="color:white;">Blitz de Trajeto - Outros Meios</b>
                                        </div>
                                    '''

        context = {
            'nome_colaborador': primeiro_nome_colaborador,
            'desc_filial_colaborador': desc_filial_colaborador,
            'str_menu_colaborador': str_menu_colaborador,
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
        elif tipo_check == '2':
            url = 'gsdpq_check'
        elif tipo_check == '3':
            url = 'blitz_trajeto_carro_check'
        elif tipo_check == '4':
            url = 'blitz_trajeto_moto_check'
        elif tipo_check == '5':
            url = 'blitz_trajeto_bicicleta_check'
        elif tipo_check == '6':
            url = 'blitz_trajeto_outros_meios_check'
        return redirect(url)

class Lista_Colaboradores(View):
    @csrf_exempt
    def get(self, request):
        tipo_check = request.GET['tipo_check']
        cod_unidade = request.GET['cod_unidade']

        lista_colaboradores = ((Colaborador.objects.filter(cod_filial=cod_unidade, situacao=1, ))
                               .order_by('nome_colaborador'))
        #                       | Colaborador.objects.filter(cod_filial=cod_unidade,perfil_usu='T'))
        if tipo_check == '1':
            lista_colaboradores = lista_colaboradores.filter(desc_cargo__icontains='op')
            lista_colaboradores = lista_colaboradores.filter(desc_cargo__icontains='empilhadeira')
        dict_colaboradores_options = []
        for colaborador in lista_colaboradores:
            dict_colaboradores_options.append({'cod_colaborador': colaborador.cod_colaborador, 'nome_colaborador': colaborador.nome_colaborador, 'desc_cargo': colaborador.desc_cargo}) #f'<option value="{operador.cod_colaborador}">{operador.nome_colaborador}</option>'
        data = {
            'lista_colaboradores': dict_colaboradores_options
        }
        return JsonResponse(data)

class Documento_Colaborador(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.GET['cod_colaborador']

        colab_informado = Colaborador.objects.get(pk=cod_colaborador)
        cpf_colab_informado = colab_informado.cpf.zfill(11)
        return JsonResponse(cpf_colab_informado, safe=False)