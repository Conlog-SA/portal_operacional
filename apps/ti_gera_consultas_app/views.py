import json
import pyodbc
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from apps.usuario_app.models import Usuario
from apps.ti_gera_consultas_app.models import Script, Parametro, Liberacao, Conexao
from datetime import datetime, timedelta, timezone
from django.http import HttpResponse
import io
import xlsxwriter
import json


class Frm_Criar_Consulta_View(View):
    def get(self, request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_usuarios = Usuario.objects.filter(status_usu='A')
        lista_consultas = list(Script.objects.all())
        lista_conexao = list(Conexao.objects.all())
        context = {
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_usuarios': lista_usuarios,
            'lista_consultas': lista_consultas,
            'lista_conexao': lista_conexao
        }
        return render(request, 'ti_gera_consultas_app/frm_criar_consulta.html', context)

    def post(self, request):
        cod_script_frm = request.POST['cod_script']
        desc_frm = request.POST['desc']
        script_frm = request.POST['script']
        obs_frm = request.POST['obs']
        cod_conexao_frm = request.POST['cod_conexao']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        data_hora_atual = datetime.now()
        data_atual_dd_mm_yyyy = data_hora_atual.strftime('%Y-%m-%d')

        obj_script = None
        obj_conexao = Conexao.objects.get(pk=cod_conexao_frm)
        msg = ''
        if cod_script_frm == '0':
            obj_script = Script(
                desc=desc_frm,
                script=script_frm,
                obs=obs_frm,
                cod_usu=obj_usuario_sessao,
                data_criacao=data_atual_dd_mm_yyyy,
                data_ultima_alteracao=data_atual_dd_mm_yyyy,
                cod_conexao=obj_conexao,
            )
            obj_script.save()
            msg = 'Consulta criada com sucesso! Agora adicione os parâmetros'
        else:
            obj_script = Script.objects.get(pk=cod_script_frm)
            obj_script.desc = desc_frm
            obj_script.script = script_frm
            obj_script.obs = obs_frm
            obj_script.cod_usu = obj_usuario_sessao
            obj_script.data_ultima_alteracao = data_hora_atual
            obj_script.cod_conexao = obj_conexao
            obj_script.save()
            msg = 'Consulta atualizados com sucesso!'

        lista_consultas = list(Script.objects.all().values('cod_script', 'desc'))

        data = dict()
        data = {
            'msg': msg,
            'cod_script': obj_script.cod_script,
            'desc': obj_script.desc,
            'script': obj_script.script,
            'obs': obj_script.obs,
            'cod_conexao': obj_conexao.cod_conexao,
            'lista_consultas': lista_consultas
        }

        return JsonResponse(data, safe=False)

class Frm_Parametro_View(View):
    def post(self, request):
        cod_param_frm = request.POST['cod_param']
        cod_script_frm = request.POST['cod_script']
        desc_frm = request.POST['desc']
        tipo_frm = request.POST['tipo']

        obj_script = Script.objects.get(pk=cod_script_frm)

        msg = ''
        obj_param = None
        if int(cod_param_frm) == 0:
            obj_param = Parametro(
                desc=desc_frm,
                tipo=tipo_frm,
                cod_script=obj_script,
            )
            obj_param.save()
            msg = 'Parâmetro adicionado!'
        else:
            obj_param = Parametro.objects.get(pk=cod_param_frm)
            obj_param.cod_script = obj_script
            obj_param.desc = desc_frm
            obj_param.tipo = tipo_frm
            obj_param.save()
            msg = 'Parâmetro atualizados com sucesso!'

        data = dict()
        data = {
            'msg': msg,
            'cod_script': obj_script.cod_script,
            'cod_param': obj_param.cod_param,
            'desc': obj_param.desc,
            'tipo': obj_param.tipo,
        }
        return JsonResponse(data, safe=False)


class Frm_Acesso_Consulta_View(View):
    def get(self, request):
        cod_script_frm = request.GET['cod_script']

        obj_script = Script.objects.get(pk=cod_script_frm)
        lista_obj_param = list(Parametro.objects.filter(cod_script=obj_script).values('cod_param', 'desc', 'tipo'))

        lista_usuarios = list(Usuario.objects.filter(status_usu='A').values('cod_usu', 'login_usu','nome_usu'))

        lista_usu_vinculados = list(
            Liberacao.objects.filter(cod_script=obj_script).values('cod_usu__cod_usu', 'cod_usu__nome_usu'))


        dic_script = {
            'desc': obj_script.desc,
            'script': obj_script.script,
            'obs': obj_script.obs,
            'cod_conexao': obj_script.cod_conexao.cod_conexao,
            'lista_obj_param': lista_obj_param,
            'lista_usu_vinculados': lista_usu_vinculados,
            'lista_usuarios': lista_usuarios
        }

        data = dict()
        data = {
            'dic_script': dic_script,
        }
        return JsonResponse(data, safe=False)

    def post(self, request):
        cod_script_frm = request.POST['cod_script']
        lista_cod_usuarios = request.POST['lista_cod_usuarios']

        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        obj_script = Script.objects.get(pk=cod_script_frm)
        lista_obj_vincula_cod_usu_consulta= Liberacao.objects.filter(cod_script=obj_script)

        for reg in lista_obj_vincula_cod_usu_consulta:
            reg.delete()
        if lista_cod_usuarios != '' and lista_cod_usuarios != None:
            for cod_usu in lista_cod_usuarios.split(','):
                obj_usu = Usuario.objects.get(pk=cod_usu)
                obj_lib= Liberacao(
                    cod_usu=obj_usu,
                    cod_script=obj_script,
                ).save()

        data = dict()
        data = {
            'msg': 'Usuário(s) vinculado(s) com sucesso!'
        }
        return JsonResponse(data, safe=False)


class Frm_Consulta_Disponivel_View(View):
    def get(self,request):
        cod_usuario_sessao = request.session['cod_usuario_logado']
        obj_usuario_sessao = Usuario.objects.get(pk=cod_usuario_sessao)

        lista_consultas_liberadas = Liberacao.objects.filter(cod_usu=obj_usuario_sessao)

        context = {
            'obj_usuario_sessao': obj_usuario_sessao,
            'lista_consultas': lista_consultas_liberadas,
        }
        return render(request, 'ti_gera_consultas_app/frm_consultas_disponiveis.html', context)


class Frm_Param_Consulta_View(View):
    def get(self, request):
        cod_script_frm = request.GET['cod_script']

        obj_script = Script.objects.get(pk=cod_script_frm)
        lista_obj_param = list(Parametro.objects.filter(cod_script=obj_script).values('cod_param', 'desc', 'tipo'))

        data = dict()
        data = {
            'lista_obj_param': lista_obj_param
        }

        return JsonResponse(data, safe=False)



class Frm_Executa_Consulta_View(View):

    def get(self, request):
        try:
            cod_script_frm = request.GET['cod_script']
            dados_json = request.GET.get('dados', '[]')
            obj_script = Script.objects.get(pk=cod_script_frm)
            obj_conexao = obj_script.cod_conexao

            dados = json.loads(dados_json)
            consulta = obj_script.script
            valores = [item['value'] for item in dados]

            conexao_string = obj_conexao.string_conexao
            with  pyodbc.connect(conexao_string) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(consulta, valores)
                    resultados = cursor.fetchall()
                    colunas = [col[0] for col in cursor.description]

            resultados_formatados = [dict(zip(colunas, linha)) for linha in resultados]

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet("Consulta")

            if resultados_formatados:
                fieldnames = list(resultados_formatados[0].keys())

                # Escrevendo cabeçalhos
                for col_num, fieldname in enumerate(fieldnames):
                    worksheet.write(0, col_num, fieldname)

                # Escrevendo dados
                for row_num, linha in enumerate(resultados_formatados, start=1):
                    for col_num, fieldname in enumerate(fieldnames):
                        value = linha.get(fieldname, '')
                        worksheet.write(row_num, col_num, value)

            workbook.close()

            response = HttpResponse(
                output.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response['Content-Disposition'] = 'attachment; filename="consulta_resultados.xlsx"'

            return response

        except Exception as e:

            return JsonResponse({'error': str(e)}, status=400)








