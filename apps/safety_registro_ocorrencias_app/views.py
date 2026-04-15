from datetime import datetime, date

from django.shortcuts import render
from django.views import View

from apps.estrut_org_app.models import Filial
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Itens_Componentes
from apps.safety_login_colaboradores_app.models import Colaborador


class Frm_Ocorrencia_Check(View):
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        nome_colaborador = colaborador.nome_colaborador
        # filial_usuario = Filial.objects.get(pk=colaborador.cod_filial)
        filial_usuario = colaborador.cod_filial

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
            filiais = Filial.objects.filter(cod_empresa=filial_usuario.cod_empresa,
                                            cod_filial__in=check_ativo.values('cod_filial').distinct())

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

        list_itens_campo_local_ocorrencia = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=668, cod_filial=filial_usuario.cod_filial)
        list_itens_campo_atividade = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=683,
                                                                             cod_filial=filial_usuario.cod_filial)
        list_itens_campo_natureza = Itens_Componentes.objects.filter(tipo_check=17, cod_pai=698,
                                                                      cod_filial=filial_usuario.cod_filial)

        context = {
            'cod_usuario': nome_colaborador,
            'cod_filial_usuario': filial_usuario.desc_filial,
            'options_select_unidade': str_options_select_unidade,
            'list_itens_campo_local_ocorrencia': list_itens_campo_local_ocorrencia,
            'list_itens_campo_atividade': list_itens_campo_atividade,
            'list_itens_campo_natureza': list_itens_campo_natureza
        }
        return render('safety_registro_ocorrencias_app/ocorrencias_frm_check.html')
