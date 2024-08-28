from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.estrut_org_app.models import Filial
from apps.safety_blitz_trajeto_bicicleta_app.models import Blitz_Trajeto_Bicicleta
from apps.safety_blitz_trajeto_carro_app.models import Blitz_Trajeto_Carro
from apps.safety_blitz_trajeto_moto_app.models import Blitz_Trajeto_Moto
from apps.safety_blitz_trajeto_outros_meios_app.models import Blitz_Trajeto_Outros_Meios
from apps.safety_checks_aplicados_app.models import Check_Aplicado, Item_Check_Aplicados, \
    Item_Fotos_Texto_Check_Aplicado, Plano_Acao
from apps.safety_gso_app.models import Gabarito_GSO
from apps.safety_layout_checklist_app.models import Layout_Check, Libera_Filial_Check, Item_Check, Itens_Componentes
from apps.safety_login_colaboradores_app.models import Colaborador
from apps.safety_relatos_app.models import Relato
from apps.usuario_app.models import Usuario


# Create your views here.

class Form_Seguranca_Check(View):
    @csrf_exempt
    def get(self, request):
        lista_tipos = {'1': 'Empilhadeiras', '2': 'Relatos', '3': 'GSDPQ',
                       '4': 'Blitz - Carro', '5': 'Blitz - Moto', '6': 'Blitz - Bicicleta',
                       '7': 'Blitz - Outros Meios', '8': 'GSO'}
        cod_usuario_sessao = request.session['cod_usuario_logado']
        usuario = Usuario.objects.get(pk=cod_usuario_sessao)
        flag_corporativo = 0
        if usuario.corporativo == 'S':
            lista_filiais = Filial.objects.filter(cod_empresa=usuario.cod_filial.cod_empresa, ativo=1)
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
            lista_checks = list(Layout_Check.objects.filter(tipo_check=cod_tipo, ativo=1))
        elif usuario.corporativo == 'N':
            checks_liberados_filial_usu = Libera_Filial_Check.objects.filter(cod_filial=usuario.cod_filial)

            lista_checks = Layout_Check.objects.filter(tipo_check=cod_tipo,cod_usu__cod_filial=usuario.cod_filial, ativo=1)
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
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.get(pk=cod_usuario_sessao)

        cod_check = request.GET['cod_check']
        lista_filiais_check = []
        filiais_check = list(Libera_Filial_Check.objects.filter(cod_check=cod_check, cod_filial__ativo=1, cod_filial__cod_empresa=obj_usuario.cod_filial.cod_empresa))

        for filial_check in filiais_check:
            filial = Filial.objects.get(cod_filial=filial_check.cod_filial.cod_filial)
            if filial.cod_empresa != None:
                lista_filiais_check.append({'cod_filial': filial.cod_filial, 'desc_filial': filial.desc_filial, 'cod_empresa': filial.cod_empresa.cod_empresa, 'desc_empresa' : filial.cod_empresa.desc_empresa})
            else:
                lista_filiais_check.append({'cod_filial': filial.cod_filial, 'desc_filial': filial.desc_filial, 'cod_empresa': '', 'desc_empresa' : ''})

        lista_filiais_object = list(Filial.objects.filter(ativo=1, cod_empresa=obj_usuario.cod_filial.cod_empresa).values('cod_filial', 'desc_filial', 'cod_empresa', 'cod_empresa__desc_empresa'))
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
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.get(pk=cod_usuario_sessao)

        cod_check = request.POST['cod_check']
        filiais_check_form = request.POST['filiais_check'][2:-2]
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

        lista_filiais_checks = Libera_Filial_Check.objects.filter(cod_check=cod_check, cod_filial__cod_empresa=obj_usuario.cod_filial.cod_empresa)
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
                perfil_usu='U',
                situacao=0
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

class Check_Aplicado_Editar(View):
    @csrf_exempt
    def get(self, request):
        id_check_aplicado = request.GET['cod_check_aplicado']
        check_aplicado = Check_Aplicado.objects.filter(cod_check_aplicado=id_check_aplicado).first()
        layout_check = Layout_Check.objects.filter(cod_check=check_aplicado.cod_layout_check.cod_check).first()
        itens_layout_check = Item_Check.objects.filter(cod_check=layout_check)
        filial = Filial.objects.filter(cod_filial=check_aplicado.cod_filial).first()
        if check_aplicado.cod_colaborador_avaliado is not None:
            relatado = Colaborador.objects.filter(cod_colaborador=check_aplicado.cod_colaborador_avaliado.cod_colaborador).first()
        else:
            relatado = None
        html_check_editar = ''
        str_categoria_condicao_insegura = ''

        if check_aplicado.cod_layout_check.tipo_check == 2:
            relato_aplicado = Relato.objects.filter(cod_check_aplicado=check_aplicado).first()
            processo = Itens_Componentes.objects.filter(tipo_check=2, campo_check=1, cod_componente=relato_aplicado.processo_relato).first()
            atividade = Itens_Componentes.objects.filter(cod_componente=relato_aplicado.atividade_relato).first()
            if relato_aplicado.cod_tipo_relato == 1:
                categoria_ato_inseguro = Itens_Componentes.objects.filter(campo_check=3, cod_componente=relato_aplicado.categoria_ato_inseguro).first()

                if categoria_ato_inseguro is not None:
                    str_categoria_ato_inseguro = f'''<div id="div_ato_inseguro_categorias" class="form-group">
                                                        <label class="responsive-font" for="ato_inseguro_categoria">Selecione o tipo de ato inseguro ocorrido, caso não identificado, selecione OUTROS</label>
                                                        <select class="selectpicker form-control" id="ato_inseguro_categoria" name="ato_inseguro_categoria" value="{categoria_ato_inseguro.cod_componente}" disabled>
                                                            <option value="{categoria_ato_inseguro.cod_componente}">{categoria_ato_inseguro.desc_componente}</option>
                                                        </select>
                                                    </div>'''
            else:
                str_categoria_ato_inseguro = ''

            if relato_aplicado.cod_tipo_relato == 2:
                categoria_condicao_insegura = Itens_Componentes.objects.filter(campo_check=4, cod_componente=relato_aplicado.categoria_condicao_insegura).first()

                if categoria_condicao_insegura is not None:
                    str_categoria_condicao_insegura = f'''<div id="div_condicao_insegura_categorias" class="form-group">
                                                        <label class="responsive-font" for="condicao_insegura_categoria">Qual tipo de condição insegura ocorreu?</label>
                                                        <select class="selectpicker form-control responsive-font" id="condicao_insegura_categoria" name="condicao_insegura_categoria" value="{categoria_condicao_insegura.cod_componente}" disabled>
                                                            <option value="{categoria_condicao_insegura.cod_componente}">{categoria_condicao_insegura.desc_componente}</option>
                                                        </select>
                                                    </div>'''
            else:
                str_categoria_condicao_insegura = ''

            empresa_colaborador_aplicante = Filial.objects.filter(cod_filial=check_aplicado.cod_colaborador_aplicante.cod_filial).first().cod_empresa.cod_empresa
            if relato_aplicado.cod_tipo_relato == 3 and empresa_colaborador_aplicante == 17:
                categoria_comportamento_seguro = Itens_Componentes.objects.filter(campo_check=5, cod_componente=relato_aplicado.categoria_condicao_insegura).first()

                if categoria_comportamento_seguro is not None:
                    str_categoria_comportamento_seguro = f'''<div id="div_comportamento_seguro_categorias" class="form-group">
                                                        <label class="responsive-font" for="comportamento_seguro_categoria">Qual tipo de condição insegura ocorreu?</label>
                                                        <select class="selectpicker form-control responsive-font" id="comportamento_seguro_categoria" name="comportamento_seguro_categoria" value="{categoria_comportamento_seguro.cod_componente}" disabled>
                                                            <option value="{categoria_comportamento_seguro.cod_componente}">{categoria_comportamento_seguro.desc_componente}</option>
                                                        </select>
                                                    </div>'''
                else:
                    str_categoria_comportamento_seguro = ''
            else:
                str_categoria_comportamento_seguro = ''

            if relatado is not None:
                str_relatado = f'''<div id="div_situacao_relatado" class="form-group">
                                      <label class="responsive-font" for="situacao_envolvido">Quem foi que gerou esta condição?</label>
                                      <select class="selectpicker form-control responsive-font" id="situacao_envolvido" name="situacao_envolvido" value="{relato_aplicado.situacao_envolvido}" disabled>
                                          <option value="1">Funcionario Conlog/Deep</option>
                                          <option value="2">Funcionario Ambev</option>
                                          <option value="3">Freteiro</option>
                                          <option value="4">Terceiros</option>
                                      </select>
                                   </div>'''
                if relato_aplicado.situacao_envolvido == 1:
                    str_relatado += f'''<div id="div_relatado" class="form-group">
                                                <label class="responsive-font" for="nome_relatado">Nome do relatado:</label>
                                                <select class="selectpicker form-control responsive-font" id="nome_relatado" name="nome_relatado" value="nome_operador" value="{relatado.cod_colaborador}" disabled>
                                                    <option value="{relatado.cod_colaborador}">{relatado.nome_colaborador}</option>
                                                </select>
                                            </div>'''
                else:
                    str_relatado += f'''<div id="div_relatado_terceiro" class="form-group">
                                                <label class="responsive-font" for="nome_relatado_terceiro">Nome do relatado:</label>
                                                <input type="text" class="form-control responsive-font" id="nome_relatado_terceiro" name="nome_relatado_terceiro" value="{relatado.nome_colaborador}" disabled>
                                            </div>'''
            else:
                str_relatado = ''

            if processo is not None:
                str_processo = f'''<div class="form-group">
                                       <label for="processo_relato">O ato ocorreu durante um processo? qual processo?</label>
                                       <select class="form-control responsive-font selectpicker" id="processo_relato" name="processo_relato" value="{processo.cod_componente}" disabled>
                                           <option value="{processo.cod_componente}">{processo.desc_componente}</option>
                                       </select>
                                   </div>'''
            else:
                str_processo = ''

            if atividade is not None:
                str_atividade = f'''<div class="form-group">
                                       <label for="atividade_relato">Que atividade estava sendo realizada?</label>
                                        <select class="form-control responsive-font selectpicker" id="atividade_relato" name="atividade_relato" value="{atividade.cod_componente}" disabled>
                                            <option value="{atividade.cod_componente}">{atividade.desc_componente}</option>
                                        </select>
                                    </div>'''
            else:
                str_atividade = ''

            html_check_editar = f'''<div class="col-md-12 w-100 h-100">
                                        <form class="h-100" id="form_preenche_check" name="form_preenche_check" style="padding-left:1rem">
                                            <div class="tab-content h-100" style="border-radius:0 0 10px 10px; font-size:15px; color: rgba(0,0,0,0.9)">
                                                <div class="tab-pane active h-100" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                                        <div class="row h-100" style="text-align:left;flex-direction:column;justify-content:space-between;">
                                                            <div style="padding:15px;padding-right:30px;padding-left:30px">
                                                                <input type="text" id="identifica_tipo_check" name="identifica_tipo_check" value={check_aplicado.cod_layout_check.tipo_check} style="display:none">
                                                                <div class="form-group">
                                                                   <label for="unidade"> Unidade: </label>
                                                                    <select class="selectpicker form-control responsive-font" id="unidade" name="unidade" value="{check_aplicado.cod_filial}" disabled>
                                                                        <option value="{check_aplicado.cod_filial}">{filial.desc_filial}</option>
                                                                    </select>
                                                                </div>
                                                                <div class="form-group">
                                                                   <label for="tipo_relato">Tipo de Relato:</label>
                                                                   <select class="selectpicker form-control responsive-font" id="tipo_relato" name="tipo_relato" value="{relato_aplicado.cod_tipo_relato}" disabled>
                                                                       <option value="1" selected="{'selected' if relato_aplicado.cod_tipo_relato == 1 else ''}">Ato inseguro</option>
                                                                       <option value="2" selected="{'selected' if relato_aplicado.cod_tipo_relato == 2 else ''}">Condição insegura</option>
                                                                       <option value="3" selected="{'selected' if relato_aplicado.cod_tipo_relato == 3 else ''}">Abordagem positiva</option>
                                                                   </select>
                                                                </div>
                                                                {str_categoria_ato_inseguro}
                                                                {str_categoria_condicao_insegura}
                                                                {str_categoria_comportamento_seguro}
                                                                {str_relatado}
                                                                <div class="form-group">
                                                                   <label for="local_relato">Local do relato:</label>
                                                                   <input type="text" class="form-control responsive-font" id="local_relato" name="local_relato" value="{relato_aplicado.local_relato}" disabled>
                                                                </div>
                                                                {str_processo}
                                                                {str_atividade}
                                                            </div>
                                                        </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>'''

        if check_aplicado.cod_layout_check.tipo_check == 4:
            blitz_carro_aplicado = Blitz_Trajeto_Carro.objects.filter(cod_check_aplicado=check_aplicado).first()

            if blitz_carro_aplicado.situacao_colaborador == 1:
                str_colaborador = f'''<div id="div_avaliado" class="form-group">
                                            <label class="responsive-font" for="nome_relatado">Nome do colaborador:</label>
                                            <select class="selectpicker form-control responsive-font" id="nome_avaliado" name="nome_avaliado" value="nome_avaliado" value="{relatado.cod_colaborador}" disabled>
                                                <option value="{relatado.cod_colaborador}">{relatado.nome_colaborador}</option>
                                            </select>
                                        </div>'''
            else:
                str_colaborador = f'''<div id="div_avaliado_terceiro" class="form-group">
                                            <label class="responsive-font" for="nome_avaliado_terceiro">Nome do colaborador:</label>
                                            <input type="text" class="form-control responsive-font" id="nome_avaliado_terceiro" name="nome_avaliado_terceiro" value="{relatado.nome_colaborador}" disabled>
                                        </div>'''

            html_check_editar = f'''<div class="col-md-12 w-100 h-100">
                                        <form class="h-100" id="form_preenche_check" name="form_preenche_check" style="padding-left:1rem">
                                            <div class="tab-content h-100" style="border-radius:0 0 10px 10px; font-size:15px; color: rgba(0,0,0,0.9)">
                                                <div class="tab-pane active h-100" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                                        <div class="row h-100" style="text-align:left;flex-direction:column;justify-content:space-between;">
                                                            <div style="padding:15px;padding-right:30px;padding-left:30px">
                                                                <input type="text" id="identifica_tipo_check" name="identifica_tipo_check" value={check_aplicado.cod_layout_check.tipo_check} style="display:none">
                                                                <div class="form-group">
                                                                   <label for="unidade"> Unidade: </label>
                                                                    <select class="selectpicker form-control responsive-font" id="unidade" name="unidade" value="{check_aplicado.cod_filial}" disabled>
                                                                        <option value="{check_aplicado.cod_filial}">{filial.desc_filial}</option>
                                                                    </select>
                                                                </div>
                                                                <div id="div_situacao_colaborador" class="form-group">
                                                                   <label class="responsive-font" for="situacao_avaliado">Quem está sendo descrito??</label>
                                                                   <select class="selectpicker form-control responsive-font" id="situacao_avaliado" name="situacao_avaliado" value="{blitz_carro_aplicado.situacao_colaborador}" disabled>
                                                                       <option value="1">Funcionario Conlog/Deep</option>
                                                                       <option value="2">Funcionario Ambev</option>
                                                                       <option value="3">Freteiro</option>
                                                                       <option value="4">Terceiros</option>
                                                                   </select>
                                                                </div>
                                                                {str_colaborador}
                                                                <div class="form-group">
                                                                   <label for="placa_carro">Placa:</label>
                                                                   <input type="text" class="form-control responsive-font" id="placa_carro" name="placa_caminhao" value={blitz_carro_aplicado.placa} disabled>
                                                                </div>
                                                            </div>
                                                        </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>'''

        if check_aplicado.cod_layout_check.tipo_check == 5:
            blitz_moto_aplicado = Blitz_Trajeto_Moto.objects.filter(cod_check_aplicado=check_aplicado).first()

            if blitz_moto_aplicado.situacao_colaborador == 1:
                str_colaborador = f'''<div id="div_avaliado" class="form-group">
                                            <label class="responsive-font" for="nome_relatado">Nome do relatado:</label>
                                            <select class="selectpicker form-control responsive-font" id="nome_avaliado" name="nome_avaliado" value="nome_avaliado" value="{relatado.cod_colaborador}" disabled>
                                                <option value="{relatado.cod_colaborador}">{relatado.nome_colaborador}</option>
                                            </select>
                                        </div>'''
            else:
                str_colaborador = f'''<div id="div_avaliado_terceiro" class="form-group">
                                            <label class="responsive-font" for="nome_avaliado_terceiro">Nome do relatado:</label>
                                            <input type="text" class="form-control responsive-font" id="nome_avaliado_terceiro" name="nome_avaliado_terceiro" value="{relatado.nome_colaborador}" disabled>
                                        </div>'''

            html_check_editar = f'''<div class="col-md-12 w-100 h-100">
                                        <form class="h-100" id="form_preenche_check" name="form_preenche_check" style="padding-left:1rem">
                                            <div class="tab-content h-100" style="border-radius:0 0 10px 10px; font-size:15px; color: rgba(0,0,0,0.9)">
                                                <div class="tab-pane active h-100" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                                        <div class="row h-100" style="text-align:left;flex-direction:column;justify-content:space-between;">
                                                            <div style="padding:15px;padding-right:30px;padding-left:30px">
                                                                <input type="text" id="identifica_tipo_check" name="identifica_tipo_check" value={check_aplicado.cod_layout_check.tipo_check} style="display:none">
                                                                <div class="form-group">
                                                                   <label for="unidade"> Unidade: </label>
                                                                    <select class="selectpicker form-control responsive-font" id="unidade" name="unidade" value="{check_aplicado.cod_filial}" disabled>
                                                                        <option value="{check_aplicado.cod_filial}">{filial.desc_filial}</option>
                                                                    </select>
                                                                </div>
                                                                <div id="div_situacao_colaborador" class="form-group">
                                                                   <label class="responsive-font" for="situacao_avaliado">Quem está sendo descrito??</label>
                                                                   <select class="selectpicker form-control responsive-font" id="situacao_avaliado_moto" name="situacao_avaliado_moto" value="{blitz_moto_aplicado.situacao_colaborador}" disabled>
                                                                       <option value="1">Funcionario Conlog/Deep</option>
                                                                       <option value="2">Funcionario Ambev</option>
                                                                       <option value="3">Freteiro</option>
                                                                       <option value="4">Terceiros</option>
                                                                   </select>
                                                                </div>
                                                                {str_colaborador}
                                                                <div class="form-group">
                                                                   <label for="placa_carro">Placa:</label>
                                                                   <input type="text" class="form-control responsive-font" id="placa_moto" name="placa_moto" value={blitz_moto_aplicado.placa} disabled>
                                                                </div>
                                                            </div>
                                                        </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>'''

        if check_aplicado.cod_layout_check.tipo_check == 6:
            blitz_bicicleta_aplicado = Blitz_Trajeto_Bicicleta.objects.filter(cod_check_aplicado=check_aplicado).first()

            if blitz_bicicleta_aplicado.situacao_colaborador == 1:
                str_colaborador = f'''<div id="div_avaliado" class="form-group">
                                            <label class="responsive-font" for="nome_relatado">Nome do colaborador:</label>
                                            <select class="selectpicker form-control responsive-font" id="nome_avaliado" name="nome_avaliado" value="nome_avaliado" value="{relatado.cod_colaborador}" disabled>
                                                <option value="{relatado.cod_colaborador}">{relatado.nome_colaborador}</option>
                                            </select>
                                        </div>'''
            else:
                str_colaborador = f'''<div id="div_avaliado_terceiro" class="form-group">
                                            <label class="responsive-font" for="nome_avaliado_terceiro">Nome do colaborador:</label>
                                            <input type="text" class="form-control responsive-font" id="nome_avaliado_terceiro" name="nome_avaliado_terceiro" value="{relatado.nome_colaborador}" disabled>
                                        </div>'''

            html_check_editar = f'''<div class="col-md-12 w-100 h-100">
                                        <form class="h-100" id="form_preenche_check" name="form_preenche_check" style="padding-left:1rem">
                                            <div class="tab-content h-100" style="border-radius:0 0 10px 10px; font-size:15px; color: rgba(0,0,0,0.9)">
                                                <div class="tab-pane active h-100" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                                        <div class="row h-100" style="text-align:left;flex-direction:column;justify-content:space-between;">
                                                            <div style="padding:15px;padding-right:30px;padding-left:30px">
                                                                <input type="text" id="identifica_tipo_check" name="identifica_tipo_check" value={check_aplicado.cod_layout_check.tipo_check} style="display:none">
                                                                <div class="form-group">
                                                                   <label for="unidade"> Unidade: </label>
                                                                    <select class="selectpicker form-control responsive-font" id="unidade" name="unidade" value="{check_aplicado.cod_filial}" disabled>
                                                                        <option value="{check_aplicado.cod_filial}">{filial.desc_filial}</option>
                                                                    </select>
                                                                </div>
                                                                <div id="div_situacao_colaborador" class="form-group">
                                                                   <label class="responsive-font" for="situacao_avaliado">Quem está sendo descrito??</label>
                                                                   <select class="selectpicker form-control responsive-font" id="situacao_avaliado_bicicleta" name="situacao_avaliado_bicicleta" value="{blitz_bicicleta_aplicado.situacao_colaborador}" disabled>
                                                                       <option value="1">Funcionario Conlog/Deep</option>
                                                                       <option value="2">Funcionario Ambev</option>
                                                                       <option value="3">Freteiro</option>
                                                                       <option value="4">Terceiros</option>
                                                                   </select>
                                                                </div>
                                                                {str_colaborador}
                                                            </div>
                                                        </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>'''

        if check_aplicado.cod_layout_check.tipo_check == 7:
            blitz_outros_meios_aplicado = Blitz_Trajeto_Outros_Meios.objects.filter(cod_check_aplicado=check_aplicado).first()

            if blitz_outros_meios_aplicado.situacao_colaborador == 1:
                str_colaborador = f'''<div id="div_avaliado" class="form-group">
                                            <label class="responsive-font" for="nome_relatado">Nome do colaborador:</label>
                                            <select class="selectpicker form-control responsive-font" id="nome_avaliado" name="nome_avaliado" value="nome_avaliado" value="{relatado.cod_colaborador}" disabled>
                                                <option value="{relatado.cod_colaborador}">{relatado.nome_colaborador}</option>
                                            </select>
                                        </div>'''
            else:
                str_colaborador = f'''<div id="div_avaliado_terceiro" class="form-group">
                                            <label class="responsive-font" for="nome_avaliado_terceiro">Nome do colaborador:</label>
                                            <input type="text" class="form-control responsive-font" id="nome_avaliado_terceiro" name="nome_avaliado_terceiro" value="{relatado.nome_colaborador}" disabled>
                                        </div>'''

            html_check_editar = f'''<div class="col-md-12 w-100 h-100">
                                        <form class="h-100" id="form_preenche_check" name="form_preenche_check" style="padding-left:1rem">
                                            <div class="tab-content h-100" style="border-radius:0 0 10px 10px; font-size:15px; color: rgba(0,0,0,0.9)">
                                                <div class="tab-pane active h-100" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                                        <div class="row h-100" style="text-align:left;flex-direction:column;justify-content:space-between;">
                                                            <div style="padding:15px;padding-right:30px;padding-left:30px">
                                                                <input type="text" id="identifica_tipo_check" name="identifica_tipo_check" value={check_aplicado.cod_layout_check.tipo_check} style="display:none">
                                                                <div class="form-group">
                                                                   <label for="unidade"> Unidade: </label>
                                                                    <select class="selectpicker form-control responsive-font" id="unidade" name="unidade" value="{check_aplicado.cod_filial}" disabled>
                                                                        <option value="{check_aplicado.cod_filial}">{filial.desc_filial}</option>
                                                                    </select>
                                                                </div>
                                                                <div id="div_situacao_colaborador" class="form-group">
                                                                   <label class="responsive-font" for="situacao_avaliado">Quem está sendo descrito??</label>
                                                                   <select class="selectpicker form-control responsive-font" id="situacao_avaliado_outros_meios" name="situacao_avaliado_outros_meios" value="{blitz_outros_meios_aplicado.situacao_colaborador}" disabled>
                                                                       <option value="1">Funcionario Conlog/Deep</option>
                                                                       <option value="2">Funcionario Ambev</option>
                                                                       <option value="3">Freteiro</option>
                                                                       <option value="4">Terceiros</option>
                                                                   </select>
                                                                </div>
                                                                {str_colaborador}
                                                                <label class="responsive-font" for="meio_transporte">Meio de transporte:</label>
                                                                <select class="selectpicker form-control responsive-font" id="meio_transporte" name="meio_transporte" value="{blitz_outros_meios_aplicado.meio_transporte}" disabled>
                                                                    <option value="1">Transporte Público</option>
                                                                    <option value="2">Carona</option>
                                                                    <option value="3">Pé</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>'''

        if check_aplicado.cod_layout_check.tipo_check == 8:
            gab_gso_aplicado = Gabarito_GSO.objects.filter(cod_check_aplicado=check_aplicado).first()

            html_check_editar = f'''<div class="col-md-12 w-100 h-100">
                                        <form class="h-100" id="form_preenche_check" name="form_preenche_check" style="padding-left:1rem">
                                            <div class="tab-content h-100" style="border-radius:0 0 10px 10px; font-size:15px; color: rgba(0,0,0,0.9)">
                                                <div class="tab-pane active h-100" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                                        <div class="row h-100" style="text-align:left;flex-direction:column;justify-content:space-between;">
                                                            <div style="padding:15px;padding-right:30px;padding-left:30px">
                                                                <input type="text" id="identifica_tipo_check" name="identifica_tipo_check" value={check_aplicado.cod_layout_check.tipo_check} style="display:none">
                                                                <div class="form-group">
                                                                   <label for="unidade"> Unidade: </label>
                                                                    <select class="selectpicker form-control responsive-font" id="unidade" name="unidade" value="{check_aplicado.cod_filial}" disabled>
                                                                        <option value="{check_aplicado.cod_filial}">{filial.desc_filial}</option>
                                                                    </select>
                                                                </div>
                                                                <div class="form-group">
                                                                   <label class="responsive-font" for="nome_avaliado_gso">Nome do avaliado:</label>
                                                                   <input type="text" class="form-control responsive-font" id="nome_avaliado_gso" name="nome_avaliado_gso" value="{relatado.nome_colaborador}">
                                                                </div>
                                                                <div class="form-group">
                                                                  <label for="placa_onibus_gso">Placa do Ônibus:</label>
                                                                  <input type="text" class="form-control responsive-font" id="placa_onibus_gso" name="placa_onibus_gso" value="{gab_gso_aplicado.placa_onibus}">
                                                                </div>
                                                            </div>
                                                        </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>'''

        html_check_editar += '<div class="background-check-preenchido" style="width:100%;display:flex;justify-content:center">'

        for item in itens_layout_check:
            str_nome_botoes = str(item.cod_item_check) + '@' + str(id_check_aplicado)
            if item.tipo_item == 2:
                html_check_editar += f'<b class="responsive-font" style="width:100%;padding-left:2rem;margin-bottom:0.5rem;margin-top:2rem;font-size:18px;background-color:rgb(242,101,34);">{item.desc_check}</b>'
            if item.tipo_item == 1:
                if item.tipo_resposta == 1 or item.tipo_resposta == 3 or item.tipo_resposta == 4 or item.tipo_resposta == 5 or item.tipo_resposta == 6:
                    desc_resposta_botao = ''
                    if item.tipo_resposta == 1 or item.tipo_resposta == '1':
                        desc_resposta_botao = 'OK/NOK'.split('/')
                    if item.tipo_resposta == 3 or item.tipo_resposta == '3':
                        desc_resposta_botao = 'SIM/NÃO'.split('/')
                    if item.tipo_resposta == 4 or item.tipo_resposta == '4':
                        desc_resposta_botao = 'PRÓPRIO/COMPANHIA'.split('/')
                    if item.tipo_resposta == 5 or item.tipo_resposta == '5':
                        desc_resposta_botao = 'OK/NA/NOK'.split('/')
                        str_botao_na = ''
                    if item.tipo_resposta == 6 or item.tipo_resposta == '6':
                        desc_resposta_botao = 'OTIMO/BOM/REGULAR/DANIFICADO'.split('/')
                        str_botao_bom = ''
                        str_botao_regular = ''
                    resposta_ok_nok_check_aplicado = Item_Check_Aplicados.objects.filter(
                        cod_check_aplicado=check_aplicado, cod_item_check=item).first()

                    str_botao_ok = ''
                    str_botao_nok = ''
                    if resposta_ok_nok_check_aplicado is not None:
                        if resposta_ok_nok_check_aplicado.resp_item == 0:
                            str_botao_ok = 'background-color:green'
                        elif resposta_ok_nok_check_aplicado.resp_item == 1:
                            str_botao_nok = 'background-color:red'
                        elif resposta_ok_nok_check_aplicado.resp_item == 3:
                            str_botao_nok = 'background-color:cyan'
                        elif resposta_ok_nok_check_aplicado.resp_item == 4:
                            str_botao_nok = 'background-color:yellow'
                        elif resposta_ok_nok_check_aplicado.resp_item == 5:
                            str_botao_nok = 'background-color:orange'
                    if item.campo_obs_img == 0:

                        if item.tipo_resposta == 5 or item.tipo_resposta == '5':
                            str_buttons = f'''<button type="button" name="{str_nome_botoes}" class="responsive-font ok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_ok}" disabled>{desc_resposta_botao[0]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[1]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[2]}</button>
                                              '''
                        elif item.tipo_resposta == 6 or item.tipo_resposta == '6':
                            str_buttons = f'''<button type="button" name="{str_nome_botoes}" class="responsive-font ok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_ok}" disabled>{desc_resposta_botao[0]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font yellow-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;" disabled>{desc_resposta_botao[1]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font orange-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;" disabled>{desc_resposta_botao[2]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[3]}</button>
                                           '''
                        else:
                            str_buttons = f''' <button type="button" name="{str_nome_botoes}" class="responsive-font ok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_ok}" disabled>{desc_resposta_botao[0]}</button>
                                                    <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[1]}</button>
                                                '''

                        html_check_editar += f'''<div style="width:100%;border-style:dashed;border-color:black;margin-bottom:0.3rem;border-radius:10px 10px 10px 10px;border-width:1.5px">
                                                <p class="responsive-font item-text" style="display:flex;justify-content:center;padding:4px;text-align:center;color:black;">{item.desc_check}</p>
                                                <input type="hidden" class="identifier" value="{item.ordem_item}">
                                                <input type="hidden" class="obrigatorio" name="obrigatorio" value="{item.obrigatorio}">
                                                <div style="display:flex;justify-content:center;padding:4px">
                                                {str_buttons}
                                                </div>
                                            </div>'''

                    if item.campo_obs_img == 1:
                        respostas_texto_fotos_check_aplicado = Item_Fotos_Texto_Check_Aplicado.objects.filter(
                            cod_check_aplicado=check_aplicado, cod_item_check=item).first()

                        if respostas_texto_fotos_check_aplicado is not None:
                            if respostas_texto_fotos_check_aplicado.comentario is not None:
                                str_comentario = respostas_texto_fotos_check_aplicado.comentario
                            else:
                                str_comentario = ''
                        else:
                            str_comentario = ''

                        if item.tipo_resposta == 5 or item.tipo_resposta == '5':
                            str_buttons = f'''<button type="button" name="{str_nome_botoes}" class="responsive-font ok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_ok}" disabled>{desc_resposta_botao[0]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[1]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[2]}</button>
                                              '''
                        elif item.tipo_resposta == 6 or item.tipo_resposta == '6':
                            str_buttons = f'''<button type="button" name="{str_nome_botoes}" class="responsive-font ok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_ok}" disabled>{desc_resposta_botao[0]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font yellow-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;" disabled>{desc_resposta_botao[1]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font orange-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;" disabled>{desc_resposta_botao[2]}</button>
                                              <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[3]}</button>
                                           '''
                        else:
                            str_buttons = f''' <button type="button" name="{str_nome_botoes}" class="responsive-font ok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_ok}" disabled>{desc_resposta_botao[0]}</button>
                                                    <button type="button" name="{str_nome_botoes}" class="responsive-font nok-button-check button-check-post input-botao relatos" type="button" style="padding:7px;border-width:1px;border-radius:5px;{str_botao_nok}" disabled>{desc_resposta_botao[1]}</button>
                                                '''


                        html_check_editar += f'''<div style="width:100%;border-style:dashed;border-color:black;margin-bottom:0.3rem;border-radius:10px 10px 10px 10px;border-width:1.5px">
                                                    <p class="responsive-font item-text" style="display:flex;justify-content:center;padding:4px;text-align:center;color:black;">{item.desc_check}</p>
                                                    <input type="hidden" class="identifier" value="{item.ordem_item}">
                                                    <input type="hidden" class="obrigatorio" name="obrigatorio" value="{item.obrigatorio}">
                                                    <div style="display:flex;justify-content:center;">
                                                       {str_buttons}
                                                    </div>
                                                    <div class="responsive-div" style="display:flex;justify-content:flex-start;margin:1rem 0.5rem 1rem 0.5rem">
                                                        <textarea name="{str_nome_botoes}" class="responsive-font responsive-w-100 textarea-check-post input-item relatos" style="width:90%;height:8rem;margin-right:1.2rem" disabled>{str_comentario}</textarea>
                                                    </div>
                                                </div>'''
                elif item.tipo_resposta == 2:
                    respostas_texto_fotos_check_aplicado = Item_Fotos_Texto_Check_Aplicado.objects.filter(
                        cod_check_aplicado=check_aplicado, cod_item_check=item).first()

                    if respostas_texto_fotos_check_aplicado is not None:
                        if respostas_texto_fotos_check_aplicado.comentario is not None:
                            str_comentario = respostas_texto_fotos_check_aplicado.comentario
                        else:
                            str_comentario = ''
                    else:
                        str_comentario = ''

                    if item.campo_obs_img == 0:
                        html_check_editar += f'''<div style="width:100%;border-style:dashed;border-color:black;margin-bottom:0.3rem;border-radius:10px 10px 10px 10px;border-width:1.5px">
                                                <p class="responsive-font item-text" style="display:flex;justify-content:center;padding:4px;text-align:center;color:black">{item.desc_check}</p>
                                                <input type="hidden" class="identifier" value="{item.ordem_item}">
                                                <input type="hidden" class="obrigatorio" name="obrigatorio" value="{item.obrigatorio}">
                                                <div class="responsive-div" style="display:flex;justify-content:center;margin:1rem 0.5rem 1rem 0.5rem">
                                                    <textarea name="{str_nome_botoes}" class="responsive-font responsive-w-100 textarea-check-post input-item relatos" style="width:90%;height:8rem;margin-right:1.2rem" disabled>{str_comentario}</textarea>
                                                </div>
                                            </div>'''
                    elif item.campo_obs_img == 1:
                        html_check_editar += f'''<div style="width:100%;border-style:dashed;border-color:black;margin-bottom:0.3rem;border-radius:10px 10px 10px 10px;border-width:1.5px">
                                                <p class="responsive-font item-text" style="display:flex;justify-content:center;padding:4px;text-align:center;color:black">{item.desc_check}</p>
                                                <input type="hidden" class="identifier" value="{item.ordem_item}">
                                                <input type="hidden" class="obrigatorio" name="obrigatorio" value="{item.obrigatorio}">
                                                <div class="responsive-div" style="display:flex;justify-content:center;margin:1rem 0.5rem 1rem 0.5rem">
                                                    <textarea name="{str_nome_botoes}" class="responsive-font responsive-w-100 textarea-check-post input-item relatos" style="width:90%;height:8rem;margin-right:1.2rem" disabled>{str_comentario}</textarea>
                                                </div>
                                            </div>'''
            html_check_editar += '</div>'

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario = Usuario.objects.get(pk=cod_usuario_sessao)
        plano_acao = Plano_Acao.objects.filter(cod_check_aplicado=check_aplicado).first()
        if plano_acao is None:
            plano_acao = Plano_Acao(
                cod_check_aplicado=check_aplicado,
                user_id=obj_usuario.cod_usu,
                data_registro=datetime.now(),
                status_plano=0,
            )
            plano_acao.save()
        if plano_acao.plano_acao is None:
            plano_acao.plano_acao = ''

        check_html_recebido = f'''
        <main id="main_container_safety" class="text-white justify-content-center align-items-center d-flex" style="flex-direction:column;">
            <div class="form-group form_div_check w-100" >
                <div class="col-md-12 w-100 h-100">
                    <form id="form_preenche_check" name="form_preenche_check">
                        <div class="tab-content" style="border-radius:0 0 10px 10px; font-size:15px">
                            <div class="tab-pane active" id="div_tab_new_check" role="tabpanel" aria-labelledby="a_tab_new_check">
                                <div style="text-align:left;">
                                    {html_check_editar}
                                </div>
                                <div class="d-flex justify-content-between align-items-between w-100" style="color:black;margin-top:30px;">
                                    <hr style="width:100%;margin-top:0 !important;opacity:0.7;">
                                </div>
                                
                                <div style="width:100%;border-style:dashed;border-color:black;margin-bottom:0.3rem;border-radius:10px 10px 10px 10px;border-width:1.5px">
                                    <p class="responsive-font item-text" style="display:flex;justify-content:center;padding:4px;text-align:center;color:black">Qual o plano de ação para tratar a ocorrência?</p>
                                    <div class="responsive-div" style="display:flex;justify-content:center;margin:1rem 0.5rem 1rem 0.5rem">
                                        <textarea name="{check_aplicado.cod_check_aplicado}" class="responsive-font responsive-w-100 textarea-check-aplicado" style="width:90%;height:8rem;margin-right:1.2rem">{plano_acao.plano_acao}</textarea>
                                    </div>
                                </div>
                                <div style="width:100%;border-style:dashed;border-color:black;margin-bottom:0.3rem;border-radius:10px 10px 10px 10px;border-width:1.5px">
                                    <p class="responsive-font item-text" style="display:flex;justify-content:center;padding:4px;text-align:center;color:black">Qual o status da tratativa?</p>
                                    <div style="display:flex;justify-content:center;padding-bottom:10px">
                                        <button name="{check_aplicado.cod_check_aplicado}" class="responsive-font pending-button-check status-button-check {'selected' if plano_acao.status_plano == 0 else ''}" type="button" style="padding:7px;border-width:1px;border-radius:5px;" value="0">PENDENTE</button>
                                        <button name="{check_aplicado.cod_check_aplicado}" class="responsive-font in-progress-button-check status-button-check {'selected' if plano_acao.status_plano == 1 else ''}" type="button" style="padding:7px;border-width:1px;border-radius:5px;" value="1">ANDAMENTO</button>
                                        <button name="{check_aplicado.cod_check_aplicado}" class="responsive-font finished-button-check status-button-check {'selected' if plano_acao.status_plano == 2 else ''}" type="button" style="padding:7px;border-width:1px;border-radius:5px;" value="2">CONCLUIDA</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </main>'''

        return HttpResponse(check_html_recebido)
