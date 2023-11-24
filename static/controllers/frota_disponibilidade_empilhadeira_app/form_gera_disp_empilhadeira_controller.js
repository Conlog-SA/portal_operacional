/* let data_atual = new Date();
let diaAtual = dataAtual.getDate();
let mesAtual = dataAtual.getMonth()+1;
let anoAtual = dataAtual.getFullYear();

var dataInicio = "01"+"/"+mesAtual+"/"+anoAtual;
var dataFim = diaAtual+"/"+mesAtual+"/"+anoAtual; */

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(document).on('click', 'button', function(){
    let let_nome_btn = $(this).attr('name');
	let let_id_btn = $(this).attr('id');
	let let_val_btn = $(this).val();

    if ( let_nome_btn == 'btn_abre_model_pesq_emp_proj') {
        let let_cod_projeto_selecionado = $("#cb_proj_form_gera_disp_empilhadeira").val();
        if (let_cod_projeto_selecionado == ''){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Selecione um projeto',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

        } else {
            let let_loader_gera_disp_emp = document.getElementById("loader_gera_disp_emp");
            let_loader_gera_disp_emp.style.display = "flex";
            $.ajax({
            type:'POST',
            data: {
                'handle_proj'   :   let_cod_projeto_selecionado,
                'status_placa'  :   'T'
            },
            url: '/frota_disponibilidade_empilhadeira_app/abre_modal_param_geracao_disp_emp',
            dataType: 'json',
            success: function (dados){
                $("#cb_empilhadeiras_proj_selecionado option").remove();
                dados.lista_empilhadeiras.forEach( e => {
                    let let_desc_status = 'Empilhadeira Ativa'
                    if (e.ativo == 'N') {
                        let_desc_status = 'Empilhadeira Desativada';
                    }
                    $("#cb_empilhadeiras_proj_selecionado").append("<option value='"+
                        e.handle+"_"+e.placa+"_"+e.ano+"_"+e.modelo+"_"+e.placa_anterior+"_"+e.ativo+"'>"+
                        e.placa+"("+e.modelo+")/"+let_desc_status+
                        "</option> "
                    );
                });
                $("#cb_empilhadeiras_proj_selecionado").selectpicker("");
                $("#cb_empilhadeiras_proj_selecionado").selectpicker('refresh');


                let_loader_gera_disp_emp.style.display = "none";
                $("#modal_param_gerar_disp_emp").show();
            },
            error: function(request, status, error) {
                let_loader_gera_disp_emp.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
        }


    }
    else if ( let_nome_btn == 'btn_fecha_modal_param_gerar_disp_emp') {
        $("#modal_param_gerar_disp_emp").hide();
    } else if ( let_nome_btn == 'btn_confirma_geracao_disp_emp') {
        let let_handle_projeto_selecionado = $("#cb_proj_form_gera_disp_empilhadeira").val();
        let let_info_emp_selecionadas = $("#cb_empilhadeiras_proj_selecionado").val().toString();
        let let_data_ini_str = $("#dt_ini_gerar_disp_emp").val();
        let let_data_ini_dt = new Date(let_data_ini_str.split('-')[2], let_data_ini_str.split('-')[1],
            let_data_ini_str.split('-')[0]);
        let let_data_fim_str = $("#dt_fim_gerar_disp_emp").val();
        let let_data_fim_dt = new Date(let_data_fim_str.split('-')[2], let_data_fim_str.split('-')[1],
            let_data_fim_str.split('-')[0]);

        let let_periodo = let_data_ini_str.split('-')[0] + '-' +
            let_data_ini_str.split('-')[1];

        if(let_handle_projeto_selecionado == '' || let_info_emp_selecionadas == '' || let_data_ini_str == '' ||
            let_data_fim_str && (let_data_fim_dt < let_data_ini_dt)) {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Campos obrigatórios não informados!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $("#modal_param_gerar_disp_emp").hide();
            $.ajax({
                type: 'POST',
                data : {
                    'cod_projeto'   :   let_handle_projeto_selecionado,
                    'info_emp'      :   let_info_emp_selecionadas,
                    'data_ini'      :   let_data_ini_str,
                    'data_fim'      :   let_data_fim_str
                },
                url: '/frota_disponibilidade_empilhadeira_app/gera_dados_disp_emp',
                dataType: 'json',
                success: function(dados){
                    povoa_tabela_apontamento_disp_emp(let_handle_projeto_selecionado, let_periodo);
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                },
                error: function(request, status, error) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });
        }

    }
    else if ( let_nome_btn == 'btn_pesq_disp_emp') {
        let let_handle_proj_benner = $("#cb_proj_form_gera_disp_empilhadeira").val();
        let let_periodo = $("#dt_periodo_pesq_disp_emp").val();
        if ( let_periodo == '') {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Campos obrigatórios não informados!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            povoa_tabela_apontamento_disp_emp(let_handle_proj_benner, let_periodo);
        }

    } else if ( let_nome_btn == 'btn_show_detalhes_apont_emp' ){
        let let_cod_apontamento = let_val_btn;
        povoa_tabela_os_apontamento(let_cod_apontamento);

    } else if ( let_nome_btn == 'btn_fecha_modal_atualiza_apont_disp_emp' ){
        $("#modal_atualiza_apont_disp_emp").hide();
        let let_handle_proj = $("#cb_proj_form_gera_disp_empilhadeira").val();
        let let_periodo = $("#dt_periodo_pesq_disp_emp").val();
        povoa_tabela_apontamento_disp_emp(let_handle_proj, let_periodo);
    } else if (let_nome_btn == 'btn_excluir_os_apont_emp'){
        let let_cod_os_apontamento = let_val_btn;
        let let_handle_proj_benner = $("#cb_proj_form_gera_disp_empilhadeira").val();
        let let_periodo = $("#dt_periodo_pesq_disp_emp").val();
        let let_cod_apontamento = $("#hd_cod_apontamento").val();
        $.ajax({
            type: 'DELETE',
            url: '/frota_disponibilidade_empilhadeira_app/deleta_reg_os_apont_disp_emp/'+let_cod_os_apontamento,
            dataType: 'json',
            success: function(dados){
                $("#tab_os_apontamento_indisp_emp").DataTable().clear().draw();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tabela_os_apontamento(let_cod_apontamento);
            }, error: function(request, status, error){
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    } else if (let_nome_btn == 'btn_pesquisa_os_benner') {
        let let_cod_apontamento = let_val_btn;
        povoa_tabela_os_benner(let_cod_apontamento);

    } else if(let_nome_btn == 'btn_fecha_modal_os_benner_vincular_apontamento') {
        $("#modal_os_benner_vincular_apontamento").hide();
        /*let let_handle_proj = $("#cb_proj_form_gera_disp_empilhadeira").val();
        let let_periodo = $("#dt_periodo_pesq_disp_emp").val();
        povoa_tabela_apontamento_disp_emp(let_handle_proj, let_periodo);*/

    } else if(let_nome_btn == 'btn_vincular_os_apont_emp') {
        let let_cod_apontamento = $("#hd_cod_apont_emp").val();
        let let_handle_os = let_val_btn;
        let let_num_os = $("#hd_numero_os_benner" + var_handle_os).val();
        let let_tipo_os = $("#hd_handle_tipo_os_benner" + var_handle_os).val();
        let let_desc_tipo_os = $("#hd_desc_tipo_os_benner" + var_handle_os).val();
        let let_data_ini_os = $("#hd_data_ini_os_benner" + var_handle_os).val();
        let let_data_fim_os = $("#hd_data_fim_os_benner" + var_handle_os).val();
        let let_desc_os = $("#hd_desc_os_benner" + var_handle_os).val();
        let let_sit_os = $("#hd_sit_os_benner" + var_handle_os).val();
        let let_handle_conj = 0
        if ($("#hd_handle_conj_os_benner" + var_handle_os).val() != 'null'){
            let_handle_conj = $("#hd_handle_conj_os_benner" + let_handle_os).val();;
        }

        let let_desc_conj = ''
        if($("#hd_desc_conj_os_benner" + let_handle_os).val() != 'null') {
            let_desc_conj = $("#hd_desc_conj_os_benner" + let_handle_os).val();
        }
        loader_gera_disp_emp.style.display = "flex";
        $.ajax({
            type:'POST',
            data: {
                'cod_apontamento':  let_cod_apontamento,
                'handle_os':        let_handle_os,
                'num_os':           let_num_os,
                'tipo_os':          let_tipo_os,
                'desc_tipo_os':     let_desc_tipo_os,
                'data_ini_os':      let_data_ini_os,
                'data_fim_os':      let_data_fim_os,
                'desc_os':          let_desc_os,
                'sit_os':           let_sit_os,
                'handle_conj':      let_handle_conj,
                'desc_conj':        let_desc_conj
            },
            url: '/frota_disponibilidade_empilhadeira_app/vincula_os_apont_disp_emp',
            dataType:'json',
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tabela_os_benner(var_cod_apontamento);

            }, error(request, status, error){
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });

    } else if (let_nome_btn == 'btn_seleciona_todas_as_placas_ativas_model_gera_disp') {
        let let_handle_proj = $("#cb_proj_form_gera_disp_empilhadeira").val();
        loader_gera_disp_emp.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/frota_disponibilidade_empilhadeira_app/retorna_todas_placas_ativa_form_gera_disp_emp',
            data: {
                'handle_proj'   :   let_handle_proj,
                'status_placa'  :   'S'
            },
            dataType: 'json',
            success: function (dados) {
                $("#cb_empilhadeiras_proj_selecionado option").remove();
                dados.lista_empilhadeiras.forEach( e => {
                    var var_desc_status = 'Empilhadeira Ativa'
                    if (e.ativo == 'N') {
                        var_desc_status = 'Empilhadeira Desativada';
                    }
                    $("#cb_empilhadeiras_proj_selecionado").append("<option value='"+
                        e.handle+"_"+e.placa+"_"+e.ano+"_"+e.modelo+"_"+e.placa_anterior+"_"+e.ativo+"' selected='selected'>"+
                        e.placa+"("+e.modelo+")/"+var_desc_status+
                        "</option> "
                    )
                });
                $("#cb_empilhadeiras_proj_selecionado").selectpicker('val', '0');
                $("#cb_empilhadeiras_proj_selecionado").selectpicker('refresh');

            },
            error: function (request, status, error) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
          });

    }
    else if (let_nome_btn == 'btn_atualiza_reg_apont_disp_emp') {
        let let_status_apontamento = $("#cb_status_atualiza_apont_disp_emp").val();
        let let_loader_gera_disp_emp = document.getElementById("loader_gera_disp_emp");
        if (let_status_apontamento == 0){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Informe o status do apontamento !',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

        } else {
            let let_cod_apontamento = let_val_btn;
            let let_obs_apontamento = $("#txt_atualiza_obs_reg_apont_disp_emp").val();
            let let_motivo_auditoria = $("#ta_motivo_os_apont_emp").val();
            let let_data_ini_aud = $("#dt_ini_auditada_os_disp_emp").val();
            let let_data_fim_aud = $("#dt_fim_auditada_os_disp_emp").val();
            loader_gera_disp_emp.style.display = "flex";
            $.ajax({
                type: 'POST',
                data: {
                    'cod_apontamento':  let_cod_apontamento,
                    'cod_sigla_status': let_status_apontamento,
                    'obs':              let_obs_apontamento,
                    'motivo_aud':       let_motivo_auditoria,
                    'data_ini_aud':     let_data_ini_aud,
                    'data_fim_aud':     let_data_fim_aud
                },
                url: '/frota_disponibilidade_empilhadeira_app/atualiza_dados_apontamento_os_vinculada',
                dataType: 'json',
                success: function(dados){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    loader_gera_disp_emp.style.display = "none";
                }, error: function(request, status, error){
                    loader_gera_disp_emp.style.display = "none";
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });


        }
    }
    else if (let_nome_btn == 'btn_importa_arquivo_disp_frota_emp') {
        $(this).prop("disabled", true);
        $("#btn_importa_arquivo_disp_frota_emp").prop("disabled", true);
        let let_form_data = new FormData();
        let_form_data.append("file", $('input[type=file]')[0].files[0]);
        let let_loader_gera_disp_emp = document.getElementById("loader_gera_disp_emp");
        let_loader_gera_disp_emp.style.display = "flex";
        $.ajax({
              type: 'POST',
              enctype: "multipart/form-data; charset=utf-8",
              url: "/frota_disponibilidade_empilhadeira_app/importa_arquivo_apontamento_promax_empilhadeira",
              data: let_form_data,
              dataType: 'json',
              processData: false,
              contentType: false,
              cache: false,
              success: function(dados){
                if ( dados.lista_apontamentos_promax.length > 0) {
                    if (dados.lista_apontamentos_promax[0].data == null ) {
                        $.gritter.add({
                            title: 'Atenção!',
                            text: dados.msg,
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                        $("#div_conteudo_importado_disp_frota").html("");
                        $("#div_conteudo_importado_disp_frotas").html(dados.lista_apontamentos_promax[0].status_leitura_importacao);
                    } else {
                        let let_lista_lanc_apont_promax = [];
                        for (let i = 0; i < dados.lista_apontamentos_promax.length; i++) {
                            let let_img_status_imp_registro = '';
                            if (dados.lista_apontamentos_promax[i].status_leitura_importacao == 'I'){
                                let_img_status_imp_registro = "<span class='s7-check' title='Importado!'></span";
                            } else if (dados.lista_apontamentos_promax[i].status_leitura_importacao == 'A'){
                                let_img_status_imp_registro = "<span class='s7-refresh' title='Atualizado!'></span";
                            } else {
                                let_img_status_imp_registro = "<span class='s7-info' title='"+dados.lista_apontamentos_promax[i].status_leitura_importacao+"'></span";
                            }

                            let let_desc_turno = '';
                            if(dados.lista_apontamentos_promax[i].turno == 'M'){
                                let_desc_turno = 'Manhã';
                            } else if(dados.lista_apontamentos_promax[i].turno == 'T'){
                                let_desc_turno = 'Tade';
                            } else if(dados.lista_apontamentos_promax[i].turno == 'N'){
                                let_desc_turno = 'Noite';
                            }

                            let let_registro_lanc = [
                                `<i class="fa-solid fa-caret-right" style="color: #f46424;"></i>`,
                                dados.lista_apontamentos_promax[i].data,
                                dados.lista_apontamentos_promax[i].turno,
                                dados.lista_apontamentos_promax[i].placa,
                                dados.lista_apontamentos_promax[i].num_os,
                                dados.lista_apontamentos_promax[i].justificativa,
                                dados.lista_apontamentos_promax[i].sigla,
                                dados.lista_apontamentos_promax[i].projeto,
                                let_img_status_imp_registro
                            ];
                            let_lista_lanc_apont_promax.push(let_registro_lanc);
                        }
                        let let_indica_dados_tab = $("#hd_indica_conteudo_tabela_apontamento_indisp_emp").val();
                        if (let_indica_dados_tab == 1 ) {
                            let let_table =
                                `<table id="tab_conteudo_arquivo_importado_apont_promax"  class="display"  style="width:100%">
                                </table>`;
                            $("#div_conteudo_importado_disp_frota").html("");
                            $("#div_conteudo_importado_disp_frota").html(let_table);
                        }
                        $('#tab_conteudo_arquivo_importado_apont_promax').DataTable( {
                            "bJQueryUI": true,
                            "destroy": true,
                            "fixedHeader": true,
                            "scrollY": "770px",
                            "scrollX": true,
                            "scrollCollapse": true,
                            "paging": true,
                            "pageLength": 7,
                            "dom": 'Bfrtip',
                            "searching": true,
                            "buttons": [
                                'copyHtml5'
                            ],
                            "data":let_lista_lanc_apont_promax,
                                "columns": [
                                        { title: "" },
                                        { title: "Data" },
                                        { title: "Turno" },
                                        { title: "Placa" },
                                        { title: "Nº OS" },
                                        { title: "Justificativa" },
                                        { title: "Sigla" },
                                        { title: "Projeto" },
                                        { title: "Importado ?" }
                                    ],
                                "oLanguage": {
                                    "sProcessing":   "Processando...",
                                    "sLengthMenu":   "Mostrar _MENU_ registros",
                                    "sZeroRecords":  "Não foram encontrados resultados",
                                    "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                                    "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
                                    "sInfoFiltered": "",
                                    "sInfoPostFix":  "",
                                    "sSearch":       "Pesquisar:",
                                    "sUrl":          "",
                                    "oPaginate": {
                                        "sFirst":    "Primeiro",
                                        "sPrevious": "Anterior",
                                        "sNext":     "Proximo",
                                        "sLast":     "Último"
                                    },
                                    "buttons":{
                                        "copyTitle": 'Dados Copiados',
                                        "copySuccess": {
                                            _: '%d linhas copiadas',
                                            1: '1 linha copiada'
                                        }
                                    }
                                }
                        });
                        $("#hd_indica_conteudo_tabela_apontamento_indisp_emp").val(1);
                    }
                    let_loader_gera_disp_emp.style.display = "none";

                } else {

                    $.gritter.add({
                        title: 'Atenção!',
                        text: 'Arquivo vazio. Verifique!',
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    $("#hd_indica_conteudo_tabela_apontamento_indisp_emp").val(0);
                    let_loader_gera_disp_emp.style.display = "none";
                }
              },
              error: function (request, status, error) {
                let_loader_gera_disp_emp.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
              }
         });
    }

});

//PS.: O cod do projeto tem q ser o handle do Benner, passar periodo já no formato MM/YYYY
function povoa_tabela_apontamento_disp_emp(handle_proj, periodo){
    let let_loader_gera_disp_emp = document.getElementById("loader_gera_disp_emp");
    let_loader_gera_disp_emp.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/frota_disponibilidade_empilhadeira_app/pesq_dados_indisp_emp',
        data: {
            'handle_proj'  :   handle_proj,
            'periodo'   :   periodo
        },
        success: function (data){
            let let_lista_apontamentos = [];
            data.lista_apontamentos_tabela_form.forEach( reg => {
                let let_button_visualizar_os_apontamento = `
                    <button type="button" name="btn_show_detalhes_apont_emp"
                        id="btn_show_detalhes_apont_emp_${reg.cod_apontamento_disp_emp}"
                        class="btn btn-rounded btn-space"
                        value="${reg.cod_apontamento_disp_emp}" title="Edita Apontamento">
                        <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                    </button>
                `;

                let let_button_pesquisa_os_benner = `
                    <button type="button" name="btn_pesquisa_os_benner"
                        id="btn_pesquisa_os_benner_${reg.cod_apontamento_disp_emp}"
                        class="btn btn-rounded btn-space"
                        value="${reg.cod_apontamento_disp_emp}"
                        title="Vincula OS">
                        <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                    </button>
                `;

                let let_data_dia = reg.dia.split('-')[2]+"-"+
                    reg.dia.split('-')[1]+"-"+
                    reg.dia.split('-')[0];

                let let_dia_semana_num = reg.dia_semana_num;
                let let_dia_semana_string = '';
                if (let_dia_semana_num == 1) {
                    let_dia_semana_string = 'seg';
                } else if (let_dia_semana_num == 2) {
                    let_dia_semana_string = 'ter';
                } else if (let_dia_semana_num == 3) {
                    let_dia_semana_string = 'qua';
                } else if (let_dia_semana_num == 4) {
                    let_dia_semana_string = 'qui';
                } else if (let_dia_semana_num == 5) {
                    let_dia_semana_string = 'sex';
                } else if (let_dia_semana_num == 6) {
                    let_dia_semana_string = 'sáb';
                } else if (let_dia_semana_num == 7) {
                    let_dia_semana_string = 'dom';
                }

                let let_desc_turno = ''
                if (reg.turno == 'M') {
                    let_desc_turno = 'Manhã';
                } else if (reg.turno == 'T') {
                    let_desc_turno = 'Tarde';
                } if (reg.turno == 'N') {
                    let_desc_turno = 'Noite';
                }

                let let_status_os_vinculada = "<span style='background:#B0E0E6'>Não Precisa</span>";
                if (reg.os_vinculada == 'ok'){
                    let_status_os_vinculada = "<span style='background:#32CD32'>Vinculada</span>";
                } else if(reg.os_vinculada == 'nok'){
                    let_status_os_vinculada = "<span style='background:#FF0000;color:#FFFFFF'>Vincular</span>";
                }
                let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                `;

                let let_reg_apontamento = [
                    let_img,
                    let_data_dia,
                    let_dia_semana_string,
                    let_desc_turno+"<br/>("+reg.hora_turno+")",
                    reg.placa,
                    reg.status_sigla,
                    reg.qtd_os_benner,
                    reg.qtd_os_vinculada,
                    reg.horas_paradas,
                    let_button_pesquisa_os_benner,
                    let_button_visualizar_os_apontamento,
                    let_status_os_vinculada
                ];
                let_lista_apontamentos.push(let_reg_apontamento);
            });
            $("#tab_lanc_apontamento_indisp_emp").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 7,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_apontamentos,
                "columns": [
                    { title: "" },
                    { title: "Dia" },
                    { title: "Dia semana"},
                    { title: "Turno" },
                    { title: "Placa" },
                    { title: "Status/Sigla" },
                    { title: "Qtd. OS no Benner" },
                    { title: "Qtd. OS Vinculada" },
                    { title: "Paradas(DD:HH:MM)" },
                    { title: "Vincular OS" },
                    { title: "Editar" },
                    { title: "Vincular OS ?" }
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "Mostrar _MENU_ registros",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                    "sInfoEmpty":    "Mostrando de 0 até 0 de 0 registros",
                    "sInfoFiltered": "",
                    "sInfoPostFix":  "",
                    "sSearch":       "Pesquisar:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "Primeiro",
                        "sPrevious": "Anterior",
                        "sNext":     "Proximo",
                        "sLast":     "Último"
                    },
                    "buttons":{
                        "copyTitle": 'Dados Copiados',
                        "copySuccess": {
                            _: '%d linhas copiadas',
                            1: '1 linha copiada'
                        }
                    }
                }
            });
            let_loader_gera_disp_emp.style.display = "none";
        }, error: function(request, status, error) {
            let_loader_gera_disp_emp.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });


}



function povoa_tabela_os_benner(cod_apontamento){
    let let_loader_gera_disp_emp = document.getElementById("loader_gera_disp_emp");
    let_loader_gera_disp_emp.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/frota_disponibilidade_empilhadeira_app/retorna_os_da_placa_do_turno_do_apondamento_selecionado/'+cod_apontamento,
        dataType: 'json',
        success: function(dados){
            $("#hd_cod_apont_emp").val(dados.dic_obj_apont_disp_emp.cod_apontamento);
            let let_data_apontamento = dados.dic_obj_apont_disp_emp.data_apontamento.split('-')[2]+"/"+
                    dados.dic_obj_apont_disp_emp.data_apontamento.split('-')[1]+"/"+
                    dados.dic_obj_apont_disp_emp.data_apontamento.split('-')[0];

            let let_desc_turno = '';
            if( dados.dic_obj_apont_disp_emp.turno == 'M' ) {
                let_desc_turno = 'Manhã';
            } else if( dados.dic_obj_apont_disp_emp.turno == 'T' ) {
                let_desc_turno = 'Tarde';
            } else if( dados.dic_obj_apont_disp_emp.turno == 'N' ) {
                let_desc_turno = 'Noite';
            }

            let let_ativo_benner = 'Sim';
            if ( dados.dic_obj_apont_disp_emp.ativo_emp == 'N' ) {
                let_ativo_benner = 'Não';
            }

            let let_info_apont =  `
                <div style="border-radius: 10px;background-color:#ffffff;box-shadow: 10px 10px 5px -3px rgba(0,0,0,0.75);padding-top: 1rem;padding-left: 1rem;padding-bottom: 1rem;padding-right: 1rem;">
                <span style="color:#000000;">
                <strong>Dados Apontamento do dia </strong> `+ let_data_apontamento +
                `<strong> Turno : </strong>`+ let_desc_turno +
                `<br/><strong>Placa: </strong> ` + dados.dic_obj_apont_disp_emp.placa_emp +`
                <strong> Modelo: </strong> `+ dados.dic_obj_apont_disp_emp.modelo_emp +` <strong> Ano: </strong> `+ dados.dic_obj_apont_disp_emp.ano_emp +`
                <br/><strong>Ativo no Benner ?: </strong> `+ let_ativo_benner +
                `</span></div>`
            ;
            $("#div_dados_header_modal_os_benner_vincular_apontamento").html(let_info_apont);


            let let_lista_os_benner = [];
            dados.lista_os_benner.forEach( os => {


                let let_comp_data_ini_os =
                `<input type="datetime-local" id="dt_ini_os_disp_emp" style="width: 140px;"
                       name="dt_ini_os_disp_emp" value="${os.data_ini}" readonly="readonly">
                `;
                let let_comp_data_fim_os =
                `<input type="datetime-local" id="dt_fim_os_disp_emp" style="width: 140px;"
                       name="dt_fim_os_disp_emp" value="${os.data_fim}" readonly="readonly">
                `;



                let let_button_vincular_reg_os_apont_emp = `
                <button type="button" name="btn_vincular_os_apont_emp"
                    id="btn_vincular_os_apont_emp${os.handle}" class="'btn btn-rounded btn-space"
                    value="${os.handle}" title="Vincula OS">
                    <i class="fa-solid fa-paperclip" style="color: #f46424;"></i>
                    </button>
                `;
                if(os.vinculada == 'S'){
                    let_button_vincular_reg_os_apont_emp = "<span style='background:#32CD32'>Vinculada</span>";
                }

                let let_desc_grupo = os.desc_conjunto;
                if ( os.desc_conjunto == null){
                    let_desc_grupo = '';
                }

                let let_reg_os = [
                    "<span class='s7-ribbon'></span>",
                    os.numero +
                    "<input type='hidden' id='hd_numero_os_benner"+os.handle+"' name='hd_numero_os_benner' value='"+os.numero+"'>",
                    os.desc_tipo +
                    "<input type='hidden' id='hd_handle_tipo_os_benner"+os.handle+"' name='hd_handle_tipo_os_benner' value='"+os.handle_tipo+"'>"+
                    "<input type='hidden' id='hd_desc_tipo_os_benner"+os.handle+"' name='hd_desc_tipo_os_benner' value='"+os.desc_tipo+"'>",
                    let_comp_data_ini_os +
                    "<input type='hidden' id='hd_data_ini_os_benner"+os.handle+"' name='hd_data_ini_os_benner' value='"+os.data_ini+"'>",
                    let_comp_data_fim_os +
                    "<input type='hidden' id='hd_data_fim_os_benner"+os.handle+"' name='hd_data_fim_os_benner' value='"+os.data_fim+"'>",
                    os.desc_os +
                    "<input type='hidden' id='hd_desc_os_benner"+os.handle+"' name='hd_desc_os_benner' value='"+os.desc_os+"'>",
                    let_desc_grupo +
                    "<input type='hidden' id='hd_handle_conj_os_benner"+os.handle+"' name='hd_handle_conj_os_benner' value='"+os.handle_conjunto+"'>" +
                    "<input type='hidden' id='hd_desc_conj_os_benner"+os.handle+"' name='hd_desc_conj_os_benner' value='"+os.desc_conjunto+"'>",
                    let_button_vincular_reg_os_apont_emp
                ];
                let_lista_os_benner.push(let_reg_os);
            });
            $("#tab_os_benner_para_vincular_ao_apontamento").DataTable( {
                "bJQueryUI": true,
                "pageLength": 4,
                "destroy": true,
                "fixedHeader": {
                    header: true,
                    footer: false
                },
                "searching": false,
                "data":let_lista_os_benner,
                "columns": [
                    { title: "" },
                    { title: "Núm. OS" },
                    { title: "Tipo" },
                    { title: "Data Ini." },
                    { title: "Data Fim" },
                    { title: "Desc. OS" },
                    { title: "Grupo" },
                    { title: "Vincular" }
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "",
                    "sInfoEmpty":    "",
                    "sInfoFiltered": "",
                    "sInfoPostFix":  "",
                    "sSearch":       "Pesquisar:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "",
                        "sPrevious": "",
                        "sNext":     "",
                        "sLast":     ""
                    }
                }
            });

            let_loader_gera_disp_emp.style.display = "none";
            $("#modal_os_benner_vincular_apontamento").show();

        },
        error: function(request, status, error) {
            let_loader_gera_disp_emp.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

}


function povoa_tabela_os_apontamento(cod_apontamento){
    let let_loader_gera_disp_emp = document.getElementById("loader_gera_disp_emp");
    let_loader_gera_disp_emp.style.display = "flex";
    $.ajax({
        type: 'GET',
        data: {
            'cod_apontamento'   :   cod_apontamento
        },
        url: '/frota_disponibilidade_empilhadeira_app/retorna_reg_apont_disp_emp',
        success: function(dados){
            $("#tab_os_apontamento_indisp_emp").DataTable().clear().draw();
            $("#hd_cod_apontamento").val(cod_apontamento);
            let let_data_apontamento = dados.dic_obj_apont_disp_emp.data_apontamento.split('-')[2]+"/"+
                dados.dic_obj_apont_disp_emp.data_apontamento.split('-')[1]+"/"+
                dados.dic_obj_apont_disp_emp.data_apontamento.split('-')[0];
            $("#lbl_data_apont_disp_emp").val(dados.dic_obj_apont_disp_emp.data_apontamento);

            let let_desc_turno = '';
            if( dados.dic_obj_apont_disp_emp.turno == 'M' ) {
                let_desc_turno = 'Manhã';
            } else if( dados.dic_obj_apont_disp_emp.turno == 'T' ) {
                let_desc_turno = 'Tarde';
            } else if( dados.dic_obj_apont_disp_emp.turno == 'N' ) {
                let_desc_turno = 'Noite';
            }
            let let_status_benner = 'Sim';
            if(dados.dic_obj_apont_disp_emp.ativo_emp == 'N'){
                let_status_benner = 'Não';
            }
            let let_info_apont =  `
                <div style="border-radius: 10px;background-color:#ffffff;box-shadow: 10px 10px 5px -3px rgba(0,0,0,0.75);padding-top: 1rem;padding-left: 1rem;padding-bottom: 1rem;">
                <span style="color: #000000;">
                <strong>Dados Apontamento do dia </strong> : `+ let_data_apontamento + `  <strong> Turno : </strong> da `+ let_desc_turno +`<br/>
                <strong>Placa: </strong> ` + dados.dic_obj_apont_disp_emp.placa_emp +`
                 <strong>Modelo: </strong> `+ dados.dic_obj_apont_disp_emp.modelo_emp +`  <strong>Ano: </strong> `+ dados.dic_obj_apont_disp_emp.ano_emp +`
                <br/><strong>Ativo no Benner ?: </strong> `+ let_status_benner +
                `</span></div>`
            ;
            $("#div_dados_header_apont_selecionado").html(let_info_apont);

            $("#cb_status_atualiza_apont_disp_emp option").remove();
            $("#cb_status_atualiza_apont_disp_emp").append("<option value='0'>Informe o Status do Apontamento</option>");
            dados.lista_siglas.forEach( status => {
                $("#cb_status_atualiza_apont_disp_emp").append("<option value='"+status.cod_sigla+"'>"+status.sigla+
                    "-"+status.desc_sigla+"</option>");
            });
            $("#cb_status_atualiza_apont_disp_emp").val(dados.dic_obj_apont_disp_emp.cod_sigla);
            $("#cb_status_atualiza_apont_disp_emp").selectpicker('refresh');


            $("#txt_atualiza_obs_reg_apont_disp_emp").val(dados.dic_obj_apont_disp_emp.obs);

            let let_lista_os = [];
            dados.obj_os_apontamento.forEach( os => {
                let let_desc_tipo_os = '';
                if(os.tipo_os_benner == '1'){
                    let_desc_tipo_os = 'PREVENTIVA';
                } else if(os.tipo_os_benner == '22'){
                    let_desc_tipo_os = 'CORRETIVA';
                }

                let let_comp_data_ini_os =
                `<input type="datetime-local" id="dt_ini_os_disp_emp" class="form-control"
                       name="dt_ini_os_disp_emp" value="${os.data_inicial_os_benner}" readonly="readonly">
                `;
                let let_comp_data_fim_os =
                `<input type="datetime-local" id="dt_fim_os_disp_emp" class="form-control"
                       name="dt_fim_os_disp_emp" value="${os.data_final_os_benner}" readonly="readonly">
                `;

                let let_comp_txt_motivo =
                `<textarea class="form-control" id="ta_motivo_os_apont_emp" name="ta_motivo_os_apont_emp"
                        autocomplete="off"rows="3" cols="20"
                        style="padding-left: 5px;padding-right: 5px;height: 60px;width: 261.6px;">
                        ${os.motivo}
                        </textarea>
                `;

                let let_comp_data_ini_auditada_os_apont_emp =
                `<input type="datetime-local" id="dt_ini_auditada_os_disp_emp"
                       name="dt_ini_auditada_os_disp_emp" value="${os.parada_ini_aud}">
                `;


                let let_comp_data_fim_auditada_os_apont_emp =
                `<input type="datetime-local" id="dt_fim_auditada_os_disp_emp"
                       name="dt_fim_auditada_os_disp_emp" value="${os.parada_fim_aud}">
                `;


                let let_button_excluir_reg_os_apont_emp = `
                <button type="button" name="btn_excluir_os_apont_emp"
                    id="btn_excluir_os_apont_emp${os.cod_os_apontamento_disp_emp}"
                    class="btn btn-rounded btn-space"
                    value="${os.cod_os_apontamento_disp_emp}">
                    <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                </button>
                `;



                let let_reg_os = [
                    os.num_os_benner,
                    let_desc_tipo_os,
                    os.data_inicial_os_benner,
                    os.data_final_os_benner,
                    os.desc_os_benner,
                    os.desc_conj_manut_benner,
                    let_comp_txt_motivo,
                    let_comp_data_ini_auditada_os_apont_emp,
                    let_comp_data_fim_auditada_os_apont_emp,
                    let_button_excluir_reg_os_apont_emp
                ];
                let_lista_os.push(let_reg_os);
            });
            $("#tab_os_apontamento_indisp_emp").DataTable( {
                "bJQueryUI": true,
                "pageLength": 4,
                "destroy": true,
                "fixedHeader": {
                    header: true,
                    footer: false
                },
                "searching": false,
                "data":let_lista_os,
                "columns": [
                    { title: "Núm. OS" },
                    { title: "Tipo" },
                    { title: "Data Ini." },
                    { title: "Data Fim" },
                    { title: "Desc. OS" },
                    { title: "Grupo" },
                    { title: "Motivo" },
                    { title: "Data Ini. Auditada" },
                    { title: "Data Fim Auditada" },
                    { title: "Excluir" }
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "",
                    "sInfoEmpty":    "",
                    "sInfoFiltered": "",
                    "sInfoPostFix":  "",
                    "sSearch":       "Pesquisar:",
                    "sUrl":          "",
                    "oPaginate": {
                        "sFirst":    "",
                        "sPrevious": "",
                        "sNext":     "",
                        "sLast":     ""
                    }
                }
            });

            $("#btn_atualiza_reg_apont_disp_emp").val(dados.dic_obj_apont_disp_emp.cod_apontamento);
            $("#modal_atualiza_apont_disp_emp").show();
            let_loader_gera_disp_emp.style.display = "none";
        },
        error: function(request, status, error) {
            let_loader_gera_disp_emp.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: error,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

}