var date = new Date();
document.getElementById('geg_input_data_ocorrencia').valueAsDate = new Date();


$(document).on('click','button', function(){
    let let_value_btn = $(this).attr('value');
    let let_id_btn = $(this).attr('id');
    let let_name_btn = $(this).attr('name');

    if (let_name_btn == 'btn_desativa_ocorrencia'){
        let let_cod_punicao = $(let_value_btn).val();
        let let_motivo_cancela_punicão = $('#input_desc_desativacao').val();


        if (let_cod_punicao ==! 0){
            $.ajax({
                type : 'POST',
                url : '/gente_gestao_fluxo_punitivo/tabela_fluxos/' ,
                data: {
                    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                    cod_punicao : let_cod_punicao,
                    motivo_desativacao : let_motivo_cancela_punicão
                },
                success: function(data){
                    $.gritter.add({
                        title: "sucesso! Punição Cancelada",
                        text: data.msg,
                        image : '/static/icons/sucess_icon.svg',
                        sticky: false,
                        time: new Date().toLocaleTimeString(),
                    });
                },
                    error: function(error) {
                    $.gritter.add({
                        title: 'Erro!',
                        text: "Por gentileza contate o adm.",
                        image: '/static/icons/triangle-exclamation-solid.svg',
                        sticky: false,
                        time: new Date().toLocaleTimeString(),
                    });
                }
            });
        }
    }
});

selectFilial = document.getElementById('geg_select_filial')
selectFilial.addEventListener('change', function() {
    id_filial = selectFilial.value

    $.ajax({
        type: "GET",
        url: "/gente_gestao_fluxo_punitivo/listar_colaboradores",
        data: {
            id_filial: id_filial,
            infoBuscada: 'lista_colabs',
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
            let options_colaboradores = ""

            data.lista_colaboradores.forEach((colaborador) =>{
                options_colaboradores += `<option value="${colaborador.cod_colab}">${colaborador.nome_colab} - ${colaborador.status_colab} - ${colaborador.cod_colab}</option>`
            })

            $('#geg_select_colab').html(options_colaboradores)
            $('#geg_select_colab').selectpicker('refresh')
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
})

selectColab = document.getElementById('geg_select_colab')
selectColab.addEventListener('change', function() {

    idColab = selectColab.value

    $.ajax({
        type: "GET",
        url: "/gente_gestao_fluxo_punitivo/listar_colaboradores",
        data: {
            idColab: idColab,
            infoBuscada: 'dados_colab',
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
            dataAdmissao = new Date(data.dados_colab[0].data_admissao_colab)
            var dia = dataAdmissao.getDate();
            var mes = dataAdmissao.getMonth() + 1;
            var ano = dataAdmissao.getFullYear();
            var dataAdmissaoFormatada = dia.toString().padStart(2, '0') + '/' + mes.toString().padStart(2, '0') + '/' + ano.toString();

            $('#cardDados_nome').html(`<b>${data.dados_colab[0].nome_colab}</b>`)
            $('#cardDados_cargo').html(data.dados_colab[0].desc_cargo_colab)
            $('#cardDados_cpf').html(data.dados_colab[0].cpf_colab)
            $('#cardDados_admissao').html(dataAdmissaoFormatada)
            $('#cardDados_matricula').html(data.dados_colab[0].matricula_colab)
            $('#cardDados_situacao').html(data.dados_colab[0].situacao_colab)
        
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
})

// * Verificação do tipo de penalidade (se for suspensão, requer preenchimento do campo geg_input_dias_suspensao)
selectTipoPenalidade = document.getElementById('geg_select_penalidade')
selectTipoPenalidade.addEventListener('change', function(){
    tipoPenalidade = selectTipoPenalidade.value
    console.log('teste')
    // Se for suspensão:
    if(tipoPenalidade == "S"){
        inputDiasSuspensao = document.getElementById('geg_input_dias_suspensao')
        inputDiasSuspensao.setAttribute("required", "true")
        inputDiasSuspensao.removeAttribute("disabled")
    }
    else{
        inputDiasSuspensao = document.getElementById('geg_input_dias_suspensao')
        inputDiasSuspensao.value = 0;
        inputDiasSuspensao.setAttribute("disabled", "true")
        inputDiasSuspensao.removeAttribute("required")
    }
})



function limpaFormulario(){
    $('#cardDados_nome').html(`<b>Colaborador</b>`)
    $('#cardDados_cargo').html('Cargo')
    $('#cardDados_cpf').html('')
    $('#cardDados_admissao').html('')
    $('#cardDados_matricula').html('')
    $('#cardDados_situacao').html('')
    
    $("#geg_select_filial").val('default')
    $("#geg_select_filial").selectpicker('refresh')
    
    $("#geg_select_colab").val('default')
    $("#geg_select_colab").selectpicker('refresh')
    
    $("#geg_select_penalidade").val('default')
    $("#geg_select_penalidade").selectpicker('refresh')
    
    $("#geg_select_motivo_juridico").val('default')
    $("#geg_select_motivo_juridico").selectpicker('refresh')
    
    $("#geg_select_motivo_especifico").val('default')
    $("#geg_select_motivo_especifico").selectpicker('refresh')

    inputDiasSuspensao = document.getElementById('geg_input_dias_suspensao')
    inputDiasSuspensao.value = 0;
    
    var date = new Date();
    document.getElementById('geg_input_data_ocorrencia').valueAsDate = new Date();

    text_area_desc_punicao = document.getElementById('text_area_desc_punicao')
    text_area_obs_punicao = document.getElementById('text_area_obs_punicao')

    text_area_desc_punicao.value = ''
    text_area_obs_punicao.value = ''

    var date = new Date();
    var competenciaPesquisa = document.getElementById('competencia_pesquisa');
    var month_atual = ("0" + (date.getMonth() + 1)).slice(-2);
    var year_atual = date.getFullYear();
    var yearMonth = `${year_atual}-${month_atual}`;

inputCompetencia = document.getElementById('competencia_pesquisa_fluxo_punitivo')
inputCompetencia.value = yearMonth
}


//Criação de Desativação de Fluxo de Punição
$(document).ready(function() {
    btnModalCadDesativaFluxo = document.getElementById('btn_desativa_ocorrencia');
    btnModalCadDesativaFluxo.addEventListener('click', function(){
        $("#modal_desativa_punicao").show();

        btnFechaModalDesativaFluxo = document.getElementById('btn_fecha_modal_desativa_fluxo');
        btnCancelaModalDesativaFluxo = document.getElementById('btn_cancela_modal_desativa_fluxo');
        
        btnFechaModalDesativaFluxo.addEventListener('click', function() {
            $("#modal_desativa_punicao").hide();
        })
        btnCancelaModalDesativaFluxo.addEventListener('click', function() {
            $("#modal_desativa_punicao").hide();
        })    
    });
});

// * Criação de novo motivo jurídico
btnModalCadMotJuridico = document.getElementById('btn_cad_mot_juridico');
btnModalCadMotJuridico.addEventListener('click', function() {
    $("#modal_mot_juridico").show();
    
    // botoes para fecha modal
    btnFechaModalCadMotJuridico = document.getElementById('btn_fecha_modal_mot_juridico');
    btnCancelaModalCadMotJuridico = document.getElementById('btn_cancela_modal_mot_juridico');
    btnFechaModalCadMotJuridico.addEventListener('click', function() {
        $("#modal_mot_juridico").hide();
    })
    btnCancelaModalCadMotJuridico.addEventListener('click', function() {
        $("#modal_mot_juridico").hide();
    })    
})

inputNovoMotivoJuridico = document.getElementById('input_desc_mot_juridico');
btnRegistraNovoMotivoJuridico = document.getElementById('btn_modal_cria_novo_mot_juridico');
btnRegistraNovoMotivoJuridico.addEventListener('click', function() {
    if(inputNovoMotivoJuridico.value != ''){
        btnCancelaModalCadMotJuridico.setAttribute("disabled", true);
        btnFechaModalCadMotJuridico.setAttribute("disabled", true);
        btnRegistraNovoMotivoJuridico.setAttribute("disabled", true);

        $.ajax({
            type: "POST",
            url: "/gente_gestao_fluxo_punitivo/cria_motivo",
            data: {
                novo_motivo: inputNovoMotivoJuridico.value,
                tipo_motivo: 'juridico',
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(data) {
                $.gritter.add({
                    title: 'Sucesso!',
                    text: "Novo motivo criado com sucesso!",
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
        inputNovoMotivoJuridico.value = "";
        
        btnCancelaModalCadMotJuridico.removeAttribute("disabled");
        btnFechaModalCadMotJuridico.removeAttribute("disabled");
        btnRegistraNovoMotivoJuridico.removeAttribute("disabled");
        
        $("#modal_mot_juridico").hide();
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

// * Criação de novo motivo especifico
btnModalCadMotEspecifico = document.getElementById('btn_cad_motivo_especifico');
btnModalCadMotEspecifico.addEventListener('click', function() {
    $("#modal_mot_especifico").show();
    
    // botoes para fecha modal
    btnFechaModalCadMotEspecifico = document.getElementById('btn_fecha_modal_mot_especifico');
    btnCancelaModalCadEspecifico = document.getElementById('btn_cancela_modal_mot_especifico');
    btnFechaModalCadMotEspecifico.addEventListener('click', function() {
        $("#modal_mot_especifico").hide();
    })
    btnCancelaModalCadEspecifico.addEventListener('click', function() {
        $("#modal_mot_especifico").hide();
    })    
})

inputNovoMotivoEspecifico = document.getElementById('input_desc_mot_especifico');
btnRegistraNovoMotivoEspecifico = document.getElementById('btn_modal_cria_novo_mot_especifico');
btnRegistraNovoMotivoEspecifico.addEventListener('click', function() {
    if(inputNovoMotivoEspecifico.value != ''){
        btnCancelaModalCadEspecifico.setAttribute("disabled", true);
        btnFechaModalCadMotEspecifico.setAttribute("disabled", true);
        btnRegistraNovoMotivoEspecifico.setAttribute("disabled", true);

        $.ajax({
            type: "POST",
            url: "/gente_gestao_fluxo_punitivo/cria_motivo",
            data: {
                novo_motivo: inputNovoMotivoEspecifico.value,
                tipo_motivo: 'especifico',
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(data) {
                $.gritter.add({
                    title: 'Sucesso!',
                    text: "Novo motivo criado com sucesso!",
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
        inputNovoMotivoEspecifico.value = "";
        
        btnCancelaModalCadEspecifico.removeAttribute("disabled");
        btnFechaModalCadMotEspecifico.removeAttribute("disabled");
        btnRegistraNovoMotivoEspecifico.removeAttribute("disabled");
        
        $("#modal_mot_especifico").hide();
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


// * Botão registra novo lançamento de fluxo punitivo
$('#form_cadastra_fluxo_punitivo').submit(function(event) {
    event.preventDefault();
    loaderLancamento = document.getElementById('loader_lancamento')
    loaderLancamento.style.display = "flex";
    
    selectFilial = document.getElementById('geg_select_filial')
    selectColaborador = document.getElementById('geg_select_colab')
    selectPenalidade = document.getElementById('geg_select_penalidade')
    selectMotivoJuridico = document.getElementById('geg_select_motivo_juridico')
    selectMotivoEspecifico = document.getElementById('geg_select_motivo_especifico')
    dataOcorrencia = document.getElementById('geg_input_data_ocorrencia')
    textOcorrencia = document.getElementById('text_area_desc_punicao')
    textObs = document.getElementById('text_area_obs_punicao')
    inputDiasSuspensao = document.getElementById('geg_input_dias_suspensao')
    colabResponsavel = document.getElementById('geg_input_colab_lancamento')
    
    
    idFilialSelecionada = selectFilial.value
    codSeniorColaborador = selectColaborador.value
    codPenalidade = selectPenalidade.value
    codMotivoJuridico = selectMotivoJuridico.value
    codMotivoEspecifico = selectMotivoEspecifico.value
    dataOcorrencia = dataOcorrencia.value
    textOcorrencia = textOcorrencia.value
    textObs = textObs.value
    diasSuspensao = inputDiasSuspensao.value
    
    $.ajax({
        type: "POST",
        url: "/gente_gestao_fluxo_punitivo/fluxo_punitivo",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            'idFilialSelecionada':idFilialSelecionada,
            'codSeniorColaborador':codSeniorColaborador,
            'codPenalidade':codPenalidade,
            'codMotivoJuridico':codMotivoJuridico,
            'codMotivoEspecifico': codMotivoEspecifico,
            'dataOcorrencia':dataOcorrencia,
            'textOcorrencia':textOcorrencia,
            'textObs':textObs,
            'diasSuspensao':diasSuspensao
        },
        success: function(data) {
            $.gritter.add({
                title: 'Sucesso!',
                text: "Lançamento registrado com sucesso!",
                image: '/static/icons/sucess_icon.svg',
                sticky: false,
                time: '',
            });
            limpaFormulario()
            
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
    loaderLancamento.style.display = "none";
});

// * Botão pesquisa fluxos lançados
$('#form_pesquisa_fluxo_punitivo_tabela').submit(function(event) {
    event.preventDefault();

    filialPesquisada = document.getElementById('geg_fluxo_punitivo_pesquisa_filial').value
    competenciaPesquisa = document.getElementById('competencia_pesquisa_fluxo_punitivo').value

    $.ajax({
        type: "GET",
        url: "/gente_gestao_fluxo_punitivo/tabela_fluxos",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            filialPesquisada: filialPesquisada,
            competenciaPesquisa: competenciaPesquisa
            
        },
        success: function(data) {
            console.log(data.linhas_tabela)

            let let_linhas_fluxo_punitivo = [];
            data.linhas_tabela.forEach( linha => {
                    let let_linha = [
                        linha.matricula,
                        linha.nome_colab,
                        linha.cargo,
                        linha.data_ocorrencia,
                        linha.motivo_juridico,
                        linha.motivo_especifico,
                        `
                        <button type='button'
                            id="btn_desativa_ocorrencia"
                            name="btn_desativa_ocorrencia"
                            class="btn btn-primary btn-rounded btn-visualizar_anexo"
                            value="${linha.cod_punicao}"
                            title="Desativa Punição" 
                            style="background-color: #f46424; border-color:#f46424;">
                            <i class="fa-solid fa-user-slash"></i>
                        </button>
                        `,
                        linha.cod_punicao,
                    ];

                let_linhas_fluxo_punitivo.push(let_linha);
            });

            $('#table_fluxo_punitivo').DataTable( {
                "bJQueryUI": true,
                "pageLength": 10,
                "destroy": true,
                "dom": 'Bfrtip',
                "buttons": [
                    'copyHtml5'
                ],
                "data":let_linhas_fluxo_punitivo,
                "columns": [
                    { title: "Matrícula" },
                    { title: "Nome" },
                    { title: "Cargo" },
                    { title: "Data Ocorrência" },
                    { title: "Motivo Jurídico" },
                    { title: "Motivo Específico" },
                    { title: "Desativa Punição"}
                ],
                "columnDefs": [
                    {"className": "dt-left", "targets": [0, 1, 2, 3, 4, 5]}, // Aplica classe text-left a todas as colunas
                    {"className": "text-left", "targets": [0, 1, 2, 3, 4, 5]}, // Aplica classe text-left a todas as colunas
                    { "width": "10%", "targets": 0 },
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

});

$( document ).ready(function() {
    limpaFormulario()
});

