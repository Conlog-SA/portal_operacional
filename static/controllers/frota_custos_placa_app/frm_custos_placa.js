

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
        let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
        let let_lista_handle_contas = $("#sl_conta_frm_custos_placa").val().toString();
        let let_comp = $("#dt_comp_frm_custos_placa").val();

        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'handle_filial'         :   let_handle_filial,
                'lista_handle_contas'   :   let_lista_handle_contas,
                'comp'                  :   let_comp
            },
            url:"/frota_custos_placa_app/gera_dados_razao_placas_proj",
            success: function(dados){
                //$("#div_placas_frm_custos_placa").html(dados);
                let let_conteudo_div_tab_resumo_custos_fil = ``;
                dados.dic_resumo_filial.forEach(conta => {
                    let_conteudo_div_tab_resumo_custos_fil += `
                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex justify-content-between align-items-between w-50">
                                ${conta.NOME_CONTA}
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-25" style="border-bottom: 2px dashed #BDB1A8;">
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-25">
                                ${conta.VAL_LANC}
                            </div>
                        </div>
                    `;
                });
                $("#div_tab_resumo_custos_fil").html(let_conteudo_div_tab_resumo_custos_fil);


                let let_div_tab_resumo_custos_proj = ``;
                dados.dic_resumo_projeto.forEach(proj => {
                    let_div_tab_resumo_custos_proj += `
                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex justify-content-between align-items-between w-50">
                                Projeto : ${proj.NOME_PROJETO}
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex justify-content-between align-items-between w-50">
                                ${proj.NOME_CONTA}
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-25" style="border-bottom: 2px dashed #BDB1A8;">
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-25">
                                R$ ${proj.VAL_LANC}
                            </div>
                        </div>
                    `;
                });
                $("#div_tab_resumo_custos_proj").html(let_div_tab_resumo_custos_proj);


                let let_div_tab_resumo_custos_placa = ``;
                dados.dic_projeto_placa.forEach(placa => {
                    let_div_tab_resumo_custos_placa += `
                        <div class="d-flex flex-column justify-content-between align-items-between w-100">
                            <div class="d-flex justify-content-between align-items-between w-50">
                                PLACA : ${placa.PLACA}
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-50">
                                Projeto : ${placa.NOME_PROJETO}
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex justify-content-between align-items-between w-50">
                                ${placa.NOME_CONTA}
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-25" style="border-bottom: 2px dashed #BDB1A8;">
                            </div>
                            <div class="d-flex justify-content-between align-items-between w-25">
                                R$ ${placa.VAL_LANC}
                            </div>
                        </div>
                    `;
                });
                $("#div_tab_resumo_custos_placa").html(let_div_tab_resumo_custos_placa);

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
                    let let_btn_visualiza_os = `
                        <i class="fa-regular fa-file" style="color: ${let_cor_empresa};"
                           title='Sem OS para visualizar.'></i>
                    `;
                    if (let_tem_os == 'S'){
                        let_btn_visualiza_os = `
                            <button type='button' name='btn_abri_modal_lista_os_razao_conta'
                                id='btn_abri_modal_lista_os_razao_conta_${doc.cod_razao_frota}'
                                class='btn btn-rounded btn-space'
                                value='${doc.cod_razao_frota}' title='Visualizar dados da(s) os(s).'>
                                <i class="fa-solid fa-file" style="color: ${let_cor_empresa};"></i>
                            </button>
                        `;
                    }


                    reg = [
                        "<i class='fa-solid fa-caret-right'></i>&nbsp;&nbsp;"+doc.placa,
                        doc.conta,
                        doc.data_lancamento,
                        doc.val_lanc,
                        let_comp_cluster,
                        let_btn_visualiza_os
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
                        { title: "Dt. Lançamento", class: "col_dt_lanc" },
                        { title: "R$ Valor", class:"col_val" },
                        { title: "Cluster", class: "col_cluster" },
                        { title: "Detalhes OS", class:"col_detail_os" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [1,4,5]},
                        {"className": "dt-left", "targets": [0,]},
                        {"className": "dt-right", "targets": [2,3]}
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

                let div_os = `

                `;
                dados.lista_obj_os_razao_conta.forEach(os => {
                    let let_checked = '';
                    if (os.eh_cluster == 1) {
                        let_checked = ' checked ';
                    }

                    let let_input_cluster_check = `
                        <input type="checkbox" ${let_checked} id="ck_os_razao_conta_${os.cod_os_razao_frota}"
                            name="ck_os_razao_conta">
                    `;

                    let let_obs_os = `&nbsp;&nbsp;`;
                    if( os.obs_os != null && os.obs_os != ''){
                        let_obs_os = os.obs_os;
                    }

                    let let_fornecedor = `&nbsp;&nbsp;`;
                    if( os.cod_razao_frota__nome_fornecedor != null ){
                        let_fornecedor = os.cod_razao_frota__nome_fornecedor;
                    }

                    div_os += `
                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>${let_img}&nbsp;&nbsp;OS</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_os}</div>
                            </div>
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Tipo OS</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.desc_tipo_os}</div>
                            </div>
                            <div class="d-flex flex-column w-100 justify-content-center align-items-end" style="margin-right: 0.25rem;">
                                ${let_input_cluster_check}
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Item</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.desc_prod}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Qtd.</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.qtd_prod}</div>
                            </div>
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Conjunto</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.desc_conj}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Observação OS</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                      style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${let_obs_os}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div><i class="fa-solid fa-receipt"></i>&nbsp;&nbsp;Núm. Contábil</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__doc_contabil}</div>
                            </div>
                            <div class="d-flex flex-column w-100 align-items-start" style="margin-right: 0.25rem;">
                                <div>Tipo Conta</div>
                                <div class="d-flex justify-content-end align-items-center w-100 p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__desc_tipo_conta}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Fornecedor</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${let_fornecedor}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Histórico lançamento</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__historico}</div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between align-items-between w-100">
                            <div class="d-flex flex-column w-100" style="margin-right: 0.25rem;">
                                <div>Projeto</div>
                                <div class="d-flex justify-content-end align-items-center p-1"
                                     style="background: #FFFFFF;color: #000000;font-size:12px;font-weight:400;">${os.cod_razao_frota__desc_projeto}</div>
                            </div>
                        </div>
                    `;
                });
                div_os += `
                    </div>
                `;

                let_loader_frm_custos_placa.style.display = "none";
                $("#div_dados_os").html(div_os);
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


$(document).on('change','#sl_handle_filial_custos_placa', function(){
    atualiza_componente_sl_conta();
});

$(document).on('change','#sl_tipo_veic_equip_custos_placa', function(){
    atualiza_componente_sl_conta();
});

$(document).on('change','#dt_comp_frm_custos_placa', function(){
    atualiza_componente_sl_conta();
});

function atualiza_componente_sl_conta(){
    let let_handle_filial = $("#sl_handle_filial_custos_placa").val();
    //let let_lista_handle_tipo_contas = $("#sl_tipo_veic_equip_custos_placa").val().toString();
    let let_comp = $("#dt_comp_frm_custos_placa").val();

    if( let_handle_filial != '' && let_comp != null && let_comp != '') {
        let let_loader_frm_custos_placa = document.getElementById("loader_frm_custos_placa");
        let_loader_frm_custos_placa.style.display = "flex";
        $.ajax({
            type: 'GET',
            data: {
                'handle_filial'         :   let_handle_filial,
                //'lista_handle_tipo_contas'  :   let_lista_handle_tipo_contas,
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