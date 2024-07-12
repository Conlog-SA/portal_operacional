var listaDados = [];

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



$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');


    if (nomeDoButton == "btnPesqCadFreteTerceiros") { 
        povoa_tab_fretes_terc();
    }
    else if (nomeDoButton == "btnReplicaCadFreteTerceiros") {
        let let_loader_cad_frete = document.getElementById("loader_cad_frete");
        $('#textFieldIniVigenciaCadTercReplic').val("");
        $('#textFieldFimVigenciaCadTercReplic').val("");

        var var_competencia_pesq = $("#textFieldPesqCadFreteTercPeriodoVigencia").val();
        var var_cod_proj = $("#listProjetosPesqCadFreteTerc").val();
        if ( var_competencia_pesq != '' ){
            let_loader_cad_frete.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    comp        :   var_competencia_pesq,
                    cod_proj    :   var_cod_proj
                },
                url: "/plan_controle_fat_2art_terc_app/pesquisa_data_origem_replicacao_cad_frete_spot",
                success: function(dados){

                    $("#cb_vigencias_cad_frete_terc option").remove();
                    $("#cb_vigencias_cad_frete_terc").append("<option value='0' selected>--- VIGÊNCIA ORIGEM ---</option>");
                    dados.lista_datas_comp.forEach ( reg => {
                        var var_data_ini_reg_origem = reg.data_ini_vigencia.split("-")[2]+"-"+
                            reg.data_ini_vigencia.split("-")[1]+"-"+
                            reg.data_ini_vigencia.split("-")[0];
                        var var_data_fim_reg_origem = reg.data_fim_vigencia.split("-")[2]+"-"+
                            reg.data_fim_vigencia.split("-")[1]+"-"+
                            reg.data_fim_vigencia.split("-")[0];
                        $("#cb_vigencias_cad_frete_terc").append("<option value='"+reg.data_ini_vigencia+"_"+
                            reg.data_fim_vigencia+"' >Replicar de frete da vigência de "+var_data_ini_reg_origem+" a "+
                             var_data_fim_reg_origem                +"</option>");
                    });
                    $("#cb_vigencias_cad_frete_terc").selectpicker('refresh');
                    let_loader_cad_frete.style.display = "none";

                },
                error: function(request, status, error){
                    let_loader_cad_frete.style.display = "none";
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });

            $("#modalReplicaCadFrete").show();
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe o período de vigência para a replicação!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }


    }
    else if ( nomeDoButton == "btnFechaModalExecReplicCadFreteSpot") {
        $("#modalReplicaCadFrete").hide();
    } else if ( nomeDoButton == "btnExecutaReplicacaoCadFreteSpot") {
        var varCodProjeto = $("#listProjetosPesqCadFreteTerc").val();
        var varDataVigencia = $("#cb_vigencias_cad_frete_terc").val();
        var varDataIniVigencia = $("#textFieldIniVigenciaCadFreteSpotReplic").val();        
        var varDataFimVigencia = $("#textFieldFimVigenciaCadFreteSpotReplic").val();        
        
        $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/replica_registro_cad_frete_spot",
            data: {
                'cod_proj'          :   varCodProjeto,
                'data_vigencia'     :   varDataVigencia,
                'data_ini_vigencia' :   varDataIniVigencia,
                'data_fim_vigencia' :   varDataFimVigencia
              },
            success: function(dados){                  
                $("#modalReplicaCadFrete").hide();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                $("#tabCadFreteTerceitos").DataTable().clear().draw();
                
            },
            error: function (request, status, error) {
                $("#modalReplicaCadFrete").hide();
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
    else if (nomeDoButton == "btnCadFreteTerceiros") {
        $("#hiddenCodCadFreteSpot").val("");   
        $("#listProjetosCadFreteSpot").val($("#listProjetosPesqCadFreteTerc").val());
        $("#listTipoPessoaCadFreteSpot").val("0");
        $("#listTipoEntrega").val("0");
        $("#listPerfilVeiculoCadFreteSpot").val("0");
        $("#textFieldCodRegiao").val("");
        $("#textFieldDescRegiao").val("");
        $("#textFieldQtdMin").val("0");
        $("#textFieldValFreteCarreteiroMin").val("0,00");
        $("#textFieldValDescargaMin").val("0,00");
        $("#textFieldValPedagioMin").val("0,00");
        $("#textFieldValCPRBMin").val("0,00");
        $("#textFieldValLucroMin").val("0,00");
        $("#textFieldQtdMax").val("0");
        $("#textFieldValFreteCarreteiroMax").val("0,00");
        $("#textFieldValDescargaMax").val("0,00");
        $("#textFieldValPedagioMax").val("0,00");
        $("#textFieldValCPRBMax").val("0,00");
        $("#textFieldValLucroMax").val("0,00");         

        
        $("input[type=text][name=textFieldValFreteCarreteiroMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValDescargaMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValPedagioMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValCPRBMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValLucroMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValFreteCarreteiroMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValDescargaMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValPedagioMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValCPRBMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValLucroMax]").mask('###0,00', {reverse: true});	

        
        $("#hiddenCodCadFreteSpot").val('0');
        $("#modalCadFreteSpot").show();

    } else if ( nomeDoButton == 'fechaModalCadFreteSpot') {
        $("#modalCadFreteSpot").hide();
    } else if (nomeDoButton == "btnSalvaRegCadFreteSpot") {  
        var varCodRegistroCadFreteSpot = $("#hiddenCodCadFreteSpot").val();   
        var varCodProjeto = $("#listProjetosCadFreteSpot").val();
        var varDataInicioVigencia = $("#textFieldIniVigenciaCadFreteSpot").val();
        var varDataFimVigencia = $("#textFieldFimVigenciaCadFreteSpot").val();
        var varTipoPessoa = $("#listTipoPessoaCadFreteSpot").val();
        var varTipoEntrega = $("#listTipoEntrega").val();
        var varPerfilVeiculo = $("#listPerfilVeiculoCadFreteSpot").val();
        var varCodRegiao = $("#textFieldCodRegiao").val();
        var varDescRegiao = $("#textFieldDescRegiao").val();
        var varQtdMin = $("#textFieldQtdMin").val();
        var varValFreteCarreteiroMin = $("#textFieldValFreteCarreteiroMin").val();
        var varValDescargaMin = $("#textFieldValDescargaMin").val();
        var varValPedagioMin = $("#textFieldValPedagioMin").val();
        var varValCPBRMin = $("#textFieldValCPRBMin").val();
        var varValLucroMin = $("#textFieldValLucroMin").val();
        var varQtdMax = $("#textFieldQtdMax").val();
        var varValFreteCarreteiroMax = $("#textFieldValFreteCarreteiroMax").val();
        var varValDescargaMax = $("#textFieldValDescargaMax").val();
        var varValPedagioMax = $("#textFieldValPedagioMax").val();
        var varValCPBRMax = $("#textFieldValCPRBMax").val();
        var varValLucroMax = $("#textFieldValLucroMax").val();
        

        $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/salva_registro_cad_frete_spot",
            data: {
                'cod_registro'          :   varCodRegistroCadFreteSpot,
                'cod_proj'              :   varCodProjeto,
                'inicio_vig'            :   varDataInicioVigencia,
                'fim_vig'               :   varDataFimVigencia,
                'tipo_pessoa'           :   varTipoPessoa,
                'tipo_entrega'          :   varTipoEntrega,
                'perfil_veic'           :   varPerfilVeiculo,
                'cod_regiao'            :   varCodRegiao,
                'desc_regiao'           :   varDescRegiao,               
                'qtd_min'               :   varQtdMin,
                'frete_carreteiro_min'  :   varValFreteCarreteiroMin.replace(',','.'),
                'descarga_min'          :   varValDescargaMin.replace(',','.'),
                'pedagio_min'           :   varValPedagioMin.replace(',','.'),
                'cpbr_min'              :   varValCPBRMin.replace(',','.'),
                'lucro_min'             :   varValLucroMin.replace(',','.'),
                'qtd_max'               :   varQtdMax,
                'frete_carreteiro_max'  :   varValFreteCarreteiroMax.replace(',','.'),
                'descarga_max'          :   varValDescargaMax.replace(',','.'),
                'pedagio_max'           :   varValPedagioMax.replace(',','.'),
                'cpbr_max'              :   varValCPBRMax.replace(',','.'),
                'lucro_max'             :   varValLucroMax.replace(',','.')                
        
              },
            success: function(dados){ 
                $("#modalCadFreteSpot").hide(); 
                /* $("#tabCadFreteTerceitos").DataTable().clear().draw(); */
                /* povoa_tab_fretes_terc(); */
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
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
    } else if (nomeDoButton == "btnEditaCadFreteSpot") {   
        var varIndiceListaDadosCadFreteSpot =  valButton;

        $('#hiddenCodCadFreteSpot').val(listaDados[varIndiceListaDadosCadFreteSpot][27]);
        $("#listProjetosCadFreteSpot").val($('#listProjetosPesqCadFreteTerc').val());
        $("#listProjetosCadFreteSpot").selectpicker('refresh');
        let let_data_ini = listaDados[varIndiceListaDadosCadFreteSpot][23].split('/')[2] + '-' +
            listaDados[varIndiceListaDadosCadFreteSpot][23].split('/')[1] + '-' +
            listaDados[varIndiceListaDadosCadFreteSpot][23].split('/')[0];
        let let_data_fim = listaDados[varIndiceListaDadosCadFreteSpot][24].split('/')[2] + '-' +
            listaDados[varIndiceListaDadosCadFreteSpot][24].split('/')[1] + '-' +
            listaDados[varIndiceListaDadosCadFreteSpot][24].split('/')[0];
        $("#textFieldIniVigenciaCadFreteSpot").val(let_data_ini);
        $("#textFieldFimVigenciaCadFreteSpot").val(let_data_fim);
        $("#listTipoPessoaCadFreteSpot").val(listaDados[varIndiceListaDadosCadFreteSpot][21]);
        $("#listTipoPessoaCadFreteSpot").selectpicker('refresh');
        $("#listTipoEntrega").val(listaDados[varIndiceListaDadosCadFreteSpot][22]);
        $("#listTipoEntrega").selectpicker('refresh');
        $("#listPerfilVeiculoCadFreteSpot").val(listaDados[varIndiceListaDadosCadFreteSpot][1]);
        $("#listPerfilVeiculoCadFreteSpot").selectpicker('refresh');
        $("#textFieldCodRegiao").val(listaDados[varIndiceListaDadosCadFreteSpot][2].split("-")[0]);
        $("#textFieldDescRegiao").val(listaDados[varIndiceListaDadosCadFreteSpot][2].split("-")[1]);
        $("#textFieldQtdMin").val(listaDados[varIndiceListaDadosCadFreteSpot][3]);
        $("#textFieldValFreteCarreteiroMin").val(listaDados[varIndiceListaDadosCadFreteSpot][4]);
        $("#textFieldValDescargaMin").val(listaDados[varIndiceListaDadosCadFreteSpot][5]);
        $("#textFieldValPedagioMin").val(listaDados[varIndiceListaDadosCadFreteSpot][6]);
        $("#textFieldValCPRBMin").val(listaDados[varIndiceListaDadosCadFreteSpot][7]);
        $("#textFieldValLucroMin").val(listaDados[varIndiceListaDadosCadFreteSpot][8]);
        $("#textFieldQtdMax").val(listaDados[varIndiceListaDadosCadFreteSpot][12]);
        $("#textFieldValFreteCarreteiroMax").val(listaDados[varIndiceListaDadosCadFreteSpot][13]);
        $("#textFieldValDescargaMax").val(listaDados[varIndiceListaDadosCadFreteSpot][14]);
        $("#textFieldValPedagioMax").val(listaDados[varIndiceListaDadosCadFreteSpot][15]);
        $("#textFieldValCPRBMax").val(listaDados[varIndiceListaDadosCadFreteSpot][16]);
        $("#textFieldValLucroMax").val(listaDados[varIndiceListaDadosCadFreteSpot][17])

        $("input[type=text][name=textFieldValFreteCarreteiroMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValDescargaMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValPedagioMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValCPRBMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValLucroMin]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValFreteCarreteiroMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValDescargaMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValPedagioMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValCPRBMax]").mask('###0,00', {reverse: true});	
        $("input[type=text][name=textFieldValLucroMax]").mask('###0,00', {reverse: true});

        $("#modalCadFreteSpot").show();         

    } else if (nomeDoButton == "btnExcluirCadFreteSpot") {
        let let_loader_cad_frete = document.getElementById("loader_cad_frete");
        let_loader_cad_frete.style.display = "flex";
        $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/retorna_qtd_mapas_pagos_vinculados_cad_frete_spot",
            data: {
                'cod_registro_cad_frete_spot'    :   valButton
            },
            success: function(dados){
                $("#hiddenIdCadFreteSpot").val(valButton);

                if (dados.indica_exclusao == 'S'){
                    $("#pMsg").html('Tem certeza que deseja excluir o registro ?');
                    $("#idDivButtonExlcuiRegCadFreteSpotSelecionado").html(`
                        <button type="button" name="btnExcluiRegCadFreteSpotSelecionado" id="btnExcluiRegCadFreteSpotSelecionado"
                        class="btn btn-primary btn-rounded botaoPrincipal">
                            <i class='fa-solid fa-trash-can'></i>
                            Excluir Registro
                        </button>
                    `);
                } else {
                    $("#pMsg").html('Não é possivel excluir o frete pois o mesmo possui ' + dados.qtd_mapas_pagos + ' mapas pagos vinculados!');
                    $("#idDivButtonExlcuiRegCadFreteSpotSelecionado").html('');
                }
                let_loader_cad_frete.style.display = "none";
                $("#modalExcluiCadFreteSpot").show();

            },
            error: function (request, status, error) {
                let_loader_cad_frete.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });


    } else if ( nomeDoButton == "btnFechaModalExcluiCadFreteSpot") {
        $("#modalExcluiCadFreteSpot").hide();
    } else if ( nomeDoButton == "btnExcluiRegCadFreteSpotSelecionado") {

        var varCodRegistroCadFreteSpot = $("#hiddenIdCadFreteSpot").val();

        $.ajax({
            type: 'DELETE',
            url:"/plan_controle_fat_2art_terc_app/exclui_registro_cad_frete_spot/" + varCodRegistroCadFreteSpot,
            success: function(dados){ 
                $("#modalExcluiCadFreteSpot").hide();
                $("#tabCadFreteTerceitos").DataTable().clear().draw();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tab_fretes_terc();
                
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
$(document).on('change', 'input', function(){  
    var nameInput = $(this).attr('name');
	var idInput = $(this).attr('id');
    var valueInput = $(this).val();
    
    if ( nameInput == 'textFieldValFreteCarreteiroMin') {
        var varValCPBR = (valueInput.replace(',','.') * 0.2) * 0.2;
        $("#textFieldValCPRBMin").val(varValCPBR.toLocaleString('pt-BR'));
    } else if ( nameInput == 'textFieldValFreteCarreteiroMax') {
        var varValCPBR = (valueInput.replace(',','.') * 0.2) * 0.2;
        $("#textFieldValCPRBMax").val(varValCPBR.toLocaleString('pt-BR'));
    }

});

*/


function povoa_tab_fretes_terc(){
    let let_loader_cad_frete = document.getElementById("loader_cad_frete");
    let_loader_cad_frete.style.display = "flex";
    var varCodProjeto = $("#listProjetosPesqCadFreteTerc").val();
    var varDataVigencia = $("#textFieldPesqCadFreteTercPeriodoVigencia").val();
    $.ajax({
        url:"/plan_controle_fat_2art_terc_app/pesquisa_registros_cad_frete_spot",
        data: {
            'cod_proj'    :   varCodProjeto,
            'periodo_vig'  :   varDataVigencia

          },
        success: function(data){
            listaDados = [];
            var img =   "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
            for (var i = 0; i < data.registros_cad_frete_terc.length; i++) {
                var varTtReceberMin = (data.registros_cad_frete_terc[i].val_frete_carreteiro_min * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_descarga_min * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_pedagio_min * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_cprb_min * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_lucro_min * 1.00);
                var varTtReceberMax = (data.registros_cad_frete_terc[i].val_frete_carreteiro_max * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_descarga_max * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_pedagio_max * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_cprb_max * 1.00) +
                                        (data.registros_cad_frete_terc[i].val_lucro_max * 1.00);

                var varValTotalPagarMin = (data.registros_cad_frete_terc[i].val_frete_carreteiro_min * 1.00) +
                                            (data.registros_cad_frete_terc[i].val_descarga_min * 1.00) +
                                            (data.registros_cad_frete_terc[i].val_pedagio_min * 1.00);

                var varValTotalPagarMax = (data.registros_cad_frete_terc[i].val_frete_carreteiro_max * 1.00) +
                                            (data.registros_cad_frete_terc[i].val_descarga_max * 1.00) +
                                            (data.registros_cad_frete_terc[i].val_pedagio_max * 1.00);

                var varDataStringIni = data.registros_cad_frete_terc[i].data_ini_vigencia.split("-")[2]+
                    "/"+data.registros_cad_frete_terc[i].data_ini_vigencia.split("-")[1]+
                    "/"+data.registros_cad_frete_terc[i].data_ini_vigencia.split("-")[0];
                var varDataStringFim = data.registros_cad_frete_terc[i].data_fim_vigencia.split("-")[2]+
                    "/"+data.registros_cad_frete_terc[i].data_fim_vigencia.split("-")[1]+
                    "/"+data.registros_cad_frete_terc[i].data_fim_vigencia.split("-")[0];
                var varButtonEditarCaddFreteSpot =
                    "<button type='button' class='btn btn-rounded btn-space' id='btnEditaCadFreteSpot"+
                    i+
                    "' name='btnEditaCadFreteSpot' value='"+
                    i+
                    "'><i class='fa-solid fa-pen-to-square' style='color: #f46424;'></i></button>"

                var varButtonExcluirCadFreteSpot =
                    "<button type='button' class='btn btn-rounded btn-space' id='btnExcluirCadFreteSpot"+
                    data.registros_cad_frete_terc[i].cod_cad_frete_spot+
                    "' name='btnExcluirCadFreteSpot' value='"+
                    data.registros_cad_frete_terc[i].cod_cad_frete_spot+
                    "'><i class='fa-solid fa-trash' style='color: #f46424;'></i></button>"

                var registro = [
                    img,
                    data.registros_cad_frete_terc[i].tipo_perfil_veiculo,
                    data.registros_cad_frete_terc[i].cod_regiao+"-"+data.registros_cad_frete_terc[i].nome_regiao,
                    data.registros_cad_frete_terc[i].qtd_min,
                    parseFloat(data.registros_cad_frete_terc[i].val_frete_carreteiro_min * 1.00).toFixed(2).toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_descarga_min.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_pedagio_min.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_cprb_min.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_lucro_min.toLocaleString('pt-BR'),
                    varTtReceberMin.toLocaleString('pt-BR'),
                    varValTotalPagarMin.toLocaleString('pt-BR'),
                    (parseFloat((varValTotalPagarMin/varTtReceberMin)*100.00).toFixed(2)).toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].qtd_max,
                    data.registros_cad_frete_terc[i].val_frete_carreteiro_max.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_descarga_max.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_pedagio_max.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_cprb_max.toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].val_lucro_max.toLocaleString('pt-BR'),
                    varTtReceberMax.toLocaleString('pt-BR'),
                    varValTotalPagarMax.toLocaleString('pt-BR'),
                    parseFloat((varValTotalPagarMax/varTtReceberMax)*100.00).toFixed(2).toLocaleString('pt-BR'),
                    data.registros_cad_frete_terc[i].tipo_pessoa,
                    data.registros_cad_frete_terc[i].tipo_entrega,
                    varDataStringIni,
                    varDataStringFim,
                    varButtonEditarCaddFreteSpot,
                    varButtonExcluirCadFreteSpot,
                    data.registros_cad_frete_terc[i].cod_cad_frete_spot

                ];
                listaDados.push(registro);
            }
            $('#tabCadFreteTerceitos').DataTable( {
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
                "initComplete": function () {
                    this.api()
                    .columns([1,2,3,12,21,22,23,24])
                    .every(function () {
                        let let_div = document.createElement('div');
                        let column = this;
                        let title = column.header().textContent;
                        // Create input element
                        let input = document.createElement('input');
                        input.classList.add('input_pesq_column_icon');
                        input.style.borderRadius = '0.2rem 0.2rem 0.2rem 0.2rem';
                        input.style.padding = '2px';
                        input.style.width = '120px';
                        input.placeholder = title;

                        let let_icon_input = document.createElement('i');
                        let_icon_input.classList.add('fa-solid');
                        let_icon_input.style.color = '#696969';
                        let_icon_input.classList.add('fa-magnifying-glass');

                        let_div.appendChild(let_icon_input);
                        let_div.appendChild(input);


                        column.header().replaceChildren(let_div);

                        // Event listener for user input
                        input.addEventListener('keyup', () => {
                            if (column.search() !== this.value) {
                                column.search(input.value).draw();
                            }
                        });
                    });

                    this.api()
                    .columns([0])
                    .every(function() {
                        let column = this;

                        let let_icon_input = document.createElement('i');
                        let_icon_input.classList.add('fa-solid');
                        let_icon_input.style.color = '#f46424';
                        let_icon_input.classList.add('fa-eraser');

                        let let_btn_limpar = document.createElement('button');
                        let_btn_limpar.classList.add('btn');
                        let_btn_limpar.title = 'Limpar pesquisa';
                        let_btn_limpar.classList.add('btn-rounded');
                        let_btn_limpar.classList.add('btn-space');
                        let_btn_limpar.appendChild(let_icon_input)

                        column.header().replaceChildren(let_btn_limpar);

                        let let_ev_enter = new Event('keyup');

                        // Event listener for user input
                        let_btn_limpar.addEventListener('click', () => {
                            let let_inputs = document.getElementsByClassName('input_pesq_column_icon');

                            for(let i = 0; i < let_inputs.length; i++) {
                                let_inputs[i].value = null;


                                // Despacha o evento para o campo de entrada
                                let_inputs[i].dispatchEvent(let_ev_enter);
                            }
                        });

                    });
                },
                "data":listaDados,
                "columns": [
                    { title: "" },
                    { title: "Perfil Veíc." },
                    { title: "Região" },
                    { title: "Até(Qtd)" },
                    { title: "Frete Carreteiro(R$)" },
                    { title: "Descarga(R$)" },
                    { title: "Pedágio(R$)" },
                    { title: "CPRB(R$)" },
                    { title: "Lucro(R$)" },
                    { title: "Tt. Receber(R$)" },
                    { title: "Val. Pagar(R$)" },
                    { title: "Margem(%)" },
                    { title: "Acima(Qtd)" },
                    { title: "Frete Carreteiro(R$)" },
                    { title: "Desgarca(R$)" },
                    { title: "Pedágio(R$)" },
                    { title: "CPRB(R$)" },
                    { title: "Lucro(R$)" },
                    { title: "Tt. Receber(R$)" },
                    { title: "Val. Pagar(R$)" },
                    { title: "Margem(%)" },
                    { title: "Tipo Pessoa" },
                    { title: "Tipo Entrega" },
                    { title: "Início Vigência" },
                    { title: "Fim Vigência" },
                    { title: "Editar" },
                    { title: "Excluir" },
                    { title: "Id" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,1,3,12,21,22,23,24,25,26,27]},
                    {"className": "dt-left", "targets": [2]},
                    {"className": "dt-right", "targets": [4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20]}
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
            let_loader_cad_frete.style.display = "none";
        },
        error: function (request, status, error) {
            let_loader_cad_frete.style.display = "none";
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