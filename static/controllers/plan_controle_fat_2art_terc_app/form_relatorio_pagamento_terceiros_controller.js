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
            success: function (dados) {


                $("#divConteudoRelPagTerc").html(dados);

                $(".display").DataTable( {
                    "bJQueryUI": true,
                    "destroy": true,
                    "fixedHeader": true,
                    //"scrollY": "570px", //770px
                    //"scrollX": true,
                    "scrollCollapse": true,
                    "paging": true,
                    "pageLength": 8,
                    "searching": true,
                    "dom": 'Bfrtip',
                    "buttons": [
                        'copyHtml5'
                    ],
                    "columnDefs": [
                        {"className": "dt-left", "targets": [0, 2]}
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
                } );
                $(".display").DataTable().columns.adjust().draw();
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
    } else if (nomeDoButton == "btnDesfazPagamentoMapasBeneficiario") {
        var varCodPagamento = valButton;
        let let_tipo_pagamento = $("#hd_tipo_pagamento_" + varCodPagamento).val();
        $("#pMsgRefazerPagamentoMapaBenefTerc").html("Você tem certeza que deseja ESTORNAR o pagamento "+varCodPagamento+" gerado para o beneficiário ?");
        $("#hiddenCodPagamento2ArtTercFinanParaDesativar").val(varCodPagamento);
        $("#hd_tipo_pagamento_confirma_estorno").val(let_tipo_pagamento);

        $("#modalRefazerPagamentoMapaBenefTerc").show();
    } else if ( nomeDoButton == 'btnFechaModalRefazerPagamentoMapaBenefTerc') {
        $("#hiddenCodPagamento2ArtTercFinanParaDesativar").val('');
        $("#hd_tipo_pagamento_confirma_estorno").val('');
        $("#ta_justificativa_estorno_pagamento").val('');
        $("#modalRefazerPagamentoMapaBenefTerc").hide();

    } else if ( nomeDoButton == 'btnDesativaPagamento2ArtTercFinanc') {
        var varCodPagamento = $("#hiddenCodPagamento2ArtTercFinanParaDesativar").val();
        let let_justificativa = $("#ta_justificativa_estorno_pagamento").val();
        let let_tipo_pagamento = $("#hd_tipo_pagamento_confirma_estorno").val();
        if( let_justificativa == null || let_justificativa == '') {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Campo justificativa obrigatório!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
             });
        } else {
            $.ajax({
                type: 'DELETE',
                url: '/plan_controle_fat_2art_terc_app/desfaz_pagamento_mapas_beneficiario_terc/' + varCodPagamento ,
                dataType: 'json',
                data: JSON.stringify({
                    'justificativa' : let_justificativa,
                    'tipo_pagamento': let_tipo_pagamento
                }),
                success: function (data) {
                    $("#modalRefazerPagamentoMapaBenefTerc").hide();
                    $("#divConteudoRelPagTerc").html("");
                    $("#hiddenCodPagamento2ArtTercFinanParaDesativar").val('');
                    $("#hd_tipo_pagamento_confirma_estorno").val('');
                    $("#ta_justificativa_estorno_pagamento").val('');
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

        }


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