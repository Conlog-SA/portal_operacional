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


$(document).on('change','input', function(){
	let let_nome_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');
    let let_val_input = $(this).attr('value');

    if ( let_nome_input == 'fl_arquivo_remunerado') {
        let let_frm_data = new FormData();
        let_frm_data.append("tipo_planilha", $('#sl_arquivo_remunerado').val());
		let_frm_data.append("file", $('input[type=file]')[0].files[0]);
		let let_loader_frm_imp_plan_freightech = document.getElementById("loader_frm_imp_plan_freightech");
		let_loader_frm_imp_plan_freightech.style.display = "flex";
		$.ajax({
		    type: 'POST',
            enctype: "multipart/form-data; charset=utf-8",
            url: "/freightech_remunerado_qlp_app/importa_plan_remunerado_selecionada",
            data: let_frm_data,
            dataType: 'json',
            processData: false,
            contentType: false,
            cache: false,
            success: function(data){

				$.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '../../static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_frm_imp_plan_freightech.style.display = "none";




			},
			error: function (request, status, error) {
			    let_loader_frm_imp_plan_freightech.style.display = "none";
			    $.gritter.add({
                    title: 'Atenção!',
                    text: "Erro na importação, contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
			}
		});

    }

});


$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_aplicar_pesq_qlp_freigh") {
        let let_nome_unidade_freigh = $('#sl_unidade_pesq_qlp_freigh').val();
        let let_data_1 = $('#dt_comp_pesq_qlp_freigh_1').val();
        let let_quinz_1 = $('#dt_quinz_pesq_qlp_freigh_1').val();
        let let_data_2 = $('#dt_comp_pesq_qlp_freigh_2').val();
        let let_quinz_2 = $('#dt_quinz_pesq_qlp_freigh_2').val();

        let let_loader_frm_imp_plan_freightech = document.getElementById("loader_frm_imp_plan_freightech");
		let_loader_frm_imp_plan_freightech.style.display = "flex";
        $.ajax({
		    type: 'GET',
            url: "/freightech_remunerado_qlp_app/retorna_rem_comparacao_competencias",
            data: {
                'nome_unidade_freigh'   :   let_nome_unidade_freigh,
                'data_1'                :   let_data_1,
                'quinz_1'               :   let_quinz_1,
                'data_2'                :   let_data_2,
                'quinz_2'               :   let_quinz_2
            },
            dataType: 'json',
            success: function(data){
                let lista_itens_rem = [];
                data.lista_obj_rem.forEach(item => {
                    let let_reg = [
                        item.vigencia,
                        item.quinzena,
                        item.desc_grupo,
                        item.desc_cargo,
                        item.qtd_qlp,
                        item.qtd_encargos,
                        item.val_unit_encargos,
                        item.qtd_ordenados,
                        item.val_unit_ordenados,
                        item.qtd_frota_leve,
                        item.val_unit_frota_leve,
                        item.qtd_beneficios,
                        item.val_unit_beneficio,
                        item.qtd_telefonia,
                        item.val_unit_telefonia,
                        item.qtd_uniformes,
                        item.val_unit_uniformes
                    ];
                    lista_itens_rem.push(let_reg);
                });
                $("#tab_qlp_adm_feigh").DataTable({
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "770px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 10,
                    "responsive": false,
                    "stateSave": true,
                    "select": true,
                    "colReorder": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "fixedColumns": {
                        "start": 4
                    },
                    "data":lista_itens_rem,
                    "columns": [
                        { title: "Vigência" },
                        { title: "Quinzena" },
                        { title: "Grupo" },
                        { title: "Cargo" },
                        { title: "Qtd." },
                        { title: "Qtd. Encargos" },
                        { title: "R$ Encargos" },
                        { title: "Qtd. Ordenados" },
                        { title: "R$ Ordenados" },
                        { title: "Qtd. Frota Leve" },
                        { title: "R$ Frota Leve" },
                        { title: "Qtd. Benefícios" },
                        { title: "R$ Benefícios" },
                        { title: "Qtd. Telefonia" },
                        { title: "R$ Telefonia" },
                        { title: "Qtd. Uniformes" },
                        { title: "R$ Uniformes" }
                    ],
                    "initComplete": function () {
                        this.api()
                            .columns([0,1,2,3])
                            .every(function () {
                                let column = this;

                                // Create select element
                                let select = document.createElement('select');
                                select.add(new Option(''));
                                column.footer().replaceChildren(select);

                                // Apply listener for user change in value
                                select.addEventListener('change', function () {
                                    column
                                        .search(select.value, {exact: true})
                                        .draw();
                                });

                                // Add list of options
                                column
                                    .data()
                                    .unique()
                                    .sort()
                                    .each(function (d, j) {
                                        select.add(new Option(d));
                                    });
                            });
                    },
                    "columnDefs": [
                        {"className": "dt-center", "targets": [1]},
                        {"className": "dt-left", "targets": [0,2,3]},
                        {"className": "dt-right", "targets": [4,5,6,7,8,9,10,11,12,13,14,15,16]}
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
                $("#tab_qlp_adm_feigh").DataTable().columns.adjust().draw();


                let let_lista_qlp = []
                data.lista_qlp.forEach(item => {
                    let let_reg = [
                        item.quinz,
                        item.periodo,
                        item.desc_proj,
                        item.desc_cargo_senior,
                        item.desc_cargo_freightech,
                        item.qlp,
                        item.val_ordenados,
                        item.qlp_rem,
                        item.val_ordenado_rem
                    ];
                    let_lista_qlp.push(let_reg);
                });
                $("#tab_qlp_senior_x_freigh").DataTable({
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "770px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 10,
                    "responsive": false,
                    "stateSave": true,
                    "select": true,
                    "colReorder": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_qlp,
                    "columns": [
                        { title: "Quinzena" },
                        { title: "Dia" },
                        { title: "Projeto" },
                        { title: "Cargo Senior" },
                        { title: "Cargo Freightech" },
                        { title: "Qlp." },
                        { title: "R$ TT Ordenados" },
                        { title: "Qlp Rem" },
                        { title: "R$ TT Ordenados Rem" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [0,1]},
                        {"className": "dt-left", "targets": [2,3,4]},
                        {"className": "dt-right", "targets": [5]}
                    ],
                    "initComplete": function () {
                        this.api()
                            .columns([0,1,2,3,4])
                            .every(function () {
                                let column = this;

                                // Create select element
                                let select = document.createElement('select');
                                select.add(new Option(''));
                                column.footer().replaceChildren(select);

                                // Apply listener for user change in value
                                select.addEventListener('change', function () {
                                    column
                                        .search(select.value, {exact: true})
                                        .draw();
                                });

                                // Add list of options
                                column
                                    .data()
                                    .unique()
                                    .sort()
                                    .each(function (d, j) {
                                        select.add(new Option(d));
                                    });
                            });
                    },
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
                $("#tab_qlp_senior_x_freigh").DataTable().columns.adjust().draw();

                let let_lista_qlp_filial = []
                data.lista_qlp_filial.forEach(item => {
                    let let_reg = [
                        item.quinz,
                        item.periodo,
                        item.nome_filial,
                        item.desc_cargo_senior,
                        item.desc_cargo_freightech,
                        item.qlp,
                        item.val_ordenados,
                        item.qlp_rem,
                        item.val_ordenado_rem
                    ];
                    let_lista_qlp_filial.push(let_reg);
                });
                $("#tab_qlp_filial_senior_x_freigh").DataTable({
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "770px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 10,
                    "responsive": false,
                    "stateSave": true,
                    "select": true,
                    "colReorder": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":let_lista_qlp_filial,
                    "columns": [
                        { title: "Quinzena" },
                        { title: "Dia" },
                        { title: "Filial" },
                        { title: "Cargo Senior" },
                        { title: "Cargo Freightech" },
                        { title: "Qlp." },
                        { title: "R$ TT Ordenados" },
                        { title: "Qlp Rem" },
                        { title: "R$ TT Ordenados Rem" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [0,1]},
                        {"className": "dt-left", "targets": [2,3,4]},
                        {"className": "dt-right", "targets": [5]}
                    ],
                    "initComplete": function () {
                        this.api()
                            .columns([0,1,2,3,4])
                            .every(function () {
                                let column = this;

                                // Create select element
                                let select = document.createElement('select');
                                select.add(new Option(''));
                                column.footer().replaceChildren(select);

                                // Apply listener for user change in value
                                select.addEventListener('change', function () {
                                    column
                                        .search(select.value, {exact: true})
                                        .draw();
                                });

                                // Add list of options
                                column
                                    .data()
                                    .unique()
                                    .sort()
                                    .each(function (d, j) {
                                        select.add(new Option(d));
                                    });
                            });
                    },
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
                $("#tab_qlp_filial_senior_x_freigh").DataTable().columns.adjust().draw();

				$.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '../../static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                let_loader_frm_imp_plan_freightech.style.display = "none";




			},
			error: function (request, status, error) {
			    let_loader_frm_imp_plan_freightech.style.display = "none";
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