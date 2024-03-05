

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




$(document).on('change', '#cb_contas', function(){
    atualiza_dados_conta_acao_cb_contas();
});

function atualiza_dados_conta_acao_cb_contas(){
    let let_cod_conta = $("#cb_contas").val();
    let cod_modelo_selecionado = 0;
        if ( $("#rd_modelo_conta_1").is(':checked') == true){
            cod_modelo_selecionado = 1;
        } else if ( $("#rd_modelo_conta_2").is(':checked') == true){
            cod_modelo_selecionado = 2;
        } else if ( $("#rd_modelo_conta_3").is(':checked') == true){
            cod_modelo_selecionado = 3;
        }
    atualiza_form_dados_conta('J', let_cod_conta);
    if(cod_modelo_selecionado == 1){
        atualiza_doc_contas_modelo_1(let_cod_conta);
    } else if(cod_modelo_selecionado == 3){
        atualiza_tab_contratos_conta(let_cod_conta);
    }
    atualiza_tabela_resp_conta(let_cod_conta);
    atualiza_tab_anexos_conta(let_cod_conta);
    atualiza_tab_status_contrato_composicao(let_cod_conta);
    /* Limpa form responsáveis */
    $("#cb_resp_composicao").val("");
    $("#cb_resp_composicao").selectpicker("refresh");
    $("#cb_resp_validacao").val("");
    $("#cb_resp_validacao").selectpicker("refresh");
    $("#dt_ini_resp").val("");
    $("#dt_fim_resp").val("");
    let let_img_btn_atualizar_dados_resp = `
        <i class="fa-solid fa-plus" ></i>
    `;
    $("#btn_associar_responsaveis_conta").html(let_img_btn_atualizar_dados_resp + "Associar responsáveis");
    $("#btn_associar_responsaveis_conta").val(0);
    /* Limpa form anexos */
    $("#file_anexo_contrato").val("");
    $("#div_visualizacao_anexo_conta").html("");
}

/*
$(document).on('change', '#cb_pacote_conta', function(){
    let let_cod_conta = $("#btn_cadastra_nova_conta").val();
    let let_cod_pacote_conta = $(this).val();
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/acessa_form_doc_contas_modelo_1',
        data: {
            'cod_pacote_conta'   :   let_cod_pacote_conta,
            'cod_conta'          :   let_cod_conta
        },
        dataType: 'json',
        success: function (dados) {

            let let_table_layout_contas_mod_1 = $("<table/>");
            let_table_layout_contas_mod_1.attr({
            id: 'tab_doc_contas_modelo_1',
                class: 'display wrap w-100 cl_tab_principal_pagina'
            });

            let let_thead = $("<thead/>");
            let let_tr = $("<tr/>");

            dados.lista_campos_layout_tab.forEach( camp => {
                let let_th = $("<th/>");
                let_th.attr({
                    scope: 'col'
                });
                let_th.html(camp.cod_campo__desc_campo);
                let_tr.append(let_th);
            });
            let_thead.append(let_tr)
            let_table_layout_contas_mod_1.append(let_thead);

            let let_body = $("<body/>");
            let_table_layout_contas_mod_1.append(let_body)

            $("#div_tab_doc_contas_modelo_1").append(let_table_layout_contas_mod_1);
            $("#tab_doc_contas_modelo_1").DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "50vh", //770px
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                //"pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
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
                } );



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
});
*/

$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_cadastra_nova_conta") {
        let let_cod_conta = let_val_btn;
        let let_transacao = 'N';
        if (let_cod_conta != '0'){
            let_transacao = 'U';
        }

        let let_desc_contra = $("#txt_desc_conta").val();

        let let_handle_conta_cp = $("#tx_handle_conta_cp").val();
        let let_cod_red_conta_cp = $("#txt_cod_red_conta_cp").val();
        let let_estrut_cp = $("#txt_cod_estrutura_cp").val();

        let let_handle_conta_lp = 0;
        let let_cod_red_conta_lp = 0;
        let let_estrut_lp = 0;

        let let_cod_pacote_conta = $("#cb_pacote_conta").val();
        let let_radio1 = $("#rd_modelo_conta_1").prop('checked');
        let let_radio2 = $("#rd_modelo_conta_2").prop('checked');
        let let_radio3 = $("#rd_modelo_conta_3").prop('checked');
        let let_cod_modelo_conta = '';
        if ( let_radio1 == true ){
            let_cod_modelo_conta = 1;
        } else if ( let_radio2 == true ){
            let_cod_modelo_conta = 2;
        } else if ( let_radio3 == true ){
            let_cod_modelo_conta = 3;
            let_handle_conta_lp = $("#tx_handle_conta_lp").val();
            let_cod_red_conta_lp = $("#txt_cod_red_conta_lp").val();
            let_estrut_lp = $("#txt_cod_estrutura_lp").val();
        }

        let let_ini_atv_conta = $("#dt_ini_atv_benner").val();
        let let_fim_atv_conta = $("#dt_fim_atv_benner").val();
        let let_status_conta_comp = 'A';
        if($("#chk_status_comp").prop('checked') == false){
            let_status_conta_comp = 'I';
        }

        if(let_val_btn != ''){
            let loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
            loader_frm_cad_contas.style.display = "flex";
            $.ajax({
                type: 'POST',
                url: '/contabil_composicao_app/cria_atualiza_conta',
                data: {
                    'transacao'         :   let_transacao,
                    'cod_conta'         :   let_cod_conta,
                    'desc_conta'        :   let_desc_contra,
                    'handle_cp'         :   let_handle_conta_cp,
                    'cod_red_cp'        :   let_cod_red_conta_cp,
                    'str_cp'            :   let_estrut_cp,
                    'handle_lp'         :   let_handle_conta_lp,
                    'cod_red_lp'        :   let_cod_red_conta_lp,
                    'str_lp'            :   let_estrut_lp,
                    'cod_pac_conta'     :   let_cod_pacote_conta,
                    'cod_modelo'        :   let_cod_modelo_conta,
                    'ini_atv'           :   let_ini_atv_conta,
                    'fim_atv'           :   let_fim_atv_conta,
                    'status_conta_comp' :   let_status_conta_comp
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

                    $("#btn_cadastra_nova_conta").val(dados.cod_conta);
                    let let_new_label_btn_cadastro_conta = `
                        <i class="fa-solid fa-arrows-rotate"></i>Atualizar dados conta
                    `;
                    $("#cb_contas option").remove();
                    dados.lista_contas.forEach(conta => {
                        $("#cb_contas").append("<option value='" +conta.cod_conta+"'>"+conta.cod_conta+" - " + conta.desc_conta+" - Modelo "+
                            conta.tipo_modelo+"</option>");

                    });
                    $("#cb_contas").selectpicker("");
                    $("#cb_contas").selectpicker('refresh');

                    $("#btn_cadastra_nova_conta").html(let_new_label_btn_cadastro_conta);
                    $("#btn_cadastra_novo_contrato").val(dados.cod_conta);
                    $("#btn_importar_contrato_benner").val(dados.cod_conta);
                    $("#btn_refresh_dados_contratos").val(dados.cod_conta);
                    $("#btn_associar_responsaveis_conta").val(dados.cod_conta);
                    $("#btn_anexa_doc_contrato").val(dados.cod_conta);
                    $("#btn_importa_contrato_pelo_num").val(dados.cod_conta);

                    let let_btn_criar_nova_conta_manual = `
                    <button type='button' name='btn_criar_nova_conta_manual'
                        id='btn_criar_nova_conta_manual' class='mr-2 btn btn-primary btn-rounded cl_btn_cad_contas'>
                        <i class="fa-solid fa-plus"></i>Limpar campos
                        </button>
                    `;
                    $("#div_btn_criar_nova_conta_manual").html(let_btn_criar_nova_conta_manual);



                    loader_frm_cad_contas.style.display = "none";

                },
                error: function (request, status, error) {
                    loader_frm_cad_contas.style.display = "none";
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
    else if(let_nome_btn == 'btn_criar_nova_conta_manual'){
        limpa_campos_form_cad_contas();
    }
    else if(let_nome_btn == "btn_cadastra_novo_contrato") {
        let let_cod_conta = $(this).val();
        if(let_cod_conta != "0"){
            let let_num_contrato = $("#txt_num_contrato").val();
            let let_nome_fornecedor = $("#txt_desc_produto").val();
            let let_data_emissao = $("#dt_emissao_contrato").val();
            let let_handle_contrato = $("#txt_handle_contrato").val();
            let let_doc_contabil = $("#txt_doc_contabil").val();
            let let_val_nominal = $("#txt_val_nominal").val();
            let let_val_liquido = $("#txt_total_liquido").val();
            let let_dia_util = $("#txt_dia_util").val();
            let let_primeira_parcela = $("#dt_primeira_parcela").val();
            let let_qtd_parcelas = $("#txt_qtd_parcelas").val();
            let let_handle_operacao = $("#txt_handle_operacao").val();
            let let_desc_operacao = $("#txt_desc_operacao").val();
            let let_check_atualiza_benner = 'S';
            if($("#chk_atualiza_com_benner").prop("checked") == false){
                let_check_atualiza_benner = 'N';
            }
            let loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
            loader_frm_cad_contas.style.display = "flex";
            $.ajax({
                type: 'POST',
                url: '/contabil_composicao_app/cadastro_contrato',
                data: {
                    'transacao'                 :   'cadastro',
                    'cod_conta'                 :   let_cod_conta,
                    'num_contrato'              :   let_num_contrato,
                    'nome_fornecedor'           :   let_nome_fornecedor,
                    'data_emissao'              :   let_data_emissao,
                    'handle_contrato'           :   let_handle_contrato,
                    'doc_contabil'              :   let_doc_contabil,
                    'val_nominal'               :   let_val_nominal,
                    'val_liquido'               :   let_val_liquido,
                    'dia_util'                  :   let_dia_util,
                    'data_primeira_parcela'     :   let_primeira_parcela,
                    'qtd_parcelas'              :   let_qtd_parcelas,
                    'handle_operacao'           :   let_handle_operacao,
                    'desc_operacao'             :   let_desc_operacao,
                    'check_atualiza_benner'     :   let_check_atualiza_benner
                },
                dataType: 'json',
                success: function (dados) {
                    atualiza_tab_contratos_conta(let_cod_conta);
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    loader_frm_cad_contas.style.display = "none";
                },
                error: function (request, status, error) {
                    loader_frm_cad_contas.style.display = "none";
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
        else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Confirme anteriormente o cadastro da conta!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }

    }
    else if(let_nome_btn == "btn_associar_responsaveis_conta"){
        let let_tipo_transacao_resp = $("#hd_tipo_transacao_resp").val();
        let let_resp_com = $("#cb_resp_composicao").val();
        let let_resp_val = $("#cb_resp_validacao").val();
        let let_dt_ini = $("#dt_ini_resp").val();
        let let_dt_fim = $("#dt_fim_resp").val();
        if(let_tipo_transacao_resp == "C") {
            let let_cod_conta = $(this).val();
            if(let_cod_conta != "0"){

                $.ajax({
                    type: 'POST',
                    url: '/contabil_composicao_app/associa_resp_conta',
                    data: {
                        'tipo_transacao'     :   'C',
                        'cod_conta'          :   let_cod_conta,
                        'resp_com'           :   let_resp_com,
                        'resp_val'           :   let_resp_val,
                        'data_ini'           :   let_dt_ini,
                        'data_fim'           :   let_dt_fim
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
                        atualiza_tabela_resp_conta(dados.cod_conta);
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
            else {
                $.gritter.add({
                    title: 'Atenção!',
                    text: 'Confirme anteriormente o cadastro da conta!',
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        }
        else if(let_tipo_transacao_resp == "U"){
            $.ajax({
                type: 'POST',
                url: '/contabil_composicao_app/associa_resp_conta',
                data: {
                    'tipo_transacao'     :   'U',
                    'cod_resp_conta'     :   let_val_btn,
                    'resp_com'           :   let_resp_com,
                    'resp_val'           :   let_resp_val,
                    'data_ini'           :   let_dt_ini,
                    'data_fim'           :   let_dt_fim
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
                    let let_img_btn_atualizar_dados_resp = `
                        <i class="fa-solid fa-plus" ></i>
                    `;
                    $("#btn_associar_responsaveis_conta").html(let_img_btn_atualizar_dados_resp + "Associar responsáveis");
                    $("#btn_associar_responsaveis_conta").val(dados.cod_conta);
                    atualiza_tabela_resp_conta(dados.cod_conta);
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


    }
    else if(let_nome_btn == "btn_liquidar_parcela"){
        let let_handle_parcela = let_val_btn;
        let let_data_pag = $("#dt_data_pag_parc_"+let_val_btn).val();
        let let_val_pag = $("#txt_val_pag_parc_"+let_val_btn).val();
        let loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
        loader_frm_cad_contas.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/atualiza_dados_parcela',
            data: {
                'transacao'         :  'pagamento',
                'handle_parcela'    :   let_handle_parcela,
                'data_pag'          :   let_data_pag,
                'val_pag'           :   let_val_pag
            },
            dataType: 'json',
            success: function (dados) {
                atualiza_tab_contratos_conta(dados.cod_conta);
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                loader_frm_cad_contas.style.display = "none";
            },
            error: function (request, status, error) {
                loader_frm_cad_contas.style.display = "none";
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
    else if(let_nome_btn == "btn_gera_conciliacao_comp_benner") {
        let let_cod_conta = $("#cb_contas_conciliacao_comp_benner").val().toString();
        let let_competencia = $("#dt_conciliacao_comp_benner").val();
        let cod_modelo_selecionado = 0;
        if ( $("#rd_modelo_conta_conc_comp_benner_1").is(':checked') == true){
            cod_modelo_selecionado = 1;
        } else if ( $("#rd_modelo_conta_conc_comp_benner_2").is(':checked') == true){
            cod_modelo_selecionado = 2;
        } else if ( $("#rd_modelo_conta_conc_comp_benner_3").is(':checked') == true){
            cod_modelo_selecionado = 3;
        }
        let let_loader_gera_comp_res = document.getElementById("loader_gera_comp_res");
        let_loader_gera_comp_res.style.display = "flex";

        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/gera_conciliacao_comp_benner',
            data: {
                'cod_modelo_selecionado' : cod_modelo_selecionado,
                'cod_conta'     :   let_cod_conta,
                'competencia'   :   let_competencia,
                'tipo_visualizacao' :   'R'
            },
            dataType: 'json',
            success: function (data) {
                //$("#tab_conciliacao_composicao_benner").DataTable().clear().draw();
                //Limpa tabela
                $("#tab_conciliacao_composicao_benner").dataTable().fnClearTable();
                $("#tab_conciliacao_composicao_benner").dataTable().fnDestroy();
                const tabela = new DataTable("#tab_conciliacao_composicao_benner");
                let let_lista_dados = [];
                for (var i = 0; i < data.lista_contas_conciliacao.length; i++) {

                    let let_img = `
                        <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                    `;


                    let let_reg = [];
                    if (cod_modelo_selecionado == 1){

                        let let_btn_detalhes_conta = `
                            <button type='button' name='btn_detalhes_conta'
                                id='btn_detalhes_conta_${data.lista_contas_conciliacao[i][0]}'
                                class='btn btn-rounded btn-space'
                                value='${data.lista_contas_conciliacao[i][0]}' title='${data.lista_contas_conciliacao[i][1]}'>
                                <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                            </button>
                        `;
                        let let_btn_visualiza_doc = `<i class="fa-solid fa-eye-slash" style="color: #f46424;"
                            title='Não há Documento Anexado'></i>`;
                        if( data.lista_contas_conciliacao[i][5] != '0') {
                            let_btn_visualiza_doc = `
                                <button type='button' name='btn_visualiza_doc_contrato'
                                    id='btn_visualiza_doc_conta_${data.lista_contas_conciliacao[i][0]}'
                                    class='btn btn-rounded btn-space'
                                    value='${data.lista_contas_conciliacao[i][5]}' title='Visualizar Documento Anexado'>
                                    <i class="fa-solid fa-eye" style="color: #f46424;"></i>
                                </button>
                            `;

                        }

                        let_reg = [
                            /* 1 cod_reduzido */ let_img + `&nbsp;&nbsp;&nbsp;&nbsp;` + data.lista_contas_conciliacao[i][6],
                            /* 2 desc conta */data.lista_contas_conciliacao[i][1],
                            /* 3 val comp */data.lista_contas_conciliacao[i][2],
                            /* 4 val bal */data.lista_contas_conciliacao[i][3],
                            /* 5 dif */data.lista_contas_conciliacao[i][4],
                            /* 6 */let_btn_detalhes_conta,
                            /* 7 */let_btn_visualiza_doc
                        ];
                        let_lista_dados.push(let_reg);
                    }
                    else if ( cod_modelo_selecionado == 3 ) {

                        let let_btn_detalhes_conta = `
                            <button type='button' name='btn_detalhes_conta'
                                id='btn_detalhes_conta_${data.lista_contas_conciliacao[i][0]}'
                                class='btn btn-rounded btn-space'
                                value='${data.lista_contas_conciliacao[i][0]}_${data.lista_contas_conciliacao[i][2]}'
                                title='${data.lista_contas_conciliacao[i][1]}'>
                                <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                            </button>
                        `;
                        let let_btn_visualiza_doc = `<i class="fa-solid fa-eye-slash" style="color: #f46424;"
                            title='Não há Documento Anexado'></i>`;
                        if( data.lista_contas_conciliacao[i][13] != '0') {
                            let_btn_visualiza_doc = `
                                <button type='button' name='btn_visualiza_doc_contrato'
                                    id='btn_visualiza_doc_conta_${data.lista_contas_conciliacao[i][0]}'
                                    class='btn btn-rounded btn-space'
                                    value='${data.lista_contas_conciliacao[i][13]}' title='Visualizar Documento Anexado'>
                                    <i class="fa-solid fa-eye" style="color: #f46424;"></i>
                                </button>
                            `;

                        }

                        let_reg = [
                            /* 0 - desc_conta */let_img + `&nbsp;&nbsp;&nbsp;&nbsp;` + data.lista_contas_conciliacao[i][1],
                            /* 1 - num_contrato */ data.lista_contas_conciliacao[i][2],
                            /* 1 - doc_contabil */ data.lista_contas_conciliacao[i][3],
                            /* 3 - val_comp_cp */ data.lista_contas_conciliacao[i][4],
                            /* 4 - val_balancete_cp */ data.lista_contas_conciliacao[i][5],
                            /* 5 - val_dif_comp_balanc_cp */ data.lista_contas_conciliacao[i][6],
                            /* 6 - val_comp_lp */ data.lista_contas_conciliacao[i][7],
                            /* 7 - val_balancete_lp */ data.lista_contas_conciliacao[i][8],
                            /* 8 - val_dif_comp_bal_lp */ data.lista_contas_conciliacao[i][9],
                            /* 9 - val_tt_comp */ data.lista_contas_conciliacao[i][10],
                            /* 10 - val_tt_balan */ data.lista_contas_conciliacao[i][11],
                            /* 11 - val_dif_tt_comp_bal */ data.lista_contas_conciliacao[i][12],
                            /* 12 */let_btn_detalhes_conta,
                            /* 13 */let_btn_visualiza_doc
                        ];
                        let_lista_dados.push(let_reg);

                    }
                    /*tabela.row
                        .add(let_reg)
                        .draw(false);*/
                }

                $("#tab_conciliacao_composicao_benner").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "50vh", //770px
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data": let_lista_dados,
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0]}
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
                } );

                let_loader_gera_comp_res.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_gera_comp_res.style.display = "none";
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
    else if(let_nome_btn == "btn_gera_conciliacao_comp_benner_detalhado") {
        gera_conciliacao_comp_benner_detalhado();
    }
    else if(let_nome_btn == "btn_detalhes_conta") {
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/acessa_frm_detalhes_conta_composicao',
            data: {
                'cod_conta'     :   let_val_btn.split('_')[0],
                'compentencia'  :   $("#dt_conciliacao_comp_benner").val()
            },
            dataType: 'json',
            success: function (data_detalhes_success) {
                $("#txt_desc_conta_dth_comp").val(data_detalhes_success.desc_conta);
                $("#txt_desc_pacote_conta_dth_comp").val(data_detalhes_success.desc_pacote);
                $("#txt_resp_comp_conta_dth_comp").val(data_detalhes_success.resp_composicao);
                $("#txt_resp_val_conta_dth_comp").val(data_detalhes_success.resp_validacao);

                if(data_detalhes_success.cod_modelo_conta == 1){
                    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
                    let_loader_frm_cad_contas.style.display = "flex";
                    $.ajax({
                        type : 'GET',
                        data : {
                            'competencia': $("#dt_conciliacao_comp_benner").val(),
                            'cod_conta' : data_detalhes_success.cod_conta
                        },
                        url: '/contabil_composicao_app/retorna_lista_docs_contas_modelo_1',
                        success: function(dados) {
                            $("#div_info_detalhes_conta").html(dados);
                            let_loader_frm_cad_contas.style.display = "none";
                        },
                        error: function(request, status, error){
                            let_loader_frm_cad_contas.style.display = "none";
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
                else if(data_detalhes_success.cod_modelo_conta == 3){
                    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
                    let_loader_frm_cad_contas.style.display = "flex";
                    $.ajax({
                        type: 'GET',
                        url: '/contabil_composicao_app/retorna_dados_contrato_conta_cadastrada',
                        data: {
                            'tipo_transacao'  :   'retornar_dados_cadastro',
                            'num_contrato'    :   let_val_btn.split('_')[1],
                            'cod_conta'       :    data_detalhes_success.cod_conta
                        },
                        success: function (dados) {
                            $("#div_info_detalhes_conta").html(dados); 
                            let_loader_frm_cad_contas.style.display = "none";
                        },
                        error: function (request, status, error) {
                            let_loader_frm_cad_contas.style.display = "none";
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

                $("#modal_detalhes_contas_composicao").show();


            },
            error: function (request, status, error) {
                let_loader_gera_comp_res.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
        /*
        let let_cod_conta = let_val_btn;
        let let_radio1 = $("#rd_modelo_conta_conc_comp_benner_1").prop('checked');
        let let_radio2 = $("#rd_modelo_conta_conc_comp_benner_2").prop('checked');
        let let_radio3 = $("#rd_modelo_conta_conc_comp_benner_3").prop('checked');
        let let_cod_modelo_conta_selecionado = 0;
        if ( let_radio1 == true ){
            let_cod_modelo_conta_selecionado = 1;
        } else if ( let_radio2 == true ){
            let_cod_modelo_conta_selecionado = 2;
        } else if ( let_radio3 == true ){
            let_cod_modelo_conta_selecionado = 3;
        }
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_conta_cadastrada',
            data: {
                'tipo_return' :    'R',
                'cod_conta'   :    let_cod_conta,
                'cod_modelo_conta_selecionado': let_cod_modelo_conta_selecionado
            },
            success: function(dados){
                $("#main_menu").html(dados);
                $('.selectpicker').selectpicker();
                if(let_cod_modelo_conta_selecionado == 1){
                    $("#rd_modelo_conta_1").prop('checked', true);
                } else if(let_cod_modelo_conta_selecionado == 2){
                    $("#rd_modelo_conta_2").prop('checked', true);
                } else if(let_cod_modelo_conta_selecionado == 3){
                    $("#rd_modelo_conta_3").prop('checked', true);
                }
                desenha_frm_cad_contas_conforme_tipo_modelo(let_cod_modelo_conta_selecionado);



                atualiza_form_dados_conta('J', let_cod_conta)
                if(let_cod_modelo_conta_selecionado == 1) {
                    atualiza_doc_contas_modelo_1(let_cod_conta);
                } else if(let_cod_modelo_conta_selecionado == 3) {
                    atualiza_tab_contratos_conta(let_cod_conta);
                }

                atualiza_tabela_resp_conta(let_cod_conta);
                atualiza_tab_anexos_conta(let_cod_conta);
                atualiza_tab_status_contrato_composicao(let_cod_conta);

                $("#cb_contas").val(let_cod_conta);
                //$("#cb_contas").selectpicker('refresh');


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
        */
    }
    else if (let_nome_btn == "btn_fecha_modal_detalhes_contas_composicao"){
        $("#modal_detalhes_contas_composicao").hide();
    }
    else if(let_nome_btn == 'btn_anexa_doc_contrato') {
        let let_cod_conta = $(this).val();
        if(let_cod_conta != "0"){
            var formDataImg = new FormData();
            formDataImg.append("file", $('input[type=file]')[0].files[0]);
            formDataImg.append("cod_conta", let_cod_conta);
            formDataImg.append("cod_contrato", $("#list_contratos_conta_anexo").val());
            formDataImg.append("competencia_doc", $("#dt_competencia_anexo_doc_contrato").val());
            $.ajax({
                type:'POST',
                enctype: "multipart/form-data; charset=utf-8",
                url: '/contabil_composicao_app/salva_caminho_anexo_conta',
                data: formDataImg,
                dataType: 'json',
                processData: false,
                contentType: false,
                cache: false,
                success: function(dados){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    $("#file_anexo_contrato").val('');
                    atualiza_tab_anexos_conta(dados.cod_conta);
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
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Confirme anteriormente o cadastro da conta!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

        }

    }
    else if(let_nome_btn == 'btn_exclui_anexo_conta') {
        let let_cod_anexo_conta = let_val_btn;
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_anexo_conta/'+let_cod_anexo_conta,
            dataType: 'json',
            data: {
                'cod_anexo_conta'     :   let_cod_anexo_conta
            },
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_anexos_conta(data.cod_conta);
                $("#div_visualizacao_anexo_conta").html("");
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
    else if(let_nome_btn == 'btn_visulizar_anexo_conta') {
        let let_img_anexo_selecionado = $('<img/>');
        let_img_anexo_selecionado.attr({
            id: 'img_anexo_pre_visualizado',
            name: 'img_anexo_pre_visualizado',
            src: '/media/'+let_val_btn,
            width: '430px',
            height: '440px',
            title: 'Clique na imagem para imprimir o documento'
        });
        $("#div_visualizacao_anexo_conta")
            .html('<embed  src="/media/'+let_val_btn+'" style="width:100%; height:100%;"/>');


    }
    else if(let_nome_btn == 'btn_importar_contrato_benner'){
        let let_cod_conta = let_val_btn;
        if(let_cod_conta != "0"){
            importa_contratos_parcela_conta('T', let_cod_conta, 0);
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Confirme anteriormente o cadastro da conta!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    }
    else if(let_nome_btn == 'btn_importa_contrato_pelo_num') {
        let let_cod_conta = $(this).val();
        let let_num_contrato = $("#txt_num_contrato_importa").val();
        if(let_cod_conta != "0"){
            importa_contratos_parcela_conta('C', let_cod_conta, let_num_contrato);
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Confirme anteriormente o cadastro da conta!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    }
    else if(let_nome_btn == 'btn_excluir_contrato'){
        let let_cod_contrato = $(this).val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_contrato/'+let_cod_contrato,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_contratos_conta(data.cod_conta);
                atualiza_tab_anexos_conta(data.cod_conta);
                atualiza_tab_status_contrato_composicao(data.cod_conta);
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
    else if(let_nome_btn == 'btn_confirma_status_composicao'){
        let let_tipo_prazo = let_val_btn.split('_')[0];
        let let_cod_contrato = let_val_btn.split('_')[1];
        let let_cod_status = $("#cb_status_conciliacao_"+let_tipo_prazo+'_'+let_cod_contrato).val();
        let let_obs_status = $("#ta_obs_status_conciliacao_"+let_tipo_prazo+'_'+let_cod_contrato).val();
        let let_competencia = $("#dt_conciliacao_comp_benner").val();
        let let_val_composicao = $("#txt_val_composicao_"+let_tipo_prazo+'_'+let_cod_contrato).val().replaceAll('.','').replaceAll(',','.');
        let let_val_balancete = $("#txt_val_balancete_"+let_tipo_prazo+'_'+let_cod_contrato).val().replaceAll('.','').replaceAll(',','.');
        let let_val_diferenca = $("#txt_val_diferenca_"+let_tipo_prazo+'_'+let_cod_contrato).val().replaceAll('.','').replaceAll(',','.');

        let let_loader_gera_comp_det = document.getElementById("loader_gera_comp_det");
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/registra_status_composicao_conta',
            data: {
                'cod_contrato': let_cod_contrato,
                'tipo_prazo': let_tipo_prazo,
                'cod_status': let_cod_status,
                'obs_status': let_obs_status,
                'competencia': let_competencia,
                'val_composicao' : let_val_composicao,
                'val_balancete' : let_val_balancete,
                'val_diferenca' : let_val_diferenca
            },
            dataType: 'json',
            success: function (dados) {
                //gera_conciliacao_comp_benner_detalhado();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_gera_comp_det.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_gera_comp_det.style.display = "none";
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
    else if(let_nome_btn == 'btn_editar_resp_conta'){
        $("#cb_resp_composicao").selectpicker('val', $("#hd_resp_comp_"+let_val_btn).val());
        $("#cb_resp_composicao").selectpicker('refresh');

        $("#cb_resp_validacao").selectpicker('val', $("#hd_resp_val_"+let_val_btn).val());
        $("#cb_resp_validacao").selectpicker('refresh');

        $("#dt_ini_resp").val( $("#hd_data_ini_atv_"+let_val_btn).val() );
        $("#dt_fim_resp").val( $("#hd_data_fim_atv_"+let_val_btn).val() );
        $("#hd_tipo_transacao_resp").val("U");
        let let_img_btn_atualizar_dados_resp = `
            <i class="fa-solid fa-rotate" ></i>
        `;
        $("#btn_associar_responsaveis_conta").html(let_img_btn_atualizar_dados_resp + "Atualiza dados");
        $("#btn_associar_responsaveis_conta").val(let_val_btn);

    }
    else if (let_nome_btn == 'btn_desmarcar_contas_comp_benner'){
        $("#cb_contas_conciliacao_comp_benner").selectpicker('deselectAll');
    }
    else if (let_nome_btn == 'btn_marcar_contas_comp_benner'){
        $("#cb_contas_conciliacao_comp_benner").selectpicker('selectAll');
    }
    else if (let_nome_btn == 'btn_visualiza_doc_contrato'){
        let let_cod_anexo_contrato = let_val_btn;

        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/visualiza_doc_contrato_competencia',
            data: {
                'cod_anexo_contrato': let_cod_anexo_contrato
            },
            dataType: 'json',
            success: function (dados) {
                /* http://127.0.0.1:8000/  */
                window.open('https://operacional.conlogsa.com.br/media/'+dados, '_blank');
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
    else if (let_nome_btn == 'btn_abre_modal_exclui_arq_docs_m1') {
        $("#btn_exclui_arq_conta_mod_1").val(let_val_btn);
        $("#modal_exclui_arq_docs_m1").show();
    }
    else if (let_nome_btn == 'btn_fecha_modal_exclui_arq_docs_m1') {
        $("#modal_exclui_arq_docs_m1").hide();
    }
    else if (let_nome_btn == 'btn_exclui_arq_conta_mod_1') {
        let let_arq_conta_motivo = let_val_btn + '_' + $("#ta_justificativa_exclusao_arq_docs_m1").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_arquivo_conta_m_1/'+let_arq_conta_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_doc_contas_modelo_1(data.cod_conta);
                $("#div_visualizacao_anexo_conta").html("");
                $("#modal_exclui_arq_docs_m1").hide();
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
    else if (let_nome_btn == 'btn_gera_conciliacao_comp_benner_detalhado_aud') {
        gera_conciliacao_comp_benner_auditoria();
    }
    else if (let_nome_btn == 'btn_importa_anexos') {
        if(let_val_btn > 0) {
            let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
            let_loader_frm_cad_contas.style.display = "flex";
            $.ajax({
                type: 'POST',
                url: '/contabil_composicao_app/importa_anexo_geral_contas',
                dataType: 'json',
                success: function(data){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    let_loader_frm_cad_contas.style.display = "none";
                    $("#btn_importa_anexos").attr('title', "Quantidade de arquivos para importar: " + data.qtd_arquivos_postados);
                    $("#btn_importa_anexos").val(data.qtd_arquivos_postados);
                },
                error: function(request, status, error){
                    let_loader_frm_cad_contas.style.display = "none";
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Não há arquivos para serem importados!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }


    } else if (let_nome_btn == 'btn_abrir_modal_atualiza_contratos_benner') {
        $("#modal_atualiza_contratos_benner").show();

    } else if (let_nome_btn == 'btn_fecha_modal_atualiza_contratos_benner') {
        $("#tab_reg_atualizacao_benner").DataTable().clear().draw();
        $("#modal_atualiza_contratos_benner").hide();

    } else if (let_nome_btn == 'btn_desmarcar_contas_atualiza_contratos_benner'){
        $("#sl_contas_atualiza_contratos_benner").selectpicker('deselectAll');
    }
    else if (let_nome_btn == 'btn_marcar_contas_atualiza_contratos_benner'){
        $("#sl_contas_atualiza_contratos_benner").selectpicker('selectAll');
    }
    else if (let_nome_btn == 'btn_atualiza_dados_contrato_benner'){
        let let_loader_frm_modal_atualiza_contratos_benner =
            document.getElementById("loader_frm_modal_atualiza_contratos_benner");
        let_loader_frm_modal_atualiza_contratos_benner.style.display = "flex";
        let let_lista_cod_contas = $("#sl_contas_atualiza_contratos_benner").val().toString();

        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/atualiza_contratos_com_dados_do_benner',
            data: {
                'lista_cod_contas': let_lista_cod_contas
            },
            dataType: 'json',
            success: function (dados) {
                let let_lista_reg_table = []
                dados.lista_parcelas_atualizados.forEach( parc => {
                    let let_img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
                    let reg = [
                        let_img,
                        parc.cod_conta,
                        parc.desc_conta,
                        parc.num_contrato,
                        parc.num_parcela,
                        parc.val_pago,
                        parc.val_principal,
                        parc.val_taxas,
                        parc.val_fundo,
                        parc.data_vencimento,
                        parc.data_liquidacao,
                        parc.handle_parcela
                    ];
                    let_lista_reg_table.push(reg);
                });
                $('#tab_reg_atualizacao_benner').DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": true,
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 6,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_reg_table,
                    "columns": [
                        { title: "" },
                        { title: "Cód. conta" },
                        { title: "Conta" },
                        { title: "Núm contrato" },
                        { title: "Núm parcela" },
                        { title: "Val pago" },
                        { title: "Val principal" },
                        { title: "Val taxas" },
                        { title: "Val fundo" },
                        { title: "Data vencimento" },
                        { title: "Data liquidação" },
                        { title: "Handle parcela" }
                    ],
                    /*"columnDefs": [
                        {"className": "dt-center", "targets": [0,1,3,12,21,22,23,24,25,26,27]},
                        {"className": "dt-left", "targets": [2]},
                        {"className": "dt-right", "targets": [4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20]}
                    ],*/
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
                let_loader_frm_modal_atualiza_contratos_benner.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_frm_modal_atualiza_contratos_benner.style.display = "none";
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

    else if (let_nome_btn == 'bnt_arq_conta') {
        let loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
        loader_frm_cad_contas.style.display = "flex";
        //Povoa tabela
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_docs_conta_m1',
            data: {
                'cod_conta'     :   let_val_btn.split('_')[0],
                'cod_arq'       :   let_val_btn.split('_')[1]
            },
            success: function (dados) {
                $("#div_docs_arq_competencia_"+let_val_btn.split('_')[1]).html(dados);

                $(".display").DataTable( {
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
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0]}
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

                loader_frm_cad_contas.style.display = "none";

            },
            error: function (request, status, error) {
                loader_frm_cad_contas.style.display = "none";
                console.log(error);
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

    else if (let_nome_btn == 'btn_refresh_dados_contratos'){
        atualiza_tab_contratos_conta(let_val_btn);
    }
    else if (let_nome_btn == 'btn_abre_modal_estornar_parc_ctr_contas_m3') {
        $("#btn_confirma_estorno_parc_ctr_contas_m3").val(let_val_btn);
        $("#modal_estornar_parc_ctr_contas_m3").show();
    }
    else if (let_nome_btn == 'btn_fecha_modal_estornar_parc_ctr_contas_m3') {
        $("#modal_estornar_parc_ctr_contas_m3").hide();
    }
    else if (let_nome_btn == 'btn_confirma_estorno_parc_ctr_contas_m3') {
        let let_cod_parc_e_motivo = let_val_btn + '_' + $("#ta_justificativa_estornar_parc_ctr_contas_m3").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/estornar_parc_ctr_contas_m3/'+let_cod_parc_e_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_contratos_conta(data.cod_conta);
                $("#ta_justificativa_estornar_parc_ctr_contas_m3").html("");
                $("#modal_estornar_parc_ctr_contas_m3").hide();
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
    }else if (let_nome_btn == 'btn_desmarcar_resp_contas'){
        $("#cb_responsaveis_contas").selectpicker('deselectAll');
    }
    else if (let_nome_btn == 'btn_marcar_resp_contas'){
        $("#cb_responsaveis_contas").selectpicker('selectAll');
    }

});

$(document).on('change','input', function(){
	let let_nome_inp = $(this).attr('name');
    let let_id_inp = $(this).attr('id');
    let let_chk_inp = $(this).prop('checked')

    if(let_nome_inp == "chk_atualiza_dados_benner_contrato"){

        let let_handle_contrato = let_id_inp.split('_')[5];
        let let_status_componente = $(this).prop("checked");
        let let_div_status_atualiza_benner = `Atualiza com o Benner ? <strong>SIM</strong>`;
        let let_status_sincroniza_benner = 'S';
        if(let_status_componente == false){
            let_status_sincroniza_benner = 'N';
            let_div_status_atualiza_benner = `Atualiza com o Benner ? <strong>NÃO</strong>`;

        }
        $.ajax({
        type: 'POST',
        url: '/contabil_composicao_app/atualiza_status_contrato_sincroniza_benner',
        data: {
            'transacao'                             :   'status_sincronia_benner',
            'handle_contrato'                       :   let_handle_contrato,
            'status_sincronia_contrato_benner'      :   let_status_sincroniza_benner
        },
        dataType: 'json',
        success: function (dados) {
            $("#div_status_atualiza_benner").empty();

            $("#sl_contas_atualiza_contratos_benner option").remove();
            dados.lista_contas_para_atualizar_benner.forEach( conta => {
                $("#sl_contas_atualiza_contratos_benner").append("<option value='"+
                conta.cod_conta__cod_conta+"'>"+conta.cod_conta__cod_conta+" - "+conta.cod_conta__desc_conta+
                " - Cód. red. CP - "+conta.cod_conta__cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_conta__cod_red_conta_contabil_lp+"</option>");
            });
            $("#sl_contas_atualiza_contratos_benner").selectpicker('refresh');

            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            $("#div_status_atualiza_benner").html(let_div_status_atualiza_benner);

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
    else if ( let_nome_inp == "rd_modelo_conta_conc_comp_benner" ) {
        let let_cod_modelo_conta = 0;
        let let_tipo_rel = $("#hd_tipo_rel").val();
        $("#div_tab_conciliacao_composicao_benner").html("");
        $("#div_tab_conciliacao_composicao_benner_detalhado").html("");
        $("#div_tab_conciliacao_composicao_benner_aud").html("");

        if(let_tipo_rel == 'R'){
            //tab_conciliacao_composicao_benner
            let let_tab_concilicacao_comp_benner = $("<table/>");
            let_tab_concilicacao_comp_benner.attr({
                id: 'tab_conciliacao_composicao_benner',
                class: 'display wrap w-100 cl_tab_principal_pagina'
            });

            let let_thead = $("<thead/>");
            let let_tr = $("<tr/>");

            let let_colunas_tabela = [];
            if (let_id_inp == "rd_modelo_conta_conc_comp_benner_1") {
                let_cod_modelo_conta = 1;
                let_colunas_tabela = [
                    'Cód. reduzido',
                    'Conta',
                    'Comp',
                    'Balan',
                    'Dif',
                    'Detalhes',
                    'Documento'
                ];
            }
            else if (let_id_inp == "rd_modelo_conta_conc_comp_benner_2") {
                let_cod_modelo_conta = 2;
                let_colunas_tabela = [
                    'Conta',
                    'Doc Cont',
                    'Comp',
                    'Balan',
                    'Dif',
                    'Detalhes',
                    'Documento'
                ];
            }
            else if (let_id_inp == "rd_modelo_conta_conc_comp_benner_3") {
                let_cod_modelo_conta = 3;
                let_colunas_tabela = [
                    'Conta',
                    'Contrato',
                    'Doc Cont',
                    'Comp CP',
                    'Balan CP',
                    'Dif CP',
                    'Comp LP',
                    'Balan LP',
                    'Dif LP',
                    'Comp Tt',
                    'Balan Tt',
                    'Dif Tt',
                    'Detalhes',
                    'Documento'
                ];
            }

            //tab_conciliacao_composicao_benner
            let_colunas_tabela.forEach( col => {
                let let_th = $("<th/>");
                let_th.attr({
                    scope: 'col',
                    align: 'left',
                    style: 'color: grey'
                });
                let_th.html(col);
                let_tr.append(let_th);
            });
            let_thead.append(let_tr)
            let_tab_concilicacao_comp_benner.append(let_thead);

            let let_body = $("<body/>");
            let_tab_concilicacao_comp_benner.append(let_body)

            $("#div_tab_conciliacao_composicao_benner").html(let_tab_concilicacao_comp_benner);
            $("#tab_conciliacao_composicao_benner").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "50vh", //770px
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0]}
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
                    } );

        }
        else if(let_tipo_rel == 'D'){
            //tab_conciliacao_composicao_benner_detalhado
            let let_tab_concilicacao_comp_benner_detalhado = $("<table/>");
            let_tab_concilicacao_comp_benner_detalhado.attr({
                id: 'tab_conciliacao_composicao_benner_detalhado',
                class: 'display wrap w-100 cl_tab_principal_pagina'
            });

            let let_thead_detalhado = $("<thead/>");
            let let_tr_detalhado = $("<tr/>");

            let let_colunas_tabela_detalhado = [];
            if (let_id_inp == "rd_modelo_conta_conc_comp_benner_1") {
                let_cod_modelo_conta = 1;

                let_colunas_tabela_detalhado = [
                    'Estrutura',
                    'Cód red',
                    'Conta',
                    'Composição',
                    'Balancete',
                    'Diferenca',
                    'Status',
                    'Detalhes',
                    'Documento'
                ];

            }
            else if (let_id_inp == "rd_modelo_conta_conc_comp_benner_2") {
                let_cod_modelo_conta = 2;

                let_colunas_tabela_detalhado = [
                    'Estrutura',
                    'Cód red',
                    'Conta',
                    'Composição',
                    'Balancete',
                    'Diferenca',
                    'Status',
                    'Detalhes'
                ];

            }
            else if (let_id_inp == "rd_modelo_conta_conc_comp_benner_3") {
                let_cod_modelo_conta = 3;

                let_colunas_tabela_detalhado = [
                    'Estrutura',
                    'Cód red',
                    'Conta',
                    'Contrato',
                    'Doc Cont',
                    'Tipo prazo',
                    'Composição',
                    'Balancete',
                    'Diferenca',
                    'Status',
                    'Detalhes',
                    'Documento'
                ];

            }

            //tab_conciliacao_composicao_benner_detalhado
            let_colunas_tabela_detalhado.forEach( col => {
                let let_th_detalhado = $("<th/>");
                let_th_detalhado.attr({
                    scope: 'col',
                    align: 'left',
                    style: 'color: grey'
                });
                let_th_detalhado.html(col);
                let_tr_detalhado.append(let_th_detalhado);
            });
            let_thead_detalhado.append(let_tr_detalhado)
            let_tab_concilicacao_comp_benner_detalhado.append(let_thead_detalhado);

            let let_body_detalhado = $("<body/>");
            let_tab_concilicacao_comp_benner_detalhado.append(let_body_detalhado)

            $("#div_tab_conciliacao_composicao_benner_detalhado").html(let_tab_concilicacao_comp_benner_detalhado);
            $("#tab_conciliacao_composicao_benner_detalhado").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "50vh", //770px
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
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
                    } );

        }
        else if(let_tipo_rel == 'A'){
            //tab_conciliacao_composicao_benner_auditoria
            let let_tab_concilicacao_comp_benner_aud = $("<table/>");
            let_tab_concilicacao_comp_benner_aud.attr({
                id: 'tab_conciliacao_composicao_benner_aud',
                class: 'display wrap w-100 cl_tab_principal_pagina'
            });

            let let_thead_aud = $("<thead/>");
            let let_tr_aud = $("<tr/>");

            let let_colunas_tabela = [];
            let let_colunas_tabela_detalhado = [];
            let let_colunas_tabela_aud = [];
            if (let_id_inp == "rd_modelo_conta_conc_comp_benner_1") {
                let_cod_modelo_conta = 1;

                let_colunas_tabela_auditoria = [
                    'Estrutura',
                    'Cód red',
                    'Conta',
                    'Composição',
                    'Balancete',
                    'Diferenca',
                    'Detalhes',
                    'Documento'
                ];
            }
            else if (let_id_inp == "rd_modelo_conta_conc_comp_benner_2") {
                let_cod_modelo_conta = 2;

                let_colunas_tabela_auditoria = [
                    'Estrutura',
                    'Cód red',
                    'Conta',
                    'Composição',
                    'Balancete',
                    'Diferenca',
                    'Status',
                    'Detalhes'
                ];
            }
            else if (let_id_inp == "rd_modelo_conta_conc_comp_benner_3") {
                let_cod_modelo_conta = 3;

                let_colunas_tabela_auditoria = [
                    'Estrutura',
                    'Cód red',
                    'Conta',
                    'Contrato',
                    'Doc Cont',
                    'Tipo prazo',
                    'Composição',
                    'Balancete',
                    'Diferenca',
                    'Detalhes',
                    'Documento'
                ];
            }

            //tab_conciliacao_composicao_benner_auditoria
            let_colunas_tabela_auditoria.forEach( col => {
                let let_th_aud = $("<th/>");
                let_th_aud.attr({
                    scope: 'col',
                    align: 'left',
                    style: 'color: grey'
                });
                let_th_aud.html(col);
                let_tr_aud.append(let_th_aud);
            });
            let_thead_aud.append(let_tr_aud)
            let_tab_concilicacao_comp_benner_aud.append(let_thead_aud);

            let let_body_aud = $("<body/>");
            let_tab_concilicacao_comp_benner_aud.append(let_body_aud)

            $("#div_tab_conciliacao_composicao_benner_aud").html(let_tab_concilicacao_comp_benner_aud);
            $("#tab_conciliacao_composicao_benner_aud").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "50vh", //770px
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
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
                    } );

        }
        let let_competencia = $("#dt_conciliacao_comp_benner").val()
        if (let_tipo_rel == 'A' && let_competencia == '') {

            $.gritter.add({
                title: 'Atenção!',
                text: 'Por favor selecione uma competência',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            $("#rd_modelo_conta_conc_comp_benner_1").attr('checked', false);
            $("#rd_modelo_conta_conc_comp_benner_2").attr('checked', false);
            $("#rd_modelo_conta_conc_comp_benner_3").attr('checked', false);

        } else {
            $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/povoa_cb_contas_conciliacao_comp_benner',
            cache: false,
            data: {
                'tipo_rel': let_tipo_rel,
                'cod_modelo_conta'  :   let_cod_modelo_conta,
                'data_competencia'  :   let_competencia,
                'nome_resp'         :   ''
            },
            dataType: 'json',
            success: function (data) {
                $("#cb_contas_conciliacao_comp_benner option").remove();
                if( let_tipo_rel == 'R' || let_tipo_rel == 'D' || let_tipo_rel == 'C'){
                    data.lista_contas.forEach(conta => {
                        $("#cb_contas_conciliacao_comp_benner").append("<option value='"+
                        conta.cod_conta+"'>"+conta.cod_conta + " - " + conta.desc_conta+" - Cód. red. CP - "+
                        conta.cod_red_conta_contabil_cp+
                        " Cód. red. LP - "+conta.cod_red_conta_contabil_lp+"</option>");

                    });
                } else {
                    data.lista_contas.forEach(conta => {
                        $("#cb_contas_conciliacao_comp_benner").append("<option value='"+
                        conta.cod_conta__cod_conta+"'>"+conta.cod_conta__cod_conta + " - " + conta.cod_conta__desc_conta
                            +" - Cód. red. CP - "+conta.cod_conta__cod_red_conta_contabil_cp+
                        " Cód. red. LP - "+conta.cod_conta__cod_red_conta_contabil_lp+"</option>");

                    });

                }
                $("#cb_contas_conciliacao_comp_benner").selectpicker('refresh');
                $("#cb_contas_conciliacao_comp_benner").selectpicker('selectAll');


                $("#cb_pacote_conta option").remove();
                data.lista_pacotes_conta.forEach(pac => {
                    $("#cb_pacote_conta").append("<option value='"+
                    pac.cod_pacote_conta+"'>"+pac.desc_pacote_conta+"</option>");
                });
                //$("#cb_pacote_conta").val(data.dic_conta.cod_pacote_conta);
                $("#cb_pacote_conta").selectpicker('refresh');


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



    }
    else if ( let_nome_inp == "rd_modelo_conta" ) {
        limpa_campos_form_cad_contas();
        let let_cod_modelo_conta = 0
        if (let_id_inp == "rd_modelo_conta_1") {
            let_cod_modelo_conta = 1;
        } else if (let_id_inp == "rd_modelo_conta_2") {
            let_cod_modelo_conta = 2;
        } else if (let_id_inp == "rd_modelo_conta_3") {
            let_cod_modelo_conta = 3;
        }
        desenha_frm_cad_contas_conforme_tipo_modelo(let_cod_modelo_conta);

    }
    else if ( let_nome_inp == "txt_val_principal" || let_nome_inp == "txt_val_taxas" || let_nome_inp == "txt_val_fundo" || let_nome_inp == 'txt_val_conta') {
        let let_handle_parcela = let_id_inp.split("_")[3];
        let let_val_conta = parseFloat($("#txt_val_conta_" + let_handle_parcela).val().replaceAll('.','').replaceAll(',','.'));
        let let_val_principal = parseFloat($("#txt_val_principal_" + let_handle_parcela).val().replaceAll('.','').replaceAll(',','.'));
        let let_val_taxas = parseFloat($("#txt_val_taxas_" + let_handle_parcela).val().replaceAll('.','').replaceAll(',','.'));
        let let_val_fundo = parseFloat($("#txt_val_fundo_" + let_handle_parcela).val().replaceAll('.','').replaceAll(',','.'));


        let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/atualiza_dados_parcela',
            data: {
                'transacao'         :  'atualiza_dados',
                'handle_parcela'    :   let_handle_parcela,
                'val_principal'     :   let_val_principal,
                'val_taxas'         :   let_val_taxas,
                'val_fundo'         :   let_val_fundo,
                'val_conta'         :   let_val_conta

            },
            //dataType: 'json',
            success: function (dados) {
                let let_val_tt = (let_val_principal + let_val_taxas + let_val_fundo).toFixed(2);
                $("#td_val_total_" + let_handle_parcela).html(let_val_tt);
                //atualiza_tab_contratos_conta(dados.cod_conta);
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_frm_cad_contas.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_frm_cad_contas.style.display = "none";
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
    else if ( let_nome_inp == "dt_conciliacao_comp_benner" ){

        $("#rd_modelo_conta_conc_comp_benner_1").prop("checked", false);
        $("#rd_modelo_conta_conc_comp_benner_2").prop("checked", false);
        $("#rd_modelo_conta_conc_comp_benner_3").prop("checked", false);
        $("#cb_contas_conciliacao_comp_benner option").remove();
        $("#cb_contas_conciliacao_comp_benner").selectpicker('refresh');
        $("#div_tab_conciliacao_composicao_benner_aud").empty();

    }


});


function atualiza_form_dados_conta(tipo_return, cod_conta) {

    let let_radio1 = $("#rd_modelo_conta_1").prop('checked');
    let let_radio2 = $("#rd_modelo_conta_2").prop('checked');
    let let_radio3 = $("#rd_modelo_conta_3").prop('checked');
    let let_cod_modelo_conta_selecionado = 0;
    if ( let_radio1 == true ){
        let_cod_modelo_conta_selecionado = 1;
    } else if ( let_radio2 == true ){
        let_cod_modelo_conta_selecionado = 2;
    } else if ( let_radio3 == true ){
        let_cod_modelo_conta_selecionado = 3;
    }

    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/retorna_dados_conta_cadastrada',
        data: {
            'tipo_return' :    tipo_return,
            'cod_conta'   :    cod_conta,
            'cod_modelo_conta_selecionado': let_cod_modelo_conta_selecionado
        },
        //dataType: 'json',
        success: function (dados) {
            $("#txt_desc_conta").val(dados.dic_conta.desc_conta);

            $("#tx_handle_conta_cp").val(dados.dic_conta.handle_benner_cp);
            $("#txt_cod_red_conta_cp").val(dados.dic_conta.cod_red_benner_cp);
            $("#txt_cod_estrutura_cp").val(dados.dic_conta.cod_estrut_cp);

            $("#tx_handle_conta_lp").val(dados.dic_conta.handle_benner_lp);
            $("#txt_cod_red_conta_lp").val(dados.dic_conta.cod_red_benner_lp);
            $("#txt_cod_estrutura_lp").val(dados.dic_conta.cod_estrut_lp);

            $("#cb_empresa_cad_conta").val(dados.dic_conta.cod_empresa);
            $("#cb_empresa_cad_conta").selectpicker('refresh');

            $("#cb_pacote_conta").val(dados.dic_conta.cod_pacote_conta);
            $("#cb_pacote_conta").selectpicker('refresh');

            let let_cod_modelo = dados.dic_conta.tipo_modelo;
            if (let_cod_modelo == 1) {
                $("#rd_modelo_conta_1").prop('checked', true);
            } else if (let_cod_modelo == 2) {
                $("#rd_modelo_conta_2").prop('checked', true);
            } else if (let_cod_modelo == 3) {
                $("#rd_modelo_conta_3").prop('checked', true);
            }


            $("#dt_ini_atv_benner").val(dados.dic_conta.data_ini_atividade);
            $("#dt_fim_atv_benner").val(dados.dic_conta.data_fim_atividade);
            $("#btn_cadastra_nova_conta").val(dados.dic_conta.cod_conta);
            let let_new_label_btn_cadastro_conta = `
                <i class="fa-solid fa-arrows-rotate"></i>Atualizar dados conta
            `;
            $("#btn_cadastra_nova_conta").html(let_new_label_btn_cadastro_conta);
            let let_btn_criar_nova_conta_manual = `
                <button type='button' name='btn_criar_nova_conta_manual'
                id='btn_criar_nova_conta_manual' class='mr-2 btn btn-primary btn-rounded cl_btn_cad_contas'>
                <i class="fa-solid fa-plus"></i>Criar conta
                </button>
            `;
            if(dados.usu_iscorporativo == 'S'){
                $("#div_btn_criar_nova_conta_manual").html(let_btn_criar_nova_conta_manual);
            }

            if (dados.dic_conta.status_comp == "A") {
                $("#chk_status_comp").prop('checked', true);
            } else {
                $("#chk_status_comp").prop('checked', false);
            }
            $("#btn_importar_contrato_benner").val(dados.dic_conta.cod_conta);
            $("#btn_refresh_dados_contratos").val(dados.dic_conta.cod_conta);
            $("#btn_cadastra_novo_contrato").val(dados.dic_conta.cod_conta);
            $("#btn_associar_responsaveis_conta").val(dados.dic_conta.cod_conta);
            $("#btn_anexa_doc_contrato").val(dados.dic_conta.cod_conta);
            $("#btn_importa_contrato_pelo_num").val(dados.dic_conta.cod_conta);
            $("#div_visualizacao_anexo_conta").html("");
            let_loader_frm_cad_contas.style.display = "none";
        },
        error: function (request, status, error) {
            let_loader_frm_cad_contas.style.display = "none";
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


function atualiza_tab_contratos_conta(cod_conta){
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/retorna_dados_contrato_conta_cadastrada',
        data: {
            'tipo_transacao'           :   'retornar_dados_cadastro',
            'num_contrato'          : 'todos',
            'cod_conta'   :    cod_conta
        },
        success: function (dados) {
            $("#div_contratos").html(dados);

            $(".display").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "60vh",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0]}
                    ],
                    "aaSorting": [[2, "asc"]],
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
            let_loader_frm_cad_contas.style.display = "none";
        },
        error: function (request, status, error) {
            let_loader_frm_cad_contas.style.display = "none";
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


function atualiza_tabela_resp_conta(cod_conta){
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_resp_associados_conta',
            data: {
                'cod_conta'   :   cod_conta
            },
            dataType: 'json',
            success: function (dados) {
                $("#tab_responsaveis_conta").DataTable().clear().draw();
                let let_lista_rep_conta = [];
                dados.lista_dic_resp_conta.forEach( resp => {
                    let let_btn_edita_resp = `
                        <button type='button' id='btn_editar_resp_conta_${resp.cod_resp_conta}'
                        name='btn_editar_resp_conta' value='${resp.cod_resp_conta}' class='btn btn-rounded btn-space'>
                            <i class="fa-solid fa-user-pen" style="color: #f46424;" ></i>
                        </button>
                    `;
                    let data_ini_atv = resp.data_ini_atividade.split('-')[2] + '-' +
                        resp.data_ini_atividade.split('-')[1] + '-' +
                        resp.data_ini_atividade.split('-')[0];

                    let data_fim_atv = resp.data_fim_atividade.split('-')[2] + '-' +
                        resp.data_fim_atividade.split('-')[1] + '-' +
                        resp.data_fim_atividade.split('-')[0];

                    let let_reg = [
                        ` <i class="fa-solid fa-user" style="color: #f46424;"></i>`,
                        resp.nome_empresa,
                        resp.resp_composicao + `<input type="hidden" id="hd_resp_comp_${resp.cod_resp_conta}" value="${resp.resp_composicao}">`,
                        resp.resp_validacao + `<input type="hidden" id="hd_resp_val_${resp.cod_resp_conta}" value="${resp.resp_validacao}">`,
                        resp.data_ini_atividade + `<input type="hidden" id="hd_data_ini_atv_${resp.cod_resp_conta}" value="` + data_ini_atv + `">`,
                        resp.data_fim_atividade + `<input type="hidden" id="hd_data_fim_atv_${resp.cod_resp_conta}" value="` + data_fim_atv + `">`,
                        let_btn_edita_resp
                    ];
                    let_lista_rep_conta.push(let_reg);
                });
                $('#tab_responsaveis_conta').DataTable( {
                    "bJQueryUI": true,
                    "pageLength": 10,
                    "destroy": true,
                    "searching": false,
                    "paging": false,
                    "data":let_lista_rep_conta,
                    "columns": [
                        { title: "" },
                        { title: "Empresa" },
                        { title: "Resp. composição" },
                        { title: "Resp. Validação" },
                        { title: "Inicio" },
                        { title: "Fim" },
                        { title: "Alterar" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [4, 5, 6]},
                        {"className": "dt-left", "targets": [1, 2, 3]}
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
                        }
                    }
                });
                let_loader_frm_cad_contas.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_frm_cad_contas.style.display = "none";
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


function atualiza_tab_anexos_conta(cod_conta){
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
        type : 'GET',
        data : {
            'cod_conta' : cod_conta
        },
        url: '/contabil_composicao_app/retorna_lista_anexos_conta',
        success: function(dados) {
            var_lista_docs = [];
            dados.lista_anexos.forEach( doc => {
                var var_btn_visualizar_anexo = `
                    <button type="button" name="btn_visulizar_anexo_conta"
                        id="btn_visulizar_anexo_conta_${doc.cod_anexo_contrato}"
                        class="btn btn-rounded btn-space"
                        value="${doc.caminho_anexo}">
                        <i class="fa-solid fa-magnifying-glass-plus" style="color: #f46424;"></i>
                    </button>
                `;
                var var_btn_exclui_anexo = `
                    <button type="button" name="btn_exclui_anexo_conta"
                        id="btn_exclui_anexo_conta_${doc.cod_anexo_contrato}"
                        class="btn btn-rounded btn-space"
                        value="${doc.cod_anexo_contrato}">
                        <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                    </button>
                `;
                if ( dados.status_corporativo_usu == 'N') {
                    var_btn_exclui_anexo = `
                        <button type="button" name="btn_exclui_anexo_conta"
                            id="btn_exclui_anexo_conta_${doc.cod_anexo_contrato}"
                            class="btn btn-rounded btn-space"
                            value="${doc.cod_anexo_contrato}" disabled>
                            <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                        </button>
                    `;
                }

                let let_num_contrato = ''
                if ( doc.cod_contrato__num_contrato != null ) {
                    let_num_contrato = doc.cod_contrato__num_contrato;
                }

                let let_competencia = doc.data_competencia.split('-')[2] + '-' +
                    doc.data_competencia.split('-')[1] + '-' +
                    doc.data_competencia.split('-')[0]


                reg = [
                    ` <i class="fa-solid fa-paperclip" style="color: #f46424"></i>`,
                    let_num_contrato,
                    let_competencia,
                    doc.desc_anexo,
                    var_btn_visualizar_anexo,
                    var_btn_exclui_anexo
                ];
                var_lista_docs.push(reg);
            });
            $("#tab_anexos_conta").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
                "destroy": true,
                "searching": false,
                "paging": true,
                "data":var_lista_docs,
                "columns": [
                    { title: "" },
                    { title: "Contrato" },
                    { title: "Competencia" },
                    { title: "Descrição" },
                    { title: "Visualizar" },
                    { title: "Excluir" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,2,3]},
                    {"className": "dt-left", "targets": [1]}
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

            $("#list_contratos_conta_anexo option").remove();
            dados.lista_contratos.forEach(contrato => {
                $("#list_contratos_conta_anexo").append("<option value='"+
                contrato.cod_contrato+"'>"+contrato.num_contrato+"</option>");

            });
            $("#list_contratos_conta_anexo").selectpicker('refresh');

            let_loader_frm_cad_contas.style.display = "none";
        },
        error: function(request, status, error){
            let_loader_frm_cad_contas.style.display = "none";
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


function atualiza_tab_status_contrato_composicao(cod_conta){
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
        type : 'GET',
        data : {
            'cod_conta' : cod_conta
        },
        url: '/contabil_composicao_app/retorna_lista_status_contrato_composicao',
        success: function(dados) {
            let let_lista_status = [];
            if(dados.lista_status_contratos_comp != null || dados.lista_status_contratos_comp == ''){
                dados.lista_status_contratos_comp.forEach( status => {
                let let_periodo_comp = status.data_competencia.split('-')[1] + '/' +
                     status.data_competencia.split('-')[0];
                let desc_status = ''
                if(status.status == '1'){
                    desc_status = 'OK';
                } else if(status.status == '2'){
                    desc_status = 'Com diferença';
                } else if(status.status == '3'){
                    desc_status = 'Falta analisar';
                } else if(status.status == '4'){
                    desc_status = 'Falta compor';
                }
                let let_reg = [
                    `<i class="fa-solid fa-caret-right" style="color: #f46424"></i>`,
                    status.cod_contrato__num_contrato,
                    status.tipo_prazo,
                    let_periodo_comp,
                    status.val_composicao,
                    status.val_balancete,
                    status.val_diferenca,
                    status.cod_usu__nome_usu,
                    desc_status,
                    status.obs_status
                ];
                let_lista_status.push(let_reg);
            });
                $("#tab_status_contrato_comp").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
                "destroy": true,
                "searching": false,
                "paging": false,
                "data":let_lista_status,
                "columns": [
                    { title: "" },
                    { title: "Contrato" },
                    { title: "Tipo Prazo" },
                    { title: "Competência" },
                    { title: "Composição" },
                    { title: "Balancete" },
                    { title: "Diferença" },
                    { title: "Usuário" },
                    { title: "Status" },
                    { title: "Observação" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [2, ]},
                    {"className": "dt-left", "targets": [0, 1, ]},
                    {"className": "dt-right", "targets": [ 3, 4, 5, 6,7,8, 9]}
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
            }

            let_loader_frm_cad_contas.style.display = "none";
        },
        error: function(request, status, error){
            let_loader_frm_cad_contas.style.display = "none";
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


function importa_contratos_parcela_conta(tipo_pesq, cod_conta, num_contrato){
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/retorna_dados_contrato_benner_conta',
        data: {
            'tipo_pesq'   :    tipo_pesq,
            'cod_conta'   :    cod_conta,
            'num_contrato':    num_contrato
        },
        dataType: 'json',
        success: function (dados) {
            let let_html_pagina = `
                <div class="d-flex flex-column align-items-start justify-content-start ml-2 w-100 accordion" id="acc_contratos">
            `;

            $("#list_contratos_conta_anexo option").remove();
            dados.lista_contratos.forEach( ctr => {
                let let_verifica_check_atualiza_benner = ``;
                if(ctr.contrato.atualiza_benner == 'SIM'){
                    let_verifica_check_atualiza_benner = `checked="checked"`;
                }

                $("#list_contratos_conta_anexo").append("<option value='"+
                ctr.contrato.cod_contrato+"'>"+ctr.contrato.num_contrato+"</option>");



                let_html_pagina += `
                    <div class="d-flex flex-column align-items-start justify-content-start ml-2 w-100 accordion-item">
                        <h2 class="d-flex flex-column align-items-start justify-content-start ml-2 w-100 accordion-header"
                            id="heading_${ctr.contrato.handle_fn_doc}">
                            <button class="accordion-button collapsed d-flex justify-content-between" type="button"
                                data-bs-toggle="collapse" data-bs-target="#collapse_${ctr.contrato.handle_fn_doc}"
                                aria-expanded="false" aria-controls="collapse_${ctr.contrato.handle_fn_doc}">
                                <div style="font-size:12px; width:80%">
                                    <div class="row">
                                        <div class="col-md-3">
                                            <i class="fa-solid fa-receipt" style="color: #f46424;"></i>
                                            <strong>Contrato:</strong> ${ctr.contrato.num_contrato}
                                        </div>
                                        <div class="col-md-3">
                                            <strong>Empresa:</strong> ${ctr.contrato.nome_empresa}
                                        </div>
                                        <div class="col-md-6" id="div_status_atualiza_benner">
                                            Atualiza com o Benner ? <strong>${ctr.contrato.atualiza_benner}</strong>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <strong>Produto:</strong> ${ctr.contrato.fornecedor}
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4">
                                            <strong>Data emissão:</strong> ${ctr.contrato.data_emissao_contrato}
                                        </div>
                                        <div class="col-md-4">
                                            <strong>Doc. Contábil:</strong> ${ctr.contrato.doc_contabil}
                                        </div>
                                        <div class="col-md-4">
                                            <strong>Operação:</strong> ${ctr.contrato.nome_operacao}
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-3" style="background-color:#87CEEB; color:#000000;">
                                            <strong>CONTA EM CURTO PRAZO</strong>
                                        </div>
                                    </div>
                                    <div class="row" style="background-color:#87CEEB; color:#000000;">
                                        <div class="col-md-4">
                                            <strong>Val. total líq.:</strong>${ctr.contrato.val_tt_liq_cp}
                                        </div>
                                        <div class="col-md-4">
                                            <strong>Val. total:</strong>${ctr.contrato.val_tt_contrato_reajustado_cp}
                                        </div>
                                        <div class="col-md-4">

                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-3" style="background-color:#0d6efd; color:#000000;">
                                            <strong>CONTA EM LONGO PRAZO</strong>
                                        </div>
                                    </div>
                                    <div class="row" style="background-color:#0d6efd; color:#000000;">
                                        <div class="col-md-4">
                                            <strong>Val. total líq.:</strong>${ctr.contrato.val_tt_liq_lp}
                                        </div>
                                        <div class="col-md-4">
                                            <strong>Val. total:</strong>${ctr.contrato.val_tt_contrato_reajustado_lp}
                                        </div>
                                        <div class="col-md-4">

                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-3" style="background-color:#f46424; color:#000000;">
                                            <strong>INFO TOTAIS CONTA</strong>
                                        </div>
                                    </div>
                                    <div class="row" style="background-color:#f46424; color:#000000;">
                                        <div class="col-md-3">
                                            <strong>Valor Total Líquido:</strong> ${ctr.contrato.val_liquido}
                                        </div>
                                        <div class="col-md-3">
                                            <strong>Valor Total Reajustado:</strong> ${ctr.contrato.val_tt_contrato_reajustado}
                                        </div>
                                        <div class="col-md-3">
                                            <strong>Total Liquidado:</strong> ${ctr.contrato.total_pago}
                                        </div>

                                    </div>
                                    <div class="row" style="background-color:#f46424; color:#000000;">
                                        <div class="col-md-3">
                                            <strong>Próxima parcela:</strong>${ctr.contrato.proxima_parc_pendente}
                                        </div>
                                        <div class="col-md-3">
                                            <strong>Venc. próxima parcela:</strong>
                                            ${ctr.contrato.data_venc_proxima_parc_pendente}
                                        </div>
                                        <div class="col-md-3">
                                            <strong>Valor próxima parcela:</strong>${ctr.contrato.val_proxima_parc_pendente}
                                        </div>
                                    </div>
                                </div>
                            </button>

                        </h2>

                        <div id="collapse_${ctr.contrato.handle_fn_doc}" class="accordion-collapse collapse"
                            aria-labelledby="heading_${ctr.contrato.handle_fn_doc}" data-bs-parent="#acc_contratos">
                        <div class="accordion-body flex-wrap d-flex justify-content-between align-items-center">
                            <div class="d-flex justify-content-between align-items-between w-100 mb-6">
                                <div class="d-flex flex-column w-100" style="margin-top: 2rem;">
                                    <button type='button' id="btn_excluir_contrato_${ctr.contrato.cod_contrato}"
                                            name="btn_excluir_contrato"
                                            class="mr-2 btn btn-primary btn-rounded cl_btn_excluir_contrato"
                                            value="${ctr.contrato.cod_contrato}">
                                        <i class="fa-solid fa-trash"></i>
                                        <span>Excluir contrato</span>
                                    </button>
                                </div>
                                <div class="d-flex flex-column w-100">
                                    <label class="col-form-label text-left cursor-pointer"
                                           for="chk_atualiza_dados_benner_contrato_${ctr.contrato.cod_contrato}">
                                        Atualiza com o Benner ?</label>
                                    <div class="container">
                                        <input type="checkbox" `+let_verifica_check_atualiza_benner+`  class="checkbox"
                                               name="chk_atualiza_dados_benner_contrato"
                                               id="chk_atualiza_dados_benner_contrato_${ctr.contrato.cod_contrato}">
                                        <label class="switch"
                                               for="chk_atualiza_dados_benner_contrato_${ctr.contrato.cod_contrato}">
                                            <span class="slider"></span>
                                        </label>
                                    </div>
                                </div>
                                <div class="d-flex flex-column w-100">
                                </div>
                                <div class="d-flex flex-column w-100">
                                </div>
                                <div class="d-flex flex-column w-100">
                                </div>
                                <div class="d-flex flex-column w-100">
                                </div>
                            </div>
                            <div class="d-flex mt-3 flex-column align-items-start justify-content-start w-100 cl_div_tabela_principal_pagina">
                                <div class="d-flex justify-content-between align-items-center ">
                                        <table id="tab_parcelas_contrato"  class="display wrap w-100 cl_tab_principal_pagina"
                                            style="font-size:12px; color: #000000;">
                                            <thead>
                                                <tr>
                                                    <th scope="col" align="left" style="color: grey"></th>
                                                    <th scope="col" align="left" style="color: grey">Vencimento</th>
                                                    <th scope="col" align="left" style="color: grey">Pagamento</th>
                                                    <th scope="col" align="left" style="color: grey">Núm. Parcela</th>
                                                    <th scope="col" align="left" style="color: grey">Tipo Prazo</th>
                                                    <th scope="col" align="left" style="color: grey">AP</th>
                                                    <th scope="col" align="left" style="color: grey">Val. Parcela</th>
                                                    <th scope="col" align="left" style="color: grey">Val. Principal</th>
                                                    <th scope="col" align="left" style="color: grey">Val. Taxas</th>
                                                    <th scope="col" align="left" style="color: grey">Val. Fundos</th>
                                                    <th scope="col" align="left" style="color: grey">Val. Total</th>
                                                    <th scope="col" align="left" style="color: grey">Val. Pago</th>
                                                    <th scope="col" align="left" style="color: grey">Liquidar</th>
                                                </tr>
                                            </thead>
                                            <tbody>`;

                        ctr.lista_parcelas_contrato.forEach( parc => {
                            let let_img = `<i class="fa-solid fa-check" style="color: #f46424;" title="Pago"></i>`;
                            let let_data_pagamento = `
                                <input type="date" id="dt_data_pag_parc_${parc.handle_parc}" readonly
                                value="${parc.data_liquidacao}">
                            `;
                            let let_valor_pago = `
                                <input type="text" id="txt_val_pag_parc_${parc.handle_parc}" readonly
                                value="${parc.val_total_pago}" style="width: 87.2px;text-align:right;">
                            `;
                            let let_btn_liquidar = `
                                <i class="fa-solid fa-receipt" style="color: #3CB371;"
                                            title="Pagamento Efetuado"></i>
                            `;
                            let let_readonly = 'readonly';
                            //if (parc.data_liquidacao == null || parc.data_liquidacao == '') {
                            if (parc.tipo_prazo != 'PG') {
                                let_readonly = '';
                                let_img = `
                                    <i class="fa-solid fa-triangle-exclamation" style="color: #f46424;" title="Pendente"></i>
                                `;
                                let_data_pagamento = `
                                    <input type="date" id="dt_data_pag_parc_${parc.handle_parc}">
                                `;
                                let_valor_pago = `
                                    <input type="text" id="txt_val_pag_parc_${parc.handle_parc}"
                                    style="width: 87.2px;text-align:right;" value="${parc.val_total_pago}">
                                `;
                                let_btn_liquidar = `
                                    <button type='button' name='btn_liquidar_parcela'
                                        id='btn_liquidar_parcela_${parc.handle_parc}' class='btn btn-rounded btn-space'
                                        value='${parc.handle_parc}'>
                                        <i class="fa-solid fa-receipt" style="color: #f46424;" title="Liquidar"></i>
                                    </button>
                                `;
                            }
                            let_html_pagina += `
                                <tr>
                                    <td>
                                   ` + let_img + `
                                   </td>
                                    <td>
                                        ${parc.data_vencimento}
                                    </td>
                                    <td>
                                    ` + let_data_pagamento + `
                                    </td>
                                    <td>
                                        ${parc.ordem_parcela}
                                    </td>
                                    <td>
                                        ${parc.tipo_prazo}
                                    </td>
                                    <td>
                                        ${parc.ap_parcela}
                                    </td>
                                    <td>
                                        <input type="text" `+ let_readonly +` id="txt_val_conta_${parc.handle_parc}"
                                        name="txt_val_conta" value="${parc.valor_conta}"
                                        style="width: 87.2px;text-align:right;">
                                    </td>
                                    <td>
                                        <input type="text" `+ let_readonly +` id="txt_val_principal_${parc.handle_parc}"
                                        name="txt_val_principal" value="${parc.valor_principal}"
                                        style="width: 87.2px;text-align:right;">
                                    </td>
                                    <td>
                                        <input type="text" `+ let_readonly +` id="txt_val_taxas_${parc.handle_parc}"
                                        name="txt_val_taxas" value="${parc.valor_taxas}"
                                        style="width: 87.2px;text-align:right;">
                                    </td>
                                    <td>
                                        <input type="text" `+ let_readonly +` id="txt_val_fundo_${parc.handle_parc}"
                                        name="txt_val_fundo" value="${parc.valor_fundo}"
                                        style="width: 87.2px;text-align:right;">
                                    </td>
                                    <td id="td_val_total_${parc.handle_parc}">
                                        ${parc.valor_total}
                                    </td>
                                    <td>
                                        ` + let_valor_pago + `
                                    </td>
                                    <td>
                                        ` + let_btn_liquidar + `
                                    </td>
                                </tr>
                            `;


                        });


                        let_html_pagina +=           `

                                            </tbody>
                                        </table>
                                </div>
                            </div>
                        </div>
                      </div>
                    </div>
                `;


                $("#list_contratos_conta_anexo").selectpicker('refresh');


            });
            let_html_pagina += `
                </div>
            `;
            $("#tab_parcelas_contrato").DataTable( {
                "bJQueryUI": true,
                "paging": false,
                //"pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": ['excelHtml5',
                            'pdfHtml5'
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
                    }
                }
            });
            $("#div_contratos").html(let_html_pagina);
            let_loader_frm_cad_contas.style.display = "none";
            $.gritter.add({
                title: 'Atenção!',
                text: dados.msg,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        },
        error: function (request, status, error) {
            let_loader_frm_cad_contas.style.display = "none";
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


function limpa_campos_form_cad_contas(){
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $("#txt_desc_conta").val("");

    $("#tx_handle_conta_cp").val("");
    $("#txt_cod_red_conta_cp").val("");
    $("#txt_cod_estrutura_cp").val("");

    $("#tx_handle_conta_lp").val("");
    $("#txt_cod_red_conta_lp").val("");
    $("#txt_cod_estrutura_lp").val("");

    $("#cb_pacote_conta").val("");
    $("#cb_pacote_conta").selectpicker("refresh");

    $("#dt_ini_atv_benner").val("");
    $("#dt_fim_atv_benner").val("");
    $("#chk_status_comp").prop("checked", "true");
    $("#div_contratos").html("");
    $("#cb_contas").val("");
    $("#cb_contas").selectpicker("refresh");
    //$("#div_btn_criar_nova_conta_manual").html("");

    let let_new_label_btn_cadastro_conta = `
        <i class="fa-solid fa-check" style="color: #f46424;"></i>Confirmar
    `;
    $("#btn_cadastra_nova_conta").html(let_new_label_btn_cadastro_conta);
    $("#btn_cadastra_nova_conta").val(0);
    $("#div_visualizacao_anexo_conta").html("");
    let_loader_frm_cad_contas.style.display = "none";

    $("#cb_resp_composicao").val("");
    $("#cb_resp_composicao").selectpicker("refresh");
    $("#cb_resp_validacao").val("");
    $("#cb_resp_validacao").selectpicker("refresh");
    $("#dt_ini_resp").val("");
    $("#dt_fim_resp").val("");
    let let_img_btn_atualizar_dados_resp = `
        <i class="fa-solid fa-plus" ></i>
    `;
    $("#btn_associar_responsaveis_conta").html(let_img_btn_atualizar_dados_resp + "Associar responsáveis");
    $("#btn_associar_responsaveis_conta").val(0);




}


function gera_conciliacao_comp_benner_detalhado(){
    let let_cod_conta = $("#cb_contas_conciliacao_comp_benner").val().toString();
    let let_competencia = $("#dt_conciliacao_comp_benner").val();
    let let_status_analise = $("#cb_status_analise_conciliacao_detalhada").val();

    let cod_modelo_selecionado = 0;
    if ( $("#rd_modelo_conta_conc_comp_benner_1").is(':checked') == true){
        cod_modelo_selecionado = 1;
    } else if ( $("#rd_modelo_conta_conc_comp_benner_2").is(':checked') == true){
        cod_modelo_selecionado = 2;
    } else if ( $("#rd_modelo_conta_conc_comp_benner_3").is(':checked') == true){
        cod_modelo_selecionado = 3;
    }

    let let_loader_gera_comp_det = document.getElementById("loader_gera_comp_det");
    let_loader_gera_comp_det.style.display = "flex";
    $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/gera_conciliacao_comp_benner',
            data: {
                'cod_modelo_selecionado' : cod_modelo_selecionado,
                'cod_conta'     :   let_cod_conta,
                'competencia'   :   let_competencia,
                'cod_status_analise':   let_status_analise,
                'tipo_visualizacao' :   'D'
            },
            dataType: 'json',
            success: function (data) {
                $("#tab_conciliacao_composicao_benner_detalhado").dataTable().fnClearTable();
                $("#tab_conciliacao_composicao_benner_detalhado").dataTable().fnDestroy();
                const tabela = new DataTable("#tab_conciliacao_composicao_benner_detalhado");

                let let_lista_dados_conciliacao = [];
                let let_lista_dados = [];
                for (var i = 0; i < data.lista_contas_conciliacao.length; i++) {
                    let let_img = `
                        <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                    `;
                    let let_desc_status_comp = '';
                    let option_0 = '';
                    let option_1 = '';
                    let option_2 = '';
                    let option_3 = '';
                    let option_4 = '';
                    let let_img_btn_status = '';



                    let_btn_status = '';
                    if( cod_modelo_selecionado == 1 ) {

                        if(data.lista_contas_conciliacao[i][7] == 0) { //cod_status_auditoria_comp
                            option_0 = `selected="selected"`;
                            let_desc_status_comp = `title='Sem status informado'`
                            let_img_btn_status = `<i class="fa-solid fa-triangle-exclamation fa-xl" style="color:#FFFF00;" title='Sem status informado'></i>`
                        } else if(data.lista_contas_conciliacao[i][7] == 1) {
                            let_desc_status_comp = `title='Status: OK / Obs.: ${data.lista_contas_conciliacao[i][8]}'`;
                            option_1 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-check fa-xl" style="color:#2E8B57;" title='Status: OK / Obs.: ${data.lista_contas_conciliacao[i][8]}'></i>`;
                        } else if(data.lista_contas_conciliacao[i][7] == 2) {
                            let_desc_status_comp = `title='Status: Com diferença / Obs.: ${data.lista_contas_conciliacao[i][8]}'`;
                            option_2 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-not-equal fa-xl" style="color:#FF0000;" title='Status: Com diferença / Obs.: ${data.lista_contas_conciliacao[i][8]}'></i>`;
                        } else if(data.lista_contas_conciliacao[i][7] == 3) {
                            let_desc_status_comp = `title='Status: Falta analisar / Obs.: ${data.lista_contas_conciliacao[i][8]}'`;
                            option_3 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-arrows-rotate fa-xl" title='Status: Falta analisar / Obs.: ${data.lista_contas_conciliacao[i][8]}'></i>`;
                        } else if(data.lista_contas_conciliacao[i][7] == 4) {
                            let_desc_status_comp = `title='Status: Falta compor / Obs.: ${data.lista_contas_conciliacao[i][8]}'`;
                            option_4 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-bolt fa-xl" style="color:#808080;" title='Status: Falta compor / Obs.: ${data.lista_contas_conciliacao[i][8]}'></i>`;
                        }
                        let let_btn_detalhes_conta = `
                            <button type='button' id="btn_detalhes_conta_${data.lista_contas_conciliacao[i][0]} "
                                    name="btn_detalhes_conta"
                                    class="btn btn-rounded btn-space"
                                    value="${data.lista_contas_conciliacao[i][0]}"
                                    title="${data.lista_contas_conciliacao[i][3]}">
                                <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                            </button>

                        `;
                        let let_btn_visualiza_doc = `<i class="fa-solid fa-eye-slash" style="color: #f46424;"
                            title='Não há Documento Anexado'></i>`;
                        if(data.lista_contas_conciliacao[i][9] != '0'){
                            let_btn_visualiza_doc = `
                                <button type='button' name='btn_visualiza_doc_contrato'
                                    id='btn_visualiza_doc_contrato_${data.lista_contas_conciliacao[i][9]}'
                                    class='btn btn-rounded btn-space'
                                    value='${data.lista_contas_conciliacao[i][9]}' title='Visualizar Documento Anexado'>
                                    <i class="fa-solid fa-eye" style="color: #f46424;"></i>
                                </button>
                            `;
                        }

                        let_btn_status = `
                            <div class="btn-group dropleft" >
                              <button type="button" class="btn btn-rounded btn-space"
                                id="btn_status_comp_m1_${data.lista_contas_conciliacao[i][0]}"
                                name="btn_status_comp"
                                aria-haspopup="true" aria-expanded="false"
                                data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false"
                                ` + let_desc_status_comp + `>
                                <i class="fa-solid fa-caret-down" style="color: #f46424;"></i>
                              </button>
                              <div class="dropdown-menu" style="box-shadow: 2px 2px 2px 1px rgba(0, 0, 0.7, 0.7); background:#f46424;">
                              <div class="d-flex justify-content-between align-items-between w-100" style="font-size: 0.75rem; color: #ffffff;">
                                    Status composição
                                    <i class="fa-solid fa-thumbtack fa-sm" style="color: #ffffff;margin-top: 0.1rem;margin-right: 0.3rem;"></i>
                                </div>
                                <form id="frm_status_conciliacao" name="frm_status_conciliacao"  method="POST"
                                class="d-flex flex-column align-items-center justify-content-between">
                                    <div class="d-flex justify-content-between align-items-between w-100 cl_comp_drop_status_comp">
                                        <select class="form-select form-select-sm" id="cb_status_conciliacao_m1_${data.lista_contas_conciliacao[i][0]}"
                                            name="cb_status_conciliacao"
                                            style="color: #000000; font-size: 11px">
                                                <option value="0" `+ option_0 +`>Selecione o status</option>
                                                <option value="1" `+ option_1 +`>OK</option>
                                                <option value="2" `+ option_2 +`>Com diferença</option>
                                                <option value="3" `+ option_3 +`>Falta analisar</option>
                                                <option value="4" `+ option_4 +`>Falta compor</option>
                                        </select>
                                    </div>
                                    <div class="d-flex justify-content-between align-items-between w-100 cl_comp_drop_status_comp">
                                        <input type="text" class="form-control" id="ta_obs_status_conciliacao_m1_${data.lista_contas_conciliacao[i][0]}"
                                            style="color: #000000; font-size: 11px;text-align: left;white-space: nowrap;width: 100%; height:70px;"
                                            name="ta_obs_status_conciliacao"
                                            autocomplete="off" placeholder="Observação" rows="3"
                                            value="${data.lista_contas_conciliacao[i][8]}">

                                    </div>
                                    <div class="d-flex justify-content-end w-100 mr-3 cl_div_conf_status_comp" >
                                        <button type='button' name='btn_confirma_status_composicao'
                                            id='btn_confirma_status_composicao_m1_${data.lista_contas_conciliacao[i][0]}'
                                            class='btn btn-rounded btn-space cl_btn_conf_status_comp'
                                            value='m1_${data.lista_contas_conciliacao[i][0]}' title='${data.lista_contas_conciliacao[i][3]}'>
                                            <i class="fa-solid fa-check" style="color: #ffffff;"></i>
                                        </button>
                                    </div>
                                </form>
                              </div>
                            </div>
                        `;

                        let_reg = [
                            /* 0 - cod_estrutura */let_img_btn_status + ' ' + data.lista_contas_conciliacao[i][2],
                            /* 1 - cod_red */ data.lista_contas_conciliacao[i][1],
                            /* 2 - desc_conta */ data.lista_contas_conciliacao[i][3],
                            /* 6 - val_comp */ data.lista_contas_conciliacao[i][4] + `<input type="hidden" id="txt_val_composicao_m1_${data.lista_contas_conciliacao[i][0]}" readonly value="${data.lista_contas_conciliacao[i][4]}" style="text-align: right;"/>`,
                            /* 7 - val_balancete */ data.lista_contas_conciliacao[i][5] + `<input type="hidden" id="txt_val_balancete_m1_${data.lista_contas_conciliacao[i][0]}" readonly value="${data.lista_contas_conciliacao[i][5]}" style="text-align: right;"/>`,
                            /* 8 -val_dif_comp_balanc */ data.lista_contas_conciliacao[i][6] +`<input type="hidden" id="txt_val_diferenca_m1_${data.lista_contas_conciliacao[i][0]}" readonly value="${data.lista_contas_conciliacao[i][6]}" style="text-align: right;"/>`,
                            /* 9 */let_btn_status,
                            /* 10 */let_btn_detalhes_conta,
                            /* 11 */let_btn_visualiza_doc
                        ];
                        let_lista_dados.push(let_reg);
                    }
                    else if( cod_modelo_selecionado == 3 ) {

                        if(data.lista_contas_conciliacao[i][11] == 0) { //cod_status_auditoria_comp
                            option_0 = `selected="selected"`;
                            let_desc_status_comp = `title='Sem status informado'`
                            let_img_btn_status = `<i class="fa-solid fa-triangle-exclamation fa-xl" style="color:#FFFF00;" title='Sem status informado'></i>`
                        } else if(data.lista_contas_conciliacao[i][11] == 1) {
                            let_desc_status_comp = `title='Status: OK / Obs.: ${data.lista_contas_conciliacao[i][12]}'`;
                            option_1 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-check fa-xl" style="color:#2E8B57;" title='Status: OK / Obs.: ${data.lista_contas_conciliacao[i][12]}'></i>`;
                        } else if(data.lista_contas_conciliacao[i][11] == 2) {
                            let_desc_status_comp = `title='Status: Com diferença / Obs.: ${data.lista_contas_conciliacao[i][12]}'`;
                            option_2 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-not-equal fa-xl" style="color:#FF0000;" title='Status: Com diferença / Obs.: ${data.lista_contas_conciliacao[i][12]}'></i>`;
                        } else if(data.lista_contas_conciliacao[i][11] == 3) {
                            let_desc_status_comp = `title='Status: Falta analisar / Obs.: ${data.lista_contas_conciliacao[i][12]}'`;
                            option_3 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-arrows-rotate fa-xl" title='Status: Falta analisar / Obs.: ${data.lista_contas_conciliacao[i][12]}'></i>`;
                        } else if(data.lista_contas_conciliacao[i][11] == 4) {
                            let_desc_status_comp = `title='Status: Falta compor / Obs.: ${data.lista_contas_conciliacao[i][12]}'`;
                            option_4 = 'selected="selected"';
                            let_img_btn_status = `<i class="fa-solid fa-bolt fa-xl" style="color:#808080;" title='Status: Falta compor / Obs.: ${data.lista_contas_conciliacao[i][12]}'></i>`;
                        }
                        let let_btn_detalhes_conta = `
                            <button type='button' id="btn_detalhes_conta_${data.lista_contas_conciliacao[i][0]} "
                                    name="btn_detalhes_conta"
                                    class="btn btn-rounded btn-space"
                                    value="${data.lista_contas_conciliacao[i][0]}_${data.lista_contas_conciliacao[i][5]}"
                                    title="${data.lista_contas_conciliacao[i][3]}">
                                <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                            </button>

                        `;
                        let let_btn_visualiza_doc = `<i class="fa-solid fa-eye-slash" style="color: #f46424;"
                            title='Não há Documento Anexado'></i>`;
                        if(data.lista_contas_conciliacao[i][13] != '0'){
                            let_btn_visualiza_doc = `
                                <button type='button' name='btn_visualiza_doc_contrato'
                                    id='btn_visualiza_doc_contrato_${data.lista_contas_conciliacao[i][13]}'
                                    class='btn btn-rounded btn-space'
                                    value='${data.lista_contas_conciliacao[i][13]}' title='Visualizar Documento Anexado'>
                                    <i class="fa-solid fa-eye" style="color: #f46424;"></i>
                                </button>
                            `;
                        }

                        let_btn_status = `
                            <div class="btn-group dropleft" >
                              <button type="button" class="btn btn-rounded btn-space"
                                id="btn_status_comp_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}"
                                name="btn_status_comp"
                                aria-haspopup="true" aria-expanded="false"
                                data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false"
                                ` + let_desc_status_comp + `>
                                <i class="fa-solid fa-caret-down" style="color: #f46424;"></i>
                              </button>
                              <div class="dropdown-menu" style="box-shadow: 2px 2px 2px 1px rgba(0, 0, 0.7, 0.7); background:#f46424;">
                              <div class="d-flex justify-content-between align-items-between w-100" style="font-size: 0.75rem; color: #ffffff;">
                                    Status composição
                                    <i class="fa-solid fa-thumbtack fa-sm" style="color: #ffffff;margin-top: 0.1rem;margin-right: 0.3rem;"></i>
                                </div>
                                <form id="frm_status_conciliacao" name="frm_status_conciliacao"  method="POST"
                                class="d-flex flex-column align-items-center justify-content-between">
                                    <div class="d-flex justify-content-between align-items-between w-100 cl_comp_drop_status_comp">
                                        <select class="form-select form-select-sm" id="cb_status_conciliacao_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}"
                                            name="cb_status_conciliacao"
                                            style="color: #000000; font-size: 11px">
                                                <option value="0" `+ option_0 +`>Selecione o status</option>
                                                <option value="1" `+ option_1 +`>OK</option>
                                                <option value="2" `+ option_2 +`>Com diferença</option>
                                                <option value="3" `+ option_3 +`>Falta analisar</option>
                                                <option value="4" `+ option_4 +`>Falta compor</option>
                                        </select>
                                    </div>
                                    <div class="d-flex justify-content-between align-items-between w-100 cl_comp_drop_status_comp">
                                        <input type="text" class="form-control" id="ta_obs_status_conciliacao_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}"
                                            style="color: #000000; font-size: 11px;text-align: left;white-space: nowrap;width: 100%; height:70px;"
                                            name="ta_obs_status_conciliacao"
                                            autocomplete="off" placeholder="Observação" rows="3"
                                            value="${data.lista_contas_conciliacao[i][12]}">

                                    </div>
                                    <div class="d-flex justify-content-end w-100 mr-3 cl_div_conf_status_comp" >
                                        <button type='button' name='btn_confirma_status_composicao'
                                            id='btn_confirma_status_composicao_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}'
                                            class='btn btn-rounded btn-space cl_btn_conf_status_comp'
                                            value='${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}'
                                            title='${data.lista_contas_conciliacao[i][3]}-${data.lista_contas_conciliacao[i][10]}'>
                                            <i class="fa-solid fa-check" style="color: #ffffff;"></i>
                                        </button>
                                    </div>
                                </form>
                              </div>
                            </div>
                        `;

                        let_reg = [
                            /* 0 - cod_estrutura */let_img_btn_status + '&nbsp;&nbsp;&nbsp;&nbsp;' + data.lista_contas_conciliacao[i][2],
                            /* 1 - cod_red */ data.lista_contas_conciliacao[i][1],
                            /* 2 - desc_conta */ data.lista_contas_conciliacao[i][3],
                            /* 3 - num_contrato */ data.lista_contas_conciliacao[i][5] ,
                            /* 4 - doc_contabil */ data.lista_contas_conciliacao[i][6],
                            /* 5 - tipo_prazo */ data.lista_contas_conciliacao[i][10],
                            /* 6 - val_comp */ data.lista_contas_conciliacao[i][7] +
                                `<input type="hidden" id="txt_val_composicao_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}"
                                readonly value="${data.lista_contas_conciliacao[i][7]}" style="text-align: right;"/>`,
                            /* 7 - val_balancete */ data.lista_contas_conciliacao[i][8]+
                                `<input type="hidden" id="txt_val_balancete_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}"
                                readonly value="${data.lista_contas_conciliacao[i][8]}" style="text-align: right;"/>`,
                            /* 8 - val_dif_comp_balanc */ data.lista_contas_conciliacao[i][9]+`<input type="hidden"
                                id="txt_val_diferenca_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}"
                                readonly value="${data.lista_contas_conciliacao[i][9]}" style="text-align: right;"/>`,
                            /* 9 */let_btn_status,
                            /* 10 */let_btn_detalhes_conta,
                            /* 11 */let_btn_visualiza_doc
                        ];
                        let_lista_dados.push(let_reg);
                    }
                    /*
                    tabela.row
                        .add(let_reg)
                        .draw(false);
                        */
                }
                $("#tab_conciliacao_composicao_benner_detalhado").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": '770px', //770px "100vh"
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    //"pageLength": 7,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0]}
                    ],
                    "data":let_lista_dados,
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
                } );
                let_loader_gera_comp_det.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_gera_comp_det.style.display = "none";
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


$(document).on('change', '#cb_responsaveis_contas', function(){
    let let_radio1 = $("#rd_modelo_conta_1").prop('checked');
    let let_radio2 = $("#rd_modelo_conta_2").prop('checked');
    let let_radio3 = $("#rd_modelo_conta_3").prop('checked');
    let let_cod_modelo_conta = 0;
    if ( let_radio1 == true ){
        let_cod_modelo_conta = 1;
    } else if ( let_radio2 == true ){
        let_cod_modelo_conta = 2;
    } else if ( let_radio3 == true ){
        let_cod_modelo_conta = 3;
    }

    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/povoa_cb_contas_conciliacao_comp_benner',
        data: {
            'tipo_rel'           :  'P',
            'cod_modelo_conta'   :  let_cod_modelo_conta,
            'nome_resp'          :  $("#cb_responsaveis_contas").val().toString()

        },
        dataType: 'json',
        success: function (data) {
            $("#cb_contas option").remove();
            data.lista_contas.forEach(conta => {
                $("#cb_contas").append("<option value='"+
                conta.cod_conta+"'>"+conta.cod_conta+" - "+conta.desc_conta+" - Cód. red. CP - "+conta.cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_red_conta_contabil_lp+"</option>");

            });
            $("#cb_contas").selectpicker('refresh');
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

});


function desenha_frm_cad_contas_conforme_tipo_modelo(let_cod_modelo_conta){

    if (let_cod_modelo_conta == 1) {
        $("#div_titulo_dados_curto_prazo").html(`
            <i class="fa-solid fa-arrow-right-to-bracket" style="color: #f46424;"></i>
            DADOS CONTA CONTÁBIL
        `);
        $("#div_hr_curto_prazo").html(`
            <hr class="hr_title">
        `);
        $("#div_dados_curto_prazo").html(`
            <div class="d-flex flex-column w-100 cl_div_tx_handle_conta_cp">
                <label>
                    Handle
                    <input type="text" id="tx_handle_conta_cp"
                           name="tx_handle_conta_cp" class="form-control">
                </label>
            </div>

            <div class="d-flex flex-column w-100 cl_div_txt_cod_red_conta_cp">
                <label>
                    Código Reduzido
                    <input type="text" id="txt_cod_red_conta_cp"
                           name="txt_cod_red_conta_cp" class="form-control" >
                </label>
            </div>

            <div class="d-flex flex-column w-100 cl_div_txt_cod_estrutura_cp">
                <label>
                    Estrutura
                    <input type="text" class="form-control"
                           id="txt_cod_estrutura_cp" name="txt_cod_estrutura_cp">
                </label>
            </div>
        `);

        $("#div_titulo_dados_longo_prazo").html("");
        $("#div_hr_longo_prazo").html("");
        $("#div_dados_longo_prazo").html("");


        let let_html_btn = `
            <i class="fa-solid fa-file-signature" style="color: #f46424;"></i>Documentos
        `;
        $("#a_tab_contratos").html(let_html_btn);
        $("#div_tab_contratos").html("");
        $("#div_tab_contratos").html(`
            <div id="div_tab_doc_contas_modelo_1" class="form-group  cl_div_tabela_principal_pagina w-100">
                <table id="tab_arq_conta_mod_1"  class="display wrap w-100 cl_tab_principal_pagina">
                    <thead>
                        <tr>
                            <th scope="col"></th>
                            <th scope="col">Importado em:</th>
                            <th scope="col">Nome arquivo</th>
                            <th scope="col">Qtd. registros</th>
                            <th scope="col">Competência</th>
                            <th scope="col">Usuario</th>
                            <th scope="col">Val. relatório(R$)</th>
                            <th scope="col">Val. razão(R$)</th>
                            <th scope="col">Excluir</th>
                          </tr>
                    </thead>
                    <tbody>

                    </tbody>

                </table>

            </div>
        `);

    }
    else if (let_cod_modelo_conta == 2) {
        $("#div_titulo_dados_curto_prazo").html("");
        $("#div_hr_curto_prazo").html("");
        $("#div_dados_curto_prazo").html("");

        $("#div_titulo_dados_longo_prazo").html("");
        $("#div_hr_longo_prazo").html("");
        $("#div_dados_longo_prazo").html("");

        $("#li_cad_conta_2").html("");
        $("#div_tab_contratos").html("");

    }
    else if (let_cod_modelo_conta == 3 ) {
        $("#div_titulo_dados_curto_prazo").html(`
            <i class="fa-solid fa-arrow-right-to-bracket" style="color: #f46424;"></i>
            DADOS CONTA CONTÁBIL CURTO PRAZO
        `);
        $("#div_hr_curto_prazo").html(`
            <hr class="hr_title">
        `);
        $("#div_dados_curto_prazo").html(`
            <div class="d-flex flex-column w-100 cl_div_tx_handle_conta_cp">
                <label>
                    Handle C.P.
                    <input type="text" id="tx_handle_conta_cp"
                           name="tx_handle_conta_cp" class="form-control">
                </label>
            </div>

            <div class="d-flex flex-column w-100 cl_div_txt_cod_red_conta_cp">
                <label>
                    Código Reduzido C.P.
                    <input type="text" id="txt_cod_red_conta_cp"
                           name="txt_cod_red_conta_cp" class="form-control" >
                </label>
            </div>

            <div class="d-flex flex-column w-100 cl_div_txt_cod_estrutura_cp">
                <label>
                    Estrutura C.P.
                    <input type="text" class="form-control"
                           id="txt_cod_estrutura_cp" name="txt_cod_estrutura_cp">
                </label>
            </div>
        `);

        $("#div_titulo_dados_longo_prazo").html(`
            <i class="fa-solid fa-arrow-right-from-bracket" style="color: #f46424;"></i>
            DADOS CONTA CONTÁBIL LONGO PRAZO
        `);
        $("#div_hr_longo_prazo").html(`
            <hr class="hr_title">
        `);
        $("#div_dados_longo_prazo").html(`
            <div class="d-flex flex-column w-100 cl_div_tx_handle_conta_lp">
                <label>
                    Handle L.P.
                    <input type="text" id="tx_handle_conta_lp"
                           name="tx_handle_conta_lp" class="form-control">
                </label>
            </div>

            <div class="d-flex flex-column w-100 cl_div_txt_cod_red_conta_lp">
                <label>
                    Código Reduzido L.P.
                    <input type="text" id="txt_cod_red_conta_lp"
                           name="txt_cod_red_conta_lp" class="form-control" >
                </label>
            </div>

            <div class="d-flex flex-column w-100 cl_div_txt_cod_estrutura_lp">
                <label>
                    Estrutura L.P.
                    <input type="text" class="form-control"
                           id="txt_cod_estrutura_lp" name="txt_cod_estrutura_lp">
                </label>
            </div>
        `);

         let let_html_btn = `
            <i class="fa-solid fa-file-signature" style="color: #f46424;"></i>Contratos
        `;
        $("#a_tab_contratos").html(let_html_btn);

        $("#div_tab_contratos").html("");
        $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/acessa_frm_cad_contratos',
        data: {
            'tipo_transacao'           :   'cadastro'
        },
        success: function (data) {
            $("#div_tab_contratos").html(data);
        },
        error: function (request, status, error) {
            $.gritter.add({
                title: 'Atenção!',
                text: "Erro ao carregar form contratos",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
      }
    });

    }

    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/povoa_cb_contas_conciliacao_comp_benner',
        data: {
            'tipo_rel'           :  'C',
            'cod_modelo_conta'   :  let_cod_modelo_conta,
            'nome_resp'          :  $("#cb_responsaveis_contas").val().toString()

        },
        dataType: 'json',
        success: function (data) {
            $("#cb_contas option").remove();
            data.lista_contas.forEach(conta => {
                $("#cb_contas").append("<option value='"+
                conta.cod_conta+"'>"+conta.cod_conta+" - "+conta.desc_conta+" - Cód. red. CP - "+conta.cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_red_conta_contabil_lp+"</option>");

            });
            $("#cb_contas").selectpicker('refresh');

            $("#cb_pacote_conta option").remove();
            data.lista_pacotes_conta.forEach(pac => {
                $("#cb_pacote_conta").append("<option value='"+
                pac.cod_pacote_conta+"'>"+pac.desc_pacote_conta+"</option>");

            });
            $("#cb_pacote_conta").selectpicker('refresh');

            $("#sl_contas_atualiza_contratos_benner option").remove();
            data.lista_contas_para_atualizar_benner.forEach( conta => {
                $("#sl_contas_atualiza_contratos_benner").append("<option value='"+
                conta.cod_conta__cod_conta+"'>"+conta.cod_conta__cod_conta+" - "+conta.cod_conta__desc_conta+
                " - Cód. red. CP - "+conta.cod_conta__cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_conta__cod_red_conta_contabil_lp+"</option>");
            });
            $("#sl_contas_atualiza_contratos_benner").selectpicker('refresh');


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


function atualiza_doc_contas_modelo_1(cod_conta){
    $("#div_tab_doc_contas_modelo_1").html("");
    let let_loader_frm_cad_contas = document.getElementById("loader_frm_cad_contas");
    let_loader_frm_cad_contas.style.display = "flex";
    $.ajax({
        type : 'GET',
        data : {
            'competencia': 'todas',
            'cod_conta' : cod_conta
        },
        url: '/contabil_composicao_app/retorna_lista_docs_contas_modelo_1',
        success: function(dados) {
            $("#div_tab_doc_contas_modelo_1").html(dados);

            let_loader_frm_cad_contas.style.display = "none";
        },
        error: function(request, status, error){
            let_loader_frm_cad_contas.style.display = "none";
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


function gera_conciliacao_comp_benner_auditoria(){
    let let_cod_conta = $("#cb_contas_conciliacao_comp_benner").val().toString();
    let let_competencia = $("#dt_conciliacao_comp_benner").val();

    let cod_modelo_selecionado = 0;
    if ( $("#rd_modelo_conta_conc_comp_benner_1").is(':checked') == true){
        cod_modelo_selecionado = 1;
    } else if ( $("#rd_modelo_conta_conc_comp_benner_2").is(':checked') == true){
        cod_modelo_selecionado = 2;
    } else if ( $("#rd_modelo_conta_conc_comp_benner_3").is(':checked') == true){
        cod_modelo_selecionado = 3;
    }

    if ( let_cod_conta == '' ) {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Nenhuma conta selecionada',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        let let_loader_comp_aud = document.getElementById("loader_comp_aud");
        let_loader_comp_aud.style.display = "flex";
        $.ajax({
                type: 'GET',
                url: '/contabil_composicao_app/gera_conciliacao_comp_benner',
                data: {
                    'cod_modelo_selecionado' : cod_modelo_selecionado,
                    'cod_conta'     :   let_cod_conta,
                    'competencia'   :   let_competencia,
                    'tipo_visualizacao' :   'A'
                },
                dataType: 'json',
                success: function (data) {
                    $("#tab_conciliacao_composicao_benner_aud").dataTable().fnClearTable();
                    $("#tab_conciliacao_composicao_benner_aud").dataTable().fnDestroy();
                    //const tabela = new DataTable("#tab_conciliacao_composicao_benner_aud");

                    let let_lista_dados_conciliacao = [];
                    let let_lista_dados = [];
                    for (var i = 0; i < data.lista_contas_conciliacao.length; i++) {
                        let let_img = `
                            <i class="fa-solid fa-caret-right" style="color: #f46424;"></i>
                        `;

                        if( cod_modelo_selecionado == 1 ) {

                            let let_btn_detalhes_conta = `
                                <button type='button' id="btn_detalhes_conta_${data.lista_contas_conciliacao[i][0]} "
                                        name="btn_detalhes_conta"
                                        class="btn btn-rounded btn-space"
                                        value="${data.lista_contas_conciliacao[i][0]}"
                                        title="${data.lista_contas_conciliacao[i][3]}">
                                    <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                                </button>

                            `;
                            let let_btn_visualiza_doc = `<i class="fa-solid fa-eye-slash" style="color: #f46424;"
                                title='Não há Documento Anexado'></i>`;
                            if(data.lista_contas_conciliacao[i][7] != '0'){
                                let_btn_visualiza_doc = `
                                    <button type='button' name='btn_visualiza_doc_contrato'
                                        id='btn_visualiza_doc_contrato_${data.lista_contas_conciliacao[i][7]}'
                                        class='btn btn-rounded btn-space'
                                        value='${data.lista_contas_conciliacao[i][7]}' title='Visualizar Documento Anexado'>
                                        <i class="fa-solid fa-eye" style="color: #f46424;"></i>
                                    </button>
                                `;
                            }

                            let_reg = [
                                /* 0 - cod_estrutura */let_img + ' ' + data.lista_contas_conciliacao[i][2],
                                /* 1 - cod_red */ data.lista_contas_conciliacao[i][1],
                                /* 2 - desc_conta */ data.lista_contas_conciliacao[i][3],
                                /* 6 - val_comp */ data.lista_contas_conciliacao[i][4] + `<input type="hidden" id="txt_val_composicao_m1_${data.lista_contas_conciliacao[i][0]}" readonly value="${data.lista_contas_conciliacao[i][4]}" style="text-align: right;"/>`,
                                /* 7 - val_balancete */ data.lista_contas_conciliacao[i][5] + `<input type="hidden" id="txt_val_balancete_m1_${data.lista_contas_conciliacao[i][0]}" readonly value="${data.lista_contas_conciliacao[i][5]}" style="text-align: right;"/>`,
                                /* 8 -val_dif_comp_balanc */ data.lista_contas_conciliacao[i][6] +`<input type="hidden" id="txt_val_diferenca_m1_${data.lista_contas_conciliacao[i][0]}" readonly value="${data.lista_contas_conciliacao[i][6]}" style="text-align: right;"/>`,
                                /* 10 */let_btn_detalhes_conta,
                                /* 11 */let_btn_visualiza_doc
                            ];
                            let_lista_dados.push(let_reg);
                        }
                        else if( cod_modelo_selecionado == 3 ) {

                            let let_btn_detalhes_conta = `
                                <button type='button' id="btn_detalhes_conta_${data.lista_contas_conciliacao[i][0]} "
                                        name="btn_detalhes_conta"
                                        class="btn btn-rounded btn-space"
                                        value="${data.lista_contas_conciliacao[i][0]}_${data.lista_contas_conciliacao[i][5]}"
                                        title="${data.lista_contas_conciliacao[i][3]}">
                                    <i class="fa-solid fa-magnifying-glass" style="color: #f46424;"></i>
                                </button>

                            `;
                            let let_btn_visualiza_doc = `<i class="fa-solid fa-eye-slash" style="color: #f46424;"
                                title='Não há Documento Anexado'></i>`;
                            if(data.lista_contas_conciliacao[i][11] != '0'){
                                let_btn_visualiza_doc = `
                                    <button type='button' name='btn_visualiza_doc_contrato'
                                        id='btn_visualiza_doc_contrato_${data.lista_contas_conciliacao[i][11]}'
                                        class='btn btn-rounded btn-space'
                                        value='${data.lista_contas_conciliacao[i][11]}' title='Visualizar Documento Anexado'>
                                        <i class="fa-solid fa-eye" style="color: #f46424;"></i>
                                    </button>
                                `;
                            }

                            let_reg = [
                                /* 0 - cod_estrutura */let_img + ' ' + data.lista_contas_conciliacao[i][2],
                                /* 1 - cod_red */ data.lista_contas_conciliacao[i][1],
                                /* 2 - desc_conta */ data.lista_contas_conciliacao[i][3],
                                /* 3 - num_contrato */ data.lista_contas_conciliacao[i][5],
                                /* 4 - doc_contabil */ data.lista_contas_conciliacao[i][6],
                                /* 5 - tipo_prazo */ data.lista_contas_conciliacao[i][10],
                                /* 6 - val_comp */ data.lista_contas_conciliacao[i][7] + `<input type="hidden" id="txt_val_composicao_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}" readonly value="${data.lista_contas_conciliacao[i][7]}" style="text-align: right;"/>`,
                                /* 7 - val_balancete */ data.lista_contas_conciliacao[i][8]+ `<input type="hidden" id="txt_val_balancete_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}" readonly value="${data.lista_contas_conciliacao[i][8]}" style="text-align: right;"/>`,
                                /* 8 - val_dif_comp_balanc */ data.lista_contas_conciliacao[i][9]+`<input type="hidden" id="txt_val_diferenca_${data.lista_contas_conciliacao[i][10]}_${data.lista_contas_conciliacao[i][4]}" readonly value="${data.lista_contas_conciliacao[i][9]}" style="text-align: right;"/>`,
                                /* 9 */let_btn_detalhes_conta,
                                /* 10 */let_btn_visualiza_doc
                            ];
                            let_lista_dados.push(let_reg);
                        }
                            /*
                        tabela.row
                            .add(let_reg)
                            .draw(false);
                           */
                    }
                    $("#tab_conciliacao_composicao_benner_aud").DataTable( {
                        "bJQueryUI": true,
                        "destroy": true,
                        "fixedHeader": true,
                        "scrollY": false, //770px
                        "scrollX": true,
                        "scrollCollapse": true,
                        "paging": false,
                        //"pageLength": 7,
                        "searching": true,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":let_lista_dados,
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
                    } );
                    let_loader_comp_aud.style.display = "none";
                },
                error: function (request, status, error) {
                    let_loader_comp_aud.style.display = "none";
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






