import locale
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.benner_app.views import ConexaoBancoBenner
from apps.frota_vendas_veic_app.models import Tabela_Preco_Veic, Veiculo_Venda, Veiculo_Venda_Tab_Precos, \
    Marca_Tab_Precos, Tipo_Veic_Tab_Precos, Modelo_Tab_Precos, Ano_Modelo_Tab_Precos

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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
            cod_ano_modelo = None
            obj_veic_venda_tab = (Veiculo_Venda_Tab_Precos.objects
                                  .filter(cod_veic=obj_veic,
                                          cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab.cod_tab_precos).first())
            if obj_veic_venda_tab == None:
                obj_veic_venda_tab = Veiculo_Venda_Tab_Precos(
                    codigo_veic_tab = None,
                    competencia = None,
                    val_comp = 0.00,
                    cod_veic = obj_veic,
                    cod_ano_modelo_tab = None
                )
                obj_veic_venda_tab.save()
            else:
                if obj_veic_venda_tab.cod_ano_modelo_tab != None:
                    cod_ano_modelo = obj_veic_venda_tab.cod_ano_modelo_tab.cod_ano_modelo_tab
                    cod_marca = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_marca_tab_precos
                    cod_modelo = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_modelo_tab_precos
                    cod_tipo_veic_tab = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_tipo_veic_tab_precos.cod_tipo_veic_tab_precos


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
                'cod_veic_venda_tab': obj_veic_venda_tab.cod_veic_venda_tab, #19
                'ano_veic_tab': cod_ano_modelo #20
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
        lista_anos = []
        if tipo_pesq_frm == 'carrega_dados_veic_tab':
            cod_ano_tabela_frm = request.GET['cod_ano_tabela']
            obj_ano_tab = Ano_Modelo_Tab_Precos.objects.get(pk=cod_ano_tabela_frm)
            lista_anos = list(Ano_Modelo_Tab_Precos.objects
                              .filter(cod_modelo_tab_precos=obj_ano_tab.cod_modelo_tab_precos)
                              .values('cod_ano_modelo_tab', 'ano'))
            lista_modelos = list(Modelo_Tab_Precos.objects
                                 .filter(cod_marca_tab_precos=obj_ano_tab.cod_modelo_tab_precos.cod_marca_tab_precos)
                                 .values('cod_modelo_tab_precos', 'desc_modelo'))
            lista_marcas = list(Marca_Tab_Precos.objects
                                .filter(cod_tipo_veic_tab_precos=obj_ano_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_tipo_veic_tab_precos)
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
        elif tipo_pesq_frm == 'carrega_dados_anos':
            cod_modelo_tab_frm = request.GET['cod_modelo_tab']
            obj_modelo_tab = Modelo_Tab_Precos.objects.get(pk=cod_modelo_tab_frm)
            lista_anos = list(Ano_Modelo_Tab_Precos.objects
                                 .filter(cod_modelo_tab_precos=obj_modelo_tab)
                                 .values('cod_ano_modelo_tab', 'ano'))


        data = dict()
        data = {
            'lista_anos': lista_anos,
            'lista_marcas': lista_marcas,
            'lista_modelos': lista_modelos
        }
        return JsonResponse(data, safe=False)


class Form_Vincula_Veic_Tab_Precos_View(View):
    def post(self, request):
        cod_tab_frm = request.POST['cod_tab']
        cod_veic_frm = request.POST['cod_veic']
        cod_ano_modelo_tab_frm = request.POST['cod_ano_modelo_tab']
        #cod_modelo_frm = request.POST['cod_modelo']
        cod_veic_na_tab_frm = request.POST['cod_veic_na_tab']

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')
        competencia_date = datetime(data_hora_atual.year, data_hora_atual.month, 1)

        obj_tab_precos = Tabela_Preco_Veic.objects.get(pk=cod_tab_frm)
        obj_veic = Veiculo_Venda.objects.get(pk=cod_veic_frm)
        #obj_modelo = Modelo_Tab_Precos.objects.get(pk=cod_modelo_frm)
        obj_ano_modelo = Ano_Modelo_Tab_Precos.objects.get(pk=cod_ano_modelo_tab_frm)

        obj_veic_tab = (Veiculo_Venda_Tab_Precos.objects
                        .filter(cod_veic=obj_veic,
                                cod_ano_modelo_tab=obj_ano_modelo)
                                #cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos = obj_tab_precos)
                        .first())

        dic_pesq_preco_tab = self.acessa_site_tab_captura_val(
            obj_ano_modelo.cod_modelo_tab_precos.cod_marca_tab_precos.cod_tipo_veic_tab_precos.id_tipo_veic_tab,
            obj_ano_modelo.cod_modelo_tab_precos.cod_marca_tab_precos.cod_marca_tab_precos,
            obj_ano_modelo.cod_modelo_tab_precos.cod_modelo_tab_precos,
            obj_ano_modelo.ano)
        val_comp_veic = 0
        cod_veic_tab = cod_veic_na_tab_frm
        if dic_pesq_preco_tab[0] == 0:
            msg = 'Não foi possível retornar o preço do site. Contate o adm!'

        else:
            msg = 'Valor do veículo atualizado!'
            cod_veic_tab = dic_pesq_preco_tab[1]
            val_comp_veic = dic_pesq_preco_tab[2]

        if obj_veic_tab == None:
            obj_veic_tab = Veiculo_Venda_Tab_Precos(
                codigo_veic_tab= cod_veic_tab,
                competencia= competencia_date,
                val_comp= val_comp_veic,
                cod_veic= obj_veic,
                cod_ano_modelo_tab= obj_ano_modelo
            )
            obj_veic_tab.save()
        else:
            obj_veic_tab.codigo_veic_tab = cod_veic_na_tab_frm
            obj_veic_tab.competencia = competencia_date
            obj_veic_tab.val_comp = val_comp_veic
            obj_veic_tab.cod_ano_modelo_tab = obj_ano_modelo
            obj_veic_tab.save()


        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)



    def acessa_site_tab_captura_val(self, cod_tipo_veic, cod_marca, cod_modelo, ano_veic):
        status = 0
        val_comp = 0

        print('Aguarde ...')
        nav_options = webdriver.FirefoxOptions()
        #nav_options.add_argument('--headless')
        nav_options.add_argument('--no-sandbox')
        nav_options.add_argument('--disable-dev-shm-usage')
        navegador = webdriver.Firefox(options=nav_options)

        navegador.get(r'https://tabelafipecarros.com.br/')
        time.sleep(3)
        tipos_veiculos = navegador.find_elements(By.XPATH, value='//*[@id="tipoVeiculo"]/option')

        for tipo in tipos_veiculos:
            if tipo.get_attribute('value') == str(cod_tipo_veic):
                tipo.click()
                break
        time.sleep(3)
        marcas = navegador.find_elements(By.XPATH, value='//*[@id="marcaVeiculo"]/option')
        for marca in marcas:
            if marca.get_attribute('value') == str(cod_marca):
                marca.click()
                break
        time.sleep(5)
        modelos = navegador.find_elements(By.XPATH, value='//*[@id="modeloVeiculo"]/option')
        for modelo in modelos:
            if modelo.get_attribute('value') == str(cod_modelo):
                modelo.click()
                break
        time.sleep(3)
        anos = navegador.find_elements(By.XPATH, value='//*[@id="anoVeiculo"]/option')

        for ano in anos:
            if ano.text == str(ano_veic):
                ano.click()
                break
        time.sleep(5)
        navegador.find_element(By.XPATH, value='//*[@id="BuscaVeiculo"]').click()
        time.sleep(10)
        #anuncio = navegador.find_elements(By.TAG_NAME, value='ins')[0]
        #navegador.execute_script("""var element = arguments[0]; element.parentNode.removeChild(element);""", anuncio)
        #btn_fecha_anuncio = navegador.find_element(By.XPATH, value='//*[@id="dismiss-button"]')
        #navegador.execute_script("arguments[0].click();", btn_fecha_anuncio)

        ins_element = navegador.find_elements(By.TAG_NAME, value='ins')
        for el in ins_element:
            navegador.execute_script("var element = arguments[0]; element.removeAttribute('style');",
                                     el)
        time.sleep(10)
        navegador.find_element(By.XPATH, value='//*[@id="BuscaVeiculo"]').click()
        '''spans = navegador.find_elements(By.TAG_NAME, value='span')
        count = 0
        for span in spans:
            print(str(count) + ' - ' + span.txt)
            count += 1'''
        time.sleep(5)
        cod_fipe = (navegador.find_element(By.XPATH, value='//*[@id="CodFipe"] ').text).split(':')[1]
        val_veic = (navegador.find_element(By.CLASS_NAME, value='Valor_Veiculo ').text).split(':')[1]
        val_comp = (val_veic.split(',')[0]).replace('R$', '')
        navegador.quit()



        return status, cod_fipe, val_comp


