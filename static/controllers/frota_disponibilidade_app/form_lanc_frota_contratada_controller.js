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




$(document).on('change', 'input', function(){
    var nameInput = $(this).attr('name');
	var idInput = $(this).attr('id');
    var valueInput = $(this).val();

    if ( nameInput == 'campoArquivoFrotaContratada') {

        if (valueInput == "" ||  valueInput == null)  {
            $("#btnImportaArqFrotaContratada").prop("disabled", true);
            $("#btnNovoImportaArqFrotaContratada").prop("disabled", true);
        } else {
            $("#btnImportaArqFrotaContratada").prop("disabled", false);
            $("#btnNovoImportaArqFrotaContratada").prop("disabled", false);
            $(this).prop("disabled", true);
		}
    }
});


$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();

	if (nomeDoButton == "btnPesqLancFrotaContratada") {
	    let let_loader_frota_contratada = document.getElementById("loader_frota_contratada");
	    let_loader_frota_contratada.style.display = "flex";
	    var varProjetoSelecionado = $("#listProjetosFrotaContratada").val();
	    var varPeriodoInformado = $("#textFieldPeriodoPesqFormFrotaContratada").val();
        $.ajax({
            type: 'GET',
            url: '/frota_disponibilidade_app/retorna_lanc_data_frota_contratada',
            data: {
                'cod_projeto'   :   varProjetoSelecionado,
                'periodo'       :   varPeriodoInformado
            },
            success: function(data) {
                $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val(1);
                lista_reg = [];
                data.lista_form_lanc_frota_contrat.forEach(reg => {
                    var varData = reg.data_ref.split('-')[2] + '/'+
                        reg.data_ref.split('-')[1] + '/'+
                        reg.data_ref.split('-')[0];

                    var varDiaSemanaNum = reg.dia_semana;
                    var varDiaSemanaString = '';
                    if (varDiaSemanaNum == 1) {
                        varDiaSemanaString = 'seg';
                    } else if (varDiaSemanaNum == 2) {
                        varDiaSemanaString = 'ter';
                    } else if (varDiaSemanaNum == 3) {
                        varDiaSemanaString = 'qua';
                    } else if (varDiaSemanaNum == 4) {
                        varDiaSemanaString = 'qui';
                    } else if (varDiaSemanaNum == 5) {
                        varDiaSemanaString = 'sex';
                    } else if (varDiaSemanaNum == 6) {
                        varDiaSemanaString = 'sáb';
                    } else if (varDiaSemanaNum == 7) {
                        varDiaSemanaString = 'dom';
                    }

                    var var_desc_turno = '';
                    if (reg.turno == 'D') {
                        var_desc_turno = 'Dia';
                    } else if (reg.turno == 'M') {
                        var_desc_turno = 'Manhã(06:00 - 13:59)';
                    } else if (reg.turno == 'T') {
                        var_desc_turno = '	Tarde(14:00 - 21:59)';
                    } else if (reg.turno == 'N') {
                        var_desc_turno = 'Noite(22:00 - 05:59)';
                    }

                    var varCompTextFieldQtdFrotaAtiva =
                        `<input type="text" class="form-control" name="textFieldQtdAtivaFrotaContratada"
                            id="textFieldQtdAtivaFrotaContratada_${reg.cod_frota_contratada}"
                            autocomplete="off"
                            value="${reg.qtd_frota_contratada_ativa}"/>`;

                    var varCompTextFieldQtdFrotaParada =
                        `<input type="text" class="form-control" name="textFieldQtdParadaFrotaContratada"
                            id="textFieldQtdParadaFrotaContratada_${reg.cod_frota_contratada}"
                            autocomplete="off"
                            value="${reg.qtd_frota_contratada_parada}"/>`;


                    reg = [
                         "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>"+
                        "<input type='hidden' name='hiddenDataRefFrotaContratada' "+
                        "id='hiddenDataRefFrotaContratada_"+reg.cod_frota_contratada+"' value='"+reg.data_ref+"'>",
                        varData,
                        varDiaSemanaString,
                        var_desc_turno,
                        varCompTextFieldQtdFrotaAtiva,
                        varCompTextFieldQtdFrotaParada,
                        ''
                    ]
                    lista_reg.push(reg);
                });
                var varIndicaDadosTab = $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val();
                if (varIndicaDadosTab == 1 ) {
                    var varTable =
                        `<table id="tabLancFrotaContratada"
                            class="display wrap w-100 cl_tab_lanc_apontamento_indisp_emp"
                            style="width:100%">
                        </table>`;
                    $("#divTabelaFormLancFrotaContrat").html("");
                    $("#divTabelaFormLancFrotaContrat").html(varTable);
                }
                if (data.desc_atividade_projeto == 'Apoio'){
                    $("#tabLancFrotaContratada").DataTable({
                        "bJQueryUI": true,
                        "destroy": true,
                        "fixedHeader": true,
                        "scrollY": "770px",
                        "scrollX": true,
                        "scrollCollapse": true,
                        "paging": true,
                        "pageLength": 7,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":lista_reg,
                        "columns": [
                            { title: "" },
                            { title: "Data Ref." },
                            { title: "Dia Semana" },
                            { title: "Turno" },
                            { title: "Qtd. Frota Ativa" },
                            { title: "Qtd. Frota Contratada" },
                            { title: "" }
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
                }
                else {
                    $("#tabLancFrotaContratada").DataTable({
                        "bJQueryUI": true,
                        "destroy": true,
                        "fixedHeader": true,
                        "scrollY": "770px",
                        "scrollX": true,
                        "scrollCollapse": true,
                        "paging": true,
                        "pageLength": 7,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":lista_reg,
                        "columns": [
                            { title: "" },
                            { title: "Data Ref." },
                            { title: "Dia Semana" },
                            { title: "Turno" },
                            { title: "Qtd. Frota Ativa" },
                            { title: "Qtd. Frota Parada" },
                            { title: "" }
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
                }

                $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val(1);
                let_loader_frota_contratada.style.display = "none";
            },
            error: function(request, status, error){
                let_loader_frota_contratada.style.display = "none";
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
	else if (nomeDoButton == "btnNovoImportaArqFrotaContratada") {
	    //$("#hiddenIndicaConteudoNaTabelaFrotaContratada").val(0);
        $("#btnImportaArqFrotaContratada").prop("disabled", true);
        $(this).prop("disabled", true);
        $("#campoArquivoFrotaContratada").val(null);
        $("#campoArquivoFrotaContratada").prop("disabled", false);
        var varIndicaDadosTab = $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val();
        if (varIndicaDadosTab == 1 ) {
            var varTable =
                `<table id="tabLancFrotaContratada"  class="display"  style="width:100%">
                </table>`;
            $("#divTabelaFormLancFrotaContrat").html("");
            $("#divTabelaFormLancFrotaContrat").html(varTable);
            $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val(0);
        }

	}
	if (nomeDoButton == "btnImportaArqFrotaContratada") {
	    let let_loader_frota_contratada = document.getElementById("loader_frota_contratada");
	    let_loader_frota_contratada.style.display = "flex";
        $(this).prop("disabled", true);
	    $("#campoArquivoFrotaContratada").prop("disabled", true);
	    var formData = new FormData();
        formData.append("file", $('input[type=file]')[0].files[0]);

        $.ajax({
			  type: 'POST',
			  enctype: "multipart/form-data; charset=utf-8",
			  url: "/frota_disponibilidade_app/importa_arquivo_frota_contratada",
              data: formData,
			  dataType: 'json',
			  processData: false,
			  contentType: false,
			  cache: false,
			  success: function(dados){
			    if(dados.lista_frota_contratada.length > 0) {
			        if(dados.lista_frota_contratada[0].data == null) {
			            $.gritter.add({
                            title: 'Atenção!',
                            text: dados.msg,
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
			            $("#divTabelaFormLancFrotaContrat").html("");
			            $("#divTabelaFormLancFrotaContrat").html(dados.lista_frota_contratada[0].status_leitura_importacao);
			        }
			        else {
			            var lista_lanc_frota_contratada = [];
			            for(var i = 0; i < dados.lista_frota_contratada.length; i++) {
			                var varImgStatusImpRegistro = '';
			                if (dados.lista_frota_contratada[i].status_leitura_importacao == 'I'){
                                varImgStatusImpRegistro = "<span class='s7-check' title='Importado!'></span";
                            } else if (dados.lista_frota_contratada[i].status_leitura_importacao == 'A'){
                                varImgStatusImpRegistro = "<span class='s7-refresh' title='Atualizado!'></span";
                            } else {
                                varImgStatusImpRegistro = "<span class='s7-info' title='"+dados.lista_frota_contratada[i].status_leitura_importacao+"'></span";
                            }
                            var var_desc_turno = '';
                            if ( dados.lista_frota_contratada[i].turno == 'D') {
                                var_desc_turno = 'Dia';
                            } else if ( dados.lista_frota_contratada[i].turno == 'M') {
                                var_desc_turno = 'Manhã';
                            } else if ( dados.lista_frota_contratada[i].turno == 'T') {
                                var_desc_turno = 'Tarde';
                            } else if ( dados.lista_frota_contratada[i].turno == 'N') {
                                var_desc_turno = 'Noite';
                            }

                            var reg_frota_contratada = [
                                "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                                dados.lista_frota_contratada[i].data,
                                dados.lista_frota_contratada[i].num_sem,
                                var_desc_turno,
                                dados.lista_frota_contratada[i].qtd_ativa,
                                dados.lista_frota_contratada[i].qtd_parada,
                                dados.lista_frota_contratada[i].cod_projeto,
                                varImgStatusImpRegistro
                            ];
                            lista_lanc_frota_contratada.push(reg_frota_contratada);
			            }
			             var varIndicaDadosTab = $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val();
                        if (varIndicaDadosTab == 1 ) {
                            var varTable =
                                `<table id="tabLancFrotaContratada"
                                    class="display wrap w-100 cl_tab_lanc_apontamento_indisp_emp"
                                    style="width:100%">
                                </table>`;
                            $("#divTabelaFormLancFrotaContrat").html("");
                            $("#divTabelaFormLancFrotaContrat").html(varTable);
                        }

                        $("#tabLancFrotaContratada").DataTable( {
                            "bJQueryUI": true,
                            "destroy": true,
                            "fixedHeader": true,
                            "scrollY": "770px",
                            "scrollX": true,
                            "scrollCollapse": true,
                            "paging": true,
                            "pageLength": 7,
                            "dom": 'Bfrtip',
                            "buttons": [
                                'copyHtml5'
                            ],
                            "data":lista_lanc_frota_contratada,
                            "columns": [
                                { title: "" },
                                { title: "Data Ref." },
                                { title: "Dia Semana" },
                                { title: "Turno" },
                                { title: "Qtd. Frota Ativa" },
                                { title: "Qtd. Frota Contratada" },
                                { title: "Cód. Projeto" },
                                { title: "" }
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
                            } );


                            $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val(1);
			        }

			    } else {
			        $.gritter.add({
                        title: 'Atenção!',
                        text: "Arquivo vazio. Verifique!",
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
			        $("#hiddenIndicaConteudoNaTabelaFrotaContratada").val(0);
			    }
			    let_loader_frota_contratada.style.display = "none";
			  },
			  error: function(request, status, error) {
			    let_loader_frota_contratada.style.display = "none";
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


$(document).on('change', 'input', function(){
    var nameInput = $(this).attr('name');
	var idInput = $(this).attr('id');
    var valueInput = $(this).val();

    if ( nameInput == 'textFieldQtdAtivaFrotaContratada') {
        var codFrotaContratada = idInput.split('_')[1];
        var varProjetoSelecionado = $("#listProjetosFrotaContratada").val();
        var varQtdFrotaAtiva = valueInput;
        var varQtdFrotaParada = $("#textFieldQtdParadaFrotaContratada_" + codFrotaContratada).val();
        var varDataRef = $("#hiddenDataRefFrotaContratada_" + codFrotaContratada).val();

        $.ajax({
            type: 'POST',
            url: '/frota_disponibilidade_app/salva_atualiza_dados_lanc_frota_contratada',
            data: {
                'cod_frota_contratada'  :   codFrotaContratada,
                'cod_projeto'   :   varProjetoSelecionado,
                'periodo'       :   varDataRef,
                'qtd_ativa'     :   varQtdFrotaAtiva,
                'qtd_parada'    :   varQtdFrotaParada
            },
            success: function(data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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

    } else if ( nameInput == 'textFieldQtdParadaFrotaContratada') {
        var codFrotaContratada = idInput.split('_')[1];
        var varProjetoSelecionado = $("#listProjetosFrotaContratada").val();
        var varQtdFrotaAtiva = $("#textFieldQtdAtivaFrotaContratada_" + codFrotaContratada).val();
        var varQtdFrotaParada = valueInput;
        var varDataRef = $("#hiddenDataRefFrotaContratada_" + codFrotaContratada).val();

        $.ajax({
            type: 'POST',
            url: '/frota_disponibilidade_app/salva_atualiza_dados_lanc_frota_contratada',
            data: {
                'cod_frota_contratada'  :   codFrotaContratada,
                'cod_projeto'   :   varProjetoSelecionado,
                'periodo'       :   varDataRef,
                'qtd_ativa'     :   varQtdFrotaAtiva,
                'qtd_parada'    :   varQtdFrotaParada
            },
            success: function(data) {
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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
