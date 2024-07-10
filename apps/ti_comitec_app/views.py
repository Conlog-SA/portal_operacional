from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.estrut_org_app.models import Atividade
from apps.help_desk_app.views import ConexaoHelpDesk
from apps.ti_comitec_app.models import Item_Gut, Ideia
from apps.usuario_app.models import Usuario
from datetime import datetime


# Create your views here.
class Frm_Cad_Ideias_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_usu_owners = Usuario.objects.filter(status_usu='A',tipo_colab__in=['L', 'H', 'M'])
        lista_usu_heads = Usuario.objects.filter(status_usu='A', tipo_colab='H')
        lista_usu_masters = Usuario.objects.filter(status_usu='A', tipo_colab='M')
        lista_atividades = Atividade.objects.all()
        lista_ideias_frm = Tabela_Ideias().carrega_tabela(obj_usuario_sessao)

        context = {
            'desc_menu': 'Comitec - Gerenciamento de idéias',
            'lista_usu_owners': lista_usu_owners,
            'lista_usu_heads': lista_usu_heads,
            'lista_usu_masters': lista_usu_masters,
            'lista_atividades': lista_atividades,
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_ideias_frm': lista_ideias_frm
        }
        return render(request, 'ti_comitec_app/frm_cad_ideias.html', context)

    def post(self, request):
        cod_ideia_frm = request.POST['cod_ideia']
        desc_ideia_frm = request.POST['desc_ideia']
        resumo_ideia_frm = request.POST['resumo_ideia']
        cod_atividade_frm = request.POST['cod_atividade']
        cod_usu_owner_frm = request.POST['cod_usu_owner']
        num_chamado_frm = request.POST['num_chamado']
        data_ideia_frm = request.POST['data_ideia']
        estimativa_val_ganhos_frm = request.POST['estimativa_val_ganhos']
        estimativa_desp_frm = request.POST['estimativa_desp']
        estimativa_ganhos_horas_frm = request.POST['estimativa_ganhos_horas']
        cod_usu_master_frm = request.POST['cod_usu_master']
        obs_usu_owner_frm = request.POST['obs_usu_owner']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        dic_usuario_sessao = {
            'cod_usu': obj_usuario_sessao.cod_usu,
            'tipo_colab_comitec': obj_usuario_sessao.tipo_colab
        }

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        obj_atv = Atividade.objects.get(pk=cod_atividade_frm)
        obj_usu_owner = Usuario.objects.get(pk=cod_usu_owner_frm)
        obj_usu_master = None
        if cod_usu_master_frm != '':
            obj_usu_master = Usuario.objects.get(pk=cod_usu_master_frm)
        if num_chamado_frm == '':
            num_chamado_frm = 0

        msg = ''
        try:
            if cod_ideia_frm > 0:
                obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
                obj_ideia.cod_chamado = num_chamado_frm
                obj_ideia.data_lancamento_idea = data_ideia_frm
                obj_ideia.desc_ideia = desc_ideia_frm
                obj_ideia.resumo_ideia = resumo_ideia_frm
                obj_ideia.val_ganhos = estimativa_val_ganhos_frm
                obj_ideia.val_despesas = estimativa_desp_frm
                obj_ideia.horas_ganhas = estimativa_ganhos_horas_frm
                obj_ideia.cod_status = 0
                obj_ideia.cod_atividade = obj_atv
                obj_ideia.cod_usu_master = obj_usu_master
                obj_ideia.cod_usu_owner = obj_usu_owner
                obj_ideia.obs_usu_owner = obs_usu_owner_frm
                obj_ideia.save()
                msg = 'Dados atualizados com sucesso!'
            else:
                obj_ideia = Ideia(
                    cod_chamado = num_chamado_frm,
                    data_lancamento_idea = data_ideia_frm,
                    desc_ideia = desc_ideia_frm,
                    resumo_ideia = resumo_ideia_frm,
                    val_ganhos = estimativa_val_ganhos_frm,
                    val_despesas = estimativa_desp_frm,
                    horas_ganhas = estimativa_ganhos_horas_frm,
                    cod_status = 0,
                    cod_atividade = obj_atv,
                    cod_usu_master = obj_usu_master,
                    cod_usu_owner = obj_usu_owner,
                    obs_usu_owner = obs_usu_owner_frm
                ).save()
                msg = 'Idéia adicionada com sucesso!'
        except Exception as e:
            msg = f'Erro ao adicionar nova ideia: {e}'

        lista_ideias_frm = Tabela_Ideias().carrega_tabela(obj_usuario_sessao)
        data = dict()
        data = {
            'msg': msg,
            'lista_ideias_frm': lista_ideias_frm,
            'dic_usuario_sessao': dic_usuario_sessao
        }
        return JsonResponse(data, safe=False)

class Frm_Cad_Item_Gut_View(View):
    def get(self, request):
        tipo_item_gut_frm = request.GET['tipo_item_gut']
        desc_head_modal_add_item_gut = ''
        icon_head_modal_add_item_gut = ''
        lista_itens_gut = list(Item_Gut.objects.filter(tipo=tipo_item_gut_frm)
                               .values('cod_item_gut', 'desc', 'peso', 'ativo', 'flag', 'color_flag'))
        if tipo_item_gut_frm == 'G':
            desc_head_modal_add_item_gut = 'Gravidade - Matriz GUT'
            icon_head_modal_add_item_gut = '<i class="fa-solid fa-g fa-2xl" style="color: #FFFFFF;"></i>'

        elif tipo_item_gut_frm == 'U':
            desc_head_modal_add_item_gut = 'Urgência - Matriz GUT'
            icon_head_modal_add_item_gut = '<i class="fa-solid fa-u fa-2xl" style="color: #FFFFFF;"></i>'
        elif tipo_item_gut_frm == 'T':
            desc_head_modal_add_item_gut = 'Tendência - Matriz GUT'
            icon_head_modal_add_item_gut = '<i class="fa-solid fa-t fa-2xl" style="color: #FFFFFF;"></i>'
        data = dict()
        data = {
            'desc_head_modal_add_item_gut': desc_head_modal_add_item_gut,
            'icon_head_modal_add_item_gut': icon_head_modal_add_item_gut,
            'lista_itens_gut': lista_itens_gut
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        desc_item_frm = request.POST['desc_item']
        peso_item_frm = request.POST['peso_item']
        tipo_item_frm = request.POST['tipo_item']

        msg = ''
        obj_item_gut = Item_Gut(
            desc = desc_item_frm,
            peso = peso_item_frm,
            tipo = tipo_item_frm
        ).save()
        msg = 'Item adicionado com sucesso!'
        lista_itens_gut = list(Item_Gut.objects.filter(tipo=tipo_item_frm)
                               .values('cod_item_gut', 'desc', 'peso', 'ativo', 'flag'))
        data = dict()
        data = {
            'lista_itens_gut': lista_itens_gut,
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Comp_Input_Chamado_View(View):
    def get(self, request):
        cod_chamado_frm = request.GET['cod_chamado']
        msg = ''
        dic_chamado = ConexaoHelpDesk().retorna_chamado_by_cod(cod_chamado_frm)
        if dic_chamado == None:
            msg = 'Chamado não encontrato'
        else:
            msg = 'Análise os dados informados no chamado'
        data = dict()
        data = {
            'dic_chamado': dic_chamado,
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Frm_Edit_Ideia_View(View):
    def get(self, request):
        cod_ideia_comitec_frm = request.GET['cod_ideia_comitec']
        obj_ideia = Ideia.objects.get(pk=cod_ideia_comitec_frm)

        flag_gut_g = 'fa-regular fa-flag'
        color_gut_g = '#FFFFFF;'
        peso_gut_g = 0
        if obj_ideia.cod_gut_g != None:
            flag_gut_g = obj_ideia.cod_gut_g.flag
            color_gut_g =  obj_ideia.cod_gut_g.color_flag
            peso_gut_g =  obj_ideia.cod_gut_g.peso

        flag_gut_u = 'fa-regular fa-flag'
        color_gut_u = '#FFFFFF;'
        peso_gut_u = 0
        if obj_ideia.cod_gut_u != None:
            flag_gut_u = obj_ideia.cod_gut_u.flag
            color_gut_u = obj_ideia.cod_gut_u.color_flag
            peso_gut_u = obj_ideia.cod_gut_u.peso

        flag_gut_t = 'fa-regular fa-flag'
        color_gut_t = '#FFFFFF;'
        peso_gut_t = 0
        if obj_ideia.cod_gut_t != None:
            flag_gut_t = obj_ideia.cod_gut_t.flag
            color_gut_t = obj_ideia.cod_gut_t.color_flag
            peso_gut_t = obj_ideia.cod_gut_t.peso

        cod_usu_master = 0
        obs_usu_master = ''
        if obj_ideia.cod_usu_master != None:
            cod_usu_master =  obj_ideia.cod_usu_master.cod_usu
            obs_usu_master = obj_ideia.obs_usu_master

        cod_usu_head = 0
        nota_head = 0
        obs_usu_head = ''
        if obj_ideia.cod_usu_head != None:
            cod_usu_head = obj_ideia.cod_usu_head.cod_usu
            nota_head =  obj_ideia.nota_head
            obs_usu_head =  obj_ideia.obs_usu_head

        ideia_dic = {
            'flag_gut_g': flag_gut_g,
            'color_gut_g': color_gut_g,
            'peso_gut_g': peso_gut_g,

            'flag_gut_u': flag_gut_u,
            'color_gut_u': color_gut_u,
            'peso_gut_u': peso_gut_u,

            'flag_gut_t': flag_gut_t,
            'color_gut_t': color_gut_t,
            'peso_gut_t': peso_gut_t,

            'nota_gut_tt': peso_gut_g + peso_gut_u + peso_gut_t,
            'cod_ideia': obj_ideia.cod_ideia,
            'cod_chamado': obj_ideia.cod_chamado,
            'desc_ideia': obj_ideia.desc_ideia,
            'resumo_ideia': obj_ideia.resumo_ideia,
            'cod_atividade': obj_ideia.cod_atividade.cod_atividade,
            'cod_usu_owner': obj_ideia.cod_usu_owner.cod_usu,
            'data_lancamento_idea': obj_ideia.data_lancamento_idea,
            'val_ganhos': obj_ideia.val_ganhos,
            'val_despesas': obj_ideia.val_despesas,
            'horas_ganhas': obj_ideia.horas_ganhas,
            'obs_usu_owner': obj_ideia.obs_usu_owner,
            'cod_usu_master': cod_usu_master,
            'obs_usu_master': obs_usu_master,
            'cod_usu_head': cod_usu_head,
            'nota_head': nota_head,
            'obs_usu_head': obs_usu_head
        }

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        obj_usu_dic = {
            'cod_usu_sessao': obj_usuario_sessao.cod_usu,
            'login_usu_sessao': obj_usuario_sessao.login_usu,
            'tipo_colab_comitec': obj_usuario_sessao.tipo_colab
        }

        data = dict()
        data = {
            'ideia_dic': ideia_dic,
            'obj_usu_dic': obj_usu_dic
        }
        return JsonResponse(data, safe=False)

class Frm_Pontua_Item_Gut_View( View):
    def get(self, request):
        tipo_item_gut_frm = request.GET['tipo_item_gut']
        lista_itens_gut = list(Item_Gut.objects
                               .filter(tipo=tipo_item_gut_frm, ativo='S')
                               .values('cod_item_gut', 'desc', 'peso', 'flag', 'color_flag'))

        if tipo_item_gut_frm == 'G':
            desc_head_modal_add_item_gut = 'Gravidade - Matriz GUT'
            icon_head_modal_add_item_gut = '<i class="fa-solid fa-g fa-2xl" style="color: #FFFFFF;"></i>'

        elif tipo_item_gut_frm == 'U':
            desc_head_modal_add_item_gut = 'Urgência - Matriz GUT'
            icon_head_modal_add_item_gut = '<i class="fa-solid fa-u fa-2xl" style="color: #FFFFFF;"></i>'
        elif tipo_item_gut_frm == 'T':
            desc_head_modal_add_item_gut = 'Tendência - Matriz GUT'
            icon_head_modal_add_item_gut = '<i class="fa-solid fa-t fa-2xl" style="color: #FFFFFF;"></i>'

        data = dict()
        data = {
            'desc_head_modal_add_item_gut': desc_head_modal_add_item_gut,
            'icon_head_modal_add_item_gut': icon_head_modal_add_item_gut,
            'lista_itens_gut': lista_itens_gut,

        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_ideia_frm = request.POST['cod_ideia']
        cod_tipo_item_gut_frm = request.POST['cod_tipo_item_gut']
        desc_tipo_item_gut = request.POST['desc_tipo_item_gut']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
        obj_item_gut = Item_Gut.objects.get(pk=cod_tipo_item_gut_frm, tipo=desc_tipo_item_gut)
        nota_item_gut_g = 0
        nota_item_gut_u = 0
        nota_item_gut_t = 0
        if desc_tipo_item_gut == 'G':
            obj_ideia.cod_gut_g = obj_item_gut
        if desc_tipo_item_gut == 'U':
            obj_ideia.cod_gut_u = obj_item_gut
        if desc_tipo_item_gut == 'T':
            obj_ideia.cod_gut_t = obj_item_gut
        obj_ideia.save()

        if obj_ideia.cod_gut_g != None:
            nota_item_gut_g = obj_ideia.cod_gut_g.peso
        if obj_ideia.cod_gut_u != None:
            nota_item_gut_u = obj_ideia.cod_gut_u.peso
        if obj_ideia.cod_gut_t != None:
            nota_item_gut_t = obj_ideia.cod_gut_t.peso
        nota_total_gut = nota_item_gut_g + nota_item_gut_u + nota_item_gut_t

        lista_ideias_frm = Tabela_Ideias().carrega_tabela(obj_usuario_sessao)
        data = dict()
        data = {
            'flag_item_gut': obj_item_gut.flag,
            'color_flag_gut': obj_item_gut.color_flag,
            'peso_item_gut': obj_item_gut.peso,
            'nota_total_gut': nota_total_gut,
            'lista_ideias_frm': lista_ideias_frm
        }
        return JsonResponse(data, safe=False)


class Frm_Avaliacao_Master_View(View):
    def post(self, request):
        cod_ideia_frm = request.POST['cod_ideia']
        cod_usu_master_frm = request.POST['cod_usu_master']
        obs_usu_master_frm = request.POST['obs_usu_master']

        obj_usu_master = Usuario.objects.get(pk=cod_usu_master_frm)

        obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
        obj_ideia.cod_usu_master = obj_usu_master
        obj_ideia.obs_usu_master = obs_usu_master_frm
        obj_ideia.save()
        data = dict()
        data = {
            'msg': 'Parecer técnico registrado'
        }
        return JsonResponse(data, safe=False)


class Frm_Avaliacao_Head_View(View):
    def post(self, request):
        cod_ideia_frm = request.POST['cod_ideia']
        cod_usu_head_frm = request.POST['cod_usu_head']
        nota_head_frm = request.POST['nota_head']
        obs_usu_head_frm = request.POST['obs_usu_head']

        obj_usu_head = Usuario.objects.get(pk=cod_usu_head_frm)

        obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
        obj_ideia.cod_usu_head = obj_usu_head
        obj_ideia.nota_head = nota_head_frm
        obj_ideia.obs_usu_head = obs_usu_head_frm
        obj_ideia.save()
        data = dict()
        data = {
            'msg': 'Parecer do head registrado'
        }
        return JsonResponse(data, safe=False)





class Tabela_Ideias():
    def carrega_tabela(self, obj_usuario):
        lista_ideias_frm = []
        lista_ideias = None
        if obj_usuario.tipo_colab == 'L':
            lista_ideias = Ideia.objects.filter(cod_status=0, cod_usu_owner=obj_usuario)
        elif obj_usuario.tipo_colab == 'M':
            lista_ideias = Ideia.objects.filter(cod_status=0, cod_usu_master=obj_usuario)
        elif obj_usuario.tipo_colab == 'H':
            lista_ideias = (Ideia.objects
                            .filter((Q(cod_usu_head=obj_usuario) | Q(cod_usu_head__isnull=True)),
                                    cod_status=0))
        elif obj_usuario.tipo_colab == 'G':
            lista_ideias = (Ideia.objects
                            .filter(cod_status=0))

        for i in lista_ideias:
            nota_gut_g = 0
            nota_gut_u = 0
            nota_gut_t = 0
            nota_head = 0
            login_head = ''
            obs_usu_head = ''
            login_master = ''
            flag_gut_g = 'fa-regular fa-flag'
            flag_gut_u = 'fa-regular fa-flag'
            flag_gut_t = 'fa-regular fa-flag'
            color_flag_gut_g = '#FFFFFF;'
            color_flag_gut_u = '#FFFFFF;'
            color_flag_gut_t = '#FFFFFF;'
            if i.cod_gut_g != None:
                nota_gut_g = i.cod_gut_g.peso
                flag_gut_g = i.cod_gut_g.flag
                color_flag_gut_g = i.cod_gut_g.color_flag
            if i.cod_gut_u != None:
                nota_gut_u = i.cod_gut_u.peso
                flag_gut_u = i.cod_gut_u.flag
                color_flag_gut_u = i.cod_gut_u.color_flag
            if i.cod_gut_t != None:
                nota_gut_t = i.cod_gut_t.peso
                flag_gut_t = i.cod_gut_t.flag
                color_flag_gut_t = i.cod_gut_t.color_flag
            if i.cod_usu_head != None:
                nota_head = i.nota_head
                login_head = i.cod_usu_head.login_usu
                obs_usu_head = i.obs_usu_head
            nota_gut = nota_gut_g + nota_gut_u + nota_gut_t
            tt_nota = nota_gut + nota_head

            if i.cod_usu_master != None:
                login_master = i.cod_usu_master.login_usu
            ideia = {
                'flag_gut_g': flag_gut_g,
                'flag_gut_u': flag_gut_u,
                'flag_gut_t': flag_gut_t,
                'color_flag_gut_g': color_flag_gut_g,
                'color_flag_gut_u': color_flag_gut_u,
                'color_flag_gut_t': color_flag_gut_t,
                'nota_gut_g': nota_gut_g,
                'nota_gut_u': nota_gut_u,
                'nota_gut_t': nota_gut_t,
                'cod_status': i.cod_status,
                'nome_empresa': i.cod_usu_owner.cod_filial.cod_empresa.cod_empresa,
                'desc_area': i.cod_atividade.desc1_atividade,
                'resumo_ideia': i.resumo_ideia,
                'login_owner': i.cod_usu_owner.login_usu,
                'login_master': login_master,
                'login_head': login_head,
                'nota_gut': nota_gut,
                'nota_head': nota_head,
                'nota_total': tt_nota,
                'cod_ideia': i.cod_ideia
            }
            lista_ideias_frm.append(ideia)

        return lista_ideias_frm
