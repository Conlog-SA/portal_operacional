
//var dt;
//var detailRows = [];

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

var var_lista_reg = [];
    var var_lista_compras_aud = [];
    var var_lista_persistencia_compra_aud = [];

$(document).ready(function(){


});

$(document).on('click', 'button', function(){
    var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if( nomeDoButton == 'btn_gera_evolucao_precos' || nomeDoButton == 'btn_gera_evolucao_pela_req' ) {
        var var_handle_filial = $("#cb_filial_gera_evolucao_precos").val();
        var var_data_ini = $("#txt_data_ini_evolucao_precos").val();
        var var_data_fim = $("#txt_data_fim_evolucao_precos").val();
        var var_handle_familia = $("#cb_familia_gera_evolucao_precos").val();
        var var_cod_ref_item = $("#cb_item_gera_evolucao_precos").val();
        var var_num_requisicao = 0;
        var var_validacao_campos = 'nok';
        if ( nomeDoButton == 'btn_gera_evolucao_pela_req' ){
            var_num_requisicao = $("#txt_num_requisicao").val();
            $("#modal_gera_evolucao_precos_requisicao").hide();
            if( var_data_ini == '' || var_data_fim == '' || var_num_requisicao == '' ) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: "Informe os campos obrigatórios indicados por (*)!",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            } else {
                var_validacao_campos = 'ok';
            }
        } else if ( nomeDoButton == 'btn_gera_evolucao_precos' ) {
            if( var_data_ini == '' || var_data_fim == '' ) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: "Informe os campos obrigatórios indicados por (*)!",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            } else {
                var_validacao_campos = 'ok';
            }
        }
         if( var_validacao_campos == 'ok') {
            let let_loader_evolucao_preco = document.getElementById("loader_evolucao_preco");
            let_loader_evolucao_preco.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    'handle_filial'     :   var_handle_filial,
                    'data_ini'          :   var_data_ini,
                    'data_fim'          :   var_data_fim,
                    'handle_familia'    :   var_handle_familia,
                    'cod_ref_item'      :   var_cod_ref_item,
                    'numero_requisicao' :   var_num_requisicao
                },
                url:'/suprimentos_evolucao_precos_app/gera_dados_evolucao_precos',
                success: function(dados){
                    var_lista_reg = [];
                    $("#cb_itens_aud_evolucao_precos option").remove();

                    dados.lista_evolucao_precos_tab.forEach( reg => {

                        $("#cb_itens_aud_evolucao_precos").append("<option value='"+reg.cod_ref_item+"'>"+
                            reg.desc_item+"</option>");

                        var var_status_analise_compra = ''
                        if(reg.analise == 'Compra Maior'){
                            var_status_analise_compra = "<span style='background-color:#FA8072;color:#FF0000;'>"+reg.analise+"</span>"
                        }else if(reg.analise == 'Compra Menor'){
                            var_status_analise_compra = "<span style='background-color:#FFE4B5;color:#f2652;'>"+reg.analise+"</span>"
                        }else if(reg.analise == 'Compra OK'){
                            var_status_analise_compra = "<span style='background-color:#98FB98;color:#3CB371;'>"+reg.analise+"</span>"
                        }else {
                            var_status_analise_compra = reg.analise
                        }

                        var var_desc_variacao = ''
                        if ( reg.desc_variacao != '0'){
                            var_desc_variacao = reg.desc_variacao;
                        }

                        reg_compra = [
                            "<input type='hidden' id='hd_info_pesq_compras' name='hd_info_pesq_compras' " +
                            "value='"+reg.handle_filial_form+"_"+reg.data_ini_form+"_"+reg.data_fim_form+"_"+reg.cod_ref_item+"'>",
                            reg.desc_familia,
                            reg.cod_ref_item,
                            reg.desc_item,
                            var_desc_variacao,
                            reg.val_antepenultima,
                            reg.dados_antepenultima_compra,
                            reg.val_penultima,
                            reg.dados_penultima_compra,
                            reg.val_ultima,
                            reg.dados_ultima_compra,
                            reg.vaLdispersao,
                            reg.dispersao,
                            var_status_analise_compra,
                            reg.qtd_total_item_periodo,
                            reg.un_medida,
                            reg.val_total_item_periodo,
                            reg.val_dispersao_unit_periodo,
                            reg.total_dispersao_periodo,
                            reg.val_pretencao_prox_compra
                        ];
                        var_lista_reg.push(reg_compra);
                    });
                    $("#cb_itens_aud_evolucao_precos").selectpicker('refresh');
                    $("#tab_analitica_evolucao_precos").DataTable().clear().draw();
                    var dt = $("#tab_analitica_evolucao_precos").DataTable( {
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
                        "data":var_lista_reg,
                        "columns": [
                            {
                                title: "" ,
                                name: "col1",
                                class: 'details-control',
                                orderable: false,
                                //data: null,
                                defaultContent: ''
                            },
                            { title: "Família", name: "col5" },
                            { title: "Cód. Referência", name: "col2" },
                            { title: "Produto", name: "col3" },
                            { title: "Variação", name: "col4" },
                            {
                                title: "R$ Unit.",
                                name: "col6",
                                class: "details-column-antepenultima-compra"
                            },
                            {
                                title: "Antepenúltima Compra",
                                name: "col7",
                                class: "details-column-antepenultima-compra"
                            },
                            {
                                title: "R$ Unit.",
                                name: "col8",
                                class: "details-column-penultima-compra"
                            },
                            {
                                title: "Penúltima Compra",
                                name: "col9",
                                class: "details-column-penultima-compra"
                            },
                            {
                                title: "R$ Unit.",
                                name: "col10",
                                class: "details-column-ultima-compra"
                            },
                            {
                                title: "Última Compra",
                                name: "col11",
                                class: "details-column-ultima-compra"
                            },
                            { title: "Disp. Unit.(R$)", name: "col12" },
                            { title: "Disp. Unit.(%)" , name: "col13"},
                            { title: "Análise", name: "col14" },
                            { title: "Qtd. TT.", name: "col15" },
                            { title: "UN", name: "col16" },
                            { title: "Val. TT.(R$)", name: "col17" },
                            { title: "Disp. Unit. Periodo(R$)", name: "col18" },
                            { title: "TT. Disp. Período(R$)", name: "col19" },
                            {
                                title: "Sugestão Compra(R$)",
                                name: "col20",
                                class: "details-column-sugestao-compra"
                            }
                        ],
                        "columnDefs": [
                            {"className": "dt-center", "targets": [6,8,10,13,15]},
                            {"className": "dt-left", "targets": [0,1,3]},
                            {"classNsme": "dt-right", "targets": [2,4,5,7,9,11,12,14,16,17,18,19]},
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

                    var detailRows = [];

                    //$("#tab_analitica_evolucao_precos tbody" ).on('click', 'tr td.details-control', function() {
                    $("#tab_analitica_evolucao_precos tbody" ).on('click', 'td.details-control', function() {
                    var tr = $(this).closest('tr');
                    var row = dt.row(tr);
                    var idx = var_lista_reg.indexOf(tr.attr('id'));

                    var var_info_pesq_compras = $(this).find("input[type=hidden][name=hd_info_pesq_compras]").val();
                    $.ajax({
                        type: 'GET',
                        url:"/suprimentos_evolucao_precos_app/retorna_compras_item_filial",
                        data: {
                            'handle_filial': var_info_pesq_compras.split('_')[0],
                            'data_ini': var_info_pesq_compras.split('_')[1],
                            'data_fim': var_info_pesq_compras.split('_')[2],
                            'cod_ref_item': var_info_pesq_compras.split('_')[3],
                        },
                        dataType: 'json',
                        success: function(data){
                            if (row.child.isShown()) {
                                tr.removeClass('details');
                                row.child.hide();

                                // Remove from the 'open' array
                                detailRows.splice(idx, 1);
                            }
                            else {
                                tr.addClass('details');
                                row.child(format(data.compras_item)).show();
                                //if(data.compras_item.length > 3){

                                //} else {
                                //    row.child("Não há compras para exibir").show();
                                //}


                                // Add to the 'open' array
                                if (idx === -1) {
                                    detailRows.push(tr.attr('id'));
                                }

                            }

                        },
                        error: function (request, status, error) {
                            let_loader_evolucao_preco.style.display = "none";
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

                    dt.on('draw', function () {
                    detailRows.forEach(function(id, i) {
                        $('#' + id + ' td.details-control').trigger('click');
                    });
                });
                let_loader_evolucao_preco.style.display = "none";

                },
                error: function(request, status, error){
                    let_loader_evolucao_preco.style.display = "none";
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
    else if( nomeDoButton == 'btn_pesq_compras_itens_aud_evolucao_precos' ){
        var var_cod_filial = $("#cb_filial_gera_evolucao_precos").val();
        var var_comp_data_ini = $("#txt_data_ini_evolucao_precos").val();
        var var_data_ini = var_comp_data_ini.split('-')[0]+"-01-01";
            var_comp_data_ini.split('-')[0]
        var var_data_fim = $("#txt_data_fim_evolucao_precos").val();
        var var_cod_ref_item = $("#cb_itens_aud_evolucao_precos").val();
        let let_loader_evolucao_preco = document.getElementById("loader_evolucao_preco");
        let_loader_evolucao_preco.style.display = "flex";
        $.ajax({
            type: 'GET',
            url:"/suprimentos_evolucao_precos_app/retorna_compras_item_filial",
            data: {
                'handle_filial': var_cod_filial,
                'data_ini': var_data_ini,
                'data_fim': var_data_fim,
                'cod_ref_item': var_cod_ref_item
            },
            dataType: 'json',
            success: function(data){
                var_lista_compras_aud = [];
                var_lista_persistencia_compra_aud = [];
                //compras_item.forEach( compra => {
                for(var i = 0; i < data.compras_item.length; i++) {

                    var var_button_atualiza_compras_itens = `
                        <button type="button" name="btn_abre_modal_conf_salva_compras_itens"
                            id="btn_abre_modal_conf_salva_compras_itens_${i}"
                            class="btn btn-rounded btn-space"
                            value="${i}">
                            <i class="fa-solid fa-check" style="color: #f46424;"></i></button>
                    `;
                    reg = [
                        "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                        data.compras_item[i].data_compra,
                        data.compras_item[i].numero_compra,
                        data.compras_item[i].comprador,
                        data.compras_item[i].doc_fornecedor,
                        data.compras_item[i].nome_fornecedor,
                        "<input type='text' class='form-control' id='txt_val_unit_"+i+
                            "' value='"+data.compras_item[i].val_unit+"' readonly/>",
                        "<input type='text' class='form-control' name='txt_qtd' id='txt_qtd_"+i+
                            "' value='"+data.compras_item[i].qtd_comprada+"' />",
                        "<input type='text' class='form-control' id='txt_val_total_"+i+
                            "' value='"+data.compras_item[i].val_total+"' readonly/>",
                        var_button_atualiza_compras_itens
                    ];
                    var_lista_compras_aud.push(reg);

                    reg_persistencia = [
                        data.compras_item[i].handle_itens_compra,
                        data.compras_item[i].handle_filial,
                        data.compras_item[i].handle_produto,
                        data.compras_item[i].val_unit,
                        data.compras_item[i].qtd_comprada
                    ];

                    var obj = {
                        'handle_itens_compra' : data.compras_item[i].handle_itens_compra,
                        'handle_filial' : data.compras_item[i].handle_filial,
                        'handle_produto': data.compras_item[i].handle_produto,
                        'val_unit': data.compras_item[i].val_unit,
                        'qtd_comprada': data.compras_item[i].qtd_comprada
                    }

                    var_lista_persistencia_compra_aud.push(obj)
                }
                $("#tab_aud_compras_item_evolucao_precos").DataTable().clear().draw();
                $("#tab_aud_compras_item_evolucao_precos").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "scrollY": "770px",
                    //"scrollX": auto,
                    "scrollCollapse": true,
                    "paging": false,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copy'
                    ],
                    "data":var_lista_compras_aud,
                    "columns": [
                        { title: "" },
                        { title: "Data" },
                        { title: "Núm. Compra" },
                        { title: "Comprador" },
                        { title: "Doc. Fornecedor" },
                        { title: "Fornecedor" },
                        { title: "Val. Unit.(R$)" },
                        { title: "Qtd." },
                        { title: "Val. Total(R$)" },
                        { title: "Auditar" }
                    ],
                    /*"columnDefs": [
                        {"className": "dt-center", "targets": [0,2,6,7,8,9,10]},
                        {"className": "dt-left", "targets": [1,3,4,5]}
                    ],*/
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
                let_loader_evolucao_preco.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_evolucao_preco.style.display = "none";
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
    else if( nomeDoButton == 'btn_salva_compras_itens' ) {
        $("#modalConfirmaArmazenamentoComprasEditadasBenner").hide();
        console.log(var_lista_persistencia_compra_aud);
        /* Val. Unitario*/
        var_lista_persistencia_compra_aud[valButton]['val_unit'] = $("#txt_val_unit_"+valButton).val();
        /* Quantidade*/
        var_lista_persistencia_compra_aud[valButton]['qtd_comprada'] = $("#txt_qtd_"+valButton).val();

        $.ajax({
            type:'POST',
            data: {
                'array_compras_editadas' :   var_lista_persistencia_compra_aud
            },
            url: '/suprimentos_evolucao_precos_app/salva_compras_auditadas',
            dataType: 'json',
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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
    else if ( nomeDoButton == 'btn_abre_modal_conf_salva_compras_itens') {
        $("#btn_salva_compras_itens").val(valButton);
        $("#modalConfirmaArmazenamentoComprasEditadasBenner").show();
    }
    else if ( nomeDoButton == 'btnFechaModalConfirmaArmazenamentoComprasEditadasBenner') {
        $("#modalConfirmaArmazenamentoComprasEditadasBenner").hide();
    }
    else if ( nomeDoButton == 'btn_abre_modal_pesq_por_num_req') {
        $("#modal_gera_evolucao_precos_requisicao").show();
    }
    else if ( nomeDoButton == 'btn_fecha_modal_gera_evolucao_precos_requisicao') {
        $("#modal_gera_evolucao_precos_requisicao").hide();
    }


});

$(document).on('change', 'input', function(){
    var nameInput = $(this).attr('name');
	var idInput = $(this).attr('id');
    var valueInput = $(this).val();


    if ( nameInput == 'txt_qtd') {
        var var_cod_itens_compra = idInput.split('_')[2];
        var var_val_total = $("#txt_val_total_"+var_cod_itens_compra).val();

        var var_novo_val_unit =
            (var_val_total.replace('.','').replace(',','.') * 1.00)
            /
            (valueInput.replace('.','').replace(',','.') * 1.00);
        $("#txt_val_unit_"+var_cod_itens_compra).val(var_novo_val_unit.toString().replace('.',','));

    }
});


$(document).on('change', '#cb_empresas_gera_evolucao_precos', function(){
    var var_cod_empresa_selecionada = $(this).val();
    $.ajax({
        type: 'GET',
        url:"/suprimentos_evolucao_precos_app/povoa_cd_filial_por_empresa",
        data: {
            'cod_empresa': var_cod_empresa_selecionada
        },
        dataType: 'json',
        success: function(data){
            $("#cb_filial_gera_evolucao_precos option").remove();
            data.lista_filiais.forEach(fil => {
                $("#cb_filial_gera_evolucao_precos").append("<option value='"+fil.handle+"'>"+fil.nome+"</option>");
            });
            $('#cb_filial_gera_evolucao_precos').selectpicker('refresh');
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


$(document).on('change', '#cb_familia_gera_evolucao_precos', function(){
    var var_cod_familia_selecionada = $(this).val();
    var var_handle_filial = $("#cb_filial_gera_evolucao_precos").val();
    $.ajax({
        type: 'GET',
        url:"/suprimentos_evolucao_precos_app/povoa_cd_itens_by_familia",
        data: {
            'handle_familia': var_cod_familia_selecionada,
            'handle_filial': var_handle_filial
        },
        dataType: 'json',
        success: function(data){
            $("#cb_item_gera_evolucao_precos option").remove();
            $("#cb_item_gera_evolucao_precos").append("<option value='0' selected='selected'> -- Todos os itens -- </option>");
            data.lista_itens.forEach(item => {
                $("#cb_item_gera_evolucao_precos").append("<option value='"+item.cod_ref+"'>"+item.nome+"("+item.cod_ref+")</option>");
            });
            $('#cb_item_gera_evolucao_precos').selectpicker('refresh');
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





function format(compras_item) {
    var var_lista_compras = [];
    var var_table = $("<table/>");
    var_table.attr({
        style: 'margin-left: 50px;'
    });

    var var_thead = $("<thead/>");
    var var_tr_cab = $("<tr/>");

    var var_th_img = $("<th/>");
    var_th_img.html("");
    var_tr_cab.append(var_th_img);

    var var_th_dt = $("<th/>");
    var_th_dt.html("Data");
    var_tr_cab.append(var_th_dt);

    var var_th_nc = $("<th/>");
    var_th_nc.html("Núm. Compra");
    var_tr_cab.append(var_th_nc);

    var var_th_us = $("<th/>");
    var_th_us.html("Comprador");
    var_tr_cab.append(var_th_us);

    var var_th_doc = $("<th/>");
    var_th_doc.html("Doc. Fornecedor");
    var_tr_cab.append(var_th_doc);

    var var_th_forn = $("<th/>");
    var_th_forn.html("Fornecedor");
    var_tr_cab.append(var_th_forn);

    var var_th_cidade = $("<th/>");
    var_th_cidade.html("Cidade/UF");
    var_tr_cab.append(var_th_cidade);

    var var_th_unit = $("<th/>");
    var_th_unit.html("Val. Unit.(R$)");
    var_tr_cab.append(var_th_unit);

    var var_th_qtd = $("<th/>");
    var_th_qtd.html("Qtd.");
    var_tr_cab.append(var_th_qtd);

    var var_th_tt = $("<th/>");
    var_th_tt.html("Val. Total(R$)");
    var_tr_cab.append(var_th_tt);

    var var_th_num_req = $("<th/>");
    var_th_num_req.html("Num. Req.");
    var_th_num_req.attr({
        style: 'background: #FFE4B5; color:#000000;'
    });
    var_tr_cab.append(var_th_num_req);

    var var_th_dt_req = $("<th/>");
    var_th_dt_req.html("Data Req.");
    var_th_dt_req.attr({
        style: 'background: #FFE4B5; color:#000000;'
    });
    var_tr_cab.append(var_th_dt_req);

    var var_th_st_req = $("<th/>");
    var_th_st_req.html("Status Req.");
    var_th_st_req.attr({
        style: 'background: #FFE4B5; color:#000000;'
    });
    var_tr_cab.append(var_th_st_req);

    var var_th_tp_compra = $("<th/>");
    var_th_tp_compra.html("Tipo Compra");
    var_th_tp_compra.attr({
        style: 'background: #FFE4B5; color:#000000;'
    });
    var_tr_cab.append(var_th_tp_compra);

    var_thead.append(var_tr_cab);
    var_table.append(var_thead);
    compras_item.forEach( compra => {
        var var_tr = $("<tr/>");

        var var_td_img = $("<td/>");
        var_td_img.html("<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>");
        var_tr.append(var_td_img);

        var var_td_data_compra = $("<td/>");
        var_td_data_compra.html(compra.data_compra)
        var_tr.append(var_td_data_compra);

        var var_td_num_compra = $("<td/>");
        var_td_num_compra.html(compra.numero_compra);
        var_tr.append(var_td_num_compra);

        var var_td_nome_usu = $("<td/>");
        var_td_nome_usu.html(compra.comprador);
        var_tr.append(var_td_nome_usu);

        var var_td_doc_forn = $("<td/>");
        var_td_doc_forn.html(compra.doc_fornecedor);
        var_tr.append(var_td_doc_forn);

        var vat_td_nome_forn = $("<td/>");
        vat_td_nome_forn.html(compra.nome_fornecedor);
        var_tr.append(vat_td_nome_forn);

        var vat_td_cidade_forn = $("<td/>");
        vat_td_cidade_forn.html(compra.cidade_fornecedor+", "+compra.uf_fornecedor);
        var_tr.append(vat_td_cidade_forn);

        var var_td_val_unit = $("<td/>");
        var_td_val_unit.html(compra.val_unit);
        var_tr.append(var_td_val_unit);

        var var_td_qtd = $("<td/>");
        var_td_qtd.html(compra.qtd_comprada);
        var_tr.append(var_td_qtd);

        var var_td_val_tt = $("<td/>");
        var_td_val_tt.html(compra.val_total);
        var_tr.append(var_td_val_tt);

        var var_td_num_req = $("<td/>");
        var_td_num_req.attr({
            style: 'background: #FFE4B5; color:#000000;'
        });
        var_td_num_req.html(compra.numero_req);
        var_tr.append(var_td_num_req);

        var var_td_data_req = $("<td/>");
        var_td_data_req.attr({
            style: 'background: #FFE4B5; color:#000000;'
        });
        var_td_data_req.html(compra.data_req);
        var_tr.append(var_td_data_req);

        var var_td_status_req = $("<td/>");
        var_td_status_req.attr({
            style: 'background: #FFE4B5; color:#000000;'
        });
        var_td_status_req.html(compra.status_req);
        var_tr.append(var_td_status_req);

        var var_td_tipo_compra_req = $("<td/>");
        var_td_tipo_compra_req.attr({
            style: 'background: #FFE4B5; color:#000000;'
        });
        var_td_tipo_compra_req.html(compra.tipo_compra_req);
        var_tr.append(var_td_tipo_compra_req);

        var_table.append(var_tr);

    });


    var var_div_tab = $("<div/>");
    var_div_tab.append(var_table);

    return var_div_tab;
}