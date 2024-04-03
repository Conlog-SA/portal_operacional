import os
import shutil
import sys
from datetime import datetime, date

from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Now
from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Colaborador, Check_Aplicado, Item_Check_Aplicados, \
    Item_Fotos_Texto_Check_Aplicado
from apps.safety_gab_op_emp_app.models import Empilhadeira, Gabarito_Operacional_Emp
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Item_Check
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR


# Create your views here.
class Form_Gerar_Gab_Emp(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(cod_colaborador=cod_colaborador)
        nome_colaborador = colaborador.nome_colaborador

        #lista_modelos_emp = Modelo_Emp.objects.all()
        #lista_modelos_emp_dict = []
        #for modelo in lista_modelos_emp:
        #    lista_modelos_emp_dict.append({'cod_modelo_emp': modelo.cod_modelo_emp, 'desc_emp': modelo.desc_emp})
        filial_colaborador = Filial.objects.get(pk=colaborador.cod_filial)
        str_options_select_unidade = ''
        if colaborador.perfil_usu == 'G':
            print(filial_colaborador.cod_filial)
            lista_empilhadeiras = Empilhadeira.objects.all()
            lista_empilhadeiras = lista_empilhadeiras.exclude(cod_filial__desc_filial__contains="AMBEV")
            lista_filiais = lista_empilhadeiras.values('cod_filial__cod_filial', 'cod_filial__desc_filial').distinct()
            str_options_select_unidade = ''
            for filial in lista_filiais:
                str_options_select_unidade += f'<option value="{str(filial["cod_filial__cod_filial"])}">{str(filial["cod_filial__desc_filial"])}</option>'

            '''filiais = Filial.objects.filter(cod_empresa=filial_colaborador.cod_empresa)
            filiais_com_empilhadeiras = filiais.filter(pk__in=related_filial_pks)
            filiais_com_empilhadeiras = filiais_com_empilhadeiras.exclude(desc_filial__contains="AMBEV")
            for filial in filiais_com_empilhadeiras:
                str_options_select_unidade += f'<option value="{str(filial.cod_filial)}">{str(filial.desc_filial)}</option>'''
        elif colaborador.perfil_usu == 'U':
            str_options_select_unidade += f'<option value="{filial_colaborador.cod_filial}">{filial_colaborador.desc_filial}</option>'

        context = {
            'nome_operador': nome_colaborador,
            'cod_filial_operador': filial_colaborador.cod_filial,
       #     'lista_modelos_emp': lista_modelos_emp_dict,
            'options_select': str_options_select_unidade,
        }
        return render(request, 'safety_gab_op_emp_app/gab_op_emp_form_gerar_check.html', context)

    @csrf_exempt
    def post(self, request):
        tipo_colaborador = request.POST['tipo_operador']
        filial_colaborador = request.POST['unidade_operador']
        usuario_informado = request.POST['nome_operador']
        colaborador = None
        if tipo_colaborador == '1':
            colaborador = Colaborador.objects.get(pk=int(usuario_informado))

        elif tipo_colaborador == '2':
            documento_usuario_informado = request.POST['documento_operador']

            colaborador = Colaborador(
                nome_colaborador=usuario_informado,
                cpf=documento_usuario_informado,
                cod_filial=filial_colaborador,
            )
            colaborador.save()

        cod_empilhadeira = request.POST['cod_empilhadeira']

        cod_colaborador = request.session['cod_colaborador']
        colaborador_envio = Colaborador.objects.filter(pk=cod_colaborador).first()
        cod_filial_usuario_sessao = colaborador_envio.cod_filial

        data_atual = datetime.now()
        check_ativo = Libera_Filial_Check.objects.filter(cod_check__tipo_check=1, cod_filial=colaborador_envio.cod_filial,
                                                         cod_check__data_desativacao__gte=date(data_atual.year,
                                                                                               data_atual.month,
                                                                                               data_atual.day),
                                                         cod_check__data_inicio__lte=date(data_atual.year,
                                                                                          data_atual.month,
                                                                                          data_atual.day)).order_by(
            '-cod_check__data_desativacao').first()

        check_aplicado = Check_Aplicado(
            cod_filial=cod_filial_usuario_sessao,
            cod_colaborador_aplicante=colaborador_envio,
            cod_colaborador_avaliado=colaborador,
            data_registro=data_atual,
            cod_layout_check=check_ativo.cod_check
        )

        check_aplicado.save()

        lista_itens = Item_Check.objects.filter(cod_check__cod_check=check_ativo.cod_check.cod_check,
                                                data_desativacao__gte=date(data_atual.year, data_atual.month,
                                                                           data_atual.day),
                                                data_inicio__lte=date(data_atual.year, data_atual.month,
                                                                      data_atual.day)).order_by('ordem_item')
        lista_itens_dict = []
        for item in lista_itens:
            lista_itens_dict.append({'cod_item_check': item.cod_item_check, 'desc_check': item.desc_check,
                                     'tipo_resposta': item.tipo_resposta, 'campo_obs_img': item.campo_obs_img,
                                     'ordem_item': item.ordem_item, 'tipo_item': item.tipo_item})

        check_cabecalho = Gabarito_Operacional_Emp(
            tipo_operador=tipo_colaborador,
            cod_empilhadeira=Empilhadeira.objects.get(pk=cod_empilhadeira),
        )
        check_cabecalho.save()

        context = {
            'lista_itens' : lista_itens_dict,
            'cod_check_aplicado': check_aplicado.cod_checks_aplicados
        }
        return render(request, 'safety_gab_op_emp_app/gab_op_emp_form_check.html', context)

class Colaborador_Portal(View):
    @csrf_exempt
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        usuario = Usuario.objects.get(cod_usu=cod_usuario_sessao)
        data = {
            'cod_colaborador': usuario.cod_usu,
            'cod_filial': usuario.cod_filial.cod_filial,
            'nome_colaborador': usuario.nome_usu,
            'filial_colaborador': usuario.cod_filial.desc_filial
        }
        return JsonResponse(data)

class Empilhadeiras_Filial(View):
    @csrf_exempt
    def get(self, request):
        unidade = request.GET['cod_unidade']
        filial_selecionada = Filial.objects.get(pk=unidade)
        lista_empilhadeiras = Empilhadeira.objects.filter(cod_filial=filial_selecionada.cod_filial)
        dict_empilhadeiras = []
        for emp in lista_empilhadeiras:
            dict_empilhadeiras.append({'cod_emp': emp.cod_emp, 'placa': emp.placa})
        data = {
            'lista_empilhadeiras': dict_empilhadeiras
        }
        return JsonResponse(data)

class Item_Check_Aplicado(View):
    @csrf_exempt
    def post(self, request):
        tipo_resposta = request.POST['tipo_input']
        cod_item_check = request.POST['cod_item_check']
        cod_check_aplicado = request.POST['cod_check_aplicado']
        msg = ''

        if tipo_resposta == 'button':
            resposta = request.POST['resposta']

            item_existente = Item_Check_Aplicados.objects.filter(
                    cod_item_check=cod_item_check,cod_checks_aplicados=cod_check_aplicado).first()
            if item_existente == None:
                resposta_item = Item_Check_Aplicados(
                    cod_item_check=Item_Check.objects.filter(pk=cod_item_check).first(),
                    cod_checks_aplicados=Check_Aplicado.objects.filter(pk=cod_check_aplicado).first(),
                    resp_item=resposta
                )
                resposta_item.save()
            else:
                item_existente.resp_item = resposta
                item_existente.save()
            msg = 'Resposta salva com sucesso!'

        if tipo_resposta == 'text':
            resposta = request.POST['resposta']

            item_existente = Item_Fotos_Texto_Check_Aplicado.objects.filter(
                cod_item_check=cod_item_check,cod_checks_aplicados=cod_check_aplicado).first()

            if item_existente == None:
                resposta_item = Item_Fotos_Texto_Check_Aplicado(
                    comentario=resposta,
                    cod_item_check=Item_Check.objects.filter(pk=cod_item_check).first(),
                    cod_checks_aplicados=Check_Aplicado.objects.filter(pk=cod_check_aplicado).first()
                )
                resposta_item.save()
            else:
                item_existente.comentario = resposta
                item_existente.save()
            msg = 'Resposta salva com sucesso!'

        if tipo_resposta == 'image':
            file_form = request.FILES['file']

            msg = self.salva_imagem_anexo(file_form, file_form.name, cod_item_check, cod_check_aplicado)

        return HttpResponse(msg)

    @csrf_exempt
    def salva_imagem_anexo(self, file_form, desc_doc_form, cod_item_check, cod_check_aplicado):
        item_existente = Item_Fotos_Texto_Check_Aplicado.objects.filter(
            cod_item_check=cod_item_check, cod_checks_aplicados=cod_check_aplicado).first()
        if item_existente == None:
            item_existente = Item_Fotos_Texto_Check_Aplicado(
                cod_item_check=Item_Check.objects.filter(pk=cod_item_check).first(),
                cod_checks_aplicados=Check_Aplicado.objects.filter(pk=cod_check_aplicado).first()
            )
            item_existente.save()
        elif item_existente.caminho_imagem != None:
            arquivo_anterior_a_deletar = str(item_existente.caminho_imagem).replace('/', '\\')
            os.remove(arquivo_anterior_a_deletar)

        fs = FileSystemStorage()
        if type(file_form) == str:
            caminho_arq_importado = os.path.join(BASE_DIR, f'media\\docs\\safety_gab_op_emp_app\\{cod_check_aplicado}\\')
            if not (os.path.exists(caminho_arq_importado) and os.path.isdir(caminho_arq_importado)):
                os.makedirs(caminho_arq_importado)
            nome_arquivo, extensao = os.path.splitext(desc_doc_form)
            destination_path = os.path.join(caminho_arq_importado, f'{nome_arquivo}__{item_existente.cod_item_fotos_texto_itens_checks_aplicados}{extensao}')
            shutil.move(file_form, destination_path)
            item_existente.caminho_imagem = destination_path
        else:
            nome_arquivo = file_form.name
            caminho_arq_importado = os.path.join(BASE_DIR, f'media\\docs\\safety_gab_op_emp_app\\{cod_check_aplicado}\\')
            if not (os.path.exists(caminho_arq_importado) and os.path.isdir(caminho_arq_importado)):
                os.makedirs(caminho_arq_importado)

            full_filepath = os.path.join(caminho_arq_importado, f'{item_existente.cod_item_fotos_texto_itens_checks_aplicados}_{nome_arquivo}')

            with open(full_filepath, 'wb+') as destination:
                for chunk in file_form.chunks():
                    destination.write(chunk)

            item_existente.caminho_imagem = full_filepath

        item_existente.save()

        msg = 'Imagem enviada com sucesso.'

        return msg
        #msg = ''
        #obj_anexo_conta_pesq
        #if obj_anexo_conta_pesq != None:
        #    arquivo_anterior_a_deletar = str(obj_anexo_conta_pesq.caminho_anexo).replace('/', '\\')
        #    os.remove(arquivo_anterior_a_deletar)
