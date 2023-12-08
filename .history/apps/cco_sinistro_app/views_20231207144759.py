from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views import View
from apps.cco_sinistro_app.models import CCO_Sinistro, CCO_Sinistro_Carga, Motivo_Sinistro, CCO_Sinistro_Equipamento
from apps.estrut_org_app.models import Projeto, OP_Estados
from datetime import datetime

from apps.usuario_app.models import Usuario


class Form_Cad_Sinistros(View):
    def get_object(self, pk):
        try:
            return CCO_Sinistro.objects.get(pk=pk)
        except CCO_Sinistro.DoesNotExist:
            return Http404

    def get(self, request):
        lista_projetos = list(Projeto.objects.filter(data_inativado__isnull=True).values('cod_projeto', 'desc_proj'))
        lista_placas = list(CCO_Sinistro.objects.all().values('placa_veiculo_cavalo').distinct())
        lista_motivos_sinistro = list(Motivo_Sinistro.objects.all().values('cod_motivo_sinistro','desc_motivo_sinistro','tipo_motivo_sinistro'))
        lista_estados = list(OP_Estados.objects.all().values('cod_estado','estado'))
        contexto = {
            'lista_projetos': lista_projetos,
            'lista_placas': lista_placas,
            'lista_motivos_sinistro':lista_motivos_sinistro,
            'lista_estados' : lista_estados,
        }
        return render(request, 'cco_sinistro_app/form_cco_cad_sinistros.html', contexto)
    def delete(self, request, pk):
        obj_excluido = self.get_object(pk)
        obj_excluido.delete()
        data = dict()
        data = {
            'msg': 'Registro excluído com sucesso !'

        }
        return JsonResponse(data, safe=False)
# Pesquisa Sinistro de Cargas, equipamentos e veiculos
class Form_Pesq_Cad_Sinistros(View):
    def get(self, request):
        tipo_pesquisa_sinistro = request.GET['tipo_pesquisa_sinistro']
        linhasTabela = []
        if tipo_pesquisa_sinistro == 'placa':
            placa_selecionada = request.GET['placa_selecionada']
            querySinistrosPlaca = CCO_Sinistro.objects.filter(
                placa_veiculo_cavalo = placa_selecionada)
            for registro in querySinistrosPlaca:
                dadosregistro = {
                    'cod_sinistro': registro.cod_sinistro,
                    'nome_mot': registro.nome_mot,
                    'cpf_mot': registro.cpf_mot,
                    'data_nasc': registro.data_nasc,
                    'desc_projeto': registro.cod_projeto.desc_proj if registro.cod_projeto else None,
                    'placa_veiculo_cavalo': registro.placa_veiculo_cavalo,
                    'data_ocorre_sinistro': registro.data_ocorre_sinistro,
                    'desc_motivo_sinistro': registro.cod_motivo_sinistro.desc_motivo_sinistro,
                    'acionado_seguro': registro.acionado_seguro,
                    'num_processo': registro.num_processo,
                    'tipo_sinistro': registro.tipo_sinistro
                }
                linhasTabela.append(dadosregistro)    

        elif tipo_pesquisa_sinistro == 'data':
              competencia_selecionada_inicio = request.GET["inicioCompetencia"]
              competencia_selecionada_final = request.GET["fimCompetencia"]
              data_inicio = datetime.strptime(competencia_selecionada_inicio, "%Y-%m-%d")
              data_final = datetime.strptime(competencia_selecionada_final, "%Y-%m-%d")
              
              querySinistrosCompetencia = CCO_Sinistro.objects.filter(data_ocorre_sinistro__range=[data_inicio,data_final])
              for registro in querySinistrosCompetencia:
                 dadosregistro = {
                     'cod_sinistro': registro.cod_sinistro,
                     'nome_mot': registro.nome_mot,
                     'cpf_mot' : registro.cpf_mot,
                     'data_nasc' : registro.data_nasc,
                    'desc_projeto': registro.cod_projeto.desc_proj if registro.cod_projeto else None,
                    'placa_veiculo_cavalo': registro.placa_veiculo_cavalo,
                    'data_ocorre_sinistro': registro.data_ocorre_sinistro,
                    'desc_motivo_sinistro': registro.cod_motivo_sinistro.desc_motivo_sinistro,
                    'acionado_seguro': registro.acionado_seguro,
                    'num_processo' : registro.num_processo,
                    'tipo_sinistro' : registro.tipo_sinistro
                 }
                 linhasTabela.append(dadosregistro)

        data = dict()
        data = {
            'linhasTabela': linhasTabela
        }    
        return JsonResponse (data,safe = False)
# Cadastro de cargas Sinistros
class Form_Cad_Sinistros_cargas(View):
    # Recebimento de dados do Javascript
    def post (self, request):
        empresaSelecionada = request.POST['empresaSelecionada']
        motoristaCargas = request.POST["motoristaCargas"]
        dt_nascimento_motorista_carga = request.POST["dt_nascimento_motorista_carga"]
        tipoFrota = request.POST["tipoFrota"]
        transportadorVeiculo = request.POST["transportadorVeiculo"]
        placaVeiculo = request.POST["placaVeiculo"]
        projetoVeiculo = request.POST["projetoVeiculo"]
        tipoVeiculo = request.POST["tipoVeiculo"]
        placaCarreta = request.POST["placaCarreta"]
        clienteCarga = request.POST["clienteCarga"]
        numeroNotaCarga = request.POST["numeroNotaCarga"]
        valorProdutosCarga = request.POST["valorProdutosCarga"]
        tipoProdutoCarga = request.POST["tipoProdutoCarga"]
        numeroSerieCarga = request.POST["numeroSerieCarga"]
        dt_ocorrencia_sinistro_carga = request.POST["dt_ocorrencia_sinistro_carga"]
        estado_sinistro_carga = request.POST["sel_estado_sinistro_carga"]
        localSinistro = request.POST["localSinistro"]
        valorSinistro = request.POST["valorSinistro"]
        txt_cidade_sinistro_carga = request.POST["txt_cidade_sinistro_carga"]
        timeSinistro = request.POST["timeSinistro"]
        motivo_sinistro_carga = request.POST["motivo_sinistro_carga"]
        respostaSeguro = request.POST["respostaSeguro"]
        data_abertura_registro_sinistro = request.POST["data_abertura_registro_sinistro"]
        data_fechamento_registro_sinistro = request.POST["data_fechamento_registro_sinistro"]
        seguradoraSinistro = request.POST["seguradoraSinistro"]
        reguladoraSinistro = request.POST["reguladoraSinistro"]
        feitoReembolso = request.POST["feitoReembolso"]
        valorReembolso = request.POST["valorReembolso"]
        numeroProcesso = request.POST["numeroProcesso"]
        dt_abertura_processo_sinistro_carga = request.POST["dt_abertura_processo_sinistro_carga"]
        dt_fim_processo_sinistro_carga = request.POST["dt_fim_processo_sinistro_carga"]
        statusProcesso = request.POST["statusProcesso"]
        txt_obs_cad_carga = request.POST["txt_obs_cad_carga"]
        cod_cad_sinistro_carga_form = request.POST['cod_cad_sinistro_carga']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        # Conversão das datas coletadas em String para modelo de Data
        # se Data de Nascimento for vazia, vai constar como None, caso contrário vai mudar a sequencia para inserção no Banco
        if dt_nascimento_motorista_carga == '':
            dt_nascimento_motorista_carga = None
        else:
            dt_nascimento_motorista_carga = datetime.strptime(dt_nascimento_motorista_carga, '%Y-%m-%d')
        if dt_ocorrencia_sinistro_carga == '':
            dt_ocorrencia_sinistro_carga = None
        else:
            dt_ocorrencia_sinistro_carga = datetime.strptime(dt_ocorrencia_sinistro_carga, '%Y-%m-%d')
        if data_abertura_registro_sinistro == '':
            data_abertura_registro_sinistro = None
        else:
            data_abertura_registro_sinistro = datetime.strptime(data_abertura_registro_sinistro, '%Y-%m-%d')
        if data_fechamento_registro_sinistro == '':
            data_fechamento_registro_sinistro = None
        else:
            data_fechamento_registro_sinistro = datetime.strptime(data_fechamento_registro_sinistro, '%Y-%m-%d')
        if dt_abertura_processo_sinistro_carga == '':
            dt_abertura_processo_sinistro_carga = None
        else:
            dt_abertura_processo_sinistro_carga = datetime.strptime(dt_abertura_processo_sinistro_carga, '%Y-%m-%d')
        if dt_fim_processo_sinistro_carga == '':
            dt_fim_processo_sinistro_carga = None
        else:
            dt_fim_processo_sinistro_carga = datetime.strptime(dt_fim_processo_sinistro_carga, '%Y-%m-%d')

        #hora_sinistro = datetime.strptime(timeSinistro, '%H:%M').time()
        hora_sinistro = None
        if timeSinistro != '' and timeSinistro != None:
            hora_sinistro = timeSinistro

        #Conversão quando Campo Estiver Nulo salvar como Nulo
        if estado_sinistro_carga == '':
            estado_sinistro_carga = None
        else : 
            estado_sinistro_carga = OP_Estados.objects.get(pk=estado_sinistro_carga)


        if cod_cad_sinistro_carga_form == '0':
            sinistro = CCO_Sinistro(
                    data_inclusao = datetime.utcnow(),
                    nome_mot = motoristaCargas,
                    data_nasc = dt_nascimento_motorista_carga,
                    placa_veiculo_cavalo = placaVeiculo,
                    cod_projeto = Projeto.objects.get(pk=projetoVeiculo),
                    data_ocorre_sinistro = dt_ocorrencia_sinistro_carga,
                    cod_estado = estado_sinistro_carga,
                    cidade = txt_cidade_sinistro_carga,
                    tipo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_carga).tipo_motivo_sinistro,
                    data_inicio_processo = dt_abertura_processo_sinistro_carga,
                    num_processo = numeroProcesso,
                    data_fim_processo = dt_fim_processo_sinistro_carga,
                    obs = txt_obs_cad_carga,
                    cod_motivo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_carga),
                    cod_usu = obj_usuario_sessao
                )
            sinistro.save()
            # # Salvando dados no Banco com Base na Model
            sinistro_carga = CCO_Sinistro_Carga(
                cod_sinistro = sinistro, #CCO_Sinistro.objects.get(pk=sinistro.cod_sinistro),
                empresa = empresaSelecionada,
                tipo_frota = tipoFrota,
                transportador = transportadorVeiculo,
                tipo_veiculo = tipoVeiculo,
                cliente = clienteCarga,
                num_nota_fiscal = numeroNotaCarga,
                valor_tot_produtos = valorProdutosCarga,
                tipo_mercadoria = tipoProdutoCarga,
                cte_serie = numeroSerieCarga,
                local_ocorre_sinistro = localSinistro,
                valor_sinistro = valorSinistro,
                hora_sinistro = hora_sinistro,
                resp_seguro = respostaSeguro,
                seguradora = seguradoraSinistro,
                reguladora = reguladoraSinistro,
                reembolso = feitoReembolso,
                val_reembolso = valorReembolso,
                status_doc = statusProcesso,
                placa_veiculo_carreta = placaCarreta,
                data_abertura_registro_sinistro= data_abertura_registro_sinistro,
                data_fechamento_registro_sinistro =data_fechamento_registro_sinistro,

                )
            sinistro_carga.save()
            msg = 'Registro salvo com sucesso!'
        else:
            obj_sinistro_carga = CCO_Sinistro_Carga.objects.get(pk=cod_cad_sinistro_carga_form)
            obj_sinistro = obj_sinistro_carga.cod_sinistro

            obj_sinistro.data_inclusao = datetime.utcnow()
            obj_sinistro.nome_mot = motoristaCargas
            obj_sinistro.data_nasc = dt_nascimento_motorista_carga
            obj_sinistro.placa_veiculo_cavalo = placaVeiculo
            obj_sinistro.cod_projeto = Projeto.objects.get(pk=projetoVeiculo)
            obj_sinistro.data_ocorre_sinistro = dt_ocorrencia_sinistro_carga
            obj_sinistro.estado = estado_sinistro_carga
            obj_sinistro.data_fechamento_registro_sinistro = data_fechamento_registro_sinistro
            obj_sinistro.data_abertura_registro_sinistro = data_abertura_registro_sinistro
            obj_sinistro.cidade = txt_cidade_sinistro_carga
            obj_sinistro.tipo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_carga).tipo_motivo_sinistro
            obj_sinistro.data_inicio_processo = dt_abertura_processo_sinistro_carga
            obj_sinistro.num_processo = numeroProcesso
            obj_sinistro.data_fim_processo = dt_fim_processo_sinistro_carga
            obj_sinistro.cod_motivo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_carga)
            obj_sinistro.obs = txt_obs_cad_carga
            obj_sinistro.save()

            obj_sinistro_carga.empresa = empresaSelecionada
            obj_sinistro_carga.tipo_frota = tipoFrota
            obj_sinistro_carga.transportador = transportadorVeiculo
            obj_sinistro_carga.tipo_veiculo = tipoVeiculo
            obj_sinistro_carga.cliente = clienteCarga
            obj_sinistro_carga.num_nota_fiscal = numeroNotaCarga
            obj_sinistro_carga.valor_tot_produtos = valorProdutosCarga
            obj_sinistro_carga.tipo_mercadoria = tipoProdutoCarga
            obj_sinistro_carga.cte_serie = numeroSerieCarga
            obj_sinistro_carga.local_ocorre_sinistro = localSinistro
            obj_sinistro_carga.valor_sinistro = valorSinistro
            obj_sinistro_carga.hora_sinistro = hora_sinistro
            obj_sinistro_carga.resp_seguro = respostaSeguro
            obj_sinistro_carga.seguradora = seguradoraSinistro
            obj_sinistro_carga.reguladora = reguladoraSinistro
            obj_sinistro_carga.reembolso = feitoReembolso
            obj_sinistro_carga.val_reembolso = valorReembolso
            obj_sinistro_carga.status_doc = statusProcesso
            obj_sinistro_carga.placa_veiculo_carreta = placaCarreta
            obj_sinistro_carga.save()

            msg = 'Registro atualizado com sucesso'

        data = {
            'msg': msg
        }
        return JsonResponse (data,safe = False)
 ##Recebimento de Dados enviados do Javascript para Url e Url para View
class Form_cad_equipamentos_veiculos(View):
    def post (self, request):
        nome_motorista_eqp = request.POST['nome_motorista_eqp']
        dt_nascimento_motorista_eqp = request.POST['dt_nascimento_motorista_eqp']
        cpf_motorista_eqp = request.POST['cpf_motorista_eqp']
        dt_ocorrencia_sinistro_carga_eqp = request.POST['dt_ocorrencia_sinistro_carga_eqp']
        motivo_sinistro_eqp = request.POST['motivo_sinistro_eqp']
        acionado_seguro_eqp = request.POST['acionado_seguro_eqp']
        projeto_eqp = request.POST['projeto_eqp']
        cidade_sinistro_eqp = request.POST['cidade_sinistro_eqp']
        estado_sinistro_eqp = request.POST['estado_sinistro_eqp']
        dt_comunicacao_seguradora_eqp = request.POST['dt_comunicacao_seguradora_eqp']
        dt_comunicacao_cco_eqp = request.POST['dt_comunicacao_cco_eqp']
        responsavel_dano_eqp = request.POST['responsavel_dano_eqp']
        desconto_colaborador_eqp = request.POST['desconto_colaborador_eqp']
        indenizado_eqp = request.POST['indenizado_eqp']
        dano_empresa_eqp = request.POST['dano_empresa_eqp']
        valor_indenizado_eqp = request.POST['valor_indenizado_eqp']
        valor_prejuizo_eqp = request.POST['valor_prejuizo_eqp']
        responsavel_pag_indenizacao_dano_eqp = request.POST['responsavel_pag_indenizacao_dano_eqp']
        feito_reembolso_eqp = request.POST['feito_reembolso_eqp']
        tipo_acionamento_eqp = request.POST['tipo_acionamento_eqp']
        numero_processo_eqp = request.POST['numero_processo_eqp']
        dt_inicio_dados_processo_eqp = request.POST['dt_inicio_dados_processo_eqp']
        dt_fim_processo_sinistro_carga_eqp = request.POST['dt_fim_processo_sinistro_carga_eqp']
        observacoes_finais = request.POST['observacoes_finais']
        placa_cavalo_cad_eqp = request.POST['placa_cavalo_cad_eqp']
        cod_cad_sinistro_eqp_veic = request.POST["cod_cad_sinistro_eqp_veic"]

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)
        

        #Tratamento para que Datas não preenchidas se tornem NUll, caso contrário preencha com data formatada.
        if dt_nascimento_motorista_eqp == '':
            dt_nascimento_motorista_eqp = None
        else:
            dt_nascimento_motorista_eqp = datetime.strptime(dt_nascimento_motorista_eqp, '%Y-%m-%d')
        if dt_ocorrencia_sinistro_carga_eqp == '':
            dt_ocorrencia_sinistro_carga_eqp = None
        else:
            dt_ocorrencia_sinistro_carga_eqp = datetime.strptime(dt_ocorrencia_sinistro_carga_eqp, '%Y-%m-%d')
        if dt_comunicacao_seguradora_eqp == '':
           dt_comunicacao_seguradora_eqp = None
        else:
            dt_comunicacao_seguradora_eqp = datetime.strptime(dt_comunicacao_seguradora_eqp, '%Y-%m-%d')
        if dt_comunicacao_cco_eqp == '':
           dt_comunicacao_cco_eqp = None
        else:
            dt_comunicacao_cco_eqp = datetime.strptime(dt_comunicacao_cco_eqp, '%Y-%m-%d')
        if dt_fim_processo_sinistro_carga_eqp == '':
            dt_fim_processo_sinistro_carga_eqp  = None
        else:
            dt_fim_processo_sinistro_carga_eqp = datetime.strptime(dt_fim_processo_sinistro_carga_eqp, '%Y-%m-%d')
        if dt_inicio_dados_processo_eqp == '':
            dt_inicio_dados_processo_eqp = None
        else:
            dt_inicio_dados_processo_eqp = datetime.strptime(dt_inicio_dados_processo_eqp, '%Y-%m-%d')

       
        #Salvando Dados constituidos na tabela sinistros
        if cod_cad_sinistro_eqp_veic == '0':  
            sinistro = CCO_Sinistro(
                data_inclusao = datetime.utcnow(),
                nome_mot = nome_motorista_eqp,
                cpf_mot = cpf_motorista_eqp,
                placa_veiculo_cavalo = placa_cavalo_cad_eqp,
                data_nasc = dt_nascimento_motorista_eqp,
                data_ocorre_sinistro = dt_ocorrencia_sinistro_carga_eqp,
                cod_estado = OP_Estados.objects.get(pk=estado_sinistro_eqp),
                cidade = cidade_sinistro_eqp,
                tipo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_eqp).tipo_motivo_sinistro,
                acionado_seguro = acionado_seguro_eqp,
                data_inicio_processo = dt_inicio_dados_processo_eqp,
                data_fim_processo = dt_fim_processo_sinistro_carga_eqp,
                num_processo = numero_processo_eqp,
                obs = observacoes_finais,
                cod_projeto = Projeto.objects.get(pk=projeto_eqp),
                cod_usu = obj_usuario_sessao,
                cod_motivo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_eqp)
            )
            sinistro.save()
            sinistro_eqp = CCO_Sinistro_Equipamento(
                cod_sinistro = sinistro,
                data_comunicacao_seguradora = dt_comunicacao_seguradora_eqp,
                data_comunicacao_cco = dt_comunicacao_cco_eqp,
                resp_dano = responsavel_dano_eqp,
                descontado_colab = desconto_colaborador_eqp,
                indenizado = indenizado_eqp,
                houve_danos_emp = dano_empresa_eqp,
                val_indenizado = valor_indenizado_eqp,
                val_prejuizo = valor_prejuizo_eqp,
                resp_indenizar_dano = responsavel_pag_indenizacao_dano_eqp,
                tipo_acionamento = tipo_acionamento_eqp,
                feito_reembolso_eqp = feito_reembolso_eqp
            )
            sinistro_eqp.save()
            msg = 'Cadastro Criado com sucesso!'

        else :
            obj_sinistro_eqp_veic = CCO_Sinistro_Equipamento.objects.get(pk=cod_cad_sinistro_eqp_veic)
            obj_sinistro = obj_sinistro_eqp_veic.cod_sinistro

            # Se o código do botão não estiver vazio ele faz a consulta ao código e atualiza com as informações.
            obj_sinistro.data_inclusao = datetime.utcnow()
            obj_sinistro.nome_mot = nome_motorista_eqp
            obj_sinistro.cpf_mot = cpf_motorista_eqp
            obj_sinistro.placa_veiculo_cavalo = placa_cavalo_cad_eqp
            obj_sinistro.data_nasc = dt_nascimento_motorista_eqp
            obj_sinistro.data_ocorre_sinistro = dt_ocorrencia_sinistro_carga_eqp
            obj_sinistro.cod_estado = OP_Estados.objects.get(pk=estado_sinistro_eqp).estado
            obj_sinistro.cidade = cidade_sinistro_eqp
            obj_sinistro.tipo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_eqp).tipo_motivo_sinistro
            obj_sinistro.acionado_seguro = acionado_seguro_eqp
            obj_sinistro.data_inicio_processo = dt_inicio_dados_processo_eqp
            obj_sinistro.data_fim_processo = dt_fim_processo_sinistro_carga_eqp
            obj_sinistro.num_processo = numero_processo_eqp
            obj_sinistro.obs = observacoes_finais
            obj_sinistro.cod_usu = obj_usuario_sessao
            obj_sinistro.cod_motivo_sinistro = Motivo_Sinistro.objects.get(pk=motivo_sinistro_eqp)
            obj_sinistro.cod_projeto = Projeto.objects.get(pk=projeto_eqp)
            obj_sinistro.save()


            obj_sinistro_eqp_veic.data_comunicacao_seguradora = dt_comunicacao_seguradora_eqp
            obj_sinistro_eqp_veic.data_comunicacao_cco = dt_comunicacao_cco_eqp
            obj_sinistro_eqp_veic.resp_dano = responsavel_dano_eqp
            obj_sinistro_eqp_veic.descontado_colab = desconto_colaborador_eqp
            obj_sinistro_eqp_veic.indenizado = indenizado_eqp
            obj_sinistro_eqp_veic.houve_danos_emp = dano_empresa_eqp
            obj_sinistro_eqp_veic.val_indenizado = valor_indenizado_eqp
            obj_sinistro_eqp_veic.val_prejuizo = valor_prejuizo_eqp
            obj_sinistro_eqp_veic.resp_indenizar_dano = responsavel_pag_indenizacao_dano_eqp
            obj_sinistro_eqp_veic.tipo_acionamento = tipo_acionamento_eqp
            obj_sinistro_eqp_veic.feito_reembolso_eqp = feito_reembolso_eqp
            obj_sinistro_eqp_veic.save()

            msg = 'Registro atualizado com sucesso!'
        data = {
            'msg': msg
        }

        return JsonResponse( data, safe = False)
class Comp_Placas_View(View):
    
    def get(self, request):
        lista_placas = list(CCO_Sinistro.objects.all().values('placa_veiculo_cavalo').distinct())
        data = dict()
        data = {
            'lista_placas':lista_placas
        }
        return JsonResponse (data,safe = False)
class Form_Edita_Cadastros_View(View):
    def get (self, request):
        #Coleta de váriaveis enviadas na URl pelo Javascript.
        tipo_sinistro_form = request.GET['tipo_sinistro']
        cod_sinistro_form = request.GET['cod_sinistro']
        obj_sinistro = CCO_Sinistro.objects.get(pk=cod_sinistro_form)
        obj_sinistro_carga = CCO_Sinistro_Carga.objects.filter(cod_sinistro=obj_sinistro).first()
        #Defino uma variável e nela puxo todos os objetos atrelados ao código que coletei lá do meu javascript posteriormente do html
        dic_sinistro_form = None
        if tipo_sinistro_form == 'C':
            cod_estado = ''
            if obj_sinistro.cod_estado != None:
                cod_estado = obj_sinistro.cod_estado.cod_estado
            cod_projeto = ''
            if obj_sinistro.cod_projeto is not None:
                cod_projeto = obj_sinistro.cod_projeto.cod_projeto
            cod_motivo_sinistro = ''
            if obj_sinistro.cod_motivo_sinistro is not None:
                cod_motivo_sinistro = obj_sinistro.cod_motivo_sinistro.cod_motivo_sinistro

            dic_sinistro_form = {
                #DADOS DO MOTORISTA
                'cod_sinistro_carga': obj_sinistro_carga.cod_sinistro_carga,
                'nome_mot': obj_sinistro.nome_mot,
                'dat_nasc': obj_sinistro.data_nasc,  ##data Nascimento motorista
                'empresa': obj_sinistro_carga.empresa,
                #DADOS DO VEICULO
                'tipo_frota': obj_sinistro_carga.tipo_frota,
                'cod_projeto': cod_projeto,
                'placa_veiculo_cavalo': obj_sinistro.placa_veiculo_cavalo,
                'transportador': obj_sinistro_carga.transportador,
                'tipo_veiculo':obj_sinistro_carga.tipo_veiculo,
                'placa_veiculo_carreta':obj_sinistro_carga.placa_veiculo_carreta,
                #DADOS DA CARGA
                'cliente': obj_sinistro_carga.cliente,
                'nota_fiscal': obj_sinistro_carga.num_nota_fiscal,
                'valor_produtos': obj_sinistro_carga.valor_tot_produtos,
                'tipo_mercadoria': obj_sinistro_carga.tipo_mercadoria,
                'cte_serie': obj_sinistro_carga.cte_serie,
                #DADOS DO SINISTRO
                'data_ocorre_sinistro': obj_sinistro.data_ocorre_sinistro,
                'valor_sinistro_carga': obj_sinistro_carga.valor_sinistro,
                'cod_estado': cod_estado,
                'cidade': obj_sinistro.cidade,
                'hora_sinistro': obj_sinistro_carga.hora_sinistro,
                'local_Sinistro':cod_estado,
                'cod_motivo_sinistro': cod_motivo_sinistro,
                'resp_seguro':obj_sinistro_carga.resp_seguro,
                #DADOS REGISTRO DO SINISTRO
                'reguladora_sinistro': obj_sinistro_carga.reguladora,
                'data_abertura_registro_sinistro': obj_sinistro_carga.data_abertura_registro_sinistro,
                'data_fechamento_registro_sinistro': obj_sinistro_carga.data_fechamento_registro_sinistro,
                'valor_reembolso': obj_sinistro_carga.val_reembolso,
                'seguradora': obj_sinistro_carga.seguradora,
                'feito_reembolso': obj_sinistro_carga.reembolso,
                #DADOS DO PROCESSO
                'data_abertura_processo': obj_sinistro.data_inicio_processo,
                'data_fechamento_processo' : obj_sinistro.data_fim_processo,
                'num_processo': obj_sinistro.num_processo,
                #DOCUMENTAÇÃO E COMPLEMENTOS
                'observacao': obj_sinistro.obs,
                'status_processo': obj_sinistro_carga.status_doc
            }
        elif tipo_sinistro_form == 'E':
            obj_sinistro_eqp_veic = CCO_Sinistro_Equipamento.objects.filter(cod_sinistro=obj_sinistro).first()
            cod_estado = ''
            if obj_sinistro.cod_estado != None:
                cod_estado = obj_sinistro.cod_estado.cod_estado
            cod_projeto = ''
            if obj_sinistro.cod_projeto is not None:
                cod_projeto = obj_sinistro.cod_projeto.cod_projeto
            cod_motivo_sinistro = ''
            if obj_sinistro.cod_motivo_sinistro is not None:
                cod_motivo_sinistro = obj_sinistro.cod_motivo_sinistro.cod_motivo_sinistro


            dic_sinistro_form = {
               'cod_sinistro_eqp_veic': obj_sinistro_eqp_veic.cod_sinistro_equipamento,
               #  Dados do motorista
               'nome_mot': obj_sinistro.nome_mot,
               'data_nasc': obj_sinistro.data_nasc,
               'cpf_mot': obj_sinistro.cpf_mot,
               # Dados do veiculo
               'cod_projeto': cod_projeto,
               'placa_veiculo_cavalo': obj_sinistro.placa_veiculo_cavalo,
               # Dados do Sinistro
               'cod_motivo_sinistro': cod_motivo_sinistro,
               'data_ocorre_sinistro': obj_sinistro.data_ocorre_sinistro,
               'cidade': obj_sinistro.cidade,
               'cod_estado': cod_estado,
               'acionado_seguro': obj_sinistro.acionado_seguro,
               # Comunicação Sinistro
               'data_comunicacao_seguradora': obj_sinistro_eqp_veic.data_comunicacao_seguradora,
               'data_comunicacao_cco': obj_sinistro_eqp_veic.data_comunicacao_cco,
               #Informações Adicionais
               'resp_indenizar_dano': obj_sinistro_eqp_veic.resp_indenizar_dano,
               'val_prejuizo': obj_sinistro_eqp_veic.val_prejuizo,
                'indenizado': obj_sinistro_eqp_veic.indenizado,
               'resp_dano': obj_sinistro_eqp_veic.resp_dano,
               'val_indenizado': obj_sinistro_eqp_veic.val_indenizado,
               'houve_danos_emp': obj_sinistro_eqp_veic.houve_danos_emp,
               'descontado_colab': obj_sinistro_eqp_veic.descontado_colab,
                'tipo_acionamento': obj_sinistro_eqp_veic.tipo_acionamento,
                'feito_reembolso_eqp': obj_sinistro_eqp_veic.feito_reembolso_eqp,
               # Dados do Processo
               'num_processo': obj_sinistro.num_processo,
               'data_inicio_processo': obj_sinistro.data_inicio_processo,
               'data_fim_processo': obj_sinistro.data_fim_processo,
               'observacao': obj_sinistro.obs
            }
        data = dict()
        data = {
            'dic_sinistro_form': dic_sinistro_form
        }
        return JsonResponse (data, safe= False)