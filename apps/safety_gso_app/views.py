from datetime import datetime, date

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado
from apps.safety_gsdpq_app.models import Gabarito_GSDPQ
from apps.safety_gso_app.models import Gabarito_GSO
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Item_Check
from apps.safety_login_colaboradores_app.models import Colaborador


class Form_Gerar_Check_Gso(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        nome_colaborador = colaborador.nome_colaborador
        filial_usuario = Filial.objects.get(pk=colaborador.cod_filial)

        str_options_select_unidade = ''
        if colaborador.perfil_usu == 'G':
            data_atual = datetime.now()
            check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=8,
                                                             cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                                   data_atual.month,
                                                                                                   data_atual.day),
                                                             cod_check__data_inicio__lte=date(data_atual.year,
                                                                                              data_atual.month,
                                                                                              data_atual.day)).order_by(
                '-cod_check__data_desativacao')

            filiais_transporte_pessoas = Filial.objects.filter(cod_empresa=12, cod_filial__in=[34, 57, 89])
            filiais = Filial.objects.filter(cod_empresa=filial_usuario.cod_empresa,
                                            cod_filial__in=check_ativo.values('cod_filial').distinct())

            if filial_usuario.cod_empresa.cod_empresa == 12 and filial_usuario.cod_filial not in [34, 57, 89]:
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif filial_usuario.cod_empresa.cod_empresa == 12 and filial_usuario.cod_filial in [34, 57, 89]:
                print(filial_usuario.cod_filial)
                filiais_transporte_pessoas = filiais_transporte_pessoas.exclude(cod_filial=filial_usuario.cod_filial)
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif filial_usuario.cod_empresa.cod_empresa == 17:
                filiais = filiais.union(filiais_transporte_pessoas)

            for filial in filiais:
                str_options_select_unidade += f'<option value="{str(filial.cod_filial)}">{str(filial.desc_filial)}</option>'

        elif colaborador.perfil_usu == 'U':
            str_options_select_unidade += f'<option value="{filial_usuario.cod_filial}">{filial_usuario.desc_filial}</option>'
        context = {
            'cod_usuario': nome_colaborador,
            'cod_filial_usuario': filial_usuario.desc_filial,
            'options_select_unidade': str_options_select_unidade
        }
        return render(request, 'safety_gso_app/gso_form_gerar_check.html', context)

    @csrf_exempt
    def post(self, request):
        filial_colaborador = request.POST['unidade_avaliado_gso']
        cod_motorista_avaliado_gso = request.POST['cod_motorista_avaliado_gso']
        placa_onibus = request.POST['placa_onibus_gso']

        colaborador = Colaborador.objects.filter(cod_colaborador=cod_motorista_avaliado_gso).first()

        cod_colaborador = request.session['cod_colaborador']
        colaborador_envio = Colaborador.objects.filter(pk=cod_colaborador).first()

        data_atual = datetime.now()
        check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=8, cod_filial=colaborador.cod_filial,
                                                         cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                               data_atual.month,
                                                                                               data_atual.day),
                                                         cod_check__data_inicio__lte=date(data_atual.year,
                                                                                          data_atual.month,
                                                                                          data_atual.day)).order_by(
            '-cod_check__data_desativacao').first()

        if (check_ativo == None):
            return HttpResponse('Não há check ativo atualmente para essa filial', status=404)

        check_aplicado = Check_Aplicado(
            cod_filial=filial_colaborador,
            cod_colaborador_aplicante=colaborador_envio,
            cod_colaborador_avaliado=colaborador,
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
        for item in lista_itens:
            desc_resposta_botao = ''
            if item.tipo_resposta == 1 or item.tipo_resposta == '1':
                desc_resposta_botao = 'OK/NOK'.split('/')
            if item.tipo_resposta == 3 or item.tipo_resposta == '3':
                desc_resposta_botao = 'SIM/NÃO'.split('/')
            if item.tipo_resposta == 4 or item.tipo_resposta == '4':
                desc_resposta_botao = 'PRÓPRIO/COMPANHIA'.split('/')
            if item.tipo_resposta == 5 or item.tipo_resposta == '5':
                desc_resposta_botao = 'OK/NA/NOK'.split('/')
            if item.tipo_resposta == 6 or item.tipo_resposta == '6':
                desc_resposta_botao = 'OTIMO/BOM/REGULAR/DANIFICADO'.split('/')

            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item,
                                     'desc_resposta': desc_resposta_botao, 'obrigatorio': item.obrigatorio})

        check_cabecalho = Gabarito_GSO(
            placa_onibus=placa_onibus,
            cod_check_aplicado=check_aplicado,
        )
        check_cabecalho.save()

        context = {
            'lista_itens': lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_check_aplicado,
            'flag_gso': True
        }
        return render(request, 'safety_checks_aplicados_app/preencher_form_check.html', context)
