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


$(document).on('change', '#cb_pacotes_imp_arq_m1', function(){
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
            $("#cb_contas_imp_arq_m1 option").remove();
            dados.lista_contas.forEach(conta => {
                $("#cb_contas_imp_arq_m1").append("<option value='"+
                conta.cod_conta+"'>"+conta.desc_conta+" - Cód. red. CP - "+conta.cod_red_conta_contabil_cp+
                " Cód. red. LP - "+conta.cod_red_conta_contabil_lp+"</option>");
            });
            $("#cb_contas_imp_arq_m1").selectpicker('refresh');

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


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_imp_arquivo_pac_m1") {
        let let_cod_pacote_conta = $("#cb_pacotes_imp_arq_m1").val();
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

    } else if( let_nome_btn == 'btn_pesq_docs_arquivo_pac_m1') {
        let loader_frm_imp_arq_m1 = document.getElementById("loader_frm_imp_arq_pac_m1");
        let let_cod_conta = $("#cb_contas_imp_arq_m1").val();
        let let_competencia = $("#dt_comp_imp_arq_contas_m1").val();
        $.ajax({
            type: 'GET',
            url: '/contabil_composicao_app/pesq_dados_importado_contas_m1',
            data: {
                'cod_conta'         :   let_cod_conta,
                'let_competencia'   :   let_competencia
            },
            //dataType: 'json',
            success: function (dados) {
                let let_cod_pac = $("#cb_pacotes_imp_arq_m1").val();
                let let_lista_dados = [];
                let let_columns_tab = []
                //Contas a pagar/receber
                if(let_cod_pac=='3'){
                    let_columns_tab = [
                        { title: "" },
                        { title: "Nº Filial(Cód. Reduzido)" },
                        { title: "Data Lançto" },
                        { title: "CNPJ" },
                        { title: "Nome Fornecedor" },
                        { title: "Nº AP" },
                        { title: "Data Vencim." },
                        { title: "Nº Parc" },
                        { title: "Valor Relatório" },
                        { title: "Valor Razão" },
                        { title: "Diferença" },
                        { title: "Observação" },
                        { title: "Editar" },
                        { title: "Excluir" }
                    ];
                    dados.lista_docs.forEach( reg => {
                        let doc = [
                            ` <i class="fa-solid fa-paperclip" style="color: #f46424"></i>`,

                        ];


                    });


                } else if(let_cod_pac=='4'){
                    //Estoque

                } else if(let_cod_pac=='5'){
                    //Folha de pagamento

                } else if(let_cod_pac=='6'){
                    //Contas compensação

                } else if(let_cod_pac=='7'){
                    //Tributos

                } else if(let_cod_pac=='9'){
                    //Financeiro disponibilidades

                } else if(let_cod_pac=='10'){
                    //Intercompany

                } else if(let_cod_pac=='11'){
                    //Imobilizado

                } else if(let_cod_pac=='13'){
                    //Consorcios ativo

                }

                $("#tab_doc_contas_modelo_1").DataTable( {
                        "bJQueryUI": true,
                        "destroy": true,
                        "searching": true,
                        "paging": false,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":let_lista_docs,
                        "columns": let_columns_tab,
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