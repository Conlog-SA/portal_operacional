from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import locale

from apps.conecta_as_app.models import Param_RV_AS
from apps.conecta_rota_app.models import Param_RV_Rota
from apps.conecta_rv_app.models import Verbas_Senior_RV, Param_Bonus_Devolucao_RV
from apps.conecta_vans_app.models import Param_RV_Van
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario


class Frm_Params_RV_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_filiais_calculo_rv = Filial.objects.filter(tem_calculo_rv=1)
        context = {
            'desc_menu': 'Parâmetros RV',
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_filiais_calculo_rv': lista_filiais_calculo_rv
        }
        return render(request, 'conecta_rv_app/frm_params_rv.html', context)

    def post(self, request):
        tipo_param_rv_frm = request.POST['tipo_param_rv']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        msg = ''
        if tipo_param_rv_frm == 'rota':
            cod_filial_frm = request.POST['cod_filial']
            dt_ini_frm = request.POST['dt_ini']
            dt_fim_frm = request.POST['dt_fim']
            cod_cargo_frm = request.POST['cod_cargo']
            fator_frm = request.POST['fator']
            val_caixa_frm = request.POST['val_caixa']
            val_entrega_frm = request.POST['val_entrega']
            tipo_recraga_frm = request.POST['tipo_recraga']
            val_recarga_frm = request.POST['val_recarga']

            obj_filial = Filial.objects.get(pk=cod_filial_frm)
            obj_param_rota = Param_RV_Rota(
                data_ini=dt_ini_frm,
                data_fim=dt_fim_frm,
                cargo=cod_cargo_frm,
                fator=fator_frm,
                val_caixaria=val_caixa_frm,
                val_entrega=val_entrega_frm,
                tipo_recarga=tipo_recraga_frm,
                val_recarga=val_recarga_frm,
                cod_usu=obj_usuario_sessao,
                cod_filial=obj_filial
            )
            obj_param_rota.save()
            msg = 'Registros parâmetros rota, salvo com sucesso!'
        elif tipo_param_rv_frm == 'van':
            cod_filial_frm = request.POST['cod_filial']
            dt_ini_frm = request.POST['dt_ini']
            dt_fim_frm = request.POST['dt_fim']
            cod_cargo_frm = request.POST['cod_cargo']
            fator_frm = request.POST['fator']
            val_caixa_frm = request.POST['val_caixa']
            val_entrega_frm = request.POST['val_entrega']
            tipo_recraga_frm = request.POST['tipo_recraga']
            val_recarga_frm = request.POST['val_recarga']

            obj_filial = Filial.objects.get(pk=cod_filial_frm)
            obj_param_van = Param_RV_Van(
                data_ini=dt_ini_frm,
                data_fim=dt_fim_frm,
                cargo=cod_cargo_frm,
                fator=fator_frm,
                val_caixaria=val_caixa_frm,
                val_entrega=val_entrega_frm,
                tipo_recarga=tipo_recraga_frm,
                val_recarga=val_recarga_frm,
                cod_usu=obj_usuario_sessao,
                cod_filial=obj_filial
            )
            obj_param_van.save()
            msg = 'Registros parâmetros vans, salvo com sucesso!'
        elif tipo_param_rv_frm == 'bonus_dev':
            cod_filial_frm = request.POST['cod_filial']
            dt_ini_frm = request.POST['dt_ini']
            dt_fim_frm = request.POST['dt_fim']
            cod_cargo_frm = request.POST['cod_cargo']
            perc_meta_frm = request.POST['perc_meta']
            val_param_bonus_dev_frm = request.POST['val_param_bonus_dev']

            obj_filial = Filial.objects.get(pk=cod_filial_frm)
            obj_param_bonus_dev = Param_Bonus_Devolucao_RV(
                data_ini=dt_ini_frm,
                data_fim=dt_fim_frm,
                cargo=cod_cargo_frm,
                perc_meta=perc_meta_frm,
                val_bonus_dev=val_param_bonus_dev_frm,
                cod_usu=obj_usuario_sessao,
                cod_filial=obj_filial
            )
            obj_param_bonus_dev.save()
            msg = 'Registros parâmetros bônus devolução, salvo com sucesso!'
        elif tipo_param_rv_frm == 'verba_senior':
            cod_filial_frm = request.POST['cod_filial']
            dt_ini_frm = request.POST['dt_ini']
            dt_fim_frm = request.POST['dt_fim']
            cod_tipo_verba_frm = request.POST['cod_tipo_verba']
            cod_verba_frm = request.POST['cod_verba']

            obj_filial = Filial.objects.get(pk=cod_filial_frm)
            obj_param_verba_senior = Verbas_Senior_RV(
                data_ini=dt_ini_frm,
                data_fim=dt_fim_frm,
                tipo_verba=cod_tipo_verba_frm,
                cod_verba=cod_verba_frm,
                cod_usu=obj_usuario_sessao,
                cod_filial=obj_filial
            )
            obj_param_verba_senior.save()
            msg = 'Registros parâmetros verbas Sênior, salvo com sucesso!'

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Tab_Params_RV_View(View):
    def get(self, request):
        tipo_param_rv_frm = request.GET['tipo_param_rv']
        cod_filial_frm = request.GET['cod_filial']

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        obj_filial = Filial.objects.get(pk=cod_filial_frm)
        lista_params_filial = []
        if tipo_param_rv_frm == 'rota':
            lista_params_filial = list(
                Param_RV_Rota.objects
                .filter(cod_filial=obj_filial)
                .values('cod_param_rv_rota', 'data_ini', 'data_fim', 'cargo', 'fator', 'val_caixaria',
                        'val_entrega', 'tipo_recarga', 'val_recarga'))

            for param in lista_params_filial:
                param['val_caixaria'] = locale.currency(param['val_caixaria'], grouping=True, symbol=None)
                param['val_entrega'] = locale.currency(param['val_entrega'], grouping=True, symbol=None)
                param['val_recarga'] = locale.currency(param['val_recarga'], grouping=True, symbol=None)
                param['data_ini'] = datetime.strftime(param['data_ini'], '%d-%m-%Y')
                param['data_fim'] = datetime.strftime(param['data_fim'], '%d-%m-%Y')

        elif tipo_param_rv_frm == 'as':
            lista_params_filial = list(
                Param_RV_AS.objects
                .filter(cod_filial=obj_filial)
                .values('cod_param_rv_as', 'data_ini', 'data_fim', 'cargo', 'fator', 'val_caixaria',
                        'val_entrega', 'tipo_recarga', 'val_recarga'))
        elif tipo_param_rv_frm == 'vans':
            lista_params_filial = list(
                Param_RV_Van.objects
                .filter(cod_filial=obj_filial)
                .values('cod_param_rv_van', 'data_ini', 'data_fim', 'cargo', 'fator', 'val_caixaria',
                        'val_entrega', 'tipo_recarga', 'val_recarga'))

            for param in lista_params_filial:
                param['val_caixaria'] = locale.currency(param['val_caixaria'], grouping=True, symbol=None)
                param['val_entrega'] = locale.currency(param['val_entrega'], grouping=True, symbol=None)
                param['val_recarga'] = locale.currency(param['val_recarga'], grouping=True, symbol=None)
                param['data_ini'] = datetime.strftime(param['data_ini'], '%d-%m-%Y')
                param['data_fim'] = datetime.strftime(param['data_fim'], '%d-%m-%Y')

        elif tipo_param_rv_frm == 'bonus_dev':
            lista_params_filial = list(
                Param_Bonus_Devolucao_RV.objects
                .filter(cod_filial=obj_filial)
                .values('cod_param_bonus_dev_rv', 'data_ini', 'data_fim', 'cargo', 'perc_meta', 'val_bonus_dev'))

            for param in lista_params_filial:
                param['perc_meta'] = locale.currency(param['perc_meta'], grouping=True, symbol=None)
                param['val_bonus_dev'] = locale.currency(param['val_bonus_dev'], grouping=True, symbol=None)
                param['data_ini'] = datetime.strftime(param['data_ini'], '%d-%m-%Y')
                param['data_fim'] = datetime.strftime(param['data_fim'], '%d-%m-%Y')
        elif tipo_param_rv_frm == 'verba_senior':
            lista_params_filial = list(
                Verbas_Senior_RV.objects
                .filter(cod_filial=obj_filial)
                .values('cod_verba_senior_rv', 'data_ini', 'data_fim', 'tipo_verba', 'cod_verba'))
            for param in lista_params_filial:
                param['data_ini'] = datetime.strftime(param['data_ini'], '%d-%m-%Y')
                param['data_fim'] = datetime.strftime(param['data_fim'], '%d-%m-%Y')
        data = dict()
        data = {
            'lista_params_filial' : lista_params_filial
        }
        return JsonResponse(data, safe=False)

