let let_lista_multas_bd = [];


$(document).on('click','button', function(){
    let let_id_btn = $(this).attr('id');
    let let_name_btn = $(this).attr('name');
    let let_value_btn = $(this).attr('value');
    
    if (let_name_btn == 'btn_pesq_placa'){
        atualiza_tab_pesquisa_multa('placa');
    }

    else if (let_name_btn == 'btn_anexa_pdf'){
        if (let_value_btn == '0'){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Cadastre a Multa antes de anexar o Documento',
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });
        }else{
            let let_frm_data = new FormData();
            let_frm_data.append("file", $('input[type=file]')[0].files[0]);
            let_frm_data.append("cod_multa", let_value_btn);
            let_frm_data.append("tipo_anexo", $("#select_anexo").val());
             $.ajax({
                type:'POST',
                enctype: "multipart/form-data; charset=utf-8",
                url: '/cco_multas_app/salva_anexo',
                data: let_frm_data,
                dataType: 'json',
                processData: false,
                contentType: false,
                cache: false,
                success: function(dados){
                    $.gritter.add({
                        title: 'Sucesso!',
                        text: dados.msg,
                        image: '/static/icons/sucess_icon.svg',
                        sticky: false,
                        time: '',
                    });
                    atualiza_tab_pesquisa_anexo(let_value_btn);

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
    }
    
    else if(let_name_btn == 'btn_excluir_multa'){
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
                atualiza_tab_pesquisa_anexo(let_cod_multa);
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

        if (let_value_btn !== 0){

            let let_indice_tabela = let_value_btn;


            $("#a_tab_pesquisa_multas").removeClass("active");
            $("#a_tab_cadastro_multas").addClass("active");
            $("#div_tab_pesq_multas").removeClass("active");
            $("#div_cad_multas").addClass("active");
            $("#btn_cadastrar_multa").val(let_lista_multas_bd[let_indice_tabela][17]);
            $("#txt_placa").val(let_lista_multas_bd[let_indice_tabela][0]);
            $("#input_auto_infracao").val(let_lista_multas_bd[let_indice_tabela][1]);
            $("#input_data_infracao").val(let_lista_multas_bd[let_indice_tabela][3]);
            $("#input_codigo_infracao").val(let_lista_multas_bd[let_indice_tabela][18]);
            $("#select_tipo_multa").val(let_lista_multas_bd[let_indice_tabela][21]);
            $("#select_tipo_multa").selectpicker('refresh');
            $("#input_nome_condutor").val(let_lista_multas_bd[let_indice_tabela][5]);
            $("#select_data_receb_multa").val(let_lista_multas_bd[let_indice_tabela][6]);
            $("#input_local_autuacao").val(let_lista_multas_bd[let_indice_tabela][7]);
            $("#select_status_multa").val(let_lista_multas_bd[let_indice_tabela][8]);
            $("#input_valor_infracao").val(let_lista_multas_bd[let_indice_tabela][11]);
            $("#input_valor_pago_infracao").val(let_lista_multas_bd[let_indice_tabela][12]);
            $("#select_data_receb_multa").val(let_lista_multas_bd[let_indice_tabela][13]);
            $("#dt_pagamento_multa").val(let_lista_multas_bd[let_indice_tabela][14]);
            $("#txt_obs").val(let_lista_multas_bd[let_indice_tabela][15]);
            $("#select_dt_cad_cco").val(let_lista_multas_bd[let_indice_tabela][16]);
            $("#input_proj").val(let_lista_multas_bd[let_indice_tabela][20]);
            $("#btn_anexa_pdf").val(let_lista_multas_bd[let_indice_tabela][17]);
            $("#input_proj").selectpicker('refresh');

            atualiza_tab_pesquisa_anexo(let_lista_multas_bd[let_indice_tabela][17]);
        }
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
                cod_cad_multa : cod_cad_multa,
            },
            success: function(data){
               $('#btn_cadastrar_multa').val(data.cod_multa);
               $('#btn_anexa_pdf').val(data.cod_multa);

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
        }

    else if(let_name_btn == 'btn_excluir_anexo'){
        let let_cod_anexo = let_value_btn;
           $.ajax({
                type: 'DELETE',
                url: '/cco_multas_app/exclui_anexo/' + let_cod_anexo,
                dataType: 'json',
                data: {
                    'cod_anexo_cco' : let_cod_anexo
                },
                success: function(data){
                    $.gritter.add({
                        title: 'Anexo Excluido com Sucesso!',
                        image: '/static/icons/sucess_icon.svg',
                        sticky: false,
                        time: '',
                    });
                    atualiza_tab_pesquisa_anexo(data.cod_multa_antt);
                    $("#div_visualizacao_anexo_conta").html("");
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
    else if (let_name_btn == 'btn_visualizar_anexo'){
        alert('Caminho do documento:', '/media/' + let_val_btn);
        let let_img_anexo_selecionado = $('<img/>');
        let_img_anexo_selecionado.attr({
            id:'img_anexo_pre_visualizado',
            name : 'img_anexo_pre_visualizado',
            src: '/media/'+let_val_btn,
            width: '430px',
            height: '440px',
            title: 'Clique na imagem para imprimir o documento'
        });   
        $("#div_visualizacao_anexo_multa")
         .html('<embed  src="/media/'+let_val_btn+'" style="width:100%; height:100%;"/>');
    }

 });

function atualiza_tab_pesquisa_anexo(cod_multa_antt){
    dados_parametros = {
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        cod_multa_antt : cod_multa_antt
    }
    $.ajax({
        type: "GET",
        url: "/cco_multas_app/pesquisa_anexo",
        data : dados_parametros,
        success: function(data) {
            let let_visualiza_tabela = data.lista_anexos_multa.map(linha => [
                linha.cod_multa_antt__placa_multa,
                linha.tipo_anexo === 'ntf' ? 'Notificação' : linha.tipo_anexo,
                `
                <button type='button'
                    id="btn_visualizar_anexo"
                    name="btn_visualizar_anexo"
                    class="btn btn-primary btn-rounded btn-visualizar_anexo"
                    value="${linha.caminho_anexo}"
                    title="Visualizar Anexo">
                    <i class="fa-solid fa-magnifying-glass-plus" style="color: #f46424;"></i>
                </button>
                ` ,
                `
                <button type='button' id="btn_excluir_anexo"
                    name="btn_excluir_anexo"
                    class="btn btn-primary btn-rounded btn_excluir_anexo"
                    value="${linha.cod_anexo_cco}"
                    title="Excluir Anexo">
                    <i class="fa-solid fa-trash-can" style="color: #f46424";></i>
                </button>
                `
            ]);

            $('#tab_anexos_conta').DataTable ({
                "bJQueryUI" : true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data": let_visualiza_tabela,
                "columns": [
                    { title: "Placa"},
                    { title: "Tipo documento"},
                    { title: "Visualizar"},
                    { title: "Excluir"},
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
        },
        error: function(request, status, error) {
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            alert("chegou até aqui")
	    }
    });
};

function atualiza_tab_pesquisa_multa (tipo_pesquisa){
    dados_parametros = ''
    if(tipo_pesquisa =='placa'){
       placa_selecionada = $("#select_placa_multa").val();
       dados_parametros = {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            placa_selecionada : placa_selecionada,
            tipo_pesquisa_multa : tipo_pesquisa
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
                /* 3 */linha.data_auto,
                /* 4 */linha.desc_multa,
                /* 5 */linha.nome_condutor,
                /* 6 */linha.data_recebe_multa,
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
                /* 19 */let_indice_registro += 1,
                /* 20 */linha.cod_projeto,
                /* 21 */linha.cod_tipo_multa,
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
                    { title: "N° Infração" },
                    { title: "Projeto" },
                    { title: "Dt. Autuação" },
                    { title: "Tipo de Multa" },
                    { title: "Condutor" },
                    { title: "Dt. Recebimento CCO" },
                    { title: "Local" },
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
    }


};

function formatar_data(data) {
    if(data){
        const partesData = data.split('-'); // Divide a data em partes (ano, mês, dia)
        const dataFormatada = `${partesData[2]}/${partesData[1]}/${partesData[0]}`; // Formato: dia/mês/ano
        return dataFormatada;
    }
    else {
        return null;
    }
};


