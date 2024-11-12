from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.estrut_org_app.models import Filial, Empresa, Projeto
from apps.menu_app.models import Menu
from apps.usuario_app.models import Usuario, Usu_Menu, Proj_Usu


class Form_Cad_Usu_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        lista_usu = Usuario.objects.all()
        lista_filiais = Filial.objects.filter(ativo=1)
        contexto = {
            'lista_usu': lista_usu,
            'lista_filiais': lista_filiais,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'usuario_app/form_cad_usuario.html', contexto)

class Usuario_View(View):
    def verifica_usu_existe(self, login_usu):
        result_usu_existe = False
        obj_usu = Usuario.objects.filter(login_usu=login_usu).first()
        if obj_usu != None:
            result_usu_existe = True
        return result_usu_existe, obj_usu

    def post(self, request):
        nome_usu_form = request.POST['nome_usu']
        habilita_usu_form = request.POST['habilita_usu']
        if habilita_usu_form == 'true':
            habilita_usu_form = 'A'
        else:
            habilita_usu_form = 'D'
        corporativo_usu_form = request.POST['corporativo_usu']
        if corporativo_usu_form == 'true':
            corporativo_usu_form = 'S'
        else:
            corporativo_usu_form = 'N'

        email_usu_form = request.POST['email_usu']
        perfil_usu_form = request.POST['perfil_usu']
        login_usu_form = request.POST['login_usu']
        cod_filial_form = request.POST['cod_filial']
        obj_filial = Filial.objects.filter(cod_filial=cod_filial_form).first()

        # verifica se o usuário já existe
        obj_usuario_pesq = Usuario.objects.filter(login_usu=login_usu_form).first()
        msg = ''
        if obj_usuario_pesq == None:
            usuario = Usuario(
                nome_usu=nome_usu_form,
                status_usu=habilita_usu_form,
                email_usu=email_usu_form,
                perfil_usu=perfil_usu_form,
                login_usu=login_usu_form,
                sala='T',
                cod_filial=obj_filial,
                corporativo=corporativo_usu_form
            )
            usuario.save()
            msg = 'Usuário cadastrado com sucesso!'
        else:
            obj_usuario_pesq.nome_usu = nome_usu_form
            obj_usuario_pesq.status_usu = habilita_usu_form
            obj_usuario_pesq.corporativo = corporativo_usu_form
            obj_usuario_pesq.email_usu = email_usu_form
            obj_usuario_pesq.perfil_usu = perfil_usu_form
            obj_usuario_pesq.login_usu = login_usu_form
            obj_usuario_pesq.cod_filial = obj_filial
            obj_usuario_pesq.save()
            msg = 'Usuário atualizado com sucesso!'

        data = dict()
        data = {
            'msg': msg,
        }
        return JsonResponse(data, safe=False)

    def get(self, request):
        list_usuario_cadastrados = list(Usuario.objects.all().values(
            'cod_usu', 'cod_filial__cod_filial', 'cod_filial__desc_filial', 'nome_usu', 'status_usu', 'data_desativacao', 'email_usu',
            'perfil_usu', 'login_usu', 'corporativo'
        ))
        data = dict()
        data = {
            'list_usuario_cadastrados': list_usuario_cadastrados
        }
        return JsonResponse(data, safe=False)

class Form_Usuario_Menus_View(View):
    def get(self, request):
        lista_usuarios_ativos = Usuario.objects.filter(status_usu='A')
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        contexto = {
            'lista_usuarios_ativos': lista_usuarios_ativos,
            'lista_filiais': lista_usuarios_ativos,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'usuario_app/form_libera_modulos.html', contexto)

class Usuario_Menu_View(View):
    def get(self, request):
        cod_usu_form = request.GET['cod_usu']
        obj_usu = Usuario.objects.get(pk=cod_usu_form)
        lista_menu = Menu.objects.filter(status_menu='A', pai_menu=0)
        lista_sub_menu = Menu.objects.filter(status_menu='A', pai_menu__gt=0)
        list_menu_form = []
        for m in lista_menu:
            menu_usu = Usu_Menu.objects.filter(cod_usu=obj_usu, cod_menu=m).first()
            status_menu = 'D'
            if menu_usu != None:
                status_menu = menu_usu.status_usu_menu
            dic_menu = {
                'cod_menu': m.cod_menu,
                'desc_menu': m.desc_menu,
                'nome_icone': m.nome_icone,
                'status_usu': status_menu
            }
            list_menu_form.append(dic_menu)
        lista_sub_menu_form = []
        for s in lista_sub_menu:
            menu_usu = Usu_Menu.objects.filter(cod_usu=obj_usu, cod_menu=s).first()
            status_menu = 'D'
            if menu_usu != None:
                status_menu = menu_usu.status_usu_menu
            dic_sub_menu = {
                'cod_sub_menu': s.cod_menu,
                'desc_sub_menu': s.desc_menu,
                'pai_menu': s.pai_menu,
                'nome_icone': s.nome_icone,
                'status_usu': status_menu
            }
            lista_sub_menu_form.append(dic_sub_menu)
        dados = dict()
        dados = {
            'list_menu_form': list_menu_form,
            'lista_sub_menu_form': lista_sub_menu_form
        }
        return JsonResponse(data=dados, safe=False)

    def post(self, request):
        cod_menu_form = request.POST['cod_menu']
        cod_usu_form = request.POST['cod_usu']
        acao_form = request.POST['status']

        # Retornando instancia de usuario e menu
        obj_usu = Usuario.objects.get(cod_usu=cod_usu_form)
        obj_menu = Menu.objects.get(cod_menu=cod_menu_form)

        obj_usu_menu = Usu_Menu.objects.filter(cod_menu=obj_menu, cod_usu=obj_usu).first()
        msg = ''
        if obj_usu_menu != None:
            obj_usu_menu.status_usu_menu = acao_form
            obj_usu_menu.save()

            if obj_menu.pai_menu == 0:
                lista_sub_menu_menu_selecionado = Usu_Menu.objects\
                    .filter(cod_usu=obj_usu, cod_menu__pai_menu=obj_menu.cod_menu)
                for sub_menu in lista_sub_menu_menu_selecionado:
                    sub_menu.status_usu_menu=acao_form
                    sub_menu.save()
                if acao_form == 'A':
                    msg = 'Módulos liberados com sucesso !'
                else:
                    msg = 'Módulos bloqueados com sucesso !'
            else:
                if acao_form == 'A':
                    msg = 'Módulo liberado com sucesso !'
                else:
                    msg = 'Módulo bloqueado com sucesso !'

        else:
            novo_registro = Usu_Menu(
                cod_usu=obj_usu,
                cod_menu=obj_menu,
                status_usu_menu=acao_form
            )
            novo_registro.save()
            if acao_form == 'A':
                msg = 'Módulo liberado com sucesso !'
            else:
                msg = 'Módulo bloqueado com sucesso !'


        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data)

class Form_Replica_Acesso_Menus_View(View):
    def post(self, request):
        cod_usu_origem_form = request.POST['cod_usu_origem']
        lista_cod_usu_string_form = request.POST['lista_cod_usu_string']


        obj_usu_origem = Usuario.objects.get(pk=cod_usu_origem_form)
        lista_acessos_usu_origem = Usu_Menu.objects.filter(cod_usu=obj_usu_origem, status_usu_menu='A')
        for c in lista_cod_usu_string_form.split(','):
            obj_usu = Usuario.objects.get(pk=c)
            for acessos in lista_acessos_usu_origem:
                '''Verifica se o usuario tem registro do acesso'''
                obj_acesso_usu = Usu_Menu.objects.filter(cod_usu=obj_usu, cod_menu=acessos.cod_menu).first()
                if obj_acesso_usu != None:
                    obj_acesso_usu.status_usu_menu = 'A'
                    obj_acesso_usu.save()
                else:
                    obj_novo_acesso = Usu_Menu(
                        cod_usu=obj_usu,
                        cod_menu=acessos.cod_menu,
                        status_usu_menu='A'
                    )
                    obj_novo_acesso.save()
        msg = 'Acessos replicados com sucesso!'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data)

class Form_Libera_Acesso_Projetos_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        lista_usuarios_ativos = Usuario.objects.filter(status_usu='A')
        lista_emp = Empresa.objects.all()
        contexto = {
            'lista_usuarios_ativos': lista_usuarios_ativos,
            'lista_emp': lista_emp,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'usuario_app/form_libera_projetos.html', contexto)

    def post(self, request):
        cod_usu_form = request.POST['cod_usu']
        lista_projetos_form = request.POST['lista_projetos']
        lista_msg = []
        obj_usuario = Usuario.objects.filter(cod_usu=cod_usu_form).first()
        obj_projeto_string = lista_projetos_form.split(',')
        for cod_proj in obj_projeto_string:
            obj_projeto = Projeto.objects.filter(cod_projeto=cod_proj).first()
            obj_proj_usu = Proj_Usu(
                cod_usu=obj_usuario,
                cod_projeto=obj_projeto,
                status_proj_usu='S',
                data_fim_proj_usu=None
            )
            obj_proj_usu_existente = Proj_Usu.objects.filter(cod_usu__cod_usu=cod_usu_form,
                                                             cod_projeto__cod_projeto=cod_proj).first()
            if obj_proj_usu_existente == None:
                obj_proj_usu.save()
                lista_msg.append('Projeto(s) liberado(s) com sucesso !')
            else:
                msg = 'Projeto ' + obj_projeto.desc_proj + ', já possui um registro para o usuário informado. Verifique!'
                lista_msg.append(msg)

        data = dict()
        data = {
            'lista_msg': lista_msg
        }
        return JsonResponse(data)



class Componente_Empresa_View(View):
    def get(self, request):
        cod_emp_form = request.GET['cod_empresa']
        obj_emp = Empresa.objects.get(pk=cod_emp_form)
        lista_filiais = list(Filial.objects.filter(cod_empresa=obj_emp, ativo=1).values('cod_filial', 'desc_filial'))
        data = dict()
        data = {
            'lista_filiais': lista_filiais
        }
        return JsonResponse(data)

class Componente_Proj_View(View):
    def get(self, request):
        lista_cod_filiais_form = request.GET['lista_cod_filiais']
        cod_empresa_form = request.GET['cod_empresa']
        lista_proj = []
        for f in lista_cod_filiais_form.split(','):
            obj_filial = Filial.objects.get(pk=f)
            lista_proj_de_f = Projeto.objects.filter(cod_filial=obj_filial, cod_empresa=cod_empresa_form)
            for p in lista_proj_de_f:
                proj = {
                    'cod_proj': p.cod_projeto,
                    'nome_proj': p.desc_proj
                }
                lista_proj.append(proj)
        data = dict()
        data = {
            'lista_proj': lista_proj
        }
        return JsonResponse(data)

class Tab_Proj_Usu_View(View):
    def get(self, request):
        cod_usu_form = request.GET['cod_usu']
        obj_usu = Usuario.objects.get(pk=cod_usu_form)

        lista_liberacoes = list(Proj_Usu.objects.filter(cod_usu=obj_usu)
                                .values('cod_proj_usu', 'cod_usu__nome_usu', 'cod_projeto__desc_proj',
                                        'cod_usu__perfil_usu',
                                        'cod_usu__corporativo', 'status_proj_usu', 'data_fim_proj_usu'))

        data = dict()
        data = {
            'lista_liberacoes': lista_liberacoes
        }
        return JsonResponse(data)

    def post(self, request):
        cod_proj_usu_form = request.POST['cod_proj_usu']
        valor_bloqueio_form = request.POST['valor_bloqueio']

        obj_proj_usu = Proj_Usu.objects.get(pk=cod_proj_usu_form)
        obj_proj_usu.status_proj_usu = valor_bloqueio_form
        obj_proj_usu.save()
        msg = ''
        if valor_bloqueio_form == 'N':
            msg = 'Projeto bloquado!'
        else:
            msg = 'Projeto liberado!'
        data = dict()
        data = {
            'msg': msg,
            'cod_usu': obj_proj_usu.cod_usu.cod_usu
        }
        return JsonResponse(data)








