from django.shortcuts import render, redirect
from django.views import View

from apps.estrut_org_app.models import Filial
from apps.home_app.views import Index_View
from apps.usuario_app.models import Usuario, Usu_Menu
from proj_portal_operacional.settings import VERSAO_PORTAL

class Menu_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        menu_usuario = Usu_Menu.objects.filter(cod_usu=obj_usuario_sessao, status_usu_menu='A',
                                               cod_menu__pai_menu=0).order_by('cod_menu')
        sub_menu_usuario = Usu_Menu.objects.filter(cod_usu=obj_usuario_sessao, status_usu_menu='A',
                                                   cod_menu__pai_menu__gt=0).order_by('cod_menu__cod_menu')

        lista_filiais = Filial.objects.filter(cod_empresa=obj_usuario_sessao.cod_filial.cod_empresa,
                                              cod_reduzido__isnull=False)
        str_bg = ''
        cor_emp_hex = ''
        if obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa == 12:
            str_bg = 'background.jpg'
            cor_emp_hex = '#f46424;'
        elif obj_usuario_sessao.cod_filial.cod_empresa.cod_empresa == 17:
            str_bg = 'background-deep.jpg'
            cor_emp_hex = '#3b8eed;'

        context = {
            'obj_usuario_sessao': obj_usuario_sessao,
            'menu_usuario': menu_usuario,
            'sub_menu_usuario': sub_menu_usuario,
            'lista_filiais': lista_filiais,
            'str_bg': str_bg,
            'cor_emp_hex': cor_emp_hex,
            'VERSAO_PORTAL': VERSAO_PORTAL,
        }
        return render(request, 'menu_app/main_menu.html', context)




class Form_Logout_View(View):
    def get(self, request):
        return redirect('index')

