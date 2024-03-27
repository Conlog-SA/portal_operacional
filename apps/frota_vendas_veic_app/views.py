import locale
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_vendas_veic_app.models import Tabela_Preco_Veic, Veiculo_Venda, Veiculo_Venda_Tab, Marca_Tabela_Fipe, \
    Modelo_Tabela_Fipe


# Create your views here.
class Form_Venda_Veic_View(View):
    def get(self, request):
        lista_tab = Tabela_Preco_Veic.objects.all()
        contexto = {
            'lista_tab': lista_tab
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
            obj_veic_venda_tab = Veiculo_Venda_Tab.objects.filter(cod_veic=obj_veic, cod_tab_precos=obj_tab).first()
            if obj_veic_venda_tab == None:
                obj_veic_venda_tab = Veiculo_Venda_Tab(
                    tipo_veic = '',
                    ano = None,
                    codigo_veic_tab = None,
                    competencia = None,
                    val_comp = 0.00,
                    cod_tab_precos = obj_tab,
                    cod_veic = obj_veic,
                    cod_modelo_tab_fipe = None
                )
                obj_veic_venda_tab.save()
            else:
                if obj_veic_venda_tab.cod_modelo_tab_fipe != None:
                    cod_marca = obj_veic_venda_tab.cod_modelo_tab_fipe.cod_marca_tab_fipe.cod_marca_tab_fipe
                    cod_modelo = obj_veic_venda_tab.cod_modelo_tab_fipe.cod_modelo_tab_fipe


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
                'placa': obj_veic.placa,
                'renavam': obj_veic.renavam,
                'tipo': obj_veic.tipo_veic,
                'eixo': obj_veic.eixo,
                'marca': obj_veic.marca,
                'modelo': obj_veic.modelo,
                'ano': obj_veic.ano,
                'filial': obj_veic.nome_filial,
                'status_benner': obj_veic.status_ativo_benner,
                'nf_venda': obj_veic.num_nf_venda,
                'data_venda': data_venda,
                'val_venda': val_venda,
                'tipo_veic_tab': obj_veic_venda_tab.tipo_veic,
                'marca_tab': cod_marca,
                'modelo_tab': cod_modelo,
                'codigo_veic_tab': obj_veic_venda_tab.codigo_veic_tab,
                'periodo_pesq': competencia,
                'val_fipe': val_fipe,
                'cod_veic_venda_tab': obj_veic_venda_tab.cod_veic_venda_tab
            }
            lista_veic_vendas.append((veic_vendas))


        dic_marcas = []
        lista_marcas = Marca_Tabela_Fipe.objects.all()
        for marca in lista_marcas:
            lista_modelos = Modelo_Tabela_Fipe.objects.filter(cod_marca_tab_fipe=marca)
            dic_modelos = []
            for modelo in lista_modelos:
                mod = {
                    'cod_modelo': modelo.cod_modelo_tab_fipe,
                    'desc_modelo': modelo.desc_modelo,
                    'cod_marca': modelo.cod_marca_tab_fipe.cod_marca_tab_fipe
                }
                dic_modelos.append(mod)
            m = {
                'cod_marca': marca.cod_marca_tab_fipe,
                'desc_marca': marca.desc_marca,
                'lista_modelos': dic_modelos
            }
            dic_marcas.append(m)


        data = dict()
        data = {
            'lista_veic_vendas': lista_veic_vendas,
            'dic_marcas': dic_marcas
        }
        return JsonResponse(data, safe=False)

