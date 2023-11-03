var var_lista_compras_diesel = [];
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

let let_loader_justifica_preco_diesel = document.getElementById("loader_justifica_preco_diesel");

$(document).on('click', 'button', function(){
    var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if( nomeDoButton == 'btn_retorna_compras_diesel' ) {
        atualiza_tab_compras_justificar_preco_diesel();

    }
    if( nomeDoButton == 'btn_abre_model_cad_motivo_just_compra_diesel'){
        $("#txt_desc_motivo_just_compra_diesel").val('');
        $("#modal_cad_motivos_justificar_compra_diesel").show();
    }
    if( nomeDoButton == 'btn_fecha_modal_cad_motivos_justificar_compra_diesel'){
        $("#modal_cad_motivos_justificar_compra_diesel").hide();
    }
    if( nomeDoButton == 'btn_add_novo_motivo_just_compra_diesel' ) {
        var var_desc_novo_motivo = $("#txt_desc_motivo_just_compra_diesel").val();
        $.ajax({
            type: 'POST',
            data : {
                'desc_novo_motivo': var_desc_novo_motivo
            },
            dataType: 'json',
            url: '/suprimentos_justifica_preco_diesel_app/salva_novo_motivo_just_preco_diesel',
            success: function(dados){
                $("#txt_desc_motivo_just_compra_diesel").val('');
                $("#modal_cad_motivos_justificar_compra_diesel").hide();

                $("#cb_motivo_just_compra_diesel option").remove();
                $("#cb_motivo_just_compra_diesel").append("<option value=''> -- Selecione um motivo -- </option>");
                dados.lista_motivos.forEach(motivo => {
                    $("#cb_motivo_just_compra_diesel").append("<option value='"+motivo.cod_motivo_just_preco_diesel+
                        "'>"+motivo.desc_motivo_just_preco_diesel+"</option>");
                });
                $('#cb_motivo_just_compra_diesel').selectpicker('refresh');


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
    if( nomeDoButton == 'btn_salva_justificativa_compra_diesel' ){
        var var_indice_dic_dados_compra_diesel = $("#cb_compras_diesel").val();
        var var_cod_motivo_justificativa = $("#cb_motivo_just_compra_diesel").val();

        if ( var_indice_dic_dados_compra_diesel == 'N' || var_cod_motivo_justificativa == '0') {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe a compra e/ou o motivo da justificativa do preço!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            var var_handle_item_compra = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][15];
            var var_num_compra = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][2];
            var var_data_compra = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][1];
            var var_val_unit_compra = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][8];
            var var_val_compra_ant = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][10];
            var var_handle_filial = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][16];
            var var_nome_filial = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][17];

            var var_desc_justificativa = $("#txt_area_justificativa_compra_diesel").val();
            loader_justifica_preco_diesel.style.display = "flex";
            $.ajax({
            type: 'POST',
            data: {
                'handle_item_compra': var_handle_item_compra,
                'num_compra': var_num_compra,
                'data_compra': var_data_compra,
                'val_unit_compra': var_val_unit_compra,
                'val_compra_ant': var_val_compra_ant,
                'handle_filial': var_handle_filial,
                'nome_filial': var_nome_filial,
                'desc_justificativa': var_desc_justificativa,
                'cod_motivo_justificativa': var_cod_motivo_justificativa
            },
            url: '/suprimentos_justifica_preco_diesel_app/salva_justificativa_compra_diesel',
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });


                //Atualiza dados no dicionario
                var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][18] = '(Justificado)';
                var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][19] = var_cod_motivo_justificativa;
                var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][20] =
                    $( '#cb_motivo_just_compra_diesel :selected' ).text();
                var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][21] = var_desc_justificativa;

                var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][14] =
                    "<i class='fa-solid fa-circle-check' style='color: #f46424;' " +
                    "title='"+$('#cb_motivo_just_compra_diesel :selected' ).text()+"'></i>";

                $("#cb_compras_diesel option").remove();
                $("#cb_compras_diesel").append("<option value='N' selected> -- Selecione a compra -- </option>");
                for (var i = 0;i < var_lista_compras_diesel.length; i++){
                    $("#cb_compras_diesel").append("<option value='"+i+"'>"+
                    var_lista_compras_diesel[i][2]+
                    " - Posto: "+var_lista_compras_diesel[i][3]+" - Val.: "+
                    var_lista_compras_diesel[i][11] +" "+
                    var_lista_compras_diesel[i][18]+ "</option>");
                }
                $('#cb_compras_diesel').selectpicker('refresh');

                $("#txt_area_justificativa_compra_diesel").val('');
                $("#cb_motivo_just_compra_diesel").val(0);
                $("#cb_motivo_just_compra_diesel").selectpicker('refresh');

                $("#tab_compras_diesel").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "scrollY": "500px",
                    //"scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copy'
                    ],
                    "data":var_lista_compras_diesel,
                    "columns": [
                        { title: "" },
                        { title: "Data" },
                        { title: "Núm. Compra" },
                        { title: "Posto" },
                        { title: "Item" },
                        { title: "NF" },
                        { title: "Emissão NF" },
                        { title: "Qtd.(L)" },
                        { title: "Val.(R$)" },
                        { title: "Tt.(R$)" },
                        { title: "Val. Anterior(R$)" },
                        { title: "Dif.(R$)",
                          class: "column_val_dif_class"
                        },
                        { title: "Tt. Dif(R$)",
                          class: "column_tt_dif_class"
                        },
                        { title: "% Disp. Tt.",
                          class: "perc_disp_tt_class"
                        },
                        { title: "Justificado ?" },
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [0,1,2,5,6,14 ]},
                        {"className": "dt-right", "targets": [7,8,9,10]}
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
                loader_justifica_preco_diesel.style.display = "none";


            },
            error(request, status, error){
                loader_justifica_preco_diesel.style.display = "none";
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


});


$(document).on('change', '#cb_empresas_gera_compras_just_diesel', function(){
    var var_cod_empresa_selecionada = $(this).val();
    $.ajax({
        type: 'GET',
        url:"/suprimentos_justifica_preco_diesel_app/povoa_cd_filial_por_empresa",
        data: {
            'cod_empresa': var_cod_empresa_selecionada
        },
        dataType: 'json',
        success: function(data){
            //var var_cd_filiais = document.getElementById("cb_filial_gera_compras_just_diesel");
            $("#cb_filial_gera_compras_just_diesel option").remove();
            data.lista_filiais.forEach(fil => {
                $("#cb_filial_gera_compras_just_diesel").append("<option value='"+fil.handle+"'>"+fil.nome+"</option>");
            });
            $('#cb_filial_gera_compras_just_diesel').selectpicker('refresh');
        },
        error: function (request, status, error) {
            loader_justifica_preco_diesel.style.display = "none";
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


$(document).on('change', '#cb_compras_diesel', function(){
    var var_indice_dic_dados_compra_diesel = $(this).val();
    if( var_indice_dic_dados_compra_diesel != 'N' ) {
        var var_handle_item_compra = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][15];
        var var_handle_filial = var_lista_compras_diesel[var_indice_dic_dados_compra_diesel][16];
        $.ajax({
            type: 'GET',
            url:"/suprimentos_justifica_preco_diesel_app/retorna_justificativa_compra_diesel_registrada",
            data: {
                'handle_item_compra': var_handle_item_compra,
                'handle_filial': var_handle_filial
            },
            dataType: 'json',
            success: function(data){
                $("#txt_area_justificativa_compra_diesel").val(data.justificativa);
                $("#cb_motivo_just_compra_diesel").val(data.cod_motivo);
                $("#cb_motivo_just_compra_diesel").selectpicker('refresh');
            },
            error: function (request, status, error) {
                loader_justifica_preco_diesel.style.display = "none";
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


function atualiza_tab_compras_justificar_preco_diesel(){
    var var_handle_filial = $("#cb_filial_gera_compras_just_diesel").val();
    var var_data_ini = $("#txt_data_ini_gera_compras_just_diesel").val();
    var var_data_fim = $("#txt_data_fim_gera_compras_just_diesel").val();
    loader_justifica_preco_diesel.style.display = "flex";
    $.ajax({
        type: 'GET',
        data : {
            'handle_filial': var_handle_filial,
            'data_ini': var_data_ini,
            'data_fim': var_data_fim
        },
        url: '/suprimentos_justifica_preco_diesel_app/retorna_compras_diesel',
        dataType: 'json',
        success: function(dados){

            $("#cb_compras_diesel option").remove();
            $("#cb_compras_diesel").append("<option value='N'> -- Selecione a compra -- </option>");

            var_lista_compras_diesel = [];
            for (var i = 0;i < dados.lista_compras_diesel_tab.length; i++){
                reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    dados.lista_compras_diesel_tab[i].data_compra,
                    dados.lista_compras_diesel_tab[i].num_compra,
                    dados.lista_compras_diesel_tab[i].nome_posto,
                    dados.lista_compras_diesel_tab[i].desc_item,
                    dados.lista_compras_diesel_tab[i].num_nf,
                    dados.lista_compras_diesel_tab[i].emissao_nf,
                    dados.lista_compras_diesel_tab[i].qtd_l,
                    dados.lista_compras_diesel_tab[i].val_unit,
                    dados.lista_compras_diesel_tab[i].val_tt,
                    dados.lista_compras_diesel_tab[i].val_unit_ant,
                    dados.lista_compras_diesel_tab[i].val_dif_atual_ant,
                    dados.lista_compras_diesel_tab[i].val_disp_tt,
                    dados.lista_compras_diesel_tab[i].perc_disp_tt,
                    dados.lista_compras_diesel_tab[i].img_indica_justificativa_existe,
                    dados.lista_compras_diesel_tab[i].handle_itens_compra,
                    dados.lista_compras_diesel_tab[i].handle_filial,
                    dados.lista_compras_diesel_tab[i].nome_filial,
                    dados.lista_compras_diesel_tab[i].status,
                    dados.lista_compras_diesel_tab[i].cod_motivo_just,
                    dados.lista_compras_diesel_tab[i].desc_motivo_just,
                    dados.lista_compras_diesel_tab[i].desc_justificativa
                ];
                var_lista_compras_diesel.push(reg);

                $("#cb_compras_diesel").append("<option value='"+i+"'>"+
                    dados.lista_compras_diesel_tab[i].num_compra+
                    " - Posto: "+dados.lista_compras_diesel_tab[i].nome_posto+" - Val.: "+
                    dados.lista_compras_diesel_tab[i].val_dif_atual_ant +" "+
                    dados.lista_compras_diesel_tab[i].status+ "</option>");

            }
            $("#tab_compras_diesel").DataTable( {
                "bJQueryUI": true,
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
                ],
                "data":var_lista_compras_diesel,
                "columns": [
                    { title: "" },
                    { title: "Data" },
                    { title: "Núm. Compra" },
                    { title: "Posto" },
                    { title: "Item" },
                    { title: "NF" },
                    { title: "Emissão NF" },
                    { title: "Qtd.(L)" },
                    { title: "Val.(R$)" },
                    { title: "Tt.(R$)" },
                    { title: "Val. Anterior(R$)" },
                    { title: "Dif.(R$)",
                      class: "column_val_dif_class"
                    },
                    { title: "Tt. Dif(R$)",
                      class: "column_tt_dif_class"
                    },
                    { title: "% Disp. Tt.",
                      class: "perc_disp_tt_class"
                    },
                    { title: "Justificado ?" },
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,1,2,5,6,14 ]},
                    {"className": "dt-right", "targets": [7,8,9,10]}
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
            $('#cb_compras_diesel').selectpicker('refresh');

            $("#cb_motivo_just_compra_diesel option").remove();
            $("#cb_motivo_just_compra_diesel").append("<option value='0'> -- Selecione o motivo da justificativa -- </option>");
            dados.lista_motivos_justificativa.forEach( motivo => {
                $("#cb_motivo_just_compra_diesel").append("<option value='"+motivo.cod_motivo_just_preco_diesel+"'>"+
                    motivo.desc_motivo_just_preco_diesel+"</option>");
            });
            $('#cb_motivo_just_compra_diesel').selectpicker('refresh');
            loader_justifica_preco_diesel.style.display = "none";
        },
        error: function(request, status, error){
            loader_justifica_preco_diesel.style.display = "none";
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