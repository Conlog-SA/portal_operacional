var date = new Date();
var competenciaPesquisa = document.getElementById('competencia_pesquisa');
var month_atual = ("0" + (date.getMonth() + 1)).slice(-2);
var year_atual = date.getFullYear();
var yearMonth = `${year_atual}-${month_atual}`;
competenciaPesquisa.value = yearMonth;

dataCompleta = date.toISOString().split('T')[0];



$(document).ready(function(){
    loader_erro_pag = document.getElementById("loader_erro_pag");

    $('#table_erros_pagamento').DataTable( {
        "bJQueryUI": true,
        "destroy": true,
        "fixedHeader": true,
        "scrollY": "50vh", //770px
        "scrollX": true,
        "scrollCollapse": true,
        "paging": false,
        //"pageLength": 7,
        "searching": true,
        "dom": 'Bfrtip',
        "buttons": [
            'copyHtml5'
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

});
// ** SCRIPTS REFERENTES AO MODAL CRIAÇÃO DE VERBAS
btnModalCriaVerbas = document.getElementById('btn_modal_cria_verbas');
btnModalCriaVerbas.addEventListener('click', function() {
    $("#modal_cadastra_verba").show();
    
    // botoes para fecha modal
    btnFechaModalCriaVerbas = document.getElementById('btn_fecha_modal_cria_verbas');
    btnCancelaModalCriaVerbas = document.getElementById('btn_cancela_modal_cria_verbas');
    btnFechaModalCriaVerbas.addEventListener('click', function() {
        $("#modal_cadastra_verba").hide();
    })
    btnCancelaModalCriaVerbas.addEventListener('click', function() {
        $("#modal_cadastra_verba").hide();
    })    
})

// * registro nova verba
inputNovaVerba = document.getElementById('input_desc_nova_task');
btnRegistraVerba = document.getElementById('btn_modal_cria_nova_verbas');
btnRegistraVerba.addEventListener('click', function() {
    if(inputNovaVerba.value != ''){
        btnCancelaModalCriaVerbas.setAttribute("disabled", true);
        btnFechaModalCriaVerbas.setAttribute("disabled", true);
        btnRegistraVerba.setAttribute("disabled", true);
        $.ajax({
            type: "POST",
            url: "/gente_gestao_erros_pagamento_app/verbas_erros_pagamento",
            data: {
                nova_verba: inputNovaVerba.value,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(data) {
                $("#geg_ep_verba_lancamento option").remove();
                data.lista_verbas.forEach((verba) =>{
                    $("#geg_ep_verba_lancamento").append(
                        `<option value="${verba.cod_verba}">${verba.desc_verba}</option>`);
                })
                $('#geg_ep_verba_lancamento').selectpicker('refresh');

                $.gritter.add({
                    title: 'Sucesso!',
                    text: "Verba criada com sucesso!",
                    image: '/static/icons/sucess_icon.svg',
                    sticky: false,
                    time: '',
                });
            },
            error: function(error) {
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
        inputNovaVerba.value = "";
        
        btnCancelaModalCriaVerbas.removeAttribute("disabled");
        btnFechaModalCriaVerbas.removeAttribute("disabled");
        btnRegistraVerba.removeAttribute("disabled");
        
        $("#modal_cadastra_verba").hide();
    }else{
        $.gritter.add({
            title: 'Atenção!',
            text: "Preencha o campo Descrição!",
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }
})

// ** SCRIPTS REFERENTES AO MODAL REGISTRO DE ERRO DE PAGAMENTO
loaderModalLancamento = document.getElementById('loader_modal_lancamento')
selectColaboradorLancamento = document.getElementById('geg_ep_colaborador_erro')
btnModalNovoLancamento = document.getElementById('btn_modal_novo_lancamento')
btnModalNovoLancamento.addEventListener('click', function() {
    filial_selecionada = document.getElementById('geg_ep_pesquisa_filial').value
    if( filial_selecionada != '') {
        $("#modal_novo_lancamento").show();

        competencia_lancamento.value = yearMonth;
        prazo_lancamento = document.getElementById('prazo_lancamento');
        prazo_lancamento.value = dataCompleta;

    } else {
        $.gritter.add({
            title: 'Atenção!',
            text: "Selecione a filial!",
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

    
    // botoes para fecha modal
})
btnFechaModalNovoLancamento = document.getElementById('btn_fecha_modal_novo_lancamento');
btnCancelaModalNovoLancamento = document.getElementById('btn_cancela_modal_novo_lancamento');
btnFechaModalNovoLancamento.addEventListener('click', function() {
    $("#modal_novo_lancamento").hide();
    limpaCamposFormLancaErros()
})
btnCancelaModalNovoLancamento.addEventListener('click', function() {
    $("#modal_novo_lancamento").hide();
    limpaCamposFormLancaErros()
})    

// Atualiza lista de colabs ao alterar filial -- modal lançamento erros pagamento
selectFilialModal = document.getElementById('geg_ep_pesquisa_filial');
selectFilialModal.addEventListener('change', function() {
    loaderModalLancamento.style.display = "flex";
    //$("#geg_ep_colaborador_erro").val('default')
    //$("#geg_ep_colaborador_erro").selectpicker('refresh')
    idFilialSelecionada = selectFilialModal.value
    povoa_comp_colaboradores_by_filial(idFilialSelecionada);
    loaderModalLancamento.style.display = "none";
})



selectFilialModal = document.getElementById('geg_ep_pesquisa_filial');
selectColaborador = document.getElementById('geg_ep_colaborador_erro');
selectVerba = document.getElementById('geg_ep_verba_lancamento');
inputValor = document.getElementById('input_valor_lancamento');
inputResolvido = document.getElementById('chk_resolvido');
inputCompetencia = document.getElementById('competencia_lancamento');
inputDataPrazo = document.getElementById('prazo_lancamento');
inputDuvida = document.getElementById('text_area_duvida');
inputAcao = document.getElementById('text_area_acao');
inputObs = document.getElementById('text_area_obs');
btnCadastrar = document.getElementById('btn_modal_registra_erro_pagamento');

// * Botão registra novo lançamento de erro pagamento
$('#form_novo_lancamento').submit(function(event) {
    event.preventDefault();
    loaderModalLancamento.style.display = "flex";



    idFilialSelecionada = selectFilialModal.value
    codSeniorColaborador = selectColaborador.value
    codVerba = selectVerba.value
    valorEP = inputValor.value
    chkResolvido = $("#chk_resolvido").prop('checked');//inputResolvido.checked
    compLancamento = inputCompetencia.value
    dataPrazo = inputDataPrazo.value
    textDuvida = inputDuvida.value
    textAcao = inputAcao.value
    textObs = inputObs.value
    cod_erro_pag = btnCadastrar.value

    $.ajax({
        type: "POST",
        url: "/gente_gestao_erros_pagamento_app/lancamento_erros_pagamento",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            'idFilialSelecionada':idFilialSelecionada,
            'codSeniorColaborador':codSeniorColaborador,
            'codVerba':codVerba,
            'valorEP':valorEP,
            'chkResolvido': chkResolvido,
            'compLancamento':compLancamento,
            'dataPrazo':dataPrazo,
            'textDuvida':textDuvida,
            'textAcao':textAcao,
            'textObs':textObs,
            'cod_erro_pag':cod_erro_pag
        },
        success: function(data) {
            $.gritter.add({
                title: 'Sucesso!',
                text: data.msg,
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });

        $("#modal_novo_lancamento").hide();
        limpaCamposFormLancaErros()
        pesq_lancamentos_erro_pag();

        },
        error: function(error) {
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });
    loaderModalLancamento.style.display = "none";
});

// Formatação do numero valor
inputValorErroPagamento = document.getElementById('input_valor_lancamento')
inputValorErroPagamento.addEventListener('change', e => {
    e.currentTarget.value = parseFloat(e.currentTarget.value).toFixed(2)
  })

function limpaCamposFormLancaErros(){
    $("#geg_ep_colaborador_erro").val('default')
    $("#geg_ep_colaborador_erro").selectpicker('refresh')

    $("#geg_ep_verba_lancamento").val('default')
    $("#geg_ep_verba_lancamento").selectpicker('refresh')


    inputValorErroPagamento.value = ''

    inputCompetencia.value = yearMonth;
    inputDataPrazo.value = dataCompleta;
    inputDuvida.value = ''
    inputAcao.value = ''
    inputObs.value = ''
}

// * Scripts referentes ao povoamento da tabela da pagina inicial.
$('#form_pesquisa_lancamentos_tabela').submit(function(event) {
    event.preventDefault();
    pesq_lancamentos_erro_pag();


});






$(document).on('click','button', function(){
	var nomeDoButton = $(this).attr('name');
    var idDoButton = $(this).attr('id');
    var valButton = $(this).attr('value');

    if ( nomeDoButton == 'btnEditaRegErroPagamento' ) {
        var varCodRegErroPag = valButton;
        loader_erro_pag.style.display = "flex";
        $.ajax({
            type:"GET",
            url: '/gente_gestao_erros_pagamento_app/retorna_registro_erros_pagamento',
            dataType: 'json',
            data: {
                'cod_erro_pag'     :   varCodRegErroPag
            },
            success: function (data) {

                $('#geg_ep_colaborador_erro').val(data.obj_erro_pagamento.cod_colaborador_senior);
                $('#geg_ep_colaborador_erro').selectpicker('refresh');

                $("#geg_ep_verba_lancamento").val(data.obj_erro_pagamento.cod_verba);
                $("#geg_ep_verba_lancamento").selectpicker('refresh');

                $("#input_valor_lancamento").val(parseFloat(data.obj_erro_pagamento.valor_erro));

                if(data.obj_erro_pagamento.status == 1){
                    $("#chk_resolvido").prop('checked', true);
                } else {
                    $("#chk_resolvido").prop('checked', false);
                }
                let let_comp = data.obj_erro_pagamento.mes_competencia.split('-')[0] + '-' +
                    data.obj_erro_pagamento.mes_competencia.split('-')[1];
                $("#competencia_lancamento").val(let_comp);
                $("#prazo_lancamento").val(data.obj_erro_pagamento.prazo);

                $("#txt_responsavel").val(data.obj_erro_pagamento.nome_responsavel);
                $("#text_area_duvida").val(data.obj_erro_pagamento.duvida);
                $("#text_area_acao").val(data.obj_erro_pagamento.acao);
                $("#text_area_obs").val(data.obj_erro_pagamento.obs);

                var varCompButtonAtualizaErroPag =
                    `<i class="fa-solid fa-check"></i>
                            <span>Atualializar dados</span>`;
                $("#btn_modal_registra_erro_pagamento").html(varCompButtonAtualizaErroPag);
                $("#btn_modal_registra_erro_pagamento").val(data.obj_erro_pagamento.cod_erro_pagamento);
                loader_erro_pag.style.display = "none";
                $("#modal_novo_lancamento").show();

            },
            error: function (request, status, error) {
                loader_erro_pag.style.display = "none";
                $.gritter.add({
                    title: 'Erro!',
                    text: "Por gentileza contate o adm.",
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
          }
        });

    }
    else if ( nomeDoButton == 'btnModalExcluirRegErroPagamento' ) {
        $("#textFieldMotivoEstornoLancErrosPagamento").val("");
        $("#hiddenCodRegErroPag").val(valButton);
        $("#modal_confirma_exclusao_erro_pagamento").show();
    }
    else if ( nomeDoButton == "btnEstornaErroPag") {
         var varCodRegErroPag = $("#hiddenCodRegErroPag").val();
         var varMotivoEstorno = $("#textFieldMotivoEstornoLancErrosPagamento").val();

         if ( varMotivoEstorno == '') {
            $.gritter.add({
                title: 'Atenção!',
                text: "Informe o motivo do Estorno!",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });

         } else {
            $.ajax({
                type:"POST",
                url:'/gente_gestao_erros_pagamento_app/estorna_registro_erros_pagamento',
                data: {
                    'cod_reg_erro_pag'       :   varCodRegErroPag,
                    'desc_motivo_estorno'    :   varMotivoEstorno
                  },
                success: function(data){
                    $("#modal_confirma_exclusao_erro_pagamento").hide();
                    $.gritter.add({
                        title: 'Anteção!',
                        text: data.msg,
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });
                    pesq_lancamentos_erro_pag();

                    //$("#tabCadPlacaTerceitos").DataTable().clear().draw();

                },
                error: function (request, status, error) {
                    $.gritter.add({
                        title: 'Erro!',
                        text: "Por gentileza contate o adm.",
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: '',
                    });

                }
            });
         }
    }

});


function povoa_comp_colaboradores_by_filial(cod_filal){

    $.ajax({
        type: "GET",
        url: "/gente_gestao_erros_pagamento_app/lancamento_erros_pagamento",
        data: {
            busca:"colaboradores",
            id_filial: cod_filal,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
            $("#geg_ep_colaborador_erro option").remove();
            data.lista_colaboradores.forEach((colaborador) =>{
                $("#geg_ep_colaborador_erro").append(
                    `<option value="${colaborador.cod_colab}">${colaborador.nome_colab} - ${colaborador.status_colab} - ${colaborador.cod_colab}</option>`);
            })
            $('#geg_ep_colaborador_erro').selectpicker('refresh');
        },
        error: function(error) {

            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });
}


function pesq_lancamentos_erro_pag(){
    selectFilial = document.getElementById('geg_ep_pesquisa_filial')

    filialPesquisada = selectFilial.value
    competenciaPesquisada = competenciaPesquisa.value
    loader_erro_pag.style.display = "flex";
    $.ajax({
        type: "GET",
        url: "/gente_gestao_erros_pagamento_app/tabela",
        data: {
            'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
            'filialPesquisada': filialPesquisada,
            'competenciaPesquisada': competenciaPesquisada,
        },
        success: function(data) {

            let let_linhas_erros_pagamento = [];
            data.linhas_tabela.forEach( linha => {
                let data_admissao = linha.admissao
                let partes = data_admissao.split("-");
                let ano = partes[0];
                let dia = partes[2];
                let mes = partes[1];
                let admissaoFormatada = `${dia}/${mes}/${ano}`;

                let data_prazo = linha.prazo
                partes = data_prazo.split("-");
                ano = partes[0];
                dia = partes[2];
                mes = partes[1];
                let prazoFormatado = `${dia}/${mes}/${ano}`;

                if(linha.status == 1){
                    status_registro = 'OK'
                }else{
                    status_registro = 'NOK'
                }

                var varBotaoEditarRegistro = "<button type='button' name='btnEditaRegErroPagamento'"+
                    "id='btnEditaRegErroPagamento"+linha.cod_erro_pagamento+"' class='btn btn-rounded btn-space' "+
                    "value='"+linha.cod_erro_pagamento+"' title='Editar registro'><i class='fa-solid fa-pen-to-square' style='color:#f46424;'></i></button>";

                var varBotaoExcluirRegistro = "<button type='button' name='btnModalExcluirRegErroPagamento'"+
                    "id='btnModalExcluirRegErroPagamento"+linha.cod_erro_pagamento+"' class='btn btn-rounded btn-space' "+
                    "value='"+linha.cod_erro_pagamento+"' title='Exluir registro'><i class='fa-solid fa-trash-can' style='color:#f46424;'></i></button>";
                if (status.status == 'E') {
                    varBotaoExcluirRegistro = `<i class="fa-solid fa-ban" style="color:#f46424;"></i>`;
                    varBotaoEditarRegistro = `<i class="fa-solid fa-ban" style="color:#f46424;"></i>`;
                }

                let let_linha = [
                    linha.nome,
                    linha.cargo,
                    admissaoFormatada,
                    linha.verba,
                    linha.valor,
                    linha.duvida,
                    linha.acao,
                    linha.responsavel,
                    prazoFormatado,
                    linha.obs,
                    status_registro,
                    varBotaoEditarRegistro,
                    varBotaoExcluirRegistro,
                ];
                let_linhas_erros_pagamento.push(let_linha);
            });

            let dataOriginal = "yyyy-dd-mm"; // Substitua essa string pela sua data no formato "yyyy-dd-mm"

            let partes = dataOriginal.split("-"); // Divide a string em três partes: ano, dia e mês

            let ano = partes[0];
            let dia = partes[2];
            let mes = partes[1];

            let dataFormatada = `${dia}/${mes}/${ano}`;

            $('#table_erros_pagamento').DataTable( {
                "bJQueryUI": true,
                "destroy": true,
                "fixedHeader": true,
                "scrollY": "50vh", //770px
                "scrollX": true,
                "scrollCollapse": true,
                "paging": false,
                //"pageLength": 7,
                "searching": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_linhas_erros_pagamento,
                "columns": [
                    { title: "Colaborador" },
                    { title: "Função" },
                    { title: "Admissão" },
                    { title: "Verba" },
                    { title: "Valor" },
                    { title: "Dúvida" },
                    { title: "Ação" },
                    { title: "Responsável" },
                    { title: "Prazo" },
                    { title: "OBS" },
                    { title: "Status" },
                    { title: "Editar" },
                    { title: "Excluir" },
                ],
                "columnDefs": [
                    // { "width": "10%", "targets": 0 },
                    // {"className": "dt-left", "targets": [0]},
                    // {"className": "dt-left", "targets": [1]}
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
            loader_erro_pag.style.display = "none";
        },
        error: function(error) {
            loader_erro_pag.style.display = "none";
            $.gritter.add({
                title: 'Erro!',
                text: "Por gentileza contate o adm.",
                image: '/static/icons/triangle-exclamation-solid.svg',
                sticky: false,
                time: '',
            });
        }
    });

}