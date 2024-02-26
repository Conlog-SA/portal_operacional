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

$(document).on('change', '#cb_responsaveis_contas', function(){
    atualiza_tab_resp_contas();
});

$(document).on('change','input', function(){
	let let_nome_inp = $(this).attr('name');
    let let_id_inp = $(this).attr('id');
    let let_chk_inp = $(this).prop('checked')

    if(let_nome_inp == "dt_data_fim_resp_conta"){
        $.ajax({
        type: 'POST',
        url: '/contabil_composicao_app/informa_data_fim_resp_conta',
        data: {
            'cod_resp_conta'    :   let_id_inp.split('_')[5],
            'data_fim'          :   $(this).val()
        },
        dataType: 'json',
        success: function (dados) {
            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

            let_loader_frm_vincula_resp_contas.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_frm_vincula_resp_contas.style.display = "none";
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


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_abre_modal_exclui_reg_resp_conta") {
        $("#btn_confirma_exclusao_reg_resp_conta").val(let_val_btn);
        $("#modal_exclui_reg_resp_conta").show();
    } else if (let_nome_btn == "btn_fecha_modal_exclui_reg_resp_conta") {
        $("#modal_exclui_reg_resp_conta").hide();
    } else if ( let_nome_btn == 'btn_confirma_exclusao_reg_resp_conta') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_reg_resp_conta/'+let_val_btn,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_reg_resp_conta").hide();
                if( $("#cb_responsaveis_contas").val() != '' ){
                    atualiza_tab_resp_contas();
                }else if ( $("#sl_pacs_vincula_resp").val().toString() != '' ){
                    atualiza_contas_x_resp_vinculadas();
                }

            },
            error: function(request, status, error){
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
    else if(let_nome_btn == 'btn_associa_contas_resp_frm_vincula_conta_resp'){
        let let_lista_cod_contas = $("#sl_contas_vincula_resp").val().toString();
        let let_resp_comp = $("#sl_resp_comp_contas_vincula_resp").val();
        let let_resp_val = $("#sl_resp_val_contas_vincula_resp").val();
        let let_ini_atv = $("#dt_ini_contas_vincula_resp").val();
        let let_fim_atv = $("#dt_fim_contas_vincula_resp").val();
        $.ajax({
            type: 'POST',
            data:{
                'tipo_transacao'     :   'L',
                'lista_cod_contas'  :   let_lista_cod_contas,
                'nome_resp_comp'    :   let_resp_comp,
                'nome_resp_val'     :   let_resp_val,
                'ini_atv'           :   let_ini_atv,
                'fim_atv'           :   let_fim_atv
            },
            url: '/contabil_composicao_app/associa_resp_conta',
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_contas_x_resp_vinculadas();
            },
            error: function(request, status, error){
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    } else if (let_nome_btn == 'btn_desmarcar_contas_vincula_resp'){
        $("#sl_contas_vincula_resp").selectpicker('deselectAll');
    }
    else if (let_nome_btn == 'btn_marcar_contas_vincula_resp'){
        $("#sl_contas_vincula_resp").selectpicker('selectAll');
    }


});


$(document).on('change', '#sl_pacs_vincula_resp', function(){
    atualiza_contas_x_resp_vinculadas();
    atualiza_comp_sl_contas_vincula_resp();

});


function atualiza_tab_resp_contas(){
    let let_loader_frm_contas_responsaveis = document.getElementById("loader_frm_contas_responsaveis");
    let_loader_frm_contas_responsaveis.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/retorna_contas_responsaveis_selecionados',
        data: {
            'lista_cod_usuario'   :   $("#cb_responsaveis_contas").val().toString()
        },
        dataType: 'json',
        success: function (dados) {
            let let_lista_reg = [];
            dados.dic_lista_contas_resp.forEach(reg => {
                let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";

                let let_input_data_fim = `
                    <input type="date" id="dt_data_fim_resp_conta_${reg.cod_resp_conta}"
                           name="dt_data_fim_resp_conta"
                           value="${reg.data_fim_atividade}">
                `;

                let let_btn_exclui_reg_resp_conta = `
                    <button type='button' name='btn_abre_modal_exclui_reg_resp_conta'
                    id='btn_abre_modal_exclui_reg_resp_conta_${reg.cod_resp_conta}' value="${reg.cod_resp_conta}"
                    class='btn btn-rounded btn-space' title="Excluí registro">
                    <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                    </button>
                `;

                let row = [
                    let_img,
                    reg.cod_conta__cod_pacote_conta__desc_pacote_conta,
                    reg.cod_conta__desc_conta,
                    reg.resp_composicao,
                    reg.resp_validacao,
                    reg.data_ini_atividade,
                    let_input_data_fim,
                    let_btn_exclui_reg_resp_conta
                ];
                let_lista_reg.push(row);
            });

            $("#tab_resp_vinculados").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
                "destroy": true,
                "searching": false,
                "paging": true,
                "data":let_lista_reg,
                "columns": [
                    { title: "" },
                    { title: "Pacote" },
                    { title: "Conta" },
                    { title: "Resp. composição" },
                    { title: "Resp. validação" },
                    { title: "Início" },
                    { title: "Fim" },
                    { title: "Excluir" }
                ],
                "columnDefs": [
                    {"className": "dt-right", "targets": [3,4]},
                    {"className": "dt-center", "targets": [3,4]},
                    {"className": "dt-left", "targets": [0,1,2,5,6]}
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "",
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

            let_loader_frm_contas_responsaveis.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_frm_contas_responsaveis.style.display = "none";
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

function atualiza_contas_x_resp_vinculadas(){
    let let_loader_frm_vincular_contas_resp = document.getElementById("loader_frm_vincular_contas_resp");
    let_loader_frm_vincular_contas_resp.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/retorna_contas_por_pac_e_regs_resp_contas',
        data: {
            'tipo_transacao'    :   'retorna_dados_contas_resp',
            'cod_pacote'        :  $("#sl_pacs_vincula_resp").val()
        },
        dataType: 'json',
        success: function (dados) {
            let let_lista_reg = [];
            dados.lista_resp_contas.forEach(reg => {
                let let_desc_conta = ''
                if(reg.cod_conta__tipo_modelo == 1) {
                    let_desc_conta = reg.cod_conta__cod_conta+ " - " +
                        reg.cod_conta__desc_conta+" - Cód. red. CP - "+
                        reg.cod_conta__cod_red_conta_contabil_cp;


                } else if(reg.cod_conta__tipo_modelo == 3) {
                    let_desc_conta = reg.cod_conta__cod_conta+ " - " +
                        reg.cod_conta__desc_conta+" - Cód. red. CP - "+
                        reg.cod_conta__cod_red_conta_contabil_cp+
                        " Cód. red. LP - "+reg.cod_conta__cod_red_conta_contabil_lp;
                }

                let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";

                let let_input_data_fim = `
                    <input type="date" id="dt_data_fim_resp_conta_${reg.cod_resp_conta}"
                           name="dt_data_fim_resp_conta"
                           value="${reg.data_fim_atividade}">
                `;

                let let_btn_exclui_reg_resp_conta = `
                    <button type='button' name='btn_abre_modal_exclui_reg_resp_conta'
                    id='btn_abre_modal_exclui_reg_resp_conta_${reg.cod_resp_conta}' value="${reg.cod_resp_conta}"
                    class='btn btn-rounded btn-space' title="Excluí registro">
                    <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                    </button>
                `;

                let row = [
                    let_img,
                    let_desc_conta,
                    reg.resp_composicao,
                    reg.resp_validacao,
                    reg.data_ini_atividade,
                    let_input_data_fim,
                    let_btn_exclui_reg_resp_conta
                ];
                let_lista_reg.push(row);



            });
            $("#tab_contas_x_resp_vinculadas").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
                "destroy": true,
                "searching": false,
                "paging": true,
                "data":let_lista_reg,
                "columns": [
                    { title: "" },
                    { title: "Conta" },
                    { title: "Resp. composição" },
                    { title: "Resp. validação" },
                    { title: "Início" },
                    { title: "Fim" },
                    { title: "Excluir" }
                ],
                "columnDefs": [
                    {"className": "dt-right", "targets": [2,3,4,5]},
                    {"className": "dt-center", "targets": [6]},
                    {"className": "dt-left", "targets": [0,1]}
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "",
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

            let_loader_frm_vincular_contas_resp.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_frm_vincular_contas_resp.style.display = "none";
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

function atualiza_comp_sl_contas_vincula_resp(){
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/retorna_contas_por_pac_e_regs_resp_contas',
        data: {
            'tipo_transacao'    :   'retorna_lista_contas',
            'cod_pacote'        :  $("#sl_pacs_vincula_resp").val()
        },
        dataType: 'json',
        success: function (dados) {
            $("#sl_contas_vincula_resp option").remove();
            dados.lista_contas_pac.forEach(reg => {
                let let_desc_conta = ''
                if(reg.tipo_modelo == 1) {
                    let_desc_conta = reg.cod_conta+ " - " +
                        reg.desc_conta+" - Cód. red. CP - "+
                        reg.cod_red_conta_contabil_cp;

                } else if(reg.tipo_modelo == 3) {
                    let_desc_conta = regcod_conta+ " - " +
                        reg.desc_conta+" - Cód. red. CP - "+
                        reg.cod_red_conta_contabil_cp+
                        " Cód. red. LP - "+reg.cod_red_conta_contabil_lp;

                }
                $("#sl_contas_vincula_resp").append("<option value='"+
                    reg.cod_conta+"'>"+let_desc_conta+"</option>");
            });
            $("#sl_contas_vincula_resp").selectpicker('refresh');

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

