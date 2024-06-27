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

    let loader_gera_pag_terc_2art = document.getElementById("loader_gera_pag_terc_2art");

    /* Variáveis globais */
    let let_lista_dados_2art_terceiros = [];
    let let_lista_dados_2art_terceiros_agrupado_por_beneficiario = [];

    let let_dataAtual = new Date();
    let let_dia_atual = let_dataAtual.getDate();
    let let_mes_atual = let_dataAtual.getMonth()+1;
    let let_ano_atual = let_dataAtual.getFullYear();

    if ( String(let_dia_atual).length == 1 ) {
        let_dia_atual = '0' + let_dia_atual;
    }
    if ( String(let_mes_atual).length == 1 ) {
        let_mes_atual = '0' + let_mes_atual;
    }

    let let_data_ini_y_m_d = let_ano_atual+"-"+let_mes_atual+"-01";
    let let_data_fim_y_m_d = let_ano_atual+"-"+let_mes_atual+"-"+let_dia_atual;

    $("#dt_pesq_mapas_terc_periodo_ini").val(let_data_ini_y_m_d);
    $("#dt_pesq_mapas_terc_periodo_fim").val(let_data_fim_y_m_d);

    $('#tab_mapas_terceitos_2art').DataTable( {
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
        "data":let_lista_dados_2art_terceiros,
        "columns": [
            { title: "" },
            { title: "Data" },
            { title: "Mapa" },
            { title: "Placa" },
            { title: "Tipo Entrega" },
            { title: "Beneficiário" },
            { title: "Tipo Pessoa" },
            { title: "Perfil Veículo" },
            { title: "Região" },
            { title: "Qtd. Entregas" },
            { title: "Tipo Imposto" },
            { title: "Perc. Imposto" },
            { title: "Val. Frete" },
            { title: "Val. Calculado" },
            { title: "Diferença" },
            { title: "Val. Faturado" },
            { title: "Descontos" },
            { title: "Acréscimos" },
            { title: "Val. á Pagar" },
            { title: "Val. CONLOG" },
            { title: "Lançamentos" },
            { title: "Status Pagamento" },
            { title: "Serial Pagamento"},
            { title: "Validação" },
            { title: "Ativa/Desativa" }
        ],
        "columnDefs": [
            {"className": "dt-center", "targets": [0,2,3,4,6,7,8,9,10,20,21,22,23,24]},
            {"className": "dt-left", "targets": [5]},
            {"className": "dt-right", "targets": [11,12,13,14,15,16,17,18,19]}
        ],
        "language": {
            "decimal": ",",
            "thousands": ".",
            "sEmptyTable": "Nenhum registro encontrado",
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


        },
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace('.','').replace(',','.') * 1.00 :
                    typeof i === 'number' ?
                        i : 0;
            };



            // Total over all pages
            total_frete = api
                .column( 12 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_frete = api
                .column( 12, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 12 ).footer() ).html(
                pageTotal_frete.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            );


            // Total over all pages
            total_calculado = api
                .column( 13 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_calculado = api
                .column( 13, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 13 ).footer() ).html(
                pageTotal_calculado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) 
            );


             // Total over all pages
             total_diferenca = api
             .column( 14 )
             .data()
             .reduce( function (a, b) {
                 return intVal(a) + intVal(b);
             }, 0 );

            // Total over this page
            pageTotal_diferenca = api
                .column( 14, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 14 ).footer() ).html(
                pageTotal_diferenca.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            );


            // Total over all pages
            total_faturado = api
                .column( 15 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_faturado = api
                .column( 15, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 15 ).footer() ).html(
                pageTotal_faturado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            );


            // Total over all pages
            total_descontos = api
                .column( 16 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_descontos = api
                .column( 16, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 16 ).footer() ).html(
                pageTotal_descontos.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            );

            // Total over all pages
            total_acrescimos = api
                .column( 17 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_acrescimos = api
                .column( 17, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 17 ).footer() ).html(
                pageTotal_acrescimos.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) 
            );

            // Total over all pages
            total_val_pagar = api
                .column( 18 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_val_pagar = api
                .column( 18, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 18 ).footer() ).html(
                pageTotal_val_pagar.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            );


            total_val_conlog = api
                .column( 19 )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            pageTotal_val_conlog = api
                .column( 19, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.column( 19 ).footer() ).html(
                pageTotal_val_conlog.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            );
            // teste footer
            // $( api.column( 19 ).footer() ).html(
            //     pageTotal_val_conlog.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) +
            //         ' De '+ total_val_conlog.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            // );
        }

  });



});

$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_pesq_mapas_terceiros") {
        povoa_tab_mapas_terceitos_2art();
    }
    else if (let_nome_btn == 'btn_desativa_mapa'){
        let let_indice_lista_dados_cad_lanc_2art_terc = let_val_btn
        let let_mapa = let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][2];
        $("#p_msg_ativa_desativa").html("Você Tem certeza que deseja DESATIVAR o mapa "+let_mapa+"?");
        $("#hd_cod_2art_terc_financ").val(let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][25]);
        $("#hd_status_2art_financ").val("N");
        $("#ta_justificativa_acao_mapa_2art_terc").val("");
        $("#modal_ativa_desativa_mapa_terc").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_ativa_desativa_mapa_terc') {
        $("#modal_ativa_desativa_mapa_terc").hide();
    }
    else if ( let_nome_btn == 'btn_executa_ativa_desativa_mapa_terc_selecionado') {
        let let_cod_2art_terc_financ = $("#hd_cod_2art_terc_financ").val();
        let let_status_mapa = $("#hd_status_2art_financ").val();
        let let_justificativa_status_mapa = $("#ta_justificativa_acao_mapa_2art_terc").val();
        $.ajax({
            type: 'POST',
            url: '/plan_controle_fat_2art_terc_app/altera_status_mapa_2art_terc_financ',
            data: {
                'cod_2art_terc_financ'       :   let_cod_2art_terc_financ,
                'status_mapa'               :   let_status_mapa,
                'justificativa_status_mapa' :   let_justificativa_status_mapa
            },
            dataType: 'json',
            success: function (data) {
                $("#modal_ativa_desativa_mapa_terc").hide();
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tab_mapas_terceitos_2art();
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
    else if ( let_nome_btn == 'btn_ativa_mapa') {
        let let_indice_lista_dados_cad_lanc_2art_terc = let_val_btn
        let let_mapa = let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][2];
        $("#p_msg_ativa_desativa").html("Você Tem certeza que deseja ATIVAR o mapa "+let_mapa+" ?");
        $("#hd_cod_2art_terc_financ").val(let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][25]);
        $("#hd_status_2art_financ").val("S");
        $("#ta_justificativa_acao_mapa_2art_terc").val("");
        $("#modal_ativa_desativa_mapa_terc").show();
    }
    else if ( let_nome_btn == 'btn_verifica_placas_inativas_benner'){
        atualiza_tab_placas_intativas_benner('btn_verifica_placas_inativas_benner');
    }
    else if ( let_nome_btn == 'btn_fecha_modal_verifica_placas_inativas_benner' ) {
        $("#modal_verifica_placas_inativas_benner").hide();
        povoa_tab_mapas_terceitos_2art();
    }
    else if ( let_nome_btn == 'btn_altera_status_mapa_com_benner' ){
        $.ajax({
            type: "POST",
            data: {
                'nome_componente'         :   'btn_altera_status_mapa_com_benner',
                'cod_2art_terc_financ'    :   let_val_btn.split('_')[0],
                'status_registro'         :   let_val_btn.split('_')[1]
            },
            url: '/plan_controle_fat_2art_terc_app/altera_status_igual_ao_benner_mapa_placas_2art_terc_financ',
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                atualiza_tab_placas_intativas_benner('btn_verifica_placas_inativas_benner');

            },
            error: function(request, error, status){
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
    else if ( let_nome_btn == 'btn_sincroniza_beneficiarios_benner' ){
        atualiza_dados_placa_benef_sinc_benner('btn_sincroniza_beneficiarios_benner');

        $("#modal_sincroniza_dados_placa_benef_benner").show();
        $('#dt_ini_placa_sinc_benner').val($("#dt_pesq_mapas_terc_periodo_ini").val());
        $('#dt_fim_placa_sinc_benner').val($("#dt_pesq_mapas_terc_periodo_fim").val());


    }
    else if ( let_nome_btn ==  'btn_fecha_modal_sincroniza_dados_placa_benef_benner') {
        $("#modal_sincroniza_dados_placa_benef_benner").hide();
        povoa_tab_mapas_terceitos_2art();
    }
    else if ( let_nome_btn == 'btn_cad_placa_benef_sinc_benner' ){
        let let_data_ini_vigencia = $("#dt_ini_placa_sinc_benner").val();
        let let_data_fim_vigencia = $("#dt_fim_placa_sinc_benner").val();
        if ( let_data_ini_vigencia == '' || let_data_fim_vigencia == '' ){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Verifique se data de vigência foi informada corretamente!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
            let let_placa_benner = $("#hd_placa_tab_sinc_benner_"+let_val_btn).val();
            let let_perfil_placa = $("#hd_perfil_placa_tab_sinc_benner_"+let_val_btn).val();
            let let_nome_benef_benner = $("#hd_nome_benef_tab_sinc_benner_"+let_val_btn).val();
            let let_doc_benef__benner = $("#hd_doc_benef_tab_sinc_benner_"+let_val_btn).val();
            let let_tipo_pessoa_benner = $("#hd_tipo_benef_tab_sinc_benner_"+let_val_btn).val();
            let let_benef_ativo_benner = '';
            if( $("#hd_status_benef_tab_sinc_benner_"+let_val_btn).val() == 'N' ) {
                let_benef_ativo_benner = 'S';
            } else if ( $("#hd_status_benef_tab_sinc_benner_"+let_val_btn).val() == 'S' ) {
                let_benef_ativo_benner = 'N';
            }
            let let_handle_benef_benner = $("#hd_handle_benef_tab_sinc_benner_"+let_val_btn).val();

            $.ajax({
                type: 'POST',
                data: {
                    'nome_componente'   :   'btn_cad_placa_benef_sinc_benner',
                    'cod_projeto'       :   let_cod_projeto,
                    'nome_benef'        :   let_nome_benef_benner,
                    'doc_benef'         :   let_doc_benef__benner,
                    'tipo_pessoa'       :   let_tipo_pessoa_benner,
                    'handle_benef'      :   let_handle_benef_benner,
                    'status_benef'      :   let_benef_ativo_benner,
                    'handle_placa'      :   let_val_btn,
                    'placa_benner'      :   let_placa_benner,
                    'perfil_placa'      :   let_perfil_placa,
                    'data_ini_vig'      :   let_data_ini_vigencia,
                    'data_fim_vig'      :   let_data_fim_vigencia
                },
                url: '/plan_controle_fat_2art_terc_app/sincronizar_dados_placa_benef_com_benner',
                success: function(dados){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    atualiza_dados_placa_benef_sinc_benner('btn_sincroniza_beneficiarios_benner');
                },
                error: function(request, error, status){
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
    else if ( let_nome_btn == 'btn_vincula_beneficiario') {
        let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
        let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
        let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();
        $.ajax({
            type:'GET',
            url: '/plan_controle_fat_2art_terc_app/vincular_placa_2art_cad_placa_terc',
            data: {
                'nome_componente'   :   'btn_vincula_beneficiario',
                'codprojeto'        :   let_cod_projeto,
                'datainicial'       :   let_data_ini,
                'datafinal'         :   let_data_fim
            },
            dataType: 'json',
            success: function (dados) {
                povoa_tab_mapas_terceitos_2art();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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
    else if ( let_nome_btn == 'btn_atualiza_fretes_mapas_terc') {
        let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
        let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
        let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();
        $.ajax({
            type: 'GET',
            url: '/plan_controle_fat_2art_terc_app/atualiza_frete_mapas_pendentes_terc',
            data: {
                'nome_componente'   :   'btn_atualiza_fretes_mapas_terc',
                'cod_projeto'       :   let_cod_projeto,
                'data_ini'          :   let_data_ini,
                'data_fim'          :   let_data_fim
            },
            dataType: 'json',
            success: function (dados) {
                povoa_tab_mapas_terceitos_2art();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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
    else if ( let_nome_btn == 'btn_efetuar_pagamento_todos_mapas') {
        $("#btn_confirma_fat_agrupado_terc_financ").prop("disabled", false);
        let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
        let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
        let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();

        let let_data_ini_formatada = let_data_ini.split('-')[2] + '-' +
            let_data_ini.split('-')[1] + '-' +
            let_data_ini.split('-')[0]

        let let_data_fim_formatada = let_data_fim.split('-')[2] + '-' +
            let_data_fim.split('-')[1] + '-' +
            let_data_fim.split('-')[0]

        /* let let_desc_proj_fat = $("#cb_projetos_pesq_mapas_terc option").prop("selected", true).text().trim(); */
        let let_desc_proj_fat = ''
        $("#cb_projetos_pesq_mapas_terc option:selected").each(function () {
           var $this = $(this);
           if ($this.length) {
            let_desc_proj_fat += $this.text().trim();
           }
        });
        $("#txt_desc_proj_fat_agrupado_terc_financ").val(let_desc_proj_fat);
        $("#txt_periodo_mapas_fat_agrupado_terc_financ").val(let_data_ini_formatada+" à "+let_data_fim_formatada);
        let let_data = new Date();
        let let_data_referencia = (let_data.getMonth() + 1)+"/"+let_data.getFullYear();
        $("#dt_perido_ref_fat_agrupado_terc_financ").val(let_data_referencia);

        povoa_tab_faturamento_agrupado_por_beneficiario();
        $("#modal_fat_agrupado_beneficiario_2art_terc").show();
    }
    else if ( let_nome_btn == 'btn_fecha_modal_fat_agrupado_beneficiario_2art_terc') {
        let_lista_dados_2art_terceiros_agrupado_por_beneficiario = [];
        $("#modal_fat_agrupado_beneficiario_2art_terc").hide();
        povoa_tab_mapas_terceitos_2art();
    }
    else if ( let_nome_btn == 'btn_confirma_fat_agrupado_terc_financ') {
        $(this).prop("disabled", true);
        let let_referencia = $("#dt_perido_ref_fat_agrupado_terc_financ").val();
        let let_cod_projeto = $("#txt_desc_proj_fat_agrupado_terc_financ").val();
        let let_obs = $("#txt_obs_fat_pag_agrupado_terc_financ").val();

        if ( let_referencia == "" || let_referencia == null ){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Referência pagamento não informado!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            let let_nome_beneficiario = '';
            let let_lista_registro = [];
            for (let i = 0; i < let_lista_dados_2art_terceiros_agrupado_por_beneficiario.length; i++) {
                let let_registro = {
                    'cod_2art_terc_financ'  :   let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][13],
                    'cod_beneficiario'      :   let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][12],
                    'nome_beneficiario'     :   let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][1],
                    'qtd_mapas'             :   let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][2],
                    'val_ff_calc'           :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][4].replace('.','').replace(',','.'),
                    'val_tt_acres'          :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][7].replace('.','').replace(',','.'),
                    'val_tt_conlog'         :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][10].replace('.','').replace(',','.'),
                    'val_tt_desc'           :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][8].replace('.','').replace(',','.'),
                    'val_tt_fat'            :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][6].replace('.','').replace(',','.'),
                    'val_tt_frete'          :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][3].replace('.','').replace(',','.'),
                    'val_tt_pagar'          :
                        let_lista_dados_2art_terceiros_agrupado_por_beneficiario[i][9].replace('.','').replace(',','.'),
                    'data_referencia'       :   let_referencia,
                    'cod_projeto'           :   let_cod_projeto,
                    'obs'                   :   let_obs
                }
                let_lista_registro.push(let_registro);
            }
            $.ajax({
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                url: "/plan_controle_fat_2art_terc_app/confirma_pag_beneficiario",
                data: JSON.stringify({
                    lista_registros_json    : let_lista_registro
                }),
                success: function(data){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    $("#modal_fat_agrupado_beneficiario_2art_terc").hide();
                    povoa_tab_mapas_terceitos_2art();
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
    else if ( let_nome_btn == 'btn_efetuar_pagamento_processado_beneficiario') {
        let let_indice_array_tab_pag = let_val_btn;
        let let_referencia = $("#dt_perido_ref_fat_agrupado_terc_financ").val();
        let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
        let let_obs = $("#txt_obs_fat_pag_agrupado_terc_financ").val();
        let let_lista_registro = [];
        if ( let_referencia == "" || let_referencia == null ){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Referência pagamento não informado!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $("#btn_efetuar_pagamento_processado_beneficiario"+let_val_btn).prop("disabled", true);
            let let_registro = {
            'cod_2art_terc_financ'  :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][13],
            'cod_beneficiario'      :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][12],
            'nome_beneficiario'     :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][1],
            'qtd_mapas'             :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][2],
            'val_ff_calc'           :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][4]
                    .replace('.','').replace(',','.'),
            'val_tt_acres'          :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][7]
                    .replace('.','').replace(',','.'),
            'val_tt_conlog'         :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][10]
                    .replace('.','').replace(',','.'),
            'val_tt_desc'           :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][8]
                    .replace('.','').replace(',','.'),
            'val_tt_fat'            :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][6]
                    .replace('.','').replace(',','.'),
            'val_tt_frete'          :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][3]
                    .replace('.','').replace(',','.'),
            'val_tt_pagar'          :
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario[let_indice_array_tab_pag][9]
                    .replace('.','').replace(',','.'),
            'data_referencia'       :   let_referencia,
            'cod_projeto'           :   let_cod_projeto,
            'obs'                   :   let_obs
        }
            let_lista_registro.push(let_registro);
            $.ajax({
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                url: "/plan_controle_fat_2art_terc_app/confirma_pag_beneficiario",
                data: JSON.stringify({
                    'lista_registros_json'  : let_lista_registro
                }),
                success: function(data){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    povoa_tab_faturamento_agrupado_por_beneficiario();
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
    else if (let_nome_btn == "btn_lanc_reg_2art_terc_financ") {
        let let_indice_lista_dados_cad_lanc_2art_terc =  let_val_btn;
        $("#list_tipo_ccorrencia_lanc_2art_terc").val(0);
        $("#txt_mapa_ocorrencia_lanc_2art_terc").val("");
        $("#txt_placa_lanc_2art_terc").val(let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][3]
            .split("-")[0].replace(' ',''));
        $("#txt_data_ocorrencia_lanc_2art_terc").val("");
        $("#txt_valor_lanc_2art_terc").val("0,00");
        $("#txt_obs_lanc_2art_terc").val("");
        $("#tab_lanc_2art_terc").DataTable().clear().draw();

        $("#hd_indice_array_pesq_2art_terc").val(let_indice_lista_dados_cad_lanc_2art_terc);
        let let_cabecalho_form =
            `<span class="text-white">
                <i class="fa-solid fa-paperclip"></i>
                <span>Lançamentos Financeiro Acréscimos / Descontos do Mapa<br/></span>
                <span style="text-transform:capitalize; font-size:0.85rem;">
                Beneficiário: `+ let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][5]+
                ` | Mapa: `+ let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][2]+
                ` | Placa: `+ let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][3].split("-")[0]+
                ` | Data: `+ let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][1]+ `</span> </span>`;



        $("#div_modal_header_modal_lanc_2art_terc").html(let_cabecalho_form);

        $("#hd_cod_reg_2art_terc_financ").val(let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][25]);
        let let_cod_reg_2art_terc_financ = let_lista_dados_2art_terceiros[let_indice_lista_dados_cad_lanc_2art_terc][25];

        povoa_tab_lanc_acres_desc_do_mapa(let_cod_reg_2art_terc_financ);

        $("input[type=text][name=txt_valor_lanc_2art_terc]").mask('999,99', {placeholder: "0,00"});

        $("#modal_lanc_2art_terc").show();

    }
    else if ( let_nome_btn == 'btn_fecha_modal_lanc_2art_terc') {
        $("#list_tipo_lancamento_lanc_2art_terc").val("0");
        $("#list_tipo_ccorrencia_lanc_2art_terc").val("0");
        $("#txt_mapa_ocorrencia_lanc_2art_terc").val("");
        $("#txt_valor_lanc_2art_terc").val("");
        $("#dt_ocorrencia_lanc_2art_terc").val("");
        $("#txt_obs_lanc_2art_terc").val("");
        $("#modal_lanc_2art_terc").hide();

        povoa_tab_mapas_terceitos_2art();


    }
    else if ( let_nome_btn == 'btn_salva_reg_lanc_2art_terc') {
        let let_cod_reg_2art_terc_financ = $("#hd_cod_reg_2art_terc_financ").val();
        let let_tipo_lancamento = $("#list_tipo_lancamento_lanc_2art_terc").val();
        let let_tipo_ocorrencia = $("#list_tipo_ccorrencia_lanc_2art_terc").val();
        let let_mapa_ocorrencia = $("#txt_mapa_ocorrencia_lanc_2art_terc").val();
        let let_placa_lan = $("#txt_placa_lanc_2art_terc").val();
        let let_data_ocorrencia = $("#dt_ocorrencia_lanc_2art_terc").val();
        let let_valor = $("#txt_valor_lanc_2art_terc").val();
        let let_obs = $("#txt_obs_lanc_2art_terc").val();

        $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/salva_registro_lanc_2art_terc",
            data: {
                'cod_registro_2art_terc_financ'     :   let_cod_reg_2art_terc_financ,
                'tipo_lancamento'                   :   let_tipo_lancamento,
                'tipo_ocorrencia'                   :   let_tipo_ocorrencia,
                'mapa_ocorrencia'                   :   let_mapa_ocorrencia,
                'placa_lanc'                        :   let_placa_lan,
                'data_ocorrencia'                   :   let_data_ocorrencia,
                'valor'                             :   let_valor.replace(',','.'),
                'obs'                               :   let_obs
              },
            success: function(dados){
                $("#list_tipo_lancamento_lanc_2art_terc").val("0");
                $("#list_tipo_ccorrencia_lanc_2art_terc").val("0");
                $("#txt_mapa_ocorrencia_lanc_2art_terc").val("");
                $("#txt_valor_lanc_2art_terc").val("");
                $("#dt_ocorrencia_lanc_2art_terc").val("");
                $("#txt_obs_lanc_2art_terc").val("");
                povoa_tab_lanc_acres_desc_do_mapa(let_cod_reg_2art_terc_financ);
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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
    else if ( let_nome_btn == 'btn_excluir_reg_lanc_2art_terc' ){
        let let_cod_lanc_2art_terc = let_val_btn;

        $.ajax({
            type: 'DELETE',
            url: '/plan_controle_fat_2art_terc_app/desativa_lanc_reg_2art_terc_financ/'+let_cod_lanc_2art_terc,
            dataType: 'json',
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tab_lanc_acres_desc_do_mapa(data.cod_reg_2art_financ);
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
    else if ( let_nome_btn == 'btn_efetuar_pagamento_todos_mapas_beneficiario') {
        let let_id_beneficiario_pag = $("#cb_benef_pesq_mapas_terc").val();
        let let_nome_beneficiario_pag = let_lista_dados_2art_terceiros[0][5];
        let let_total_mapas_pag = let_lista_dados_2art_terceiros.length;
        let let_total_frete_pag = 0;
        let let_total_calc_pag = 0;
        let let_total_dif_pag = 0;
        let let_total_faturado_pag = 0;
        let let_total_acresc_pag = 0;
        let let_total_desc_pag = 0;
        let let_total_pagar = 0;
        let let_total_conlog = 0;
        for (let i = 0; i < let_lista_dados_2art_terceiros.length; i++) {
            if  ( let_lista_dados_2art_terceiros[i][26] == 'A' ) {
                let_total_frete_pag += let_lista_dados_2art_terceiros[i][12].split(' ')[0].replace('.','').replace(',','.') * 1.00;
                let_total_calc_pag += let_lista_dados_2art_terceiros[i][13].replace('.','').replace(',','.') * 1.00;
                let_total_dif_pag += let_lista_dados_2art_terceiros[i][14].replace('R$','').replace('.','').replace(',','.') * 1.00;
                let_total_faturado_pag += let_lista_dados_2art_terceiros[i][15].split(' ')[0].replace('.','').replace(',','.') * 1.00;
                let_total_acresc_pag += let_lista_dados_2art_terceiros[i][17].replace('.','').replace(',','.') * 1.00;
                let_total_desc_pag += let_lista_dados_2art_terceiros[i][16].replace('.','').replace(',','.') * 1.00;
                let_total_pagar += let_lista_dados_2art_terceiros[i][18].replace('.','').replace(',','.') * 1.00;
                let_total_conlog += let_lista_dados_2art_terceiros[i][19].replace('.','').replace(',','.') * 1.00;
            }
        }
        $("#div_nome_beneficiario_efet_pag_terc_financ").html("Beneficiário<br/>"+let_nome_beneficiario_pag);
        $("#txt_qtd_mapas_efet_pag_terc_financ").val(let_total_mapas_pag);
        $("#txt_obs_efet_pag_terc_financ").val("");
        $("#div_val_total_frete_efet_pag_terc_financ").html("Total Frete(R$)<br/>"+let_total_frete_pag.toLocaleString('pt-BR'));
        $("#div_val_total_calculado_efet_pag_terc_financ").html("Total Calculado(R$)<br/>"+let_total_calc_pag.toLocaleString('pt-BR'));
        $("#div_val_total_diferenca_efet_pag_terc_financ").html("Total(R$)<br/>"+let_total_dif_pag.toLocaleString('pt-BR'));
        $("#div_val_total_faturado_efet_pag_terc_financ").html("Total Faturado(R$)<br/>"+let_total_faturado_pag.toLocaleString('pt-BR'));
        $("#div_val_total_acresc_efet_pag_terc_financ").html("Total Acréscimos(R$)<br/>"+let_total_acresc_pag.toLocaleString('pt-BR'));
        $("#div_val_total_desc_efet_pag_terc_financ").html("Total Descontos(R$)<br/>"+let_total_desc_pag.toLocaleString('pt-BR'));
        $("#div_val_total_pagar_efet_pag_terc_financ").html("Total À Pagar(R$)<br/>"+let_total_pagar.toLocaleString('pt-BR'));
        $("#div_val_total_conlog_efet_pag_terc_financ").html("Total Conlog(R$)<br/>"+let_total_conlog.toLocaleString('pt-BR'));

        $("#hd_id_beneficiario_pag_2art_financ").val(let_id_beneficiario_pag);
        $("#hd_val_frete_calc_pag_2art_financ").val(let_total_calc_pag);
        $("#hd_val_acrescimo_pag_2art_financ").val(let_total_acresc_pag);
        $("#hd_val_desconto_pag_2art_financ").val(let_total_desc_pag);
        $("#hd_val_pagar_pag_2art_financ").val(let_total_pagar);
        $("#hd_val_conlog_pag_2art_financ").val(let_total_conlog);

        let let_data_atual = new Date();
        let let_data_referencia = (let_data_atual.getMonth() + 1)+"/"+let_data_atual.getFullYear();
        $("#txt_perido_ref_efet_pag_terc_financ").val(let_data_referencia);

        $("#modal_efetua_pag_2art_terc_financ").show();

    }
    else if ( let_nome_btn == 'btn_fecha_modal_efetua_pag_2art_terc_financ') {
        $("#modal_efetua_pag_2art_terc_financ").hide();

    }
    else if ( let_nome_btn == 'btn_model_atualiza_mapa') {
        var varIndiceListaDadosCadLanc2ArtTerc = let_val_btn
        var varMapa = let_lista_dados_2art_terceiros[varIndiceListaDadosCadLanc2ArtTerc][2];
        $("#pMsglAtualizaDadosMapaTerc").html("Você tem certeza que deseja ATUALIZAR o mapa "+varMapa+" ?");
        $("#hiddenCod2ArtTercFinanc").val(let_lista_dados_2art_terceiros[varIndiceListaDadosCadLanc2ArtTerc][25]);

        $("#modalAtualizaDadosMapaTerc").show();

    }
    else if ( let_nome_btn == 'btnFechaModalAtualizaDadosMapaTerc') {
        $("#modalAtualizaDadosMapaTerc").hide();

    }
    else if ( let_nome_btn == 'btnExecutaAtualizacaoDadosMapaTercFinanSelecionado') {
        var varCod2ArtTercFinanc = $("#hiddenCod2ArtTercFinanc").val();
        $.ajax({
            type: 'POST',
            url: '/plan_controle_fat_2art_terc_app/atualiza_dados_reg_2art_terc_financ',
            data: {
                'cod_reg_2art_terc_financ'   :   varCod2ArtTercFinanc
            },
            dataType: 'json',
            success: function (data) {
                $("#modalAtualizaDadosMapaTerc").hide();
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tab_mapas_terceitos_2art();
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


});


$(document).on('change', '#cb_projetos_pesq_mapas_terc', function(){
    povoa_cb_beneficiarios();
});


$(document).on('change', '#dt_pesq_mapas_terc_periodo_ini', function(){
    povoa_cb_beneficiarios();
});

$(document).on('change', '#dt_pesq_mapas_terc_periodo_fim', function(){
    povoa_cb_beneficiarios();
});

function povoa_cb_beneficiarios(){
    let let_projeto_selecionado = $("#cb_projetos_pesq_mapas_terc").val();
    let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
    let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();

    if (let_projeto_selecionado == "" || let_data_ini == "" || let_data_fim == "") {
        $("#cb_benef_pesq_mapas_terc option").remove();
        $("#cb_benef_pesq_mapas_terc").selectpicker('refresh');
    } else {
        $.ajax({
            type: 'GET',
            url: '/plan_controle_fat_2art_terc_app/povoa_cb_benef_pesq_mapas_terc',
            data: {
                'cod_projeto'   :   let_projeto_selecionado,
                'data_ini'      :   let_data_ini,
                'data_fim'      :   let_data_fim
            },
            dataType: 'json',
            success: function (data) {
                $("#cb_benef_pesq_mapas_terc option").remove();
                $("#cb_benef_pesq_mapas_terc")
                    .append("<option value='0' selected='selected'>-- Todos os Beneficiários --</option>");
                data.lista_beneficiarios.forEach(benef => {
                    $("#cb_benef_pesq_mapas_terc").append("<option value='"+
                    benef.cod_cad_placa_terc__cod_benef_terc__cod_benef_terc+"'>"+benef.cod_cad_placa_terc__cod_benef_terc__doc_benef_terc+"-"+benef.cod_cad_placa_terc__cod_benef_terc__nome_benef_terc+"("+benef.cod_cad_placa_terc__cod_benef_terc__tipo_pessoa_benef_terc+")</option>");

                });
                $("#cb_benef_pesq_mapas_terc").selectpicker('val', '0');
                $("#cb_benef_pesq_mapas_terc").selectpicker('refresh');

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

function povoa_tab_mapas_terceitos_2art(){
    let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
    let let_cod_beneficiario = $("#cb_benef_pesq_mapas_terc").val();

    if ( let_cod_beneficiario == "" || let_cod_beneficiario == null ){
        let_cod_beneficiario = 0;
    }
    let let_check_mapas_desativados = $("#chk_mapa_desativado").prop("checked");
    let let_val_mapas_ativos = 'S';
    if ( let_check_mapas_desativados == true ) {
        let_val_mapas_ativos = 'N';
    }
    let let_data_inicial = $("#dt_pesq_mapas_terc_periodo_ini").val();
    let let_data_final = $("#dt_pesq_mapas_terc_periodo_fim").val();
    if ( let_data_inicial == "" || let_data_final == "" ) {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Período informado incorreto!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        loader_gera_pag_terc_2art.style.display = "flex";
        $.ajax({
        url:"/plan_controle_fat_2art_terc_app/pesq_mapas_terceiros",
        data: {
            'cod_projeto'          :   let_cod_projeto,
            'cod_beneficiario'     :   let_cod_beneficiario,
            'check_mapas_ativos'   :   let_val_mapas_ativos,
            'data_inicial'         :   let_data_inicial,
            'data_final'           :   let_data_final

          },
        success: function(data){
            let let_btn_verifica_placas_inativas_benner = `
                <button type='button' name='btn_verifica_placas_inativas_benner'
                id='btn_verifica_placas_inativas_benner'
                class='mr-2 btn btn-primary btn-rounded botaoPrincipal'>
                <i class="fa-solid fa-triangle-exclamation"></i>Verifica Placas Inativas Benner
                </button>
            `;
            let let_btn_sincroniza_beneficiarios_benner = `
                <button type='button' name='btn_sincroniza_beneficiarios_benner'
                id='btn_sincroniza_beneficiarios_benner'
                class='mr-2 btn btn-primary btn-rounded botaoPrincipal'>
                <i class="fa-solid fa-code-compare"></i>Sincroniza Dados Benner</button>
            `;
            let let_btn_vincula_beneficiarios = `
                <button type='button' name='btn_vincula_beneficiario'
                id='btn_vincula_beneficiario'
                class='mr-2 btn btn-primary btn-rounded botaoPrincipal'>
                <i class="fa-solid fa-user-plus"></i>Vincular Beneficiário</button>
            `;
            let let_btn_atualiza_fretes_mapas_terc = `
                <button type='button' name='btn_atualiza_fretes_mapas_terc'
                id='btn_atualiza_fretes_mapas_terc'
                class='mr-2 btn btn-primary btn-rounded botaoPrincipal'>
                <i class="fa-solid fa-arrows-rotate"></i>Atualiza Fretes</button>
            `;
            let let_btn_efetuar_pagamento_todos_mapas_beneficiario = `
                <button type='button' name='btn_efetuar_pagamento_todos_mapas_beneficiario'
                id='btn_efetuar_pagamento_todos_mapas_beneficiario'
                class='mr-2 btn btn-primary btn-rounded botaoPrincipal'>
                <i class="fa-solid fa-filter-circle-dollar"></i>Efetuar Pagamento</button>
            `;
            let let_btn_efetuar_pagamento_todos_mapas = `
                <button type='button' name='btn_efetuar_pagamento_todos_mapas'
                id='btn_efetuar_pagamento_todos_mapas'
                class='mr-2 btn btn-primary btn-rounded botaoPrincipal'>
                <i class="fa-solid fa-comment-dollar"></i>Efetuar Pagamento</button>
            `;

            if ( let_cod_beneficiario == "0" && let_val_mapas_ativos == "S"){
                $("#div_btn_gera_pag_2art_terc_1").html(let_btn_verifica_placas_inativas_benner);
                $("#div_btn_gera_pag_2art_terc_2").html(let_btn_sincroniza_beneficiarios_benner);
                $("#div_btn_gera_pag_2art_terc_3").html(let_btn_vincula_beneficiarios);
                $("#div_btn_gera_pag_2art_terc_4").html(let_btn_atualiza_fretes_mapas_terc);
                $("#div_btn_gera_pag_2art_terc_5").html(let_btn_efetuar_pagamento_todos_mapas);

            }
            else if ( let_cod_beneficiario != "0" && let_val_mapas_ativos == "S") {
                $("#div_btn_gera_pag_2art_terc_1").html(let_btn_verifica_placas_inativas_benner);
                $("#div_btn_gera_pag_2art_terc_2").html(let_btn_sincroniza_beneficiarios_benner);
                $("#div_btn_gera_pag_2art_terc_3").html(let_btn_vincula_beneficiarios);
                $("#div_btn_gera_pag_2art_terc_4").html(let_btn_atualiza_fretes_mapas_terc);
                $("#div_btn_gera_pag_2art_terc_5").html(let_btn_efetuar_pagamento_todos_mapas_beneficiario);

            }
            else {
                $("#div_btn_gera_pag_2art_terc_1").html(let_btn_verifica_placas_inativas_benner);
                $("#div_btn_gera_pag_2art_terc_2").html(let_btn_sincroniza_beneficiarios_benner);
                $("#div_btn_gera_pag_2art_terc_3").html(let_btn_vincula_beneficiarios);
                $("#div_btn_gera_pag_2art_terc_4").html(let_btn_atualiza_fretes_mapas_terc);
                $("#div_btn_gera_pag_2art_terc_4").html(`&nbsp;&nbsp;`);
            }


            let_lista_dados_2art_terceiros = [];
            let let_val_total_pagar = 0.00;
            let let_val_total_conlog = 0.00;
            for (let i = 0; i < data.tab_mapas_terceiros.length; i++) {
                let let_img;
                let let_status_atualizacao_mapa = '';
                let_val_total_pagar += data.tab_mapas_terceiros[i].val_pagar * 1.00;
                let_val_total_conlog +=  data.tab_mapas_terceiros[i].val_conlog * 1.00;
                let let_status_validacao = "<span >Convergente</span>";
                let let_placa_diferente = '';
                let let_tipo_entrega_diferente = '';
                let let_dados_beneficiario = data.tab_mapas_terceiros[i].nome_doc_beneficiorio.trim();
                let let_tipo_pessoa = data.tab_mapas_terceiros[i].tipo_pessoa;
                let let_perfil_veic_diferente = '';
                let let_regiao_diferente = '';
                let let_qtd_entrega_diferente = '';
                let let_tipo_imp_diferente = '';
                let let_perc_imp_diferente = '';
                let let_val_frete_diferente = '';
                let let_val_faturado_diferente = '';
                if ( data.tab_mapas_terceiros[i].placa_reg_terc != data.tab_mapas_terceiros[i].placa_reg_2art ){
                    let_placa_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                    data.tab_mapas_terceiros[i].placa_reg_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].tipo_entrega_reg_terc !=
                        data.tab_mapas_terceiros[i].tipo_entrega_2art ){
                    let_tipo_entrega_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                        data.tab_mapas_terceiros[i].tipo_entrega_2art+" )</span>";
                    let_status_validacao = "<span >Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( let_dados_beneficiario == 'Inexistente' || let_dados_beneficiario == 'Placa não cadastrada') {
                    let_dados_beneficiario = "<span style='background:#FF0000;color:#ffffff'>"+let_dados_beneficiario
                        +"</span>";
                    let_tipo_pessoa = "<span style='background:#FF0000;color:#ffffff'>"+let_tipo_pessoa+"</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                }
                if ( data.tab_mapas_terceiros[i].perfil_veic_reg_terc != data.tab_mapas_terceiros[i].perfil_veic_2art ){
                    let_perfil_veic_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                        data.tab_mapas_terceiros[i].perfil_veic_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' && data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].regiao_reg_terc != data.tab_mapas_terceiros[i].regiao_2art ) {
                    let_regiao_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                        data.tab_mapas_terceiros[i].regiao_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].qtd_entr_reg_terc != data.tab_mapas_terceiros[i].qtd_entr_2art ) {
                    let_qtd_entrega_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                        data.tab_mapas_terceiros[i].qtd_entr_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].tipo_imp_reg_terc != data.tab_mapas_terceiros[i].tipo_imp_2art ) {
                    let_tipo_imp_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                        data.tab_mapas_terceiros[i].tipo_imp_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].perc_imposto_reg_terc !=
                        data.tab_mapas_terceiros[i].perc_imposto_2art ) {
                    let_perc_imp_diferente = "<span style='background:#FF0000;color:#FFFFFF'>( "+
                        data.tab_mapas_terceiros[i].perc_imposto_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].val_frete_reg_terc !=
                        data.tab_mapas_terceiros[i].val_frete_2art ) {
                    let_val_frete_diferente = "<span style='background:#FF0000;color:#FFFFFF'>-( "+
                        data.tab_mapas_terceiros[i].val_frete_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].val_faturado_reg_terc !=
                        data.tab_mapas_terceiros[i].val_faturado_2art ) {
                    let_val_faturado_diferente = "<span style='background:#FF0000;color:#FFFFFF'>-( "+
                        data.tab_mapas_terceiros[i].val_faturado_2art+" )</span>";
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                    if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                            data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                        let_status_atualizacao_mapa = 'P';
                    }
                }
                if ( data.tab_mapas_terceiros[i].nome_doc_beneficiorio == 'Inexistente' ||
                        data.tab_mapas_terceiros[i].tipo_pessoa == 'Inexistente' ||
                            data.tab_mapas_terceiros[i].perfil_veic_reg_terc == 'Inexistente' ) {
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                }

                if ( data.tab_mapas_terceiros[i].val_calculado >  data.tab_mapas_terceiros[i].val_frete_reg_terc  + 1 ||
                     data.tab_mapas_terceiros[i].val_calculado <
                        (data.tab_mapas_terceiros[i].val_frete_reg_terc  + 1) * -1){
                    let_status_validacao = "<span style='background:#FF0000;color:#ffffff'>Divergente</span>";
                }

                let let_btn_lancamentos_mapa = `
                    <button type='button' class='btn btn-rounded btn-space'
                    id='btn_lanc_reg_2art_terc_financ_${i}' name='btn_lanc_reg_2art_terc_financ' value='${i}' disabled>
                    <i class="fa-solid fa-paperclip" style="color: #f46424;"></i></button>
                `;
                if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                        data.tab_mapas_terceiros[i].status_mapa == 'S' ) {
                    let_btn_lancamentos_mapa = `
                        <button type='button' class='btn btn-rounded btn-space' title='Lançar Acréscimos/Desconto'
                        id='btn_lanc_reg_2art_terc_financ_${i}' name='btn_lanc_reg_2art_terc_financ' value='${i}'>
                        <i class="fa-solid fa-paperclip" style="color: #f46424;"></i> </button>
                    `;
                }

                let let_btn_status_pagamento_mapa = '';
                if ( data.tab_mapas_terceiros[i].status_financeiro == 'P' ){
                    let_btn_status_pagamento_mapa = "<span style=''>Efetuado</span>";
                    let_img = `
                        <i class="fa-solid fa-receipt" style="color: #3CB371;"
                            title="Pagamento Efetuado"></i>
                    `;
                } else if ( data.tab_mapas_terceiros[i].status_financeiro == 'A' &&
                        data.tab_mapas_terceiros[i].status_mapa == 'S' ){
                    let_btn_status_pagamento_mapa = "<span style=''>Pendente</span>";
                }

                let let_btn_ativa_desativa_mapa = "<span>Processado</span>";

                if ( data.tab_mapas_terceiros[i].status_mapa == 'N' &&
                        data.tab_mapas_terceiros[i].status_financeiro == 'A') {
                    let_btn_ativa_desativa_mapa = `
                        <button type='button' class='btn btn-rounded btn-space'
                        title='Ativar'
                        id='btn_ativa_mapa_${i}' name='btn_ativa_mapa' value='${i}'>
                        <i class="fa-solid fa-location-dot" style="color: #f46424;"></i></button>
                    `;
                    let_img = `
                        <i class="fa-solid fa-location-pin-lock" style="color: #f46424;" title="${data.tab_mapas_terceiros[i].motivo_ultima_acao_mapa}"></i>
                    `;
                } else if ( data.tab_mapas_terceiros[i].status_mapa == 'S' &&
                        data.tab_mapas_terceiros[i].status_financeiro == 'A') {
                    let_btn_ativa_desativa_mapa = `
                        <button type='button' class='btn btn-rounded btn-space'
                        title='Desativar'
                        id='btn_desativa_mapa_${i}' name='btn_desativa_mapa' value='${i}'>
                        <i class="fa-solid fa-location-pin-lock" style="color: #f46424;"></i> </button>
                    `;
                    let_img = `
                        <i class="fa-solid fa-location-dot fa-beat-fade" style="color: #f46424;" title="${data.tab_mapas_terceiros[i].motivo_ultima_acao_mapa}"></i>
                    `;
                }

                if ( let_status_atualizacao_mapa == 'P') {
                    let_img = `
                        <button type='button' class='btn btn-rounded btn-space'
                        title='Atualizar dados mapa'
                        id='btn_model_atualiza_mapa_${i}' name='btn_model_atualiza_mapa' value='${i}'>
                        <i class="fa-solid fa-arrows-rotate" style="color: #fff;"></i></button>
                    `;
                }
            let let_dado_2art_terc = [
                  let_img,
                  data.tab_mapas_terceiros[i].data,
                  data.tab_mapas_terceiros[i].mapa,
                  data.tab_mapas_terceiros[i].placa_reg_terc+" "+let_placa_diferente,
                  data.tab_mapas_terceiros[i].tipo_entrega_reg_terc+" "+let_tipo_entrega_diferente,
                  let_dados_beneficiario,
                  let_tipo_pessoa,
                  data.tab_mapas_terceiros[i].perfil_veic_reg_terc+" "+let_perfil_veic_diferente,
                  data.tab_mapas_terceiros[i].regiao_reg_terc+" "+let_regiao_diferente,
                  data.tab_mapas_terceiros[i].qtd_entr_reg_terc+" "+let_qtd_entrega_diferente,
                  data.tab_mapas_terceiros[i].tipo_imp_reg_terc+" "+let_tipo_imp_diferente,
                  data.tab_mapas_terceiros[i].perc_imposto_reg_terc.toLocaleString('pt-BR')+" "+let_perc_imp_diferente,
                  data.tab_mapas_terceiros[i].val_frete_reg_terc.toLocaleString('pt-BR')+" "+let_val_frete_diferente,
                  data.tab_mapas_terceiros[i].val_calculado.toLocaleString('pt-BR'),
                  data.tab_mapas_terceiros[i].diferenca.toLocaleString('pt-BR'),
                  data.tab_mapas_terceiros[i].val_faturado_reg_terc.toLocaleString('pt-BR')+let_val_faturado_diferente,
                  data.tab_mapas_terceiros[i].desconto.toLocaleString('pt-BR'),
                  data.tab_mapas_terceiros[i].acrescimo.toLocaleString('pt-BR'),
                  data.tab_mapas_terceiros[i].val_pagar.toLocaleString('pt-BR'),
                  data.tab_mapas_terceiros[i].val_conlog.toLocaleString('pt-BR'),
                  let_btn_lancamentos_mapa,
                  let_btn_status_pagamento_mapa,
                  data.tab_mapas_terceiros[i].id_pagamento_serial,
                  let_status_validacao,
                  let_btn_ativa_desativa_mapa,
                  data.tab_mapas_terceiros[i].cod_idreg2arttercfinanc,
                  data.tab_mapas_terceiros[i].status_financeiro
              ];

              let_lista_dados_2art_terceiros.push(let_dado_2art_terc);

            }

            $('#tab_mapas_terceitos_2art').DataTable( {
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
                "searching": true,
                "initComplete": function () {
                    this.api()
                    .columns([1,2,3,4,5,7,8])
                    .every(function () {
                        let let_div = document.createElement('div');
                        let column = this;
                        let title = column.header().textContent;
                        // Create input element
                        let input = document.createElement('input');
                        input.classList.add('input_pesq_column_icon');
                        input.style.borderRadius = '0.2rem 0.2rem 0.2rem 0.2rem';
                        input.style.padding = '2px';
                        input.style.width = '120px';
                        input.placeholder = title;

                        let let_icon_input = document.createElement('i');
                        let_icon_input.classList.add('fa-solid');
                        let_icon_input.style.color = '#696969';
                        let_icon_input.classList.add('fa-magnifying-glass');

                        let_div.appendChild(let_icon_input);
                        let_div.appendChild(input);


                        column.header().replaceChildren(let_div);

                        // Event listener for user input
                        input.addEventListener('keyup', () => {
                            if (column.search() !== this.value) {
                                column.search(input.value).draw();
                            }
                        });
                    });

                    this.api()
                    .columns([0])
                    .every(function() {
                        let column = this;

                        let let_icon_input = document.createElement('i');
                        let_icon_input.classList.add('fa-solid');
                        let_icon_input.style.color = '#f46424';
                        let_icon_input.classList.add('fa-eraser');

                        let let_btn_limpar = document.createElement('button');
                        let_btn_limpar.classList.add('btn');
                        let_btn_limpar.title = 'Limpar pesquisa';
                        let_btn_limpar.classList.add('btn-rounded');
                        let_btn_limpar.classList.add('btn-space');
                        let_btn_limpar.appendChild(let_icon_input)

                        column.header().replaceChildren(let_btn_limpar);

                        let let_ev_enter = new Event('keyup');

                        // Event listener for user input
                        let_btn_limpar.addEventListener('click', () => {
                            let let_inputs = document.getElementsByClassName('input_pesq_column_icon');

                            for(let i = 0; i < let_inputs.length; i++) {
                                let_inputs[i].value = null;


                                // Despacha o evento para o campo de entrada
                                let_inputs[i].dispatchEvent(let_ev_enter);
                            }
                        });

                    });
                },
                "data":let_lista_dados_2art_terceiros,
                "columns": [
                    { title: "" },
                    { title: "Data" },
                    { title: "Mapa" },
                    { title: "Placa" },
                    { title: "Tipo Entrega" },
                    { title: "Beneficiário" },
                    { title: "Tipo Pessoa" },
                    { title: "Perfil Veículo" },
                    { title: "Região" },
                    { title: "Qtd. Entregas" },
                    { title: "Tipo Imposto" },
                    { title: "Perc. Imposto" },
                    { title: "Val. Frete" },
                    { title: "Val. Calculado" },
                    { title: "Diferença" },
                    { title: "Val. Faturado" },
                    { title: "Descontos" },
                    { title: "Acréscimos" },
                    { title: "Val. á Pagar" },
                    { title: "Val. CONLOG" },
                    { title: "Lançamentos" },
                    { title: "Status Pagamento" },
                    { title: "Serial Pagamento"},
                    { title: "Validação" },
                    { title: "Ativa/Desativa" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,2,3,4,6,7,8,9,10,20,21,22,23,24]},
                    {"className": "dt-left", "targets": [5]},
                    {"className": "dt-right", "targets": [11,12,13,14,15,16,17,18,19]}
                ],
                "language": {
                    "decimal": ",",
                    "thousands": ".",
                    "sEmptyTable": "Nenhum registro encontrado",
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


                },
                "footerCallback": function ( row, data, start, end, display ) {
                    var api = this.api(), data;

                    // Remove the formatting to get integer data for summation
                    var intVal = function ( i ) {
                        return typeof i === 'string' ?
                            i.replace('.','').replace(',','.') * 1.00 :
                            typeof i === 'number' ?
                                i : 0;
                    };

                    // Total over all pages
                    total_frete = api
                        .column( 12 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_frete = api
                        .column( 12, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 12 ).footer() ).html(
                        pageTotal_frete.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );


                    // Total over all pages
                    total_calculado = api
                        .column( 13 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_calculado = api
                        .column( 13, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 13 ).footer() ).html(
                        pageTotal_calculado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );


                     // Total over all pages
                     total_diferenca = api
                     .column( 14 )
                     .data()
                     .reduce( function (a, b) {
                         return intVal(a) + intVal(b);
                     }, 0 );

                    // Total over this page
                    pageTotal_diferenca = api
                        .column( 14, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 14 ).footer() ).html(
                        pageTotal_diferenca.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );


                    // Total over all pages
                    total_faturado = api
                        .column( 15 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_faturado = api
                        .column( 15, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 15 ).footer() ).html(
                        pageTotal_faturado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );


                    // Total over all pages
                    total_descontos = api
                        .column( 16 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_descontos = api
                        .column( 16, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 16 ).footer() ).html(
                        pageTotal_descontos.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );

                    // Total over all pages
                    total_acrescimos = api
                        .column( 17 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_acrescimos = api
                        .column( 17, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 17 ).footer() ).html(
                        pageTotal_acrescimos.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );

                    // Total over all pages
                    total_val_pagar = api
                        .column( 18 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_val_pagar = api
                        .column( 18, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 18 ).footer() ).html(
                        pageTotal_val_pagar.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );


                    total_val_conlog = api
                        .column( 19 )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Total over this page
                    pageTotal_val_conlog = api
                        .column( 19, { page: 'current'} )
                        .data()
                        .reduce( function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0 );

                    // Update footer
                    $( api.column( 19 ).footer() ).html(
                        pageTotal_val_conlog.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    );
                }

          });
            loader_gera_pag_terc_2art.style.display = "none";

        },
        error: function (request, status, error) {
            loader_gera_pag_terc_2art.style.display = "none";
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


function atualiza_tab_placas_intativas_benner(param_nome_componenete_acionado){
    let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
    let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
    let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();
    loader_gera_pag_terc_2art.style.display = "flex";
    $.ajax({
        type:'GET',
        data:{
            'nome_componente'   :   param_nome_componenete_acionado,
            'cod_proj'          :   let_cod_projeto,
            'data_ini'          :   let_data_ini,
            'data_fim'          :   let_data_fim
        },
        url:'/plan_controle_fat_2art_terc_app/retona_placas_para_inativacao_do_benner',
        success:function(dados){

            var lista_dados = [];
            dados.lista_placas_inativas_benner.forEach( reg => {
                var var_data_mapa = reg.data_2art_terc_financ.split("-")[2] + "-" +
                    reg.data_2art_terc_financ.split("-")[1] + "-" +
                    reg.data_2art_terc_financ.split("-")[0];
                var var_desc_status_placa_benner = '';
                if( reg.status_benner == 'N' ) {
                    var_desc_status_placa_benner = 'Ativo';
                } else if ( reg.status_benner == 'S' ) {
                    var_desc_status_placa_benner = 'Inativo';
                }
                var var_desc_status_placa_portal = '';
                var var_novo_status_placa_portal = '';
                if( reg.status_mapa_2art_terc_financ == 'N' ) {
                    var_desc_status_placa_portal = 'Inativo';
                    var_novo_status_placa_portal = 'S';
                } else if ( reg.status_mapa_2art_terc_financ == 'S' ) {
                    var_desc_status_placa_portal = 'Ativo';
                    var_novo_status_placa_portal = 'N';
                }

                var var_value_button_altera_status_mapa = reg.cod_reg_2art_terc_financ+"_"+
                    var_novo_status_placa_portal;
                var var_btn_altera_status_mapa = `
                    <button type="button" name="btn_altera_status_mapa_com_benner"
                        id="btn_altera_status_mapa_com_benner_${reg.cod_reg_2art_terc_financ}"
                        class="btn btn-rounded btn-space"
                        value="`+var_value_button_altera_status_mapa+`"
                        title="Alterar Status">
                        <i class="fa-solid fa-rotate-right" style="color: #f46424;"></i>
                    </button>
                `;
                let let_img = `<i class="fa-solid fa-location-dot" style="color: #f46424;"></i>`;
                reg = [
                    let_img,
                    var_data_mapa,
                    reg.mapa_2art_terc_financ,
                    reg.placa_2art_terc_financ,
                    reg.nome_benef,
                    var_desc_status_placa_benner,
                    var_desc_status_placa_portal,
                    var_btn_altera_status_mapa
                ];
                lista_dados.push(reg);
            });
            $('#tab_dados_placa_inativas_benner').DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
                "destroy": true,
                "paging": true,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copy'
                ],
                "data":lista_dados,
                "columns": [
                    { title: "" },
                    { title: "Data" },
                    { title: "Mapa" },
                    { title: "Placa" },
                    { title: "Beneficiário" },
                    { title: "Status Benner" },
                    { title: "Status Portal" },
                    { title: "Ação" }
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
            loader_gera_pag_terc_2art.style.display = "none";
            $("#modal_verifica_placas_inativas_benner").show();

        },
        error:function(request, status, error){
            loader_gera_pag_terc_2art.style.display = "none";
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


function atualiza_dados_placa_benef_sinc_benner(param_nome_componenete_acionado) {
    let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
    let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
    let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();
    loader_gera_pag_terc_2art.style.display = "flex";
    $.ajax({
        type:'GET',
        data:{
            'nome_componente'   :   param_nome_componenete_acionado,
            'cod_proj'          :   let_cod_projeto,
            'data_ini'          :   let_data_ini,
            'data_fim'          :   let_data_fim
        },
        url:'/plan_controle_fat_2art_terc_app/retona_placas_nao_cadastradas_periodo_fat_terceiro',
        success:function(dados){

            let let_lista_dados_tab_placas = [];
            dados.lista_dados_tab_placa_a_sincronizar.forEach( placa_benef => {
                let let_desc_status_placa = '';
                if( placa_benef.status_placa == 'N' ) {
                    let_desc_status_placa = 'Sim';
                } else if ( placa_benef.status_placa == 'S' ) {
                    let_desc_status_placa = 'Não';
                }

                let let_btn_cad_placa_benef = `
                    <button type="button" name="btn_cad_placa_benef_sinc_benner"
                        id="btn_cad_placa_benef_sinc_benner_${placa_benef.handle_placa}"
                        class="btn btn-lg btn-outline-primary btn-rounded"
                        value="${placa_benef.handle_placa}">
                        <i class="fa-solid fa-rotate-right" style="color: #f46424;"></i>
                        Sincroniza Dados
                    </button>
                `;
                let let_nome_benef = '';
                if ( placa_benef.status_cadastro_bd_operacional == 'S'){
                    let_nome_benef = "<span style='background:#98FB98;color:#228B22;'>"+placa_benef.nome_benef+"</span>";
                } else if ( placa_benef.status_cadastro_bd_operacional == 'N' ) {
                    let_nome_benef = "<span style='background:#FFA07A;color:#FF0000;'>"+placa_benef.nome_benef+"</span>";
                }
                let let_desc_tipo_benef = '';
                if ( placa_benef.tipo_benef == '1' ){
                    let_desc_tipo_benef = 'Pessoa Física';
                } else if ( placa_benef.tipo_benef == '2' ) {
                    let_desc_tipo_benef = 'Pessoa Jurídica';
                }
                let let_desc_status_benef = '';
                if( placa_benef.status_benef == 'N' ) {
                    let_desc_status_benef = 'Sim';
                } else if ( placa_benef.status_benef == 'S' ) {
                    let_desc_status_benef = 'Não';
                }
                reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    placa_benef.placa +
                    "<input type='hidden' id='hd_placa_tab_sinc_benner_"+placa_benef.handle_placa+"' value='"+
                        placa_benef.placa+"'/>",
                    placa_benef.perfil_placa +
                    "<input type='hidden' id='hd_perfil_placa_tab_sinc_benner_"+placa_benef.handle_placa+"' value='"+
                        placa_benef.perfil_placa+"'/>",
                    let_desc_status_placa,
                    let_nome_benef +
                    "<input type='hidden' id='hd_nome_benef_tab_sinc_benner_"+placa_benef.handle_placa+"' value='"+
                        placa_benef.nome_benef+"'/>",
                    placa_benef.doc_benef +
                    "<input type='hidden' id='hd_doc_benef_tab_sinc_benner_"+
                        placa_benef.handle_placa+"' value='"+
                        placa_benef.doc_benef.toString().replaceAll('.','').replaceAll('-','').replaceAll('/','')+"'/>",
                    let_desc_tipo_benef +
                    "<input type='hidden' id='hd_tipo_benef_tab_sinc_benner_"+placa_benef.handle_placa+"' value='"+
                        let_desc_tipo_benef+"'/>",
                    let_desc_status_benef +
                    "<input type='hidden' id='hd_status_benef_tab_sinc_benner_"+placa_benef.handle_placa+"' value='"+
                        placa_benef.status_benef+"'/>",
                    placa_benef.handle_benef +
                    "<input type='hidden' id='hd_handle_benef_tab_sinc_benner_"+placa_benef.handle_placa+"' value='"+
                        placa_benef.handle_benef+"'/>",
                    let_btn_cad_placa_benef
                ];
                let_lista_dados_tab_placas.push(reg);
            });
            $('#tab_dados_placa_sincroniza_benner').DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
                "destroy": true,
                "paging": true,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copy'
                ],
                "data":let_lista_dados_tab_placas,
                "columns": [
                    { title: "" },
                    { title: "Placa" },
                    { title: "Perfil Placa" },
                    { title: "Placa Ativa?" },
                    { title: "Beneficiário" },
                    { title: "Doc" },
                    { title: "Tipo Pessoa" },
                    { title: "Benef. Ativo?" },
                    { title: "Handle Beneficiário" },
                    { title: "Ação Beneficiário" }
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
            loader_gera_pag_terc_2art.style.display = "none";
        },
        error:function(request, status, error){
            loader_gera_pag_terc_2art.style.display = "none";
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


function povoa_tab_faturamento_agrupado_por_beneficiario(){
    let let_cod_projeto = $("#cb_projetos_pesq_mapas_terc").val();
    let let_data_ini = $("#dt_pesq_mapas_terc_periodo_ini").val();
    let let_data_fim = $("#dt_pesq_mapas_terc_periodo_fim").val();
    loader_gera_pag_terc_2art.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/plan_controle_fat_2art_terc_app/retorna_dados_2art_terc_agrupado_por_beneficiario',
        data: {
            'cod_projeto'   :   let_cod_projeto,
            'data_ini'      :   let_data_ini,
            'data_fim'      :   let_data_fim
        },
        dataType: 'json',
        success: function (data) {
            let_lista_dados_2art_terceiros_agrupado_por_beneficiario = [];
            for (let i = 0; i < data.tab_mapas_terceiros.length; i++) {

                let let_btn_processar_pagamento_benef = `
                    <button type='button' name='btn_efetuar_pagamento_processado_beneficiario'
                        id="btn_efetuar_pagamento_processado_beneficiario${i}" value="${i}"
                        class='btn btn-rounded btn-space'
                        title="Efetuar Pagamento ${data.tab_mapas_terceiros[i].nome_beneficiario.trim()}">
                        <i class="fa-solid fa-check" style="color:#f46424;"></i>
                    </button>
                `;
                if ( data.tab_mapas_terceiros[i].val_ff_calc == 0) {
                    let_btn_processar_pagamento_benef = "<span style='background:#fa6163;color:#ffffff;'>"+
                        "Divergência</span>";
                }

                let let_img = `<i class="fa-solid fa-location-dot" style="color: #f46424;"></i>`;
                let let_dado_2art_terc = [
                    let_img,
                    data.tab_mapas_terceiros[i].nome_beneficiario.trim(),
                    data.tab_mapas_terceiros[i].qtd_mapas,
                    data.tab_mapas_terceiros[i].val_tt_frete.toLocaleString('pt-BR'),
                    data.tab_mapas_terceiros[i].val_ff_calc.toLocaleString('pt-BR'),
                    ((data.tab_mapas_terceiros[i].val_tt_frete * 1.00) -
                        (data.tab_mapas_terceiros[i].val_ff_calc * 1.00)).toLocaleString('pt-BR'),
                    data.tab_mapas_terceiros[i].val_tt_fat.toLocaleString('pt-BR'),
                    data.tab_mapas_terceiros[i].val_tt_acres.toLocaleString('pt-BR'),
                    data.tab_mapas_terceiros[i].val_tt_desc.toLocaleString('pt-BR'),
                    data.tab_mapas_terceiros[i].val_tt_pagar.toLocaleString('pt-BR'),
                    data.tab_mapas_terceiros[i].val_tt_conlog.toLocaleString('pt-BR'),
                    let_btn_processar_pagamento_benef,
                    data.tab_mapas_terceiros[i].cod_beneficiario,
                    data.tab_mapas_terceiros[i].cod_2art_terc_financ
                ];
                let_lista_dados_2art_terceiros_agrupado_por_beneficiario.push(let_dado_2art_terc);
            }
            $('#tab_fat_agrupado_2art_terc').DataTable( {
            "bJQueryUI": true,
            "pageLength": 6,
            "destroy": true,
            "dom": 'Bfrtip',
            "buttons": [
                'copyHtml5'
             ],
            "data":let_lista_dados_2art_terceiros_agrupado_por_beneficiario,
            "columns": [
                { title: "" },
                { title: "Beneficiário" },
                { title: "Qtd. Mapas" },
                { title: "Tt. Fretes" },
                { title: "Tt. Calc." },
                { title: "Dif." },
                { title: "Tt. Fat." },
                { title: "Tt. Acrésc." },
                { title: "Tt. Desc." },
                { title: "Tt. à Pagar" },
                { title: "Tt. Conlog" },
                { title: "Pagar" }
            ],
            "columnDefs": [
                {"className": "dt-center", "targets": [0,2,11]},
                {"className": "dt-left", "targets": [1]},
                {"className": "dt-right", "targets": [3,4,5,6,7,8,9,10]}
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
            loader_gera_pag_terc_2art.style.display = "none";

        },
        error: function (request, status, error) {
            loader_gera_pag_terc_2art.style.display = "none";
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



function povoa_tab_lanc_acres_desc_do_mapa(let_cod_reg_2art_terc_financ){
       loader_gera_pag_terc_2art.style.display = "flex";
    $.ajax({
        type: "GET",
        url:"/plan_controle_fat_2art_terc_app/retorna_registros_lanc_2art_terc_do_mapa",
        data: {
            'cod_reg_2art_terc_financ'     :   let_cod_reg_2art_terc_financ
        },
        success: function(dados){
            $("#tab_lanc_2art_terc").DataTable().clear().draw();
            let let_lista_dado_lanc_mapa = [];
            let let_img = '';
            let let_total_descontos = 0.00;
            let let_total_acrescimos = 0.00;
            for (let i = 0; i < dados.lista_lancamentos_mapa.length; i++) {
                let let_btn_excluir_reg_lanc_2art_terc = `
                    <button type="button" class="btn btn-rounded btn-space"
                    id="btn_excluir_reg_lanc_2art_terc_${dados.lista_lancamentos_mapa[i].id_registro_bd}"
                    name="btn_excluir_reg_lanc_2art_terc" value="${dados.lista_lancamentos_mapa[i].id_registro_bd}"
                    title="${dados.lista_lancamentos_mapa[i].desc_ocorrencia}/ Data:${dados.lista_lancamentos_mapa[i].data_ocorrencia}/ Mapa:${dados.lista_lancamentos_mapa[i].mapa_ocorrencia}/ Placa: ${dados.lista_lancamentos_mapa[i].placa_lanc}">
                    <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                    </button>
                `;


                if (dados.lista_lancamentos_mapa[i].tipo_lanc == 'D'){
                    let_total_descontos = let_total_descontos + (dados.lista_lancamentos_mapa[i].valor * 1.0)
                    let_img = `<i class="fa-solid fa-minus" style="color: #f46424;" title="Desconto"></i>`;
                } else if (dados.lista_lancamentos_mapa[i].tipo_lanc == 'A'){
                    let_total_acrescimos = let_total_acrescimos + (dados.lista_lancamentos_mapa[i].valor * 1.0)
                    let_img = `<i class="fa-solid fa-plus" style="color: #f46424;" title="Acréscimo"></i>`;
                }
                let let_reg_lanc = [
                    let_img,
                    dados.lista_lancamentos_mapa[i].desc_ocorrencia,
                    dados.lista_lancamentos_mapa[i].data_ocorrencia,
                    dados.lista_lancamentos_mapa[i].mapa_ocorrencia,
                    dados.lista_lancamentos_mapa[i].placa_lanc,
                    dados.lista_lancamentos_mapa[i].valor.toLocaleString('pt-BR'),
                    dados.lista_lancamentos_mapa[i].obs,
                    let_btn_excluir_reg_lanc_2art_terc,
                    dados.lista_lancamentos_mapa[i].id_registro_bd

                ];
                let_lista_dado_lanc_mapa.push(let_reg_lanc);
            }

            $('#tab_lanc_2art_terc').DataTable( {
                "bJQueryUI": true,
                "pageLength": 4,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5',
                ],
                "data":let_lista_dado_lanc_mapa,
                    "columns": [
                            { title: "" },
                            { title: "Ocorrência" },
                            { title: "Data ocorrência" },
                            { title: "Mapa Ocorrência" },
                            { title: "Placa" },
                            { title: "Valor(R$)" },
                            { title: "Observação" },
                            { title: "Excluir" }
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
            loader_gera_pag_terc_2art.style.display = "none";



        },
        error: function (request, status, error) {
            loader_gera_pag_terc_2art.style.display = "none";
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



$(document).on('change', '#list_tipo_lancamento_lanc_2art_terc', function(){
    let let_tipo_lancamento = $(this).val();
    if (let_tipo_lancamento == "0") {
        $("#list_tipo_ccorrencia_lanc_2art_terc option").remove();
        $("#list_tipo_ccorrencia_lanc_2art_terc").append("<option value='0'>--Selecione Tipo Lançamento--</option>");
    } else {
        $.ajax({
            type: 'GET',
            url: '/plan_controle_fat_2art_terc_app/povoa_listTipoOcorrenciaLanc2ArtTerc_formLanc2ArtTerc',
            data: {
                'tipo_lancamento'   :   let_tipo_lancamento
            },
            dataType: 'json',
            success: function (data) {
                $("#list_tipo_ccorrencia_lanc_2art_terc option").remove();
                data.lista_ocorrencia.forEach(ocorrencia => {
                    $("#list_tipo_ccorrencia_lanc_2art_terc")
                        .append("<option value='"+ocorrencia.cod_tipo_ocor_financ_terc+"'>"+
                        ocorrencia.desc_ocorrencia+"</option>");

                });

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

});