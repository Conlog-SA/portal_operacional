import os
import shutil
from datetime import date, datetime
import time
from itertools import count

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from pyhtml2pdf import converter

from apps.estrut_org_app.models import Filial
from apps.safety_checks_aplicados_app.models import Check_Aplicado, Colaborador, Item_Check_Aplicados, \
    Item_Fotos_Texto_Check_Aplicado
from apps.safety_layout_checklist_app.models import Item_Check, Libera_Filial_Check
from apps.usuario_app.models import Usuario
from proj_portal_operacional.settings import BASE_DIR

class Check_Aplicado_View(View):
    @csrf_exempt
    def get(self, request):
        tipo_check_aplicado = request.GET.get('tipo_check_aplicado', None)
        filial_check_aplicado = request.GET['cod_filial_check_aplicado']
        inicio_periodo_check_aplicado = request.GET['inicio_periodo_check_aplicado'] + ' 00:00'
        fim_periodo_check_aplicado = request.GET['fim_periodo_check_aplicado'] + ' 23:59'

        lista_checks_aplicados = Check_Aplicado.objects.filter(cod_layout_check__tipo_check=tipo_check_aplicado,
                                                               cod_filial=filial_check_aplicado,
                                                               data_registro__range=[inicio_periodo_check_aplicado, fim_periodo_check_aplicado])

        lista_checks_aplicados_dict = []
        for check in lista_checks_aplicados:
            count_respostas_ok = Item_Check_Aplicados.objects.filter(resp_item=0, cod_check_aplicado=check).count()
            count_respostas_nok = Item_Check_Aplicados.objects.filter(resp_item=1, cod_check_aplicado=check).count()
            obj_layout_check = check.cod_layout_check
            total_itens_layout = Item_Check.objects.filter(cod_check=obj_layout_check).count()
            count_respostas_nao_respondidos = total_itens_layout - (count_respostas_ok + count_respostas_nok)
            lista_checks_aplicados_dict.append({'cod_checks_aplicados': check.cod_check_aplicado, 'nome_colaborador_avaliado': check.cod_colaborador_avaliado.nome_colaborador,
                                     'nome_colaborador_aplicante': check.cod_colaborador_aplicante.nome_colaborador, 'data_registro': (check.data_registro).strftime("%d/%m/%Y %H:%M"), 'cod_layout_check': check.cod_layout_check.cod_check,
                                     'desc_check': check.cod_layout_check.desc_check, 'qtd_ok': str(count_respostas_ok), 'qtd_nok': str(count_respostas_nok), 'qtd_nao_respondidos': str(count_respostas_nao_respondidos),
                                                'qtd_total': str(total_itens_layout), 'pdf': '<i class="fa-solid fa-file-pdf pdf-clickable" style="font-size:20px;color:grey"></i>'})

        return JsonResponse(lista_checks_aplicados_dict, safe=False)

class Itens_Check_Aplicado(View):
    @csrf_exempt
    def get(self, request):
        cod_check_aplicado = request.GET.get('cod_check_aplicado', None)
        check_aplicado = Check_Aplicado.objects.get(pk=cod_check_aplicado)

        lista_itens_check_aplicado = Item_Check_Aplicados.objects.filter(cod_check_aplicado=cod_check_aplicado).order_by('cod_item_check__ordem_item').first()
        lista_fotos_texto_check_aplicado = Item_Fotos_Texto_Check_Aplicado.objects.filter(cod_check_aplicado=cod_check_aplicado).order_by('cod_item_check__ordem_item').first()

        lista_itens_check_aplicado_dict = []
        if lista_itens_check_aplicado != None:
            lista_itens_check_aplicado = Item_Check_Aplicados.objects.filter(
                cod_check_aplicado=cod_check_aplicado).order_by('cod_item_check__ordem_item')
            for item in lista_itens_check_aplicado:
                fotos_texto_item = Item_Fotos_Texto_Check_Aplicado.objects.filter(cod_item_check__ordem_item=item.cod_item_check.ordem_item).first()

                caminho_imagem = None
                comentario = None
                if fotos_texto_item != None:
                    caminho_imagem = fotos_texto_item.caminho_imagem
                    comentario = fotos_texto_item.comentario

                lista_itens_check_aplicado_dict.append({'resp_item': item.resp_item,
                                                        'cod_item_check': item.cod_item_check.cod_item_check,
                                                        'caminho_imagem' : caminho_imagem, 'comentario' : comentario,
                                                        'desc_item_check': item.cod_item_check.desc_check})
        else:
            print('Sem respostas!')

        if lista_fotos_texto_check_aplicado != None:
            lista_fotos_texto_check_aplicado = Item_Fotos_Texto_Check_Aplicado.objects.filter(
                cod_check_aplicado=cod_check_aplicado).order_by('cod_item_check__ordem_item')
            for item in lista_fotos_texto_check_aplicado:
                resposta_item_existente = Item_Check_Aplicados.objects.filter(
                    cod_item_check__ordem_item=item.cod_item_check.ordem_item).first()

                if resposta_item_existente == None:
                    lista_itens_check_aplicado_dict.append({'resp_item': '', 'cod_item_check': item.cod_item_check.cod_item_check,
                                                            'caminho_imagem' : item.caminho_imagem, 'comentario' : item.comentario,
                                                            'desc_item_check': item.cod_item_check.desc_check})

        print(lista_itens_check_aplicado_dict)
        html_check_aplicado = f'<div style="width:100%;margin-top:3rem;display:flex;justify-content:flex-start"><i class="fa-solid fa-arrow-left arrow-go-back"></i></div><p>{check_aplicado.cod_layout_check.desc_check}</p>'
        for item_aplicado in lista_itens_check_aplicado_dict:
            html_check_aplicado += f'<p style="margin-top:1rem">{item_aplicado["desc_item_check"]}</p>'
            flag_vazio = True
            if item_aplicado["resp_item"] == 0:
                html_check_aplicado += '<i class="fa-solid fa-check" style="color: #63E6BE;margin-bottom:5px"></i>'
                flag_vazio = False
            elif item_aplicado["resp_item"] == 1:
                html_check_aplicado += '<i class="fa-solid fa-x" style="color: #e01010;margin-bottom:5px"></i>'
                flag_vazio = False
            if item_aplicado["comentario"] != None:
                html_check_aplicado += f'<div style="width:100%;display:flex;justify-content:center"><textarea style="width:30rem;height:5rem;background-color:white !important" disabled>{item_aplicado["comentario"]}</textarea></div>'
                flag_vazio = False
            if item_aplicado["caminho_imagem"] != None:
                html_check_aplicado += f'<div style="width:100%;display:flex;justify-content:center"><img src="{item_aplicado["caminho_imagem"]}"></img></div>'
                flag_vazio = False
            if flag_vazio == False:
                html_check_aplicado += '</div>'
#
        #with open("html_check_aplicado.html", "w", encoding='utf-8') as file:
        #    file.write(html_check_aplicado)
        #path = os.path.abspath('html_check_aplicado.html')
#
        #converter.convert(f'file:///{path}', 'pdf_site_vagas.pdf')
        #path_pdf = os.path.abspath('pdf_site_vagas.pdf')

        #with open(path_pdf, 'r') as f:
        #    file_data = f.read()

            # sending response
        #response = HttpResponse(file_data, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="pdf_site_vagas.pdf"'

        #pdf = open(path_pdf, 'rb')
#
        #response = HttpResponse(pdf.read())
        #response['Content-Type'] = 'application/pdf'
        #response['Content-disposition'] = 'attachment'
        ##response = FileResponse(open('pdf_site_vagas.pdf', 'rb'), content_type='application/pdf')
        ##response['Content-Disposition'] = 'attachment; filename="pdf_site_vagas.pdf"'  # Optional: suggest filename
        #return response

        return HttpResponse(html_check_aplicado)

class Item_Check_Aplicado(View):
    @csrf_exempt
    def post(self, request):
        tipo_resposta = request.POST['tipo_input']
        cod_item_check = request.POST['cod_item_check']
        cod_check_aplicado = request.POST['cod_check_aplicado']
        #tipo_check_informado = request.POST['tipo_check']

        tipo_check = Item_Check.objects.get(pk=cod_item_check).cod_check.tipo_check
        #if tipo_check_informado == tipo_check:


        if tipo_resposta == 'button':
            resposta = request.POST['resposta']

            item_existente = Item_Check_Aplicados.objects.filter(
                    cod_item_check=cod_item_check,cod_check_aplicado=cod_check_aplicado).first()
            if item_existente == None:
                resposta_item = Item_Check_Aplicados(
                    cod_item_check=Item_Check.objects.filter(pk=cod_item_check).first(),
                    cod_check_aplicado=Check_Aplicado.objects.filter(pk=cod_check_aplicado).first(),
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
                cod_item_check=cod_item_check,cod_check_aplicado=cod_check_aplicado).first()

            if item_existente == None:
                resposta_item = Item_Fotos_Texto_Check_Aplicado(
                    comentario=resposta,
                    cod_item_check=Item_Check.objects.filter(pk=cod_item_check).first(),
                    cod_check_aplicado=Check_Aplicado.objects.filter(pk=cod_check_aplicado).first()
                )
                resposta_item.save()
            else:
                item_existente.comentario = resposta
                item_existente.save()
            msg = 'Resposta salva com sucesso!'

        if tipo_resposta == 'image':
            file_form = request.FILES['file']
            if tipo_check == 1:
                path_app = 'safety_gab_op_emp_app'
            elif tipo_check == 2:
                path_app = 'safety_relatos_app'

            msg = self.salva_imagem_anexo(file_form, file_form.name, cod_item_check, cod_check_aplicado, path_app)

        return HttpResponse(msg)

    @csrf_exempt
    def salva_imagem_anexo(self, file_form, desc_doc_form, cod_item_check, cod_check_aplicado, path_app):

        msg = ''
        item_existente = Item_Fotos_Texto_Check_Aplicado.objects.filter(
            cod_item_check=cod_item_check, cod_check_aplicado=cod_check_aplicado).first()
        if item_existente == None:
            item_existente = Item_Fotos_Texto_Check_Aplicado(
                cod_item_check=Item_Check.objects.filter(pk=cod_item_check).first(),
                cod_check_aplicado=Check_Aplicado.objects.filter(pk=cod_check_aplicado).first()
            )
            item_existente.save()
        elif item_existente.caminho_imagem != None:
            arquivo_anterior_a_deletar = str(item_existente.caminho_imagem).replace('/', '\\')
            os.remove(arquivo_anterior_a_deletar)

        fs = FileSystemStorage()
        if type(file_form) == str:
            caminho_arq_importado = os.path.join(BASE_DIR, f'media\\docs\\{path_app}\\{cod_check_aplicado}\\')
            if not (os.path.exists(caminho_arq_importado) and os.path.isdir(caminho_arq_importado)):
                os.makedirs(caminho_arq_importado)
            nome_arquivo, extensao = os.path.splitext(desc_doc_form)
            destination_path = os.path.join(caminho_arq_importado, f'{nome_arquivo}__{item_existente.cod_item_fotos_texto_itens_checks_aplicados}{extensao}')
            shutil.move(file_form, destination_path)
            item_existente.caminho_imagem = destination_path
        else:
            nome_arquivo = file_form.name
            caminho_arq_importado = os.path.join(BASE_DIR, f'media\\docs\\{path_app}\\{cod_check_aplicado}\\')
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
