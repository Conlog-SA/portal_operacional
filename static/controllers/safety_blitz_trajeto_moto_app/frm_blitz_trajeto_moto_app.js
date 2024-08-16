$(document).on('click','.create-check-blitz-trajeto-moto' , function(){
    let let_unidade_avaliado_moto = $('#unidade_colaborador_moto').val();
    let let_situacao_avaliado_moto = $('#situacao_avaliado_moto').val();
    let let_placa_moto = $('#placa_moto').val();
    let let_nome_relatado = "";

    if (let_situacao_avaliado_moto == '1') {
        let_nome_avaliado_moto = $('#nome_avaliado_moto').val();
    }
    else if (let_situacao_avaliado_moto == '2' || let_situacao_avaliado_moto == '3' || let_situacao_avaliado_moto == '4') {
        let_nome_avaliado_moto = $('#nome_avaliado_terceiro').val();
    }

    msg_erro = '';
    if (let_unidade_avaliado_moto == '') {
        msg_erro += 'Selecione uma filial!<br>';
    }
    if (let_situacao_avaliado_moto == '') {
        msg_erro += 'Informe a situação do avaliado!<br>';
    }
    if (let_nome_avaliado_moto == '') {
        msg_erro += 'Informe o nome do avaliado!<br>';
    }
    if (let_placa_moto == '') {
        msg_erro += 'Informe a placa do moto!';
    }
    if (msg_erro == '') {
        $.ajax({
            type: 'POST',
            url: '/safety_blitz_trajeto_moto_app/blitz_trajeto_moto_check',
            data: {
                'unidade_avaliado'   :   let_unidade_avaliado_moto,
                'situacao_avaliado'  :  let_situacao_avaliado_moto,
                'nome_avaliado'   :   let_nome_avaliado_moto,
                'placa_moto'   :   let_placa_moto
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

$(document).on('change','#situacao_avaliado_moto',function(){
    let let_cod_unidade = $('#unidade_colaborador_moto').val();
    if (let_cod_unidade != '') {
        if ($(this).val() == '1') {
            $.ajax({
                type: 'GET',
                url: '/safety_login_colaboradores_app/lista_colaboradores',
                data: {
                    'cod_unidade'   :   let_cod_unidade,
                    'tipo_check'    :   '4'
                },
                dataType: 'json',
                success: function (dados) {
                    console.log(dados);
                    $('#nome_avaliado_moto option').remove();
                    dados.lista_colaboradores.forEach(operacao => {
                        $("#nome_avaliado_moto").append("<option value='"+
                        operacao.cod_colaborador+"'>"+operacao.nome_colaborador+" (" + operacao.desc_cargo+")</option>");
                    });
                    if ($('#nome_avaliado_moto option').length == 0) {
                        $('#situacao_avaliado_moto').val("4");
                        $('#situacao_avaliado_moto').selectpicker('refresh');
                        $('#situacao_avaliado_moto').trigger('change');

                        $.gritter.add({
                            title: 'Erro!',
                            text: 'Não foram encontrados colaboradores para a unidade selecionada!',
                            image: '/static/icons/triangle-exclamation-solid.svg',
                            sticky: false,
                            time: '',
                        });
                    } else {
                        $('#nome_avaliado_moto').prop('disabled',false);
                        $('#div_avaliado_moto').removeClass('hidden-div');
                        $('#nome_avaliado_moto').selectpicker('refresh');
                        $('#div_avaliado_terceiro_moto').addClass('hidden-div');
                        $('#nome_avaliado_terceiro_moto').val('');
                    };
                }
            });
        }
    }
    else {
        $('#situacao_avaliado_moto').val('');
        $('#situacao_avaliado_moto').selectpicker('refresh');

        $.gritter.add({
            title: 'Atenção!',
            text: 'Selecione a unidade primeiro!',
            image: '/static/icons/triangle-exclamation-solid.svg',
            sticky: false,
            time: '',
        });
    }

    if ($(this).val() == '2' || $(this).val() == '3' || $(this).val() == '4') {
        $('#div_avaliado_terceiro_moto').removeClass('hidden-div');
        $('#div_avaliado_moto').addClass('hidden-div');
        $('#nome_avaliado_moto').val('');
        $('#nome_avaliado_moto').selectpicker('refresh');
    }


});
