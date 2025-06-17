

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

$(document).ready(function(){



});

$(document).on('change', 'input', function(){  
    var nameInput = $(this).attr('name');
	var idInput = $(this).attr('id');
    var valueInput = $(this).val();
    
    if ( nameInput == 'campoArquivoImpArqFatTerc') {
        var varListaProjetos = $("#listProjetosImpArqFatTerc").val();        
        if ( (valueInput == "" ||  valueInput == null) || varListaProjetos == '0' ) {
            $("#btnImportaArquivoAcresDescFatTerc").prop("disabled", true);
            $("#btnImportaArquivoPagamentosExtraFatTerc").prop("disabled", true);
            
        } else {
            $("#btnImportaArquivoAcresDescFatTerc").prop("disabled", false);
            $("#btnImportaArquivoPagamentosExtraFatTerc").prop("disabled", false);
            
		}

    }
	
});	




$(document).on('click', 'button', function(){
	var nomeDoButton = $(this).attr('name');
	var idDoButton = $(this).attr('id');
	var valButton = $(this).val();
	
	if (nomeDoButton == "btnImportaArquivoAcresDescFatTerc") {
	    let let_loader_arq_fat = document.getElementById("loader_arq_fat");
		var formData = new FormData();
        formData.append("file", $('#campoArquivoImpArqFatTerc')[0].files[0]);
        formData.append("tipo_arq", "arq_acresc_desc");
		let_loader_arq_fat.style.display = "flex";
		$.ajax({
		    type: 'POST',
			enctype: "multipart/form-data; charset=utf-8",
			url: "/plan_controle_fat_2art_terc_app/importa_arquivo_lanc_terc_financ",
            data: formData,
			dataType: 'json',
			processData: false,
			contentType: false,
			cache: false,
			success: function(dados){
			    $("#divConteudoImportadoFatTerc").html("");
			    if(dados.lista_form_lanc_tab.length > 0){
			        var varTabelaDadosImpAcresDescTerc =
                    `<table id="tabImpLanc2ArtTerc"  class="display wrap w-100 cl_tab_principal_pagina"
                        style="width:100%">
                        <thead>
                          <tr>
                            <th scope="col">Tipo Lanc.</th>
                            <th scope="col">Mapa Ocorrência</th>
                            <th scope="col">Data Ocorrência</th>
                            <th scope="col">Mapa Destino</th>
                            <th scope="col">Placa</th>
                            <th scope="col">Valor(R$) </th>
                            <th scope="col">Observação</th>
                            </tr>
                          </thead>
                         <tbody>

                          </tbody>
                        </table>`;
                    var listaDadoLancMapa = [];
                    for (var i = 0; i < dados.lista_form_lanc_tab.length; i++) {
                        var varImgStatusImpRegistro = `
                                <i class="fa-solid fa-circle-check" style="color:#7FFFD4;"
                                title="Registro importado com sucesso!"></i>

                            `;

                        var registro_lanc = [
                            varImgStatusImpRegistro + ' ' + dados.lista_form_lanc_tab[i].desc_tipo_lanc,
                            dados.lista_form_lanc_tab[i].mapa_ocorrencia,
                            dados.lista_form_lanc_tab[i].data_ocorrencia,
                            dados.lista_form_lanc_tab[i].mapa,
                            dados.lista_form_lanc_tab[i].placa,
                            dados.lista_form_lanc_tab[i].valor.toLocaleString('pt-BR'),
                            dados.lista_form_lanc_tab[i].observacao,
                            dados.lista_form_lanc_tab[i].id_lanc_banco

                        ];
                        listaDadoLancMapa.push(registro_lanc);
                    }
                    $("#divConteudoImportadoFatTerc").html(varTabelaDadosImpAcresDescTerc);
                    $('#tabImpLanc2ArtTerc').DataTable( {
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
                        "data":listaDadoLancMapa,
                            "columns": [
                                    { title: "Tipo Lanc." },
                                    { title: "Mapa Ocorrência" },
                                    { title: "Data ocorrência" },
                                    { title: "Mapa Destino" },
                                    { title: "Placa" },
                                    { title: "Valor(R$)" },
                                    { title: "Observação" }
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

                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

			    } else {
			        $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
			    }

                let_loader_arq_fat.style.display = "none";
			},
			error: function (request, status, error) {
			    let_loader_arq_fat.style.display = "none";
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
	else if (nomeDoButton == "btnImportaArquivoPagamentosExtraFatTerc") {
	    let let_loader_arq_fat = document.getElementById("loader_arq_fat");
        var formData = new FormData();
        formData.append("file", $('#campoArquivoImpArqFatTerc')[0].files[0]);
        formData.append("tipo_arq", "arq_pag_extras");
		let_loader_arq_fat.style.display = "flex";
		$.ajax({
		    type: 'POST',
			enctype: "multipart/form-data; charset=utf-8",
			url: "/plan_controle_fat_2art_terc_app/importa_arquivo_lanc_terc_financ",
            data: formData,
			dataType: 'json',
			processData: false,
			contentType: false,
			cache: false,
			success: function(dados){
			    $("#divConteudoImportadoFatTerc").html("");
			    if(dados.lista_form_pagamentos_extra_tab.length > 0){
			        var varTabelaDadosImpPagExtra =
                        `<table id="tabImpPagExtraTerc"  class="display wrap w-100 cl_tab_principal_pagina"
                            style="width:100%">
                        <thead>
                          <tr>
                            <th scope="col">Status Importação</th>
                            <th scope="col">Beneficiário</th>
                            <th scope="col">Data</th>
                            <th scope="col">Placa</th>
                            <th scope="col">Valor(R$) </th>
                            <th scope="col">Referência</th>
                            <th scope="col">Observação</th>
                            </tr>
                          </thead>
                         <tbody>

                          </tbody>
                        </table>`;
                    var listaDadosPagamentosExtra = [];
                    for (var i = 0; i < dados.lista_form_pagamentos_extra_tab.length; i++) {

                        var varImgStatusImpRegistro = '';
                        if (dados.lista_form_pagamentos_extra_tab[i].status_importacao == 'P'){
                            varImgStatusImpRegistro = `
                                <i class="fa-regular fa-triangle-exclamation" style="color:#FFFF00;"
                                title="Erro ao importar registro !"></i>
                            `;
                        } else if (dados.lista_form_pagamentos_extra_tab[i].status_importacao == 'I'){
                            varImgStatusImpRegistro = `
                                <i class="fa-solid fa-circle-check" style="color:#7FFFD4;"
                                title="Registro importado com sucesso!"></i>
                            `;
                        }

                        var var_nome_beneficiario = dados.lista_form_pagamentos_extra_tab[i].nome_benef;
                        if (var_nome_beneficiario == 'Cadastro não encontrado'){
                            var_nome_beneficiario = "<span style='background:#fa6163;color:#ffffff;'>"+
                                var_nome_beneficiario+"</span>";
                        }

                        var registro_pag = [
                            varImgStatusImpRegistro,
                            var_nome_beneficiario,
                            dados.lista_form_pagamentos_extra_tab[i].data,
                            dados.lista_form_pagamentos_extra_tab[i].placa,
                            dados.lista_form_pagamentos_extra_tab[i].valor.toLocaleString('pt-BR'),
                            dados.lista_form_pagamentos_extra_tab[i].periodo_ref,
                            dados.lista_form_pagamentos_extra_tab[i].observacao,
                            dados.lista_form_pagamentos_extra_tab[i].id_lanc_banco

                        ];
                        listaDadosPagamentosExtra.push(registro_pag);
                    }
                    $("#divConteudoImportadoFatTerc").html(varTabelaDadosImpPagExtra);
                    $('#tabImpPagExtraTerc').DataTable( {
                        "bJQueryUI": true,
                        "pageLength": 7,
                        "destroy": true,
                        "dom": 'Bfrtip',
                        "buttons": [
                            'copyHtml5'
                        ],
                        "data":listaDadosPagamentosExtra,
                            "columns": [
                                    { title: "Status Importação" },
                                    { title: "Beneficiário" },
                                    { title: "Data" },
                                    { title: "Placa" },
                                    { title: "Valor(R$)" },
                                    { title: "Referência" },
                                    { title: "Observação" }
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

                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });


			    } else {
			        $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

			    }

                let_loader_arq_fat.style.display = "none";

                  
			},
			error: function (request, status, error) {
			    let_loader_arq_fat.style.display = "none";
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