$(document).on('change','#unidade_colaborador_bicicleta',function(){

    $('#nome_avaliado_bicicleta option').remove();

    $('#nome_avaliado_bicicleta').prop('disabled',true);
    $('#nome_avaliado_bicicleta').selectpicker('refresh');
    $('#situacao_avaliado_bicicleta').prop('disabled',false);
    $('#situacao_avaliado_bicicleta').val('');
    $('#situacao_avaliado_bicicleta').selectpicker('refresh');

});

$(document).on('click','.create-check-blitz-trajeto-bicicleta' , function(){
    let let_unidade_avaliado_bicicleta = $('#unidade_colaborador_bicicleta').val();
    let let_situacao_avaliado_bicicleta = $('#situacao_avaliado_bicicleta').val();
    let let_nome_relatado = "";

    if (let_situacao_avaliado_bicicleta == '1') {
        let_nome_avaliado_bicicleta = $('#nome_avaliado_bicicleta').val();
    }
    else if (let_situacao_avaliado_bicicleta == '2' || let_situacao_avaliado_bicicleta == '3' || let_situacao_avaliado_bicicleta == '4') {
        let_nome_avaliado_bicicleta = $('#nome_avaliado_terceiro_bicicleta').val();
    }

    msg_erro = '';
    if (let_unidade_avaliado_bicicleta == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_situacao_avaliado_bicicleta == '') {
        msg_erro += 'Informe a situação do avaliado!<br>';
    }
    if (let_nome_avaliado_bicicleta == '') {
        msg_erro += 'Informe o nome do avaliado!<br>';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_blitz_trajeto_bicicleta_app/blitz_trajeto_bicicleta_check',
            data: {
                'unidade_avaliado'   :   let_unidade_avaliado_bicicleta,
                'situacao_avaliado'  :  let_situacao_avaliado_bicicleta,
                'nome_avaliado'   :   let_nome_avaliado_bicicleta,
            },
            success: function (dados) {
                $("#div_corpo_relato_blitz_trajeto").html(dados);
                $("#div_corpo_relato_blitz_trajeto").css('background-color', 'rgba(0,0,0,0)')
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
    }
    else {
        $.gritter.add({
            title: 'Erro!',
            text: msg_erro,
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }
});

$(document).on('change','#situacao_avaliado_bicicleta',function(){
    let let_cod_unidade = $('#unidade_colaborador_bicicleta').val();
    if (let_cod_unidade != '') {
        if ($(this).val() == '1') {
            $.ajax({
                type: 'GET',
                url: '/safety_login_colaboradores_app/lista_colaboradores',
                data: {
                    'cod_unidade'   :   let_cod_unidade,
                    'tipo_check'    :   '6'
                },
                dataType: 'json',
                success: function (dados) {
                    console.log(dados);
                    $('#nome_avaliado_bicicleta option').remove();
                    dados.lista_colaboradores.forEach(operacao => {
                        $("#nome_avaliado_bicicleta").append("<option value='"+
                        operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                    });
                    if ($('#nome_avaliado_bicicleta option').length == 0) {
                        $('#situacao_avaliado_bicicleta').val("4");
                        $('#situacao_avaliado_bicicleta').selectpicker('refresh');
                        $('#situacao_avaliado_bicicleta').trigger('change');

                        $.gritter.add({
                            title: 'Erro!',
                            text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    } else {
                        $('#nome_avaliado_bicicleta').prop('disabled',false);
                        $('#div_avaliado_bicicleta').removeClass('hidden-div');
                        $('#nome_avaliado_bicicleta').selectpicker('refresh');
                        $('#div_avaliado_terceiro_bicicleta').addClass('hidden-div');
                        $('#nome_avaliado_terceiro_bicicleta').val('');
                    };
                }
            });
        }
    }
    else {
        $('#situacao_avaliado_bicicleta').val('');
        $('#situacao_avaliado_bicicleta').selectpicker('refresh');

        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a unidade primeiro!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

    if ($(this).val() == '2' || $(this).val() == '3' || $(this).val() == '4') {
        $('#div_avaliado_terceiro_bicicleta').removeClass('hidden-div');
        $('#div_avaliado_bicicleta').addClass('hidden-div');
        $('#nome_avaliado_bicicleta').val('');
        $('#nome_avaliado_bicicleta').selectpicker('refresh');
    }


});
