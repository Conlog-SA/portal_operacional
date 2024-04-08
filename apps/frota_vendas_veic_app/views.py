import locale
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_vendas_veic_app.models import Tabela_Preco_Veic, Veiculo_Venda, Veiculo_Venda_Tab_Precos, \
    Marca_Tab_Precos, Tipo_Veic_Tab_Precos, Modelo_Tab_Precos


# Create your views here.
class Form_Venda_Veic_View(View):
    def get(self, request):
        lista_tab = Tabela_Preco_Veic.objects.all()



        contexto = {
            'lista_tab': lista_tab,

        }
        return render(request, 'frota_vendas_veic_app/frm_vendas_veic.html', contexto)

    def post(self, request):
        cod_tab_frm = request.POST['cod_tab']
        mostra_veic_vendidos_frm = request.POST['mostra_veic_vendidos']
        data_hora_atual = datetime.now()
        obj_tab = Tabela_Preco_Veic.objects.get(pk=cod_tab_frm)
        lista_veic_vendas = []
        lista_veic_vendas_benner = ConexaoBancoBenner().retorna_veiculos_proj_vendas(mostra_veic_vendidos_frm)
        for veic_benner in lista_veic_vendas_benner:
            obj_veic = Veiculo_Venda.objects.filter(handle_veic=veic_benner['handle_veic']).first()
            if obj_veic == None:
                obj_veic = Veiculo_Venda(
                    handle_veic = veic_benner['handle_veic'],
                    placa = veic_benner['placa_veic'],
                    eixo = veic_benner['eixo_veic'],
                    tipo_veic = veic_benner['desc_tipo_veic'],
                    renavam = veic_benner['renavam_veic'],
                    uf_compra = veic_benner['estado_compra_veic'],
                    marca = veic_benner['desc_marca_veic'],
                    modelo = veic_benner['desc_modelo_veic'],
                    ano = veic_benner['ano_veic'],
                    nome_filial = veic_benner['nome_filial_veic'],
                    status_ativo_benner = veic_benner['status_ativo_veic'],
                    num_nf_venda = veic_benner['num_nf_veic'],
                    data_venda = veic_benner['data_venda_veic'],
                    val_venda = veic_benner['val_venda_veic'],
                    nome_cliente = veic_benner['nome_comprador']
                )
                obj_veic.save()
            else:
                obj_veic.status_ativo_benner = veic_benner['status_ativo_veic']
                obj_veic.num_nf_venda = veic_benner['num_nf_veic']
                obj_veic.data_venda = veic_benner['data_venda_veic']
                obj_veic.val_venda = veic_benner['val_venda_veic']
                obj_veic.nome_cliente = veic_benner['nome_comprador']
                obj_veic.save()

            cod_marca = None
            cod_modelo = None
            cod_tipo_veic_tab = None
            obj_veic_venda_tab = (Veiculo_Venda_Tab_Precos.objects
                                  .filter(cod_veic=obj_veic,
                                          cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab.cod_tab_precos).first())
            if obj_veic_venda_tab == None:
                obj_veic_venda_tab = Veiculo_Venda_Tab_Precos(
                    ano = None,
                    codigo_veic_tab = None,
                    competencia = None,
                    val_comp = 0.00,
                    cod_veic = obj_veic,
                    cod_modelo_tab_precos = None
                )
                obj_veic_venda_tab.save()
            else:
                if obj_veic_venda_tab.cod_modelo_tab_fipe != None:
                    cod_marca = obj_veic_venda_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_marca_tab_precos
                    cod_modelo = obj_veic_venda_tab.cod_modelo_tab_precos.cod_modelo_tab_precos
                    cod_tipo_veic_tab = obj_veic_venda_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_tipo_veic_tab_precos.cod_tipo_veic_tab_precos


            locale.setlocale(locale.LC_MONETARY, 'pt-BR')
            val_venda = 0.00
            if obj_veic.val_venda != None:
                val_venda = locale.currency(round(obj_veic.val_venda, 2), grouping=True, symbol=None)

            val_fipe = 0.00
            if obj_veic_venda_tab.val_comp != None:
                val_fipe = locale.currency(round(obj_veic_venda_tab.val_comp, 2), grouping=True, symbol=None)

            data_venda = ''
            if obj_veic.data_venda != None:
                data_venda = datetime.strptime(obj_veic.data_venda, '%Y-%m-%d').strftime('%d-%m-%Y')

            competencia = ''
            if obj_veic_venda_tab.competencia != None:
                competencia = datetime.strftime(obj_veic_venda_tab.competencia, '%m-%Y')





            veic_vendas = {
                'cod_veic': obj_veic.cod_veic, #0
                'placa': obj_veic.placa, #1
                'renavam': obj_veic.renavam, #2
                'tipo': obj_veic.tipo_veic, #3
                'eixo': obj_veic.eixo, #4
                'marca': obj_veic.marca, #5
                'modelo': obj_veic.modelo, #6
                'ano': obj_veic.ano, #7
                'filial': obj_veic.nome_filial, #8
                'status_benner': obj_veic.status_ativo_benner, #9
                'nf_venda': obj_veic.num_nf_venda, #10
                'data_venda': data_venda, #11
                'val_venda': val_venda, #12
                'tipo_veic_tab': cod_tipo_veic_tab, #13
                'marca_tab': cod_marca, #14
                'modelo_tab': cod_modelo, #15
                'codigo_veic_tab': obj_veic_venda_tab.codigo_veic_tab, #16
                'periodo_pesq': competencia, #17
                'val_fipe': val_fipe, #18
                'cod_veic_venda_tab': obj_veic_venda_tab.cod_veic_venda_tab #19
            }
            lista_veic_vendas.append((veic_vendas))

            dic_tipo_veic = list(Tipo_Veic_Tab_Precos.objects
                          .filter(cod_tab_precos=obj_tab)
                          .values('cod_tipo_veic_tab_precos', 'desc_tipo_veic'))


        data = dict()
        data = {
            'lista_veic_vendas': lista_veic_vendas,
            'dic_tipo_veic': dic_tipo_veic
        }
        return JsonResponse(data, safe=False)


class Form_Componente_Select_Tipo_Veic_Marcas_Modelo_View(View):
    def get(self, request):
        tipo_pesq_frm = request.GET['tipo_pesq']
        lista_marcas = []
        lista_modelos = []
        if tipo_pesq_frm == 'carrega_dados_veic_tab':
            cod_modelo_tabela_frm = request.GET['cod_modelo_tabela']
            obj_modelo_tab = Modelo_Tab_Precos.objects.get(pk=cod_modelo_tabela_frm)
            lista_modelos = list(Modelo_Tab_Precos.objects
                                 .filter(cod_marca_tab_precos=obj_modelo_tab.cod_marca_tab_precos)
                                 .values('cod_modelo_tab_precos', 'desc_modelo'))
            lista_marcas = list(Marca_Tab_Precos.objects
                                .filter(cod_tipo_veic_tab_precos=obj_modelo_tab.cod_marca_tab_precos.cod_tipo_veic_tab_precos)
                                .values('cod_marca_tab_precos', 'desc_marca'))
        elif tipo_pesq_frm == 'carrega_dados_marca':
            cod_tipo_veic_frm = request.GET['cod_tipo_veic']
            obj_tipo_veic = Tipo_Veic_Tab_Precos.objects.get(pk=cod_tipo_veic_frm)

            lista_marcas = list(Marca_Tab_Precos.objects
                                .filter(cod_tipo_veic_tab_precos=obj_tipo_veic)
                                .values('cod_marca_tab_precos', 'desc_marca'))
        elif tipo_pesq_frm == 'carrega_dados_modelos':
            cod_marca_tab = request.GET['cod_marca_tab']
            obj_marca_tab = Marca_Tab_Precos.objects.get(pk=cod_marca_tab)
            lista_modelos = list(Modelo_Tab_Precos.objects
                                 .filter(cod_marca_tab_precos=obj_marca_tab)
                                 .values('cod_modelo_tab_precos', 'desc_modelo'))


        data = dict()
        data = {
            'lista_marcas': lista_marcas,
            'lista_modelos': lista_modelos
        }
        return JsonResponse(data, safe=False)

