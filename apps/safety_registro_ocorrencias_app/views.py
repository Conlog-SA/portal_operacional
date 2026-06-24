from datetime import datetime, date

from django.shortcuts import render
from django.views import View

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Itens_Componentes, Layout_Check, Item_Check
from apps.safety_login_colaboradores_app.models import Colaborador
from apps.safety_registro_ocorrencias_app.models import Registro_Ocorrencia


class Frm_Gerar_Check_Registro_Ocorrencia(View):
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        nome_colaborador = colaborador.nome_colaborador
        # filial_usuario = Filial.objects.get(pk=colaborador.cod_filial)
        obj_filial_usuario = colaborador.cod_filial

        str_options_select_unidade = ''
        if colaborador.perfil_usu == 'G':
            # lista_filiais_liberadas = Libera_Filial_Check.objects.filter(cod_check__)

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
            filiais = Filial.objects.filter(cod_empresa=colaborador.cod_empresa,
                                            cod_filial__in=check_ativo.values('cod_filial').distinct())

            if colaborador.cod_empresa == 12 and obj_filial_usuario.cod_filial not in [34, 57, 89]:
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif colaborador.cod_empresa == 12 and obj_filial_usuario.cod_filial in [34, 57, 89]:
                filiais_transporte_pessoas = filiais_transporte_pessoas.exclude(cod_filial=obj_filial_usuario.cod_filial)
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif colaborador.cod_empresa == 17:
                filiais = filiais.union(filiais_transporte_pessoas)

            for filial in filiais:
                str_options_select_unidade += f'<option value="{str(filial.cod_filial)}">{str(filial.desc_filial)}</option>'
        elif colaborador.perfil_usu == 'U' or colaborador.perfil_usu == 'V':
            str_options_select_unidade += f'<option selected value="{obj_filial_usuario.cod_filial}">{obj_filial_usuario.desc_filial}</option>'

        list_itens_campo_local_ocorrencia = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=668, cod_empresa=colaborador.cod_empresa)
        list_itens_campo_atividade = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=683,
                                                                             cod_empresa=colaborador.cod_empresa)
        list_itens_campo_natureza = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=698,
                                                                      cod_empresa=colaborador.cod_empresa)
        list_itens_campo_causa = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=714,
                                                                     cod_empresa=colaborador.cod_empresa)

        cor_empresa = '#f46424 !important'
        if colaborador.cod_empresa == 17:
            cor_empresa = '#3b8eed !important'


        context = {
            'cod_usuario': nome_colaborador,
            'cor_empresa': cor_empresa,
            'cod_filial_usuario': obj_filial_usuario.desc_filial,
            'options_select_unidade': str_options_select_unidade,
            'list_itens_campo_local_ocorrencia': list_itens_campo_local_ocorrencia,
            'list_itens_campo_atividade': list_itens_campo_atividade,
            'list_itens_campo_natureza': list_itens_campo_natureza,
            'list_itens_campo_causa': list_itens_campo_causa
        }
        return render(request, 'safety_registro_ocorrencias_app/frm_check_registro_ocorrencias.html', context)

    def post(self, request):
        cod_unidade_frm = request.POST['cod_unidade']
        cod_negocio_frm = request.POST['cod_negocio']
        cod_tipo_relato_frm = request.POST['cod_tipo_relato']
        nome_empresa_envolvida_frm = request.POST['nome_empresa_envolvida']
        turno_frm = request.POST['turno']
        cod_nexo_frm = request.POST['cod_nexo']
        cod_local_ocorrencia_frm = request.POST['cod_local_ocorrencia']
        area_detalhada_frm = request.POST['area_detalhada']
        cod_atividade_frm = request.POST['cod_atividade']
        cod_natureza_frm = request.POST['cod_natureza']
        dt_reg_ocorencia_frm = request.POST['dt_reg_ocorencia']
        hr_reg_ocorencia_frm = request.POST['hr_reg_ocorencia']
        classificacao_ocorrencia_frm = request.POST['classificacao_ocorrencia']
        risco_real_frm = request.POST['risco_real']
        causa_frm = request.POST['causa']
        dt_ocorrencia_str = dt_reg_ocorencia_frm + ' ' + hr_reg_ocorencia_frm
        dt_ocorrencia_date = datetime.strptime(dt_ocorrencia_str, "%Y-%m-%d %H:%M")

        cod_colaborador_logado = request.session['cod_colaborador']
        obj_colaborador_logado = Colaborador.objects.get(cod_colaborador=cod_colaborador_logado)

        data_atual = datetime.now()
        obj_filial = Filial.objects.get(pk=cod_unidade_frm)
        obj_check = Layout_Check.objects.get(pk=17)
        obj_check_aplicado = Check_Aplicado(
            cod_filial=obj_filial,
            cod_colaborador_aplicante=obj_colaborador_logado,
            cod_colaborador_avaliado=None,
            data_registro=data_atual,
            cod_layout_check=obj_check
        )
        obj_check_aplicado.save()
        obj_check_reg_ocor = Registro_Ocorrencia(
            data_ocorrencia=dt_ocorrencia_date,
            cod_negocio=cod_negocio_frm,
            cod_tipo=cod_tipo_relato_frm,
            nome_empresa_envolvida=nome_empresa_envolvida_frm,
            turno=turno_frm,
            cod_nexo=cod_nexo_frm,
            cod_classificacao=classificacao_ocorrencia_frm,
            cod_risco_real=risco_real_frm,
            cod_local_ocorrencia=Itens_Componentes.objects.get(pk=cod_local_ocorrencia_frm),
            area_detalhada=area_detalhada_frm,
            cod_atividade=Itens_Componentes.objects.get(pk=cod_atividade_frm),
            cod_natrueza=Itens_Componentes.objects.get(pk=cod_natureza_frm),
            causa=causa_frm,
            cod_check_aplicado=obj_check_aplicado
        )
        obj_check_reg_ocor.save()

        lista_itens = Item_Check.objects.filter(cod_check__cod_check=17,
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
                                     'desc_resposta': desc_resposta_botao, 'obrigatorio': item.obrigatorio})

        cor_empresa = '#f46424 !important'
        if obj_colaborador_logado.cod_empresa == 17:
            cor_empresa = '#3b8eed !important'

        context = {
            'lista_itens': lista_itens_dict,
            'cod_check_aplicado': obj_check_aplicado.cod_check_aplicado,
            'cor_empresa': cor_empresa
        }
        return render(request, 'safety_checks_aplicados_app/preencher_form_check.html', context)