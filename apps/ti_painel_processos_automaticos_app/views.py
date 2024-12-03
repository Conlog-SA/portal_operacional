from django.shortcuts import render
from django.views import View
from apps.usuario_app.models import Usuario
from apps.ti_painel_processos_automaticos_app.models import Processo


class Frm_Painel_Processos_Automaticos_View(View):
    def get(self, request):
        id_usu_session = request.session['cod_usuario_logado']
        obj_usuario_logado = Usuario.objects.get(pk=id_usu_session)

        lista_dic_proc_pri_0 = []
        lista_obj_proc_pri_0 = Processo.objects.filter(eh_ativo=0, cod_prioridade=0)
        for proc in lista_obj_proc_pri_0:
            dic_proc_info = {
                'nome_proc': proc.desc_processo,
                'data_ult_exec': '',
                'hora_ult_exec': '',
                'data_prox_exec': '',
                'hora_prox_exec': ''
            }
            lista_dic_proc_pri_0.append(dic_proc_info)



        lista_dic_proc_pri_1 = []
        lista_obj_proc_pri_1 = Processo.objects.filter(eh_ativo=1, cod_prioridade=1)
        for proc in lista_obj_proc_pri_1:
            dic_proc_info = {
                'nome_proc': proc.desc_processo,
                'data_ult_exec': '',
                'hora_ult_exec': '',
                'data_prox_exec': '',
                'hora_prox_exec': ''
            }
            lista_dic_proc_pri_1.append(dic_proc_info)



        context = {
            'desc_menu': 'Painel de Controle dos Processos - TI',
            'obj_usuario_logado': obj_usuario_logado,
            'lista_dic_proc_pri_0': lista_dic_proc_pri_0,
            'lista_dic_proc_pri_1': lista_dic_proc_pri_1
        }

        return render(request, 'ti_painel_processos_automaticos_app/frm_painel_processos_automaticos.html', context)

