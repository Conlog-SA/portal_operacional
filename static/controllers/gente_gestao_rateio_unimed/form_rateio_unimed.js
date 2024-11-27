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

{
    tabelaRateioUnimed = null;
    tabelaConsultaDespesas = null;
    tabelaCalculaRateio = null;
    tabelaHistoricoImportacao = null;
    tabelaCadastroExcecao = null;
}

$(document).on('click','.btn-realiza-importacao' , function(){
    let let_id_input = $('#fl_campo_arquivo_plan_despesas').attr('id');
    let let_val_input = $('#fl_campo_arquivo_plan_despesas').attr('value');
    let let_val_plano = $('#input_importacao_plano').val();

    let loader_imp_2art = document.getElementById("loader_imp_plan_despesas")
    let let_frm_data = new FormData();
    let_frm_data.append("file", $('input[type=file]')[0].files[0]);
    let_frm_data.append("cod_plano", let_val_plano);
    loader_imp_2art.style.display = "flex";
    $.ajax({
        type: 'POST',
        enctype: "multipart/form-data; charset=utf-8",
        url: "/gente_gestao_rateio_unimed_app/rateio_unimed",
        data: let_frm_data,
        dataType: 'json',
        processData: false,
        contentType: false,
        cache: false,
        success: function(data){
            let let_lista_dados_rateio = [];
            data.tab_rateio_despesas_nao_importadas.forEach( despesa => {
                let let_dado_despesa = [
                    '<i class="fa-solid fa-circle-exclamation" style="color: #f46424;"></i>',
                    despesa.competencia.split('-')[1]+'/'+despesa.competencia.split('-')[0],
                    despesa.beneficiario.replaceAll("_", " "),
                    ('000000'+despesa.cpf.split('.')[0]).slice(-11),
                    despesa.dependencia,
                    despesa.titular.replaceAll("_", " "),
                    ('000000'+despesa.cpf_titular.split('.')[0]).slice(-11),
                    despesa.desc_despesa.replaceAll("_", " "),
                    despesa.valor,
                    '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal buscaColabModal" name="'+despesa.cod_despesa+'_1">Buscar</button>',
                    '',
                    '',
                    '',
                    ''
                ];
                let_lista_dados_rateio.push(let_dado_despesa);
            });

            tabelaRateioUnimed = $('#tab_rateio_despesas_erros').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 7,
                "autoWidth": false,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_dados_rateio,
                "columns": [
                    { title: "" },
                    { title: "Competência" },
                    { title: "Beneficiário" },
                    { title: "CPF Beneficiário" },
                    { title: "Tipo Dependência" },
                    { title: "Titular" },
                    { title: "CPF Titular" },
                    { title: "Despesa" },
                    { title: "Valor" },
                    { title: "Matricula Titular" },
                    { title: "Nome Tit. Senior" },
                    { title: "Filial" },
                    { title: "Projeto" },
                    { title: "Editar" }
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

            loader_imp_2art.style.display = "none";
            tabelaRateioUnimed.columns.adjust();

            $('#input_filial option').remove();
            $('#input_filial_calculo_rateio option').remove();

            data.lista_filiais.forEach( filial => {
                $('#input_filial').append('<option value="'+filial.cod_filial_senior+'">'+filial.desc_filial_senior+'</option>');
                $('#input_filial_calculo_rateio').append('<option value="'+filial.cod_filial_senior+'">'+filial.desc_filial_senior+'</option>');
            });

            $('#input_filial').selectpicker('refresh');
            $('#input_filial_calculo_rateio').selectpicker('refresh');

            $('#fl_campo_arquivo_plan_despesas').val('');

            /*$.ajax({
                type: 'GET',
                url: "/gente_gestao_rateio_unimed_app/obter_filiais",
                success: function(response){

                }
            });*/
        },
        error: function (xhr, status, error) {
             $.gritter.add({
                title: 'Erro!',
                text: xhr.responseText,
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            loader_imp_2art.style.display = "none";
            $('#fl_campo_arquivo_plan_despesas').val('');
        }
    });

});

$(document).on('click','.buscaColabModal, .editaColabModal' , function(){

    $("#textFieldMatricColab").val("");
    $("#nomeTitularSenior").val("");
    $("#filialTitularSenior").val("");
    $("#projetoTitularSenior").val("");
    $("#btnSalvaColabSenior").val($(this).attr('name'));

    $("#modalBuscaColabSenior").show();

});

$(document).on('click','.consultaMatriculaColab' , function(){
    let let_matricula_colab = $("#textFieldMatricColab").val();
    if (let_matricula_colab == '') {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Preencha a matricula!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else if(isNaN(let_matricula_colab)) {
         $.gritter.add({
            title: 'Atenção!',
            text: 'Insira uma matricula válida (apenas números)!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        $.ajax({
            type: 'GET',
            url: '/gente_gestao_rateio_unimed_app/preenche_colab',
            data: {
                'matricula'   :   let_matricula_colab,
            },
            dataType: 'json',
            success: function (dados) {
                $("#nomeTitularSenior").val(dados.nome_titular_senior);
                $("#filialTitularSenior").val(dados.nom_filial_colab);
                $("#projetoTitularSenior").val(dados.nom_projeto_colab);

                let novo_nome_btn = $("#btnSalvaColabSenior").val() + '_' + dados.cod_filial_colab + '_' + dados.cod_projeto_colab;
                $("#btnSalvaColabSenior").val(novo_nome_btn);
            }
        });
    }
});

$(document).on('click','.btnSalvaColabSenior' , function(){
    let arr_split = $("#btnSalvaColabSenior").val().split('_');
    let let_cod_despesa = arr_split[0];
    let let_matricula_colab = $("#textFieldMatricColab").val();
    let let_nome_titular = $("#nomeTitularSenior").val();
    let let_cod_filial = arr_split[2];
    let let_desc_filial = $("#filialTitularSenior").val();
    let let_cod_projeto = arr_split[3];
    let let_desc_projeto = $("#projetoTitularSenior").val();
    $.ajax({
        type: 'POST',
        url: '/gente_gestao_rateio_unimed_app/preenche_colab',
        data: {
            'matricula'   :   let_matricula_colab,
            'nome_titular'   :   let_nome_titular,
            'cod_filial'   :   let_cod_filial,
            'desc_filial'   :   let_desc_filial,
            'cod_projeto'   :   let_cod_projeto,
            'desc_projeto'   :   let_desc_projeto,
            'cod_despesa'   :   let_cod_despesa,
        },
        success: function (dados) {
            $('#modalBuscaColabSenior').hide();
            html_nome_titular = let_nome_titular;
            $('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(10).html(html_nome_titular);
            html_filial = let_desc_filial;
            $('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(11).html(html_filial);
            html_projeto = let_desc_projeto;
            $('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(12).html(html_projeto);
            html_editar = '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal editaColabModal" name="'+let_cod_despesa+'">Editar</button>'
            $('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(13).html(html_editar);
            html_matricula = let_matricula_colab;
            $('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(9).html(html_matricula);

            if (arr_split[1] == '1') {
                try {
                    tabelaRateioUnimed.row($('button[name^="'+let_cod_despesa+'"]').parent().parent()).remove().draw();
                    tabelaConsultaDespesas.clear().draw();
                } catch { };
            }
            if (arr_split[1] == '2') {
                try {
                    console.log($('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(11).html());
                    console.log($('#input_filial option:selected').text());
                    if ($('button[name^="'+let_cod_despesa+'"]').parent().parent().find('td').eq(11).html() != $('#input_filial option:selected').text()) {
                        tabelaConsultaDespesas.row($('button[name^="'+let_cod_despesa+'"]').parent().parent()).remove().draw();
                    }
                } catch { };
            }
        }
    });
});

$(document).on('click','.btn-input-busca-despesas' , function(){
    let let_competencia = $("#input_competencia").val();
    let let_filial = $("#input_filial").val();

    msg_erro = '';
    if (let_competencia == '') {
        msg_erro += 'Selecione uma competencia!<br>';
    }
    if (let_filial == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'GET',
            url: '/gente_gestao_rateio_unimed_app/busca_despesas',
            data: {
                'competencia'   :   let_competencia,
                'filial'   :    let_filial,
            },
            success: function (dados) {
                let_lista_dados_rateio = [];
                dados.tab_rateio_despesas_busca.forEach( despesa => {
                    let let_html_matricula = '';
                    let let_html_editar = '';

                    if (despesa['Matricula_Titular'] == '') {
                        let_html_matricula = '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal buscaColabModal" name="'+despesa['Cod_Despesa']+'_2">Buscar</button>';
                    }
                    else {
                        let_html_matricula = despesa['Matricula_Titular'];
                        let_html_editar = '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal editaColabModal" name="'+despesa['Cod_Despesa']+'_2">Editar</button>';
                    }

                    let let_dado_despesa = [
                        '<i class="fa-solid fa-circle-exclamation" style="color: #f46424;"></i>',
                        despesa['Competencia'].split('-')[1]+'/'+despesa['Competencia'].split('-')[0],
                        despesa['Beneficiario'],
                        ('000000'+despesa['Cpf'].split('.')[0]).slice(-11),
                        despesa['Dependencia'],
                        despesa['Titular'],
                        despesa['Cpf_Titular'].split('.')[0],
                        despesa['Desc_Despesa'],
                        despesa['Valor'].split('.')[0]+','+despesa['Valor'].split('.')[1].substring(0,2),
                        let_html_matricula,
                        despesa['Nome_Titular_Senior'],
                        despesa['Desc_Filial_Senior'],
                        despesa['Desc_Projeto_Senior'],
                        let_html_editar
                    ];
                    let_lista_dados_rateio.push(let_dado_despesa);
                });
                tabelaConsultaDespesas = $('#tab_rateio_despesas_consulta').DataTable( {
                        "bJQueryUI": true,
                        "destroy": true,
                        "fixedHeader": true,
                        "scrollY": "770px",
                        "scrollX": true,
                        "scrollCollapse": true,
                        "paging": true,
                        "pageLength": 7,
                        "autoWidth": false,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":let_lista_dados_rateio,
                        "columns": [
                            { title: "" },
                            { title: "Competência" },
                            { title: "Beneficiário" },
                            { title: "CPF Beneficiário" },
                            { title: "Tipo Dependência" },
                            { title: "Titular" },
                            { title: "CPF Titular" },
                            { title: "Despesa" },
                            { title: "Valor" },
                            { title: "Matricula Titular" },
                            { title: "Nome Tit. Senior" },
                            { title: "Filial" },
                            { title: "Projeto" },
                            { title: "Editar" }
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
                tabelaConsultaDespesas.columns.adjust();
                //$('#contabilizador_valor_nf_filial_despesas')[0].innerText = 'Valor total da Filial: ' + String(let_soma_valor).split('.')[0]+','+String(let_soma_valor).split('.')[1].substring(0,2);

                $('#contabilizador_valor_nf_filial_despesas').html('Valor total da Filial: <p style="font-size:25px">R$ ' + dados.valor_total_despesas_atribuidas.toFixed(2) + '</p>');

            }
        });
    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    }

});

$(document).on('click','.btn-input-calculo-rateios' , function(){
    let let_competencia = $("#input_competencia_calculo_rateio").val();
    let let_cod_filial = $("#input_filial_calculo_rateio").val();
    let let_cod_plano_saude = $("#input_plano_calculo_rateio").val();

    msg_erro = '';
    if (let_competencia == '') {
        msg_erro += 'Selecione uma competencia!<br>';
    }
    if (let_cod_filial == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_cod_plano_saude == '') {
        msg_erro += 'Selecione um plano de saúde!';
    }
    if (msg_erro == '') {

        $.ajax({
            type: 'GET',
            url: '/gente_gestao_rateio_unimed_app/calcula_rateio',
            data: {
                'competencia'   :   let_competencia,
                'cod_filial'   :    let_cod_filial,
                'cod_plano_saude':  let_cod_plano_saude
            },
            success: function (dados) {
                let_lista_dados_rateio = [];
                flag_custo_empresa_zero = false;
                dados.tab_rateio_despesas_busca.forEach( despesa => {
                    let let_dado_despesa = [
                        despesa['desc_projeto_senior'],
                        parseFloat(despesa['valor_total_empresa']).toFixed(2),
                        parseFloat(despesa['valor_total_colaborador']).toFixed(2),
                        parseFloat(despesa['custo_titulares_do_projeto_parcela_empresa']).toFixed(2),
                        parseFloat(despesa['custo_titulares_do_projeto_parcela_colaborador']).toFixed(2),
                        parseFloat(despesa['custo_dependentes_do_projeto_parcela_empresa']).toFixed(2),
                        parseFloat(despesa['custo_dependentes_do_projeto_parcela_colaborador']).toFixed(2)
                    ];
                    let_lista_dados_rateio.push(let_dado_despesa);
                    if (parseFloat(despesa['valor_total']) == 0) {
                        flag_custo_empresa_zero = true;
                    }
                });
                if (flag_custo_empresa_zero == false) {
                    ordenar = [1, 'desc'];
                }
                else {
                    ordenar = [2, 'desc'];
                }

                tabelaCalculaRateio = $('#tab_calculo_rateio').DataTable( {
                        "bJQueryUI": true,
                        "destroy": true,
                        "fixedHeader": true,
                        "scrollY": "770px",
                        "scrollX": true,
                        "scrollCollapse": true,
                        "paging": true,
                        "pageLength": 7,
                        "autoWidth": false,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":let_lista_dados_rateio,
                        "columns": [
                            { title: "Projeto" },
                            { title: "Custo Empresa" },
                            { title: "Custo Colaborador" },
                            { title: "Custo Empresa - Titular" },
                            { title: "Custo Colaborador - Titular" },
                            { title: "Custo Empresa - Dependente" },
                            { title: "Custo Colaborador - Dependente" }
                        ],
                        "columnDefs": [
                            {"className": "dt-center", "targets": [0, 1, 2, 3, 4, 5]},
                            {'targets': [1, 2], 'className': 'bolded'}
                        ],
                        'order': [ordenar],
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
                tabelaCalculaRateio.columns.adjust();
                //$('#contabilizador_valor_nf_filial_rateio')[0].innerText = 'Valor total da NF: ' + String(let_soma_valor).replace('.', ',');
                $('#contabilizador_valor_nf_filial_rateio').html('Valor total do Plano: <p style="font-size:25px">R$ ' + parseFloat(dados.custo_total).toFixed(2), + '</p>');
            },
            error: function (xhr, status, error) {
                $.gritter.add({
                        title: 'Erro!',
                        text: xhr.responseText,
                        image: '../../icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                });
            }
        });

    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    }

});

$(document).on('click','.btn-input-busca-historico' , function(){
    let let_id_colaborador = $("#input_colaborador_historico_importacao").val();

    $.ajax({
        type: 'GET',
        url: '/gente_gestao_rateio_unimed_app/historico_importacoes',
        data: {
            'id_colaborador'   :   let_id_colaborador
        },
        success: function (dados) {
            console.log(dados);
            let_lista_historico_importacao = [];
            dados.forEach( arquivo => {
                if (arquivo['id_importacao_cancelamento'].split('--')[0] == '1') {
                    str_cancelar = '<i class="fa-solid fa-circle-xmark cancelar-importacao" name="' + arquivo['id_importacao_cancelamento'].split('--')[1] + '" style="font-size:20px;color:#f46424"></i>'
                }
                else if (arquivo['id_importacao_cancelamento'].split('--')[0] == '0') {
                    str_cancelar = 'Importação cancelada!'
                }
                let let_dado_arquivo = [
                    arquivo['nome_arq_original'],
                    arquivo['plano_saude'],
                    new Date(arquivo['data']).toLocaleString("pt-BR"),
                    arquivo['qtd_registros'],
                    str_cancelar
			    ];
			    let_lista_historico_importacao.push(let_dado_arquivo);
            });
            tabelaHistoricoImportacao = $('#tab_historico_importacao').DataTable( {
				    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "770px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 7,
                    "autoWidth": false,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
			  		"data":let_lista_historico_importacao,
			  		"columns": [
			  		    { title: "Nome Arq." },
			  		    { title: "Plano" },
                        { title: "Data" },
                        { title: "Qtd. Registros" },
                        { title: "Cancelar" }
                    ],
                    "order": [[2, 'desc']],
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
            tabelaHistoricoImportacao.columns.adjust();
            //$('#contabilizador_valor_nf_filial_rateio')[0].innerText = 'Valor total da NF: ' + String(let_soma_valor).replace('.', ',');
        },
        error: function (xhr, status, error) {
            $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '../../icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
            });
        }
    });
});

$(document).on('click','.dt-paging-button' , function() {
    if ($(this).attr('aria-controls') == 'tab_rateio_despesas_consulta') {
        tabelaConsultaDespesas.columns.adjust();
        //tabelaConsultaDespesas.draw();
    }
    else if ($(this).attr('aria-controls') == 'tab_calculo_rateio'){
        tabelaCalculaRateio.columns.adjust();
        //tabelaCalculaRateio.draw();
    }
    else if ($(this).attr('aria-controls') == 'tab_historico_importacao'){
        tabelaHistoricoImportacao.columns.adjust();
        //tabelaHistoricoImportacao.draw();
    }
});
//$('#tab_historico_importacao').on('draw.dt', function() {
//    tabelaHistoricoImportacao.columns.adjust();
//);

$(document).on('click','.cancelar-importacao' , function(){
    let let_id_importacao = $(this).attr('name');

    $.ajax({
        type: 'POST',
        url: '/gente_gestao_rateio_unimed_app/historico_importacoes',
        data: {
            'id_importacao'   :   let_id_importacao
        },
        success: function (dados) {
            console.log(dados);
            $("#busca_historico").trigger('click');
            tabelaHistoricoImportacao.columns.adjust();
        },
        error: function (xhr, status, error) {
            $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '../../icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
            });
        }
    });
});

$(document).on('change','.input-colaborador-historico-importacao' , function(){
    let let_id_importacao = $(this).attr('name');
    tabelaHistoricoImportacao = $('#tab_historico_importacao').DataTable();
    tabelaHistoricoImportacao.clear().columns.adjust();
    tabelaHistoricoImportacao.draw();
});

$(document).on('shown.bs.tab','.tab-nav' , function(e) {
  let target = e.target.id;

  if (target == 'a_tab_rateio_despesas_erros') {
    tabelaRateioUnimed = $('#tab_rateio_despesas_erros').DataTable();
    tabelaRateioUnimed.clear().columns.adjust();
    tabelaRateioUnimed.draw();
  }
  else if (target == 'a_tab_rateio_despesas_importadas') {
    tabelaConsultaDespesas = $('#tab_rateio_despesas_consulta').DataTable();
    tabelaConsultaDespesas.clear().columns.adjust();
    tabelaConsultaDespesas.draw();
  }
  else if (target == 'a_tab_rateio_projetos') {
    tabelaCalculaRateio = $('#tab_calculo_rateio').DataTable();
    tabelaCalculaRateio.clear().columns.adjust();
    tabelaCalculaRateio.draw();
  }
  else if (target == 'a_tab_historico_importacao') {
    tabelaHistoricoImportacao = $('#tab_historico_importacao').DataTable();
    tabelaHistoricoImportacao.clear().columns.adjust();
    tabelaHistoricoImportacao.draw();
  }
  else if (target == 'a_tab_cadastro_excecoes') {

    $.ajax({
        type: 'GET',
        url: '/gente_gestao_rateio_unimed_app/colaboradores_excecao',
        success: function (dados) {
            let let_lista_colabs_excecao_dict = [];
            dados.forEach( col => {
                let_lista_colabs_excecao_dict.push([
                    col.cod_colab_excecao,
                    col.nome_colab_excecao,
                    col.cpf_colab_excecao,
                    col.projeto_col,
                    '<i class="fa-solid fa-lock" style="color: #f46424;font-size:24px"></i>',
                    '<i class="fa-solid fa-ban" style="color: #B90E0A;font-size:24px"></i>',
                ])
            });

            tabelaCadastroExcecao = $('#tab_excecoes_colaboradores').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "pageLength": 7,
                "autoWidth": false,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_lista_colabs_excecao_dict,
                "columns": [
                    { title: "Cód. Exceção" },
                    { title: "Nome do Colab." },
                    { title: "CPF do Colab." },
                    { title: "Projeto" },
                    { title: "Fim Vigência" },
                    { title: "Anular" },
                ],
                "order": [1, 'desc'],
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

            //tabelaCadastroExcecao = $('#tab_excecoes_colaboradores').DataTable();
            tabelaCadastroExcecao.columns.adjust();

        },
        error: function (xhr, status, error) {
            $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '../../icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
            });
        }
    });
  }
});

$(document).on('click','.fechaModalBuscaColabSenior' , function(){
    $('#modalBuscaColabSenior').hide();
});

$(document).on('click','.fechaModalCadastraExcecao' , function(){
    $('#modalAdicionaExcecao').hide();
});

$(document).on('click','.btn-input-criar-excecao' , function(){

    $("#nomeColabExcecao").val("");
    $("#cpfColabExcecao").val("");
    $("#filialColabExcecao").val("");
    $("#projetoColabExcecao").val("");

    $("#modalAdicionaExcecao").show();
});

$(document).on('change','.filial-colab-excecao' , function(){
    let let_cod_filial = $('#filialColabExcecao').val();

    $.ajax({
        type: 'GET',
        url: '/gente_gestao_rateio_unimed_app/projetos_filial',
        data: {
            'cod_filial'   :   let_cod_filial
        },
        success: function (dados) {
            $('#projetoColabExcecao').prop('disabled',false);
            $('#projetoColabExcecao option').remove();
            dados.forEach( projeto => {
                $('#projetoColabExcecao').append('<option value="'+projeto.cod_projeto+'">'+projeto.desc_proj+'</option>');
            });
            $('#projetoColabExcecao').selectpicker('refresh');
        },
        error: function (xhr, status, error) {
            $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '../../icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
            });
        }
    });
});

$(document).on('click','.btn-adiciona-excecao' , function(){
    let let_nome_colab_excecao = $('#nomeColabExcecao').val();
    let let_cpf_colab_excecao = $('#cpfColabExcecao').val();
    let let_cod_filial_colab_excecao = $('#filialColabExcecao').val();
    let let_cod_projeto_colab_excecao = $('#projetoColabExcecao').val();
    let let_competencia_inicio = $("#input_competencia_inicio_excecao").val();

    let_competencia_inicio = let_competencia_inicio.split('-')[1] + '/' + let_competencia_inicio.split('-')[0];

    msg_erro = '';
    if (let_nome_colab_excecao == '' || let_nome_colab_excecao == null) {
        msg_erro += 'Informe o nome do cadastrado!<br>';
    }
    if (let_cpf_colab_excecao == '' || let_cpf_colab_excecao == null) {
        msg_erro += 'Informe o cpf do cadastrado!<br>';
    }

    if (let_cod_filial_colab_excecao == '') {
        msg_erro += 'Selecione a filial que o colaborador deve constar!<br>';
    }
    if (let_cod_projeto_colab_excecao == '') {
        msg_erro += 'Selecione o projeto que o colaborador deve constar!<br>';
    }

    if (let_competencia_inicio == '') {
        msg_erro += 'Selecione o inicio da vigência da exceção!';
    }

    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/gente_gestao_rateio_unimed_app/colaboradores_excecao',
            data: {
                'nome_colab_excecao'   :   let_nome_colab_excecao,
                'cpf_colab_excecao'   :   let_cpf_colab_excecao,
                'cod_projeto_colab_excecao'   :   let_cod_projeto_colab_excecao,
                'cod_filial_colab_excecao' : let_cod_filial_colab_excecao,
                'competencia_inicio_vigencia' :   let_competencia_inicio,
            },
            success: function (dados) {
                $('#modalAdicionaExcecao').hide();
                $('#projetoColabExcecao').prop('disabled',false);
                $('#projetoColabExcecao option').remove();
                dados.forEach( projeto => {
                    $('#projetoColabExcecao').append('<option value="'+projeto.cod_projeto+'">'+projeto.desc_proj+'</option>');
                });
                $('#projetoColabExcecao').selectpicker('refresh');
            },
            error: function (xhr, status, error) {
                $.gritter.add({
                        title: 'Erro!',
                        text: xhr.responseText,
                        image: '../../icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                });
            }
        });
    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });

    }


});



