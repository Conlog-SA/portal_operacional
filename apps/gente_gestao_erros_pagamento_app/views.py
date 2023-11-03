import locale
from datetime import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.conecta_senior_app.views import Conexao_Senior_BD

from apps.gente_gestao_erros_pagamento_app.models import Verbas_Erros_de_Pagamentos, Erros_de_Pagamento
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario


class Form_Erros_Pagamento(View):
    def get(self, request):

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        lista_obj_filiais = None
        if obj_usuario_sessao.perfil_usu == 'C':
            lista_obj_filiais = Filial.objects.filter(cod_filial=obj_usuario_sessao.cod_filial.cod_filial)
        else:
            lista_obj_filiais = Filial.objects.all()

        lista_obj_verbas = Verbas_Erros_de_Pagamentos.objects.all()

        contexto = {
            'lista_obj_filiais': lista_obj_filiais,
            'obj_usu': obj_usuario_sessao,
            'lista_obj_verbas': lista_obj_verbas,
        }
        return render(request, 'gente_gestao_erros_pagamento_app/erros_pagamento.html', contexto)


class Manipulacao_Verbas(View):
    def post(self, request):
        desc_nova_verba = request.POST['nova_verba']

        nova_verba = Verbas_Erros_de_Pagamentos(
            desc_verba=desc_nova_verba.upper()
        )
        nova_verba.save()

        data = {}
        return JsonResponse(data, safe=False)


class Lancamento_Erros_Pagamento(View):

    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        informacao_buscada = request.GET['busca']
        if informacao_buscada == 'colaboradores':
            id_filial = request.GET['id_filial']
            id_empresa_senior = Filial.objects.get(pk=id_filial).cod_empresa
            id_filial_senior = Filial.objects.get(pk=id_filial).cod_filial_senior
            banco_senior = Conexao_Senior_BD()
            lista_colaboradores = banco_senior.listar_colaboradores_filial(id_empresa_senior, id_filial_senior)
        data = {
            # 'obj_usu': obj_usuario_sessao,
            'lista_colaboradores': lista_colaboradores,
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_erro_pag_form = request.POST['cod_erro_pag']
        idFilialSelecionada = request.POST['idFilialSelecionada']
        objFilial = Filial.objects.get(pk=idFilialSelecionada)
        codSeniorColaborador = request.POST['codSeniorColaborador']
        codVerba = request.POST['codVerba']
        objVerba = Verbas_Erros_de_Pagamentos.objects.get(pk=codVerba)
        valorEP = request.POST['valorEP']
        chkResolvido = request.POST['chkResolvido']
        if chkResolvido == 'true':
            chkResolvido = 1
        else:
            chkResolvido = 0
        compLancamento = request.POST['compLancamento']
        dataPrazo = request.POST['dataPrazo']
        textDuvida = request.POST['textDuvida']
        textAcao = request.POST['textAcao']
        textObs = request.POST['textObs']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        nome_usuario_sessao = obj_usuario_sessao.nome_usu

        banco_senior = Conexao_Senior_BD()
        dic_dados_colab = banco_senior.listar_dados_colaborador(codSeniorColaborador)
        nomeColab = dic_dados_colab[0]['nome_colab']
        codCargoColab = dic_dados_colab[0]['cod_cargo_colab']
        descCargoColab = dic_dados_colab[0]['desc_cargo_colab']
        dataAdmissaoColab = dic_dados_colab[0]['data_admissao_colab']
        msg = ''
        if cod_erro_pag_form != '0':
            obj_erro_pag_existente = Erros_de_Pagamento.objects.get(pk=cod_erro_pag_form)
            obj_erro_pag_existente.cod_colaborador_senior = codSeniorColaborador
            obj_erro_pag_existente.nome_colaborador = nomeColab
            obj_erro_pag_existente.cod_cargo_senior = codCargoColab
            obj_erro_pag_existente.desc_cargo = descCargoColab
            obj_erro_pag_existente.data_admissao = dataAdmissaoColab
            obj_erro_pag_existente.mes_competencia = datetime.strptime(compLancamento, '%Y-%m')
            obj_erro_pag_existente.valor_erro = round(float(valorEP), 2)
            obj_erro_pag_existente.duvida = textDuvida
            obj_erro_pag_existente.acao = textAcao
            obj_erro_pag_existente.nome_responsavel = nome_usuario_sessao
            obj_erro_pag_existente.prazo = datetime.strptime(dataPrazo, '%Y-%m-%d')
            obj_erro_pag_existente.obs = textObs
            obj_erro_pag_existente.status = chkResolvido
            obj_erro_pag_existente.cod_usu = obj_usuario_sessao
            obj_erro_pag_existente.cod_verba = objVerba
            obj_erro_pag_existente.save()
            msg = 'Registro atualizado com sucesso!'
        else:
            lancamento_erro_pagamento = Erros_de_Pagamento(
                cod_colaborador_senior=codSeniorColaborador,
                nome_colaborador=nomeColab,
                cod_cargo_senior=codCargoColab,
                desc_cargo=descCargoColab,
                data_admissao=dataAdmissaoColab,
                mes_competencia=datetime.strptime(compLancamento, '%Y-%m'),
                valor_erro=round(float(valorEP), 2),
                duvida=textDuvida,
                acao=textAcao,
                nome_responsavel=nome_usuario_sessao,
                prazo=datetime.strptime(dataPrazo, '%Y-%m-%d'),
                obs=textObs,
                status=chkResolvido,
                cod_usu=obj_usuario_sessao,
                cod_filial=objFilial,
                cod_verba=objVerba
            )
            lancamento_erro_pagamento.save()
            msg = 'Lançamento registrado com sucesso'

        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


class Tabela_Erros_Pagamentos(View):
    def get(self, request):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        competencia = request.GET['competenciaPesquisada']
        filial = Filial.objects.get(pk=request.GET['filialPesquisada'])

        query_erros_pagamento = Erros_de_Pagamento.objects.filter(cod_filial=filial,
                                                                  mes_competencia__month=competencia.split('-')[1],
                                                                  mes_competencia__year=competencia.split('-')[0],
                                                                  status_lancamento="S")

        linhas_tabela = []
        for registro in query_erros_pagamento:
            dados_registro = {
                'cod_erro_pagamento': registro.cod_erro_pagamento,
                'nome': registro.nome_colaborador,
                'cargo': registro.desc_cargo,
                'admissao': registro.data_admissao,
                'verba': registro.cod_verba.desc_verba,
                'valor': locale.currency(registro.valor_erro, grouping=True, symbol=None),
                'duvida': registro.duvida,
                'acao': registro.acao,
                'responsavel': registro.nome_responsavel,
                'prazo': registro.prazo,
                'obs': registro.obs,
                'status': registro.status,
                'editar': 'botao',
                'excluir': 'botao',
            }
            linhas_tabela.append(dados_registro)

        data = {
            'linhas_tabela': linhas_tabela
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_reg_erro_pag_form = request.POST['cod_reg_erro_pag']
        desc_motivo_estorno_form = request.POST['desc_motivo_estorno']

        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual = data_hora_atual.strftime('%d-%m-%Y')
        hora_atual = data_hora_atual.strftime('%H:%M')

        obj_erro_pag = Erros_de_Pagamento.objects.get(pk=cod_reg_erro_pag_form)
        obj_erro_pag.status_lancamento = 'E'
        obj_erro_pag.cod_usu = obj_usuario_logado
        obj_erro_pag.obs += ' / Estornado em ' + str(data_atual) + ', em, '+ str(hora_atual) + ', pelo motivo: '+ desc_motivo_estorno_form
        obj_erro_pag.save()

        data = {
            'msg': 'Estorno realizado com sucesso!'
        }
        return JsonResponse(data, safe=False)






class Edita_Erros_Pagamento_View(View):
    def get(self, request):
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        cod_erro_pag = request.GET['cod_erro_pag']
        obj_erro_pagamento_pesq = Erros_de_Pagamento.objects.get(pk=cod_erro_pag)
        obj_verba = Verbas_Erros_de_Pagamentos.objects.filter(cod_verba=obj_erro_pagamento_pesq.cod_verba.cod_verba).first()
        obj_erro_pagamento = {
            'cod_erro_pagamento': obj_erro_pagamento_pesq.cod_erro_pagamento,
            'acao' : obj_erro_pagamento_pesq.acao,
            'cod_cargo_senior': obj_erro_pagamento_pesq.cod_cargo_senior,
            'cod_colaborador_senior': obj_erro_pagamento_pesq.cod_colaborador_senior,
            'cod_filial': obj_erro_pagamento_pesq.cod_filial.cod_filial,
            'cod_usu': obj_erro_pagamento_pesq.cod_usu.nome_usu,
            'cod_verba': obj_erro_pagamento_pesq.cod_verba.cod_verba,
            'data_admissao': obj_erro_pagamento_pesq.data_admissao,
            'desc_cargo': obj_erro_pagamento_pesq.desc_cargo,
            'duvida': obj_erro_pagamento_pesq.duvida,
            'mes_competencia': obj_erro_pagamento_pesq.mes_competencia,
            'nome_colaborador': obj_erro_pagamento_pesq.nome_colaborador,
            'nome_responsavel': obj_erro_pagamento_pesq.nome_responsavel,
            'obs': obj_erro_pagamento_pesq.obs,
            'prazo': obj_erro_pagamento_pesq.prazo,
            'status': obj_erro_pagamento_pesq.status,
            'status_lancamento': obj_erro_pagamento_pesq.status_lancamento,
            'valor_erro': obj_erro_pagamento_pesq.valor_erro
        }

        data = dict()
        data = {
            'obj_erro_pagamento': obj_erro_pagamento,
            'desc_verba':obj_verba.desc_verba
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_erro_pag = request.POST['cod_erro_pag']
        competencia = request.POST['competencia']
        valor = request.POST['valor']
        prazo = request.POST['prazo']
        duvida = request.POST['duvida']
        acao = request.POST['acao']
        status = request.POST['status']
        obs = request.POST['obs']

        id_usu_session = request.session['usuario']
        usuario_portal = Usuario.objects.filter(cod_usu=id_usu_session).first()

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%d-%m-%Y')

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')
        obj_erro_pagamento = Erros_de_Pagamento.objects.filter(cod_erro_pagamento=cod_erro_pag).first()
        obj_erro_pagamento.mes_competencia = datetime.strptime(competencia, '%m/%Y')
        obj_erro_pagamento.valor_erro = round(float(valor),2)
        obj_erro_pagamento.prazo = datetime.strptime(prazo, '%d/%m/%Y')
        obj_erro_pagamento.duvida = duvida
        obj_erro_pagamento.acao = acao
        obj_erro_pagamento.status = status
        obj_erro_pagamento.obs = obs
        obj_erro_pagamento.cod_usu = usuario_portal
        obj_erro_pagamento.data_lancamento = datetime.strptime(data_atual_dd_mm_yyyy, '%d-%m-%Y')
        obj_erro_pagamento.save(update_fields=['mes_competencia','valor_erro','prazo','duvida','acao','status','obs','cod_usu', 'data_lancamento'])

        msg = 'Registro atualizado com sucesso!'
        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)