from datetime import datetime, date

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Colaborador, Check_Aplicado, Item_Check_Aplicados, \
    Item_Fotos_Texto_Check_Aplicado
from apps.safety_gab_op_emp_app.models import Empilhadeira, Gabarito_Operacional_Emp
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Item_Check
from apps.safety_pci_app.models import Check_Pci
from proj_portal_operacional.settings import BASE_DIR


# Create your views here.
class Form_Gerar_Check_Pci(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)

        filial_colaborador = Filial.objects.get(pk=colaborador.cod_filial)
        str_options_select_unidade = ''
        if colaborador.perfil_usu == 'G':

            data_atual = datetime.now()
            check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=11,
                                                             cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                                   data_atual.month,
                                                                                                   data_atual.day),
                                                             cod_check__data_inicio__lte=date(data_atual.year,
                                                                                              data_atual.month,
                                                                                              data_atual.day)).order_by(
                '-cod_check__data_desativacao')

            lista_filiais = check_ativo.values('cod_filial__cod_filial', 'cod_filial__desc_filial').distinct()
            str_options_select_unidade = ''
            for filial in lista_filiais:
                str_options_select_unidade += f'<option value="{str(filial["cod_filial__cod_filial"])}">{str(filial["cod_filial__desc_filial"])}</option>'

        elif colaborador.perfil_usu == 'U':
            str_options_select_unidade += f'<option value="{filial_colaborador.cod_filial}">{filial_colaborador.desc_filial}</option>'

        context = {
            'options_select_unidade': str_options_select_unidade,
        }
        return render(request, 'safety_pci_app/pci_form_gerar_check.html', context)

    def post(self, request):
        cod_filial = request.POST['filial']
        cod_item = request.POST['cod_item']
        local = request.POST['local']

        cod_colaborador_envio = request.session['cod_colaborador']
        colaborador_envio = Colaborador.objects.filter(pk=cod_colaborador_envio).first()
        #cod_filial_usuario_sessao = colaborador_envio.cod_filial

        #filial = Filial.objects.filter(pk=cod_filial).first()

        data_atual = datetime.now()
        check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=11, cod_filial=cod_filial,
                                                         cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                               data_atual.month,
                                                                                               data_atual.day),
                                                         cod_check__data_inicio__lte=date(data_atual.year,
                                                                                          data_atual.month,
                                                                                          data_atual.day)).order_by(
            '-cod_check__data_desativacao').first()

        if (check_ativo == None):
            return HttpResponse('Não há check de PCI ativo atualmente para essa filial', status=404)

        check_aplicado = Check_Aplicado(
            cod_filial=cod_filial,
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

        lista_itens_hit_db = list(lista_itens)
        lista_itens_itens_pci = [item for item in lista_itens_hit_db if item.tipo_item == 2]
        categoria_item_pci = lista_itens_itens_pci[int(cod_item)-1]
        if int(cod_item) == len(lista_itens_itens_pci):
            itens_categoria_item_pci = lista_itens_hit_db[categoria_item_pci.ordem_item-1:]
        else:
            prox_categoria_item_pci = lista_itens_itens_pci[int(cod_item)]
            itens_categoria_item_pci = lista_itens_hit_db[categoria_item_pci.ordem_item-1:prox_categoria_item_pci.ordem_item-1]

        print(itens_categoria_item_pci)

        lista_itens_dict = []
        str_itens_obrigatorios = []

        for item in itens_categoria_item_pci:
            desc_resposta_botao = ''
            if item.tipo_resposta == 1 or item.tipo_resposta == '1':
                desc_resposta_botao = 'OK/NOK'.split('/')
            if item.tipo_resposta == 3 or item.tipo_resposta == '3':
                desc_resposta_botao = 'SIM/NÃO'.split('/')
            if item.tipo_resposta == 4 or item.tipo_resposta == '4':
                desc_resposta_botao = 'PRÓPRIO/COMPANHIA'.split('/')
            if item.tipo_resposta == 5 or item.tipo_resposta == '5':
                desc_resposta_botao = 'OK/NA/NOK'.split('/')

            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item,
                                     'desc_resposta': desc_resposta_botao, 'obrigatorio': item.obrigatorio})

        check_cabecalho = Check_Pci(
            item=cod_item,
            cod_check_aplicado=check_aplicado,
        )
        check_cabecalho.save()

        context = {
            'lista_itens' : lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_check_aplicado
        }
        return render(request, 'safety_checks_aplicados_app/preencher_form_check.html', context)