

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
	    let_loader_arq_fat.style.display = "flex";
        var formData = new FormData();
        formData.append("file", $('#campoArquivoImpArqFatTerc')[0].files[0]);
        formData.append("tipo_arq", "arq_pag_extras");

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
			    povoa_tab_pag_extras_pendentes_fat_terc(dados.lista_dic_lanc_pendentes_validado);
			    $("#sl_filial_frm_imp_arq_pag_terc option").remove();
                $("#sl_filial_frm_imp_arq_pag_terc")
                    .append("<option value='0' selected='selected'>-- Todas as filiais --</option>");
                dados.lista_filiais_pesq.forEach(fil => {
                    $("#sl_filial_frm_imp_arq_pag_terc").append("<option value='"+
                    fil.cod_filial+"'>"+fil.nome_filial+")</option>");

                });
                $("#sl_filial_frm_imp_arq_pag_terc").selectpicker('val', '0');
                $("#sl_filial_frm_imp_arq_pag_terc").selectpicker('refresh');

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
    else if (nomeDoButton == "btn_abre_modal_status_lanc_pag_extra") {
        let let_status = 2;
        let let_cabecalho_modal = '';
        let let_msg_caixa_dialogo = '';
        if(idDoButton == "btn_aprova_lanc_pag_extra"){
            let_status = 0;
            let_cabecalho_modal = 'Aprovar Lançamentos';
            let_msg_caixa_dialogo = `
                Tem certeza que deseja &nbsp;<strong> APROVAR </strong>&nbsp; o lançamento ?
            `;
        } else if (idDoButton == "btn_reprova_lanc_pag_extra"){
            let_status = 1
            let_cabecalho_modal = 'Reprovar Lançamentos';
            let_msg_caixa_dialogo = `
                Tem certeza que deseja &nbsp;<strong> REPROVAR </strong>&nbsp; o lançamento ?
            `;
        }
        $("#sp_desc_status_lanc_pag_extra_terc").html(let_cabecalho_modal);
        $("#dv_msg_status_lanc_pag_extra_terc").html(let_msg_caixa_dialogo);
        $("#hd_status_lanc_pag_extra_terc").val(let_status);
        let let_lista_cod_lanc = valButton;
        $("#btn_confirma_status_lanc_pag_extra").val(let_lista_cod_lanc);
        $("#modal_confirma_status_lanc_pag_extra_terc").show();

    }
    else if (nomeDoButton == "btn_fecha_modal_confirma_status_lanc_pag_extra_terc") {
        $("#modal_confirma_status_lanc_pag_extra_terc").hide();
    }
    else if(nomeDoButton == "btn_detalhes_lanc_pag_extra_terc"){
        let let_loader_arq_fat = document.getElementById("loader_arq_fat");
	    let_loader_arq_fat.style.display = "flex";
        let let_lista_codigos_lanc_pag_extra = valButton;
        $.ajax({
            type: 'GET',
            url:"/plan_controle_fat_2art_terc_app/lancamentos_pag_extra_terc",
            data: {
                'tipo_transacao'    :   'por_lancamento',
                'lista_codigos_lanc_pag_extra'  :   let_lista_codigos_lanc_pag_extra
              },
            success: function(dados){
                let let_lista_lanc = [];
                let let_img = `
                    <i class='fa-solid fa-caret-right' style='color: #f46424;'></i>
                `;
                dados.lista_dic_lanc_pag_extra.forEach(lan => {
                    let let_reg = [
                        let_img,
                        lan.data_pag_extra,
                        lan.placa_pag_extra,
                        lan.val_pag_extra,
                        lan.obs_pag_extra
                    ];
                    let_lista_lanc.push(let_reg);
                });
                $('#tab_detalhes_lanc_pag_extra_terc').DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    "scrollY": "630px",
                    "scrollX": true,
                    "scrollCollapse": true,
                    "paging": false,
                    "searching": true,
                    //"pageLength": 10,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "data": let_lista_lanc,
                    "columns": [
                        { title: "" },
                        { title: "Data" },
                        { title: "Placa" },
                        { title: "Valor" },
                        { title: "Observação" }
                    ],
                    "columnDefs": [
                        {"className": "dt-center", "targets": [1,2]},
                        {"className": "dt-left", "targets": [0]},
                        {"className": "dt-right", "targets": [3, 4]}
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
                $("#modal_detalhes_lanc_pag_extra_terc").show();
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
    else if (nomeDoButton == "btn_fecha_modal_detalhes_lanc_pag_extra_terc") {
        $("#modal_detalhes_lanc_pag_extra_terc").hide();
    }
    else if(nomeDoButton == 'btn_confirma_status_lanc_pag_extra'){
        let let_loader_arq_fat = document.getElementById("loader_arq_fat");
	    let_loader_arq_fat.style.display = "flex";
        let let_status = $("#hd_status_lanc_pag_extra_terc").val();
        let let_justificativa = $("#ta_justificativa_status_lanc_pag_extra_terc").val();
        let let_lista_reg_lanc_pag_extra = valButton.split('/')[0];
        let let_cod_benef = valButton.split('/')[1];
        let let_competencia = $("#dt_ref_pag_extra_terc").val();
        let let_cod_filial_pesq = $("#sl_filial_frm_imp_arq_pag_terc").val();
        let let_chk_lanc_reprovado = $("#chk_lanc_pag_extra_reprovados").prop("checked");
        if(let_status == 1 && (let_justificativa == '' || let_justificativa == null)){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Justificativa obrigatória para esta operação!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            let_loader_arq_fat.style.display = "none";

        } else {
            $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/confirma_status_lanc_pag_extra",
            data: {
                'status'    : let_status,
                'justificativa' :   let_justificativa,
                'cod_benef' :   let_cod_benef,
                'lista_reg_lanc_pag_extra'  :   let_lista_reg_lanc_pag_extra,
                'cod_filial_pesq' :   let_cod_filial_pesq,
                'chk_lanc_reprovado' : let_chk_lanc_reprovado,
                'competencia': let_competencia
              },
            success: function(dados){
                povoa_tab_pag_extras_pendentes_fat_terc(dados.lista_dic_lanc_pendentes_validado);

                $("#modal_confirma_status_lanc_pag_extra_terc").hide();
                $("#ta_justificativa_status_lanc_pag_extra_terc").val('');
                let_loader_arq_fat.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
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



    }
    else if (nomeDoButton == 'btn_pesq_lanc_pag_extra'){
        let let_loader_arq_fat = document.getElementById("loader_arq_fat");
	    let_loader_arq_fat.style.display = "flex";
	    let let_competencia = $("#dt_ref_pag_extra_terc").val();
	    let let_cod_filial_pesq = $("#sl_filial_frm_imp_arq_pag_terc").val();
        let let_chk_lanc_reprovado = $("#chk_lanc_pag_extra_reprovados").prop("checked");
        if(let_competencia == '' || let_competencia == null){
            $.gritter.add({
                title: 'Atenção!',
                text: 'Data da competência não informada',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
            let_loader_arq_fat.style.display = "none";
        } else {
            $.ajax({
            type: 'GET',
            url:"/plan_controle_fat_2art_terc_app/lancamentos_pag_extra_terc",
            data: {
                'tipo_transacao'    :   'por_filial',
                'competencia'   :   let_competencia,
                'cod_filial_pesq'    : let_cod_filial_pesq,
                'chk_lanc_reprovado' :   let_chk_lanc_reprovado
              },
            success: function(dados){
                povoa_tab_pag_extras_pendentes_fat_terc(dados.lista_dic_lanc_pendentes_validado);

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



    }
	
});

function povoa_tab_pag_extras_pendentes_fat_terc(lista_dic_lanc_pendentes_validado){
    let let_lista_lanc = [];
    let let_img = `
        <i class='fa-solid fa-caret-right' style='color: #f46424;'></i>
    `;
    lista_dic_lanc_pendentes_validado.forEach(lan => {
        let let_btn_detalhes = `
            <button type="button" class="btn btn-rounded btn-space"
                    id="btn_detalhes_lanc_pag_extra_terc"
                    name="btn_detalhes_lanc_pag_extra_terc" value="${lan.cod_lanc_pag_extra}"
                    title="Ver lançamentos">
                <i class="fa-solid fa-eye" style="color: #f46424;"></i>
            </button>
        `;

        let let_btn_aprova = `
            <button type="button" class="btn btn-rounded btn-space"
                    id="btn_aprova_lanc_pag_extra"
                    name="btn_abre_modal_status_lanc_pag_extra" value="${lan.cod_lanc_pag_extra}/${lan.cod_benef}"
                    title="Aprovar Pagamento">
                <i class="fa-solid fa-thumbs-up" style="color: #f46424;"></i>
            </button>
        `;

        let let_btn_reprova = `
            <button type="button" class="btn btn-rounded btn-space"
                    id="btn_reprova_lanc_pag_extra"
                    name="btn_abre_modal_status_lanc_pag_extra" value="${lan.cod_lanc_pag_extra}/${lan.cod_benef}"
                    title="Reprovar Pagamento">
                <i class="fa-solid fa-thumbs-down" style="color: #f46424;"></i>
            </button>
        `;
        if (lan.status == '0') {
            let_btn_aprova = `
                <i class="fa-solid fa-thumbs-up" style="color: #f46424;"></i>
            `;
            let_btn_reprova = `
                <i class="fa-solid fa-thumbs-down" style="color: #363636!important;"></i>
            `;
        } else if (lan.status == '1') {
            let_btn_aprova = `
                <i class="fa-solid fa-thumbs-up" style="color: #363636!important;"></i>
            `;
            let_btn_reprova = `
                <i class="fa-solid fa-thumbs-down" style="color: #f46424;"></i>
            `;
        }

        let let_reg = [
            let_img,
            lan.nome_filial,
            lan.doc_benef,
            lan.nome_benef,
            lan.data_ref_pagamento,
            lan.valor,
            let_btn_detalhes,
            let_btn_aprova,
            let_btn_reprova
        ];
        let_lista_lanc.push(let_reg);
    });
    $('#tab_pag_extras_pendentes_fat_terc').DataTable( {
        "bJQueryUI": true,
        "destroy": true,
        "fixedHeader": true,
        "scrollY": "630px",
        "scrollX": true,
        "scrollCollapse": true,
        "paging": false,
        "searching": true,
        //"pageLength": 10,
        "dom": 'Bfrtip',
        "buttons": [
            'copyHtml5'
        ],
        "data": let_lista_lanc,
        "columns": [
            { title: "" },
            { title: "Filial" },
            { title: "CPF/CNPJ" },
            { title: "Beneficiário" },
            { title: "Pag. Referência" },
            { title: "R$ Total" },
            { title: "Detalhes" },
            { title: "Aprovar" },
            { title: "Reprovar" }
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
}