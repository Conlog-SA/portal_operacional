from datetime import date, datetime

from django.shortcuts import render
from django.views import View

from apps.safety_checks_aplicados_app.models import Check_Aplicado, Colaborador
from apps.safety_layout_checklist_app.models import Item_Check, Libera_Filial_Check
from apps.usuario_app.models import Usuario


class Items_Check(View):
    @staticmethod
    def get(cod_usuario_sessao, cod_filial_usuario_sessao, cod_filial_informado, usuario_informado):
        data_atual = datetime.now()
        usuario = Usuario.objects.get(cod_usu=cod_usuario_sessao)
        colaborador_envio = Colaborador.objects.filter(pk=cod_usuario_sessao).first()
        if colaborador_envio == None:
            colaborador = Colaborador(
                nome_colaborador=usuario.nome_usu,
                cod_filial=cod_filial_usuario_sessao
            )
            if cod_filial_informado != None:
                colaborador.filial_informada_terceiro = cod_filial_informado
            if usuario_informado != None:
                colaborador.operador_informado_terceiro = usuario_informado
        colaborador.save()
        check_aplicado = Check_Aplicado(
            cod_filial=cod_filial_usuario_sessao,
            cod_colaborador=operador,
            data_registro=data_atual,
            cod_layout_check=check_ativo.cod_check
        )
        check_aplicado.save()
        check_ativo = Libera_Filial_Check.objects.get(cod_check=check_aplicado.cod_layout_check.cod_check)
        lista_itens = Item_Check.objects.filter(cod_check__cod_check=check_ativo.cod_check.cod_check,
                                                data_desativacao__gte=date(data_atual.year, data_atual.month,
                                                                           data_atual.day),
                                                data_inicio__lte=date(data_atual.year, data_atual.month,
                                                                      data_atual.day)).order_by('ordem_item')
        lista_itens = Item_Check.objects.filter(cod_check__cod_check=check_ativo.cod_check.cod_check,
                                                data_desativacao__gte=date(data_atual.year, data_atual.month,
                                                                           data_atual.day),
                                                data_inicio__lte=date(data_atual.year, data_atual.month,
                                                                      data_atual.day)).order_by('ordem_item')
        lista_itens_dict = []
        for item in lista_itens:
            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item})

