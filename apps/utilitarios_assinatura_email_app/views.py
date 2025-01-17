import os

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.conecta_senior_app.views import Conexao_Senior_BD
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR


# Create your views here.


class Frm_Assinatura_Email_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        conexao_senior = Conexao_Senior_BD(obj_usuario_logado.cod_filial.cod_empresa.cod_empresa)
        dados_colab = conexao_senior.pesq_colab_by_nome(obj_usuario_logado.nome_usu)

        caminho_foto = 'https://operacional.conlogsa.com.br/media/fotos/user_default.jpg'
        if obj_usuario_logado.caminho_foto != None:
            caminho_foto = 'https://operacional.conlogsa.com.br/media/' + obj_usuario_logado.caminho_foto

        tel_colab = '00 9 0000 0000'
        if obj_usuario_logado.tel != None:
            tel_colab = obj_usuario_logado.tel
        contexto = {
            'obj_usuario_logado': obj_usuario_logado,
            'dados_colab': dados_colab,
            'caminho_foto': caminho_foto,
            'tel_colab': tel_colab
        }
        return render(request, 'utilitarios_assinatura_email_app/frm_gera_assinatura_email.html', contexto)


    def post(self, request):
        transacao_frm = request.POST['transacao']

        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        dados = dict()
        if transacao_frm == 'update_foto':
            myfile = request.FILES['file']
            extensao_file = (myfile.name).split('.')[-1]
            caminho_arq_importado = 'fotos/' + obj_usuario_logado.login_usu + '.' + extensao_file
            fs = FileSystemStorage()
            uploaded_file_url = os.path.join(BASE_DIR, 'media/' + caminho_arq_importado)
            file_path = fs.path(uploaded_file_url)
            if os.path.exists(file_path):
                os.remove(file_path)

            filename = fs.save(caminho_arq_importado, myfile)
            #uploaded_file_url = os.path.join(BASE_DIR, 'static/img/' + caminho_arq_importado)
            obj_usuario_logado.caminho_foto = caminho_arq_importado
            obj_usuario_logado.save()
            dados = {
                'foto_postada': caminho_arq_importado
            }
        elif transacao_frm == 'update_tel':
            tel_frm = request.POST['tel']
            obj_usuario_logado.tel = tel_frm
            obj_usuario_logado.save()
            dados = {
                'msg': 'ok'
            }


        return JsonResponse(dados, safe=False)




