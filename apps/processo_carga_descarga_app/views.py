import traceback
from django.shortcuts import render
from django.views import View
from apps.estrut_org_app.models import Filial
from apps.usuario_app.models import Usuario
from apps.conecta_app.views import ConexaoBancoConecta
from django.http import JsonResponse, Http404, FileResponse
from apps.processo_carga_descarga_app.models import Despesas_Carga_Descarga, Despesas_Carga_Descarga_Cliente
from datetime import datetime
from django.shortcuts import get_object_or_404

class Frm_Acesso_Despesa_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)
        lista_filiais = Filial.objects.filter(ativo=1, cod_empresa=12, cod_operacao=23)
        context = {
            'lista_filiais': lista_filiais,
            'obj_usuario_logado': obj_usuario_logado
        }
        return render(request, 'processo_carga_descarga_app/frm_consulta_despesas.html', context)

class Frm_Despesa_View(View):
    def get_object(self, pk):
        try:
            return Despesas_Carga_Descarga.objects.get(pk=pk)
        except Despesas_Carga_Descarga.DoesNotExist:
            raise Http404

    def get(self, request):
        cod_filial_form = request.GET['cod_filial']
        obj_filial = Filial.objects.get(pk=cod_filial_form)
        data_ini_form = request.GET['data_inicial']
        data_fim_form = request.GET['data_final']
        lista_clientes = list(
            Despesas_Carga_Descarga_Cliente.objects.filter(cod_filial=obj_filial).values('cod_cliente',
                                                                                         'cod_promax_cliente',
                                                                                         'nome_cliente'))
        '''Rota e AS'''
        list_mapas = ConexaoBancoConecta().retorna_dados_mapas(obj_filial.cod_promax, data_ini_form, data_fim_form)
        lista_dic_mapas_despesas = []
        for mapa in list_mapas:
            info_mapa = {
                'id': mapa['id'],
                'dt_mapa': mapa['data'].strftime('%d-%m-%Y'),
                'mapa': mapa['mapa'],
                'placa': mapa['placa'],
                'cod_filial_promax': mapa['cod_filial_promax'],
                'entrega': mapa['entrega']
            }
            lista_obj_despesas = (Despesas_Carga_Descarga.objects
                             .filter(mapa=mapa['mapa'], cod_filial__cod_promax=int(float(mapa['cod_filial_promax']))))

            if lista_obj_despesas:
                info_mapa['tem_despesa'] = 'S'
                lista_desp_mapa = []
                for obj_desp in lista_obj_despesas:
                    desp = {
                        'id_despesa' : obj_desp.id_despesa,
                        'tipo_despesa' : obj_desp.tipo_despesa,
                        'despesa' : obj_desp.despesa,
                        'subcategoria' : obj_desp.subcategoria,
                        'cod_cliente' : obj_desp.cod_cliente.cod_cliente,
                        'tipo_descarga' : obj_desp.tipo_descarga,
                        'quantidade' : obj_desp.quantidade,
                        'valor_unit' : obj_desp.valor_unit,
                        'comprovante' : obj_desp.comprovante.name,
                        'importado' : obj_desp.importado,
                        'data_lancamento' : obj_desp.data_lancamento,
                        'un_venda' : obj_desp.un_venda
                    }
                    lista_desp_mapa.append(desp)
                info_mapa['lista_desp_mapa'] = lista_desp_mapa
            else:
                info_mapa['tem_despesa'] = 'N'
                info_mapa['lista_desp_mapa'] = None

            lista_dic_mapas_despesas.append(info_mapa)

        '''Empurrada'''
        list_mapas_emp = list((Despesas_Carga_Descarga.objects
                          .filter(cod_filial__cod_promax=obj_filial.cod_promax, dt_mapa__range=[data_ini_form, data_fim_form],entrega='Empurrada')
                          .values('dt_mapa','mapa','entrega','placa','cod_filial__cod_promax','modal')
                          .distinct()).order_by('dt_mapa', 'placa'))
        lista_dic_mapas_despesas_empurrada = []
        for mapa_emp in list_mapas_emp:
            info_mapa_emp = {
                'dt_mapa': mapa_emp['dt_mapa'].strftime('%d-%m-%Y'),
                'mapa': mapa_emp['mapa'],
                'placa': mapa_emp['placa'],
                'cod_promax': mapa_emp['cod_filial__cod_promax'],
                'entrega': mapa_emp['entrega'],
                'modal': mapa_emp['modal']
            }
            lista_obj_despesas_emp = (Despesas_Carga_Descarga.objects
                             .filter(mapa=mapa_emp['mapa'], cod_filial__cod_promax=mapa_emp['cod_filial__cod_promax'], entrega='Empurrada'))
            if lista_obj_despesas_emp:
                info_mapa_emp['tem_despesa'] = 'S'
                lista_desp_mapa_emp = []
                for obj_desp_emp in lista_obj_despesas_emp:
                    desp_emp = {
                        'id_despesa' : obj_desp_emp.id_despesa,
                        'tipo_despesa' : obj_desp_emp.tipo_despesa,
                        'despesa' : obj_desp_emp.despesa,
                        'subcategoria' : obj_desp_emp.subcategoria,
                        'cod_cliente' : obj_desp_emp.cod_cliente.cod_cliente,
                        'tipo_descarga' : obj_desp_emp.tipo_descarga,
                        'quantidade' : obj_desp_emp.quantidade,
                        'valor_unit' : obj_desp_emp.valor_unit,
                        'comprovante' : obj_desp_emp.comprovante.name,
                        'importado' : obj_desp_emp.importado,
                        'data_lancamento' : obj_desp_emp.data_lancamento,
                        'un_venda': obj_desp_emp.un_venda,
                        'modal': obj_desp_emp.modal
                    }
                    lista_desp_mapa_emp.append(desp_emp)
                info_mapa_emp['lista_desp_mapa_emp'] = lista_desp_mapa_emp
            else:
                info_mapa_emp['tem_despesa'] = 'N'
                info_mapa_emp['lista_desp_mapa_emp'] = None

            lista_dic_mapas_despesas_empurrada.append(info_mapa_emp)

        '''ROTA/AS Lançadas'''
        list_mapas_lancados = list((Despesas_Carga_Descarga.objects
                               .filter(cod_filial__cod_promax=obj_filial.cod_promax,
                                       dt_mapa__range=[data_ini_form, data_fim_form], modal='LancRota/AS')
                               .values('dt_mapa', 'mapa', 'entrega', 'placa', 'cod_filial__cod_promax','modal')
                               .distinct()).order_by('dt_mapa', 'placa'))
        lista_dic_mapas_despesas_rota_lancadas = []
        for mapa_lanc in list_mapas_lancados:
            info_mapa_lanc = {
                'dt_mapa': mapa_lanc['dt_mapa'].strftime('%d-%m-%Y'),
                'mapa': mapa_lanc['mapa'],
                'placa': mapa_lanc['placa'],
                'cod_promax': mapa_lanc['cod_filial__cod_promax'],
                'entrega': mapa_lanc['entrega'],
                'modal': mapa_lanc['modal']
            }
            lista_obj_despesas_lanc = (Despesas_Carga_Descarga.objects
                                      .filter(mapa=mapa_lanc['mapa'],
                                              cod_filial__cod_promax=mapa_lanc['cod_filial__cod_promax'],
                                              modal='LancRota/AS'))
            if lista_obj_despesas_lanc:
                info_mapa_lanc['tem_despesa'] = 'S'
                lista_desp_mapa_lanc = []
                for obj_desp_lanc in lista_obj_despesas_lanc:
                    desp_lancada = {
                        'id_despesa': obj_desp_lanc.id_despesa,
                        'tipo_despesa': obj_desp_lanc.tipo_despesa,
                        'despesa': obj_desp_lanc.despesa,
                        'subcategoria': obj_desp_lanc.subcategoria,
                        'cod_cliente': obj_desp_lanc.cod_cliente.cod_cliente,
                        'tipo_descarga': obj_desp_lanc.tipo_descarga,
                        'quantidade': obj_desp_lanc.quantidade,
                        'valor_unit': obj_desp_lanc.valor_unit,
                        'comprovante': obj_desp_lanc.comprovante.name,
                        'importado': obj_desp_lanc.importado,
                        'data_lancamento': obj_desp_lanc.data_lancamento,
                        'un_venda': obj_desp_lanc.un_venda,
                        'modal': obj_desp_lanc.modal
                    }
                    lista_desp_mapa_lanc.append(desp_lancada)
                info_mapa_lanc['lista_desp_mapa_lanc'] = lista_desp_mapa_lanc
            else:
                info_mapa_lanc['tem_despesa'] = 'N'
                info_mapa_lanc['lista_desp_mapa_lanc'] = None

            lista_dic_mapas_despesas_rota_lancadas.append(info_mapa_lanc)
        data = dict()
        data = {
            'lista_dic_mapas_despesas': lista_dic_mapas_despesas,
            'lista_dic_mapas_despesas_empurrada': lista_dic_mapas_despesas_empurrada,
            'lista_dic_mapas_despesas_rota_lancadas': lista_dic_mapas_despesas_rota_lancadas,
            'lista_clientes': lista_clientes
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        modal_frm = request.POST['modal']
        tipo_despesa_frm = request.POST['tipo_despesa']
        entrega_frm = request.POST['entrega']
        despesa_frm = request.POST['despesa']
        subcategoria_frm = request.POST['subcategoria']
        data_frm = request.POST['dt_mapa']
        mapa_frm = request.POST['mapa']
        placa_frm = request.POST['placa']
        tipo_descarga_frm = request.POST['tipo_descarga']
        quantidade_frm = request.POST['quantidade']
        valor_unit_frm = request.POST['valor_unit']
        un_venda_frm = request.POST['un_venda']

        comprovante_frm = request.FILES['file']
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        data_hora_atual = datetime.now()
        data_atual = data_hora_atual.strftime('%Y-%m-%d')
        msg = ''
        id_despesa_frm = ''
        obj_filial = None
        obj_cliente = None
        if modal_frm == 'Mapas_2art':
            cod_promax_frm = request.POST['cod_promax']
            obj_cliente = Despesas_Carga_Descarga_Cliente.objects.get(pk=request.POST['cod_cliente'] )
            id_despesa_frm = str(request.POST['id_despesa']) + '-' + str(obj_cliente.cod_cliente)
            obj_filial = Filial.objects.get(cod_promax=cod_promax_frm)
            modal_frm = 'Mapas2art'

        else:
            if entrega_frm == 'Empurrada':
                modal_frm = 'LancEmpurrada'
            if modal_frm == 'LancRota/AS':
                modal_frm = 'LancRota/AS'
                if entrega_frm == 'Rota' :
                    subcategoria_frm = 0
                else:
                    subcategoria_frm = 1
            cod_filial_frm = request.POST['cod_filial']
            obj_filial = Filial.objects.get(pk=cod_filial_frm)
            obj_cliente = Despesas_Carga_Descarga_Cliente.objects.get(pk=request.POST['cod_cliente'])
            id_despesa_frm = mapa_frm + '-' + str(obj_filial.cod_promax) + '-' + str(obj_cliente.cod_cliente)


        lista_dic_despesas = []
        obj_cliente = Despesas_Carga_Descarga_Cliente.objects.get(pk=request.POST['cod_cliente'])
        bloquear = False
        if modal_frm == 'LancRota/AS':
            mapa_exist = ConexaoBancoConecta().existe_mapa(obj_filial.cod_promax, mapa_frm)
            if mapa_exist:
                msg = 'Despesa NÃO CADASTRADA, pois esse mapa já foi importado no Conecta, por favor localizar o mapa e criar a despesa na aba 2art!'
                bloquear = True

                data = dict()
                data = {
                    'msg': msg
                }
        if modal_frm == 'LancEmpurrada':
            msg = 'Aba em manutenção. Favor entrar em contato com o Admin!'
            bloquear = True

            data = dict()
            data = {
                'msg': msg
            }
        if not bloquear:
            try:
                obj_despesa = Despesas_Carga_Descarga.objects.get(pk=id_despesa_frm)

                if obj_despesa.importado == 0:
                    if comprovante_frm:
                        if obj_despesa.comprovante:
                            if obj_despesa.comprovante.name != comprovante_frm.name:
                                try:
                                    if os.path.isfile(obj_despesa.comprovante.path):
                                        os.remove(obj_despesa.comprovante.path)
                                except Exception:
                                    pass
                        obj_despesa.comprovante = comprovante_frm

                    obj_despesa.tipo_despesa = tipo_despesa_frm
                    obj_despesa.tipo_descarga = tipo_descarga_frm
                    obj_despesa.despesa = despesa_frm
                    obj_despesa.subcategoria = subcategoria_frm
                    obj_despesa.cod_cliente = obj_cliente
                    obj_despesa.quantidade = quantidade_frm
                    obj_despesa.valor_unit = valor_unit_frm
                    obj_despesa.cod_filial = obj_filial
                    obj_despesa.comprovante = comprovante_frm
                    obj_despesa.un_venda = un_venda_frm
                    obj_despesa.modal = modal_frm
                    obj_despesa.save()
                    msg = 'Despesa atualizados com sucesso!'
                else:
                    msg = 'Despesa já foi importada! Alteração não foi realizada!'

            except Despesas_Carga_Descarga.DoesNotExist:

                obj_despesa = Despesas_Carga_Descarga(
                    id_despesa=id_despesa_frm,
                    tipo_despesa=tipo_despesa_frm,
                    entrega=entrega_frm,
                    despesa=despesa_frm,
                    subcategoria=subcategoria_frm,
                    dt_mapa=datetime.strptime(data_frm, '%d-%m-%Y').date().strftime('%Y-%m-%d'),
                    mapa=mapa_frm,
                    placa=placa_frm,
                    cod_cliente=obj_cliente,
                    tipo_descarga=tipo_descarga_frm,
                    quantidade=quantidade_frm,
                    valor_unit=valor_unit_frm,
                    cod_filial=obj_filial,
                    cod_usu=obj_usuario_sessao,
                    data_lancamento=data_atual,
                    comprovante = comprovante_frm,
                    importado = 0,
                    un_venda=un_venda_frm,
                    modal=modal_frm
                )
                obj_despesa.save()
                msg = 'Despesa cadastrada com sucesso!'

            except Exception as e:
                traceback.print_exc()
                msg = str(e) + '. Por favor, contate o desenvolvimento.'

            # Retorna todas as despesas da viagem.
            num_viagem = id_despesa_frm.split('-')[0]
            lista_obj_despesas = (Despesas_Carga_Descarga
                                  .objects
                                  .filter(mapa=num_viagem, cod_filial=obj_filial))

            if lista_obj_despesas:
                for obj_desp in lista_obj_despesas:
                    desp = {
                        'id_despesa': obj_desp.id_despesa,
                        'tipo_despesa': obj_desp.tipo_despesa,
                        'despesa': obj_desp.despesa,
                        'subcategoria': obj_desp.subcategoria,
                        'cod_cliente': obj_desp.cod_cliente.cod_cliente,
                        'tipo_descarga': obj_desp.tipo_descarga,
                        'quantidade': obj_desp.quantidade,
                        'valor_unit': obj_desp.valor_unit,
                        'comprovante': obj_desp.comprovante.name,
                        'importado': obj_desp.importado,
                        'un_venda': obj_desp.un_venda,
                        'data_lancamento': obj_desp.data_lancamento
                    }
                    lista_dic_despesas.append(desp)

            data = dict()
            data = {
                'msg': msg,
                'lista_dic_despesas': lista_dic_despesas
            }

        return JsonResponse(data, safe=False)

    def delete(self, request, pk):
        item = self.get_object(pk)
        num_despesa = item.id_despesa
        num_mapa = item.mapa
        num_filial = item.cod_filial
        item.delete()

        # Retorna todas as despesas
        lista_obj_despesas = (Despesas_Carga_Descarga
                              .objects
                              .filter(mapa=num_mapa, cod_filial=num_filial))
        lista_dic_despesas = []
        if lista_obj_despesas:
            for obj_desp in lista_obj_despesas:
                desp = {
                    'id_despesa': obj_desp.id_despesa,
                    'tipo_despesa': obj_desp.tipo_despesa,
                    'despesa': obj_desp.despesa,
                    'subcategoria': obj_desp.subcategoria,
                    'cod_cliente': obj_desp.cod_cliente.cod_cliente,
                    'tipo_descarga': obj_desp.tipo_descarga,
                    'quantidade': obj_desp.quantidade,
                    'valor_unit': obj_desp.valor_unit,
                    'comprovante': obj_desp.comprovante.name,
                    'importado': obj_desp.importado,
                    'data_lancamento': obj_desp.data_lancamento,
                    'un_venda': obj_desp.un_venda
                }
                lista_dic_despesas.append(desp)


        data = {
            'msg' : 'Despesa Excluida com Sucesso!',
            'lista_dic_despesas': lista_dic_despesas
        }
        return JsonResponse(data, safe=False)

class Frm_Cadastro_Cliente(View):
    def post(self, request):
        cod_filial_frm = request.POST['cod_filial']
        obj_filial = Filial.objects.get(pk=cod_filial_frm)
        cod_promax_cliente_frm = request.POST['cod_promax_cliente']
        nome_cliente_frm = request.POST['nome_cliente'].upper()
        cod_cliente_frm= str(obj_filial.cod_promax) + str(cod_promax_cliente_frm)

        msg = ''
        if Despesas_Carga_Descarga_Cliente.objects.filter(pk=cod_cliente_frm).exists():
            msg = 'Já existe um cliente cadastrado com esse código! Por favor, entre em contato com o Adm para verificar'
            obj_cliente = None
        else:
            obj_cliente = Despesas_Carga_Descarga_Cliente(
                cod_cliente= cod_cliente_frm,
                cod_promax_cliente=cod_promax_cliente_frm,
                nome_cliente=nome_cliente_frm,
                cod_filial=obj_filial
            )
            obj_cliente.save()
            msg = 'Cliente cadastrado!'
        data = dict()
        data = {
            'msg': msg
        }
        return JsonResponse(data, safe=False)


