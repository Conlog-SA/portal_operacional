from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado
from apps.safety_layout_checklist_app.models import Layout_Check, Libera_Filial_Check, Item_Check, Itens_Componentes
from apps.safety_login_colaboradores_app.models import Colaborador
from apps.usuario_app.models import Usuario


# Create your views here.

class Form_Seguranca_Check(View):
    @csrf_exempt
    def get(self, request):
        lista_tipos = {'1': 'Empilhadeiras', '2': 'Relatos', '3': 'GSDPQ'}
        cod_usuario_sessao = request.session['cod_usuario_logado']
        usuario = Usuario.objects.get(pk=cod_usuario_sessao)
        flag_corporativo = 0
        if usuario.corporativo == 'S':
            lista_filiais = Filial.objects.filter(cod_empresa=usuario.cod_filial.cod_empresa)
            #lista_filiais = Filial.objects.all()
            flag_corporativo = 1
        elif usuario.corporativo == 'N':
            lista_filiais = [usuario.cod_filial]

        '''for filial in lista_filiais:
            lista_filiais_dict.append({filial.cod_filial, filial.desc_filial})
        print(lista_filiais_dict)'''
        contexto = {
            'lista_tipos': lista_tipos,
            'lista_filiais' : lista_filiais,
            'flag_corporativo': flag_corporativo
        }
        return render(request,'safety_layout_checklist_app/form_cad_layout_checklist.html', contexto)

class Lista_Check(View):
    @csrf_exempt
    def get(self, request):
        cod_tipo = request.GET['cod_tipo']
        cod_usuario_sessao = request.session['cod_usuario_logado']
        usuario = Usuario.objects.get(pk=cod_usuario_sessao)
        if usuario.corporativo == 'S':
            lista_checks = list(Layout_Check.objects.filter(tipo_check=cod_tipo))
        elif usuario.corporativo == 'N':
            checks_liberados_filial_usu = Libera_Filial_Check.objects.filter(cod_filial=usuario.cod_filial)

            lista_checks = Layout_Check.objects.filter(tipo_check=cod_tipo,cod_usu__cod_filial=usuario.cod_filial)
            lista_checks = lista_checks.union(Layout_Check.objects.filter(cod_check__in=checks_liberados_filial_usu))

        lista_checks_dict = []
        for check in lista_checks:
            lista_checks_dict.append({'cod_check': check.cod_check, 'desc_check': check.desc_check})
        data = {
            'lista_checks': lista_checks_dict
        }
        return JsonResponse(data)

class Form_Cadastro_Check(View):
    @csrf_exempt
    def get(self, request):
        cod_check = request.GET['cod_check']
        check_selecionado = Layout_Check.objects.get(pk=cod_check)
        verifica_check_aplicado_existente = Check_Aplicado.objects.filter(cod_layout_check=check_selecionado).first()
        flag_aplicado = None
        if verifica_check_aplicado_existente == None:
            flag_aplicado = False
        else:
            flag_aplicado = True

        data = {
            'check_selecionado': {
                'desc_check': check_selecionado.desc_check,
                'versao': check_selecionado.versao,
                'data_inicio': check_selecionado.data_inicio,
                'data_desativacao': check_selecionado.data_desativacao,
                'periodicidade': check_selecionado.periodicidade,
                'medida_periodicidade': check_selecionado.medida_periodicidade,
                'flag_aplicado': flag_aplicado
            }
        }
        return JsonResponse(data)
    @csrf_exempt
    def post(self, request):
        cod_check = request.POST['cod_check']
        desc_check = request.POST['desc_check']
        versao = request.POST['versao']
        data_inicio = request.POST['data_inicio']
        data_desativacao = request.POST['data_desativacao']
        medida_periodicidade = request.POST['medida_periodicidade']
        periodicidade = request.POST['periodicidade']
        cod_usuario_sessao = request.session['cod_usuario_logado']
        tipo = request.POST['tipo']

        if cod_check == '':
            obj_check = Layout_Check(
                desc_check=desc_check,
                versao=versao,
                data_inicio=data_inicio,
                data_desativacao=data_desativacao,
                medida_periodicidade=medida_periodicidade,
                periodicidade=periodicidade,
                cod_usu=Usuario.objects.get(cod_usu=cod_usuario_sessao),
                data_inclusao=datetime.now(),
                tipo_check=tipo
            )
            novo_check = True
            mensagem = 'Inserção realizada com sucesso!'
        else:
            obj_check = Layout_Check.objects.get(pk=cod_check)
            if obj_check.desc_check != desc_check:
                obj_check.desc_check = desc_check
            if obj_check.versao != versao:
                obj_check.versao = versao
            if obj_check.data_inicio != data_inicio:
                obj_check.data_inicio = data_inicio
            if obj_check.data_desativacao != data_desativacao:
                obj_check.data_desativacao = data_desativacao
            if obj_check.medida_periodicidade != medida_periodicidade:
                obj_check.medida_periodicidade = medida_periodicidade
            if obj_check.periodicidade != periodicidade:
                obj_check.periodicidade = periodicidade
            novo_check = False
            mensagem = 'Edição realizada com sucesso!'
        obj_check.save()
        data = {
            'msg': mensagem,
            'novo_check': novo_check,
            'cod_check': obj_check.cod_check,
            'desc_check': obj_check.desc_check
        }
        return JsonResponse(data, safe=False)

class Form_Filial_Check(View):
    @csrf_exempt
    def get(self, request):
        cod_check = request.GET['cod_check']
        lista_filiais_check = []
        filiais_check = list(Libera_Filial_Check.objects.filter(cod_check=cod_check))

        for filial_check in filiais_check:
            filial = Filial.objects.get(cod_filial=filial_check.cod_filial.cod_filial)
            if filial.cod_empresa != None:
                lista_filiais_check.append({'cod_filial': filial.cod_filial, 'desc_filial': filial.desc_filial, 'cod_empresa': filial.cod_empresa.cod_empresa, 'desc_empresa' : filial.cod_empresa.desc_empresa})
            else:
                lista_filiais_check.append({'cod_filial': filial.cod_filial, 'desc_filial': filial.desc_filial, 'cod_empresa': '', 'desc_empresa' : ''})

        lista_filiais_object = list(Filial.objects.all().values('cod_filial', 'desc_filial', 'cod_empresa', 'cod_empresa__desc_empresa'))
        lista_filiais = []
        for filial in lista_filiais_object:
            lista_filiais.append({'cod_filial': filial['cod_filial'], 'desc_filial': filial['desc_filial'], 'cod_empresa': filial['cod_empresa'], 'desc_empresa': filial['cod_empresa__desc_empresa']})

        for filial_check in lista_filiais_check:
            for filial in lista_filiais:
                if filial_check['cod_filial'] == filial['cod_filial'] and filial_check['desc_filial'] == filial['desc_filial'] and filial_check['cod_empresa'] == filial['cod_empresa']:
                    #print('removi o:' + filial['desc_filial'])
                    lista_filiais.remove(filial)

        data = {
            'lista_filiais_check' : lista_filiais_check,
            'lista_filiais': lista_filiais,
            },

        return JsonResponse(data, safe=False)
    @csrf_exempt
    def post(self, request):
        cod_check = request.POST['cod_check']
        filiais_check_form = request.POST['filiais_check'][2:-2]
        print(filiais_check_form)
        filiais_check_form = filiais_check_form.split('","')
        lista_filiais_select = []
        if filiais_check_form != ['']:
            for filial in filiais_check_form:
                filial_get = Filial.objects.get(cod_filial=filial)
                lista_filiais_select.append(filial_get)
             #   else:
             #       print(filial_split)
             #       filial_string = filial_split[0]
             #       if filial_split[1] != 'null':
             #           filial_get = Filial.objects.get(desc_filial=filial_string, cod_empresa=filial_split[1])
             #       else:
             #           filial_get = Filial.objects.get(desc_filial=filial_string)

        lista_filiais_checks = Libera_Filial_Check.objects.filter(cod_check=cod_check)
        lista_filiais_old = []
        for filial_check in lista_filiais_checks:
            filial = Filial.objects.get(cod_filial=filial_check.cod_filial.cod_filial)
            lista_filiais_old.append(filial)

        lista_filiais_add = list(set(lista_filiais_select).difference(lista_filiais_old))
        #print(lista_filiais_add)
        lista_filiais_del = list(set(lista_filiais_old).difference(lista_filiais_select))
        #print(lista_filiais_del)

        for filial in lista_filiais_add:
            obj_filial_check = Libera_Filial_Check(
                cod_check=Layout_Check.objects.get(cod_check=cod_check),
                cod_filial=filial
            )
            obj_filial_check.save()

        for filial in lista_filiais_del:
            Libera_Filial_Check.objects.get(cod_check=cod_check, cod_filial=filial.cod_filial).delete()

        #filiais_check = list(Libera_Filial_Check.objects.filter(cod_check=cod_check))

        #obj_check = Layout_Check(
        #    desc_check = desc_check,
        #    versao = versao,
        #    data_desativacao = data_desativacao,
        #    medida_periodicidade = medida_periodicidade,
        #    periodicidade = periodicidade,
        #    cod_usu = Usuario.objects.get(cod_usu = cod_usuario_sessao),
        #    data_inclusao = datetime.now()
        #)
        #obj_check.save()
        teste = 'Deu bom'
        data = {
            'msg': teste
        }
        return JsonResponse(data, safe=False)

class Form_Item_Check(View):
    @csrf_exempt
    def get(self, request):
        cod_check = request.GET['cod_check']
        lista_itens = Item_Check.objects.filter(cod_check=cod_check)
        lista_itens_check = []

        for item in lista_itens:
            lista_itens_check.append({'cod_item_check': item.cod_item_check,
                                       'desc_check': item.desc_check,
                                       'tipo_resposta': item.tipo_resposta,
                                       'data_inclusao': item.data_inclusao,
                                       'cod_usuario': item.cod_usuario,
                                       'data_inicio': item.data_inicio,
                                       'data_desativacao': item.data_desativacao,
                                       'campo_obs_img': item.campo_obs_img,
                                       'obrigatorio': item.obrigatorio,
                                       'ordem_item': item.ordem_item,
                                       'tipo_item': item.tipo_item,
                                       })

        def get_ordem(item_check):
            return item_check.get('ordem_item')

        lista_itens_check.sort(key=get_ordem)

        data = {
            'lista_itens_check': lista_itens_check
        }
        return JsonResponse(data)

    @csrf_exempt
    def post(self, request):
        cod_item_check = request.POST['cod_item_check']
        cod_check = request.POST['cod_check']
        ordem_item = request.POST['ordem']
        #True - request feita ao arrastar um elemento no sortable,
        #False - request feita ao adicionar um novo item via botão.
        flag_arrastar_sortable = request.POST['flag_arrastar_sortable']
        obj_item_check = None
        flag_incrementa_elementos_sortable = False

        if flag_arrastar_sortable == '1':
            obj_item_check = Item_Check.objects.get(pk=cod_item_check)
            if obj_item_check.ordem_item != ordem_item:
                if int(obj_item_check.ordem_item) > int(ordem_item):
                    #print('obj_item_check.ordem_item > ordem_item')
                    flag_incrementa_elementos_sortable = False
                else:
                    #print('obj_item_check.ordem_item < ordem_item')
                    flag_incrementa_elementos_sortable = True
                obj_item_check.ordem_item = ordem_item

            mensagem = 'Ordem alterada com sucesso!'

        elif flag_arrastar_sortable == '0':
            desc_item = request.POST['desc_item']
            tipo_item = request.POST['tipo_item']
            data_inicio = request.POST['inicio_item']
            data_desativar = request.POST['desativar_item']
            imagem_obs = request.POST['imagem_obs']
            resposta_obrigatoria = request.POST['resposta_obrigatoria']
            if request.POST['tipo_resposta'] == '' and tipo_item == '2':
                tipo_resposta = None
            else:
                tipo_resposta = request.POST['tipo_resposta']
            cod_usuario_sessao = request.session['cod_usuario_logado']
            if cod_item_check == '':
                obj_item_check = Item_Check(
                    desc_check=desc_item,
                    tipo_resposta=tipo_resposta,
                    data_inclusao=datetime.now(),
                    cod_usuario=cod_usuario_sessao,
                    data_inicio=data_inicio,
                    data_desativacao=data_desativar,
                    campo_obs_img=imagem_obs,
                    obrigatorio=resposta_obrigatoria,
                    ordem_item=ordem_item,
                    tipo_item=tipo_item,
                    cod_check=Layout_Check.objects.get(cod_check=cod_check)
                )
                mensagem = 'Inserção de Item feita com sucesso!'
            else:
                obj_item_check = Item_Check.objects.get(pk=cod_item_check)
                if obj_item_check.desc_check != desc_item:
                    obj_item_check.desc_check = desc_item
                if obj_item_check.tipo_item != tipo_item:
                    obj_item_check.tipo_item = tipo_item
                if obj_item_check.ordem_item != ordem_item:
                    obj_item_check.ordem_item = ordem_item
                if obj_item_check.data_inicio != data_inicio:
                    obj_item_check.data_inicio = data_inicio
                if obj_item_check.data_desativacao != data_desativar:
                    obj_item_check.data_desativacao = data_desativar
                if obj_item_check.campo_obs_img != imagem_obs:
                    obj_item_check.campo_obs_img = imagem_obs
                if obj_item_check.obrigatorio != resposta_obrigatoria:
                    obj_item_check.obrigatorio = resposta_obrigatoria
                if obj_item_check.tipo_resposta != tipo_resposta:
                    obj_item_check.tipo_resposta = tipo_resposta
                mensagem = 'Edição de Item feita com sucesso!'

        lista_item_check = Item_Check.objects.filter(cod_check=cod_check)
        obj_item_check.save()
        Comportamentos_Sortable().ordena_itens(obj_item_check, lista_item_check, flag_incrementa_elementos_sortable)
        Comportamentos_Sortable().define_indices_itens_check(cod_check)

        data = {
            'msg': mensagem
        }
        return JsonResponse(data, safe=False)

class Sortable_View(View):
    @csrf_exempt
    def get(self, request):
        cod_item = request.GET['cod_item_check']
        item_selecionado = Item_Check.objects.get(pk=cod_item) #a
        data = {
            'item_selecionado': {
                'cod_item_check': item_selecionado.cod_item_check,
                'desc_check': item_selecionado.desc_check,
                'tipo_resposta': item_selecionado.tipo_resposta,
                'data_inclusao': item_selecionado.data_inclusao,
                'cod_usuario': item_selecionado.cod_usuario,
                'data_inicio': item_selecionado.data_inicio,
                'data_desativacao': item_selecionado.data_desativacao,
                'campo_obs_img': item_selecionado.campo_obs_img,
                'obrigatorio': item_selecionado.obrigatorio,
                'ordem_item': item_selecionado.ordem_item,
                'tipo_item': item_selecionado.tipo_item
            }
        }
        return JsonResponse(data)

class Form_Cadastro_Colaborador(View):
    @csrf_exempt
    def post(self, request):
        nome_colab = request.POST['nome_colab']
        cpf_colab = request.POST['cpf_colab']
        dt_nasc_colab = request.POST['dt_nasc_colab']
        filial_cad_colab = request.POST['filial_cad_colab']
        if Colaborador.objects.filter(cpf=str(cpf_colab).zfill(11)).first() != None:
            response = HttpResponse('Colaborador já consta no sistema!')
            response.status_code = 400
            return response
        else:
            novo_colab = Colaborador(
                nome_colaborador=nome_colab,
                cpf=cpf_colab,
                data_nascimento=dt_nasc_colab,
                cod_filial=filial_cad_colab,
                perfil_usu='U'
            )
            novo_colab.save()

        return HttpResponse('Colaborador cadastrado com sucesso!')

class Comportamentos_Sortable():
    @csrf_exempt
    def ordena_itens(self, item_check_inserido, lista_itens_check, flag_incrementa_elementos_sortable):
        for item in lista_itens_check:
            if int(item_check_inserido.ordem_item) == int(item.ordem_item) and int(item_check_inserido.cod_item_check) != int(item.cod_item_check):
                if flag_incrementa_elementos_sortable == False:
                    item.ordem_item = item.ordem_item + 1
                elif flag_incrementa_elementos_sortable == True:
                    item.ordem_item = item.ordem_item - 1
                item.save() #a
                Comportamentos_Sortable().ordena_itens(item, lista_itens_check, flag_incrementa_elementos_sortable)
    @csrf_exempt
    def define_indices_itens_check(self, cod_check):
        lista_itens_check = Item_Check.objects.filter(cod_check=cod_check).order_by('ordem_item')
        i = 1
        for item in lista_itens_check:
            item.ordem_item = i
            item.save()
            i += 1


