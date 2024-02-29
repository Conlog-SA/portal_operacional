from datetime import datetime, date

from django.shortcuts import render
from django.views import View

from apps.safety_checks_aplicados_app.models import Colaborador, Check_Aplicado
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Item_Check
from apps.safety_relatos_app.models import Relato
from apps.usuario_app.models import Usuario


class Form_Gerar_Relatos_Check(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        usuario = Usuario.objects.get(cod_usu=cod_usuario_sessao)
        nome_usuario = usuario.nome_usu

        context = {
            'cod_usuario': nome_usuario,
            'cod_filial_usuario': usuario.cod_filial.desc_filial,
        }
        return render(request, 'safety_relatos_app/relatos_form_gerar_check.html', context)

    def post(self, request):
        unidade_relato = request.POST['unidade_relato']
        tipo_relato = request.POST['tipo_relato']
        situacao_envolvido = request.POST['situacao_envolvido']
        nome_relatado = request.POST['nome_relatado']
        local_relato = request.POST['local_relato']
        atividade_relato = request.POST['atividade_relato']
        descricao_relato = request.POST['situacao_relato']
        cod_usuario_sessao = request.session['cod_usuario_logado']

        usuario = Usuario.objects.get(cod_usu=cod_usuario_sessao)
        colaborador_envio = Colaborador.objects.filter(pk=cod_usuario_sessao).first()
        cod_filial_usuario_sessao = usuario.cod_filial.cod_filial
        if colaborador_envio == None:
            colaborador_envio = Colaborador(
                nome_colaborador=usuario.nome_usu,
                cod_filial=cod_filial_usuario_sessao
                #filial_informada_terceiro=cod_filial_informado,
                #operador_informado_terceiro=usuario_informado
            )
            colaborador_envio.save()

        data_atual = datetime.now()
        check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=2, cod_filial=usuario.cod_filial,
                                                         cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                               data_atual.month,
                                                                                               data_atual.day),
                                                         cod_check__data_inicio__lte=date(data_atual.year,
                                                                                          data_atual.month,
                                                                                          data_atual.day)).order_by(
            '-cod_check__data_desativacao').first()

        check_aplicado = Check_Aplicado(
            cod_filial=cod_filial_usuario_sessao,
            cod_colaborador=colaborador_envio,
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
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item})

        check_cabecalho = Relato(
            cod_tipo_relato=tipo_relato,
            situacao_envolvido=situacao_envolvido,
            nome_relatado=nome_relatado,
            local_relato=local_relato,
            atividade_relato=atividade_relato,
            descricao_relato=descricao_relato
        )
        check_cabecalho.save()

        context = {
            'lista_itens' : lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_checks_aplicados
        }
        return render(request, 'safety_relatos_app/relatos_form_check.html', context)