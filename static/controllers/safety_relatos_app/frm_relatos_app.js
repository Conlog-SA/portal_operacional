$(document).on('click','.clickable' , function(){
    let URL = $(this).attr("value");
    window.open(URL,'_blank','','');
});

$(document).on('change','#unidade',function(){

    $('#nome_relatado option').remove();

    $('#nome_relatado').prop('disabled',true);
    $('#nome_relatado').selectpicker('refresh');
    $('#situacao_envolvido').prop('disabled',false);
    $('#situacao_envolvido').val('');
    $('#situacao_envolvido').selectpicker('refresh');


});

$(document).on('click','.create-check-relatos' , function(){
    let let_unidade_relato = $('#unidade').val();
    let let_tipo_relato = $('#tipo_relato').val();
    let let_local_relato = $('#local_relato').val();
    let let_atividade_relato = $('#atividade_relato').val();
    let let_processo_relato = $('#processo_relato').val();
    let let_descricao_situacao = $('#descricao_situacao').val();
    let let_categoria_ato_inseguro = $('#ato_inseguro_categoria').val();
    let let_categoria_condicao_insegura = $('#condicao_insegura_categoria').val();
    let let_nome_relatado = "";
    let let_situacao_envolvido = "";

    if (let_tipo_relato != '2') {
        let_situacao_envolvido = $('#situacao_envolvido').val();
        if (let_situacao_envolvido == '1') {
            let_nome_relatado = $('#nome_relatado').val();
        }
        else if (let_situacao_envolvido == '2' || let_situacao_envolvido == '3' || let_situacao_envolvido == '4') {
            let_nome_relatado = $('#nome_relatado_terceiro').val();
        }
    } else {
        let_situacao_envolvido = null;
        let_nome_relatado = '';
    }

    msg_erro = '';
    if (let_unidade_relato == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_tipo_relato == '') {
        msg_erro += 'Selecione um tipo de relato!<br>';
    }
    if (let_categoria_ato_inseguro == '' && let_tipo_relato == '1') {
        msg_erro += 'Selecione uma categoria de ato inseguro!<br>';
    }
    if (let_categoria_condicao_insegura == '' && let_tipo_relato == '2') {
        msg_erro += 'Selecione uma categoria de condição insegura!<br>';
    }
    if ((let_situacao_envolvido == '' || let_situacao_envolvido == null) && let_tipo_relato != '2') {
        msg_erro += 'Informe a situação do relatado!<br>';
    }
    if ((let_nome_relatado == '' || let_nome_relatado == null) && let_tipo_relato != '2') {
        msg_erro += 'Informe o nome do relatado!<br>';
    }
    if (let_local_relato == '') {
        msg_erro += 'Informe o local do relato!<br>';
    }
    if (let_processo_relato == '' || let_processo_relato == null) {
        msg_erro += 'Informe o processo do relato!<br>';
    }
    if (let_atividade_relato == '' || let_atividade_relato == null) {
        msg_erro += 'Informe a atividade do relato!<br>';
    }
    /*if (let_descricao_situacao.length <= 299) {
        msg_erro += 'Descreva a situação (min. 300 caracteres)';
    }*/
    console.log(msg_erro);
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_relatos_app/relatos_check',
            data: {
                'unidade_relato'   :   let_unidade_relato,
                'tipo_relato'   :   let_tipo_relato,
                'situacao_envolvido'   :   let_situacao_envolvido,
                'nome_relatado'   :   let_nome_relatado,
                'local_relato'   :   let_local_relato,
                'processo_relato' : let_processo_relato,
                'atividade_relato' : let_atividade_relato,
                'categoria_ato_inseguro' : let_categoria_ato_inseguro,
                'categoria_condicao_insegura' : let_categoria_condicao_insegura
            },
            success: function (dados) {
                $("#div_corpo_relatos").html(dados);
                $("#div_corpo_relatos").css('background-color', 'rgba(0,0,0,0)')
            },
            error: function (xhr, status, error) {
                 $.gritter.add({
                    title: 'Erro!',
                    text: xhr.responseText,
                    image: '/static/icons/triangle-exclamation-solid.svg',
                    sticky: false,
                    time: '',
                });
            }
        });
    } else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }
});

$(document).on('change','#situacao_envolvido',function(){
    let let_cod_unidade = $('#unidade').val();
    if (let_cod_unidade != '') {
        if ($(this).val() == '1') {
            $.ajax({
                type: 'GET',
                url: '/safety_login_colaboradores_app/lista_colaboradores',
                data: {
                    'cod_unidade'   :   let_cod_unidade,
                    'tipo_check'    :   '2'
                },
                dataType: 'json',
                success: function (dados) {
                    console.log(dados);
                    $('#nome_relatado option').remove();
                    dados.lista_colaboradores.forEach(operacao => {
                        $("#nome_relatado").append("<option value='"+
                        operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                    });
                    if ($('#nome_relatado option').length == 0) {
                        $('#situacao_envolvido').val("4");
                        $('#situacao_envolvido').selectpicker('refresh');
                        $('#situacao_envolvido').trigger('change');

                        $.gritter.add({
                            title: 'Erro!',
                            text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    } else {
                        $('#nome_relatado').prop('disabled',false);
                        $('#div_relatado').removeClass('hidden-div');
                        $('#nome_relatado').selectpicker('refresh');
                        $('#div_relatado_terceiro').addClass('hidden-div');
                        $('#nome_relatado_terceiro').val('');
                    };
                }
            });
        }
    }
    else {
        $('#situacao_envolvido').val('');
        $('#situacao_envolvido').selectpicker('refresh');

        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a unidade primeiro!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

    if ($(this).val() == '2' || $(this).val() == '3' || $(this).val() == '4') {
        $('#div_relatado_terceiro').removeClass('hidden-div');
        $('#div_relatado').addClass('hidden-div');
        $('#nome_relatado').val('');
        $('#nome_relatado').selectpicker('refresh');
    }


});

$(document).on('change','#processo_relato',function(){
    let cod_processo = $(this).val();
    $.ajax({
        type: 'GET',
        url: '/safety_relatos_app/lista_atividades',
        data: {
            'cod_processo'   :   cod_processo,
        },
        dataType: 'json',
        success: function (dados) {
            $('#atividade_relato option').remove();
            dados.lista_atividades.forEach(atividade => {
                $("#atividade_relato").append("<option value='"+
                atividade.cod_atividade+"'>"+atividade.desc_atividade+"</option>");
            });

            $('#atividade_relato').prop('disabled',false);
            $('#atividade_relato').selectpicker('refresh');
        }
    });

});

$(document).on('change','#tipo_relato',function(){

    if ($(this).val() == 1) {
        $('#div_ato_inseguro_categorias').removeClass('hidden-div');
        $('#div_relatado').removeClass('hidden-div');
        $('#div_situacao_relatado').removeClass('hidden-div');
        $('#div_condicao_insegura_categorias').addClass('hidden-div');
        $('#condicao_insegura_categoria').val('');
        $('#condicao_insegura_categoria').selectpicker('refresh');

    }
    else if ($(this).val() == 2) {
        $('#div_condicao_insegura_categorias').removeClass('hidden-div');
        $('#div_ato_inseguro_categorias').addClass('hidden-div');
        $('#div_situacao_relatado').addClass('hidden-div');
        $('#div_relatado').addClass('hidden-div');
        $('#situacao_envolvido').val('');
        $('#situacao_envolvido').selectpicker('refresh');
        $('#nome_relatado').val('');
        $('#nome_relatado').selectpicker('refresh');
        $('#nome_relatado_terceiro').val('');
        $('#nome_relatado_terceiro').selectpicker('refresh');
        $('#ato_inseguro_categoria').val('');
        $('#ato_inseguro_categoria').selectpicker('refresh');
    }
    else {
        $('#ato_inseguro_categoria').val('');
        $('#ato_inseguro_categoria').selectpicker('refresh');
        $('#div_situacao_relatado').removeClass('hidden-div');
        $('#div_relatado').removeClass('hidden-div');
        $('#div_ato_inseguro_categorias').addClass('hidden-div');
        $('#div_condicao_insegura_categorias').addClass('hidden-div');
        $('#condicao_insegura_categoria').val('');
        $('#condicao_insegura_categoria').selectpicker('refresh');
        $('#ato_inseguro_categoria').val('');
        $('#ato_inseguro_categoria').selectpicker('refresh');
    }

});
