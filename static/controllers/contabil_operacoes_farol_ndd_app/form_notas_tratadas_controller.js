var var_lista_notas = [];

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


$(document).ready(function(){
    let loader_frm_op_ndd = document.getElementById("loader_frm_op_ndd");

    $("#tab_excecoes_operacao").DataTable( {
        "bJQueryUI": true,
        "destroy": true,
        "fixedHeader": true,
        "scrollY": "770px",
        "scrollX": true,
        "scrollCollapse": true,
        "paging": true,
        "pageLength": 7,
        "searching": true,
        "dom": 'Bfrtip',
        "buttons": [
            'copyHtml5'
        ],
        "columnDefs": [
            {"className": "dt-center", "targets": [2]},
            {"className": "dt-left", "targets": [0, 1]}
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

});


$(document).on('change', 'input', function(){
    var nomeDoInput = $(this).attr('name');
    var idDoInput = $(this).attr('id');
    var valInput = $(this).attr('value');

    if ( nomeDoInput == 'txt_pesq_chave_nota') {
        var var_chave_nota = $(this).val();
        povoa_tab_notas_pesq_proc_nfe('0', null, null, var_chave_nota);
    }
});

$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if ( nomeDoButton == 'btn_pesq_nota') {
        var var_num_nota = $("#txt_pesq_numero_nota").val();
        var var_data_ini = $("#txt_data_ini_emissao_nota").val();
        var var_data_fim = $("#txt_data_fim_emissao_nota").val();
        povoa_tab_notas_pesq_proc_nfe(var_num_nota, var_data_ini, var_data_fim, 0);
    }
    else if ( nomeDoButton == 'btn_add_excecao' ) {
        var var_desc_operacao_excecao = $("#cb_operacoes").val().toString();
        $.ajax({
        type: 'POST',
        url: '/contabil_operacoes_farol_ndd_app/add_excecao_operacao',
        data: {
            'desc_operacao_excecao' :   var_desc_operacao_excecao
        },
        dataType: 'json',
        success: function (data) {
            $.gritter.add({
                title: 'Atenção!',
                text: data.msg,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

            povoa_tab_excecoes_operacoes();
            $("#cb_operacoes").selectpicker('val', '');
            atualiza_cd_operacoes(data.lista_benner_sem_excecao);
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
    else if ( nomeDoButton == 'btn_abre_model_excluir_excecao') {
        $("#btn_excluir_excecao_operacao").val(valButton);
        $("#modal_confirma_exclusao_excecao").show();
    }
    else if ( nomeDoButton == 'bnt_fecha_modal_confirma_exclusao_excecao') {
        $("#modal_confirma_exclusao_excecao").hide();
    }
    else if ( nomeDoButton == 'btn_excluir_excecao_operacao') {
        var var_cod_reg = valButton;
        $.ajax({
            type: 'DELETE',
            url: '/contabil_operacoes_farol_ndd_app/excluir_excecao_operacao/'+var_cod_reg,
            dataType: 'json',
            data: {
                'cod_reg'     :   var_cod_reg
            },
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                $("#modal_confirma_exclusao_excecao").hide();
                povoa_tab_excecoes_operacoes();
                atualiza_cd_operacoes(data.lista_benner_sem_excecao);
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
    else if ( nomeDoButton == 'btn_abre_modal_nova_justificativa_nota_tratada') {
        $("#hd_tipo_transacao").val('add');
        $("#txt_area_justificativa_nota_tratada").val('');
        $("#btn_confirma_justificativa_nota_tratada").val(valButton);
        $("#modal_add_justificativa_nota_tratada").show();
    }
    else if ( nomeDoButton == 'btn_abre_modal_edita_justificativa_nota_tratada') {
        $("#hd_tipo_transacao").val('update');
        $("#txt_area_justificativa_nota_tratada").val(var_lista_notas[valButton][15]);
        $("#btn_confirma_justificativa_nota_tratada").val(var_lista_notas[valButton][14]);
        $("#modal_add_justificativa_nota_tratada").show();
    }
    else if ( nomeDoButton == 'bnt_fecha_modal_add_justificativa_nota_tratada') {
        $("#modal_add_justificativa_nota_tratada").hide();
    } else if ( nomeDoButton == 'btn_confirma_justificativa_nota_tratada' ) {
        var var_tipo_transacao = $("#hd_tipo_transacao").val();
        var var_data = {};
        if(var_tipo_transacao == 'add') {
            var_data = {
                'tipo_transacao': var_tipo_transacao,
                'handle_emp': var_lista_notas[valButton][12],
                'nome_emp': var_lista_notas[valButton][1],
                'handle_fil': var_lista_notas[valButton][13],
                'nome_fil': var_lista_notas[valButton][2],
                'num_nota': var_lista_notas[valButton][3],
                'serie': var_lista_notas[valButton][4],
                'chave_nota': var_lista_notas[valButton][10],
                'natureza': var_lista_notas[valButton][7],
                'emissao': var_lista_notas[valButton][5],
                'doc_fornec': var_lista_notas[valButton][8],
                'nome_fornec': var_lista_notas[valButton][9],
                'justificativa': $("#txt_area_justificativa_nota_tratada").val()
            }
        } else if (var_tipo_transacao=='update'){
            var_data = {
                'tipo_transacao': var_tipo_transacao,
                'cod_nota_tratada': valButton,
                'justificativa': $("#txt_area_justificativa_nota_tratada").val()
            }
        }
        $.ajax({
            type: 'POST',
            url: '/contabil_operacoes_farol_ndd_app/add_update_justificativa_nota_tratada',
            dataType: 'json',
            data: var_data,
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                $("#txt_area_justificativa_nota_tratada").val();
                $("#modal_add_justificativa_nota_tratada").hide();
                var var_num_nota = $("#txt_pesq_numero_nota").val();
                var var_data_ini = $("#txt_data_ini_emissao_nota").val();
                var var_data_fim = $("#txt_data_fim_emissao_nota").val();
                povoa_tab_notas_pesq_proc_nfe(var_num_nota, var_data_ini, var_data_fim, 0);
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
    else if ( nomeDoButton == 'btn_abre_modal_exclui_justificativa_nota_tratada') {
        $("#btn_excluir_justificativa_nota_tratada").val(valButton);
        $("#modal_confirma_exclusao_justificativa").show();
    }
    else if ( nomeDoButton == 'bnt_fecha_modal_confirma_exclusao_justificativa') {
        $("#modal_confirma_exclusao_justificativa").hide();
    }
    else if (nomeDoButton == 'btn_excluir_justificativa_nota_tratada') {
        var var_cod_reg = valButton;
        $.ajax({
            type: 'DELETE',
            url: '/contabil_operacoes_farol_ndd_app/excluir_nota_tratada/'+var_cod_reg,
            dataType: 'json',
            data: {
                'cod_reg'     :   var_cod_reg
            },
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                $("#modal_confirma_exclusao_justificativa").hide();
                var var_num_nota = $("#txt_pesq_numero_nota").val();
                var var_data_ini = $("#txt_data_ini_emissao_nota").val();
                var var_data_fim = $("#txt_data_fim_emissao_nota").val();
                povoa_tab_notas_pesq_proc_nfe(var_num_nota, var_data_ini, var_data_fim, 0);
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

});

function atualiza_cd_operacoes(lista_operacoes){
    var var_cb_operacoes = document.getElementById("cb_operacoes");
    $("#cb_operacoes option").remove();
    lista_operacoes.forEach(op => {
        $("#cb_operacoes").append("<option value='"+op.desc_operacao+"'>"+op.desc_operacao+"</option>");
    });
    $("#cb_operacoes").selectpicker('refresh');

}

function povoa_tab_notas_pesq_proc_nfe(var_num_nota, var_data_ini, var_data_fim, var_chave_nota){
    loader_frm_op_ndd.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_operacoes_farol_ndd_app/pesc_nota_proc_nfe',
        data: {
            'num_nota'      :   var_num_nota,
            'data_ini'      :   var_data_ini,
            'data_fim'      :   var_data_fim,
            'chave_nota'    :   var_chave_nota
        },
        dataType: 'json',
        success: function (data) {
            $.gritter.add({
                title: 'Atenção!',
                text: data.msg,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

            var_lista_notas = [];
            for (var i = 0; i < data.lista_notas_validadas.length; i++) {
                var var_img = "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
                var var_button = `
                    <button type='button' id='btn_abre_modal_nova_justificativa_nota_tratada_${i}'
                    name='btn_abre_modal_nova_justificativa_nota_tratada' value='${i}'
                    class='btn btn-rounded btn-space'>
                    <i class="fa-solid fa-paperclip" style="color: #f46424;"></i>
                    </button>
                `;
                if (data.lista_notas_validadas[i].tratada == 'S'){
                    var_img = `
                        <button type='button' id='btn_abre_modal_exclui_justificativa_nota_tratada_${i}'
                        name='btn_abre_modal_exclui_justificativa_nota_tratada' value='${data.lista_notas_validadas[i].cod_nota_tratada}'
                        class='btn btn-rounded btn-space'
                        title='${data.lista_notas_validadas[i].justificativa}'>
                        <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                        </button>
                    `;
                    var_button = `
                        <button type='button' id='btn_abre_modal_edita_justificativa_nota_tratada_${i}'
                        name='btn_abre_modal_edita_justificativa_nota_tratada' value='${i}'
                        class='btn btn-rounded btn-space'
                        title='${data.lista_notas_validadas[i].justificativa}'>
                        <i class="fa-solid fa-paperclip" style="color: #f46424;"></i>
                        </button>
                    `;
                }


                var var_reg = [
                    /* 0 */var_img,
                    /* 1 */data.lista_notas_validadas[i].nome_empresa_nota,
                    /* 2 */data.lista_notas_validadas[i].nome_filial_nota,
                    /* 3 */data.lista_notas_validadas[i].num_nota,
                    /* 4 */data.lista_notas_validadas[i].serie_nota,
                    /* 5 */data.lista_notas_validadas[i].emissao_nota,
                    /* 6 */data.lista_notas_validadas[i].valor_nota,
                    /* 7 */data.lista_notas_validadas[i].natureza_nota,
                    /* 8 */data.lista_notas_validadas[i].doc_fornecedor_nota,
                    /* 9 */data.lista_notas_validadas[i].nome_fornec_nota,
                    /* 10 */data.lista_notas_validadas[i].chave_nota,
                    /* 11 */var_button,

                    /* 12 */data.lista_notas_validadas[i].handle_empresa_nota,
                    /* 13 */data.lista_notas_validadas[i].handle_filial_nota,
                    /* 14 */data.lista_notas_validadas[i].cod_nota_tratada,
                    /* 15 */data.lista_notas_validadas[i].justificativa
                ];
                var_lista_notas.push(var_reg);
            }
            $("#tab_notas_pesq_proc_nfe").DataTable( {
                /*"bJQueryUI": true,
                "destroy": true,
                //"fixedHeader": true,
                "scrollY": "500px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copy'
                ],*/
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":var_lista_notas,
                "columns": [
                    { title: "" },
                    { title: "Empresa" },
                    { title: "Filial" },
                    { title: "Núm. Nota" },
                    { title: "Série" },
                    { title: "Emissão" },
                    { title: "Val.(R$)" },
                    { title: "Natureza" },
                    { title: "Doc. Fornecedor" },
                    { title: "Fornecedor" },
                    { title: "Chave" },
                    { title: "Justificar" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0, 11]},
                    {"className": "dt-left", "targets": [1, 2]},
                    {"className": "dt-right", "targets": [3, 4, 5, 6, 7, 8, 9, 10]}
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

            loader_frm_op_ndd.style.display = "none";


        },
        error: function (request, status, error) {
            loader_frm_op_ndd.style.display = "none";
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

function povoa_tab_excecoes_operacoes(){
    loader_frm_op_ndd.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_operacoes_farol_ndd_app/retorna_excecoes_lancadas',
        dataType: 'json',
        success: function (data) {
            var var_lista_excecoes = [];
            data.lista_excecoes.forEach( excecao => {
            var var_button = `
                    <button type='button' id='btn_abre_model_excluir_excecao_${excecao.cod_excecao}'
                    name='btn_abre_model_excluir_excecao' value='${excecao.cod_excecao}'
                    class='btn btn-rounded btn-space'>
                    <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                    </button>
                `;
                var var_reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    excecao.desc_operacao,
                    var_button
                ];
                var_lista_excecoes.push(var_reg);
            });
            $("#tab_excecoes_operacao").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":var_lista_excecoes,
                "columns": [
                    { title: "" },
                    { title: "Natureza Operação" },
                    { title: "Excluir" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [2]},
                    {"className": "dt-left", "targets": [0, 1]}
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

            loader_frm_op_ndd.style.display = "none";


        },
        error: function (request, status, error) {
            loader_frm_op_ndd.style.display = "none";
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