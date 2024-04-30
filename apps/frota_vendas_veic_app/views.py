import decimal
import locale
from datetime import datetime

from django.db.models import Avg, Count
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
        lista_veic_vendidos = []
        lista_modelos_tab_informados = []
        lista_veic_vendas_benner = ConexaoBancoBenner().retorna_veiculos_proj_vendas(mostra_veic_vendidos_frm)



        for veic_benner in lista_veic_vendas_benner:
            obj_veic = Veiculo_Venda.objects.filter(handle_veic=veic_benner['handle_veic']).first()

            status_venda_veic = 'N'
            if (veic_benner['num_nf_veic'] != None) or (veic_benner['data_venda_veic'] != None) or veic_benner[
                'val_venda_veic']:
                status_venda_veic = 'S'

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
                    val_compra = veic_benner['val_compra_veic'],
                    nome_cliente = veic_benner['nome_comprador'],
                    status_venda = status_venda_veic
                )
                obj_veic.save()
            else:
                obj_veic.status_ativo_benner = veic_benner['status_ativo_veic']
                obj_veic.num_nf_venda = veic_benner['num_nf_veic']
                obj_veic.data_venda = veic_benner['data_venda_veic']
                obj_veic.val_venda = veic_benner['val_venda_veic']
                obj_veic.val_compra = veic_benner['val_compra_veic']
                obj_veic.nome_cliente = veic_benner['nome_comprador']
                obj_veic.status_venda = status_venda_veic
                obj_veic.save()

            cod_marca = None
            desc_marca_tab = ''
            cod_modelo = None
            desc_modelo_tab = ''
            cod_tipo_veic_tab = None
            cod_ano_modelo = None
            ano_tab = ''
            obj_veic_venda_tab = (Veiculo_Venda_Tab_Precos.objects
                                  .filter(cod_veic=obj_veic,
                                          cod_tab_precos=obj_tab).first())
                                          #cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab.cod_tab_precos).first())
            if obj_veic_venda_tab == None:
                obj_veic_venda_tab = Veiculo_Venda_Tab_Precos(
                    codigo_veic_tab = None,
                    competencia = None,
                    val_comp = 0.00,
                    cod_veic = obj_veic,
                    cod_tab_precos = obj_tab,
                    cod_ano_modelo_tab = None
                )
                obj_veic_venda_tab.save()
            else:
                if obj_veic_venda_tab.cod_ano_modelo_tab != None:
                    cod_ano_modelo = obj_veic_venda_tab.cod_ano_modelo_tab.cod_ano_modelo_tab
                    ano_tab = obj_veic_venda_tab.cod_ano_modelo_tab.ano
                    cod_marca = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_marca_tab_precos
                    desc_marca_tab = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_marca_tab_precos.desc_marca
                    cod_modelo = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_modelo_tab_precos
                    desc_modelo_tab = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.desc_modelo
                    cod_tipo_veic_tab = obj_veic_venda_tab.cod_ano_modelo_tab.cod_modelo_tab_precos.cod_marca_tab_precos.cod_tipo_veic_tab_precos.cod_tipo_veic_tab_precos


            locale.setlocale(locale.LC_MONETARY, 'pt-BR')
            val_venda = 0.00
            if obj_veic.val_venda != None:
                val_venda = locale.currency(round(obj_veic.val_venda, 2), grouping=True, symbol=None)

            val_fipe = 0.00
            if obj_veic_venda_tab.val_comp != None:
                val_fipe = locale.currency(round(obj_veic_venda_tab.val_comp, 2), grouping=True, symbol=None)

            tipo_regra = ''
            if obj_veic.tipo_veic == 'CAVALO MECANICO':
                tipo_regra = 'CAVALO MECANICO'
            elif 'AMBEV' in obj_veic.nome_filial:
                tipo_regra = 'AMBEV'
            else:
                tipo_regra = 'OUTROS'

            status_venda = ''
            dados_sugestao = self.calcula_sugestao_perc_val_veic(tipo_regra, obj_veic_venda_tab.val_comp)
            perc_sug_venda = 0
            if dados_sugestao[0] != None:
                perc_sug_venda = dados_sugestao[0] * 100
            val_sug_venda = 0
            if dados_sugestao[1] != None:
                val_sug_venda = locale.currency(round(dados_sugestao[1], 2), grouping=True, symbol=None)

            perc_tab_x_venda = 0
            if obj_veic.val_venda != None and obj_veic_venda_tab.val_comp != None:
                if obj_veic.val_venda > 0 and obj_veic_venda_tab.val_comp > 0:
                    perc_tab_x_venda = ((obj_veic.val_venda - obj_veic_venda_tab.val_comp) / obj_veic_venda_tab.val_comp) * 100

                    if perc_tab_x_venda >= perc_sug_venda:
                        status_venda = 'OK'
                    else:
                        status_venda = 'NOK'

                    perc_tab_x_venda = locale.currency(round(perc_tab_x_venda, 2), grouping=True, symbol=None)

            data_venda = ''
            idade_veic = None
            if obj_veic.data_venda != None:
                data_venda = datetime.strptime(obj_veic.data_venda, '%Y-%m-%d').strftime('%d-%m-%Y')
                idade_veic = data_hora_atual.year - datetime.strptime(obj_veic.data_venda, '%Y-%m-%d').year
            else:
                idade_veic = data_hora_atual.year - obj_veic.ano

            competencia = ''
            if obj_veic_venda_tab.competencia != None:
                competencia = datetime.strftime(obj_veic_venda_tab.competencia, '%m-%Y')



            val_compra_veic = 0
            if veic_benner['val_compra_veic'] != None:
                val_compra_veic = locale.currency(round(veic_benner['val_compra_veic'], 2), grouping=True, symbol=None)




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
                'ano_veic_tab': cod_ano_modelo, #20,
                'ano_tab': ano_tab,
                'desc_marca_tab': desc_marca_tab,
                'desc_modelo_tab': desc_modelo_tab,
                'val_compra': val_compra_veic,
                'idade_veic': idade_veic,
                'perc_tab_x_venda': perc_tab_x_venda,
                'perc_sug_venda': str(perc_sug_venda) + ' %',
                'val_sug_venda': val_sug_venda,
                'status_venda': status_venda,
                'status_venda_veic': status_venda_veic
            }

            if status_venda_veic == 'N':
                lista_veic_vendas.append(veic_vendas)
            else:
                lista_veic_vendidos.append(veic_vendas)

            dic_tipo_veic = list(Tipo_Veic_Tab_Precos.objects
                          .filter(cod_tab_precos=obj_tab)
                          .values('cod_tipo_veic_tab_precos', 'desc_tipo_veic'))

        lista_obj_modelos_tab_informados = list(Veiculo_Venda_Tab_Precos.objects
                                        .filter(cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab)
                                        .values('cod_veic__marca', 'cod_veic__modelo', 'cod_veic__ano',
                                                'cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__desc_marca',
                                                'cod_ano_modelo_tab__cod_modelo_tab_precos__desc_modelo',
                                                'cod_ano_modelo_tab__ano', 'codigo_veic_tab')
                                        .annotate(val_media_tab_precos=Avg('val_comp'),
                                                  val_media_venda=Avg('cod_veic__val_venda'),
                                                  val_media_compra=Avg('cod_veic__val_compra'),
                                                  qtd_veic=Count('cod_veic')))
        for modelo in lista_obj_modelos_tab_informados:
            perc_venda_x_tab_preco = 0
            val_media_venda = 0
            if modelo['val_media_venda'] != None:
                val_media_venda = locale.currency(round(modelo['val_media_venda'], 2), grouping=True, symbol=None)
                calc_perc_venda_x_tab_preco = (modelo['val_media_venda'] / decimal.Decimal(modelo['val_media_tab_precos'])) * 100
                if calc_perc_venda_x_tab_preco > 0:
                    perc_venda_x_tab_preco = locale.currency(round(calc_perc_venda_x_tab_preco, 2), grouping=True, symbol=None)

            val_medio_tab_precos = 0
            if modelo['val_media_tab_precos'] != None:
                val_medio_tab_precos = locale.currency(round(modelo['val_media_tab_precos'], 2), grouping=True, symbol=None)

            val_medio_compra_veic = 0
            if modelo['val_media_compra'] != None:
                val_medio_compra_veic = locale.currency(round(modelo['val_media_compra'], 2), grouping=True,
                                                       symbol=None)

            dic_modelo = {
                'marca_veic': modelo['cod_veic__marca'],
                'modelo_veic': modelo['cod_veic__modelo'],
                'ano_veic': modelo['cod_veic__ano'],
                'marca_tab': modelo['cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__desc_marca'],
                'modelo_tab': modelo['cod_ano_modelo_tab__cod_modelo_tab_precos__desc_modelo'],
                'ano_tab': modelo['cod_ano_modelo_tab__ano'],
                'cod_modelo_tabela': modelo['codigo_veic_tab'],
                'val_medio_compra_veic': val_medio_compra_veic,
                'val_medio_tab_precos': val_medio_tab_precos,
                'val_media_venda': val_media_venda,
                'perc_venda_x_tab_preco': perc_venda_x_tab_preco,
                'qtd_veic': modelo['qtd_veic']
            }
            lista_modelos_tab_informados.append(dic_modelo)

        data = dict()
        data = {
            'lista_veic_vendas': lista_veic_vendas,
            'lista_veic_vendidos': lista_veic_vendidos,
            'lista_modelos_tab_informados': lista_modelos_tab_informados,
            'dic_tipo_veic': dic_tipo_veic
        }
        return JsonResponse(data, safe=False)


    def calcula_sugestao_perc_val_veic(self, tipo_regra, val_tab_preco):
        '''Tipo regra de venda
        Cavalo mecãnico : 95% da tabela
        DISTRIBUIÇÂO URBANA/AMBEV : 65%
        DEMAIS 75%
        '''
        perc_regra_sug_venda = 0
        val_sug_venda = 0
        if tipo_regra == 'CAVALO MECANICO':
            perc_regra_sug_venda = 0.95
        elif tipo_regra == 'AMBEV':
            perc_regra_sug_venda = 0.65
        else:
            perc_regra_sug_venda = 0.75

        val_sug_venda = val_tab_preco * perc_regra_sug_venda
        return perc_regra_sug_venda, val_sug_venda




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

        locale.setlocale(locale.LC_MONETARY, 'pt-BR')



        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')
        competencia_date = datetime(data_hora_atual.year, data_hora_atual.month, 1)

        obj_tab_precos = Tabela_Preco_Veic.objects.get(pk=cod_tab_frm)
        obj_veic = Veiculo_Venda.objects.get(pk=cod_veic_frm)
        #obj_modelo = Modelo_Tab_Precos.objects.get(pk=cod_modelo_frm)
        obj_ano_modelo = Ano_Modelo_Tab_Precos.objects.get(pk=cod_ano_modelo_tab_frm)

        obj_veic_tab = (Veiculo_Venda_Tab_Precos.objects
                        .filter(cod_veic=obj_veic,
                                cod_tab_precos=obj_tab_precos)
                                #cod_ano_modelo_tab=obj_ano_modelo)
                                #cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos = obj_tab_precos)
                        .first())

        val_comp_veic = 0
        cod_veic_tab = cod_veic_na_tab_frm

        '''dic_pesq_preco_tab = None
        dic_pesq_preco_tab = Veiculo_Venda_Tab_Precos.objects.filter(cod_ano_modelo_tab=obj_ano_modelo).first()
        if dic_pesq_preco_tab != None:
            cod_veic_tab = dic_pesq_preco_tab.codigo_veic_tab
            val_comp_veic = dic_pesq_preco_tab.val_comp
            msg = 'Valor do veículo atualizado!'
        else:'''
        dic_pesq_preco_tab = self.acessa_site_tab_captura_val_atual(
            obj_ano_modelo.cod_modelo_tab_precos.cod_marca_tab_precos.cod_tipo_veic_tab_precos.id_tipo_veic_tab,
            obj_ano_modelo.cod_modelo_tab_precos.cod_marca_tab_precos.cod_marca_tab_precos,
            obj_ano_modelo.cod_modelo_tab_precos.cod_modelo_tab_precos,
            obj_ano_modelo.ano)
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
                cod_ano_modelo_tab= obj_ano_modelo,
                cod_tab_precos=obj_tab_precos
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
            'msg': msg,
            'val_comp_veic': locale.currency(round(float(val_comp_veic), 2), grouping=True, symbol=None),
            'cod_veic_tab': cod_veic_tab
        }
        return JsonResponse(data, safe=False)

    def acessa_site_tab_captura_val_atual(self, cod_tipo_veic, cod_marca, cod_modelo, ano_veic):
        status = None
        val_comp = None
        msg_erro = ''

        nav_options = webdriver.FirefoxOptions()
        nav_options.add_argument('--headless')
        nav_options.add_argument('--no-sandbox')
        nav_options.add_argument('--disable-dev-shm-usage')
        navegador = webdriver.Firefox(options=nav_options)

        navegador.get(r'https://tabelafipecarros.com.br/')
        time.sleep(2)
        tipos_veiculos = navegador.find_elements(By.XPATH, value='//*[@id="tipoVeiculo"]/option')

        for tipo in tipos_veiculos:
            if tipo.get_attribute('value') == str(cod_tipo_veic):
                tipo.click()
                break
        time.sleep(2)
        marcas = navegador.find_elements(By.XPATH, value='//*[@id="marcaVeiculo"]/option')
        for marca in marcas:
            if marca.get_attribute('value') == str(cod_marca):
                marca.click()
                break
        time.sleep(2)
        modelos = navegador.find_elements(By.XPATH, value='//*[@id="modeloVeiculo"]/option')
        for modelo in modelos:
            if modelo.get_attribute('value') == str(cod_modelo):
                modelo.click()
                break
        time.sleep(2)
        anos = navegador.find_elements(By.XPATH, value='//*[@id="anoVeiculo"]/option')

        for ano in anos:
            if ano.text == str(ano_veic):
                ano.click()
                break
        time.sleep(2)
        navegador.find_element(By.XPATH, value='//*[@id="BuscaVeiculo"]').click()
        time.sleep(3)
        #anuncio = navegador.find_elements(By.TAG_NAME, value='ins')[0]
        #navegador.execute_script("""var element = arguments[0]; element.parentNode.removeChild(element);""", anuncio)
        #btn_fecha_anuncio = navegador.find_element(By.XPATH, value='//*[@id="dismiss-button"]')
        #navegador.execute_script("arguments[0].click();", btn_fecha_anuncio)

        ins_element = navegador.find_elements(By.TAG_NAME, value='ins')
        for el in ins_element:
            navegador.execute_script("var element = arguments[0]; element.removeAttribute('style');",
                                     el)
        time.sleep(3)
        navegador.find_element(By.XPATH, value='//*[@id="BuscaVeiculo"]').click()
        '''spans = navegador.find_elements(By.TAG_NAME, value='span')
        count = 0
        for span in spans:
            print(str(count) + ' - ' + span.txt)
            count += 1'''
        time.sleep(2)
        cod_fipe = (navegador.find_element(By.XPATH, value='//*[@id="CodFipe"]').text).split(':')[1]
        val_veic = (navegador.find_element(By.CLASS_NAME, value='Valor_Veiculo').text).split(':')[1]
        try:
            val_comp = int((val_veic.split(',')[0]).replace('R$', '').replace('.','').strip())
            status = 1
        except Exception as e:
            val_comp = 0
            status = 0
            msg_erro = e

        navegador.quit()

        return status, cod_fipe, val_comp, msg_erro

    def pesquisa_val_tab_comp(self, competencia, cod_modelo_tab_precos, ano_veic):
        valor_veic_comp = 0

        '''A competência tem q ser no formato 2024/04'''
        mes_int = int(competencia.split('-')[1])
        ano = competencia.split('-')[0]
        param_comp = ''
        if mes_int == 1:
            param_comp = 'janeiro/'+ano
        elif mes_int == 2:
            param_comp = 'fevereiro/' + ano
        elif mes_int == 3:
            param_comp = 'março/' + ano
        elif mes_int == 4:
            param_comp = 'abril/' + ano
        elif mes_int == 5:
            param_comp = 'maio/' + ano
        elif mes_int == 6:
            param_comp = 'junho/' + ano
        elif mes_int == 7:
            param_comp = 'julho/' + ano
        elif mes_int == 8:
            param_comp = 'agosto/' + ano
        elif mes_int == 9:
            param_comp = 'setembro/' + ano
        elif mes_int == 10:
            param_comp = 'outubro/' + ano
        elif mes_int == 11:
            param_comp = 'novembro/' + ano
        elif mes_int == 12:
            param_comp = 'dezembro/' + ano




        nav_options = webdriver.FirefoxOptions()
        # nav_options.add_argument('--headless')
        nav_options.add_argument('--no-sandbox')
        nav_options.add_argument('--disable-dev-shm-usage')
        navegador = webdriver.Firefox(options=nav_options)

        navegador.get(r'https://veiculos.fipe.org.br/')
        time.sleep(2)

        li = navegador.find_elements(By.CLASS_NAME, value='ilustra')[1]
        li.click()
        links = li.find_elements(By.TAG_NAME, value='a')
        for link in links:
            if link.get_attribute('text') == 'Pesquisa por código Fipe':
                link.click()

        time.sleep(2)
        div_chosen = navegador.find_element(By.XPATH,
                                            value='//*[@id="selectTabelaReferenciacaminhaoCodigoFipe_chosen"]')
        a_single = div_chosen.find_element(By.CLASS_NAME, value='chosen-single')
        a_single.send_keys(param_comp)
        a_single.send_keys(Keys.ENTER)

        time.sleep(1)
        txt_cod_fipe = navegador.find_element(By.XPATH, value='//*[@id="selectCodigocaminhaoCodigoFipe"]')
        txt_cod_fipe.send_keys(cod_modelo_tab_precos)
        txt_cod_fipe.send_keys(Keys.ENTER)

        time.sleep(3)

        div_chosen = navegador.find_element(By.XPATH, value='//*[@id="selectCodigoAnocaminhaoCodigoFipe_chosen"]')
        a_single = div_chosen.find_element(By.CLASS_NAME, value='chosen-single')

        a_single.send_keys(ano_veic)
        a_single.send_keys(Keys.ENTER)

        time.sleep(2)

        navegador.find_element(By.XPATH, value='//*[@id="buttonPesquisarcaminhaoPorCodigoFipe"]').click()

        time.sleep(2)

        div_resultado = navegador.find_element(By.XPATH, value='//*[@id="resultadocaminhaoCodigoFipe"]')
        objs_td_valor = div_resultado.find_elements(By.TAG_NAME, value='td')[15]
        valor_veic_comp = str(objs_td_valor.text).strip().replace('R$', '').replace('.', '').replace(',', '.')
        navegador.quit()
        return valor_veic_comp


class Form_Atualiza_Veic_Vinculados_View(View):
    def post(self, request):
        cod_tab_preco_frm = request.POST['cod_tab_preco']
        check_atualiza_veic_vendidos_frm = request.POST['check_atualiza_veic_vendidos']


        obj_tab_preco = Tabela_Preco_Veic.objects.get(pk=cod_tab_preco_frm)
        lista_dados_tab_modelos_veic_pesq_tab = []

        lista_obj_modelos_veic_venda = list(Veiculo_Venda_Tab_Precos.objects
                                            .filter(cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab_preco,
                                                    cod_veic__status_venda='N', codigo_veic_tab__isnull=False)
                                            .values('cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_marca_tab_precos',
                                                    'cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__id_tipo_veic_tab',
                                                    'cod_ano_modelo_tab__cod_modelo_tab_precos__cod_modelo_tab_precos',
                                                    'cod_ano_modelo_tab__ano', 'codigo_veic_tab', 'cod_ano_modelo_tab').distinct())
        
        #return status, cod_fipe, val_comp, msg_erro
        for reg in lista_obj_modelos_veic_venda:
            dados_pesq_tab = (Form_Vincula_Veic_Tab_Precos_View()
                              .acessa_site_tab_captura_val_atual(reg['cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__id_tipo_veic_tab'],
                                                                 reg['cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_marca_tab_precos'],
                                                                 reg['cod_ano_modelo_tab__cod_modelo_tab_precos__cod_modelo_tab_precos'],
                                                                 reg['cod_ano_modelo_tab__ano']))
            dic_dados = {
                'cod_ano_modelo_tab': reg['cod_ano_modelo_tab__ano'],
                'status_venda': 'N',
                'val_tabela': dados_pesq_tab[2]
            }
            lista_dados_tab_modelos_veic_pesq_tab.append(dic_dados)

        for modelo in lista_dados_tab_modelos_veic_pesq_tab:
            lista_veic_atualizar = (Veiculo_Venda_Tab_Precos.objects
                                                .filter(cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab_preco,
                                                        cod_veic__status_venda='N', cod_ano_modelo_tab__cod_ano_modelo_tab=modelo['cod_ano_modelo_tab']))
            for veic in lista_veic_atualizar:
                veic.val_comp = modelo['val_comp']
                veic.save()

        if check_atualiza_veic_vendidos_frm == 'S':
            lista_dados_tab_modelos_veic_vencidos_pesq_tab = []
            lista_obj_modelos_veic_vendidos = list(Veiculo_Venda_Tab_Precos.objects
                                                   .filter(cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab_preco,
                                                           cod_veic__status_venda='S', codigo_veic_tab__isnull=False)
                                                   .values('cod_veic__data_venda', 'codigo_veic_tab', 'cod_ano_modelo_tab__ano', 'cod_ano_modelo_tab').distinct())

            for reg in lista_obj_modelos_veic_vendidos:
                competencia_pesq = datetime.strftime(reg['cod_veic__data_venda'], '%Y-%m')
                cod_tab_fipe = reg['codigo_veic_tab'].strip().replace('-','')
                val_tabela_veic = (Form_Vincula_Veic_Tab_Precos_View()
                                  .pesquisa_val_tab_comp(competencia_pesq, cod_tab_fipe,reg['cod_ano_modelo_tab__ano']))
                dic_dados = {
                    'cod_ano_modelo_tab': reg['cod_ano_modelo_tab'],
                    'status_venda': 'S',
                    'val_tabela': decimal.Decimal(val_tabela_veic),
                    'mes_ref': reg['cod_veic__data_venda'].month,
                    'ano_ref': reg['cod_veic__data_venda'].year
                }
                lista_dados_tab_modelos_veic_vencidos_pesq_tab.append(dic_dados)

                for modelo in lista_dados_tab_modelos_veic_vencidos_pesq_tab:
                    lista_veic_vendidos_atualizar = (Veiculo_Venda_Tab_Precos.objects
                                                           .filter(cod_ano_modelo_tab__cod_modelo_tab_precos__cod_marca_tab_precos__cod_tipo_veic_tab_precos__cod_tab_precos=obj_tab_preco,
                                                                   cod_veic__status_venda='S',
                                                                   cod_ano_modelo_tab__cod_ano_modelo_tab=modelo['cod_ano_modelo_tab'],
                                                                   cod_veic__data_venda__month=modelo['mes_ref'],
                                                                   cod_veic__data_venda__year=modelo['ano_ref']))
                    for veic in lista_veic_vendidos_atualizar:
                        veic.val_comp = modelo['val_comp']
                        veic.save()

        data = dict()
        data = {
            'msg': 'Preços atualizados'
        }
        return JsonResponse(data, safe=False)







