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
    let loader_frm_imp_arq_m1 = document.getElementById("loader_frm_imp_arq_m1");
});


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_imp_arquivo_conta_m1") {
        var formData = new FormData();
        formData.append("file", $('input[type=file]')[0].files[0]);
        formData.append("cod_conta", $("#cb_contas_imp_arq_m1").val());
        formData.append("competencia", $("#dt_comp_imp_arq_contas_m1").val());
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
			    const tabela = new DataTable("#tab_doc_contas_modelo_1");

			    for (var i = 0; i < dados.lista_linhas.length; i++) {
			        tabela.row
			            .add(dados.lista_linhas[i])
			            .draw(false);
			    }

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
    else if (let_nome_btn == "btn_pesq_arquivo_conta_m1") {
        let let_cod_conta = $("#cb_contas_imp_arq_m1").val();
        let let_competencia = $("#dt_comp_imp_arq_contas_m1").val();
        let let_tipo_pesquisa = $("#hd_tipo_pesquisa").val();



        params = {};
        if(let_tipo_pesquisa == 'D'){
            params = {
                'tipo_pesquisa': let_tipo_pesquisa,
                'cod_conta':    let_cod_conta,
                'competencia': let_competencia,
                'data_ini': $("#dt_ini_pesq_doc_m_1").val(),
                'data_fim': $("#dt_fim_pesq_doc_m_1").val()
            }
        } else if(let_tipo_pesquisa == 'T' ){
            params = {
                'tipo_pesquisa': let_tipo_pesquisa,
                'cod_conta':    let_cod_conta,
                'competencia': let_competencia,
                'txt_param_pesq_doc_m_1' : $("#txt_param_pesq_doc_m_1").val()
            }
        }

        loader_frm_imp_arq_m1.style.display = "flex";
        $.ajax({
		    type: 'GET',
			url: "/contabil_composicao_app/pesq_dados_importado_contas_m1",
            data: params,
			dataType: 'json',
			success: function(dados){
			    /*let let_lista_registros = [];
			    dados.lista_dic_resp_conta.forEach( resp => {
			        let reg

			    });*/
			    $('#tab_doc_contas_modelo_1').DataTable( {
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
                    "data":dados.lista_linhas,
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
			    /*
			    const tabela = new DataTable("#tab_doc_contas_modelo_1");
			    tabela.row
			            .add(dados.lista_linhas[0])
			            .draw(false);
			    for (var i = 1; i < dados.lista_linhas.length; i++) {
			        tabela.row
			            .add(dados.lista_linhas[i])
			            .draw(false);
			    }

                */
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

});




$(document).on('change', '#cb_contas_imp_arq_m1', function(){
    let let_cod_conta = $(this).val();
    monta_tabela_imp_contas_m1(let_cod_conta);




});


function monta_tabela_imp_contas_m1(cod_conta){
    loader_frm_imp_arq_m1.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/contabil_composicao_app/acessa_form_doc_contas_modelo_1',
        data: {
            'cod_conta'   :   cod_conta
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

            let let_dados_pesquisa = '';
            if(dados.cod_pacote_conta == 3 || dados.cod_pacote_conta == 5 || dados.cod_pacote_conta == 9 ||
                dados.cod_pacote_conta == 10 || dados.cod_pacote_conta == 13) {

                let_dados_pesquisa = 'Data Lançto.'
            } else if (dados.cod_pacote_conta == 4){
                let_dados_pesquisa = 'Nome Almoxerifado';
            } else if (dados.cod_pacote_conta == 6 || dados.cod_pacote_conta == 7){
                let_dados_pesquisa = 'Data Emissão';
            } else if (dados.cod_pacote_conta == 11){
                let_dados_pesquisa = 'Data Entrada';
            }
            $("#div_desc_pacote_conta").html("Pacote conta : " + dados.desc_pacote_conta + "/ Pesquisa: " + let_dados_pesquisa);

            $("#div_tab_imp_doc_contas_modelo_1").html("");
            $("#div_tab_imp_doc_contas_modelo_1").html(let_table_layout_contas_mod_1);

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
            $("#hd_tipo_pesquisa").val(dados.tipo_pesquisa);
            $("#div_campo_pesq_dados_pac_2").html("");
            $("#div_campo_pesq_dados_pac_3").html("");
            $("#div_campo_pesq_dados_pac_4").html("");

            if(dados.tipo_pesquisa == 'D') {
                $("#div_campo_pesq_dados_pac_2").html(`<input type="date" id="dt_ini_pesq_doc_m_1"
                    class="form-control" name="dt_ini_pesq_doc_m_1">`);
                $("#div_campo_pesq_dados_pac_3").html(`<input type="date" id="dt_fim_pesq_doc_m_1"
                    class="form-control" name="dt_fim_pesq_doc_m_1">`);

                $("#div_campo_pesq_dados_pac_4").html(`
                    <button type="button" name="btn_pesq_arquivo_conta_m1"
                            id="btn_pesq_arquivo_conta_m1"
                            class="btn btn-primary btn-rounded botaoPrincipal">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        Pesquisa
                    </button>
                `);

            } else if(dados.tipo_pesquisa == 'T') {
                $("#div_campo_pesq_dados_pac_3").html(`<input type="text" id="txt_param_pesq_doc_m_1"
                    class="form-control" name="txt_param_pesq_doc_m_1" title="Nome Almoxerifado">`);

                $("#div_campo_pesq_dados_pac_4").html(`
                    <button type="button" name="btn_pesq_arquivo_conta_m1"
                            id="btn_pesq_arquivo_conta_m1"
                            class="btn btn-primary btn-rounded botaoPrincipal">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        Pesquisa
                    </button>
                `);

            }



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