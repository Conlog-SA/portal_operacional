from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.utils import timezone
from apps.conecta_senior_app.views import Conexao_Senior_BD

# from apps.gente_gestao_fluxo_punitivo.models import Verbas_Erros_de_Pagamentos, Erros_de_Pagamento
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario
from apps.gente_gestao_fluxo_punitivo.models import Gente_Gestao_Motivo_Juridico, Gente_Gestao_Motivo_Especifico, \
    Gente_Gestao_Punicao, Gente_Gestao_Dias_Suspensao



class Form_Fluxo_Punitivo(View):
    def get(self, request):

        lista_obj_filiais = Filial.objects.all()
        lista_motivo_juridico = Gente_Gestao_Motivo_Juridico.objects.all()
        lista_motivo_especifico = Gente_Gestao_Motivo_Especifico.objects.all()

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        contexto = {
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_obj_filiais': lista_obj_filiais,
            'lista_motivo_juridico': lista_motivo_juridico,
            'lista_motivo_especifico': lista_motivo_especifico,
        }
        return render(request, 'gente_gestao_fluxo_punitivo/fluxo_punitivo.html', contexto)

    def post(self, request):
        id_filial_form = request.POST["idFilialSelecionada"]
        obj_filial = Filial.objects.get(pk=id_filial_form)

        cod_senior_colab = request.POST["codSeniorColaborador"]
        info_senior_colab = Listar_Colaboradores.lista_dados_colab(cod_senior_colab)
        nome_colab = info_senior_colab[0]["nome_colab"]
        cod_tipo_penalidade = request.POST["codPenalidade"]

        cod_motivo_juridico = request.POST["codMotivoJuridico"]
        obj_motivo_juridico = Gente_Gestao_Motivo_Juridico.objects.get(pk=cod_motivo_juridico)

        cod_motivo_especifico = request.POST["codMotivoEspecifico"]
        obj_motivo_especifico = Gente_Gestao_Motivo_Especifico.objects.get(pk=cod_motivo_especifico)

        data_ocorrencia = request.POST["dataOcorrencia"]
        desc_ocorrencia = request.POST["textOcorrencia"]
        observacao = request.POST["textObs"]

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        if cod_tipo_penalidade == "S":
            qtde_dias_suspensao = request.POST["diasSuspensao"]
        else:
            pass

        punicaoLancada = Gente_Gestao_Punicao(
            nome_colab=nome_colab,
            matricula_colab=cod_senior_colab,
            data_admissao=info_senior_colab[0]["data_admissao_colab"],
            cpf_colab=info_senior_colab[0]["cpf_colab"],
            cod_cargo_colab=info_senior_colab[0]["cod_cargo_colab"],
            desc_cargo_colab=info_senior_colab[0]["desc_cargo_colab"],
            situacao_colab=info_senior_colab[0]["situacao_colab"],
            penalidade=cod_tipo_penalidade,
            data_ocorrencia=data_ocorrencia,
            desc_motivo=desc_ocorrencia,
            obs_punicao=observacao,
            cod_filial=obj_filial,
            cod_mot_juridico=obj_motivo_juridico,
            cod_usu=obj_usuario_sessao,
            cod_mot_especifico=obj_motivo_especifico
        )
        punicaoLancada.save()

        if cod_tipo_penalidade == "S":
            qtde_dias_suspensao = request.POST["diasSuspensao"]
            data_ocorrencia = datetime.strptime(data_ocorrencia, "%Y-%m-%d")
            lancamentoSuspensao = Gente_Gestao_Dias_Suspensao(
                inicio_suspensao=data_ocorrencia,
                fim_suspensao=data_ocorrencia + timedelta(int(qtde_dias_suspensao)) - timedelta(1),
                cod_punicao=punicaoLancada
            )
            lancamentoSuspensao.save()
        else:
            pass

        data = {}
        return JsonResponse(data, safe=False)


class Listar_Colaboradores(View):
    def get(self, request):
        info_buscada = request.GET['infoBuscada']

        if info_buscada == 'lista_colabs':
            id_filial = request.GET['id_filial']
            id_empresa_senior = Filial.objects.get(pk=id_filial).cod_empresa
            id_filial_senior = Filial.objects.get(pk=id_filial).cod_filial_senior
            banco_senior = Conexao_Senior_BD()
            lista_colaboradores = banco_senior.listar_colaboradores_filial(id_empresa_senior, id_filial_senior)

            data = {
                'lista_colaboradores': lista_colaboradores,
            }
            return JsonResponse(data, safe=False)

        elif info_buscada == 'dados_colab':
            id_senior_colab = request.GET['idColab']

            banco_senior = Conexao_Senior_BD()
            dados_colab = banco_senior.listar_dados_colaborador(id_senior_colab)

            data = {
                'dados_colab': dados_colab,
            }
            return JsonResponse(data, safe=False)

    def lista_dados_colab(matricula_senior):
        banco_senior = Conexao_Senior_BD()
        dados_colab = banco_senior.listar_dados_colaborador(matricula_senior)
        return dados_colab


class Criacao_Motivos(View):
    def post(self, request):
        tipo_motivo = request.POST['tipo_motivo']

        if tipo_motivo == "juridico":
            desc_novo_motivo = request.POST['novo_motivo']
            novo_motivo = Gente_Gestao_Motivo_Juridico(desc_motivo_juridico=desc_novo_motivo.upper())
            novo_motivo.save()

        elif tipo_motivo == "especifico":
            desc_novo_motivo = request.POST['novo_motivo']
            novo_motivo = Gente_Gestao_Motivo_Especifico(desc_motivo_especifico=desc_novo_motivo.upper())
            novo_motivo.save()

        data = {}
        return JsonResponse(data, safe=False)


class Tabelaa_Fluxos(View):
    def get(self, request):
        obj_filial_pesquisa = Filial.objects.get(pk=int(request.GET['filialPesquisada']))
        competencia_pesquisa = datetime.strptime(request.GET['competenciaPesquisa'], "%Y-%m")

        query_lancamentos_pesquisa = Gente_Gestao_Punicao.objects.filter(
            data_ocorrencia__year=competencia_pesquisa.year, data_ocorrencia__month=competencia_pesquisa.month,
            cod_filial=obj_filial_pesquisa)

        linhas_tabela = []
        for linha in query_lancamentos_pesquisa:
            registro = {
                'cod_punicao': linha.cod_punicao,
                'matricula': linha.matricula_colab,
                'nome_colab': linha.nome_colab,
                'cargo': linha.desc_cargo_colab,
                'data_ocorrencia': linha.data_ocorrencia,
                'motivo_juridico': linha.cod_mot_juridico.desc_motivo_juridico,
                'motivo_especifico': linha.cod_mot_especifico.desc_motivo_especifico,
                'id_lancamento': linha.cod_punicao,
                'ativo': linha.ativo,
                'obs_punicao' : linha.obs_punicao
            }

            linhas_tabela.append(registro)

        data = {
            'linhas_tabela': linhas_tabela
        }
        return JsonResponse(data, safe=False)
    

class Cancela_Punicao(View):
    def post(self, request):
        cod_punicao = request.POST['cod_punicao']
        ativo = request.POST['ativo']
        obs_punicao_novo = request.POST['obs_punicao']


        if ativo == 'N' :
            
            obj_punicao = get_object_or_404(Gente_Gestao_Punicao, pk=cod_punicao)

             # Recupera o valor atual de obs_punicao
            obs_punicao_atual = obj_punicao.obs_punicao if obj_punicao.obs_punicao else ""

             # Concatena os dados antigos com os novos
            obs_punicao_atual += f"\nNovos dados: {obs_punicao_novo}"

            obj_punicao.data_desativacao = timezone.now()
            obj_punicao.ativo = ativo
            obj_punicao.obs_punicao = obs_punicao_atual


            obj_punicao.save()

            data = {}

            return JsonResponse(data, safe=False)
        