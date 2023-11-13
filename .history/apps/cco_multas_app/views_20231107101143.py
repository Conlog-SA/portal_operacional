from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, Http404
from apps.cco_multas_app.models import CCO_Multas, CCO_Tipo_Multa
from apps.usuario_app.models import Usuario, Projeto


class Multas_View(View):
    def get(self, request):
        lista_projetos = list(Projeto.objects.filter(data_inativado__isnull=True).values('cod_projeto', 'desc_proj'))
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
        excluir_objeto = self.get_object(pk)
        excluir_objeto.delete()
        data = dict()
        data = {
            'msg': 'Registro excluido com sucesso!'
        }
        return JsonResponse(data, safe=False)


class Cadastro_Multas_View(View):
    def post(self, request):
        msg = ''
        try:
            placa = request.POST['placa']
            nome_condutor = request.POST['nome_condutor']
            cod_infracao = request.POST['cod_infracao']
            numero_auto = request.POST['numero_auto']
            tipo_multa = request.POST['tipo_multa']
            local_auto = request.POST['local_auto']
            projeto = request.POST['projeto']
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

            if cod_cad_multa == '0':
                multa = CCO_Multas(
                    placa_multa=placa,
                    num_auto_infracao=numero_auto,
                    nome_condutor=nome_condutor,
                    data_auto=data_infracao,
                    cod_infracao=cod_infracao,
                    data_recebe_multa=data_recebimento_infracao,
                    local_multa=local_auto,
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

        except Exception as e:
            msg = 'Erro ao processar a solicitação: {}'.format(str(e))

        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

class Pesquisa_Multa_View(View):
    def get(self, request):
        tipo_pesquisa = request.GET['tipo_pesquisa_multa']
        linhasTabela = []
        if tipo_pesquisa == "placa":
            placa_selecionada = request.GET['placa_selecionada']
            queryMultasPlaca = CCO_Multas.objects.filter(placa_multa=placa_selecionada)
            for registro in queryMultasPlaca:
                dadosregistro = {
                    'cod_multa_antt' : registro.cod_multa_antt,
                    'placa_multa' : registro.placa_multa,
                    'num_auto_infracao': registro.num_auto_infracao,
                    'desc_projeto' : registro.cod_projeto.desc_proj,
                    'data_auto' : registro.data_auto,
                    'desc_multa' : registro.cod_tipo_multa.desc_multa,
                    'nome_condutor' : registro.nome_condutor,
                    'data_recebe_multa' : registro.data_recebe_multa,
                    'local_multa' : registro.local_multa,
                    'status': registro.status,
                    'obs' : registro.obs,
                    'valor_pagar' : registro.valor_pagar,
                    'valor_pago' : registro.valor_pago,
                    'data_recebe_multa' : registro.data_recebe_multa,
                    'data_pag_multa' : registro.data_pag_multa,
                    'data_inclusao' : registro.data_inclusao,
                    'cod_infracao' : registro.cod_infracao,
                }
                linhasTabela.append(dadosregistro)

        data = {
            'linhasTabela' : linhasTabela
        }
        return JsonResponse(data,safe = False)