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
                    let split_retorno = despesa.split(' ');
                    let let_dado_despesa = [
                        '<i class="fa-solid fa-circle-exclamation" style="color: #f46424;"></i>',
                        split_retorno[1],
                        split_retorno[4].replaceAll("_", " "),
                        ('000000'+split_retorno[6].split('.')[0]).slice(-11),
                        split_retorno[8],
                        split_retorno[10].replaceAll("_", " "),
                        ('000000'+split_retorno[12].split('.')[0]).slice(-11),
                        split_retorno[14].replaceAll("_", " "),
                        split_retorno[16],
                        '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal buscaColabModal" name="'+split_retorno[18]+'">Buscar</button>',
                        '',
                        '',
                        '',
                        ''
					];
					let_lista_dados_rateio.push(let_dado_despesa);
                });

				tabelaRateioUnimed = $('#tab_rateio_despesas_importadas').DataTable( {
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
    var var_cod_projeto = $("#listProjetosPesqCadPlacaTerc").val();
    if (var_cod_projeto == '') {
        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione um projeto !',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    } else {
        $("#textFieldMatricColab").val("");
        $("#nomeTitularSenior").val("");
        $("#filialTitularSenior").val("");
        $("#projetoTitularSenior").val("");
        $("#btnSalvaColabSenior").val($(this).attr('name'));

        $("#modalBuscaColabSenior").show();
    }

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
    let let_cod_filial = arr_split[1];
    let let_desc_filial = $("#filialTitularSenior").val();
    let let_cod_projeto = arr_split[2];
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

            tabelaRateioUnimed.columns.adjust();
        }
    });
});

$(document).on('click','.btnInputBuscaDespesas' , function(){
    let let_competencia = $("#input_competencia").val();
    let let_filial = $("#input_filial").val();

    $.ajax({
        type: 'POST',
        url: '/gente_gestao_rateio_unimed_app/busca_despesas',
        data: {
            'competencia'   :   let_competencia,
            'filial'   :    let_filial,
        },
        success: function (dados) {
            data.tab_rateio_despesas_nao_importadas.forEach( despesa => {
                let split_retorno = despesa.split(' ');
                let let_dado_despesa = [
                    '<i class="fa-solid fa-circle-exclamation" style="color: #f46424;"></i>',
                    split_retorno[1],
                    split_retorno[4].replaceAll("_", " "),
                    ('000000'+split_retorno[6].split('.')[0]).slice(-11),
                    split_retorno[8],
                    split_retorno[10].replaceAll("_", " "),
                    ('000000'+split_retorno[12].split('.')[0]).slice(-11),
                    split_retorno[14].replaceAll("_", " "),
                    split_retorno[16],
                    '<button type="button" class="btn btn-primary btn-rounded botaoPrincipal buscaColabModal" name="'+split_retorno[18]+'">Buscar</button>',
                    '',
                    '',
                    '',
                    ''
			    ];
			    let_lista_dados_rateio.push(let_dado_despesa);
            });
            $('#tab_rateio_despesas_consulta').DataTable( {
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

            tabelaRateioUnimed.columns.adjust();
        }
    });
});

$(document).on('click','.fechaModalBuscaColabSenior' , function(){
    $('#modalBuscaColabSenior').hide();
});

