var listaDados2ArtTerceiros = [];

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
/*
$.fn.dataTable.Api.register('sum()', function() {
    return this.flatten().reduce(function(a, b) {
        if (typeof a === 'string') {
            a = a.replace(/[^\d.-]/g, '') * 1;
        }
        if (typeof b === 'string') {
            b = b.replace(/[^\d.-]/g, '') * 1;
        }
        return a + b;
    }, 0);
});
*/



$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if (nomeDoButton == "btnPesqRelPagTerceirosProjPeriodoTipo") {
        var varCodProj = $("#listProjetosRelPagTerc").val(); 
        var varCodBenef = '0';
        var varRef = $("#textFieldPeriodoReferenciaRelPagTerc").val(); 
        var varCodPag = '0';
        var tipoOcorrencia = $("#listOcorrenciaPagamentoRelPagTerc").val();
        var varQuinzena = $("#listQuinzRelPagTerc").val();
        let let_loader_rel_pag_terc = document.getElementById("loader_rel_pag_terc");
        let_loader_rel_pag_terc.style.display = "flex";
        $.ajax({
            type: 'GET',
            url: '/plan_controle_fat_2art_terc_app/retorna_pagamentos_terceiro',
            data: {
                'cod_projeto'       :   varCodProj,
                'cod_benef'         :   varCodBenef,
                'periodo_ref'       :   varRef,
                'cod_pag'           :   varCodPag,
                'tipo_ocorr'        :   tipoOcorrencia,
                'tipo_relatorio'    :   'rel_proj_periodo_tipo',
                'quinzena'          :   varQuinzena
            },
            dataType: 'json',
            success: function (dados) {
                let rows = '';
                if (tipoOcorrencia == 'M') {
                    dados.registros_tab_pagamentos_terc.forEach(pag => {
                        var varStatusPagamento = '';
                        var varButtonEstornoPagamento = '';
                        var varButtonGerarPDF = '';
                        var varButtonGerarPDFDescAcres = '';
                        if (pag.status_pag == 'E') {
                            varStatusPagamento = '(ESTORNADO POR : '+pag.nome_usu_status+')';
                        } else {
                            if ( dados.tipo_corporativo_usuario == 'S') {
                                varButtonEstornoPagamento =
                                `<button type="button" name="btnDesfazPagamentoMapasBeneficiario"
                                    id="btnDesfazPagamentoMapasBeneficiario${pag.cod_pag}"
                                    class="btn btn-primary btn-rounded botaoPrincipal"
                                    value="${pag.cod_pag}">
                                        <i class="fa-solid fa-clock-rotate-left"></i>Estornar Pagamento
                                </button>`;
                            }
                            varButtonGerarPDF =
                                `<button type="button" name="btnGeraPDFPagMapas" id="btnGeraPDFPagMapas${pag.cod_pag}"
                                    class="btn btn-primary btn-rounded botaoPrincipal"
                                    value="${pag.cod_pag}">
                                        <i class="fa-regular fa-file-pdf"></i>PDF Pagamento
                                 </button>`;
                            if( pag.desc != '0,00' || pag.acres != '0,00') {
                                varButtonGerarPDFDescAcres = `<button type="button" name="btnGeraPDFDescAcres" id="btnGeraPDFDescAcres${pag.cod_pag}"
                                    class="btn btn-primary btn-rounded botaoPrincipal"
                                    value="${pag.cod_pag}">
                                        <i class="fa-regular fa-file-pdf"></i>PDF Desc./Acrés.
                                 </button>`;
                            }
                        }

                        rows +=
                            `<div class="d-flex justify-content-between align-items-between w-100">
                                <div id="accordion${pag.cod_pag}" class="accordion" style="width: 100%;border: 0px solid #dcdcdc;margin-left: 5px; margin-right: 0px;">
                                    <div class="card">
                                        <div id="heading${pag.cod_pag}" class="card-header" style="padding-top: 0.25rem;padding-left: 0.25rem;padding-bottom: 0.25rem;padding-right: 0.25rem;">
                                            <div class="d-flex justify-content-between align-items-between w-100">
                                                <button type="button" data-toggle="collapse" name="btnMapasPagosBeneficiario"  id="btnMapasPagosBeneficiario${pag.cod_pag}" value="${pag.cod_pag}" aria-expanded="false" aria-controls="collapsetwo2" class="btn collapsed"
                                                            style="border-top-width:0px;border-right-width:0px;border-bottom-width:0px;border-left-width:0px;padding-top: 5px;padding-right: 5px;padding-bottom: 5px;padding-left: 5px;">
                                                    <div class="d-flex justify-content-between align-items-between w-100">
                                                        <span class="icon s7-angle-right"></span>
                                                        <span style="color:#FF7575;font-size:14px">
                                                            <input type="hidden" name="hiddenNomeBeneficiarioRel" id="hiddenNomeBeneficiarioRel${pag.cod_pag}" value="${pag.doc_benef}_${pag.nome_beneficiario}">
                                                            <b>${pag.doc_benef} - ${pag.nome_beneficiario}</b>
                                                            <span style="background:#fa6163;color:#FFFFFF;">`+varStatusPagamento+`</span>
                                                            <br/>
                                                            <span style="color:#000000">
                                                                Info. Pagamento -
                                                                <b>Data: </b>${pag.data} |
                                                                <b>Serial: </b> ${pag.num_doc_pagamento}-${pag.serial_pag_proj} |
                                                                <b>Val.(R$): </b> ${pag.val_frete} |
                                                                <b>Desc.(R$): </b> ${pag.desc} |
                                                                <b>Acrés.(R$): </b> ${pag.acres} |
                                                                <b>Val. TT.(R$): </b> ${pag.val_pagar}
                                                            </span>
                                                        </span>
                                                        <input type="hidden" name="hiddenDataGeracaoPagamento" id="hiddenDataGeracaoPagamento${pag.cod_pag}" value="${pag.data}">
                                                        <input type="hidden" name="hiddenSerialPagamento" id="hiddenSerialPagamento${pag.cod_pag}" value="${pag.num_doc_pagamento}_${pag.serial_pag_proj}">
                                                    </div>
                                                </button>
                                            </div>
                                            <div class="d-flex justify-content-between align-items-between w-100 mb-4">
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;color:#ffffff;font-size:10px;background:#948c8c;padding-top: 5px;border-radius: 10px;">
                                                    &nbsp;Observação do Pagamento<br/>Data: ${pag.data}/ Ocorrência : ${pag.tipo_ocorrencia}/ ${pag.complemento}/ ${pag.obs_desc}<br/>${pag.obs_desc}&nbsp;
                                                </div>
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;">
                                                    `+varButtonEstornoPagamento+`
                                                </div>
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;">
                                                    `+varButtonGerarPDF+`
                                                </div>
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;">
                                                    `+varButtonGerarPDFDescAcres+`
                                                </div>
                                            </div>
                                            <br/>
                                        </div>
                                        <div id="collapse${pag.cod_pag}" aria-labelledby="heading${pag.cod_pag}" data-parent="#accordion${pag.cod_pag}" class="collapse">
                                            <div class="card-block" id="divMapasPagoBeneficiarioSelecionado${pag.cod_pag}" style="width: 100%;height:100%;padding-top: 5px;">


                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                    });

                }
                else if (tipoOcorrencia == 'E') {
                    dados.registros_tab_pagamentos_terc.forEach(pag => {
                        var varStatusPagamento = '';
                        var varButtonEstornoPagamento = '';
                        var varButtonGerarPDF = '';
                        var varButtonGerarPDFDescAcres = '';
                        if (pag.status_pag == 'E') {
                            varStatusPagamento = '(ESTORNADO POR : '+pag.nome_usu_status+')';
                        } else {
                            if ( dados.tipo_corporativo_usuario == 'S') {
                                varButtonEstornoPagamento =
                                `<button type="button" name="btnDesfazPagamentoMapasBeneficiario"
                                    id="btnDesfazPagamentoMapasBeneficiario${pag.cod_pag}"
                                    class="btn btn-primary btn-rounded botaoPrincipal"
                                    value="${pag.cod_pag}">
                                        <i class="fa-solid fa-clock-rotate-left"></i>Estornar Pagamento
                                 </button>`;
                            }
                            varButtonGerarPDF =
                                `<button type="button" name="btnGeraPDFPagMapas" id="btnGeraPDFPagMapas${pag.cod_pag}"
                                    class="btn btn-primary btn-rounded botaoPrincipal"
                                    value="${pag.cod_pag}">
                                        <i class="fa-regular fa-file-pdf"></i>Relatório PDF
                                </button>`;
                            
                            if( pag.desc != '0,00' || pag.acres != '0,00') {
                                varButtonGerarPDFDescAcres = `<button type="button" name="btnGeraPDFDescAcres" id="btnGeraPDFDescAcres${pag.cod_pag}"
                                    class="btn btn-primary btn-rounded botaoPrincipal"
                                    value="${pag.cod_pag}">
                                        <i class="fa-regular fa-file-pdf"></i>PDF Desc./Acrés.
                                 </button>`;
                            }
                        }

                        rows +=
                            `<div class="d-flex justify-content-between align-items-between w-100">
                                <div id="accordion${pag.cod_pag}" class="accordion" style="width: 100%;border: 0px solid #dcdcdc;margin-left: 5px; margin-right: 0px;">
                                    <div class="card">
                                        <div id="heading${pag.cod_pag}" class="card-header">
                                            <div class="d-flex justify-content-between align-items-between w-100">
                                                <button type="button" data-toggle="collapse" name="btnMapasPagosBeneficiario"  id="btnMapasPagosBeneficiario${pag.cod_pag}" value="${pag.cod_pag}" aria-expanded="false" aria-controls="collapsetwo2" class="btn collapsed"
                                                    style="border-top-width:0px;border-right-width:0px;border-bottom-width:0px;border-left-width:0px;padding-top: 5px;padding-right: 5px;padding-bottom: 5px;padding-left: 5px;">
                                                        <div class="d-flex justify-content-between align-items-between w-100">
                                                            <span class="icon s7-angle-right"></span>
                                                            <span style="color:#FF7575;font-size:14px">
                                                                <input type="hidden" name="hiddenNomeBeneficiarioRel" id="hiddenNomeBeneficiarioRel${pag.cod_pag}" value="${pag.doc_benef}_${pag.nome_beneficiario}">
                                                                ${pag.doc_benef} - ${pag.nome_beneficiario}
                                                                <span style="background:#fa6163;color:#FFFFFF">`+varStatusPagamento+`</span>
                                                                <br/>
                                                                <span style="color:#000000">
                                                                    Info. Pagamento -
                                                                    <b>Data: </b>${pag.data} |
                                                                    <b>Serial: </b> ${pag.num_doc_pagamento}-${pag.serial_pag_proj} |
                                                                    <b>Val.(R$): </b> ${pag.val_frete} |
                                                                    <b>Desc.(R$): </b> ${pag.desc} |
                                                                    <b>Acrés.(R$): </b> ${pag.acres} |
                                                                    <b>Val. TT.(R$): </b> ${pag.val_pagar}
                                                                </span>
                                                            </span>
                                                            <input type="hidden" name="hiddenDataGeracaoPagamento" id="hiddenDataGeracaoPagamento${pag.cod_pag}" value="${pag.data}">
                                                            <input type="hidden" name="hiddenSerialPagamento" id="hiddenSerialPagamento${pag.cod_pag}" value="${pag.num_doc_pagamento}_${pag.serial_pag_proj}">
                                                        </div>
                                                </button>
                                            </div>
                                            <div class="d-flex justify-content-between align-items-between w-100 mb-4">
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;color:#ffffff;font-size:10px;background:#948c8c;padding-top: 5px;border-radius: 10px;">
                                                    &nbsp;Observação do Pagamento<br/>Data: ${pag.data}/ Ocorrência : ${pag.tipo_ocorrencia}/ ${pag.complemento}/ ${pag.obs_desc}<br/>${pag.obs_desc}&nbsp;
                                                </div>
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;">
                                                    `+varButtonEstornoPagamento+`
                                                </div>
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;">
                                                    `+varButtonGerarPDF+`
                                                </div>
                                                <div class="d-flex flex-column w-100" style="padding-right: 0.25rem;">
                                                    `+varButtonGerarPDFDescAcres+`
                                                </div>
                                            </div>
                                            <br/>
                                        </div>
                                        <div id="collapse${pag.cod_pag}" aria-labelledby="heading${pag.cod_pag}" data-parent="#accordion${pag.cod_pag}" class="collapse">
                                            <div class="card-block" id="divMapasPagoBeneficiarioSelecionado${pag.cod_pag}" style="width: 100%;height:100%;padding-top: 5px;">


                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                    });
                }

                $("#divConteudoRelPagTerc").html(rows);
                let_loader_rel_pag_terc.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_rel_pag_terc.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
          }
          });
    } else if ( nomeDoButton == 'btnGeraPDFPagMapas') {
        var varCodPagamento = valButton;
        var varTipoRelatorio = 'rel_proj_periodo_tipo';
        var varTipoPagamento = $("#listOcorrenciaPagamentoRelPagTerc").val();
        var varBeneficiario = $("#hiddenNomeBeneficiarioRel"+valButton).val();
        var varPeriodoPag = $("#textFieldPeriodoReferenciaRelPagTerc").val();

        var varDataGeracaoPagamento = $("#hiddenDataGeracaoPagamento"+valButton).val().split('-')[0];
        var varNumeroQuinzenaDataGeracaoPagamento = '1_quinz';
        if ((varDataGeracaoPagamento * 1) > 15 ) {
            varNumeroQuinzenaDataGeracaoPagamento = '2_quinz';
        }

        var varSerialPagamento = $("#hiddenSerialPagamento"+valButton).val();

        $.ajax({
            url: '/plan_controle_fat_2art_terc_app/gera_rel_pdf_mapas_pagos_terc_por_beneficiario',
            xhrFields: {
                responseType: 'blob'
              },

            data: {
                'cod_pagamento'   :   varCodPagamento,
                'tipo_relatorio'  :   varTipoRelatorio,
                'tipo_pagamento'  :   varTipoPagamento
            },
            success: function (blob) {
                //console.log(blob);
                //console.log(blob.size);
                //console.log(blob.nome_beneficiario);
                  var link=document.createElement('a');
                  link.href=window.URL.createObjectURL(blob);
                  link.download="Relatorio_Pagamento_" + varSerialPagamento + "_" + varBeneficiario + "_"+ varNumeroQuinzenaDataGeracaoPagamento + "_" + varPeriodoPag + ".pdf";
                  link.click();
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

    } else if (nomeDoButton == "btnApresentaFormPesqPagTercProjPeriodoTipoPag") {
        //var varIdUsuario = $("#selectListUsuario").val();

        var varValorAriaExpanded = $(this).attr("aria-expanded");

        if (varValorAriaExpanded == 'false') {
            var varDataAtual = new Date();
            var varDataReferencia = (varDataAtual.getMonth() + 1)+"/"+varDataAtual.getFullYear();
            $("#textFieldPeriodoReferenciaRelPagTerc").val(varDataReferencia);

            $("#divPanelDefaultDivContainerFormParamRelPag2artTerc").attr("style","width:100%;height: 280px;border-radius: 10px;");
            $("#divContainerRelPagTerc").attr("style","max-width: 1250px;width: 100%;height: 690px;padding-bottom:0px;padding-top:20px;border:solid 0px;margin-top: 80px;");

            $(this).attr("aria-expanded", "true");
            $(this).attr("class", "btn");
            $("#collapseTwo2").attr("class", "collapse show");

        } else {
            $("#divPanelDefaultDivContainerFormParamRelPag2artTerc").attr("style","width:100%;height: 200px;border-radius: 10px;");
            $("#divContainerRelPagTerc").attr("style","max-width: 1250px; width: 100%; height: 690px;padding-bottom:0px;padding-top:20px;border:solid 0px");
            $("#divConteudoRelPagTerc").attr("style","overflow: auto;width: 100%; height: 680px; border:solid 0px;padding-left:0px;padding-right:0px;");

            $(this).attr("aria-expanded", "false");
            $(this).removeAttr("class");
            $(this).attr("class", "collapsed");
            $("#collapseTwo2").attr("class", "collapse");

        }
    } else if (nomeDoButton == "btnMapasPagosBeneficiario") {
        var varCodPagamento = valButton;

        var varValorAriaExpanded = $(this).attr("aria-expanded");

        if (varValorAriaExpanded == 'false') {
        /*
            $("#divPanelDefaultDivContainerConteudoRelPagTerc").attr("style", "width:1070px; margin-bottom: 0px;border-radius: 10px;");
            $("#divContainerRelPagTerc").attr("style","max-width: 1250px; width: 1070px; height: 1140px;padding-bottom:0px;padding-top:20px;border:solid 0px");
            $("#divConteudoRelPagTerc").attr("style","overflow: auto;width: 1070px; height: 1090px; border:solid 0px;padding-left:0px;padding-right:0px;");
            $("#divFooterGeralProj").attr("style", "background-color: #c52f33;border-top-width: 20px;padding-top: 0px;margin-top: 475px;");
         */

            var varTabPagMapas =
            `<table id="tabPagMapasTerc`+varCodPagamento+`"  class="display wrap w-100 cl_tab_principal_pagina"" >
                <thead>
                    <tr>
                        <th scope="col">Data</th>
                        <th scope="col">Mapa</th>
                        <th scope="col">Placa</th>
                        <th scope="col">Valor(R$) </th>
                        <th scope="col">Desc(R$)</th>
                        <th scope="col">Acrés.(R$)</th>
                        <th scope="col">Valor Total(R$)</th>
                        <th scope="col">Obs. Desc.</th>
                        <th scope="col">Obs. Acres.</th>
                    </tr>
                </thead>
                <tbody>

                </tbody>
            </table>`;

            $.ajax({
                type: 'GET',
                url: '/plan_controle_fat_2art_terc_app/retorna_mapas_pagamento_selecionado',
                data: {
                    'cod_pagamento'   :   varCodPagamento
                },
                dataType: 'json',
                success: function (dados) {
                    var listaDadosPagamentos = [];
                    for (var i = 0; i < dados.registros_tab_pagamentos_terc.length; i++) {
                        var varDataFormatada = dados.registros_tab_pagamentos_terc[i].data.split('-')[2] + '/'+
                            dados.registros_tab_pagamentos_terc[i].data.split('-')[1] + '/' +
                            dados.registros_tab_pagamentos_terc[i].data.split('-')[0];

                        var registro_pag = [
                            varDataFormatada,
                            dados.registros_tab_pagamentos_terc[i].mapa,
                            dados.registros_tab_pagamentos_terc[i].placa,
                            dados.registros_tab_pagamentos_terc[i].val_frete.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
                            dados.registros_tab_pagamentos_terc[i].desc.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
                            dados.registros_tab_pagamentos_terc[i].acres.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
                            dados.registros_tab_pagamentos_terc[i].val_pagar.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
                            dados.registros_tab_pagamentos_terc[i].obs_desc,
                            dados.registros_tab_pagamentos_terc[i].obs_acresc
                        ];
                        listaDadosPagamentos.push(registro_pag);
                    }
                    $("#divMapasPagoBeneficiarioSelecionado"+varCodPagamento).html(varTabPagMapas);
                    $("#tabPagMapasTerc"+varCodPagamento).DataTable( {
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
                        "data":listaDadosPagamentos,
                        "columns": [
                            { title: "Data" },
                            { title: "Mapa" },
                            { title: "Placa" },
                            { title: "Valor(R$)" },
                            { title: "Desc.(R$)" },
                            { title: "Acrésc.(R$)" },
                            { title: "Val. Total" },
                            { title: "Obs. Desc." },
                            { title: "Obs. Acres." }
                        ],
                        "columnDefs": [
                            {"className": "dt-left", "targets": [0]},
                            {"className": "dt-center", "targets": [1,2]},
                            {"className": "dt-right", "targets": [3,4,5,6,7,8]}
                        ],
                        "oLanguage": {
                            "sProcessing":   "Processando...",
                            "sLengthMenu":   "",
                            "sZeroRecords":  "Não foram encontrados resultados",
                            "sInfo":         "",
                            "sInfoEmpty":    "",
                            "sInfoFiltered": "",
                            "sInfoPostFix":  "",
                            "sSearch":       "Pesquisar:",
                            "sUrl":          "",
                            "oPaginate": {
                                "sFirst":    "Primeiro",
                                "sPrevious": "Anterior",
                                "sNext":     "Proximo",
                                "sLast":     "Último"
                            }
                        }
                    });


                },error: function (request, status, error) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
             });


            $(this).attr("aria-expanded", "true");
            $(this).attr("class", "btn");
            $("#collapse"+varCodPagamento).attr("class", "collapse show");

        } else {
        /*
            $("#divPanelDefaultDivContainerConteudoRelPagTerc").attr("style", "width:1070px; margin-bottom: 0px;border-radius: 10px;");
            $("#divContainerRelPagTerc").attr("style","max-width: 1250px; width: 1070px; height: 690px;padding-bottom:0px;padding-top:20px;border:solid 0px");
            $("#divConteudoRelPagTerc").attr("style","overflow: auto;width: 1070px; height: 640px; border:solid 0px;padding-left:0px;padding-right:0px;");
            $("#divFooterGeralProj").attr("style", "background-color: #c52f33;border-top-width: 20px;padding-top: 0px;margin-top: 25px;");
           */

            $(this).attr("aria-expanded", "false");
            $(this).removeAttr("class");
            $(this).attr("class", "collapsed");
            $("#collapse"+varCodPagamento).attr("class", "collapse");

        }
    } else if (nomeDoButton == "btnDesfazPagamentoMapasBeneficiario") {
        var varCodPagamento = valButton;
        $("#pMsgRefazerPagamentoMapaBenefTerc").html("Você tem certeza que deseja ESTORNAR o pagamento "+varCodPagamento+" gerado para o beneficiário ?");
        $("#hiddenCodPagamento2ArtTercFinanParaDesativar").val(varCodPagamento);

        $("#modalRefazerPagamentoMapaBenefTerc").show();
    } else if ( nomeDoButton == 'btnFechaModalRefazerPagamentoMapaBenefTerc') {
        $("#modalRefazerPagamentoMapaBenefTerc").hide();

    } else if ( nomeDoButton == 'btnDesativaPagamento2ArtTercFinanc') {
        var varCodPagamento = $("#hiddenCodPagamento2ArtTercFinanParaDesativar").val();
        $.ajax({
            type: 'DELETE',
            url: '/plan_controle_fat_2art_terc_app/desfaz_pagamento_mapas_beneficiario_terc/' + varCodPagamento,
            dataType: 'json',
            success: function (data) {
                $("#modalRefazerPagamentoMapaBenefTerc").hide();
                $("#divConteudoRelPagTerc").html("");
                //povoa_tabMapasTerceitos2Art();
                $.gritter.add({
                    title: 'Atenção!',
                    text: data.msg,
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

    } else if ( nomeDoButton == 'btnGeraPDFDescAcres') {
      var varCodPagamento = valButton;

      $.ajax({
          url: '/plan_controle_fat_2art_terc_app/gera_rel_pdf_acres_desc_pagamento_mapas_terc',
          xhrFields: {
              responseType: 'blob'
            },

          data: {
              'cod_pagamento'   :   varCodPagamento
          },
          success: function (blob) {
              //console.log(blob);
              //console.log(blob.size);
              //console.log(blob.nome_beneficiario);
                var link=document.createElement('a');
                link.href=window.URL.createObjectURL(blob);
                link.download="Relatorio_Acrescimos_Desconto_Pagamento_Portal_Operacional.pdf";
                link.click();
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



/*
$(document).on('change', '#listProjetosRelPagTerc', function(){
    var varProjetoSelecionado = $(this).val(); 
    var varListPagamentosBenef = document.getElementById("listCodPagamentoRelPagTerc");
    $("#listCodPagamentoRelPagTerc option").remove();
    $("#listCodPagamentoRelPagTerc").append("<option value='0'>Selecione projeto>beneficiário>referência</option>");
    if (varProjetoSelecionado == "0") {
        var varListBeneficiarios = document.getElementById("listBeneficiariosRelPagTerc");
        $("#listBeneficiariosRelPagTerc option").remove();
        $("#listBeneficiariosRelPagTerc").append("<option value='0'>Selecione o projeto para filtrar os beneficiários</option>");
    } else {
        $.ajax({
            url: '/povoa_listBeneficiariosPesqMapasTerc_formPesqMapasTerc',    
            data: {
                'cod_projeto'   :   varProjetoSelecionado
            },      
            dataType: 'json',  
            success: function (data) {
                var varListBeneficiarios = document.getElementById("listBeneficiariosRelPagTerc");
                $("#listBeneficiariosRelPagTerc option").remove();
                $("#listBeneficiariosRelPagTerc").append("<option value='0'>Selecione o Beneficiário</option>");
                data.lista_beneficiarios_distintos_from_cad_placa.forEach(beneficiario => {
                    $("#listBeneficiariosRelPagTerc").append("<option value='"+beneficiario.cod_benef_terc+"'>"+beneficiario.doc_benef_terc+"-"+beneficiario.nome_benef_terc+"</option>");
    
                });   
                
                $(".classSelectListBeneficiariosRelPagTerc").select2({
                    placeholder:"Selecione o Beneficiário",
                    allowClear: true
                });
    
            },
            error: function (request, status, error) {
                alert(error);
          }
          });

    }   

});  



$(document).on('change', '#textFieldPeriodoReferenciaRelPagTerc', function(){    
    var varBeneficiarioSelecionado = $("#listBeneficiariosRelPagTerc").val(); 
    var varPeriodoReferencia = $("#textFieldPeriodoReferenciaRelPagTerc").val();
    if (varBeneficiarioSelecionado == "0") {
        var varListPagamentosBenef = document.getElementById("listCodPagamentoRelPagTerc");
        $("#listCodPagamentoRelPagTerc option").remove();
        $("#listCodPagamentoRelPagTerc").append("<option value='0'>Selecione projeto>beneficiãrio>Referência</option>");
    } else {
        $.ajax({
            url: '/retorna_pagamentos_beneficiario_terceiros',    
            data: {                
                'cod_beneficiario'      :   varBeneficiarioSelecionado,
                'periodo_referencia'    :   varPeriodoReferencia
            },      
            dataType: 'json',  
            success: function (data) {
                var varListPagamentos = document.getElementById("listCodPagamentoRelPagTerc");
                $("#listCodPagamentoRelPagTerc option").remove();
                $("#listCodPagamentoRelPagTerc").append("<option value='0'>Todos os Pagamentos</option>");
                data.lista_cod_pagamentos.forEach(pag => {
                    $("#listCodPagamentoRelPagTerc").append("<option value='"+pag+"'>"+pag+"</option>");               							
    
                });   
                
                $(".classSelectListCodPagamentoRelPagTerc").select2({
                    placeholder:"Selecione o Pagamento",
                    allowClear: true
                });
    
            },
            error: function (request, status, error) {
                alert(error);
          }
          });

    }   

}); 


$(document).on('change', '#listBeneficiariosRelPagTerc', function(){
    var varPeriodoReferencia = $("#textFieldPeriodoReferenciaRelPagTerc").val();
    var varBeneficiarioSelecionado = $(this).val(); 
    if (varPeriodoReferencia == "") {
        var varListPagamentosBenef = document.getElementById("listCodPagamentoRelPagTerc");
        $("#listCodPagamentoRelPagTerc option").remove();
        $("#listCodPagamentoRelPagTerc").append("<option value='0'>Selecione periodo de referência</option>");
    } else {
        $.ajax({
            url: '/retorna_pagamentos_beneficiario_terceiros',    
            data: {                
                'cod_beneficiario'      :   varBeneficiarioSelecionado,
                'periodo_referencia'    :   varPeriodoReferencia
            },      
            dataType: 'json',  
            success: function (data) {
                var varListPagamentos = document.getElementById("listCodPagamentoRelPagTerc");
                $("#listCodPagamentoRelPagTerc option").remove();
                $("#listCodPagamentoRelPagTerc").append("<option value='0'>--Todos os Pagamentos --</option>");
                data.lista_cod_pagamentos.forEach(pag => {
                    $("#listCodPagamentoRelPagTerc").append("<option value='"+pag+"'>"+pag+"</option>");               							
    
                });   
                
                $(".classSelectListCodPagamentoRelPagTerc").select2({
                    placeholder:"Selecione o Pagamento",
                    allowClear: true
                });
    
            },
            error: function (request, status, error) {
                alert(error);
          }
          });

    }   

});
*/