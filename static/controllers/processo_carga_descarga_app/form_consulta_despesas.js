let let_lista_dados_tab_mapas = []
let let_lista_dados_tab_mapas_emp = []
let let_lista_dados_tab_mapas_lanc = []
let let_lista_clientes_filial = []
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

$(document).on('click','button', function(){
	let let_nome_btn = $(this).attr('name');
    let let_id_btn = $(this).attr('id');
    let let_val_btn = $(this).attr('value');

    if (let_nome_btn == "btn_pesq_mapas_clientes") {
        povoa_tab_mapas_despesa_2art();
    } else if (let_nome_btn == "btn_abre_modal_desp") {
        limpa_campos();
        $("#in_data_mapa").prop('disabled', true);
        $("#in_mapa").prop('disabled',true);
        $("#in_entrega").prop('disabled', true);
        $("#in_placa").prop('disabled', true);
        $("#sub_categoria").prop('disabled', true);

        let let_indice_dado = let_val_btn.split('_')[0];
        let let_modal = let_val_btn.split('_')[2];
        $("#fecha_modal_carga_desc").val(let_indice_dado);
        $("#hd_tipo_modal").val(let_modal);

        console.log(let_lista_clientes_filial)
        $("#cod_promax_cliente").selectpicker('val', let_lista_clientes_filial).selectpicker('refresh');

        if (let_modal == 'Mapas2art') {
            let let_id_mapa = let_lista_dados_tab_mapas[let_indice_dado][7];
            $("#btn_salva_desp_carg_desc").val(let_id_mapa);
            $("#in_data_mapa").val(let_lista_dados_tab_mapas[let_indice_dado][1]);
            $("#in_mapa").val(let_lista_dados_tab_mapas[let_indice_dado][2]);
            $("#in_entrega").selectpicker('val', let_lista_dados_tab_mapas[let_indice_dado][3]).selectpicker('refresh');
            $("#in_placa").val(let_lista_dados_tab_mapas[let_indice_dado][4]);
            if (let_lista_dados_tab_mapas[let_indice_dado][3] == 'Rota'){
               $("#sub_categoria").selectpicker('val', '0').selectpicker('refresh');
            } else if (let_lista_dados_tab_mapas[let_indice_dado][3] == 'AS'){
               $("#sub_categoria").selectpicker('val', '1').selectpicker('refresh');
            }
            povoa_tab_cliente_vincul_mapa('formatado', let_lista_dados_tab_mapas[let_indice_dado][8]);
        } else if (let_modal == 'LancEmpurrada') {
            let let_id_mapa = let_lista_dados_tab_mapas_emp[let_indice_dado][2];
            let let_id_filial =  $("#cb_filial_pesq_mapas").val();
            $("#btn_salva_desp_carg_desc").val(let_id_mapa + '-' + let_id_filial);
            $("#in_placa").val(let_lista_dados_tab_mapas_emp[let_indice_dado][4]);
            $("#in_data_mapa").val(let_lista_dados_tab_mapas_emp[let_indice_dado][1]);
            $("#in_mapa").val(let_lista_dados_tab_mapas_emp[let_indice_dado][2]);
            $("#in_entrega").selectpicker('val', let_lista_dados_tab_mapas_emp[let_indice_dado][3]).selectpicker('refresh');
            povoa_tab_cliente_vincul_mapa('formatado', let_lista_dados_tab_mapas_emp[let_indice_dado][8]);
        } else if (let_modal == 'LancRota/AS') {
            let let_id_mapa = let_lista_dados_tab_mapas_lanc[let_indice_dado][2];
            let let_id_filial =  $("#cb_filial_pesq_mapas").val();
            $("#btn_salva_desp_carg_desc").val(let_id_mapa + '-' + let_id_filial);
            $("#in_placa").val(let_lista_dados_tab_mapas_lanc[let_indice_dado][4]);
            $("#in_data_mapa").val(let_lista_dados_tab_mapas_lanc[let_indice_dado][1]);
            $("#in_mapa").val(let_lista_dados_tab_mapas_lanc[let_indice_dado][2]);
            $("#in_entrega").selectpicker('val', let_lista_dados_tab_mapas_lanc[let_indice_dado][3]).selectpicker('refresh');
            povoa_tab_cliente_vincul_mapa('formatado', let_lista_dados_tab_mapas_lanc[let_indice_dado][8]);
        }
        $("#div_tabela").show();
        $("#modal_lanca_despesa").show();
    } else if (let_nome_btn == "fecha_modal_carga_desc") {
        $("#modal_lanca_despesa").hide();
        povoa_tab_mapas_despesa_2art();
    } else if (let_nome_btn == "fecha_modal_cad_cliente") {
        $("#modal_cad_cliente").hide();
    } else if (let_nome_btn == "btn_cad_clientes") {
        let let_cod_filial = $("#cb_filial_pesq_mapas").val();
        if (!let_cod_filial || let_cod_filial.trim() === '') {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Por favor, selecione a filial para cadastrar o fornecedor.',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            return;
        } else {
            $("#modal_cad_cliente").show();
        }
    } else if (let_nome_btn == "btn_salva_cadastro_cli") {
        let let_cod_filial = $("#cb_filial_pesq_mapas").val();
        let let_cod_promax_cliente = $("#cliente").val();
        let let_nome_cliente = $("#nome_cliente").val();
        if ((!let_cod_filial || let_cod_filial.trim() === '') || (!let_cod_promax_cliente || let_cod_promax_cliente.trim() === '') || (!let_nome_cliente || let_nome_cliente === "0")) {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Por favor, preencha os dois campos.',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            return;
        } else {
            $.ajax({
            type: 'POST',
            url: '/processo_carga_descarga_app/frm_cadastra_cliente',
            data: {
                'cod_filial': let_cod_filial,
                'cod_promax_cliente': let_cod_promax_cliente,
                'nome_cliente': let_nome_cliente
              },
            success: function (dados) {
                limpa_campos_cadastro_cli()
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
    } else if (let_nome_btn == "btn_salva_desp_carg_desc") {
        let let_id_despesa = $(this).val();
        let let_valor_btn = $(this).val();
        let let_cod_filial = $("#cb_filial_pesq_mapas").val();
        let let_tipo_despesa = $("#slc_tipo_despesa").val();
        let let_entrega = $("#in_entrega").val();
        let let_despesa = $("#sl_desp").val();
        let let_subcategoria = $("#sub_categoria").val();
        let let_data = $("#in_data_mapa").val();
        let let_mapa = $("#in_mapa").val();
        let let_placa = $("#in_placa").val();
        let let_cod_cliente = $("#cod_promax_cliente").val();
        let let_tipo_descarga = $("#tipo_descarga").val();
        let let_quantidade = $("#qntd_carga").val();
        let let_valor_unit = $("#val_unit").val();
        let let_comprovante = $("#fl_comp_pagamento").val();
        let let_modal = $("#hd_tipo_modal").val();
        let let_un_venda = $("#un_venda").val();
        let let_cod_promax = let_val_btn.split('-')[1];

        if (let_tipo_descarga == 1){
            let_quantidade = 1
        }

        let let_frm_data = new FormData();
        let_frm_data.append('cod_filial', let_cod_filial);
        let_frm_data.append('modal', let_modal);
        let_frm_data.append('id_despesa', let_id_despesa);
        let_frm_data.append('tipo_despesa', let_tipo_despesa);
        let_frm_data.append('entrega', let_entrega);
        let_frm_data.append('despesa', let_despesa);
        let_frm_data.append('subcategoria', let_subcategoria);
        let_frm_data.append('dt_mapa', let_data);
        let_frm_data.append('mapa', let_mapa);
        let_frm_data.append('placa', let_placa);
        let_frm_data.append('tipo_descarga', let_tipo_descarga);
        let_frm_data.append('quantidade', let_quantidade);
        let_frm_data.append('valor_unit', let_valor_unit);
        let_frm_data.append('un_venda', let_un_venda);
        let_frm_data.append('cod_promax', let_cod_promax);
        let_frm_data.append("file", $('#fl_comp_pagamento')[0].files[0]);
        let_frm_data.append('cod_cliente', let_cod_cliente);

        if((let_tipo_descarga != '' && let_tipo_descarga != 0) && (let_cod_cliente != 0 && let_cod_cliente != '')
            && (let_quantidade != 0 && let_quantidade != '') && (let_valor_unit != 0 && let_valor_unit != '')
            && (let_comprovante != 0 && let_comprovante != '') && (let_data != 0 && let_data != '')
            && (let_mapa != 0 && let_mapa != '') && (let_entrega != 0 && let_entrega != '')
            && (let_placa != 0 && let_placa != '') && (let_un_venda != '') && (let_cod_filial != '')){
            $.ajax({
                type: 'POST',
                enctype: "multipart/form-data; charset=utf-8",
                url: '/processo_carga_descarga_app/frm_salva_lancamento_despesa',
                data: let_frm_data,
                dataType: 'json',
                processData: false,
                contentType: false,
                cache: false,
                success: function (dados) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    if (let_valor_btn == 0){
                        limpa_todos_campos();
                    } else {
                        limpa_campos();
                    }
                    povoa_tab_cliente_vincul_mapa('sem_formatacao', dados.lista_dic_despesas);
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
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Selecione a unidade e preencha todas as informações! É possível selecionar somente Rota ou AS',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    } else if ( let_nome_btn == "btn_visualiza_comprovante") {
        let let_caminho_comprovante = let_val_btn;
        //window.open('https://operacional.conlogsa.com.br//media/'+let_caminho_comprovante, '_blank');
        window.open('http://127.0.0.1:8000/media/'+let_caminho_comprovante, '_blank');
    } else if (let_nome_btn == "btn_adc_mapa_empurrada"){
        $("#hd_tipo_modal").val('Empurrada');
        $("#cod_promax_cliente").selectpicker('val', let_lista_clientes_filial).selectpicker('refresh');
        limpa_campos();
        $("#in_data_mapa").prop('disabled', false);
        $("#in_mapa").prop('disabled', false);
        $("#in_entrega").prop('disabled', false);
        $("#in_placa").prop('disabled', false);
        $("#sub_categoria").prop('disabled', false);
        $("#in_data_mapa").val('');
        $("#in_mapa").val('');
        $("#in_placa").val('');
        $("#in_entrega option[value='Rota']").prop("disabled", true);
        $("#in_entrega option[value='AS']").prop("disabled", true);
        $("#in_entrega option[value='Empurrada']").prop("disabled", false);
        $('#in_entrega').selectpicker('refresh');
        $("#btn_salva_desp_carg_desc").val(0);
        $("#div_tabela").hide();
        $("#modal_lanca_despesa").show();
        $("#in_entrega").val('Empurrada');
    } else if (let_nome_btn == "btn_adc_mapa_rota_lancado"){
        $("#hd_tipo_modal").val('LancRota/AS');
        $("#cod_promax_cliente").selectpicker('val', let_lista_clientes_filial).selectpicker('refresh');
        limpa_campos();
        $("#in_data_mapa").prop('disabled', false);
        $("#in_mapa").prop('disabled', false);
        $("#in_entrega").prop('disabled', false);
        $("#in_placa").prop('disabled', false);
        $("#sub_categoria").prop('disabled', false);
        $("#in_entrega").val('');
        $("#in_data_mapa").val('');
        $("#in_mapa").val('');
        $("#in_placa").val('');
        $("#in_entrega").selectpicker('refresh');
        $("#div_tabela").hide();
        $("#btn_salva_desp_carg_desc").val(0);
        $("#in_entrega option[value='Empurrada']").prop("disabled", true);
        $("#in_entrega option[value='Rota']").prop("disabled", false);
        $("#in_entrega option[value='AS']").prop("disabled", false);
        $('#in_entrega').selectpicker('refresh');
        $("#modal_lanca_despesa").show();
    } else if ( let_nome_btn == 'btn_excluir_desp'){
        let let_cod_reg = let_val_btn;
        $.ajax({
            type: 'DELETE',
            url: '/processo_carga_descarga_app/frm_deleta_lancamento_despesa/'+let_val_btn,
            dataType: 'json',
            success: function(data){
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tab_cliente_vincul_mapa('sem_formatacao',data.lista_dic_despesas);
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
});

function povoa_tab_mapas_despesa_2art(){
    $(".cl_btn_abre_modal_desp").prop('disabled', true);
    $(".cl_btn_abre_modal_desp_emp").prop('disabled', true);
    $(".cl_btn_abre_modal_desp_lancadas").prop('disabled', true);
    $("#btn_adc_mapa_empurrada").prop('disabled', true);
    $("#btn_adc_mapa_rota_lancado").prop('disabled', true);

    let let_cod_filial = $("#cb_filial_pesq_mapas").val();
    let let_data_ini = $("#dt_pesq_mapas_clientes_ini").val();
    let let_data_fim = $("#dt_pesq_mapas_clientes_fim").val();
    if ( let_data_ini == "" || let_data_fim == "" && let_cod_filial ==  "") {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Favor informe a data e a unidade!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        loader_carrega_despesa_2art.style.display = "flex";

        $.ajax({
            type: 'GET',
            url:"/processo_carga_descarga_app/frm_consulta_despesas",
            data: {
                'cod_filial': let_cod_filial,
                'data_inicial': let_data_ini,
                'data_final': let_data_fim
              },
            success: function(dados){
                let_lista_dados_tab_mapas = [];
                let_lista_dados_tab_mapas_emp = [];
                let_lista_dados_tab_mapas_lanc = [];
                let_lista_clientes_filial = [];
                let let_img = `<i class="fa-solid fa-caret-right icon-color-e"></i>`;
                let let_count_reg = 0
                let let_count_emp = 0
                let let_count_lanc = 0
                let let_cod_filial = $("#cb_filial_pesq_mapas").val();
                /* Lista Filial */
                dados.lista_clientes.forEach(cliente => {
                     let let_cliente = [
                        /*0*/cliente.cod_cliente,
                        /*1*/cliente.cod_promax_cliente,
                        /*2*/cliente.nome_cliente,
                    ];
                    let_lista_clientes_filial.push(let_cliente)
                });

                let clienteSelect = $("#cod_promax_cliente");
                clienteSelect.empty();
                let_lista_clientes_filial.forEach(cliente_fil => {
                    clienteSelect.append(`
                        <option value="${cliente_fil[0]}">
                            ${cliente_fil[1]} - Cliente: ${cliente_fil[2]}
                        </option>
                    `);
                });
                /* Mapas do 2art */
                dados.lista_dic_mapas_despesas.forEach(mapa => {
                    let let_btn_lanca_desp = `
                        <button type='button' name='btn_abre_modal_desp'
                            style='background: transparent;padding-left: 14px;padding-right: 14px;'
                            id='btn_abre_modal_desp_${mapa.mapa}_${let_cod_filial}' class='mr-2 btn cl_btn_abre_modal_desp'
                            value='${let_count_reg}_${mapa.entrega}_Mapas2art'>

                            <i class="fa-solid fa-circle-plus" style="color: #f46424!important;" title="Lançar Despesa" ></i>
                        </button>
                    `;

                    if (mapa.tem_despesa == 'S') {
                        mapa.tem_despesa = 'Lançada'
                    } else {
                        mapa.tem_despesa = 'Não lançada'
                    }
                    let let_dado_2art_cli = [
                        /*0*/let_img,
                        /*1*/mapa.dt_mapa,
                        /*2*/mapa.mapa,
                        /*3*/mapa.entrega,
                        /*4*/mapa.placa,
                        /*5*/let_btn_lanca_desp,
                        /*6*/mapa.tem_despesa,
                        /*7*/mapa.id
                    ];

                    let let_dado_despesas = [];
                    if(mapa.lista_desp_mapa != null){
                        mapa.lista_desp_mapa.forEach(desp => {

                            let let_btn_exclui_desp = `
                                <button type='button' name='btn_excluir_desp' style='background: transparent;padding-left: 14px;padding-right: 14px;'
                                    id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas'
                                    value='${desp.id_despesa}'>
                                    <i class="fa-solid fa-trash-can" style="color: #f46424!important;" title="Excluir Despesa" ></i>
                                </button>
                            `;

                            let let_status_importacao = 'Não Importado'
                            if (desp.importado == 1) {
                                let_status_importacao = 'Importado'
                                let_btn_exclui_desp = `
                                    <button type='button' name='btn_excluir_desp' id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas' style='border: none;padding-left: 38px;'
                                        value='${desp.id_despesa}' disabled="disabled" title="Bloqueado">
                                        <i class="fa-solid fa-ban" style="color: #f46424!important;" title="Bloqueado"></i>
                                    </button>
                                `;
                            }
                            if (desp.despesa == 1) {
                                let_despesa = 'Serviço'
                            }
                            if (desp.tipo_descarga == 1) {
                                let_tipo_descarga = 'Por Entrega'
                            } else if (desp.tipo_descarga == 2) {
                                let_tipo_descarga = 'Por Paleta'
                            } else if (desp.tipo_descarga == 3) {
                                let_tipo_descarga = 'Por Caixa'
                            }
                            let let_btn_abre_comp = `
                                    <button type='button' name='btn_visualiza_comprovante'
                                            id='btn_visualiza_comprovante'
                                            class='btn btn-rounded btn-space'
                                            value='${desp.comprovante}'>
                                        <i class="fa-solid fa-file-pdf fa-2xl" style="color: rgb(25,107,152);"></i>
                                    </button>
                                `;

                            let let_desp = [
                                /*0*/let_img,
                                /*1*/desp.cod_cliente,
                                /*2*/let_tipo_descarga,
                                /*3*/desp.quantidade,
                                /*4*/desp.valor_unit,
                                /*5*/let_despesa,
                                /*6*/desp.data_lancamento,
                                /*7*/let_btn_abre_comp,
                                /*8*/let_status_importacao,
                                /*9*/desp.un_venda,
                                /*10*/let_btn_exclui_desp
                            ]
                            let_dado_despesas.push(let_desp)
                        });
                    }

                    let_dado_2art_cli.push(let_dado_despesas);
                    let_lista_dados_tab_mapas.push(let_dado_2art_cli);
                    let_count_reg+=1;
                });
                $('#tab_mapas_clientes_2art').DataTable({
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
                    "dom": 'frtip',
                    "buttons": [],
                    "searching": true,
                    "data":let_lista_dados_tab_mapas,
                    "columns": [
                        { title: "" },
                        { title: "Data da viagem" },
                        { title: "Mapa" },
                        { title: "Entrega" },
                        { title: "Placa" },
                        { title: "Despesa" },
                        { title: "Despesa Lançada" },
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [1,2,3,4,5,6]},
                        {"className": "dt-left", "targets": [0]},
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
                    }

              });

              /* DT de Empurrada Lançados */
              dados.lista_dic_mapas_despesas_empurrada.forEach(mapa => {
                    let let_btn_lanca_desp = `
                        <button type='button' name='btn_abre_modal_desp' style='background: transparent;padding-left: 14px;padding-right: 14px;'
                            id='btn_abre_modal_desp_${mapa.mapa}_${let_cod_filial}' class='mr-2 btn cl_btn_abre_modal_desp_emp'
                            value='${let_count_emp}_${mapa.entrega}_LancEmpurrada'>

                            <i class="fa-solid fa-circle-plus" style="color: #f46424!important;" title="Lançar Despesa" ></i>
                        </button>
                    `;


                    if (mapa.tem_despesa == 'S') {
                        mapa.tem_despesa = 'Lançada'
                    } else {
                        mapa.tem_despesa = 'Não lançada'
                    }

                    let let_dado_emp_cli = [
                        /*0*/let_img,
                        /*1*/mapa.dt_mapa,
                        /*2*/mapa.mapa,
                        /*3*/mapa.entrega,
                        /*4*/mapa.placa,
                        /*5*/let_btn_lanca_desp,
                        /*6*/mapa.tem_despesa,
                        /*7*/let_cod_filial
                    ];


                    let let_dado_despesas = [];
                    if(mapa.lista_desp_mapa_emp != null){
                        mapa.lista_desp_mapa_emp.forEach(desp => {
                            let let_btn_exclui_desp = `
                                <button type='button' name='btn_excluir_desp' style='background: transparent;padding-left: 14px;padding-right: 14px;'
                                    id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas'
                                    value='${desp.id_despesa}'>
                                    <i class="fa-solid fa-trash-can" style="color: #f46424!important;" title="Excluir Despesa" ></i>
                                </button>
                            `;
                            let let_status_importacao = 'Não Importado'
                            if (desp.importado == 1) {
                                let_status_importacao = 'Importado'
                                let_btn_exclui_desp = `
                                    <button type='button' name='btn_excluir_desp' id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas' style='border: none;padding-left: 38px;'
                                        value='${desp.id_despesa}' disabled="disabled" title="Bloqueado">
                                        <i class="fa-solid fa-ban" style="color: #f46424!important;" title="Bloqueado"></i>
                                    </button>
                                `;
                            }


                            if (desp.despesa == 1) {
                                let_despesa = 'Serviço'
                            }

                            if (desp.tipo_descarga == 1) {
                                let_tipo_descarga = 'Por Entrega'
                            } else if (desp.tipo_descarga == 2) {
                                let_tipo_descarga = 'Por Paleta'
                            } else if (desp.tipo_descarga == 3) {
                                let_tipo_descarga = 'Por Caixa'
                            }

                            let let_btn_abre_comp = `
                                    <button type='button' name='btn_visualiza_comprovante'
                                            id='btn_visualiza_comprovante'
                                            class='btn btn-rounded btn-space'
                                            value='${desp.comprovante}'>
                                        <i class="fa-solid fa-file-pdf fa-2xl" style="color: rgb(25,107,152);"></i>
                                    </button>
                                `;


                            let let_desp = [
                                /*0*/let_img,
                                /*1*/desp.cod_cliente,
                                /*2*/let_tipo_descarga,
                                /*3*/desp.quantidade,
                                /*4*/desp.valor_unit,
                                /*5*/let_despesa,
                                /*6*/desp.data_lancamento,
                                /*7*/let_btn_abre_comp,
                                /*8*/let_status_importacao,
                                /*9*/desp.un_venda,
                                /*10*/let_btn_exclui_desp
                            ]
                            let_dado_despesas.push(let_desp)
                        });
                    }

                    let_dado_emp_cli.push(let_dado_despesas);
                    let_lista_dados_tab_mapas_emp.push(let_dado_emp_cli);
                    let_count_emp+=1;
                });
                $('#tab_mapas_clientes_emp').DataTable( {
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
                    "dom": 'frtip',
                    "buttons": [],
                    "searching": true,
                    "data":let_lista_dados_tab_mapas_emp,
                    "columns": [
                        { title: "" },
                        { title: "Data da viagem" },
                        { title: "Mapa" },
                        { title: "Entrega" },
                        { title: "Placa" },
                        { title: "Despesa" },
                        { title: "Despesa Lançada" },
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [1,2,3,4,5,6]},
                        {"className": "dt-left", "targets": [0]},
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
                    }

              });
              $("#tab_mapas_clientes_emp").DataTable().columns.adjust().draw();

              /* Mapas Lançados */
              dados.lista_dic_mapas_despesas_rota_lancadas.forEach(mapa => {
                    let let_btn_lanca_desp = `
                        <button type='button' name='btn_abre_modal_desp' style='background: transparent;padding-left: 14px;padding-right: 14px;'
                            id='btn_abre_modal_desp_${mapa.mapa}_${let_cod_filial}' class='mr-2 btn cl_btn_abre_modal_desp_lancadas'
                            value='${let_count_lanc}_${mapa.entrega}_LancRota/AS'>

                            <i class="fa-solid fa-circle-plus" style="color: #f46424!important;" title="Lançar Despesa" ></i>
                        </button>
                    `;

                    if (mapa.tem_despesa == 'S') {
                        mapa.tem_despesa = 'Lançada'
                    } else {
                        mapa.tem_despesa = 'Não lançada'
                    }

                    let let_dado_lancado = [
                        /*0*/let_img,
                        /*1*/mapa.dt_mapa,
                        /*2*/mapa.mapa,
                        /*3*/mapa.entrega,
                        /*4*/mapa.placa,
                        /*5*/let_btn_lanca_desp,
                        /*6*/mapa.tem_despesa,
                        /*7*/let_cod_filial
                    ];


                    let let_dado_despesas = [];
                    if(mapa.lista_desp_mapa_lanc != null){
                        mapa.lista_desp_mapa_lanc.forEach(desp => {
                            let let_btn_exclui_desp = `
                                <button type='button' name='btn_excluir_desp' style='background: transparent;padding-left: 14px;padding-right: 14px;'
                                    id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas'
                                    value='${desp.id_despesa}'>
                                    <i class="fa-solid fa-trash-can" style="color: #f46424!important;" title="Excluir Despesa" ></i>
                                </button>
                            `;
                            let let_status_importacao = 'Não Importado'
                            if (desp.importado == 1) {
                                let_status_importacao = 'Importado'
                                let_btn_exclui_desp = `
                                    <button type='button' name='btn_excluir_desp' id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas' style='border: none;padding-left: 38px;'
                                        value='${desp.id_despesa}' disabled="disabled" title="Bloqueado">
                                        <i class="fa-solid fa-ban" style="color: #f46424!important;" title="Bloqueado"></i>
                                    </button>
                                `;
                            }
                            if (desp.despesa == 1) {
                                let_despesa = 'Serviço'
                            }
                            if (desp.tipo_descarga == 1) {
                                let_tipo_descarga = 'Por Entrega'
                            } else if (desp.tipo_descarga == 2) {
                                let_tipo_descarga = 'Por Paleta'
                            } else if (desp.tipo_descarga == 3) {
                                let_tipo_descarga = 'Por Caixa'
                            }

                            let let_btn_abre_comp = `
                                    <button type='button' name='btn_visualiza_comprovante'
                                            id='btn_visualiza_comprovante'
                                            class='btn btn-rounded btn-space'
                                            value='${desp.comprovante}'>
                                        <i class="fa-solid fa-file-pdf fa-2xl" style="color: rgb(25,107,152);"></i>
                                    </button>
                                `;


                            let let_desp = [
                                /*0*/let_img,
                                /*1*/desp.cod_cliente,
                                /*2*/let_tipo_descarga,
                                /*3*/desp.quantidade,
                                /*4*/desp.valor_unit,
                                /*5*/let_despesa,
                                /*6*/desp.data_lancamento,
                                /*7*/let_btn_abre_comp,
                                /*8*/let_status_importacao,
                                /*9*/desp.un_venda,
                                /*10*/let_btn_exclui_desp
                            ]
                            let_dado_despesas.push(let_desp)
                        });
                    }

                    let_dado_lancado.push(let_dado_despesas);
                    let_lista_dados_tab_mapas_lanc.push(let_dado_lancado);
                    let_count_lanc+=1;
                });
                $('#tab_mapas_clientes_lancado').DataTable( {
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
                    "dom": 'frtip',
                    "buttons": [],
                    "searching": true,
                    "data":let_lista_dados_tab_mapas_lanc,
                    "columns": [
                        { title: "" },
                        { title: "Data da viagem" },
                        { title: "Mapa" },
                        { title: "Entrega" },
                        { title: "Placa" },
                        { title: "Despesa" },
                        { title: "Despesa Lançada" },
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [1,2,3,4,5,6]},
                        {"className": "dt-left", "targets": [0]},
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
                    }
              });
              $("#tab_mapas_clientes_lancado").DataTable().columns.adjust().draw();
              loader_carrega_despesa_2art.style.display = "none";
            },
            error: function (request, status, error) {
            loader_carrega_despesa_2art.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            },
            complete: function(){
                $(".cl_btn_abre_modal_desp").prop('disabled', false);
                $(".cl_btn_abre_modal_desp_emp").prop('disabled', false);
                $(".cl_btn_abre_modal_desp_lancadas").prop('disabled', false);
                $("#btn_adc_mapa_empurrada").prop('disabled', false);
                $("#btn_adc_mapa_rota_lancado").prop('disabled', false);
            }
        });
    }
}


function povoa_tab_cliente_vincul_mapa(origem, lista_despesas){
    let let_dado_despesas = [];
    if(origem == 'formatado'){
        let_dado_despesas = lista_despesas;
    } else {
        /*Atualiza tabela despesas*/
        let let_img = `<i class="fa-solid fa-caret-right icon-color-e"></i>`;
        if(lista_despesas != null){
            lista_despesas.forEach(desp => {
                let let_status_importacao = ``;
                let let_btn_exclui_desp = ``;
                if (desp.importado == 1) {
                    let_status_importacao = 'Importado';
                    let_btn_exclui_desp = `
                        <i class="fa-solid fa-solid fa-ban" style="color: #f46424!important;" title="Bloqueado" ></i>
                    `;
                } else {
                    let_status_importacao += 'Não Importado';
                    let_btn_exclui_desp += `
                        <button type='button' name='btn_excluir_desp' style='background: transparent;padding-left: 14px;padding-right: 14px;'
                            id='btn_excluir_desp' class='mr-2 btn cl_btn_cad_contas'
                            value='${desp.id_despesa}'>
                            <i class="fa-solid fa-trash-can" style="color: #f46424!important;" title="Excluir Despesa" ></i>
                        </button>
                    `;
                }

                if (desp.despesa == 1) {
                    let_despesa = 'Serviço'
                }
                if (desp.tipo_descarga == 1) {
                    let_tipo_descarga = 'Por Entrega'
                } else if (desp.tipo_descarga == 2) {
                    let_tipo_descarga = 'Por Paleta'
                } else if (desp.tipo_descarga == 3) {
                    let_tipo_descarga = 'Por Caixa'
                }


                let let_btn_abre_comp = `
                        <button type='button' name='btn_visualiza_comprovante'
                                id='btn_visualiza_comprovante'
                                class='btn btn-rounded btn-space'
                                value='${desp.comprovante}'>
                            <i class="fa-solid fa-file-pdf fa-2xl" style="color: rgb(25,107,152);"></i>
                        </button>
                    `;


                let let_desp = [
                    /*0*/let_img,
                    /*1*/desp.cod_cliente,
                    /*2*/let_tipo_descarga,
                    /*3*/desp.quantidade,
                    /*4*/desp.valor_unit,
                    /*5*/let_despesa,
                    /*6*/desp.data_lancamento,
                    /*7*/let_btn_abre_comp,
                    /*8*/let_status_importacao,
                    /*9*/desp.un_venda,
                    /*10*/let_btn_exclui_desp
                ]
                let_dado_despesas.push(let_desp)
            });
        }
    }
    $('#tab_mapas_clientes_vinculados').DataTable( {
        "bJQueryUI": true,
        "destroy": true,
        "fixedHeader": true,
        "scrollY": "50vh",
        "scrollX": false,
        "scrollCollapse": true,
        "paging": false,
        "searching": true,
        "dom": 'frtip',
        "data":let_dado_despesas,
        "columns": [
            { title: "" },
            { title: "Cód Cliente" },
            { title: "Tipo de descarga" },
            { title: "Quantidade" },
            { title: "Valor Unit" },
            { title: "Despesa Lançada" },
            { title: "Lançamento" },
            { title: "Comprovante" },
            { title: "Importado" },
            { title: "UN Venda" },
            { title: "Excluir" },
        ],
        "columnDefs": [
            {"className": "dt-center", "targets": [1,2,3,4,5,6,7,8,9,10] },
            {"className": "dt-left", "targets": [0]},
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
        }
    });

}

function limpa_campos(){
    $("#un_venda").val('');
    $("#cod_promax_cliente").val('0');
    $("#cod_promax_cliente").selectpicker('refresh');
    $("#qntd_carga").val('');
    $("#val_unit").val('');
    $("#tipo_descarga").val('0');
    $("#tipo_descarga").selectpicker('refresh');
    $("#fl_comp_pagamento").val('');
}

function limpa_campos_cadastro_cli(){
    $("#cliente").val('');
    $("#nome_cliente").val('');
}

function limpa_todos_campos(){
    $("#in_data_mapa").val('');
    $("#in_mapa").val('');
    $("#un_venda").val('');
    $("#in_placa").val('');
    $("#cod_cli_promax").val('');
    $("#qntd_carga").val('');
    $("#val_unit").val('');
    $("#fl_comp_pagamento").val('');
    $("#tipo_descarga").val('0');
    $("#tipo_descarga").selectpicker('refresh');
    $("#in_entrega").val('');
    $("#cliente").val('');
    $("#nome_cliente").val('');
    $("#in_entrega").selectpicker('refresh');
    $("#cod_promax_cliente").val('0');
    $("#cod_promax_cliente").selectpicker('refresh');
}
