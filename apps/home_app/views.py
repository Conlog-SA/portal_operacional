from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.calendario_app.views import gera_datas_previstas_requisicoes_frota
from apps.conecta_ad_app.views import Conexao_AD
from apps.envio_email_app.views import Envio_Email
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario
from apps.usuario_app.views import Usuario_View


#Class Index
class Index_View(View):
    def get(self, request):
        #gera_datas_previstas_requisicoes_frota()
        msg_recebida = ''
        if request.GET.get('msg'):
            msg_recebida = request.GET.get('msg')
        context = {
            'cod_status_login': 0,
            'msg': msg_recebida
        }
        return render(request, 'home_app/index.html', context)


    def post(self, request):
        usu_form = request.POST['txt_usu']
        senha_form = request.POST['txt_pwd']
        '''Valida dados do usuario no AD'''
        obj_con_ad = Conexao_AD().identificacao_ad(usu_form, senha_form)
        validacao_usuario_ad = obj_con_ad[0]
        msg_erro_validao_ad = obj_con_ad[1]
        obj_usu_ad = obj_con_ad[2]
        pag_redirecionamento = ''
        dados = ''
        msg_form_index = ''
        '''Verifica usuario esta ok no ad'''
        if validacao_usuario_ad == True:
            '''Verifica se o usuário esta cadastrado no portal operacional'''
            metodo_verifica_existe_cad_usu = Usuario_View().verifica_usu_existe(usu_form)
            usu_existe = metodo_verifica_existe_cad_usu[0]
            obj_usuario = metodo_verifica_existe_cad_usu[1]
            '''Atualiza o status do usuário conforme o AD'''
            if obj_usuario != None:
                obj_usuario.status_usu = obj_usu_ad['status']
                obj_usuario.save()

            if usu_existe == True and obj_usuario.status_usu == 'A':
                request.session['cod_usuario_logado'] = obj_usuario.cod_usu
                return redirect('acessa_menu')
            elif usu_existe == True and obj_usuario.status_usu == 'I':
                msg_form_index = 'Acesso do usuário bloqueado! Verifique com a equipe da área de TI'
                Envio_Email().envia_email_alerta_adm(msg_form_index)
            elif usu_existe == False and obj_usu_ad['status'] == 'A':
                base_url = reverse('solicita_acesso')
                query_string = urlencode(obj_usu_ad)
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            elif usu_existe == False and obj_usu_ad['status'] == 'I':
                msg_form_index = 'Cadastro bloqueado no AD! Verifique com a equipe da área de TI '
                Envio_Email().envia_email_alerta_adm(msg_form_index)

        else:
            msg_form_index = msg_erro_validao_ad
            dados = {
                'cod_status_login': 1,
                'msg_erro': msg_form_index
            }
            pag_redirecionamento = 'home_app/index.html'

        return render(request, pag_redirecionamento, dados)



class Solicitacao_Acesso_View(View):
    def get(self, request):
        login_usu = request.GET.get('login_usu')
        nome_completo_usu = request.GET.get('nome_completo_usu')
        email_usu = request.GET.get('email_usu')
        lista_filiais = list(Filial.objects.filter(ativo=1).values('cod_filial', 'desc_filial', 'cod_empresa__desc_empresa'))
        dados = {
            'cod_status_login': 0,
            'login_usu': login_usu,
            'nome_completo_usu': nome_completo_usu,
            'email_usu': email_usu,
            'lista_filiais': lista_filiais
        }
        return render(request, 'home_app/form_solicita_acesso.html', dados)

    def post(self, request):
        login_usu_form = request.POST['txt_login_usu_sol']
        nome_usu_form = request.POST['txt_nome_usu_sol']
        email_usu_form = request.POST['txt_email_usu_sol']
        cod_filial_form = request.POST['cb_filiais_sol']

        obj_filial = Filial.objects.get(pk=cod_filial_form)
        obj_usu_sol = Usuario(
            cod_filial= obj_filial,
            nome_usu = nome_usu_form,
            data_desativacao = None,
            email_usu = email_usu_form,
            perfil_usu = 'C',
            login_usu = login_usu_form,
            sala = 'T'
        )
        obj_usu_sol.save()
        Envio_Email().envia_email_solicitacao_acesso_adm(obj_usu_sol)
        msg_solicitacao_usu = {
            'msg' : f'''{obj_usu_sol.nome_usu} , sua solicitação foi enviada com sucesso!. Aguarde contato do adm para liberação 
                                     dos módulos necessários para executar suas atividades.'''
        }
        base_url = reverse('index')
        query_string = urlencode(msg_solicitacao_usu)
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


