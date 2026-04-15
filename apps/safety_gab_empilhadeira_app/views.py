import os
import shutil
import sys
from datetime import datetime, date

from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Now
from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Colaborador, Check_Aplicado, Item_Check_Aplicados, \
    Item_Fotos_Texto_Check_Aplicado
from apps.safety_gab_op_emp_app.models import Empilhadeira
from apps.safety_gab_empilhadeira_app.models import Check_Empilhadeira
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Item_Check
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR


# Create your views here.
class Form_Gerar_Gab_Emp(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        nome_colaborador = colaborador.nome_colaborador

        #lista_modelos_emp = Modelo_Emp.objects.all()
        #lista_modelos_emp_dict = []
        #for modelo in lista_modelos_emp:
        #    lista_modelos_emp_dict.append({'cod_modelo_emp': modelo.cod_modelo_emp, 'desc_emp': modelo.desc_emp})
        filial_colaborador = colaborador.cod_filial
        str_options_select_unidade = ''
        if colaborador.perfil_usu == 'G':
            data_atual = datetime.now()
            check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=9,
                                                             cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                                   data_atual.month,
                                                                                                   data_atual.day),
                                                             cod_check__data_inicio__lte=date(data_atual.year,
                                                                                              data_atual.month,
                                                                                              data_atual.day)).order_by(
                '-cod_check__data_desativacao')

            lista_empilhadeiras = Empilhadeira.objects.all()
            lista_empilhadeiras = lista_empilhadeiras.exclude(cod_filial__desc_filial__contains="AMBEV")
            lista_empilhadeiras = lista_empilhadeiras.filter(cod_filial__cod_filial__in=check_ativo.values('cod_filial').distinct())

            lista_filiais = lista_empilhadeiras.values('cod_filial__cod_filial', 'cod_filial__desc_filial').distinct()
            str_options_select_unidade = ''
            for filial in lista_filiais:
                str_options_select_unidade += f'<option value="{str(filial["cod_filial__cod_filial"])}">{str(filial["cod_filial__desc_filial"])}</option>'

            '''filiais = Filial.objects.filter(cod_empresa=filial_colaborador.cod_empresa)
            filiais_com_empilhadeiras = filiais.filter(pk__in=related_filial_pks)
            filiais_com_empilhadeiras = filiais_com_empilhadeiras.exclude(desc_filial__contains="AMBEV")
            for filial in filiais_com_empilhadeiras:
                str_options_select_unidade += f'<option value="{str(filial.cod_filial)}">{str(filial.desc_filial)}</option>'''
        elif colaborador.perfil_usu == 'U':
            str_options_select_unidade += f'<option value="{filial_colaborador.cod_filial}">{filial_colaborador.desc_filial}</option>'

        cor_empresa = '#f46424 !important'
        if colaborador.cod_empresa == 17:
            cor_empresa = '#3b8eed !important'

        context = {
            'nome_operador': nome_colaborador,
            'cod_filial_operador': filial_colaborador.cod_filial,
            'options_select': str_options_select_unidade,
            'cor_empresa': cor_empresa
        }
        return render(request, 'safety_gab_empilhadeira_app/gab_empilhadeira_form_gerar_check.html', context)

    @csrf_exempt
    def post(self, request):
        filial_colaborador = request.POST['unidade_operador']

        cod_empilhadeira = request.POST['cod_empilhadeira']

        cod_colaborador = request.session['cod_colaborador']
        colaborador_envio = Colaborador.objects.filter(pk=cod_colaborador).first()
        cod_filial_usuario_sessao = colaborador_envio.cod_filial

        data_atual = datetime.now()
        check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=9, cod_filial=filial_colaborador,
                                                         cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                               data_atual.month,
                                                                                               data_atual.day),
                                                         cod_check__data_inicio__lte=date(data_atual.year,
                                                                                          data_atual.month,
                                                                                          data_atual.day)).order_by(
            '-cod_check__data_desativacao').first()

        if (check_ativo == None):
            return HttpResponse('Não há check de empilhadeiras ativo atualmente para essa filial', status=404)

        obj_filial = Filial.objects.get(pk=filial_colaborador)
        check_aplicado = Check_Aplicado(
            cod_filial=obj_filial,
            cod_colaborador_aplicante=colaborador_envio,
            data_registro=data_atual,
            cod_layout_check=check_ativo.cod_check
        )

        check_aplicado.save()

        lista_itens = Item_Check.objects.filter(cod_check__cod_check=check_ativo.cod_check.cod_check,
                                                data_desativacao__gte=date(data_atual.year, data_atual.month,
                                                                           data_atual.day),
                                                data_inicio__lte=date(data_atual.year, data_atual.month,
                                                                      data_atual.day)).order_by('ordem_item')
        lista_itens_dict = []
        str_itens_obrigatorios = []
        for item in lista_itens:
            desc_resposta_botao = ''
            if item.tipo_resposta == 1 or item.tipo_resposta == '1':
                desc_resposta_botao = 'OK/NOK'.split('/')
            if item.tipo_resposta == 3 or item.tipo_resposta == '3':
                desc_resposta_botao = 'SIM/NÃO'.split('/')
            if item.tipo_resposta == 4 or item.tipo_resposta == '4':
                desc_resposta_botao = 'PRÓPRIO/COMPANHIA'.split('/')
            if item.tipo_resposta == 5 or item.tipo_resposta == '5':
                desc_resposta_botao = 'SIM/NA/NÃO'.split('/')

            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item,
                                     'desc_resposta': desc_resposta_botao, 'obrigatorio': item.obrigatorio})

        check_cabecalho = Check_Empilhadeira(
            cod_empilhadeira=Empilhadeira.objects.get(pk=cod_empilhadeira),
            cod_check_aplicado=check_aplicado,
        )
        check_cabecalho.save()

        cor_empresa = '#f46424 !important'
        if colaborador_envio.cod_empresa == 17:
            cor_empresa = '#3b8eed !important'

        context = {
            'lista_itens' : lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_check_aplicado,
            'cor_empresa': cor_empresa
        }
        return render(request, 'safety_checks_aplicados_app/preencher_form_check.html', context)

class Colaborador_Portal(View):
    @csrf_exempt
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        usuario = Usuario.objects.get(cod_usu=cod_usuario_sessao)
        data = {
            'cod_colaborador': usuario.cod_usu,
            'cod_filial': usuario.cod_filial.cod_filial,
            'nome_colaborador': usuario.nome_usu,
            'filial_colaborador': usuario.cod_filial.desc_filial
        }
        return JsonResponse(data)

class Empilhadeiras_Filial(View):
    @csrf_exempt
    def get(self, request):
        unidade = request.GET['cod_unidade']
        filial_selecionada = Filial.objects.get(pk=unidade)
        lista_empilhadeiras = Empilhadeira.objects.filter(cod_filial=filial_selecionada.cod_filial)
        dict_empilhadeiras = []
        for emp in lista_empilhadeiras:
            dict_empilhadeiras.append({'cod_emp': emp.cod_emp, 'placa': emp.placa})
        data = {
            'lista_empilhadeiras': dict_empilhadeiras
        }
        return JsonResponse(data)


        #msg = ''
        #obj_anexo_conta_pesq
        #if obj_anexo_conta_pesq != None:
        #    arquivo_anterior_a_deletar = str(obj_anexo_conta_pesq.caminho_anexo).replace('/', '\\')
        #    os.remove(arquivo_anterior_a_deletar)
