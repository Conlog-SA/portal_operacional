$(document).on('click','.create-check-blitz-trajeto-carro' , function(){
    let let_unidade_avaliado = $('#unidade_colaborador').val();
    let let_situacao_avaliado = $('#situacao_avaliado').val();
    let let_placa_carro = $('#placa_carro').val();
    let let_nome_relatado = "";

    if (let_situacao_avaliado == '1') {
        let_nome_avaliado = $('#nome_avaliado').val();
    }
    else if (let_situacao_avaliado == '2' || let_situacao_avaliado == '3' || let_situacao_avaliado == '4') {
        let_nome_avaliado = $('#nome_avaliado_terceiro').val();
    }

    msg_erro = '';
    if (let_unidade_avaliado == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_situacao_avaliado == '') {
        msg_erro += 'Informe a situação do avaliado!<br>';
    }
    if (let_nome_avaliado == '') {
        msg_erro += 'Informe o nome do avaliado!<br>';
    }
    if (let_placa_carro == '') {
        msg_erro += 'Informe a placa do carro!';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_blitz_trajeto_carro_app/blitz_trajeto_carro_check',
            data: {
                'unidade_avaliado'   :   let_unidade_avaliado,
                'situacao_avaliado'  :  let_situacao_avaliado,
                'nome_avaliado'   :   let_nome_avaliado,
                'placa_carro'   :   let_placa_carro
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

$(document).on('change','#situacao_avaliado',function(){
    let let_cod_unidade = $('#unidade_colaborador').val();
    if (let_cod_unidade != '') {
        if ($(this).val() == '1') {
            $.ajax({
                type: 'GET',
                url: '/safety_login_colaboradores_app/lista_colaboradores',
                data: {
                    'cod_unidade'   :   let_cod_unidade,
                    'tipo_check'    :   '3'
                },
                dataType: 'json',
                success: function (dados) {
                    console.log(dados);
                    $('#nome_avaliado option').remove();
                    dados.lista_colaboradores.forEach(operacao => {
                        $("#nome_avaliado").append("<option value='"+
                        operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                    });
                    if ($('#nome_avaliado option').length == 0) {
                        $('#situacao_avaliado').val("4");
                        $('#situacao_avaliado').selectpicker('refresh');
                        $('#situacao_avaliado').trigger('change');

                        $.gritter.add({
                            title: 'Erro!',
                            text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    } else {
                        $('#nome_avaliado').prop('disabled',false);
                        $('#div_avaliado').removeClass('hidden-div');
                        $('#nome_avaliado').selectpicker('refresh');
                        $('#div_avaliado_terceiro').addClass('hidden-div');
                        $('#nome_avaliado_terceiro').val('');
                    };
                }
            });
        }
    }
    else {
        $('#situacao_avaliado').val('');
        $('#situacao_avaliado').selectpicker('refresh');

        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a unidade primeiro!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

    if ($(this).val() == '2' || $(this).val() == '3' || $(this).val() == '4') {
        $('#div_avaliado_terceiro').removeClass('hidden-div');
        $('#div_avaliado').addClass('hidden-div');
        $('#nome_avaliado').val('');
        $('#nome_avaliado').selectpicker('refresh');
    }


});
