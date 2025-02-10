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
            formData.append("file", $('#file_arquivo_pac_m1')[0].files[0]);
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
    else if( let_nome_btn == 'btn_abre_modal_edita_doc_pac_pagar_receber') {
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
                'val_rel': $("#num_val_rel_pac_pg_rb").val().replace('.','').replace(',','.'),
                'val_razao': $("#num_val_raz_doc_pac_pg_rb").val().replace('.','').replace(',','.'),
                'val_dif': $("#num_val_dif_doc_pac_pg_rb").val().replace('.','').replace(',','.'),
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
    else if ( let_nome_btn == 'btn_abre_modal_exclui_doc_pac_pagar_receber' ) {
        $("#btn_confirma_exclusao_doc_pac_pagar_receber").val(let_val_btn);
        $("#modal_exclui_doc_pac_pagar_receber").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_pagar_receber' ) {
        $("#modal_exclui_doc_pac_pagar_receber").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_pagar_receber') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_pagar_receber").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_pagar_receber/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_pagar_receber").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if( let_nome_btn == 'btn_abre_modal_edita_doc_pac_estoque') {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_estoque',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_estoque").val(let_cod_red);
                $("#sl_filial_pac_estoque").selectpicker('refresh');

                $("#txt_nome_almoxarifado_pac_estoque").val(dados.doc_dic.nome_almoxarifado);
                $("#txt_cod_prod_pac_estoque").val(dados.doc_dic.cod_produto);
                $("#txt_desc_prod_pac_estoque").val(dados.doc_dic.desc_produto);
                $("#txt_qtd_prod_pac_estoque").val(dados.doc_dic.qtd_prod);


                $("#num_custo_medio_pac_estoque").val(dados.doc_dic.custo_medio);
                $("#num_val_rel_pac_estoque").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_estoque").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_estoque").val(dados.doc_dic.val_dif);
                $("#txt_obs_pac_estoque").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_estoque").val(dados.doc_dic.cod_pac_doc_estoque);

                $("#modal_edita_doc_pac_estoque").show();

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
    else if( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_estoque') {
        $("#modal_edita_doc_pac_estoque").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_estoque') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_estoque',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_estoque").val(),
                'nome_almoxarifado': $("#txt_nome_almoxarifado_pac_estoque").val(),
                'cod_prod': $("#txt_cod_prod_pac_estoque").val(),
                'desc_prod': $("#txt_desc_prod_pac_estoque").val(),
                'qtd': $("#txt_qtd_prod_pac_estoque").val(),
                'custo_medio': $("#num_custo_medio_pac_estoque").val().replace('.','').replace(',','.'),
                'val_rel': $("#num_val_rel_pac_estoque").val().replace('.','').replace(',','.'),
                'val_razao': $("#num_val_raz_doc_estoque").val().replace('.','').replace(',','.'),
                'val_dif': $("#num_val_dif_doc_pac_estoque").val().replace('.','').replace(',','.'),
                'obs': $("#txt_obs_pac_estoque").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_estoque").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_exclui_doc_pac_estoque' ) {
        $("#btn_confirma_exclusao_doc_pac_estoque").val(let_val_btn);
        $("#modal_exclui_doc_pac_estoque").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_estoque' ) {
        $("#modal_exclui_doc_pac_estoque").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_estoque') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_estoque").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_estoque/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_estoque").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_folha_pag' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_folha_pag',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_pag_folha").val(let_cod_red);
                $("#sl_filial_pac_pag_folha").selectpicker('refresh');

                $("#txt_matricula_pac_folha_pag").val(dados.doc_dic.matricula);
                $("#txt_historico_pac_folha_pag").val(dados.doc_dic.historico);
                $("#txt_num_doc_pac_folha_pag").val(dados.doc_dic.num_doc);
                $("#txt_num_doc_cont_pac_folha_pag").val(dados.doc_dic.num_doc_contabil);


                $("#dt_lancto_pac_folha_pag").val(dados.doc_dic.data_lancto);
                $("#num_val_rel_pac_folha_pag").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_folha_pag").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_folha_pag").val(dados.doc_dic.val_dif);
                $("#txt_obs_pac_folha_pag").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_folha_pag").val(dados.doc_dic.cod_pac_doc_folha_pag);

                $("#modal_edita_doc_pac_folha_pag").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_folha_pag') {
         $("#modal_edita_doc_pac_folha_pag").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_folha_pag') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_folha_pag',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_pag_folha").val(),
                'matricula': $("#txt_matricula_pac_folha_pag").val(),
                'historico': $("#txt_historico_pac_folha_pag").val(),
                'num_doc': $("#txt_num_doc_pac_folha_pag").val(),
                'num_doc_contabil': $("#txt_num_doc_cont_pac_folha_pag").val(),
                'data_lancto': $("#dt_lancto_pac_folha_pag").val(),
                'val_rel': $("#num_val_rel_pac_folha_pag").val().replace('.','').replace(',','.'),
                'val_razao': $("#num_val_raz_doc_folha_pag").val().replace('.','').replace(',','.'),
                'val_dif': $("#num_val_dif_doc_pac_folha_pag").val().replace('.','').replace(',','.'),
                'obs': $("#txt_obs_pac_folha_pag").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_folha_pag").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_exclui_doc_pac_folha_pag' ) {
        $("#btn_confirma_exclusao_doc_pac_folha_pag").val(let_val_btn);
        $("#modal_exclui_doc_pac_folha_pag").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_folha_pag' ) {
        $("#modal_exclui_doc_pac_folha_pag").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_folha_pag') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_folha_pag").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_folha_pag/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_folha_pag").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_compensacao' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_compensacao',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_comp").val(let_cod_red);
                $("#sl_filial_pac_comp").selectpicker('refresh');

                $("#txt_cnpj_fornec_pac_comp").val(dados.doc_dic.cnpj);
                $("#txt_nome_fornec_pac_comp").val(dados.doc_dic.nome_fornecedor);
                $("#txt_num_doc_pac_comp").val(dados.doc_dic.num_doc);
                $("#txt_num_doc_cont_pac_comp").val(dados.doc_dic.num_doc_contabil);


                $("#dt_emissao_pac_comp").val(dados.doc_dic.data_emissao);
                $("#dt_entrada_pac_comp").val(dados.doc_dic.data_entrada);
                $("#num_val_rel_pac_comp").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_comp").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_comp").val(dados.doc_dic.val_dif);
                $("#txt_historico_pac_comp").val(dados.doc_dic.historico);
                $("#txt_obs_pac_comp").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_comp").val(dados.doc_dic.cod_pac_doc_contas_compensacao);

                $("#modal_edita_doc_pac_compensacao").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_compensacao') {
         $("#modal_edita_doc_pac_compensacao").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_comp') {
        let let_val_rel = $("#num_val_rel_pac_comp").val();
        let let_val_raz = $("#num_val_raz_doc_comp").val();
        let let_dif = $("#num_val_dif_doc_pac_comp").val();
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_composicao',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_comp").val(),
                'data_emissao': $("#dt_emissao_pac_comp").val(),
                'data_entrada': $("#dt_entrada_pac_comp").val(),
                'cnpj': $("#txt_cnpj_fornec_pac_comp").val(),
                'nome_fornecedor': $("#txt_nome_fornec_pac_comp").val(),
                'num_doc': $("#txt_num_doc_pac_comp").val(),
                'num_doc_contabil': $("#txt_num_doc_cont_pac_comp").val(),
                'val_rel': let_val_rel,
                'val_razao': let_val_raz,
                'val_dif': let_dif,
                'obs': $("#txt_obs_pac_comp").val(),
                'historico': $("#txt_historico_pac_comp").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_compensacao").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_compensacao' ) {
        $("#btn_confirma_exclusao_doc_pac_compensacao").val(let_val_btn);
        $("#modal_exclui_doc_pac_compensacao").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_compensacao' ) {
        $("#modal_exclui_doc_pac_compensacao").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_compensacao') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_compensacao").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_comensacao/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_compensacao").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_tributos' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_tributos',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_trib").val(let_cod_red);
                $("#sl_filial_pac_trib").selectpicker('refresh');

                $("#txt_nome_fornec_pac_trib").val(dados.doc_dic.nome_fornecedor);
                $("#txt_num_doc_pac_trib").val(dados.doc_dic.num_doc);
                $("#txt_num_doc_cont_pac_trib").val(dados.doc_dic.num_doc_contabil);


                $("#dt_emissao_pac_trib").val(dados.doc_dic.data_emissao);
                $("#dt_entrada_pac_trib").val(dados.doc_dic.data_entrada);
                $("#num_val_rel_pac_trib").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_trib").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_trib").val(dados.doc_dic.val_dif);
                $("#txt_historico_pac_trib").val(dados.doc_dic.historico);
                $("#txt_obs_pac_trib").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_trib").val(dados.doc_dic.cod_pac_doc_tributos);

                $("#modal_edita_doc_pac_tributos").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_tributos') {
         $("#modal_edita_doc_pac_tributos").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_trib') {
        let let_val_rel = $("#num_val_rel_pac_trib").val();
        let let_val_raz = $("#num_val_raz_doc_trib").val();
        let let_dif = $("#num_val_dif_doc_pac_trib").val();
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_trib',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_trib").val(),
                'data_emissao': $("#dt_emissao_pac_trib").val(),
                'data_entrada': $("#dt_entrada_pac_trib").val(),
                'nome_fornecedor': $("#txt_nome_fornec_pac_trib").val(),
                'num_doc': $("#txt_num_doc_pac_trib").val(),
                'num_doc_contabil': $("#txt_num_doc_cont_pac_trib").val(),
                'val_rel': let_val_rel,
                'val_razao': let_val_raz,
                'val_dif': let_dif,
                'obs': $("#txt_obs_pac_trib").val(),
                'historico': $("#txt_historico_pac_trib").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_tributos").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_tributos' ) {
        $("#btn_confirma_exclusao_doc_pac_trib").val(let_val_btn);
        $("#modal_exclui_doc_pac_trib").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_trib' ) {
        $("#modal_exclui_doc_pac_trib").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_trib') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_trib").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_tributo/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_trib").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_financ_disp' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_financ_disp',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_financ_disp").val(let_cod_red);
                $("#sl_filial_pac_financ_disp").selectpicker('refresh');

                $("#txt_num_doc_pac_financ_disp").val(dados.doc_dic.num_doc);

                $("#dt_lancto_pac_financ_disp").val(dados.doc_dic.data_lancto);
                $("#num_val_rel_pac_financ_disp").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_pac_financ_disp").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_financ_disp").val(dados.doc_dic.val_dif);
                $("#txt_historico_pac_financ_disp").val(dados.doc_dic.historico);
                $("#txt_obs_pac_financ_disp").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_financ_disp").val(dados.doc_dic.cod_pac_doc_financ_disp);

                $("#modal_edita_doc_pac_financ_disp").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_financ_disp') {
         $("#modal_edita_doc_pac_financ_disp").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_financ_disp') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_financ_disp',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_financ_disp").val(),
                'data_lancto': $("#dt_lancto_pac_financ_disp").val(),
                'num_doc': $("#txt_num_doc_pac_financ_disp").val(),
                'val_rel': $("#num_val_rel_pac_financ_disp").val(),
                'val_razao': $("#num_val_raz_doc_pac_financ_disp").val(),
                'val_dif': $("#num_val_dif_doc_pac_financ_disp").val(),
                'obs': $("#txt_obs_pac_financ_disp").val(),
                'historico': $("#txt_historico_pac_financ_disp").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_financ_disp").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_financ_disp' ) {
        $("#btn_confirma_exclusao_doc_pac_financ_disp").val(let_val_btn);
        $("#modal_exclui_doc_pac_financ_disp").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_financ_disp' ) {
        $("#modal_exclui_doc_pac_financ_disp").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_financ_disp') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_financ_disp").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_financ_disp/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_financ_disp").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_intercompany' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_intercompany',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_intercompany").val(let_cod_red);
                $("#sl_filial_pac_intercompany").selectpicker('refresh');

                $("#txt_num_doc_pac_intercompany").val(dados.doc_dic.num_doc);

                $("#dt_lancto_pac_intercompany").val(dados.doc_dic.data_lancto);
                $("#num_val_rel_pac_intercompany").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_pac_intercompany").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_intercompany").val(dados.doc_dic.val_dif);
                $("#txt_historico_pac_intercompany").val(dados.doc_dic.historico);
                $("#txt_obs_pac_intercompany").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_intercompany").val(dados.doc_dic.cod_pac_doc_intercompany);

                $("#modal_edita_doc_pac_intercompany").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_intercompany') {
         $("#modal_edita_doc_pac_intercompany").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_intercompany') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_intercompany',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_intercompany").val(),
                'data_lancto': $("#dt_lancto_pac_intercompany").val(),
                'num_doc': $("#txt_num_doc_pac_intercompany").val(),
                'val_rel': $("#num_val_rel_pac_intercompany").val(),
                'val_razao': $("#num_val_raz_doc_pac_intercompany").val(),
                'val_dif': $("#num_val_dif_doc_pac_intercompany").val(),
                'obs': $("#txt_obs_pac_intercompany").val(),
                'historico': $("#txt_historico_pac_intercompany").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_intercompany").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_intercompany' ) {
        $("#btn_confirma_exclusao_doc_pac_intercompany").val(let_val_btn);
        $("#modal_exclui_doc_pac_intercompany").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_intercompany' ) {
        $("#modal_exclui_doc_pac_intercompany").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_intercompany') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_intercompany").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_intercompany/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_intercompany").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_imobilizado' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_imobilizado',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_imob").val(let_cod_red);
                $("#sl_filial_pac_imob").selectpicker('refresh');

                $("#txt_plaqueta_pac_imob").val(dados.doc_dic.plaqueta);
                $("#txt_desc_imob_pac_imob").val(dados.doc_dic.desc_imobilizado);
                $("#txt_val_aquisicao_pac_imob").val(dados.doc_dic.val_aquisicao);
                $("#txt_num_doc_pac_imob").val(dados.doc_dic.num_doc);
                $("#txt_nome_fornec_pac_imob").val(dados.doc_dic.nome_fornecedor);
                $("#dt_entrada_pac_imob").val(dados.doc_dic.data_entrada);
                $("#num_deprec_acum_pac_imob").val(dados.doc_dic.depreciacao_acum);
                $("#num_val_liq_pac_imob").val(dados.doc_dic.val_liq);
                $("#num_taxa_depre_doc_pac_imob").val(dados.doc_dic.taxa_depreciacao);

                $("#num_val_rel_pac_imob").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_pac_imob").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_imob").val(dados.doc_dic.val_dif);

                $("#txt_obs_pac_imob").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_imob").val(dados.doc_dic.cod_pac_doc_imobilizado);

                $("#modal_edita_doc_pac_imobilizado").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_imobilizado') {
         $("#modal_edita_doc_pac_imobilizado").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_imob') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_imobilizado',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_imob").val(),
                'plaqueta': $("#txt_plaqueta_pac_imob").val(),
                'desc_imobilizado': $("#txt_desc_imob_pac_imob").val(),
                'val_aquisicao': $("#txt_val_aquisicao_pac_imob").val(),
                'num_doc': $("#txt_num_doc_pac_imob").val(),
                'nome_fornec': $("#txt_nome_fornec_pac_imob").val(),
                'data_entrada': $("#dt_entrada_pac_imob").val(),
                'deprec_acum': $("#num_deprec_acum_pac_imob").val(),
                'val_liq': $("#num_val_liq_pac_imob").val(),
                'taxa_deprec': $("#num_taxa_depre_doc_pac_imob").val(),
                'val_rel': $("#num_val_rel_pac_imob").val(),
                'val_razao': $("#num_val_raz_doc_pac_imob").val(),
                'val_dif': $("#num_val_dif_doc_pac_imob").val(),
                'obs': $("#txt_obs_pac_imob").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_imobilizado").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_imobilizado' ) {
        $("#btn_confirma_exclusao_doc_pac_imobilizado").val(let_val_btn);
        $("#modal_exclui_doc_pac_imobilizado").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_imobilizado' ) {
        $("#modal_exclui_doc_pac_imobilizado").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_imobilizado') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_imobilizado").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_imobilizado/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_imobilizado").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_consorc_atv' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_consorc_atv',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_consorc_atv").val(let_cod_red);
                $("#sl_filial_pac_consorc_atv").selectpicker('refresh');

                $("#txt_historico_pac_consorc_atv").val(dados.doc_dic.historico);
                $("#txt_num_doc_pac_consorc_atv").val(dados.doc_dic.num_doc);
                $("#dt_lancto_pac_consorc_atv").val(dados.doc_dic.data_lancto);

                $("#num_val_rel_pac_consorc_atv").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_pac_consorc_atv").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_consorc_atv").val(dados.doc_dic.val_dif);

                $("#txt_obs_pac_consorc_atv").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_consorc_atv").val(dados.doc_dic.cod_pac_doc_consorcio_ativo);

                $("#modal_edita_doc_pac_consorcios_ativos").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_consorcios_ativos') {
         $("#modal_edita_doc_pac_consorcios_ativos").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_consorc_atv') {
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_consorc_atv',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_consorc_atv").val(),
                'data_lancto': $("#dt_lancto_pac_consorc_atv").val(),
                'num_doc': $("#txt_num_doc_pac_consorc_atv").val(),
                'val_rel': $("#num_val_rel_pac_consorc_atv").val(),
                'val_razao': $("#num_val_raz_doc_pac_consorc_atv").val(),
                'val_dif': $("#num_val_dif_doc_pac_consorc_atv").val(),
                'obs': $("#txt_obs_pac_consorc_atv").val(),
                'historico': $("#txt_historico_pac_consorc_atv").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_consorcios_ativos").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_consorcio_ativo' ) {
        $("#btn_confirma_exclusao_doc_pac_consorcios_ativos").val(let_val_btn);
        $("#modal_exclui_doc_pac_consorcios_ativos").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_consorcios_ativos' ) {
        $("#modal_exclui_doc_pac_consorcios_ativos").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_consorcios_ativos') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_consorcios_ativos").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_consorcios_ativos/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_consorcios_ativos").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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
    else if ( let_nome_btn == 'btn_abre_modal_edita_doc_pac_demais_contas' ) {
        let let_cod_doc = let_val_btn;
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/retorna_dados_doc_pac_demais_contas',
            data: {
                'cod_doc'    :   let_cod_doc
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_red = dados.doc_dic.cod_red_fil;
                $("#sl_filial_pac_demais_contas").val(let_cod_red);
                $("#sl_filial_pac_demais_contas").selectpicker('refresh');

                $("#txt_num_doc_pac_demais_contas").val(dados.doc_dic.num_doc);
                $("#txt_num_doc_cont_pac_demais_contas").val(dados.doc_dic.num_doc_contabil);


                $("#dt_lancto_pac_demais_contas").val(dados.doc_dic.data_lancto);
                $("#dt_entrada_pac_demais_contas").val(dados.doc_dic.data_entrada);
                $("#num_val_rel_pac_demais_contas").val(dados.doc_dic.val_rel);
                $("#num_val_raz_doc_demais_contas").val(dados.doc_dic.val_razao);
                $("#num_val_dif_doc_pac_demais_contas").val(dados.doc_dic.val_dif);
                $("#txt_historico_pac_demais_contas").val(dados.doc_dic.historico);
                $("#txt_obs_pac_demais_contas").val(dados.doc_dic.obs);
                $("#btn_confirma_update_doc_pac_demais_contas").val(dados.doc_dic.cod_pac_doc_outros);

                $("#modal_edita_doc_pac_demais_contas").show();

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
    else if ( let_nome_btn == 'btn_fecha_modal_edita_doc_pac_demais_contas') {
         $("#modal_edita_doc_pac_demais_contas").hide();
    }
    else if( let_nome_btn == 'btn_confirma_update_doc_pac_demais_contas') {
        let let_val_rel = $("#num_val_rel_pac_demais_contas").val();
        let let_val_raz = $("#num_val_raz_doc_demais_contas").val();
        let let_dif = $("#num_val_dif_doc_pac_demais_contas").val();
        $.ajax({
            type: 'POST',
            url: '/contabil_composicao_app/altera_dados_doc_pac_demais_contas',
            data: {
                'let_cod_doc': let_val_btn,
                'cod_red_fil': $("#sl_filial_pac_demais_contas").val(),
                'data_lancto': $("#dt_lancto_pac_demais_contas").val(),
                'data_entrada': $("#dt_entrada_pac_demais_contas").val(),
                'num_doc': $("#txt_num_doc_pac_demais_contas").val(),
                'num_doc_contabil': $("#txt_num_doc_cont_pac_demais_contas").val(),
                'val_rel': let_val_rel,
                'val_razao': let_val_raz,
                'val_dif': let_dif,
                'obs': $("#txt_obs_pac_demais_contas").val(),
                'historico': $("#txt_historico_pac_demais_contas").val()
            },
            //dataType: 'json',
            success: function (dados) {
                $("#modal_edita_doc_pac_demais_contas").hide();
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
    else if ( let_nome_btn == 'btn_abre_modal_excluir_doc_pac_demais_contas' ) {
        $("#btn_confirma_exclusao_doc_pac_demais_contas").val(let_val_btn);
        $("#modal_exclui_doc_pac_demais_contas").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_exclui_doc_pac_demais_contas' ) {
        $("#modal_exclui_doc_pac_demais_contas").hide();
    }
    else if ( let_nome_btn == 'btn_confirma_exclusao_doc_pac_demais_contas') {
        //cod_reg/obs
        let let_cod_reg = let_val_btn;
        let let_motivo = $("#ta_justificativa_exclusao_doc_pac_demais_contas").val();
        $.ajax({
            type: 'DELETE',
            url: '/contabil_composicao_app/exclui_doc_pac_demais_contas/'+let_val_btn + '_' + let_motivo,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modal_exclui_doc_pac_demais_contas").hide();
                atualiza_tab_imp_docs_pac_mod_1();
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

            let let_body = $("<tbody/>");
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
    $("#txt_val_rel").val("0,00");
    $("#txt_val_balancete").val("0,00");
    $("#txt_val_dif").val("0,00");
    $("#div_resumo_conta_comp").html("");
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
                let let_resumo_docs = ``;
                dados.resumo_docs.forEach( resumo => {
                    let_resumo_docs = `
                        <div class="d-flex flex-column align-items-start">
                            <label for="txt_val_rel">R$ Rel.</label>
                            <input class="form-control" id="txt_val_rel" style="text-align: right;" value="${resumo.tt_val_rel}" readonly/>
                        </div>

                        <div class="d-flex flex-column align-items-start" style="margin-left: 0.25rem;">
                            <label for="txt_val_balancete">R$ Balancete</label>
                            <input class="form-control" id="txt_val_balancete" style="text-align: right;" value="${resumo.val_balancete}" readonly/>
                        </div>

                        <div class="d-flex flex-column align-items-start" style="margin-left: 0.25rem;">
                            <label for="txt_val_dif">R$ Dif.</label>
                            <input class="form-control" id="txt_val_dif" style="text-align: right;" value="${resumo.val_dif_comp_bal}" readonly/>
                        </div>


                    `;
                });
                $("#div_resumo_conta_comp").html(let_resumo_docs);

                /*
                <b>Qtd.: Registros:</b>&nbsp;<span style="font-size: 20px;">${resumo.qtd_registros}</span>
                        &nbsp;&nbsp;<b>Val. Relatório(R$):</b>&nbsp;<span style="font-size: 20px;">${resumo.tt_val_rel}
                        </span>&nbsp;&nbsp;<b>Val. Razão(R$):</b>&nbsp;<span style="font-size: 20px;">
                        ${resumo.tt_val_razao}</span>&nbsp;&nbsp;<b>Dif.(R$):</b>&nbsp;<span style="font-size: 20px;">
                        ${resumo.tt_dif}</span>&nbsp;&nbsp;<b>Balancete(R$):</b>&nbsp;<span style="font-size: 20px;">
                        ${resumo.val_balancete}</span>&nbsp;&nbsp;<b>Dif. Comp. x Bal.(R$):</b>&nbsp;
                        <span style="font-size: 20px;">${resumo.val_dif_comp_bal}</span>
                        */


                $("#div_campo_pesq_dados_pac_4").html();


                if(let_cod_pac=='3'){
                    //Contas a pagar/receber
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_abre_modal_edita_doc_pac_pagar_receber"
                                id="btn_abre_modal_edita_doc_pac_pagar_receber_${reg.cod_pac_doc_contas_pagar_receber}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_pagar_receber}"
                                title="Editar Registro">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_exclui_doc_pac_pagar_receber"
                                id="btn_abre_modal_exclui_doc_pac_pagar_receber_${reg.cod_pac_doc_contas_pagar_receber}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_pagar_receber}"
                                title="Excluir Registro">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_estoque"
                                id="btn_abre_modal_edita_doc_pac_estoque_${reg.cod_pac_doc_estoque}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_estoque}"
                                title="Editar Registro">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_exclui_doc_pac_estoque"
                                id="btn_abre_modal_exclui_doc_pac_estoque_${reg.cod_pac_doc_estoque}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_estoque}"
                                title="Excluir Registro">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_folha_pag"
                                id="btn_abre_modal_edita_doc_pac_folha_pag_${reg.cod_pac_doc_folha_pag}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_folha_pag}"
                                title="Editar Registro">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_exclui_doc_pac_folha_pag"
                                id="btn_abre_modal_exclui_doc_pac_folha_pag_${reg.cod_pac_doc_folha_pag}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_folha_pag}"
                                title="Excluir Registro">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_compensacao"
                                id="btn_abre_modal_edita_doc_pac_compensacao_${reg.cod_pac_doc_contas_compensacao}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_compensacao}"
                                title="Editar Registro">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_compensacao"
                                id="btn_abre_modal_excluir_doc_pac_compensacao_${reg.cod_pac_doc_contas_compensacao}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_contas_compensacao}"
                                title="Excluir Registro">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_tributos"
                                id="btn_abre_modal_edita_doc_pac_tributos_${reg.cod_pac_doc_tributos}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_tributos}"
                                title="Editar Registro">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_tributos"
                                id="btn_abre_modal_excluir_doc_pac_tributos_${reg.cod_pac_doc_tributos}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_tributos}"
                                title="Excluir Registro">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

                        let doc = [
                            reg.cod_filial__desc_filial,
                            reg.historico,
                            reg.num_doc,
                            reg.num_doc_contabil,
                            reg.nome_fornecedor,
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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_financ_disp"
                                id="btn_abre_modal_edita_doc_pac_financ_disp_${reg.cod_pac_doc_financ_disp}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_financ_disp}">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_financ_disp"
                                id="btn_abre_modal_excluir_doc_pac_financ_disp_${reg.cod_pac_doc_financ_disp}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_financ_disp}">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_intercompany"
                                id="btn_abre_modal_edita_doc_pac_intercompany_${reg.cod_pac_doc_intercompany}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_intercompany}">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_intercompany"
                                id="btn_abre_modal_excluir_doc_pac_intercompany_${reg.cod_pac_doc_intercompany}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_intercompany}">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_imobilizado"
                                id="btn_abre_modal_edita_doc_pac_imobilizado_${reg.cod_pac_doc_imobilizado}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_imobilizado}">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_imobilizado"
                                id="btn_abre_modal_excluir_doc_pac_imobilizado_${reg.cod_pac_doc_imobilizado}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_imobilizado}">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

                        let doc = [
                            reg.data_entrada,
                            reg.cod_filial__desc_filial,
                            reg.plaqueta,
                            reg.desc_imobilizado,
                            reg.val_aquisicao,
                            reg.num_doc,
                            reg.nome_fornecedor,
                            reg.depreciacao_acum,
                            reg.val_liq,
                            reg.taxa_depreciacao,
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
                            <button type="button" name="btn_abre_modal_edita_doc_pac_consorc_atv"
                                id="btn_abre_modal_edita_doc_pac_consorc_atv_${reg.cod_pac_doc_consorcio_ativo}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_consorcio_ativo}">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_consorcio_ativo"
                                id="btn_abre_modal_excluir_doc_pac_consorcio_ativo_${reg.cod_pac_doc_consorcio_ativo}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_consorcio_ativo}">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

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
                    //Demais Contas
                    dados.lista_docs.forEach( reg => {
                        let let_btn_editar_arquivo = `
                            <button type="button" name="btn_abre_modal_edita_doc_pac_demais_contas"
                                id="btn_abre_modal_edita_doc_pac_demais_contas_${reg.cod_pac_doc_outros}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_outros}">
                                <i class="fa-solid fa-pen-to-square icon-color-e"></i>
                            </button>
                        `;

                        let let_btn_excluir_arquivo = `
                            <button type="button" name="btn_abre_modal_excluir_doc_pac_demais_contas"
                                id="btn_abre_modal_excluir_doc_pac_demais_contas_${reg.cod_pac_doc_outros}"
                                class="btn btn-rounded btn-space"
                                value="${reg.cod_pac_doc_outros}">
                                <i class="fa-solid fa-trash-can icon-color-e"></i>
                            </button>
                        `;

                        if ( reg.ativo == 'N') {
                            let_btn_editar_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;

                            let_btn_excluir_arquivo = `
                                <i class="fa-solid fa-ban icon-color-e" title="${reg.obs}"></i>
                            `;
                        }

                        let doc = [
                            reg.data_entrada,
                            reg.data_lancto,
                            reg.cod_filial__desc_filial,
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


