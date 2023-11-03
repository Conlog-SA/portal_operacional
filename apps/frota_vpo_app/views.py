from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_vpo_app.models import Vincula_Roteiro_Pecas


# Create your views here.

class Form_Vincula_Roteiro_Pecas_View(View):
    def get(self, request):
        lista_roteiros_benner = ConexaoBancoBenner().retorna_roteiros_frota()
        lista_roteiros_pecas = Vincula_Roteiro_Pecas.objects.all()
        context = {
            'lista_roteiros_benner': lista_roteiros_benner,
            'lista_roteiros_pecas': lista_roteiros_pecas
        }
        return render(request, 'frota_vpo_app/form_vincula_roteiros_pecas.html', context)

class Comp_Descricao_Prod_Benner_View(View):
    def get(self, request):
        cod_ref_form = request.GET['cod_ref']
        descricao_item_benner = ConexaoBancoBenner().retorna_descricao_prod_cod_ref(cod_ref_form)
        data = dict()
        data = {
            'descricao_item_benner': descricao_item_benner
        }
        return JsonResponse(data, safe=False)


class Vincular_Roteiro_Peca_View(View):
    def get_object(self, pk):
        try:
            return Vincula_Roteiro_Pecas.objects.get(pk=pk)
        except Vincula_Roteiro_Pecas.DoesNotExist:
            return Http404

    def post(self, request):
        handles_chave_vinculo_form = request.POST['handles_chave_vinculo']
        desc_dados_vinculo_form = request.POST['desc_dados_vinculo']
        cod_ref_item_form = request.POST['cod_ref_item']
        desc_item_form = request.POST['desc_item']
        un_item_form = request.POST['un_item']
        qtd_item_form = request.POST['qtd_item']
        troca_obgo_form = request.POST['troca_obgo']
        troca_obgo_boolean = False
        if troca_obgo_form == 'true':
            troca_obgo_boolean = True
        msg = ''

        try:
            for i,handle_roteiro in enumerate(handles_chave_vinculo_form.split(',')):
                obj_vinculo = Vincula_Roteiro_Pecas(
                    cod_roteiro_peca= int(str(handle_roteiro.split('_')[0])+
                                          str(handle_roteiro.split('_')[1])+
                                          str(handle_roteiro.split('_')[2])+
                                          cod_ref_item_form),
                    handle_roteiro = handle_roteiro.split('_')[0],
                    nome_roteiro = desc_dados_vinculo_form.split(',')[i].split('/')[0],
                    handle_marca = handle_roteiro.split('_')[1],
                    nome_marca = desc_dados_vinculo_form.split(',')[i].split('/')[1],
                    handle_modelo = handle_roteiro.split('_')[2],
                    nome_modelo = desc_dados_vinculo_form.split(',')[i].split('/')[2],
                    handle_tipo_veiculo = handle_roteiro.split('_')[3],
                    nome_tipo_veiculo = desc_dados_vinculo_form.split(',')[i].split('/')[3],
                    cod_ref_item = cod_ref_item_form,
                    desc_item = desc_item_form,
                    un_item = un_item_form,
                    qtd = qtd_item_form,
                    troca = troca_obgo_boolean
                )
                obj_vinculo.save()
            msg = 'Vinculo realizado com sucesso!'
        except Exception as erro:
            msg = 'Ocorreu algum erro ao vincular os registro. Verifique com o adm!' + str(erro)
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)

    def get(self, request):
        roteiros_pecas = Vincula_Roteiro_Pecas.objects.all()
        lista_roteiros_pecas = []
        for reg in roteiros_pecas:
            roteiro = {
                'cod_roteiro_peca': reg.cod_roteiro_peca,
                'nome_roteiro': reg.nome_roteiro,
                'nome_marca': reg.nome_marca,
                'nome_modelo': reg.nome_modelo,
                'cod_ref_item':reg.cod_ref_item,
                'desc_item':reg.desc_item,
                'un_item':reg.un_item,
                'qtd':reg.qtd,
                'troca':reg.troca
            }
            lista_roteiros_pecas.append(roteiro)
        data = dict()
        data = {
            'lista_roteiros_pecas': lista_roteiros_pecas
        }
        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        obj_vincula_roteiro_peca = self.get_object(pk)
        obj_vincula_roteiro_peca.delete()
        data = dict()
        data = {
            'msg': 'Registro desvinculado com sucesso !'
        }
        return JsonResponse(data, safe=False)


