

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
    let let_cor_empresa = $("#hd_cor_empresa_frm_custos_placa").val();
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
        let let_lista_handle_contas = $("#sl_conta_frm_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'lista_handle_proj'         :   let_lista_handle_proj,
                'lista_handle_tipo_contas'  :   let_lista_handle_tipo_contas,
                'lista_handle_contas'       :   let_lista_handle_contas,
                'comp'                      :   let_comp
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                //$("#div_placas_frm_custos_placa").html(dados);

                lista_placas_razao = [];
                dados.dic_dados_razao.forEach(doc => {
                    let let_comp_cluster = `
                        <select id="sl_cluster_frm_custos_placa_${doc.cod_razao_frota}"
                                name="sl_cluster_frm_custos_placa"
                                style="width: 160px!important;font-size: 10px;"
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

                    let let_tem_os = doc.tem_os;
                    let let_btn_visualiza_oss = `
                        <i class="fa-regular fa-file" style="color: ${let_cor_empresa};"
                           title='Sem OS para visualizar.'></i>
                    `;
                    if (let_tem_os == 'S'){
                        let_btn_visualiza_oss = `
                            <button type='button' name='btn_abri_modal_lista_os_razao_conta'
                                id='btn_abri_modal_lista_os_razao_conta_${doc.cod_razao_frota}'
                                class='btn btn-rounded btn-space'
                                value='${doc.cod_razao_frota}' title='Visualizar dados da(s) os(s).'>
                                <i class="fa-solid fa-file" style="color: ${let_cor_empresa};"></i>
                            </button>
                        `;
                    }


                    reg = [
                        doc.placa,
                        doc.conta,
                        doc.val_lanc,
                        doc.codigo_os,
                        doc.desc_tipo_os,
                        doc.obs,
                        doc.nome_fornec,
                        doc.num_doc_contabil,
                        doc.data_lancamento,
                        doc.nome_projeto,
                        doc.desc_tipo_conta,
                        let_comp_cluster,
                        let_btn_visualiza_oss
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
                    "pageLength": 6,
                    //"responsive": true,
                    "stateSave": true,
                    "select": true,
                    "colReorder": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data":lista_placas_razao,
                    "columns": [
                        { title: "Placa", class: "col_placa" },
                        { title: "Conta", class: "col_conta" },
                        { title: "R$ Valor", class:"col_val" },
                        { title: "OS", class: "col_os" },
                        { title: "Tipo OS", class: "col_tip_os" },
                        { title: "Histórico", class: "col_hist" },
                        { title: "Fornecedor", class: "col_fornec" },
                        { title: "Núm. Contábil", class: "col_num_cont" },
                        { title: "Dt. Lançamento", class: "col_dt_lanc" },
                        { title: "Projeto", class: "col_proj" },
                        { title: "Tipo Conta", class: "col_tipo_conta" },
                        { title: "Cluster", class: "col_cluster" },
                        { title: "Detalhes OS", class:"col_detail_os" }
                    ],
                    "initComplete": function () {
                        this.api()
                            .columns([0,1,2,3,7,10])
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
                        {"className": "dt-center", "targets": [8, 4]},
                        {"className": "dt-left", "targets": [0,1,10]},
                        {"className": "dt-right", "targets": [2,3,5,6,7,9,11]}
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
    } else if (let_nome_btn == 'btn_desmarcar_conta_frm_custos_placa'){
        $("#sl_conta_frm_custos_placa").selectpicker('deselectAll');

    }
    else if (let_nome_btn == 'btn_seleciona_todas_conta_frm_custos_placa') {
        $("#sl_conta_frm_custos_placa").selectpicker('selectAll');
    } else if(let_nome_btn == 'btn_abri_modal_lista_os_razao_conta') {

        $("#tab_lista_os_razao_placa tbody tr").remove();
        let let_cod_razao_frota = $(this).val();
        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        let let_cor_empresa = $("#hd_cor_empresa_frm_custos_placa").val();
        $.ajax({
            type: 'GET',
            data: {
                'cod_razao_frota'         :   let_cod_razao_frota
            },
            url:"/frota_custos_placa_app/retorna_oss_razao_conta",
            success: function(dados){
                let let_img = `
                    <i class="fa-solid fa-caret-right" style="color: ${let_cor_empresa}"></i>
                `;



                lista_os_razao_conta = [];
                dados.lista_obj_os_razao_conta.forEach(os => {
                    let let_checked = '';
                    if (os.eh_cluster == 1) {
                        let_checked = ' checked ';
                    }

                    let let_input_cluster_check = `
                        <input type="checkbox" ${let_checked} id="ck_os_razao_conta_${os.cod_os_razao_frota}"
                            name="ck_os_razao_conta">
                    `;

                    $("#tab_lista_os_razao_placa tbody").append(
                        `
                        <tr>
                            <td style="width: 2%;padding: 0.7rem;">${let_img}</td>
                            <td style="width: 3%;padding: 0.7rem;">${os.desc_tipo_os}</td>
                            <td style="width: 5%;padding: 0.7rem;">${os.cod_os}</td>
                            <td style="width: 15%;padding: 0.7rem;white-space: normal;">${os.desc_os}</td>
                            <td style="width: 15%;padding: 0.7rem;white-space: normal;">${os.desc_prod}</td>
                            <td style="width: 3%;padding: 0.7rem;">${os.qtd_prod}</td>
                            <td style="width: 5%;padding: 0.7rem;white-space: normal;">${os.desc_conj}</td>
                            <td style="width: 40%;padding: 0.7rem;white-space: normal;">${os.obs_os}</td>
                            <td style="max-width:5%;padding: 0.7rem;">${let_input_cluster_check}</td>
                        </tr>
                        `
                    );



                });


                let_loader_frm_custos_placa.style.display = "none";
                $("#modal_lista_os_razao_conta").show();


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

    } else if(let_nome_btn == 'btn_fecha_modal_lista_os_razao_conta') {
        $("#modal_lista_os_razao_conta").hide();

    }

});



$(document).on('change','#sl_cluster_frm_custos_placa', function(){
    let let_nome_select = $(this).attr('name');
    let let_id_select = $(this).attr('id');

    let let_cod_razao_frota = let_id_select.split('_')[5];
    let let_cod_item_cluster = $(this).val();

    let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
    let_loader_frm_custos_placa.style.display = "flex";
    $.ajax({
        type: 'POST',
        url: '/frota_custos_placa_app/altera_item_cluster_lancamento',
        data: {
            'cod_razao_frota'   :   let_cod_razao_frota,
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

});

$(document).on('change','input', function(){
    let let_name_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');

    if(let_name_input == 'ck_os_razao_conta'){
        let let_cod_os_razao_conta = let_id_input.split('_')[4];
        let let_check_comp = $(this).prop("checked");
        let let_status_check_comp = 0;
        if (let_check_comp == true) {
            let_status_check_comp = 1;
        }
        $.ajax({
            type: "POST",
            url: '/frota_custos_placa_app/altera_status_cluster_razao',
            data: {
                'cod_os_razao_conta'       :   let_cod_os_razao_conta,
                'status_check_comp'        :   let_status_check_comp
            },
            dataType: 'json',
            success: function (data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
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

});


$(document).on('change','#sl_proj_custos_placa', function(){
    atualiza_componente_sl_conta();
});

$(document).on('change','#sl_tipo_veic_equip_custos_placa', function(){
    atualiza_componente_sl_conta();
});

$(document).on('change','#dt_comp_frm_custos_placa', function(){
    atualiza_componente_sl_conta();
});

function atualiza_componente_sl_conta(){
    let let_lista_handle_proj = $("#sl_proj_custos_placa").val().toString();
    let let_lista_handle_tipo_contas = $("#sl_tipo_veic_equip_custos_placa").val().toString();
    let let_comp = $("#dt_comp_frm_custos_placa").val();

    if( let_lista_handle_proj != '' & let_lista_handle_tipo_contas != '' & let_comp != null & let_comp != '') {
        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'lista_handle_proj'         :   let_lista_handle_proj,
                'lista_handle_tipo_contas'  :   let_lista_handle_tipo_contas,
                'comp'                      :   let_comp
            },
            url:"/frota_custos_placa_app/atualiza_comp_sl_contas",
            success: function(dados){

                $("#sl_conta_frm_custos_placa option").remove();
                dados.lista_contas_periodo.forEach(conta => {
                    $("#sl_conta_frm_custos_placa").append(`<option value="${conta.handle_conta}">${conta.desc_conta}</option>`);
                });
                $("#sl_conta_frm_custos_placa").selectpicker('refresh');

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



}