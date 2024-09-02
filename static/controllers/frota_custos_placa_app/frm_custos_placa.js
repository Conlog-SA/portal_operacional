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
        let let_lista_handle_contas = $("#sl_tipo_veic_equip_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'lista_handle_proj'         :   let_lista_handle_proj,
                'lista_handle_contas'       :   let_lista_handle_contas,
                'comp'                      :   let_comp
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                //$("#div_placas_frm_custos_placa").html(dados);
                lista_placas_razao = [];
                dados.dic_dados_razao.forEach(doc => {
                    reg = [
                        '',
                        doc.placa,
                        doc.nome_projeto,
                        doc.desc_tipo_conta,
                        doc.conta,
                        doc.desc_tipo_doc,
                        doc.num_doc,
                        doc.num_doc_contabil,
                        doc.val_lanc,
                        doc.tipo_lancamento,
                        doc.obs,
                        doc.codigo_os,
                        doc.desc_os,
                        doc.desc_produto,
                        doc.desc_cluster,
                        ''
                    ];
                    lista_placas_razao.push(reg);
                });
                $("#tab_placas_razao").DataTable({
                    /*"bJQueryUI": true,
                    "pageLength": 10,
                    "destroy": true,
                    "fixedHeader": {
                        header: true,
                        footer: false
                    },
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copy'
                    ],
                    */
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
                    "data":lista_placas_razao,
                    "columns": [
                        { title: "" },
                        { title: "Placa" },
                        { title: "Projeto" },
                        { title: "Tipo Conta" },
                        { title: "Conta" },
                        { title: "Tipo Doc." },
                        { title: "Núm. Doc." },
                        { title: "Núm. Contábil" },
                        { title: "R$ Valor" },
                        { title: "Tipo Lançamento" },
                        { title: "Histórico" },
                        { title: "OS" },
                        { title: "Descrição OS" },
                        { title: "Item OS" },
                        { title: "Cluster" },
                        { title: "Editar" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [5,7]},
                        {"className": "dt-left", "targets": [0]},
                        {"className": "dt-right", "targets": [1, 2, 3, 4, 6,8]}
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