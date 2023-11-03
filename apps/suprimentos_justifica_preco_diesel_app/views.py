from datetime import datetime
import locale

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.usuario_app.models import Usuario
from apps.suprimentos_justifica_preco_diesel_app.models import Justificativa_Preco_Diesel, Motivo_Just_Preco_Diesel


class Form_Gera_Compras_Diesel_View(View):
    def get(self, request):
        lista_filiais = ConexaoBancoBenner().retornaTabFiliaisBennerByEmpresa(12)
        context = {
            'lista_filiais': lista_filiais
        }
        return render(request, 'suprimentos_justifica_preco_diesel_app/form_justifica_preco_diesel.html', context)

class Gera_Compras_Diesel_View(View):
    def get(self, request):
        handle_filial_form = request.GET['handle_filial']
        data_ini_form = request.GET['data_ini']
        data_fim_form = request.GET['data_fim']

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        lista_compras_diesel_tab = []
        lista_compras_benner = ConexaoBancoBenner().compras_diesel(handle_filial_form, data_ini_form, data_fim_form)
        for reg in lista_compras_benner:
            reg_existente = Justificativa_Preco_Diesel.objects.filter(handle_itens_compra=reg.handle_itens_compra)\
                .first()
            img_indica_justificativa_existe = "<i class='fa-solid fa-triangle-exclamation' title='Não Justificado' style='color: #f46424;'></i>"
            status = '(Não justificado)'
            cod_motivo_just = '0'
            desc_motivo_just = ''
            desc_justificativa = ''
            if reg_existente != None:
                img_indica_justificativa_existe = (f"<i class='fa-solid fa-circle-check' style='color: #f46424;' "
                                                   f"title='{reg_existente.cod_motivo_just_preco_diesel.desc_motivo_just_preco_diesel}'></i>")
                status = '(Justificado)'
                cod_motivo_just = reg_existente.cod_motivo_just_preco_diesel.cod_motivo_just_preco_diesel
                desc_motivo_just= reg_existente.cod_motivo_just_preco_diesel.desc_motivo_just_preco_diesel
                desc_justificativa = reg_existente.desc_justificativa

            if (reg.val_unit_itens_compra - reg.val_anterior_item_compra) > 0.01:
                compra = {
                    'data_compra': datetime.strftime(reg.data_ordem_compra, '%d-%m-%Y'),
                    'num_compra': reg.numero_compra,
                    'nome_posto': reg.nome_fornecedor_compra,
                    'desc_item': reg.desc_produto_itens_compra,
                    'num_nf': reg.numero_nota_fiscal_compra,
                    'emissao_nf': datetime.strftime(reg.data_emissao_nf_compra, '%d-%m-%Y'),
                    'qtd_l': reg.qtd_compra_itens_compra,
                    'val_unit': locale.currency(reg.val_unit_itens_compra, grouping=True, symbol=None),
                    'val_tt': locale.currency(reg.val_total_itens_compra, grouping=True, symbol=None),
                    'val_unit_ant': locale.currency(reg.val_anterior_item_compra, grouping=True, symbol=None),
                    'val_dif_atual_ant': locale.currency(reg.val_unit_itens_compra - reg.val_anterior_item_compra,
                                                         grouping=True, symbol=None),
                    'val_disp_tt':
                        locale.currency(
                            (reg.val_unit_itens_compra - reg.val_anterior_item_compra) * reg.qtd_compra_itens_compra,
                            grouping=True, symbol=None
                        ),
                    'perc_disp_tt':
                        locale.currency(
                            (((reg.val_unit_itens_compra - reg.val_anterior_item_compra) * reg.qtd_compra_itens_compra) /
                            (reg.qtd_compra_itens_compra * reg.val_unit_itens_compra)) * 100,
                            grouping=True,
                            symbol=None
                        ),
                    'img_indica_justificativa_existe': img_indica_justificativa_existe,
                    'handle_itens_compra': reg.handle_itens_compra,
                    'handle_filial': reg.handle_filial_compra,
                    'nome_filial': reg.nome_filial_compra,
                    'status': status,
                    'cod_motivo_just': cod_motivo_just,
                    'desc_motivo_just': desc_motivo_just,
                    'desc_justificativa': desc_justificativa
                }
                lista_compras_diesel_tab.append(compra)

        lista_motivos_justificativa = list(Motivo_Just_Preco_Diesel.objects.all()
                                           .values('cod_motivo_just_preco_diesel', 'desc_motivo_just_preco_diesel'))
        data = dict()
        data = {
            'lista_compras_diesel_tab': lista_compras_diesel_tab,
            'lista_motivos_justificativa': lista_motivos_justificativa
        }
        return JsonResponse(data, safe=False)


class Comp_Filial_Form_Just_Preco_Diesel_View(View):
    def get(self, request):
        cod_empresa_form = request.GET['cod_empresa']
        lista_filiais_from_benner = list(ConexaoBancoBenner().retornaTabFiliaisBennerByEmpresa(cod_empresa_form))
        lista_filiais = []
        for fil in lista_filiais_from_benner:
            reg = {
                'handle': fil.HANDLE,
                'nome': fil.NOME
            }
            lista_filiais.append(reg)
        data = dict()
        data = {
            'lista_filiais': lista_filiais
        }
        return JsonResponse(data, safe=False)

class Form_Motivo_Just_Preco_Diesel_View(View):
    def post(self, request):
        desc_novo_motivo_form = request.POST['desc_novo_motivo']
        obj_motivo = Motivo_Just_Preco_Diesel(
            desc_motivo_just_preco_diesel=desc_novo_motivo_form
        ).save()
        lista_motivos = list(Motivo_Just_Preco_Diesel.objects.all()
                             .values('cod_motivo_just_preco_diesel', 'desc_motivo_just_preco_diesel'))
        data = dict()
        data = {
            'lista_motivos': lista_motivos
        }
        return JsonResponse(data, safe=False)

class Form_Justificativa_Preco_Diesel_View(View):
    def post(self, request):
        handle_item_compra_form = request.POST['handle_item_compra']
        num_compra_form = request.POST['num_compra']
        data_compra_form = request.POST['data_compra']
        val_unit_compra_form = request.POST['val_unit_compra']
        val_compra_ant_form = request.POST['val_compra_ant']
        handle_filial_form = request.POST['handle_filial']
        nome_filial_form = request.POST['nome_filial']
        desc_justificativa_form = request.POST['desc_justificativa']
        cod_motivo_justificativa_form = request.POST['cod_motivo_justificativa']
        id_usu_session = request.session['cod_usuario_logado']
        usu_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        obj_motivo_justificativa = Motivo_Just_Preco_Diesel.objects.get(pk=cod_motivo_justificativa_form)
        msg = ''
        obj_just_preco_diesel_existente = Justificativa_Preco_Diesel.objects\
            .filter(handle_itens_compra=handle_item_compra_form,handle_filial=handle_filial_form).first()
        if obj_just_preco_diesel_existente == None:
            obj_just_preco_diesel = Justificativa_Preco_Diesel(
                handle_itens_compra=handle_item_compra_form,
                num_compra=num_compra_form,
                data_compra = datetime.strptime(data_compra_form, '%d-%m-%Y'),
                val_unit_compra = val_unit_compra_form.replace('.','').replace(',','.'),
                val_compra_ant = val_compra_ant_form.replace('.','').replace(',','.'),
                handle_filial = handle_filial_form,
                nome_filial = nome_filial_form,
                desc_justificativa = desc_justificativa_form,
                cod_motivo_just_preco_diesel = obj_motivo_justificativa,
                cod_usu=usu_logado
            ).save()
            msg = 'Registro salvo com sucesso !'
        else:
            obj_just_preco_diesel_existente.desc_justificativa = desc_justificativa_form
            obj_just_preco_diesel_existente.cod_motivo_just_preco_diesel = obj_motivo_justificativa
            obj_just_preco_diesel_existente.save()
            msg = 'Registro atualizado com sucesso!'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def get(self, request):
        handle_item_compra_form = request.GET['handle_item_compra']
        handle_filial_form = request.GET['handle_filial']

        obj_just_preco_diesel_exist = Justificativa_Preco_Diesel.objects \
            .filter(handle_itens_compra=handle_item_compra_form, handle_filial=handle_filial_form).first()
        justificativa = ''
        cod_motivo = 0
        if obj_just_preco_diesel_exist != None:
            justificativa = obj_just_preco_diesel_exist.desc_justificativa
            cod_motivo = obj_just_preco_diesel_exist.cod_motivo_just_preco_diesel.cod_motivo_just_preco_diesel
        data = dict()
        data = {
            'justificativa': justificativa,
            'cod_motivo': cod_motivo
        }
        return JsonResponse(data, safe=False)



