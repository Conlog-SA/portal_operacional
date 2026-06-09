import ast
import traceback
from datetime import datetime, date

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.envio_email_app.views import Envio_Email
from apps.estrut_org_app.models import Filial
from apps.safety_blitz_trajeto_bicicleta_app.models import Blitz_Trajeto_Bicicleta
from apps.safety_blitz_trajeto_carro_app.models import Blitz_Trajeto_Carro
from apps.safety_blitz_trajeto_moto_app.models import Blitz_Trajeto_Moto
from apps.safety_blitz_trajeto_outros_meios_app.models import Blitz_Trajeto_Outros_Meios
from apps.safety_checks_aplicados_app.models import Check_Aplicado, Item_Check_Aplicados, \
    Item_Fotos_Texto_Check_Aplicado
from apps.safety_gab_empilhadeira_app.models import Check_Empilhadeira
from apps.safety_gab_op_emp_app.models import Gabarito_Operacional_Emp
from apps.safety_gso_app.models import Gabarito_GSO
from apps.safety_layout_checklist_app.models import Libera_Filial_Check, Layout_Check, Item_Check, Itens_Componentes
from apps.safety_login_colaboradores_app.models import Colaborador
from apps.safety_relatos_app.models import Relato
from apps.usuario_app.models import Usu_Menu
from proj_portal_operacional.settings import VERSAO_SAFETY

class Login_Colaborador(View):
    @csrf_exempt
    def get(self, request):
        id_visitante = request.GET.get('id_visitante')
        if id_visitante is not None:
            colaborador = Colaborador.objects.get(cod_colaborador=id_visitante)
            if "Visitante" in colaborador.nome_colaborador:
                request.session['cod_colaborador'] = id_visitante
                filial_visitante = colaborador.cod_filial
                request.session['cod_empresa_selecionada'] = str(filial_visitante.cod_empresa.cod_empresa)
                request.session['cod_empresa'] = str(filial_visitante.cod_empresa.cod_empresa)
                if request.session['cod_empresa'] == '12':
                    request.session['cor_empresa'] = '#f46424'
                elif request.session['cod_empresa'] == '17':
                    request.session['cor_empresa'] = '#3b8eed'
                return redirect('relatos_check')

        '''flag_voltar = request.GET.get('flag_voltar')
        if flag_voltar == "1":
            return render(request, 'safety_login_colaboradores_app/seleciona_empresa_fragment.html')'''
        empresa = request.GET.get('empresa')
        if empresa == 'conlog':
            cod_empresa = '12'
            cor_empresa = '#f46424'
            request.session['cod_empresa_selecionada'] = '12'
            request.session['cod_empresa'] = cod_empresa
        elif empresa == 'deep':
            cod_empresa = '17'
            cor_empresa = '#3b8eed'
            request.session['cod_empresa_selecionada'] = '17'
            request.session['cod_empresa'] = cod_empresa
        else:
            #return redirect('/safety_login_colaboradores_app/')
            return render(request, 'safety_login_colaboradores_app/frm_seleciona_empresa.html')
        context = {
            'VERSAO_SAFETY': VERSAO_SAFETY,
            'cor_empresa': cor_empresa,
            'cod_empresa': cod_empresa
        }
        return render(request, 'safety_login_colaboradores_app/frm_safe_login.html', context)

    @csrf_exempt
    def post(self, request):
        flag_voltar = request.POST.get('flag_voltar', '0')
        if '1' in flag_voltar:
            cod_check_aplicado_frm = request.POST.get('cod_check_aplicado', '0')
            if cod_check_aplicado_frm != '':
                self.envia_email_check_aplicado(cod_check_aplicado_frm)
            return redirect('safe_main_menu')
        cpf_colaborador = request.POST['cpf_colaborador']
        data_nasc_colab = request.POST['data_nasc_colaborador']
        data_nasc_array = data_nasc_colab.split('-')
        data_nasc_colab = datetime(int(data_nasc_array[0]), int(data_nasc_array[1]), int(data_nasc_array[2]))
        cod_empresa_selecionada = request.session['cod_empresa_selecionada']
        #print(f'Empresa selecionada : {cod_empresa_selecionada}')
        colaboradores = Colaborador.objects.filter(cpf=cpf_colaborador, data_nascimento=data_nasc_colab, situacao=1,
                                                   cod_empresa = cod_empresa_selecionada)

        if colaboradores.first() != None and colaboradores.count() == 1:
            #filial_colaborador = Filial.objects.get(pk=colaboradores.first().cod_filial)
            filial_colaborador = colaboradores.first().cod_filial
            cod_empresa_colaborador = filial_colaborador.cod_empresa.cod_empresa
            #print(f"Empresa selecionada : {request.session['cod_empresa_selecionada']}, empresa do colaborador : {cod_empresa_colaborador}")
            if str(request.session['cod_empresa_selecionada']) == str(cod_empresa_colaborador) or filial_colaborador.cod_filial not in [34, 57, 89]:
                request.session['cod_colaborador'] = colaboradores.first().cod_colaborador
                return redirect('safe_main_menu')
            elif str(request.session['cod_empresa_selecionada']) != str(cod_empresa_colaborador) or filial_colaborador.cod_filial in [34, 57, 89]:
                request.session['cod_colaborador'] = colaboradores.first().cod_colaborador
                return redirect('safe_main_menu')
            else:
                msg_erro = 'Empresa incorreta, clique em voltar e escolha a empresa correta.'
        else:
            msg_erro = 'Colaborador não existente/cadastrado.'

        return HttpResponse(msg_erro, status=401)


    def envia_email_check_aplicado(self, cod_check_aplicado_frm):
        obj_check_aplicado = Check_Aplicado.objects.get(pk=int(cod_check_aplicado_frm))
        lista_email_cco = ast.literal_eval(obj_check_aplicado.cod_filial.emails_envio_checks_safety)
        lista_obj_itens_lay = Item_Check.objects.filter(cod_check=obj_check_aplicado.cod_layout_check.cod_check)
        corpo_email = ''
        assunto_email = ''
        try:
            #GSO Empilhadeira
            if obj_check_aplicado.cod_layout_check.cod_check == 3:
                obj_check_emp = Gabarito_Operacional_Emp.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                desc_tipo_operador = 'Colaborador' if obj_check_emp.tipo_operador == 1 else 'Terceiro'
                items_check = ''
                qtd_itens_check = 0
                qtd_itens_ok = 0
                qtd_itens_nok = 0
                qtd_itens_sem_resp = 0
                for item_lay in lista_obj_itens_lay:
                    qtd_itens_check += 1
                    obj_item_aplicado = Item_Check_Aplicados.objects.filter(cod_check_aplicado=obj_check_aplicado, cod_item_check=item_lay).first()
                    desc_resp = ''
                    campo_obs_img = ''
                    if obj_item_aplicado != None:
                        if obj_item_aplicado.resp_item == 1:
                            desc_resp = '<span style="color: #FB2C36;">NOK</span>'
                            qtd_itens_nok += 1
                        else:
                            desc_resp = '<span style="color: #05DF72;">OK</span>'
                            qtd_itens_ok += 1
                        if obj_item_aplicado.cod_item_check.campo_obs_img == 1:
                            obj_obs_img = Item_Fotos_Texto_Check_Aplicado.objects.filter(cod_check_aplicado=obj_check_aplicado, cod_item_check=obj_item_aplicado.cod_item_check).first()
                            list_caminho_imagem = obj_obs_img.caminho_imagem.split('\\')
                            caminho_imagem_server = 'https://operacional.conlogsa.com.br/' + '/'.join(list_caminho_imagem[4:])
                            campo_obs_img += f'''
                                <b>Observação:</b>{obj_obs_img.comentario}<br/>
                                <img src="{caminho_imagem_server}" width="500" heigth="600">
                            '''
                    else:
                        desc_resp = '<span style="color: #FFDF20;">Não respondido</span>'
                        qtd_itens_sem_resp += 1

                    items_check += f'''
                        <p>
                            - {item_lay.desc_check} : <b>{desc_resp}</b></br>
                            {campo_obs_img}
                        </p>
                    '''

                corpo_email = f'''
                    <h3>CHECK EMPILHADEIRA #{obj_check_aplicado.cod_check_aplicado}</h3>
                    <div style="font-size: 15px;">
                        <b>Unidade: </b>{obj_check_aplicado.cod_filial.desc_filial}<br>
                        <b>Colaborador: </b>{obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}<br>
                        <b>Tipo operador: </b>{desc_tipo_operador}<br>
                        <b>Empilhadeira: </b> {obj_check_emp.cod_empilhadeira.placa}({obj_check_emp.cod_empilhadeira.desc_placa})
                        <br/>
                        <table style="width: 100%; margin: .5rem; border-collapse: collapse;background: #B8E6FE;color: #000000;">
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total itens check
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total OK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total NOK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">Não respondidos</td>
                            </tr>                
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_check}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_ok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_nok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_sem_resp}
                                </td>
                            </tr>
                        </table>     
                        <h4>#ITENS AVALIADOS</h4>
                         {items_check}
                        <span style="font-size: 12px;">Para mais detalhes, acesso o 
                        <a href="https://bi.conlogsa.com.br/">BI da companhia</a>, ou acesse o <a href="https://operacional.conlogsa.com.br/">Portal Operacional</a> </span>
                    </div>
                '''
                assunto_email += f'Safety - Check empilhadeira #{obj_check_aplicado.cod_check_aplicado}. Filial: {obj_check_aplicado.cod_filial.desc_filial}. Empilhadeira:  {obj_check_emp.cod_empilhadeira.placa}({obj_check_emp.cod_empilhadeira.desc_placa}).'

            #GSO onibus
            elif obj_check_aplicado.cod_layout_check.cod_check in (11, 12):
                obj_check_onibus = Gabarito_GSO.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                items_check = ''
                qtd_itens_check = 0
                qtd_itens_ok = 0
                qtd_itens_nok = 0
                qtd_itens_na = 0
                qtd_itens_sem_resp = 0
                for item_lay in lista_obj_itens_lay:
                    qtd_itens_check += 1
                    obj_item_aplicado = Item_Check_Aplicados.objects.filter(cod_check_aplicado=obj_check_aplicado, cod_item_check=item_lay).first()
                    desc_resp = ''
                    campo_obs_img = ''
                    if obj_item_aplicado != None:
                        if item_lay.tipo_resposta == 5:
                            if obj_item_aplicado.resp_item == 0:
                                desc_resp = '<span style="color: #05DF72;">OK</span>'
                                qtd_itens_ok += 1
                            elif obj_item_aplicado.resp_item == 1:
                                desc_resp = '<span style="color: #FB2C36;">NOK</span>'
                                qtd_itens_nok += 1
                            elif obj_item_aplicado.resp_item == 2:
                                desc_resp = '<span style="color: #53EAFD;">NA</span>'
                                qtd_itens_na += 1
                        elif item_lay.tipo_resposta == 6:
                            if obj_item_aplicado.resp_item == 0:
                                desc_resp = '<span style="color: #05DF72;">ÓTIMO</span>'
                            elif obj_item_aplicado.resp_item == 3:
                                desc_resp = '<span style="color: #FFDF20;">BOM</span>'
                            elif obj_item_aplicado.resp_item == 4:
                                desc_resp = '<span style="color: #FE9A37;">REGULAR</span>'
                            elif obj_item_aplicado.resp_item == 1:
                                desc_resp = '<span style="color: #FB2C36;">DANIFICADO</span>'


                        if obj_item_aplicado.cod_item_check.campo_obs_img == 1:
                            obj_obs_img = Item_Fotos_Texto_Check_Aplicado.objects.filter(cod_check_aplicado=obj_check_aplicado, cod_item_check=obj_item_aplicado.cod_item_check).first()
                            comp_img = ''
                            if obj_obs_img.caminho_imagem != None:
                                list_caminho_imagem = obj_obs_img.caminho_imagem.split('\\')
                                caminho_imagem_server = 'https://operacional.conlogsa.com.br/' + '/'.join(list_caminho_imagem[4:])
                                comp_img = f'<img src="{caminho_imagem_server}" width="500" heigth="600">'
                            campo_obs_img += f'''
                                <b>Observação:</b>{obj_obs_img.comentario}<br/>
                                {comp_img}
                            '''
                    else:
                        desc_resp = '<span style="color: #AD46FF;">Não respondido</span>'
                        qtd_itens_sem_resp += 1

                    items_check += f'''
                        <p>
                            - {item_lay.desc_check} : <b>{desc_resp}</b></br>
                            {campo_obs_img}
                        </p>
                    '''

                corpo_email = f'''
                    <h3>CHECK GSO ÔNIBUS #{obj_check_aplicado.cod_check_aplicado}</h3>
                    <div style="font-size: 15px;">
                        <b>Unidade: </b>{obj_check_aplicado.cod_filial.desc_filial}<br>
                        <b>Colaborador: </b>{obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}<br>
                        <b>Placa: </b> {obj_check_onibus.placa_onibus}
                        <br/>
                        <table style="width: 100%; margin: .5rem; border-collapse: collapse;background: #B8E6FE;color: #000000;">
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total itens check
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total OK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total NOK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total NA
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Não respondidos
                                </td>
                            </tr>                
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_check}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_ok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_nok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_na}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_sem_resp}
                                </td>
                            </tr>
                        </table>     
                        <h4>#ITENS AVALIADOS</h4>
                         {items_check}
                        <span style="font-size: 12px;">Para mais detalhes, acesso o 
                        <a href="https://bi.conlogsa.com.br/">BI da companhia</a>, ou acesse o <a href="https://operacional.conlogsa.com.br/">Portal Operacional</a> </span>
                    </div>
                '''
                assunto_email += f'Safety - Check GSO Ônibus #{obj_check_aplicado.cod_check_aplicado}. Filial: {obj_check_aplicado.cod_filial.desc_filial}. Placa ônibus:  {obj_check_onibus.placa_onibus}.'

            #Check Empilhadeira
            elif obj_check_aplicado.cod_layout_check.cod_check == 13:
                obj_check_emp = Check_Empilhadeira.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                items_check = ''
                qtd_itens_check = 0
                qtd_itens_ok = 0
                qtd_itens_nok = 0
                qtd_itens_na = 0
                qtd_itens_sem_resp = 0
                for item_lay in lista_obj_itens_lay:
                    qtd_itens_check += 1
                    obj_item_aplicado = Item_Check_Aplicados.objects.filter(cod_check_aplicado=obj_check_aplicado, cod_item_check=item_lay).first()
                    desc_resp = ''
                    campo_obs_img = ''
                    if obj_item_aplicado != None:
                        if item_lay.tipo_resposta == 5:
                            if obj_item_aplicado.resp_item == 0:
                                desc_resp = '<span style="color: #05DF72;">OK</span>'
                                qtd_itens_ok += 1
                            elif obj_item_aplicado.resp_item == 1:
                                desc_resp = '<span style="color: #FB2C36;">NOK</span>'
                                qtd_itens_nok += 1
                            elif obj_item_aplicado.resp_item == 2:
                                desc_resp = '<span style="color: #53EAFD;">NA</span>'
                                qtd_itens_na += 1


                        if obj_item_aplicado.cod_item_check.campo_obs_img == 1:
                            obj_obs_img = Item_Fotos_Texto_Check_Aplicado.objects.filter(cod_check_aplicado=obj_check_aplicado, cod_item_check=obj_item_aplicado.cod_item_check).first()
                            comp_img = ''
                            if obj_obs_img.caminho_imagem != None:
                                list_caminho_imagem = obj_obs_img.caminho_imagem.split('\\')
                                caminho_imagem_server = 'https://operacional.conlogsa.com.br/' + '/'.join(list_caminho_imagem[4:])
                                comp_img = f'<img src="{caminho_imagem_server}" width="500" heigth="600">'
                            campo_obs_img += f'''
                                <b>Observação:</b>{obj_obs_img.comentario}<br/>
                                {comp_img}
                            '''
                    else:
                        desc_resp = '<span style="color: #AD46FF;">Não respondido</span>'
                        qtd_itens_sem_resp += 1

                    items_check += f'''
                        <p>
                            - {item_lay.desc_check} : <b>{desc_resp}</b></br>
                            {campo_obs_img}
                        </p>
                    '''

                corpo_email = f'''
                    <h3>CHECK EMPILHADEIRA #{obj_check_aplicado.cod_check_aplicado}</h3>
                    <div style="font-size: 15px;">
                        <b>Unidade: </b>{obj_check_aplicado.cod_filial.desc_filial}<br>
                        <b>Colaborador: </b>{obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}<br>
                        <b>Placa: </b> {obj_check_emp.cod_empilhadeira.placa}({obj_check_emp.cod_empilhadeira.desc_placa})
                        <br/>
                        <table style="width: 100%; margin: .5rem; border-collapse: collapse;background: #B8E6FE;color: #000000;">
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total itens check
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total OK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total NOK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total NA
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Não respondidos
                                </td>
                            </tr>                
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_check}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_ok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_nok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_na}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_sem_resp}
                                </td>
                            </tr>
                        </table>     
                        <h4>#ITENS AVALIADOS</h4>
                         {items_check}
                        <span style="font-size: 12px;">Para mais detalhes, acesso o 
                        <a href="https://bi.conlogsa.com.br/">BI da companhia</a>, ou acesse o <a href="https://operacional.conlogsa.com.br/">Portal Operacional</a> </span>
                    </div>
                '''
                assunto_email += f'Safety - Check Empilhadeira #{obj_check_aplicado.cod_check_aplicado}. Filial: {obj_check_aplicado.cod_filial.desc_filial}. Placa:  {obj_check_emp.cod_empilhadeira.placa}({obj_check_emp.cod_empilhadeira.desc_placa}).'

            #Relatos
            elif obj_check_aplicado.cod_layout_check.cod_check == 5:
                obj_check_relato = Relato.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                items_check = ''
                info_tipo_relato = ''
                if obj_check_relato.cod_tipo_relato == 1:
                    desc_situacao_envolvido = 'Não informado'
                    if obj_check_relato.situacao_envolvido == 1:
                        desc_situacao_envolvido = 'Funcionario Conlog/Deep'
                    elif obj_check_relato.situacao_envolvido == 2:
                        desc_situacao_envolvido = 'Funcionario Ambev'
                    elif obj_check_relato.situacao_envolvido == 3:
                        desc_situacao_envolvido = 'Freteiro'
                    elif obj_check_relato.situacao_envolvido == 4:
                        desc_situacao_envolvido = 'Terceiro'

                    info_tipo_relato += f'''
                        <b>Tipo Relato: </b> Ato Inseguro - {Itens_Componentes.objects.get(pk=obj_check_relato.categoria_ato_inseguro).desc_componente}<br/>
                        <b>Quem gerou esta condição?: </b> {desc_situacao_envolvido}<br/>
                        <b>Relatado: </b> {obj_check_aplicado.cod_colaborador_avaliado.nome_colaborador}<br/>                    
                    '''
                elif obj_check_relato.cod_tipo_relato == 2:
                    info_tipo_relato += f'''
                        <b>Tipo Relato: </b> Condição Insegura - {Itens_Componentes.objects.get(pk=obj_check_relato.categoria_condicao_insegura).desc_componente}<br/>                   
                    '''
                elif obj_check_relato.cod_tipo_relato == 3:
                    desc_situacao_envolvido = 'Não informado'
                    if obj_check_relato.situacao_envolvido == 1:
                        desc_situacao_envolvido = 'Funcionario Conlog/Deep'
                    elif obj_check_relato.situacao_envolvido == 2:
                        desc_situacao_envolvido = 'Funcionario Ambev'
                    elif obj_check_relato.situacao_envolvido == 3:
                        desc_situacao_envolvido = 'Freteiro'
                    elif obj_check_relato.situacao_envolvido == 4:
                        desc_situacao_envolvido = 'Terceiro'

                    info_tipo_relato += f'''
                        <b>Tipo Relato: </b> Abordagem Positiva - {Itens_Componentes.objects.get(pk=obj_check_relato.categoria_comportamento_seguro).desc_componente}<br/>
                        <b>Quem gerou esta condição?: </b> {desc_situacao_envolvido}<br/>
                        <b>Relatado: </b> {obj_check_aplicado.cod_colaborador_avaliado.nome_colaborador}<br/>                 
                    '''


                for item_lay in lista_obj_itens_lay:
                    obj_obs_img = Item_Fotos_Texto_Check_Aplicado.objects.filter(
                        cod_check_aplicado=obj_check_aplicado,
                        cod_item_check=item_lay.cod_item_check).first()
                    campo_obs_img = ''
                    comp_img = ''

                    items_check += f'''
                        <p>
                        - {item_lay.desc_check} : <br/>
                    '''
                    if obj_obs_img != None:
                        if obj_obs_img.caminho_imagem != None:
                            list_caminho_imagem = obj_obs_img.caminho_imagem.split('\\')
                            caminho_imagem_server = 'https://operacional.conlogsa.com.br/' + '/'.join(
                                list_caminho_imagem[4:])
                            comp_img = f'<img src="{caminho_imagem_server}" width="500" heigth="600">'


                        items_check += f'''
                            <p>
                                <b>{obj_obs_img.comentario}</b></br>
                                {comp_img}
                            </p>
                        '''
                    else:
                        items_check += f'''
                            <p>
                                <b>Nenhuma ação tomada no momento</b></br>
                            </p>
                        '''


                corpo_email = f'''
                                <h3>CHECK RELATO #{obj_check_aplicado.cod_check_aplicado}</h3>
                                <div style="font-size: 15px;">
                                    <b>Unidade: </b>{obj_check_aplicado.cod_filial.desc_filial}<br>
                                    <b>Colaborador: </b>{obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}<br>
                                    {info_tipo_relato}
                                    <b>Local: </b>{obj_check_relato.local_relato}<br/>
                                    <b>Processo: </b>{Itens_Componentes.objects.get(pk = obj_check_relato.processo_relato).desc_componente}
                                    <br/>
                                    <br/>                                    
                                    <h4>#DETALHES DO RELATO</h4>
                                     {items_check}
                                    <span style="font-size: 12px;">Para mais detalhes, acesso o 
                                    <a href="https://bi.conlogsa.com.br/">BI da companhia</a>, ou acesse o <a href="https://operacional.conlogsa.com.br/">Portal Operacional</a> </span>
                                </div>
                            '''
                assunto_email += f'Safety - Relato #{obj_check_aplicado.cod_check_aplicado}. Filial: {obj_check_aplicado.cod_filial.desc_filial}. (Relatado por:  {obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}).'

            # Blitz Trajeto/Carro/Moto/Bicicleta/Outros Meios
            elif obj_check_aplicado.cod_layout_check.cod_check in [7, 8, 9, 10]:
                meio_transporte = ''
                info_placa = ''
                obj_check_blitz = None
                if obj_check_aplicado.cod_layout_check.cod_check == 7:
                    meio_transporte = 'Carro'
                    obj_check_blitz = Blitz_Trajeto_Carro.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                    info_placa = f'<b> Placa: </b> {obj_check_blitz.placa} <br/>'
                elif obj_check_aplicado.cod_layout_check.cod_check == 8:
                    meio_transporte = 'Moto'
                    obj_check_blitz = Blitz_Trajeto_Moto.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                    info_placa = f'<b> Placa: </b> {obj_check_blitz.placa} <br/>'
                elif obj_check_aplicado.cod_layout_check.cod_check == 9:
                    meio_transporte = 'Bicicleta'
                    obj_check_blitz = Blitz_Trajeto_Bicicleta.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                elif obj_check_aplicado.cod_layout_check.cod_check == 10:
                    obj_check_blitz = Blitz_Trajeto_Outros_Meios.objects.filter(cod_check_aplicado=obj_check_aplicado).first()
                    if obj_check_blitz.meio_transporte == 1:
                        meio_transporte = 'Outros Meios(Transporte Público)'
                    elif obj_check_blitz.meio_transporte == 2:
                        meio_transporte = 'Outros Meios(Carona)'
                    elif obj_check_blitz.meio_transporte == 3:
                        meio_transporte = 'Outros Meios(Pé)'
                    elif obj_check_blitz.meio_transporte == 4:
                        meio_transporte = 'Outros Meios(Transporte por aplicativo)'
                items_check = ''
                qtd_itens_check = 0
                qtd_itens_ok = 0
                qtd_itens_nok = 0
                qtd_itens_sem_resp = 0
                for item_lay in lista_obj_itens_lay:
                    obj_item_aplicado = Item_Check_Aplicados.objects.filter(cod_check_aplicado=obj_check_aplicado,
                                                                            cod_item_check=item_lay).first()
                    desc_resp = ''
                    campo_obs_img = ''
                    if item_lay.tipo_resposta == 1:
                        qtd_itens_check += 1
                    if obj_item_aplicado != None and item_lay.tipo_resposta != 2:
                        if item_lay.tipo_resposta == 1:
                            if obj_item_aplicado.resp_item == 0:
                                desc_resp = '<span style="color: #05DF72;">OK</span>'
                                qtd_itens_ok += 1
                            elif obj_item_aplicado.resp_item == 1:
                                desc_resp = '<span style="color: #FB2C36;">NOK</span>'
                                qtd_itens_nok += 1
                        elif item_lay.tipo_resposta == 3:
                            if obj_item_aplicado.resp_item == 0:
                                desc_resp = '<span style="color: #05DF72;">SIM</span>'
                            elif obj_item_aplicado.resp_item == 1:
                                desc_resp = '<span style="color: #FB2C36;">NÃO</span>'
                        elif item_lay.tipo_resposta == 4:
                            if obj_item_aplicado.resp_item == 0:
                                desc_resp = '<span style="color: #05DF72;">PRÓPRIO</span>'
                            elif obj_item_aplicado.resp_item == 1:
                                desc_resp = '<span style="color: #FB2C36;">COMPANHIA</span>'
                    elif item_lay.tipo_resposta == 2:
                        obj_obs_img = Item_Fotos_Texto_Check_Aplicado.objects.filter(
                            cod_check_aplicado=obj_check_aplicado,
                            cod_item_check=item_lay).first()
                        desc_resp = obj_obs_img.comentario
                    else:
                        desc_resp = '<span style="color: #FFDF20;">Não respondido</span>'
                        qtd_itens_sem_resp += 1

                    items_check += f'''
                        <p>
                            - {item_lay.desc_check} : <b>{desc_resp}</b></br>
                        </p>
                    '''

                desc_situacao_envolvido = 'Não informado'
                if obj_check_blitz.situacao_colaborador == 1:
                    desc_situacao_envolvido = 'Funcionario Conlog/Deep'
                elif obj_check_blitz.situacao_colaborador == 2:
                    desc_situacao_envolvido = 'Funcionario Ambev'
                elif obj_check_blitz.situacao_colaborador == 3:
                    desc_situacao_envolvido = 'Freteiro'
                elif obj_check_blitz.situacao_colaborador == 4:
                    desc_situacao_envolvido = 'Terceiro'
                nome_avaliado = obj_check_aplicado.cod_colaborador_avaliado.nome_colaborador

                table_resumo_qtd_itens_check = ''
                if qtd_itens_check > 0:
                    table_resumo_qtd_itens_check += f'''
                        <table style="width: 100%; margin: .5rem; border-collapse: collapse;background: #B8E6FE;color: #000000;">
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total itens check
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total OK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">
                                    Total NOK
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 11px;">Não respondidos</td>
                            </tr>                
                            <tr>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_check}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_ok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_nok}
                                </td>
                                <td style="padding: .5rem;font-weight: bold; text-align: center;vertical-align: middle; font-size: 18px;">
                                    {qtd_itens_sem_resp}
                                </td>
                            </tr>
                        </table>
                    '''
                corpo_email = f'''
                    <h3>CHECK BLITZ {meio_transporte} #{obj_check_aplicado.cod_check_aplicado}</h3>
                    <div style="font-size: 15px;">
                        <b>Unidade: </b>{obj_check_aplicado.cod_filial.desc_filial}<br>
                        <b>Aplicado por: </b>{obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}<br>
                        <b>Aplicado a: </b>{nome_avaliado}({desc_situacao_envolvido})<br/>
                        {info_placa}                        
                        <br/>
                        {table_resumo_qtd_itens_check}                                                         
                        <h4>#DETALHES DA BLITZ APLICADA</h4>
                         {items_check}
                        <span style="font-size: 12px;">Para mais detalhes, acesso o 
                        <a href="https://bi.conlogsa.com.br/">BI da companhia</a>, ou acesse o <a href="https://operacional.conlogsa.com.br/">Portal Operacional</a> </span>
                    </div>
                '''
                assunto_email += f'Safety - Blitz Trajeto {meio_transporte}. Check #{obj_check_aplicado.cod_check_aplicado}. Filial: {obj_check_aplicado.cod_filial.desc_filial}. (Aplicado por:  {obj_check_aplicado.cod_colaborador_aplicante.nome_colaborador}).'
            #lista_email_cco = ['danilo.costa@conlogsa.com.br', 'juliana.deus@conlogsa.com.br']
            Envio_Email().envia_email_layout_generico_safety_deep(lista_email_cco, assunto_email, corpo_email)
        except Exception as e:
            lista_email_cco = ['danilo.costa@conlogsa.com.br', 'juliana.deus@conlogsa.com.br']
            assunto_email = f'Erro Safety check #{obj_check_aplicado.cod_check_aplicado}'
            corpo_email = f'''
                <p>Exception: {e}. {traceback.print_exc()}</p>
            '''
            Envio_Email().envia_email_layout_generico_safety_deep(lista_email_cco, assunto_email, corpo_email)




class Login_Colaborador_Deep(View):
    @csrf_exempt
    def get(self, request):
        return render(request, 'safety_login_colaboradores_app/frm_safe_login_deep.html')

class Menu_Safe(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.session['cod_colaborador']
        colaborador = Colaborador.objects.get(pk=cod_colaborador)
        #print(f'Nome do colaborador logado: {colaborador.cod_colaborador} - {colaborador.nome_colaborador}')
        primeiro_nome_colaborador = colaborador.nome_colaborador.split(' ')[0].upper()
        #filial_colaborador = Filial.objects.get(pk=colaborador.cod_filial)
        filial_colaborador = colaborador.cod_filial
        desc_filial_colaborador = filial_colaborador.desc_filial
        empresa_colaborador = filial_colaborador.cod_empresa

        data_atual = datetime.now()

        if colaborador.perfil_usu == 'V':
            context = {
                'nome_colaborador': primeiro_nome_colaborador,
                'desc_filial_colaborador': desc_filial_colaborador,
                'id_relato': request.session['cod_relato'],
                'flag_visitante': True
            }

            return render(request, 'safety_login_colaboradores_app/safe_visitante_submit.html', context)
        else:
            check_ativo = None
            if colaborador.perfil_usu == 'U':
                check_ativo = (Libera_Filial_Check
                               .objects
                               .filter(cod_check__data_desativacao__gte=date(data_atual.year,
                                                                             data_atual.month,
                                                                             data_atual.day),
                                       cod_check__data_inicio__lte=date(data_atual.year,
                                                                        data_atual.month,
                                                                        data_atual.day),
                                       cod_filial=filial_colaborador)
                               .order_by('-cod_check__data_desativacao'))
            else:
                check_ativo = (Libera_Filial_Check
                               .objects
                               .filter(cod_check__data_desativacao__gte=date(data_atual.year,
                                                                             data_atual.month,
                                                                             data_atual.day),
                                       cod_check__data_inicio__lte=date(data_atual.year,
                                                                        data_atual.month,
                                                                        data_atual.day))
                               .order_by('-cod_check__data_desativacao'))


            str_menu_colaborador = ''


            filiais_transporte_pessoas = Filial.objects.filter(cod_empresa=12, cod_filial__in=[34, 57, 89])
            filiais = Filial.objects.filter(cod_empresa=filial_colaborador.cod_empresa,
                                            cod_filial__in=check_ativo.values('cod_filial').distinct())


            if filial_colaborador.cod_empresa.cod_empresa == 12 and filial_colaborador.cod_filial not in [34, 57, 89]:
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))
            elif filial_colaborador.cod_empresa.cod_empresa == 12 and filial_colaborador.cod_filial in [34, 57, 89]:
                filiais_transporte_pessoas = filiais_transporte_pessoas.exclude(cod_filial=filial_colaborador.cod_filial)
                filiais = filiais.exclude(cod_filial__in=filiais_transporte_pessoas.values('cod_filial'))

            elif filial_colaborador.cod_empresa.cod_empresa == 17:
                filiais = filiais.union(filiais_transporte_pessoas)

            check_ativo = check_ativo.filter(cod_filial__in=filiais.values('cod_filial'))



            if check_ativo.filter(cod_check__tipo_check=1).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-empilhadeiras-gso" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-dolly icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;">GSO - Empilhadeiras</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=8).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-gso" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-bus icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;">GSO - Ônibus</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=9).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-empilhadeiras" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-warehouse icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;">Empilhadeiras</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=2).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-relatos" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-file-signature icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;">Relatos</b>
                    </div>
                '''

            if check_ativo.filter(cod_check__tipo_check=4).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-blitz-trajeto-carro" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-car icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;margin-left: .4rem;">Blitz de Trajeto - Carro</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=5).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-blitz-trajeto-moto" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-motorcycle icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;">Blitz de Trajeto - Moto</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=6).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-blitz-trajeto-bicicleta" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-bicycle icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;">Blitz de Trajeto - Bicicleta</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=7).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-blitz-trajeto-outros-meios" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-road icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;margin-left: .4rem;">Blitz de Trajeto - Outros Meios</b>
                    </div>
                '''
            if check_ativo.filter(cod_check__tipo_check=12).first() is not None:
                str_menu_colaborador += '''
                    <div class="safety-container-app safety-app-registro-ocorrencias" style="margin-bottom:0.4rem;cursor:pointer;">
                        <i class="fa-solid fa-file-circle-exclamation icon-menu-safety" style="margin-bottom:5px"></i>
                        <b style="color:white;margin-left: .4rem;">Registro de Ocorrências</b>
                    </div>
                '''
            if colaborador.setor_administrativo == 1:
                if check_ativo.filter(cod_check__tipo_check=10).first() is not None:
                    str_menu_colaborador += '''
                        <div class="safety-container-app safety-app-predial" style="margin-bottom:0.4rem;cursor:pointer;">
                            <i class="fa-solid fa-building-circle-check icon-menu-safety" style="margin-bottom:5px"></i>
                            <b style="color:white;">Infra. e Predial</b>
                        </div>
                    '''

                if check_ativo.filter(cod_check__tipo_check=11).first() is not None:
                    str_menu_colaborador += '''
                        <div class="safety-container-app safety-app-pci" style="margin-bottom:0.4rem;cursor:pointer;">
                            <i class="fa-solid fa-fire-extinguisher icon-menu-safety" style="margin-bottom:5px"></i>
                            <b style="color:white;margin-left: .4rem;">Check - PCI</b>
                        </div>
                    '''

            str_menu_colaborador += '''</div>'''



            context = {
                'nome_colaborador': primeiro_nome_colaborador,
                'desc_filial_colaborador': desc_filial_colaborador,
                'str_menu_colaborador': str_menu_colaborador,
            }
            return render(request, 'safety_login_colaboradores_app/safe_main_menu.html', context)

    @csrf_exempt
    def post(self, request):
        tipo_check = request.POST.get('tipo_check', '')

        url = ''
        if tipo_check == '999':
            cod_colaborador = request.session['cod_colaborador']
            colaborador = Colaborador.objects.get(pk=cod_colaborador)
            empresa_colaborador = colaborador.cod_filial.cod_empresa.cod_empresa
            #if empresa_colaborador in [34, 57, 89]:
            #    cod_empresa = 17

            context = {
                "cod_empresa": request.session['cod_empresa']
            }

            return render(request, 'safety_login_colaboradores_app/frm_safe_login.html', context)
        elif tipo_check == '0':
            url = 'empilhadeira_gso_check'
        elif tipo_check == '1':
            url = 'relatos_check'
        #elif tipo_check == '2':
        #    url = 'gsdpq_check'
        elif tipo_check == '3':
            url = 'blitz_trajeto_carro_check'
        elif tipo_check == '4':
            url = 'blitz_trajeto_moto_check'
        elif tipo_check == '5':
            url = 'blitz_trajeto_bicicleta_check'
        elif tipo_check == '6':
            url = 'blitz_trajeto_outros_meios_check'
        elif tipo_check == '7':
            url = 'gso_check'
        elif tipo_check == '8':
            url = 'empilhadeira_check'
        elif tipo_check == '9':
            url = 'predial_check'
        elif tipo_check == '10':
            url = 'pci_check'
        elif tipo_check == '12':
            url = 'registro_de_ocorrencia_check'
        return redirect(url)

class Lista_Colaboradores(View):
    @csrf_exempt
    def get(self, request):
        tipo_check = request.GET['tipo_check']
        cod_unidade = request.GET['cod_unidade']

        lista_colaboradores = ((Colaborador.objects.filter(cod_filial=cod_unidade, situacao=1, ))
                               .order_by('nome_colaborador'))
        #                       | Colaborador.objects.filter(cod_filial=cod_unidade,perfil_usu='T'))
        if tipo_check == '1':
            lista_colaboradores = lista_colaboradores.filter(desc_cargo__icontains='op')
            lista_colaboradores = (lista_colaboradores.filter(desc_cargo__icontains='empilhadeira')
                                   .union(lista_colaboradores.filter(desc_cargo__icontains='Operador Conferente I')))
        if tipo_check == '8':
            lista_colaboradores = (lista_colaboradores.filter(desc_cargo__icontains='Motorista de Ônibus Rodoviário')
                                   .union(lista_colaboradores.filter(desc_cargo__icontains='Motorista Instrutor'))
                                   .union(lista_colaboradores.filter(desc_cargo__icontains='Instrutor de Motorista')))
        dict_colaboradores_options = []
        for colaborador in lista_colaboradores:
            dict_colaboradores_options.append({'cod_colaborador': colaborador.cod_colaborador, 'nome_colaborador': colaborador.nome_colaborador, 'desc_cargo': colaborador.desc_cargo}) #f'<option value="{operador.cod_colaborador}">{operador.nome_colaborador}</option>'
        data = {
            'lista_colaboradores': dict_colaboradores_options
        }
        return JsonResponse(data)

class Documento_Colaborador(View):
    @csrf_exempt
    def get(self, request):
        cod_colaborador = request.GET['cod_colaborador']

        colab_informado = Colaborador.objects.get(pk=cod_colaborador)
        cpf_colab_informado = colab_informado.cpf.zfill(11)
        return JsonResponse(cpf_colab_informado, safe=False)