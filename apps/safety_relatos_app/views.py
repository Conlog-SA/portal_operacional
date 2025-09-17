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
        #filial_usuario = Filial.objects.get(pk=colaborador.cod_filial)
        filial_usuario = colaborador.cod_filial

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
            filiais_transporte_pessoas = Filial.objects.filter(cod_empresa=12, cod_filial__in=[34, 57, 89])
            filiais = Filial.objects.filter(cod_empresa=filial_usuario.cod_empresa, cod_filial__in=check_ativo.values('cod_filial').distinct())

            if filial_usuario.cod_empresa.cod_empresa == 12 and filial_usuario.cod_filial not in [34, 57, 89]:
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif filial_usuario.cod_empresa.cod_empresa == 12 and filial_usuario.cod_filial in [34, 57, 89]:
                filiais_transporte_pessoas = filiais_transporte_pessoas.exclude(cod_filial=filial_usuario.cod_filial)
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif filial_usuario.cod_empresa.cod_empresa == 17:
                filiais = filiais.union(filiais_transporte_pessoas)

            for filial in filiais:
                str_options_select_unidade += f'<option value="{str(filial.cod_filial)}">{str(filial.desc_filial)}</option>'
        elif colaborador.perfil_usu == 'U' or colaborador.perfil_usu == 'V':
            str_options_select_unidade += f'<option selected value="{filial_usuario.cod_filial}">{filial_usuario.desc_filial}</option>'

        str_options_select_processo = ''
        #if filial_usuario.cod_empresa.cod_empresa == 12:
        processos = Itens_Componentes.objects.filter(tipo_check=2, campo_check=1, cod_empresa=filial_usuario.cod_empresa.cod_empresa)
        for processo in processos:
            str_options_select_processo += f'<option value="{processo.cod_componente}">{processo.desc_componente}</option>'
        if filial_usuario.cod_filial not in [34, 57, 89]:
            lista_categorias_ato_inseguro = Itens_Componentes.objects.filter(campo_check=3, cod_empresa=filial_usuario.cod_empresa.cod_empresa)
            lista_categorias_condicao_insegura = Itens_Componentes.objects.filter(campo_check=4, cod_empresa=filial_usuario.cod_empresa.cod_empresa)
            lista_categorias_comportamento_seguro = Itens_Componentes.objects.filter(campo_check=5, cod_empresa=filial_usuario.cod_empresa.cod_empresa)
        else:
            lista_categorias_ato_inseguro = Itens_Componentes.objects.filter(campo_check=3, cod_empresa=17)
            lista_categorias_condicao_insegura = Itens_Componentes.objects.filter(campo_check=4, cod_empresa=17)
            lista_categorias_comportamento_seguro = Itens_Componentes.objects.filter(campo_check=5, cod_empresa=17)

        str_options_select_local = ''
        lista_setores = []
        if filial_usuario.cod_empresa.cod_empresa == 17 or filial_usuario.cod_filial in [34, 57, 89]:
            flag_deep = True
            locais = Itens_Componentes.objects.filter(tipo_check=2, campo_check=6)
            for local in locais:
                str_options_select_local += f'<option value="{local.cod_componente}">{local.desc_componente}</option>'
        else:
            setores = Itens_Componentes.objects.filter(tipo_check=2, campo_check=7)
            for setor in setores:
                lista_setores.append({
                    'id_setor': setor.cod_componente,
                    'desc_setor': setor.desc_componente
                })
            flag_deep = False

        context = {
            'cod_usuario': nome_colaborador,
            'flag_deep': flag_deep,
            'cod_filial_usuario': filial_usuario.desc_filial,
            'options_select_unidade': str_options_select_unidade,
            'options_select_processo': str_options_select_processo,
            'options_select_local': str_options_select_local,
            'lista_categorias_ato_inseguro': lista_categorias_ato_inseguro,
            'lista_categorias_condicao_insegura': lista_categorias_condicao_insegura,
            'lista_categorias_comportamento_seguro': lista_categorias_comportamento_seguro,
            'lista_setores_relatos': lista_setores
        }

        if "Visitante" in colaborador.nome_colaborador:
            request.session['flag_deep'] = flag_deep
            return render(request, 'safety_relatos_app/relatos_form_gerar_check_visitante.html', context)

        return render(request, 'safety_relatos_app/relatos_form_gerar_check.html', context)

    @csrf_exempt
    def post(self, request):
        tipo_relato = request.POST['tipo_relato']
        situacao_envolvido = request.POST['situacao_envolvido']
        nome_relatado = request.POST['nome_relatado']
        local_relato = request.POST['local_relato']
        atividade_relato = request.POST['atividade_relato']
        processo_relato = request.POST['processo_relato']
        unidade_relato = request.POST['unidade_relato']
        categoria_ato_inseguro = request.POST['categoria_ato_inseguro']
        categoria_condicao_insegura = request.POST['categoria_condicao_insegura']
        comportamento_seguro_categoria = request.POST['comportamento_seguro_categoria']
        setor_relato = request.POST.get('setor_relato', None)
        relato_anonimo = request.POST.get('relato_anonimo', 'false')

        filial = Filial.objects.get(pk=unidade_relato)

        if categoria_ato_inseguro == '':
            categoria_ato_inseguro = None
        if categoria_condicao_insegura == '':
            categoria_condicao_insegura = None
        if comportamento_seguro_categoria == '':
            comportamento_seguro_categoria = None
        if processo_relato == '':
            processo_relato = None
        if atividade_relato == '':
            atividade_relato = None

        colaborador = None
        if situacao_envolvido == '1':
            colaborador = Colaborador.objects.get(pk=int(nome_relatado))
        elif (situacao_envolvido == '2' or situacao_envolvido == '3' or situacao_envolvido == '4') and tipo_relato != '2':

            colaborador = Colaborador(
                nome_colaborador=nome_relatado,
                cod_filial=filial,
                situacao=0
            )
            colaborador.save()

        cod_colaborador_envio = request.session['cod_colaborador']
        colaborador_envio_original = Colaborador.objects.filter(pk=cod_colaborador_envio).first()
        filial_colaborador_envio_original = colaborador_envio_original.cod_filial

        if relato_anonimo == 'false':
            colaborador_envio = colaborador_envio_original
            filial_colaborador_envio = filial_colaborador_envio_original
        elif relato_anonimo == 'true':
            filial_colaborador_envio = Filial.objects.get(pk=int(unidade_relato))
            colaborador_envio = Colaborador.objects.filter(cod_filial=filial_colaborador_envio.cod_filial,perfil_usu='V').first()
            filial_colaborador_envio = Filial.objects.get(pk=colaborador_envio.cod_filial)

        if filial_colaborador_envio.cod_empresa.cod_empresa == 17 or filial_colaborador_envio.cod_filial in [34, 57, 89]:
            local_relato = Itens_Componentes.objects.filter(pk=int(local_relato)).first().desc_componente
        elif setor_relato == None:
            return HttpResponse('Setor do relato não informado', status=404)



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
            cod_filial=filial,
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

            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item,
                                     'desc_respostas': desc_resposta_botao, 'obrigatorio': item.obrigatorio})

        if tipo_relato == '2':
            situacao_envolvido = None

        check_cabecalho = Relato(
            cod_tipo_relato=tipo_relato,
            situacao_envolvido=situacao_envolvido,
            local_relato=local_relato,
            processo_relato=processo_relato,
            atividade_relato=atividade_relato,
            cod_check_aplicado=check_aplicado,
            categoria_ato_inseguro=categoria_ato_inseguro,
            categoria_condicao_insegura=categoria_condicao_insegura,
            categoria_comportamento_seguro=comportamento_seguro_categoria,
            setor_relato=setor_relato
        )
        check_cabecalho.save()

        request.session['cod_relato'] = check_cabecalho.cod_relato_check

        context = {
            'lista_itens' : lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_check_aplicado
        }
        return render(request, 'safety_checks_aplicados_app/preencher_form_check.html', context)

class Lista_Atividades(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        #filial_colaborador = Filial.objects.filter(cod_filial=colaborador.cod_filial).first()
        filial_colaborador = colaborador.cod_filial
        if filial_colaborador.cod_empresa.cod_empresa != 12:
            data = []
            return JsonResponse(data, safe=False)
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