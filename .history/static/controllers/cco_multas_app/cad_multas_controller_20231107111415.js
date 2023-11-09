let let_lista_multas_bd = [];

function formatarData(data) {
    if(data){
        const partesData = data.split('-'); // Divide a data em partes (ano, mês, dia)
        const dataFormatada = `${partesData[2]}/${partesData[1]}/${partesData[0]}`; // Formato: dia/mês/ano
        return dataFormatada;
    }
    else {
        return null;
    }
};


$(document).on('click','button', function(){
    let let_id_btn = $(this).attr('id');
    let let_name_btn = $(this).attr('name');
    let let_value_btn = $(this).attr('value');
    
    if (let_name_btn == 'btn_pesq_placa'){
        atualiza_tab_pesquisa_multa('placa');
    }
    if(let_name_btn == 'btn_excluir_multa'){
        let let_cod_multa = let_value_btn;
        $.ajax({
        type : 'DELETE',
        url: '/cco_multas_app/exclui_multa/' +let_cod_multa,
        dataType : "json",
        success: function(data){
            $.gritter.add({
                    title: 'Sucesso!',
                    text: data.msg,
                    image: '/static/icons/sucess_icon.svg',
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
    else if (let_name_btn == 'btn_editar_multa'){
        let let_indice_tabela = let_value_btn;

        $("#myTab a[href='#div_cad_multas']").tab("show");
        $("#txt_placa").val(let_lista_multas_bd[let_indice_tabela][0]);
        $("#input_auto_infracao").val(let_lista_multas_bd[let_indice_tabela][1]);
        $("#input_proj").val(let_lista_multas_bd[let_indice_tabela][2]);
        $("#input_data_infracao").val(let_lista_multas_bd[let_indice_tabela][3]);
        $("#select_tipo_multa").val(let_lista_multas_bd[let_indice_tabela][4]);
        $("#input_nome_condutor").val(let_lista_multas_bd[let_indice_tabela][5]);
        $("#select_data_receb_multa").val(let_lista_multas_bd[let_indice_tabela][6]);
        $("#input_local_autuacao").val(let_lista_multas_bd[let_indice_tabela][7]);
        $("#select_status_multa").val(let_lista_multas_bd[let_indice_tabela][8]);
        $("#input_valor_infracao").val(let_lista_multas_bd[let_indice_tabela][11]);data_recebe_multa
        $("#input_valor_pago_infracao").val(let_lista_multas_bd[let_indice_tabela][12]);
        $("#select_data_receb_multa").val(let_lista_multas_bd[let_indice_tabela][13]);
        $("#dt_pagamento_multa").val(let_lista_multas_bd[let_indice_tabela][14]);
        $("#txt_obs").val(let_lista_multas_bd[let_indice_tabela][15]);
        $("#select_dt_cad_cco").val(let_lista_multas_bd[let_indice_tabela][16]);
        $("#input_codigo_infracao").val(let_lista_multas_bd[let_indice_tabela][18]);

    }
    else if(let_name_btn == 'btn_cadastrar_multa'){
    // Coleta de dados da form do cadastro de equipamentos e veiculos
        placa = document.getElementById("txt_placa").value
        numero_auto = document.getElementById("input_auto_infracao").value
        cod_infracao = document.getElementById("input_codigo_infracao").value
        data_cad_cco = document.getElementById("select_dt_cad_cco").value
        tipo_multa = document.getElementById("select_tipo_multa").value
        local_auto = document.getElementById("input_local_autuacao").value
        projeto = document.getElementById("input_proj").value
        data_infracao = document.getElementById("input_data_infracao").value
        valor_infracao = document.getElementById("input_valor_infracao").value
        valor_pago = document.getElementById("input_valor_pago_infracao").value
        data_recebimento_infracao = document.getElementById("select_data_receb_multa").value
        data_pagamento_infracao = document.getElementById("dt_pagamento_multa").value
        status_multa = document.getElementById("select_status_multa").value
        obs = document.getElementById("txt_obs").value
        nome_condutor = document.getElementById("input_nome_condutor").value
        cod_cad_multa = document.getElementById("btn_cadastrar_multa").value

    }

        $.ajax({
            type: "POST",
            url:"/cco_multas_app/cadastro_multas",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                placa : placa,
                numero_auto : numero_auto,
                cod_infracao : cod_infracao,
                data_cad_cco : data_cad_cco,
                tipo_multa : tipo_multa,
                local_auto : local_auto,
                projeto : projeto,
                data_infracao : data_infracao,
                valor_infracao : valor_infracao,
                valor_pago : valor_pago,
                data_recebimento_infracao : data_recebimento_infracao,
                data_pagamento_infracao : data_pagamento_infracao,
                status_multa : status_multa,
                obs : obs,
                nome_condutor : nome_condutor,
                cod_cad_multa : cod_cad_multa
            },
            success: function(data){

                $.gritter.add({
                    title: "sucesso!",
                    text: data.msg,
                    image : '/static/icons/sucess_icon.svg',
                    sticky: false,
                    time: new Date().toLocaleTimeString(),
                });

            },
                error: function(error) {
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: new Date().toLocaleTimeString(),
                });
            }
        });
});


function atualiza_tab_pesquisa_multa (tipo_pesquisa){
    dados_parametros = ''
    if(tipo_pesquisa =='placa'){
       placa_selecionada = $("#select_placa_multa").val();
       dados_parametros = {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            placa_selecionada : placa_selecionada,
            tipo_pesquisa_multa : tipo_pesquisa
        }
    }
    $.ajax({
        type: "GET",
        url: "/cco_multas_app/pesquisa_multas",
        data: dados_parametros,
        success: function(data) {
            $("#hd_tipo_pesquisa_multa").val(tipo_pesquisa);
            //const consulta_multas = data.linhasTabela.map(linha => [
            let let_indice_registro = 0;
            let_lista_multas_bd = data.linhasTabela.map(linha => [
                /* 0 */linha.placa_multa,
                /* 1 */linha.num_auto_infracao,
                /* 2 */linha.desc_projeto,
                /* 3 */formatarData(linha.data_auto),
                /* 4 */linha.desc_multa,
                /* 5 */linha.nome_condutor,
                /* 6 */formatarData(linha.data_recebe_multa),
                /* 7 */linha.local_multa,
                /* 8 */linha.status,
                /* 9 */`
                <button type='button' id="btn_editar_multa_${let_indice_registro} "
                    name="btn_editar_multa"
                    class="btn btn-primary btn-rounded btn-editar"
                    value="${let_indice_registro}"
                    title="Editar Multa">
                    <i class="fa-solid fa-pen-to-square"></i>
                </button>
                ` ,
                /* 10 */`
                <button type='button' id="btn_excluir_multa_${linha.cod_multa_antt} "
                    name="btn_excluir_multa"
                    class="btn btn-primary btn-rounded btn-excluir"
                    value="${linha.cod_multa_antt}"
                    title="Excluir Multa">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
                `,
                /* 11 */linha.valor_pagar,
                /* 12 */linha.valor_pago,
                /* 13 */linha.data_recebe_multa,
                /* 14 */linha.data_pag_multa,
                /* 15 */linha.obs,
                /* 16 */linha.data_inclusao,
                /* 17 */linha.cod_multa_antt,
                /* 18 */linha.cod_infracao,
                /* 19 */let_indice_registro += 1
            ])

            $('#tab_multas').DataTable( {
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_multas_bd,
                "columns": [
                    { title: "Placa" },
                    { title: "N° Auto Infração" },
                    { title: "Projeto" },
                    { title: "Dt. Autuação" },
                    { title: "Tipo de Multa" },
                    { title: "Condutor" },
                    { title: "Dt. Recebimento CCO" },
                    { title: "Local de Autuação" },
                    { title: "Status" },
                    { title: "Editar" },
                    { title: "Excluir" },
                ],
                "columnDefs": [{
                    // { "width": "10%", "targets": 0 },
                    // {"className": "dt-left", "targets": [0]},
                    // {"className": "dt-left", "targets": [1]}
                }
                ],
                "oLanguage": {
                    "sProcessing":   "Processando...",
                    "sLengthMenu":   "Mostrar MENU registros",
                    "sZeroRecords":  "Não foram encontrados resultados",
                    "sInfo":         "Mostrando de START até END de TOTAL registros",
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
            $.gritter.add({
                title: 'Sucesso!',
                text: "Pesquisa realizada com Sucesso!",
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });
        },
        error: function(error) {
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
		}
	});

};
