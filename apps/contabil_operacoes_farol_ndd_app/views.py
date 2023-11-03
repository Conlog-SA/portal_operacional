from datetime import datetime, date, timedelta

from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.contabil_operacoes_farol_ndd_app.models import Notas_Tratadas, Excecoes_Natureza_Operacao
from apps.usuario_app.models import Usuario


class Form_Registra_Notas_Tratadas_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_excecoes = Excecoes_Natureza_Operacao.objects.filter(
            cod_usu__cod_filial__cod_empresa=usuario_portal.cod_filial.cod_empresa
        )
        lista_benner_sem_excecao = self.atualiza_cb_operacoes(usuario_portal.cod_filial.cod_empresa.cod_empresa)


        context = {
            'lista_excecoes': lista_excecoes,
            'lista_operacoes': lista_benner_sem_excecao
        }
        return render(request, 'contabil_operacoes_farol_ndd_app/form_notas_tratadas.html', context)


    def atualiza_cb_operacoes(self, cod_empresa):
        lista_operacoes_benner = ConexaoBancoBenner().retorna_natureza_operacoes_distintas_proc_nfe()

        lista_benner_sem_excecao = []
        for op in lista_operacoes_benner:
            excecao_cad = Excecoes_Natureza_Operacao.objects\
                .filter(desc_operacao=op['desc_operacao'],
                        cod_usu__cod_filial__cod_empresa__cod_empresa = cod_empresa).first()
            if excecao_cad == None:
                lista_benner_sem_excecao.append(op)
        return lista_benner_sem_excecao

class Registra_Notas_Tratadas_View(View):
    def get(self, request):
        num_nota_form = request.GET['num_nota']
        data_ini_form = request.GET['data_ini']
        data_fim_form = request.GET['data_fim']
        chave_nota_form = request.GET['chave_nota']
        lista_notas_validadas = []
        if num_nota_form != '0':
            lista_notas = ConexaoBancoBenner()\
                .retorna_dados_nota_proc_nfe(num_nota_form, data_ini_form, data_fim_form, 0)
        else:
            lista_notas = ConexaoBancoBenner().retorna_dados_nota_proc_nfe(0, None, None, chave_nota_form)
        for nota in lista_notas:
            nota_tratada = Notas_Tratadas.objects.filter(chave_nota=nota['chave_nota']).first()
            nota['tratada'] = 'N'
            if nota_tratada != None:
                nota['tratada'] = 'S'
                nota['justificativa'] = nota_tratada.justificativa
                nota['cod_nota_tratada'] = nota_tratada.cod_nota_tratada
            lista_notas_validadas.append(nota)



        dados = dict()
        dados = {
            'lista_notas_validadas': lista_notas_validadas,
            'msg': 'Foi localizado, ' + str(len(lista_notas))
        }
        return JsonResponse(dados, safe=False)




class Form_Registra_Excecoes_Operacao_View(View):
    def get_object(self, pk):
        try:
            return Excecoes_Natureza_Operacao.objects.get(pk=pk)
        except Excecoes_Natureza_Operacao.DoesNotExist:
            return Http404

    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        lista_excecoes = []
        lista_excecoes_banco = Excecoes_Natureza_Operacao.objects.filter(
            cod_usu__cod_filial__cod_empresa = usuario_portal.cod_filial.cod_empresa
        )
        for ex in lista_excecoes_banco:
            excecao = {
                'cod_excecao': ex.cod_excecao_operacao,
                'desc_operacao': ex.desc_operacao
            }
            lista_excecoes.append(excecao)
        data = dict()
        data = {
            'lista_excecoes': lista_excecoes
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        desc_operacao_excecao_form = request.POST['desc_operacao_excecao']
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        for op in desc_operacao_excecao_form.split(','):
            obj_excecao = Excecoes_Natureza_Operacao(
                desc_operacao = op,
                cod_usu = usuario_portal
            )
            obj_excecao.save()
        lista_benner_sem_excecao = Form_Registra_Notas_Tratadas_View().atualiza_cb_operacoes(usuario_portal.cod_filial.cod_empresa.cod_empresa)
        data = dict()
        data = {
            'msg': 'Exceção Registrada com sucesso!',
            'lista_benner_sem_excecao': lista_benner_sem_excecao
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        id_usu_session = request.session['cod_usuario_logado']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()
        obj_excecao_operacao = self.get_object(pk)
        obj_excecao_operacao.delete()

        lista_benner_sem_excecao = Form_Registra_Notas_Tratadas_View().atualiza_cb_operacoes(usuario_portal.cod_filial.cod_empresa.cod_empresa)
        data = dict()
        data = {
            'msg': 'Registro excluído com sucesso !',
            'lista_benner_sem_excecao': lista_benner_sem_excecao
        }
        return JsonResponse(data, safe=False)

class Cadastro_Justificativa_Nota_Tratada_View(View):
    def get_object(self, pk):
        try:
            return Notas_Tratadas.objects.get(pk=pk)
        except Notas_Tratadas.DoesNotExist:
            return Http404


    def post(self, request):
        tipo_transacao_form = request.POST['tipo_transacao']
        msg = ''
        if tipo_transacao_form == 'add':
            handle_emp_form = request.POST['handle_emp']
            nome_emp_form = request.POST['nome_emp']
            handle_fil_form = request.POST['handle_fil']
            nome_fil_form = request.POST['nome_fil']
            num_nota_form = request.POST['num_nota']
            serie_form = request.POST['serie']
            chave_nota_form = request.POST['chave_nota']
            natureza_form = request.POST['natureza']
            emissao_form = request.POST['emissao']
            doc_fornec_form = request.POST['doc_fornec']
            nome_fornec_form = request.POST['nome_fornec']
            justificativa_form = request.POST['justificativa']

            id_usu_session = request.session['cod_usuario_logado']
            obj_usu_session = Usuario.objects.filter(cod_usu=id_usu_session).first()
            obj_nota_tratada = Notas_Tratadas(
                handle_empresa=handle_emp_form,
                nome_empresa = nome_emp_form,
                handle_filial = handle_fil_form,
                nome_filial = nome_fil_form,
                numero_nota = num_nota_form,
                serie = serie_form,
                chave_nota = chave_nota_form,
                natureza = natureza_form,
                emissao = datetime.strptime(emissao_form, '%d-%m-%Y') ,
                doc_fornec = doc_fornec_form,
                nome_fornec = nome_fornec_form,
                justificativa = justificativa_form,
                cod_usu = obj_usu_session
            )
            obj_nota_tratada.save()
            msg = 'Justificativa armazenada com sucesso !'

        elif tipo_transacao_form == 'update':
            cod_nota_tratada_form = request.POST['cod_nota_tratada']
            justificativa_form = request.POST['justificativa']

            obj_nota_tratada = Notas_Tratadas.objects.get(pk=cod_nota_tratada_form)
            obj_nota_tratada.justificativa = justificativa_form
            obj_nota_tratada.save()
            msg = 'Justificativa alterada com sucesso'

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


    def delete(self, request, pk):
        obj_nota_tratada = self.get_object(pk)
        obj_nota_tratada.delete()

        data = dict()
        data = {
            'msg': 'Registro excluído com sucesso !'
        }
        return JsonResponse(data, safe=False)






