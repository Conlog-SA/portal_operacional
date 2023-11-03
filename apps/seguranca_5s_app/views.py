from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from apps.seguranca_5s_app.models import Cadastro_5s


class Form_5s_View(View):
    def get(self, request):
        return render(request, 'seguranca_5s_app/form_registra_reg_5s.html')


class Cadastro_5s_View(View):
    def get(self, request):
        lista_registros_5s = Cadastro_5s.objects.all()

    def post(self, request):
        data_lancamento = request.POST['data_lancamento']
        filial = request.POST['filial']
        matricula_motorista = request.POST['matricula_motorista']
        placa = request.POST['placa']
        avaliador = request.POST['avaliador']
        mapa = request.POST['mapa']
        cabine_livre = request.POST['cabine_livre']
        doc_veiculo_lug_adequado = request.POST['doc_veiculo_lug_adequado']
        estofado_bom = request.POST['estofado_bom']
        aparelho_trk_bom = request.POST['aparelho_trk_bom']
        notas_organizadas = request.POST['notas_organizadas']
        baias_bom = request.POST['baias_bom']
        chapatex_organizados = request.POST['chapatex_organizados']
        plast_papel_segregados = request.POST['plast_papel_segregados']
        pallets_bom = request.POST['pallets_bom']
        vasilhames_separados = request.POST['vasilhames_separados']
        cabine_limpa = request.POST['cabine_limpa']
        baias_limpas = request.POST['baias_limpas']
        eqpe_saber_func_limp = request.POST['eqpe_saber_func_limp']
        eqpe_saber_func_s = request.POST['eqpe_saber_func_s']
        eqpe_saber_func_rotina_aud = request.POST['eqpe_saber_func_rotina_aud']
        eqpe_recorda_gaps = request.POST['eqpe_recorda_gaps']
        eqpq_saber_prog_reconhecimento = request.POST['eqpq_saber_prog_reconhecimento']
        button_inserir = request.POST['button_inserir']
        obs = request.POST['obs']
        ajudante_1 = request.POST['ajudante_1']
        ajudante_2 = request.POST['ajudante_2']

        if button_inserir == '0':
            obj_5s = Cadastro_5s(
                data_lancamento=data_lancamento,
                desc_filial=filial,
                matricula_motorista=matricula_motorista,
                placa=placa,
                nome_avaliador=avaliador,
                mapa=mapa,
                cabine_livre=cabine_livre,
                doc_lugar_adequado=doc_veiculo_lug_adequado,
                estofado_bom=estofado_bom,
                aparelho_trk_bom=aparelho_trk_bom,
                baias_bom=baias_bom,
                notas_organizadas=notas_organizadas,
                chapatex_organizados=chapatex_organizados,
                plast_papel_segregados=plast_papel_segregados,
                pallets_bom=pallets_bom,
                vasilhames_separados=vasilhames_separados,
                cabine_limpa=cabine_limpa,
                baias_limpas=baias_limpas,
                eqpe_saber_func_limp=eqpe_saber_func_limp,
                eqpe_saber_func_s=eqpe_saber_func_s,
                eqpe_saber_func_rotina_aud=eqpe_saber_func_rotina_aud,
                eqpe_recorda_gaps=eqpe_recorda_gaps,
                eqpq_saber_prog_reconhecimento=eqpq_saber_prog_reconhecimento,
                ajudante_1=ajudante_1,
                ajudante_2=ajudante_2,
                obs=obs

            )
            obj_5s.save()
            msg = 'Cadastro Criado com sucesso!'

            data = {
                'msg': msg
            }
            return JsonResponse(data, safe=False)

