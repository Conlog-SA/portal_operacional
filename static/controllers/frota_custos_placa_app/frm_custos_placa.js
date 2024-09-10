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
	let let_nome_btn = $(this).attr('name');
	let let_id_btn = $(this).attr('id');
	let let_val_btn = $(this).val();

    if (let_nome_btn == 'btn_desmarcar_projetos_frm_custos_placa'){
        $("#sl_proj_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_proj_frm_custos_placa') {
        $("#sl_proj_custos_placa").selectpicker('selectAll');
    } else if (let_nome_btn == 'btn_desmarcar_tipo_veic_equip_frm_custos_placa'){
        $("#sl_tipo_veic_equip_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_tipo_veic_equip_frm_custos_placa') {
        $("#sl_tipo_veic_equip_custos_placa").selectpicker('selectAll');
    } else if ( let_nome_btn == 'btn_gera_dados_custos_placas_proj' ) {
        let let_lista_handle_proj = $("#sl_proj_custos_placa").val().toString();
        let let_lista_handle_tipo_contas = $("#sl_tipo_veic_equip_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'lista_handle_proj'         :   let_lista_handle_proj,
                'lista_handle_tipo_contas'  :   let_lista_handle_tipo_contas,
                'comp'                      :   let_comp
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                //$("#div_placas_frm_custos_placa").html(dados);

                lista_placas_razao = [];
                dados.dic_dados_razao.forEach(doc => {
                    let let_comp_cluster = `
                        <select id="sl_cluster_frm_custos_placa_${doc.handle_lan}"
                                name="sl_cluster_frm_custos_placa"
                                style="font-size: 10px;"
                                data-live-search="true">
                    `;
                    dados.lista_cluster.forEach(item => {
                        let let_selected = ``;
                        if(item.cod_item_cluster == doc.cod_cluster){
                            let_selected = `selected=selected`;
                        }
                        let_comp_cluster += `<option value="${item.cod_item_cluster}" ${let_selected}>${item.desc_item_cluster}</option>`;
                    });
                    let_comp_cluster += `</select>`;

                    reg = [
                        doc.placa,
                        doc.conta,
                        doc.codigo_os,
                        doc.desc_os,
                        doc.val_lanc,
                        let_comp_cluster,
                        doc.obs,
                        doc.nome_fornec,
                        doc.desc_produto,
                        doc.num_doc_contabil,
                        doc.nome_projeto,
                        doc.desc_tipo_conta,
                        doc.desc_tipo_os,
                        doc.obs_os
                    ];
                    lista_placas_razao.push(reg);
                });
                $("#tab_placas_razao").DataTable({
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "770px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 10,
                    "responsive": true,
                    "stateSave": true,
                    "select": true,
                    "colReorder": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":lista_placas_razao,
                    "columns": [
                        { title: "Placa" },
                        { title: "Conta" },
                        { title: "OS" },
                        { title: "Descrição OS" },
                        { title: "R$ Valor" },
                        { title: "Cluster" },
                        { title: "Histórico" },
                        { title: "Fornecedor" },
                        { title: "Item OS" },
                        { title: "Núm. Contábil" },
                        { title: "Projeto" },
                        { title: "Tipo Conta" },
                        { title: "Tipo OS" },
                        { title: "Obs. OS" }
                    ],
                    "initComplete": function () {
                        this.api()
                            .columns([0,1,2,7,9,10,11])
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
                        {"className": "dt-center", "targets": [2,5,9]},
                        {"className": "dt-left", "targets": [0,1,4,6,7,8,10,11]},
                        {"className": "dt-right", "targets": [3]}
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
                $("#tab_placas_razao").DataTable().columns.adjust().draw();

                let_loader_frm_custos_placa.style.display = "none";


            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    } if (let_nome_btn == 'btn_desmarcar_conta_frm_custos_placa'){
        $("#sl_conta_frm_custos_placa").selectpicker('deselectAll');

    } else if (let_nome_btn == 'btn_seleciona_todas_conta_frm_custos_placa') {
        $("#sl_conta_frm_custos_placa").selectpicker('selectAll');
    }

});



$(document).on('change','select', function(){
    let let_nome_select = $(this).attr('name');
    let let_id_select = $(this).attr('id');

    if (let_nome_select == 'sl_cluster_frm_custos_placa'){
        let let_cod_lan = let_id_select.split('_')[5];
        let let_cod_item_cluster = $(this).val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'POST',
            url: '/frota_custos_placa_app/altera_item_cluster_lancamento',
            data: {
                'cod_lan'           :   let_cod_lan,
                'cod_item_cluster'  :   let_cod_item_cluster
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



                let_loader_frm_custos_placa.style.display = "none";

            },
            error: function (request, status, error) {
                let_loader_frm_custos_placa.style.display = "none";
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