from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime, date, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import pandas as pd
import locale
import ast
from querystring_parser import parser

from apps.benner_app.views import ConexaoBancoBenner
from apps.usuario_app.models import Usuario
from apps.suprimentos_evolucao_precos_app.models import Compra_Auditada, Justificativa_Compra


class Form_Gera_Evolucao_Precos_View(View):
    def get(self, request):
        lista_filiais = ConexaoBancoBenner().retornaTabFiliaisBennerByEmpresa(12)
        lista_familias = ConexaoBancoBenner()\
            .retorna_familias(" WHERE handle not in (12,18,23,25,28,29,34,35,36,37,39,42,53,66,71,75,92)"
                              " AND nome not like '%SERVIÇO%' AND nome not like '%SERVICO%'")
        data_ini = datetime.strftime(date.today() - timedelta(90), '%Y-%m-%d')
        data_fim = datetime.strftime(date.today(), '%Y-%m-%d')
        context = {
            'data_ini': data_ini,
            'data_fim': data_fim,
            'lista_familias': lista_familias,
            'lista_filiais': lista_filiais,
            'desc_menu_principal': 'Evolução de preços',
            'id_menu_pai': 45
        }
        return render(request, 'suprimentos_evolucao_precos_app/form_gera_evolucao_precos.html',context)


    def post(self, request):
        handle_item_compra_frm = request.POST['handle_item_compra']
        justificativa_frm = request.POST['justificativa']

        id_usu_session = request.session['cod_usuario_logado']
        usu_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()
        msg = ''
        obj_justificativa = Justificativa_Compra.objects.filter(handle_itens_compra=handle_item_compra_frm).first()
        if obj_justificativa == None:
            obj_justificativa = Justificativa_Compra(
                justificativa = justificativa_frm,
                eh_ativa = 'S',
                handle_itens_compra = handle_item_compra_frm,
                cod_usu = usu_logado
            )
            obj_justificativa.save()
            msg = 'Compra justificada'
        else:
            data_hora_atual = datetime.now()
            data_atual_yyyy_mm_dd = data_hora_atual.strftime('%Y-%m-%d')

            obj_justificativa.justificativa = justificativa_frm
            obj_justificativa.data_cad = data_atual_yyyy_mm_dd
            obj_justificativa.cod_usu = usu_logado
            obj_justificativa.save()
            msg = 'Justificativa atualizada'

        data = dict()
        data = {
            'msg' : msg
        }
        return JsonResponse(data, safe=False)







class Comp_Filiais_Evolucao_Precos_View(View):
    def get(self, request):
        cod_empresa_form = request.GET['cod_empresa']
        lista_filiais_from_benner = list(ConexaoBancoBenner().retornaTabFiliaisBennerByEmpresa(cod_empresa_form))
        lista_filiais = []
        for fil in lista_filiais_from_benner:
            reg = {
                'handle': fil.HANDLE,
                'nome': fil.NOME
            }
            lista_filiais.append(reg)
        data = dict()
        data = {
            'lista_filiais': lista_filiais
        }
        return JsonResponse(data, safe=False)


class Form_Compras_Item_Filial_View(View):
    def get(self, request):
        handle_filial_form = request.GET['handle_filial']
        data_ini_form = request.GET['data_ini']
        data_fim_form = request.GET['data_fim']
        cod_ref_item_form = request.GET['cod_ref_item']

        compras_item = []
        compras_benner = ConexaoBancoBenner()\
            .retorna_compras_by_item_filial(handle_filial_form, cod_ref_item_form, data_ini_form, data_fim_form)
        for reg in compras_benner:
            num_req= ''
            dat_req = ''
            tip_compra_req = ''
            if reg.handle_req_pai != None:
                num_req = reg.numero_req
                dat_req = datetime.strftime(reg.data_req, '%d-%m-%Y')
                tip_compra_req = reg.desc_tipo_compra_req

            justificativa_item_compra_registrada = 'Não justificado'
            obj_justificativa = Justificativa_Compra.objects.filter(handle_itens_compra=reg.handle_itens_compra,
                                                                    eh_ativa='S').last()
            if obj_justificativa != None:
                justificativa_item_compra_registrada = obj_justificativa.justificativa

            compra = {
                'handle_filial': reg.handle_filial_compra,
                'cod_ref_prod': reg.cod_ref_prod,
                'nome_prod': reg.nome_produto,
                'desc_variacao': reg.desc_variacao,
                'desc_familia': reg.desc_familia,
                'val_unit': locale.currency(reg.val_unit, grouping=True, symbol=False),
                'un_medida': reg.nome_un_medida,
                'qtd_comprada': reg.qtd_item,
                'val_total': locale.currency(reg.val_tt_item, grouping=True, symbol=False),
                'numero_compra': reg.numero_compra,
                'data_compra': datetime.strftime(reg.data_compra, '%d-%m-%Y'),
                'comprador': reg.nome_usuario_incluiu_compra,
                'nome_fornecedor': reg.nome_fornecedor_compra,
                'doc_fornecedor': reg.doc_fornecedor_compra,
                'cidade_fornecedor': reg.nome_cidade_fornecedor,
                'uf_fornecedor': reg.uf_fornecedor,
                'numero_req': num_req,
                'data_req': dat_req,
                'status_req': reg.status_req,
                'tipo_compra_req': tip_compra_req,
                'handle_itens_compra': reg.handle_itens_compra,
                'handle_produto': reg.handle_produto,
                'justificativa_item_compra_registrada': justificativa_item_compra_registrada
            }
            compras_item.append(compra)
        data = dict()
        data = {
            'compras_item': compras_item
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        array_compras_editadas_form = parser.parse(request.POST.urlencode('array_compras_editadas'))

        id_usu_session = request.session['cod_usuario_logado']
        usu_logado = Usuario.objects.filter(cod_usu=id_usu_session).first()

        for key, value in array_compras_editadas_form['array_compras_editadas'].items():
            compra_aud = Compra_Auditada.objects.filter(handle_filial_compra = value['handle_filial'],
                handle_itens_compra = value['handle_itens_compra']).first()
            if compra_aud == None:
                compra_aud = Compra_Auditada(
                    handle_filial_compra = value['handle_filial'],
                    handle_itens_compra = value['handle_itens_compra'],
                    handle_produto = value['handle_produto'],
                    val_unit = value['val_unit'].replace('.','').replace(',','.'),
                    qtd_item = value['qtd_comprada'],
                    cod_usu = usu_logado
                ).save()
            else:
                compra_aud.val_unit = value['val_unit'].replace('.', '').replace(',', '.')
                compra_aud.qtd_item = value['qtd_comprada']
                compra_aud.save()

        data = dict()
        data = {
            'msg': 'Itens atualizados com sucesso!'
        }
        return JsonResponse(data, safe=False)


class Comp_Itens_Evolucao_Precos_View(View):
    def get(self, request):
        handle_familia_form = request.GET['handle_familia']
        handle_filial_form = request.GET['handle_filial']
        lista_itens_from_benner = list(ConexaoBancoBenner()
                                       .retorna_itens_by_familia_filial(handle_familia_form, handle_filial_form))
        lista_itens = []
        for item in lista_itens_from_benner:
            reg = {
                'handle': item.handle,
                'nome': item.nome,
                'cod_ref': item.cod_ref
            }
            lista_itens.append(reg)
        data = dict()
        data = {
            'lista_itens': lista_itens
        }
        return JsonResponse(data, safe=False)


class Dash_Evolucao_Precos_View(View):
    def get(self, request):
        '''A data inicial são os últimos 5 dias da data atual'''
        data_ini = datetime.strftime(date.today() - timedelta(90), '%Y-%m-%d')
        data_fim = datetime.strftime(date.today(), '%Y-%m-%d')

        lista_filiais = ConexaoBancoBenner().retornaTabFiliaisBennerByEmpresa(12)
        lista_familias = ConexaoBancoBenner()\
            .retorna_familias(" WHERE handle not in (12,18,23,25,28,29,34,35,36,37,39,42,53,66,71,75,92)"
                              " AND nome not like '%SERVIÇO%' AND nome not like '%SERVICO%'")
        context = {
            #'plot1': self.grafico_pizza_plotly(),
            'lista_familias': lista_familias,
            'lista_filiais': lista_filiais,
            'desc_menu_principal': 'Dashboard Evolução de preços',
            'data_ini': data_ini,
            'data_fim': data_fim,
            'id_menu_pai': 45
        }
        return render(request, 'suprimentos_evolucao_precos_app/dash_evolucao_precos.html',context)




class Gera_Dash_Evolucao_Precos_View(View):
    def grafico_barras(self, lista_labels, lista_val, titulo, width, height):

        trace = go.Bar(
            x=lista_labels,
            y=lista_val,
            text=lista_val,
            textposition='auto',
            opacity=0.5
        )
        layout = go.Layout({
            'title': titulo,
            'autosize': False,
            'width': width,
            'height': height,
            'xaxis': {
                'titlefont': {
                    'size': 8
                }
            },
            'yaxis': dict(showgrid=False, zeroline=False, showticklabels=True)
        })
        fig = go.Figure(data=trace, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def grafico_pizza_plotly(self, labels, valores, titulo):
        valores = valores
        labels = labels

        trace = go.Pie(
            labels=labels,
            values=valores
        )
        data = [trace]
        colors = []
        for l in labels:
            if l == 'Sem Ocorrência':
                colors.append('#ab63fa')
            elif l == 'Compra Maior':
                colors.append('#ef553b')
            elif l == 'Compra OK':
                colors.append('#00cc96')
            elif l == 'Compra Menor':
                colors.append('#636efa')

        layout = go.Layout({
            'title': titulo,
            'width': 670, #1150
            'height': 370
        })
        fig = go.Figure(data=data, layout=layout)
        fig.update_traces(marker=dict(colors=colors))
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div


    def grafico_barras_agrupado(self, lista_labels, lista_val_compra_maior, lista_val_compra_menor, lista_val_compra_ok,
                                titulo, width, height):

        trace1 = go.Bar(
            x=lista_labels,
            y=lista_val_compra_menor,
            name = 'Compra Menor',
            text=lista_val_compra_menor,
            textposition='auto',
            opacity=0.5
        )
        trace2 = go.Bar(
            x=lista_labels,
            y=lista_val_compra_maior,
            name='Compra Maior',
            text=lista_val_compra_maior,
            textposition='auto',
            opacity=0.5
        )
        trace3 = go.Bar(
            x=lista_labels,
            y=lista_val_compra_ok,
            name='Compra OK',
            text=lista_val_compra_ok,
            textposition='auto',
            opacity=0.5
        )
        data = [trace1, trace2, trace3]
        layout = go.Layout({
            'barmode': 'group',
            'title': titulo,
            'autosize' : False,
            'width': width,
            'height': height,
            'xaxis':{
                'titlefont': {
                    'size': 8
                }
            },
            'yaxis' : dict(showgrid=False, zeroline=False, showticklabels=True)
        })
        '''colors = []        
        if l == 'Sem Ocorrência':
            colors.append('#ab63fa')
        elif l == 'Compra Maior':
            colors.append('#ef553b')
        elif l == 'Compra OK':
            colors.append('#00cc96')
        elif l == 'Compra Menor':
            colors.append('#636efa')'''

        fig = go.Figure(data=data, layout=layout)
        #fig.update_traces(marker=dict(colors=colors))
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div


    def get(self, request):
        handle_filial_form = request.GET['handle_filial']
        data_ini_form = request.GET['data_ini']
        data_fim_form = request.GET['data_fim']
        lista_df_evolucao_preco_filial = []
        #df_evolucao_preco = None
        for handle_fil in handle_filial_form.split(','):
            def_evolucao_preco_fil = ConexaoBancoBenner() \
                .retorna_df_ultimas_compras(handle_fil, data_ini_form, data_fim_form, '0', '0',
                                            '0')
            lista_df_evolucao_preco_filial.append(def_evolucao_preco_fil)

        df_evolucao_preco = pd.concat(lista_df_evolucao_preco_filial)

        df_evolucao_preco = df_evolucao_preco. \
            sort_values(['handle_filial_compra', 'cod_ref_prod', 'handle_variacao', 'seq_item'], ascending=False)
        # display(df_evolucao_preco)
        #df_evolucao_preco.to_excel('df_evolucao_preco_dash.xlsx')

        # Dataframe últimas três compras
        df_ultimas_tres_compras = df_evolucao_preco[df_evolucao_preco['seq_item'] < 4]
        df_ultimas_tres_compras.loc[df_ultimas_tres_compras['seq_item'] == 3, 'val_disp_atual_menos_anterior'] = 0
        '''df_ultimas_tres_compras['status_compra'] = 'Avaliar'
        df_ultimas_tres_compras.loc[(df_ultimas_tres_compras['seq_item'] == 1) &
                                    (df_ultimas_tres_compras['handle_item_compra_anterior'] == 0), 'status_compra'] = 'Sem Ocorrência'''
        #df_ultimas_tres_compras.to_excel('df_ultimas_tres_compras.xlsx')

        df_status_compra = df_evolucao_preco[df_evolucao_preco['seq_item'] == 1]\
            .drop(['nome_filial_compra', 'handle_produto', 'nome_produto', 'desc_variacao' , 'handle_familia',
                              'desc_familia' , 'val_unit', 'handle_variacao', 'handle_compra', 'numero_compra',
                              'data_compra', 'handle_usuario_incluiu_compra', 'nome_usuario_incluiu_compra',
                              'seq_item', 'handle_fornecedor_comra', 'nome_fornecedor_compra', 'doc_fornecedor_compra',
                              'val_disp_atual_menos_anterior', 'qtd_item', 'val_tt_item', 'nome_un_medida',
                              'val_disp_total'], axis=1)
        df_status_compra['status_compra'] = 'Avaliar'
        df_status_compra.loc[df_status_compra['handle_compra_anterior'] == 0, 'status_compra'] = 'Sem Ocorrência'

        #df_status_compra.to_excel('df_status_compra.xlsx')

        # Dataframe itens
        df_itens_aux = df_ultimas_tres_compras \
            .drop(['handle_produto', 'val_unit', 'handle_variacao', 'handle_compra',
                   'numero_compra', 'data_compra', 'seq_item'], axis=1) \
            .groupby(['handle_filial_compra', 'nome_filial_compra', 'cod_ref_prod', 'nome_produto', 'handle_familia',
                      'desc_familia', 'nome_un_medida'])[['val_disp_atual_menos_anterior']].sum().reset_index()
        #df_itens_aux.to_excel('df_itens_aux.xlsx')

        df_itens = \
            pd.merge(df_itens_aux, df_status_compra,
                     how='left',
                     on=['handle_filial_compra', 'cod_ref_prod']).reset_index()
        #df_itens.to_excel('df_itens.xlsx')

        df_itens.loc[df_itens['status_compra'] == 'Avaliar', 'status_compra'] = df_itens['val_disp_atual_menos_anterior'] \
            .apply(lambda x: 'Compra Maior' if x > 0 else ('Compra Menor' if x < 0 else 'Compra OK'))
        #df_itens.to_excel('df_itens.xlsx')
        #print(df_itens)

        df_ultimo_comprador = df_ultimas_tres_compras[['handle_filial_compra','cod_ref_prod',
                                                       'handle_usuario_incluiu_compra', 'nome_usuario_incluiu_compra']]\
            .loc[df_ultimas_tres_compras['seq_item'] == 1].reset_index()
        #df_ultimo_comprador.to_excel('df_ultimo_comprador.xlsx')



        df_resumo_status_compra = df_itens.drop(['cod_ref_prod','nome_produto','nome_un_medida'], axis=1)\
            .groupby(['handle_filial_compra', 'nome_filial_compra',
                                                    'handle_familia', 'desc_familia',
                                                    'status_compra']).count() \
            .rename(columns={'val_disp_atual_menos_anterior': 'qtd_compras'}).reset_index()
        #df_resumo_status_compra.to_excel('df_resumo_status_compra.xlsx')
        #df_status_cont = df_resumo_status_compra.groupby(['status_compra'])[['status_compra']].count()


        df_group_status_compra = df_resumo_status_compra.groupby(['status_compra'])[['qtd_compras']].sum().reset_index()
        df_group_status_compra['ordem_grafico'] = df_group_status_compra['status_compra']\
            .apply(lambda x: 0 if x == 'Sem Ocorrência' else ( 1 if x == 'Compra Maior' else ( 2 if x == 'Compra OK' else 3)))
        df_group_status_compra.sort_values(['ordem_grafico'], ascending=False)


        #Dados por familia
        df_compras_maior_familia = df_resumo_status_compra\
            .loc[(df_resumo_status_compra['status_compra'] == 'Compra Maior')|
                 (df_resumo_status_compra['status_compra'] == 'Compra Menor')|
                 (df_resumo_status_compra['status_compra'] == 'Compra OK')]\
            .groupby(['desc_familia','status_compra'])[['qtd_compras']].sum().reset_index()
        lista_ocorrencia_familia = df_compras_maior_familia['desc_familia'].unique().tolist()
        lista_familia = []
        lista_compra_maior = []
        lista_compra_menor = []
        lista_compra_ok = []
        for familia in lista_ocorrencia_familia:
            lista_familia.append(familia)
            df_qtd_compra_maior = df_compras_maior_familia\
                .loc[(df_compras_maior_familia['status_compra'] == 'Compra Maior')&
                     (df_compras_maior_familia['desc_familia'] == familia)]
            if df_qtd_compra_maior.empty:
                lista_compra_maior.append(0)
            else:
                lista_compra_maior.append(df_qtd_compra_maior['qtd_compras'].values[0])

            df_qtd_compra_menor = df_compras_maior_familia \
                .loc[(df_compras_maior_familia['status_compra'] == 'Compra Menor') &
                     (df_compras_maior_familia['desc_familia'] == familia)]
            if df_qtd_compra_menor.empty:
                lista_compra_menor.append(0)
            else:
                lista_compra_menor.append(df_qtd_compra_menor['qtd_compras'].values[0])

            df_qtd_compra_ok = df_compras_maior_familia \
                .loc[(df_compras_maior_familia['status_compra'] == 'Compra OK') &
                     (df_compras_maior_familia['desc_familia'] == familia)]
            if df_qtd_compra_ok.empty:
                lista_compra_ok.append(0)
            else:
                lista_compra_ok.append(df_qtd_compra_ok['qtd_compras'].values[0])

        #Grafico agrupa ultimo atendente
        df_ultimo_atendente = \
            pd.merge(df_itens, df_ultimo_comprador,
                     how='left',
                     on=['handle_filial_compra', 'cod_ref_prod']).reset_index()
        df_resumo_atendente = df_ultimo_atendente.drop(['index','handle_familia','cod_ref_prod','nome_produto',
                                                        'desc_familia','nome_un_medida','handle_filial_compra',
                                                        'nome_filial_compra','handle_usuario_incluiu_compra',
                                                        ], axis=1)\
            .groupby(['nome_usuario_incluiu_compra', 'status_compra']).count() \
            .rename(columns={'val_disp_atual_menos_anterior': 'qtd_compras'}).reset_index()
        df_resumo_atendente.to_excel('df_resumo_atendente.xlsx')
        lista_ocorrencia_atendente = df_resumo_atendente['nome_usuario_incluiu_compra'].unique().tolist()
        lista_atendente = []
        lista_atendente_compra_maior = []
        lista_atendente_compra_menor = []
        lista_atendente_compra_ok = []
        for atendente in lista_ocorrencia_atendente:
            lista_atendente.append(atendente.split(' ')[0])
            df_qtd_compra_maior = df_resumo_atendente \
                .loc[(df_resumo_atendente['status_compra'] == 'Compra Maior') &
                     (df_resumo_atendente['nome_usuario_incluiu_compra'] == atendente)]
            if df_qtd_compra_maior.empty:
                lista_atendente_compra_maior.append(0)
            else:
                lista_atendente_compra_maior.append(df_qtd_compra_maior['qtd_compras'].values[0])

            df_qtd_compra_menor = df_resumo_atendente \
                .loc[(df_resumo_atendente['status_compra'] == 'Compra Menor') &
                     (df_resumo_atendente['nome_usuario_incluiu_compra'] == atendente)]
            if df_qtd_compra_menor.empty:
                lista_atendente_compra_menor.append(0)
            else:
                lista_atendente_compra_menor.append(df_qtd_compra_menor['qtd_compras'].values[0])

            df_qtd_compra_ok = df_resumo_atendente \
                .loc[(df_resumo_atendente['status_compra'] == 'Compra OK') &
                     (df_resumo_atendente['nome_usuario_incluiu_compra'] == atendente)]
            if df_qtd_compra_ok.empty:
                lista_atendente_compra_ok.append(0)
            else:
                lista_atendente_compra_ok.append(df_qtd_compra_ok['qtd_compras'].values[0])


        #Dados por filial
        '''df_compras_filial = df_resumo_status_compra \
            .loc[(df_resumo_status_compra['status_compra'] == 'Compra Maior') |
                 (df_resumo_status_compra['status_compra'] == 'Compra Menor') |
                 (df_resumo_status_compra['status_compra'] == 'Compra OK')]\
            .groupby(['nome_filial_compra', 'status_compra'])[['qtd_compras']].sum().reset_index()'''
        df_compras_filial = df_resumo_status_compra \
            .groupby(['nome_filial_compra', 'status_compra'])[['qtd_compras']].sum().reset_index()
        lista_ocorrencia_filial = df_compras_filial['nome_filial_compra'].unique().tolist()
        lista_filial = []
        lista_compra_maior_filial = []
        lista_compra_menor_filial = []
        lista_compra_ok_filial = []
        for filial in lista_ocorrencia_filial:
            lista_filial.append(filial)
            df_qtd_compra_maior = df_compras_filial\
                .loc[(df_compras_filial['status_compra'] == 'Compra Maior') &
                     (df_compras_filial['nome_filial_compra'] == filial)]
            if df_qtd_compra_maior.empty:
                lista_compra_maior_filial.append(0)
            else:
                lista_compra_maior_filial.append(df_qtd_compra_maior['qtd_compras'].values[0])

            df_qtd_compra_menor = df_compras_filial \
                .loc[(df_compras_filial['status_compra'] == 'Compra Menor') &
                     (df_compras_filial['nome_filial_compra'] == filial)]
            if df_qtd_compra_menor.empty:
                lista_compra_menor_filial.append(0)
            else:
                lista_compra_menor_filial.append(df_qtd_compra_menor['qtd_compras'].values[0])

            df_qtd_compra_ok = df_compras_filial \
                .loc[(df_compras_filial['status_compra'] == 'Compra OK') &
                     (df_compras_filial['nome_filial_compra'] == filial)]
            if df_qtd_compra_ok.empty:
                lista_compra_ok_filial.append(0)
            else:
                lista_compra_ok_filial.append(df_qtd_compra_ok['qtd_compras'].values[0])

        '''Qtd Itens Avalidos por Filial'''
        df_qtd_itens_avaliados_filial = df_resumo_status_compra \
            .groupby(['nome_filial_compra'])[['qtd_compras']].sum().reset_index()\
            .sort_values(['qtd_compras'], ascending=False)

        #df_qtd_itens_avaliados_filial.to_excel('df_qtd_itens_avaliados_filial.xlsx')




        data = dict()
        data = {
            'grafico_pizza_resumo_status': self.grafico_pizza_plotly(df_group_status_compra['status_compra'].tolist(),
                                               df_group_status_compra['qtd_compras'].tolist(), "Gráfico de % por análise de compra"),
            'grafico_barra_agrupado': self.grafico_barras_agrupado(lista_familia, lista_compra_maior, lista_compra_menor, lista_compra_ok,
                                                                   "Gráfico de qtd. por análise de compra por familia", 1350, 550),
            'grafico_atendente_barra_agrupado': self.grafico_barras_agrupado(lista_atendente,
                                                                             lista_atendente_compra_maior,
                                                                             lista_atendente_compra_menor,
                                                                             lista_atendente_compra_ok,
                                                                             "Gráfico de qtd. por análise de compra por atendente", 670, 370),
            'grafico_barra_agrupado_filial': self.grafico_barras_agrupado(lista_filial, lista_compra_maior_filial,
                                                                   lista_compra_menor_filial, lista_compra_ok_filial,
                                                                   "Gráfico de qtd. por análise de compra por filial", 1350, 550),
            'grafico_barra_agrupado_itens_filial': self.grafico_barras(df_qtd_itens_avaliados_filial['nome_filial_compra'].tolist(),
                                                                          df_qtd_itens_avaliados_filial['qtd_compras'].tolist(),
                                                                          "Gráfico de qtd. itens avaliados por filial",
                                                                          1350, 550),
        }
        return JsonResponse(data, safe=False)


class Gera_Evolucao_Precos_View(View):

    def get(self, request):
        handle_filial_form = request.GET['handle_filial']
        data_ini_form = request.GET['data_ini']
        data_fim_form = request.GET['data_fim']
        handle_familia_form = request.GET['handle_familia']
        cod_ref_item_form = request.GET['cod_ref_item']
        numero_requisicao_form = request.GET['numero_requisicao']
        locale.setlocale(locale.LC_MONETARY, 'pt-BR')

        lista_evolucao_precos_tab = []
        df_evolucao_preco = ConexaoBancoBenner()\
            .retorna_df_ultimas_compras(handle_filial_form, data_ini_form, data_fim_form,
                                        handle_familia_form, cod_ref_item_form,numero_requisicao_form)

        df_evolucao_preco = df_evolucao_preco\
            .sort_values(['handle_filial_compra', 'cod_ref_prod', 'handle_variacao', 'seq_item'], ascending=False)
        #df_evolucao_preco.to_excel('df_evolucao_preco_rel.xlsx')


        '''Totaliza evolução dos itens'''
        '''Exclui colunas'''
        df_tt_evolucao_produtos = df_evolucao_preco \
            .drop(['handle_fornecedor_comra', 'seq_item', 'handle_usuario_incluiu_compra', 'numero_compra',
                   'data_compra', 'nome_usuario_incluiu_compra', 'nome_fornecedor_compra', 'doc_fornecedor_compra'],
                  axis=1)
        '''Set index'''
        df_tt_evolucao_produtos = df_tt_evolucao_produtos.set_index(['handle_filial_compra', 'cod_ref_prod'])


        '''Agrupa e calcula o valor da evolução dos itens'''
        df_tt_evolucao_produtos_base_sum = df_tt_evolucao_produtos\
            .groupby(['handle_filial_compra', 'nome_filial_compra', 'cod_ref_prod', 'nome_produto',
                      'handle_familia', 'desc_familia', 'nome_un_medida'])\
            [['val_disp_atual_menos_anterior','qtd_item','val_tt_item','val_disp_total','val_unit']].sum().reset_index()
        #df_tt_evolucao_produtos_base_sum.to_excel('df_tt_evolucao_produtos_base_sum.xlsx')


        df_tt_evolucao_produtos_base_count = df_tt_evolucao_produtos \
            .groupby(['handle_filial_compra', 'nome_filial_compra', 'cod_ref_prod'])[['handle_compra']].count().reset_index()




        df_tt_evolucao_produtos_base = pd.merge(
            df_tt_evolucao_produtos_base_sum, df_tt_evolucao_produtos_base_count,
            how='left',
            on=['handle_filial_compra', 'cod_ref_prod']).reset_index()
        #df_tt_evolucao_produtos_base.to_excel('df_tt_evolucao_produtos_base.xlsx')


        ''' Filtra ultima compra '''
        df_ultimas_compras = df_evolucao_preco[df_evolucao_preco['seq_item'] == 1] \
            .set_index(['handle_filial_compra', 'cod_ref_prod']) \
            .rename(columns={'numero_compra': 'num_ult', 'data_compra': 'data_ult', 'val_unit': 'val_ult',
                             'nome_usuario_incluiu_compra': 'nome_usu_ult',
                             'nome_fornecedor_compra': 'nome_fornec_ult',
                             'val_disp_atual_menos_anterior': 'val_disp_ult'})
        df_ultimas_compras['status_compra'] = 'Avaliar'
        df_ultimas_compras.loc[df_ultimas_compras[
                                 'handle_compra_anterior'] == 0, 'status_compra'] = 'Sem Ocorrência'

        ''' Exclui as colunas concatenadas'''
        df_ultimas_compras = df_ultimas_compras \
            .drop(['handle_variacao', 'handle_produto', 'nome_produto', 'handle_familia',
                   'handle_fornecedor_comra', 'seq_item','handle_usuario_incluiu_compra', 'doc_fornecedor_compra',
                   'handle_compra','qtd_item','val_tt_item','val_disp_total','handle_compra_anterior', 'desc_variacao',
                   'desc_familia'], axis=1)
        #df_ultimas_compras.to_excel('df_ultimas_compras.xlsx')


        df_base_evolucao_ultimas_compra = pd.merge(
            df_tt_evolucao_produtos_base, df_ultimas_compras,
            how='left',
            on=['handle_filial_compra', 'cod_ref_prod'])

        ''' Filtra penúltima compra '''
        df_penultimas_compras = df_evolucao_preco[df_evolucao_preco['seq_item'] == 2] \
            .set_index(['handle_filial_compra', 'cod_ref_prod']) \
            .rename(columns={'numero_compra': 'num_pen', 'data_compra': 'data_pen', 'val_unit': 'val_pen',
                             'nome_usuario_incluiu_compra': 'nome_usu_pen', 'nome_fornecedor_compra': 'nome_fornec_pen',
                             'val_disp_atual_menos_anterior': 'val_disp_pen'})

        ''' Exclui as colunas concatenadas'''
        df_penultimas_compras = df_penultimas_compras \
            .drop(['handle_variacao', 'handle_produto', 'nome_produto', 'desc_variacao', 'handle_familia',
                   'desc_familia', 'handle_fornecedor_comra', 'seq_item',
                   'handle_usuario_incluiu_compra', 'doc_fornecedor_compra', 'handle_compra','qtd_item',
                   'val_tt_item','nome_un_medida','val_disp_total', 'nome_filial_compra','handle_compra_anterior'], axis=1)
        #df_penultimas_compras.to_excel('df_penultimas_compras.xlsx')


        df_base_evolucao_ultimas_penultima_compra = pd.merge(
            df_base_evolucao_ultimas_compra, df_penultimas_compras,
            how='left',
            on=['handle_filial_compra', 'cod_ref_prod'])

        ''' Filtra antepenúltima compra '''
        df_antepenultimas_compras = df_evolucao_preco[df_evolucao_preco['seq_item'] == 3] \
            .set_index(['handle_filial_compra', 'cod_ref_prod']) \
            .rename(columns={'numero_compra': 'num_ant', 'data_compra': 'data_ant', 'val_unit': 'val_ant',
                             'nome_usuario_incluiu_compra': 'nome_usu_ant', 'nome_fornecedor_compra': 'nome_fornec_ant',
                             'val_disp_atual_menos_anterior': 'val_disp_ant'})
        df_antepenultimas_compras.loc[df_antepenultimas_compras['val_disp_ant'] != 0, 'val_disp_ant'] = 0

        ''' Exclui as colunas concatenadas'''
        df_antepenultimas_compras = df_antepenultimas_compras \
            .drop(['handle_variacao', 'handle_produto', 'nome_produto', 'desc_variacao', 'handle_familia',
                   'desc_familia', 'handle_fornecedor_comra', 'seq_item',
                   'handle_usuario_incluiu_compra', 'doc_fornecedor_compra', 'handle_compra','qtd_item',
                   'val_tt_item','nome_un_medida','val_disp_total','nome_filial_compra','handle_compra_anterior'], axis=1)
        #df_antepenultimas_compras.to_excel('df_antepenultimas_compras.xlsx')


        df_base_evolucao_ultimas_penultima_antepenultima_compra = \
            pd.merge(df_base_evolucao_ultimas_penultima_compra, df_antepenultimas_compras,
                     how='left',
                     on=['handle_filial_compra', 'cod_ref_prod']).reset_index()
        df_base_evolucao_ultimas_penultima_antepenultima_compra.fillna(value=0,inplace=True)
        #df_base_evolucao_ultimas_penultima_antepenultima_compra.to_excel('df_base_evolucao_ultimas_penultima_antepenultima_compra.xlsx')

        for index, row in df_base_evolucao_ultimas_penultima_antepenultima_compra.iterrows():
            perc_dispersao = 0
            dif_val_compra = df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_disp_ult'] +\
                             df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_disp_pen'] + \
                             df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_disp_ant']
            '''if df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ant'] > 0:
                dif_val_compra = \
                    (df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_pen']  -
                     df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ant']) + \
                    (df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ult']  -
                     df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_pen'] )
            elif df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_pen']  > 0:
                dif_val_compra = \
                    (df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ult']  -
                     df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_pen'] )'''

            perc_dispersao = dif_val_compra / \
                             df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ult']

            analise_reg = ''

            ''' if perc_dispersao > 0:
                analise_reg = 'Compra Maior'
            elif perc_dispersao < 0:
                analise_reg = 'Compra Menor'
            elif df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ant']  == 0 and \
                    df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_pen']  == 0:
                analise_reg = 'Sem ocorrência'
            else:
                analise_reg = 'Compra OK'''

            if df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'status_compra'] == 'Avaliar':
                if dif_val_compra > 0:
                    analise_reg = 'Compra Maior'
                elif dif_val_compra < 0:
                    analise_reg = 'Compra Menor'
                else:
                    analise_reg = 'Compra OK'
            else:
                analise_reg = 'Sem Ocorrência'



            info_ult_compra = ''
            val_ult_compra = ''
            info_pen_compra = ''
            val_pen_compra = ''
            info_ant_compra = ''
            val_ant_compra = ''
            if df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ant'] > 0:
                info_ant_compra = \
                    '<b>Nº.:</b> ' + str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'num_ant'])\
                    .replace('.0','')+\
                    ' <br/><b>Data:</b> ' + \
                    datetime.strftime(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                  .loc[index, 'data_ant'], '%d-%m-%Y')
                val_ant_compra = locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                 .loc[index, 'val_ant'],grouping=True,symbol=False)

            if df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_pen'] > 0:
                info_pen_compra = \
                    '<b>Nº.: </b>' + str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'num_pen'])\
                        .replace('.0','') +\
                    '<br/> <b>Data:</b> ' + datetime.strftime(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                         .loc[index, 'data_pen'], '%d-%m-%Y')
                val_pen_compra = locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                 .loc[index, 'val_pen'],grouping=True,symbol=False)

            if df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_ult'] > 0:
                info_ult_compra = \
                    '<b>Nº.:</b> ' + str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'num_ult'])\
                    .replace('.0','')+\
                    ' <br/><b>Data:</b> ' + datetime.strftime(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                  .loc[index, 'data_ult'], '%d-%m-%Y')
                val_ult_compra = locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                 .loc[index, 'val_ult'],grouping=True,symbol=False)


            val_disp_total_calc_sugestao_compra = df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_disp_atual_menos_anterior']
            if val_disp_total_calc_sugestao_compra > 0:
                val_disp_total_calc_sugestao_compra = val_disp_total_calc_sugestao_compra * (-1)
            val_pretencao_prox_compra =\
                (df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'val_unit'] + \
                val_disp_total_calc_sugestao_compra) / \
                df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'handle_compra']


            row = {
                'nome_filial': str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'nome_filial_compra']),
                'cod_ref_item': str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'cod_ref_prod']),
                'desc_item': df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'nome_produto'],
                'desc_variacao': '',#str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'desc_variacao']),
                'desc_familia': df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'desc_familia'],
                'val_antepenultima': val_ant_compra,
                'dados_antepenultima_compra': info_ant_compra,
                'val_penultima': val_pen_compra,
                'dados_penultima_compra': info_pen_compra,
                'val_ultima': val_ult_compra,
                'dados_ultima_compra': info_ult_compra,
                'dispersao': locale.currency(perc_dispersao * 100, grouping=True, symbol=None),
                'analise': analise_reg,
                'vaLdispersao': locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                .loc[index, 'val_ult'] * perc_dispersao,grouping=True,symbol=False),
                'un_medida': df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'nome_un_medida_x'],
                'qtd_total_item_periodo':locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                         .loc[index, 'qtd_item'],grouping=True,symbol=False),
                'val_total_item_periodo':locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                         .loc[index, 'val_tt_item'],grouping=True,symbol=False),
                'val_dispersao_unit_periodo': locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                              .loc[index, 'val_disp_atual_menos_anterior']
                                                              ,grouping=True,symbol=False),
                'total_dispersao_periodo':locale.currency(df_base_evolucao_ultimas_penultima_antepenultima_compra
                                                          .loc[index, 'val_disp_total'],grouping=True,symbol=False),
                #'handle_filial_form': handle_filial_form,
                'handle_filial_compra': str(df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'handle_filial_compra']),
                'data_ini_form': data_ini_form,
                'data_fim_form': data_fim_form,
                'val_pretencao_prox_compra': locale.currency(val_pretencao_prox_compra, grouping=True, symbol=False),
                'atendente_ult_compra': df_base_evolucao_ultimas_penultima_antepenultima_compra.loc[index, 'nome_usu_ult']

            }
            lista_evolucao_precos_tab.append(row)

            df_evolucao_precos_gerado = pd.DataFrame(lista_evolucao_precos_tab)
            # Agrupa por status de compra
            df_evolucao_precos_gerado_status = df_evolucao_precos_gerado \
                .groupby(['analise'])[['cod_ref_item']].count()
            #print(df_evolucao_precos_gerado_status)


        data = dict()
        data = {
            'lista_evolucao_precos_tab': lista_evolucao_precos_tab
        }
        return JsonResponse(data, safe=False)


