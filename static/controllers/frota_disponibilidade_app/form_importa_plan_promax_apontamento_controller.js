

var dataAtual = new Date();
var diaAtual = dataAtual.getDate();
var mesAtual = dataAtual.getMonth()+1;
var anoAtual = dataAtual.getFullYear();

var data_periodo_mes_ano = mesAtual+"/"+anoAtual;

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

let loader_imp_plan_promax = document.getElementById("loader_imp_plan_promax");


$(document).on('change', 'input', function(){
    var nameInput = $(this).attr('name');
	var idInput = $(this).attr('id');
    var valueInput = $(this).val();

    if ( nameInput == 'campoArquivoImpArqDispFrota') {

        if (valueInput == "" ||  valueInput == null)  {
            $("#btnImportaArquivoDispFrotaRota").prop("disabled", true);
            $("#btnImportaArquivoDispFrotaEmp").prop("disabled", true);
        } else {
            $("#btnImportaArquivoDispFrotaRota").prop("disabled", false);
            $("#btnImportaArquivoDispFrotaEmp").prop("disabled", false);
            $("#btnNovoImportaArquivoDispFrota").prop("disabled", false);
            $(this).prop("disabled", true);
		}
    }
});


$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();

	if (nomeDoButton == "btnImportaArquivoDispFrotaRota") {
	    $(this).prop("disabled", true);
	    //$("#btnImportaArquivoDispFrotaEmp").prop("disabled", true);
	    $("#campoArquivoImpArqDispFrota").prop("disabled", true);
        var formData = new FormData();
        formData.append("file", $('input[type=file]')[0].files[0]);
        loader_imp_plan_promax.style.display = "flex";
        $.ajax({
			  type: 'POST',
			  enctype: "multipart/form-data; charset=utf-8",
			  url: "/frota_disponibilidade_app/importa_arquivo_apontamento_promax",
              data: formData,
			  dataType: 'json',
			  processData: false,
			  contentType: false,
			  cache: false,
			  success: function(dados){
			    if ( dados.lista_apontamentos_promax.length > 0) {
			        if (dados.lista_apontamentos_promax[0].data == null ) {
                        $.gritter.add({
                            title: 'Atenção!',
                            text: dados.msg,
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                        $("#divConteudoImportadoDispFrota").html("");
                        $("#divConteudoImportadoDispFrota").html(dados.lista_apontamentos_promax[0].status_leitura_importacao);
                    } else {
                        var lista_lanc_apont_promax = [];
                        for (var i = 0; i < dados.lista_apontamentos_promax.length; i++) {
                            var varImgStatusImpRegistro = '';
                            if (dados.lista_apontamentos_promax[i].status_leitura_importacao == 'I'){
                                varImgStatusImpRegistro = "<i class='fa-solid fa-check' style='color: #32CD32;' title='Importado!'></i>";
                            } else if (dados.lista_apontamentos_promax[i].status_leitura_importacao == 'A'){
                                varImgStatusImpRegistro = "<i class='fa-solid fa-arrows-rotate' style='color: #008B8B;' title='Atualizado!'></i>";
                            } else {
                                varImgStatusImpRegistro = "<i class='fa-light fa-triangle-exclamation' style='color: #FFD700;' title='"+dados.lista_apontamentos_promax[i].status_leitura_importacao+"'></i>";
                            }

                            var registro_lanc = [
                                "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                                dados.lista_apontamentos_promax[i].data,
                                dados.lista_apontamentos_promax[i].placa,
                                dados.lista_apontamentos_promax[i].status,
                                dados.lista_apontamentos_promax[i].num_os,
                                dados.lista_apontamentos_promax[i].justificativa,
                                dados.lista_apontamentos_promax[i].sigla,
                                dados.lista_apontamentos_promax[i].grupo_disponibilidade,
                                dados.lista_apontamentos_promax[i].projeto,
                                varImgStatusImpRegistro
                            ];
                            lista_lanc_apont_promax.push(registro_lanc);
                        }
                        var varIndicaDadosTab = $("#hd_indica_conteudo_na_tabela").val();
                        if (varIndicaDadosTab == 1 ) {
                            var varTable =
                                `<table id="tabConteudoArquivoImportadoApontPromax"  class="display"  style="width:100%">
                                </table>`;
                            //$("#divConteudoImportadoDispFrota").html("");
                            //$("#divConteudoImportadoDispFrota").html(varTable);
                            //$("#tabConteudoArquivoImportadoApontPromax").DataTable().clear().draw();
                            //$("#tabConteudoArquivoImportadoApontPromax").DataTable().clear();
                        }
                        $("#tabConteudoArquivoImportadoApontPromax").DataTable().clear();
                        $('#tabConteudoArquivoImportadoApontPromax').DataTable( {
                            "bJQueryUI": true,
                            "destroy": true,
                            "fixedHeader": true,
                            "scrollY": "770px",
                            "scrollX": true,
                            "scrollCollapse": true,
                            "paging": true,
                            "pageLength": 7,
                            "dom": 'Bfrtip',
                            "searching": true,
                            "buttons": [
                                'copyHtml5'
                            ],
                            "data":lista_lanc_apont_promax,
                                "columns": [
                                        { title: "" },
                                        { title: "Data" },
                                        { title: "Placa" },
                                        { title: "Status" },
                                        { title: "Nº OS" },
                                        { title: "Justificativa" },
                                        { title: "Sigla" },
                                        { title: "Grupo Insdispobilidade" },
                                        { title: "Projeto" },
                                        { title: "Importado ?" }
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
                        $("#hd_indica_conteudo_na_tabela").val(1);
                        loader_imp_plan_promax.style.display = "none";
                        $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                    }

			    } else {
                    loader_imp_plan_promax.style.display = "none";
			        $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
			        $("#hd_indica_conteudo_na_tabela").val(0);
			    }
			  },
			  error: function (request, status, error) {
			    loader_imp_plan_promax.style.display = "none";
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
	else if (nomeDoButton == "btnNovoImportaArquivoDispFrota") {
	    $("#btnImportaArquivoDispFrotaRota").prop("disabled", true);
        $("#btnImportaArquivoDispFrotaEmp").prop("disabled", true);
        $("#btnNovoImportaArquivoDispFrota").prop("disabled", true);
        $("#campoArquivoImpArqDispFrota").val(null);
        $("#campoArquivoImpArqDispFrota").prop("disabled", false);

        $("#divMsgFormImpArqDispFrota").html("");
        var varIndicaDadosTab = $("#hd_indica_conteudo_na_tabela").val();
        if (varIndicaDadosTab == 1 ) {
            var varTable =
                `<table id="tabConteudoArquivoImportadoApontPromax"  class="display"  style="width:100%">
                </table>`;
            $("#divConteudoImportadoDispFrota").html("");
            $("#divConteudoImportadoDispFrota").html(varTable);
            $("#hd_indica_conteudo_na_tabela").val(0);
        }

	} else if (nomeDoButton == "btnModalCadastroSiglaFormDispFrota") {
	    povoa_tabela_siglas_disp_frota();
	    $("#modalCadastroSiglaDispFrota").show();
	} else if (nomeDoButton == "fechaModalCadastroSiglaDispFrota") {
	    $("#modalCadastroSiglaDispFrota").hide();
	} else if (nomeDoButton == "btnModalCadastroGrupoFormDispFrota") {
	    povoa_tabela_grupos_indisp_disp_frota();
	    $("#modalCadastroGrupoDispFrota").show();
	} else if (nomeDoButton == "fechaModalCadastroGrupoDispFrota") {
	    $("#modalCadastroGrupoDispFrota").hide();
	} else if (nomeDoButton == "btnConfirmaCadSiglaDispFrota") {
	    var varSigla = $("#textFieldSiglaDispFrota").val();
	    var varDescsigla = $("#textFieldDescSiglaDispFrota").val();

	    $.ajax({
	        type: 'POST',
	        url: '/frota_disponibilidade_app/salva_reg_sigla_disp_frota',
	        data: {
	            'sigla'         :   varSigla,
	            'desc_sigla'    :   varDescsigla
	        },
	        success: function(data) {
	            $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

	            povoa_tabela_siglas_disp_frota();

	            $("#textFieldSiglaDispFrota").val("");
	            $("#textFieldDescSiglaDispFrota").val("");
	            $("#textFieldSiglaDispFrota").focus();


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
	} else if (nomeDoButton == "btnExcluiCadSiglaDispFrota") {
	    var varCodRegSigla = valButton;
	    $.ajax({
	        type: 'DELETE',
	        url: '/frota_disponibilidade_app/exclui_reg_sigla_disp_frota/'+varCodRegSigla,
	        success: function(data) {
	            $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

	            povoa_tabela_siglas_disp_frota();
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
	} else if (nomeDoButton == "btnConfirmaCadGrupoDispFrota") {
	    var varDescGrupo = $("#textFieldDescGrupoDispFrota").val();

	    $.ajax({
	        type: 'POST',
	        url: '/frota_disponibilidade_app/salva_reg_grupo_disp_frota',
	        data: {
	            'desc_grupo'    :   varDescGrupo
	        },
	        success: function(data) {
	            $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

	            povoa_tabela_grupos_indisp_disp_frota();

	            $("#textFieldDescGrupoDispFrota").val("");
	            $("#textFieldDescGrupoDispFrota").focus();


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
	} else if (nomeDoButton == "btnExcluiCadGrupoDispFrota") {
	    var varCodRegGrupo = valButton;
	    $.ajax({
	        type: 'DELETE',
	        url: '/frota_disponibilidade_app/exclui_reg_grupo_disp_frota/'+varCodRegGrupo,
	        success: function(data) {
	            $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

	            povoa_tabela_grupos_indisp_disp_frota();
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
	} else if (nomeDoButton == "btnModalPesquisaDadosDispFrota") {
	    $.ajax({
	        type: 'POST',
	        url: '/frota_disponibilidade_app/carrega_projetos_form_pesq_apont_promax',
	        success: function(data) {
                $("#listProjetosPesqApontPromax option").remove();
                //$("#listProjetosPesqApontPromax").append("<option value='0'> SELECIONE O PROJETO </option>");
                if(data.indica_obj_pesquisado == 'C'){
                    data.lista_projetos.forEach(proj => {
                        $("#listProjetosPesqApontPromax").append("<option value='"+proj.cod_projeto+"'>"+proj.desc_proj+"</option>");
                    });
                } else if(data.indica_obj_pesquisado == 'U'){
                    data.lista_projetos.forEach(proj => {
                        $("#listProjetosPesqApontPromax").append("<option value='"+proj.cod_projeto__cod_projeto+"'>"+proj.cod_projeto__desc_proj+"</option>");
                    });
                }
                $("#listProjetosPesqApontPromax").selectpicker('refresh');
                $("#textFieldPeriodoPesqApontPromax").val(data_periodo_mes_ano);
	        },
	        error: function(request, status, error) {
	            $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
	        }
	    });
        $("#modalPesquisaApontamentoPromaxDispFrota").show();
	} else if (nomeDoButton == "fechaModalPesquisaApontamentoPromaxDispFrota") {
	    $("#modalPesquisaApontamentoPromaxDispFrota").hide();
	} else if (nomeDoButton == "btnPesqApontPromax"){
	    var varCodProjSelecionado = $("#listProjetosPesqApontPromax").val();
        var varPeriodoSelecionado = $("#textFieldPeriodoPesqApontPromax").val();
        if(varCodProjSelecionado == '' || varCodProjSelecionado == 0) {
            $.gritter.add({
                title: 'Atenção!',
                text: "Selecione um projeto válido!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $("#hd_cod_projeto_pesq_apont_promax").val(varCodProjSelecionado);
            $("#hd_periodo_pesq_apont_promax").val(varPeriodoSelecionado);

            $("#modalPesquisaApontamentoPromaxDispFrota").hide();
            povoa_tabela_lanc_apontamentos_promax_importados(varCodProjSelecionado, varPeriodoSelecionado);
        }

	} else if (nomeDoButton == "btnModalExcluiRegLancApontPromax"){
	    $("#hiddenCodRegLancApontPromax").val(valButton);
	    $("#modalConfirmaEstornoLanApontPromax").show();
	} else if (nomeDoButton == "btnFechaModalConfirmaEstornoLanApontPromax"){
	    $("#modalConfirmaEstornoLanApontPromax").hide();
	} else if (nomeDoButton == "btnEstornaLancApontPromax"){
	    var varCodRegLancApontPromax = $("#hiddenCodRegLancApontPromax").val();
	    var varCodProjSelecionado = $("#hd_cod_projeto_pesq_apont_promax").val();
        var varPeriodoSelecionado = $("#hd_periodo_pesq_apont_promax").val();
	    $.ajax({
	        type: 'DELETE',
	        url: '/frota_disponibilidade_app/exclui_reg_lanc_apont_promax_disp_frota/'+varCodRegLancApontPromax,
	        success: function(data) {
	            $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                $("#modalConfirmaEstornoLanApontPromax").hide();
	            povoa_tabela_lanc_apontamentos_promax_importados(varCodProjSelecionado, varPeriodoSelecionado);
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
	} else if (nomeDoButton == 'btnImportaArquivoDispFrotaEmp') {
        $(this).prop("disabled", true);
        $("#btnImportaArquivoDispFrotaEmp").prop("disabled", true);
        let let_form_data = new FormData();
        let_form_data.append("file", $('input[type=file]')[0].files[0]);
        loader_imp_plan_promax.style.display = "flex";
        $.ajax({
              type: 'POST',
              enctype: "multipart/form-data; charset=utf-8",
              url: "/frota_disponibilidade_empilhadeira_app/importa_arquivo_apontamento_promax_empilhadeira",
              data: let_form_data,
              dataType: 'json',
              processData: false,
              contentType: false,
              cache: false,
              success: function(dados){
                if ( dados.lista_apontamentos_promax.length > 0) {
                    if (dados.lista_apontamentos_promax[0].data == null ) {
                        $.gritter.add({
                            title: 'Atenção!',
                            text: dados.msg,
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                        //$("#divConteudoImportadoDispFrota").html("");
                        //$("#divConteudoImportadoDispFrota").html(dados.lista_apontamentos_promax[0].status_leitura_importacao);
                    } else {
                        let let_lista_lanc_apont_promax = [];
                        for (let i = 0; i < dados.lista_apontamentos_promax.length; i++) {
                            let let_img_status_imp_registro = '';
                            if (dados.lista_apontamentos_promax[i].status_leitura_importacao == 'I'){
                                let_img_status_imp_registro = "<i class='fa-solid fa-check' style='color: #32CD32;' title='Importado!'></i>";
                            } else if (dados.lista_apontamentos_promax[i].status_leitura_importacao == 'A'){
                                let_img_status_imp_registro = "<i class='fa-solid fa-arrows-rotate' style='color: #008B8B;' title='Atualizado!'></i>";
                            } else {
                                let_img_status_imp_registro = "<i class='fa-light fa-triangle-exclamation' style='color: #FFD700;' title='"+dados.lista_apontamentos_promax[i].status_leitura_importacao+"'></i>";
                            }

                            let let_desc_turno = '';
                            if(dados.lista_apontamentos_promax[i].turno == 'M'){
                                let_desc_turno = 'Manhã';
                            } else if(dados.lista_apontamentos_promax[i].turno == 'T'){
                                let_desc_turno = 'Tade';
                            } else if(dados.lista_apontamentos_promax[i].turno == 'N'){
                                let_desc_turno = 'Noite';
                            }

                            let let_registro_lanc = [
                                `<i class="fa-solid fa-caret-right" style="color: #f46424;"></i>`,
                                dados.lista_apontamentos_promax[i].data,
                                dados.lista_apontamentos_promax[i].turno,
                                dados.lista_apontamentos_promax[i].placa,
                                dados.lista_apontamentos_promax[i].num_os,
                                dados.lista_apontamentos_promax[i].justificativa,
                                dados.lista_apontamentos_promax[i].sigla,
                                dados.lista_apontamentos_promax[i].projeto,
                                let_img_status_imp_registro
                            ];
                            let_lista_lanc_apont_promax.push(let_registro_lanc);
                        }
                        let let_indica_dados_tab = $("#hd_indica_conteudo_na_tabela").val();
                        /*if (let_indica_dados_tab == 1 ) {
                            let let_table =
                                `<table id="tab_conteudo_arquivo_importado_apont_promax"  class="display wrap w-100 cl_tab_principal_pagina"  style="width:100%">
                                </table>`;
                            $("#divConteudoImportadoDispFrota").html("");
                            $("#divConteudoImportadoDispFrota").html(let_table);
                        }*/
                        $('#tabConteudoArquivoImportadoApontPromaxEmp').DataTable( {
                            "bJQueryUI": true,
                            "destroy": true,
                            "fixedHeader": true,
                            "scrollY": "770px",
                            "scrollX": true,
                            "scrollCollapse": true,
                            "paging": true,
                            "pageLength": 7,
                            "dom": 'Bfrtip',
                            "searching": true,
                            "buttons": [
                                'copyHtml5'
                            ],
                            "data":let_lista_lanc_apont_promax,
                                "columns": [
                                        { title: "" },
                                        { title: "Data" },
                                        { title: "Turno" },
                                        { title: "Placa" },
                                        { title: "Nº OS" },
                                        { title: "Justificativa" },
                                        { title: "Sigla" },
                                        { title: "Projeto" },
                                        { title: "Importado ?" }
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
                        $("#hd_indica_conteudo_na_tabela").val(1);
                        loader_imp_plan_promax.style.display = "none";
                        $.gritter.add({
                            title: 'Atenção!',
                            text: dados.msg,
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    }

                } else {
                    loader_imp_plan_promax.style.display = "none";
                    $.gritter.add({
                        title: 'Atenção!',
                        text: 'Arquivo vazio. Verifique!',
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    $("#hd_indica_conteudo_na_tabela").val(0);
                }
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


function povoa_tabela_siglas_disp_frota(){
    loader_imp_plan_promax.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/frota_disponibilidade_app/retorna_lista_siglas_disp_frota',
        success: function(data){
            lista_siglas = [];
            data.lista_siglas.forEach(sigla => {
                var varBotaoExcluirRegistro = "<button type='button' name='btnExcluiCadSiglaDispFrota'"+
                "id='btnExcluiCadSiglaDispFrota"+sigla.cod_sigla+"' class='btn btn-rounded btn-space' "+
                "value='"+sigla.cod_sigla+"'><i class='fa-solid fa-trash' style='color: #f46424;'></i></button>";

                reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    sigla.cod_sigla,
                    sigla.desc_sigla,
                    sigla.sigla,
                    varBotaoExcluirRegistro
                ];
                lista_siglas.push(reg);
            });
            $("#tabSiglasFormDispFrota").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
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
                "data":lista_siglas,
                "columns": [
                    { title: "" },
                    { title: "Cód." },
                    { title: "Desc. Sigla" },
                    { title: "Sigla" },
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
            loader_imp_plan_promax.style.display = "none";
        },
        error: function(request, status, error){
            loader_imp_plan_promax.style.display = "none";
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

function povoa_tabela_grupos_indisp_disp_frota() {
    loader_imp_plan_promax.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/frota_disponibilidade_app/retorna_lista_grupos_disp_frota',
        success: function(data){
            lista_grupos = [];
            data.lista_grupos.forEach(grupo => {
                var varBotaoExcluirRegistro = "<button type='button' name='btnExcluiCadGrupoDispFrota'"+
                "id='btnExcluiCadGrupoDispFrota"+grupo.cod_grupo_indisponibilidade+"' class='btn btn-rounded btn-space' "+
                "value='"+grupo.cod_grupo_indisponibilidade+"'><i class='fa-solid fa-trash' style='color: #f46424;'></i></button>";

                reg = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    grupo.cod_grupo_indisponibilidade,
                    grupo.desc_grupo_indisp,
                    varBotaoExcluirRegistro
                ];
                lista_grupos.push(reg);
            });
            $("#tabGruposFormDispFrota").DataTable( {
                "bJQueryUI": true,
                "pageLength": 5,
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
                "data":lista_grupos,
                "columns": [
                    { title: "" },
                    { title: "Cód." },
                    { title: "Desc. Grupo" },
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
            loader_imp_plan_promax.style.display = "none";
        },
        error: function(request, status, error){
            loader_imp_plan_promax.style.display = "none";
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


function povoa_tabela_lanc_apontamentos_promax_importados(varCodProjSelecionado, varPeriodoSelecionado){
    loader_imp_plan_promax.style.display = "flex";
    $.ajax({
        type: 'GET',
        url: '/frota_disponibilidade_app/retorna_lanc_apontamentos_promax_importados',
        data: {
            'cod_proj'  :   varCodProjSelecionado,
            'periodo'   :   varPeriodoSelecionado
        },
        success: function(data){
            var lista_lanc_apont_promax = [];
            data.lista_apontamentos_promax_importados.forEach(reg => {
                var varBotaoExcluirRegistro = `
                    <button type="button" class="btn btn-rounded btn-space"
                        id="btnModalExcluiRegLancApontPromax${reg.cod_apontamento_promax}"
                        name="btnModalExcluiRegLancApontPromax" value="${reg.cod_apontamento_promax}"
                        title="Excluir registro">
                        <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                    </button>
                `;


                if (reg.status_lanc == 'E'){
                    varBotaoExcluirRegistro = `<i class="fa-solid fa-circle-xmark" style="color: #f46424;" title="Estornado!"></i>`;
                }

                var var_data_apont = reg.data_apontamento.split("-")[2]+"/"+
                        reg.data_apontamento.split("-")[1]+"/"+
                        reg.data_apontamento.split("-")[0];


                var registro_lanc = [
                    "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>",
                    var_data_apont,
                    reg.placa,
                    reg.status_placa,
                    reg.numero_os,
                    reg.justificativa,
                    reg.cod_sigla__sigla,
                    reg.cod_grupo_indisponibilidade__desc_grupo_indisp,
                    reg.cod_projeto__desc_proj,
                    varBotaoExcluirRegistro
                ];
                lista_lanc_apont_promax.push(registro_lanc);
            });
            //var varIndicaDadosTab = $("#hd_indica_conteudo_na_tabela").val();
            //if (varIndicaDadosTab == 1 ) {
            //    var varTable =
            //        `<table id="tab_conteudo_arquivo_importado_apont_promax"  class="display"  style="width:100%">
            //        </table>`;
            //    $("#divConteudoImportadoDispFrota").html("");
            //    $("#divConteudoImportadoDispFrota").html(varTable);
                //$("#tabConteudoArquivoImportadoApontPromax").DataTable().clear().draw();
            //}
            $("#tabConteudoArquivoImportadoApontPromax").DataTable().clear().draw();
            $('#tabConteudoArquivoImportadoApontPromax').DataTable( {
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                 ],
                "data":lista_lanc_apont_promax,
                    "columns": [
                            { title: "" },
                            { title: "Data" },
                            { title: "Placa" },
                            { title: "Status" },
                            { title: "Nº OS" },
                            { title: "Justificativa" },
                            { title: "Sigla" },
                            { title: "Grupo Insdispobilidade" },
                            { title: "Projeto" },
                            { title: "Ação" }
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
            $("#hiddenIndicaConteudoNaTabhd_indica_conteudo_na_tabelaela").val(1);
            loader_imp_plan_promax.style.display = "none";
        },
        error: function(request, status, error) {
            loader_imp_plan_promax.style.display = "none";
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