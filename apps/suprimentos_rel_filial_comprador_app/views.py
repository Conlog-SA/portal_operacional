from django.http import JsonResponse, Http404
from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.views import View

from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario
from apps.suprimentos_rel_filial_comprador_app.models import Relacao_Filial_Comprador


class Form_Cad_Rel_Filial_Comprador_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        lista_filiais = Filial.objects.all()
        lista_usuarios = Usuario.objects.filter(sala='SPR', data_desativacao__isnull=True)
        lista_filial_comprador = Relacao_Filial_Comprador.objects.all()

        for reg in lista_filial_comprador:
            reg.data_ini = reg.data_ini.strftime('%d-%m-%Y')
            if reg.data_fim != None:
                reg.data_fim = reg.data_fim.strftime('%d-%m-%Y')

        context = {
            'lista_filiais': lista_filiais,
            'lista_usuarios': lista_usuarios,
            'lista_filial_comprador': lista_filial_comprador,
            'desc_menu_principal': 'Cadastro Filial x Comprador',
            'id_menu_pai': 45,
            'obj_usuario_logado': obj_usuario_logado

        }
        return render(request, 'suprimentos_rel_filial_comprador_app/form_cad_rel_filial_comprador.html', context)


class Cad_Rel_Filial_Comprador_View(View):
    def get_object(self, pk):
        try:
            return Relacao_Filial_Comprador.objects.get(pk=pk)
        except:
            raise Http404

    def post(self, request):
        cod_filial = request.POST['cod_filial']
        cod_usuario = request.POST['cod_usuario']
        data_ativacao = request.POST['data_ativacao']
        data_desativacao = request.POST['data_desativacao']

        data_ativacao_vigencia_YYYY_MM_DD = data_ativacao
        data_desativacao_vigencia_YYYY_MM_DD = None
        if data_desativacao != '':
            data_desativacao_vigencia_YYYY_MM_DD = data_desativacao


        obj_filial = Filial.objects.filter(cod_filial=cod_filial).first()
        obj_usuario = Usuario.objects.filter(cod_usu=cod_usuario).first()
        obj_filial_comprador = Relacao_Filial_Comprador(
            cod_filial=obj_filial,
            cod_usu=obj_usuario,
            data_ini=data_ativacao_vigencia_YYYY_MM_DD,
            data_fim=data_desativacao_vigencia_YYYY_MM_DD
        )
        obj_filial_comprador.save()
        msg='Registro salvo com sucesso!'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def get(self, request):
        cod_filial_comprador = request.GET['cod_reg_filial_comprador']
        data_desativacao = request.GET['data_desativacao']

        obj_filial_comprador = Relacao_Filial_Comprador.objects.filter(cod_rel_filial_comprador=cod_filial_comprador).first()
        obj_filial_comprador.data_fim = data_desativacao
        obj_filial_comprador.save(update_fields=['data_fim'])
        msg = 'Comprador será desativado em ' + str(data_desativacao)

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Table_Filial_Compradores_View(View):
    def get(self, request):
        lista_filial_comprador = list(Relacao_Filial_Comprador.objects.all()
                                      .values('cod_rel_filial_comprador', 'cod_filial__desc_filial',
                                              'cod_usu__nome_usu', 'data_ini', 'data_fim'))

        data = dict()
        data = {
            'lista_filial_comprador': lista_filial_comprador
        }
        return JsonResponse(data, safe=False)


