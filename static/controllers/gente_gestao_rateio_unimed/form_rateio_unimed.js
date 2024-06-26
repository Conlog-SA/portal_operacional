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
}

$(document).on('change','input', function(){
	let let_nome_input = $(this).attr('name');
    let let_id_input = $(this).attr('id');
    let let_val_input = $(this).attr('value');

    if ( let_nome_input == 'fl_campo_arquivo_plan_despesas') {
        let loader_imp_2art = document.getElementById("loader_imp_plan_despesas")
        let let_frm_data = new FormData();
		let_frm_data.append("file", $('input[type=file]')[0].files[0]);
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
				let let_msg = `
				    Total Registros : ${data.qtd_total_reg}<br/>
				    Novos Mapas : ${data.qtd_reg_imp}<br/>
				    Mapas Atualizados : ${data.qtd_reg_up}
				`;
				$.gritter.add({
                    title: 'Atenção!',
                    text: let_msg,
                    image: '../../static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
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

                /*$.ajax({
                    type: 'GET',
                    url: "/gente_gestao_rateio_unimed_app/obter_filiais",
                    success: function(response){

                    }
			    });*/
			},
			error: function (request, status, error) {
			    loader_imp_2art.style.display = "none";
			    $.gritter.add({
                    title: 'Atenção!',
                    text: "Erro na importação, contate o adm.",
                    image: '../../icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
			}
		});

    }

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

    $.ajax({
        type: 'GET',
        url: '/gente_gestao_rateio_unimed_app/busca_despesas',
        data: {
            'competencia'   :   let_competencia,
            'filial'   :    let_filial,
        },
        success: function (dados) {
            let_lista_dados_rateio = [];
            let let_soma_valor = 0;
            dados.tab_rateio_despesas_busca.forEach( despesa => {
                let let_html_matricula = '';
                let let_html_editar = '';

                if (despesa['Matricula_Titular'] == '') {
                    let_html_matricula = '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal buscaColabModal" name="'+despesa['Cod_Despesa']+'_2">Buscar</button>';
                }
                else {
                    let_html_matricula = despesa['Matricula_Titular'];
                    let_html_editar = '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal editaColabModal" name="'+despesa['Cod_Despesa']+'_2">Editar</button>';
                    let_soma_valor += parseFloat(despesa['Valor']);
                }

                let let_dado_despesa = [
                    '<i class="fa-solid fa-circle-exclamation" style="color: #f46424;"></i>',
                    despesa['Competencia'].split('-')[1]+'/'+despesa['Competencia'].split('-')[0],
                    despesa['Beneficiario'],
                    ('000000'+despesa['Cpf'].split('.')[0]).slice(-11),
                    despesa['Dependencia'],
                    despesa['Titular'],
                    ('000000'+despesa['Cpf_Titular'].split('.')[0]).slice(-11),
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
            let let_valor_final = '';
            if (String(let_soma_valor).split('.').length > 1) {
                if (String(let_soma_valor).split('.')[1].length > 2) {
                    let_valor_final = String(let_soma_valor).split('.')[0]+','+String(let_soma_valor).split('.')[1].substring(0,2);
                }
                if (String(let_soma_valor).split('.')[1].length == 1) {
                    let_valor_final = String(let_soma_valor).split('.')[0]+','+String(let_soma_valor).split('.')[1].substring(0,1)+'0';
                }
            }
            else if (String(let_soma_valor).split('.').length == 1) {
                let_valor_final = String(let_soma_valor)+',00';
            }
            $('#contabilizador_valor_nf_filial_despesas').html('Valor total da Filial: <p style="font-size:25px">R$ ' + let_valor_final + '</p>');

        }
    });
});

$(document).on('click','.btn-input-calculo-rateios' , function(){
    let let_competencia = $("#input_competencia_calculo_rateio").val();
    let let_filial = $("#input_filial_calculo_rateio").val();

    $.ajax({
        type: 'GET',
        url: '/gente_gestao_rateio_unimed_app/calcula_rateio',
        data: {
            'competencia'   :   let_competencia,
            'filial'   :    let_filial,
        },
        success: function (dados) {
            let_lista_dados_rateio = [];
            let let_soma_valor = 0;
            dados.tab_rateio_despesas_busca.forEach( despesa => {
                let_soma_valor += parseFloat(despesa['valor']);
                let let_dado_despesa = [
                    despesa['desc_projeto_senior'],
                    parseFloat(despesa['valor']).toFixed(2),
                    despesa['quantidade_beneficiarios']
			    ];
			    let_lista_dados_rateio.push(let_dado_despesa);
            });
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
                        { title: "Valor" },
                        { title: "Quantidade de Beneficiários" }
                    ],
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0]}
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
            tabelaCalculaRateio.columns.adjust();
            //$('#contabilizador_valor_nf_filial_rateio')[0].innerText = 'Valor total da NF: ' + String(let_soma_valor).replace('.', ',');
            console.log(let_soma_valor);
            let let_valor_final = '';
            let let_primeiro_valor_com_ponto = '';
            if (String(let_soma_valor).split('.').length > 1) {
                if (String(let_soma_valor).split('.')[1].length > 2) {
                    let_valor_final = String(let_soma_valor).split('.')[0]+','+String(let_soma_valor).split('.')[1].substring(0,2);
                }
                if (String(let_soma_valor).split('.')[1].length == 1) {
                    let_valor_final = String(let_soma_valor).split('.')[0]+','+String(let_soma_valor).split('.')[1].substring(0,1)+'0';
                }
            }
            else if (String(let_soma_valor).split('.').length == 1) {
                let_valor_final = String(let_soma_valor)+',00';
            }
            $('#contabilizador_valor_nf_filial_rateio').html('Valor total da Filial: <p style="font-size:25px">R$ ' + let_valor_final + '</p>');
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
});

$(document).on('click','.fechaModalBuscaColabSenior' , function(){
    $('#modalBuscaColabSenior').hide();
});


