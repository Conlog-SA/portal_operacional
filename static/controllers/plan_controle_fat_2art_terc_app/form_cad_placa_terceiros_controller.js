

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


$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if (nomeDoButton == "btnCadPlacaTerceiros") {
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
            $("#textFieldNomeProprietario").val("");
            $("#textFieldPlacaCadTerc").val("");
            $("#textFieldCnpjCpf").val("");
            $("#listTipoPessoa").val("0");
            $("#listPerfilVeiculo").val("0");
            $("#textFieldIniVigenciaCadTerc").val("");
            $("#textFieldFimVigenciaCadTerc").val("");
            $("#listProjetosCadPlacaTerc").val(var_cod_projeto);
            $("#listProjetosCadPlacaTerc").selectpicker('refresh');
            atualiza_comp_beneficiarios_benner_cad_placa(var_cod_projeto);

            $("#modalCadPlacaTerceiros").show();
        }


    } else if ( nomeDoButton == 'fechaModalCadPlacaTerc') {
        $("#modalCadPlacaTerceiros").hide();
    } else if (nomeDoButton == "btnSalvaRegCadPlacaTerc") {       
        var varIdBeneficiario = $("#listNomeBeneficiarioCadPlacaTerc").val();
        var varPlaca = $("#textFieldPlacaCadTerc").val();
        var varPerfilVeiculo = $("#listPerfilVeiculo").val();
        var varDataInicioVigencia = $("#textFieldIniVigenciaCadTerc").val();
        var varDataFimVigencia = $("#textFieldFimVigenciaCadTerc").val();
        var varCodProjeto = $("#listProjetosCadPlacaTerc").val();

        if(varIdBeneficiario == '' || varPlaca == '' || varPerfilVeiculo == '0' ||
            varDataInicioVigencia == '' || varDataFimVigencia == '' || varCodProjeto == '') {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Todos os campos do formulário são obrigatórios!',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/salva_registro_cad_placa_terceiros",
            data: {
                'id_benef'      :   varIdBeneficiario,
                'placa'         :   varPlaca,
                'perfil_veic'   :   varPerfilVeiculo,
                'inicio_vig'    :   varDataInicioVigencia,
                'fim_vig'       :   varDataFimVigencia,
                'cod_proj'      :   varCodProjeto

              },
            success: function(dados){
                $("#modalCadPlacaTerceiros").hide();
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
        }
    
    } else if (nomeDoButton == "btnPesqCadPlacaTerceiros") {       
        povoa_tab_cad_placas_terc();
    } else if (nomeDoButton == "btnExcluirCadPlacaTerc") {
        let let_loader_cad_placa = document.getElementById("loader_cad_placa");
        let_loader_cad_placa.style.display = "flex";
        $.ajax({
            type: 'POST',
            url:"/plan_controle_fat_2art_terc_app/retorna_qtd_mapas_pagos_vinculados_cad_placa",
            data: {
                'cod_registro_cad_placa_terc'    :   valButton
              },
            success: function(dados){
                $("#hiddenIdCadPlacaTerc").val(valButton);

                if (dados.indica_exclusao == 'S'){
                    $("#pMsgModalExcluiPlaca").html('Tem certeza que deseja excluir o registro ?');
                    $("#idDivButtonExlcuiRegCadPlacaSelecionado").html(`
                        <button type="button" name="btnExcluiRegCadPlacaTercSelecionado" id="btnExcluiRegCadPlacaTercSelecionado"
                        class="btn btn-primary btn-rounded botaoPrincipal">
                            <i class='fa-solid fa-trash-can'></i>
                            Excluir Registro
                        </button>
                    `);
                } else {
                    $("#pMsgModalExcluiPlaca").html('Não é possivel excluir o frete pois o mesmo possui ' + dados.qtd_mapas_pagos + ' mapas pagos vinculados!');
                    $("#idDivButtonExlcuiRegCadPlacaSelecionado").html('');
                }
                let_loader_cad_placa.style.display = "none";
                $("#modalExcluiCadPlacaTerc").show();

            },
            error: function (request, status, error) {
                let_loader_cad_placa.style.display = "none";
                $.gritter.add({
                    title: 'Atenção!',
                    text: error,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

            }
        });


    } else if ( nomeDoButton == "btnFechaModalExcluiCadPlacaTerc") {
        $("#modalExcluiCadPlacaTerc").hide();
    } else if ( nomeDoButton == "btnExcluiRegCadPlacaTercSelecionado") {
        var varCodRegistroCadPlacaTerc = $("#hiddenIdCadPlacaTerc").val();
        $.ajax({
            type: 'DELETE',
            url:"/plan_controle_fat_2art_terc_app/exclui_registro_cad_placa_terceiros/" + varCodRegistroCadPlacaTerc,
            success: function(dados){ 
                $("#modalExcluiCadPlacaTerc").hide();
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
                povoa_tab_cad_placas_terc();
                
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


    } else if ( nomeDoButton == "btnReplicaCadPlacaTerceiros") {
        let let_loader_cad_placa = document.getElementById("loader_cad_placa");
        $('#textFieldIniVigenciaCadTercReplic').val("");
        $('#textFieldFimVigenciaCadTercReplic').val("");

        var var_competencia_pesq = $("#textFieldPesqCadPlacaTercPeriodoVigencia").val();
        var var_cod_proj = $("#listProjetosPesqCadPlacaTerc").val();
        if ( var_competencia_pesq != '' ){

            let_loader_cad_placa.style.display = "flex";
            $.ajax({
                type: 'GET',
                data: {
                    comp        :   var_competencia_pesq,
                    cod_proj    :   var_cod_proj
                },
                url: "/plan_controle_fat_2art_terc_app/pesquisa_data_origem_replicacao_cad_placa_spot",
                success: function(dados){
                    $("#cb_vigencias_cad_placa_terc option").remove();
                    $("#cb_vigencias_cad_placa_terc").append("<option value='0' selected>--- VIGÊNCIA ORIGEM ---</option>");
                    dados.lista_datas_comp.forEach ( reg => {
                        var var_data_ini_reg_origem = reg.data_ini_vigencia.split("-")[2]+"-"+
                            reg.data_ini_vigencia.split("-")[1]+"-"+
                            reg.data_ini_vigencia.split("-")[0];
                        var var_data_fim_reg_origem = reg.data_fim_vigencia.split("-")[2]+"-"+
                            reg.data_fim_vigencia.split("-")[1]+"-"+
                            reg.data_fim_vigencia.split("-")[0];
                        $("#cb_vigencias_cad_placa_terc").append("<option value='"+reg.data_ini_vigencia+"_"+
                            reg.data_fim_vigencia+"' >Replicar de frete da vigência de "+var_data_ini_reg_origem+" a "+
                             var_data_fim_reg_origem                +"</option>");
                    });
                    $("#cb_vigencias_cad_placa_terc").selectpicker('refresh');
                    let_loader_cad_placa.style.display = "none";

                },
                error: function(request, status, error){
                    let_loader_cad_placa.style.display = "none";
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });

            $("#modalReplicaCadPlacaTerc").show();
        } else {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe o período de vigência para a replicação!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }

    
    } else if ( nomeDoButton == "btnFechaModalExecReplicCadPlacaTerc") {
        $("#modalReplicaCadPlacaTerc").hide();
    } else if ( nomeDoButton == "btnExecutaReplicacaoCadPlacaTerc") {
        var varCodProjeto = $("#listProjetosPesqCadPlacaTerc").val();
        var varDataVigencia = $("#cb_vigencias_cad_placa_terc").val();
        var varDataIniVigencia = $("#textFieldIniVigenciaCadTercReplic").val();        
        var varDataFimVigencia = $("#textFieldFimVigenciaCadTercReplic").val();        
        if ( varDataVigencia == '0' ) {
             $.gritter.add({
                title: 'Atenção!',
                text: "Informe a vigência de origem!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $.ajax({
                type: 'POST',
                url:"/plan_controle_fat_2art_terc_app/replica_registro_cad_placa_terceiros",
                data: {
                    'cod_proj'          :   varCodProjeto,
                    'data_vigencia'     :   varDataVigencia,
                    'data_ini_vigencia' :   varDataIniVigencia,
                    'data_fim_vigencia' :   varDataFimVigencia
                },
                success: function(dados){
                    $("#modalReplicaCadPlacaTerc").hide();
                    $.gritter.add({
                        title: 'Atenção!',
                        text: dados.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                    $("#tabCadPlacaTerceitos").DataTable().clear().draw();

                },
                error: function (request, status, error) {
                    $("#modalReplicaCadPlacaTerc").hide();
                    $.gritter.add({
                        title: 'Atenção!',
                        text: "Erro ao replicar os dados. Possivelmente existem dados duplicados. Verique !",
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });
        }

    } else if (nomeDoButton == "btnCadBeneficiarioTerceiros") {
        var var_cod_projeto_pesq_placas = $("#listProjetosPesqCadPlacaTerc").val();
        if (var_cod_projeto_pesq_placas == '') {
            $.gritter.add({
                title: 'Atenção!',
                text: 'Selecione um projeto !',
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        } else {
            $('#listProjetosCadBenefTerc').val(var_cod_projeto_pesq_placas);
            $('#listProjetosCadBenefTerc').selectpicker('refresh');
            atualiza_comp_beneficiarios_benner_cad_benef(var_cod_projeto_pesq_placas);
            povoa_tab_beneficiarios_terc();
            $("#modalCadBeneficiarioTerceiros").show();
        }

    } else if ( nomeDoButton == 'fechaModalCadBeneficiarioTerceiros') {
        $("#modalCadBeneficiarioTerceiros").hide();
    } else if (nomeDoButton == "btnSalvaRegCadBenefTerc") {
        var varCodProjeto = $("#listProjetosCadBenefTerc").val();

        var var_dados_benef_benner = $("#cb_handle_benner_beneficiario").val();
        if(var_dados_benef_benner == ''){
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe um Beneficiário",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });


        } else {
            var var_handle_benner = var_dados_benef_benner.split('_')[0];
            var varNomeBeneficiario = var_dados_benef_benner.split('_')[1];
            var varTipoPessoa = 'Pessoa Física';
            if(var_dados_benef_benner.split('_')[2]==2){
                varTipoPessoa = 'Pessoa Jurídica';
            }
            var varDocBenef = var_dados_benef_benner.split('_')[4];
            var var_status_benef = 'D';
            if(var_dados_benef_benner.split('_')[3]=='N'){
                var_status_benef = 'A';
            }
            $.ajax({
                type: "POST",
                url:"/plan_controle_fat_2art_terc_app/salva_registro_cad_beneficiario_terceiros",
                data: {
                    'cod_projeto'   :   varCodProjeto,
                    'nome_benef'    :   varNomeBeneficiario,
                    'doc_benef'     :   varDocBenef,
                    'tipo_benef'    :   varTipoPessoa,
                    'handle_benner' :   var_handle_benner,
                    'status_benef'  :   var_status_benef
                  },
                success: function(data){
                    $.gritter.add({
                        title: 'Atenção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                    atualiza_comp_beneficiarios_benner_cad_benef(varCodProjeto);
                    povoa_tab_beneficiarios_terc();

                },
                error: function (request, status, error) {
                    $.gritter.add({
                        title: 'Atenção!',
                        text: error,
                        text: error,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                }
            });
        }


    } else if (nomeDoButton == "btn_ativa_benef_terc" || nomeDoButton == "btn_desativa_benef_terc") {
         var varCodRegistroCadBenefTerc = valButton;

        $.ajax({
            type: 'DELETE',
            url:"/plan_controle_fat_2art_terc_app/desativa_ativa_registro_cad_beneficiario_terceiros/" + varCodRegistroCadBenefTerc,
            success: function(dados){
                $.gritter.add({
                    title: 'Atenção!',
                    text: dados.msg,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });

                povoa_tab_beneficiarios_terc();

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
$(document).on('change','input', function(){
    var nomeDoInput = $(this).attr('name');
    var valRadio = $(this).attr('value');

    if (nomeDoInput == 'rdTipoDocBenefTerc'){
        if (valRadio == 'CPF') {
            $(textFieldCnpjCpfBenefTerc).attr("maxlength", "11");
        } else if (valRadio == 'CNPJ') {
            $(textFieldCnpjCpfBenefTerc).attr("maxlength", "14");
        }
    }

});
*/


function povoa_tab_beneficiarios_terc(){
    var varCodProjeto = $("#listProjetosPesqCadPlacaTerc").val();
    let let_loader_cad_placa = document.getElementById("loader_cad_placa");
    let_loader_cad_placa.style.display = "flex";
    $.ajax({
            url:"/plan_controle_fat_2art_terc_app/retorna_cad_beneficiario_terceiros_projeto_selecionado",
            data: {
                'cod_projeto'   :   varCodProjeto
              },
            success: function(data){

                var listaDadosBenef = [];
                var img = "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
                for (var i = 0; i < data.lista_beneficiarios_do_projeto.length; i++) {
                    var var_btn_ativa_desativa_benef = '';

                    var varStatusBenef = ''
                    if (data.lista_beneficiarios_do_projeto[i].status_benef == 'A') {
                        varStatusBenef = 'Ativo';
                        var_btn_ativa_desativa_benef = `
                            <button type='button' class='btn btn-rounded btn-space'
                            id='btn_desativa_benef_terc_`+data.lista_beneficiarios_do_projeto[i].cod_benef_terc+`'
                            name='btn_desativa_benef_terc'
                            value='`+data.lista_beneficiarios_do_projeto[i].cod_benef_terc+`'>
                            <i class="fa-solid fa-circle-xmark" style="color: #f46424;"></i>
                            </button>
                        `;

                    }else if (data.lista_beneficiarios_do_projeto[i].status_benef == 'D'){
                        varStatusBenef = 'Desativado';
                        var_btn_ativa_desativa_benef = `
                            <button type='button' class='btn btn-rounded btn-space'
                            id='btn_ativa_benef_terc_`+data.lista_beneficiarios_do_projeto[i].cod_benef_terc+`'
                            name='btn_ativa_benef_terc'
                            value='`+data.lista_beneficiarios_do_projeto[i].cod_benef_terc+`'>
                            <i class="fa-solid fa-circle-check" style="color: #f46424;"></i>
                            </button>
                        `;
                    }
                    var registro = [
                        img,
                        data.lista_beneficiarios_do_projeto[i].doc_benef_terc+"-"+data.lista_beneficiarios_do_projeto[i].nome_benef_terc,
                        data.lista_beneficiarios_do_projeto[i].tipo_pessoa_benef_terc,
                        data.lista_beneficiarios_do_projeto[i].handle_benner,
                        varStatusBenef,
                        var_btn_ativa_desativa_benef

                    ];
                    listaDadosBenef.push(registro);
                }
                $('#tabBenefTerc').DataTable( {
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
                    /*"bJQueryUI": true,
                    "pageLength": 6,
                    "destroy": true,
                      "dom": 'Bfrtip',
                      "buttons": [
                        'copyHtml5'
                        ],*/
                      "data":listaDadosBenef,
                        "columns": [
                                { title: "" },
                                { title: "Beneficiário" },
                                { title: "Tipo Pessoa" },
                                { title: "Handle" },
                                { title: "Status" },
                                { title: "Ativa/Desativa" }
                            ],
                            "columnDefs": [
                                {"className": "dt-center", "targets": [2, 3, 4, 5]},
                                {"className": "dt-left", "targets": [0, 1]}
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
                let_loader_cad_placa.style.display = "none";
            },
            error: function (request, status, error) {
                let_loader_cad_placa.style.display = "none";
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

function atualiza_comp_beneficiarios_benner_cad_benef(cod_projeto){
    let let_loader_cad_placa = document.getElementById("loader_cad_placa");
    let_loader_cad_placa.style.display = "flex";
    $.ajax({
        type: "GET",
        data: {
            'tipo_cad'  :   'benef',
            'cod_proj'  :   cod_projeto
        },
        url: "/plan_controle_fat_2art_terc_app/atualiza_comp_benef_benner_cad_placa_terc",
        success: function(data){
            var var_options = "";
            data.lista_benef_benner_dic.forEach(b => {
                var var_inativo = 'Ativo';
                if( b.inativo == 'S' ){
                    var_inativo = 'Inativo';
                }
                var_options += "<option value='"+b.handle+"_"+b.nome+"_"+b.tipo+"_"+
                    b.inativo+"_"+b.doc.replaceAll('.','').replaceAll('/','').replaceAll('-','')+"' >"+
                    b.doc.replaceAll('.','').replaceAll('/','').replaceAll('-','')+" - "+b.nome+"("+var_inativo+")</option> ";
            });
            $("#cb_handle_benner_beneficiario").html(var_options);
            $("#cb_handle_benner_beneficiario").selectpicker('refresh');
            let_loader_cad_placa.style.display = "none";

        },
        error: function(request, status, error){
            let_loader_cad_placa.style.display = "none";
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


function atualiza_comp_beneficiarios_benner_cad_placa(cod_projeto){
    let let_loader_cad_placa = document.getElementById("loader_cad_placa");
    let_loader_cad_placa.style.display = "flex";
    $.ajax({
        type: "GET",
        data: {
            'tipo_cad'  :   'placa',
            'cod_proj'  :   cod_projeto
        },
        url: "/plan_controle_fat_2art_terc_app/atualiza_comp_benef_benner_cad_placa_terc",
        success: function(data){
            var var_options = "";
            data.lista_benef_benner_dic.forEach(b => {
                var var_inativo = 'Ativo';
                if( b.status_benef == 'S' ){
                    var_inativo = 'Inativo';
                }
                var_options += "<option value='"+b.cod_benef_terc+"' >"+
                    b.doc_benef_terc + " - "+b.nome_benef_terc + "("+var_inativo+")</option> ";
            });
            $("#listNomeBeneficiarioCadPlacaTerc").html(var_options);
            $("#listNomeBeneficiarioCadPlacaTerc").selectpicker('refresh');
            let_loader_cad_placa.style.display = "none";

        },
        error: function(request, status, error){
            let_loader_cad_placa.style.display = "none";
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


$(document).on('change', '#listProjetosCadBenefTerc', function(){
    var var_cod_projeto = $(this).val();
    atualiza_comp_beneficiarios_benner_cad_benef(var_cod_projeto);
});

$(document).on('change', '#listProjetosCadPlacaTerc', function(){
    var var_cod_projeto = $(this).val();
    atualiza_comp_beneficiarios_benner_cad_placa(var_cod_projeto);
});


function povoa_tab_cad_placas_terc(){
    var varCodProjeto = $("#listProjetosPesqCadPlacaTerc").val();
    var varDataVigencia = $("#textFieldPesqCadPlacaTercPeriodoVigencia").val();
    let let_loader_cad_placa = document.getElementById("loader_cad_placa");
    let_loader_cad_placa.style.display = "flex";
    $.ajax({
        url:"/plan_controle_fat_2art_terc_app/pesquisa_registros_cad_placa_terceiros",
        data: {
            'cod_proj'    :   varCodProjeto,
            'periodo_vig'  :   varDataVigencia

          },
        success: function(data){
            listaDados = [];
            var img =  "<i class='fa-solid fa-caret-right' style='color: #f46424;'></i>";
            for (var i = 0; i < data.registros_cad_placa_terc.length; i++) {
                var varDataStringIni = data.registros_cad_placa_terc[i].data_ini.split("-")[2]+"/"+data.registros_cad_placa_terc[i].data_ini.split("-")[1]+"/"+data.registros_cad_placa_terc[i].data_ini.split("-")[0];
                var varDataStringFim = data.registros_cad_placa_terc[i].data_fim.split("-")[2]+"/"+data.registros_cad_placa_terc[i].data_fim.split("-")[1]+"/"+data.registros_cad_placa_terc[i].data_fim.split("-")[0];
                var varButtonExcluirCadPlacaTerc = `
                    <button type="button" class="btn btn-rounded btn-space"
                    id="btnExcluirCadPlacaTerc_${data.registros_cad_placa_terc[i].id_cad_placa_terc}"
                    name="btnExcluirCadPlacaTerc" value="${data.registros_cad_placa_terc[i].id_cad_placa_terc}"
                    title="Exclulir registro da placa ${data.registros_cad_placa_terc[i].placa} - ${data.registros_cad_placa_terc[i].perfil_veic}">
                    <i class="fa-solid fa-trash" style="color: #f46424;"></i>
                    </button>
                `;

                var registro = [
                    img,
                    data.registros_cad_placa_terc[i].placa,
                    data.registros_cad_placa_terc[i].perfil_veic,
                    data.registros_cad_placa_terc[i].handle_placa,
                    data.registros_cad_placa_terc[i].nome_beneficiario,
                    data.registros_cad_placa_terc[i].doc_benef,
                    data.registros_cad_placa_terc[i].tipo_pessoa_benef,
                    data.registros_cad_placa_terc[i].handle_benef,
                    varDataStringIni,
                    varDataStringFim,
                    varButtonExcluirCadPlacaTerc

                ];
                listaDados.push(registro);
            }
            $('#tabCadPlacaTerceitos').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "770px",
                "scrollX": true,
                "scrollCollapse": true,
                "paging": true,
                "searching": true,
                "pageLength": 7,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                /*"bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],*/
                "data":listaDados,
                "columns": [
                    { title: "" },
                    { title: "Placa" },
                    { title: "Perfil Veículo" },
                    { title: "Handle Placa" },
                    { title: "Beneficiário" },
                    { title: "CPF/CNPJ" },
                    { title: "Tipo Pessoa" },
                    { title: "Handle Beneficiário" },
                    { title: "Início Vigência" },
                    { title: "Fim Vigência" },
                    { title: "Excluir" }
                ],
                "columnDefs": [
                    {"className": "dt-center", "targets": [0,1,2,5]},
                    {"className": "dt-left", "targets": [4]},
                    {"className": "dt-right", "targets": [3,6,7,8,9]}
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
            let_loader_cad_placa.style.display = "none";
        },
        error: function (request, status, error) {
            let_loader_cad_placa.style.display = "none";
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