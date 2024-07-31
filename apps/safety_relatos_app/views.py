from datetime import datetime, date

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Colaborador, Check_Aplicado
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Item_Check, Itens_Componentes
from apps.safety_relatos_app.models import Relato
from apps.usuario_app.models import Usuario


class Form_Gerar_Relatos_Check(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        nome_colaborador = colaborador.nome_colaborador
        filial_usuario = Filial.objects.get(pk=colaborador.cod_filial)

        str_options_select_unidade = ''
        if colaborador.perfil_usu == 'G':
            #lista_filiais_liberadas = Libera_Filial_Check.objects.filter(cod_check__)

            data_atual = datetime.now()
            check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=2,
                                                             cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                                   data_atual.month,
                                                                                                   data_atual.day),
                                                             cod_check__data_inicio__lte=date(data_atual.year,
                                                                                              data_atual.month,
                                                                                              data_atual.day)).order_by(
                '-cod_check__data_desativacao')

            filiais = Filial.objects.filter(cod_empresa=filial_usuario.cod_empresa, cod_filial__in=check_ativo.values('cod_filial').distinct())

            for filial in filiais:
                str_options_select_unidade += f'<option value="{str(filial.cod_filial)}">{str(filial.desc_filial)}</option>'
        elif colaborador.perfil_usu == 'U':
            str_options_select_unidade += f'<option selected value="{filial_usuario.cod_filial}">{filial_usuario.desc_filial}</option>'

        str_options_select_processo = ''
        #if filial_usuario.cod_empresa.cod_empresa == 12:
        processos = Itens_Componentes.objects.filter(tipo_check=2, campo_check=1)
        for processo in processos:
            str_options_select_processo += f'<option value="{processo.cod_componente}">{processo.desc_componente}</option>'
        lista_categorias_ato_inseguro = Itens_Componentes.objects.filter(campo_check=3)

        context = {
            'cod_usuario': nome_colaborador,
            'cod_filial_usuario': filial_usuario.desc_filial,
            'options_select_unidade': str_options_select_unidade,
            'options_select_processo': str_options_select_processo,
            'lista_categorias': lista_categorias_ato_inseguro
        }

        if "Visitante" in colaborador.nome_colaborador:
            return render(request, 'safety_relatos_app/relatos_form_gerar_check_visitante.html', context)

        return render(request, 'safety_relatos_app/relatos_form_gerar_check.html', context)

    @csrf_exempt
    def post(self, request):
        tipo_relato = request.POST['tipo_relato']
        situacao_envolvido = request.POST['situacao_envolvido']
        nome_relatado = request.POST['nome_relatado']
        local_relato = request.POST['local_relato']
        turno_relato = request.POST['turno_relato']
        atividade_relato = request.POST['atividade_relato']
        processo_relato = request.POST['processo_relato']
        unidade_relato = request.POST['unidade_relato']
        categoria_relato = request.POST['categoria_relato']

        if categoria_relato == '':
            categoria_relato = None

        colaborador = None
        if situacao_envolvido == '1':
            colaborador = Colaborador.objects.get(pk=int(nome_relatado))

        elif situacao_envolvido == '2' or situacao_envolvido == '3' or situacao_envolvido == '4':

            colaborador = Colaborador(
                nome_colaborador=nome_relatado,
                cod_filial=unidade_relato,
                situacao=0
            )
            colaborador.save()

        cod_colaborador = request.session['cod_colaborador']
        colaborador_envio = Colaborador.objects.filter(pk=cod_colaborador).first()
        filial = Filial.objects.get(pk=unidade_relato)

        data_atual = datetime.now()
        check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=2, cod_filial=filial,
                                                         cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                               data_atual.month,
                                                                                               data_atual.day),
                                                         cod_check__data_inicio__lte=date(data_atual.year,
                                                                                          data_atual.month,
                                                                                          data_atual.day)).order_by(
            '-cod_check__data_desativacao').first()

        if (check_ativo == None):
            return HttpResponse('Não há check de relatos ativo atualmente para essa filial', status=404)

        check_aplicado = Check_Aplicado(
            cod_filial=unidade_relato,
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
            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item,
                                     'obrigatorio': item.obrigatorio})

        check_cabecalho = Relato(
            cod_tipo_relato=tipo_relato,
            situacao_envolvido=situacao_envolvido,
            local_relato=local_relato,
            turno_relato=turno_relato,
            processo_relato=processo_relato,
            atividade_relato=atividade_relato,
            cod_check_aplicado=check_aplicado,
            categoria=categoria_relato
        )
        check_cabecalho.save()

        context = {
            'lista_itens' : lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_check_aplicado
        }
        return render(request, 'safety_relatos_app/relatos_form_check.html', context)

class Lista_Atividades(View):
    @csrf_exempt
    def get(self, request):
        cod_processo = request.GET['cod_processo']

        lista_atividades = Itens_Componentes.objects.filter(cod_pai=cod_processo)
        dict_atividades_options = []
        for atividade in lista_atividades:
            dict_atividades_options.append({'cod_atividade': atividade.cod_componente, 'desc_atividade': atividade.desc_componente}) #f'<option value="{operador.cod_colaborador}">{operador.nome_colaborador}</option>'

        #return HttpResponse(str_operadores_options)

        data = {
            'lista_atividades': dict_atividades_options
        }
        return JsonResponse(data)