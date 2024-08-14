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

$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();

	if (nomeDoButton == 'btn_gera_dados_prov_senior'){
	    let let_loader_prov_senior = document.getElementById("loader_prov_senior");
	    var var_tipo_provisao = $("#cb_tipo_prov_senior").val();
	    var var_cod_competencia = $("#cb_competencia_prov_senior").val();
        var var_lista_handle_proj = $("#cb_proj_prov_senior").val().toString();
        let let_cod_empresa = $("#cb_emp_prov_senior").val();

        if(var_tipo_provisao == "0" || var_cod_competencia == "0" || (var_lista_handle_proj == "0" && var_lista_handle_proj.length == 1) ||
            var_lista_handle_proj == null || var_lista_handle_proj == '' ) {
            $.gritter.add({
                title: 'Atenção!',
                text: "Por favor informe os dados obrigatórios para a gerar os dados solicitados!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
        else {
            var val_realizado_dre = 0;
            let_loader_prov_senior.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    cod_tipo_provisao   :   var_tipo_provisao,
                    cod_competencia     :   var_cod_competencia,
                    lista_handle_proj   :   var_lista_handle_proj,
                    cod_empresa         :   let_cod_empresa
                },
                url:"/plan_controle_provisoes_folha_app/gera_dados_provisoes_senior",
                success: function(dados){
                    lista_dados_proeventos_colab = [];
                    dados.dados_proeventos_colabs.forEach( reg => {

                        valprov = reg.val_prov;
                        valprovf = valprov.replace("-","").replace(".","").replace(",",".");
                        valajusteprov = reg.val_ajuste_prov;
                        valajusteprovf = valajusteprov.replace("-","").replace(".","").replace(",",".");
                        if(parseFloat(reg.val_ajuste_prov) >= 0){
                            soma = parseFloat(valprovf) + parseFloat(valajusteprovf)
                            val_realizado_dre = parseFloat(soma).toFixed(2).toString();
                        }else{
                            val_realizado_dre = parseFloat(valprovf - valajusteprovf).toFixed(2).toString();
                        }
                        val_realizado_dre = val_realizado_dre.replace(".",",");

                        var var_data_adm = reg.data_adm.split('-')[2] + '-' +
                            reg.data_adm.split('-')[1] + '-' +
                            reg.data_adm.split('-')[0];

                        reg = [
                            "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                            "<b>"+reg.mat_fun+"</b>",
                            "<b>"+reg.nome_fun+"</b>",
                            reg.nome_filial,
                            reg.desc_ccu,
                            var_data_adm,
                            reg.desc_cargo,
                            reg.desc_prov,
                            reg.val_base_prov.toLocaleString('pt-BR'),
                            reg.perc_dias_prov,
                            reg.val_anterior_prov.toLocaleString('pt-BR'),
                            reg.val_transf_prov.toLocaleString('pt-BR'),
                            reg.val_ajuste_prov.toLocaleString('pt-BR'),
                            reg.val_prov.toLocaleString('pt-BR'),
                            val_realizado_dre,
                            reg.val_pag_prov.toLocaleString('pt-BR'),
                            reg.val_indenizado_prov.toLocaleString('pt-BR'),
                            reg.val_saldo_prov.toLocaleString('pt-BR')
                        ];
                        lista_dados_proeventos_colab.push(reg);
                    });
                    $("#tab_dados_prov_colabs").DataTable({
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
                        "data":lista_dados_proeventos_colab,
                        "columns": [
                            { title: "" },
                            { title: "Matrícula" },
                            { title: "Colaborador" },
                            { title: "Filial" },
                            { title: "Projeto" },
                            { title: "Admissão" },
                            { title: "Cargo" },
                            { title: "Item" },
                            { title: "Base" },
                            { title: "% Dias" },
                            { title: "Anterior" },
                            { title: "Transferido" },
                            { title: "Ajuste" },
                            { title: "Provisão" },
                            { title: "Val. Realizado DRE" },
                            { title: "Pagas" },
                            { title: "Idenizado" },
                            { title: "Saldo" }
                        ],
                        "columnDefs": [
                            {"className": "dt-center", "targets": [0,1,3,5]},
                            {"className": "dt-left", "targets": [2,4]},
                            {"className": "dt-right", "targets": [6,7,8,9,10,11,12,13,14]}
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


                    lista_dados_proeventos_itens = [];
                    dados.dados_proeventos_itens.forEach( reg => {

                        valprovT = reg.val_prov;
                        valprovfT = valprovT.replace("-","").replace(".","").replace(",",".");
                        valajusteprovT = reg.val_ajuste_prov;
                        valajusteprovfT = valajusteprovT.replace("-","").replace(".","").replace(",",".");
                        if(parseFloat(reg.val_ajuste_prov) >= 0){
                            soma = parseFloat(valprovfT) + parseFloat(valajusteprovfT)
                            val_realizado_dre_Tot = parseFloat(soma).toFixed(2).toString();
                        }else{
                            val_realizado_dre_Tot = parseFloat(valprovfT - valajusteprovfT).toFixed(2).toString();
                        }
                        val_realizado_dre_Tot = val_realizado_dre_Tot.replace(".",",");



                        reg = [
                            "<b style='color: #f46424;'>"+reg.desc_prov+"</b>",
                            reg.val_base_prov.toLocaleString('pt-BR'),
                            reg.perc_dias_prov,
                            reg.val_anterior_prov.toLocaleString('pt-BR'),
                            reg.val_transf_prov.toLocaleString('pt-BR'),
                            reg.val_ajuste_prov.toLocaleString('pt-BR'),
                            reg.val_prov.toLocaleString('pt-BR'),
                            val_realizado_dre_Tot,
                            reg.val_pag_prov.toLocaleString('pt-BR'),
                            reg.val_indenizado_prov.toLocaleString('pt-BR'),
                            reg.val_saldo_prov.toLocaleString('pt-BR')
                        ];
                        lista_dados_proeventos_itens.push(reg);

                    });

                    $("#tab_dados_prov_itens").DataTable({
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
                        "data":lista_dados_proeventos_itens,
                        "columns": [
                            { title: "Item" },
                            { title: "Base" },
                            { title: "% Dias" },
                            { title: "Anterior" },
                            { title: "Transferido" },
                            { title: "Ajuste" },
                            { title: "Provisão" },
                            { title: "Val. Realizado DRE" },
                            { title: "Pagas" },
                            { title: "Idenizado" },
                            { title: "Saldo" }
                        ],
                        "columnDefs": [
                            {"className": "dt-left", "targets": [0]},
                            {"className": "dt-right", "targets": [1,2,3,4,5,6,7,8,9]}
                        ],
                        "language": {
                            "decimal": ",",
                            "thousands": ".",
                            "sProcessing":   "Processando...",
                            "sLengthMenu":   "Mostrar _MENU_ registros",
                            "sZeroRecords":  "Não foram encontrados resultados",
                            "sInfo":         "",
                            "sInfoEmpty":    "",
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
                        "footerCallback": function(row, data, start, end, display) {
                            var api = this.api(), data;
                            var intVal = function(i){
                                return typeof i === 'string' ?
                                    i.replace('.', '').replace(',','.') * 1.00 :
                                    typeof i === 'number' ?
                                        i : 0;
                            };

                            page_total_base = api
                                .column(3)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(3).footer()).html(
                                page_total_base.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );

                            page_total_transferido = api
                                .column(4)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(4).footer()).html(
                                page_total_transferido.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );

                            page_total_ajuste = api
                                .column(5)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(5).footer()).html(
                                page_total_ajuste.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );

                            page_total_provisao = api
                                .column(6)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(6).footer()).html(
                                page_total_provisao.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );

                            page_total_pagas = api
                                .column(7)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(7).footer()).html(
                                page_total_pagas.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );

                            page_total_idenizado = api
                                .column(8)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(8).footer()).html(
                                page_total_idenizado.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );

                            page_total_saldo = api
                                .column(9)
                                .data()
                                .reduce( function(a,b){
                                    return intVal(a) + intVal(b);
                                },0);
                            $(api.column(9).footer()).html(
                                page_total_saldo.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})
                            );
                        }
                    });


                    let_loader_prov_senior.style.display = "none";


                },
                error: function (request, status, error) {
                    let_loader_prov_senior.style.display = "none";
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
	else if (nomeDoButton == 'btn_seleciona_todos_proj_prov_senior'){
        $("#cb_proj_prov_senior").selectpicker('selectAll');
    }
    else if (nomeDoButton == 'btn_desmarcar_projetos_prov_senior'){
        $("#cb_proj_prov_senior").selectpicker('deselectAll');
    }

});

$(document).on('change', '#cb_emp_prov_senior', function(){
    let let_cod_empresa = $(this).val();
    let let_loader_prov_senior = document.getElementById("loader_prov_senior");
    let_loader_prov_senior.style.display = "flex";
    $.ajax({
        type: 'GET',
        data: {
            'cod_empresa'         : let_cod_empresa
        },
        url:"/plan_controle_folha_pag_analitico_app/pesq_projetos_by_emp",
        success: function(dados){
            $("#cb_proj_prov_senior option").remove();
            dados.lista_projetos.forEach(proj => {
                $("#cb_proj_prov_senior").append("<option value='"+
                proj.handle_benner+"'>"+proj.desc_proj_benner+"</option>");

            });
            $("#cb_proj_prov_senior").selectpicker('refresh');



            let_loader_prov_senior.style.display = "none";


        },
        error: function (request, status, error) {
            let_loader_prov_senior.style.display = "none";
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

