from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import QueryDict

from apps.help_desk_app.views import ConexaoHelpDesk
from apps.ti_comitec_app.models import Item_Gut, Ideia, Projeto, Atividade, Usuarios_Projeto
from apps.usuario_app.models import Usuario
from apps.estrut_org_app.models import Atividade as atv
from datetime import datetime, timedelta

from django.utils import timezone
data_atual = timezone.now()

# Create your views here.
class Frm_Cad_Ideias_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_usu_owners = Usuario.objects.filter(status_usu='A',tipo_colab__in=['L', 'H', 'M'])
        lista_usu_heads = Usuario.objects.filter(status_usu='A', tipo_colab='H')
        lista_usu_masters = Usuario.objects.filter(status_usu='A', tipo_colab='M')
        lista_atividades = atv.objects.all()
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

        obj_atv = atv.objects.get(pk=cod_atividade_frm)
        obj_usu_owner = Usuario.objects.get(pk=cod_usu_owner_frm)
        obj_usu_master = None
        if cod_usu_master_frm != '':
            obj_usu_master = Usuario.objects.get(pk=cod_usu_master_frm)
        if num_chamado_frm == '':
            num_chamado_frm = 0
        if estimativa_val_ganhos_frm == '':
            estimativa_val_ganhos_frm = 0.00
        else:
            estimativa_val_ganhos_frm = estimativa_val_ganhos_frm.replace('.','').replace(',','.')
        if estimativa_desp_frm == '':
            estimativa_desp_frm = 0.00
        else:
            estimativa_desp_frm = estimativa_desp_frm.replace('.', '').replace(',', '.')
        if estimativa_ganhos_horas_frm == '':
            estimativa_ganhos_horas_frm = 0

        msg = ''
        try:
            if int(cod_ideia_frm) > 0:
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
                )
                obj_ideia.save()
                cod_ideia_frm = obj_ideia.cod_ideia
                msg = 'Idéia adicionada com sucesso!'
        except Exception as e:
            msg = f'Erro ao adicionar nova ideia: {e}'

        lista_ideias_frm = Tabela_Ideias().carrega_tabela(obj_usuario_sessao)
        data = dict()
        data = {
            'msg': msg,
            'lista_ideias_frm': lista_ideias_frm,
            'dic_usuario_sessao': dic_usuario_sessao,
            'cod_ideia': cod_ideia_frm
        }
        return JsonResponse(data, safe=False)

class Frm_Lista_Projetos_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        lista_dic_proj = []
        lista_obj_projetos = []
        if obj_usuario_sessao.tipo_colab in ('H', 'G'):
            lista_obj_projetos = Projeto.objects.all()
        else:
            lista_obj_usu_projetos = Usuarios_Projeto.objects.filter(cod_usu=obj_usuario_sessao)
            for proj in lista_obj_usu_projetos:
                lista_obj_projetos.append(proj.cod_projeto)

        contador = 0
        col = 0
        lista_col = []
        for obj_proj in lista_obj_projetos:
            if contador % 3 == 0:
                col += 1
                lista_col.append(col)

            perc_progresso_proj = self.calcula_progresso_projeto(obj_proj)
            status_cronograma_proj = self.verifica_status_cronograma_proj(obj_proj)
            obj_proj.status_cronograma_proj = status_cronograma_proj
            obj_proj.save()

            '''Verifica prazo última ação do projeto'''
            obj_ultima_acao = Atividade.objects.filter(cod_projeto=obj_proj, tipo_atividade='A').last()
            dt_prazo_proj = ''
            if obj_ultima_acao != None:
                dt_prazo_proj = obj_ultima_acao.data_fim

            foto_owner = 'https://operacional.conlogsa.com.br/media/fotos/avatar.png'
            if obj_proj.cod_ideia.cod_usu_owner.caminho_foto != None:
                foto_owner = 'https://operacional.conlogsa.com.br/media/' + obj_proj.cod_ideia.cod_usu_owner.caminho_foto

            foto_sponsor = 'https://operacional.conlogsa.com.br/media/fotos/avatar.png'
            if obj_proj.cod_ideia.cod_usu_master.caminho_foto != None:
                foto_sponsor = 'https://operacional.conlogsa.com.br/media/' + obj_proj.cod_ideia.cod_usu_master.caminho_foto

            lista_dic_usu_envolvidos = []
            lista_obj_usu_envolvidos = Usuarios_Projeto.objects.filter(cod_projeto=obj_proj)
            for obj_usu_proj in lista_obj_usu_envolvidos:
                foto_user = 'https://operacional.conlogsa.com.br/media/fotos/avatar.png'
                if obj_usu_proj.cod_usu.caminho_foto != None:
                    foto_user = 'https://operacional.conlogsa.com.br/media/' + obj_usu_proj.cod_usu.caminho_foto
                reg_usu = {
                    'login_usu': obj_usu_proj.cod_usu.login_usu,
                    'foto_user': foto_user
                }
                lista_dic_usu_envolvidos.append(reg_usu)

            proj = {
                'resumo_ideia': obj_proj.cod_ideia.resumo_ideia,
                'desc_area': obj_proj.cod_ideia.cod_atividade.desc1_atividade,
                'login_owner': obj_proj.cod_ideia.cod_usu_owner.login_usu,
                'foto_owner': foto_owner,
                'login_sponsor': obj_proj.cod_ideia.cod_usu_master.login_usu,
                'foto_sponsor': foto_sponsor,
                'data_ini': obj_proj.data_ini,
                'data_prazo': dt_prazo_proj,
                'data_fim': obj_proj.data_fim,
                'data_atualizacao': obj_proj.data_atualizacao,
                'status_proj': 'Concluído' if obj_proj.status_proj == 1 else 'Em andamento',
                'status_cronograma_proj': obj_proj.status_cronograma_proj,
                'perc_progresso_proj': perc_progresso_proj,
                'cod_projeto': obj_proj.cod_projeto,
                'lista_dic_usu_envolvidos': lista_dic_usu_envolvidos,
                'col': col
            }
            lista_dic_proj.append(proj)
            contador += 1

        lista_obj_acoes_prox_ou_atradadas = self.retorna_prox_acoes_proj(obj_usuario_sessao, lista_obj_projetos)


        context = {
            'lista_projetos': lista_dic_proj,
            'lista_col': lista_col,
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_obj_acoes_prox_ou_atradadas': lista_obj_acoes_prox_ou_atradadas
        }

        return render(request, 'ti_comitec_app/frm_lista_projetos.html', context)


    def calcula_progresso_projeto(self, obj_proj):
        qtd_tt_acoes = (Atividade.objects.filter(cod_projeto=obj_proj, tipo_atividade='A').count())

        qtd_acoes_concluidas = (Atividade.objects
                                .filter(cod_projeto=obj_proj, tipo_atividade='A',
                                        data_conclusao__isnull=False).count())

        perc_progresso_acoes = 0
        try:
            perc_progresso_acoes = int((qtd_acoes_concluidas / qtd_tt_acoes) * 100)
        except:
            perc_progresso_acoes = 0

        return perc_progresso_acoes

    def verifica_status_cronograma_proj(self, obj_proj):
        status = 0
        '''Verifica se o projeto está atrasado'''
        obj_ultima_acao = Atividade.objects.filter(cod_projeto=obj_proj, tipo_atividade='A').last()
        if obj_ultima_acao:
            if obj_ultima_acao.data_conclusao is None and obj_ultima_acao.data_fim < datetime.now().date():
                status = 2
            elif obj_ultima_acao.data_conclusao != None and obj_ultima_acao.data_conclusao > obj_ultima_acao.data_fim:
                status = 2
        '''Verifica se o projeto está em risco'''
        lista_obj_acoes =  Atividade.objects.filter(cod_projeto=obj_proj, tipo_atividade='A')
        for obj_acao in lista_obj_acoes:
            if obj_ultima_acao:
                if obj_acao.data_conclusao is None and obj_acao.data_fim < datetime.now().date():
                    status = 1
                elif obj_acao.data_conclusao != None and obj_acao.data_conclusao > obj_acao.data_fim:
                    status = 1

        return status


    def retorna_prox_acoes_proj(self, obj_usuario_sessao, lista_obj_projetos):
        data_hora_atual = datetime.now()
        lista_obj_acoes_prox_ou_atradadas = []
        if obj_usuario_sessao.tipo_colab in ('L', 'M'):
            '''Ações atrasadas'''
            lista_obj_acoes_atrasadas = Atividade.objects.filter(
                tipo_atividade='A', data_conclusao__isnull=True, data_fim__lt=data_hora_atual,
                cod_usu=obj_usuario_sessao
            )
            for acao_atrasada in lista_obj_acoes_atrasadas:
                status_acao = Frm_Acao_View().retorna_status_acao(acao_atrasada)
                acao = {
                    'status': status_acao,
                    'login_master': acao_atrasada.cod_usu.login_usu,
                    'desc_projeto': acao_atrasada.cod_projeto.cod_ideia.resumo_ideia,
                    'cronograma_projeto': acao_atrasada.cod_projeto.status_cronograma_proj,
                    'desc_acao': acao_atrasada.desc_atividade,
                    'prazo': datetime.strftime(acao_atrasada.data_fim, '%d-%m-%Y'),
                    'cod_projeto': acao_atrasada.cod_projeto.cod_projeto,
                    'data_ultima_atualizacao_proj': datetime.strftime(acao_atrasada.cod_projeto.data_atualizacao, '%d-%m-%Y %H:%M')
                }
                lista_obj_acoes_prox_ou_atradadas.append(acao)

            for proj in lista_obj_projetos:
                if proj.status_proj == 0:
                    '''Proximas ações'''
                    obj_prox_acoes_proj = Atividade.objects.filter(
                        tipo_atividade='A', data_conclusao__isnull=True, data_fim__gt=data_hora_atual,
                        cod_projeto=proj,
                        cod_usu=obj_usuario_sessao
                    ).first()
                    if obj_prox_acoes_proj != None:
                        status_acao = Frm_Acao_View().retorna_status_acao(obj_prox_acoes_proj)
                        acao = {
                            'status': status_acao,
                            'login_master': obj_prox_acoes_proj.cod_usu.login_usu,
                            'desc_projeto': obj_prox_acoes_proj.cod_projeto.cod_ideia.resumo_ideia,
                            'cronograma_projeto': obj_prox_acoes_proj.cod_projeto.status_cronograma_proj,
                            'desc_acao': obj_prox_acoes_proj.desc_atividade,
                            'prazo': datetime.strftime(obj_prox_acoes_proj.data_fim, '%d-%m-%Y'),
                            'cod_projeto': obj_prox_acoes_proj.cod_projeto.cod_projeto,
                            'data_ultima_atualizacao_proj': datetime.strftime(obj_prox_acoes_proj.cod_projeto.data_atualizacao, '%d-%m-%Y %H:%M')
                        }
                        lista_obj_acoes_prox_ou_atradadas.append(acao)
                    '''Ações no dia corrrente'''
                    obj_dia_corrente_acoes_proj = Atividade.objects.filter(
                        tipo_atividade='A', data_conclusao__isnull=True, data_fim=data_hora_atual,
                        cod_projeto=proj,
                        cod_usu=obj_usuario_sessao
                    )
                    for acao_hj in obj_dia_corrente_acoes_proj:
                        status_acao = Frm_Acao_View().retorna_status_acao(acao_hj)
                        acao = {
                            'status': status_acao,
                            'login_master': acao_hj.cod_usu.login_usu,
                            'desc_projeto': acao_hj.cod_projeto.cod_ideia.resumo_ideia,
                            'cronograma_projeto': acao_hj.cod_projeto.status_cronograma_proj,
                            'desc_acao': acao_hj.desc_atividade,
                            'prazo': datetime.strftime(acao_hj.data_fim, '%d-%m-%Y'),
                            'cod_projeto': acao_hj.cod_projeto.cod_projeto,
                            'data_ultima_atualizacao_proj': datetime.strftime(
                                acao_hj.cod_projeto.data_atualizacao, '%d-%m-%Y %H:%M')
                        }
                        lista_obj_acoes_prox_ou_atradadas.append(acao)

        else:
            '''Ações atrasadas'''
            lista_obj_acoes_atrasadas = Atividade.objects.filter(
                tipo_atividade='A', data_conclusao__isnull=True, data_fim__lt=data_hora_atual
            )
            for acao_atrasada in lista_obj_acoes_atrasadas:
                status_acao = Frm_Acao_View().retorna_status_acao(acao_atrasada)
                acao = {
                    'status': status_acao,
                    'login_master': acao_atrasada.cod_usu.login_usu,
                    'desc_projeto': acao_atrasada.cod_projeto.cod_ideia.resumo_ideia,
                    'cronograma_projeto': acao_atrasada.cod_projeto.status_cronograma_proj,
                    'desc_acao': acao_atrasada.desc_atividade,
                    'prazo': datetime.strftime(acao_atrasada.data_fim, '%d-%m-%Y'),
                    'cod_projeto': acao_atrasada.cod_projeto.cod_projeto,
                    'data_ultima_atualizacao_proj': datetime.strftime(acao_atrasada.cod_projeto.data_atualizacao, '%d-%m-%Y %H:%M')
                }
                lista_obj_acoes_prox_ou_atradadas.append(acao)
            for proj in lista_obj_projetos:
                if proj.status_proj == 0:
                    '''Proximas ações'''
                    obj_prox_acoes_proj = Atividade.objects.filter(
                        tipo_atividade='A', data_conclusao__isnull=True, data_fim__gte=data_hora_atual,
                        cod_projeto=proj
                    ).first()
                    if obj_prox_acoes_proj != None:
                        status_acao = Frm_Acao_View().retorna_status_acao(obj_prox_acoes_proj)
                        acao = {
                            'status': status_acao,
                            'login_master': obj_prox_acoes_proj.cod_usu.login_usu,
                            'desc_projeto': obj_prox_acoes_proj.cod_projeto.cod_ideia.resumo_ideia,
                            'cronograma_projeto': obj_prox_acoes_proj.cod_projeto.status_cronograma_proj,
                            'desc_acao': obj_prox_acoes_proj.desc_atividade,
                            'prazo': datetime.strftime(obj_prox_acoes_proj.data_fim, '%d-%m-%Y'),
                            'cod_projeto': obj_prox_acoes_proj.cod_projeto.cod_projeto,
                            'data_ultima_atualizacao_proj': datetime.strftime(obj_prox_acoes_proj.cod_projeto.data_atualizacao, '%d-%m-%Y %H:%M')
                        }
                        lista_obj_acoes_prox_ou_atradadas.append(acao)
                    '''Ações no dia corrrente'''
                    obj_dia_corrente_acoes_proj = Atividade.objects.filter(
                        tipo_atividade='A', data_conclusao__isnull=True, data_fim=data_hora_atual,
                        cod_projeto=proj,
                        cod_usu=obj_usuario_sessao
                    )
                    for acao_hj in obj_dia_corrente_acoes_proj:
                        status_acao = Frm_Acao_View().retorna_status_acao(acao_hj)
                        acao = {
                            'status': status_acao,
                            'login_master': acao_hj.cod_usu.login_usu,
                            'desc_projeto': acao_hj.cod_projeto.cod_ideia.resumo_ideia,
                            'cronograma_projeto': acao_hj.cod_projeto.status_cronograma_proj,
                            'desc_acao': acao_hj.desc_atividade,
                            'prazo': datetime.strftime(acao_hj.data_fim, '%d-%m-%Y'),
                            'cod_projeto': acao_hj.cod_projeto.cod_projeto,
                            'data_ultima_atualizacao_proj': datetime.strftime(
                                acao_hj.cod_projeto.data_atualizacao, '%d-%m-%Y %H:%M')
                        }
                        lista_obj_acoes_prox_ou_atradadas.append(acao)

        return lista_obj_acoes_prox_ou_atradadas




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
        cod_usu_head = 0
        obs_usu_head = ''
        nota_head = 0
        if obj_ideia.cod_usu_master != None:
            cod_usu_master =  obj_ideia.cod_usu_master.cod_usu
            obs_usu_master = obj_ideia.obs_usu_master
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

            'nota_gut_tt': peso_gut_g * peso_gut_u * peso_gut_t,
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
        data_atual = datetime.now()

        obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
        obj_item_gut = Item_Gut.objects.get(pk=cod_tipo_item_gut_frm, tipo=desc_tipo_item_gut)
        obj_ideia.data_nota_gut = data_atual
        obj_ideia.cod_usu_head = obj_usuario_sessao
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
        nota_total_gut = nota_item_gut_g * nota_item_gut_u * nota_item_gut_t

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
        data_atual = datetime.now()

        obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
        obj_ideia.cod_usu_head = obj_usu_head
        obj_ideia.nota_head = nota_head_frm
        obj_ideia.obs_usu_head = obs_usu_head_frm
        obj_ideia.data_nota_head = data_atual
        obj_ideia.save()

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        lista_ideias_frm = Tabela_Ideias().carrega_tabela(obj_usuario_sessao)
        data = dict()
        data = {
            'msg': 'Parecer do head registrado',
            'lista_ideias_frm': lista_ideias_frm
        }
        return JsonResponse(data, safe=False)





class Tabela_Ideias():
    def carrega_tabela(self, obj_usuario):
        lista_ideias_frm = []
        lista_ideias = Ideia.objects.filter(cod_status=0)
        '''if obj_usuario.tipo_colab == 'L':
            lista_ideias = Ideia.objects.filter(cod_status=0, cod_usu_owner=obj_usuario)
        elif obj_usuario.tipo_colab == 'M':
            lista_ideias = Ideia.objects.filter(cod_status=0, cod_usu_master=obj_usuario)
        elif obj_usuario.tipo_colab == 'H':
            lista_ideias = (Ideia.objects
                            .filter((Q(cod_usu_head=obj_usuario) | Q(cod_usu_head__isnull=True)),
                                    cod_status=0))
        elif obj_usuario.tipo_colab == 'G':
            lista_ideias = (Ideia.objects.filter(cod_status=0))'''

        for i in lista_ideias:
            nota_gut_g = 0
            nota_gut_u = 0
            nota_gut_t = 0
            nota_head = 0
            desc_gut_g = ''
            desc_gut_u = ''
            desc_gut_t = ''
            tt_nota = 0
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
                desc_gut_g = i.cod_gut_g.desc
            if i.cod_gut_u != None:
                nota_gut_u = i.cod_gut_u.peso
                flag_gut_u = i.cod_gut_u.flag
                color_flag_gut_u = i.cod_gut_u.color_flag
                desc_gut_u = i.cod_gut_u.desc
            if i.cod_gut_t != None:
                nota_gut_t = i.cod_gut_t.peso
                flag_gut_t = i.cod_gut_t.flag
                color_flag_gut_t = i.cod_gut_t.color_flag
                desc_gut_t = i.cod_gut_t.desc
            if i.cod_usu_head != None:
                nota_head = i.nota_head
                login_head = i.cod_usu_head.login_usu
                obs_usu_head = i.obs_usu_head
            nota_gut = nota_gut_g * nota_gut_u * nota_gut_t
            if nota_head > 0:
                tt_nota = nota_gut * nota_head
            else:
                tt_nota = nota_gut

            if i.cod_usu_master != None:
                login_master = i.cod_usu_master.login_usu

            empresa_usu = 'CONLOG'
            if i.cod_usu_owner.cod_filial.cod_empresa.cod_empresa == 17:
                empresa_usu = 'DEEP'
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
                'nome_empresa': empresa_usu,
                'desc_area': i.cod_atividade.desc1_atividade,
                'resumo_ideia': i.resumo_ideia,
                'login_owner': i.cod_usu_owner.login_usu,
                'login_master': login_master,
                'login_head': login_head,
                'nota_gut': nota_gut,
                'nota_head': nota_head,
                'nota_total': tt_nota,
                'cod_ideia': i.cod_ideia,
                'cod_usu_owner': i.cod_usu_owner.cod_usu,
                'desc_gut_g': desc_gut_g,
                'desc_gut_u': desc_gut_u,
                'desc_gut_t': desc_gut_t
            }
            lista_ideias_frm.append(ideia)

        return lista_ideias_frm


class Frm_Edita_Projetos_Ideia_View(View):
    def get(self, request):
        tipo_processo_frm = request.GET['tipo_processo']
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        data_hora_atual = datetime.now()
        data_hora = data_hora_atual.strftime('%d-%m-%Y')

        lista_usuarios = list(
            Usuario.objects.filter(status_usu='A', tipo_colab__in=['L', 'M', 'H', 'G']).values('cod_usu', 'login_usu', 'nome_usu'))

        data = dict()
        dic_projeto = None
        if tipo_processo_frm == 'novo':
            cod_ideia_frm = request.GET['cod_ideia']
            obj_ideia = Ideia.objects.get(pk=cod_ideia_frm)
            obj_ideia.cod_status = 1
            obj_ideia.save()

            obj_novo_projeto = Projeto(
                data_atualizacao = data_hora_atual,
                cod_ideia = obj_ideia,
                cod_usu=obj_usuario_sessao,
                data_ini = data_hora
            )
            obj_novo_projeto.save()



            '''Vincula usuarios owner,master e head ao projeto'''
            if obj_ideia.cod_usu_owner != None:
                obj_usu_proj = Usuarios_Projeto(
                    envia_email=1,
                    cod_usu=obj_ideia.cod_usu_owner,
                    cod_projeto=obj_novo_projeto
                ).save()
            if obj_ideia.cod_usu_master != None:
                obj_usu_proj = (Usuarios_Projeto.objects
                                .filter(cod_usu=obj_ideia.cod_usu_master, cod_projeto=obj_novo_projeto).first())
                if obj_usu_proj == None:
                    obj_usu_proj = Usuarios_Projeto(
                        envia_email=1,
                        cod_usu=obj_ideia.cod_usu_master,
                        cod_projeto=obj_novo_projeto
                    ).save()
            if obj_ideia.cod_usu_head != None:
                obj_usu_proj = (Usuarios_Projeto.objects
                                .filter(cod_usu=obj_ideia.cod_usu_head, cod_projeto=obj_novo_projeto).first())
                if obj_usu_proj == None:
                    obj_usu_proj = Usuarios_Projeto(
                        envia_email=1,
                        cod_usu=obj_ideia.cod_usu_head,
                        cod_projeto=obj_novo_projeto
                    ).save()


            lista_ideias_frm = Tabela_Ideias().carrega_tabela(obj_usuario_sessao)

            data = {
                'lista_ideias_frm': lista_ideias_frm,
                'lista_usuarios': lista_usuarios,
                'msg': 'Projeto criado com sucesso!!! Agora, acesse a aba Projetos e inicie o planejamento!'

            }


        elif tipo_processo_frm == 'edicao':
            cod_projeto_frm = request.GET['cod_projeto']
            obj_proj = Projeto.objects.get(pk=cod_projeto_frm)

            lista_obj_tarefas = (Atividade.objects
                                 .filter(cod_projeto=obj_proj, tipo_atividade='T'))#.values('cod_atividade', 'desc_atividade', 'cod_usu__cod_usu', 'cod_usu__login_usu'))

            ultima_tarefa = ' '
            obj_ultima_tarefa = (
                Atividade.objects.filter(cod_projeto=obj_proj, tipo_atividade='T').order_by(
                    'cod_atividade').last())

            if obj_ultima_tarefa:
                obj_ultima_acao = (
                    Atividade.objects.filter(tipo_atividade='A', cod_projeto=obj_proj)
                    .order_by('cod_atividade').last())

                if obj_ultima_acao != None:
                    if obj_ultima_acao.data_fim != None:
                        ultima_tarefa = datetime.strftime(obj_ultima_acao.data_fim, '%d-%m-%Y')


            '''Cálculo progresso das ações geral'''
            perc_progresso_acoes = Frm_Lista_Projetos_View().calcula_progresso_projeto(obj_proj)

            lista_dic_tarefas = []
            for tarefa in lista_obj_tarefas:
                status_tarefa = 'Em andamento'

                data_ini_tarefa = '-'
                obj_primeira_acao = (
                    Atividade.objects.filter(tipo_atividade='A', cod_atividade_pai=tarefa.cod_atividade)
                    .order_by('cod_atividade').first())

                if obj_primeira_acao != None:
                    if obj_primeira_acao.data_ini != None:
                        data_ini_tarefa = datetime.strftime(obj_primeira_acao.data_ini, '%d-%m-%Y')


                data_prazo_tarefa = '-'
                data_termino_tarefa = '-'
                obj_ultima_acao = (
                    Atividade.objects.filter(tipo_atividade='A', cod_atividade_pai=tarefa.cod_atividade)
                    .order_by('cod_atividade').last())
                if obj_ultima_acao != None:
                    if obj_ultima_acao.data_fim != None:
                        data_prazo_tarefa = datetime.strftime(obj_ultima_acao.data_fim, '%d-%m-%Y')
                    if obj_ultima_acao.data_conclusao != None:
                        data_termino_tarefa = datetime.strftime(obj_ultima_acao.data_conclusao, '%d-%m-%Y')

                    '''Verifica status tarefa'''
                    if obj_ultima_acao.data_conclusao != None and obj_ultima_acao.data_fim != None:
                        if obj_ultima_acao.data_conclusao > obj_ultima_acao.data_fim:
                            status_tarefa = 'Atrasada'
                    elif obj_ultima_acao.data_conclusao == None and obj_ultima_acao.data_fim != None:
                        if obj_ultima_acao.data_fim < data_hora_atual.date():
                            status_tarefa = 'Atrasada'


                '''Cálculo progresso tarefa'''
                qtd_tt_acoes = Atividade.objects.filter(tipo_atividade='A', cod_atividade_pai=tarefa.cod_atividade).count()
                qtd_acoes_concluidas = (Atividade.objects
                                        .filter(tipo_atividade='A', cod_atividade_pai=tarefa.cod_atividade,
                                                data_conclusao__isnull=False).count())
                perc_progresso_tarefa = 0
                try:
                    perc_progresso_tarefa = int((qtd_acoes_concluidas / qtd_tt_acoes) * 100)
                except:
                    perc_progresso_tarefa = 0


                if perc_progresso_tarefa == 100:
                    status_tarefa = 'Concluída'

                reg = {
                    'cod_atividade': tarefa.cod_atividade,
                    'desc_atividade': tarefa.desc_atividade,
                    'data_ini_tarefa': data_ini_tarefa,
                    'data_prazo_tarefa': data_prazo_tarefa,
                    'data_termino_tarefa': data_termino_tarefa,
                    'cod_usu__cod_usu': tarefa.cod_usu.cod_usu,
                    'cod_usu__login_usu': tarefa.cod_usu.login_usu,
                    'perc_progresso_tarefa': str(perc_progresso_tarefa) + '%',
                    'status_tarefa': status_tarefa
                }
                lista_dic_tarefas.append(reg)

            lista_cod_usuarios_vinculados = list(
                Usuarios_Projeto.objects.filter(cod_projeto=obj_proj).values('cod_usu__cod_usu')
            )

            dic_projeto = {
                'nome_projeto': obj_proj.cod_ideia.resumo_ideia,
                'nome_sponsor': obj_proj.cod_ideia.cod_usu_owner.login_usu,
                'nome_gerente': obj_proj.cod_ideia.cod_usu_master.login_usu,
                'objetivos_proj': obj_proj.cod_ideia.obs_usu_owner,
                'riscos': obj_proj.cod_ideia.obs_usu_master,
                'desc_fase': obj_proj.fase_projeto,
                'ult_atualização':  obj_proj.data_atualizacao.astimezone().strftime('%d-%m-%Y %H:%M') if obj_proj.data_atualizacao != None else '',
                'data_inicio': datetime.strftime(obj_proj.data_ini, '%d-%m-%Y'),
                'data_fim': ultima_tarefa,
                'perc_progresso_acoes': str(perc_progresso_acoes) + '%',
                'status_proj': obj_proj.status_proj,
                'cronograma': obj_proj.status_cronograma_proj,
                'lista_cod_usuarios_vinculados': lista_cod_usuarios_vinculados
            }


            data = {
                'dic_projeto': dic_projeto,
                'lista_dic_tarefas': lista_dic_tarefas,
                'lista_usuarios': lista_usuarios,
            }

        return JsonResponse(data, safe=False)


    def post(self, request):
        cod_projeto_frm = request.POST['cod_projeto']
        fase_projeto_frm = request.POST['fase_projeto']

        data_atual = datetime.now()

        obj_projeto = Projeto.objects.get(pk=cod_projeto_frm)

        obj_projeto.fase_projeto = fase_projeto_frm
        obj_projeto.data_atualizacao = data_atual
        obj_projeto.save()
        msg = 'Fase Editada!'

        data = dict()
        data = {
            'cod_tarefa': obj_projeto.cod_projeto,
            'desc_tarefa': obj_projeto.fase_projeto,
            'msg': msg
        }

        return JsonResponse(data, safe=False)


    def put(self, request):
        put = QueryDict(request.body)
        cod_projeto_frm = put.get('cod_projeto')
        status_proj_frm = put.get('status_proj')

        data_atual = datetime.now()

        obj_projeto = Projeto.objects.get(pk=cod_projeto_frm)
        obj_projeto.status_proj=1
        obj_projeto.data_atualizacao = data_atual
        obj_projeto.data_fim = data_atual
        obj_projeto.save()
        msg = 'Projeto Finalizado'

        data = dict()
        data = {
            'cod_projeto': obj_projeto.cod_projeto,
            'status_proj': obj_projeto.status_proj,
            'msg': msg
        }

        return JsonResponse(data, safe=False)

class Frm_Tarefa_View(View):
    def post(self, request):
        cod_projeto_frm = request.POST['cod_projeto']
        cod_tarefa_frm = request.POST['cod_tarefa']
        desc_tarefa_frm = request.POST['desc_tarefa']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        data_atual = datetime.now()

        lista_dic_acoes = list(Atividade.objects.filter(
            cod_atividade_pai=cod_tarefa_frm
        ).values('cod_atividade', 'desc_atividade', 'data_ini', 'data_fim', 'observacao', 'data_conclusao', 'cod_usu__cod_usu'))


        obj_projeto = Projeto.objects.get(pk=cod_projeto_frm)
        obj_tarefa = None
        msg = ''
        if cod_tarefa_frm == '0':
            obj_tarefa = Atividade(
                tipo_atividade = 'T',
                cod_atividade_pai = 0,
                desc_atividade = desc_tarefa_frm,
                cod_projeto = obj_projeto,
                cod_usu = obj_usuario_sessao
            )
            obj_tarefa.save()
            msg = 'Tarefa adicionada ao projeto com sucesso!'
        else:
            obj_tarefa = Atividade.objects.get(pk=cod_tarefa_frm)
            obj_tarefa.desc_atividade = desc_tarefa_frm
            obj_tarefa.cod_usu = obj_usuario_sessao
            obj_tarefa.save()
            msg = 'Tarefa editada com sucesso!'

        obj_projeto.data_atualizacao = data_atual
        obj_projeto.save()

        data = dict()
        data = {
            'lista_dic_acoes': lista_dic_acoes,
            'cod_tarefa': obj_tarefa.cod_atividade,
            'desc_tarefa': obj_tarefa.desc_atividade,
            'msg': msg
        }

        return JsonResponse(data, safe=False)

class Frm_Acao_View(View):
    def get(self,request):
        cod_tarefa_frm = request.GET['cod_tarefa']

        data_hora_atual = datetime.now()

        obj_tarefa = Atividade.objects.get(pk=cod_tarefa_frm)
        desc_tarefa = obj_tarefa.desc_atividade
        data_fim = obj_tarefa.data_fim
        data_ini= obj_tarefa.data_ini
        observacao = obj_tarefa.observacao
        data_conclusao = obj_tarefa.data_conclusao
        lista_obj_acoes = (Atividade.objects.filter(
            cod_atividade_pai = cod_tarefa_frm
        ))
        lista_dic_acoes = []
        for acao in lista_obj_acoes:
            status_acao =  self.retorna_status_acao(acao)
            reg = {
                'cod_atividade': acao.cod_atividade,
                'desc_atividade': acao.desc_atividade,
                'data_ini': acao.data_ini,
                'data_fim': acao.data_fim,
                'observacao': acao.observacao,
                'data_conclusao': acao.data_conclusao,
                'cod_usu__cod_usu': acao.cod_usu.cod_usu,
                'status_acao': status_acao
            }
            lista_dic_acoes.append(reg)


        data = dict()
        data = {
            'lista_dic_acoes': lista_dic_acoes,
            'desc_tarefa': desc_tarefa,
            'data_fim': data_fim,
            'data_ini': data_ini
        }

        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_projeto_frm = request.POST['cod_projeto']
        cod_acao_frm = request.POST['cod_acao']
        cod_atividade_pai_frm = request.POST['cod_atividade_pai']
        observacao_frm = request.POST['observacao']
        desc_acao_frm = request.POST['desc_acao']
        prazo_frm = request.POST['prazo']
        cod_usu_atribuido_frm = request.POST['cod_usu_atribuido']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        obj_usu_resp_acao = Usuario.objects.get(pk=cod_usu_atribuido_frm)
        data_atual = datetime.now()

        obj_projeto = Projeto.objects.get(pk=cod_projeto_frm)
        obj_atividade_pai = Atividade.objects.get(pk=cod_atividade_pai_frm)
        obj_acao = None
        msg = ''


        if cod_acao_frm == '0':
            obj_acao = Atividade(
                cod_projeto=obj_projeto,
                tipo_atividade='A',
                cod_atividade_pai=cod_atividade_pai_frm,
                desc_atividade=desc_acao_frm,
                data_fim=prazo_frm,
                observacao=observacao_frm,
                cod_usu=obj_usu_resp_acao
            )
            obj_acao.save()
            msg = 'Acao adicionada ao projeto com sucesso!'
        else:
            obj_acao = Atividade.objects.get(pk=cod_acao_frm)
            obj_acao.cod_projeto = obj_projeto
            obj_acao.cod_atividade_pai = cod_atividade_pai_frm
            obj_acao.desc_atividade = desc_acao_frm
            obj_acao.data_fim = prazo_frm
            obj_acao.observacao = observacao_frm
            obj_acao.cod_usu = obj_usu_resp_acao
            obj_acao.save()
            msg = 'Acao editada com sucesso!'

        obj_projeto.data_atualizacao = data_atual
        obj_projeto.save()

        data = dict()
        data = {
            'cod_acao': obj_acao.cod_atividade,
            'msg': msg,
        }

        return JsonResponse(data, safe=False)

    def put(self, request):
        put = QueryDict(request.body)
        data_ini_frm = put.get('data_ini')
        tipo_data_frm = put.get('tipo_data')
        cod_projeto_frm = put.get('cod_projeto')
        data_conclusao_frm = put.get('data_conclusao')
        cod_acao_frm = put.get('cod_acao')
        tipo_data_frm = put.get('tipo_data')
        data_atual = datetime.now()
        data_ini_frm = data_atual
        data_ini_frm = data_ini_frm.strftime('%Y-%m-%d')

        data_conclusao_frm = data_atual
        data_conclusao_frm = data_conclusao_frm.strftime('%Y-%m-%d')

        msg = ''

        if tipo_data_frm == 'data_ini':
            if cod_acao_frm != 0:
                obj_acao = Atividade.objects.get(pk=cod_acao_frm)
                obj_acao.data_ini = data_ini_frm
                obj_acao.save()
                msg = 'Acao iniciada com sucesso!'
            else:
                msg = 'Acao ainda não foi salvo!'

            projeto = obj_acao.cod_projeto
            projeto.data_atualizacao = data_atual
            projeto.save()

            data = dict()
            data = {
                'cod_acao': obj_acao.cod_atividade,
                'data_ini': obj_acao.data_ini,
                'msg': msg
            }


        elif tipo_data_frm == 'data_conclusao':
            if cod_acao_frm != 0:
                obj_acao = Atividade.objects.get(pk=cod_acao_frm)
                obj_acao.data_conclusao = data_conclusao_frm
                obj_acao.save()
                msg = 'Ação concluída!'
            else:
                msg = 'Acao ainda não pode ser concluída!'

            projeto = obj_acao.cod_projeto
            projeto.data_atualizacao = data_atual
            projeto.save()

            data = dict()
            data = {
                'cod_acao': obj_acao.cod_atividade,
                'data_conclusao': obj_acao.data_conclusao,
                'msg': msg
            }

        return JsonResponse(data, safe=False)

    def retorna_status_acao(self, obj_acao):
        data_hora_atual = datetime.now()
        status_acao = 'Em andamento'
        '''Verifica status da ação'''
        if obj_acao.data_ini == None and obj_acao.data_fim < data_hora_atual.date():
            status_acao = 'Atrasada'
        elif obj_acao.data_ini != None and obj_acao.data_conclusao != None:
            if obj_acao.data_conclusao > obj_acao.data_fim:
                status_acao = 'Atrasada'
            elif obj_acao.data_conclusao <= obj_acao.data_fim:
                status_acao = 'Concluída'

        return status_acao


class Frm_Usuarios_Projeto_View(View):
    def post(self, request):
        cod_projeto_frm = request.POST['cod_projeto']
        lista_cod_usuarios = request.POST['lista_cod_usuarios']

        lista_obj_vinculos_usu_proj = Usuarios_Projeto.objects.filter(cod_projeto__cod_projeto=cod_projeto_frm)
        for reg in lista_obj_vinculos_usu_proj:
            reg.delete()

        obj_projeto = Projeto.objects.get(pk=cod_projeto_frm)
        for cod_usu in lista_cod_usuarios.split(','):
            obj_usu = Usuario.objects.get(pk=cod_usu)
            obj_usu_proj = Usuarios_Projeto(
                cod_usu=obj_usu,
                cod_projeto=obj_projeto
            ).save()

        data = dict()
        data = {
            'msg': 'Usuário(s) vinculado(s) com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Frm_Acoes_Usuario_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_obj_projetos = []
        if obj_usuario_sessao.tipo_colab in ('H', 'G'):
            lista_obj_projetos = Projeto.objects.all()
        else:
            lista_obj_usu_projetos = Usuarios_Projeto.objects.filter(cod_usu=obj_usuario_sessao)
            for proj in lista_obj_usu_projetos:
                lista_obj_projetos.append(proj.cod_projeto)

        lista_obj_acoes_prox_ou_atradadas = Frm_Lista_Projetos_View().retorna_prox_acoes_proj(obj_usuario_sessao,
                                                                                              lista_obj_projetos)
        data = dict()
        data = {
            'msg': 'Dados atualizados',
            'lista_obj_acoes_prox_ou_atradadas': lista_obj_acoes_prox_ou_atradadas
        }
        return JsonResponse(data, safe=False)
