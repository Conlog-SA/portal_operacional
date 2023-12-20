from django.http import JsonResponse, Http404, FileResponse
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.core.files.storage import FileSystemStorage
from apps.cco_multas_app.models import CCO_Multas, CCO_Tipo_Multa, CCO_Anexos
from apps.usuario_app.models import Usuario, Projeto
import os
from datetime import datetime

from proj_portal_operacional.settings import BASE_DIR

class Multas_View(View):
    def get(self, request):
        lista_projetos = list(Projeto.objects.filter(data_inativado__isnull=True, handle_benner__gt=0).values('cod_projeto', 'desc_proj', 'handle_benner', 'cod_reduzido_benner'))
        lista_tipo_multa = list(CCO_Tipo_Multa.objects.filter().values('cod_tipo_multa', 'desc_multa'))
        lista_placas = list(CCO_Multas.objects.filter().values('placa_multa', 'cod_multa_antt'))

        contexto = {
            'lista_projetos': lista_projetos,
            'lista_tipo_multa': lista_tipo_multa,
            'lista_placas': lista_placas,
        }
        return render(request, 'cco_multas_app/form_cco_cad_multas.html', contexto)

class Exclui_Multa_View(View):
    def get_object(self,pk):
        try:
            return CCO_Multas.objects.get(pk=pk)
        except CCO_Multas.DoesNotExist:
            return Http404("Multa não Encontrada")

    def delete(self, request, pk):
        obj_multa = self.get_object(pk)
        obj_multa.delete()
        data = dict()
        data = {
            'msg': 'Registro excluido com sucesso!'
        }
        return JsonResponse(data, safe=False)

class Cadastro_Multas_View(View):
    def post(self, request):
        msg = ''
        cod_multa = 0
        try:
            placa = request.POST['placa']
            nome_condutor = request.POST['nome_condutor']
            cod_infracao = request.POST['cod_infracao']
            numero_auto = request.POST['numero_auto']
            tipo_multa = request.POST['tipo_multa']
            local_auto = request.POST['local_auto']
            projeto = request.POST['projeto']
            data_recebe_multa_cco = request.POST['data_recebe_multa_cco']
            data_infracao = request.POST['data_infracao']
            valor_infracao = request.POST['valor_infracao']
            valor_pago = request.POST['valor_pago']
            data_recebimento_infracao = request.POST['data_recebimento_infracao']
            data_pagamento_infracao = request.POST['data_pagamento_infracao']
            status_multa = request.POST['status_multa']
            obs = request.POST['obs']
            cod_cad_multa = request.POST['cod_cad_multa']
            cod_usuario_sessao = request.session['cod_usuario_logado']
            obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)


            if data_infracao == '':
                data_infracao = None
            else:
                data_infracao = datetime.strptime(data_infracao, '%Y-%m-%d')

            if data_recebimento_infracao == '':
                data_recebimento_infracao = None
            else:
                data_recebimento_infracao = datetime.strptime(data_recebimento_infracao, '%Y-%m-%d')

            if data_pagamento_infracao == '':
                data_pagamento_infracao = None
            else:
                data_pagamento_infracao = datetime.strptime(data_pagamento_infracao, '%Y-%m-%d')

            if data_recebe_multa_cco == '':
                data_recebe_multa_cco = None
            else:
                data_recebe_multa_cco = datetime.strptime(data_recebe_multa_cco, '%Y-%m-%d')



            if cod_cad_multa == '0':
                multa = CCO_Multas(
                    placa_multa=placa,
                    num_auto_infracao=numero_auto,
                    nome_condutor=nome_condutor,
                    data_auto=data_infracao,
                    cod_infracao=cod_infracao,
                    data_recebe_multa=data_recebimento_infracao,
                    local_multa=local_auto,
                    data_recebe_multa_cco=data_recebe_multa_cco,
                    cod_projeto=Projeto.objects.get(pk=projeto),
                    cod_tipo_multa=CCO_Tipo_Multa.objects.get(pk=tipo_multa),
                    cod_usu=obj_usuario_sessao,
                    data_pag_multa=data_pagamento_infracao,
                    status=status_multa,
                    valor_pagar=valor_infracao,
                    valor_pago=valor_pago,
                    obs=obs
                )
                multa.save()
                msg = 'Registro cadastrado com sucesso'

                cod_multa = multa.cod_multa_antt
            else:
                obj_cadastro_multa = CCO_Multas.objects.get(pk=cod_cad_multa)

                obj_cadastro_multa.placa_multa = placa
                obj_cadastro_multa.num_auto_infracao = numero_auto
                obj_cadastro_multa.data_auto = data_infracao
                obj_cadastro_multa.data_recebe_multa = data_recebimento_infracao
                obj_cadastro_multa.cod_infracao = cod_infracao
                obj_cadastro_multa.local_multa = local_auto
                obj_cadastro_multa.data_recebe_multa_cco = data_recebe_multa_cco
                obj_cadastro_multa.cod_projeto = Projeto.objects.get(pk=projeto)
                obj_cadastro_multa.cod_tipo_multa = CCO_Tipo_Multa.objects.get(pk=tipo_multa)
                obj_cadastro_multa.cod_usu = obj_usuario_sessao
                obj_cadastro_multa.obs = obs
                obj_cadastro_multa.data_pag_multa = data_pagamento_infracao
                obj_cadastro_multa.status = status_multa
                obj_cadastro_multa.valor_pagar = valor_infracao
                obj_cadastro_multa.valor_pago = valor_pago
                obj_cadastro_multa.nome_condutor = nome_condutor

                obj_cadastro_multa.save()

                msg = 'Registro Atualizado com Sucesso'

                cod_multa = obj_cadastro_multa.cod_multa_antt

        except Exception as e:
            msg = 'Erro ao processar a solicitação: {}'.format(str(e))

        data = {
            'msg': msg,
            'cod_multa': cod_multa,
        }
        return JsonResponse(data, safe=False)

class Pesquisa_Multa_View(View):
    def get(self, request):
        tipo_pesquisa = request.GET['tipo_pesquisa_multa']
        linhasTabela = []
        if tipo_pesquisa == 'placa':
            placa_selecionada = request.GET['placa_selecionada']
            queryMultasPlaca = CCO_Multas.objects.filter(placa_multa=placa_selecionada)
            for registro in queryMultasPlaca:
                dadosregistro = {
                    'cod_multa_antt' : registro.cod_multa_antt, #codigo da multa código transito
                    'placa_multa' : registro.placa_multa, #placa do cavalo[0]
                    'num_auto_infracao': registro.num_auto_infracao, #Número do Auto de infração[1]
                    'desc_projeto' : registro.cod_projeto.desc_proj, # Descrição do Projeto[2]
                    'data_auto' : registro.data_auto, #Data que levou a multa[3]
                    'data_recebe_multa_cco': registro.data_recebe_multa_cco,#[4]
                    'data_recebe_multa': registro.data_recebe_multa,  # data CCO Recebeu Multa[5]
                    'data_pag_multa': registro.data_pag_multa,  # data Pagamento da Multa[6]
                    'desc_multa' : registro.cod_tipo_multa.desc_multa, #Descrição Tipo de multa[7]
                    'nome_condutor' : registro.nome_condutor, #Nome Condutor[8]
                    'local_multa' : registro.local_multa, #local da multa[9]
                    'status': registro.status, #Status do processo[10]
                    'obs' : registro.obs, #Observação[11]
                    'valor_pagar' : registro.valor_pagar, #Valor a pagar da Multa[12]
                    'valor_pago' : registro.valor_pago, #Valor pago da multa[13]
                    'data_inclusao' : registro.data_inclusao, #data inclusão CCO[14]
                    'cod_infracao' : registro.cod_infracao, #código da infração[15]
                    'cod_projeto' : registro.cod_projeto.cod_projeto, # Envia o Código do projeto[17]
                    'cod_tipo_multa' : registro.cod_tipo_multa.cod_tipo_multa# Envia o Código do tipo de multa[17]
                }
                linhasTabela.append(dadosregistro)
                
        elif tipo_pesquisa == 'status':
            status_selecionado = request.GET['status_selecionado']
            queryStatusPlaca = CCO_Multas.objects.filter(status=status_selecionado)
            for registro in queryStatusPlaca:
                dadosregistro = {
                    'cod_multa_antt' : registro.cod_multa_antt, #codigo da multa código transito
                    'placa_multa' : registro.placa_multa, #placa do cavalo[0]
                    'num_auto_infracao': registro.num_auto_infracao, #Número do Auto de infração[1]
                    'desc_projeto' : registro.cod_projeto.desc_proj, # Descrição do Projeto[1]
                    'data_auto' : registro.data_auto, #Data que levou a multa[2]
                    'data_recebe_multa_cco': registro.data_recebe_multa_cco,#[3]
                    'data_recebe_multa': registro.data_recebe_multa,  # data CCO Recebeu Multa[4]
                    'data_pag_multa': registro.data_pag_multa,  # data Pagamento da Multa[5]
                    'desc_multa' : registro.cod_tipo_multa.desc_multa, #Descrição Tipo de multa[6]
                    'nome_condutor' : registro.nome_condutor, #Nome Condutor[7]
                    'local_multa' : registro.local_multa, #local da multa[8]
                    'status': registro.status, #Status do processo[9]
                    'obs' : registro.obs, #Observação[10]
                    'valor_pagar' : registro.valor_pagar, #Valor a pagar da Multa
                    'valor_pago' : registro.valor_pago, #Valor pago da multa
                    'data_inclusao' : registro.data_inclusao, #data inclusão CCO
                    'cod_infracao' : registro.cod_infracao, #código da infração
                    'cod_projeto' : registro.cod_projeto.cod_projeto, # Envia o Código do projeto
                    'cod_tipo_multa' : registro.cod_tipo_multa.cod_tipo_multa# Envia o Código do tipo de multa

                }
                linhasTabela.append(dadosregistro)

        data = dict()
        data = {
            'linhasTabela' : linhasTabela
        }      
        return JsonResponse(data,safe = False)

class Anexa_Doc_View(View):
    def get_object(self, pk):
        try:
            return CCO_Anexos.objects.get(pk=pk)
        except CCO_Anexos.DoesNotExist:
            return Http404
        
    def post(self, request):
        file_form = request.FILES['file']
        cod_multa = request.POST['cod_multa']
        tipo_anexo = request.POST['tipo_anexo']

        fs = FileSystemStorage()

        caminho_arquivo = 'docs/cco_multas_app/'+ tipo_anexo + '_' + str(cod_multa) + '_' + str(file_form)
        filename = fs.save(caminho_arquivo, file_form)
        uploaded_file_url = fs.url(filename)

        obj_anexo = CCO_Anexos(
            caminho_anexo=caminho_arquivo,
            cod_multa_antt=CCO_Multas.objects.get(pk=cod_multa),
            tipo_anexo=tipo_anexo
        )
        obj_anexo.save()

        msg = 'Doc Anexado com sucesso'

        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data,safe= False)


    def delete(self, request, cod_anexo_cco):

        obj_anexo = self.get_object(cod_anexo_cco)
        cod_multa_antt = obj_anexo.cod_multa_antt.cod_multa_antt


        caminho_arquivo = os.path.join(BASE_DIR, 'media\\' + str(obj_anexo.caminho_anexo).replace('/', '\\'))
        os.remove(caminho_arquivo)
        obj_anexo.delete()
        data = dict()
        data = {
            'msg': 'Anexo excluido com sucesso!',
            'cod_multa_antt': cod_multa_antt
        }
        return JsonResponse(data, safe=False)


class Pesquisa_Anexo_View(View):
    def get(self,request):        
        cod_multa = request.GET['cod_multa_antt']
        obj_multa = CCO_Multas.objects.get(pk=cod_multa)
        lista_anexos_multa = list(CCO_Anexos.objects.filter(cod_multa_antt=obj_multa).values('cod_multa_antt__placa_multa','cod_anexo_cco','tipo_anexo','caminho_anexo',))

        data = dict()
        data = {
            'lista_anexos_multa' : lista_anexos_multa
        }
        return JsonResponse(data,safe= False)



class Atualiza_Placa_View(View):
    def get(self, request):
        lista_placas = list(CCO_Multas.objects.all().values('placa_multa').distinct())
        data = dict()
        data = {
            'lista_placas' :lista_placas
        }
        return JsonResponse(data,safe= False)