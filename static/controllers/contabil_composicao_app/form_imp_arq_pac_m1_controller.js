//const loader = document.getElementById("loader");

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


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_imp_arquivo_pac_m1") {
        let let_pac = $("#cb_pacotes_imp_doc_pac_contas_m1").val();
        let let_file = $("#file_arquivo_pac_m1").val();
        let let_data_comp = $("#dt_comp_imp_arq_contas_m1").val();
        if ( let_pac=='' || let_file == '' || let_data_comp == '' ) {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Selecione um arquivo válido ou verifique se competência foi informada!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

        } else {
            let let_cod_pacote_conta = $("#cb_pacotes_imp_doc_pac_contas_m1").val();
            var formData = new FormData();
            formData.append("file", $('input[type=file]')[0].files[0]);
            formData.append("cod_pacote_conta", let_cod_pacote_conta);
            formData.append("competencia", $("#dt_comp_imp_arq_contas_m1").val());
            let loader_frm_imp_arq_m1 = document.getElementById("loader_frm_imp_arq_pac_m1");
            loader_frm_imp_arq_m1.style.display = "flex";
            $.ajax({
                type: 'POST',
                enctype: "multipart/form-data; charset=utf-8",
                url: "/contabil_composicao_app/importa_arqv_contas_m1",
                data: formData,
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
                    loader_frm_imp_arq_m1.style.display = "none";
                },
                error: function (request, status, error) {
                    loader_frm_imp_arq_m1.style.display = "none";
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
    else if( let_nome_btn == 'btn_pesq_docs_arquivo_pac_m1') {
        atualiza_tab_imp_docs_pac_mod_1();
    }
    else if( let_nome_btn == 'btn_editar_doc_pac_conta_mod_1') {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_contas_pag_receb',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_doc_pac_pg_rb").val(let_cod_red);
                $("#sl_filial_doc_pac_pg_rb").selectpicker('refresh');

                $("#txt_cnpj_fornec_doc_pac_pg_rb").val(dados.doc_dic.cnpj_fornec);
                $("#txt_nome_fornec_doc_pac_pg_rb").val(dados.doc_dic.nome_fornec);
                $("#txt_doc_pac_pg_rb").val(dados.doc_dic.num_doc);
                $("#txt_num_ap_doc_pac_pg_rb").val(dados.doc_dic.num_ap);
                $("#dt_lanc_doc_pac_pg_rb").val(dados.doc_dic.data_lancto);
                $("#dt_venc_doc_pac_pg_rb").val(dados.doc_dic.data_venc);
                $("#num_parc_doc_pac_pg_rb").val(dados.doc_dic.num_parc);
                $("#num_val_rel_pac_pg_rb").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_pac_pg_rb").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_pg_rb").val(dados.doc_dic.val_dif);
                $("#txt_obs_pac_pg_rb").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_pg_rb").val(dados.doc_dic.cod_pac_doc_contas_pagar_receber);

                $("#modal_edita_doc_pac_pagar_receber").show();

            },
            error: function (request, status, error) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: true,
                    time: '',
                });

          }
        });

    }
    else if( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_pagar_receber') {
        $("#modal_edita_doc_pac_pagar_receber").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_pg_rb') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_contas_pag_receb',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_doc_pac_pg_rb").val(),
                'cnpj_fornec': $("#txt_cnpj_fornec_doc_pac_pg_rb").val(),
                'nome_fornec': $("#txt_nome_fornec_doc_pac_pg_rb").val(),
                'num_doc': $("#txt_doc_pac_pg_rb").val(),
                'num_ap': $("#txt_num_ap_doc_pac_pg_rb").val(),
                'data_lancto': $("#dt_lanc_doc_pac_pg_rb").val(),
                'data_venc': $("#dt_venc_doc_pac_pg_rb").val(),
                'num_parc': $("#num_parc_doc_pac_pg_rb").val(),
                'val_rel': $("#num_val_rel_pac_pg_rb").val(),
                'val_razao': $("#num_val_raz_doc_pac_pg_rb").val(),
                'val_dif': $("#num_val_dif_doc_pac_pg_rb").val(),
                'obs': $("#txt_obs_pac_pg_rb").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_pagar_receber").hide();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: true,
                    time: '',
                });

                atualiza_tab_imp_docs_pac_mod_1();

            },
            error: function (request, status, error) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: true,
                    time: '',
                });
          }
        });



    }

});


$(document).on('change', '#cb_pacotes_imp_doc_pac_contas_m1', function(){
    let let_cod_pacote = $(this).val();
    monta_tabela_imp_pac_m1(let_cod_pacote);
    atualiza_comp_contas_form_imp_docs_pac_m1(let_cod_pacote);
});


function monta_tabela_imp_pac_m1(cod_pacote){
    let let_loader_frm_imp_arq_pac_m1 = document.getElementById("loader_frm_imp_arq_pac_m1");
    let_loader_frm_imp_arq_pac_m1.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/acessa_form_doc_contas_modelo_1',
        data: {
            'cod_conta'     : '0',
            'cod_pacote_conta'    :  cod_pacote
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
            let_table_layout_contas_mod_1.append(let_body);

            $("#div_tab_imp_doc_pac_modelo_1").html("");
            $("#div_tab_imp_doc_pac_modelo_1").html(let_table_layout_contas_mod_1);

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



            let_loader_frm_imp_arq_pac_m1.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_frm_imp_arq_pac_m1.style.display = "none";
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


function atualiza_comp_contas_form_imp_docs_pac_m1(cod_pacote){
    let let_loader_frm_imp_arq_pac_m1 = document.getElementById("loader_frm_imp_arq_pac_m1");
    let_loader_frm_imp_arq_pac_m1.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/atualiza_contas_cb_contas_pac_doc_m1',
        data: {
            'cod_pacote_conta'    :  cod_pacote
        },
        dataType: 'json',
        success: function (dados) {
            $("#cb_pac_contas_imp_doc_pac_conta_m1 option").remove();
            dados.lista_contas.forEach(conta => {
                $("#cb_pac_contas_imp_doc_pac_conta_m1").append("<option value='"+
                conta.cod_conta+"'>"+conta.cod_conta+ " - " + conta.desc_conta+" - Cód. red. CP - "+conta.cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_red_conta_contabil_lp+"</option>");
            });
            $("#cb_pac_contas_imp_doc_pac_conta_m1").selectpicker('refresh');

            let_loader_frm_imp_arq_pac_m1.style.display = "none";

        },
        error: function (request, status, error) {
            let_loader_frm_imp_arq_pac_m1.style.display = "none";
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

function atualiza_tab_imp_docs_pac_mod_1() {
    let let_cod_conta = $("#cb_pac_contas_imp_doc_pac_conta_m1").val();
    let let_competencia = $("#dt_comp_imp_arq_contas_m1").val();
    if(let_cod_conta == '' || let_competencia == ''){
        $.gritter.add({
            title: 'Atenção!',
            text: 'É necessário informar uma conta e competêcia !!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    }
    else {
        let loader_frm_imp_arq_m1 = document.getElementById("loader_frm_imp_arq_pac_m1");
        loader_frm_imp_arq_m1.style.display = "flex";
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/pesq_dados_importado_pac_contas_m1',
            data: {
                'cod_conta'         :   let_cod_conta,
                'competencia'   :   let_competencia
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_pac = $("#cb_pacotes_imp_doc_pac_contas_m1").val();
                let let_lista_docs = [];
                let let_columns_tab = [];

                //Contas a pagar/receber
                if(let_cod_pac=='3'){
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_contas_pagar_receber}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_pagar_receber}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_contas_pagar_receber}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_pagar_receber}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.data_lancto,
                            reg.cnpj,
                            reg.nome_fornecedor,
                            reg.num_doc,
                            reg.num_ap,
                            reg.data_venc,
                            reg.num_parc,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });
                }
                else if(let_cod_pac=='4'){
                    //Estoque
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_estoque}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_estoque}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_estoque}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_estoque}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.nome_almoxarifado,
                            reg.cod_produto,
                            reg.desc_produto,
                            reg.qtd_prod,
                            reg.custo_medio,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='5'){
                    //Folha de pagamento
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_folha_pag}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_folha_pag}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_folha_pag}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_folha_pag}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.matricula,
                            reg.historico,
                            reg.num_doc,
                            reg.num_doc_contabil,
                            reg.data_lancto,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='6'){
                    //Contas compensação
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_contas_compensacao}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_compensacao}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_contas_compensacao}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_compensacao}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.cnpj,
                            reg.nome_fornecedor,
                            reg.num_doc,
                            reg.num_doc_contabil,
                            reg.data_emissao,
                            reg.data_entrada,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='7'){
                    //Tributos
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_tributos}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_tributos}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_tributos}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_tributos}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.num_doc,
                            reg.num_doc_contabil,
                            reg.data_emissao,
                            reg.data_entrada,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='9'){
                    //Financeiro disponibilidades
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_financ_disp}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_financ_disp}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_financ_disp}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_financ_disp}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.num_doc,
                            reg.data_lancto,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='10'){
                    //Intercompany
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_intercompany}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_intercompany}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_intercompany}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_intercompany}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.num_doc,
                            reg.data_lancto,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='11'){
                    //Imobilizado
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_imobilizado}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_imobilizado}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_imobilizado}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_imobilizado}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.num_doc,
                            reg.data_lancto,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='13'){
                    //Consorcios ativo
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_conta_mod_1"
                                id="btn_editar_doc_pac_conta_mod_1_${reg.cod_pac_doc_consorcio_ativo}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_consorcio_ativo}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_conta_mod_1"
                                id="btn_excluir_doc_pac_conta_mod_1_${reg.cod_pac_doc_consorcio_ativo}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_consorcio_ativo}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.num_doc,
                            reg.data_lancto,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }
                else if(let_cod_pac=='14'){
                    //Consorcios ativo
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_editar_doc_pac_demais_contas_mod_1"
                                id="btn_editar_doc_pac_demais_contas_mod_1_${reg.cod_pac_doc_outros}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_outros}">
                                <i class="fa-solid fa-pen-to-square" style="color: #f46424;"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_excluir_doc_pac_demais_conta_mod_1"
                                id="btn_excluir_doc_pac_demais_conta_mod_1_${reg.cod_pac_doc_outros}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_outros}">
                                <i class="fa-solid fa-trash-can" style="color: #f46424;"></i>
                            </button>
                        `;
                        let doc = [
                            reg.data_entrada,
                            reg.data_lancto,
                            reg.cod_filial__cod_reduzido,
                            reg.historico,
                            reg.num_doc,
                            reg.num_doc_contabil,
                            reg.val_rel,
                            reg.val_razao,
                            reg.val_dif,
                            reg.obs,
                            let_btn_editar_arquivo,
                            let_btn_excluir_arquivo
                        ];
                        let_lista_docs.push(doc);
                    });

                }

                $("#tab_doc_contas_modelo_1").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "770px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 10,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_docs,
                    //"columns": let_columns_tab,
                    /*
                    "columnDefs": [
                        {"className": "dt-center", "targets": [0,2,3]},
                        {"className": "dt-left", "targets": [1]}
                    ],
                    */
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

                loader_frm_imp_arq_m1.style.display = "none";

            },
            error: function (request, status, error) {
                loader_frm_imp_arq_m1.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: true,
                    time: '',
                });

          }
        });
    }

}


